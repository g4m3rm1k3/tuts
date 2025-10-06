# Chapter 1.7-1.10: API Layer & Dependency Injection

## Chapter 1.7: Request/Response Schemas

**Purpose**: Validate inputs, serialize outputs. API contracts independent of domain models.

**File**: `backend/schemas/requests.py`

```python
from pydantic import BaseModel, Field, field_validator

class CheckoutRequest(BaseModel):
    """Request to checkout a file."""
    filename: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1, max_length=500)

    @field_validator('filename')
    @classmethod
    def validate_filename(cls, v: str) -> str:
        """Prevent path traversal attacks."""
        if '..' in v or '/' in v or '\\' in v:
            raise ValueError('Invalid filename')
        if not v.endswith('.mcam'):
            raise ValueError('Only .mcam files allowed')
        return v

class CheckinRequest(BaseModel):
    """Request to checkin a file."""
    filename: str = Field(..., min_length=1)
```

**File**: `backend/schemas/responses.py`

```python
from pydantic import BaseModel
from datetime import datetime

class LockResponse(BaseModel):
    """Lock information response."""
    filename: str
    locked_by: str
    locked_at: datetime
    message: str

    class Config:
        from_attributes = True  # Allow creating from domain objects

class ErrorResponse(BaseModel):
    """Standard error format."""
    error: str
    detail: str | None = None
    code: str | None = None
```

**Learn more:**

- [Data Transfer Objects (DTO)](https://martinfowler.com/eaaCatalog/dataTransferObject.html) - Why separate from domain
- [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/) - Input sanitization

---

## Chapter 1.8: Dependency Injection

**Why**: Don't hardcode dependencies. Inject them. Testable, flexible, explicit.

**File**: `backend/api/dependencies.py`

```python
from fastapi import Depends
from typing import Annotated
from domain.locks import LockService
from adapters.storage import JSONLockStorage, LockStorage

def get_lock_storage() -> LockStorage:
    """Factory for lock storage."""
    return JSONLockStorage()

def get_lock_service(
    storage: Annotated[LockStorage, Depends(get_lock_storage)]
) -> LockService:
    """Factory for lock service."""
    return LockService(storage)

# Type alias for cleaner route signatures
LockServiceDep = Annotated[LockService, Depends(get_lock_service)]
```

**Pattern explanation**:

```python
# Without DI (bad)
def checkout():
    storage = JSONLockStorage()  # Hardcoded!
    service = LockService(storage)
    service.checkout_file(...)

# With DI (good)
def checkout(service: LockServiceDep):
    service.checkout_file(...)  # Injected automatically
```

**Benefits**:

- Testing: inject mock storage
- Flexibility: swap JSON → Postgres in one place
- Explicit: see what each route needs

**Learn more:**

- [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection) - Core concept
- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) - How FastAPI does it

---

## Chapter 1.9: API Routes (HTTP Layer)

**Philosophy**: Routes are THIN. They translate HTTP → domain calls → HTTP responses.

**File**: `backend/api/routes/locks.py`

```python
from fastapi import APIRouter, HTTPException, status
from core.exceptions import FileLockedException, OwnershipError, FileNotFoundError
from schemas.requests import CheckoutRequest, CheckinRequest
from schemas.responses import LockResponse, ErrorResponse
from api.dependencies import LockServiceDep

router = APIRouter(prefix="/api/locks", tags=["locks"])

@router.post("/checkout", status_code=status.HTTP_201_CREATED)
def checkout_file(
    request: CheckoutRequest,
    service: LockServiceDep,
    # user: CurrentUser  # We'll add auth in Chapter 2
) -> dict:
    """
    Checkout a file for editing.

    - Validates request (Pydantic does this)
    - Calls domain service
    - Translates exceptions to HTTP responses
    """
    try:
        # For now, hardcode user (Chapter 2 will fix)
        service.checkout_file(request.filename, "testuser", request.message)
        return {"message": f"Checked out {request.filename}"}

    except FileLockedException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"File locked by {e.locked_by}"
        )
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/checkin")
def checkin_file(
    request: CheckinRequest,
    service: LockServiceDep
) -> dict:
    """Release lock on a file."""
    try:
        service.checkin_file(request.filename, "testuser")
        return {"message": f"Checked in {request.filename}"}

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except OwnershipError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@router.get("/locks/{filename}", response_model=LockResponse | None)
def get_lock_info(
    filename: str,
    service: LockServiceDep
) -> LockResponse | None:
    """Get lock information for a file."""
    lock = service.get_lock_info(filename)
    if lock is None:
        return None

    # Convert domain object to response schema
    return LockResponse(
        filename=lock.filename,
        locked_by=lock.locked_by,
        locked_at=lock.locked_at,
        message=lock.message
    )
```

**Key patterns**:

1. **Exception translation**: Domain exceptions → HTTP status codes
2. **Thin routes**: Just coordinate, don't contain logic
3. **Type safety**: Pydantic validates inputs/outputs

**Learn more:**

- [RESTful API Design](https://restfulapi.net/) - HTTP semantics
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) - When to use what

---

## Chapter 1.10: Application Factory

**Why factory pattern**: Create app instances for testing, different configs, etc.

**File**: `backend/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.config import settings
from api.routes import locks

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown hooks."""
    # Startup
    print(f"Starting {settings.app_name} in {settings.environment} mode")
    yield
    # Shutdown
    print("Shutting down...")

def create_app() -> FastAPI:
    """
    Application factory.

    Benefits:
    - Can create multiple instances (test vs prod)
    - Configuration happens in one place
    - Easy to extend
    """
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan
    )

    # CORS (for frontend)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    app.include_router(locks.router)

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Catch-all for unhandled exceptions."""
        return {
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else None
        }

    return app

# Create the app instance
app = create_app()

# For development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
```

**Learn more:**

- [Application Factory Pattern](https://flask.palletsprojects.com/en/2.3.x/patterns/appfactories/) - Flask docs but same concept
- [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/) - Startup/shutdown

---

## Chapter 1 Complete: Test It

**Create `.env` file**:

```bash
SECRET_KEY=dev-secret-change-in-production
```

**Run the server**:

```bash
cd backend
uvicorn main:app --reload
```

**Test with curl**:

```bash
# Checkout a file
curl -X POST http://localhost:8000/api/locks/checkout \
  -H "Content-Type: application/json" \
  -d '{"filename": "part001.mcam", "message": "Editing dimensions"}'

# Get lock info
curl http://localhost:8000/api/locks/locks/part001.mcam

# Checkin
curl -X POST http://localhost:8000/api/locks/checkin \
  -H "Content-Type: application/json" \
  -d '{"filename": "part001.mcam"}'
```

**Interactive docs**: http://localhost:8000/docs

---

## Architecture Review

**What we built**:

```
HTTP Request
    ↓
FastAPI Route (thin, just HTTP translation)
    ↓
LockService (orchestrates domain + storage)
    ↓
LockManager (pure business logic)
    ↓
JSONLockStorage (persistence)
```

**Key wins**:

- Each layer has ONE responsibility
- Business logic has zero FastAPI/HTTP knowledge
- Can test domain logic without starting a server
- Can swap storage without touching routes

**What's missing**:

- Authentication (Chapter 2)
- File management (Chapter 3)
- Frontend (Chapter 4)
- Git integration (Chapter 5)

**Next**: Chapter 2 will add JWT authentication, user management, and proper authorization. Want to continue?
