'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-28 16:00:24
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-28 16:00:27
 # @ Description:
 '''
import os
import openai
import json
from dotenv import load_dotenv
##############
load_dotenv()
os.environ["MODEL"] = os.getenv("MODEL")
os.environ["BASE_URL"] = os.getenv("BASE_URL")
os.environ["OTHER_MODEL"] = os.getenv("OTHER_MODEL")


def is_smalltalk(message: str) -> bool:
    greetings = ["你好", "hi", "hello", "嗨", "在吗", "你是谁", "你能做什么"]
    return any(kw in message.lower() for kw in greetings)


def should_greet_or_chitchat(message: str) -> bool:


    client = openai.OpenAI(
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        base_url=os.environ.get("BASE_URL")
    )

    system_prompt = (
        "你是一个分类助手，目标是判断用户输入是否属于“非任务性问候或闲聊内容”。\n\n"
        "【如果满足以下任意情况，请返回 True（表示是问候或闲聊）】：\n"
        "- 问候（你好、hi、hello、早上好、在吗）\n"
        "- 聊天意图（你是谁、你能干嘛、我们聊聊天、你刚刚干嘛了）\n"
        "- 表达情绪或感谢（谢谢你、我很高兴、有点烦等）\n"
        "- 提问但和教学/编程/写报告/出题无关（你喜欢什么颜色、起个名字）\n\n"
        "【以下类型请返回 False（表示是任务请求）】：\n"
        "- 任何有关教学/知识讲解的问题（如“我想学动态规划”、“请讲讲 CNN 原理”、“解释决策树”、“讲讲 AI 在医疗的应用”）\n"
        "- 要求写代码或分析代码（如“写个快排”、“解释以下 Python 代码”）\n"
        "- 要求生成报告、总结、出题（如“生成一份 markdown 报告”、“出 5 道题”）\n\n"
        "⚠️ 请只返回：True 或 False，不要返回其它内容。\n"
    )


    try:
        response = client.chat.completions.create(
            model=os.environ["OTHER_MODEL"] ,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.0,
        )
        result = response.choices[0].message.content.strip().lower()
        print(f"[Chitchat Classify Raw Result]: {result}")
        return result == "true"
    except Exception as e:
        print(f"[Chitchat Classify Error]: {e}")
        return False
    
def summarize_thoughts_stream(thought_text):


    client = openai.OpenAI(api_key=os.environ["OPENROUTER_API_KEY"],base_url=os.environ["BASE_URL"])

    # 用 streaming 模式调用模型总结
    response = client.chat.completions.create(
        model=os.environ["OTHER_MODEL"],  # or gpt-4o-mini
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一个 AI 观察记录员，负责将多位 AI Agent 的任务执行过程，"
                    "以结构清晰、容易理解的格式总结出来。"
                    "\n\n"
                    "你应该模仿 CrewAI 的 `thought` 日志风格，用中文表达，但要逻辑清楚、简明易懂。\n"
                    "请使用以下结构来组织输出：\n"
                    "1. 总览：本次任务的主要目标是什么；\n"
                    "2. 分配：哪些 Agent 被分配到哪些任务；\n"
                    "3. 执行：各个 Agent 是如何执行这些任务的，有没有使用工具，工具输出了什么；\n"
                    "4. 结果简述：总结整体输出结果，是否成功，是否产生文件；\n"
                    "5. 若有必要，补充关键逻辑或注意事项。\n\n"
                    "风格上可以模仿 CrewAI 思考日志，但要更清楚更适合用户阅读，不要逐字复述原始输出。"
                )
            },
            {
                "role": "user",
                "content": (
                    f"以下是 AI agents 在任务执行过程中的原始日志：\n\n{thought_text}\n\n"
                    "请根据上面结构总结输出："
                )
            }
        ],
        stream=True,
        temperature=0.5
    )
    
    # 流式返回
    for chunk in response:
        delta = chunk.choices[0].delta
        if hasattr(delta, "content") and delta.content:
            yield json.dumps({"type": "thought", "data": delta.content}, ensure_ascii=False) + "\n"
