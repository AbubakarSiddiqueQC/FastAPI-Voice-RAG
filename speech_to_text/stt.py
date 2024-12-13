import os, sys

# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path to the parent directory
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to the Python path
sys.path.append(parent_dir)

#imports functions or constants
from open_ai_client import client
def convert_audio_to_text(audio_file):
  try:
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
      )
    print(transcription.text)
    return transcription.text
  except Exception as e:
    return e
  