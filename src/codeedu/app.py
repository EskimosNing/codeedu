'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-26 17:54:25
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-28 14:08:11
 # @ Description: @Deprecated
 '''

from flask import Flask, Response, stream_with_context,request,jsonify
import sys
import threading
import queue
import io
import time
from crewai import Crew,Agent,Task,Process # 假设你已经有 agents 和 tasks 构建好了
from crewai_tools import SerperDevTool,CodeInterpreterTool,FileWriterTool

#from langchain.memory import ConversationBufferMemory

#from langchain_core.prompts import ChatPromptTemplate
import json
import re
import uuid
import glob
from crewai import LLM
import os
import html
from flask import send_from_directory
from flask_cors import CORS
from agent_pool import planner, researcher, reporting_analyst, programmer, educator,agents_config,executor,chat_agent
from task import distribute_task, code_task, reporting_task, tasks_config,research_task,education_task,code_analysis_task,generate_quiz_task,greeting_task
from utils.intention import should_greet_or_chitchat,summarize_thoughts_stream
#src.codeedu.task 
from pathlib import Path

app = Flask(__name__)
CORS(app)
OUTPUT_DIR =Path(__file__).parent / "output"
STORAGE_PATH = Path(__file__).parent / "conversations" 
#print(STORAGE_PATH)
#print("**********")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STORAGE_PATH, exist_ok=True)
  # user_id or convo_id → {'crew': ..., 'memory': ..., 'history': [...]}
# 队列存储日志
#log_queue = queue.Queue()
log_queue_thought = queue.Queue()
log_queue_result = queue.Queue()
internal_thought_log = [] #记录 raw_thought

agents_dict = {
  'researcher': {"id": "researcher", "configuration": agents_config["researcher"], "agent": researcher},
  'reporting_analyst': {"id": "reporting_analyst", "configuration": agents_config["reporting_analyst"], "agent": reporting_analyst},
  'programmer': {"id": "programmer", "configuration": agents_config["programmer"], "agent": programmer},
  'educator': {"id": "educator", "configuration": agents_config["educator"], "agent": educator},
  #'executor': {"id": "executor", "configuration": agents_config["executor"], "agent": executor},
}
#print("agents_dict: ",agents_dict)
tasks_dict = {
  'research_task': {"id": "research_task", "configuration": tasks_config["research_task"], "task": research_task},
  'reporting_task': {"id": "reporting_task", "configuration": tasks_config["reporting_task"], "task": reporting_task},
  'code_task': {"id": "code_task", "configuration": tasks_config["code_task"], "task": code_task},
  'education_task': {"id": "education_task", "configuration": tasks_config["education_task"], "task": education_task},
  'generate_quiz_task':{"id": "generate_quiz_task", "configuration": tasks_config["generate_quiz_task"], "task": generate_quiz_task},
}
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

# 匹配 ANSI 转义序列的正则
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
#box_drawing = re.compile(r'[─╮╯╰│╭╮╯╰]+')
# 清除颜色控制字符
def strip_ansi(text):
    return ansi_escape.sub('', text)
def clear_queue(q: queue.Queue):
    while not q.empty():
        try:
            q.get_nowait()
        except queue.Empty:
            break

class WordStream(io.StringIO):
    def __init__(self):
        super().__init__()
        self.result_buffer = ""
        self.thought_buffer = ""
        self.raw_thought_lines = []  # 👈 保存每行日志

    def write(self, s):
        self.result_buffer += s
        self.thought_buffer += s
        # 实时收集，但不推送
        lines = s.splitlines(keepends=True)
        for line in lines:
            if line.strip():
                self.raw_thought_lines.append(line)

    def get_thought(self):
        return "\n".join(self.raw_thought_lines)

    def get_result(self):
        return strip_ansi(self.result_buffer)



def scan_output_files():
    output_dir = Path("output")
    return set(str(f) for f in output_dir.glob("*") if f.is_file())


# def summarize_thoughts_stream(thought_text):
#     from openai import OpenAI  # 或其他你用的 LLM 接口
#     import openai

#     client = openai.OpenAI(api_key=os.environ["OPENROUTER_API_KEY"],base_url=os.environ["BASE_URL"])

#     # 用 streaming 模式调用模型总结
#     response = client.chat.completions.create(
#         model=os.environ["OTHER_MODEL"],  # or gpt-4o-mini
#         messages=[
#             {
#                 "role": "system",
#                 "content": (
#                     "你是一个 AI 观察记录员，负责将多位 AI Agent 的任务执行过程，"
#                     "以结构清晰、容易理解的格式总结出来。"
#                     "\n\n"
#                     "你应该模仿 CrewAI 的 `thought` 日志风格，用中文表达，但要逻辑清楚、简明易懂。\n"
#                     "请使用以下结构来组织输出：\n"
#                     "1. 总览：本次任务的主要目标是什么；\n"
#                     "2. 分配：哪些 Agent 被分配到哪些任务；\n"
#                     "3. 执行：各个 Agent 是如何执行这些任务的，有没有使用工具，工具输出了什么；\n"
#                     "4. 结果简述：总结整体输出结果，是否成功，是否产生文件；\n"
#                     "5. 若有必要，补充关键逻辑或注意事项。\n\n"
#                     "风格上可以模仿 CrewAI 思考日志，但要更清楚更适合用户阅读，不要逐字复述原始输出。"
#                 )
#             },
#             {
#                 "role": "user",
#                 "content": (
#                     f"以下是 AI agents 在任务执行过程中的原始日志：\n\n{thought_text}\n\n"
#                     "请根据上面结构总结输出："
#                 )
#             }
#         ],
#         stream=True,
#         temperature=0.5
#     )
    
#     # 流式返回
#     for chunk in response:
#         delta = chunk.choices[0].delta
#         if hasattr(delta, "content") and delta.content:
#             yield json.dumps({"type": "thought", "data": delta.content}, ensure_ascii=False) + "\n"

def run_chatcrew_and_stream(crew: Crew, inputs: dict,session:dict,cid:str):
    original_stdout = sys.stdout
    word_stream = WordStream()
    sys.stdout = word_stream
    #files_before = set(scan_output_files())  # 执行前文件列表

    def run():
        try:
            result = crew.kickoff(inputs=inputs)  # 调用你自己的 CrewAI 实例
            session["final_result"] = result.raw
            
            for i in range(0, len(result.raw), 3):
                chunk = result.raw[i:i+3]
                log_queue_result.put({"type": "result", "data": chunk})
        except Exception as e:
            err = f"[ERROR] {str(e)}"
            log_queue_result.put({"type": "result", "data": f"[ERROR] {str(e)}"})
            session["final_result"] = err


    thread = threading.Thread(target=run)
    thread.start()

    try:
        while thread.is_alive() or not log_queue_thought.empty():
            for line in word_stream.raw_thought_lines:
                log_queue_thought.put({"type": "raw_thought", "data": strip_ansi(line)})
            word_stream.raw_thought_lines.clear()
            try:
                item = log_queue_thought.get(timeout=0.1)
                yield json.dumps(item, ensure_ascii=False) + "\n"
            except queue.Empty:
                continue
        # #  任务完成后，总结 execution thought
        # execution_thought = word_stream.get_thought()
        # session["execution_thought"] = execution_thought

        
        # for chunk in summarize_thoughts_stream(execution_thought):
        #     parsed = json.loads(chunk)
        #     if parsed.get("type") == "thought":
        #         log_queue_thought.put(parsed)  # 优先展示 thought

        # #  输出 summary thought
        # while not log_queue_thought.empty():
        #     yield json.dumps(log_queue_thought.get(timeout=0.5), ensure_ascii=False) + "\n"
            
            

        #  输出 result（在 thought 之后）
        while not log_queue_result.empty():
            yield json.dumps(log_queue_result.get(timeout=2), ensure_ascii=False) + "\n"

        # files_after = scan_output_files()
        # new_files = files_after - files_before
        # if new_files:
        #     file_infos = [{"filename": f, "download_url": f"{f}"} for f in new_files]
        #     session["file_infos"] = file_infos
        #     yield json.dumps({"type": "file_list", "files": file_infos}, ensure_ascii=False) + "\n"


    finally:
        # 还原 stdout
        sys.stdout = original_stdout
        session["history"].append({"role": "assistant", "content": session.get("final_result", ""),})
        save_conversation(cid, session["history"])

# 实时运行 crew 并把输出放到队列中
def run_crewai_and_stream(crew: Crew, inputs: dict,session:dict,cid:str):
    original_stdout = sys.stdout
    word_stream = WordStream()
    sys.stdout = word_stream
    files_before = set(scan_output_files())  # 执行前文件列表

    def run():
        try:
            result = crew.kickoff(inputs=inputs)  # 调用你自己的 CrewAI 实例
            session["final_result"] = result.raw
            
            for i in range(0, len(result.raw), 3):
                chunk = result.raw[i:i+3]
                log_queue_result.put({"type": "result", "data": chunk})
        except Exception as e:
            err = f"[ERROR] {str(e)}"
            log_queue_result.put({"type": "result", "data": f"[ERROR] {str(e)}"})
            session["final_result"] = err


    thread = threading.Thread(target=run)
    thread.start()

    try:
        while thread.is_alive() or not log_queue_thought.empty():
            for line in word_stream.raw_thought_lines:
                log_queue_thought.put({"type": "raw_thought", "data": strip_ansi(line)})
            word_stream.raw_thought_lines.clear()
            try:
                item = log_queue_thought.get(timeout=0.1)
                yield json.dumps(item, ensure_ascii=False) + "\n"
            except queue.Empty:
                continue
        #  任务完成后，总结 execution thought
        execution_thought = word_stream.get_thought()
        session["execution_thought"] = execution_thought

        
        # for chunk in summarize_thoughts_stream(execution_thought):
        #     parsed = json.loads(chunk)
        #     if parsed.get("type") == "thought":
        #         log_queue_thought.put(parsed)  # 优先展示 thought

        # #  输出 summary thought
        # while not log_queue_thought.empty():
        #     yield json.dumps(log_queue_thought.get(timeout=0.5), ensure_ascii=False) + "\n"
            
            

        # #  输出 result（在 thought 之后）
        # while not log_queue_result.empty():
        #     yield json.dumps(log_queue_result.get(timeout=0.5), ensure_ascii=False) + "\n"

        # files_after = scan_output_files()
        # new_files = files_after - files_before
        # if new_files:
        #     file_infos = [{"filename": f, "download_url": f"{f}"} for f in new_files]
        #     session["file_infos"] = file_infos
        #     yield json.dumps({"type": "file_list", "files": file_infos}, ensure_ascii=False) + "\n"


    finally:
        # 还原 stdout
        sys.stdout = original_stdout
        # 获取最终生成结果并存入内存 + history
        # print("####################excu##########")
        # print(session["final_result"])
        

        files_after = scan_output_files()
        new_files = files_after - files_before
        if new_files:
            #session['file_flag']=True
            file_infos = []
            for file in new_files:
                file_infos.append({
                        "filename": file,
                        "download_url": f"{file}"
                    })
            #print("####################file_infos##########")
            #print(file_infos)
            #  通知前端文件信息

            # yield json.dumps({
            #     "type": "file_list",
            #     "files": file_infos
            # }, ensure_ascii=False) + "\n"
            session['file_infos']=file_infos


def run_planner_and_stream(planner_crew: Crew, inputs: dict, session: dict):
    original_stdout = sys.stdout
    word_stream = WordStream()
    sys.stdout = word_stream
    

    def run():
        try:
            result = planner_crew.kickoff(inputs=inputs)
            session["planner_output"] = result.raw
            
        except Exception as e:
            session["planner_output"] = f"[ERROR] {str(e)}"
        #     for i in range(0, len(result.raw), 3):
        #         log_queue_result.put({"type": "result", "data": result.raw[i:i+3]})
        # except Exception as e:
        #     log_queue_result.put({"type": "result", "data": f"[ERROR] {str(e)}"})

    thread = threading.Thread(target=run)
    thread.start()

    try:
        while thread.is_alive() or not log_queue_thought.empty():
            # 实时将 WordStream 中的 thought 送入 log_queue_thought
            for line in word_stream.raw_thought_lines:
                log_queue_thought.put({"type": "raw_thought", "data": strip_ansi(line)})
            word_stream.raw_thought_lines.clear()
            try:
                # 输出前面 planner 阶段产生的 thought 日志
                yield json.dumps(log_queue_thought.get(timeout=0.1), ensure_ascii=False) + "\n"
            except queue.Empty:
                continue
        #  总结 planner 思考，插入到 thought 队列中（优先输出）

        planner_thought = word_stream.get_thought()
        session["planner_thought"] = planner_thought
        # for chunk in summarize_thoughts_stream(planner_thought):
        #     parsed = json.loads(chunk)
        #     if parsed.get("type") == "thought":
        #         log_queue_thought.put(parsed)

        # # 将最终 summary 也 yield 出去
        # while not log_queue_thought.empty():
        #     yield json.dumps(log_queue_thought.get(timeout=0.5), ensure_ascii=False) + "\n"
    finally:
        sys.stdout = original_stdout

def run_code_analysis_and_stream(crew: Crew, inputs: dict, session: dict, cid: str):
    original_stdout = sys.stdout
    word_stream = WordStream()
    sys.stdout = word_stream
    files_before = set(scan_output_files())

    def run():
        try:
            result = crew.kickoff(inputs=inputs)
            session["final_result"] = result.raw
            for i in range(0, len(result.raw), 3):
                chunk = result.raw[i:i+3]
                log_queue_result.put({"type": "result", "data": chunk})
        except Exception as e:
            err = f"[ERROR] {str(e)}"
            session["final_result"] = err
            log_queue_result.put({"type": "result", "data": err})

    thread = threading.Thread(target=run)
    thread.start()

    try:
        # 实时记录 raw thought 日志
        while thread.is_alive() or not log_queue_thought.empty():
            for line in word_stream.raw_thought_lines:
                log_queue_thought.put({"type": "raw_thought", "data": strip_ansi(line)})
            word_stream.raw_thought_lines.clear()
            try:
                item = log_queue_thought.get(timeout=0.1)
                yield json.dumps(item, ensure_ascii=False) + "\n"
            except queue.Empty:
                continue

        # 总结 execution thought
        execution_thought = word_stream.get_thought()
        session["execution_thought"] = execution_thought
        summary_text = ""
        for chunk in summarize_thoughts_stream(execution_thought):
            parsed = json.loads(chunk)
            if parsed.get("type") == "thought":
                summary_text += parsed["data"]
                yield json.dumps(parsed, ensure_ascii=False) + "\n"

        # 输出 result
        while not log_queue_result.empty():
            yield json.dumps(log_queue_result.get(timeout=2), ensure_ascii=False) + "\n"

        # 输出文件列表
        files_after = scan_output_files()
        new_files = files_after - files_before
        if new_files:
            file_infos = [{"filename": f, "download_url": f"{f}"} for f in new_files]
            session["file_infos"] = file_infos
            yield json.dumps({"type": "file_list", "files": file_infos}, ensure_ascii=False) + "\n"

        # 保存历史
        session["history"].append({
            "role": "assistant",
            "content": session.get("final_result", ""),
            "thought": summary_text,
            "files": session.get("file_infos", [])
        })
        save_conversation(cid, session["history"])

    finally:
        sys.stdout = original_stdout


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
import re
def extract_json_from_text(text):
    try:
        # 提取最外层 JSON
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            raise ValueError("No JSON object found")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON Decode Error: {e}")

# 发送消息并更新对话历史
@app.route('/chat', methods=['POST'])
def chat():
    clear_queue(log_queue_thought)
    clear_queue(log_queue_result)
    cid = request.json['conversation_id']
    message = request.json['message'].strip()
    session = get_or_create_session(cid)
    #memory = session["memory"]
    #history = session["history"]
    if not message:
        return jsonify({"error": "消息不能为空"}), 400
    
    
    
    session["history"].append({"role": "user", "content": message})
    save_conversation(cid, session["history"])



    # ---------------------- 自动判断是否是闲聊/问候 ----------------------
    if should_greet_or_chitchat(message):  #  自动使用 LLM 判断
        # 构建轻量 Crew 执行简单问候任务
        execution_inputs = {
            "user_input": message,
            "context": format_history(session["history"]),
        }

        crew = Crew(
            agents=[chat_agent],
            tasks=[greeting_task],
            process=Process.sequential,
            verbose=True
        )
        return Response(
            stream_with_context(
                run_chatcrew_and_stream(
                    crew=crew,
                    inputs=execution_inputs,
                    session=session,
                    cid=cid
                )
            ),
            mimetype="text/plain"
        )

    # ---------------------- 进入正常 planner 分配流程 ----------------------

    planner_inputs = {
        "user_input": message,
        "context": format_history(session["history"]),
        "agents": json.dumps({
            "Agents": [{"id": item["id"], "configuration": item["configuration"]} 
                       for item in agents_dict.values()]
                },ensure_ascii=False),
        "tasks": json.dumps({
            "Tasks": [{"id": item["id"], "configuration": item["configuration"]} 
                      for item in tasks_dict.values()]
                },ensure_ascii=False),
    }
    # print(">>>> AGENTS JSON >>>>")
    # print(planner_inputs["agents"])
    # print(">>>> TASKS JSON >>>>")
    # print(planner_inputs["tasks"])

    def multi_stage_streaming():
        # Step 1: Planner

        manager_crew = Crew(
            agents=[planner],
            tasks=[distribute_task],
            process=Process.sequential,
            verbose=True
        )
        yield from run_planner_and_stream(manager_crew, planner_inputs, session)
 
        # Step 2: Parse Planner Result
        try:
            #print(session.get("planner_output", "{}"))
            parsed = extract_json_from_text(session.get("planner_output", ""))
            #print("#######")
            #print(parsed)
            agent_ids = [a["id"] for a in parsed["distribution_config"]["agents"]]
            task_ids = [t["id"] for t in parsed["distribution_config"]["tasks"]]

            log_queue_thought.put({"type": "thought", "data": f"\n[ Planner 分配结果] 使用 Agent: {agent_ids}, 任务: {task_ids}\n"})
            json.dumps({"type": "thought", "data": f"\n[ Planner 分配结果] 使用 Agent: {agent_ids}, 任务: {task_ids}\n"}, ensure_ascii=False) + "\n"
            dynamic_agents = [agents_dict[aid]["agent"] for aid in agent_ids]
            dynamic_tasks = [tasks_dict[tid]["task"] for tid in task_ids]
        except Exception as e:
            yield json.dumps({"type": "thought", "data": f"[ERROR]: {str(e)}"}, ensure_ascii=False) + "\n"
            return

        # Step 3: 执行任务
        execution_inputs = {
            "user_input": message,
            "context": format_history(session["history"]),
        }
        execution_crew = Crew(
            agents=dynamic_agents,
            tasks=dynamic_tasks,
            process=Process.sequential,
            verbose=True
        )

        yield from run_crewai_and_stream(execution_crew, execution_inputs, session, cid)
        #session["execution_thought"] = exec_stream.get_thought()


        # Step 4: 总结 Planner + Execution
        full_thought = (
            session.get("planner_thought", "") + "\n" +
            session.get("execution_thought", "")
        )
        summary_text = ""
        for chunk in summarize_thoughts_stream(full_thought):
            parsed = json.loads(chunk)
            if parsed.get("type") == "thought":
                summary_text += parsed["data"]
                # 总结也伪装成 Thought Log 提前输出
                yield json.dumps(parsed, ensure_ascii=False) + "\n"
         # Step 5: result 输出
        while not log_queue_result.empty():
            yield json.dumps(log_queue_result.get(timeout=2), ensure_ascii=False) + "\n"

        # Step 6: 文件
        if "file_infos" in session:
            yield json.dumps({
                "type": "file_list",
                "files": session["file_infos"]
            }, ensure_ascii=False) + "\n"

        # Step 7: 保存历史
        session["history"].append({
            "role": "assistant",
            "content": session.get("final_result", ""),
            "thought": summary_text,
            "files": session.get("file_infos", [])
        })
        
        save_conversation(cid, session["history"])


    return Response(
        stream_with_context(multi_stage_streaming()),
        mimetype="text/plain"
    )

@app.route('/output/<filename>', methods=['GET'])
def download_output_file(filename):
    return send_from_directory('output', filename, as_attachment=True)

@app.route("/upload_code", methods=["POST"])
def upload_code():
    file = request.files["file"]
    cid = request.form["conversation_id"]
    session = get_or_create_session(cid)

    # 文件注入到历史
    code = file.read().decode("utf-8")
    code_msg = f"用户上传了一段代码如下：\n```python\n{code}\n```"
    session["history"].append({"role": "user", "content": code_msg})
    save_conversation(cid, session["history"])

    return jsonify({"message": "代码已注入上下文成功"})


@app.route('/execute_code_snippet', methods=['POST'])
def execute_code_snippet():
    cid = request.form["conversation_id"]
    session = get_or_create_session(cid)

    if 'file' not in request.files:
        return jsonify({"error": "未提供文件"}), 400
    file = request.files["file"]
    if file.filename == '':
        return jsonify({"error": "文件名为空"}), 400

    # 保存文件
    save_path = os.path.join(OUTPUT_DIR, file.filename)
    file.save(save_path)
    # print(save_path)

    # 保存文件内容到历史中（markdown）
    with open(save_path, "r", encoding="utf-8") as f:
        code_content = f.read()
    #print(code_content)
    session["history"].append({
        "role": "user",
        "content": f"```python\n{code_content}\n```"
    })
    save_conversation(cid, session["history"])

    # 构造 Crew
    direct_crew = Crew(
        agents=[executor],
        tasks=[code_analysis_task],
        process=Process.sequential,
        verbose=True
    )

    # 清空队列
    clear_queue(log_queue_thought)
    clear_queue(log_queue_result)

    # 启动流式响应（调用新函数）
    return Response(
        stream_with_context(
            run_code_analysis_and_stream(
                crew=direct_crew,
                inputs={"path": save_path},
                session=session,
                cid=cid
            )
        ),
        mimetype="text/plain"
    )



@app.route('/submit_code', methods=['POST'])
def submit_code():
    data = request.json
    code = data.get("code", "")

    if not code:
        return jsonify({"error": "未提交代码"}), 400

    # 通过 CrewAI 调度任务执行
    crew = build_my_crew()
    result, suggestion = crew.kickoff(inputs={"code": code})

    return jsonify({
        "result": result,
        "suggestions": suggestion
    })


# --- 页面路由 ---
# @app.route("/")
# def index():
#     return render_template("index2.html")


# --- 会话管理 ---
@app.route('/new_conversation', methods=['POST'])
def new_conversation():
    user_id = request.json.get("user_id", "default")
    message = request.json.get("message", "")
    cid = str(uuid.uuid4())
    save_conversation(cid, [])
    return jsonify({"conversation_id": cid, "title":message[:50]})


@app.route('/conversations', methods=['GET'])
def get_conversations():
    if not os.path.exists(STORAGE_PATH):
        return jsonify([])

    conversations = []
    for filename in os.listdir(STORAGE_PATH):
        if filename.endswith(".json") and not filename.endswith(".meta.json"):
            cid = filename.replace(".json", '')
            title = "(未命名)"

            meta_path = os.path.join(STORAGE_PATH, f"{cid}.meta.json")
            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                    title = metadata.get("title", title)
            else:
                # 兼容旧文件：尝试读取第一句话
                try:
                    with open(os.path.join(STORAGE_PATH, filename), "r", encoding="utf-8") as f:
                        history = json.load(f)
                        title = next((m["content"] for m in history if m["role"] == "user"), title)
                except:
                    pass

            conversations.append({
                "id": cid,
                "title": title.strip()
            })

    return jsonify(conversations)


#获取对话历史   
@app.route('/conversation/<cid>', methods=['GET'])
def get_conversation_history(cid):
    convo_path = get_convo_path(cid)

    if not os.path.exists(convo_path):
        return jsonify({"error": "对话不存在"}), 404

    with open(convo_path, "r", encoding="utf-8") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            return jsonify({"error": "对话数据格式错误"}), 500

    return jsonify(history)


@app.route("/answer",methods=["GET"])
def answer():
    message = request.args.get("message", "")
    #message = data["message"]
    # 这里你应该提前构建好 crew 实例和 inputs 参数
    crew = build_my_crew()  # 自定义函数，返回 crew 对象
    inputs = {"topic": message}  # 示例 inputs
    return Response(
        stream_with_context(run_crewai_and_stream(crew, inputs)),
        mimetype="text/plain"
    )

#删除对话
@app.route("/delete_conversation/<cid>", methods=["DELETE"])
def delete_conversation(cid):
    convo_path = get_convo_path(cid)

    if os.path.exists(convo_path):
        os.remove(convo_path)

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0',port=5000)
