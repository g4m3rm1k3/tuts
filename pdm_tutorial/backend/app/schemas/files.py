"""
Pydantic schemas for file operaions.
These define the shape of request/response data
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# SECTION 1: Response Models
# ===========================


class FileInfo(BaseModel):
    """
    Represents a single file in the respository
    This is what we send to the client
    """
    name: str = Field(..., description="Filename")
    status: str = Field(..., description="available or checked_out")
    size_bytes: int = Field(..., description="File size in bytes")
    locked_by: Optional[str] = Field(
        None, description="Username who locked the file")

    class Config:
        # Example for API documentation
        schema_extra = {
            "example": {
                "name": "4806148.mcam",
                "status": "available",
                "size_bytes": 1234567,
                "locked_by": None
            }
        }


class FileListResponse(BaseModel):
    """
    Response for GET /api/files endpoint
    """
    files: List[FileInfo]
    total: int = Field(..., description="Total number of files")


# SECTION 2: Request Models (for future stages)
# ========================

class FileCheckoutRequest(BaseModel):
    """Request body for checking out a file."""
    filename: str = Field(..., min_length=1)
    user: str = Field(..., min_length=3)
    message: str = Field(..., min_length=1, max_length=500)


class FileCheckinRequest(BaseModel):
    """Request body for checking in a file"""
    filename: str
    user: str
