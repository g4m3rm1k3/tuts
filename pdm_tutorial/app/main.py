# main.py

import os
import logging
import asyncio
from pathlib import Path
from pydantic import BaseModel

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

VALID_EXTENSIONS = {".mcam", ".vnc"}

app = FastAPI(title="SourceRevision", version="0.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

REPO_PATH = "repo"


# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/files")
async def get_files():
    logger.info("Fetching all files")
    files_to_return = []
    try:
        # Get a slit of all the items in the directory
        repo_files = os.listdir(REPO_PATH)
        for filename in repo_files:
            # For now, we'll assum every file is 'available'
            # We also filter to only show files we care about
            if Path(filename).suffix in VALID_EXTENSIONS:
                files_to_return.append(
                    {"name": filename, "status": "available"})
    except FileNotFoundError:
        print(f"ERROR: The repository directory '{REPO_PATH}' was not found.")
        # Retrun an empty list if the directory doesn't exist
        return []

    return files_to_return


@app.get("/api/files/{filename}")
def get_file(filename: str):
    # The {filename} in the paht is captured here
    valid_files = [file for file in os.listdir(REPO_PATH)]
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


@app.get("/api/parts/{part_number}")
def get_part(part_number: int):
    return {
        "part_number": part_number,
        "type": type(part_number).__name__
    }


@app.get("/api/search")
def search_files(
    query: str = "",
    status: str = "all",
    limit: int = 10
):
    return {
        "query": query,
        "status": status,
        "limit": limit,
        "results": f"Searching for '{query} with status='{status}', showing {limit} results"
    }


@app.get("/sync-slow")
def sync_slow():
    import time
    time.sleep(2)  # BLOCKS everything
    return {"message": "Sync done"}


@app.get("/async-fast")
async def async_fast():
    await asyncio.sleep(2)  # Does Not block
    return {"message": "Async done"}


class FileCheckout(BaseModel):
    filename: str
    user: str
    message: str


@app.post("/api/checkout")
def checkout_file(checkout: FileCheckout):
    return {
        "success": True,
        "message": f"User '{checkout.user}' checked out '{checkout.filename}'",
        "details": checkout.message
    }
