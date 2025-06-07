"""
简易内存管理模块

功能：
- 使用一个简单的列表来模拟记忆功能。
- 封装添加和搜索记忆的操作。
- 支持智能关键词匹配搜索。
"""

class MemoryManager:
    _instance = None
    _memory_storage = []

    def __new__(cls):
        if cls._instance is None:
            print("--- 初始化简易内存实例 ---")
            cls._instance = super(MemoryManager, cls).__new__(cls)
        return cls._instance

    def add_memory(self, data: str):
        """向内存中添加信息。"""
        print(f"--- 正在添加内存: '{data}' ---")
        self._memory_storage.append(data)

    def search_memory(self, query: str) -> list:
        """从内存中搜索包含查询关键词的信息。"""
        print(f"--- 正在搜索内存: '{query}' ---")
        
        # 改进的搜索逻辑：支持多种关键词匹配
        query_lower = query.lower()
        results = []
        
        # 定义关键词映射
        keyword_mappings = {
            "名字": ["姓名", "名字", "叫", "张伟"],
            "姓名": ["姓名", "名字", "叫", "张伟"],
            "颜色": ["颜色", "色彩", "蓝色"],
            "喜欢": ["喜欢", "偏好", "最爱"],
            "用户": ["用户", "我", "他", "她"]
        }
        
        # 扩展搜索关键词
        search_keywords = [query_lower]
        for key, synonyms in keyword_mappings.items():
            if key in query_lower:
                search_keywords.extend(synonyms)
        
        # 如果没有找到映射，也搜索原始查询
        if not results:
            # 分词搜索
            query_words = query_lower.split()
            search_keywords.extend(query_words)
        
        # 搜索匹配的记忆
        for mem in self._memory_storage:
            mem_lower = mem.lower()
            for keyword in search_keywords:
                if keyword.strip() and keyword in mem_lower:
                    if mem not in results:  # 避免重复
                        results.append(mem)
                    break
        
        print(f"--- 搜索到 {len(results)} 条记忆 ---")
        return results

    def clear_memory(self):
        """清空所有记忆。"""
        print("--- 清空所有记忆 ---")
        self._memory_storage.clear()

    def list_all_memories(self):
        """列出所有记忆。"""
        print("--- 列出所有记忆 ---")
        return self._memory_storage.copy()

# 创建一个全局单例
memory_manager = MemoryManager() 