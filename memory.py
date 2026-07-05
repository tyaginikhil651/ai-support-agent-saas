import json
import os

MEMORY_FILE = "memory.json"


def load_json(filename):

    if not os.path.exists(filename):
        return {}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_json(filename, data):

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# ----------------------------------
# Conversation Memory Functions
# ----------------------------------

def get_history(user_id):

    memory = load_json(MEMORY_FILE)

    return memory.get(str(user_id), [])


def add_message(user_id, role, content):

    memory = load_json(MEMORY_FILE)

    user_id = str(user_id)

    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append(
        {
            "role": role,
            "content": content
        }
    )

    # Keep last 10 messages
    memory[user_id] = memory[user_id][-10:]

    save_json(MEMORY_FILE, memory)