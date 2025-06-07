#!/usr/bin/env python3
"""
LangChain Agent 记忆功能演示脚本

展示项目的核心功能，包括：
1. 翻译功能演示
2. 记忆 Agent 对话演示
3. 多记忆系统切换演示
"""

import sys
import time
from chain_factory import create_translation_chain, create_agent_executor
from mem0_tools import check_mem0_service
from openmemory_tools import check_openmemory_service

def print_header(title):
    """打印格式化的标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_section(title):
    """打印章节标题"""
    print(f"\n--- {title} ---")

def simulate_typing(text, delay=0.02):
    """模拟打字效果"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def demo_translation():
    """演示翻译功能"""
    print_header("🌍 翻译功能演示")
    
    try:
        # 创建翻译链
        print("正在初始化翻译服务...")
        translation_chain = create_translation_chain()
        
        # 演示翻译
        test_cases = [
            {
                "text": "Hello, how are you today?",
                "target": "中文"
            },
            {
                "text": "人工智能正在改变世界",
                "target": "English"
            },
            {
                "text": "Bonjour, comment allez-vous?",
                "target": "日语"
            }
        ]
        
        for i, case in enumerate(test_cases, 1):
            print_section(f"翻译示例 {i}")
            print(f"原文: {case['text']}")
            print(f"目标语言: {case['target']}")
            print("翻译中...", end="")
            
            # 执行翻译
            result = translation_chain.invoke({
                "text_to_translate": case["text"],
                "target_language": case["target"]
            })
            
            print(f"\n译文: {result.content}")
            time.sleep(1)
            
    except Exception as e:
        print(f"翻译演示失败: {e}")

def demo_memory_services():
    """演示记忆服务状态"""
    print_header("🧠 记忆服务状态检查")
    
    services = [
        {
            "name": "Mem0 AI",
            "check_func": check_mem0_service,
            "description": "专业的 AI 记忆管理系统"
        },
        {
            "name": "OpenMemory MCP",
            "check_func": check_openmemory_service,
            "description": "基于 MCP 协议的记忆服务"
        }
    ]
    
    for service in services:
        print_section(f"检查 {service['name']}")
        print(f"描述: {service['description']}")
        
        try:
            status = service["check_func"]()
            status_text = "✅ 可用" if status else "❌ 不可用"
            print(f"状态: {status_text}")
        except Exception as e:
            print(f"状态: ❌ 检查失败 - {e}")
        
        time.sleep(0.5)
    
    print_section("模拟记忆工具")
    print("描述: 简单的内存记忆系统")
    print("状态: ✅ 总是可用")

def demo_agent_conversation():
    """演示 Agent 对话功能"""
    print_header("🤖 智能 Agent 对话演示")
    
    try:
        print("正在初始化智能 Agent...")
        agent_executor = create_agent_executor()
        
        # 对话场景
        conversation_steps = [
            {
                "step": "自我介绍",
                "input": "你好，我叫李明，是一名软件工程师，我喜欢阅读和编程。",
                "description": "用户提供个人信息"
            },
            {
                "step": "询问爱好",
                "input": "我的爱好是什么？",
                "description": "测试记忆回忆功能"
            },
            {
                "step": "询问职业",
                "input": "你记得我的职业吗？",
                "description": "测试职业信息回忆"
            },
            {
                "step": "综合查询",
                "input": "请告诉我你记住的关于我的所有信息。",
                "description": "测试综合信息回忆"
            }
        ]
        
        for i, step in enumerate(conversation_steps, 1):
            print_section(f"对话步骤 {i}: {step['step']}")
            print(f"场景: {step['description']}")
            print(f"用户: {step['input']}")
            print("Agent 思考中...")
            
            try:
                response = agent_executor.invoke({"input": step["input"]})
                print(f"Agent: {response['output']}")
            except Exception as e:
                print(f"Agent: 抱歉，我遇到了一些问题: {e}")
            
            print("-" * 40)
            time.sleep(2)
            
    except Exception as e:
        print(f"Agent 对话演示失败: {e}")

def demo_architecture():
    """展示项目架构"""
    print_header("🏗️ 项目架构展示")
    
    architecture = """
    LangChain Agent 多记忆集成架构
    
    ┌─────────────────────────────────────────────┐
    │                用户接口                      │
    │   (main.py, test_simple.py, test_final.py) │
    └─────────────────┬───────────────────────────┘
                      │
    ┌─────────────────▼───────────────────────────┐
    │              Agent 工厂                     │
    │            (chain_factory.py)               │
    │     ┌─────────────────────────────────┐     │
    │     │    自动记忆服务选择逻辑          │     │
    │     │  Mem0 → OpenMemory → 模拟工具   │     │
    │     └─────────────────────────────────┘     │
    └─────────────────┬───────────────────────────┘
                      │
    ┌─────────────────▼───────────────────────────┐
    │               记忆层                        │
    │  ┌─────────┐ ┌─────────┐ ┌─────────────┐   │
    │  │  Mem0   │ │OpenMemory│ │  模拟工具   │   │
    │  │  工具   │ │   MCP   │ │ (内存存储)  │   │
    │  └─────────┘ └─────────┘ └─────────────┘   │
    └─────────────────┬───────────────────────────┘
                      │
    ┌─────────────────▼───────────────────────────┐
    │               基础层                        │
    │  ┌─────────┐ ┌─────────┐ ┌─────────────┐   │
    │  │ LLM配置 │ │提示模板 │ │ 记忆管理器  │   │
    │  └─────────┘ └─────────┘ └─────────────┘   │
    └─────────────────────────────────────────────┘
    """
    
    print(architecture)

def main():
    """主演示函数"""
    print_header("🎯 LangChain Agent 多记忆集成项目演示")
    
    print("欢迎体验 LangChain Agent 多记忆集成项目！")
    print("本演示将展示项目的核心功能和特性。")
    
    # 菜单选项
    options = [
        ("1", "🌍 翻译功能演示", demo_translation),
        ("2", "🧠 记忆服务状态检查", demo_memory_services),
        ("3", "🤖 智能 Agent 对话演示", demo_agent_conversation),
        ("4", "🏗️ 项目架构展示", demo_architecture),
        ("5", "🚀 完整功能演示", lambda: run_all_demos()),
        ("q", "❌ 退出", None)
    ]
    
    while True:
        print_header("📋 演示菜单")
        for option, description, _ in options:
            print(f"  {option}. {description}")
        
        choice = input("\n请选择演示内容 (输入数字或 q 退出): ").strip().lower()
        
        if choice == 'q':
            print("\n感谢体验！再见！ 👋")
            break
        
        # 查找并执行对应的演示
        demo_func = None
        for option, description, func in options:
            if choice == option:
                demo_func = func
                break
        
        if demo_func:
            try:
                demo_func()
            except KeyboardInterrupt:
                print("\n\n演示被用户中断。")
            except Exception as e:
                print(f"\n演示过程中发生错误: {e}")
            
            input("\n按 Enter 键返回主菜单...")
        else:
            print("无效选择，请重试。")

def run_all_demos():
    """运行所有演示"""
    print_header("🚀 完整功能演示")
    print("即将展示所有功能模块...")
    
    demos = [
        ("项目架构", demo_architecture),
        ("记忆服务状态", demo_memory_services),
        ("翻译功能", demo_translation),
        ("Agent 对话", demo_agent_conversation)
    ]
    
    for name, demo_func in demos:
        print(f"\n正在演示: {name}")
        time.sleep(1)
        try:
            demo_func()
        except Exception as e:
            print(f"{name} 演示失败: {e}")
        
        print(f"\n{name} 演示完成。")
        time.sleep(2)
    
    print_header("✅ 所有演示完成")
    print("感谢观看完整功能演示！")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断。再见！")
    except Exception as e:
        print(f"\n程序发生错误: {e}")
        sys.exit(1) 