"""
Mem0 集成工具模块

该模块定义了与 mem0ai 直接集成的 LangChain 工具，包括：
- 添加记忆工具
- 搜索记忆工具
- 列表记忆工具
- 删除记忆工具
"""

from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional, Dict, Any
import logging
import json
from llm_config import get_llm_config

class Mem0Client:
    """Mem0 客户端"""
    
    def __init__(self):
        """初始化 Mem0 客户端"""
        self.config = get_llm_config()
        self.user_id = self.config.USER_ID
        self.client_name = self.config.CLIENT_NAME
        self._memory = None
        self._is_healthy = False
        self._initialize_memory()
        
    def _initialize_memory(self):
        """初始化 mem0 Memory 实例"""
        try:
            from mem0 import Memory
            
            # 尝试使用简化配置
            config = {
                "llm": {
                    "provider": "openai",
                    "config": {
                        "model": self.config.MODEL_NAME,
                        "api_key": self.config.API_KEY,
                        "base_url": self.config.BASE_URL
                    }
                }
            }
            
            self._memory = Memory(config=config)
            self._is_healthy = True
            logging.info(f"Mem0 客户端初始化完成 - 用户ID: {self.user_id}")
            
        except Exception as e:
            logging.error(f"初始化 Mem0 客户端失败: {e}")
            # 使用默认配置重试
            try:
                from mem0 import Memory
                self._memory = Memory()
                self._is_healthy = True
                logging.info("使用默认配置初始化 Mem0 客户端")
            except Exception as e2:
                logging.error(f"使用默认配置初始化也失败: {e2}")
                self._memory = None
                self._is_healthy = False
    
    def add_memory(self, text: str, metadata: Optional[Dict] = None) -> str:
        """添加记忆"""
        if not self._memory or not self._is_healthy:
            return "错误: Mem0 客户端未正确初始化"
        
        try:
            messages = [{"role": "user", "content": text}]
            result = self._memory.add(
                messages, 
                user_id=self.user_id,
                metadata=metadata or {"source": "langchain_agent", "client": self.client_name}
            )
            logging.info(f"成功添加记忆: {text[:50]}...")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            error_msg = f"添加记忆失败: {e}"
            logging.error(error_msg)
            self._is_healthy = False  # 标记为不健康
            return error_msg
    
    def search_memory(self, query: str, limit: int = 10) -> str:
        """搜索记忆"""
        if not self._memory or not self._is_healthy:
            return "错误: Mem0 客户端未正确初始化"
        
        try:
            result = self._memory.search(
                query=query,
                user_id=self.user_id,
                limit=limit
            )
            logging.info(f"搜索记忆完成，查询: {query}")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            error_msg = f"搜索记忆失败: {e}"
            logging.error(error_msg)
            self._is_healthy = False  # 标记为不健康
            return error_msg
    
    def list_memories(self) -> str:
        """列出所有记忆"""
        if not self._memory or not self._is_healthy:
            return "错误: Mem0 客户端未正确初始化"
        
        try:
            result = self._memory.get_all(user_id=self.user_id)
            logging.info("获取记忆列表完成")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            error_msg = f"获取记忆列表失败: {e}"
            logging.error(error_msg)
            self._is_healthy = False  # 标记为不健康
            return error_msg
    
    def delete_all_memories(self) -> str:
        """删除所有记忆"""
        if not self._memory or not self._is_healthy:
            return "错误: Mem0 客户端未正确初始化"
        
        try:
            result = self._memory.delete_all(user_id=self.user_id)
            logging.info("成功删除所有记忆")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            error_msg = f"删除所有记忆失败: {e}"
            logging.error(error_msg)
            self._is_healthy = False  # 标记为不健康
            return error_msg
    
    def health_check(self) -> bool:
        """健康检查"""
        return self._memory is not None and self._is_healthy

# 全局客户端实例
_mem0_client = None

def get_mem0_client() -> Mem0Client:
    """获取全局 Mem0 客户端实例（单例模式）"""
    global _mem0_client
    if _mem0_client is None:
        _mem0_client = Mem0Client()
    return _mem0_client

# 工具定义
class AddMemoryInput(BaseModel):
    """添加记忆工具的输入参数"""
    text: str = Field(description="要记忆的文本内容")

class AddMemoryTool(BaseTool):
    """添加记忆到 Mem0 的工具"""
    name: str = "add_memory"
    description: str = ("用于添加新的记忆信息。当用户告诉你任何关于他们自己的信息、偏好、"
                       "或任何可能在未来对话中有用的相关信息时调用此工具。"
                       "例如：姓名、喜好、经历、工作信息等。")
    args_schema: Type[BaseModel] = AddMemoryInput
    
    def _run(self, text: str) -> str:
        """执行添加记忆操作"""
        try:
            client = get_mem0_client()
            if not client.health_check():
                return "错误: Mem0 服务不可用"
            result = client.add_memory(text)
            return f"已成功记住: {text}"
        except Exception as e:
            error_msg = f"添加记忆时发生错误: {e}"
            logging.error(error_msg)
            return error_msg

class SearchMemoryInput(BaseModel):
    """搜索记忆工具的输入参数"""
    query: str = Field(description="搜索查询，用于查找相关的记忆内容")

class SearchMemoryTool(BaseTool):
    """从 Mem0 搜索记忆的工具"""
    name: str = "search_memory"
    description: str = ("用于搜索已存储的记忆信息。每当用户提问时都应该调用此工具，"
                       "以查找可能相关的历史信息和偏好。这有助于提供更个性化的回答。")
    args_schema: Type[BaseModel] = SearchMemoryInput
    
    def _run(self, query: str) -> str:
        """执行搜索记忆操作"""
        try:
            client = get_mem0_client()
            if not client.health_check():
                return "错误: Mem0 服务不可用"
            result = client.search_memory(query)
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
            client = get_mem0_client()
            if not client.health_check():
                return "错误: Mem0 服务不可用"
            result = client.list_memories()
            return result
        except Exception as e:
            error_msg = f"获取记忆列表时发生错误: {e}"
            logging.error(error_msg)
            return error_msg

def get_mem0_tools():
    """
    获取所有 Mem0 相关的工具
    
    Returns:
        list: 工具列表
    """
    return [
        AddMemoryTool(),
        SearchMemoryTool(),
        ListMemoriesTool()
    ]

def check_mem0_service():
    """
    检查 Mem0 服务是否可用
    
    Returns:
        bool: 服务是否可用
    """
    try:
        client = get_mem0_client()
        return client.health_check()
    except Exception as e:
        logging.warning(f"Mem0 服务检查失败: {e}")
        return False 