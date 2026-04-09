# ReAct Agent - 快速参考卡片

## 🚀 快速启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行交互式对话
python main.py

# 3. 运行测试
python test_agent.py

# 4. 运行示例
python examples/simple_demo.py
```

## 💻 编程调用

```python
from core.agent import ReActAgent

# 创建 Agent
agent = ReActAgent(
    api_key="your_api_key",
    model="qwen-turbo",
    max_iterations=5
)

# 简单对话
response = agent.chat("你好！")

# 查看详细过程
response = agent.chat("计算 (15 + 25) * 3", verbose=True)

# 清空记忆
agent.clear_memory()
```

## 🔧 可用工具

| 工具名称 | 功能 | 参数 | 示例 |
|---------|------|------|------|
| calculator | 数学计算 | expression | `{"expression": "2+2"}` |
| file_read | 读取文件 | filename | `{"filename": "test.txt"}` |
| file_write | 写入文件 | filename, content | `{"filename": "test.txt", "content": "Hello"}` |
| search | 网络搜索 | query | `{"query": "Python"}` |

## 📝 添加自定义工具

```python
# 1. 创建工具文件 tools/my_tool.py
from tools import BaseTool, register_tool

class MyTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="我的工具描述。参数：param1（说明）"
        )
    
    def run(self, param1: str, **kwargs) -> str:
        # 实现逻辑
        return f"结果：{param1}"

# 注册工具
register_tool(MyTool())

# 2. 在主程序中导入
from tools import my_tool

# 3. 使用
agent.chat("使用 my_tool 处理 xxx")
```

## 🎯 ReAct 格式

```
Thought: 思考应该做什么
Action: 工具名称
Action Input: {"参数": "值"}
Observation: 工具返回结果
...（可以重复多次）
Thought: 我已经知道答案
Final Answer: 最终回答
```

## 📚 核心 API

### ReActAgent

```python
# 初始化
agent = ReActAgent(api_key, model="qwen-turbo", max_iterations=5)

# 对话
response = agent.chat(question, verbose=False)

# 清空记忆
agent.clear_memory()
```

### ConversationMemory

```python
# 添加消息
memory.add_user_message("用户消息")
memory.add_assistant_message("助手消息")

# 获取历史
history = memory.get_history()
recent = memory.get_recent_turns(5)

# 清空
memory.clear()
```

### Prompt 构建

```python
from core.prompt import build_react_prompt

prompt = build_react_prompt(
    question="用户问题",
    history=["历史记录"]
)
```

## 🔍 调试技巧

### 启用详细模式

```python
response = agent.chat("你的问题", verbose=True)
```

输出：
```
--- 迭代 1 ---
LLM 响应：
Thought: ...
Action: ...
Action Input: ...

🔧 执行动作：calculator
📥 输入：{'expression': '2+2'}
📤 观察结果：计算结果：4

✅ 找到最终答案
```

### 查看工具列表

```python
from tools import get_all_tools

for tool in get_all_tools():
    print(f"{tool.name}: {tool.description}")
```

### 检查记忆状态

```python
print(f"历史消息数: {agent.memory.size()}")
print(f"历史记录: {agent.memory.get_history()}")
```

## ⚙️ 配置选项

### ReActAgent 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| api_key | str | 必需 | DashScope API Key |
| model | str | "qwen-turbo" | 模型名称 |
| max_iterations | int | 5 | 最大迭代次数 |

### ConversationMemory 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| max_turns | int | 10 | 最大保留轮数 |

## 🐛 常见问题

### API 调用失败

```python
# 检查 API Key
import os
from dotenv import load_dotenv
load_dotenv()
print(os.getenv("DASHSCOPE_API_KEY"))
```

### 工具未找到

```python
# 确认工具已注册
from tools import TOOL_REGISTRY
print(TOOL_REGISTRY.keys())

# 确保已导入工具文件
from tools import calculator  # 等
```

### 无限循环

```python
# 减少最大迭代次数
agent = ReActAgent(api_key="...", max_iterations=3)
```

## 📖 文档导航

- **README.md** - 项目简介
- **USAGE.md** - 使用指南
- **TOOLS_GUIDE.md** - 工具开发
- **PROJECT_SUMMARY.md** - 项目总结
- **CHECKLIST.md** - 检查清单

## 💡 实用示例

### 数学计算

```python
agent.chat("计算 (123 + 456) * 2")
```

### 文件操作

```python
# 写入
agent.chat("创建文件 hello.txt，内容是 'Hello World'")

# 读取
agent.chat("读取 hello.txt 的内容")
```

### 多步任务

```python
agent.chat("""
1. 计算 100 除以 3 的结果
2. 将结果保存到 result.txt
3. 读取并显示文件内容
""")
```

### 复杂推理

```python
agent.chat("""
如果一个房间有 4 个角落，每个角落有一只猫，
每只猫对面有 3 只猫，请问房间里总共有几只猫？
请逐步推理。
""", verbose=True)
```

## 🎓 学习路径

1. **入门**: 运行 `main.py` 体验对话
2. **理解**: 阅读 `USAGE.md` 了解用法
3. **实践**: 运行 `test_agent.py` 查看测试
4. **扩展**: 阅读 `TOOLS_GUIDE.md` 学习添加工具
5. **深入**: 阅读源代码理解实现

## 🔗 重要链接

- DashScope API: https://help.aliyun.com/zh/dashscope/
- ReAct Paper: https://arxiv.org/abs/2210.03629
- OpenAI SDK: https://github.com/openai/openai-python

## 📞 支持

遇到问题？

1. 查看 `USAGE.md` 的使用说明
2. 查看 `TOOLS_GUIDE.md` 的工具开发指南
3. 检查 `CHECKLIST.md` 确认配置正确
4. 运行 `test_agent.py` 验证功能

---

**提示**: 将此文件保存为书签，方便快速查阅！🔖
