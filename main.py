from dotenv import load_dotenv

# Load environment variables from .env early
load_dotenv()

from core.assistant import CindyAssistant

from input.voice_input import wait_for_wake_word, listen_for_command
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

import config


def startup_banner():
    print("\n==============================")
    print(f" {ASSISTANT_NAME} Assistant Ready")
    print(f" Wake word : {WAKE_WORD.capitalize()}")
    print(f" Voice mode: type '{VOICE_MODE_COMMAND}'")
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

    in_voice_mode = False

    while True:
        
        # Idle listening state with passive LED check
        overlay.update_status_externally("idle")
        status, payload = wait_for_wake_word(overlay=overlay)
        
        # If the user typed manually into the GUI while we were passively recording
        if status == "MANUAL_OVERRIDE":
            user_input = payload
        
        # If the passive listener caught the "picovoice" hotword
        elif status == "VOICE":
            overlay.update_status_externally("listening")
            user_input = listen_for_command()
            if not user_input:
                continue
                
        else:
            # Wake word engine failed or encountered an error
            continue

        if user_input == EXIT_COMMAND or user_input == EXIT_VOICE_COMMAND:
            if config.ENABLE_LOGGING:
                log("Exiting Cindy.")
            break

        if config.ENABLE_LOGGING:
            log(f"User: {user_input}")

        response = assistant.process_input(user_input)
        
        if not response:
            overlay.update_status_externally("idle")
            continue

        if config.PRINT_RESPONSES:
            print(response)

        if config.ENABLE_LOGGING:
            log(f"{ASSISTANT_NAME}: {response}")

        if config.ENABLE_VOICE_OUTPUT:
            overlay.update_status_externally("speaking")
            speak(response)

        overlay.update_status_externally("idle")
        
        # Multi-Turn Conversation: if Cindy ends her response with a '?',
        # she is asking a follow-up question — keep the mic open immediately.
        response_stripped = response.strip()
        if response_stripped.endswith("?"):
            print("[Multi-turn] Cindy asked a follow-up — listening for reply...")
            overlay.update_status_externally("listening")
            follow_up = listen_for_command()
            if follow_up:
                # Prepend "execute" so it passes the wake word check
                user_input = f"execute {follow_up}"
                # Log and process the follow-up directly without going back to Porcupine
                if config.ENABLE_LOGGING:
                    log(f"User (follow-up): {follow_up}")
                response2 = assistant.process_input(user_input)
                if response2:
                    if config.PRINT_RESPONSES:
                        print(response2)
                    if config.ENABLE_LOGGING:
                        log(f"{ASSISTANT_NAME}: {response2}")
                    if config.ENABLE_VOICE_OUTPUT:
                        overlay.update_status_externally("speaking")
                        speak(response2)
            overlay.update_status_externally("idle")


if __name__ == "__main__":
    main()