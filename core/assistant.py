from utils.helpers import contains_wake_word, clean_command
from core.parser import parse_command
from core.executor import execute_command
from utils.constants import RESPONSE_UNKNOWN

import config


class CindyAssistant:
    """
    Core assistant controller for Cindy.
    Handles command processing from cleaned input to execution.
    """

    def __init__(self):

        # Speed mode allows commands without wake word
        self.speed_mode = False

    def process_input(self, user_input: str) -> str:
        """
        Process raw user input from terminal or voice.
        """

        if not user_input:
            return ""

        # -----------------------------------------
        # Wake Word Requirement
        # -----------------------------------------
        if config.REQUIRE_WAKE_WORD and not self.speed_mode:

            if not contains_wake_word(user_input):
                return ""

            command = clean_command(user_input)

        else:

            command = user_input.lower().strip()

        # -----------------------------------------
        # Parse Command
        # -----------------------------------------
        action = parse_command(command)

        # -----------------------------------------
        # Execute Command
        # -----------------------------------------
        response = execute_command(action, self)

        if not response:
            return RESPONSE_UNKNOWN

        return response