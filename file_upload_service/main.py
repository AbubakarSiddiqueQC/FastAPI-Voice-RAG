# Main imports
from pathlib import Path
from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
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
from file_db import *
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


@app.post("/upload-file", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: Annotated[UploadFile, File(description="The file to be uploaded (e.g., document, audio, etc.)")],
    department: Annotated[str, Form(description="Specify the department related to this file (One of these, HR, Tech, Accounts.)")],
):
    """
    Upload a file along with additional parameters.a
    """
    # check file type if allowed 
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="File type not supported. Supported file types are : PDF, TXT, DOCX",
        )
    # check Department if allowed 
    if department not in ALLOWED_DEPARTMENTS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Department is not supported. Supported departments are : HR, Tech, Accounts",
        )
    
    # Validate file size (example: 1 MB limit)
    max_file_size = 1 * 1024 * 1024  # 1 MB
    file_content = await file.read()
    if len(file_content) > max_file_size:
        logging.error(f"File size exceeded: {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds 1 MB limit.",
        )
    
    # Save the file in the UPLOAD_DIR
    file_path = UPLOAD_DIR / file.filename
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        logging.info(f"File {file.filename} saved successfully.")

        # store file matadata in db
        try:
            insert_file(file.filename, file.content_type, str(file_path), department)
        except Exception as e:
            logging.error(f"Error saving file {file.filename}: {e}")
            raise HTTPException(
                status_code=status.WS_1011_INTERNAL_ERROR,
                detail="file is not saved in database.",
            )
        return {
            "message": f"File {file.filename} uploaded successfully.",
            "file_type": file.content_type
        }
    except Exception as e:
        logging.error(f"Error saving file {file.filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving the file.",
        )
    finally:
        # Cleanup: Free memory of file content after processing
        del file_content

