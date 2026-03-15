# Cindy Assistant

A lightweight, extensible voice and text-based personal assistant for Windows, designed for simplicity and customizability.

## Features

-   **Voice & Text Control**: Interact via typed commands or voice recognition.
-   **Application Launcher**: Open any installed application on your Windows machine (e.g., "open chrome").
-   **Note Taking**: Quickly save and retrieve notes.
-   **Task Management**: Maintain a simple to-do list.
-   **System Commands**: Shutdown or restart your computer.
-   **Time Inquiry**: Ask for the current time.
-   **Configurable**: Easily toggle features like voice output, logging, and wake word requirements via `config.py`.
-   **Speed Mode**: Chain commands rapidly without repeating the wake word.

## Installation

1.  **Prerequisites**:
    -   Python 3.x
    -   `pip` package manager

2.  **Clone the repository** (or download the source code):
    ```bash
    git clone <your-repo-url>
    cd Assistant
    ```

3.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

4.  **Install dependencies**:
    The project uses several Python libraries. Install them using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```
    > **Note**: `PyAudio` can sometimes be challenging to install on Windows. If you encounter issues, you may need to find and install a pre-compiled wheel (`.whl`) file that matches your Python version and system architecture (32-bit or 64-bit).

## Usage

1.  **Run the assistant**:
    ```bash
    python main.py
    ```
    The assistant will start, load your installed applications, and be ready for commands.

2.  **Interact with Cindy**:
    -   You will start in **text mode**. You can type commands directly into the terminal.
    -   Type `listen` to enter **voice mode**. The assistant will now listen for voice commands.
    -   In voice mode, start your command with the wake word "**execute**" (e.g., "execute open chrome").
    -   To leave voice mode, say "**exit voice mode**".
    -   To stop the assistant entirely, type `exit` in text mode.

### Speed Mode

For executing multiple commands in a row, you can enable "speed mode" to avoid repeating the wake word.

-   **Enable**: Say or type `execute speed mode`.
-   **Usage**: Once enabled, you no longer need to say "execute" before each command.
-   **Disable**: Say or type `exit speed`.

## Available Commands

| Command | Description | Example |
| :--- | :--- | :--- |
| `open <app>` | Opens an installed application. | `execute open vscode` |
| `note <text>` | Saves a new note. | `execute note remember to buy milk` |
| `show notes` | Displays all saved notes. | `execute show notes` |
| `add task <text>` | Adds a task to your to-do list. | `execute add task finish the readme` |
| `show tasks` | Displays all tasks. | `execute show tasks` |
| `time` | Tells you the current time. | `execute time` |
| `shutdown` | Shuts down the computer after 1 second. | `execute shutdown` |
| `restart` | Restarts the computer after 1 second. | `execute restart` |

## Configuration

You can customize the assistant's behavior by editing the `config.py` file.

| Setting | Description |
| :--- | :--- |
| `ENABLE_VOICE_OUTPUT` | Set to `True` for the assistant to have spoken responses. |
| `ENABLE_LOGGING` | Set to `True` to create a log file of all interactions. |
| `ENABLE_VOICE_INPUT` | Set to `True` to allow switching into voice mode with the `listen` command. |
| `REQUIRE_WAKE_WORD` | Set to `True` to require the wake word for commands (can be bypassed with Speed Mode). |
| `PRINT_RESPONSES` | Set to `True` to see the assistant's text responses printed in the terminal. |
