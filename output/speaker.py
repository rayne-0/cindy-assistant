import asyncio
import tempfile
import os
import edge_tts

# Hide the pygame support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Initialize pygame mixer required for audio playback
pygame.mixer.init()

def speak(text: str) -> None:
    """
    Speak a message using high-quality Azure Neural TTS.
    Downloads the audio to a temp file and plays it via pygame.
    """
    if not text:
        return

    try:
        async def _generate_and_play():
            # 'en-US-AriaNeural' is highly expressive, and slight adjustments make it sound more upbeat and natural
            voice = 'en-US-AriaNeural'
            communicate = edge_tts.Communicate(text, voice, rate="+5%", pitch="+2Hz")
            
            # Create a secure temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                temp_filename = fp.name
            
            # Download audio from Microsoft Edge API
            await communicate.save(temp_filename)
            
            # Play the audio file
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            # Wait until playback is completely finished
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # Cleanup
            pygame.mixer.music.unload()
            os.remove(temp_filename)

        # Run the async function synchronously block
        asyncio.run(_generate_and_play())

    except Exception as e:
        print(f"Speech engine error: {e}")