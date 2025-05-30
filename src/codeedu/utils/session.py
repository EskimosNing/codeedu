'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-29 14:39:25
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-29 19:48:42
 # @ Description:Session 管理与对话历史存储
 '''


import json
import os
from pathlib import Path
from config.paths import STORAGE_PATH


session_store = {}
# --- 工具函数 ---
# 获取对话的路径
def get_convo_path(cid: str) -> Path:
    #return os.path.join(STORAGE_PATH, f'{cid}.json')
    return STORAGE_PATH / f"{cid}.json"

# 加载对话历史
def load_conversation(cid: str) -> list:
    path = get_convo_path(cid)
    if os.path.exists(path):
        with open(path, 'r',encoding='utf-8') as f:
            return json.load(f)
    return []

# 保存对话历史
def save_conversation(cid: str, history: list):
    with open(get_convo_path(cid), 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)




def get_or_create_session(conversation_id: str) -> dict:
    if conversation_id not in session_store:
   
        crew = None
        session_store[conversation_id] = {
            "crew": crew,
            "memory": [],
            "history": load_conversation(conversation_id)
        }
    return session_store[conversation_id]
