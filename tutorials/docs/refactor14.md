Let's begin the final phase of our backend refactoring. This is where we'll wire everything together, make our dependency injection system fully operational, and officially retire the old monolithic script.

---

## Phase 4: Final Wiring & Cleanup

Our goal now is to bring the application to life in its new structure. We'll do this by properly initializing our services when the application starts and making them available to our API routers.

### Stage 4.1: Implementing the Lifespan Manager

We're going to put the logic from your original `initialize_application` function into the `lifespan` function in `app/main.py`.

#### The "Why": The Application Lifecycle

A web application has a lifecycle: it **starts up** once, **serves** many requests, and then **shuts down** once.

Expensive setup operations, like creating our `ConfigManager` and cloning the `GitRepository`, should only happen during the "startup" phase. It would be incredibly inefficient to do this for every single API request.

FastAPI's `lifespan` manager is the modern, correct place to manage these startup and shutdown events. We will create our service instances here and attach them to a special object called `app.state`. Then, our dependency provider functions (in `dependencies.py`) will simply grab the pre-initialized services from this state object for each request. This is the final piece that connects our services to our API endpoints efficiently.

#### Your Action Items

We have two files to update to complete this wiring.

---

**1. Update the Dependency Providers**

First, let's update `backend/app/api/dependencies.py` so that our provider functions retrieve the services from `app.state` instead of creating them. Replace the entire file with this code:

```python
# backend/app/api/dependencies.py

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# We no longer need to import the services themselves here,
# as we're just retrieving them from the app's state.

# Reusable security scheme
reusable_oauth2 = HTTPBearer(scheme_name="Bearer")

# --- Service Provider Functions ---

def get_config_manager(request: Request):
  return request.app.state.config_manager

def get_lock_manager(request: Request):
  return request.app.state.metadata_manager

def get_git_repo(request: Request):
  return request.app.state.git_repo

def get_user_auth(request: Request):
  return request.app.state.user_auth

# --- Security and Authentication Dependencies ---

def get_current_user(
  token: HTTPAuthorizationCredentials = Depends(reusable_oauth2),
  auth_service = Depends(get_user_auth)
) -> dict:
  """Dependency to verify a token and return the user payload."""
  payload = auth_service.verify_token(token.credentials)
  if not payload:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid or expired token",
    )
  return payload

def get_current_admin_user(current_user: dict = Depends(get_current_user)) -> dict:
  """Dependency that requires the user to be an admin."""
  if not current_user.get("is_admin"):
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="The user does not have administrative privileges.",
    )
  return current_user
```

---

**2. Implement the Lifespan Logic**

Now, let's add the full initialization logic to `backend/app/main.py`. This code combines our dependency providers with the application's lifecycle.

Replace the entire contents of `backend/app/main.py` with this final version:

```python
# backend/app/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from pathlib import Path

# Import all our components
from app.core.config import ConfigManager
from app.services.lock_service import MetadataManager, ImprovedFileLockManager
from app.services.git_service import GitRepository, setup_git_lfs_path
from app.core.security import UserAuth
from app.api.routers import auth, files, admin, config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
  """
  Handles application startup and shutdown events. This is where we
  initialize our services and make them available to the rest of
  the application.
  """
  logger.info("Application starting up...")

  # 1. Setup Git LFS
  setup_git_lfs_path()

  # 2. Initialize Config Manager (Singleton)
  config_manager = ConfigManager()
  app.state.config_manager = config_manager

  cfg = config_manager.config
  gitlab_cfg = cfg.gitlab

  # 3. Initialize Services if configured
  if all(gitlab_cfg.get(k) for k in ['base_url', 'token', 'project_id']):
    try:
      repo_path_str = gitlab_cfg.get("repo_path") # Simplified for this refactor
      if not repo_path_str:
        raise ValueError("Repository path not configured.")
      repo_path = Path(repo_path_str)

      # Initialize all services
      repo_lock_manager = ImprovedFileLockManager(repo_path / ".git" / "repo.lock")
      metadata_manager = MetadataManager(repo_path=repo_path)
      git_repo = GitRepository(
        repo_path=repo_path,
        remote_url=gitlab_cfg['base_url'],
        token=gitlab_cfg['token'],
        config_manager=config_manager,
        lock_manager=repo_lock_manager
      )
      user_auth = UserAuth(git_repo=git_repo)

      # 4. Store services on the app state object
      app.state.metadata_manager = metadata_manager
      app.state.git_repo = git_repo
      app.state.user_auth = user_auth

      logger.info("Application fully initialized.")
    except Exception as e:
      logger.error(f"Initialization failed: {e}", exc_info=True)
      # Set services to None so the app can start in a limited state
      app.state.metadata_manager = None
      app.state.git_repo = None
      app.state.user_auth = None
  else:
    logger.warning("Running in limited mode - GitLab is not configured.")
    app.state.metadata_manager = None
    app.state.git_repo = None
    app.state.user_auth = None

  yield # The application runs here

  # --- Shutdown Logic ---
  logger.info("Application shutting down.")
  if hasattr(app.state, 'config_manager'):
    app.state.config_manager.save_config()


app = FastAPI(
  title="Mastercam GitLab Interface",
  description="A comprehensive file management system for Mastercam and GitLab.",
  version="2.0.0",
  lifespan=lifespan,
  openapi_tags=[
    {"name": "Authentication", "description": "User login and token management."},
    {"name": "File Management", "description": "Core file operations."},
    {"name": "Administration", "description": "Privileged, admin-only operations."},
    {"name": "Configuration", "description": "Getting and setting application configuration."},
  ]
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, methods=["*"], allow_headers=["*"])

app.include_router(auth.router)
app.include_router(files.router)
app.include_router(admin.router)
app.include_router(config.router)

@app.get("/")
async def root(request: Request):
  if request.app.state.git_repo:
    return {"message": "Welcome! The API is configured and running."}
  return {"message": "Welcome! The API is running in limited mode. Please configure GitLab credentials."}
```

---

### Stage 4.2: Final Cleanup

With all the logic successfully moved to our new structure, the original `mastercam_main.py` file is now obsolete.

#### Your Action Item

You can now safely **delete the `mastercam_main.py` file** from your project.

---

## Backend Refactoring Complete\! ✅

Congratulations\! You have successfully refactored a monolithic Python script into a modern, scalable, and professional service-oriented backend. We have applied key principles of software architecture to create a system that is secure, maintainable, and easy to understand.

We're now ready to apply these same principles to the frontend.

Let me know when you're ready to begin **Phase 4: Structuring the Frontend Application**.
