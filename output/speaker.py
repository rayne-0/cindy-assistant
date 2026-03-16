import asyncio
import tempfile
import os
import edge_tts

# Hide the pygame support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Initialize pygame mixer required for audio playback
pygame.mixer.init()


def _speak_offline(text: str) -> None:
    """Fallback: use pyttsx3 for local offline TTS."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        # Pick a female-sounding voice if available
        voices = engine.getProperty('voices')
        for v in voices:
            if 'female' in v.name.lower() or 'zira' in v.name.lower():
                engine.setProperty('voice', v.id)
                break
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"Offline TTS error: {e}")


def speak(text: str) -> None:
    """
    Speak using high-quality Azure Neural TTS (edge-tts).
    Automatically falls back to offline pyttsx3 if there is no internet.
    """
    if not text:
        return

    try:
        async def _generate_and_play():
            voice = 'en-US-AriaNeural'
            communicate = edge_tts.Communicate(text, voice, rate="+5%", pitch="+2Hz")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                temp_filename = fp.name

            await communicate.save(temp_filename)

            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.music.unload()
            os.remove(temp_filename)

        asyncio.run(_generate_and_play())

    except Exception:
        # If edge-tts fails (likely no internet), fall back to local pyttsx3
        _speak_offline(text)