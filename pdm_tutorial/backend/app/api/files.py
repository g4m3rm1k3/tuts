"""
File management API endpoints

This file contains ONLY route definitions.
Business logic will go in services/ (Stage 3)
"""


from fastapi import APIRouter, HTTPException, status
from app.schemas.files import FileInfo, FileListResponse
from typing import List

# SECTION 1. Router Setup
# ======================

router = APIRouter(
    prefix="/api/files",
    tags=["files"],
)

# SECTION 2: Hardcoded Data (Temporary - Stage 3 will read from filesystem)
# =========================

MOCK_FILES = [
    {"name": "4200124.mcam", "status": "available",
        "size_bytes": 1234567, "locked_by": None},
    {"name": "4806148.mcam", "status": "checked_out",
        "size_bytes": 2345678, "locked_by": "mmclean"},
    {"name": "4604524.mcam", "status": "available",
        "size_bytes": 987654, "locked_by": None},

]

# SECTION 3: GET endpoints
# ========================


@router.get("/", response_model=FileListResponse)
def get_files():
    return FileListResponse(files=MOCK_FILES, total=len(MOCK_FILES))


@router.get("/{filename}", response_model=FileInfo)
def get_file(filename: str):
    for file in MOCK_FILES:
        if file["name"] == filename:
            return FileInfo(**file)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"File '{filename}' not found"
    )

# SECTION 4. Placeholder Endpoints (Will implement in Stage 3)


@router.post("/checkout")
def checkout_file():
    return {"message": "Checkout endpoint - comming in stage 3"}


@router.post("/checkin")
def checkin_file():
    return {"message": "Checkin endpoint - comming in stage 3"}
