import json
import os

TASK_FILE = "data/tasks.json"


def load_tasks():

    if not os.path.exists(TASK_FILE):
        return []

    try:
        with open(TASK_FILE, "r") as f:
            data = f.read().strip()

            if not data:
                return []

            return json.loads(data)

    except Exception:
        return []


def save_tasks(tasks):

    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(task):

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

def remove_task(index: int):
    """
    Remove a task by index
    """
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)


def get_tasks():

    return load_tasks()