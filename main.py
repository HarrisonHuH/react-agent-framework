"""
ReAct Agent Framework - 入口文件
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


def main():
    # 获取 API Key
    api_key = os.getenv("DASHSCOPE_API_KEY", "")

    if not api_key:
        print("❌ 错误：请设置 DASHSCOPE_API_KEY 环境变量")
        print("   检查 .env 文件是否正确配置")
        return

    # 创建 Agent
    agent = ReActAgent(
        api_key=api_key,
        model="qwen-turbo"
    )

    print("🤖 ReAct Agent 已就绪！")
    print("可用工具：计算器、文件读写、搜索")
    print("输入 'quit' 退出\n")

    # 交互式对话
    while True:
        try:
            user_input = input("👤 你：").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 再见！")
                break

            if not user_input:
                continue

            # 运行 Agent
            response = agent.chat(user_input, verbose=True)

            print(f"🤖 Agent: {response}\n")

        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误：{str(e)}\n")


if __name__ == "__main__":
    main()