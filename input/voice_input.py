import os
import struct
import pyaudio
import pvporcupine
import speech_recognition as sr
from colorama import Fore, Style

from utils.helpers import normalize_text
from utils.constants import (
    VOICE_LISTEN_TIMEOUT,
    VOICE_PHRASE_LIMIT,
    RESPONSE_LISTENING
)

recognizer = sr.Recognizer()

def wait_for_wake_word(overlay=None) -> bool:
    """
    Passively listens for the Porcupine wake word ('picovoice') using a low-footprint 
    audio stream, without sending anything to Whisper or freezing the main loop.
    """
    access_key = os.environ.get("PICOVOICE_API_KEY")
    if not access_key:
        print(Fore.RED + "Missing PICOVOICE_API_KEY. Cannot start continuous listener." + Style.RESET_ALL)
        return False
        
    try:
        porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=['picovoice']
        )
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        
        print(Fore.YELLOW + "Passive Listening mode active. Say 'picovoice' to wake Cindy." + Style.RESET_ALL)
        
        try:
            while True:
                # Update overlay if it exists to prevent UI from freezing
                if overlay:
                    overlay.update()
                    # Also check if text was typed manually!
                    q = overlay.get_and_clear_query()
                    if q:
                        audio_stream.close()
                        pa.terminate()
                        porcupine.delete()
                        return "MANUAL_OVERRIDE", q
                        
                pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                audio_frame = struct.unpack_from("h" * porcupine.frame_length, pcm)
                
                keyword_index = porcupine.process(audio_frame)
                if keyword_index >= 0:
                    print(Fore.GREEN + "\nWake word detected!" + Style.RESET_ALL)
                    break
        finally:
            audio_stream.close()
            pa.terminate()
            porcupine.delete()
            
        return "VOICE", None
        
    except Exception as e:
        print(f"Wake word engine error: {e}")
        return "ERROR", None

def listen_for_command() -> str:
    """
    Listen to microphone input for the actual command *after* the wake word,
    and process it through local Whisper.
    """
    print(f"🎤 {RESPONSE_LISTENING}")
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(
                source,
                timeout=VOICE_LISTEN_TIMEOUT,
                phrase_time_limit=VOICE_PHRASE_LIMIT
            )
            # Send to whisper for text transcription
            print("Processing audio...")
            command = recognizer.recognize_whisper(audio)
            print(Fore.CYAN + f"You said: {command}" + Style.RESET_ALL)
            return normalize_text(command)

        except sr.WaitTimeoutError:
            print(Fore.YELLOW + "No speech detected. Going back to sleep." + Style.RESET_ALL)
            return ""
        except sr.UnknownValueError:
            print(Fore.RED + "Sorry, I could not understand." + Style.RESET_ALL)
            return ""
        except sr.RequestError:
            print(Fore.RED + "Speech service unavailable." + Style.RESET_ALL)
            return ""