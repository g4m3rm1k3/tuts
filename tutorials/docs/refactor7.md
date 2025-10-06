Let's do it. We've laid a fantastic foundation, and now we get to the really satisfying part.

Welcome to **Phase 3: Refactoring the API Layer**. In this phase, we'll dismantle the long list of API endpoints in your original file and rebuild them in a clean, professional way. We'll use two of FastAPI's most powerful features to achieve this: **API Routers** and **Dependency Injection**.

---

### The "Why": API Routers and Dependency Injection

These two concepts are fundamental to building scalable and maintainable web applications.

#### 1\. API Routers: The Application's Switchboard

Imagine your application is a large office building. In the original script, every call goes to a single, overwhelmed receptionist in the lobby who has to know how to route every single request.

**API Routers** are like giving each department its own specialized receptionist.

- One router will handle all calls related to **authentication** (`/login`, `/logout`).
- Another router will handle all calls for **file operations** (`/files/checkout`, `/files/checkin`).

This keeps our main application file (`app/main.py`) incredibly simple. Its only job is to direct traffic to the correct router. This makes the codebase vastly easier to navigate and expand.

#### 2\. Dependency Injection: Getting What You Need, When You Need It

This is the most important concept in this phase. It's how we will finally eliminate the global `app_state` dictionary.

- **The Old Way (Global State):** Your original functions had to reach out to a global `app_state` dictionary to grab the tools they needed (like the `git_repo` or `metadata_manager`). This is like a chef having to run to a giant, messy, shared pantry every time they need an ingredient. It's unpredictable and makes the chef's recipe (the function) hard to test in isolation.

- **The New Way (Dependency Injection):** Instead of our functions fetching their own dependencies, we will "inject" or provide those dependencies to them as arguments. FastAPI handles this automatically and elegantly with its `Depends` system. This is like a professional kitchen where an assistant brings the chef the exact ingredients they need for a recipe right when they need them.

The benefits are immense:

- **Explicit is Better:** A function's signature makes it crystal clear what "ingredients" or services it needs to do its job.
- **Insanely Testable:** When we test an API endpoint, we can easily provide a "mock" or fake `GitService`. This is a superpower for writing reliable tests.
- **Decoupled Code:** Our API endpoints are now decoupled from _how_ their dependencies are created. They just know they'll receive a working `GitService`.

Let's put this into practice.

---

### Stage 3.1: Creating Dependency Providers

First, we'll create a special file to teach FastAPI how to "provide" our services.

#### Your Action Item

Create the file `backend/app/api/dependencies.py` and add the following code. These functions are our "dependency providers"—they are the "kitchen assistants" that prepare our services.

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Generator

# Import the managers and services we've created
from app.core.config import ConfigManager
from app.services.lock_service import MetadataManager, ImprovedFileLockManager
from app.services.git_service import GitRepository
from app.core.security import UserAuth

# --- Dependency Provider Functions ---

# This function will be a singleton factory for the ConfigManager.
# It ensures we only create one instance of it for the entire application life.
_config_manager = ConfigManager()
def get_config_manager() -> ConfigManager:
  return _config_manager

# The following functions depend on the ConfigManager to get settings.
# FastAPI will automatically resolve this chain of dependencies.

def get_lock_manager(config: ConfigManager = Depends(get_config_manager)) -> Generator[MetadataManager, None, None]:
  # This is a placeholder for now. We will wire this up properly once the full
  # application initialization logic is moved to main.py's lifespan event.
  # For now, this structure allows our code to be organized correctly.
  yield MetadataManager(repo_path=Path(config.config.local.get("repo_path", "./temp_repo")))

def get_git_repo(config: ConfigManager = Depends(get_config_manager)) -> Generator[GitRepository, None, None]:
  # Placeholder similar to the one above.
  yield GitRepository(...)

def get_user_auth(git_repo: GitRepository = Depends(get_git_repo)) -> Generator[UserAuth, None, None]:
  yield UserAuth(git_repo=git_repo)


# --- Security and Authentication Dependencies ---

reusable_oauth2 = HTTPBearer(
  scheme_name="Bearer"
)

def get_current_user(
  token: HTTPAuthorizationCredentials = Depends(reusable_oauth2),
  auth_service: UserAuth = Depends(get_user_auth)
) -> dict:
  """
  Dependency to verify the JWT token from the Authorization header and return the user payload.
  This will protect our endpoints.
  """
  payload = auth_service.verify_token(token.credentials)
  if not payload:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid or expired token",
      headers={"WWW-Authenticate": "Bearer"},
    )
  return payload

def get_current_admin_user(current_user: dict = Depends(get_current_user)) -> dict:
  """
  Dependency that requires the user to be an admin.
  """
  if not current_user.get("is_admin"):
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="The user does not have administrative privileges",
    )
  return current_user
```

_Note: Some of these providers are placeholders because they depend on the full application startup logic, which we haven't refactored yet. But this structure is the correct professional pattern._

---

### Stage 3.2: Creating Your First API Router

Now, let's create our first router for authentication and refactor the `/login` endpoint to use our new dependency system.

#### Your Action Items

1. Create a new file at `backend/app/api/routers/auth.py`.
2. Add the following code to it. Compare the new `login` function to the old one—see how much simpler it is\! It just declares the dependencies it needs (`UserAuth`) and FastAPI provides them.

<!-- end list -->

```python
from fastapi import APIRouter, Depends, HTTPException, Response, status, Form
from app.core.security import UserAuth, ADMIN_USERS
from app.api.dependencies import get_user_auth
from app.models import schemas # We import our schemas now!

router = APIRouter(
  prefix="/auth", # All routes in this file will start with /auth
  tags=["Authentication"], # Group these endpoints in the API docs
)

@router.post("/login")
async def login(
  response: Response,
  username: str = Form(...),
  password: str = Form(...),
  auth_service: UserAuth = Depends(get_user_auth)
):
  """Handles user login and sets a secure, httpOnly cookie for authentication."""
  if not auth_service.verify_user(username, password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )

  access_token = auth_service.create_access_token(username)

  response.set_cookie(
    key="auth_token",
    value=access_token,
    httponly=True, # The cookie cannot be accessed by client-side JavaScript
    secure=False, # In production with HTTPS, this should be True
    samesite="lax",
    max_age=28800 # Expires in 8 hours
  )

  return {
    "status": "success",
    "username": username,
    "is_admin": username in ADMIN_USERS
  }

# We will move the other authentication endpoints here in the next step.
```

3. Finally, open `backend/app/main.py` and tell it to use your new router. Replace the entire file with this updated version:

<!-- end list -->

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# NEW: Import the router we just created
from app.api.routers import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
  logging.info("Application starting up...")
  yield
  logging.info("Application shutting down.")


app = FastAPI(
  title="Mastercam GitLab Interface",
  description="A comprehensive file management system for Mastercam and GitLab.",
  version="2.0.0",
  lifespan=lifespan
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  methods=["*"],
  allow_headers=["*"],
)

# NEW: Tell the main app to include all the routes from our auth router
app.include_router(auth.router)


@app.get("/")
async def root():
  return {"message": "Welcome to the Mastercam PDM Refactored API"}

```

---

We just completed a huge step\! We've introduced two of the most powerful patterns in modern web development and completely refactored our first endpoint. The logic is now clean, decoupled, and testable.

Confirm you're ready, and we will continue this process by migrating the rest of the authentication endpoints to our new router.
