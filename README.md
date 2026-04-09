# ReAct Agent Framework

一个基于 ReAct（Reasoning + Acting）模式的智能体框架，能够结合推理和行动来解决复杂任务。

## 🌟 特性

- 🧠 **智能推理**: 使用 ReAct 模式进行思考和决策
- 🔧 **工具集成**: 内置计算器、文件操作、搜索等工具
- 💭 **记忆管理**: 支持多轮对话和上下文理解
- 🚀 **易于扩展**: 模块化设计，轻松添加新工具
- 📝 **详细日志**: 可查看完整的推理过程

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

在 `.env` 文件中设置您的 DashScope API Key：

```
DASHSCOPE_API_KEY=your_api_key_here
```

### 3. 运行

```bash
# 交互式对话
python main.py

# 运行测试
python test_agent.py
```

## 📖 文档

- [使用指南](USAGE.md) - 详细的使用说明和示例
- [项目总结](PROJECT_SUMMARY.md) - 完整的项目介绍

## 🏗️ 架构

```
react-agent-framework/
├── core/              # 核心模块
│   ├── agent.py      # ReAct Agent 实现
│   ├── memory.py     # 记忆管理系统
│   └── prompt.py     # Prompt 模板
├── tools/            # 工具集
│   ├── calculator.py # 计算器
│   ├── file_ops.py   # 文件操作
│   └── search.py     # 搜索工具
├── main.py           # 入口文件
└── test_agent.py     # 测试脚本
```

## 💡 示例

```python
from core.agent import ReActAgent

agent = ReActAgent(api_key="your_api_key")

# 数学计算
response = agent.chat("计算 (15 + 25) * 3 的结果")

# 文件操作
response = agent.chat("帮我创建一个文件 hello.txt")

# 查看详细过程
response = agent.chat("计算 100 / 3", verbose=True)
```

## 🛠️ 技术栈

- Python 3.7+
- OpenAI SDK (兼容模式)
- DashScope/Qwen API
- ReAct Design Pattern

## 📄 许可证

MIT License