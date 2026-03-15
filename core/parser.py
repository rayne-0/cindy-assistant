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

    if command == "show tasks":
        return "show_tasks"

    # ----------------------------------
    # Open Applications
    # ----------------------------------
    if command.startswith("open "):

        app_name = command.replace("open ", "").strip()

        # Correct common speech errors
        app_name = APP_CORRECTIONS.get(app_name, app_name)

        return ("open_app", app_name)

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
    # Unknown Command
    # ----------------------------------
    return "unknown"