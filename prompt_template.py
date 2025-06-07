"""
Prompt 模板模块

功能：
- 定义并返回一个用于生成翻译任务的Prompt模板
"""
from langchain_core.prompts import ChatPromptTemplate

def get_translation_prompt_template():
    """
    创建一个用于翻译的Prompt模板。

    模板包含一个系统消息和一个用户占位符。

    Returns:
        ChatPromptTemplate: 用于翻译的聊天提示模板。
    """
    # 系统消息定义了AI的角色和任务
    system_message = "你是一个专业的翻译家，只能返回翻译后的内容，不要有任何多余的解释。"
    
    # 用户消息模板，"{text_to_translate}" 是一个占位符，将在运行时被替换
    human_message_template = "请将以下文本翻译成 {target_language}: {text_to_translate}"

    # 创建并返回ChatPromptTemplate实例
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", human_message_template)
    ])
    
    return prompt

def get_agent_prompt_template():
    """
    创建一个用于 ReAct Agent 的 Prompt 模板。

    这个模板是专门为 LangChain 的 ReAct Agent 设计的，
    包含了必要的占位符：input, agent_scratchpad。

    - input: 用户的原始问题。
    - agent_scratchpad: Agent 的思考过程和工具使用记录，由 AgentExecutor 动态填充。

    Returns:
        PromptTemplate: 用于 Agent 的提示模板。
    """
    # 这个特殊的模板来自于 LangChain Hub，是 `hwchase17/react` 的一个通用版本。
    # 它指导LLM如何进行"思考 -> 行动 -> 观察 -> 思考..."的循环。
    template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""
    # from_template 方法会自动处理模板中的占位符
    prompt = ChatPromptTemplate.from_template(template)
    return prompt 