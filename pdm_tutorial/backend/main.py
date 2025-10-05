import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import logging
import asyncio

# Get absolute path to the directory containin this file
BASE_DIR = Path(__file__).resolve().parent

# Path to repository folder
REPO_PATH = BASE_DIR / 'repo'

# Path to locs file (we'll create this soon)
LOCKS_FILE = BASE_DIR / 'locks.json'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"),  name="static")

# Data model for checkout


class FileCheckout(BaseModel):
    filename: str
    user: str
    message: str

# Serve the main HTML file at teh root


@app.get("/")
def read_root():
    return FileResponse("static/index.html")


@app.get("/api/files")
def get_files():
    logger.info("Fetching all files")
    # Hardcoded for now - we'll make this real later
    files = [
        {"name": "4500124.mcam", "status": "avaialble"},
        {"name": "4800147.mcam", "status": "checked_out"},
        {"name": "1810012.mcam", "status": "avaialble"},
    ]
    logger.info(f"Returning {len(files)} files")
    return {"files": files}


@app.get("/api/files/{filename}")
def get_file(filename: str):
    # Teh {filename} in the path is captured here
    # Simulate checking if file exists
    valid_files = ["4801247.mcam", "1810118.mcam"]
    if filename not in valid_files:
        raise HTTPException(
            status_code=404,
            detail=f"File '{filename}' not found"
        )
    return {
        "filename": filename,
        "status": "available",
        "size": "1.2 MB",
        "last_modified": "2025-10-01"
    }


@app.post("/api/checkout")
def checkout_file(checkout: FileCheckout):
    return {
        "success": True,
        "message": f"User '{checkout.user}' checked out '{checkout.filename}'",
        "details": checkout.message
    }


@app.get("/async-demo")
async def async_demo():
    logger.info("Starting async operation")
    await asyncio.sleep(1)
    await asyncio.sleep(1)
    logger.info("Async operation complete")
    return {"messsage": "Async done"}
