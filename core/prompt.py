"""
Prompt 模板系统 - 定义 ReAct Agent 的提示词模板
"""

from tools import get_tools_description


SYSTEM_PROMPT = """你是一个智能助手，使用 ReAct（Reasoning + Acting）模式来解决问题。

你可以使用以下工具来帮助完成任务：
{tools}

请按照以下格式进行思考和行动：

Thought: 思考当前应该做什么
Action: 选择要使用的工具名称
Action Input: 工具的输入参数（JSON 格式）
Observation: 工具执行的结果
...（这个 Thought/Action/Action Input/Observation 可以重复 N 次）
Thought: 我已经知道最终答案
Final Answer: 给出最终答案

重要规则：
1. 每次只能执行一个动作（Action）
2. Action 必须是上述工具列表中的工具名称
3. Action Input 必须是有效的 JSON 格式
4. 在得到 Observation 后，继续思考下一步
5. 当你有足够信息回答问题时，给出 Final Answer
6. 如果不需要使用工具，直接给出 Final Answer

开始！
"""


def build_system_prompt() -> str:
    """构建系统提示词"""
    tools_desc = get_tools_description()
    return SYSTEM_PROMPT.format(tools=tools_desc)


def build_user_prompt(question: str) -> str:
    """构建用户提示词"""
    return f"问题：{question}\n"


def build_react_prompt(question: str, history: list = None) -> str:
    """构建完整的 ReAct 提示词（包含历史对话）"""
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(question)
    
    if history:
        history_str = "\n".join(history)
        full_prompt = f"{system_prompt}\n\n{history_str}\n\n{user_prompt}"
    else:
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
    
    return full_prompt