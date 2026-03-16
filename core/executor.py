import os
import subprocess
import datetime
import urllib.parse

from utils.constants import (
    RESPONSE_SHUTDOWN,
    RESPONSE_RESTART,
    RESPONSE_UNKNOWN
)

from utils.app_registry import load_apps
from utils.notes import add_note, get_notes
from utils.tasks import add_task, get_tasks
from utils.gemini_client import ask_assistant
from utils.overlay import show_overlay
from utils.optimizer import speed_up_system
from utils.agent_control import run_agent_command
import config
from plyer import notification

def _execute_command_inner(action, assistant=None):
    """
    Execute parsed commands from Cindy's parser.
    """
    
    if action == "show_todo_overlay":
        # Launch the overlay in a separate detached process so it doesn't block
        # Since tkinter mainloop blocks, we run it in a subprocess
        # Popen without wait allows the assistant to keep listening
        subprocess.Popen(["python", "-c", "import sys; sys.path.append('.'); from utils.overlay import show_overlay; show_overlay()"])
        return "Opening To-Do List."

    if action == "test_notification":
        notification.notify(
            title="Cindy Assistant",
            message="This is a test notification from Cindy!",
            app_icon=None,
            timeout=5,
        )
        return "Notification sent."

    if action == "run_background":
        if assistant:
            assistant.run_in_background()
            return "Minimizing to system tray."
        return "I can't do that right now."

    if action == "speed_up_system":
        return speed_up_system()

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

        # -----------------------------
        # Web Search
        # -----------------------------
        if command == "search":
            browser, query = value
            
            # URL encode the search text
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            
            # Execute browser start command
            if browser == "chrome":
                os.system(f'start chrome "{url}"')
                return f"Searching for {query} on Chrome."
            elif browser == "brave":
                os.system(f'start brave "{url}"')
                return f"Searching for {query} on Brave."

        # -----------------------------
        # Agent Computer Control
        # -----------------------------
        if command == "agent":
            return run_agent_command(value.get("action"), value)

        # -----------------------------
        # Gemini Chat Fallback
        # -----------------------------
        if command == "chat":
            if config.USE_GEMINI:
                # Optionally log or print that we are asking Gemini
                return ask_assistant(value)
            else:
                return RESPONSE_UNKNOWN

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

def execute_command_safe(action, assistant=None):
    try:
        return _execute_command_inner(action, assistant)
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        print(f"Executor Error: {err}")
        return f"Error executing command: {e}"

# Reassign the exported function to the safe wrapper
execute_command = execute_command_safe