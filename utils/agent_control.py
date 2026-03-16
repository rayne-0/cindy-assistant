"""
Agentic Computer Control – lets Cindy physically control the Desktop
using PyAutoGUI to move the mouse, click, and type text.
"""
import time
import pyautogui

# Safety: stop if mouse hits a screen corner
pyautogui.FAILSAFE = True
# Slightly slow down actions so they feel intentional
pyautogui.PAUSE = 0.05


def agent_type(text: str, interval: float = 0.04) -> str:
    """Type text at the current cursor position."""
    pyautogui.write(text, interval=interval)
    return f"Typed: {text}"


def agent_press(key: str) -> str:
    """Press a single key (e.g. 'enter', 'tab', 'escape')."""
    pyautogui.press(key)
    return f"Pressed key: {key}"


def agent_hotkey(*keys) -> str:
    """Trigger a keyboard shortcut (e.g. 'ctrl', 'c')."""
    pyautogui.hotkey(*keys)
    return f"Hotkey: {'+'.join(keys)}"


def agent_click(x: int = None, y: int = None, button: str = "left") -> str:
    """Click at an absolute position, or at the current cursor if x/y are None."""
    if x is not None and y is not None:
        pyautogui.click(x, y, button=button)
        return f"Clicked {button} at ({x}, {y})"
    else:
        pyautogui.click(button=button)
        return f"Clicked {button} at current position"


def agent_move(x: int, y: int, duration: float = 0.3) -> str:
    """Smoothly move the mouse to (x, y)."""
    pyautogui.moveTo(x, y, duration=duration)
    return f"Moved mouse to ({x}, {y})"


def agent_screenshot(path: str = None) -> str:
    """Take a screenshot and save it."""
    import os
    save_path = path or os.path.join(os.getcwd(), "data", "screenshot.png")
    img = pyautogui.screenshot()
    img.save(save_path)
    return f"Screenshot saved to: {save_path}"


def run_agent_command(action: str, args: dict) -> str:
    """
    Dispatcher: routes parsed agent commands to the correct function.
    Expected 'action' values: 'type', 'press', 'hotkey', 'click', 'move', 'screenshot'
    """
    handlers = {
        "type": lambda: agent_type(args.get("text", "")),
        "press": lambda: agent_press(args.get("key", "enter")),
        "hotkey": lambda: agent_hotkey(*args.get("keys", ["ctrl", "c"])),
        "click": lambda: agent_click(args.get("x"), args.get("y"), args.get("button", "left")),
        "move": lambda: agent_move(args.get("x", 0), args.get("y", 0)),
        "screenshot": lambda: agent_screenshot(args.get("path")),
    }
    handler = handlers.get(action)
    if handler:
        return handler()
    return f"Unknown agent action: {action}"
