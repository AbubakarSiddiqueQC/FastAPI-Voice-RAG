import os, sys

# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path to the parent directory
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to the Python path
sys.path.append(parent_dir)

#imports functions or constants
from open_ai_client import client
def convert_text_to_speech(text):
    response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=text
    )
    return response
