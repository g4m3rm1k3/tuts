# Deep Dive: Your `app/main.py` - The Application Core

## Overview: What This File Does

This is the **heart** of your application. If `run.py` is the ignition switch, `main.py` is the engine. This file:

1. **Creates the FastAPI application**
2. **Initializes all services** (Git, authentication, locking)
3. **Manages application lifecycle** (startup/shutdown)
4. **Registers all API routes**
5. **Serves static files** (your frontend)

Let's go through it piece by piece.

---

## Part 1: The Imports - Understanding Your Dependencies

```python
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import logging
from pathlib import Path
```

### Breaking Down Each Import

**`from fastapi import FastAPI, Request`**

- **`FastAPI`**: The main application class - you create ONE instance of this
- **`Request`**: Represents an HTTP request (you'll use this in route handlers to access headers, body, etc.)

📚 **Learn more:** [FastAPI Main Concepts](https://fastapi.tiangolo.com/tutorial/)

---

**`from fastapi.staticfiles import StaticFiles`**

This is a special ASGI application that serves static files (HTML, CSS, JS, images).

**Why you need it:** Your frontend (HTML/CSS/JS) needs to be served to the browser. FastAPI doesn't serve files by default - it's an API framework.

**How it works:**

- You "mount" it to a path like `/static`
- When browser requests `/static/css/styles.css`
- StaticFiles reads from your `static/` folder and returns the file

**Alternative approach:** Use Nginx to serve static files in production (faster), but this works great for development.

📚 **Learn more:** [FastAPI Static Files](https://fastapi.tiangolo.com/tutorial/static-files/)

---

**`from fastapi.middleware.cors import CORSMiddleware`**

**CORS = Cross-Origin Resource Sharing**

**The problem it solves:** Browsers have a security policy - a page from `http://localhost:3000` cannot call an API at `http://localhost:8000` by default. This is called the "Same-Origin Policy."

**When you need CORS:**

- Frontend and backend on different ports (development)
- Frontend and backend on different domains (production)
- Any JavaScript `fetch()` call to a different origin

**What the middleware does:** Adds special HTTP headers telling the browser "yes, I allow requests from other origins."

**Security note:** Using `allow_origins=["*"]` means "allow from anywhere" - fine for development, dangerous for production. In production, specify exact origins.

📚 **Learn more:**

- [MDN CORS Explanation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)

---

**`from fastapi.responses import FileResponse`**

A response type that streams a file to the client. You use this to serve your `index.html`.

**Why not just read the file and return it?**

```python
# BAD - loads entire file into memory
return open('index.html').read()

# GOOD - streams file efficiently
return FileResponse('index.html')
```

`FileResponse` handles:

- Setting correct `Content-Type` header
- Streaming (sending chunks, not loading entire file)
- Browser caching headers
- File not found errors

---

**`from contextlib import asynccontextmanager`**

This is a Python standard library tool for creating **async context managers**.

**What's a context manager?** The `with` statement:

```python
with open('file.txt') as f:
    # Do something
    pass
# File is automatically closed, even if an error occurred
```

**Async context managers** are the same but for async code:

```python
async with some_resource() as r:
    # Do async work
    pass
# Resource cleaned up
```

**Why you need it:** FastAPI's `lifespan` parameter expects an async context manager. We'll build one.

📚 **Learn more:** [Python Context Managers](https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager)

---

**`import logging`**

Python's standard logging library. Professional applications use logging instead of `print()` because:

1. **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
2. **Filtering**: Show only WARNING+ in production, DEBUG+ in development
3. **Formatting**: Timestamps, module names, stack traces
4. **Destinations**: Console, files, remote servers, all simultaneously

```python
print("Something happened")  # Bad - no context, no filtering
logger.info("User logged in")  # Good - timestamped, filterable, contextual
```

📚 **Learn more:** [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html)

---

**`from pathlib import Path`**

Modern Python uses `Path` objects instead of string manipulation for file paths.

**Old way (string manipulation):**

```python
import os
path = os.path.join("backend", "static", "index.html")  # "backend/static/index.html"
```

**New way (Path objects):**

```python
from pathlib import Path
path = Path("backend") / "static" / "index.html"  # More readable!
```

**Benefits:**

- Cross-platform (Windows vs Linux path separators)
- Readable operations: `path.exists()`, `path.read_text()`, `path.mkdir()`
- Type-safe (can't accidentally concat strings wrong)

📚 **Learn more:** [Real Python - Path](https://realpython.com/python-pathlib/)

---

### Your Service Imports

```python
from app.core.config import ConfigManager
from app.services.lock_service import MetadataManager, ImprovedFileLockManager
from app.services.git_service import GitRepository, setup_git_lfs_path
from app.core.security import UserAuth
from app.api.routers import auth, files, admin, config, websocket, dashboard
```

These are YOUR modules - the business logic of your app. We'll explain each when we see them used.

**Important architectural note:** You're importing the classes/functions, not creating instances yet. Instances are created in the `lifespan` function.

---

### Logging Setup

```python
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
```

**`logging.basicConfig()`** - Sets up the root logger (only do this once, at the application entry point)

**Parameters:**

- `level=logging.INFO` - Show INFO and above (INFO, WARNING, ERROR, CRITICAL), hide DEBUG
- `format='...'` - How log messages look:
  - `%(asctime)s` - Timestamp
  - `%(levelname)s` - INFO, ERROR, etc.
  - `%(message)s` - Your actual message

**`logger = logging.getLogger(__name__)`** - Creates a logger for this module

**Why `__name__`?** In `app/main.py`, `__name__` is `"app.main"`. Your logs will show:

```
2024-10-11 10:30:00 - INFO - app.main - Application starting up...
```

This tells you WHICH module logged the message - crucial for debugging large apps.

---

## Part 2: The Resource Path Helper

```python
def resource_path(relative_path):
    base_path = Path(__file__).resolve().parents[1]
    return base_path / relative_path
```

**What this does:** Figures out where files are relative to this module.

**Let's trace through it:**

**`Path(__file__)`** - `__file__` is the path to the current file (`app/main.py`)

**`.resolve()`** - Converts to absolute path

- If you're in `/home/user/mastercam-pdm/backend/app/main.py`
- `.resolve()` gives you that full path

**`.parents[1]`** - Goes UP two directory levels

**Path anatomy:**

```
/home/user/mastercam-pdm/backend/app/main.py
                          ^^^^^^^ <- parents[0] (app/)
                  ^^^^^^^^^^^^^^^ <- parents[1] (backend/)
```

So `parents[1]` gives you the `backend/` directory.

**Why do this?** Your app might be run from different directories:

```bash
cd backend && python run.py           # Working dir: backend/
cd mastercam-pdm && python backend/run.py  # Working dir: mastercam-pdm/
```

Using `__file__` makes paths work regardless of where you run from.

**Example usage:**

```python
resource_path("static")  # Returns: /full/path/to/backend/static
resource_path("static/index.html")  # Returns: /full/path/to/backend/static/index.html
```

---

## Part 3: The Lifespan Manager (THE KEY PATTERN)

This is one of the most important patterns in your entire app.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup. This is where we initialize our services
    and make them available to the rest of the application via app.state.
    """
    logger.info("Application starting up...")

    # ... initialization code ...

    yield  # The application runs here

    # ... shutdown code ...
```

### Understanding Context Managers

**The pattern:**

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. STARTUP - runs once when server starts
    print("Starting up!")

    yield  # 2. SERVER RUNS - application is alive here

    # 3. SHUTDOWN - runs once when server stops
    print("Shutting down!")
```

**Why this pattern?** Many resources need **cleanup**:

- Database connections must be closed
- Files must be saved
- Background tasks must be stopped

Without cleanup, you get resource leaks.

**The beauty of context managers:** Shutdown code ALWAYS runs, even if there's an error.

📚 **Learn more:** [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)

---

### The Startup Sequence

Let's trace through what happens when your app starts:

```python
# 1. Setup Git LFS path environment
setup_git_lfs_path()
```

**What this does:** Configures Git LFS (Large File Storage) in the environment.

**Why?** Your Mastercam files are BIG (megabytes). Git doesn't handle large binary files well. Git LFS stores large files separately and keeps pointers in Git.

**The function probably does:**

```python
# Sets environment variables or Git config so LFS works
os.environ['GIT_LFS_SKIP_SMUDGE'] = '1'  # Don't download LFS files on clone
```

**Your spec mentions "LFS On-Demand"** - this is the setup for that feature.

📚 **Learn more:** [Git LFS Documentation](https://git-lfs.com/)

---

```python
# 2. Initialize the Config Manager and attach it to the app state
config_manager = ConfigManager(base_dir=resource_path(""))
app.state.config_manager = config_manager
```

**`ConfigManager(base_dir=...)`** - Creates your config system (the class you showed me earlier)

**`app.state.config_manager = config_manager`** - This is KEY!

**Understanding `app.state`:**

FastAPI's `app` object has a special `.state` attribute where you can store ANYTHING. It's a namespace for sharing data across your entire application.

**Why use `app.state`?**

**The problem:** Your route handlers need access to services (Git, auth, etc.), but routes are just functions. How do they get access?

**Bad solution:** Global variables

```python
git_repo = GitRepository()  # Global - gross!

@app.get("/files")
def list_files():
    files = git_repo.list_files()  # Using global
```

**Good solution:** Dependency injection via `app.state`

```python
# Store in app.state during startup
app.state.git_repo = GitRepository()

# Access in routes via dependency injection
from fastapi import Depends

def get_git_repo(request: Request):
    return request.app.state.git_repo

@app.get("/files")
def list_files(git_repo: GitRepository = Depends(get_git_repo)):
    files = git_repo.list_files()  # Clean!
```

**Benefits:**

- No global variables
- Easy to test (inject mock services)
- Clear dependencies
- Type-safe

📚 **Learn more:** [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)

---

```python
# 3. Read the config to see if we can initialize the other services
cfg = config_manager.config
gitlab_cfg = cfg.gitlab

if all(gitlab_cfg.get(k) for k in ['base_url', 'token', 'project_id']):
```

**What's happening:** Checking if GitLab is configured.

**`all(gitlab_cfg.get(k) for k in [...])`** - Let's break this down:

```python
# Equivalent to:
has_base_url = 'base_url' in gitlab_cfg and gitlab_cfg['base_url'] is not None
has_token = 'token' in gitlab_cfg and gitlab_cfg['token'] is not None
has_project_id = 'project_id' in gitlab_cfg and gitlab_cfg['project_id'] is not None

if has_base_url and has_token and has_project_id:
    # All required fields present
```

**Why this check?** First-time users haven't configured GitLab yet. The app should still start and show them a config UI.

**This is graceful degradation** - app works in "limited mode" until fully configured.

---

### Service Initialization

```python
repo_path_str = gitlab_cfg.get("repo_path")
if not repo_path_str:
    # Fallback for first-time setup
    repo_path = Path.home() / 'MastercamGitRepo' / gitlab_cfg['project_id']
    config_manager.config.local["repo_path"] = str(repo_path)
else:
    repo_path = Path(repo_path_str)
```

**Understanding the logic:**

**First run:** No `repo_path` in config

- Default to: `~/MastercamGitRepo/{project_id}`
- Save this default for next time

**Subsequent runs:** Use saved path

**`Path.home()`** - Cross-platform home directory

- Linux/Mac: `/home/username`
- Windows: `C:\Users\username`

---

```python
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
```

**Service dependency chain:**

```
ImprovedFileLockManager (lowest level - just file locking)
    ↓
MetadataManager (tracks file metadata)
    ↓
GitRepository (Git operations, uses lock manager)
    ↓
UserAuth (authentication, uses git for user validation)
```

**Each service depends on the ones above it.** This is **layered architecture**.

**Note the pattern:** Services take dependencies as constructor parameters. This is **dependency injection** - makes testing easier.

---

```python
# Store the initialized services on the app state object
app.state.metadata_manager = metadata_manager
app.state.git_repo = git_repo
app.state.user_auth = user_auth
```

**Now all your route handlers can access these services via `app.state`!**

---

### Error Handling

```python
except Exception as e:
    logger.error(f"Full initialization failed: {e}", exc_info=True)
    # Ensure services are set to None so the app can start in a limited state
    app.state.metadata_manager = None
    app.state.git_repo = None
    app.state.user_auth = None
```

**`exc_info=True`** - Includes full stack trace in the log. Critical for debugging!

**Setting services to `None`** - Graceful degradation again. App starts, but routes that need these services will show errors or redirect to config page.

---

### The Yield Statement

```python
yield  # The application runs here
```

**Everything before `yield`:** Startup
**The `yield` itself:** Server is running, handling requests
**Everything after `yield`:** Shutdown

---

### Shutdown Logic

```python
# --- Shutdown Logic ---
logger.info("Application shutting down.")
if hasattr(app.state, 'config_manager'):
    app.state.config_manager.save_config()
```

**When does this run?** When you press Ctrl+C or the server stops.

**`hasattr(app.state, 'config_manager')`** - Checks if the attribute exists (in case startup failed)

**`save_config()`** - Persists any config changes to disk before shutdown.

**Why is this important?** If user changes settings and kills the server, you don't want to lose those changes!

---

## Part 4: Creating the FastAPI App

```python
app = FastAPI(title="Mastercam GitLab Interface",
              version="2.0.0", lifespan=lifespan)
```

**This line creates the application!**

**Parameters:**

- `title` - Shows in API docs at `/docs`
- `version` - Also in API docs, useful for tracking deployments
- `lifespan=lifespan` - **KEY!** Connects our startup/shutdown logic

---

## Part 5: Mounting Static Files

```python
app.mount("/static", StaticFiles(directory=resource_path("static")), name="static")
```

**`app.mount()`** - Attaches another ASGI application at a path

**What this does:**

- Browser requests `/static/css/styles.css`
- FastAPI routes to the StaticFiles app
- StaticFiles reads `backend/static/css/styles.css`
- Returns the file content

**The `name="static"` parameter** - Used for URL generation (reverse routing). Not critical here.

📚 **Learn more:** [FastAPI Sub Applications](https://fastapi.tiangolo.com/advanced/sub-applications/)

---

## Part 6: CORS Middleware

```python
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
```

**What is middleware?** Code that runs on EVERY request, before your route handlers.

**Request flow with middleware:**

```
Browser → CORS Middleware → Your Route Handler → Response
          ↑                                        ↓
          Adds CORS headers ←←←←←←←←←←←←←←←←←←←←←←←←
```

**Parameters explained:**

**`allow_origins=["*"]`** - Accept requests from ANY origin

- ⚠️ **Security risk in production!**
- In production, use: `allow_origins=["https://your-frontend.com"]`

**`allow_credentials=True`** - Allow cookies and auth headers

- Needed for your JWT cookie authentication

**`allow_methods=["*"]`** - Allow GET, POST, PUT, DELETE, etc.

**`allow_headers=["*"]`** - Allow any HTTP headers

**Middleware order matters!** CORS must be added BEFORE routes are registered.

---

## Part 7: Registering Routers

```python
app.include_router(auth.router)
app.include_router(files.router)
app.include_router(admin.router)
app.include_router(config.router)
app.include_router(websocket.router)
app.include_router(dashboard.router)
```

**What are routers?** Modules that group related endpoints.

**Your app architecture:**

```
app/api/routers/
├── auth.py       - Login, logout, token management
├── files.py      - List, checkout, checkin files
├── admin.router  - Admin operations (force unlock, etc.)
├── config.py     - GitLab configuration endpoints
├── websocket.py  - Real-time updates
└── dashboard.py  - Dashboard statistics
```

**Each router file has:**

```python
from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/login")
def login():
    ...
```

**`include_router()` merges them into the main app.**

**Why separate routers?**

- **Organization** - Related endpoints together
- **Team work** - Different developers can work on different routers
- **Testing** - Can test each router independently
- **Reusability** - Can reuse routers in different apps

📚 **Learn more:** [FastAPI Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

---

## Part 8: The Root Endpoint

```python
@app.get("/")
async def root():
    return FileResponse(resource_path("static/index.html"))
```

**When does this run?** When user visits `http://localhost:8000/` (the root URL)

**What it does:** Serves your main HTML file (the frontend entry point)

**`async def`** - This is an async function, can use `await` if needed

**Flow:**

```
User types localhost:8000 in browser
    ↓
Browser sends GET /
    ↓
FastAPI routes to root()
    ↓
Returns static/index.html
    ↓
Browser loads HTML
    ↓
HTML loads CSS and JS from /static/...
    ↓
JS fetches data from /api/...
```

---

## Your Complete Commented `main.py`

Here's your file with comprehensive comments:

```python
"""
Main application module - The FastAPI application core.

This file:
1. Creates the FastAPI application instance
2. Initializes all services (Git, auth, locking) during startup
3. Registers all API routers
4. Serves the frontend static files
5. Handles graceful shutdown

Architecture:
- Services are initialized once at startup and stored in app.state
- Route handlers access services via dependency injection
- Lifespan context manager ensures proper startup/shutdown
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import logging
from pathlib import Path

# Import all our components
from app.core.config import ConfigManager
from app.services.lock_service import MetadataManager, ImprovedFileLockManager
from app.services.git_service import GitRepository, setup_git_lfs_path
from app.core.security import UserAuth
from app.api.routers import auth, files, admin, config, websocket, dashboard

# Configure logging for this module
# Note: basicConfig should really only be in run.py, but keeping for backwards compat
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def resource_path(relative_path):
    """
    Calculate absolute path to a resource relative to this file.

    This ensures paths work regardless of where the app is run from.

    Args:
        relative_path: Path relative to the backend/ directory

    Returns:
        Path object pointing to the resource

    Example:
        resource_path("static") -> /full/path/to/backend/static
        resource_path("static/index.html") -> /full/path/to/backend/static/index.html
    """
    # __file__ is this file (app/main.py)
    # .resolve() makes it an absolute path
    # .parents[1] goes up to backend/ directory
    base_path = Path(__file__).resolve().parents[1]
    return base_path / relative_path


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager - handles startup and shutdown.

    This is an async context manager. Code before 'yield' runs at startup,
    code after 'yield' runs at shutdown.

    Startup sequence:
    1. Configure Git LFS
    2. Load configuration from disk
    3. If GitLab is configured, initialize all services
    4. Store services in app.state for access by routes

    Shutdown sequence:
    1. Save any config changes to disk

    Note: If initialization fails, app runs in "limited mode" with services=None.
    Routes must check if services exist before using them.
    """
    logger.info("Application starting up...")

    # === STARTUP ===

    # 1. Setup Git LFS path environment
    # This configures Git to work with Large File Storage
    # Your spec requires "LFS On-Demand" - only download files when needed
    setup_git_lfs_path()

    # 2. Initialize the Config Manager and attach it to the app state
    # ConfigManager handles loading/saving config.json and encryption
    config_manager = ConfigManager(base_dir=resource_path(""))
    app.state.config_manager = config_manager

    # app.state is a special FastAPI namespace for storing shared data
    # Anything stored here is accessible in all route handlers via request.app.state

    # 3. Check if GitLab is configured
    # If user hasn't configured GitLab yet, we run in "limited mode"
    cfg = config_manager.config
    gitlab_cfg = cfg.gitlab

    # Check if all required GitLab settings exist and are not empty
    if all(gitlab_cfg.get(k) for k in ['base_url', 'token', 'project_id']):
        try:
            # === FULL INITIALIZATION MODE ===

            # Determine where the Git repository should be stored locally
            repo_path_str = gitlab_cfg.get("repo_path")
            if not repo_path_str:
                # First-time setup: use default location in user's home directory
                # e.g., ~/MastercamGitRepo/12345 (where 12345 is the project ID)
                repo_path = Path.home() / 'MastercamGitRepo' / gitlab_cfg['project_id']

                # Save this default for next time
                config_manager.config.local["repo_path"] = str(repo_path)
            else:
                # Use the saved path from config
                repo_path = Path(repo_path_str)

            logger.info(f"Initializing repository services at {repo_path}")

            # Initialize services in dependency order (bottom-up)

            # 1. File lock manager - prevents concurrent Git operations
            #    Uses a lock file in .git/repo.lock
            repo_lock_manager = ImprovedFileLockManager(
                repo_path / ".git" / "repo.lock"
            )

            # 2. Metadata manager - tracks file descriptions, revisions, etc.
            #    Reads/writes .meta.json files alongside each tracked file
            metadata_manager = MetadataManager(repo_path=repo_path)

            # 3. Git repository - handles all Git operations (clone, commit, push, etc.)
            #    Depends on: lock manager (to prevent concurrent ops)
            git_repo = GitRepository(
                repo_path=repo_path,
                remote_url=gitlab_cfg['base_url'],
                token=gitlab_cfg['token'],
                config_manager=config_manager,
                lock_manager=repo_lock_manager
            )

            # 4. User authentication - validates users and manages sessions
            #    Depends on: git_repo (to validate against GitLab)
            user_auth = UserAuth(git_repo=git_repo)

            # Store all initialized services on app.state
            # Route handlers will access these via dependency injection
            app.state.metadata_manager = metadata_manager
            app.state.git_repo = git_repo
            app.state.user_auth = user_auth

            logger.info("Application fully initialized.")

        except Exception as e:
            # If initialization fails (e.g., can't reach GitLab, bad token, etc.)
            # log the error and run in limited mode
            logger.error(f"Full initialization failed: {e}", exc_info=True)

            # Set services to None so routes know to show config page or error
            app.state.metadata_manager = None
            app.state.git_repo = None
            app.state.user_auth = None
    else:
        # === LIMITED MODE ===
        # GitLab not configured yet - user needs to visit config page
        logger.warning("Running in limited mode - GitLab is not configured.")
        app.state.metadata_manager = None
        app.state.git_repo = None
        app.state.user_auth = None

    yield  # === APPLICATION RUNS HERE ===

    # Everything after this point is SHUTDOWN logic

    # === SHUTDOWN ===
    logger.info("Application shutting down.")

    # Save any config changes that happened during runtime
    # hasattr check protects against startup failures
    if hasattr(app.state, 'config_manager'):
        app.state.config_manager.save_config()
        logger.info("Configuration saved.")


# === CREATE THE FASTAPI APPLICATION ===

app = FastAPI(
    title="Mastercam GitLab Interface",  # Shows in /docs
    version="2.0.0",                      # Shows in /docs
    lifespan=lifespan                     # Connect our startup/shutdown logic
)

# === MOUNT STATIC FILE SERVING ===

# Serve files from backend/static/ at the /static URL path
# Example: /static/css/styles.css -> backend/static/css/styles.css
app.mount(
    "/static",
    StaticFiles(directory=resource_path("static")),
    name="static"
)

# === ADD CORS MIDDLEWARE ===

# CORS (Cross-Origin Resource Sharing) allows frontend to call API
# even if they're on different ports/domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # ⚠️ Allow from any origin (dev only!)
    allow_credentials=True,     # Allow cookies/auth headers
    allow_methods=["*"],        # Allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],        # Allow any headers
)

# TODO: In production, replace allow_origins=["*"] with specific domain:
# allow_origins=["https://your-production-domain.com"]

# === REGISTER API ROUTERS ===

# Each router groups related endpoints
# Routes are prefixed and tagged for organization in /docs
app.include_router(auth.router)        # /api/auth/* - Login, logout
app.include_router(files.router)       # /api/files/* - File operations
app.include_router(admin.router)       # /api/admin/* - Admin actions
app.include_router(config.router)      # /api/config/* - Configuration
app.include_router(websocket.router)   # /ws - Real-time updates
app.include_router(dashboard.router)   # /api/dashboard/* - Statistics

# === ROOT ENDPOINT ===

@app.get("/")
async def root():
    """
    Serve the main frontend HTML page.

    When user visits http://localhost:8000/, they get the index.html file.
    The HTML then loads CSS/JS from /static/ and calls /api/ endpoints.
    """
    return FileResponse(resource_path("static/index.html"))
```

---

## Issues I Notice

### Issue 1: WebSocket/Dashboard Routers Commented Out

You have comments saying "ADD THIS LINE" but they're already there. Those comments should be removed - they're confusing.

### Issue 2: Polling Not Working

You mentioned polling doesn't work. The issue is likely in your `websocket.router` or how the frontend connects. We'll need to see those files.

### Issue 3: Admin/Dashboard Not Working

These likely depend on services being initialized. If GitLab isn't configured, these won't work.

### Issue 4: Duplicate logging.basicConfig

You have it in both `run.py` and `main.py`. Should only be in `run.py`. Remove from `main.py`.

---

## Understanding Questions

**Q1:** Why store services in `app.state` instead of global variables?

**Q2:** What would happen if you removed the `try-except` around service initialization?

**Q3:** Why does the app set services to `None` on initialization failure instead of crashing?

**Q4:** What's the purpose of the `yield` statement in the lifespan function?

---

## What's Next?

Now that you understand `main.py`, we need to see the files that it depends on. Based on what's not working:

**📁 Next File to Share: `backend/app/api/routers/websocket.py`**

This is likely where your polling/real-time update issue is. Share that file and I'll explain how WebSockets work and fix the polling.
