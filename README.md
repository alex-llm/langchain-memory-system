# LangChain Agent with Multi-Memory Integration

一个集成了多种记忆功能的 LangChain Agent 项目，支持 Mem0、OpenMemory MCP 和模拟记忆工具的智能对话系统。

## 🚀 项目特性

### 核心功能
- **多层级记忆系统**: 支持 Mem0 → OpenMemory MCP → 模拟工具的自动回退机制
- **智能对话 Agent**: 基于 LangChain 构建的 ReAct Agent
- **模块化设计**: 高度模块化的代码结构，易于扩展和维护
- **多种记忆后端**: 灵活的记忆存储选择
- **翻译功能**: 内置多语言翻译功能

### 记忆系统特性
- **智能关键词搜索**: 支持同义词和模糊匹配
- **持久化存储**: 支持向量数据库和本地存储
- **实时记忆**: 对话过程中的动态记忆管理
- **记忆分类**: 自动提取和分类用户信息

## 📁 项目结构

```
langchain-base-memery-20250607/
├── README.md                 # 项目说明文档
├── requirements.txt          # Python 依赖
├── .env                     # 环境变量配置
├── main.py                  # 主程序入口
├── test_simple.py           # 简化测试
├── test_final.py            # 完整功能测试
│
├── 核心模块/
│   ├── llm_config.py           # LLM 和记忆服务配置
│   ├── prompt_template.py      # 提示模板管理
│   ├── chain_factory.py        # Agent 创建工厂
│   └── memory_manager.py       # 简单记忆管理器
│
├── 记忆集成模块/
│   ├── mem0_tools.py           # Mem0 集成工具
│   ├── openmemory_tools.py     # OpenMemory MCP 工具
│   ├── openmemory_client.py    # OpenMemory 客户端
│   ├── custom_tools.py         # 模拟记忆工具
│   └── start_openmemory.py     # OpenMemory 服务器启动脚本
│
└── 其他/
    ├── .venv/                  # Python 虚拟环境
    └── __pycache__/           # Python 缓存文件
```

## 🛠️ 安装和配置

### 1. 环境准备

```bash
# 克隆项目
git clone <your-repo-url>
cd langchain-base-memery-20250607

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或者 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 环境变量配置

创建 `.env` 文件并配置以下变量：

```env
# OpenRouter 配置 (必需)
OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"
OPENROUTER_API_KEY="your-openrouter-api-key"
OPENROUTER_MODEL="openrouter/auto"

# OpenAI 兼容配置 (用于 Mem0)
OPENAI_BASE_URL="https://openrouter.ai/api/v1"
OPENAI_API_KEY="your-openrouter-api-key"
OPENAI_EMBEDDING_MODEL="text-embedding-ada-002"

# OpenMemory MCP 配置 (可选)
OPENMEMORY_API_BASE=http://localhost:8765
USER_ID=langchain_user
CLIENT_NAME=langchain_agent
```

### 3. 获取 API 密钥

1. 访问 [OpenRouter](https://openrouter.ai/)
2. 注册账户并获取 API 密钥
3. 将密钥添加到 `.env` 文件中

## 🎯 使用指南

### 快速开始

```bash
# 运行主程序
python main.py

# 运行简化测试
python test_simple.py

# 运行完整功能测试
python test_final.py
```

### 记忆系统选择

项目会按以下优先级自动选择记忆系统：

1. **Mem0** (优先): 专业的 AI 记忆管理系统
2. **OpenMemory MCP**: 需要额外启动服务器
3. **模拟工具** (回退): 简单的内存记忆系统

### 启动 OpenMemory 服务 (可选)

```bash
# 启动 OpenMemory 服务器
python start_openmemory.py

# 或者使用 Docker (如果已安装)
# 脚本会自动检测并使用最佳方式启动
```

## 📋 功能模块详解

### 1. LLM 配置模块 (`llm_config.py`)
- 统一管理 OpenRouter 和记忆服务配置
- 环境变量验证和错误处理
- 支持多种 LLM 提供商

### 2. 记忆工具集成

#### Mem0 工具 (`mem0_tools.py`)
- **功能**: 专业的 AI 记忆管理
- **特性**: 自动事实提取、向量存储、智能搜索
- **状态**: 配置中 (需要兼容的 embeddings 端点)

#### OpenMemory MCP 工具 (`openmemory_tools.py`)
- **功能**: 基于 MCP 协议的记忆服务
- **特性**: REST API 接口、持久化存储
- **状态**: 需要额外服务器启动

#### 模拟记忆工具 (`custom_tools.py`)
- **功能**: 简单的内存记忆系统
- **特性**: 即开即用、智能关键词匹配
- **状态**: 完全可用 ✅

### 3. Agent 工厂 (`chain_factory.py`)
- 自动检测可用的记忆服务
- 创建 ReAct Agent 和执行器
- 错误处理和服务回退机制

### 4. 提示模板 (`prompt_template.py`)
- 翻译功能的提示模板
- Agent 对话的提示模板
- 支持自定义模板扩展

## 🧪 测试功能

### 基础测试 (`test_simple.py`)
```bash
python test_simple.py
```
- 测试基本的记忆添加和搜索功能
- 使用模拟工具确保稳定性

### 完整测试 (`test_final.py`)
```bash
python test_final.py
```
- 测试所有记忆系统的集成
- 多场景测试：个人信息、偏好、历史记录
- 记忆服务可用性检查

### 测试场景
1. **添加个人信息**: 姓名、偏好、居住地等
2. **信息回忆**: 按类别查询历史信息
3. **综合查询**: 获取所有已记录信息
4. **错误处理**: 服务不可用时的回退机制

## 🔧 故障排除

### 常见问题

1. **Mem0 初始化失败**
   ```
   ERROR: 'dict' object has no attribute 'custom_fact_extraction_prompt'
   ```
   - **解决方案**: 项目会自动回退到模拟工具，功能正常

2. **OpenRouter 404 错误**
   ```
   ERROR: Error code: 404 - {'error': {'message': 'Not Found', 'code': 404}}
   ```
   - **原因**: OpenRouter 不支持 embeddings 端点
   - **解决方案**: 使用模拟工具或配置其他 embeddings 提供商

3. **OpenMemory 连接失败**
   ```
   Connection refused on localhost:8765
   ```
   - **解决方案**: 运行 `python start_openmemory.py` 启动服务

### 调试模式

启用详细日志：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 性能特性

### 记忆系统对比

| 特性 | Mem0 | OpenMemory MCP | 模拟工具 |
|------|------|----------------|----------|
| 设置复杂度 | 中等 | 高 | 低 |
| 搜索精度 | 高 | 高 | 中等 |
| 持久化 | ✅ | ✅ | ❌ |
| 即开即用 | ⚠️ | ❌ | ✅ |
| 向量搜索 | ✅ | ✅ | ❌ |
| 推荐场景 | 生产环境 | 企业级 | 开发测试 |

### 系统要求
- **Python**: 3.8+
- **内存**: 最少 512MB
- **网络**: 访问 OpenRouter API
- **存储**: 约 100MB (含依赖)

## 🛣️ 开发路线图

### 当前状态 (v1.0)
- ✅ 基础 Agent 功能
- ✅ 多记忆系统集成
- ✅ 自动回退机制
- ✅ 完整测试套件

### 计划功能 (v1.1)
- [ ] Mem0 配置优化
- [ ] 更多 LLM 提供商支持
- [ ] 记忆导入/导出功能
- [ ] Web UI 界面

### 长期规划 (v2.0)
- [ ] 分布式记忆系统
- [ ] 多用户支持
- [ ] 高级记忆分析
- [ ] API 服务化

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支: `git checkout -b feature/AmazingFeature`
3. 提交更改: `git commit -m 'Add some AmazingFeature'`
4. 推送分支: `git push origin feature/AmazingFeature`
5. 提交 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - 强大的 LLM 应用框架
- [Mem0](https://github.com/mem0ai/mem0) - 专业的 AI 记忆系统
- [OpenRouter](https://openrouter.ai/) - 统一的 LLM API 访问

## 📞 支持

如果你遇到问题或有建议，请：
1. 查看 [常见问题](#故障排除)
2. 在 GitHub Issues 中搜索相关问题
3. 创建新的 Issue 描述你的问题

---

**注意**: 本项目仍在积极开发中，某些功能可能需要额外配置。建议从模拟工具开始测试，然后逐步集成其他记忆系统。 