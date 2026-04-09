# ReAct Agent Framework 使用指南

## 📋 项目简介

这是一个基于 ReAct（Reasoning + Acting）模式的智能体框架，能够结合推理和行动来解决复杂任务。

## 🏗️ 架构说明

### 核心模块

1. **core/agent.py** - ReAct Agent 核心逻辑
   - 实现推理-行动循环
   - 解析模型输出并执行工具
   - 管理对话流程

2. **core/memory.py** - 记忆管理系统
   - 存储对话历史
   - 管理上下文窗口
   - 支持多轮对话

3. **core/prompt.py** - Prompt 模板系统
   - 定义 ReAct 提示词格式
   - 动态生成工具描述
   - 构建完整的对话上下文

### 工具集

1. **calculator** - 计算器工具
   - 支持加减乘除和括号运算
   - 安全的表达式求值

2. **file_read / file_write** - 文件操作工具
   - 读取文件内容
   - 写入文件内容
   - 自动创建目录

3. **search** - 搜索工具
   - 网络搜索（当前为模拟实现）
   - 可接入真实搜索 API

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

确保 `.env` 文件中包含您的 DashScope API Key：

```
DASHSCOPE_API_KEY=your_api_key_here
```

### 3. 运行交互式对话

```bash
python main.py
```

然后您可以输入问题与 Agent 交互，例如：
- "计算 (15 + 25) * 3 的结果"
- "帮我写一个文件 test.txt，内容是 Hello World"
- "读取 test.txt 的内容"

### 4. 运行测试脚本

```bash
python test_agent.py
```

这将自动运行一系列测试，验证各个功能模块。

## 💡 使用示例

### 基本对话

```python
from core.agent import ReActAgent

agent = ReActAgent(api_key="your_api_key", model="qwen-turbo")
response = agent.chat("你好，请介绍一下你自己")
print(response)
```

### 使用计算器

```python
response = agent.chat("计算 123 * 456 的结果")
print(response)  # 输出: 计算结果：56088
```

### 文件操作

```python
# 写入文件
response = agent.chat("请帮我写一个文件 hello.txt，内容是 'Hello, World!'")

# 读取文件
response = agent.chat("请读取 hello.txt 的内容")
```

### 查看详细过程

```python
# 设置 verbose=True 查看 ReAct 循环的详细过程
response = agent.chat("计算 (10 + 20) * 2", verbose=True)
```

输出示例：
```
--- 迭代 1 ---
LLM 响应：
Thought: 我需要计算这个表达式
Action: calculator
Action Input: {"expression": "(10 + 20) * 2"}

🔧 执行动作：calculator
📥 输入：{'expression': '(10 + 20) * 2'}
📤 观察结果：计算结果：60

✅ 找到最终答案
```

## 🔧 添加自定义工具

1. 在 `tools/` 目录下创建新的工具文件，例如 `my_tool.py`

2. 继承 `BaseTool` 类并实现 `run` 方法：

```python
from tools import BaseTool, register_tool

class MyCustomTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="我的自定义工具描述"
        )
    
    def run(self, param1: str, **kwargs) -> str:
        # 实现工具逻辑
        return f"结果：{param1}"

# 注册工具
register_tool(MyCustomTool())
```

3. 在 `main.py` 或测试脚本中导入您的工具：

```python
from tools import my_tool
```

工具会自动注册到系统中，Agent 就可以使用它了！

## 📝 ReAct 工作流程

1. **接收问题** - 用户提出问题
2. **思考（Thought）** - LLM 分析需要什么信息
3. **行动（Action）** - 选择合适的工具
4. **观察（Observation）** - 获取工具执行结果
5. **重复 2-4** - 直到获得足够信息
6. **最终答案（Final Answer）** - 给出回答

## ⚙️ 配置选项

### ReActAgent 参数

- `api_key`: DashScope API Key（必需）
- `model`: 使用的模型名称，默认 "qwen-turbo"
- `max_iterations`: 最大迭代次数，默认 5（防止无限循环）

### ConversationMemory 参数

- `max_turns`: 最大保留的对话轮数，默认 10

## 🎯 最佳实践

1. **明确的问题描述** - 越具体的问题，Agent 越容易理解
2. **合理使用工具** - 不是所有问题都需要工具
3. **监控迭代次数** - 复杂问题可能需要更多迭代
4. **清理记忆** - 长时间运行时定期调用 `agent.clear_memory()`

## 🐛 故障排除

### 问题：API 调用失败

- 检查 `.env` 文件中的 API Key 是否正确
- 确认网络连接正常
- 验证 DashScope 账户余额充足

### 问题：工具未找到

- 确保工具文件已正确导入
- 检查工具是否已调用 `register_tool()`
- 验证工具名称拼写正确

### 问题：无限循环

- 降低 `max_iterations` 参数
- 简化问题复杂度
- 检查 Prompt 模板是否正确

## 📚 扩展阅读

- [ReAct Paper](https://arxiv.org/abs/2210.03629) - ReAct 原始论文
- [DashScope API](https://help.aliyun.com/zh/dashscope/) - 阿里云 DashScope 文档
- [OpenAI Compatible API](https://platform.openai.com/docs/api-reference) - OpenAI API 参考

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个框架！

## 📄 许可证

MIT License
