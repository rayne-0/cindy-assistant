import os
import pvporcupine
import pyaudio
import struct
from dotenv import load_dotenv

load_dotenv()

def test_porcupine():
    access_key = os.environ.get("PICOVOICE_API_KEY")
    if not access_key:
        print("Missing PICOVOICE_API_KEY")
        return

    try:
        # Initialize porcupine with the default 'picovoice' keyword for testing
        porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=['picovoice', 'grapefruit']
        )
        print(f"Porcupine loaded successfully. Version: {porcupine.version}")
        
        # Initialize PyAudio
        pa = pyaudio.PyAudio()
        print("PyAudio initialized.")
        
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        print("Microphone stream opened successfully.")
        
        print("Test passed! Cleaning up...")
        audio_stream.close()
        pa.terminate()
        porcupine.delete()
        
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test_porcupine()
