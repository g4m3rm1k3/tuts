# PDM Tutorial - Stage 1: First Backend - FastAPI Fundamentals

**Prerequisites**: Completed Stage 0. You should have the folder structure with `backend/app/__init__.py` and placeholders. Test: `cd pdm-tutorial/backend && python -c "import app; print('Package OK')"` → "Package OK".
**Time**: 3-4 hours
**What you'll build**: A minimal FastAPI server with one endpoint. Deep dive into ASGI/WSGI, HTTP, and core concepts. _Incremental_: One import/line at a time—build, test, understand.

---

### Deep Dive: ASGI vs WSGI (CS: Async Evolution, SE: Abstraction Layers)

Before code, grasp the foundation. **CS Topic**: Web servers evolved from sync (WSGI, 2003) to async (ASGI, 2016) due to I/O bottlenecks (e.g., DB calls block threads). WSGI: Single-threaded, one request at a time (like a busy restaurant with one chef). ASGI: Event-loop based (async/await in Python 3.5+), handles 1000s concurrently (chef delegates to sous-chefs).

**App Topic**: FastAPI uses ASGI (Starlette) for speed—perfect for our PDM (real-time sync later). **SE Principle**: Abstraction (ASGI hides sync details, like SOLID's dependency inversion). **Python Specific**: `async def` yields control (coroutines, CS: cooperative multitasking).

Run your original learn file if you have it, or skip—focus on building.

---

### 1.1: Install FastAPI & Uvicorn (One Command)

**Step 1: Create requirements.txt**

```bash
cd backend
touch requirements.txt
```

Paste minimal:

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
```

- **Explanation**: FastAPI: ASGI framework (app: declarative APIs). Uvicorn: ASGI server (CS: event loop runner). Pin versions (SE: reproducibility).
- **Test**: `pip install -r requirements.txt` → No errors.
- **Gotcha**: [standard] includes websockets (future Stage 8).

**Step 2: Verify Install**

```bash
python -c "import fastapi, uvicorn; print('FastAPI:', fastapi.__version__); print('Uvicorn:', uvicorn.__version__)"
```

- **Output**: Versions.
- **CS Revisit**: Import system (sys.path, packages from Stage 0).

---

### 1.2: Create Basic App (One Import/Line)

**Step 1: Edit main.py (Skeleton)**

```bash
touch app/main.py
```

Paste:

```python
from fastapi import FastAPI  # NEW: Core import

app = FastAPI()  # NEW: Create ASGI app instance

@app.get("/")  # NEW: Decorator for route
def read_root():  # NEW: Handler function
    return {"Hello": "World"}  # NEW: Response dict (JSON auto)
```

- **Explanation**: `FastAPI()` = app object (CS: callable, ASGI spec—dict with 'type', 'asgi_version'). `@app.get("/")` = route (design: declarative, Python decorator pattern). Handler returns dict → auto JSON (app: RESTful).
- **SE Principle**: Single responsibility—main.py only routes (inversion: deps later).
- **Test**: `uvicorn app.main:app --reload` → "Uvicorn running on http://127.0.0.1:8000". Visit / → {"Hello": "World"}.
- **Gotcha**: `app.main:app` = module:app_var (ASGI entry).

**Step 2: Add Title/Version (Metadata)**
In FastAPI():

```python
app = FastAPI(title="PDM API", version="1.0.0")  # NEW: Metadata
```

- **Explanation**: Auto-docs (OpenAPI, CS: self-describing APIs). Revisit Stage 0 README for versioning (SE: semantic).
- **Test**: Restart, /docs → Swagger UI with title.

**Step 3: Add Startup Event (One Event)**
Add at end:

```python
@app.on_event("startup")  # NEW: Lifecycle hook
def startup_event():  # NEW: Sync function
    print("PDM API started")  # NEW: Log
```

- **Explanation**: Runs on server start (CS: lifecycle, like init in OOP). Print for debug (logging later).
- **SE Revisit**: Hooks for setup (e.g., DB connect, Stage 5 users).
- **Test**: Restart—console: "PDM API started".

**Full main.py**: Minimal server running.

---

### 1.3: Add First Real Endpoint (Files List)

**Step 1: Import Pathlib (Data)**
Add:

```python
from pathlib import Path  # NEW: File paths
```

- **Explanation**: Pathlib = object-oriented paths (CS: abstraction over strings, cross-platform). Revisit Stage 0 structure.
- **Test**: No change—imports OK.

**Step 2: Add /files Endpoint (Stub)**
Add:

```python
from typing import List  # NEW: Type hints

@app.get("/api/files")  # NEW: Route
def get_files() -> List[dict]:  # NEW: Return type
    return []  # NEW: Empty list
```

- **Explanation**: `/api/` prefix (design: namespacing). List[dict] = JSON array (Python: typing for IDEs/SE: contracts).
- **Test**: Visit /api/files → [].

**Step 3: Read Repo Dir (One Glob)**
Add inside get_files:

```python
repo_path = Path("repo")  # NEW: Local path
files = [f.name for f in repo_path.glob("*.mcam")]  # NEW: Glob files
return [{"name": f} for f in files]  # NEW: Dict list
```

- **Explanation**: Glob = pattern match (CS: regex-like, efficient FS traversal). Assumes `repo/*.mcam` from Stage 0.
- **App Revisit**: Ties to structure (SE: loose coupling—path configurable later).
- **Test**: Create dummy: `mkdir repo; touch repo/test.mcam`. /api/files → [{"name": "test.mcam"}].

**Step 4: Add Error Handling (Try/Except)**
Wrap glob:

```python
try:
    repo_path = Path("repo")
    files = [f.name for f in repo_path.glob("*.mcam")]
    return [{"name": f} for f in files]
except Exception as e:  # NEW
    return {"error": str(e)}  # NEW: Error response
```

- **Explanation**: FS errors (e.g., no repo) (CS: exception hierarchy, Python's try/except). JSON error (app: graceful fail).
- **SE Principle**: Fail fast but safe (defensive programming).
- **Test**: `rm -rf repo` → /api/files → {"error": "..."}.

**Full get_files**: Lists .mcam files.

---

### 1.4: Add Logging & Startup (Revisit Events)

**Step 1: Import Logging**
Add:

```python
import logging  # NEW
```

- **Explanation**: Python stdlib logging (CS: levels—DEBUG/INFO/ERROR). Revisit Stage 0 README for debug.
- **Test**: No change.

**Step 2: Configure Logger in Startup**
In startup_event:

```python
logging.basicConfig(level=logging.INFO)  # NEW: Setup
logger = logging.getLogger("pdm")  # NEW: Namespaced logger
logger.info("PDM API started")  # NEW: Log instead of print
```

- **Explanation**: basicConfig = simple setup (SE: configurable later). Logger.info = structured (CS: log levels for filters).
- **Test**: Restart—console: "INFO:pdm:PDM API started".

**Step 3: Log in Endpoint**
In get_files:

```python
logger.info(f"Files requested by {request.state.user}")  # NEW: Later, stub
logger.info(f"Returning {len(files)} files")  # NEW
```

- **Explanation**: Logs ops (SE: observability, revisit Stage 6 audit).
- **Test**: Call /api/files—log shows count.

**Full main.py**: Logged, robust server.

---

### 1.5: Serve Static Files (Frontend Tie-In)

**Step 1: Import StaticFiles**
Add:

```python
from fastapi.staticfiles import StaticFiles  # NEW
```

- **Explanation**: Mounts dir for serving (app: separates API/static, MVC).
- **Test**: No change.

**Step 2: Mount Static**
After app = FastAPI():

```python
app.mount("/static", StaticFiles(directory="static"), name="static")  # NEW
```

- **Explanation**: /static/css/main.css serves from backend/static (CS: URL mapping).
- **Test**: Create `backend/static/test.txt` with "Hello". /static/test.txt → "Hello".

**Step 3: Root Redirect to Frontend**
Add:

```python
from fastapi.responses import RedirectResponse  # NEW

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")  # NEW: Serve HTML
```

- **Import**: Add `from fastapi.responses import RedirectResponse`.
- **Explanation**: / → frontend (app: SPA entry). Redirect for SEO (SE: clean URLs).
- **Test**: / → /static/index.html (loads placeholder).

**Full main.py**: Serves API + static.

---

### Stage 1 Complete

**Test Full App**:

```bash
uvicorn app.main:app --reload
```

- Visit /docs → Swagger with /api/files.
- /api/files → Files list (if repo has .mcam).
- / → index.html.
- Logs on calls.

**Verification**:

- [ ] Server starts, logs "PDM API started".
- [ ] /api/files returns JSON (empty or files).
- [ ] /static serves files.
- [ ] /docs shows endpoints.

**What You Learned (Depth)**:

- **CS**: Async (ASGI event loop vs WSGI blocking), HTTP methods (GET), glob (pattern matching).
- **App**: REST APIs (endpoints, JSON), static serving (SPA).
- **Python**: Decorators (@app.get), pathlib (OO paths), logging (levels).
- **SE**: Dependency inversion (routes as handlers), error handling (try/except), 12-factor (ports/env).

**Next: Stage 2** (Frontend CSS/JS, incremental ITCSS). Ready?
