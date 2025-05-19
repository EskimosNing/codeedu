from flask import Flask, Response, stream_with_context,render_template,request,jsonify
import sys
import threading
import queue
import io
import time
from crewai import Crew,Agent,Task,Process # 假设你已经有 agents 和 tasks 构建好了
from crewai_tools import SerperDevTool,CodeInterpreterTool,FileWriterTool
#from crewai.llms.openai import OpenAI
import copy
import json
import re
from crewai import LLM
import os
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
os.environ["MODEL"] = os.getenv("MODEL")
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["BASE_URL"] = os.getenv("BASE_URL")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

llm=LLM(model=os.environ["MODEL"],api_key=os.environ["OPENROUTER_API_KEY"],base_url=os.environ["BASE_URL"],streaming=True)


app = Flask(__name__)
CORS(app)
# 队列存储日志
log_queue = queue.Queue()


search_tool=SerperDevTool()
write_tool=FileWriterTool()
researcher = Agent(
    role="{topic} Senior Researcher",
    goal="Uncover cutting-edge developments in {topic}",
    backstory="You're a seasoned researcher with a knack for uncovering the latest developments in {topic}. Known for your ability to find the most relevant information and present it in a clear and concise manner.",
    #human_input=True,
    #memory=True,  # Default: True
    verbose=True,  # Default: False
    allow_delegation=False,  # Default: False
    tools=[search_tool],  # Optional: List of tools
    llm=llm
)
reporting_analyst = Agent(
    role="{topic} Reporting Analyst",
    goal="Create detailed reports based on {topic} data analysis and research findings no longer than 100 words",
    backstory=" You're a meticulous analyst with a keen eye for detail. You're known for your ability to turn complex data into clear and concise reports, making it easy for others to understand and act on the information you provide.",
    #llm="gpt-4",  # Default: OPENAI_MODEL_NAME or "gpt-4
    #memory=True,  # Default: True
    verbose=True,  # Default: False
    allow_delegation=False,  # Default: False
    llm=llm,
    #tools=[write_tool]
)

research_task = Task(
    description="Conduct a thorough research about {topic} Make sure you find any interesting and relevant information given",
    expected_output="A list with 2 bullet points of the most relevant information about {topic}",
    agent=researcher # type: ignore[index]
)

reporting_task = Task(
    description="Review the context you got and expand each topic into a full section for a report. Make sure the report is detailed and contains any and all relevant information.",
    expected_output="A fully fledge reports with the mains topics, each with a full section of information.Formatted as markdown without '```'",
    output_file="output/report.md",
    agent=reporting_analyst # type: ignore[index]
)

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


@app.route("/")
def index():
    return render_template("index.html")

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


if __name__ == "__main__":
    app.run(debug=False,host='127.0.0.1',port=5000)
