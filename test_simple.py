"""
简化测试程序

直接使用模拟记忆工具测试 Agent 功能
"""
from langchain_openai import ChatOpenAI
from llm_config import get_llm_config
from prompt_template import get_agent_prompt_template
from langchain.agents import create_react_agent, AgentExecutor
from custom_tools import get_mock_tools

def create_simple_agent():
    """创建使用模拟工具的简单 Agent"""
    print("--- 创建简单 Agent（使用模拟记忆工具）---")
    
    # 获取LLM配置
    config = get_llm_config()
    
    # 创建LLM实例
    llm = ChatOpenAI(
        model=config.MODEL_NAME,
        base_url=config.BASE_URL,
        api_key=config.API_KEY,
        temperature=0.7
    )
    
    # 获取模拟工具
    tools = get_mock_tools()
    print(f"--- 加载了 {len(tools)} 个模拟工具 ---")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
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
        max_iterations=5
    )
    
    return agent_executor

def run_simple_test():
    """运行简化测试"""
    print("===== 简化 Agent 记忆功能测试 =====")
    
    # 创建 Agent
    agent_executor = create_simple_agent()
    
    # 测试 1: 添加记忆
    question1 = "你好，我的名字叫张伟，我最喜欢的颜色是蓝色。"
    print(f"\n[测试1] 用户输入: {question1}")
    try:
        response1 = agent_executor.invoke({"input": question1})
        print(f"Agent回应: {response1['output']}")
    except Exception as e:
        print(f"执行Agent时发生错误: {e}")
    
    # 测试 2: 回忆信息
    question2 = "你知道我叫什么名字，还有我最喜欢的颜色是什么吗？"
    print(f"\n[测试2] 用户输入: {question2}")
    try:
        response2 = agent_executor.invoke({"input": question2})
        print(f"Agent回应: {response2['output']}")
    except Exception as e:
        print(f"执行Agent时发生错误: {e}")

if __name__ == "__main__":
    run_simple_test() 