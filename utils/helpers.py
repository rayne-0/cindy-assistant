from utils.constants import WAKE_WORD


def normalize_text(text: str) -> str:
    """
    Normalize user input for consistent parsing.
    Converts to lowercase and strips whitespace.
    """
    if not text:
        return ""

    return text.lower().strip()


def contains_wake_word(text: str) -> bool:
    """
    Check if the wake word is present in the input.
    """
    text = normalize_text(text)
    return text.startswith(WAKE_WORD)


def remove_wake_word(text: str) -> str:
    """
    Remove the wake word from the command.
    Example:
        'cindy shutdown computer' -> 'shutdown computer'
    """
    text = normalize_text(text)

    if text.startswith(WAKE_WORD):
        return text[len(WAKE_WORD):].strip()

    return text


def clean_command(text: str) -> str:
    """
    Full cleaning pipeline for commands.
    """
    text = normalize_text(text)
    text = remove_wake_word(text)
    return text


def is_empty(text: str) -> bool:
    """
    Check if input is empty after normalization.
    """
    return normalize_text(text) == ""