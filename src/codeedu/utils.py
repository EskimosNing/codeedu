from flask import Flask, Response, stream_with_context,render_template,request,jsonify
import sys
import threading
import queue
import io
import time
from crewai import Crew,Agent,Task,Process # 假设你已经有 agents 和 tasks 构建好了
from crewai_tools import SerperDevTool,CodeInterpreterTool,FileWriterTool

#from langchain.memory import ConversationBufferMemory

from langchain_core.prompts import ChatPromptTemplate
import json
import re
import uuid
import glob
from crewai import LLM
import os
import html
from flask import send_from_directory
from flask_cors import CORS
from agent_pool import planner, researcher, reporting_analyst, programmer, educator,agents_config
from task import distribute_task, code_task, reporting_task, tasks_config,research_task,education_task

#src.codeedu.task 
from pathlib import Path


OUTPUT_DIR =Path(__file__).parent / "output"
STORAGE_PATH = Path(__file__).parent / "conversations" 
#print(STORAGE_PATH)
#print("**********")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STORAGE_PATH, exist_ok=True)
  # user_id or convo_id → {'crew': ..., 'memory': ..., 'history': [...]}
# 队列存储日志
log_queue = queue.Queue()

# --- 工具函数 ---
# 获取对话的路径
def get_convo_path(cid):
    return os.path.join(STORAGE_PATH, f'{cid}.json')

# 加载对话历史
def load_conversation(cid):
    path = get_convo_path(cid)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []

# 保存对话历史
def save_conversation(cid, history):
    with open(get_convo_path(cid), 'w') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


session_store = {}

def get_or_create_session(conversation_id):
    if conversation_id not in session_store:
   
        crew = build_my_crew()
        session_store[conversation_id] = {
            "crew": crew,
            "memory": [],
            "history": load_conversation(conversation_id)
        }
    return session_store[conversation_id]

# def build_memory_from_history(history):
#     #memory = ConversationBufferMemory(return_messages=True)
#     memory  
#     # 加载历史记录，创建 memory
#     for item in history:
#         if item['role'] == 'user':
#             memory.chat_memory.add_user_message(item['content'])
#         elif item['role'] == 'assistant':
#             memory.chat_memory.add_ai_message(item['content'])
#     return memory

# 匹配 ANSI 转义序列的正则
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
#box_drawing = re.compile(r'[─╮╯╰│╭╮╯╰]+')
# 清除颜色控制字符
def strip_ansi(text):
    return ansi_escape.sub('', text)

class StreamToQueue(io.StringIO):
    def write(self, msg):
        if msg.strip():  # 避免空行
            log_queue.put(msg)
        return super().write(msg)

class WordStream(io.StringIO):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.buffer = ""
        self.result_buffer = ""
        self.thought_buffer = ""

    def write(self, s):
        self.buffer += s
        self.result_buffer += s
        self.thought_buffer += s
        words = re.split(r'(\s+)', self.buffer)
        self.buffer = ""
        for i, word in enumerate(words):
            if i == len(words) - 1 and not re.match(r'\s+', word):
                self.buffer = word
            else:
                if word == "\n":
                    self.queue.put({"type": "thought", "data": "\n"})
                elif word.strip() == "":
                    self.queue.put({"type": "thought", "data": " "})
                else:
                    self.queue.put({"type": "thought", "data": word})
                    #self.thought_buffer += word  #  收集思考过程
    def get_result(self):
        return strip_ansi(self.result_buffer)
    def get_thought(self):
        return strip_ansi(self.thought_buffer)

def scan_output_files():
    output_dir = Path("output")
    return set(str(f) for f in output_dir.glob("*") if f.is_file())

# 实时运行 crew 并把输出放到队列中
def run_crewai_and_stream(crew: Crew, inputs: dict,session:dict,cid):
    # 保存原始 stdout
    original_stdout = sys.stdout
    
    #sys.stdout = StreamToQueue()
    word_stream = WordStream(log_queue)
    sys.stdout = word_stream

    files_before = set(scan_output_files())  # 执行前文件列表
    def run():
        try:
            result = crew.kickoff(inputs=inputs)  # 调用你自己的 CrewAI 实例
            # print("####################planner##########")
            # print(result.raw)
            parsed = json.loads(result.raw)  # 把字符串变成 dict
            pretty_json = json.dumps(parsed, ensure_ascii=False, indent=2)

            session["final_result"] = json.dumps(parsed, ensure_ascii=False)
            #raw_output = result.raw
            #session["final_result"] = raw_output
            n = 3  # 每3个字符为一块
            for i in range(0, len(pretty_json), n):
                chunk = pretty_json[i:i+n]
                log_queue.put({"type": "result", "data": chunk})
            #print("RESULT:", result)
            #log_queue.put({"type": "result", "data": result.raw})
        except Exception as e:
            err = f"[ERROR] {str(e)}"
            log_queue.put({"type": "result", "data": f"[ERROR] {str(e)}"})
            session["final_result"] = err


    thread = threading.Thread(target=run)
    thread.start()

    try:
        while thread.is_alive() or not log_queue.empty():
            try:
                item = log_queue.get(timeout=0.5)
                #print("yielding item:", item)
                if isinstance(item, dict) and "data" in item:
                    item["data"] = strip_ansi(item["data"])
                    yield json.dumps(item, ensure_ascii=False) + "\n"
                else:
                    yield strip_ansi(str(item)) #+ "\n"

            except queue.Empty:
                continue


    finally:
        # 还原 stdout
        sys.stdout = original_stdout
        # 获取最终生成结果并存入内存 + history
        #print("####################excu##########")
        #print(session["final_result"])
        final_result = session.get("final_result", "[EMPTY]")
        final_thought = word_stream.get_thought()
        files_after = scan_output_files()
        new_files = files_after - files_before
        if new_files:
            file_infos = []
            for file in new_files:
                # session["history"].append({
                #     "role": "assistant",
                #     "content": strip_ansi(final_result),
                #     "filename": file,
                #     "download_url": f"{file}"
                # })
                file_infos.append({
                        "filename": file,
                        "download_url": f"{file}"
                    })
            #print("####################file_infos##########")
            #print(file_infos)
            #  通知前端文件信息
            yield json.dumps({
                "type": "file_list",
                "files": file_infos
            }, ensure_ascii=False) + "\n"
            session["history"].append({
                "role": "assistant",
                "content":  strip_ansi(final_result),
                "files": file_infos,
                "thought": strip_ansi(final_thought)
            })
        else:
            session["history"].append({
                    "role": "assistant",
                    "content":  strip_ansi(final_result),
                    "thought": strip_ansi(final_thought)
            })
        #session["memory"].chat_memory.add_ai_message(final_result)

        save_conversation(cid, session["history"])

def run_planner_and_stream(planner_crew: Crew, inputs: dict, session: dict):
    original_stdout = sys.stdout
    word_stream = WordStream(log_queue)
    sys.stdout = word_stream

    def run():
        try:
            result = planner_crew.kickoff(inputs=inputs)
            # print("####################planner##########")
            # print(result.raw)
            parsed = json.loads(result.raw)  # 把字符串变成 dict
            pretty_json = json.dumps(parsed, ensure_ascii=False, indent=2)

            session["planner_output"] = json.dumps(parsed, ensure_ascii=False)
            n = 3
            for i in range(0, len(pretty_json), n):
                chunk = pretty_json[i:i+n]
                log_queue.put({"type": "planner_result", "data": chunk})
        except Exception as e:
            log_queue.put({"type": "planner_result", "data": f"[ERROR] {str(e)}"})

    thread = threading.Thread(target=run)
    thread.start()

    try:
        while thread.is_alive() or not log_queue.empty():
            try:
                item = log_queue.get(timeout=0.5)
                if isinstance(item, dict) and "data" in item:
                    item["data"] = strip_ansi(item["data"])
                    yield json.dumps(item, ensure_ascii=False) + "\n"
                else:
                    yield strip_ansi(str(item))
            except queue.Empty:
                continue
    finally:
        sys.stdout = original_stdout
        #print("#########planner###")
        #print(session["planner_output"])





def build_my_crew():
    # 创建内存并共享给所有 agent
    #memory = build_memory_from_history(history)

    crew = Crew(agents=[planner,researcher,reporting_analyst,programmer,educator], 
                tasks=[research_task, reporting_task,code_task,education_task],process=Process.sequential, verbose=True)  # 自定义函数，返回 crew 对象
    return crew

def format_history(history):
    return "\n".join([
        f"{msg['role']}: {msg['content']}" for msg in history
    ])




