import os
import json
import msvcrt
from datetime import datetime, timezone
from pathlib import Path
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import logging
import asyncio

VALID_EXTENSIONS = {".mcam", ".vnc"}

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

app = FastAPI(title="PDM",
              descrption="The API for PDM",
              version="0.0.0"
              )

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"),  name="static")


class File(BaseModel):
    name: str
    status: str

# Data model for checkout


class FileCheckout(BaseModel):
    filename: str
    user: str
    message: str


class CheckoutRequest(BaseModel):
    filename: str
    user: str
    message: str = Field(..., min_length=1, max_length=500)


class CheckinRequest(BaseModel):
    filename: str
    user: str

# LOCK MANAGEMENT FUNCTIONS


class LockedFile:
    """Context manager for file locking
    Ensures only one process can access the file at a time

    Raises:
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, filepath, mode='r'):
        self.filepath = filepath
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filepath, self.mode)
        # Acquire exlusive lock (blocks until available)
        msvcrt.flock(self.file, msvcrt.LOCK_EX)
        logger.debug(f"Acquired lock on {self.filepath}")
        return self.file

    def __exit__(self, exe_type, exc_val, exc_tb):
        # Release lock
        msvcrt.flock(self.file, msvcrt.LOCK_UN)
        self.file.close()
        logger.debug(f"Released lock on {self.filepath}")
        return False


def load_locks() -> dict:
    """Load lock data from locks.json

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        dict: _description_
    """
    if not LOCKS_FILE.exists():
        logger.info("Locks file doesn't exist, returning empty dict")
        return {}

    try:
        with LockedFile(LOCKS_FILE, 'r') as f:
            locks = json.load(f)
        logger.info(f"Loaded {len(locks)} locks from file")
        return locks
    except josn.JSONDecoderError as e:
        logger.error(f"Error parsing locks.json: {e}")
        return {}


def save_locks(locks: dict):
    """Save lock data to locks.json

    Args:
        locs (dict): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:
        with LockedFile(LOCKS_FILE, 'w') as f:
            json.dump(locks, f, indent=4)
        logger.info(f"Saved {len(locks)} locks from file")
    except Exception as e:
        logger.error(f"Error saving locks: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to save lock data"
        )


def is_locked(filename: str) -> bool:
    """Check if a file is curently locked

    Args:
        filename (str): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        bool: 

    """
    locks = load_locks()
    return filename in locks


def get_lock_info(filename: str) -> dict:
    """Get lock information for a specific file

    Args:
        filename (str): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        dict: _description_
        None: if not locked
    """
    locks = load_locks()
    return locks.get(filename)


# Serve the main HTML file at teh root


@app.get("/")
def read_root():
    return FileResponse("static/index.html")


@app.get("/api/files")
def get_files():
    logger.info("Fetching all files")
    """Returns a list of all cam files in the repository

    Raises:
        HTTPException: 500

    Returns:
        dict: files
    """
    logger.info(f"Scanning repository: {REPO_PATH}")

    # Check if repo directroy exists
    if not REPO_PATH.exists():
        logger.error(f"Repository path does not exists: {REPO_PATH}")
        raise HTTPException(
            status_code=500,
            detail="Repository directory not found"
        )

    # Load lock information
    locks = load_locks()

    # Get all files in repo directory
    all_items = os.listdir(REPO_PATH)
    logger.info(f"Found {len(all_items)} items in repo")

    # Filter to only cam files
    files = []
    for filename in all_items:
        # Build full path
        full_path = REPO_PATH / filename

        # Check if it's safe (not directory) and has cam extension
        if full_path.is_file() and Path(filename).suffix in VALID_EXTENSIONS:
            # Check if file is locked
            if filename in locks:
                lock_info = locks[filename]
                status = "checked_out"
                locked_by = lock_info["user"]
            else:
                status = "available"
                locked_by = None
            files.append({
                "name": filename,
                "status": status,  # For now, all are available
                "size": full_path.stat().st_size,  # Size in bytes
                "locked_by": locked_by
            })
    logger.info(f"Returning {len(files)} cam files")
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


@app.post("/api/files/checkout")
def checkout_file(request: CheckoutRequest):
    """Checkout a file (acquire lock).

    Args:
        reqeust (CheckoutRequest): _description_
    """
    logger.info(f"Checkout request: {request.user} -> {request.filename}")

    # Check if file exists
    file_path = REPO_PATH / request.filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    # Load current locks
    locks = load_locks()

    # Check if already locked
    if request.filename in locks:
        existing_lock = locks[request.filename]
        raise HTTPException(
            status_code=409,
            detail={
                "error": "File is already checked out",
                "locked_by": existing_lock["user"],
                "locked_at": existing_lock["timestamp"]
            }
        )
    # Create lock
    locks[request.filename] = {
        "user": request.user,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": request.message
    }

    # Save locks
    save_locks(locks)

    logger.info(f"File checkout out successfully: {request.filename}")

    return {
        "success": True,
        "message": f"File '{request.filename}' checked out by {request.user}"
    }


@app.post("/api/files/checkin")
def checkin_file(request: CheckinRequest):
    """Checkin File (release lock).

    Args:
        request (CheckinRequest): _description_
    """
    logger.info(f"Checkin request: {request.user} -> {request.filename}")

    # Load current locks
    locks = load_locks()

    # Check if file is locked
    if request.filename not in locks:
        raise HTTPException(
            status_code=400,
            detail="File is not checked out"
        )

    # Verify user owns the lock
    lock_info = locks[request.filename]
    if lock_info["user"] != request.user:
        raise HTTPException(
            status_code=403,
            detail=f"File is locked by {lock_info['user'], not {request.user}}"
        )

    # Remove lock
    del locks[request.filename]

    # Save locks
    save_locks(locks)

    logger.info(f"File checked in successfully: {request.filename}")

    return {
        "success": True,
        "message": f"File '{request.filename}' checked in by {request.user}"
    }
