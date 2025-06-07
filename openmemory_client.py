"""
OpenMemory MCP 客户端模块

该模块提供与 OpenMemory MCP 服务器的集成，包括：
- 记忆的添加、搜索、列表和删除功能
- 自动初始化和配置管理
- 错误处理和重试机制
"""

import json
import logging
import requests
from typing import Optional, Dict, Any
from llm_config import get_llm_config

class OpenMemoryClient:
    """OpenMemory MCP 客户端"""
    
    def __init__(self):
        """初始化 OpenMemory 客户端"""
        self.config = get_llm_config()
        self.base_url = self.config.OPENMEMORY_API_BASE
        self.user_id = self.config.USER_ID
        self.client_name = self.config.CLIENT_NAME
        self.session = requests.Session()
        
        # 设置默认的请求头
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': f'LangChain-Agent-{self.client_name}'
        })
        
        logging.info(f"OpenMemory客户端初始化完成 - 用户ID: {self.user_id}, 客户端名称: {self.client_name}")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, retries: int = 3) -> Dict[str, Any]:
        """
        发送HTTP请求到OpenMemory API
        
        Args:
            method: HTTP方法 (GET, POST, DELETE等)
            endpoint: API端点
            data: 请求数据
            retries: 重试次数
            
        Returns:
            Dict: API响应数据
            
        Raises:
            Exception: 当请求失败时
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(retries):
            try:
                if method.upper() == 'GET':
                    response = self.session.get(url, params=data)
                elif method.upper() == 'POST':
                    response = self.session.post(url, json=data)
                elif method.upper() == 'DELETE':
                    response = self.session.delete(url, json=data)
                else:
                    raise ValueError(f"不支持的HTTP方法: {method}")
                
                response.raise_for_status()
                
                # 尝试解析JSON响应
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {"message": response.text, "status": "success"}
                    
            except requests.exceptions.ConnectionError as e:
                if attempt < retries - 1:
                    logging.warning(f"连接失败，正在重试 (第{attempt + 1}次)...")
                    continue
                else:
                    raise Exception(f"无法连接到OpenMemory服务器: {e}")
            except requests.exceptions.HTTPError as e:
                error_msg = f"HTTP错误 {response.status_code}: {response.text}"
                logging.error(error_msg)
                raise Exception(error_msg)
            except Exception as e:
                if attempt < retries - 1:
                    logging.warning(f"请求失败，正在重试: {e}")
                    continue
                else:
                    raise Exception(f"请求失败: {e}")
    
    def add_memory(self, text: str, metadata: Optional[Dict] = None) -> str:
        """
        添加新的记忆
        
        Args:
            text: 要记忆的文本内容
            metadata: 可选的元数据
            
        Returns:
            str: 操作结果
        """
        try:
            # 使用 mem0ai 格式的数据结构
            data = {
                "messages": [
                    {"role": "user", "content": text}
                ],
                "user_id": self.user_id,
                "metadata": metadata or {"source": "langchain_agent", "client": self.client_name}
            }
            
            response = self._make_request('POST', '/api/v1/memories/', data)
            logging.info(f"成功添加记忆: {text[:50]}...")
            return json.dumps(response, ensure_ascii=False, indent=2)
            
        except Exception as e:
            error_msg = f"添加记忆失败: {e}"
            logging.error(error_msg)
            return error_msg
    
    def search_memory(self, query: str, limit: int = 10) -> str:
        """
        搜索记忆
        
        Args:
            query: 搜索查询
            limit: 返回结果的最大数量
            
        Returns:
            str: 搜索结果JSON字符串
        """
        try:
            data = {
                "query": query,
                "user_id": self.user_id,
                "limit": limit
            }
            
            response = self._make_request('POST', '/api/v1/memories/search/', data)
            logging.info(f"搜索记忆完成，查询: {query}")
            return json.dumps(response, ensure_ascii=False, indent=2)
            
        except Exception as e:
            error_msg = f"搜索记忆失败: {e}"
            logging.error(error_msg)
            return error_msg
    
    def list_memories(self) -> str:
        """
        列出所有记忆
        
        Returns:
            str: 记忆列表JSON字符串
        """
        try:
            data = {"user_id": self.user_id}
            response = self._make_request('GET', '/api/v1/memories/', data)
            logging.info("获取记忆列表完成")
            return json.dumps(response, ensure_ascii=False, indent=2)
            
        except Exception as e:
            error_msg = f"获取记忆列表失败: {e}"
            logging.error(error_msg)
            return error_msg
    
    def delete_all_memories(self) -> str:
        """
        删除所有记忆
        
        Returns:
            str: 操作结果
        """
        try:
            data = {"user_id": self.user_id}
            response = self._make_request('DELETE', '/api/v1/memories/', data)
            logging.info("成功删除所有记忆")
            return json.dumps(response, ensure_ascii=False, indent=2)
            
        except Exception as e:
            error_msg = f"删除所有记忆失败: {e}"
            logging.error(error_msg)
            return error_msg
    
    def health_check(self) -> bool:
        """
        检查OpenMemory服务器健康状态
        
        Returns:
            bool: 服务器是否健康
        """
        try:
            response = self._make_request('GET', '/health', retries=1)
            return True
        except Exception as e:
            logging.warning(f"OpenMemory服务器健康检查失败: {e}")
            return False

# 全局客户端实例
_openmemory_client = None

def get_openmemory_client() -> OpenMemoryClient:
    """
    获取全局OpenMemory客户端实例（单例模式）
    
    Returns:
        OpenMemoryClient: 客户端实例
    """
    global _openmemory_client
    if _openmemory_client is None:
        _openmemory_client = OpenMemoryClient()
    return _openmemory_client 