from utils.helpers import normalize_text


def get_text_input() -> str:
    """
    Capture user input from the terminal and normalize it.
    """
    try:
        user_input = input("> ")
        return normalize_text(user_input)

    except KeyboardInterrupt:
        print("\nExiting Cindy.")
        return "exit"