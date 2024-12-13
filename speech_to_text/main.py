# Main imports
from pathlib import Path
from typing import Annotated
from fastapi import FastAPI, File, UploadFile, HTTPException, status
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
from Constants import *
from stt import *
# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initiate App
app = FastAPI()


@app.get("/health", status_code=status.HTTP_200_OK)
async def check_health():
    """
    Health check endpoint to verify the service is running.
    """
    logging.info("Health check successful.")
    return {"response": "healthy"}


@app.post("/stt")
async def upload_file(
    file: Annotated[UploadFile, File(description="Audio file to be uploaded to convert into text")],
):
    """
    speech to text service
    """
    try:
        # check file type if allowed 
        if file.content_type not in ALLOWED_FILE_TYPES_AUD:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="File type not supported. Only Audio file supported.",
            )
        
        # Save the file temporarily
        with open(file.filename, "wb") as buffer:
            buffer.write(file.file.read())
        audio_input = open(file.filename, "rb")
        
        text = convert_audio_to_text(audio_input)
        return {
            "message": f"Audio File {file.filename} successfully converted to text.",
            "file_type": file.content_type,
            "transcription":text
        }
    except Exception as e:
        logging.error(f"Error converting text to speech file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while converting text to audio file.",
        )
    finally:
        try:
            os.remove(file.filename)
        except OSError as e:
            # If it fails, inform the user.
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e,
        )
    
