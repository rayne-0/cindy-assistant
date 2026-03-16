# Cindy Assistant

A lightweight, extensible voice and text-based personal assistant for Windows, designed for simplicity, customizability, and deep Desktop OS integration.

## Features

-   **Gemini AI Brain**: Cindy uses the `gemini-2.5-flash` model for intelligent fallbacks and conversational contextual memory.
-   **Natural Voice TTS**: Powered by `edge-tts` connected directly to Microsoft Azure Neural APIs for highly realistic speech.
-   **Web Search Integration**: Launch Google searches instantly via Chrome or Brave browsers.
-   **GUI To-Do Overlay**: A transparent, always-on-top checklist interface built in `tkinter` to manage tasks seamlessly.
-   **System Tray Backgrounding**: Uses `pystray` to minimize Cindy to your system tray natively.
-   **System Optimizer**: Instantly kill heavy background games/apps and purge `Temp` folders to free up RAM via `psutil`.
-   **Application Launcher**: Open any installed application on your Windows machine (e.g., "open chrome").
-   **Native Notifications**: Alert you to background changes with Windows Toast notifications.

## Installation

1.  **Prerequisites**:
    -   Python 3.10+
    -   `pip` package manager
    -   A free Google Gemini API Key

2.  **Clone the repository** (or download the source code):
    ```bash
    git clone https://github.com/rayne-0/cindy-assistant.git
    cd Assistant
    ```

3.  **Environment Variables**:
    Create a `.env` file in the root directory and add your key:
    ```
    GEMINI_API_KEY=your_key_here
    ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the assistant**:
    ```bash
    python main.py
    ```

2.  **Interact with Cindy**:
    -   You will start in **text mode**. Type commands directly into the terminal.
    -   Start your command with the wake word "**execute**" (e.g., "execute open chrome").
    -   Type `listen` to enter **voice mode**. 

## Available Commands

| Command | Description | Example |
| :--- | :--- | :--- |
| `open <app>` | Opens an installed application. | `execute open vscode` |
| `search <query> on <browser>` | Googles a query. Chrome is default. | `execute search weather tomorrow on brave` |
| `sequence 1 write todo list <task>` | Adds a task to `tasks.json`. | `execute sequence 1 write todo list buy milk` |
| `sequence 2 pull up todo list` | Spawns the transparent GUI to-do list. | `execute sequence 2 pull up todo list` |
| `sequence 3 a notification thing` | Sends a Windows Toast notification. | `execute sequence 3 a notification thing` |
| `sequence 4 run in the background thing`| Hides the terminal window to the System Tray. | `execute sequence 4 run in the background thing` |
| `sequence 5 check all processes...` | Kills background apps and clears temp cache. | `execute sequence 5 check all processes and speed up the system` |
| `<unknown>` | Anything else routes through the Gemini AI. | `execute how are you feeling today?` |

## Configuration
You can customize the assistant's behavior by editing the `config.py` file.
| Setting | Description |
| :--- | :--- |
| `USE_GEMINI` | Set to `True` to enable the AI fallback brain. |
| `ENABLE_VOICE_OUTPUT` | Set to `True` for Cindy to speak her responses using `edge-tts`. |
| `REQUIRE_WAKE_WORD` | Set to `True` to require the 'execute' prefix. |
