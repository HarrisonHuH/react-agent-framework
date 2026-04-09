"""
计算器工具 - 执行数学计算
"""

from tools import BaseTool, register_tool
import re


class CalculatorTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="calculator",
            description="执行数学计算，支持加减乘除和括号。例如：2+2, 10*5, (3+4)*2"
        )

    def run(self, expression: str, **kwargs) -> str:
        """执行数学计算"""
        try:
            # 安全评估表达式
            if not re.match(r'^[\d+\-*/().\s]+$', expression):
                return "错误：表达式包含非法字符"

            result = eval(expression)
            return f"计算结果：{result}"
        except Exception as e:
            return f"计算错误：{str(e)}"


# 注册工具
register_tool(CalculatorTool())