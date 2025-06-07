#!/usr/bin/env python3
"""
OpenMemory 服务器启动脚本

该脚本用于启动本地的 OpenMemory MCP 服务器，提供记忆管理功能。
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_dependencies():
    """检查必要的依赖是否已安装"""
    try:
        import mem0
        print("✓ mem0ai 已安装")
    except ImportError:
        print("✗ mem0ai 未安装，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mem0ai"])
        print("✓ mem0ai 安装完成")

def check_docker():
    """检查 Docker 是否可用"""
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Docker 可用")
            return True
        else:
            print("✗ Docker 不可用")
            return False
    except FileNotFoundError:
        print("✗ Docker 未安装")
        return False

def start_openmemory_docker():
    """使用 Docker 启动 OpenMemory 服务"""
    print("正在使用 Docker 启动 OpenMemory 服务...")
    
    # 检查是否已有运行的容器
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=openmemory", "--format", "{{.Names}}"],
            capture_output=True, text=True
        )
        if "openmemory" in result.stdout:
            print("OpenMemory 容器已在运行")
            return True
    except Exception as e:
        print(f"检查容器状态时出错: {e}")
    
    # 启动 OpenMemory 容器
    try:
        # 设置环境变量
        env = os.environ.copy()
        env["OPENAI_API_KEY"] = env.get("OPENROUTER_API_KEY", "")
        
        # 使用官方的快速启动命令
        cmd = [
            "bash", "-c",
            "curl -sL https://raw.githubusercontent.com/mem0ai/mem0/main/openmemory/run.sh | bash"
        ]
        
        print("正在下载并启动 OpenMemory...")
        process = subprocess.Popen(cmd, env=env)
        
        # 等待服务启动
        print("等待服务启动...")
        time.sleep(30)
        
        return check_service_health()
        
    except Exception as e:
        print(f"启动 OpenMemory 时出错: {e}")
        return False

def start_openmemory_local():
    """使用本地 mem0 启动简单的记忆服务"""
    print("正在启动本地 mem0 记忆服务...")
    
    try:
        from mem0 import Memory
        
        # 创建一个简单的内存实例
        memory = Memory()
        print("✓ 本地 mem0 记忆服务已启动")
        return True
        
    except Exception as e:
        print(f"启动本地记忆服务时出错: {e}")
        return False

def check_service_health(url="http://localhost:8765/health", timeout=5):
    """检查服务健康状态"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print("✓ OpenMemory 服务健康检查通过")
            return True
        else:
            print(f"✗ 服务健康检查失败，状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ 无法连接到服务: {e}")
        return False

def main():
    """主函数"""
    print("=== OpenMemory 服务器启动脚本 ===")
    
    # 检查依赖
    check_dependencies()
    
    # 首先尝试检查服务是否已经运行
    if check_service_health():
        print("OpenMemory 服务已在运行，无需重新启动")
        return
    
    # 尝试使用 Docker 启动
    if check_docker():
        if start_openmemory_docker():
            print("✓ OpenMemory 服务已通过 Docker 启动")
            return
    
    # 回退到本地启动
    print("回退到本地 mem0 服务...")
    if start_openmemory_local():
        print("✓ 本地记忆服务已启动")
        print("注意: 使用的是简化的本地记忆服务，功能可能有限")
    else:
        print("✗ 无法启动任何记忆服务")
        sys.exit(1)

if __name__ == "__main__":
    main() 