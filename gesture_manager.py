import json
import os

LABELS_FILE = "labels.json"
DATA_DIR = "data"

def load_labels():
    if not os.path.exists(LABELS_FILE):
        return {}
    with open(LABELS_FILE, "r") as f:
        return json.load(f)

def add_new_gesture(name, desc):
    labels = load_labels()

    new_id = str(len(labels))
    labels[new_id] = {"name": name, "desc": desc}

    with open(LABELS_FILE, "w") as f:
        json.dump(labels, f, indent=4)

    os.makedirs(os.path.join(DATA_DIR, new_id), exist_ok=True)
    return new_id
