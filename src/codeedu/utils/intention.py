'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-28 16:00:24
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-28 16:00:27
 # @ Description:
 '''
import os
from openai import OpenAI
import openai

def is_smalltalk(message: str) -> bool:
    greetings = ["你好", "hi", "hello", "嗨", "在吗", "你是谁", "你能做什么"]
    return any(kw in message.lower() for kw in greetings)


# def detect_intent(message: str) -> str:
#     client = OpenAI(api_key=os.environ["OPENROUTER_API_KEY"], base_url=os.environ["BASE_URL"])
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "你是一个助手，请判断用户输入属于哪种类型：smalltalk（打招呼）、task（请求处理任务）、other（其它）。只返回类型标签。"},
#             {"role": "user", "content": message}
#         ]
#     )
#     return response.choices[0].message.content.strip()


def should_greet_or_chitchat(message: str) -> bool:
    import openai
    import os

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
            model="openai/gpt-4o-mini",
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
