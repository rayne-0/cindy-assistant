from dotenv import load_dotenv

# Load environment variables from .env early
load_dotenv()

from core.assistant import CindyAssistant

from input.voice_input import wait_for_wake_word, listen_for_command
from input.text_input import get_text_input
from output.speaker import speak
from output.logger import log

from utils.constants import (
    ASSISTANT_NAME,
    VOICE_MODE_COMMAND,
    EXIT_COMMAND,
    WAKE_WORD,
    EXIT_VOICE_COMMAND
)

from utils.app_registry import load_apps
from utils.gui import get_overlay
import threading
import queue

import config


def startup_banner():
    print("\n==============================")
    print(f" {ASSISTANT_NAME} Assistant Ready")
    print(f" Wake word : {WAKE_WORD.capitalize()}")
    print(f" Speed mode: type 'speed mode' to skip wake word")
    print(f" Exit      : type '{EXIT_COMMAND}'")
    print("==============================\n")


def main():

    assistant = CindyAssistant()

    # Preload installed apps
    print("Loading installed applications...")
    load_apps()

    print("Initializing GUI Overlay...")
    
    # Initialize CTk on the exact same thread that will call root.update()
    overlay = get_overlay(assistant)
    
    startup_banner()

    if config.ENABLE_LOGGING:
        log(f"{ASSISTANT_NAME} initialized.")

    # Queue to pass voice inputs from the Porcupine background thread to the main loop
    voice_queue = queue.Queue()

    def voice_listener_thread():
        """Runs Porcupine passively in background, pushes hotword detections to queue."""
        while True:
            status, payload = wait_for_wake_word(overlay=None)  # no overlay updates from thread
            voice_queue.put((status, payload))

    # Start the Porcupine listener in the background
    t = threading.Thread(target=voice_listener_thread, daemon=True)
    t.start()

    def process_response(response: str):
        """Handle a completed response: print, log, speak, update LED, check for follow-up."""
        if not response:
            overlay.update_status_externally("idle")
            return

        if config.PRINT_RESPONSES:
            print(response)

        if config.ENABLE_LOGGING:
            log(f"{ASSISTANT_NAME}: {response}")

        if config.ENABLE_VOICE_OUTPUT:
            overlay.update_status_externally("speaking")
            speak(response)

        overlay.update_status_externally("idle")

        # Multi-Turn: keep mic hot if Cindy asks a question back
        if response.strip().endswith("?"):
            print("[Multi-turn] Listening for follow-up...")
            overlay.update_status_externally("listening")
            follow_up = listen_for_command()
            if follow_up:
                if config.ENABLE_LOGGING:
                    log(f"User (follow-up): {follow_up}")
                r2 = assistant.process_input(f"execute {follow_up}")
                if r2:
                    if config.PRINT_RESPONSES:
                        print(r2)
                    if config.ENABLE_LOGGING:
                        log(f"{ASSISTANT_NAME}: {r2}")
                    if config.ENABLE_VOICE_OUTPUT:
                        overlay.update_status_externally("speaking")
                        speak(r2)
            overlay.update_status_externally("idle")

    while True:
        overlay.update()

        # ── 1. Check overlay GUI for typed commands ──────────────────────
        gui_query = overlay.get_and_clear_query()
        if gui_query:
            if config.ENABLE_LOGGING:
                log(f"User (GUI): {gui_query}")
            r = assistant.process_input(gui_query)
            process_response(r)
            continue

        # ── 2. Check terminal keyboard (non-blocking) ─────────────────────
        from input.text_input import _check_keyboard  # non-blocking single key poll
        char = _check_keyboard()
        if char is not None:
            # We got a character; gather the full line in a blocking-but-overlay-aware way
            line = get_text_input(overlay, prefill=char)
            user_input = line.strip()

            if not user_input:
                continue

            if user_input == EXIT_COMMAND:
                if config.ENABLE_LOGGING:
                    log("Exiting Cindy.")
                break

            if user_input == "speed mode":
                assistant.speed_mode = True
                print("Speed mode ON — no wake word needed.")
                continue

            if user_input == "exit speed":
                assistant.speed_mode = False
                print("Speed mode OFF.")
                continue

            if config.ENABLE_LOGGING:
                log(f"User: {user_input}")

            # Speed mode: skip wake word; normal mode: require wake word prefix
            cmd = user_input if assistant.speed_mode else f"execute {user_input}"
            r = assistant.process_input(cmd)
            process_response(r)
            continue

        # ── 3. Check voice queue (non-blocking) ───────────────────────────
        try:
            status, payload = voice_queue.get_nowait()
            if status == "VOICE":
                overlay.update_status_externally("listening")
                user_input = listen_for_command()
                if user_input:
                    if config.ENABLE_LOGGING:
                        log(f"User (voice): {user_input}")
                    r = assistant.process_input(f"execute {user_input}")
                    process_response(r)
        except queue.Empty:
            pass


if __name__ == "__main__":
    main()