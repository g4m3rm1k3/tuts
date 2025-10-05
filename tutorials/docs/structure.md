# Progressive Code Organization Map

This guide tells you WHERE to put code as you build it, not after. Reference this alongside the tutorial - when the tutorial says "add this to main.py," check here first to see if it should actually go somewhere else.

---

## STAGE 0: Environment Setup

**Keep simple - everything in root:**

```
pdm-tutorial/
├── backend/
│   └── (empty for now)
├── venv/
└── .gitignore
```

**Why**: Too early to organize. Learn the basics first.

---

## STAGE 1: First Backend - Time to Organize

**When the tutorial says "create backend/main.py":**

**Actually create this structure:**

```
backend/
├── app/
│   ├── __init__.py          # Empty for now
│   ├── main.py              # Main app entry point
│   └── config.py            # We'll add this in Stage 5
├── static/                  # For Stage 2
└── requirements.txt
```

**File: `backend/app/main.py`**

```python
from fastapi import FastAPI

app = FastAPI(
    title="PDM Backend API",
    description="The API for the Parts Data Management system.",
    version="0.1.0",
)

@app.get("/")
def read_root():
    return {"message": "Hello from the PDM Backend!"}
```

**File: `backend/app/__init__.py`**

```python
# Empty for now - we'll use this in Stage 11
```

**Update your run command:**

```bash
# OLD: uvicorn main:app --reload
# NEW:
uvicorn app.main:app --reload
```

**Why**: Starting with `app/` folder establishes that this isn't just a script - it's an application package. The `__init__.py` makes it a proper Python package.

---

## STAGE 1 (continued): Adding More Endpoints

**When tutorial says "add to main.py":**

**Actually do this:**

Keep simple endpoints in `main.py` for now, but organize imports at the top:

```python
# app/main.py
from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI(...)

# Your routes here
```

**Why**: Stages 1-2 are still learning basics. Don't over-organize yet.

---

## STAGE 2: Frontend - Organize Static Files

**Tutorial says "create static/index.html":**

**Actually create:**

```
backend/
├── app/
│   └── main.py
└── static/
    ├── css/
    │   ├── tokens.css       # Design system
    │   ├── base.css         # Base styles
    │   ├── components.css   # Component styles
    │   └── main.css         # Imports the others
    ├── js/
    │   └── app.js
    └── index.html
```

**File: `backend/static/css/main.css`**

```css
@import "tokens.css";
@import "base.css";
@import "components.css";
```

**Why**:

- **Separation of concerns**: Tokens, base, components each have one job
- **Maintainability**: Finding a button style is easy - it's in components.css
- **Scalability**: Can add new component files without touching existing ones

---

## STAGE 3: File Operations - First Service Layer

**Tutorial says "add these functions to main.py":**

**DON'T. Instead:**

**Create:**

```
backend/app/
├── main.py
├── services/
│   ├── __init__.py
│   └── file_service.py
└── utils/
    ├── __init__.py
    └── file_locking.py
```

**File: `backend/app/utils/file_locking.py`**

```python
import os
if os.name == 'nt':
    import msvcrt
else:
    import fcntl

class LockedFile:
    """Cross-platform file locking context manager."""
    # ... (the LockedFile class code)
```

**File: `backend/app/services/file_service.py`**

```python
from pathlib import Path
import json
from app.utils.file_locking import LockedFile

def load_locks(locks_file: Path) -> dict:
    if not locks_file.exists():
        return {}

    try:
        with LockedFile(locks_file, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_locks(locks_file: Path, locks: dict):
    with LockedFile(locks_file, 'w') as f:
        json.dump(locks, f, indent=4)
```

**File: `backend/app/main.py`** (imports only)

```python
from pathlib import Path
from app.services.file_service import load_locks, save_locks
from app.utils.file_locking import LockedFile

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent  # Goes up to 'backend'
REPO_PATH = BASE_DIR / 'repo'
LOCKS_FILE = BASE_DIR / 'locks.json'

# Your route functions here use the imported functions
```

**Why**:

- **utils/**: Reusable utilities (locking mechanism) with no business logic
- **services/**: Business logic (how to load/save locks)
- **main.py**: Routes only - delegate to services

**Rule of thumb**: If a function doesn't have `@app` decorator, it probably doesn't belong in main.py.

---

## STAGE 4: UI Components - Modularize Frontend

**Tutorial says "add ModalManager to app.js":**

**Actually create:**

```
backend/static/js/
├── modules/
│   ├── modal-manager.js
│   ├── notifications.js
│   └── theme-manager.js
└── app.js
```

**File: `backend/static/js/modules/modal-manager.js`**

```javascript
export class ModalManager {
  constructor(modalId) {
    this.modal = document.getElementById(modalId);
    // ... rest of implementation
  }
  // ...
}
```

**File: `backend/static/js/app.js`**

```javascript
import { ModalManager } from "./modules/modal-manager.js";
import { ThemeManager } from "./modules/theme-manager.js";

const checkoutModal = new ModalManager("checkout-modal");

document.addEventListener("DOMContentLoaded", () => {
  // Your initialization
});
```

**Update `index.html`:**

```html
<script type="module" src="/static/js/app.js"></script>
```

**Why**:

- **Modules**: ES6 modules keep related code together
- **Reusability**: Can use ModalManager in other projects
- **Testing**: Can test modules in isolation

---

## STAGE 5: Authentication - Separate Auth Logic

**Tutorial says "add JWT functions to main.py":**

**Create this structure:**

```
backend/app/
├── main.py
├── config.py              # NEW
├── schemas/               # NEW
│   ├── __init__.py
│   └── auth.py
├── services/
│   ├── __init__.py
│   ├── file_service.py
│   └── auth_service.py    # NEW
├── api/                   # NEW
│   ├── __init__.py
│   ├── deps.py
│   └── auth.py
└── utils/
    └── ...
```

**File: `backend/app/config.py`**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

**File: `backend/app/schemas/auth.py`**

```python
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    full_name: str
    role: str
```

**File: `backend/app/services/auth_service.py`**

```python
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
```

**File: `backend/app/api/deps.py`**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.config import settings
from app.schemas.auth import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # ... validation logic
    return User(username=username, full_name=full_name, role=role)
```

**File: `backend/app/api/auth.py`**

```python
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token
from app.services.auth_service import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Login logic here
    pass
```

**File: `backend/app/main.py`** (now much simpler)

```python
from fastapi import FastAPI
from app.api import auth

app = FastAPI(...)

# Include the auth router
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Hello from PDM!"}
```

**Why**:

- **config.py**: Single source of truth for settings
- **schemas/**: Data shape definitions (Pydantic models)
- **services/**: Pure business logic (no HTTP concerns)
- **api/**: HTTP layer (routes and dependencies)
- **Separation**: Services can be reused; routes are just thin wrappers

**Key principle**: Routes should be ~5 lines max. They validate input, call a service, return response.

---

## STAGE 6: RBAC - Dependencies Pattern

**Tutorial says "add require_role to main.py":**

**Add to existing `app/api/deps.py`:**

```python
from typing import List

def require_role(allowed_roles: List[str]):
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user
    return role_checker

# Convenience aliases
require_admin = require_role(["admin"])
```

**Create `app/api/admin.py`:**

```python
from fastapi import APIRouter, Depends
from app.api.deps import require_admin
from app.schemas.auth import User

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.delete("/files/{filename}")
def delete_file(filename: str, current_user: User = Depends(require_admin)):
    # Implementation
    pass
```

**Update `app/main.py`:**

```python
from app.api import auth, admin

app.include_router(auth.router)
app.include_router(admin.router)
```

**Why**: Each feature area gets its own router file. Main.py just wires them together.

---

## STAGE 7: Git Integration - Service Pattern

**Tutorial says "add Git functions to main.py":**

**Create `backend/app/services/git_service.py`:**

```python
from git import Repo, Actor
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class GitService:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.repo = self._initialize_repo()

    def _initialize_repo(self) -> Repo:
        # Initialization logic
        pass

    def commit_changes(self, file_path: Path, user: str, message: str):
        # Commit logic
        pass
```

**Create `backend/app/services/__init__.py`:**

```python
from app.services.git_service import GitService
from app.services.auth_service import verify_password, create_access_token
from app.services.file_service import load_locks, save_locks

# Create singleton instances
git_service = None  # Will be initialized in startup

__all__ = ["GitService", "git_service", "verify_password", ...]
```

**Update `backend/app/main.py`:**

```python
from app.services import git_service, GitService
from pathlib import Path

@app.on_event("startup")
def startup_event():
    global git_service
    git_service = GitService(Path(__file__).parent.parent / 'git_repo')
```

**Why**:

- Services are initialized once at startup
- Routes import the singleton instance
- Testable: Can mock git_service in tests

---

## STAGE 9: WebSockets - Separate Module

**Tutorial says "add WebSocket code to main.py":**

**Create `backend/app/websocket/`:**

```
backend/app/
├── websocket/
│   ├── __init__.py
│   ├── manager.py
│   └── routes.py
```

**File: `backend/app/websocket/manager.py`:**

```python
from fastapi import WebSocket
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket

    async def broadcast(self, message: dict):
        # Broadcast logic
        pass

# Singleton instance
manager = ConnectionManager()
```

**File: `backend/app/websocket/routes.py`:**

```python
from fastapi import APIRouter, WebSocket, Depends
from app.websocket.manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    # WebSocket logic
    pass
```

**Update `backend/app/main.py`:**

```python
from app.websocket import routes as ws_routes

app.include_router(ws_routes.router)
```

**Frontend: `backend/static/js/modules/websocket.js`:**

```javascript
export class WebSocketClient {
  constructor() {
    this.ws = null;
  }

  connect() {
    // Connection logic
  }
}

export const wsClient = new WebSocketClient();
```

**Why**: WebSocket is complex enough to deserve its own module. Manager handles connections, routes handle endpoints.

---

## STAGE 10: Testing - Proper Structure from Start

**Create test structure immediately:**

```
backend/
├── app/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_files.py
│   └── test_websockets.py
```

**File: `backend/tests/conftest.py`:**

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)
```

**Why**: Tests mirror the app structure. One test file per route file.

---

## STAGE 11: Database - Models Separate from Start

**When adding database, create:**

```
backend/app/
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── file_lock.py
├── database.py
└── ...
```

**File: `backend/app/models/user.py`:**

```python
from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    # ...
```

**Why**: Models are your data layer. Keep them isolated.

---

## Complete Final Structure

```
pdm-tutorial/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Entry point only
│   │   ├── config.py            # Settings
│   │   ├── database.py          # DB connection
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── file_lock.py
│   │   ├── schemas/             # Pydantic models
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── files.py
│   │   ├── services/            # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── git_service.py
│   │   │   ├── file_service.py
│   │   │   └── cache_service.py
│   │   ├── api/                 # Routes
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   ├── auth.py
│   │   │   ├── files.py
│   │   │   └── admin.py
│   │   ├── websocket/           # WebSocket
│   │   │   ├── __init__.py
│   │   │   ├── manager.py
│   │   │   └── routes.py
│   │   └── utils/               # Utilities
│   │       ├── __init__.py
│   │       └── file_locking.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── tokens.css
│   │   │   ├── base.css
│   │   │   ├── components.css
│   │   │   └── main.css
│   │   ├── js/
│   │   │   ├── modules/
│   │   │   │   ├── store.js
│   │   │   │   ├── api.js
│   │   │   │   ├── websocket.js
│   │   │   │   └── modal-manager.js
│   │   │   └── app.js
│   │   └── index.html
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   └── test_files.py
│   └── requirements.txt
```

---

## Organization Rules

**When tutorial says "add to main.py", ask:**

1. **Is it a route?** → Put in `app/api/[feature].py`
2. **Is it business logic?** → Put in `app/services/[feature]_service.py`
3. **Is it a data model?** → Put in `app/models/[name].py` or `app/schemas/[name].py`
4. **Is it a reusable utility?** → Put in `app/utils/[name].py`
5. **Is it configuration?** → Put in `app/config.py`

**Never put in main.py**: Functions, classes, business logic, utilities

**Always in main.py**: App creation, router inclusion, startup events

This way, you build properly from the start and learn good habits immediately.
