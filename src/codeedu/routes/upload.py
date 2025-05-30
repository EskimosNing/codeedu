'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-29 22:21:46
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-29 22:22:05
 # @ Description:upload.py
 '''


from flask import Blueprint, request, jsonify, Response, stream_with_context,send_from_directory
import os
from crewai import Crew,Process
from utils.log_queues import log_queue_thought, log_queue_result
from core.executor import run_code_analysis_and_stream
from utils.session import get_or_create_session, save_conversation
from core.stream import clear_queue
from config.paths import OUTPUT_PATH
from agent_pool import executor
from task import code_analysis_task

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload_code", methods=["POST"])
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


@upload_bp.route("/execute_code_snippet", methods=["POST"])
def execute_code_snippet():
    file = request.files.get("file")
    cid = request.form.get("conversation_id")
    
    if not file or file.filename == "":
        return jsonify({"error": "未提供有效文件"}), 400

    session = get_or_create_session(cid)
    save_path = os.path.join(OUTPUT_PATH, file.filename)
    file.save(save_path)

    with open(save_path, "r", encoding="utf-8") as f:
        code_content = f.read()

    session["history"].append({
        "role": "user",
        "content": f"```python\n{code_content}\n```"
    })
    save_conversation(cid, session["history"])

    clear_queue(log_queue_thought)
    clear_queue(log_queue_result)

    return Response(
        stream_with_context(
            run_code_analysis_and_stream(
                crew=Crew(agents=[executor], tasks=[code_analysis_task],process=Process.sequential,verbose=True),
                inputs={"path": save_path},
                session=session,
                cid=cid
            )
        ),
        mimetype="text/plain"
    )


# 
@upload_bp.route('/output/<filename>', methods=['GET'])
def download_output_file(filename):
    return send_from_directory('output', filename, as_attachment=True)