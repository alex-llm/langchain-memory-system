"""
自定义工具模块

功能：
- 定义一个或多个供 LangChain Agent 使用的自定义工具。
"""
from langchain.agents import tool
from memory_manager import memory_manager

@tool
def add_memory(data: str) -> str:
    """
    一个用于记录和储存信息的工具。
    当你需要记住新的事实、数据或用户偏好时使用它。
    """
    memory_manager.add_memory(data)
    return f"已成功记住信息: '{data}'"

@tool
def search_memory(query: str) -> str:
    """
    一个用于从记忆中搜索和回忆信息的工具。
    当你需要回答关于过去对话或已知事实的问题时使用它。
    """
    memories = memory_manager.search_memory(query)
    if not memories:
        return "在我的记忆中没有找到相关信息。"
    # 将搜索结果格式化为字符串返回给Agent
    result = "从记忆中找到以下相关信息：\n" + "\n".join([f"- {mem}" for mem in memories])
    return result

def get_mock_tools():
    """
    获取模拟记忆工具列表
    
    Returns:
        list: 工具列表
    """
    return [add_memory, search_memory] 