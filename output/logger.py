from datetime import datetime


def log(message: str) -> None:
    """
    Print a timestamped log message.
    """

    timestamp = datetime.now().strftime("%H:%M:%S")

    print(f"[{timestamp}] {message}")