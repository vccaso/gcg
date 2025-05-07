# memory_manager.py
import json
import os

MEMORY_DIR = "workspace/memory"
os.makedirs(MEMORY_DIR, exist_ok=True)

def get_memory_path(session_id):
    return os.path.join(MEMORY_DIR, f"memory_{session_id}.json")

def load_memory(session_id):
    path = get_memory_path(session_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"history": [], "latest_workflow": None}

def save_memory(memory, session_id):
    path = get_memory_path(session_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def list_sessions():
    sessions = []
    for f in os.listdir(MEMORY_DIR):
        if f.startswith("memory_") and f.endswith(".json"):
            sessions.append(f[len("memory_"):-len(".json")])
    return sorted(sessions)
