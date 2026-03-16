from utils.constants import (
    CMD_SHUTDOWN,
    CMD_RESTART,
    CMD_TIME
)

# Common speech recognition mistakes for apps
APP_CORRECTIONS = {
    "clone": "chrome",
    "comb": "chrome",
    "from": "chrome",
    "lab": "vscode",
    "vs code": "vscode",
    "visual studio": "vscode"
}


def parse_command(command: str):
    """
    Convert a cleaned command into an action
    the executor understands.
    """

    if not command:
        return "unknown"

    command = command.lower().strip()

    # ----------------------------------
    # Speed Mode
    # ----------------------------------
    if command == "speed mode":
        return "enable_speed"

    if command == "exit speed":
        return "disable_speed"

    # ----------------------------------
    # Sequence parsing structure
    # pattern: sequence [id] [name]
    # ----------------------------------
    if command.startswith("sequence "):
        parts = command.split(" ", 2)
        if len(parts) >= 3:
            seq_id = parts[1]
            seq_name = parts[2].strip()
            
            if seq_name in ["pull up todo list"]:
                return "show_todo_overlay"
            elif seq_name in ["a notification thing", "notifications"]:
                return "test_notification"
            elif seq_name in ["run in the background thing", "background"]:
                return "run_background"
            elif seq_name in ["check all processes and speed up the system"]:
                return "speed_up_system"
            elif seq_name.startswith("write todo list "):
                task = seq_name.replace("write todo list ", "").strip()
                return ("add_task", task)
            
            return ("sequence", (seq_id, seq_name))

    # ----------------------------------
    # Notes
    # ----------------------------------
    if command.startswith("note "):
        note = command.replace("note ", "").strip()
        return ("add_note", note)

    if command == "show notes":
        return "show_notes"

    # ----------------------------------
    # Tasks
    # ----------------------------------
    if command.startswith("add task "):
        task = command.replace("add task ", "").strip()
        return ("add_task", task)

    if command == "show tasks" or command == "pull up todo list":
        return "show_todo_overlay"

    # ----------------------------------
    # Open Applications
    # ----------------------------------
    if command.startswith("open "):

        app_name = command.replace("open ", "").strip()

        # Correct common speech errors
        app_name = APP_CORRECTIONS.get(app_name, app_name)

        return ("open_app", app_name)

    # ----------------------------------
    # Web Search
    # ----------------------------------
    if command.startswith("search "):
        query = command[7:].strip()
        browser = "chrome"  # default
        
        if query.endswith(" on chrome"):
            query = query[:-10].strip()
        elif query.endswith(" on brave"):
            browser = "brave"
            query = query[:-9].strip()
        elif query.startswith("chrome "):
            query = query[7:].strip()
        elif query.startswith("brave "):
            browser = "brave"
            query = query[6:].strip()
            
        return ("search", (browser, query))

    # ----------------------------------
    # System Commands
    # ----------------------------------
    if CMD_SHUTDOWN in command:
        return "shutdown"

    if CMD_RESTART in command:
        return "restart"

    if CMD_TIME in command:
        return "time"

    # ----------------------------------
    # Local Calendar Commands (offline)
    # ----------------------------------
    if "my schedule" in command or "events today" in command or "what do i have today" in command:
        return "calendar_today"

    if "upcoming" in command and ("event" in command or "schedule" in command):
        return "calendar_upcoming"

    if command.startswith("add event "):
        # format: add event <title> on <date> at <time>
        rest = command[10:].strip()
        title = rest
        date_str = None
        time_str = None
        if " on " in rest:
            parts = rest.split(" on ", 1)
            title = parts[0].strip()
            tail = parts[1].strip()
            if " at " in tail:
                d, t = tail.split(" at ", 1)
                date_str = d.strip()
                time_str = t.strip()
            else:
                date_str = tail
        elif " at " in rest:
            parts = rest.split(" at ", 1)
            title = parts[0].strip()
            time_str = parts[1].strip()
        return ("add_event", {"title": title, "date": date_str, "time": time_str})

    if command.startswith("remove event ") or command.startswith("delete event "):
        title = command.split("event ", 1)[1].strip()
        return ("remove_event", title)

    # ----------------------------------
    # Agent (Computer Control) Commands
    # Pattern: agent type <text>, agent click, agent press <key>, agent screenshot
    # ----------------------------------
    if command.startswith("agent "):
        rest = command[6:].strip()
        if rest.startswith("type "):
            return ("agent", {"action": "type", "text": rest[5:]})
        elif rest.startswith("press "):
            return ("agent", {"action": "press", "key": rest[6:]})
        elif rest.startswith("click"):
            return ("agent", {"action": "click"})
        elif rest == "screenshot":
            return ("agent", {"action": "screenshot"})
        elif rest.startswith("hotkey "):
            keys = rest[7:].split("+")
            return ("agent", {"action": "hotkey", "keys": keys})

    # ----------------------------------
    # Unknown Command Fallback to LLM
    # ----------------------------------
    return ("chat", command)