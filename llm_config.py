"""
大语言模型配置模块

该模块定义了与LLM相关的配置参数，包括:
- OpenRouter API配置
- OpenMemory MCP 配置 
- 模型参数设置
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class LLMConfig:
    """LLM配置类"""
    # OpenRouter API配置
    API_KEY = os.getenv("OPENROUTER_API_KEY")
    BASE_URL = "https://openrouter.ai/api/v1"
    MODEL_NAME = "openrouter/auto"
    
    # OpenMemory MCP 配置
    OPENMEMORY_API_BASE = os.getenv("OPENMEMORY_API_BASE", "http://localhost:8765")
    USER_ID = os.getenv("USER_ID", "default_user")
    CLIENT_NAME = os.getenv("CLIENT_NAME", "langchain_agent")
    
    @classmethod
    def validate(cls):
        """验证必需的配置是否已设置"""
        missing_vars = []
        if not cls.API_KEY:
            missing_vars.append("OPENROUTER_API_KEY")
        
        if missing_vars:
            raise ValueError(f"以下环境变量必须设置: {', '.join(missing_vars)}")
        
        return True

def get_llm_config():
    """
    获取验证后的LLM配置实例
    
    Returns:
        LLMConfig: 配置实例
        
    Raises:
        ValueError: 当必需配置缺失时
    """
    LLMConfig.validate()
    return LLMConfig 