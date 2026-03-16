import os
from dotenv import load_dotenv

# Load explicitly
load_dotenv()

from utils.gemini_client import ask_assistant

print(f"API Key loaded: {'GEMINI_API_KEY' in os.environ}")

try:
    print("Testing ask_assistant()...")
    res = ask_assistant("hello world")
    print(f"Response: {res}")
except Exception as e:
    import traceback
    traceback.print_exc()
