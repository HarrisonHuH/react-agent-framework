"""
测试脚本 - 验证 ReAct Agent 功能
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入工具（确保工具被注册）
from tools import calculator
from tools import file_ops
from tools import search

# 导入 Agent
from core.agent import ReActAgent


def test_basic_chat():
    """测试基本对话功能"""
    print("=" * 60)
    print("测试 1: 基本对话（不需要工具）")
    print("=" * 60)
    
    api_key = os.getenv("DASHSCOPE_API_KEY", "")
    if not api_key:
        print("❌ 错误：请设置 DASHSCOPE_API_KEY 环境变量")
        return
    
    agent = ReActAgent(api_key=api_key, model="qwen-turbo")
    
    question = "你好，请介绍一下你自己"
    print(f"\n👤 问题：{question}\n")
    
    response = agent.chat(question, verbose=True)
    print(f"\n🤖 回答：{response}\n")


def test_calculator():
    """测试计算器工具"""
    print("=" * 60)
    print("测试 2: 使用计算器工具")
    print("=" * 60)
    
    api_key = os.getenv("DASHSCOPE_API_KEY", "")
    if not api_key:
        print("❌ 错误：请设置 DASHSCOPE_API_KEY 环境变量")
        return
    
    agent = ReActAgent(api_key=api_key, model="qwen-turbo")
    
    question = "计算 (15 + 25) * 3 的结果是多少？"
    print(f"\n👤 问题：{question}\n")
    
    response = agent.chat(question, verbose=True)
    print(f"\n🤖 回答：{response}\n")


def test_file_operations():
    """测试文件操作工具"""
    print("=" * 60)
    print("测试 3: 使用文件操作工具")
    print("=" * 60)
    
    api_key = os.getenv("DASHSCOPE_API_KEY", "")
    if not api_key:
        print("❌ 错误：请设置 DASHSCOPE_API_KEY 环境变量")
        return
    
    agent = ReActAgent(api_key=api_key, model="qwen-turbo")
    
    # 先写入文件
    question = "请帮我写一个文件 test_output.txt，内容是 'Hello, ReAct Agent!'"
    print(f"\n👤 问题：{question}\n")
    
    response = agent.chat(question, verbose=True)
    print(f"\n🤖 回答：{response}\n")
    
    # 再读取文件
    question = "请读取 test_output.txt 的内容"
    print(f"\n👤 问题：{question}\n")
    
    response = agent.chat(question, verbose=True)
    print(f"\n🤖 回答：{response}\n")


def test_search():
    """测试搜索工具"""
    print("=" * 60)
    print("测试 4: 使用搜索工具")
    print("=" * 60)
    
    api_key = os.getenv("DASHSCOPE_API_KEY", "")
    if not api_key:
        print("❌ 错误：请设置 DASHSCOPE_API_KEY 环境变量")
        return
    
    agent = ReActAgent(api_key=api_key, model="qwen-turbo")
    
    question = "搜索一下 Python 编程语言的特点"
    print(f"\n👤 问题：{question}\n")
    
    response = agent.chat(question, verbose=True)
    print(f"\n🤖 回答：{response}\n")


if __name__ == "__main__":
    print("\n🧪 开始测试 ReAct Agent\n")
    
    # 运行所有测试
    test_basic_chat()
    test_calculator()
    test_file_operations()
    test_search()
    
    print("\n✅ 所有测试完成！\n")
