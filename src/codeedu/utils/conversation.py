'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-28 14:17:36
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-28 14:17:48
 # @ Description:
 '''

import os
import json
from pathlib import Path

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path.cwd()))
STORAGE_PATH = PROJECT_ROOT / "conversations"

os.makedirs(STORAGE_PATH, exist_ok=True)

def get_convo_path(cid):
    return os.path.join(STORAGE_PATH, f'{cid}.json')

def load_conversation(cid):
    path = get_convo_path(cid)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []

def save_conversation(cid, history):
    with open(get_convo_path(cid), 'w') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)