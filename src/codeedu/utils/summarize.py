'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-28 14:54:19
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-28 14:54:22
 # @ Description:
 '''
import json
import os
from openai import OpenAI  
import openai

def summarize_thoughts_stream(thought_text):
    client = openai.OpenAI(api_key=os.environ["OPENROUTER_API_KEY"],base_url=os.environ["BASE_URL"])

    # 用 streaming 模式调用模型总结
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",  # or gpt-4o-mini
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