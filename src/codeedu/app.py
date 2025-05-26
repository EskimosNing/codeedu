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
OUTPUT_DIR =Path(__file__).parent /  "output"
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
            
            final_output = result.raw
            session["final_result"] = final_output
            n = 3  # 每3个字符为一块
            for i in range(0, len(result.raw), n):
                chunk = result.raw[i:i+n]
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
                    yield json.dumps(item) + "\n"
                else:
                    yield strip_ansi(str(item)) #+ "\n"

            except queue.Empty:
                continue


    finally:
        # 还原 stdout
        sys.stdout = original_stdout
        # 获取最终生成结果并存入内存 + history
        final_result = session.get("final_result", "[EMPTY]")
        final_thought = word_stream.get_thought()
        #session["memory"].chat_memory.add_ai_message(final_result)
        #session["history"].append({"role": "assistant", "content": final_result})
        session["history"].append({"role": "assistant", "content": final_result,"thought": final_thought})
       
        save_conversation(cid, session["history"])

def build_manager_crew():
    return Crew(
        agents=[planner],
        tasks=[distribute_task],
        process=Process.sequential,
        verbose=True
    )

def build_execution_crew(agent_list, task_list):
    return Crew(
        agents=agent_list,
        tasks=task_list,
        process=Process.sequential,
        verbose=True
    )
def format_history(history):
    return "\n".join([f"{item['role']}: {item['content']}" for item in history])

# inputs = {
#     "request": message,
#     "history": format_history(session["history"]),
#     "agents": json.dumps({...}),
#     "tasks": json.dumps({...})
# }
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

    message = request.json['message']
    session = get_or_create_session(cid)
    #memory = session["memory"]
    crew = session["crew"]
    #history = session["history"]
    if not message:
        return jsonify({"error": "消息不能为空"}), 400

    session["history"].append({"role": "user", "content": message})
    print("cid:  ",cid)
    print("################")
    save_conversation(cid, session["history"])

    #history.append({"role": "user", "content": message})
    # 加入内存
    #memory.chat_memory.add_user_message(message)

    # 调用 Crew 执行自然语言对话，并返回
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
    for filename in reversed(os.listdir(STORAGE_PATH)):
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
