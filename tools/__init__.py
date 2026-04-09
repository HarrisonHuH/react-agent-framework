"""
工具模块 - 定义工具基类和注册机制
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """工具基类"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, **kwargs) -> Any:
        """执行工具"""
        pass

    def get_info(self) -> Dict:
        """获取工具信息"""
        return {
            "name": self.name,
            "description": self.description
        }


# 工具注册表
TOOL_REGISTRY = {}


def register_tool(tool: BaseTool):
    """注册工具"""
    TOOL_REGISTRY[tool.name] = tool


def get_tool(tool_name: str) -> BaseTool:
    """获取工具"""
    return TOOL_REGISTRY.get(tool_name)


def get_all_tools() -> list:
    """获取所有已注册的工具"""
    return list(TOOL_REGISTRY.values())


def get_tools_description() -> str:
    """获取工具描述（用于 Prompt）"""
    descriptions = []
    for tool in TOOL_REGISTRY.values():
        descriptions.append(f"- {tool.name}: {tool.description}")
    return "\n".join(descriptions)


def get_tool_names() -> list:
    """获取所有工具名称"""
    return list(TOOL_REGISTRY.keys())