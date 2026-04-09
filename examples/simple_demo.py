"""
简单示例 - 演示如何使用 ReAct Agent
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入工具（确保工具被注册）
from tools import calculator, file_ops, search

# 导入 Agent
from core.agent import ReActAgent


def main():
    # 获取 API Key
    api_key = os.getenv("DASHSCOPE_API_KEY", "")
    
    if not api_key:
        print("❌ 错误：请设置 DASHSCOPE_API_KEY 环境变量")
        return
    
    # 创建 Agent
    agent = ReActAgent(api_key=api_key, model="qwen-turbo")
    
    print("=" * 60)
    print("ReAct Agent 简单示例")
    print("=" * 60)
    
    # 示例 1: 基本对话
    print("\n📝 示例 1: 基本对话")
    print("-" * 60)
    question = "你好！"
    print(f"问: {question}")
    response = agent.chat(question)
    print(f"答: {response}")
    
    # 示例 2: 数学计算
    print("\n📝 示例 2: 数学计算")
    print("-" * 60)
    question = "计算 25 * 48 的结果"
    print(f"问: {question}")
    response = agent.chat(question, verbose=True)
    print(f"答: {response}")
    
    # 示例 3: 文件写入
    print("\n📝 示例 3: 文件写入")
    print("-" * 60)
    question = "请创建一个文件 example.txt，内容是 'Hello, ReAct Agent!'"
    print(f"问: {question}")
    response = agent.chat(question)
    print(f"答: {response}")
    
    # 示例 4: 文件读取
    print("\n📝 示例 4: 文件读取")
    print("-" * 60)
    question = "读取 example.txt 的内容"
    print(f"问: {question}")
    response = agent.chat(question)
    print(f"答: {response}")
    
    # 示例 5: 复杂任务（多步推理）
    print("\n📝 示例 5: 复杂任务")
    print("-" * 60)
    question = "计算 (100 + 200) / 3 的结果，然后把结果保存到 result.txt"
    print(f"问: {question}")
    response = agent.chat(question, verbose=True)
    print(f"答: {response}")
    
    print("\n" + "=" * 60)
    print("✅ 所有示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
