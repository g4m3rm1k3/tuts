from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI(title="SourceRevision", version="0.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/files")
async def get_files():
    mock_files_data = [
        {"name": "4600548.mcam", "status": "available"},
        {"name": "4200874.mcam", "status": "checked_out"},
        {"name": "4804125.mcam", "status": "available"},
    ]
    return mock_files_data
