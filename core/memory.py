"""
Memory 记忆管理系统 - 管理对话历史和上下文
"""

from typing import List, Dict, Optional


class ConversationMemory:
    """对话记忆管理类"""

    def __init__(self, max_turns: int = 10):
        """
        初始化记忆系统
        
        Args:
            max_turns: 最大保留的对话轮数
        """
        self.max_turns = max_turns
        self.history: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        """
        添加消息到历史记录
        
        Args:
            role: 角色类型 ('user', 'assistant', 'system')
            content: 消息内容
        """
        self.history.append({
            "role": role,
            "content": content
        })
        
        # 如果超过最大轮数，删除最早的记录
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-self.max_turns * 2:]

    def add_user_message(self, content: str):
        """添加用户消息"""
        self.add_message("user", content)

    def add_assistant_message(self, content: str):
        """添加助手消息"""
        self.add_message("assistant", content)

    def get_history(self) -> List[Dict[str, str]]:
        """获取完整的对话历史"""
        return self.history.copy()

    def get_recent_turns(self, n: int = None) -> List[Dict[str, str]]:
        """
        获取最近的 n 轮对话
        
        Args:
            n: 要获取的轮数，默认为所有
        """
        if n is None:
            return self.get_history()
        
        # 每轮包含 user 和 assistant 两条消息
        messages_count = n * 2
        return self.history[-messages_count:]

    def format_history_for_prompt(self) -> List[str]:
        """
        将历史格式化为适合 Prompt 的字符串列表
        
        Returns:
            格式化后的历史列表
        """
        formatted = []
        for msg in self.history:
            if msg["role"] == "user":
                formatted.append(f"问题：{msg['content']}")
            elif msg["role"] == "assistant":
                formatted.append(f"回答：{msg['content']}")
        return formatted

    def clear(self):
        """清空历史记录"""
        self.history.clear()

    def size(self) -> int:
        """获取历史记录数量"""
        return len(self.history)