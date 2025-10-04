from fastapi import FastAPI
import asyncio
from pydantic import BaseModel


class FileCheckout(BaseModel):
    filename: str
    user: str
    message: str


app = FastAPI()


@app.post("/api/checkout")
def checkout_file(checkout: FileCheckout):
    return {
        "success": True,
        "message": f"User '{checkout.user}' checked out '{checkout.filename}'",
        "details": checkout.message
    }


@app.get("/")
def read_root():
    return {"message": "Hello world"}


@app.get("/api/files")
def get_files():
    # Hardcoded for now - we'll make this real later
    files = [
        {"name": "4500124.mcam", "status": "avaialble"},
        {"name": "4800147.mcam", "status": "checked_out"},
        {"name": "1810012.mcam", "status": "avaialble"},
    ]
    return {"files": files}


@app.get("/api/files/{filename}")
def get_file(filename: str):
    # Teh {filename} in the path is captured here
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
    limit:  int = 10
):
    return {
        "query": query,
        "status": status,
        "limit": limit,
        "results": f"Searching for '{query}' with status='{status}', showing {limit} results"
    }


@app.get("/sync-slow")
def sync_slow():
    import time
    time.sleep(4)  # BLOCKS everything
    return {"message": "Sync done"}


@app.get("/async-fast")
async def async_fast():
    await asyncio.sleep(4)  # DOES NOT block
    return {"message": "Async done"}
