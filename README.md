# Cindy Assistant

A lightweight, extensible voice and text-based personal assistant for Windows, designed for simplicity, customizability, and deep Desktop OS integration.

## Features

-   **Gemini AI Brain**: Powered by `gemini-2.5-flash` with local memory for intelligent, contextual conversations.
-   **Natural Voice TTS**: Azure Neural TTS via `edge-tts` with expressive `AriaNeural` voice profile.
-   **Persistent GUI Overlay**: Floating dark-mode search bar (CustomTkinter) — always on top, status LED indicator.
-   **Porcupine Wake-Word Engine**: Always-on passive listening — say "picovoice" to activate Cindy hands-free.
-   **Multi-Turn Voice Conversations**: Cindy keeps the mic open automatically when she asks a follow-up question.
-   **Agentic Desktop Control**: Physically control your mouse, keyboard, and take screenshots via `pyautogui`.
-   **Google Workspace Integration**: Read your Google Calendar events and send emails by voice.
-   **Web Search**: Launch Google searches instantly via Chrome or Brave.
-   **GUI To-Do Overlay**: Transparent, always-on-top checklist interface.
-   **App Launcher**: Open any installed Windows application by name.
-   **System Optimizer**: Kill background processes and clear temp folders to free RAM.
-   **System Tray**: Run silently in the background via the system tray.
-   **Windows Notifications**: Native Toast notification support.

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
