import os
import subprocess
import datetime

from utils.constants import (
    RESPONSE_SHUTDOWN,
    RESPONSE_RESTART,
    RESPONSE_UNKNOWN
)

from utils.app_registry import load_apps
from utils.notes import add_note, get_notes
from utils.tasks import add_task, get_tasks


def execute_command(action, assistant=None):
    """
    Execute parsed commands from Cindy's parser.
    """

    # -----------------------------------------
    # Structured commands (tuples)
    # -----------------------------------------
    if isinstance(action, tuple):

        command, value = action

        # -----------------------------
        # Open Applications
        # -----------------------------
        if command == "open_app":

            value = value.lower()

            try:
                apps = load_apps()

                for name, app_id in apps.items():

                    if value in name:

                        subprocess.Popen(
                            ["explorer.exe", f"shell:AppsFolder\\{app_id}"]
                        )

                        return f"Opening {name}"

                return f"Could not find {value}"

            except Exception:
                return f"Could not open {value}"

        # -----------------------------
        # Notes
        # -----------------------------
        if command == "add_note":

            add_note(value)

            return "Note saved."

        # -----------------------------
        # Tasks
        # -----------------------------
        if command == "add_task":

            add_task(value)

            return "Task added."

    # -----------------------------------------
    # Simple Commands
    # -----------------------------------------

    # -----------------------------
    # Show Notes
    # -----------------------------
    if action == "show_notes":

        notes = get_notes()

        if not notes:
            return "No notes saved."

        return "\n".join(notes)

    # -----------------------------
    # Show Tasks
    # -----------------------------
    if action == "show_tasks":

        tasks = get_tasks()

        if not tasks:
            return "No tasks."

        return "\n".join(tasks)

    # -----------------------------
    # Speed Mode
    # -----------------------------
    if action == "enable_speed" and assistant:

        assistant.speed_mode = True
        return "Speed mode enabled."

    if action == "disable_speed" and assistant:

        assistant.speed_mode = False
        return "Speed mode disabled."

    # -----------------------------
    # System Commands
    # -----------------------------
    if action == "shutdown":
        os.system("shutdown /s /t 1")
        return RESPONSE_SHUTDOWN

    if action == "restart":
        os.system("shutdown /r /t 1")
        return RESPONSE_RESTART

    if action == "time":
        now = datetime.datetime.now()
        return now.strftime("Current time: %H:%M")

    # -----------------------------------------
    # Unknown Command
    # -----------------------------------------
    return RESPONSE_UNKNOWN