# 工具开发指南

本指南将教您如何为 ReAct Agent 创建和注册自定义工具。

## 📋 目录

1. [工具基础](#工具基础)
2. [创建新工具](#创建新工具)
3. [工具注册](#工具注册)
4. [最佳实践](#最佳实践)
5. [示例](#示例)

## 工具基础

### BaseTool 类

所有工具都必须继承自 `BaseTool` 类：

```python
from tools import BaseTool

class MyTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="my_tool",           # 工具名称（唯一）
            description="工具描述"     # 工具功能描述
        )
    
    def run(self, **kwargs) -> str:
        """执行工具的主要逻辑"""
        # 实现您的逻辑
        return "结果"
```

### 关键方法

- `__init__`: 初始化工具名称和描述
- `run`: 执行工具的核心逻辑，返回字符串结果
- `get_info`: 获取工具信息（已实现，无需重写）

## 创建新工具

### 步骤 1: 创建工具文件

在 `tools/` 目录下创建新的 Python 文件，例如 `weather.py`：

```python
"""
天气查询工具 - 查询指定城市的天气信息
"""

from tools import BaseTool, register_tool


class WeatherTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="weather",
            description="查询城市天气。参数：city（城市名称）"
        )
    
    def run(self, city: str, **kwargs) -> str:
        """查询天气信息"""
        # 这里可以接入真实的天气 API
        # 为了演示，我们返回模拟数据
        weather_data = {
            "北京": "晴天，温度 25°C",
            "上海": "多云，温度 28°C",
            "广州": "小雨，温度 30°C"
        }
        
        if city in weather_data:
            return f"{city}的天气：{weather_data[city]}"
        else:
            return f"抱歉，暂无 {city} 的天气信息"


# 注册工具
register_tool(WeatherTool())
```

### 步骤 2: 在主程序中导入

在 `main.py` 或测试脚本中导入您的工具：

```python
from tools import weather  # 这会自动执行注册
```

### 步骤 3: 使用工具

现在 Agent 就可以使用您的新工具了：

```python
agent = ReActAgent(api_key="your_api_key")
response = agent.chat("北京今天的天气怎么样？")
```

## 工具注册

### 自动注册

在工具文件的末尾调用 `register_tool()`：

```python
# 注册单个工具
register_tool(MyTool())

# 注册多个工具
register_tool(Tool1())
register_tool(Tool2())
```

### 注册机制

工具会被添加到全局注册表 `TOOL_REGISTRY` 中：

```python
# 查看所有已注册的工具
from tools import TOOL_REGISTRY
print(TOOL_REGISTRY.keys())

# 获取特定工具
from tools import get_tool
tool = get_tool("calculator")
```

## 最佳实践

### 1. 清晰的命名

- 工具名称应该简洁明了
- 使用小写字母和下划线
- 避免与现有工具重名

```python
# ✅ 好的命名
name="weather"
name="file_read"
name="calculator"

# ❌ 不好的命名
name="MyWeatherTool"
name="WR"
name="calc_123"
```

### 2. 详细的描述

描述应该说明：
- 工具的功能
- 需要的参数
- 使用示例

```python
# ✅ 好的描述
description="查询城市天气。参数：city（城市名称）。例如：北京、上海"

# ❌ 不好的描述
description="天气工具"
```

### 3. 参数验证

在 `run` 方法中验证输入参数：

```python
def run(self, city: str, **kwargs) -> str:
    if not city:
        return "错误：请提供城市名称"
    
    if not isinstance(city, str):
        return "错误：城市名称必须是字符串"
    
    # 继续处理...
```

### 4. 错误处理

捕获并优雅地处理异常：

```python
def run(self, url: str, **kwargs) -> str:
    try:
        # 可能出错的操作
        response = requests.get(url)
        return response.text
    except requests.exceptions.ConnectionError:
        return "错误：无法连接到服务器"
    except Exception as e:
        return f"错误：{str(e)}"
```

### 5. 返回字符串

工具必须返回字符串类型的结果：

```python
# ✅ 正确
return f"结果：{value}"
return "成功"
return json.dumps(data)

# ❌ 错误
return 123          # 不是字符串
return None         # 不是字符串
return {"key": "value"}  # 字典，需要转换为 JSON 字符串
```

### 6. 支持关键字参数

使用 `**kwargs` 接收额外参数：

```python
def run(self, param1: str, param2: int = 10, **kwargs) -> str:
    # param1 是必需参数
    # param2 是可选参数，默认值为 10
    # kwargs 包含其他可能的参数
    pass
```

## 示例

### 示例 1: 时间工具

```python
"""
时间工具 - 获取当前时间
"""

from tools import BaseTool, register_tool
from datetime import datetime


class TimeTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="get_time",
            description="获取当前日期和时间。无需参数。"
        )
    
    def run(self, **kwargs) -> str:
        """获取当前时间"""
        now = datetime.now()
        return f"当前时间：{now.strftime('%Y年%m月%d日 %H:%M:%S')}"


register_tool(TimeTool())
```

### 示例 2: JSON 处理工具

```python
"""
JSON 处理工具 - 格式化和验证 JSON
"""

from tools import BaseTool, register_tool
import json


class JsonFormatterTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="json_format",
            description="格式化 JSON 字符串。参数：json_str（JSON 字符串）"
        )
    
    def run(self, json_str: str, **kwargs) -> str:
        """格式化 JSON"""
        try:
            parsed = json.loads(json_str)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            return f"格式化后的 JSON:\n{formatted}"
        except json.JSONDecodeError as e:
            return f"错误：无效的 JSON 格式 - {str(e)}"


register_tool(JsonFormatterTool())
```

### 示例 3: HTTP 请求工具

```python
"""
HTTP 请求工具 - 发送 GET 请求
"""

from tools import BaseTool, register_tool
import requests


class HttpRequestTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="http_get",
            description="发送 HTTP GET 请求。参数：url（请求地址）"
        )
    
    def run(self, url: str, **kwargs) -> str:
        """发送 GET 请求"""
        try:
            # 简单的 URL 验证
            if not url.startswith(('http://', 'https://')):
                return "错误：URL 必须以 http:// 或 https:// 开头"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            return f"状态码: {response.status_code}\n响应内容:\n{response.text[:500]}"
        except requests.exceptions.Timeout:
            return "错误：请求超时"
        except requests.exceptions.ConnectionError:
            return "错误：连接失败"
        except Exception as e:
            return f"错误：{str(e)}"


register_tool(HttpRequestTool())
```

### 示例 4: 数据库查询工具

```python
"""
数据库查询工具 - 执行 SQL 查询（示例）
"""

from tools import BaseTool, register_tool
import sqlite3


class DatabaseQueryTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="db_query",
            description="执行 SQLite 数据库查询。参数：query（SQL 查询语句），db_path（数据库路径，可选）"
        )
    
    def run(self, query: str, db_path: str = ":memory:", **kwargs) -> str:
        """执行数据库查询"""
        try:
            # 安全检查：只允许 SELECT 语句
            if not query.strip().upper().startswith('SELECT'):
                return "错误：只允许执行 SELECT 查询"
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            
            conn.close()
            
            if not rows:
                return "查询结果为空"
            
            # 格式化结果
            result = f"列名: {', '.join(columns)}\n"
            result += "数据:\n"
            for row in rows:
                result += ", ".join(str(val) for val in row) + "\n"
            
            return result
        except Exception as e:
            return f"数据库错误：{str(e)}"


register_tool(DatabaseQueryTool())
```

## 调试工具

### 测试工具

创建独立的测试脚本来测试您的工具：

```python
"""
测试 weather 工具
"""

from tools.weather import WeatherTool

# 创建工具实例
tool = WeatherTool()

# 测试不同场景
print(tool.run(city="北京"))
print(tool.run(city="上海"))
print(tool.run(city="未知城市"))
```

### 查看工具信息

```python
from tools import get_all_tools, get_tools_description

# 查看所有工具
for tool in get_all_tools():
    print(f"{tool.name}: {tool.description}")

# 获取格式化的工具描述（用于 Prompt）
print(get_tools_description())
```

## 常见问题

### Q: 工具没有被识别？

A: 确保：
1. 工具文件已被导入（`from tools import my_tool`）
2. 调用了 `register_tool()`
3. 工具名称拼写正确

### Q: 如何处理复杂参数？

A: 使用 JSON 格式的字符串：

```python
def run(self, params: str, **kwargs) -> str:
    import json
    data = json.loads(params)
    # 处理 data...
```

### Q: 工具执行太慢怎么办？

A: 
1. 设置合理的超时时间
2. 使用异步处理（如果需要）
3. 优化算法逻辑

### Q: 如何访问外部 API？

A: 使用 `requests` 库：

```python
import requests

def run(self, query: str, **kwargs) -> str:
    response = requests.get(f"https://api.example.com?q={query}")
    return response.json()
```

## 总结

创建工具的步骤：
1. ✅ 继承 `BaseTool` 类
2. ✅ 定义工具名称和描述
3. ✅ 实现 `run` 方法
4. ✅ 添加错误处理
5. ✅ 调用 `register_tool()` 注册
6. ✅ 在主程序中导入工具
7. ✅ 测试工具功能

现在您可以创建自己的工具来扩展 ReAct Agent 的能力了！🚀
