Absolutely. We can expand **Stage 1** to include **more levels of detail**: CS concepts, Python/FastAPI mechanics, async behavior, MVC rationale, testing reasoning, and common pitfalls. I’ll rewrite Stage 1 with deeper explanations per line/block.

---

## Stage 1: FastAPI Basics — Expanded with Deep Explanations

**Prerequisites**: Stage 0 complete
**Time**: 2–3 hours (including testing & reading explanations)
**Goal**: Serve a simple endpoint, static HTML, and test the basics of FastAPI.

---

### Step 1: Install Dependencies

```bash
pip install fastapi uvicorn python-dotenv
```

**Deep Explanation**:

- `fastapi`: Modern Python web framework, async-first, uses **type hints** for automatic validation, serialization, and OpenAPI docs.
- `uvicorn`: Lightweight **ASGI server**, handles async requests efficiently. Runs FastAPI apps.
- `python-dotenv`: Loads `.env` variables into `os.environ`. Good for **separating config from code** (12-factor principle).
- **CS Concept**: Dependency management & virtual environments prevent "DLL hell" type conflicts.

**Test**:

```bash
python -c "import fastapi, uvicorn, dotenv; print('Imports OK')"
```

**Gotcha**: If you see `ModuleNotFoundError`, ensure you installed inside a virtual environment (`python -m venv venv` → `source venv/bin/activate` or `venv\Scripts\activate`).

---

### Step 2: Create the Main App File

```bash
touch backend/app/main.py
```

Paste:

```python
from fastapi import FastAPI

# Initialize FastAPI app object
app = FastAPI(title="PDM Tutorial App")

# Route decorator binds URL path '/' to this function
@app.get("/")
async def read_root():
    """
    Responds with a simple JSON message.
    'async def' allows non-blocking operations.
    """
    return {"message": "Hello, PDM!"}
```

**Deep Explanation**:

1. `FastAPI()`

   - Creates an **ASGI application object**.
   - Stores **routes, middleware, exception handlers**.
   - Singleton per module: Only one app instance should handle all routes.

2. `@app.get("/")`

   - **Decorator** pattern (CS concept): wraps function to register route metadata.
   - `"GET"` method indicates HTTP verb.

3. `async def read_root()`

   - **Asynchronous function**: can yield control while waiting for I/O.
   - Enables handling multiple requests **concurrently without threads**.
   - If you use `def` instead of `async def`, FastAPI will run it in a threadpool.

4. `return {"message": ...}`

   - FastAPI automatically **serializes Python dict to JSON**.
   - Response headers set: `Content-Type: application/json`.

**Test**:

```bash
uvicorn app.main:app --reload
```

Open: `http://127.0.0.1:8000/` → Should see `{"message": "Hello, PDM!"}`

**Gotcha**:

- Wrong module path: `ModuleNotFoundError` → must run from `backend/` or adjust PYTHONPATH.
- Forgetting `async` won't break small apps but may **block server under load**.

---

### Step 3: Mount Static Files

Add this to `main.py`:

```python
from fastapi.staticfiles import StaticFiles

# Mount static folder
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
```

**Deep Explanation**:

- `StaticFiles` is a **FastAPI utility** to serve files.
- `app.mount(path, ...)` registers a **sub-application** for a specific URL prefix.
- `directory="backend/static"` → File-system path relative to **current working directory**.
- **CS Concept**: Separation of concerns (MVC):

  - `API` = dynamic endpoints
  - `Static` = frontend files, CSS, JS, images

- **App UX**: Users can load `index.html` without hitting backend routes.

**Test**:

Open: `http://127.0.0.1:8000/static/index.html` → HTML should render

**Gotcha**:

- Directory path must exist. Typos or relative paths from the wrong folder cause `RuntimeError: Directory does not exist`.
- Always lowercase filenames (Linux/macOS are case-sensitive).

---

### Step 4: Basic Endpoint Testing (TDD Mindset)

Create: `backend/tests/test_main.py`

```python
from fastapi.testclient import TestClient
from app.main import app

# Simulate HTTP client
client = TestClient(app)

def test_read_root():
    """
    Verify root endpoint returns expected JSON
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, PDM!"}
```

**Deep Explanation**:

- `TestClient(app)` uses **requests under the hood** to simulate HTTP calls without running Uvicorn.
- **Red-Green-Refactor**: You write the test first to verify functionality.
- `assert` statements: Python built-in; raise exception if check fails.
- **CS Concept**: Testing = deterministic verification; prevents regressions.

**Test**:

```bash
pytest backend/tests
```

→ Should pass with green output

**Gotcha**:

- Import errors: missing `__init__.py` → cannot `from app.main import app`.
- `TestClient` runs sync, so async functions are handled automatically.

---

### Step 5: Verify and Summarize

**Run**:

1. `uvicorn app.main:app --reload` → `/` returns JSON
2. `/static/index.html` loads
3. `pytest backend/tests` → green

**Learned Deeply**:

| Area    | Concept                                                                          |
| ------- | -------------------------------------------------------------------------------- |
| CS      | Async I/O, decorator pattern, singleton app object, tree structure (file layout) |
| Python  | Async functions, dict-to-JSON serialization, type hints (for later)              |
| FastAPI | Routing, static mounting, TestClient, request lifecycle                          |
| App Dev | MVC separation, endpoint-first mindset, serving static assets                    |
| SE      | TDD approach, config/env separation, incremental verification                    |

---

✅ **Stage 1 Complete** — Fully functional FastAPI app + static HTML + tests.
You now have a **solid foundation** for Stage 2: introducing **schemas, services, and more complex endpoints**.

---

If you want, I can **rewrite Stage 2 in the same level of deep, line-by-line explanation**, keeping each step 5–15 lines, covering:

- Pydantic schemas
- Services for business logic
- Connecting endpoints to service layer
- Incremental testing

Do you want me to proceed with Stage 2 next?
