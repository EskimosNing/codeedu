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
from flask_cors import CORS
from agent_pool import researcher,programmer,reporting_analyst,planner,educator
from task import distribute_task, code_task, reporting_task, tasks_config,research_task,education_task
#src.codeedu.task 
from pathlib import Path

app = Flask(__name__)
CORS(app)
STORAGE_PATH = Path(__file__).parent / "conversations" 
#print(STORAGE_PATH)
#print("**********")
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
        print("####################################")
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

# 清除颜色控制字符
def strip_ansi(text):
    return ansi_escape.sub('', text)


<<<<<<< HEAD:src/codeedu/app copy.py
=======

# def clean_for_json(text: str) -> str:
#     """清理 ANSI 控制符、替换双引号、转义换行"""
#     text = ansi_escape.sub('', text)


    
#     text = text.replace('"', '\\"')         # 转义双引号
#     text = text.replace('\r', '')           # 去除回车
#     text = text.replace('\n', '\\n')        # 转义换行
#     return text

>>>>>>> 5b55d15 (update app.py thought log text ascii):src/codeedu/app_developing.py
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

    def write(self, s):
<<<<<<< HEAD:src/codeedu/app copy.py
        self.buffer += s
        self.result_buffer += s
=======
        

        # 安全清洗并保存到思考缓冲区
        #clean_s = strip_ansi(s)
        try:
            decoded = json.loads(s)
            if isinstance(decoded, str):
                self.buffer += decoded
                self.result_buffer += decoded
                self.thought_buffer += decoded
            else:
                self.buffer += json.dumps(decoded, ensure_ascii=False)
                self.result_buffer += json.dumps(decoded, ensure_ascii=False)
                self.thought_buffer += json.dumps(decoded, ensure_ascii=False)
        except:
            self.buffer += s
            self.result_buffer += s
            self.thought_buffer += s

>>>>>>> 5b55d15 (update app.py thought log text ascii):src/codeedu/app_developing.py
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
    def get_result(self):
        return self.result_buffer

# 实时运行 crew 并把输出放到队列中
def run_crewai_and_stream(crew: Crew, inputs: dict,session:dict,cid):
    # 保存原始 stdout
    original_stdout = sys.stdout
    
    #sys.stdout = StreamToQueue()
    word_stream = WordStream(log_queue)
    sys.stdout = word_stream

    def run():
        try:
            result = crew.kickoff(inputs=inputs)  # 调用你自己的 CrewAI 实例
<<<<<<< HEAD:src/codeedu/app copy.py
=======
            # print("####################planner##########")
            # print(result.raw)
            parsed = json.loads(result.raw)  # 把字符串变成 dict
            pretty_json = json.dumps(parsed, ensure_ascii=False, indent=2)

            session["final_result"] = json.dumps(parsed, ensure_ascii=False)
            #raw_output = result.raw
            #session["final_result"] = raw_output
>>>>>>> 5b55d15 (update app.py thought log text ascii):src/codeedu/app_developing.py
            n = 3  # 每3个字符为一块
            for i in range(0, len(pretty_json), n):
                chunk = pretty_json[i:i+n]
                log_queue.put({"type": "result", "data": chunk})
            #print("RESULT:", result)
            #log_queue.put({"type": "result", "data": result.raw})
        except Exception as e:
            log_queue.put({"type": "result", "data": f"[ERROR] {str(e)}"})


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
                #yield f"data: {line}\n\n"  # Server-Sent Events 格式
                #yield f"{json.dumps(item)}"  # 每行为一条 JSON
            except queue.Empty:
                continue
        #thread.join()
        #thread.close()  ################

    finally:
        # 还原 stdout
        sys.stdout = original_stdout
        # 获取最终生成结果并存入内存 + history
<<<<<<< HEAD:src/codeedu/app copy.py
        final_result = word_stream.get_result()
=======
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
>>>>>>> 5b55d15 (update app.py thought log text ascii):src/codeedu/app_developing.py
        #session["memory"].chat_memory.add_ai_message(final_result)
        #session["history"].append({"role": "assistant", "content": final_result})
        session["history"].append({"role": "assistant", "content": final_result})
       
        save_conversation(cid, session["history"])

<<<<<<< HEAD:src/codeedu/app copy.py
=======
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



>>>>>>> 5b55d15 (update app.py thought log text ascii):src/codeedu/app_developing.py


def build_my_crew():
    # 创建内存并共享给所有 agent
    #memory = build_memory_from_history(history)

    crew = Crew(agents=[planner,researcher,reporting_analyst,programmer,educator], 
                tasks=[research_task, reporting_task,code_task,education_task],process=Process.sequential, verbose=True)  # 自定义函数，返回 crew 对象
    return crew

# def send_from_directory(directory, filename):
#     return send_file(os.path.join(directory, filename))

# def send_file(path):
#     return send_from_directory(STORAGE_PATH, path)

# 发送消息并更新对话历史
@app.route('/chat', methods=['POST'])
def chat():
    cid = request.json['conversation_id']
    #print(cid)
    #print("*********")
    message = request.json['message']
    session = get_or_create_session(cid)
    #memory = session["memory"]
    crew = session["crew"]
    #history = session["history"]
    if not message:
        return jsonify({"error": "消息不能为空"}), 400

    session["history"].append({"role": "user", "content": message})
    save_conversation(cid, session["history"])
    #history.append({"role": "user", "content": message})
    # 加入内存
    #memory.chat_memory.add_user_message(message)

<<<<<<< HEAD:src/codeedu/app copy.py
    # 调用 Crew 执行自然语言对话，并返回
=======
    

    planner_inputs = {
        "user_input": message,
        "history": format_history(session["history"]),
        "agents": json.dumps({
            "Agents": [{"id": item["id"], "configuration": item["configuration"]} 
                       for item in agents_dict.values()]
                },ensure_ascii=False),
        "tasks": json.dumps({
            "Tasks": [{"id": item["id"], "configuration": item["configuration"]} 
                      for item in tasks_dict.values()]
                },ensure_ascii=False),
    }

    def multi_stage_streaming():
        # Step 1: Run planner stage and stream result
        manager_crew = Crew(
            agents=[planner],
            tasks=[distribute_task],
            process=Process.sequential,
            verbose=True
        )

        yield from run_planner_and_stream(manager_crew, planner_inputs, session)

        # Step 2: Parse planner result
        try:
            parsed = json.loads(session.get("planner_output", "{}"))
            agent_ids = [a["id"] for a in parsed["distribution_config"]["agents"]]
            task_ids = [t["id"] for t in parsed["distribution_config"]["tasks"]]

            summary_msg = (
                f"\n[🧠 Planner 分配结果]\n"
                f"将使用以下 Agent：{', '.join(agent_ids)}\n"
                f"对应任务：{', '.join(task_ids)}\n\n"
            )
            log_queue.put({"type": "planner_result", "data": summary_msg})

            dynamic_agents = [agents_dict[aid]["agent"] for aid in agent_ids]
            dynamic_tasks = [tasks_dict[tid]["task"] for tid in task_ids]

        except Exception as e:
            yield json.dumps({"type": "planner_result", "data": f"[ERROR]: {str(e)}"}, ensure_ascii=False) + "\n"
            return

        # Step 3: Run execution phase
        execution_crew = Crew(
            agents=dynamic_agents,
            tasks=dynamic_tasks,
            process=Process.sequential,
        
            verbose=True
        )

        yield from run_crewai_and_stream(
            crew=execution_crew,
            inputs={"user_input": message},
            session=session,
            cid=cid
        )

>>>>>>> 5b55d15 (update app.py thought log text ascii):src/codeedu/app_developing.py
    return Response(
        stream_with_context(run_crewai_and_stream(crew, {'question': message},session,cid)),
        mimetype="text/plain"
    )
    # result = crew.kickoff(inputs={'question': message})
    # memory.chat_memory.add_ai_message(result.raw)
    # history.append({"role": "assistant", "content": result.raw})

    # # 创建 AI 响应
    # #ai_response = "AI 的回答: " + message  # 这里只是简单的回显消息，可以用 CrewAI 代替
    # #ai_thought = "AI 的思考: " + message  # 这里只是简单的回显消息，可以用 CrewAI 代替
    # #history.append({"role": "assistant", "content": result.raw,"thought":ai_thought})

    # # 保存更新后的历史
    # save_conversation(cid, history)

    # #return jsonify({"reply": result.raw,"thought":ai_thought})
    # return jsonify({"reply": result.raw})

@app.route("/upload_code", methods=["POST"])
def upload_code():
    file = request.files["file"]
    cid = request.form["conversation_id"]

    session = get_or_create_session(cid)
    memory = session["memory"]

    code = file.read().decode("utf-8")
    memory.chat_memory.add_user_message(f"这是用户上传的代码：\n```python\n{code}\n```")

    return jsonify({"message": "代码已添加到上下文中。"})


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
@app.route("/")
def index():
    return render_template("index2.html")


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
