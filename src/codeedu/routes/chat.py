'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-29 21:46:31
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-29 21:47:15
 # @ Description:
 '''

from flask import Blueprint, Response, request, stream_with_context, jsonify
import json
import re
from crewai import Crew, Process
from utils.session import get_or_create_session, save_conversation
from utils.log_queues import log_queue_thought, log_queue_result
from utils.intention import should_greet_or_chitchat, summarize_thoughts_stream
from core.executor import (
    run_chatcrew_and_stream,
    run_crewai_and_stream,
    run_planner_and_stream
)
from core.stream import clear_queue
from core.registry import agents_dict, tasks_dict
from agent_pool import planner, chat_agent
from task import distribute_task, greeting_task

chat_bp = Blueprint('chat', __name__)

def format_history(history):
    return "\n".join([
        f"{msg['role']}: {msg['content']}" for msg in history
    ])

def extract_json_from_text(text):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            raise ValueError("No JSON object found")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON Decode Error: {e}")



@chat_bp.route('/chat', methods=['POST'])
def chat():
    clear_queue(log_queue_thought)
    clear_queue(log_queue_result)

    cid = request.json['conversation_id']
    message = request.json['message'].strip()
    session = get_or_create_session(cid)

    if not message:
        return jsonify({"error": "消息不能为空"}), 400

    session["history"].append({"role": "user", "content": message})
    save_conversation(cid, session["history"])

    if should_greet_or_chitchat(message):
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

    planner_inputs = {
        "user_input": message,
        "context": format_history(session["history"]),
        "agents": json.dumps({
            "Agents": [{"id": item["id"], "configuration": item["configuration"]}
                       for item in agents_dict.values()]
        }, ensure_ascii=False),
        "tasks": json.dumps({
            "Tasks": [{"id": item["id"], "configuration": item["configuration"]}
                      for item in tasks_dict.values()]
        }, ensure_ascii=False),
    }

    def multi_stage_streaming():
        # Step 1: Planner 分配
        manager_crew = Crew(
            agents=[planner],
            tasks=[distribute_task],
            process=Process.sequential,
            verbose=True
        )
        yield from run_planner_and_stream(manager_crew, planner_inputs, session)

        # Step 2: Parse planner 输出
        try:
            parsed = extract_json_from_text(session.get("planner_output", ""))
            agent_ids = [a["id"] for a in parsed["distribution_config"]["agents"]]
            task_ids = [t["id"] for t in parsed["distribution_config"]["tasks"]]

            log_queue_thought.put({
                "type": "thought",
                "data": f"\n[Planner 分配结果] 使用 Agent: {agent_ids}, 任务: {task_ids}\n"
            })
            json.dumps({
                "type": "thought", 
                "data": f"\n[ Planner 分配结果] 使用 Agent: {agent_ids}, 任务: {task_ids}\n"
                }, ensure_ascii=False) + "\n"
            dynamic_agents = [agents_dict[aid]["agent"] for aid in agent_ids]
            dynamic_tasks = [tasks_dict[tid]["task"] for tid in task_ids]
        except Exception as e:
            yield json.dumps({"type": "thought", "data": f"[ERROR]: {str(e)}"}, ensure_ascii=False) + "\n"
            return

        # Step 3: 执行 Crew
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
                yield json.dumps(parsed, ensure_ascii=False) + "\n"

        # Step 5: 输出最终结果
        while not log_queue_result.empty():
            yield json.dumps(log_queue_result.get(timeout=2), ensure_ascii=False) + "\n"

        # Step 6: 输出文件（如果有）
        if "file_infos" in session:
            yield json.dumps({
                "type": "file_list",
                "files": session["file_infos"]
            }, ensure_ascii=False) + "\n"

        # Step 7: 存储历史
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
