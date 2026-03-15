import speech_recognition as sr

from utils.helpers import normalize_text
from utils.constants import (
    VOICE_LISTEN_TIMEOUT,
    VOICE_PHRASE_LIMIT,
    RESPONSE_LISTENING
)


recognizer = sr.Recognizer()


def listen_for_command() -> str:
    """
    Listen to microphone input and return recognized text.
    """

    with sr.Microphone() as source:
        print(f"🎤 {RESPONSE_LISTENING}")

        try:
            audio = recognizer.listen(
                source,
                timeout=VOICE_LISTEN_TIMEOUT,
                phrase_time_limit=VOICE_PHRASE_LIMIT
            )

            command = recognizer.recognize_whisper(audio)

            print(f"You said: {command}")

            return normalize_text(command)

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

        except sr.UnknownValueError:
            print("Sorry, I could not understand.")
            return ""

        except sr.RequestError:
            print("Speech service unavailable.")
            return ""