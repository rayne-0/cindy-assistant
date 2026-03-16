import sys
import msvcrt
import time
from utils.helpers import normalize_text


def _check_keyboard():
    """
    Non-blocking check: return the next character typed, or None if nothing pressed.
    Used by main.py to detect when the user starts typing without blocking the event loop.
    """
    if msvcrt.kbhit():
        try:
            char = msvcrt.getwche()
            return char
        except Exception:
            return None
    return None


def get_text_input(overlay, prefill: str = "") -> str:
    """
    Capture user input from the terminal non-blockingly while updating the overlay GUI.
    `prefill` is used when the first character was already consumed by `_check_keyboard`.
    """
    if not prefill:
        print("> ", end="", flush=True)
    
    input_str = prefill
    
    while True:
        # Update the CustomTkinter GUI so it doesn't freeze
        if overlay:
            overlay.update()
            q = overlay.get_and_clear_query()
            if q:
                print(q)
                return q
            
        # Check if a keyboard key was pressed
        if msvcrt.kbhit():
            try:
                char = msvcrt.getwche()
                
                # Handle Enter
                if char == '\r' or char == '\n':
                    print()
                    return normalize_text(input_str)
                # Handle Backspace
                elif char == '\b':
                    input_str = input_str[:-1]
                    print(" \b", end="", flush=True)
                # Handle Ctrl+C
                elif char == '\x03':
                    raise KeyboardInterrupt
                else:
                    input_str += char
                    
            except KeyboardInterrupt:
                print("\nExiting Cindy.")
                return "exit"
        
        # Prevent 100% CPU usage loop
        time.sleep(0.01)