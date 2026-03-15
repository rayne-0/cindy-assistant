from core.assistant import CindyAssistant

from input import get_text_input, listen_for_command
from output import speak, log

from utils.constants import (
    ASSISTANT_NAME,
    VOICE_MODE_COMMAND,
    EXIT_COMMAND,
    WAKE_WORD,
    EXIT_VOICE_COMMAND
)

from utils.app_registry import load_apps

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

    startup_banner()

    if config.ENABLE_LOGGING:
        log(f"{ASSISTANT_NAME} initialized.")

    in_voice_mode = False

    while True:

        if in_voice_mode:

            user_input = listen_for_command()

            if not user_input:
                continue

            if EXIT_VOICE_COMMAND in user_input:
                print("Exiting Voice Mode.")
                in_voice_mode = False
                continue

        else:

            user_input = get_text_input()

            if user_input == EXIT_COMMAND:

                if config.ENABLE_LOGGING:
                    log("Exiting Cindy.")

                break

            if user_input == VOICE_MODE_COMMAND and config.ENABLE_VOICE_INPUT:

                print("Entering Voice Mode. Say 'exit voice mode' to return to text input.")
                in_voice_mode = True
                continue

        if config.ENABLE_LOGGING:
            log(f"User: {user_input}")

        response = assistant.process_input(user_input)

        if not response:
            continue

        if config.PRINT_RESPONSES:
            print(response)

        if config.ENABLE_LOGGING:
            log(f"{ASSISTANT_NAME}: {response}")

        if config.ENABLE_VOICE_OUTPUT:
            speak(response)


if __name__ == "__main__":
    main()