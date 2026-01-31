import os, json
from typing import Dict

DB_FILE = "./data/store.json"

def _ensure():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"files": []}, f)

def add_file(meta: Dict):
    _ensure()
    data = load_all()
    data["files"].append(meta)
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_all():
    _ensure()
    with open(DB_FILE) as f:
        return json.load(f)
