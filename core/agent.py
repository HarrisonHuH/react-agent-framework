"""
ReAct Agent 核心实现 - 推理 + 行动的循环逻辑
"""

import json
import re
from typing import Optional, List
from openai import OpenAI

from core.prompt import build_react_prompt
from core.memory import ConversationMemory
from tools import get_all_tools, get_tool


class ReActAgent:
    """ReAct Agent 主类"""

    def __init__(self, api_key: str, model: str = "qwen-turbo", max_iterations: int = 5):
        """
        初始化 ReAct Agent
        
        Args:
            api_key: DashScope API Key
            model: 使用的模型名称
            max_iterations: 最大迭代次数（防止无限循环）
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.model = model
        self.max_iterations = max_iterations
        self.memory = ConversationMemory(max_turns=10)
        self.tools = {tool.name: tool for tool in get_all_tools()}

    def _call_llm(self, prompt: str) -> str:
        """
        调用大语言模型
        
        Args:
            prompt: 提示词
            
        Returns:
            模型生成的文本
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"调用 LLM 失败：{str(e)}")

    def _parse_action(self, text: str) -> Optional[dict]:
        """
        从模型输出中解析 Action
        
        Args:
            text: 模型生成的文本
            
        Returns:
            包含 action_name 和 action_input 的字典，如果没有 Action 则返回 None
        """
        # 匹配 Action 和 Action Input
        action_pattern = r"Action:\s*(.+?)\s*Action Input:\s*(.+?)(?=\n|$)"
        match = re.search(action_pattern, text, re.DOTALL)
        
        if match:
            action_name = match.group(1).strip()
            action_input_str = match.group(2).strip()
            
            # 尝试解析 JSON 输入
            try:
                action_input = json.loads(action_input_str)
            except json.JSONDecodeError:
                # 如果不是标准 JSON，尝试将其转换为字典
                action_input = {"query": action_input_str}
            
            return {
                "action_name": action_name,
                "action_input": action_input
            }
        
        return None

    def _parse_final_answer(self, text: str) -> Optional[str]:
        """
        从模型输出中解析 Final Answer
        
        Args:
            text: 模型生成的文本
            
        Returns:
            Final Answer 的内容，如果没有则返回 None
        """
        final_answer_pattern = r"Final Answer:\s*(.+)"
        match = re.search(final_answer_pattern, text, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        return None

    def _execute_action(self, action_name: str, action_input: dict) -> str:
        """
        执行工具动作
        
        Args:
            action_name: 工具名称
            action_input: 工具输入参数
            
        Returns:
            工具执行结果
        """
        tool = get_tool(action_name)
        
        if not tool:
            return f"错误：未找到工具 '{action_name}'"
        
        try:
            result = tool.run(**action_input)
            return str(result)
        except Exception as e:
            return f"工具执行错误：{str(e)}"

    def _run_react_loop(self, question: str, verbose: bool = False) -> str:
        """
        运行 ReAct 循环
        
        Args:
            question: 用户问题
            verbose: 是否打印详细过程
            
        Returns:
            最终答案
        """
        history = []
        
        for iteration in range(self.max_iterations):
            if verbose:
                print(f"\n--- 迭代 {iteration + 1} ---")
            
            # 构建提示词
            prompt = build_react_prompt(question, history)
            
            # 调用 LLM
            llm_response = self._call_llm(prompt)
            
            if verbose:
                print(f"LLM 响应：\n{llm_response}\n")
            
            # 检查是否有 Final Answer
            final_answer = self._parse_final_answer(llm_response)
            if final_answer:
                if verbose:
                    print(f"✅ 找到最终答案")
                return final_answer
            
            # 解析并执行 Action
            action = self._parse_action(llm_response)
            if action:
                action_name = action["action_name"]
                action_input = action["action_input"]
                
                if verbose:
                    print(f"🔧 执行动作：{action_name}")
                    print(f"📥 输入：{action_input}")
                
                # 执行工具
                observation = self._execute_action(action_name, action_input)
                
                if verbose:
                    print(f"📤 观察结果：{observation}")
                
                # 将这一轮添加到历史
                history.append(f"Thought: {llm_response}")
                history.append(f"Observation: {observation}")
            else:
                # 如果没有解析到 Action，可能是直接回答
                if verbose:
                    print("⚠️ 未解析到 Action，尝试直接使用响应")
                return llm_response
        
        # 达到最大迭代次数
        return "抱歉，我未能在合理的迭代次数内找到答案。请尝试简化问题或提供更多上下文。"

    def chat(self, question: str, verbose: bool = False) -> str:
        """
        与 Agent 对话
        
        Args:
            question: 用户问题
            verbose: 是否打印详细过程
            
        Returns:
            Agent 的回答
        """
        # 添加用户消息到记忆
        self.memory.add_user_message(question)
        
        # 运行 ReAct 循环
        answer = self._run_react_loop(question, verbose)
        
        # 添加助手消息到记忆
        self.memory.add_assistant_message(answer)
        
        return answer

    def clear_memory(self):
        """清空对话记忆"""
        self.memory.clear()