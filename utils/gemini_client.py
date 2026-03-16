import os
from google import genai
from google.genai import types
from utils.memory import load_memory, add_to_memory

client = None

def ask_assistant(query: str) -> str:
    """
    Sends a query to Gemini API with conversational context.
    """
    global client
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Gemini API key is missing. Please check your .env file."
        
    if client is None:
        try:
            client = genai.Client(api_key=api_key)
        except Exception as e:
            return f"Failed to initialize Gemini client: {e}"

    try:
        # Load past messages and format them for the Gemini API
        history = load_memory()
        
        # We need to construct the chat session
        # Define Cindy's personality and awareness
        cindy_persona = (
            "You are Cindy, a highly advanced, helpful, and concise virtual windows desktop assistant. "
            "You have a natural-sounding female voice powered by Microsoft Azure Neural TTS. "
            "You are capable of performing web searches, managing to-do lists via an interactive GUI overlay, "
            "triggering Windows notifications, running silently in the system tray, and automatically optimizing OS performance by killing heavy background processes. "
            "Keep your responses short, conversational, and directly answer the user's prompt without being overly wordy."
        )

        formatted_history = []
        for msg in history:
            # We must map "user" or "model" history to a dict with role and parts.
            formatted_history.append(
                {'role': msg['role'], 'parts': [{'text': msg['content']}]}
            )
            
        chat = client.chats.create(
            model='gemini-2.5-flash',
            # History is passed if formatted_history is populated
            history=formatted_history if formatted_history else None,
            config=types.GenerateContentConfig(
                system_instruction=cindy_persona,
                temperature=0.7,
            )
        )

        # Send the new message
        response = chat.send_message(query)
        
        reply = ""
        if response.text:
            reply = response.text.strip()
        
        # Save to local memory file
        add_to_memory("user", query)
        add_to_memory("model", reply)
        
        return reply
        
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        print(f"Gemini Error details: {err}")
        return f"Sorry, I am having trouble connecting to my Gemini brain. Error: {e}"
