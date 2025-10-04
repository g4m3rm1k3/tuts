# main.py

import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

VALID_EXTENSIONS = {".mcam", ".vnc"}

app = FastAPI(title="SourceRevision", version="0.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

REPO_PATH = "repo"


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/files")
async def get_files():
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
