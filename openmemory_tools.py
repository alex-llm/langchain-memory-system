"""
OpenMemory 集成工具模块

该模块定义了与 OpenMemory 集成的 LangChain 工具，包括：
- 添加记忆工具
- 搜索记忆工具
- 列表记忆工具
- 删除记忆工具
"""

from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional
import logging
from openmemory_client import get_openmemory_client

class AddMemoryInput(BaseModel):
    """添加记忆工具的输入参数"""
    text: str = Field(description="要记忆的文本内容")

class AddMemoryTool(BaseTool):
    """添加记忆到 OpenMemory 的工具"""
    name: str = "add_memory"
    description: str = ("用于添加新的记忆信息。当用户告诉你任何关于他们自己的信息、偏好、"
                       "或任何可能在未来对话中有用的相关信息时调用此工具。"
                       "例如：姓名、喜好、经历、工作信息等。")
    args_schema: Type[BaseModel] = AddMemoryInput
    
    def _run(self, text: str) -> str:
        """执行添加记忆操作"""
        try:
            client = get_openmemory_client()
            result = client.add_memory(text)
            logging.info(f"成功添加记忆: {text[:50]}...")
            return f"已成功记住: {text}"
        except Exception as e:
            error_msg = f"添加记忆时发生错误: {e}"
            logging.error(error_msg)
            return error_msg

class SearchMemoryInput(BaseModel):
    """搜索记忆工具的输入参数"""
    query: str = Field(description="搜索查询，用于查找相关的记忆内容")

class SearchMemoryTool(BaseTool):
    """从 OpenMemory 搜索记忆的工具"""
    name: str = "search_memory"
    description: str = ("用于搜索已存储的记忆信息。每当用户提问时都应该调用此工具，"
                       "以查找可能相关的历史信息和偏好。这有助于提供更个性化的回答。")
    args_schema: Type[BaseModel] = SearchMemoryInput
    
    def _run(self, query: str) -> str:
        """执行搜索记忆操作"""
        try:
            client = get_openmemory_client()
            result = client.search_memory(query)
            logging.info(f"成功搜索记忆，查询: {query}")
            return result
        except Exception as e:
            error_msg = f"搜索记忆时发生错误: {e}"
            logging.error(error_msg)
            return error_msg

class ListMemoriesInput(BaseModel):
    """列出记忆工具的输入参数"""
    pass

class ListMemoriesTool(BaseTool):
    """列出所有记忆的工具"""
    name: str = "list_memories"
    description: str = "用于获取所有已存储的记忆信息的列表。当用户想要回顾或查看所有记录的信息时使用。"
    args_schema: Type[BaseModel] = ListMemoriesInput
    
    def _run(self) -> str:
        """执行列出记忆操作"""
        try:
            client = get_openmemory_client()
            result = client.list_memories()
            logging.info("成功获取记忆列表")
            return result
        except Exception as e:
            error_msg = f"获取记忆列表时发生错误: {e}"
            logging.error(error_msg)
            return error_msg

class DeleteAllMemoriesInput(BaseModel):
    """删除所有记忆工具的输入参数"""
    confirmation: str = Field(description="确认删除的字符串，必须是 'CONFIRM_DELETE_ALL'")

class DeleteAllMemoriesTool(BaseTool):
    """删除所有记忆的工具"""
    name: str = "delete_all_memories"
    description: str = ("用于删除所有已存储的记忆信息。这是一个危险操作，只有在用户明确要求"
                       "删除所有记忆时才使用。需要确认参数 'CONFIRM_DELETE_ALL'。")
    args_schema: Type[BaseModel] = DeleteAllMemoriesInput
    
    def _run(self, confirmation: str) -> str:
        """执行删除所有记忆操作"""
        if confirmation != "CONFIRM_DELETE_ALL":
            return "删除操作被取消：需要正确的确认字符串"
        
        try:
            client = get_openmemory_client()
            result = client.delete_all_memories()
            logging.info("成功删除所有记忆")
            return "所有记忆已被删除"
        except Exception as e:
            error_msg = f"删除记忆时发生错误: {e}"
            logging.error(error_msg)
            return error_msg

def get_openmemory_tools():
    """
    获取所有 OpenMemory 相关的工具
    
    Returns:
        list: 工具列表
    """
    return [
        AddMemoryTool(),
        SearchMemoryTool(),
        ListMemoriesTool(),
        DeleteAllMemoriesTool()
    ]

# 检查 OpenMemory 服务可用性
def check_openmemory_service():
    """
    检查 OpenMemory 服务是否可用
    
    Returns:
        bool: 服务是否可用
    """
    try:
        client = get_openmemory_client()
        return client.health_check()
    except Exception as e:
        logging.warning(f"OpenMemory 服务检查失败: {e}")
        return False 