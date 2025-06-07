"""
主程序入口

功能：
- 演示如何调用具备记忆功能的 Agent
"""
from chain_factory import create_agent_executor

def run_agent_with_memory_example():
    """
    运行一个演示Agent记忆功能的两步示例。
    """
    print("===== Agent 简易记忆功能示例 =====")
    print("正在创建Agent...")
    agent_executor = create_agent_executor()
    print("Agent创建完成。")
    
    # --- 步骤 1: 告诉 Agent 一个新信息 ---
    question1 = "你好，我的名字叫张伟，我最喜欢的颜色是蓝色。"
    print(f"\n[第一步] 用户输入: {question1}")
    try:
        response1 = agent_executor.invoke({"input": question1})
        print(f"Agent回应: {response1['output']}")
    except Exception as e:
        print(f"在执行Agent时发生错误: {e}")

    # --- 步骤 2: 提问，看 Agent 是否能回忆起信息 ---
    question2 = "你知道我叫什么名字，还有我最喜欢的颜色是什么吗？"
    print(f"\n[第二步] 用户输入: {question2}")
    try:
        response2 = agent_executor.invoke({"input": question2})
        print(f"Agent回应: {response2['output']}\n")
    except Exception as e:
        print(f"在执行Agent时发生错误: {e}\n")


def main():
    """
    主函数，执行 Agent 示例。
    """
    try:
        run_agent_with_memory_example()
    except Exception as e:
        print(f"程序发生严重错误: {e}")

if __name__ == "__main__":
    main() 