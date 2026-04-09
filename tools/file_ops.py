"""
文件操作工具 - 读取和写入文件
"""

from tools import BaseTool, register_tool
import os


class FileReadTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="file_read",
            description="读取文件内容。参数：filename（文件路径）"
        )

    def run(self, filename: str, **kwargs) -> str:
        """读取文件内容"""
        try:
            if not os.path.exists(filename):
                return f"错误：文件 '{filename}' 不存在"

            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"文件内容:\n{content}"
        except Exception as e:
            return f"读取错误：{str(e)}"


class FileWriteTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="file_write",
            description="写入文件内容。参数：filename（文件路径）, content（要写入的内容）"
        )

    def run(self, filename: str, content: str, **kwargs) -> str:
        """写入文件内容"""
        try:
            dirname = os.path.dirname(filename)
            if dirname:
                os.makedirs(dirname, exist_ok=True)

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"成功：内容已写入 '{filename}'"
        except Exception as e:
            return f"写入错误：{str(e)}"


# 注册工具
register_tool(FileReadTool())
register_tool(FileWriteTool())