import pyttsx3


engine = pyttsx3.init()

# Optional: adjust voice settings
engine.setProperty("rate", 170)


def speak(text: str) -> None:
    """
    Speak a message using text-to-speech.
    """

    if not text:
        return

    try:
        engine.say(text)
        engine.runAndWait()

    except Exception:
        print("Speech engine error.")