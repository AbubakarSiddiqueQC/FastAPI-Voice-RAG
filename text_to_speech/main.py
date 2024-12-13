# Main imports
from io import BytesIO
from pathlib import Path
from typing import Annotated
from fastapi import FastAPI, File, Form, HTTPException, status
from fastapi.responses import StreamingResponse,FileResponse
import logging
import os, sys

# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path to the parent directory
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to the Python path
sys.path.append(parent_dir)

#imports functions or constants
from tts import *
# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initiate App
app = FastAPI()

# Directory to save uploaded files
UPLOAD_DIR = Path(parent_dir+"/tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health", status_code=status.HTTP_200_OK)
async def check_health():
    """
    Health check endpoint to verify the service is running.
    """
    logging.info("Health check successful.")
    return {"response": "healthy"}

def iterfile(stream_file):
    with open(stream_file, mode='rb') as file_like:
        yield from file_like
        
@app.get("/tts")
async def tts(text: str):
    """
    Text to speech service
    """
    try:
        logging.info(f"Text to convert into audio: {text}")
        response = convert_text_to_speech(text)
        # Return the audio stream as a response
        return StreamingResponse(response.iter_bytes(), media_type="audio/mpeg")
    except Exception as e:
        logging.error(f"Error converting text to speech file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while converting text to audio file.",
        )
    
