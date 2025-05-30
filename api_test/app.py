from flask import Flask, Response, stream_with_context,render_template,request,jsonify
import sys
import threading
import queue
import io
import time
from crewai import Crew,Agent,Task,Process # 假设你已经有 agents 和 tasks 构建好了
from crewai_tools import SerperDevTool,CodeInterpreterTool,FileWriterTool

from langchain_core.memory import ConversationBufferMemory

from langchain_core.prompts import ChatPromptTemplate
import json
import re
import uuid
import glob
from crewai import LLM
import os
from flask_cors import CORS
#from agents import researcher, research_task


app = Flask(__name__)
CORS(app)
STORAGE_PATH = 'conversations'
os.makedirs(STORAGE_PATH, exist_ok=True)

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


def build_memory_from_history(history):
    memory = ConversationBufferMemory(return_messages=True)

    # 加载历史记录，创建 memory
    for item in history:
        if item['role'] == 'user':
            memory.chat_memory.add_user_message(item['content'])
        elif item['role'] == 'assistant':
            memory.chat_memory.add_ai_message(item['content'])
    return memory

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

    def write(self, s):
        self.buffer += s
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

# 实时运行 crew 并把输出放到队列中
def run_crewai_and_stream(crew: Crew, inputs: dict):
    # 保存原始 stdout
    original_stdout = sys.stdout
    
    #sys.stdout = StreamToQueue()
    sys.stdout = WordStream(log_queue)

    def run():
        try:
            result = crew.kickoff(inputs=inputs)  # 调用你自己的 CrewAI 实例
            n = 3  # 每3个字符为一块
            for i in range(0, len(result.raw), n):
                chunk = result.raw[i:i+n]
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
                    yield json.dumps(item) + "\n"
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



def build_my_crew():
    crew = Crew(agents=[researcher], tasks=[research_task],process=Process.sequential, verbose=True)  # 自定义函数，返回 crew 对象
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
    if not message:
        return jsonify({"error": "消息不能为空"}), 400

    
    history = load_conversation(cid)

    history.append({"role": "user", "content": message})

    # 创建 AI 响应
    ai_response = "AI 的回答: " + message  # 这里只是简单的回显消息，可以用 CrewAI 代替
    ai_thought = "AI 的思考: " + message  # 这里只是简单的回显消息，可以用 CrewAI 代替
    history.append({"role": "assistant", "content": ai_response,"thought":ai_thought})

    # 保存更新后的历史
    save_conversation(cid, history)

    return jsonify({"reply": ai_response,"thought":ai_thought})

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
    app.run(debug=False,host='127.0.0.1',port=5000)
