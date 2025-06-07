"""
最终的完整测试程序

测试 Agent 的记忆功能，包括 Mem0、OpenMemory 和模拟工具的集成
"""
from langchain_openai import ChatOpenAI
from llm_config import get_llm_config
from prompt_template import get_agent_prompt_template
from langchain.agents import create_react_agent, AgentExecutor
from chain_factory import create_agent_executor
import logging

# 设置日志级别
logging.basicConfig(level=logging.INFO)

def run_complete_test():
    """运行完整的集成测试"""
    print("===== 完整的 Agent 记忆功能集成测试 =====")
    print("测试优先级：Mem0 > OpenMemory > 模拟工具")
    print()
    
    # 创建 Agent（使用工厂方法，会自动选择最佳的记忆服务）
    print("正在创建 Agent...")
    agent_executor = create_agent_executor()
    print("Agent 创建完成。\n")
    
    # 测试场景
    test_scenarios = [
        {
            "name": "添加个人信息",
            "input": "你好，我的名字叫张伟，我最喜欢的颜色是蓝色，我住在北京。",
            "expected_keywords": ["张伟", "蓝色", "北京"]
        },
        {
            "name": "回忆姓名",
            "input": "你知道我叫什么名字吗？",
            "expected_keywords": ["张伟"]
        },
        {
            "name": "回忆颜色偏好",
            "input": "我最喜欢的颜色是什么？",
            "expected_keywords": ["蓝色"]
        },
        {
            "name": "回忆居住地",
            "input": "我住在哪里？",
            "expected_keywords": ["北京"]
        },
        {
            "name": "综合回忆",
            "input": "请告诉我你记住的关于我的所有信息。",
            "expected_keywords": ["张伟", "蓝色", "北京"]
        }
    ]
    
    # 执行测试
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"[测试 {i}] {scenario['name']}")
        print(f"用户输入: {scenario['input']}")
        print("-" * 50)
        
        try:
            response = agent_executor.invoke({"input": scenario["input"]})
            output = response['output']
            print(f"Agent回应: {output}")
            
            # 简单的关键词检查
            found_keywords = []
            for keyword in scenario.get('expected_keywords', []):
                if keyword in output:
                    found_keywords.append(keyword)
            
            if found_keywords:
                print(f"✓ 包含期望关键词: {found_keywords}")
            else:
                print("⚠ 回应中未包含期望的关键词")
                
        except Exception as e:
            print(f"✗ 执行出错: {e}")
        
        print("=" * 70)
        print()

def run_memory_service_comparison():
    """比较不同记忆服务的可用性"""
    print("===== 记忆服务可用性检查 =====")
    
    # 检查 Mem0
    try:
        from mem0_tools import check_mem0_service
        mem0_available = check_mem0_service()
        print(f"Mem0 服务: {'✓ 可用' if mem0_available else '✗ 不可用'}")
    except Exception as e:
        print(f"Mem0 服务: ✗ 检查失败 - {e}")
    
    # 检查 OpenMemory
    try:
        from openmemory_tools import check_openmemory_service
        openmemory_available = check_openmemory_service()
        print(f"OpenMemory 服务: {'✓ 可用' if openmemory_available else '✗ 不可用'}")
    except Exception as e:
        print(f"OpenMemory 服务: ✗ 检查失败 - {e}")
    
    # 模拟工具总是可用
    print(f"模拟记忆工具: ✓ 可用")
    print()

if __name__ == "__main__":
    # 先检查服务可用性
    run_memory_service_comparison()
    
    # 运行完整测试
    run_complete_test()
    
    print("===== 测试完成 =====")
    print("如果您想要使用 OpenMemory 完整功能，请运行：")
    print("python start_openmemory.py")
    print()
    print("如果您想要配置 Mem0 使用外部向量数据库，请参考 mem0ai 官方文档：")
    print("https://github.com/mem0ai/mem0") 