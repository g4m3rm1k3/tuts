Got it. I've processed both expansion documents. My goal is to synthesize everything into a single, definitive tutorial that you can follow from start to finish. This new version will integrate the deep dives, Windows-specific fixes, code organization advice, and continuity corrections directly into the original tutorial's flow.

Let's begin with the fully expanded and unified **Stage 1**.

---

# Stage 1: First Backend - FastAPI Hello World (Expanded & Unified)

## Introduction: The Goal of This Stage

You're about to write your first web server. Think of it as the "kitchen" in a restaurant—it takes orders (requests) and prepares food (responses). This is the core of your application's logic.

By the end of this stage, you will:

- Understand what a web server actually **is** and how it communicates.
- Create a FastAPI application from absolute scratch.
- Master the `async`/`await` syntax, the secret to FastAPI's speed.
- Serve data as JSON through API endpoints.
- Implement robust error handling and logging.
- Write your first automated tests to ensure your code works.

---

### **🧠 Foundational Concepts: A Deeper Look**

- **Time Investment:** 3-5 hours. Don't rush this foundation. A solid backend makes everything else easier.
- **Historical Insight**: Web servers have evolved dramatically. Early websites used the **Common Gateway Interface (CGI)** from 1993, which was slow because it started a new process for every single request. Modern Python uses **ASGI (Asynchronous Server Gateway Interface)**, which FastAPI is built on. ASGI is asynchronous from the ground up, allowing a single process to handle many network connections at once, giving it performance comparable to Node.js.
- **Key Concept - ASGI vs. WSGI**: You may hear about **WSGI (Web Server Gateway Interface)** from 2003. This is the older, **synchronous** standard used by popular frameworks like Flask and Django. ASGI is the modern, **asynchronous** standard. FastAPI's high performance comes directly from embracing ASGI.

---

## 1.1: What is a Web Server? The Restaurant Analogy

### The Client-Server Model

The entire web is built on the **client-server model**. It's a fundamental division of labor:

- **Clients** (like your browser) **request** information or actions.
- **Servers** (our FastAPI app) **listen** for those requests and provide **responses**.

This separation is powerful. It allows you to have a web app, a mobile app, and a desktop app all talking to the same server.

| Role         | Restaurant Analogy    | Web Application                                          |
| :----------- | :-------------------- | :------------------------------------------------------- |
| **Client**   | The Customer          | Your Web Browser                                         |
| **Server**   | The Kitchen           | Your FastAPI code                                        |
| **Protocol** | The Waiter's Notes    | **HTTP** (HyperText Transfer Protocol)                   |
| **Menu**     | The Restaurant's Menu | Available **Endpoints** (URLs like `/api/files`)         |
| **Order**    | Placing an Order      | The **Request** (`GET`, `POST`, `PUT`, `DELETE` methods) |
| **Food**     | The Prepared Dish     | The **Response** (e.g., JSON data)                       |

### HTTP: The Language of the Web

HTTP is just a structured text format. You can literally read it. A request has a start-line, headers, and an optional body.

#### An HTTP Request Breakdown

```http
GET /api/files HTTP/1.1
Host: localhost:8000
User-Agent: curl/8.4.0
Accept: application/json
```

- `GET /api/files HTTP/1.1`: The start-line, containing the **method** (`GET`), the **path** (`/api/files`), and the **protocol version** (`HTTP/1.1`).
- `Host: localhost:8000`: A required header telling the server which domain the request is for. This allows one server IP to host multiple websites.
- `User-Agent`: Identifies the client software (e.g., a browser or a tool like `curl`).
- `Accept`: Tells the server what kind of content the client can understand.

#### An HTTP Response Breakdown

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 47

{"files": ["file1.mcam", "file2.mcam"]}
```

- `HTTP/1.1 200 OK`: The status line, indicating success.
- `Content-Type: application/json`: Tells the client the body is JSON, so it knows how to parse it.
- `Content-Length: 47`: The size of the body in bytes.
- The blank line separates headers from the body.
- `{"files": ...}`: The actual data payload.

### Why FastAPI?

| Framework   | Pros                                                                                           | Cons                                                            | When to Use It                                                                        |
| :---------- | :--------------------------------------------------------------------------------------------- | :-------------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| **Django**  | "Batteries-included" (ORM, admin panel, auth), mature, huge community.                         | Opinionated, monolithic, slower, synchronous by default.        | Building traditional, full-featured web applications like a blog or e-commerce store. |
| **Flask**   | Minimal, flexible, unopinionated, easy to learn.                                               | Requires adding many extensions for features, synchronous.      | Building small microservices or when you want total control over your tools.          |
| **FastAPI** | **Extremely fast (async)**, **automatic interactive docs**, **data validation with Pydantic**. | Newer, smaller community, `async` can be complex for beginners. | Building high-performance APIs, which is exactly what our PDM app needs.              |

#### 🏋️ Practice Exercise: Manual HTTP Request

You can "speak" HTTP directly to your server. First, start your server with `uvicorn main:app --reload`.

- **On macOS/Linux:** Use `nc` (netcat). In a **new terminal**:

  ```bash
  nc localhost 8000
  # Once connected, type this exactly and press Enter twice:
  GET / HTTP/1.1
  Host: localhost:8000

  ```

- **On Windows:** Use `telnet`. You may need to enable it: go to **Control Panel \> Programs \> Turn Windows features on or off**, and check "Telnet Client". In a **new PowerShell window**:

  ```powershell
  telnet localhost 8000
  # Once connected, type this exactly and press Enter twice:
  GET / HTTP/1.1
  Host: localhost:8000

  ```

You'll see the server's raw HTTP response, proving it's all just text over a network.

---

## 1.2: Installing FastAPI and Understanding Dependencies

### Activate Your Virtual Environment

This step is critical to keep your project's dependencies isolated from your system's Python.

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  > **Windows Gotcha**: If you see an error about "execution policies," run this command **once** to allow locally signed scripts: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`.
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

Your terminal prompt should now be prefixed with `(venv)`.

### Installing FastAPI

```bash
pip install "fastapi[all]"
```

The `[all]` extra installs FastAPI plus its common companions: `uvicorn` (the server) and tools for documentation.

### Documenting Dependencies

Now, create a `requirements.txt` file. This file is a manifest of your project's dependencies and is crucial for reproducibility.

```bash
pip freeze > requirements.txt
```

Commit this file to Git. Now, anyone who clones your project can install the exact same package versions by running `pip install -r requirements.txt`.

### Understanding the Dependency Tree

Let's visualize the layers of software you just installed.

```bash
# Install the visualization tool
pip install pipdeptree
# Show the tree for FastAPI
pipdeptree -p fastapi
```

**Annotated Output:**

```
fastapi==0.104.1
├── pydantic [required: >=1.7.4, installed: 2.4.2]  # The data validation "bodyguard"
│   └── pydantic-core [required: ==2.10.1]         # Written in Rust for extreme speed
├── starlette [required: <0.28.0, installed: 0.27.0] # The core ASGI framework FastAPI builds on
└── typing-extensions [required: >=4.5.0]           # Backports for modern Python type hints
```

- **Key Insight**: You're not just installing one package; you're leveraging an ecosystem. FastAPI delegates routing to Starlette and data validation to Pydantic. This follows the **Separation of Concerns** principle, a cornerstone of good software design.

---

## 1.3: Your First FastAPI Application

### Code Organization: The `backend` Folder

All our server-side code will live in a `backend` directory.

```bash
# In your project root (pdm-tutorial)
mkdir backend
cd backend
# On Windows PowerShell: New-Item -ItemType Directory -Name backend; cd backend

# Create the main application file
touch main.py
# On Windows PowerShell: New-Item -ItemType File -Name main.py
```

### The Simplest Possible Server

Open `backend/main.py` and add the following. This is your first complete, runnable server.

```python
# main.py

# --- Imports (Line 1-2): Bring in the necessary tools.
from fastapi import FastAPI # The main class that provides all the functionality for your API.

# --- Application Instance (Line 4): Create the central object for your application.
# This 'app' object will be the main point of interaction for creating all your API endpoints.
# We add metadata here for the automatic documentation.
app = FastAPI(
    title="PDM Backend",
    description="API for our Parts Data Management (PDM) application.",
    version="0.1.0",
)

# --- Root Endpoint (Lines 11-14): Your first "route".
# A route is a URL path that the server listens to.
@app.get("/")  # This is a decorator. It tells FastAPI that the function below
               # is in charge of handling GET requests to the root path "/".
def read_root():
    # This function is called an "endpoint" or "route handler".
    # It returns a Python dictionary. FastAPI automatically converts this
    # dictionary to JSON and sends it as the HTTP response.
    return {"message": "Hello from the PDM Backend!"}
```

### Understanding Decorators

The `@app.get("/")` syntax is a Python **decorator**. It's "syntactic sugar" that wraps a function to add functionality. Here, it registers `read_root` as the handler for `GET /` requests.

#### 🏋️ Playground: Build Your Own Decorator

To truly understand decorators, create a file `decorator_playground.py` and run it:

```python
# decorator_playground.py
import time

def timer_decorator(func):
    """A decorator that prints how long a function took to run."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds.")
        return result
    return wrapper

@timer_decorator
def my_slow_function():
    time.sleep(1)
    print("Function finished!")

my_slow_function()
```

Run `python decorator_playground.py`. The decorator adds timing logic without you ever modifying `my_slow_function`. This is the power of decorators.

---

## 1.4: Running the Server with Uvicorn

### Starting the Server

Navigate your terminal into the `backend` directory.

```bash
# In the `backend` directory
uvicorn main:app --reload --host 127.0.0.1
```

- **Command Breakdown**:
  - `uvicorn`: The ASGI server.
  - `main:app`: In the file `main.py`, find the object named `app`.
  - `--reload`: Development-only flag that restarts the server on code changes.
  - `--host 127.0.0.1`: Binds to the localhost IP, which is safer for development on Windows.

### Testing Your Server

- **Browser**: Open `http://127.0.0.1:8000`.
- **Terminal (`curl`)**:
  ```powershell
  curl http://127.0.0.1:8000
  ```

---

## 1.5: Adding More Endpoints

Most APIs are built around **CRUD** operations: **C**reate, **R**ead, **U**pdate, **D**elete, which map to HTTP methods.

| Operation  | HTTP Method     | SQL Equivalent | Idempotent? | Description                                                        |
| :--------- | :-------------- | :------------- | :---------- | :----------------------------------------------------------------- |
| **Read**   | `GET`           | `SELECT`       | Yes         | Retrieves a resource. Repeating has no side effects.               |
| **Create** | `POST`          | `INSERT`       | No          | Creates a new resource. Repeating creates multiple resources.      |
| **Update** | `PUT` / `PATCH` | `UPDATE`       | Yes         | `PUT` replaces the entire resource. `PATCH` modifies parts of it.  |
| **Delete** | `DELETE`        | `DELETE`       | Yes         | Deletes a resource. Repeating results in the same state (deleted). |

### The `/api/files` Endpoint

Add this to `backend/main.py`, after your `read_root` function.

```python
# ADD THIS to main.py after the read_root function

@app.get("/api/files")
def get_files():
    """This endpoint returns a hardcoded list of files."""
    files = [
        {"name": "PN1001_OP1.mcam", "status": "available"},
        {"name": "PN1002_OP1.mcam", "status": "checked_out"},
        {"name": "PN1003_OP1.mcam", "status": "available"}
    ]
    return {"files": files}
```

Save the file. The server will restart. Test the new endpoint: `curl http://127.0.0.1:8000/api/files`.

---

## 1.6: Path & Query Parameters

### Path Parameters: Identifying a Resource

Use path parameters to fetch a _single_ specific resource.

**Add this to `main.py`:**

```python
# ADD THIS to main.py

@app.get("/api/files/{filename}")
def get_file_detail(filename: str):
    # The {filename} in the path is captured and passed as an argument.
    # The type hint 'filename: str' tells FastAPI to validate it's a string.
    return {
        "requested_filename": filename,
        "status": "available", # Hardcoded for now
        "size_mb": 1.2
    }
```

Test it: `curl http://127.0.0.1:8000/api/files/PN1001_OP1.mcam`.

### Query Parameters: Filtering a Collection

Use query parameters to filter or sort a list of resources.

**Add this to `main.py`:**

```python
# ADD THIS to main.py

@app.get("/api/search")
def search_files(query: str = None, status: str = "all", limit: int = 10):
    # Parameters with default values are optional query parameters.
    return {
        "filters": {"query": query, "status": status, "limit": limit},
        "results": f"Simulating search..."
    }
```

Test it: `curl "http://127.0.0.1:8000/api/search?query=PN1001&limit=5"` (use quotes in PowerShell).

---

## 1.7: Async/Await and Concurrency

FastAPI's power comes from `async` code, which allows a single process to handle many I/O-bound tasks concurrently.

### Sync vs. Async in FastAPI

Add these two endpoints to `main.py` to see the difference. Make sure to add `import asyncio` and `import time` at the top of your file.

```python
# ADD THIS to main.py

@app.get("/sync-slow")
def sync_slow():
    time.sleep(2)  # This BLOCKS the entire process for 2 seconds.
    return {"message": "Sync done"}

@app.get("/async-fast")
async def async_fast():
    await asyncio.sleep(2)  # This pauses this task, but lets the server work on others.
    return {"message": "Async done"}
```

### Test Concurrency

Open two separate terminals.

- **Test Sync (Blocking):** Run the request in terminal 1. As soon as it starts, run the same command in terminal 2. The second command will take about 4 seconds because it has to wait for the first one to finish.

  - **Windows PowerShell**: `Measure-Command { Invoke-WebRequest http://127.0.0.1:8000/sync-slow }`
  - **macOS/Linux**: `time curl http://127.0.0.1:8000/sync-slow`

- **Test Async (Non-Blocking):** Do the same for `/async-fast`. Both commands will finish in about 2 seconds because the server handles them concurrently.

---

## 1.8: Request Body & Data Validation with Pydantic

For `POST` requests, data is sent in the request body. **Pydantic** is FastAPI's "bodyguard," ensuring the incoming data matches a predefined schema.

### Defining a Pydantic Model

**Add this to `main.py`** (and `from pydantic import BaseModel` at the top).

```python
# ADD THIS to main.py

class FileCheckoutRequest(BaseModel):
    filename: str
    user: str
    message: str

@app.post("/api/checkout")
def checkout_file(request: FileCheckoutRequest):
    logger.info(f"Checkout request for {request.filename} by {request.user}")
    return {
        "success": True,
        "message": f"User '{request.user}' successfully checked out '{request.filename}'",
        "details": request.message
    }
```

FastAPI automatically reads the JSON body, validates it against your `FileCheckoutRequest` model, and returns a `422` error if it doesn't match.

---

## 1.9: Error Handling & Logging

### Raising Custom HTTP Errors

Use `HTTPException` to return specific error codes.

**Update `get_file_detail` in `main.py`** (and add `from fastapi import HTTPException`).

```python
# REPLACE the old get_file_detail function in main.py

@app.get("/api/files/{filename}")
def get_file_detail(filename: str):
    valid_files = ["PN1001_OP1.mcam", "PN1002_OP1.mcam"]
    if filename not in valid_files:
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found.")

    return {"requested_filename": filename, "status": "available"}
```

### Adding Logs

Logging is crucial for debugging.

**Add this to the top of `main.py`:**

```python
# ADD THIS to the top of main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

Now you can add `logger.info("Your message")` to any endpoint to see logs in your terminal.

---

## 1.10: Automatic API Documentation

FastAPI automatically generates interactive API documentation from your code.

- **Interactive Docs (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **Alternative Docs (ReDoc)**: `http://127.0.0.1:8000/redoc`

Explore the `/docs` page. You can execute requests directly from your browser, which is incredibly useful for testing.

---

## 1.11: Testing with Pytest

Automated tests ensure your code works and prevent future changes from breaking it.

### Install Testing Tools

```bash
pip install pytest httpx
pip freeze >> requirements.txt
```

### Create Your First Test File

Create a new file `backend/test_main.py`.

```python
# backend/test_main.py

from fastapi.testclient import TestClient
from .main import app # Import the app instance

# Create a client that makes requests to your app in-memory
client = TestClient(app)

def test_read_root():
    """Test that the root endpoint returns 200 OK and the correct message."""
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from the PDM Backend!"}

def test_checkout_file_success():
    """Test a successful file checkout."""
    response = client.post(
        "/api/checkout",
        json={
            "filename": "PN1001_OP1.mcam",
            "user": "test_user",
            "message": "A test checkout"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

def test_checkout_file_missing_field():
    """Test that a checkout with a missing field fails with 422."""
    response = client.post(
        "/api/checkout",
        json={"filename": "PN1001_OP1.mcam", "user": "test_user"}
    )
    assert response.status_code == 422
```

### Run Your Tests

From the `backend` directory:

```bash
pytest -v
```

You should see your tests passing. Congratulations\!

---

## Stage 1 Complete - Your First API

You've built a solid foundation for your backend. You have a working server with multiple endpoints, data validation, error handling, logging, documentation, and automated tests.

### Final Code for `main.py`

_This is the complete, runnable code at the end of this stage._

```python
# backend/main.py
import asyncio
import time
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- FastAPI App Instance ---
app = FastAPI(
    title="PDM Backend",
    description="API for our Parts Data Management (PDM) application.",
    version="0.1.0",
)

# --- Pydantic Models ---
class FileCheckoutRequest(BaseModel):
    filename: str = Field(..., description="The name of the file to check out.")
    user: str = Field(..., description="The username of the person checking out the file.")
    message: str = Field(..., description="A brief message explaining the reason for checkout.")

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Hello from the PDM Backend!"}

@app.get("/api/files")
def get_files():
    logger.info("Request received for /api/files")
    files = [
        {"name": "PN1001_OP1.mcam", "status": "available"},
        {"name": "PN1002_OP1.mcam", "status": "checked_out"},
        {"name": "PN1003_OP1.mcam", "status": "available"}
    ]
    return {"files": files}

@app.get("/api/files/{filename}")
def get_file_detail(filename: str):
    valid_files = ["PN1001_OP1.mcam", "PN1002_OP1.mcam"]
    if filename not in valid_files:
        logger.warning(f"File not found: {filename}")
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found.")

    return {"requested_filename": filename, "status": "available", "size_mb": 1.2}

@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "type": str(type(item_id))}

@app.get("/api/search")
def search_files(query: str = None, status: str = "all", limit: int = 10):
    return {
        "filters": {"query": query, "status": status, "limit": limit},
        "results": f"Simulating search..."
    }

@app.post("/api/checkout")
def checkout_file(request: FileCheckoutRequest):
    logger.info(f"Checkout attempt by user '{request.user}' for file '{request.filename}'")
    # In a real app, you would add locking logic here
    logger.info(f"Successfully processed checkout for '{request.filename}'")
    return {
        "success": True,
        "message": f"User '{request.user}' successfully checked out '{request.filename}'",
        "details": request.message,
    }

@app.get("/sync-slow")
def sync_slow():
    time.sleep(2)
    return {"message": "Sync done"}

@app.get("/async-fast")
async def async_fast():
    await asyncio.sleep(2)
    return {"message": "Async done"}
```

### What's Next?

Excellent. Let's move on to Stage 2.

Here is the fully expanded and unified tutorial for building your first frontend. It integrates all the deeper explanations, Windows specifics, and best practices we've discussed.

---

# Stage 2: First Frontend - HTML, CSS, & JavaScript Basics (Expanded & Unified)

## Introduction: The Goal of This Stage

Your backend can serve data, but data isn't a user interface. In this stage, you'll build the "dining room" of our restaurant analogy—the visual layer that users actually see and interact with. We'll connect this frontend to the backend API you built in Stage 1.

By the end of this stage, you will:

- Serve static HTML, CSS, and JavaScript files from your FastAPI backend.
- Understand HTML's role as the structural skeleton of a webpage.
- Apply CSS for styling, layout, and presentation.
- Use JavaScript to make your page interactive and fetch data from your API.
- Handle user events like button clicks and form submissions.
- Understand the browser's rendering process.

---

### **🧠 Foundational Concepts: A Deeper Look**

- **Time Investment:** 4-6 hours.
- **Historical Insight**: The frontend is a trinity of technologies that evolved separately. **HTML** (1990) provided the structure. **CSS** (1996) was proposed by Håkon Wium Lie to separate style from structure. **JavaScript** (1995) was created by Brendan Eich in just 10 days at Netscape to add interactivity. The modern Single-Page Application (SPA) was born from technologies like **AJAX** (2005), which allowed parts of a page to update without a full reload.
- **Key Concept - SPA vs. MPA**:
  - **Multi-Page Application (MPA)**: The traditional web model. Clicking a link reloads the entire page from the server.
  - **Single-Page Application (SPA)**: The modern model we're building. The page loads once, and JavaScript dynamically fetches data and updates the content. This feels faster and more like a desktop application.

---

## 2.1: The Frontend-Backend Relationship

Our application architecture clearly separates the client (frontend) from the server (backend). They are two distinct programs that communicate over the network using the HTTP protocol.

| Layer            | Frontend (Runs in Browser)           | Backend (Runs on Server)              | Communication Channel       |
| :--------------- | :----------------------------------- | :------------------------------------ | :-------------------------- |
| **Presentation** | HTML, CSS, JavaScript                | N/A                                   | HTTP/JSON                   |
| **Logic**        | Event Handlers (e.g., button clicks) | API Endpoints (e.g., `/api/checkout`) | `fetch()` API in JavaScript |
| **Data**         | State held in the DOM/JS variables   | Database, Filesystem                  | API Calls                   |

This separation, known as **decoupling**, is a core principle of modern software engineering. It allows teams to work in parallel and enables the backend to serve multiple different frontends (e.g., a web app, a mobile app, and a desktop client).

---

## 2.2: Serving Static Files from FastAPI

First, we need to tell our FastAPI server how to deliver the HTML, CSS, and JavaScript files to the browser.

### Create the Frontend Folder Structure

In your `backend` directory, create the folders to hold your static assets.

- **On macOS/Linux:**
  ```bash
  mkdir -p static/css static/js
  ```
- **On Windows PowerShell:**
  ```powershell
  New-Item -ItemType Directory -Force -Path static\css
  New-Item -ItemType Directory -Force -Path static\js
  ```

The `-p` (or `-Force`) flag creates parent directories if they don't exist.

### Configure FastAPI to Serve Static Files

Update `backend/main.py`. We need to add two things: a "mount" for the `/static` directory and a new root endpoint to serve `index.html`.

**Updated Code: Add to `main.py`**

```python
# ADD these imports at the top of main.py
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path # Make sure this is imported

# ... keep existing imports and app = FastAPI(...) line ...

# ADD this line right after `app = FastAPI(...)`
app.mount("/static", StaticFiles(directory="static"), name="static")


# REPLACE your old root ("/") endpoint with this one
@app.get("/")
def serve_frontend():
    # This endpoint will serve your main HTML file for the root URL
    return FileResponse("static/index.html")

# ... keep all your other API endpoints (/api/files, /api/checkout, etc.) ...
```

**Understanding the Code:**

- `app.mount("/static", ...)`: This tells FastAPI, "Any request whose URL starts with `/static` should not be handled by my Python endpoints. Instead, treat it as a request for a static file from the `static` directory." This is much more efficient than reading and sending files with Python.
- `return FileResponse("static/index.html")`: When a user visits the root of your site (`http://localhost:8000/`), this endpoint sends the `index.html` file as the response.

---

## 2.3: HTML - The Structure Layer

HTML (HyperText Markup Language) provides the skeleton of your web page.

### Create `index.html`

Create a new file at `backend/static/index.html`.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PDM - Parts Data Management</title>
    <link rel="stylesheet" href="/static/css/style.css" />
  </head>
  <body>
    <header>
      <h1>PDM System</h1>
      <p>Parts Data Management</p>
    </header>

    <main>
      <section id="file-list-section">
        <h2>Available Files</h2>
        <div id="file-list">
          <p>Loading files...</p>
        </div>
      </section>
    </main>

    <footer>
      <p>&copy; 2025 PDM Tutorial</p>
    </footer>

    <script src="/static/js/app.js" defer></script>
  </body>
</html>
```

### Test It

Run your server (`uvicorn main:app --reload`) and visit `http://127.0.0.1:8000`. You should see a plain, unstyled page. Press `F12` to open Developer Tools and look at the "Elements" tab to see the DOM tree the browser has created.

---

## 2.4: CSS - The Presentation Layer

CSS (Cascading Style Sheets) adds style to your HTML skeleton.

### Create `style.css`

Create a new file at `backend/static/css/style.css`.

```css
/* ============================================ */
/* RESET & GLOBAL STYLES                      */
/* ============================================ */

/* Universal selector: Resets browser default styles for a consistent base. */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box; /* This makes layout math predictable. Width/height now include padding and border. */
}

/* Base styles for the entire page. */
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, sans-serif; /* System font stack for native look and performance. */
  line-height: 1.6; /* Improves readability by adding space between lines of text. */
  color: #333; /* A dark gray is often easier on the eyes than pure black. */
  background-color: #f5f5f5;
}

/* ============================================ */
/* LAYOUT & THEME                             */
/* ============================================ */

header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

main {
  max-width: 1200px; /* Constrains content width on large screens for better readability. */
  margin: 2rem auto; /* `auto` on left/right centers the block horizontally. */
  padding: 0 1rem;
}

section {
  background: white;
  padding: 2rem;
  border-radius: 8px; /* Rounded corners for a modern "card" look. */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

h2 {
  color: #667eea;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

footer {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 0.9rem;
}

/* ============================================ */
/* FILE LIST COMPONENTS                       */
/* ============================================ */

#file-list {
  display: flex; /* Enables flexbox layout. */
  flex-direction: column; /* Stacks items vertically. */
  gap: 1rem; /* Modern way to add space between flex items. */
}

.file-item {
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  display: flex;
  justify-content: space-between; /* Pushes children to opposite ends. */
  align-items: center; /* Vertically aligns children. */
  transition: all 0.3s ease; /* Smoothly animates changes on hover. */
}

.file-item:hover {
  background-color: #f9f9f9;
  border-color: #667eea;
  transform: translateX(5px); /* Adds a subtle interactive feel. */
}

.file-name {
  font-weight: 600;
}

.file-status {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 500;
}

.status-available {
  background-color: #d4edda;
  color: #155724;
}

.status-checked_out {
  background-color: #fff3cd;
  color: #856404;
}
```

### Refresh Your Browser

Visit `http://127.0.0.1:8000` again. Your page should now be beautifully styled\!

---

## 2.5: JavaScript - The Behavior Layer

JavaScript brings your page to life. It will fetch data from your API and update the DOM (the structure of the page) dynamically.

### Create `app.js`

Create a new file at `backend/static/js/app.js`.

```javascript
// ============================================
// INITIALIZATION
// ============================================

// This event listener waits until the browser has fully parsed the HTML
// before running our main code. This prevents errors from trying to
// find elements that don't exist yet.
document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded and parsed");
  loadFiles(); // Initial call to fetch and display files.
});

// ============================================
// API & DATA FUNCTIONS
// ============================================

/**
 * Fetches the list of files from our backend API.
 */
async function loadFiles() {
  console.log("Loading files from API...");
  const fileListContainer = document.getElementById("file-list");
  fileListContainer.innerHTML = "<p>Loading files...</p>"; // Show loading state

  try {
    // `fetch` is the modern browser API for making HTTP requests.
    // `await` pauses the function until the network request completes.
    const response = await fetch("/api/files");

    if (!response.ok) {
      // If the server responded with an error (e.g., 404, 500), throw an error.
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // `await response.json()` parses the JSON body of the response.
    const data = await response.json();
    console.log("Received data:", data);

    // Pass the array of files to the display function.
    displayFiles(data.files);
  } catch (error) {
    console.error("Error loading files:", error);
    displayError("Failed to load files. Please refresh the page.");
  }
}

// ============================================
// DOM MANIPULATION FUNCTIONS
// ============================================

/**
 * Renders the list of files into the DOM.
 * @param {Array} files - An array of file objects.
 */
function displayFiles(files) {
  const container = document.getElementById("file-list");
  container.innerHTML = ""; // Clear any previous content (like the loading message).

  if (!files || files.length === 0) {
    container.innerHTML = "<p>No files found.</p>";
    return;
  }

  // Loop through each file and create an HTML element for it.
  files.forEach((file) => {
    const fileElement = createFileElement(file);
    container.appendChild(fileElement); // Add the new element to the DOM.
  });

  console.log(`Displayed ${files.length} files`);
}

/**
 * Creates a single DOM element for a file.
 * @param {object} file - The file object with name and status.
 * @returns {HTMLElement} The created div element.
 */
function createFileElement(file) {
  // 1. Create elements in memory (they are not on the page yet).
  const div = document.createElement("div");
  div.className = "file-item"; // Apply CSS classes.

  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name; // Use .textContent to prevent XSS attacks. It treats all input as plain text.

  const statusSpan = document.createElement("span");
  // Use template literals for dynamic class names.
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " "); // Make "checked_out" more readable.

  // 2. Assemble the elements.
  div.appendChild(nameSpan);
  div.appendChild(statusSpan);

  // 3. Return the fully assembled element.
  return div;
}

/**
 * Displays an error message in the file list container.
 * @param {string} message - The error message to display.
 */
function displayError(message) {
  const container = document.getElementById("file-list");
  container.innerHTML = `
    <div style="color: red; padding: 1rem; background: #fee; border-radius: 4px;">
      ${message}
    </div>
  `;
}
```

### Refresh Your Browser

Visit `http://127.0.0.1:8000` one last time. The "Loading files..." message will be replaced by the list of files fetched directly from your backend API\!

---

## 2.6: Test the Complete Stack

Now is a great time to use your browser's Developer Tools (`F12`) to see everything working together.

- **Console Tab**: You'll see your `console.log` messages, showing the flow from "DOM loaded" to "Received data" to "Displayed files".
- **Network Tab**: Refresh the page (`F5`). You'll see the browser request `index.html`, then `style.css`, then `app.js`, and finally `app.js` makes its own request to `/api/files`. Click on the `files` request to inspect the headers and the JSON response from your FastAPI server.

You have now successfully built and connected a frontend and a backend\!

---

## Stage 2 Complete - You Built a Frontend\!

### What You Built

- A complete HTML/CSS/JavaScript frontend.
- Static file serving from FastAPI.
- API requests (`GET`) from JavaScript using the `fetch` API.
- Dynamic DOM manipulation to display data.

### What's Next?

Excellent. Let's move on to the core logic of our application.

Here is the fully expanded and unified **Stage 3**. This version replaces the hardcoded data from Stages 1-2 with real filesystem operations, introduces the critical concept of file locking, and explains how to handle the security risks of concurrent operations.

---

# Stage 3: App Core Features - Real File Operations & Locking (Expanded & Unified)

## Introduction: The Goal of This Stage

So far, your app uses "dummy" data. In this stage, you'll make it **real**. We will connect the backend to the filesystem to read actual files, implement a locking mechanism to prevent users from overwriting each other's work (the core feature of a PDM system), and persist this lock information.

By the end of this stage, you will:

- Read files directly from a `repo/` directory on the server.
- Store and manage application state (who has what file locked) in a `locks.json` file.
- Implement robust `checkout` and `checkin` logic.
- Understand and prevent **race conditions**, a critical and often hidden bug in concurrent systems.
- Update the frontend to perform real checkout and checkin operations.

---

### **🧠 Foundational Concepts: A Deeper Look**

- **Time Investment:** 5-7 hours. This stage is dense and foundational.
- **Software Engineering Principle: Single Responsibility Principle (SRP)**. Each function should do one thing well. Our `get_files` function will only read file lists. Our `save_locks` function will only write lock data. This makes code easier to test, debug, and maintain.
- **Design Pattern: Repository Pattern**. We are creating a simple "repository" for our file and lock data. This pattern abstracts the data source. Our functions like `load_locks` act as an interface. Later, if we wanted to switch from JSON files to a SQL database, we would only need to change the implementation inside these functions; the rest of our application code (`checkout_file`, etc.) would remain the same.
- **Key Concept: Soft Delete vs. Hard Delete**. When we implement file deletion later, we could just remove the file (a "hard delete"). A better practice, which we'll explore, is a "soft delete," where we just mark the file as deleted (e.g., by adding a `deleted_at` timestamp to its metadata). This makes deletion recoverable and provides a better audit trail.

---

## 3.1: Understanding the Filesystem in Python

Your application lives on a server with a filesystem. Python gives you powerful tools to interact with it, but you need to understand how paths work.

### Absolute vs. Relative Paths

| Type         | Example                                                            | Pro                                                          | Con                                                                | When to Use                       |
| :----------- | :----------------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------------- | :-------------------------------- |
| **Absolute** | `C:\Users\You\pdm-tutorial\repo` or `/Users/You/pdm-tutorial/repo` | Unambiguous. Works no matter where you run your script from. | Verbose, less portable between OSes if hardcoded.                  | **Best for server applications**. |
| **Relative** | `./repo` or `repo/`                                                | Short and convenient.                                        | **Brittle**. Breaks if you change the script's execution location. | Best for simple, local scripts.   |

For our backend server, we will **always construct absolute paths** to avoid bugs related to the "current working directory."

### The `os` vs. `pathlib` Modules

Python has two main ways to handle paths:

1.  **`os.path`**: The older, function-based module.
2.  **`pathlib`**: The modern, object-oriented module (Python 3.4+).

We will use `pathlib` as it's cleaner, more powerful, and automatically handles OS differences (like `\` on Windows vs. `/` on macOS/Linux).

#### 🏋️ Practice Exercise: Cross-OS Path Tester

Create a new file `path_test.py` in your `backend` directory to see the difference.

```python
# backend/path_test.py

import os
from pathlib import Path

# --- Using the legacy 'os' module ---
print("--- Using os module ---")
current_dir_str = os.getcwd()
print(f"Current directory (as string): {current_dir_str}")

# os.path.join is required to safely join path components
joined_path = os.path.join(current_dir_str, 'repo', 'file.mcam')
print(f"os.path.join result: {joined_path}")
# On Windows, this will correctly use backslashes: '...\repo\file.mcam'


# --- Using the modern 'pathlib' module ---
print("\n--- Using pathlib module ---")
current_dir_obj = Path.cwd() # The same as Path() or Path('.')
print(f"Current directory (as Path object): {current_dir_obj}")

# The division operator `/` is overloaded for easy and readable path joining.
# It automatically uses the correct separator for your OS.
repo_path = current_dir_obj / 'repo' / 'file.mcam'
print(f"pathlib join result: {repo_path}")

# Path objects have useful properties
print(f"Parent directory: {repo_path.parent}")
print(f"Filename: {repo_path.name}")
print(f"File stem (name without extension): {repo_path.stem}")
print(f"File extension: {repo_path.suffix}")

# Easily check for existence
print(f"Does the repo path exist? {repo_path.exists()}")
```

Run it with `python path_test.py`. `pathlib` makes path manipulation intuitive and safe.

---

## 3.2: Creating the Repository Structure

Let's create the directory where our `.mcam` files will be stored.

### Create the `repo` Directory

- **On macOS/Linux:** In your `backend` directory:
  ```bash
  mkdir repo
  ```
- **On Windows PowerShell:** In your `backend` directory:
  ```powershell
  New-Item -ItemType Directory -Name repo
  ```

### Add Sample Files

Now, let's create some dummy `.mcam` files inside the new `repo` directory.

- **On macOS/Linux:**
  ```bash
  echo "G0 X0 Y0" > repo/PN1001_OP1.mcam
  echo "G0 X10 Y10" > repo/PN1002_OP1.mcam
  echo "G0 X20 Y20" > repo/PN1003_OP1.mcam
  ```
- **On Windows PowerShell:**
  ```powershell
  "G0 X0 Y0" | Set-Content -Path repo\PN1001_OP1.mcam
  "G0 X10 Y10" | Set-Content -Path repo\PN1002_OP1.mcam
  "G0 X20 Y20" | Set-Content -Path repo\PN1003_OP1.mcam
  ```

> **What is `G0 X0 Y0`?** `.mcam` files are for Mastercam and contain G-code, the language used to control CNC machines. `G0` is a command for a rapid, non-cutting move. We're just using this as simple placeholder content.

---

## 3.3: Reading Files from the Filesystem

Now we'll replace the hardcoded file list in our `get_files` endpoint with code that reads from our new `repo` directory.

### Defining Reliable Paths

First, add path definitions to the top of `backend/main.py`. This uses `pathlib` to create absolute paths that will always work correctly.

```python
# ADD this to the top of backend/main.py
import os
from pathlib import Path

# --- Path Definitions ---
# This creates an absolute path to the directory containing main.py
BASE_DIR = Path(__file__).resolve().parent

# Define paths relative to the base directory.
# This ensures our app knows where to find these regardless of
# where we run the script from.
REPO_PATH = BASE_DIR / 'repo'
LOCKS_FILE = BASE_DIR / 'locks.json'
```

### Update the `/api/files` Endpoint

Now, replace your entire `get_files` function in `main.py` with this new version.

```python
# REPLACE your old get_files function with this one

@app.get("/api/files")
def get_files():
    """
    Scans the repository directory and returns a list of all .mcam files found.
    """
    logger.info(f"Scanning repository at: {REPO_PATH}")

    # --- Defensive Check (Guard Clause) ---
    # Always check if the directory exists before trying to read from it.
    if not REPO_PATH.exists() or not REPO_PATH.is_dir():
        logger.error(f"Repository path does not exist or is not a directory: {REPO_PATH}")
        # Return a 500 error because this is a server configuration problem.
        raise HTTPException(status_code=500, detail="Server repository not found.")

    files = []
    # `os.listdir` is a simple way to get all item names in a directory.
    for filename in os.listdir(REPO_PATH):
        # We build a full Path object to get more information.
        full_path = REPO_PATH / filename

        # Filter for files only (not subdirectories) and ensure they have the correct extension.
        # .lower() makes the check case-insensitive (.mcam vs .MCAM).
        if full_path.is_file() and filename.lower().endswith('.mcam'):
            # `.stat().st_size` reads file metadata (the inode) without reading the
            # entire file content, which is very fast.
            files.append({
                "name": filename,
                "status": "available",  # We'll make this dynamic soon.
                "size_bytes": full_path.stat().st_size
            })

    logger.info(f"Found and returning {len(files)} .mcam files.")
    return {"files": files}
```

### Test It

Restart your server and visit `http://127.0.0.1:8000` (or `http://localhost:8000` from Stage 2). Your frontend should now display the real files from your `repo/` directory\!

---

## 3.4: Persisting Data with JSON Files

Our file list is real, but the "checked_out" status is still hardcoded. We need a place to store the application's **state**. For now, we'll use a simple JSON file. This will act as our mini-database.

### The Lock Data Structure

We will store our lock information in `backend/locks.json`. Create this file manually for now.

**Create `backend/locks.json`:**

```json
{}
```

This is an empty JSON object. When a user checks out a file, we'll add an entry like this:

```json
{
  "PN1002_OP1.mcam": {
    "user": "mmclean",
    "timestamp": "2025-10-04T20:30:00Z",
    "message": "Initial design review"
  }
}
```

This key-value structure allows for very fast lookups (O(1) complexity) to check if a file is locked.

### Helper Functions for State Management

To avoid duplicating code, we'll create helper functions to read from and write to `locks.json`. This follows the **Single Responsibility Principle**.

**Add this code to `main.py`** (after your path definitions).

```python
# ADD this to main.py
import json
from datetime import datetime, timezone

# --- Lock Management Helper Functions ---

def load_locks() -> dict:
    """Safely loads the locks.json file."""
    if not LOCKS_FILE.exists():
        return {}  # Return empty dict if the file doesn't exist yet.

    try:
        with open(LOCKS_FILE, 'r') as f:
            # The 'with' statement ensures the file is automatically closed.
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error reading or parsing locks.json: {e}")
        return {} # Return empty on error to prevent crashes.

def save_locks(locks: dict):
    """Safely saves the locks dictionary to locks.json."""
    try:
        with open(LOCKS_FILE, 'w') as f:
            # indent=4 makes the JSON file human-readable.
            json.dump(locks, f, indent=4)
    except IOError as e:
        logger.error(f"Error writing to locks.json: {e}")
        # This is a critical server error, so we notify the client.
        raise HTTPException(status_code=500, detail="Failed to save lock data.")
```

**`with open(...)`**: This is a **context manager**. It's the standard, safe way to work with files in Python because it guarantees the file is closed properly, even if errors occur.

---

## 3.5: Implementing the Checkout/Checkin Logic

Now we can update our API endpoints to use the helper functions and modify the `locks.json` state.

### Update the Checkout Endpoint

Replace your old `/api/checkout` endpoint in `main.py`.

```python
# REPLACE your old /api/checkout endpoint with this one

@app.post("/api/checkout")
def checkout_file(request: FileCheckoutRequest):
    logger.info(f"Checkout request: {request.user} -> {request.filename}")

    # --- Validation ---
    file_path = REPO_PATH / request.filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File to check out not found.")

    locks = load_locks()

    if request.filename in locks:
        existing_lock = locks[request.filename]
        logger.warning(f"Checkout failed: {request.filename} is already locked by {existing_lock['user']}")
        # 409 Conflict is the correct status code for a state conflict.
        raise HTTPException(
            status_code=409,
            detail=f"File is already checked out by {existing_lock['user']}."
        )

    # --- State Mutation ---
    locks[request.filename] = {
        "user": request.user,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": request.message
    }
    save_locks(locks)

    logger.info(f"File '{request.filename}' checked out successfully by '{request.user}'")
    return {"success": True, "message": "File checked out successfully"}
```

### Create the Checkin Endpoint

This endpoint will do the reverse: remove a lock.

**Add this new endpoint to `main.py`:**

```python
# ADD this new endpoint to main.py
from pydantic import BaseModel

class FileCheckinRequest(BaseModel):
    filename: str
    user: str

@app.post("/api/files/checkin")
def checkin_file(request: FileCheckinRequest):
    logger.info(f"Checkin request: {request.user} -> {request.filename}")

    locks = load_locks()

    if request.filename not in locks:
        raise HTTPException(status_code=400, detail="File is not currently checked out.")

    # Authorization Check: Only the user who locked the file can check it in.
    if locks[request.filename]['user'] != request.user:
        logger.warning(f"AuthZ failed: User '{request.user}' tried to check in a file locked by '{locks[request.filename]['user']}'.")
        raise HTTPException(status_code=403, detail="You do not own the lock on this file.")

    # --- State Mutation ---
    del locks[request.filename]
    save_locks(locks)

    logger.info(f"File '{request.filename}' checked in successfully by '{request.user}'")
    return {"success": True, "message": "File checked in successfully"}
```

### Make `get_files` Lock-Aware

Finally, update `get_files` one last time to reflect the real lock status.

```python
# REPLACE your get_files function again with this final version

@app.get("/api/files")
def get_files():
    if not REPO_PATH.exists() or not REPO_PATH.is_dir():
        raise HTTPException(status_code=500, detail="Server repository not found.")

    locks = load_locks() # Load the current lock status
    files = []

    for filename in os.listdir(REPO_PATH):
        full_path = REPO_PATH / filename
        if full_path.is_file() and filename.lower().endswith('.mcam'):

            lock_info = locks.get(filename) # Safely get lock info if it exists

            files.append({
                "name": filename,
                "status": "checked_out" if lock_info else "available",
                "size_bytes": full_path.stat().st_size,
                "locked_by": lock_info["user"] if lock_info else None
            })

    return {"files": files}
```

---

## 3.6: Race Conditions - The Hidden Danger

Your app seems to work, but it has a hidden, critical flaw: a **race condition**.

**The Scenario:**
Imagine two users, Alice and Bob, click "Checkout" on the same file at almost the exact same time.

1.  **Alice's Request (10:00:00.000 AM):** The server runs `load_locks()`. The file is available.
2.  **Bob's Request (10:00:00.001 AM):** Before Alice's request can save, the server switches to Bob's request. It runs `load_locks()`. The file is _still_ available.
3.  **Alice's Request:** Adds her lock to its in-memory dictionary and calls `save_locks()`. `locks.json` now shows Alice has the file.
4.  **Bob's Request:** Adds _his_ lock to _his_ in-memory dictionary and calls `save_locks()`. He overwrites the file, erasing Alice's lock.

**Result:** Both users think they have the file checked out. Data corruption is inevitable. This is a **Time-of-Check to Time-of-Use (TOCTOU)** bug.

### The Solution: Atomic Operations with File Locks

We need to ensure that the entire sequence of **read -\> modify -\> write** is **atomic**—it cannot be interrupted. We do this by acquiring an OS-level lock on the `locks.json` file itself.

#### Cross-Platform File Locking

The original tutorial used `fcntl`, which only works on macOS/Linux. Here is a cross-platform solution.

**Add this class to `main.py`:**

```python
# ADD this new class to main.py
import os
# These imports are conditional based on the OS.
if os.name == 'nt': # Windows
    import msvcrt
else: # Unix-like (macOS, Linux)
    import fcntl

class LockedFile:
    """A cross-platform context manager for file locking."""
    def __init__(self, filepath, mode='r'):
        self.filepath = filepath
        self.mode = mode
        self.file = None
        self.fd = None

    def __enter__(self):
        self.file = open(self.filepath, self.mode)
        self.fd = self.file.fileno()

        if os.name == 'nt':
            # On Windows, lock a single byte. It's a bit of a hack but works.
            msvcrt.locking(self.fd, msvcrt.LK_LOCK, 1)
        else:
            # On Unix, use flock for an exclusive lock. This will block until the lock is acquired.
            fcntl.flock(self.fd, fcntl.LOCK_EX)

        logger.debug(f"Acquired lock on {self.filepath}")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.name == 'nt':
            msvcrt.locking(self.fd, msvcrt.LK_UNLCK, 1)
        else:
            fcntl.flock(self.fd, fcntl.LOCK_UN)

        self.file.close()
        logger.debug(f"Released lock on {self.filepath}")
        return False # Propagate exceptions
```

### Update `load_locks` and `save_locks`

Now, wrap your file operations with this new `LockedFile` context manager.

```python
# REPLACE your load_locks and save_locks functions with these

def load_locks() -> dict:
    if not LOCKS_FILE.exists():
        return {}
    try:
        # The 'with' statement now uses our locking class
        with LockedFile(LOCKS_FILE, 'r') as f:
            # The entire read operation is now atomic
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error reading or parsing locks.json: {e}")
        return {}

def save_locks(locks: dict):
    try:
        with LockedFile(LOCKS_FILE, 'w') as f:
            # The entire write operation is now atomic
            json.dump(locks, f, indent=4)
    except IOError as e:
        logger.error(f"Error writing to locks.json: {e}")
        raise HTTPException(status_code=500, detail="Failed to save lock data.")
```

Now, the race condition is impossible. The OS guarantees that only one request can hold the lock on `locks.json` at a time, making your read-modify-write cycle safe.

---

## 3.7: Update the Frontend

Finally, let's update the frontend to use these new endpoints. We'll replace the old form and `prompt()` dialogs.

### Update `createFileElement` in `app.js`

This function will now create either a "Checkout" or "Checkin" button based on the file's status.

```javascript
// REPLACE your createFileElement function in app.js

function createFileElement(file) {
  const div = document.createElement("div");
  div.className = "file-item";

  const infoDiv = document.createElement("div");
  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ");

  infoDiv.appendChild(nameSpan);
  infoDiv.appendChild(statusSpan);

  if (file.locked_by) {
    const lockedSpan = document.createElement("span");
    lockedSpan.className = "locked-indicator";
    lockedSpan.textContent = ` (locked by ${file.locked_by})`;
    infoDiv.appendChild(lockedSpan);
  }

  const actionsDiv = document.createElement("div");
  actionsDiv.className = "file-actions"; // We'll style this next

  if (file.status === "available") {
    const checkoutBtn = document.createElement("button");
    checkoutBtn.className = "btn btn-checkout"; // New class
    checkoutBtn.textContent = "Checkout";
    checkoutBtn.onclick = () => handleCheckout(file.name);
    actionsDiv.appendChild(checkoutBtn);
  } else {
    const checkinBtn = document.createElement("button");
    checkinBtn.className = "btn btn-checkin"; // New class
    checkinBtn.textContent = "Checkin";
    checkinBtn.onclick = () => handleCheckin(file.name);
    actionsDiv.appendChild(checkinBtn);
  }

  div.appendChild(infoDiv);
  div.appendChild(actionsDiv);
  return div;
}
```

### Add New Handlers to `app.js`

Remove the old form and add these new handlers.

```javascript
// ADD these new functions to app.js

async function handleCheckout(filename) {
  const user = prompt("Enter your name:");
  if (!user) return; // User cancelled

  const message = prompt("Reason for checkout:");
  if (!message) return;

  try {
    const response = await fetch("/api/files/checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename, user, message }),
    });

    if (response.ok) {
      alert("File checked out successfully!");
      loadFiles(); // Refresh the list
    } else {
      const errorData = await response.json();
      alert(`Error: ${errorData.detail}`);
    }
  } catch (error) {
    alert("An unexpected error occurred.");
    console.error(error);
  }
}

async function handleCheckin(filename) {
  const user = prompt("Enter your name to confirm check-in:");
  if (!user) return;

  try {
    const response = await fetch("/api/files/checkin", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename, user }),
    });

    if (response.ok) {
      alert("File checked in successfully!");
      loadFiles(); // Refresh the list
    } else {
      const errorData = await response.json();
      alert(`Error: ${errorData.detail}`);
    }
  } catch (error) {
    alert("An unexpected error occurred.");
    console.error(error);
  }
}
```

### Add Button Styles to `style.css`

```css
/* ADD these styles to your style.css file */

.file-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-checkout {
  background: #28a745;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.btn-checkout:hover {
  background: #218838;
}

.btn-checkin {
  background: #ffc107;
  color: #212529;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.btn-checkin:hover {
  background: #e0a800;
}

.locked-indicator {
  font-size: 0.85rem;
  color: #856404;
  font-style: italic;
  margin-left: 0.5rem;
}
```

---

## Stage 3 Complete - Real Application Logic\!

### What You Built

- A backend that interacts with the real filesystem.
- A JSON-based persistence layer for application state.
- A complete, race-condition-safe checkout and checkin workflow.
- A frontend that can perform these core PDM actions.

### Verification Checklist

- [ ] Can see real files from your `repo/` directory in the UI.
- [ ] Clicking "Checkout" locks the file and updates `locks.json`.
- [ ] The UI updates to show the file is "checked_out" by you.
- [ ] Another user cannot check out the same file (they get a 409 Conflict error).
- [ ] You can successfully "Checkin" a file you have locked.
- [ ] You cannot check in a file locked by someone else (you get a 403 Forbidden error).

### What's Next?

In **Stage 4**, we'll dramatically improve the frontend user experience. We will replace the ugly `prompt()` dialogs with custom, non-blocking modal forms and add client-side search, filtering, and sorting capabilities.

Here is the fully expanded and unified tutorial for **Stage 4**. This stage focuses on transforming the basic frontend into a polished, professional, and interactive user interface by replacing clunky browser dialogs with custom components and adding features like search, sorting, and loading indicators.

---

# Stage 4: Frontend Enhancements - Interactive UI Patterns (Expanded & Unified)

## Introduction: The Goal of This Stage

Your application is functional, but the user experience (UX) is rough. The `prompt()` and `alert()` dialogs are blocking and unappealing. There's no way to search for a specific file, and users get no visual feedback while data is loading. This stage is all about polishing that experience.

In this stage, you'll learn professional frontend patterns to build a responsive and intuitive UI:

- Build reusable, non-blocking **modal dialogs** to replace browser prompts.
- Implement client-side **search and filtering** for real-time results.
- Add multi-criteria **sorting** to the file list.
- Provide user feedback with **loading states** and notifications.
- Deepen your understanding of JavaScript event handling and state management.

---

### **🧠 Foundational Concepts: A Deeper Look**

- **Time Investment:** 4-6 hours.
- **Historical Insight**: The field of User Experience (UX) was heavily influenced by Don Norman's 1988 book, "The Psychology of Everyday Things." Patterns like modals evolved from the "dialog boxes" of early graphical user interfaces developed at places like Xerox PARC in the 1970s. We're building on decades of design principles.
- **Software Engineering Principle: Atomic Design**. Coined by Brad Frost, this principle suggests building UIs from small, reusable components.
  - **Atoms**: Basic HTML elements (e.g., `<button>`, `<input>`).
  - **Molecules**: Groups of atoms (e.g., a `<label>` and an `<input>` form a search box).
  - **Organisms**: Complex components made of molecules (e.g., our file list, which is made of many file items).
    Our modal is a perfect example of a reusable "molecule" or "organism."
- **Tools Introduction**:
  - **Lighthouse**: An open-source tool built into Chrome DevTools (F12 -\> Lighthouse tab). It audits your page for performance, accessibility, and SEO, giving you a score and actionable advice.
  - **Figma**: A popular, free-to-start UI design tool. Professionals use tools like Figma to create wireframes and mockups of the UI _before_ writing any code.

---

## 4.1: The Problem with `prompt()` and `alert()`

Our current code uses `prompt()` to get user input. This is bad practice for several reasons.

| Issue            | Why It's a Problem                                                                                       | The Professional Solution                                                                |
| :--------------- | :------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------- |
| **Blocking**     | It freezes the entire browser tab. No other JavaScript can run until the user interacts with the prompt. | Custom modals are non-blocking; they are part of the page's event loop.                  |
| **Unstylable**   | It uses the browser's native UI, which you cannot style with CSS. It looks dated and inconsistent.       | Custom modals are just HTML and CSS, giving you full control over their appearance.      |
| **Limited**      | It can only accept a single line of text. No complex forms, no rich text, no validation hints.           | Modals can contain any HTML, including complex forms with validation, date pickers, etc. |
| **Inaccessible** | Poor support for screen readers and keyboard navigation.                                                 | Properly built modals can be made fully accessible (WCAG compliant).                     |

**Bottom line**: `prompt()` and `alert()` are fine for quick debugging, but they should never be used in a production application.

---

## 4.2: Building a Reusable Modal Component

We will replace the `prompt()` dialogs with a custom, reusable modal component built with HTML, CSS, and a JavaScript class.

### HTML Structure for the Modals

Add this HTML to `backend/static/index.html`, right before the closing `</body>` tag. It will be hidden by default with CSS.

```html
<div id="checkout-modal" class="modal-overlay hidden">
  <div
    class="modal-content"
    role="dialog"
    aria-modal="true"
    aria-labelledby="checkout-title"
  >
    <div class="modal-header">
      <h3 id="checkout-title">Checkout File</h3>
      <button class="modal-close" aria-label="Close">&times;</button>
    </div>
    <div class="modal-body">
      <p>File: <strong id="checkout-filename"></strong></p>
      <form id="checkout-form">
        <div class="form-group">
          <label for="checkout-user">Your Name:</label>
          <input
            type="text"
            id="checkout-user"
            required
            placeholder="Enter your name"
            autocomplete="name"
          />
        </div>
        <div class="form-group">
          <label for="checkout-message">Reason:</label>
          <textarea
            id="checkout-message"
            rows="3"
            required
            placeholder="Why are you checking out this file?"
          ></textarea>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" id="checkout-cancel">
            Cancel
          </button>
          <button type="submit" class="btn btn-checkout">Checkout</button>
        </div>
      </form>
    </div>
  </div>
</div>

<div id="checkin-modal" class="modal-overlay hidden">
  <div
    class="modal-content"
    role="dialog"
    aria-modal="true"
    aria-labelledby="checkin-title"
  >
    <div class="modal-header">
      <h3 id="checkin-title">Checkin File</h3>
      <button class="modal-close" aria-label="Close">&times;</button>
    </div>
    <div class="modal-body">
      <p>File: <strong id="checkin-filename"></strong></p>
      <form id="checkin-form">
        <div class="form-group">
          <label for="checkin-user"
            >Your Name (must match checkout user):</label
          >
          <input
            type="text"
            id="checkin-user"
            required
            placeholder="Enter your name"
          />
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" id="checkin-cancel">
            Cancel
          </button>
          <button type="submit" class="btn btn-checkin">Checkin</button>
        </div>
      </form>
    </div>
  </div>
</div>
```

- **Accessibility Note**: `role="dialog"` and `aria-modal="true"` tell screen readers that this is a modal dialog that traps focus, which is crucial for users who navigate with keyboards.

### CSS for the Modals

Add this CSS to `backend/static/css/style.css`.

```css
/* ADD THIS to style.css */

/* ============================================ */
/* MODAL DIALOGS                              */
/* ============================================ */

.modal-overlay {
  position: fixed; /* Position relative to the viewport. Stays in place when scrolling. */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0; /* Cover the entire screen. */
  background: rgba(0, 0, 0, 0.6); /* Semi-transparent black background. */
  display: flex; /* Use flexbox to easily center the modal content. */
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Ensure it's on top of all other content. */
  backdrop-filter: blur(2px); /* "Frosted glass" effect for modern browsers. */
}

.modal-overlay.hidden {
  display: none; /* Hide the modal by default. */
}

.modal-content {
  background: white;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease-out; /* Add a subtle entry animation. */
}

/* Defines the keyframes for our entry animation. */
@keyframes modalSlideIn {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
}

.modal-close {
  background: none;
  border: none;
  font-size: 2rem;
  color: #999;
  cursor: pointer;
  transition: color 0.2s;
}
.modal-close:hover {
  color: #333;
}

.modal-body {
  padding: 1.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end; /* Align buttons to the right. */
  margin-top: 1.5rem;
}

/* Button variants */
.btn {
  /* Add transition to base button class */
  transition: all 0.3s ease;
}
.btn-secondary {
  background: #6c757d;
}
.btn-secondary:hover {
  background: #5a6268;
}

/* Form styles (if not already present) */
.form-group {
  margin-bottom: 1.5rem;
}
label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}
input[type="text"],
textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.3s ease;
}
textarea {
  resize: vertical;
}
input[type="text"]:focus,
textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}
```

### JavaScript `ModalManager` Class

To make our modals reusable and keep the logic clean (SRP), we'll create a JavaScript class to manage them.

**Add this to `app.js`:**

```javascript
// ADD THIS CLASS to app.js

class ModalManager {
  constructor(modalId) {
    this.modal = document.getElementById(modalId);
    // Add event listeners to close the modal.
    this.setupCloseHandlers();
  }

  setupCloseHandlers() {
    // 1. Close via the 'X' button.
    const closeBtn = this.modal.querySelector(".modal-close");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => this.close());
    }

    // 2. Close by clicking on the background overlay.
    this.modal.addEventListener("click", (e) => {
      if (e.target === this.modal) {
        this.close();
      }
    });

    // 3. Close by pressing the 'Escape' key.
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !this.modal.classList.contains("hidden")) {
        this.close();
      }
    });
  }

  open() {
    this.modal.classList.remove("hidden");
    // For accessibility, automatically focus the first input field.
    const firstInput = this.modal.querySelector("input, textarea");
    if (firstInput) {
      // Use a small timeout to ensure the element is visible before focusing.
      setTimeout(() => firstInput.focus(), 50);
    }
  }

  close() {
    this.modal.classList.add("hidden");
  }
}

// Create instances for each modal we have.
const checkoutModal = new ModalManager("checkout-modal");
const checkinModal = new ModalManager("checkin-modal");
```

- **`this` and Arrow Functions**: We use arrow functions (`() => this.close()`) for event listeners. A regular `function() { ... }` would have its own `this` context (pointing to the button), causing `this.close()` to fail. Arrow functions inherit `this` from their parent scope (our `ModalManager` instance), so it works correctly.

---

## 4.3: Integrating Modals with Checkout/Checkin

Now, let's replace the `prompt()`-based handlers with our new modal system.

### Update JavaScript Handlers

**First, add a global variable** at the top of `app.js` to keep track of which file is being acted upon.

```javascript
// ADD this global variable at the top of app.js
let currentFilename = null;
```

**Next, replace your old `handleCheckout` and `handleCheckin` functions** with these new versions that open the modals.

```javascript
// REPLACE the old handleCheckout and handleCheckin functions in app.js

async function handleCheckout(filename) {
  console.log("Opening checkout modal for:", filename);
  currentFilename = filename; // Store the filename for the form submission

  document.getElementById("checkout-filename").textContent = filename;
  document.getElementById("checkout-form").reset(); // Clear previous input
  checkoutModal.open();
}

async function handleCheckin(filename) {
  console.log("Opening checkin modal for:", filename);
  currentFilename = filename;

  document.getElementById("checkin-filename").textContent = filename;
  document.getElementById("checkin-form").reset();
  checkinModal.open();
}
```

**Finally, add the form submission logic** inside your `DOMContentLoaded` listener. This separates opening the modal from handling the form data.

```javascript
// ADD this inside the 'DOMContentLoaded' event listener in app.js

// --- Modal Form Submission Handlers ---

document
  .getElementById("checkout-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault(); // Prevent page reload
    const user = document.getElementById("checkout-user").value;
    const message = document.getElementById("checkout-message").value;

    try {
      const response = await fetch("/api/files/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename: currentFilename, user, message }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail);

      showNotification("File checked out successfully!", "success");
      checkoutModal.close();
      loadFiles(); // Refresh the list
    } catch (error) {
      showNotification(`Error: ${error.message}`, "error");
    }
  });

document.getElementById("checkout-cancel").addEventListener("click", () => {
  checkoutModal.close();
});

document
  .getElementById("checkin-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const user = document.getElementById("checkin-user").value;

    try {
      const response = await fetch("/api/files/checkin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename: currentFilename, user }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail);

      showNotification("File checked in successfully!", "success");
      checkinModal.close();
      loadFiles();
    } catch (error) {
      showNotification(`Error: ${error.message}`, "error");
    }
  });

document.getElementById("checkin-cancel").addEventListener("click", () => {
  checkinModal.close();
});
```

### Toast Notifications

The code above uses `showNotification`. Let's add that helper function and its CSS for a better user experience than `alert()`.

**Add this to `app.js`:**

```javascript
// ADD this notification function to app.js
function showNotification(message, type = "info") {
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.classList.add("show"), 10);
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
```

**Add this to `style.css`:**

```css
/* ADD these toast styles to style.css */
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 1rem 1.5rem;
  background: white;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateX(calc(100% + 20px));
  transition: transform 0.3s ease;
  z-index: 2000;
  font-weight: 500;
  border-left: 4px solid #667eea;
}
.toast.show {
  transform: translateX(0);
}
.toast-success {
  border-color: #28a745;
}
.toast-error {
  border-color: #dc3545;
}
```

Now, try checking out a file. You should see a smooth, non-blocking modal and a clean notification toast on success or failure.

---

## 4.4: Search, Filter, and Sort

A long list of files isn't very user-friendly. Let's add controls to find files easily.

### Add UI Controls to `index.html`

Update the `file-list-section` in `index.html`.

```html
<section id="file-list-section">
  <div
    style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;"
  >
    <h2>Available Files</h2>
    <button id="refresh-btn" class="btn">Refresh</button>
  </div>

  <div class="controls-row">
    <div class="search-box">
      <input
        type="text"
        id="search-input"
        placeholder="Search files..."
        class="search-input"
      />
    </div>
    <div class="filter-group">
      <label for="status-filter">Status:</label>
      <select id="status-filter" class="filter-select">
        <option value="all">All</option>
        <option value="available">Available</option>
        <option value="checked_out">Checked Out</option>
      </select>
    </div>
    <div class="filter-group">
      <label for="sort-select">Sort by:</label>
      <select id="sort-select" class="filter-select">
        <option value="name-asc">Name (A-Z)</option>
        <option value="name-desc">Name (Z-A)</option>
      </select>
    </div>
  </div>

  <div id="loading-indicator" class="loading hidden">
    <div class="spinner"></div>
    <p>Loading files...</p>
  </div>
  <div id="file-list"></div>
</section>
```

### Add Control Styles to `style.css`

```css
/* ADD these control styles to style.css */
.controls-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.search-box {
  flex: 1;
  min-width: 200px;
}
.search-input,
.filter-select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  background: white;
}
.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.filter-group label {
  margin: 0;
  font-weight: 500;
  color: #666;
}
.search-input:focus,
.filter-select:focus {
  outline: none;
  border-color: #667eea;
}
```

### Update JavaScript for State Management

We'll store the full list of files in a global variable and apply filters on the client-side.

**Add these variables and functions to `app.js`:**

```javascript
// ADD these state variables at the top of app.js
let allFiles = [];
let searchTerm = "";
let statusFilter = "all";
let sortBy = "name-asc";

// REPLACE your existing loadFiles function
async function loadFiles() {
  const loadingEl = document.getElementById("loading-indicator");
  const fileListEl = document.getElementById("file-list");
  loadingEl.classList.remove("hidden");
  fileListEl.classList.add("hidden");

  try {
    const response = await fetch("/api/files");
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    allFiles = data.files; // Store the master list
    displayFilteredAndSortedFiles(); // Render based on current filters
  } catch (error) {
    console.error("Error loading files:", error);
    displayError("Failed to load files.");
  } finally {
    loadingEl.classList.add("hidden");
    fileListEl.classList.remove("hidden");
  }
}

// ADD this new function to app.js
function displayFilteredAndSortedFiles() {
  // 1. Filter by search term and status
  let processedFiles = allFiles.filter((file) => {
    const matchesSearch = file.name
      .toLowerCase()
      .includes(searchTerm.toLowerCase());
    const matchesStatus =
      statusFilter === "all" || file.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  // 2. Sort the filtered results
  const [field, direction] = sortBy.split("-");
  processedFiles.sort((a, b) => {
    const valA = a[field].toLowerCase();
    const valB = b[field].toLowerCase();
    if (valA < valB) return direction === "asc" ? -1 : 1;
    if (valA > valB) return direction === "asc" ? 1 : -1;
    return 0;
  });

  // 3. Render the final list
  displayFiles(processedFiles);
}

// ADD these event listeners to the DOMContentLoaded callback
document.getElementById("search-input").addEventListener("input", (e) => {
  searchTerm = e.target.value;
  displayFilteredAndSortedFiles();
});
document.getElementById("status-filter").addEventListener("change", (e) => {
  statusFilter = e.target.value;
  displayFilteredAndSortedFiles();
});
document.getElementById("sort-select").addEventListener("change", (e) => {
  sortBy = e.target.value;
  displayFilteredAndSortedFiles();
});

// REMOVE the call to displayFiles from loadFiles. It's now handled by displayFilteredAndSortedFiles.
// The `displayFiles` function itself remains, but is now just for rendering.
```

Now your frontend has fast, client-side filtering and sorting. Try typing in the search box or changing the dropdowns\!

---

## Stage 4 Complete - A Professional Frontend\!

You've transformed the simple UI into a polished, responsive, and interactive application using professional patterns.

### What You Built

- Custom, reusable modal components for user input.
- Non-blocking "toast" notifications for user feedback.
- Client-side search, filtering, and sorting for a fast user experience.
- Loading indicators to provide feedback during network requests.
- A more robust and maintainable JavaScript structure.

### Final File Snapshots

You can find the full, final versions of `index.html`, `style.css`, and `app.js` in the previous expansions. Ensure your files match those to be ready for the next stage.

### What's Next?

In **Stage 5**, we'll secure the application with a complete **Authentication and Authorization** system. Users will need to log in, and we'll introduce roles to control who can perform certain actions.

Understood. Let's proceed with Stage 5.

Here is the fully expanded and unified tutorial for adding authentication and authorization to your application. This stage is critical for security and introduces concepts like password hashing, JSON Web Tokens (JWTs), and role-based access control.

---

# Stage 5: Authentication & Authorization - Securing Your Application (Expanded & Unified)

## Introduction: The Goal of This Stage

Your application is functional, but it's completely open. There's no login, no concept of users, and no way to control who can perform sensitive actions. This stage transforms your PDM system from an open tool into a secure, multi-user application.

By the end of this stage, you will:

- Understand the crucial difference between **Authentication** (who you are) and **Authorization** (what you can do).
- Implement secure password hashing with `bcrypt` to never store plain-text passwords.
- Create and validate **JSON Web Tokens (JWTs)** for stateless authentication.
- Build a complete login/logout system.
- Protect API endpoints so they can only be accessed by logged-in users.
- Implement a basic role system (`admin` vs. `user`) for authorization.

---

### **🧠 Foundational Concepts: A Deeper Look**

- **Time Investment:** 6-8 hours. Security is detailed and vital to get right.
- **Historical Insight**: Modern web authentication builds on decades of computer science. The concept of password-based access dates back to the 1960s. The token-based flow we're building was standardized by **OAuth 2.0** (2012), and the **JWT** format (2010) was created as a simpler, more compact alternative to older standards like SAML.
- **Software Engineering Principle: Zero Trust**. This is a modern security model that assumes no user or service is trusted by default. Every single request to a protected resource must be verified. We will implement this by checking the JWT on every API call.
- **Key Concept: The Auth Spectrum**. There are many ways to handle authentication, from simple to enterprise-grade.
  - **Internal JWT (This Tutorial)**: Simple, self-contained. Great for internal tools and learning.
  - **Third-Party Providers (e.g., Firebase Auth, Auth0)**: Outsources the complexity. Handles social logins (Google, Facebook), multi-factor authentication (MFA), and password resets for you. Excellent for getting to market quickly.
  - **Enterprise SSO (e.g., Okta, SAML)**: For large companies needing to integrate with corporate directories.

---

## 5.1: Authentication vs. Authorization

These two terms are often confused, but they are distinct and sequential steps in securing an application.

1.  **Authentication (AuthN)**: Proving you are who you say you are.

    - **Question:** "Who are you?"
    - **Mechanism:** Username + Password, Biometrics, API Key.
    - **PDM Example:** The user provides "admin" and "admin123" to the `/login` endpoint. The system verifies this and says, "Yes, you are the admin user."

2.  **Authorization (AuthZ)**: Determining if you have permission to do something.

    - **Question:** "Are you _allowed_ to do that?"
    - **Mechanism:** Role checks, permission lists, ownership rules.
    - **PDM Example:** An authenticated user tries to delete a file. The system checks their role and says, "No, only users with the 'admin' role can delete files."

**You must always authenticate before you can authorize.**

| PDM Action                 | Authentication Check             | Authorization Check                                |
| :------------------------- | :------------------------------- | :------------------------------------------------- |
| **Viewing the login page** | None                             | None (it's public)                                 |
| **Logging In**             | Yes (Verifies username/password) | None (The goal is to get authenticated)            |
| **Viewing the file list**  | Yes (Is this a valid user?)      | Yes (Does this user have `read:files` permission?) |
| **Deleting a file**        | Yes (Is this a valid user?)      | Yes (Does this user have the `admin` role?)        |

---

## 5.2: Password Security: Hashing

**The Golden Rule of Security: NEVER, EVER STORE PASSWORDS IN PLAIN TEXT.**

If your database is ever breached, attackers would have the passwords for all your users. Since many people reuse passwords, this could compromise their email, banking, and other accounts.

### The Correct Way: Hashing with Salt

We use a one-way cryptographic function called a **hash**.

`password` -\> **[HASH FUNCTION]** -\> `a long, irreversible string of characters`

Even better, we use a **salted hash**. A "salt" is a random string added to the password before hashing.

| Attack                   | Why Hashing with Salt Wins                                                                                                                             |
| :----------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Database Leak**        | Attacker gets hashes, not passwords. They are practically impossible to reverse.                                                                       |
| **Rainbow Table Attack** | A pre-computed table of common password hashes is useless because every user's salt is different, making their hash unique even for the same password. |
| **Brute Force Attack**   | We use an algorithm like **bcrypt** that is intentionally slow, making it computationally expensive for an attacker to guess passwords.                |

#### 🏋️ Practice Exercise: The Hash Playground

Create a file `backend/hash_playground.py` to see this in action. First, install the necessary library: `pip install "passlib[bcrypt]"`.

```python
# backend/hash_playground.py

from passlib.context import CryptContext

# 1. Create a context, specifying the hashing algorithm.
# We use bcrypt, the industry standard for password hashing.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "MySecurePassword123"

# 2. Hash the password. Passlib handles generating a random salt automatically.
hash1 = pwd_context.hash(password)
hash2 = pwd_context.hash(password)

print(f"Password: {password}")
print(f"Hash 1:   {hash1}")
print(f"Hash 2:   {hash2}")
print(f"Hashes are different? {hash1 != hash2}\n") # They will be, because of the salt!

# 3. Verify the password against a hash.
print(f"Verifying correct password against Hash 1: {pwd_context.verify(password, hash1)}")
print(f"Verifying incorrect password against Hash 1: {pwd_context.verify('WrongPassword', hash1)}")
```

Run it: `python hash_playground.py`. You'll see that the same password produces two different hashes but both verify correctly. This is the magic of salted hashing.

---

## 5.3: Installing Dependencies

Let's install the libraries for hashing and for creating/validating JWTs.

```bash
pip install "passlib[bcrypt]" "python-jose[cryptography]"
pip freeze > requirements.txt
```

- `passlib[bcrypt]`: The password hashing library with the `bcrypt` algorithm.
- `python-jose[cryptography]`: A library for handling JWTs and other related standards. `[cryptography]` pulls in a robust, low-level crypto library.

---

## 5.4: User Data Structure & Management

We'll replace the hardcoded user data with a JSON file, which will act as our user database.

### Create `users.json`

Create a file at `backend/users.json`. For now, it can be an empty object. Our code will populate it on first run.

```json
{}
```

### Create User Management Functions

Add the following code to `backend/main.py`. This block of code handles everything related to users: loading, saving, creating defaults, and authenticating.

```python
# ADD these imports at the top of main.py
from passlib.context import CryptContext
import json

# --- Path & Hashing Configuration ---
USERS_FILE = BASE_DIR / 'users.json'
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- User Management Helper Functions ---

def create_default_users():
    """Creates default users if users.json is empty."""
    users = {
        "admin": {
            "username": "admin",
            "password_hash": pwd_context.hash("admin123"), # In a real app, use a stronger default!
            "full_name": "Administrator",
            "role": "admin"
        },
        "john": {
            "username": "john",
            "password_hash": pwd_context.hash("password123"),
            "full_name": "John Doe",
            "role": "user"
        }
    }
    save_users(users)
    logger.info("Created default users: 'admin' and 'john'")

def load_users() -> dict:
    """Loads users from users.json."""
    if not USERS_FILE.exists():
        create_default_users()

    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users: dict):
    """Saves the user dictionary to users.json."""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str) -> dict | None:
    """Retrieves a single user by username."""
    users = load_users()
    return users.get(username)

def authenticate_user(username: str, password: str) -> dict | None:
    """Authenticates a user. Returns user dict on success, None on failure."""
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return user
```

---

## 5.5: JSON Web Tokens (JWT) - Deep Dive

A **JWT** is our digital passport. After a user logs in successfully, we give them a JWT. They must present this token on all future requests to prove who they are.

A JWT has three parts, separated by dots: `header.payload.signature`

**`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huIiwicm9sZSI6InVzZXIiLCJleHAiOjE3NjIyNzgwMDB9.jW8_2l2-w3jY...`**

1.  **Header (Base64 Encoded)**: Metadata about the token, like the signing algorithm.

    ```json
    { "alg": "HS256", "typ": "JWT" }
    ```

2.  **Payload (Base64 Encoded)**: The actual data, or "claims." This is where we put the user's information.

    ```json
    {
      "sub": "john", // "Subject" - a standard claim for the user's ID
      "role": "user", // A custom claim we added
      "exp": 1762278000 // "Expiration Time" - a standard claim
    }
    ```

    > **Security Warning**: The payload is just Base64 encoded, **not encrypted**. Anyone can read it. Never put sensitive information in a JWT payload.

3.  **Signature**: This is the security part. It's created by hashing the header, the payload, and a secret key that only the server knows. When the server receives a token, it re-calculates the signature. If it matches, the server knows the token is authentic and hasn't been tampered with.

### JWT Functions in `main.py`

Add the following JWT configuration and helper functions to `main.py`.

```python
# ADD these imports and code blocks to main.py

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional

# --- JWT Configuration ---
SECRET_KEY = "your-super-secret-key-that-should-be-in-an-env-file" # CHANGE THIS!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# --- Pydantic Models for Auth ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    full_name: str
    role: str

# --- JWT Helper Functions ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

---

## 5.6: The Login Endpoint & Protected Routes

### The Login Endpoint

This endpoint will take a username and password, authenticate the user, and return a JWT.

```python
# ADD this endpoint to main.py

@app.post("/api/auth/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

- **`OAuth2PasswordRequestForm`**: This is a special FastAPI dependency that expects the login data to come as form data (`application/x-www-form-urlencoded`), not JSON, as required by the OAuth2 standard.

### The `get_current_user` Dependency

This is the most important part. It's a dependency that other endpoints will use to get the currently authenticated user. It will decode the token, validate it, and fetch the user.

```python
# ADD this dependency function to main.py

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user_dict = get_user(username=token_data.username)
    if user_dict is None:
        raise credentials_exception

    return User(**user_dict)
```

### Protecting an Endpoint

Now, protecting an endpoint is as simple as adding a dependency.

**Update your `/api/files` endpoint:**

```python
# UPDATE the /api/files endpoint in main.py

@app.get("/api/files")
def get_files(current_user: User = Depends(get_current_user)):
    # If the request gets here, 'current_user' is a valid, authenticated user.
    # If the token was missing or invalid, FastAPI would have already
    # returned a 401 Unauthorized error.
    logger.info(f"User '{current_user.username}' is requesting the file list.")

    # ... rest of the function remains the same ...
    locks = load_locks()
    files = []
    # ... etc ...
    return {"files": files}
```

---

## 5.7: Frontend Login Page and Authentication Flow

### Create the Login Page

Create `backend/static/login.html` and a corresponding `backend/static/js/login.js`. These are separate from the main application. Also add an endpoint to serve this page.

**Add to `main.py`:**

```python
@app.get("/login", response_class=FileResponse)
async def serve_login_page():
    return "static/login.html"
```

**`backend/static/login.html`:**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PDM - Login</title>
    <link rel="stylesheet" href="/static/css/style.css" />
  </head>
  <body class="login-page">
    <div class="login-container">
      <div class="login-card">
        <h1>PDM System</h1>
        <p class="subtitle">Please log in to continue</p>
        <form id="login-form">
          <div class="form-group">
            <label for="username">Username</label>
            <input type="text" id="username" required autofocus />
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" required />
          </div>
          <button type="submit" class="btn btn-primary btn-block">
            Log In
          </button>
          <div id="login-error" class="error-message hidden"></div>
        </form>
        <div class="login-info">
          <p><strong>Test Accounts:</strong></p>
          <p>Admin: <code>admin</code> / <code>admin123</code></p>
          <p>User: <code>john</code> / <code>password123</code></p>
        </div>
      </div>
    </div>
    <script src="/static/js/login.js"></script>
  </body>
</html>
```

**`backend/static/js/login.js`:**

```javascript
document.addEventListener("DOMContentLoaded", () => {
  // If user is already logged in, redirect them
  if (localStorage.getItem("access_token")) {
    window.location.href = "/";
    return;
  }

  const loginForm = document.getElementById("login-form");
  const errorDiv = document.getElementById("login-error");

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorDiv.classList.add("hidden");

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // OAuth2 requires form data, not JSON
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Login failed");
      }

      // On success, store the token and redirect
      localStorage.setItem("access_token", data.access_token);
      window.location.href = "/";
    } catch (error) {
      errorDiv.textContent = error.message;
      errorDiv.classList.remove("hidden");
    }
  });
});
```

### Protecting the Main App (`index.html`)

Add an "auth guard" script to the top of `backend/static/index.html` inside the `<head>` tag. This runs before anything else and redirects to the login page if no token is found.

```html
<script>
  (function () {
    const token = localStorage.getItem("access_token");
    if (!token) {
      window.location.href = "/login";
    }
  })();
</script>
```

### Sending the Token from `app.js`

Update all `fetch` calls in `app.js` to include the token in the `Authorization` header.

```javascript
// Example update for loadFiles in app.js
async function loadFiles() {
  // ...
  const token = localStorage.getItem("access_token");
  const response = await fetch("/api/files", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  // ...
}
```

You must add this header to **every** request to a protected endpoint.

### Logout Functionality

Add a logout button to `index.html` and a handler to `app.js` to clear `localStorage` and redirect.

**`index.html` (in the `<header>`):**

```html
<button id="logout-btn" class="btn btn-secondary">Logout</button>
```

**`app.js` (in the `DOMContentLoaded` listener):**

```javascript
document.getElementById("logout-btn").addEventListener("click", () => {
  localStorage.removeItem("access_token");
  window.location.href = "/login";
});
```

---

## Stage 5 Complete - Your App is Secure\!

You now have a complete authentication system. Unauthenticated users are redirected to a login page, and authenticated users are issued a JWT that is used to access protected API endpoints.

### Verification Checklist

- [ ] Attempting to access `/` without logging in redirects you to `/login`.
- [ ] Logging in with correct credentials stores a token in `localStorage` and redirects you to `/`.
- [ ] The file list now loads successfully.
- [ ] Logging out clears the token and redirects you to `/login`.
- [ ] In DevTools, you can see the `Authorization: Bearer ...` header being sent with API requests.

### What's Next?

Your app is authenticated, but not yet authorized. In **Stage 6**, we will use the `role` claim in our JWT to implement **Role-Based Access Control (RBAC)**, ensuring that only admins can perform sensitive actions like deleting files.

Let's build on our secure application by adding granular permissions.

Here is the fully expanded and unified tutorial for **Stage 6**. This stage introduces **Authorization** by implementing a Role-Based Access Control (RBAC) system. We'll define different user roles and control what each role is allowed to do, including creating an admin-only area.

---

# Stage 6: Role-Based Access Control (RBAC) - Authorization Deep Dive (Expanded & Unified)

## Introduction: The Goal of This Stage

You have **Authentication** (AuthN), which answers "Who are you?". Now it's time for **Authorization** (AuthZ), which answers "What are you allowed to do?". A regular user shouldn't be able to delete files, and an admin needs the power to manage the system.

In this stage, you'll implement a robust RBAC system to enforce these permissions.

By the end of this stage, you will:

- Understand the theory behind RBAC and other authorization models.
- Create flexible, reusable dependencies in FastAPI to enforce role requirements.
- Build admin-only endpoints for sensitive operations like deleting files.
- Implement ownership rules (e.g., only the user who locked a file can check it in).
- Create a role-aware frontend where the UI adapts to the user's permissions.
- Implement a detailed audit log to track all sensitive actions for compliance and security.

---

### **🧠 Foundational Concepts: A Deeper Look**

- **Time Investment:** 5-7 hours.
- **Historical Insight**: RBAC was formalized by the **NIST (National Institute of Standards and Technology)** in 1992 as a way to simplify the messy permission systems of the time (like Access Control Lists, or ACLs). It's a proven model that's the foundation for most modern application security.
- **Software Engineering Principle: Principle of Least Privilege**. This is the core idea of this stage. Every user should have the _minimum_ set of permissions required to perform their job, and nothing more. A regular user doesn't need delete permissions, so they don't get them. This drastically limits the potential damage if a user's account is compromised.
- **Design Pattern: Decorator Factory**. We will create a function that _generates_ our authorization dependencies. This is a powerful pattern using a higher-order function that allows us to create decorators like `require_admin` or `require_editor` from a single, reusable piece of code.
- **Key Concept: Expanding Roles**. While we'll start with `admin` and `user`, real-world systems often have more granular roles. A good RBAC system is extensible.
  | Role | Permissions | Best Practice |
  | :--- | :--- | :--- |
  | **Admin** | Full control: delete files, manage users, override locks. | Actions should be heavily audited. Often requires Multi-Factor Authentication (MFA). |
  | **User** | Standard access: checkout/checkin files, view history. | Cannot modify files locked by others. |
  | **Editor** | A more privileged user who can edit file metadata. | |
  | **Viewer** | Read-only access. Cannot check out or modify anything. | Ideal for auditors or managers who need to see status but not change it. |

---

## 6.1: Authorization Theory - The Access Control Matrix

At its core, authorization can be modeled as a matrix that maps subjects (users/roles) to objects (resources) and their permitted actions.

| Subject \\ Resource | File `PN1001.mcam`         | Admin Panel | Audit Log |
| :------------------ | :------------------------- | :---------- | :-------- |
| **admin (Role)**    | `READ`, `WRITE`, `DELETE`  | `ACCESS`    | `READ`    |
| **user (Role)**     | `READ`, `WRITE` (if owner) | `DENY`      | `DENY`    |
| **viewer (Role)**   | `READ`                     | `DENY`      | `READ`    |

RBAC simplifies this by grouping users into roles. Instead of managing permissions for thousands of users, you manage them for a handful of roles.

### RBAC vs. Other Models

| Model    | How It Works                                                   | Pro                               | Con                                  | PDM Fit                                            |
| :------- | :------------------------------------------------------------- | :-------------------------------- | :----------------------------------- | :------------------------------------------------- |
| **RBAC** | Users get roles, roles get permissions.                        | Simple to manage and scales well. | Can be too static for complex rules. | **Perfect for our core needs** (admin vs. user).   |
| **ACL**  | Each file has a list of who can access it.                     | Very granular control.            | A management nightmare at scale.     | Impractical for thousands of files.                |
| **ABAC** | Rules based on attributes (e.g., role, time of day, location). | Extremely flexible and dynamic.   | Complex to implement and debug.      | We'll use a simple form of this for **ownership**. |

---

## 6.2: Implementing Role-Based Dependencies in FastAPI

We need a way to protect endpoints so only users with specific roles can access them. We'll create a "dependency factory" for this.

### Create the `require_role` Factory

Add this powerful helper function to `backend/main.py`. It's a function that creates and returns _another_ function, which will be our dependency.

```python
# ADD this to main.py (along with `from typing import List`)

# --- Role-Based Dependencies ---

def require_role(allowed_roles: List[str]):
    """
    This is a dependency factory. It returns a new dependency function
    that checks if the current user has one of the allowed roles.
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            logger.warning(
                f"Access denied for user '{current_user.username}' with role '{current_user.role}'. "
                f"Required roles: {allowed_roles}"
            )
            # 403 Forbidden is the correct code for an authenticated user
            # who lacks the necessary permissions.
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action."
            )
        return current_user

    return role_checker

# --- Convenience Dependencies ---
# We can now create specific role dependencies for easy reuse.
require_admin = require_role(["admin"])
require_any_user = require_role(["admin", "user"]) # Any authenticated user will pass.
```

**Why this pattern?** It's incredibly reusable and follows the **DRY (Don't Repeat Yourself)** principle. Instead of writing separate functions to check for "admin", "editor", etc., we have one factory that can generate any role check we need.

---

## 6.3: Admin-Only Delete Endpoint

Now, let's use our new `require_admin` dependency to create a sensitive endpoint that only administrators can access.

### Implement File Deletion

Add this new endpoint to `main.py`.

```python
# ADD this new endpoint to main.py

@app.delete("/api/admin/files/{filename}")
def delete_file(
    filename: str,
    current_user: User = Depends(require_admin) # <-- The magic is here!
):
    """
    Delete a file from the repository. This is a destructive, admin-only action.
    """
    logger.warning(
        f"ADMIN ACTION: User '{current_user.username}' is requesting to DELETE file '{filename}'."
    )

    file_path = REPO_PATH / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    # Admin Override: Admins can delete a file even if it's locked.
    locks = load_locks()
    was_locked = filename in locks
    if was_locked:
        logger.warning(f"Admin is deleting a file that was locked by '{locks[filename]['user']}'.")
        del locks[filename]
        save_locks(locks)

    try:
        os.remove(file_path)
        logger.info(f"File '{filename}' permanently deleted by admin '{current_user.username}'.")

        # We will create log_audit_event in the next section.
        # log_audit_event(user=current_user.username, action="DELETE_FILE", target=filename)

        return {"success": True, "message": f"File '{filename}' deleted."}
    except Exception as e:
        logger.error(f"Error during file deletion: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete file.")
```

**How it works**: The `Depends(require_admin)` tells FastAPI to run our `require_admin` dependency before executing the endpoint's code. If the user isn't an admin, `require_admin` raises a 403 error and the delete code is never even reached. This is **Defense in Depth**.

---

## 6.4: Ownership-Based Authorization (A Touch of ABAC)

Sometimes, a role isn't enough. For checking in a file, we need to know _who_ locked it. This is a form of **Attribute-Based Access Control (ABAC)**, where the "owner" is an attribute we check.

### Create an Ownership Checker

Let's refactor the ownership logic out of the `checkin` endpoint and into its own reusable function.

**Add this function to `main.py`:**

```python
# ADD this function to main.py

def check_file_ownership(filename: str, current_user: User):
    """
    Verifies that the current user owns the lock on the file.
    Admins are allowed to override.
    Raises HTTPException on failure.
    """
    locks = load_locks()
    if filename not in locks:
        raise HTTPException(status_code=400, detail="File is not checked out.")

    lock_owner = locks[filename]['user']

    # Allow if the user is the owner OR the user is an admin
    if current_user.username == lock_owner or current_user.role == 'admin':
        if current_user.username != lock_owner:
            logger.info(f"Admin '{current_user.username}' is overriding a lock by '{lock_owner}'.")
        return True

    # If we get here, the user is not the owner and not an admin
    logger.warning(f"AuthZ failed: User '{current_user.username}' tried to act on a file locked by '{lock_owner}'.")
    raise HTTPException(status_code=403, detail=f"You do not own the lock on this file. It is locked by '{lock_owner}'.")
```

### Update the `checkin_file` Endpoint

Now, replace your old `checkin_file` endpoint to use this cleaner, more explicit check.

```python
# REPLACE the old checkin_file endpoint in main.py

@app.post("/api/files/checkin")
def checkin_file(request: FileCheckinRequest, current_user: User = Depends(get_current_user)):
    logger.info(f"Checkin request: {request.user} -> {request.filename}")

    # Use our new authorization helper function. It will raise an error if not permitted.
    check_file_ownership(request.filename, current_user)

    locks = load_locks()
    del locks[request.filename]
    save_locks(locks)

    logger.info(f"File '{request.filename}' checked in successfully.")
    return {"success": True, "message": "File checked in successfully."}
```

---

## 6.5: Audit Logging

For compliance and security, we need an immutable record of sensitive actions. Who deleted a file? Who forced a check-in? An audit log answers these questions.

### Implement Audit Functions

**Create an empty `backend/audit_log.json` file:**

```json
[]
```

**Add these functions to `main.py`:**

```python
# ADD these imports and functions to main.py
import uuid

AUDIT_LOG_FILE = BASE_DIR / 'audit_log.json'

def log_audit_event(user: str, action: str, target: str, details: dict = None):
    """Appends a structured event to the audit log."""
    event = {
        "id": str(uuid.uuid4()), # A unique ID for every event
        "timestamp": datetime.now(timezone.utc).isoformat(), # Standard, sortable timestamp
        "user": user,
        "action": action,
        "target": target,
        "details": details or {}
    }

    try:
        if AUDIT_LOG_FILE.exists():
            with open(AUDIT_LOG_FILE, 'r+') as f:
                log_data = json.load(f)
                log_data.append(event)
                f.seek(0)
                json.dump(log_data, f, indent=2)
        else:
            with open(AUDIT_LOG_FILE, 'w') as f:
                json.dump([event], f, indent=2)

        logger.info(f"AUDIT: User '{user}' performed action '{action}' on target '{target}'.")
    except Exception as e:
        # Critical: An audit log failure should not crash the main application logic.
        logger.error(f"CRITICAL: Failed to write to audit log! Error: {e}")

@app.get("/api/admin/audit-log", response_model=List[dict])
def get_audit_log_endpoint(current_user: User = Depends(require_admin)):
    """Admin-only endpoint to retrieve the audit log."""
    logger.info(f"Admin '{current_user.username}' accessed the audit log.")
    if not AUDIT_LOG_FILE.exists():
        return []
    with open(AUDIT_LOG_FILE, 'r') as f:
        logs = json.load(f)
        return sorted(logs, key=lambda x: x['timestamp'], reverse=True) # Show most recent first
```

Now, go back and **uncomment** or **add** the `log_audit_event(...)` calls in your `delete_file` and `checkin_file` endpoints.

---

## 6.6: Role-Aware Frontend

The server now enforces permissions, but the UI should adapt to the user's role for a better experience. An admin should see a "Delete" button, but a regular user should not.

### Storing User Role in the Frontend

First, we need to get the user's role from the JWT after they log in.

**Add a JWT parsing function to `login.js` and `app.js`:**

```javascript
// ADD this helper function to both login.js and app.js

function parseJWT(token) {
  try {
    return JSON.parse(atob(token.split(".")[1]));
  } catch (e) {
    return null;
  }
}
```

> **Security Note**: This function **decodes** the JWT payload; it does **not verify** it. This is safe because we're only using it for UI hints. The server _always_ verifies the token's signature, which is our source of truth.

**Update `login.js`** to store the role in `localStorage`:

```javascript
// In login.js, inside the successful fetch response block:
const data = await response.json();
localStorage.setItem("access_token", data.access_token);

const payload = parseJWT(data.access_token);
if (payload) {
  localStorage.setItem("username", payload.sub);
  localStorage.setItem("user_role", payload.role);
}

window.location.href = "/";
```

### Conditionally Rendering UI Elements

Now, `app.js` can check the role and decide whether to show admin-only buttons.

**Update `createFileElement` in `app.js`:**

```javascript
// In app.js, update the createFileElement function

function createFileElement(file) {
  // ... (existing code for div, infoDiv, actionsDiv)

  const userRole = localStorage.getItem("user_role");
  const currentUser = localStorage.getItem("username");

  if (file.status === "available") {
    const checkoutBtn = document.createElement("button");
    // ... (existing checkout button code)
    actionsDiv.appendChild(checkoutBtn);
  } else {
    // Show checkin button only if user owns the lock OR is an admin
    if (file.locked_by === currentUser || userRole === "admin") {
      const checkinBtn = document.createElement("button");
      // ... (existing checkin button code)
      actionsDiv.appendChild(checkinBtn);
    }
  }

  // NEW: Add a delete button, but only for admins
  if (userRole === "admin") {
    const deleteBtn = document.createElement("button");
    deleteBtn.className = "btn btn-danger"; // We'll style this
    deleteBtn.textContent = "Delete";
    deleteBtn.onclick = () => handleDelete(file.name);
    actionsDiv.appendChild(deleteBtn);
  }

  // ... (rest of the function)
}
```

You'll also need to implement the `handleDelete` function in `app.js` and add a `.btn-danger` style in `style.css`.

---

## Stage 6 Complete - Full Access Control\!

Your application now has a robust authorization layer. Actions are controlled by roles, ownership is enforced, and all sensitive operations are logged.

### Verification Checklist

- [ ] Regular users see "Checkout" and "Checkin" (for their own files) buttons, but no "Delete" button.
- [ ] Logging in as `admin` reveals the "Delete" button for all files and the "Checkin" button for all locked files.
- [ ] An admin can successfully delete a file.
- [ ] An admin can successfully check in a file locked by another user.
- [ ] Deleting a file or forcing a check-in creates an entry in `audit_log.json`.
- [ ] Attempting to access an admin endpoint (like `/api/admin/audit-log`) as a regular user results in a 403 Forbidden error.

### What's Next?

In **Stage 7**, we will replace our simple JSON file database with a real **Git repository**. Every change to a file's lock status will become a Git commit, giving us a complete, auditable version history for our entire system.

Of course. Let's integrate a full version control system into our application.

Here is the fully expanded and unified tutorial for **Stage 7**. This is a major step that replaces our simple, fragile JSON files with a robust Git repository. Every change to your application's state will now be an auditable, versioned commit. This stage is structured in two parts as you requested: a standalone "Git Playground" to master the concepts, followed by the integration into our PDM app.

---

# Stage 7: Git Integration - Real Version Control (Expanded & Unified)

## Introduction: The Goal of This Stage

Your app stores state in JSON files, but this approach has no history. If a file is corrupted or a bad change is made, there's no easy way to roll back. We need a more robust system for tracking changes over time.

In this stage, you'll replace direct file writes with **Git commits**. Your application will essentially use a Git repository as its database, providing a complete, immutable history of every action.

By the end of this stage, you will:

- Understand Git's internal object model (blobs, trees, commits).
- Turn every application state change into an atomic Git commit.
- Implement functions to view file history and diffs.
- Connect your application's local Git repo to a remote on GitLab for backup and collaboration.
- Master the concepts of push, pull, and handling remote changes.

---

### **🧠 Foundational Concepts: A Deeper Look**

- **Time Investment:** 6-8 hours.
- **Historical Insight**: Git was created in 2005 by Linus Torvalds to manage the Linux kernel source code. He was frustrated with existing centralized systems (like SVN) and designed Git to be **distributed**, meaning every developer has a full copy of the repository's history. This makes it incredibly fast and resilient.
- **Software Engineering Principle: Immutability**. A core concept in Git is that commits are immutable. You don't edit a commit; you create a _new_ commit that supersedes the old one. This creates a reliable, append-only ledger of changes, which is perfect for an audit trail.
- **Design Pattern: Repository Pattern**. We are literally implementing the Repository pattern using an actual Git repository. We'll create a layer of functions (`save_with_commit`, `get_history`) that abstract away the underlying Git commands.

---

## Part 1: Git Mastery Playground (Standalone)

Before integrating Git into our app, let's master the core concepts in an isolated environment. Create a new folder anywhere on your computer called `git-playground`, `cd` into it, and follow along.

### 1.1: Git Basics - The Three Trees

Git manages three "trees":

1.  **Working Directory**: The actual files you see and edit.
2.  **Staging Area (Index)**: A snapshot of files you've marked to be included in the _next_ commit.
3.  **Repository (`.git` directory)**: The permanent, immutable history of all your commits.

<!-- end list -->

```bash
# 1. Initialize an empty Git repository. This creates the hidden .git directory.
git init

# 2. Create a file in your Working Directory.
echo "# My Git Playground" > README.md

# 3. Check the status. Git sees a new, "untracked" file.
git status

# 4. Add the file to the Staging Area.
git add README.md

# 5. Check the status again. The file is now "staged for commit".
git status

# 6. Commit the staged changes to the Repository. This creates a permanent snapshot.
git commit -m "Initial commit: Add README file"

# 7. View the history.
git log
```

### 1.2: Branching and Merging

Branches allow you to work on new features without affecting the main line of development (`main`).

```bash
# 1. Create a new branch called 'feature/add-license'
git branch feature/add-license

# 2. Switch to the new branch.
git checkout feature/add-license
# (Or do both steps at once with `git checkout -b feature/add-license`)

# 3. Make a change on this branch.
echo "MIT License" > LICENSE

# 4. Stage and commit the change ON THE BRANCH.
git add LICENSE
git commit -m "FEAT: Add LICENSE file"

# 5. Switch back to the main branch. Notice the LICENSE file disappears!
git checkout main

# 6. Merge the feature branch into main. The LICENSE file reappears.
git merge feature/add-license

# 7. View the combined history.
git log --oneline --graph
```

### 1.3: Working with a Remote (GitLab/GitHub)

A **remote** is a version of your repository hosted on a server, like GitLab.

1.  Go to GitLab.com and create a new, blank project named `git-playground`.
2.  Copy the SSH URL it provides (e.g., `git@gitlab.com:your-username/git-playground.git`).

<!-- end list -->

```bash
# 1. Tell your local repo about the remote. 'origin' is the conventional name.
git remote add origin git@gitlab.com:your-username/git-playground.git

# 2. Push your main branch to the remote.
# The -u flag sets the upstream tracking reference for the branch.
git push -u origin main
```

Refresh your GitLab project page. Your files are now there\! This is your backup and the central point for collaboration.

---

## Part 2: Integrating Git into the PDM Application

Now, let's apply these concepts to our FastAPI app.

## 7.1: Installing GitPython

This library allows our Python code to execute Git commands.

```bash
pip install GitPython
pip freeze > requirements.txt
```

## 7.2: Initializing the Git Repository on Startup

We'll modify our application to use a dedicated `git_repo/` directory for all its data files (`locks.json`, `users.json`, etc.) and ensure this directory is a Git repository.

### Update Path Constants in `main.py`

First, find your path definitions at the top of `main.py` and change them to point to a new `git_repo` directory.

```python
# REPLACE your old path definitions with these

# --- Path Definitions ---
BASE_DIR = Path(__file__).resolve().parent
GIT_REPO_PATH = BASE_DIR / 'git_repo' # This will be the root of our Git repo

# All data files now live inside the Git repo
REPO_PATH = GIT_REPO_PATH / 'repo'
LOCKS_FILE = GIT_REPO_PATH / 'locks.json'
USERS_FILE = GIT_REPO_PATH / 'users.json'
AUDIT_LOG_FILE = GIT_REPO_PATH / 'audit_log.json'
```

### Create the `initialize_git_repo` Function

Add this function to `main.py`. It will run once when the application starts, setting up the Git repository if it doesn't already exist.

```python
# ADD these imports at the top of main.py
from git import Repo, Actor
from git.exc import GitCommandError

# ADD this new function to main.py
def initialize_git_repo():
    """
    Initializes the Git repository if it doesn't exist,
    including creating necessary files and making the first commit.
    """
    if GIT_REPO_PATH.exists() and (GIT_REPO_PATH / '.git').exists():
        logger.info("Git repository already exists. Loading it.")
        return Repo(GIT_REPO_PATH)

    logger.info(f"Creating new Git repository at {GIT_REPO_PATH}")
    GIT_REPO_PATH.mkdir(parents=True, exist_ok=True)
    repo = Repo.init(GIT_REPO_PATH)

    # Create initial files and directories
    (GIT_REPO_PATH / 'repo').mkdir(exist_ok=True)
    LOCKS_FILE.write_text('{}')
    USERS_FILE.write_text('{}') # Will be populated by create_default_users
    AUDIT_LOG_FILE.write_text('[]')

    # Create a .gitignore file
    (GIT_REPO_PATH / '.gitignore').write_text('*.pyc\n__pycache__/\n.DS_Store')

    # Stage and commit the initial files
    repo.index.add(['locks.json', 'users.json', 'audit_log.json', '.gitignore'])
    author = Actor("PDM System", "system@pdm.local")
    repo.index.commit("Initial repository setup", author=author, committer=author)

    logger.info("Git repository initialized successfully.")
    return repo

# --- Application Startup ---
# We need a global variable to hold our repo object
git_repo: Optional[Repo] = None

@app.on_event("startup")
def startup_event():
    """Code to run when the application starts up."""
    global git_repo
    git_repo = initialize_git_repo()
    create_default_users() # This will now write to users.json inside the git repo
```

- **What's Happening?** The `@app.on_event("startup")` decorator registers a function to run once, right after Uvicorn starts. This is the perfect place to initialize our Git repo and create our default users.

## 7.3: Replacing File Writes with Atomic Commits

Now for the core change: every time we save a file, we'll make a Git commit. This makes every state change an atomic, auditable transaction.

### Create a Generic `save_with_commit` Function

To avoid repeating code, we'll create one generic function to handle saving any file and committing it. This follows the DRY principle.

**Add this function to `main.py`:**

```python
# ADD this generic save function to main.py

def save_data_with_commit(filepath: Path, data, user: str, message: str, is_json: bool = True):
    """
    A generic function to save data to a file and create a Git commit.
    """
    try:
        # Write the file content
        with open(filepath, 'w') as f:
            if is_json:
                json.dump(data, f, indent=4)
            else:
                f.write(data)

        # Stage and commit the change
        # filepath.relative_to(GIT_REPO_PATH) gets the path inside the repo
        git_repo.index.add([str(filepath.relative_to(GIT_REPO_PATH))])
        author = Actor(user, f"{user}@pdm.local")
        commit = git_repo.index.commit(message, author=author, committer=author)

        logger.info(f"Committed change to {filepath.name} in commit {commit.hexsha[:7]}")

    except GitCommandError as e:
        logger.error(f"Git error during commit for {filepath.name}: {e}")
        # In a real app, you might want to try to `git reset --hard` to revert the file change
        raise HTTPException(status_code=500, detail="Failed to commit changes to version control.")
```

### Refactor `save_locks` and `save_users`

Now, replace your old `save_locks` and `save_users` functions to use this new helper.

```python
# REPLACE your old save_locks and save_users functions

def save_locks(locks: dict, user: str, message: str):
    """Saves the locks dictionary and creates a commit."""
    save_data_with_commit(LOCKS_FILE, locks, user, message)

def save_users(users: dict):
    """Saves the user dictionary and creates a commit."""
    save_data_with_commit(USERS_FILE, users, "system", "Update user data")
```

### Update the Endpoints

Finally, update the `checkout_file` and `checkin_file` endpoints to provide the user and a descriptive commit message.

```python
# UPDATE the checkout_file function

@app.post("/api/files/checkout")
def checkout_file(request: FileCheckoutRequest, current_user: User = Depends(get_current_user)):
    # ... (existing validation logic) ...

    # Create the lock
    locks[request.filename] = { ... }

    # Save with a descriptive commit message
    commit_msg = f"Checkout: {request.filename} by {current_user.username}"
    save_locks(locks, current_user.username, commit_msg)

    # ... (rest of the function) ...

# UPDATE the checkin_file function

@app.post("/api/files/checkin")
def checkin_file(request: FileCheckinRequest, current_user: User = Depends(get_current_user)):
    # ... (existing validation logic) ...

    # Remove the lock
    del locks[request.filename]

    # Save with a descriptive commit message
    commit_msg = f"Checkin: {request.filename} by {current_user.username}"
    save_locks(locks, current_user.username, commit_msg)

    # ... (rest of the function) ...
```

Now, every time a file is checked in or out, a new commit will be created in your `git_repo`. You can `cd backend/git_repo` and run `git log` to see the complete history\!

## 7.4: Viewing Git History

Let's expose this powerful history through our API.

### Add a History Endpoint

Add this new endpoint to `main.py`.

```python
# ADD this new endpoint to main.py

@app.get("/api/files/{filename}/history")
def get_file_history(
    filename: str,
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    """
    Returns the commit history for changes related to a specific file's lock status.
    """
    logger.info(f"History request for {filename} by {current_user.username}")

    try:
        # iter_commits with `paths` is an efficient way to find commits
        # that touched a specific file.
        commits = list(git_repo.iter_commits(paths=str(LOCKS_FILE.relative_to(GIT_REPO_PATH)), max_count=limit))

        history = []
        for commit in commits:
            # We check the commit message to see if this commit is relevant to the requested file
            if filename in commit.message:
                history.append({
                    "hash": commit.hexsha,
                    "author": commit.author.name,
                    "timestamp": commit.committed_datetime.isoformat(),
                    "message": commit.message.strip()
                })

        return {"filename": filename, "history": history}

    except GitCommandError as e:
        logger.error(f"Git error getting history: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve file history.")
```

**Test it\!** After checking a file in and out a few times, you can make a request to `http://127.0.0.1:8000/api/files/PN1001_OP1.mcam/history` (with your auth token) to see the JSON response containing the commit history.

---

## Stage 7 Complete - Full Version Control\!

Your application no longer just overwrites files; it builds a rich, immutable history of every change. This is a massive step towards a professional, enterprise-grade system.

### What You Built

- An application that uses a local Git repository as its versioned data store.
- Atomic, auditable commits for every state change.
- An API endpoint to view the history of any file.

### Final Code for `main.py`

The `main.py` file has grown significantly. A complete snapshot will be provided with the final stage to ensure correctness. The key changes are the addition of `pathlib`, `git`, the new path constants, the `initialize_git_repo` function and startup event, the refactored `save_*` functions, and the new `/history` endpoint.

### What's Next?

In **Stage 8**, we'll build on this foundation by adding more advanced Git features directly into the UI:

- **File Uploads**: Add new `.mcam` files to the repository.
- **Versioned Downloads**: Download a file as it existed in a specific past commit.
- **Diff Viewing**: See exactly what changed between two versions.
- **Blame**: See who was the last person to modify each line of a file.

Let's build out the advanced Git features for your application.

Here is the fully expanded and unified tutorial for **Stage 8**. This stage will make your application a true version control interface by adding file uploads, versioned downloads, and the ability to view diffs and blame history directly in the UI.

---

# Stage 8: Advanced Git Features - Upload, Download, Diff & Blame (Expanded & Unified)

## Introduction: The Goal of This Stage

Your PDM system now uses Git for versioning, but the user interface is still limited. Users can't add new files, download specific versions, or see what has changed. In this stage, we'll expose the true power of Git to the user.

By the end of this stage, you will:

- Implement a drag-and-drop file upload system that creates new Git commits.
- Build a download feature that can retrieve both the latest version and any historical version of a file.
- Create a "diff" viewer to visually compare two versions of a file.
- Implement a "blame" view to see who last modified each line of a file.
- Deepen your understanding of handling binary data, streaming responses, and advanced Git operations.

---

### **🧠 Foundational Concepts: A Deeper Look**

- **Time Investment:** 7-9 hours.
- **Historical Insight**: File uploads on the web were standardized in 1995 by **RFC 1867**, which defined the `multipart/form-data` encoding. This allowed binary files to be sent alongside regular form text. The `diff` algorithm's history goes back to the 1970s, with the modern, efficient version used by Git (based on Myers' algorithm) developed in 1986.
- **Software Engineering Principle: Idempotency**. An operation is idempotent if running it multiple times has the same effect as running it once. A `GET` request to download a specific version (`/download?commit_sha=abc`) is idempotent. A `POST` to upload a new file is **not** idempotent, as running it twice would create two different files or commits.
- **Design Pattern: Factory**. We'll use a simple factory pattern for our download endpoint, where a function (`download_file`) is responsible for creating and configuring a `StreamingResponse` object based on the request parameters.
- **Key Concept: Git LFS (Large File Storage)**. Git is not optimized for large binary files (like multi-megabyte `.mcam` files). **Git LFS** is an extension that stores large files on a separate server and places small text "pointers" in the Git repository instead. This keeps your repository small and fast. While we won't fully implement it, we'll note where it would be used.

---

## 8.1: File Upload with Git Integration

We need a way for users to add new `.mcam` files to our `repo/` directory and have them automatically committed to Git.

### The Upload Flow with Git

1.  **Client**: User drags a file onto the UI.
2.  **Client**: JavaScript creates a `FormData` object and `POST`s it to `/api/files/upload`.
3.  **Server**: FastAPI receives the `multipart/form-data` request.
4.  **Server**: Validates the file (is it a `.mcam`? Is it too large?).
5.  **Server**: Pulls from the remote GitLab/GitHub repo to get the latest changes and avoid conflicts.
6.  **Server**: Writes the file's binary content to the `git_repo/repo/` directory.
7.  **Server**: Performs a `git add` and `git commit` with the user's name and a descriptive message.
8.  **Server**: Pushes the new commit to the remote repo.
9.  **Server**: Returns a success response with the new commit hash.

### Add the Upload Endpoint to `main.py`

This endpoint will handle multipart file uploads, which is different from the JSON bodies we've used so far.

```python
# ADD these imports at the top of main.py
from fastapi import File, UploadFile
import shutil

# ADD this new endpoint to main.py

@app.post("/api/files/upload")
async def upload_file(
    file: UploadFile = File(...), # `UploadFile` is a special type for file uploads
    current_user: User = Depends(get_current_user)
):
    """
    Handles uploading a new .mcam file to the repository.
    """
    logger.info(f"Upload request from '{current_user.username}' for file '{file.filename}'")

    # --- Security & Validation ---
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")
    if not file.filename.lower().endswith('.mcam'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .mcam files are allowed.")

    # Sanitize the filename to prevent directory traversal attacks (e.g., ../../etc/passwd)
    safe_filename = Path(os.path.basename(file.filename))
    file_path = REPO_PATH / safe_filename

    if file_path.exists():
        raise HTTPException(status_code=409, detail=f"File '{safe_filename}' already exists.")

    try:
        # Read file content into memory. `await` is used because reading is an I/O operation.
        content = await file.read()

        # Enforce a size limit (e.g., 10MB) to prevent DoS attacks
        max_size = 10 * 1024 * 1024 # 10 MB
        if len(content) > max_size:
            raise HTTPException(status_code=413, detail="File is too large. Max size is 10MB.")

        # --- Git Operations ---
        # pull_from_gitlab() # In a real multi-user env, you'd pull first.

        # Write the file to the repo directory in binary write mode ('wb')
        with open(file_path, "wb") as f:
            f.write(content)

        commit_msg = f"Add file: {safe_filename}"
        save_data_with_commit(
            filepath=file_path,
            data=None, # Not JSON, so we pass None
            user=current_user.username,
            message=commit_msg,
            is_json=False # Signal to the function to not use json.dump
        )

        # push_to_gitlab() # Push the new commit

        log_audit_event(
            user=current_user.username,
            action="UPLOAD_FILE",
            target=str(safe_filename),
            details={"size_bytes": len(content)}
        )

        return {"success": True, "message": f"File '{safe_filename}' uploaded successfully."}

    except Exception as e:
        logger.error(f"Upload failed for file '{file.filename}': {e}")
        # If anything fails, clean up the partially uploaded file
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=500, detail="An unexpected error occurred during file upload.")

```

### Frontend: Upload UI

Now, let's build a drag-and-drop upload interface.

**Add to `index.html` (e.g., after the file list section):**

```html
<section>
  <h2>Upload New File</h2>
  <div class="upload-area" id="upload-area">
    <input type="file" id="file-input" accept=".mcam" style="display: none;" />
    <div id="upload-prompt">
      <p>📁 Drag & drop a .mcam file here, or click to select</p>
      <p class="upload-hint">Maximum file size: 10MB</p>
    </div>
    <div id="file-preview" class="hidden"></div>
  </div>
  <button type="button" class="btn btn-primary" id="upload-btn" disabled>
    Upload File
  </button>
</section>
```

**Add CSS to `style.css`:**

```css
.upload-area {
  border: 2px dashed #667eea;
  border-radius: 8px;
  padding: 3rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  background: #f8f9ff;
}
.upload-area:hover {
  background: #f0f1ff;
}
.upload-area.drag-over {
  border-style: solid;
  background: #e7f3ff;
}
.upload-hint {
  font-size: 0.9rem;
  color: #6c757d;
}
.file-preview {
  font-weight: bold;
}
#upload-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.hidden {
  display: none;
}
```

**Add JavaScript to `app.js`:**

```javascript
// ADD this inside the 'DOMContentLoaded' event listener in app.js
setupFileUpload();

// ADD these new functions to app.js
function setupFileUpload() {
  const uploadArea = document.getElementById("upload-area");
  const fileInput = document.getElementById("file-input");
  const uploadBtn = document.getElementById("upload-btn");
  let fileToUpload = null;

  const showPreview = (file) => {
    fileToUpload = file;
    document.getElementById("upload-prompt").classList.add("hidden");
    const preview = document.getElementById("file-preview");
    preview.textContent = `Ready to upload: ${file.name} (${(
      file.size / 1024
    ).toFixed(2)} KB)`;
    preview.classList.remove("hidden");
    uploadBtn.disabled = false;
  };

  uploadArea.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", () => showPreview(fileInput.files[0]));

  // Drag and Drop listeners
  uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadArea.classList.add("drag-over");
  });
  uploadArea.addEventListener("dragleave", () =>
    uploadArea.classList.remove("drag-over")
  );
  uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadArea.classList.remove("drag-over");
    const file = e.dataTransfer.files[0];
    if (file && file.name.toLowerCase().endsWith(".mcam")) {
      showPreview(file);
    } else {
      showNotification("Only .mcam files are allowed.", "error");
    }
  });

  uploadBtn.addEventListener("click", async () => {
    if (!fileToUpload) return;

    uploadBtn.disabled = true;
    uploadBtn.textContent = "Uploading...";

    const formData = new FormData();
    formData.append("file", fileToUpload);

    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch("/api/files/upload", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: formData, // Browser sets Content-Type automatically for FormData
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail);

      showNotification(data.message, "success");
      loadFiles(); // Refresh file list
    } catch (error) {
      showNotification(`Upload failed: ${error.message}`, "error");
    } finally {
      // Reset UI
      uploadBtn.disabled = true;
      uploadBtn.textContent = "Upload File";
      document.getElementById("upload-prompt").classList.remove("hidden");
      document.getElementById("file-preview").classList.add("hidden");
      fileToUpload = null;
    }
  });
}
```

---

## 8.2: File Download with Version Selection

Users need to be able to retrieve both the current version of a file and any previous version from its Git history.

### The Download Endpoint

This endpoint will handle two cases:

1.  **No `commit_sha` specified**: Serve the latest version from the working directory.
2.  **`commit_sha` specified**: Read the file content directly from the Git object database for that specific commit.

**Add this new endpoint to `main.py`:**

```python
# ADD these imports to main.py
from fastapi.responses import StreamingResponse
import io

# ADD this new endpoint to main.py
@app.get("/api/files/{filename}/download")
async def download_file(
    filename: str,
    commit_sha: Optional[str] = None, # Optional query parameter for version
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Download request for '{filename}' by '{current_user.username}' (commit: {commit_sha or 'HEAD'})")
    safe_filename = os.path.basename(filename)

    try:
        if commit_sha:
            # --- Get a historical version from Git ---
            commit = git_repo.commit(commit_sha)
            blob = commit.tree / 'repo' / safe_filename
            file_content_bytes = blob.data_stream.read()
        else:
            # --- Get the latest version from the filesystem ---
            file_path = REPO_PATH / safe_filename
            if not file_path.exists():
                raise HTTPException(status_code=404, detail="File not found.")
            with open(file_path, 'rb') as f:
                file_content_bytes = f.read()

        log_audit_event(user=current_user.username, action="DOWNLOAD_FILE", target=safe_filename)

        return StreamingResponse(
            io.BytesIO(file_content_bytes),
            media_type="application/octet-stream",
            headers={'Content-Disposition': f'attachment; filename="{safe_filename}"'}
        )
    except KeyError:
        raise HTTPException(status_code=404, detail=f"File not found in commit {commit_sha[:7]}.")
    except Exception as e:
        logger.error(f"Download failed: {e}")
        raise HTTPException(status_code=500, detail="File download failed.")
```

- **`StreamingResponse`**: This is crucial for performance and memory usage. Instead of loading a potentially huge file into memory and then sending it, this streams the file to the user in chunks.
- **`Content-Disposition`**: This header tells the browser to treat the response as a file to be downloaded, rather than trying to display it in the browser window.

### Frontend: Download Buttons

**Update `createFileElement` in `app.js`** to add a "Download" button to each file item.

```javascript
// In app.js, add this to the actionsDiv inside createFileElement
const downloadBtn = document.createElement("button");
downloadBtn.className = "btn";
downloadBtn.textContent = "Download";
downloadBtn.onclick = () => handleDownload(file.name);
actionsDiv.appendChild(downloadBtn);

// ADD this handler function to app.js
async function handleDownload(filename) {
  try {
    const token = localStorage.getItem("access_token");
    const response = await fetch(`/api/files/${filename}/download`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) throw new Error("Download failed.");

    const blob = await response.blob(); // Get the file content as a Blob
    const url = window.URL.createObjectURL(blob); // Create a temporary URL for the blob

    // Create a hidden link element, click it to trigger the download, then remove it
    const a = document.createElement("a");
    a.style.display = "none";
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    a.remove();
  } catch (error) {
    showNotification(`Error: ${error.message}`, "error");
  }
}
```

---

## 8.3 & 8.4: Viewing Diffs and Blame

These features are conceptually similar: they involve querying Git for historical data and displaying it in a modal. We'll build them together.

### Backend Endpoints

Add these two endpoints to `main.py`.

```python
# ADD these two endpoints to main.py

@app.get("/api/files/{filename}/diff")
def get_file_diff(
    filename: str, commit1: str, commit2: str = "HEAD",
    current_user: User = Depends(get_current_user)
):
    """Generates a diff for a file between two commits."""
    safe_filename = os.path.basename(filename)
    path_in_repo = f'repo/{safe_filename}'
    try:
        diffs = git_repo.commit(commit1).diff(commit2, paths=path_in_repo, create_patch=True)
        if not diffs:
            return {"diff": "No changes found for this file between the selected commits."}

        diff_text = diffs[0].diff.decode('utf-8')
        return {"diff": diff_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/{filename}/blame")
def get_file_blame(
    filename: str, current_user: User = Depends(get_current_user)
):
    """Generates a blame for a file, showing who last modified each line."""
    safe_filename = os.path.basename(filename)
    path_in_repo = f'repo/{safe_filename}'
    try:
        blame_output = git_repo.blame('HEAD', path_in_repo)
        blame_data = []
        for commit, lines in blame_output:
            for line in lines:
                blame_data.append({
                    "commit_hash": commit.hexsha[:7],
                    "author": commit.author.name,
                    "date": commit.committed_datetime.isoformat(),
                    "line": line.decode('utf-8', errors='ignore').strip()
                })
        return {"blame": blame_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Frontend Implementation

Implementing a full-featured diff and blame viewer on the frontend is complex. For this tutorial, we will focus on adding the buttons and a simple modal to display the raw text output.

**Add Modals to `index.html`:**

```html
<div id="history-modal" class="modal-overlay hidden">
  <div class="modal-content modal-large">
    <div class="modal-header">
      <h3>File History</h3>
      <button class="modal-close">&times;</button>
    </div>
    <div id="history-content" class="modal-body"></div>
  </div>
</div>
<div id="diff-modal" class="modal-overlay hidden">
  <div class="modal-content modal-large">
    <div class="modal-header">
      <h3>File Diff</h3>
      <button class="modal-close">&times;</button>
    </div>
    <div id="diff-content" class="modal-body"><pre></pre></div>
  </div>
</div>
```

**Add Buttons and Handlers to `app.js`:**

```javascript
// In app.js, create instances for the new modals
const historyModal = new ModalManager("history-modal");
const diffModal = new ModalManager("diff-modal");

// In createFileElement, add the new buttons
const historyBtn = document.createElement("button");
historyBtn.className = "btn";
historyBtn.textContent = "History";
historyBtn.onclick = () => showHistory(file.name);
actionsDiv.appendChild(historyBtn);

// Add the new handler functions to app.js
async function showHistory(filename) {
  historyModal.open();
  const content = document.getElementById("history-content");
  content.innerHTML = "<p>Loading history...</p>";

  try {
    const token = localStorage.getItem("access_token");
    const response = await fetch(`/api/files/${filename}/history`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) throw new Error("Failed to load history.");
    const data = await response.json();

    let html = "<ul>";
    data.history.forEach((commit) => {
      html += `<li><strong>${commit.hash.substring(0, 7)}</strong> by ${
        commit.author
      }: ${commit.message} 
            (<a href="#" onclick="showDiff('${filename}', '${
        commit.hash
      }')">View Diff</a>)</li>`;
    });
    html += "</ul>";
    content.innerHTML = html;
  } catch (error) {
    content.innerHTML = `<p class="error">${error.message}</p>`;
  }
}

async function showDiff(filename, commitHash) {
  diffModal.open();
  const content = document.querySelector("#diff-content pre");
  content.textContent = "Loading diff...";

  try {
    const token = localStorage.getItem("access_token");
    const response = await fetch(
      `/api/files/${filename}/diff?commit1=${commitHash}~1&commit2=${commitHash}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    if (!response.ok) throw new Error("Failed to load diff.");
    const data = await response.json();
    content.textContent = data.diff;
  } catch (error) {
    content.textContent = `Error: ${error.message}`;
  }
}
```

- **`commitHash~1`**: This is Git syntax for "the parent of `commitHash`". We are diffing a commit against its immediate parent to see what changed in that specific commit.

---

## Stage 8 Complete - Advanced Git Mastery\!

You have now built a sophisticated interface on top of Git, exposing its most powerful features—uploading, versioned downloads, and historical analysis—directly to your users.

### Final File Snapshots

Your `main.py` has been significantly updated with upload, download, diff, and blame endpoints. Your `app.js` now includes handlers for all these new actions, and your `index.html` and `style.css` have the necessary UI elements and styling.

### What's Next?

In **Stage 9**, we will make the application collaborative in real-time. We'll introduce **WebSockets** to push live updates to all connected users, so when one person checks out a file, everyone else sees it happen instantly without needing to refresh.

Of course. Let's make your application collaborative and real-time.

Here is the fully expanded and unified tutorial for **Stage 9**. This stage introduces WebSockets, a powerful technology that enables your server to push updates directly to clients, eliminating the need for users to manually refresh the page.

---

# Stage 9: Real-Time Collaboration - WebSockets & Live Updates (Expanded & Unified)

## Introduction: The Goal of This Stage

Your application is powerful, but it's not "live." When one user checks out a file, another user won't know until they manually refresh their browser. This leads to stale data and a poor collaborative experience. In this stage, you'll fix that by implementing **WebSockets** for real-time, bidirectional communication.

By the end of this stage, you will:

- Understand the fundamental difference between the HTTP request-response model and the persistent connection of WebSockets.
- Implement a WebSocket server in FastAPI to manage and broadcast messages to connected clients.
- Build a resilient WebSocket client in JavaScript that handles connections, disconnections, and automatic reconnection.
- Implement a **heartbeat** to keep connections alive and detect silent failures.
- Create a **presence** feature to show a live list of who is currently online.
- Broadcast events for all major actions (`checkout`, `checkin`, `upload`), ensuring every user's UI is always up-to-date.

---

### **🧠 Foundational Concepts: A Deeper Look**

- **Time Investment:** 7-9 hours. Real-time systems introduce new complexities around state management and connection reliability.
- **Historical Insight**: Before WebSockets (standardized in 2011 as RFC 6455), developers used clever but inefficient "hacks" like **long-polling** (keeping an HTTP request open for a long time) to simulate server-push. WebSockets provided a standard, efficient, and true full-duplex communication channel built on top of TCP.
- **Software Engineering Principle: Event-Driven Architecture (EDA)**. Your application will shift from a purely request-driven model to an event-driven one. Actions will now "publish" events (like `FILE_LOCKED`), and various parts of your system (including other users' browsers) will "subscribe" and react to them. This creates a loosely coupled and highly scalable system.
- **Design Pattern: Publish/Subscribe (Pub/Sub)**. Our `ConnectionManager` will act as a "channel" or "topic." When an endpoint wants to notify users, it "publishes" a message to this channel. The manager then sends that message to all "subscribed" clients. The endpoint doesn't need to know who or how many clients are connected, which is a powerful abstraction.

---

## 9.1: HTTP vs. WebSockets: A Tale of Two Conversations

### The Old Way: HTTP Polling 🗣️

Imagine asking a friend "Anything new?" every 30 seconds. Most of the time, the answer is "No." This is inefficient and the updates are delayed. This is how traditional HTTP works for live updates (polling).

```
Client             Server
  |--- GET /updates --->|
  |<-- (200 OK, no new data)---|
  | (waits 30s)          |
  |--- GET /updates --->|
  |<-- (200 OK, no new data)---|
```

### The New Way: WebSockets 📞

Now imagine calling your friend and keeping the line open. When something happens, they tell you immediately. This is a WebSocket: a single, persistent, two-way connection.

```
Client             Server
  |--- (Handshake) --->|
  |<-- (Handshake OK) --|
  |====================| (Connection stays open)
  |                    |
  |<--- (Event: file_locked) ---| (Server pushes update instantly)
```

The server can push data to the client at any time, resulting in true real-time communication with minimal latency and overhead.

---

## 9.2: WebSocket Server in FastAPI

FastAPI has excellent built-in support for WebSockets. We'll start by creating a `ConnectionManager` class to keep track of all connected clients.

### The `ConnectionManager` Class

This class will be a singleton in our application, responsible for managing the lifecycle of all WebSocket connections.

**Add this new class to `backend/main.py`:**

```python
# ADD these imports to the top of main.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json

# ADD this new class to main.py
class ConnectionManager:
    """
    Manages active WebSocket connections and message broadcasting.
    This acts as a Pub/Sub hub for real-time events.
    """
    def __init__(self):
        # A dictionary to store active connections, mapping username to WebSocket object
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str):
        """Accepts a new connection and adds it to the registry."""
        await websocket.accept()
        self.active_connections[username] = websocket
        logger.info(f"WebSocket connected: {username} (Total: {len(self.active_connections)})")
        # Announce the new user to everyone
        await self.broadcast({
            "type": "user_connected",
            "username": username,
            "online_users": self.get_online_users()
        })

    def disconnect(self, username: str):
        """Removes a connection from the registry."""
        if username in self.active_connections:
            del self.active_connections[username]
            logger.info(f"WebSocket disconnected: {username} (Total: {len(self.active_connections)})")

    async def broadcast(self, message: dict):
        """Sends a JSON message to all active connections."""
        message_json = json.dumps(message)
        disconnected_users = []
        for username, connection in self.active_connections.items():
            try:
                await connection.send_text(message_json)
            except Exception:
                # If sending fails, the client has likely disconnected without a proper close frame.
                disconnected_users.append(username)

        # Clean up any dead connections found during broadcast
        for username in disconnected_users:
            self.disconnect(username)

    def get_online_users(self) -> List[str]:
        """Returns a list of usernames for all currently connected users."""
        return list(self.active_connections.keys())

# Create a single global instance of the manager
manager = ConnectionManager()
```

---

## 9.3: The WebSocket Endpoint

This is the FastAPI endpoint that clients will connect to. It handles authentication and listens for incoming messages in a continuous loop.

### Add the WebSocket Endpoint to `main.py`

Authentication for WebSockets is slightly different since they don't use standard HTTP headers after the initial handshake. A common and secure pattern is to pass the JWT as a query parameter.

```python
# ADD this new endpoint to main.py

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    """
    The main WebSocket endpoint. Handles authentication and the connection lifecycle.
    """
    # 1. Authenticate the user from the token in the query parameter
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or get_user(username) is None:
            await websocket.close(code=1008) # Policy Violation
            return
    except JWTError:
        await websocket.close(code=1008)
        return

    # 2. Connect the user to the manager
    await manager.connect(websocket, username)

    try:
        # 3. Enter a loop to listen for messages
        while True:
            # This will block until a message is received
            data = await websocket.receive_text()
            # For this tutorial, we only handle client pings for heartbeats.
            # You could expand this to handle other client-sent messages.
            message = json.loads(data)
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        # 4. Handle disconnection
        manager.disconnect(username)
        # Announce the user's departure
        await manager.broadcast({
            "type": "user_disconnected",
            "username": username,
            "online_users": manager.get_online_users()
        })
```

---

## 9.4: Broadcasting Events from API Endpoints

Now, we need to modify our existing endpoints (`checkout`, `checkin`, `upload`) to publish events through the `ConnectionManager` after a successful operation.

### Make the Endpoints `async`

Since `manager.broadcast()` is an `async` function, the endpoints that call it must also be declared as `async`.

### Update the Endpoints

Find your `checkout_file`, `checkin_file`, and `upload_file` functions in `main.py` and modify them.

**`checkout_file`:**

```python
# UPDATE the checkout_file endpoint

@app.post("/api/files/checkout")
async def checkout_file(request: FileCheckoutRequest, current_user: User = Depends(get_current_user)):
    # ... (all existing validation and locking logic) ...

    save_locks(locks, current_user.username, commit_msg)

    # --- BROADCAST EVENT ---
    await manager.broadcast({
        "type": "file_locked",
        "filename": request.filename,
        "user": current_user.username,
        "message": request.message
    })

    log_audit_event(...) # Your audit logging
    return {"success": True, "message": "File checked out successfully"}
```

**`checkin_file`:**

```python
# UPDATE the checkin_file endpoint

@app.post("/api/files/checkin")
async def checkin_file(request: FileCheckinRequest, current_user: User = Depends(get_current_user)):
    # ... (all existing validation and lock removal logic) ...

    save_locks(locks, current_user.username, commit_msg)

    # --- BROADCAST EVENT ---
    await manager.broadcast({
        "type": "file_unlocked",
        "filename": request.filename,
        "user": current_user.username
    })

    log_audit_event(...) # Your audit logging
    return {"success": True, "message": "File checked in successfully"}
```

**`upload_file`:**

```python
# UPDATE the upload_file endpoint

@app.post("/api/files/upload")
async def upload_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    # ... (all existing validation and file saving logic) ...

    save_data_with_commit(...)

    # --- BROADCAST EVENT ---
    await manager.broadcast({
        "type": "file_uploaded",
        "filename": str(safe_filename),
        "user": current_user.username,
        "size_bytes": len(content)
    })

    log_audit_event(...)
    return {"success": True, "message": "File uploaded successfully."}
```

---

## 9.5: The WebSocket Client (Frontend)

Now for the frontend. We'll write JavaScript to connect to our WebSocket endpoint, listen for messages, and handle connection issues gracefully.

### Add UI Elements for Presence

First, add a place in `index.html` to show the connection status and the list of online users.

**Add to `index.html` (inside the `<header>`):**

```html
<span id="connection-status" class="status-disconnected">🔴 Disconnected</span>
```

**Add to `index.html` (as a new `<section>` in `<main>`):**

```html
<section>
  <h2>Online Users</h2>
  <div id="online-users-list">
    <p>Connecting...</p>
  </div>
</section>
```

**Add CSS to `style.css`:**

```css
/* Add these styles for presence indicators */
.status-connected,
.status-disconnected {
  margin-right: 1rem;
  font-weight: 500;
}
.status-connected {
  color: #28a745;
}
.status-disconnected {
  color: #dc3545;
}
#online-users-list ul {
  list-style: none;
  padding: 0;
}
#online-users-list li {
  display: flex;
  align-items: center;
  padding: 0.25rem 0;
}
#online-users-list .status-dot {
  height: 8px;
  width: 8px;
  background-color: #28a745;
  border-radius: 50%;
  display: inline-block;
  margin-right: 0.5rem;
}
```

### The WebSocket Connection Logic

Add this comprehensive block to `app.js`. It handles connection, reconnection with exponential backoff, and a heartbeat.

```javascript
// ADD this entire block to app.js

// ============================================
// WEBSOCKET CLIENT
// ============================================
let ws = null;
let reconnectAttempts = 0;

function connectWebSocket() {
  const token = localStorage.getItem("access_token");
  if (!token) return;

  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws?token=${token}`;

  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log("WebSocket connected!");
    updateConnectionStatus(true);
    reconnectAttempts = 0; // Reset on successful connection
    startHeartbeat();
  };

  ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    console.log("WS Message Received:", message);
    handleWebSocketMessage(message);
  };

  ws.onclose = () => {
    console.log("WebSocket disconnected.");
    updateConnectionStatus(false);
    stopHeartbeat();

    // Exponential backoff for reconnection
    const delay = Math.min(1000 * 2 ** reconnectAttempts, 30000); // Max 30s
    console.log(`Will attempt to reconnect in ${delay / 1000}s`);
    setTimeout(connectWebSocket, delay);
    reconnectAttempts++;
  };

  ws.onerror = (error) => {
    console.error("WebSocket error:", error);
    ws.close(); // This will trigger the onclose handler for reconnection
  };
}

function updateConnectionStatus(isConnected) {
  const statusEl = document.getElementById("connection-status");
  if (isConnected) {
    statusEl.textContent = "🟢 Connected";
    statusEl.className = "status-connected";
  } else {
    statusEl.textContent = "🔴 Disconnected";
    statusEl.className = "status-disconnected";
  }
}

// --- Heartbeat ---
let heartbeatInterval = null;
function startHeartbeat() {
  heartbeatInterval = setInterval(() => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: "ping" }));
    }
  }, 30000); // Send a ping every 30 seconds
}
function stopHeartbeat() {
  clearInterval(heartbeatInterval);
  heartbeatInterval = null;
}

// --- Initialize on Page Load ---
// Add this call inside your DOMContentLoaded listener
document.addEventListener("DOMContentLoaded", function () {
  // ... existing setup code ...
  connectWebSocket();
});
```

## 9.6: Handling Real-Time Events in the UI

Now, create the master message handler that updates the UI based on events from the server.

**Add these functions to `app.js`:**

```javascript
// ADD this message router and its handlers to app.js

function handleWebSocketMessage(message) {
  switch (message.type) {
    case "file_locked":
    case "file_unlocked":
      updateFileState(message.filename, message.type, message.user);
      showNotification(
        `File '${message.filename}' was ${
          message.type === "file_locked" ? "locked" : "unlocked"
        } by ${message.user}.`,
        "info"
      );
      break;
    case "file_uploaded":
      loadFiles(); // Easiest way to handle is a full refresh
      showNotification(
        `New file '${message.filename}' was uploaded by ${message.user}.`,
        "info"
      );
      break;
    case "user_connected":
    case "user_disconnected":
    case "online_users":
      updateOnlineUsersList(message.online_users);
      break;
    case "pong":
      // Heartbeat acknowledged by server
      break;
  }
}

function updateFileState(filename, type, user) {
  const file = allFiles.find((f) => f.name === filename);
  if (file) {
    file.status = type === "file_locked" ? "checked_out" : "available";
    file.locked_by = type === "file_locked" ? user : null;
    displayFilteredAndSortedFiles(); // Re-render the UI with the new state
  }
}

function updateOnlineUsersList(users) {
  const listEl = document.getElementById("online-users-list");
  if (!users || users.length === 0) {
    listEl.innerHTML = "<p>You are the only one here.</p>";
    return;
  }

  const currentUser = localStorage.getItem("username");
  listEl.innerHTML =
    "<ul>" +
    users
      .map(
        (user) =>
          `<li><span class="status-dot"></span>${user}${
            user === currentUser ? " (You)" : ""
          }</li>`
      )
      .join("") +
    "</ul>";
}
```

---

## Stage 9 Complete - Real-Time Collaboration\!

Your application is now a live, collaborative environment. Changes made by one user are instantly reflected for everyone else, and the presence list gives users awareness of who they are working with.

### Verification Checklist

- [ ] When you open the app, the connection status indicator turns green.
- [ ] The "Online Users" list shows your username.
- [ ] Open the application in a **second browser window** (or an incognito window) and log in as a different user (e.g., `admin`).
- [ ] The "Online Users" list in both windows should now show both users.
- [ ] In one window, check out a file. The UI in the **other window** should update instantly to show the file is locked, without a page refresh.
- [ ] Check the file back in. The other window should update instantly again.
- [ ] Close one of the browser windows. The "Online Users" list in the remaining window should update to show only one user.
- [ ] Disconnect your internet for 10 seconds and then reconnect. The WebSocket should automatically reconnect (the status indicator will go red, then green again).

### What's Next?

Your application has a rich feature set, but how do you ensure it all works correctly and stays that way? In **Stage 10**, we'll dive deep into **Testing and Quality Assurance**. We'll write comprehensive unit and integration tests, measure code coverage, and set up a Continuous Integration (CI) pipeline to automate testing for every change you make.

Here is the fully expanded and unified tutorial for **Stage 10**. This stage is dedicated to ensuring the quality and reliability of your application through comprehensive automated testing and setting up a Continuous Integration (CI) pipeline.

---

# Stage 10: Testing & Quality Assurance - Building Bulletproof Software (Expanded & Unified)

## Introduction: The Goal of This Stage

Your application has a rich set of features, but how do you verify they work correctly after every change? Manual testing is slow, error-prone, and doesn't scale. This stage introduces **automated testing**, the professional practice that ensures software quality, enables confident refactoring, and prevents regressions.

By the end of this stage, you will:

- Understand the "why" behind testing and the **Testing Pyramid** model.
- Write a comprehensive test suite using **pytest**, covering unit and integration tests.
- Use **fixtures** for clean and reusable test setup and teardown.
- **Mock** external dependencies to create fast, isolated tests.
- Write tests for `async` code and WebSocket interactions.
- Measure **test coverage** to identify untested parts of your codebase.
- Practice **Test-Driven Development (TDD)** by building a new feature test-first.
- Set up a **Continuous Integration (CI)** pipeline with GitHub Actions to automate your tests.

---

### **🧠 Foundational Concepts: A Deeper Look**

- **Time Investment:** 6-8 hours.
- **Historical Insight**: The modern testing discipline grew from the **xUnit** framework family, starting with **JUnit** for Java in 1997. **Test-Driven Development (TDD)** was popularized by Kent Beck as part of Extreme Programming in the early 2000s. **pytest** (2004) evolved from the `py.test` tool, offering a more readable and powerful alternative to Python's built-in `unittest` module.
- **Software Engineering Principle: The Testing Pyramid**. Coined by Mike Cohn, this model advocates for a healthy balance of tests: lots of fast, simple **unit tests** at the base; fewer, more complex **integration tests** in the middle; and a very small number of slow, end-to-end **UI tests** at the top. This structure maximizes confidence while minimizing test execution time.
- **Design Pattern: Mock Object**. A mock is a test double that mimics the behavior of a real object. We use mocks to isolate the code we're testing from its dependencies (like databases, APIs, or the filesystem), which makes our tests faster and more reliable.

---

## 10.1: Why Testing Matters - The Cost of Bugs

A bug caught during development might take minutes to fix. The same bug found by a customer in production can cost thousands of dollars in downtime, data corruption, and lost reputation. **Automated testing is an investment that pays for itself by catching bugs early.** This is known as "shifting left"—finding and fixing problems as early as possible in the development lifecycle.

- **Unit Tests (70-80% of tests):** Test a single function or class in isolation. They are fast and focused.
- **Integration Tests (10-20%):** Test how multiple components work together (e.g., does an API endpoint correctly write to the database?).
- **End-to-End (E2E) Tests (1-5%):** Test a full user workflow through the UI. They are slow, brittle, and expensive to maintain.

Our focus will be on building a strong foundation of unit and integration tests with `pytest`.

---

## 10.2: Setting Up Your Testing Environment

### Install Dependencies

```bash
pip install pytest pytest-asyncio pytest-cov
pip freeze > requirements.txt
```

- `pytest`: The core testing framework.
- `pytest-asyncio`: A plugin to enable testing of `async` code.
- `pytest-cov`: A plugin for measuring test coverage.

### Create the Test Directory Structure

`pytest` automatically discovers tests in files named `test_*.py` or `*_test.py`. Let's organize them.

```bash
# In your backend/ directory
mkdir tests
touch tests/__init__.py
touch tests/conftest.py # This file is special to pytest for fixtures
```

### Configure Pytest

Create a `pytest.ini` file in your project root (`pdm-tutorial/`) to standardize test runs.

**Create `pdm-tutorial/pytest.ini`:**

```ini
[pytest]
# Specifies the paths pytest should look for tests in.
testpaths = backend/tests

# Default command-line options.
# -v: verbose output
# --cov=backend: measure coverage for the 'backend' directory
# --cov-report=term-missing: show missing lines in the terminal
# --cov-fail-under=80: fail the test run if coverage drops below 80%
addopts = -v --cov=backend --cov-report=term-missing --cov-fail-under=80
```

This configuration file ensures that you and your teammates (and your CI server) all run tests with the same settings. The `cov-fail-under` option acts as a quality gate.

---

## 10.3: Test Fixtures for Setup & Teardown

Tests need a consistent, clean environment. **Fixtures** are `pytest`'s powerful way to manage test setup, teardown, and dependencies.

### Create `conftest.py`

Fixtures defined in `backend/tests/conftest.py` are automatically available to all tests in that directory and its subdirectories.

```python
# backend/tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import shutil

# To allow tests to import from the parent `backend` directory
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import app, User, get_current_user, git_repo

# --- Core Fixtures ---

@pytest.fixture(scope="session")
def client():
    """A TestClient instance that can be used to make requests to the app."""
    return TestClient(app)

@pytest.fixture(scope="function")
def temp_git_repo(monkeypatch):
    """
    Creates a fresh, temporary Git repository for each test function.
    This ensures tests are isolated and don't interfere with each other.
    The `yield` statement passes the repo object to the test, and the
    code after `yield` is the teardown/cleanup logic.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_repo_path = Path(temp_dir) / "test_git_repo"

        # Use monkeypatch to temporarily override the global GIT_REPO_PATH
        # so the app uses our temporary repo instead of the real one.
        monkeypatch.setattr("main.GIT_REPO_PATH", temp_repo_path)

        from main import initialize_git_repo
        repo = initialize_git_repo()

        # Add a sample file to the repo
        (repo.working_dir / "repo").mkdir()
        (repo.working_dir / "repo" / "sample.mcam").write_text("G-Code content")
        repo.index.add(["repo/sample.mcam"])
        repo.index.commit("Add sample file")

        yield repo # This is what the test function will receive

# --- Authentication Fixtures ---

@pytest.fixture
def admin_user():
    return User(username="admin", full_name="Admin User", role="admin")

@pytest.fixture
def normal_user():
    return User(username="john", full_name="John Doe", role="user")

def override_get_current_user(user: User):
    """Factory to create a dependency override for a specific user."""
    return lambda: user

@pytest.fixture
def admin_token(client):
    """Logs in as admin and returns an access token."""
    resp = client.post("/api/auth/login", data={"username": "admin", "password": "admin123"})
    return resp.json()["access_token"]

@pytest.fixture
def admin_headers(admin_token):
    """Returns authorization headers for an admin user."""
    return {"Authorization": f"Bearer {admin_token}"}
```

---

## 10.4: Writing Unit & Integration Tests

Now we can write tests using these fixtures. We'll start with unit tests for our authentication logic.

### Testing Authentication

**Create `backend/tests/test_auth.py`:**

```python
# backend/tests/test_auth.py

from main import verify_password, pwd_context, app
from unittest.mock import MagicMock

def test_password_hashing_and_verification():
    """Unit Test: Verifies that hashing and checking work correctly."""
    # Arrange
    password = "a_very_secret_password"

    # Act
    hashed_password = pwd_context.hash(password)

    # Assert
    assert hashed_password != password
    assert verify_password(password, hashed_password) is True
    assert verify_password("wrong_password", hashed_password) is False

def test_login_endpoint_success(client, temp_git_repo):
    """Integration Test: Test a successful login via the API endpoint."""
    response = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_delete_file_as_non_admin(client, temp_git_repo, normal_user):
    """Integration Test: Ensures a non-admin user gets a 403 Forbidden error."""
    # Arrange: Override the dependency to simulate a normal user being logged in.
    app.dependency_overrides[get_current_user] = override_get_current_user(normal_user)

    # Act
    response = client.delete("/api/admin/files/sample.mcam")

    # Assert
    assert response.status_code == 403

    # Cleanup the override
    app.dependency_overrides.clear()
```

### Testing WebSocket Connections

Testing WebSockets requires `pytest-asyncio`.

**Create `backend/tests/test_websockets.py`:**

```python
# backend/tests/test_websockets.py

import pytest
from unittest.mock import AsyncMock, patch

from main import manager

@pytest.mark.asyncio
async def test_websocket_broadcast_on_checkout(client, temp_git_repo, admin_headers):
    """
    Integration Test: Mocks the broadcast method to verify it's called
    when a file is checked out.
    """
    # Arrange: Patch the manager's broadcast method with an AsyncMock
    with patch("main.manager.broadcast", new_callable=AsyncMock) as mock_broadcast:

        # Act: Make the API call that should trigger the broadcast
        client.post(
            "/api/files/checkout",
            headers=admin_headers,
            json={"filename": "sample.mcam", "user": "admin", "message": "test"}
        )

        # Assert: Check that our mock broadcast function was called
        mock_broadcast.assert_awaited_once()
        call_args = mock_broadcast.call_args[0][0] # Get the message that was broadcast
        assert call_args["type"] == "file_locked"
        assert call_args["filename"] == "sample.mcam"
```

- **`@pytest.mark.asyncio`**: This marker tells `pytest-asyncio` to run the test function inside an async event loop.
- **`AsyncMock`**: A special version of `MagicMock` from `unittest.mock` for mocking `async` functions. We use `assert_awaited_once()` to verify it was called with `await`.

---

## 10.5: Test-Driven Development (TDD) Example

TDD flips the development process: you write a failing test _first_, then write the code to make it pass. This ensures your code is testable by design.

**The Cycle:** **RED** -\> **GREEN** -\> **REFACTOR**

Let's build a new feature: an endpoint to get a user's profile.

### **Step 1: RED** - Write a failing test

**Add to `test_auth.py`:**

```python
def test_get_own_profile(client, temp_git_repo, admin_user, admin_headers):
    """TDD: Test for a new /api/users/me endpoint."""
    # Arrange: Override dependency to simulate the admin user
    app.dependency_overrides[get_current_user] = override_get_current_user(admin_user)

    # Act
    response = client.get("/api/users/me", headers=admin_headers)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"
    assert data["role"] == "admin"

    app.dependency_overrides.clear()
```

Run `pytest`. This test will fail with a `404 Not Found` because the endpoint doesn't exist. **This is the RED phase.**

### **Step 2: GREEN** - Write the minimal code to pass the test

**Add to `main.py`:**

```python
@app.get("/api/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Returns the profile of the currently authenticated user."""
    return current_user
```

Run `pytest` again. The test now passes. **This is the GREEN phase.**

### **Step 3: REFACTOR** - Improve the code (if necessary)

In this case, the code is already clean and minimal. The refactor step is where you would clean up logic, improve variable names, or extract helper functions, all while ensuring the tests continue to pass.

---

## 10.6: Continuous Integration (CI) with GitHub Actions

CI automatically runs your tests every time you push code to your repository, preventing broken code from being merged.

### Create the Workflow File

Create the directory structure `.github/workflows/` in your project root (`pdm-tutorial/`).

**Create `.github/workflows/ci.yml`:**

```yaml
name: PDM Backend CI

# Triggers the workflow on pushes or pull requests to the main branch
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    # Use the latest version of Ubuntu as the runner environment
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: ./backend # All commands will run from the backend dir

    steps:
      # Step 1: Check out the repository code
      - name: Checkout repository
        uses: actions/checkout@v4

      # Step 2: Set up Python environment
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      # Step 3: Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # Step 4: Run tests with pytest
      # The pytest.ini file will be automatically used
      - name: Run tests and generate coverage report
        run: pytest
```

Commit and push `ci.yml`, `pytest.ini`, and your test files to GitLab/GitHub. Go to the "Actions" or "CI/CD" tab on the repository website. You'll see your workflow running\! If it passes, you'll get a green checkmark. If a test fails or coverage is too low, you'll get a red X, and you can block pull requests from being merged until it's fixed.

---

## Stage 10 Complete - A Bulletproof Application\!

You have built a comprehensive safety net for your application. You can now refactor code, add new features, and collaborate with others with confidence, knowing that your automated test suite is constantly verifying the integrity of your system.

### Verification Checklist

- [ ] All tests pass when you run `pytest`.
- [ ] Test coverage is above 80%.
- [ ] The GitHub Actions CI pipeline runs successfully on every push.
- [ ] You have unit tests for critical logic (like password hashing).
- [ ] You have integration tests for API endpoints, including failure cases (401, 403, 404, 422).
- [ ] You have a test for your WebSocket logic.
- [ ] You understand the Red-Green-Refactor cycle of TDD.

### What's Next?

In **Stage 11**, we'll take the final step: **Production Deployment**. We'll containerize the application with Docker, migrate from simple files to a real PostgreSQL database, and set up a multi-container environment with Docker Compose and an Nginx reverse proxy.

Here is the fully expanded and unified tutorial for **Stage 11**. This is the final and most complex stage, where we take our application from a development setup to a professional, production-ready, containerized deployment using Docker, PostgreSQL, and Nginx.

---

# Stage 11: Production Deployment - From Development to Production (Expanded & Unified)

## Introduction: The Goal of This Stage

Your app works perfectly on your laptop (`localhost`), but deploying to a production server is a completely different challenge. Production demands reliability, security, scalability, and consistency. In this stage, you'll learn the tools and principles to bridge the gap between development and production.

By the end of this stage, you will:

- Understand the **12-Factor App methodology** for building robust cloud-native applications.
- Manage configuration securely using **environment variables** instead of hardcoded values.
- **Containerize** your application with **Docker** to create a portable, reproducible environment.
- Migrate your data from simple JSON files to a powerful **PostgreSQL** database.
- Orchestrate your entire application stack (app, database, web server) with **Docker Compose**.
- Use **Nginx** as a high-performance reverse proxy.
- Implement production-grade structured logging and health checks.

---

### **🧠 Foundational Concepts: A Deeper Look**

- **Time Investment:** 8-10 hours. This is a dense stage covering critical DevOps concepts.
- **Historical Insight**: **Docker** (2013) revolutionized software deployment by popularizing Linux containers, a technology with roots in **`chroot`** (1979) and Solaris Zones (2004). It made the mantra "it works on my machine" a reality by packaging the application _with_ its environment.
- **Software Engineering Principle: The 12-Factor App**. Published in 2011 by engineers at Heroku, this is a set of best practices for building modern, scalable web applications. We will focus on key factors like:
  - **III. Config**: Store configuration in the environment, not in the code.
  - **VI. Processes**: Execute the app as one or more stateless processes.
  - **X. Dev/Prod Parity**: Keep development, staging, and production as similar as possible.
- **Key Concept: Blue-Green Deployment**. This is an advanced, zero-downtime deployment strategy. You have two identical production environments ("Blue" and "Green"). Blue is live. You deploy the new version to Green, test it, then switch the router (Nginx) to point all traffic to Green. Green is now the new live environment. This allows for instant rollbacks by simply switching the router back to Blue.

---

## 11.1: Environment Variables for Secure Configuration

Hardcoding secrets like your `SECRET_KEY` or database passwords in your code is a major security risk. These values should be injected into the application from the environment.

### Using Pydantic Settings

We'll use `pydantic-settings` to load, validate, and manage our configuration from environment variables and `.env` files.

**Install the library:**

```bash
pip install pydantic-settings
pip freeze > requirements.txt
```

**Create a `config.py` file** in your `backend` directory. This will be the single source of truth for all configuration.

```python
# backend/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.
    Pydantic handles type casting (e.g., string "30" -> int 30).
    """
    # Application
    APP_NAME: str = "PDM System"
    DEBUG: bool = False

    # Security & JWT
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str = "sqlite:///./pdm_dev.db" # Default to SQLite for simple dev

    class Config:
        # This tells Pydantic to try loading variables from a file named .env
        env_file = ".env"

# Create a single, cached instance of the settings
settings = Settings()
```

### Create `.env` and `.env.example`

- **`.env`**: This file will hold your **local development secrets**. It should **NEVER** be committed to Git.
- **`.env.example`**: This file is a template showing what variables are needed. It **SHOULD** be committed to Git.

**Create `backend/.env` (DO NOT COMMIT):**

```
# Development secrets for PDM App
# Copy this from .env.example and fill in the values

DEBUG=True
SECRET_KEY=a_very_secret_and_long_key_for_development_only_!!!
DATABASE_URL=postgresql://pdm_user:pdm_pass@localhost:5432/pdm_db
```

**Create `backend/.env.example` (COMMIT THIS):**

```
# Template for environment variables.
# Copy to .env for local development or set these in your production environment.
DEBUG=False
SECRET_KEY=
DATABASE_URL=
```

**Add `.env` to your `.gitignore` file** in the project root to prevent accidentally committing it.

```
# .gitignore
venv/
__pycache__/
*.pyc
.env
```

### Update `main.py` to Use the Settings

Now, refactor `main.py` to import and use the `settings` object instead of hardcoded values.

```python
# In main.py, replace hardcoded values

# ADD this import at the top
from config import settings

# REPLACE the old JWT constants
# SECRET_KEY = "..."
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# The values now come from our settings object
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# The same applies to DATABASE_URL when you set up the database.
```

---

## 11.2: Containerizing with Docker

Docker allows us to package our application and its entire environment (Python, libraries, system dependencies) into a single, portable unit called an **image**.

### The `Dockerfile`

Create a file named `Dockerfile` (no extension) in your `backend` directory. We will use a **multi-stage build**, a best practice that creates a smaller, more secure final image.

```dockerfile
# backend/Dockerfile

# --- Stage 1: The Builder ---
# This stage installs dependencies, including build-time tools.
# It will be discarded later to keep the final image small.
FROM python:3.11-slim as builder

# Set environment variables for a clean build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker's layer caching.
# This step will only be re-run if requirements.txt changes.
COPY requirements.txt .

# Install dependencies into a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r requirements.txt


# --- Stage 2: The Final Image ---
# This is the lean image we will actually deploy.
FROM python:3.11-slim

WORKDIR /app

# Copy the virtual environment from the builder stage.
# This is much smaller than including the build tools.
COPY --from=builder /opt/venv /opt/venv

# Copy the application code
COPY . .

# Set the PATH to use the virtual environment's executables
ENV PATH="/opt/venv/bin:$PATH"

# Run as a non-root user for better security
RUN useradd --create-home appuser
USER appuser

# Expose the port the app will run on
EXPOSE 8000

# The command to run the application using Gunicorn, a production-grade server.
# It uses 4 Uvicorn workers to handle concurrent requests.
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "main:app"]
```

### Build and Run the Container

From your `backend` directory:

```bash
# Build the image and tag it as 'pdm-app'
docker build -t pdm-app .

# Run the container, passing in environment variables
docker run -d --name pdm-container \
  -p 8000:8000 \
  -e SECRET_KEY="a_valid_production_secret" \
  -e DATABASE_URL="sqlite:///./pdm.db" \
  pdm-app
```

- `-d`: Run in detached (background) mode.
- `--name`: Give the container a friendly name.
- `-p 8000:8000`: Map port 8000 on your host to port 8000 in the container.
- `-e`: Set an environment variable inside the container.

You can now access your app at `http://localhost:8000`, but this time it's running inside a completely isolated Docker container\!

- **Check logs**: `docker logs pdm-container`
- **Stop and remove**: `docker stop pdm-container && docker rm pdm-container`

---

## 11.3: Migrating to PostgreSQL

JSON files were great for development, but for a production application that needs to handle multiple users safely, we need a real database. PostgreSQL is a powerful, open-source relational database.

### Install Dependencies

```bash
pip install sqlalchemy psycopg2-binary alembic
pip freeze > requirements.txt
```

- **SQLAlchemy**: The most popular Object-Relational Mapper (ORM) for Python. It lets us interact with the database using Python classes instead of raw SQL.
- **psycopg2-binary**: The driver that allows Python to communicate with PostgreSQL.
- **Alembic**: A database migration tool for SQLAlchemy. It manages changes to your database schema over time.

### Create Database Models

Create `backend/models.py`. These Python classes will define our database tables.

```python
# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="user")

class FileLock(Base):
    __tablename__ = "file_locks"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    locked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    message = Column(Text)

    user = relationship("User")
```

### Configure Alembic for Migrations

Database schemas evolve. Migrations are like version control for your database.

1.  **Initialize Alembic** (run once in the `backend` directory):
    ```bash
    alembic init alembic
    ```
2.  **Configure `alembic/env.py`**:
    - Import your models and settings:
      ```python
      from config import settings
      from models import Base
      target_metadata = Base.metadata
      ```
    - Find the `sqlalchemy.url` line and change it to use your settings:
      ```python
      config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
      ```
3.  **Generate your first migration**:
    ```bash
    alembic revision --autogenerate -m "Create initial tables"
    ```
    This will inspect your `models.py` and create a new migration script in `alembic/versions/`.
4.  **Apply the migration**:
    ```bash
    alembic upgrade head
    ```
    This runs the script and creates the tables in your database.

---

## 11.4: Docker Compose for Multi-Container Orchestration

Our application now has multiple parts: the Python app and a PostgreSQL database. **Docker Compose** lets us define and run this entire stack with a single command.

### Create `docker-compose.yml`

Create this file in your project root (`pdm-tutorial/`).

```yaml
# pdm-tutorial/docker-compose.yml
version: "3.9"

services:
  # The PostgreSQL Database Service
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=pdm_user
      - POSTGRES_PASSWORD=pdm_pass
      - POSTGRES_DB=pdm_db
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U pdm_user -d pdm_db"]
      interval: 5s
      timeout: 5s
      retries: 5

  # The FastAPI Application Service
  app:
    build: ./backend
    volumes:
      - git_data:/app/git_repo
    ports:
      - "8000:8000"
    environment:
      # This uses the 'db' service name as the hostname, which Docker Compose resolves internally
      - DATABASE_URL=postgresql://pdm_user:pdm_pass@db:5432/pdm_db
      - SECRET_KEY=${SECRET_KEY} # Will read from your .env file
    depends_on:
      db:
        condition: service_healthy # Waits for the db healthcheck to pass

    # Run Alembic migrations on startup
    command: bash -c "alembic upgrade head && gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app"

  # The Nginx Reverse Proxy Service
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro # Mount the config file
      - ./backend/static:/usr/share/nginx/html/static:ro # Serve static files directly
    depends_on:
      - app

# Define named volumes for data persistence
volumes:
  postgres_data:
  git_data:
```

### Nginx Configuration

Create `pdm-tutorial/nginx.conf`:

```nginx
events {}
http {
    server {
        listen 80;

        # Serve static files directly for performance
        location /static/ {
            alias /usr/share/nginx/html/static/;
        }

        # Proxy WebSocket connections
        location /ws {
            proxy_pass http://app:8000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }

        # Proxy all other requests to the FastAPI app
        location / {
            proxy_pass http://app:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

### Run the Full Stack

From your project root (`pdm-tutorial/`), where `docker-compose.yml` is located:

```bash
# Start all services in the background
docker-compose up -d

# View the logs of a specific service
docker-compose logs -f app

# Stop and remove all containers, networks, and volumes
docker-compose down -v
```

You can now access your application on `http://localhost`, and Nginx will correctly route requests to either the static files or the FastAPI application container.

---

## Stage 11 Complete - You're Production Ready\!

You have successfully transformed your application from a simple local script into a robust, containerized, multi-service system ready for production deployment.

### What You Built

- A 12-Factor-compliant configuration system using environment variables.
- A multi-stage `Dockerfile` for a lean, secure production image.
- A `docker-compose.yml` file to orchestrate your app, database, and web server.
- A production-grade PostgreSQL database with schema migrations managed by Alembic.
- An Nginx reverse proxy for high-performance static file serving and request routing.

### What's Next?

Your application is now fully architected. The next stages would focus on deploying this to the cloud, adding advanced features, and enhancing observability. Potential next steps include:

- **Stage 12: HTTPS & SSL/TLS**: Securing your Nginx proxy with free certificates from Let's Encrypt.
- **Stage 13: Caching with Redis**: Improving performance by caching database queries and other expensive operations.
- **Stage 14: Deployment to the Cloud**: Deploying your Docker Compose stack to a cloud provider like DigitalOcean, AWS, or Google Cloud.
