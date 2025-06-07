"""
Chain 工厂模块

功能：
- 将LLM和Prompt模板组装成一个可执行的Chain
- 集成 Mem0 和 OpenMemory MCP 工具来创建具有记忆功能的 Agent
"""
from langchain_openai import ChatOpenAI
from llm_config import get_llm_config
from prompt_template import get_translation_prompt_template, get_agent_prompt_template
from langchain.agents import create_react_agent, AgentExecutor
from mem0_tools import get_mem0_tools, check_mem0_service
from openmemory_tools import get_openmemory_tools, check_openmemory_service
from custom_tools import get_mock_tools
import logging

def create_translation_chain():
    """
    创建并返回一个翻译Chain。

    这个Chain由一个Prompt模板和一个LLM组成。
    它接收 'text_to_translate' 和 'target_language' 作为输入。

    Returns:
        A runnable sequence (chain).
    """
    # 1. 获取LLM配置
    config = get_llm_config()
    
    # 2. 创建LLM实例
    llm = ChatOpenAI(
        model=config.MODEL_NAME,
        base_url=config.BASE_URL,
        api_key=config.API_KEY,
        temperature=0.7
    )
    
    # 3. 获取Prompt模板
    prompt = get_translation_prompt_template()
    
    # 4. 使用 LangChain Expression Language (LCEL) 将 prompt 和 llm "链接" 在一起
    chain = prompt | llm
    
    return chain 

def create_agent_executor():
    """
    创建并返回一个使用记忆工具的 Agent Executor。

    优先级：Mem0 > OpenMemory MCP > 模拟工具
    """
    print("--- 正在初始化 Agent 和工具... ---")
    
    # 获取LLM配置
    config = get_llm_config()
    
    # 创建LLM实例
    llm = ChatOpenAI(
        model=config.MODEL_NAME,
        base_url=config.BASE_URL,
        api_key=config.API_KEY,
        temperature=0.7
    )
    
    # 按优先级检查并获取工具
    tools = []
    memory_service_used = None
    
    # 1. 优先尝试 Mem0
    if check_mem0_service():
        print("--- Mem0 服务可用，加载 Mem0 工具... ---")
        mem0_tools = get_mem0_tools()
        tools.extend(mem0_tools)
        memory_service_used = "Mem0"
        print(f"--- 成功加载 {len(mem0_tools)} 个 Mem0 工具 ---")
        for tool in mem0_tools:
            print(f"  - {tool.name}: {tool.description}")
    
    # 2. 如果 Mem0 不可用，尝试 OpenMemory
    elif check_openmemory_service():
        print("--- OpenMemory 服务可用，加载 OpenMemory 工具... ---")
        openmemory_tools = get_openmemory_tools()
        tools.extend(openmemory_tools)
        memory_service_used = "OpenMemory"
        print(f"--- 成功加载 {len(openmemory_tools)} 个 OpenMemory 工具 ---")
        for tool in openmemory_tools:
            print(f"  - {tool.name}: {tool.description}")
    
    # 3. 如果都不可用，使用模拟工具
    else:
        print("--- 记忆服务不可用，使用模拟记忆工具... ---")
        logging.warning("所有记忆服务都不可用，回退到简单的内存记忆功能")
        mock_tools = get_mock_tools()
        tools.extend(mock_tools)
        memory_service_used = "Mock"
        print(f"--- 加载了 {len(mock_tools)} 个模拟工具 ---")
        for tool in mock_tools:
            print(f"  - {tool.name}: {tool.description}")

    print(f"--- 使用的记忆服务: {memory_service_used} ---")

    # 获取 Agent 的 Prompt 模板
    prompt = get_agent_prompt_template()

    # 创建 Agent
    agent = create_react_agent(llm, tools, prompt)

    # 创建 Agent Executor
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,  # 限制最大迭代次数
        early_stopping_method="generate"  # 在生成答案后停止
    )
    
    return agent_executor 