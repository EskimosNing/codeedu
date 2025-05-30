'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-29 22:23:01
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-29 22:23:04
 # @ Description:
 '''

# routes/conversation.py

from flask import Blueprint, jsonify, request
import os
import json
import uuid
from utils.log_queues import log_queue_thought, log_queue_result
from utils.session import get_convo_path, save_conversation, load_conversation
from config.paths import STORAGE_PATH

convo_bp = Blueprint("conversation", __name__)

@convo_bp.route("/new_conversation", methods=["POST"])
def new_conversation():
    #user_id = request.json.get("user_id", "default")
    message = request.json.get("message", "")
    cid = str(uuid.uuid4())
    save_conversation(cid, [])
    return jsonify({"conversation_id": cid, "title": message[:50]})


@convo_bp.route("/conversations", methods=["GET"])
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
                try:
                    with open(os.path.join(STORAGE_PATH, filename), "r", encoding="utf-8") as f:
                        history = json.load(f)
                        title = next((m["content"] for m in history if m["role"] == "user"), title)
                except:
                    pass

            conversations.append({"id": cid, "title": title.strip()})
    return jsonify(conversations)


@convo_bp.route("/conversation/<cid>", methods=["GET"])
def get_conversation_history(cid):
    convo_path = get_convo_path(cid)
    if not os.path.exists(convo_path):
        return jsonify({"error": "对话不存在"}), 404

    try:
        with open(convo_path, "r", encoding="utf-8") as f:
            history = json.load(f)
        return jsonify(history)
    except json.JSONDecodeError:
        return jsonify({"error": "对话数据格式错误"}), 500


@convo_bp.route("/delete_conversation/<cid>", methods=["DELETE"])
def delete_conversation(cid):
    convo_path = get_convo_path(cid)
    if os.path.exists(convo_path):
        os.remove(convo_path)
    return jsonify({"success": True})
