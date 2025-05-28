'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-28 14:57:02
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-28 14:57:25
 # @ Description:
 '''


import sys
import threading
import json
import queue
from .stream import WordStream, strip_ansi
from .file_ops import scan_output_files
from .summarize import summarize_thoughts_stream

log_queue_thought = queue.Queue()
log_queue_result = queue.Queue()

def clear_queue(q: queue.Queue):
    while not q.empty():
        try:
            q.get_nowait()
        except queue.Empty:
            break

def run_crewai_and_stream(crew, inputs: dict, session: dict, cid: str):
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
        while thread.is_alive() or not log_queue_thought.empty():
            for line in word_stream.raw_thought_lines:
                log_queue_thought.put({"type": "raw_thought", "data": strip_ansi(line)})
            word_stream.raw_thought_lines.clear()
            try:
                item = log_queue_thought.get(timeout=0.5)
                yield json.dumps(item, ensure_ascii=False) + "\n"
            except queue.Empty:
                continue

        execution_thought = word_stream.get_thought()
        session["execution_thought"] = execution_thought
        summary_text = ""
        for chunk in summarize_thoughts_stream(execution_thought):
            parsed = json.loads(chunk)
            if parsed.get("type") == "thought":
                summary_text += parsed["data"]
                yield json.dumps(parsed, ensure_ascii=False) + "\n"

        while not log_queue_result.empty():
            yield json.dumps(log_queue_result.get(timeout=0.5), ensure_ascii=False) + "\n"

        files_after = scan_output_files()
        new_files = files_after - files_before
        if new_files:
            file_infos = [{"filename": f, "download_url": f"{f}"} for f in new_files]
            session["file_infos"] = file_infos
            yield json.dumps({"type": "file_list", "files": file_infos}, ensure_ascii=False) + "\n"

    finally:
        sys.stdout = original_stdout
