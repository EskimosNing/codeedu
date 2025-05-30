'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-29 19:34:51
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-29 19:52:03
 # @ Description:
 '''

import sys
import threading
import queue
import json
from crewai import Crew
from core.stream import WordStream, clear_queue, strip_ansi
from core.output import scan_output_files,detect_new_files
from utils.intention import summarize_thoughts_stream
#from config.paths import STORAGE_PATH, OUTPUT_PATH
from utils.session import save_conversation
from utils.log_queues import log_queue_result,log_queue_thought





def run_chatcrew_and_stream(crew: Crew, inputs: dict,session:dict,cid:str):
    original_stdout = sys.stdout
    word_stream = WordStream()
    sys.stdout = word_stream
    

    def run():
        try:
            result = crew.kickoff(inputs=inputs) 
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

            
            

        #  输出 result（在 thought 之后）
        while not log_queue_result.empty():
            yield json.dumps(log_queue_result.get(timeout=2), ensure_ascii=False) + "\n"




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
            result = crew.kickoff(inputs=inputs)  
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

        



    finally:
        # 还原 stdout
        sys.stdout = original_stdout
        new_files = detect_new_files(files_before) 
        if new_files:
            file_infos = []
            for file in new_files:
                file_infos.append({
                        "filename": file,
                        "download_url": f"{file}"
                    })
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
        new_files = detect_new_files(files_before) 
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
