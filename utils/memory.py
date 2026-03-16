import json
import os

MEMORY_FILE = "data/memory.json"

def get_memory_file_path() -> str:
    """Ensure the data directory exists and return the file path."""
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    return MEMORY_FILE

def load_memory() -> list:
    """
    Load conversation history from the local JSON file.
    Returns a list of dicts: [{"role": "user"|"model", "content": "..."}]
    """
    path = get_memory_file_path()
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = f.read().strip()
            if not data:
                return []
            return json.loads(data)
    except Exception as e:
        print(f"Error loading memory: {e}")
        return []

def save_memory(messages: list):
    """
    Save the entire conversation history back to the JSON file.
    """
    path = get_memory_file_path()
    try:
        # Keep only the last 20 messages to prevent token limits/bloat
        pruned_messages = messages[-20:]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pruned_messages, f, indent=2)
    except Exception as e:
        print(f"Error saving memory: {e}")

def add_to_memory(role: str, content: str):
    """
    Helper to append a single message to history.
    role must be 'user' or 'model'.
    """
    history = load_memory()
    history.append({
        "role": role,
        "content": content
    })
    save_memory(history)
