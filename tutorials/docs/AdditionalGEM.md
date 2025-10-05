# PDM Tutorial (New Format) - Stage 0: The Professional Environment

**Goal**: To set up a professional, scalable, and maintainable project environment from day one. We will not just run commands; we will understand _why_ each part of this structure is an industry best practice.

**What You'll Learn**:

- The "why" behind professional Python project layouts.
- How virtual environments work to prevent dependency chaos.
- The fundamentals of Python's import system.
- The power of modern Python features like Type Hints and `pathlib`.
- The basics of Git for version control.

---

## 0.1: Laying the Foundation - Project Structure

First, we create our project's folder structure. A clean structure is like the foundation of a house; getting it right from the start prevents major headaches later.

### Your Turn: Create the Directory Tree

- Open your terminal or command prompt.
- Navigate to where you want to store your projects (e.g., `Documents/Projects`).
- Run these commands one by one:

```

  # 1. Create the main project folder and enter it
  mkdir pdm-tutorial
  cd pdm-tutorial

  # 2. Create the main 'backend' folder
  mkdir backend
  cd backend

  # 3. Create the Python application package folder
  mkdir app

  # 4. Create folders for static assets (HTML, CSS, JS)
  mkdir -p static/css
  mkdir -p static/js/modules

  # 5. Create the testing folder
  mkdir tests

  # 6. Create essential starting files (they can be empty for now)
  touch app/__init__.py
  touch app/main.py
  touch static/index.html
  touch static/js/app.js
  touch .env.example
  touch .gitignore
  touch ../README.md
```

You should now have a structure that looks like this:

```
pdm-tutorial/
├── backend/
│  ├── app/
│  │  ├── __init__.py
│  │  └── main.py
│  ├── static/
│  │  ├── css/
│  │  ├── js/
│  │  │  └── modules/
│  │  └── index.html
│  ├── tests/
│  ├── .env.example
│  └── .gitignore
└── README.md
```

### Deep Dive: The "Why" Behind This Structure

- `pdm-tutorial/`: The **root** of our entire project. The `.git` repository will live here.
- `backend/`: This folder contains everything related to our Python server application. It separates our backend code from other potential top-level folders like `documentation/` or `mobile-app/`.
- `app/`: This is our main **Python package**. The `app/__init__.py` file, even if empty, is a magic file that tells Python, "This folder is a package, and you can import code from it." This is what allows clean imports like `from app.services import ...`.
- `static/`: This folder will hold all files that are served directly to the user's browser without being processed by Python: HTML, CSS, JavaScript, images, etc.
- `tests/`: A dedicated place for our automated tests. Professional projects always have tests. Keeping them separate from the application code is standard practice.
- `.gitignore`: A crucial file that tells Git which files and folders to **ignore** (e.g., temporary files, virtual environments, secret keys).
- `.env.example`: A template for our configuration file. It shows other developers what environment variables are needed to run the app, but it contains no secret values. The actual secrets will go in a `.env` file, which will be ignored by Git.

---

## 0.2: The Isolated Toolbox - Virtual Environments

Before we install any Python packages (like FastAPI), we need to create a **virtual environment**.

### Deep Dive: What is a `venv`?

Think of a virtual environment as a clean, isolated toolbox for a single project. 🧰

- **Without a `venv`**: Every package you install (`pip install fastapi`) goes into a single, global collection on your computer. If Project A needs `library v1.0` and Project B needs `library v2.0`, you have a conflict\! This is often called "dependency hell."
- **With a `venv`**: Each project gets its own private `venv` folder containing its own Python interpreter and its own set of installed libraries. Project A can have `library v1.0` and Project B can have `library v2.0` without ever conflicting.

This is a non-negotiable best practice in modern Python development.

### Your Turn: Create and Activate Your `venv`

- Make sure you are inside the `backend` directory in your terminal.

- Run the command to create the virtual environment. This creates a new folder named `venv`.

```bash
  python -m venv venv
```

- **Activate** the environment. This tells your terminal session to use this project's specific Python toolbox instead of the global one.

**On macOS/Linux:**

```bash
  source venv/bin/activate
```

**On Windows (PowerShell):**

```bash
  .\venv\Scripts\Activate.ps1
```

_(Note: If you get an error on Windows, you may need to run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first.)_

**Verification**: You'll know it's active because your terminal prompt will change to show `(venv)` at the beginning.

_Before_: `PS C:\Users\You\pdm-tutorial\backend>`
_After_: `(venv) PS C:\Users\You\pdm-tutorial\backend>`

From now on, always make sure your `venv` is active before running any Python or `pip` commands for this project. To deactivate, simply type `deactivate`.

**Further Reading**: [Python `venv` Documentation](<https://www.google.com/search?q=%5Bhttps://docs.python.org/3/library/venv.html%5D(https://docs.python.org/3/library/venv.html)>)

---

## 0.3: The Rulebook - Package Management

A `requirements.txt` file is your project's "shopping list." It lists all the external Python packages your project needs to run. This allows any developer to set up an identical environment by running a single command.

### Your Turn: Create and Install Requirements

- Create the `backend/requirements.txt` file.

- Add our first two dependencies. The `==` pins the version, ensuring the project works the same way for everyone, everywhere.

  **File: `backend/requirements.txt`**

```
# Core web framework
fastapi==0.104.1

# Asynchronous server to run FastAPI
uvicorn[standard]==0.24.0
```

- **FastAPI**: The modern, high-performance web framework we'll use to build our API.
- **Uvicorn**: The lightning-fast server that runs our FastAPI application.

- Now, with your `venv` active, install these packages from your requirements file.

```bash
pip install -r requirements.txt
```

- **Verification**: You'll see `pip` download and install the packages and their dependencies. You can confirm they're installed by running:

```bash
pip freeze
```

This command lists all packages installed in your current (virtual) environment. You should see `fastapi==0.104.1` and `uvicorn==0.24.0` in the list.

---

## 0.4: First Contact - Git Version Control

**Git** is the industry-standard **Version Control System (VCS)**. Think of it as an infinite "undo" button for your entire project, but much more powerful. It tracks every change, lets you work on features in parallel (branches), and collaborates with others without overwriting work.

### Your Turn: Initialize Your Repository

- Navigate to the **root** of your project, the `pdm-tutorial` folder.

- **Configure Git** with your name and email. This is important because every change (commit) you make will be stamped with this information.

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

- **Initialize the repository**. This command creates a hidden `.git` folder in your project root. This folder is the "brain" of Git, where it stores all the history and tracking information.

```bash
git init
```

### Your Turn: Configure `.gitignore`

Now, we tell Git what _not_ to track. This is critical for security and for keeping your repository clean.

- Open the `.gitignore` file you created earlier in the `backend` directory.

- Add the following rules. Read the comments to understand what each section does.

  **File: `backend/.gitignore`**

```
# Python temporary files
__pycache__/
*.pyc
*.pyo
*.pyd

# Virtual Environment - Never commit this! It's huge and machine-specific.
venv/

# Environment variables - Contains secrets! NEVER commit this.
.env

# IDE/Editor specific files
.vscode/
.idea/
*.swp
*.swo

# OS-specific files
.DS_Store
Thumbs.db

# Project-specific generated files
# The locks.json file represents runtime state, not source code.
locks.json
users.json
audit.json
messages.json
# We will track our repository files in a separate Git repo later (GitLab)
repo/
gitlab_repo_clone/
git_repo/
```

### Your Turn: Make Your First Commit

A **commit** is a snapshot of your project at a specific point in time. Let's save the initial structure we've built.

- **Stage** your changes. This tells Git, "I want to include these changes in my next snapshot." The `.` means "all changes in the current directory and subdirectories."

```bash
# Make sure you are in the pdm-tutorial root folder
git add .
```

- **Commit** your staged changes. The `-m` flag provides a descriptive message explaining what this snapshot contains. Commit messages are crucial for understanding the project's history.

```bash
git commit -m "Initial commit: Set up professional project structure and environment"
```

- **Verification**: Run `git log`. You will see your first commit, complete with your name, email, date, and message. Congratulations, your project history has officially begun\! 🚀

---

## Stage 0 Complete ✓

You've successfully set up a professional development environment. This is a huge first step that many tutorials skip, but it will pay dividends in maintainability and scalability.

### Verification Checklist

- [ ] Your project has the correct folder structure.
- [ ] You have a `venv` folder inside `backend/`.
- [ ] Your terminal prompt shows `(venv)` when in the `backend` directory.
- [ ] `pip freeze` shows `fastapi` and `uvicorn` are installed.
- [ ] You have a `.git` folder in your `pdm-tutorial` root.
- [ ] `git log` shows your initial commit.

You have learned the fundamentals of project structure, dependency isolation, and version control. You're no longer just writing scripts; you're starting to engineer a software project.

Ready to write our first line of code in Stage 1?

Excellent\! Let's get started on Stage 1. We'll build our first backend server, but more importantly, we'll take the time to understand the fundamental technologies that make it work: the HTTP protocol, the ASGI standard, and the Pydantic data validation library.

---

# PDM Tutorial (New Format) - Stage 1: Your First Professional API

**Goal**: To build a functional, well-organized FastAPI backend. We'll move from theory to a running server with live API endpoints and automatic interactive documentation.

**What You'll Learn**:

- The difference between synchronous (WSGI) and asynchronous (ASGI) web servers, and why FastAPI is so fast.
- The fundamentals of the HTTP protocol: methods, status codes, and headers.
- How to use **Pydantic** to define strict "data contracts" for your API.
- How to create a scalable API structure using **Routers**.
- How FastAPI uses your Python code to automatically generate interactive API documentation.

---

## 1.1: The "Need for Speed" - ASGI vs. WSGI

Before we write our server, let's understand the engine that powers it. For years, Python web servers used WSGI (Web Server Gateway Interface), which is **synchronous**. Think of it like a single-lane checkout at a grocery store; the cashier must finish with one customer completely before starting with the next. If one customer is slow, everyone behind them waits.

FastAPI uses a newer standard called ASGI (Asynchronous Server Gateway Interface). Think of this like a barista at a coffee shop. ☕

- Customer A orders a latte (a slow operation, like waiting for a database).
- The barista starts the latte machine (`await db.query()`).
- Instead of staring at the machine, the barista immediately takes Customer B's order.
- When the latte is ready, the barista serves Customer A.

This non-blocking approach allows a single worker to handle many connections concurrently, making it incredibly efficient for I/O-bound tasks (like web APIs that talk to databases, files, or other services).

### Your Turn: Explore the Concepts

**Assumptions / quick notes**

- Python 3.8+ recommended (3.11+ is better).
- If you use an interactive REPL: IPython or `python -m asyncio` / IPython supports top-level `await`. Regular `python` script requires `asyncio.run(...)`.
- File name suggestions: `async_demo_step1.py`, `async_demo_step2.py`, etc. Type each short snippet, run it, then continue.

# Step 0 — quick setup

Type this first in a new file or REPL.

```py
# Step0_setup.py
import asyncio
import time     # used in sync examples
```

**Why**: `asyncio` is the event loop library. `time` shows blocking behavior.

---

# Step 1 — synchronous blocking demo (WSGI style)

Type and run this block as a script.

```py
# Step1_sync.py (type this)
import time

def synchronous_task(name, wait_time):
  print(f"Task {name}: start ({wait_time}s)")
  time.sleep(wait_time)     # BLOCKS the whole thread
  print(f"Task {name}: done")

def run_synchronous_demo():
  print("Synchronous demo start")
  t0 = time.time()
  synchronous_task("A", 2)
  synchronous_task("B", 1)
  print("Total:", time.time() - t0)

if __name__ == "__main__":
  run_synchronous_demo()
```

**What you’ll see**

```
Synchronous demo start
Task A: start (2s)
Task A: done
Task B: start (1s)
Task B: done
Total: ~3.00
```

**Why / concept**

- `time.sleep()` blocks the OS thread. Nothing else runs while sleeping.
- This models **WSGI** server behavior where each request handler blocks a worker thread/process; concurrent requests require multiple workers.

**Side note**: Blocking I/O in web servers forces you to add processes/threads to get concurrency — wasteful for many concurrent network-bound tasks.

---

# Step 2 — asynchronous coroutines (ASGI style)

Now type the async version (use a new file or REPL cell). Run with `python step2_async.py` **or** in REPL use `await run_asynchronous_demo()` (IPython).

```py
# Step2_async.py
import asyncio
import time

async def asynchronous_task(name, wait_time):
  print(f"Task {name}: start ({wait_time}s)")
  await asyncio.sleep(wait_time)  # NON-blocking: yields control to event loop
  print(f"Task {name}: done")

async def run_asynchronous_demo():
  print("Asynchronous demo start")
  t0 = time.time()
  await asyncio.gather(
    asynchronous_task("C", 2),
    asynchronous_task("D", 1)
  )
  print("Total:", time.time() - t0)

if __name__ == "__main__":
  asyncio.run(run_asynchronous_demo())
```

**What you’ll see**

```
Asynchronous demo start
Task C: start (2s)
Task D: start (1s)
Task D: done
Task C: done
Total: ~2.00
```

**Why / concept**

- `async def` declares a coroutine function. Calling it returns a coroutine object; `await` suspends the coroutine and lets other coroutines run.
- `asyncio.sleep` is non-blocking — it schedules a wake-up with the loop, letting other tasks run in the meantime.
- `asyncio.gather` runs coroutines concurrently (not parallel). The total time ≈ longest task, not sum.

**Gotcha**: `await` does _not_ spawn a new OS thread. It yields to the loop; concurrency is cooperative.

---

# Step 3 — `create_task` vs `gather`

Type this to see different behaviors and why you'd use one or the other.

```py
# Step3_create_vs_gather.py
import asyncio, time

async def t(name, delay):
  print(f"{name} start")
  await asyncio.sleep(delay)
  print(f"{name} end")
  return name

async def demo():
  # create_task launches tasks that run concurrently and are not automatically awaited
  task1 = asyncio.create_task(t("T1", 2))
  task2 = asyncio.create_task(t("T2", 1))

  # do other work while tasks run
  print("Doing other work between scheduling and awaiting")
  await asyncio.sleep(0.2)

  # await both results — here we wait for both; gather could also be used
  results = await asyncio.gather(task1, task2)
  print("Results:", results)

asyncio.run(demo())
```

**Why / concept**

- `create_task` schedules execution immediately; it returns an `asyncio.Task` object you can hold on to.
- `gather` is best when you want to start and wait for multiple coroutines in one step.
- If you `create_task` and forget to await (or monitor) it, the program might exit with unfinished tasks or they may run in background (depending on loop/host). Always manage tasks (await, cancel, or add callbacks).

**Side note**: `asyncio.create_task` is the “spawn” primitive; `gather` is a convenience to await many things.

---

# Step 4 — I/O-bound vs CPU-bound & `run_in_executor`

**Important rule**: use `async/await` for _I/O-bound_ concurrency. For CPU heavy tasks, use threads/processes.

Type this snippet to offload CPU-bound work without blocking the loop.

```py
# Step4_executor.py
import asyncio, time
from concurrent.futures import ThreadPoolExecutor

def cpu_heavy(n):
  # blocking CPU-bound task (fake work)
  s = 0
  for i in range(10_000_000):
    s += (i % n)
  return s

async def main():
  loop = asyncio.get_running_loop()
  t0 = time.time()
  # run cpu_heavy in threadpool to avoid blocking the event loop
  result = await loop.run_in_executor(None, cpu_heavy, 7) # None = default ThreadPoolExecutor
  print("CPU result:", result, "took", time.time() - t0)

asyncio.run(main())
```

**Why / concept**

- `run_in_executor` schedules blocking work in a thread (or process) pool so the event loop remains responsive.
- Use `concurrent.futures.ProcessPoolExecutor` for CPU-bound tasks if Python’s GIL is a bottleneck.

**Gotcha**: spinning threads unconstrained can lead to context switching overhead. Tune your pool size.

---

# Step 5 — timeouts and cancellation

Type and run this small example to see cancellation and `asyncio.wait_for`.

```py
# Step5_timeout.py
import asyncio

async def slow():
  try:
    await asyncio.sleep(5)
    return "done"
  except asyncio.CancelledError:
    print("slow: cancelled")
    raise

async def main():
  try:
    # cancel if not done in 1 second
    result = await asyncio.wait_for(slow(), timeout=1.0)
    print("Result:", result)
  except asyncio.TimeoutError:
    print("Timed out!")

asyncio.run(main())
```

**What you’ll see**

```
Timed out!
slow: cancelled
```

**Why / concept**

- `asyncio.wait_for` raises `asyncio.TimeoutError` and cancels the wrapped task.
- Proper coroutine code should handle `CancelledError` for cleanup if needed.

---

# Step 6 — quick mapping to FastAPI / ASGI

A minimal FastAPI app illustrating async vs sync endpoints. Type this into `app.py` and run with `uvicorn app:app --reload`.

```py
# app.py
from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/sync")
def sync_endpoint():
  time.sleep(2)     # blocks the worker (thread/process)
  return {"type": "sync", "msg": "finished"}

@app.get("/async")
async def async_endpoint():
  await asyncio.sleep(2) # yields to event loop — other requests handled concurrently
  return {"type": "async", "msg": "finished"}
```

**Why / concept**

- ASGI (Uvicorn/Hypercorn) uses an event loop; `async def` endpoints allow high concurrency for network I/O.
- `sync` endpoints are run in a threadpool by FastAPI/Starlette by default — they block that worker thread while running.
- **Scaling note**: uvicorn `--workers N` spawns N OS processes; each has its own event loop and threadpool. Use processes for CPU-bound scale-out.

---

# Step 7 — debugging tips and tooling

- `PYTHONASYNCIODEBUG=1` or `asyncio.get_event_loop().set_debug(True)` — more verbose loop diagnostics.
- `asyncio.all_tasks()` inside loop (or `asyncio.Task.all_tasks()` in older versions) shows outstanding tasks.
- Use logging rather than `print` for production tracing.
- Use `trio` or `anyio` for alternative structured concurrency models (optional advanced).

---

# Common gotchas (short)

- `time.sleep()` vs `asyncio.sleep()` — don’t mix them inside coroutines.
- Forgetting to `await` a coroutine: calling `async def f(): ...; f()` returns coroutine object and does nothing until awaited/scheduled.
- Unhandled `CancelledError` may swallow cleanup; handle it if necessary.
- `await` inside a for-loop is sequential; use `gather` to run things concurrently.
- `asyncio.run` cannot be called when an event loop is already running (e.g., inside some REPLs); use `await` in IPython or `nest_asyncio` only if you really know what you’re doing.

---

# Playground exercises (type them and run; solutions follow)

- **Convert** the synchronous demo (`Step1_sync`) to an async version step-by-step and show total time is max, not sum. (You did this earlier — retype to reinforce.)
- **Forget-to-await**: create an `async def f(): ...` then call it without `await` — inspect the returned object and explain.
- **Parallel fetch simulation**: simulate 5 network calls using `asyncio.sleep` and run them concurrently with a concurrency limit of 2.
- **CPU offload**: run a small CPU-bound function 4x concurrently using `run_in_executor` and measure elapsed time vs running them sequentially.
- **FastAPI concurrency test**: run the `app.py` from Step 6 and `curl` both endpoints simultaneously — compare behavior.

---

# Solutions (concise)

### Ex 2 (forget-to-await)

```py
async def say():
  print("hello")
  await asyncio.sleep(0.1)
  print("bye")

coro = say()         # returns coroutine object
print(coro)         # <coroutine object say at 0x...>
# nothing runs until you await or schedule:
asyncio.run(say())      # correct way
# or schedule: t = asyncio.create_task(say())
```

### Ex 3 (concurrency limit: semaphore)

```py
import asyncio, time
async def fake_network(i):
  print("start", i)
  await asyncio.sleep(1)  # simulate IO
  print("end", i)
  return i

async def limited_run(tasks, limit=2):
  sem = asyncio.Semaphore(limit)
  async def worker(i):
    async with sem:
      return await fake_network(i)
  return await asyncio.gather(*(worker(i) for i in tasks))

async def main():
  t0 = time.time()
  res = await limited_run(range(5), limit=2)
  print("done", res, "took", time.time()-t0)

asyncio.run(main())
```

### Ex 4 (run_in_executor)

```py
from concurrent.futures import ThreadPoolExecutor
import asyncio, time

def cpu_task(n):
  s=0
  for i in range(5_000_000):
    s += i % n
  return s

async def main():
  loop = asyncio.get_running_loop()
  t0 = time.time()
  # run 4 CPU tasks concurrently in threadpool
  futs = [loop.run_in_executor(None, cpu_task, x) for x in (2,3,4,5)]
  results = await asyncio.gather(*futs)
  print("took", time.time()-t0, results)

asyncio.run(main())
```

- Running sequentially would take ~4× time; in threadpool they overlap on IO/blocked times but CPU still competes for cores — use process pool for true parallel CPU work.

---

# Final checklist — short cheatsheet

- Use async for I/O-bound concurrency.
- Use `asyncio.sleep` in tests (never `time.sleep`).
- `asyncio.create_task` schedules; `await` waits.
- Use `run_in_executor` (thread/process) for blocking or CPU tasks.
- Handle `CancelledError` / use `wait_for` for timeouts.
- For web apps: prefer `async def` endpoints for I/O work; sync endpoints run in threadpool and block that worker.

---

Create this educational file to see the concepts in code. This file is for learning only and won't be part of our final app.

**File: `backend/app/learn_asgi.py`**

```python
"""
Understanding ASGI (Asynchronous Server Gateway Interface)
and the 'async' and 'await' keywords in Python.
"""
import asyncio

# ============================================================================
# CONCEPT 1: Synchronous Code (The "Old Way" - WSGI)
# ============================================================================

def synchronous_task(name, wait_time):
  """A task that blocks everything while it runs."""
  import time
  print(f"Task '{name}': Starting, will take {wait_time}s.")
  time.sleep(wait_time) # This is a blocking call. Nothing else can happen.
  print(f"Task '{name}': Finished.")

def run_synchronous_demo():
  print("\n--- Running Synchronous Demo (like WSGI) ---")
  start_time = time.time()
  synchronous_task("A", 2) # Runs and finishes completely...
  synchronous_task("B", 1) # ...before this one can even start.
  duration = time.time() - start_time
  print(f"Total time: {duration:.2f}s (Expected: 2 + 1 = 3s)")

# ============================================================================
# CONCEPT 2: Asynchronous Code (The "New Way" - ASGI)
# ============================================================================

async def asynchronous_task(name, wait_time):
  """
  An 'async' function is a coroutine. It can be paused and resumed.
  'await' is the pause point. It says "this might take a while,
  so let the event loop run other tasks in the meantime."
  """
  print(f"Task '{name}': Starting, will take {wait_time}s.")
  await asyncio.sleep(wait_time) # This is a NON-blocking call.
  print(f"Task '{name}': Finished.")

async def run_asynchronous_demo():
  print("\n--- Running Asynchronous Demo (like ASGI) ---")
  start_time = time.time()
  # asyncio.gather runs multiple coroutines concurrently.
  await asyncio.gather(
    asynchronous_task("C", 2),
    asynchronous_task("D", 1)
  )
  duration = time.time() - start_time
  # The total time is determined by the LONGEST task, not the sum.
  print(f"Total time: {duration:.2f}s (Expected: max(2, 1) = 2s)")

# ============================================================================
# CONCEPT 3: When to Use `async/await`
# ============================================================================
"""
Rule of Thumb: Use `async/await` for I/O-bound operations.
- I/O-bound: Waiting for something external (network, database, file system). Your CPU is idle.
- CPU-bound: Heavy computation (math, complex loops). Your CPU is busy.

GOOD uses for async/await (I/O-bound):
- `await db.fetch_data()`  # Waiting for a database
- `await client.get(...)`  # Waiting for another API
- `await file.read()`    # Waiting for the hard drive

BAD uses for async/await (CPU-bound):
- `result = heavy_math_calculation()` # This blocks anyway, async provides no benefit.
 For CPU-bound tasks in FastAPI, you run them in a separate thread pool.
"""

if __name__ == "__main__":
  run_synchronous_demo()

  # To run async code, you need an event loop.
  asyncio.run(run_asynchronous_demo())

```

- Save the code above in `backend/app/learn_asgi.py`.
- From your `backend` directory (with `venv` active), run it:

```bash
python -m app.learn_asgi
```

- **Observe the output.** Notice how the synchronous tasks run one after another, taking 3 seconds total. The asynchronous tasks effectively run at the same time, taking only 2 seconds (the length of the longest task). This is the magic of ASGI.

---

## 1.2: The Language of the Web - The HTTP Protocol

Before building an API, you need to understand the language it speaks: **HTTP (HyperText Transfer Protocol)**. It's a simple request-response protocol.

- Your browser (**client**) sends an **HTTP Request** to a server.
- The **server** processes the request and sends back an **HTTP Response**.

### Your Turn: Explore the Concepts

Create this second educational file. It explains the parts of an HTTP request and the conventions we'll be using.

**File: `backend/app/learn_http.py`**

```python
"""
Understanding HTTP - The protocol that powers the web.
"""

# ============================================================================
# SECTION 1: HTTP Request Structure
# ============================================================================
"""
An HTTP request is just plain text with four parts:

- REQUEST LINE: What do you want?
  GET /api/files HTTP/1.1
  │  └─ Path/Endpoint (the resource you want)
  └─ Method/Verb (the action you want to perform)

- HEADERS: Who are you and what are your preferences? (Key-Value metadata)
  Host: localhost:8000
  Accept: application/json
  Authorization: Bearer <your_login_token>

- BLANK LINE: A single blank line separates headers from the body.

- BODY: Here's the data you need for the request. (Optional, for POST/PUT/PATCH)
  {"filename": "new_part.mcam", "user": "alice"}
"""

# ============================================================================
# SECTION 2: The 5 Most Common HTTP Methods (Verbs)
# ============================================================================
"""
RESTful APIs use these methods with conventional meanings:

- GET:  "GIVE ME data." (Retrieve a resource or list of resources)
- POST:  "CREATE a new resource with this data."
- PUT:  "REPLACE a resource completely with this data."
- PATCH: "UPDATE part of a resource with this data."
- DELETE: "DELETE this resource."
"""

# ============================================================================
# SECTION 3: HTTP Status Codes (The Server's Reply)
# ============================================================================
"""
The server's response starts with a status code to tell you what happened.

- 2xx (Success): Everything worked!
 - 200 OK: Standard success.
 - 201 Created: You sent a POST request and a new resource was created.
 - 204 No Content: Success, but I have nothing to send back (common for DELETE).

- 4xx (Client Error): YOU did something wrong.
 - 400 Bad Request: Your request was malformed or the data was invalid.
 - 401 Unauthorized: You aren't logged in.
 - 403 Forbidden: You are logged in, but you don't have permission to do this.
 - 404 Not Found: The resource you asked for doesn't exist.
 - 422 Unprocessable Entity: Your data was well-formed, but failed validation (e.g., email format wrong). FastAPI uses this a lot.

- 5xx (Server Error): *I* did something wrong.
 - 500 Internal Server Error: A generic error for an unexpected crash in my code.
"""

if __name__ == "__main__":
  print("HTTP concepts explained. No code to run.")
  print("These concepts are the foundation for the API endpoints we are about to build.")
```

- Save the code in `backend/app/learn_http.py`.
- You can run it (`python -m app.learn_http`) to see the printout, but the value is in reading and understanding the concepts within the file.

---

## 1.3: The Data Bouncer - Pydantic Schemas

How do we ensure the data sent to our API (like a JSON body) is in the correct format? We use **Pydantic**. Pydantic uses Python's type hints to create strict "data contracts" or **schemas**.

Think of Pydantic as a bouncer at the door of your API endpoint. 👮
It checks the "ID" (data) of every request. If the data doesn't match the guest list (the schema), it's rejected with a helpful `422 Unprocessable Entity` error explaining exactly what's wrong. This eliminates a massive category of bugs at the boundary of your application.

### Your Turn: Explore Pydantic

Create this file to see Pydantic's power in action.

**File: `backend/app/learn_pydantic.py`**

```python
"""
Pydantic: Data validation using Python type hints.
FastAPI uses Pydantic for everything related to data shape.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional

# ============================================================================
# SECTION 1: A Basic Model
# ============================================================================
class User(BaseModel):
  """A Pydantic model defines the 'shape' of your data."""
  username: str
  email: str
  age: int
  is_active: bool = True # You can provide default values
  full_name: Optional[str] = None # 'Optional' means it can be None

# --- Testing the basic model ---
print("--- Pydantic Basic Validation ---")
# This works: data matches the schema
user_data = {"username": "alice", "email": "alice@example.com", "age": 30}
valid_user = User(**user_data)
print(f"Valid user created: {valid_user.username}")

# This fails: 'age' is a string, not an integer
try:
  invalid_data = {"username": "bob", "email": "bob@example.com", "age": "thirty"}
  User(**invalid_data)
except Exception as e:
  print(f"\nValidation failed as expected!")
  print(e)

# ============================================================================
# SECTION 2: Advanced Validation with `Field`
# ============================================================================
class FileCheckoutRequest(BaseModel):
  """
  A more realistic model for our app.
  `Field` lets us add constraints beyond just the type.
  """
  filename: str = Field(
    ..., # The ellipsis (...) means this field is required
    min_length=3,
    max_length=255,
    pattern=r"^[\w\-. ]+\.mcam$" # Regex: must end in .mcam
  )
  message: str = Field(..., min_length=10)

  # A custom validator
  @validator('filename')
  def filename_must_not_contain_paths(cls, v):
    if '/' in v or '\\' in v or '..' in v:
      raise ValueError('Filename cannot contain path separators')
    return v

# --- Testing the advanced model ---
print("\n--- Pydantic Advanced Validation ---")
# This fails our custom validator
try:
  attack_data = {"filename": "../etc/passwd", "message": "A valid message."}
  FileCheckoutRequest(**attack_data)
except Exception as e:
  print("Blocked a directory traversal attempt!")
```

- Save this code in `backend/app/learn_pydantic.py`.
- Run it from the `backend` directory:

```bash
python -m app.learn_pydantic
```

- **Observe the output.** See how Pydantic automatically catches the wrong data type for `age` and how our custom validator prevents a potential security risk. This is why FastAPI is so robust.

---

## 1.4: Building the Application Core

Enough theory\! Let's build our server. We will follow a professional pattern where `main.py` is a thin "entry point" that wires everything together, and the actual logic lives in other files.

### Your Turn: Create the Configuration

First, a place for our settings. This avoids hardcoding values in our code.

**File: `backend/app/config.py`**

```python
"""
Application Configuration

Uses Pydantic to create a type-safe settings object. It will automatically
load settings from a .env file or environment variables.
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  APP_NAME: str = "PDM Backend API"
  APP_VERSION: str = "0.1.0"

  class Config:
    env_file = ".env" # Specifies that we can use a .env file

# Create a single, importable instance of the settings
settings = Settings()
```

### Your Turn: Create the Main App Entry Point

Now, let's create the main application file.

**File: `backend/app/main.py`**

```python
"""
Main FastAPI application entry point.
This file should be kept thin. Its job is to:
- Create the FastAPI app instance.
- Configure middleware (like CORS).
- Include API routers from other files.
- Define startup/shutdown events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# --- Application Factory Pattern ---
def create_application() -> FastAPI:
  """Creates and configures the FastAPI application instance."""

  app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Parts Data Management System - A collaborative file locking system.",
  )

  # --- Middleware: CORS ---
  # Cross-Origin Resource Sharing (CORS) is a security feature browsers use.
  # It prevents a web page from making requests to a different domain.
  # We need to explicitly tell our backend that it's OK to accept
  # requests from our frontend (which will be served from the same server).
  app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, lock this down to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

  # --- Event Handlers ---
  @app.on_event("startup")
  async def startup_event():
    """Code to run when the application starts up."""
    print(f"Starting up {settings.APP_NAME} v{settings.APP_VERSION}...")
    # This is where we will later initialize database connections, etc.

  @app.on_event("shutdown")
  async def shutdown_event():
    """Code to run when the application is shutting down."""
    print("Shutting down...")

  # --- Root Endpoint ---
  @app.get("/")
  def read_root():
    """A simple health-check endpoint."""
    return {
      "status": "ok",
      "name": settings.APP_NAME,
      "version": settings.APP_VERSION,
    }

  return app

# Create the application instance by calling the factory
app = create_application()
```

### Your Turn: Run the Server\!

- Make sure you are in the `backend` directory with your `venv` active.

- Run Uvicorn, pointing it to your `app` instance inside `app.main`:

```bash
uvicorn app.main:app --reload
```

- `app.main:app`: Look inside the `app/main.py` file for a variable named `app`.
- `--reload`: This is a magical flag for development. It automatically restarts the server every time you save a code change.

- **Verification**: You will see Uvicorn start up and display something like:
  `Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)`

- Open your web browser and go to **[http://127.0.0.1:8000](https://www.google.com/url?sa=E&source=gmail&q=http://127.0.0.1:8000)**. You should see the JSON response from your `read_root` function\!

```json
{ "status": "ok", "name": "PDM Backend API", "version": "0.1.0" }
```

You now have a running web server\! Keep it running; `--reload` will handle the rest.

---

## 1.5: Organizing with Routers and Schemas

As our app grows, putting all endpoints in `main.py` becomes messy. We'll organize our code by feature. All file-related endpoints will live in their own file.

### Your Turn: Create the Data Schemas

First, let's define the Pydantic models (schemas) for our file data.

- Create the file `backend/app/schemas/files.py`.

- Add the models that define what a "file" looks like in our API.

  **File: `backend/app/schemas/files.py`**

```python
"""
Pydantic schemas for file operations.
These define the shape of our API's input and output data.
"""
from pydantic import BaseModel, Field
from typing import Optional, List

class FileInfo(BaseModel):
  """Represents the data for a single file sent to the client."""
  name: str
  status: str
  size_bytes: int
  locked_by: Optional[str] = None

  class Config:
    # This provides an example for the interactive API docs.
    json_schema_extra = {
      "example": {
        "name": "PN1001_OP1.mcam",
        "status": "available",
        "size_bytes": 1234567,
        "locked_by": None
      }
    }

class FileListResponse(BaseModel):
  """The response model for the endpoint that lists all files."""
  files: List[FileInfo]
  total: int
```

### Your Turn: Create the API Router

Now, create the file that will contain our file-related API endpoints.

- Create the file `backend/app/api/files.py`.

- Add the router and our first real endpoints, using the schemas we just defined.

  **File: `backend/app/api/files.py`**

```python
"""
API endpoints for file management.
This is a 'Router', a self-contained set of routes that can be
included in the main application.
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.files import FileInfo, FileListResponse

# Create a router instance. We can add routes to this just like the app.
router = APIRouter(
  prefix="/api/files", # All routes in this file will start with /api/files
  tags=["Files"],    # Group these endpoints under "Files" in the docs
)

# --- Temporary Mock Data ---
# In Stage 3, we will replace this with real filesystem calls.
MOCK_FILES = [
  {"name": "PN1001_OP1.mcam", "status": "available", "size_bytes": 1234567, "locked_by": None},
  {"name": "PN1002_OP1.mcam", "status": "checked_out", "size_bytes": 2345678, "locked_by": "john"},
  {"name": "PN1003_OP1.mcam", "status": "available", "size_bytes": 987654, "locked_by": None},
]

@router.get("/", response_model=FileListResponse)
def get_files():
  """
  Get a list of all files in the repository.
  The `response_model` tells FastAPI to validate the output against
  our `FileListResponse` schema.
  """
  return FileListResponse(files=MOCK_FILES, total=len(MOCK_FILES))


@router.get("/{filename}", response_model=FileInfo)
def get_file(filename: str):
  """
  Get details for a specific file by its name.
  `filename: str` is a path parameter taken from the URL.
  """
  for file in MOCK_FILES:
    if file["name"] == filename:
      return FileInfo(**file)

  # If the loop finishes without finding the file, raise a 404 error.
  raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"File '{filename}' not found",
  )
```

### Your Turn: Wire It All Together

The final step is to tell our main app to use this new router.

- Open `backend/app/main.py`.

- Import the new router and include it in the app.

```python
# At the top with other imports
from app.api import files

# In your create_application function, after the root endpoint

# --- Include Routers ---
# This line tells the main app to include all the routes
# defined in the 'files' router.
app.include_router(files.router)

return app
```

- **Verification**: Your server (which is still running with `--reload`) should have automatically restarted.

- Go to **[http://127.0.0.1:8000/api/files](https://www.google.com/search?q=http://127.0.0.1:8000/api/files)**. You should see the list of mock files.
- Go to **[http://127.0.0.1:8000/api/files/PN1001_OP1.mcam](https://www.google.com/search?q=http://127.0.0.1:8000/api/files/PN1001_OP1.mcam)**. You should see the details for that single file.
- Go to **[http://127.0.0.1:8000/api/files/fake.mcam](https://www.google.com/search?q=http://127.0.0.1:8000/api/files/fake.mcam)**. You should see a `{"detail":"File 'fake.mcam' not found"}` error with a `404 Not Found` status.

---

## 1.6: The Payoff - Automatic Interactive Docs

Because we used FastAPI with Pydantic and type hints, we get an incredible feature for free: interactive API documentation.

### Your Turn: Explore Your API Docs

- Open your browser to **[http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)**.

You will see a beautiful, interactive Swagger UI page.

- You can see your endpoints grouped under "Files".
- You can expand an endpoint to see its details, including the example response we defined in our Pydantic schema.
- You can click **"Try it out"** and **"Execute"** to run the API endpoints directly from your browser\!

<!-- end list -->

- Now, open **[http://127.0.0.1:8000/redoc](https://www.google.com/search?q=http://127.0.0.1:8000/redoc)** for an alternative, more documentation-focused view.

This is one of the most powerful features of FastAPI. Your documentation is **always** in sync with your code because it's generated _from_ your code.

---

## Stage 1 Complete ✓

You've successfully built a well-structured, running API server with two live endpoints and professional, interactive documentation.

### Verification Checklist

- [ ] The server runs with `uvicorn app.main:app --reload`.
- [ ] The root endpoint (`/`) works.
- [ ] The get all files endpoint (`/api/files`) works and returns a list.
- [ ] The get single file endpoint (`/api/files/{filename}`) works for a real file and returns a 404 for a fake one.
- [ ] The interactive API docs at `/docs` load correctly and let you test the endpoints.

**What You Learned**:

- Why `async` and ASGI make FastAPI fast.
- The fundamental structure of HTTP requests and responses.
- How Pydantic creates robust, self-documenting data schemas.
- How to organize a FastAPI application with `config`, `schemas`, and `api` routers.
- How to automatically generate powerful API documentation from your code.

You're now ready to build the frontend that will consume this API.

Ready for Stage 2?

You are absolutely right. My apologies. That last response fell back into the old "here's the final code" format, which is exactly what you told me you don't want. It's a terrible way to learn, and you're correct to call it out.

Let's start Stage 2 over, and I will make it truly interactive and incremental. We will build each file piece by piece. I will provide a skeleton, you will add code to it, and we will test the changes at every small step. This will be the best way to build muscle memory and understand how the pieces connect.

Thank you for the feedback. Let's do this right.

---

# PDM Tutorial (New Format) - Stage 2: Building the Frontend

**Goal**: To build a dynamic, professional-grade frontend that communicates with our API. We will focus on a scalable CSS architecture and modular JavaScript, building and testing one component at a time.

**What You'll Learn**:

- **CSS Architecture**: How to organize CSS using a Design Token system for easy theming and maintenance.
- **DOM Manipulation**: How to use JavaScript to create, modify, and display HTML elements dynamically based on API data.
- **ES6 Modules**: How to write clean, modular, and reusable JavaScript.
- **API Communication**: How to use the `fetch` API to get data from our backend.
- **Event Handling**: How to make the UI interactive by responding to user actions like button clicks.

---

## 2.1: The CSS Foundation - Architecture and Skeletons

First, let's create the empty files for our CSS. We'll follow the **ITCSS (Inverted Triangle CSS)** methodology, where we go from the most generic styles to the most specific.

- `tokens.css`: The "Settings" layer. Contains all our variables (colors, spacing, fonts). This is the single source of truth for our design.
- `base.css`: The "Elements" layer. Styles for raw HTML tags (`body`, `h1`, `a`, etc.). No classes.
- `components.css`: The "Components" layer. Styles for our reusable UI pieces like `.btn` and `.file-item`.
- `main.css`: The entry point that imports the others in the correct order.

### Your Turn: Create the CSS Files

- In your terminal, navigate to `backend/static/css`.
- Create the empty files:

```bash
touch tokens.css base.css components.css main.css
```

---

## 2.2: Step-by-Step Styling: The Design Tokens

We'll start with the most important file, `tokens.css`. This file won't produce any visible styles on its own, but it will define all the variables our other files will use.

### Your Turn: Add Color and Spacing Tokens

- Open `backend/static/css/tokens.css`.

- Add the `:root` selector and our color and spacing variables.

```css
/**
 * Design Tokens - The Single Source of Truth for our UI
 * The :root selector is equivalent to the <html> tag, but with
 * higher specificity. Variables defined here are global.
 */
:root {
  /* =========================================================================
   COLOR PALETTE - Raw color values (Primitives)
   ========================================================================= */

  /* Primary Brand Color - A scale from light to dark */
  --color-primary-100: #ebf0ff;
  --color-primary-500: #667eea; /* Main brand color */
  --color-primary-700: #4453b8;

  /* Neutral Grays */
  --color-gray-50: #fafafa;
  --color-gray-100: #f5f5f5;
  --color-gray-200: #e5e5e5;
  --color-gray-600: #525252;
  --color-gray-900: #171717;

  /* Semantic Colors (for success, error, etc.) */
  --color-success-500: #10b981;
  --color-success-600: #059669;
  --color-warning-500: #f59e0b;
  --color-danger-500: #ef4444;

  /* =========================================================================
   SPACING SCALE - Based on a 4px grid (0.25rem)
   ========================================================================= */
  --spacing-1: 0.25rem; /* 4px */
  --spacing-2: 0.5rem; /* 8px */
  --spacing-3: 0.75rem; /* 12px */
  --spacing-4: 1rem; /* 16px */
  --spacing-6: 1.5rem; /* 24px */
  --spacing-8: 2rem; /* 32px */
}
```

### Your Turn: Add Semantic Tokens

Now, let's add variables that describe _purpose_, not just color. These "semantic" tokens will reference the primitive tokens above. This is a key concept: we build our components using semantic tokens. If we want to change the theme, we only have to change what the semantic tokens point to.

- Add this code **inside** the `:root { ... }` block in `tokens.css`.

```css
/* =========================================================================
  SEMANTIC TOKENS - Light Theme (Default)
  These describe the PURPOSE of a color or value.
  ========================================================================= */

/* Backgrounds */
--bg-primary: #ffffff;
--bg-secondary: var(--color-gray-50);
--bg-tertiary: var(--color-gray-100);

/* Text */
--text-primary: var(--color-gray-900);
--text-secondary: var(--color-gray-600);
--text-link: var(--color-primary-700);

/* Borders */
--border-default: var(--color-gray-200);

/* Interactive Elements (Buttons, links, etc.) */
--interactive-primary: var(--color-primary-500);
--interactive-primary-hover: var(--color-primary-700);

/* Statuses */
--status-success-bg: rgba(16, 185, 129, 0.1);
--status-success-text: var(--color-success-600);
--status-warning-bg: rgba(245, 158, 11, 0.1);
--status-warning-text: var(--color-warning-500);
```

---

## 2.3: Step-by-Step Styling: Base Styles

Now we'll add styles to `base.css`. This file sets up sensible defaults for our entire application.

### Your Turn: Add Reset and Body Styles

- Open `backend/static/css/base.css`.

- Add the following code. This is a simple "CSS Reset" to remove inconsistent default browser styling, and it sets up our basic `body` styles using our new tokens.

```css
/*
 * A simple "CSS Reset" to create a consistent baseline across browsers.
 */
*,
*::before,
*::after {
  box-sizing: border-box; /* The most important reset rule! */
  margin: 0;
  padding: 0;
}

body {
  font-family: system-ui, -apple-system, sans-serif;
  line-height: 1.6;

  /* USING OUR TOKENS! */
  color: var(--text-primary);
  background-color: var(--bg-secondary);
}
```

---

## 2.4: Step-by-Step Styling: The HTML Skeleton

It's time to see something\! Let's create our basic HTML file and link our CSS.

### Your Turn: Create the Basic HTML

- Open `backend/static/index.html`.

- Add the basic HTML structure and link the CSS.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PDM System</title>

    <link rel="stylesheet" href="/static/css/main.css" />
  </head>
  <body>
    <h1>PDM System</h1>
    <p>This is our application.</p>
  </body>
</html>
```

### Your Turn: Import Your CSS Files

Our `index.html` links to `main.css`, but that file is still empty. Let's use it to import our other CSS files in the correct order.

- Open `backend/static/css/main.css`.

- Add the `@import` rules. The order is critical for the cascade to work correctly.

```css
/* 1. Design Tokens - Must load first so variables are available */
@import "tokens.css";

/* 2. Base Styles - Sets defaults for raw HTML elements */
@import "base.css";

/* 3. Components - We'll add styles here soon */
@import "components.css";
```

### Your Turn: Update FastAPI to Serve the Frontend

Our Python server doesn't know about these new files yet. Let's tell it to serve them.

- Open `backend/app/main.py`.

- Add imports for `StaticFiles` and `FileResponse`.

- Modify your `create_application` function to mount the `static` directory and serve the `index.html` at the root URL.

  **Modify `backend/app/main.py`**

```python
# Add these to your imports at the top of the file
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

def create_application() -> FastAPI:
  app = FastAPI(...) # Your existing app creation

  # Your CORS middleware...

  # --- Static Files & Frontend Entry Point ---
  # This tells FastAPI to serve any file in the 'static' directory
  # if the URL starts with /static.
  app.mount("/static", StaticFiles(directory="static"), name="static")

  # Your existing startup/shutdown events...

  # --- Root Endpoint (MODIFIED) ---
  # We change the root endpoint to serve our index.html file.
  @app.get("/", response_class=FileResponse)
  def read_root():
    """Serves the main application frontend."""
    return FileResponse("static/index.html")

  # Your router inclusion will go here later...

  return app
```

### ✅ Verification Point 1

- Make sure your `uvicorn` server is still running in the `backend` directory.
- Go to **[http://127.0.0.1:8000](https://www.google.com/search?q=http://127.0.0.1:8000)** in your browser.

You should now see a very plain page with "PDM System" as the title. But crucially, if you inspect the page with your browser's developer tools, you'll see that the `<body>` has the light gray background color (`--bg-secondary`) and dark text (`--text-primary`) that we defined in our tokens\! Our CSS is working.

---

## 2.5: Building the UI, Component by Component

Now we'll add styles to `components.css` and the corresponding HTML to `index.html`, building up the UI one piece at a time.

### Your Turn: Style and Build the Header

- **Add the CSS** for the header to `backend/static/css/components.css`.

```css
/* === Layout Components === */

.container {
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--spacing-4);
  padding-right: var(--spacing-4);
}

header {
  background: linear-gradient(
    135deg,
    var(--color-primary-500),
    var(--color-primary-700)
  );
  color: #ffffff; /* Use a direct value for text on a gradient */
  padding: var(--spacing-6);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}
```

- **Add the HTML** to `backend/static/index.html`, replacing the placeholder `<h1>` and `<p>`.

```html
<header>
  <div class="header-content">
    <div>
      <h1>PDM System</h1>
      <p>Parts Data Management</p>
    </div>
  </div>
</header>

<main>
  <div class="container" id="main-content">
    <p>Loading files...</p>
  </div>
</main>
```

### ✅ Verification Point 2

Refresh your browser. You should now see the beautiful gradient header\!

### Your Turn: Style and Build the File List

- **Add the CSS** for the file list items to `backend/static/css/components.css`.

```css
/* === File List Component === */

#file-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4); /* Use our spacing token for gaps! */
}

.file-item {
  padding: var(--spacing-4);
  border: 1px solid var(--border-default);
  border-radius: 0.5rem; /* 8px */
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-primary);
  transition: all 150ms ease-in-out;
}

.file-item:hover {
  transform: translateY(-2px);
  border-color: var(--interactive-primary);
}

.file-name {
  font-weight: 600;
  color: var(--text-primary);
}

.file-status {
  padding: var(--spacing-1) var(--spacing-3);
  border-radius: 9999px;
  font-size: 0.875rem; /* 14px */
  font-weight: 500;
}

.status-available {
  background-color: var(--status-success-bg);
  color: var(--status-success-text);
}

.status-checked_out {
  background-color: var(--status-warning-bg);
  color: var(--status-warning-text);
}
```

- We won't add the HTML for this manually. In the next step, we'll use JavaScript to create it dynamically from our API data. For now, we'll just prepare the container.

  **Modify `index.html`:**

```html
<section>
  <h2>Available Files</h2>
  <div id="loading-indicator"><p>Loading files from API...</p></div>
  <div id="file-list"></div>
</section>
```

---

## 2.6: Bringing It to Life with JavaScript

Now for the fun part. Let's fetch data from our API and build the file list.

### Your Turn: Create the JavaScript Skeletons

Create the empty files for our modular JavaScript.

- Navigate to `backend/static/js/`.

- `app.js` already exists. Now create the module for our API client.

```bash
touch modules/api-client.js
```

### Your Turn: Build the API Client

This module's only job is to talk to our backend.

- Open `backend/static/js/modules/api-client.js`.

- Add the following code:

```javascript
/**
 * API Client Module
 * A centralized place for all communication with our backend.
 */

// We export this class so other modules can import it.
export class APIClient {
  constructor(baseURL = "") {
    this.baseURL = baseURL;
  }

  // The core fetch function
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };
    const config = { ...options, headers };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP error! status: ${response.status}`
        );
      }
      return await response.json();
    } catch (error) {
      console.error(`API Error on ${endpoint}:`, error);
      throw error; // Re-throw the error so the calling code can handle it
    }
  }

  // A helper method for GET requests
  async get(endpoint) {
    return this.request(endpoint, { method: "GET" });
  }

  // --- Our App-Specific Methods ---

  async getFiles() {
    // This calls the endpoint we built in Stage 1!
    return this.get("/api/files");
  }
}

// Export a single, pre-made instance for convenience
export const apiClient = new APIClient();
```

### Your Turn: Write the Main Application Logic

Now let's use our API client in `app.js` to fetch data and update the DOM.

- Open `backend/static/js/app.js`.

- Replace its content with this initial structure.

```javascript
/**
 * Main Application Entry Point
 */

// Import the apiClient we just created
import { apiClient } from "./modules/api-client.js";

// --- DOM Elements ---
// Get references to the HTML elements we'll be working with.
const fileListEl = document.getElementById("file-list");
const loadingEl = document.getElementById("loading-indicator");

/**
 * Creates the HTML for a single file item.
 * @param {object} file - The file data from the API.
 * @returns {HTMLElement} - The created DOM element.
 */
function createFileElement(file) {
  const div = document.createElement("div");
  div.className = "file-item";

  // Note: In a real app, be careful with innerHTML to prevent XSS attacks.
  // For our controlled data, this is safe.
  div.innerHTML = `
    <span class="file-name">${file.name}</span>
    <span class="file-status status-${file.status}">
      ${file.status.replace("_", " ")}
    </span>
  `;
  return div;
}

/**
 * Fetches files from the API and renders them to the page.
 */
async function loadAndDisplayFiles() {
  try {
    // 1. Show the loading indicator
    loadingEl.style.display = "block";
    fileListEl.innerHTML = ""; // Clear old content

    // 2. Fetch data from the API
    const data = await apiClient.getFiles();
    const files = data.files;

    // 3. Hide the loading indicator
    loadingEl.style.display = "none";

    // 4. Check if we got any files
    if (files.length === 0) {
      fileListEl.innerHTML = "<p>No files found.</p>";
      return;
    }

    // 5. Create and append an element for each file
    files.forEach((file) => {
      const fileElement = createFileElement(file);
      fileListEl.appendChild(fileElement);
    });
  } catch (error) {
    // If the API call fails, show an error message
    loadingEl.style.display = "none";
    fileListEl.innerHTML = `<p style="color: red;">Error loading files: ${error.message}</p>`;
  }
}

// --- Initialization ---
// This runs when the page is fully loaded.
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded. Firing initial data load.");
  loadAndDisplayFiles();
});
```

- Finally, add the `type="module"` attribute to your script tag in `index.html` so it can use `import`.

  **Modify `index.html`:**

```html
<script type="module" src="/static/js/app.js"></script>
```

### ✅ Verification Point 3

Refresh your browser. You should see:

- A brief "Loading files from API..." message.
- The message disappears and is replaced by three styled file items, populated with the mock data from your FastAPI backend\!

You have successfully built a dynamic frontend that fetches data from a backend API and renders it to the screen.

---

## Stage 2 Complete ✓

You've created a professional frontend architecture from scratch, with a design system, modular code, and live API communication.

### Verification Checklist

- [ ] `index.html` is served at the root URL.
- [ ] The page has a styled header and a main content area.
- [ ] The CSS is organized into `tokens`, `base`, and `components`.
- [ ] JavaScript is modular, with a separate `api-client.js`.
- [ ] On page load, a "loading" message appears briefly.
- [ ] The file list is dynamically fetched from your `/api/files` endpoint and displayed.
- [ ] All elements are styled according to the CSS you wrote.
- [ ] There are no errors in the browser's developer console.

You are now ready to make the application truly interactive by implementing the checkout and check-in logic.

Ready for Stage 3?

Excellent. Let's dive into Stage 3. We'll replace our temporary mock data with real file system logic, build a professional-grade locking system to prevent data corruption, and refactor our code into a clean, scalable "service layer" architecture.

Get ready to interact with your code at every step.

---

# PDM Tutorial (New Format) - Stage 3: Real Files & Atomic Locks

**Goal**: To make our application interact with the actual filesystem, replacing all mock data. We will build a robust, cross-platform file locking mechanism to ensure data integrity and refactor our backend logic into a professional service layer.

**What You'll Learn**:

- How to perform filesystem operations in Python using the modern `pathlib` library.
- The critical importance of **atomic operations** and how to prevent **race conditions**.
- How to build a cross-platform file **locking** mechanism using a Python **context manager**.
- The **Service Layer** architecture pattern for clean, maintainable code.
- How to use **Dependency Injection** in FastAPI to provide services to your API endpoints.
- How to build and manage interactive modal dialogs on the frontend.

---

## 3.1: The "Why" - Race Conditions & The Need for Locking

Before we touch our application code, let's understand the core problem we need to solve. When multiple users or processes try to modify the same file (`locks.json`) at once, they can overwrite each other's changes, leading to data corruption. This is called a **race condition**.

### Your Turn: Witness a Race Condition

We'll use a "playground" file to see this bug in action. This file is for learning and won't be part of our final app.

- Create a new file: `backend/app/learn_race_condition.py`.

- Add the following code. Read the comments to understand the scenario.

  **File: `backend/app/learn_race_condition.py`**

```python
import threading
import json
from pathlib import Path
import time

print("--- Demonstrating a Race Condition (The Bug We Will Fix) ---")

# Imagine this is our shared locks.json file
test_file = Path("race_test.json")
test_file.write_text('{"counter": 0}')

def increment_counter_unsafe():
  """
  This function simulates two users trying to update the file at the same time.
  It performs a NON-ATOMIC "read-modify-write" sequence.
  """
  for _ in range(500):
    # 1. READ: Read the current value from the file.
    data = json.loads(test_file.read_text())

    # --- DANGER ZONE ---
    # At this exact moment, the other thread could also read the same value
    # before this thread has a chance to write its update!
    time.sleep(0.001) # A small delay to make the race condition more likely

    # 2. MODIFY: Increment the counter in memory.
    data['counter'] += 1

    # 3. WRITE: Write the new value back to the file.
    test_file.write_text(json.dumps(data))

# We create two "threads" to simulate two concurrent users.
thread1 = threading.Thread(target=increment_counter_unsafe)
thread2 = threading.Thread(target=increment_counter_unsafe)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

# Check the final result
final_data = json.loads(test_file.read_text())
print(f"Expected final counter: 1000 (500 from thread1 + 500 from thread2)")
print(f"Actual final counter:  {final_data['counter']}")
if final_data['counter'] < 1000:
  print(">>> Race condition occurred! Data was lost. <<<")
else:
  print(">>> No race condition this time (you were lucky!). Try running again. <<<")

# Clean up the test file
test_file.unlink()
```

### ✅ Verification

- From your `backend` directory (with `venv` active), run the script:

```bash
python -m app.learn_race_condition
```

- **Observe the output.** The "Actual final counter" will almost certainly be less than 1000. Both threads read the same value (e.g., 50), they both calculated `50 + 1 = 51`, and the last one to write "won," overwriting the other's work. Data was lost.

This is why we need an "atomic" way to update files.

---

## 3.2: The Solution - A Cross-Platform File Lock

We will build a special tool called a **context manager** that ensures only one process can access a file at a time. This makes our read-modify-write sequence **atomic**.

### Your Turn: Build the `LockedFile` Utility

- Create a new file: `backend/app/utils/file_locking.py`.

- Add the following code. This class is a powerful, reusable tool.

  **File: `backend/app/utils/file_locking.py`**

```python
import os
from pathlib import Path
import fcntl # This is for macOS/Linux
import msvcrt # This is for Windows

class LockedFile:
  """
  A context manager that provides an exclusive, cross-platform file lock.
  When you use it in a `with` statement, it guarantees that no other
  process can access the file until the `with` block is finished.
  """
  def __init__(self, filepath: Path, mode: str):
    self.filepath = filepath
    self.mode = mode
    self.file = None

  def __enter__(self):
    """Called when entering the 'with' block. Opens file and acquires lock."""
    self.file = self.filepath.open(self.mode)
    if os.name == 'nt':
      msvcrt.locking(self.file.fileno(), msvcrt.LK_LOCK, 1)
    else:
      fcntl.flock(self.file.fileno(), fcntl.LOCK_EX)
    return self.file

  def __exit__(self, exc_type, exc_val, exc_tb):
    """Called when exiting the 'with' block. Releases lock and closes file."""
    if os.name == 'nt':
      msvcrt.locking(self.file.fileno(), msvcrt.LK_UNLCK, 1)
    else:
      fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)
    self.file.close()
```

### Your Turn: Test the Lock

Let's prove our new tool works by adding a test block to the bottom of the same file.

- Add this code to the end of `backend/app/utils/file_locking.py`.

```python
if __name__ == "__main__":
  # This block only runs when you execute this file directly.
  # It's a great way to include tests for your utilities.
  import json
  import threading
  import time

  print("--- Testing File Locking to PREVENT Race Condition ---")

  test_file = Path("lock_test.json")
  test_file.write_text('{"counter": 0}')

  def safe_increment():
    """This is an ATOMIC increment using our new LockedFile class."""
    for _ in range(500):
      # The 'with' block makes the entire read-modify-write operation atomic.
      with LockedFile(test_file, 'r+') as f:
        data = json.load(f)
        data['counter'] += 1
        f.seek(0)
        f.truncate()
        json.dump(data, f)
      time.sleep(0.001)

  threads = [threading.Thread(target=safe_increment) for _ in range(2)]
  for t in threads: t.start()
  for t in threads: t.join()

  final_data = json.loads(test_file.read_text())
  print(f"Expected final counter: 1000")
  print(f"Actual final counter:  {final_data['counter']}")
  if final_data['counter'] == 1000:
    print(">>> Success! The lock prevented the race condition. <<<")
  else:
    print(">>> Something went wrong. The lock didn't work. <<<")

  test_file.unlink()
```

- Now, run this file from your `backend` directory:

```bash
python -m app.utils.file_locking
```

### ✅ Verification

The "Actual final counter" is now **1000**. Success\! Our `LockedFile` tool works perfectly. We are now ready to use it in our application. You can now delete the `learn_race_condition.py` file if you wish.

---

## 3.3: Building the Service Layer, Piece by Piece

It's time to create the "brain" of our file operations. We'll build a `FileService` that contains all the logic for listing, locking, and unlocking files.

### Your Turn: Create the Service Skeleton

- Replace the contents of `backend/app/services/file_service.py` with this skeleton. We're defining the structure before we fill in the logic.

  **File: `backend/app/services/file_service.py`**

```python
from pathlib import Path
from typing import List, Dict
import json
import logging
from app.utils.file_locking import LockedFile

logger = logging.getLogger(__name__)

class FileService:
  """The main service for all file and lock operations."""
  def __init__(self, repo_path: Path, locks_file: Path):
    self.repo_path = repo_path
    self.locks_file = locks_file

    # Ensure the repository and locks file exist
    self.repo_path.mkdir(parents=True, exist_ok=True)
    if not self.locks_file.exists():
      self.locks_file.write_text('{}')

  def get_files_with_status(self) -> List[Dict]:
    # TODO: Implement this method
    pass

  def checkout_file(self, filename: str, user: str, message: str):
    # TODO: Implement this method
    pass

  def checkin_file(self, filename: str, user: str):
    # TODO: Implement this method
    pass
```

### Your Turn: Implement File Listing

Let's implement the `get_files_with_status` method. It needs to do two things:

- Read the list of files from the `repo/` directory.

- Read the `locks.json` file to see which ones are locked.

- Combine that information into a single list.

- Replace the `get_files_with_status` method in `file_service.py` with this implementation:

```python
def get_files_with_status(self) -> List[Dict]:
  """
  Scans the repo directory for .mcam files and combines that
  information with the current lock status from locks.json.
  """
  all_files = []
  try:
    # 1. Load the current locks using our safe LockedFile context manager.
    with LockedFile(self.locks_file, 'r') as f:
      locks = json.load(f)

    # 2. Scan the repository directory for files.
    for item in self.repo_path.glob("*.mcam"):
      if item.is_file():
        filename = item.name
        lock_info = locks.get(filename)

        all_files.append({
          'name': filename,
          'size_bytes': item.stat().st_size,
          'status': 'checked_out' if lock_info else 'available',
          'locked_by': lock_info.get('user') if lock_info else None,
        })
    return all_files
  except Exception as e:
    logger.error(f"Failed to get files with status: {e}")
    return []
```

### Your Turn: Implement Checkout and Check-in Logic

Now let's add the logic for modifying the `locks.json` file. We will use our `LockedFile` tool to make these operations atomic and safe.

- Replace the `checkout_file` and `checkin_file` methods in `file_service.py` with these implementations:

```python
def checkout_file(self, filename: str, user: str, message: str):
  """Checks out a file by adding an entry to the locks file."""
  # Use our atomic context manager for a safe read-modify-write
  with LockedFile(self.locks_file, 'r+') as f:
    locks = json.load(f)

    # Business logic: Is the file present in the repo?
    if not (self.repo_path / filename).exists():
      raise ValueError(f"File '{filename}' does not exist in the repository.")

    # Business logic: Is the file already locked?
    if filename in locks:
      raise ValueError(f"File '{filename}' is already checked out by {locks[filename]['user']}.")

    # Modify the data
    locks[filename] = {
      "user": user,
      "message": message,
      "timestamp": datetime.now(timezone.utc).isoformat()
    }

    # Write the modified data back to the file
    f.seek(0)
    f.truncate()
    json.dump(locks, f, indent=4)

def checkin_file(self, filename: str, user: str):
  """Checks in a file by removing its entry from the locks file."""
  with LockedFile(self.locks_file, 'r+') as f:
    locks = json.load(f)

    # Business logic: Is the file actually locked?
    if filename not in locks:
      raise ValueError(f"File '{filename}' is not currently checked out.")

    # Authorization: Can this user check in this file?
    if locks[filename]['user'] != user:
      raise PermissionError(f"You cannot check in a file locked by another user.")

    # Modify the data
    del locks[filename]

    # Write the modified data back to the file
    f.seek(0)
    f.truncate()
    json.dump(locks, f, indent=4)
```

_(Note: You'll need to add `from datetime import datetime, timezone` to your imports at the top of the file.)_

Our `FileService` is now complete and robust\!

---

## 3.4: Connecting the Service to the API

Our service is ready, but our API endpoints in `api/files.py` are still using mock data. Let's wire them up to use the new service. To do this, we'll use a powerful FastAPI feature called **Dependency Injection**.

### Deep Dive: Dependency Injection (`Depends`)

Dependency Injection is a fancy term for a simple idea: your endpoint function declares what it _needs_, and FastAPI provides it.

Instead of this:

```python
@router.post("/checkout")
def checkout_file(request: ...):
  # Manually create the service inside the endpoint
  file_service = FileService(...)
  file_service.checkout_file(...)
```

We do this:

```python
def get_file_service():
  """A 'dependency' function that creates and returns the service."""
  return FileService(...)

@router.post("/checkout")
def checkout_file(request: ..., file_service: FileService = Depends(get_file_service)):
  # FastAPI runs get_file_service for us and passes the result
  # as the 'file_service' argument.
  file_service.checkout_file(...)
```

**Why is this better?**

- **Decoupling**: The endpoint doesn't need to know _how_ to create the service.
- **Testability**: In tests, we can easily provide a _mock_ `FileService` instead of the real one.
- **Reusability**: Many endpoints can `Depend` on the same `get_file_service` function.

### Your Turn: Update the API Endpoints

- Open `backend/app/api/files.py`.

- Replace the entire file with this new version, which uses our `FileService` via dependency injection.

  **File: `backend/app/api/files.py`**

```python
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.files import FileInfo, FileListResponse, FileCheckoutRequest, FileCheckinRequest
from app.services.file_service import FileService
from app.config import settings

router = APIRouter(
  prefix="/api/files",
  tags=["Files"],
)

# --- Dependency ---
def get_file_service() -> FileService:
  """This dependency creates and provides a FileService instance."""
  return FileService(
    repo_path=settings.BASE_DIR / 'repo',
    locks_file=settings.BASE_DIR / 'locks.json'
  )

# --- Endpoints ---
@router.get("/", response_model=FileListResponse)
def get_files(file_service: FileService = Depends(get_file_service)):
  """Get list of all files, now reading from the real filesystem."""
  files = file_service.get_files_with_status()
  return FileListResponse(files=files, total=len(files))

@router.post("/checkout")
def checkout_file(request: FileCheckoutRequest, file_service: FileService = Depends(get_file_service)):
  try:
    file_service.checkout_file(request.filename, request.user, request.message)
    return {"success": True, "message": "File checked out successfully"}
  except ValueError as e:
    # A known business logic error (e.g., already locked)
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
  except Exception as e:
    # An unexpected error
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/checkin")
def checkin_file(request: FileCheckinRequest, file_service: FileService = Depends(get_file_service)):
  try:
    file_service.checkin_file(request.filename, request.user)
    return {"success": True, "message": "File checked in successfully"}
  except PermissionError as e:
    # A specific authorization error
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
  except ValueError as e:
    # A known business logic error (e.g., not locked)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```

### ✅ Verification

- Create a `repo` directory inside `backend` if it doesn't exist.
- Create a few empty test files inside `backend/repo`:

```bash
cd backend
mkdir -p repo
touch repo/PN1001.mcam
touch repo/PN1002.mcam
```

- Go to **[http://127.0.0.1:8000/api/files](https://www.google.com/search?q=http://127.0.0.1:8000/api/files)** in your browser. You should now see the real files from your `repo` directory, not the old mock data\!
- Go to the interactive docs at **[http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)**. Try out the `POST /checkout` endpoint. It should now work and create a `locks.json` file in your `backend` directory.

Our backend is now fully functional and robust. It's time to connect the frontend.

---

## 3.5: Building the Frontend Modals

We need a way for users to input their name and a message when checking out a file. For this, we'll build interactive modal dialogs.

### Your Turn: Build the ModalManager

This JavaScript module will be a reusable class for controlling any modal on our page.

- Create the file `backend/static/js/modules/modal-manager.js`.

- Add the following class definition:

  **File: `backend/static/js/modules/modal-manager.js`**

```javascript
export class ModalManager {
  constructor(modalId) {
    this.modal = document.getElementById(modalId);
    if (!this.modal) {
      console.error(`Modal with ID ${modalId} not found.`);
      return;
    }
    // The overlay is the semi-transparent background
    this.overlay = this.modal;
    this.closeBtn = this.modal.querySelector(".modal-close");

    this._bindEvents();
  }

  _bindEvents() {
    // Close when clicking the 'X' button
    this.closeBtn.addEventListener("click", () => this.close());

    // Close when clicking on the background overlay
    this.overlay.addEventListener("click", (e) => {
      if (e.target === this.overlay) this.close();
    });

    // Close when pressing the 'Escape' key
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !this.modal.classList.contains("hidden")) {
        this.close();
      }
    });
  }

  open() {
    this.modal.classList.remove("hidden");
    // Focus the first input field for better accessibility
    const firstInput = this.modal.querySelector("input, textarea");
    if (firstInput) {
      setTimeout(() => firstInput.focus(), 50);
    }
  }

  close() {
    this.modal.classList.add("hidden");
    // Reset any forms inside the modal when it closes
    const form = this.modal.querySelector("form");
    if (form) form.reset();
  }
}
```

### Your Turn: Add Modal CSS and HTML

- Add the CSS for modals and forms to the bottom of `backend/static/css/components.css`.

```css
/* === Modal Component === */
.modal-overlay {
  position: fixed; /* Cover the whole screen */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: var(--bg-primary);
  padding: var(--spacing-6);
  border-radius: 0.5rem;
  width: 90%;
  max-width: 500px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-4);
  padding-bottom: var(--spacing-4);
  border-bottom: 1px solid var(--border-default);
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-3);
  margin-top: var(--spacing-6);
}

/* === Form Component === */
.form-group {
  margin-bottom: var(--spacing-4);
}
.form-group label {
  display: block;
  margin-bottom: var(--spacing-2);
  font-weight: 500;
}
.form-group input,
.form-group textarea {
  width: 100%;
  padding: var(--spacing-3);
  border: 1px solid var(--border-default);
  border-radius: 0.25rem;
}
```

- Add the HTML for our two modals to `backend/static/index.html`, just before the closing `</body>` tag.

```html
<div id="checkout-modal" class="modal-overlay hidden">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Check Out File</h3>
      <button class="modal-close">&times;</button>
    </div>
    <form id="checkout-form">
      <p>You are checking out: <strong id="checkout-filename"></strong></p>
      <div class="form-group">
        <label for="checkout-user">Your Name:</label>
        <input type="text" id="checkout-user" required />
      </div>
      <div class="form-group">
        <label for="checkout-message">Reason for checkout:</label>
        <textarea id="checkout-message" rows="3" required></textarea>
      </div>
      <div class="modal-actions">
        <button
          type="button"
          class="btn btn-secondary"
          onclick="checkoutModal.close()"
        >
          Cancel
        </button>
        <button type="submit" class="btn btn-primary">Confirm Checkout</button>
      </div>
    </form>
  </div>
</div>

<div id="checkin-modal" class="modal-overlay hidden"></div>
```

_(Note: The check-in modal is similar; for brevity, we'll focus on checkout logic for now, but you can build the check-in modal using the same pattern.)_

### Your Turn: Connect Everything in `app.js`

This is the final step where we make our UI interactive.

- Open `backend/static/js/app.js`.

- We'll import our new `ModalManager`, create instances for our modals, and update our event handlers to use them. Replace the entire file with this new version.

  **File: `backend/static/js/app.js`**

```javascript
import { apiClient } from "./modules/api-client.js";
import { ModalManager } from "./modules/modal-manager.js"; // NEW

// --- State & DOM Elements ---
const fileListEl = document.getElementById("file-list");
const loadingEl = document.getElementById("loading-indicator");
let currentFilename = null; // To keep track of which file we're acting on

// --- Modal Instances (NEW) ---
const checkoutModal = new ModalManager("checkout-modal");
// const checkinModal = new ModalManager("checkin-modal"); // You'll add this

// --- Functions ---
function createFileElement(file) {
  const div = document.createElement("div");
  div.className = "file-item";

  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ");

  const actionsDiv = document.createElement("div");
  const actionButton = document.createElement("button");
  actionButton.className = "btn btn-primary btn-sm";

  if (file.status === "available") {
    actionButton.textContent = "Checkout";
    actionButton.onclick = () => handleCheckout(file.name);
  } else {
    actionButton.textContent = "Checkin";
    actionButton.onclick = () => handleCheckin(file.name, file.locked_by);
  }
  actionsDiv.appendChild(actionButton);

  div.appendChild(nameSpan);
  div.appendChild(statusSpan);
  div.appendChild(actionsDiv);
  return div;
}

async function loadAndDisplayFiles() {
  loadingEl.style.display = "block";
  fileListEl.innerHTML = "";
  try {
    const data = await apiClient.getFiles();
    loadingEl.style.display = "none";
    if (data.files.length === 0) {
      fileListEl.innerHTML = "<p>No files found.</p>";
      return;
    }
    data.files.forEach((file) =>
      fileListEl.appendChild(createFileElement(file))
    );
  } catch (error) {
    loadingEl.style.display = "none";
    fileListEl.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
  }
}

// --- Event Handlers (NEW and UPDATED) ---
function handleCheckout(filename) {
  currentFilename = filename;
  document.getElementById("checkout-filename").textContent = filename;
  checkoutModal.open();
}

function handleCheckin(filename, lockedBy) {
  alert(
    `Check-in for ${filename} (locked by ${lockedBy}) will be implemented next!`
  );
  // We'll wire up the checkinModal here later.
}

async function submitCheckoutForm(event) {
  event.preventDefault(); // Stop the form from causing a page reload
  const user = document.getElementById("checkout-user").value;
  const message = document.getElementById("checkout-message").value;

  try {
    await apiClient.post("/api/files/checkout", {
      filename: currentFilename,
      user: user,
      message: message,
    });
    checkoutModal.close();
    await loadAndDisplayFiles(); // Refresh the list!
  } catch (error) {
    alert(`Checkout failed: ${error.message}`);
  }
}

// --- Initialization ---
document.addEventListener("DOMContentLoaded", () => {
  document
    .getElementById("checkout-form")
    .addEventListener("submit", submitCheckoutForm);
  loadAndDisplayFiles();
});
```

_(Note: We also updated the `api-client.js` to include a `post` method. Ensure you add it.)_

**Add to `api-client.js`:**

```javascript
// Inside the APIClient class
async post(endpoint, body) {
  return this.request(endpoint, { method: 'POST', body: JSON.stringify(body) });
}
```

---

## Stage 3 Complete ✓

You have now replaced the entire mock data system with a real, robust, and safe backend service layer and connected it to an interactive frontend.

### Final Verification Workflow

- Refresh your browser at **[http://127.0.0.1:8000](https://www.google.com/search?q=http://127.0.0.1:8000)**.
- The file list should load from your `repo/` directory.
- Click the "Checkout" button on an available file.
- The checkout modal should appear.
- Fill in your name and a reason, then click "Confirm Checkout."
- The modal should close, and the file list should automatically refresh, showing the file is now "checked out."
- Check your `backend` directory. A `locks.json` file should now exist with the lock information.

You have successfully built a full-stack feature, from the database (our `.json` files), through the service layer and API, all the way to the user interface.

Ready for Stage 4, where we'll add a professional state management system and polish the user experience?

Yes\! I'm ready. Let's continue with this interactive format.

This stage is all about elevating our frontend from merely functional to professional. We'll refactor our JavaScript to use a **centralized state management** system, which is a cornerstone of modern frontend development. This will make our app more robust, easier to debug, and ready for more complex features. We'll also add some polished user experience (UX) improvements like non-blocking notifications.

That is an absolutely fantastic point, and you're spot on. Rushing ahead without solidifying the fundamentals is how bugs and bad habits are born. These topics are not just "nice to have"; they are essential for professional development.

Let's pause before Stage 8 and create a "Stage 3A" dedicated to these foundational deep dives. We will give each of these topics the full, interactive playground treatment they deserve. This will make the entire application stronger and your understanding deeper.

Excellent call. Let's begin.

---

# PDM Tutorial (New Format) - Stage 3A: Foundational Deep Dives

**Goal**: To take a focused look at the core technologies we're using: JSON for data interchange, `datetime` for handling time, Pydantic for robust data validation, and `logging` for production-ready application monitoring.

**What You'll Learn**:

- The intricacies of **JSON serialization (`dump`/`dumps`)** and **deserialization (`load`/`loads`)**.
- How to handle time correctly using Python's **`datetime`** module, including timezones and the ISO 8601 standard.
- Advanced validation with **Pydantic's `Field`** to create more descriptive and constrained data models.
- How to configure a **production-ready logging system** that writes to rotating files instead of just the console.

---

## 3A.1: Deep Dive - The JSON Data Language

JSON (JavaScript Object Notation) is the _lingua franca_ of modern web APIs. It's a lightweight, text-based format that is easy for humans to read and for machines to parse. We're using it for our `locks.json` file and for all our API responses.

### Your Turn: The JSON Playground

- Create a new learning file: `backend/app/learn_json.py`.

- Add the following code to explore how Python's built-in `json` module works.

  **File: `backend/app/learn_json.py`**

```python
import json
from pathlib import Path

print("--- Learning to work with JSON in Python ---")

# This is a standard Python dictionary.
python_object = {
  "filename": "PN1001.mcam",
  "is_locked": True,
  "locked_by": "alice",
  "version": 1,
  "history": [
    {"sha": "abc1234", "message": "Initial commit"},
    {"sha": "def5678", "message": "Updated toolpath"}
  ],
  "metadata": None
}

# ============================================================================
# SERIALIZATION: Python Object -> JSON String
# ============================================================================
print("\n1. Serialization (Python -> JSON)")

# `dumps` means "dump to string".
# `indent=2` makes it human-readable (pretty-printing).
json_string = json.dumps(python_object, indent=2)

print("This is a JSON string:")
print(json_string)
print(f"The type of this is: {type(json_string)}") # It's a <class 'str'>

# Notice the Python-to-JSON type conversion:
# True -> true
# None -> null

# ============================================================================
# DESERIALIZATION: JSON String -> Python Object
# ============================================================================
print("\n2. Deserialization (JSON -> Python)")

# `loads` means "load from string".
parsed_python_object = json.loads(json_string)

print("This is a Python dictionary parsed from the string:")
print(parsed_python_object)
print(f"The type of this is: {type(parsed_python_object)}") # It's a <class 'dict'>
print(f"Accessing a nested value: {parsed_python_object['history'][0]['message']}")

# ============================================================================
# WORKING WITH FILES: `dump` and `load`
# ============================================================================
print("\n3. Working with Files")

file_path = Path("my_data.json")

# `dump` (no 's') means "dump to a file object".
with file_path.open("w") as f:
  json.dump(python_object, f, indent=4)
print(f"Successfully wrote data to '{file_path}'")

# `load` (no 's') means "load from a file object".
with file_path.open("r") as f:
  data_from_file = json.load(f)
print(f"Successfully read data from '{file_path}'")
print(f"Is the read data the same as the original? {data_from_file == python_object}")

# Clean up the file
file_path.unlink()
```

### ✅ Verification

- Run the playground file from your `backend` directory:

```bash
python -m app.learn_json
```

- **Observe the output.** See how the Python `dict` is converted into a formatted string, and then parsed back into a `dict`. Notice how `True` becomes `true` and `None` becomes `null`, following the JSON standard. You'll also see the `my_data.json` file appear and then disappear.

---

## 3A.2: Deep Dive - Handling Time Correctly with `datetime`

Handling dates and times is notoriously difficult in programming due to timezones, daylight saving, and different formats. The golden rules are:

- **Store everything in UTC**: Use Coordinated Universal Time (UTC) as your reference for all timestamps stored in your backend.
- **Use ISO 8601 Format**: When sending or storing dates as strings, use the unambiguous `YYYY-MM-DDTHH:MM:SS.ffffff+00:00` format.
- **Convert to local time only for display**: Only convert from UTC to a user's local timezone at the very last moment, in the frontend UI.

### Your Turn: The `datetime` Playground

- Create a new learning file: `backend/app/learn_datetime.py`.

- Add the following code to explore these concepts.

  **File: `backend/app/learn_datetime.py`**

```python
from datetime import datetime, timezone, timedelta

print("--- Learning to work with Dates and Times in Python ---")

# ============================================================================
# Naive vs. Aware Datetime Objects
# ============================================================================
print("\n1. Naive vs. Aware Datetime Objects")

# A "naive" object has no timezone information. This is dangerous!
# Does this mean 9 AM in London? New York? Tokyo? We don't know.
naive_now = datetime.now()
print(f"Naive datetime: {naive_now} (Timezone is unknown!)")

# An "aware" object has timezone information. This is what we should always use.
# We create it by specifying the timezone. For backend logic, ALWAYS use UTC.
utc_now = datetime.now(timezone.utc)
print(f"Aware datetime: {utc_now} (Timezone is UTC)")

# ============================================================================
# The ISO 8601 Standard
# ============================================================================
print("\n2. The ISO 8601 Format (The Universal Language of Timestamps)")

# When we need to store a datetime as a string (e.g., in JSON), we use .isoformat()
iso_string = utc_now.isoformat()
print(f"As an ISO 8601 string: {iso_string}")
# The 'Z' or '+00:00' at the end explicitly states this is a UTC timestamp.

# We can parse this string back into a full, aware datetime object.
parsed_datetime = datetime.fromisoformat(iso_string)
print(f"Parsed back to object:  {parsed_datetime}")
print(f"Is the parsed object aware? {parsed_datetime.tzinfo is not None}")

# ============================================================================
# Timezone Conversion (For Display)
# ============================================================================
print("\n3. Converting Timezones for Display")

# Let's define a timezone for US Eastern Time (UTC-4 during DST)
eastern_tz = timezone(timedelta(hours=-4))

# We can convert our UTC time to the user's local timezone for display.
local_time_for_user = utc_now.astimezone(eastern_tz)

print(f"UTC Time:   {utc_now.strftime('%Y-%m-%d %I:%M:%S %p %Z')}")
print(f"Eastern Time: {local_time_for_user.strftime('%Y-%m-%d %I:%M:%S %p %Z')}")
print("This conversion should only happen in the frontend, just before showing it to the user.")
```

### ✅ Verification

- Run the playground file: `python -m app.learn_datetime`.
- **Observe the output.** See the difference between a naive and an aware `datetime` object. Notice the clean, standard format of the ISO 8601 string. This is exactly the format we're storing in our `locks.json` file.

---

## 3A.3: Deep Dive - Advanced Pydantic with `Field`

In Stage 1, we used Pydantic for basic type validation (`name: str`). But we can add much more specific rules and metadata using `Field`. This makes our API more robust and our documentation more helpful.

### Your Turn: The `Field` Playground

- Create `backend/app/learn_pydantic_field.py`.

- Add the code to explore `Field`'s capabilities.

  **File: `backend/app/learn_pydantic_field.py`**

```python
from pydantic import BaseModel, Field, ValidationError

print("--- Learning Advanced Pydantic with Field ---")

class AdvancedCheckoutRequest(BaseModel):
  # Using Field allows us to add constraints and metadata.
  filename: str = Field(
    ..., # The ellipsis means the field is required.
    min_length=3,
    max_length=50,
    pattern=r"\.mcam$", # Regex: must end with .mcam
    description="The name of the Mastercam file to be checked out.",
    example="PN1001_OP1.mcam"
  )
  user_id: int = Field(
    ...,
    gt=0, # "Greater Than" 0. Use 'ge' for "Greater than or Equal to".
    description="The ID of the user performing the checkout.",
    example=101
  )
  priority: int = Field(
    default=1, # This field is optional and defaults to 1.
    le=5, # "Less than or Equal to" 5.
    description="Priority of the checkout, from 1 (lowest) to 5 (highest)."
  )

# --- DEMO ---
print("\n1. A valid request:")
valid_data = {"filename": "PART_A.mcam", "user_id": 42}
try:
  request = AdvancedCheckoutRequest(**valid_data)
  print(" -> Success! Pydantic model created.")
  print(f" -> Priority defaulted to: {request.priority}")
except ValidationError as e:
  print(f" -> This should not happen. Error: {e}")

print("\n2. An invalid request (filename too short and bad user_id):")
invalid_data = {"filename": "a.mcam", "user_id": -5, "message": "This is extra"}
try:
  AdvancedCheckoutRequest(**invalid_data)
except ValidationError as e:
  print(" -> Success! Pydantic caught the errors as expected:")
  # Pydantic gives detailed, machine-readable errors.
  print(e.json(indent=2))
```

### ✅ Verification

- Run the playground: `python -m app.learn_pydantic_field`.
- **Observe the output.** See how the valid data passes, but the invalid data is caught, with Pydantic generating a detailed JSON error report explaining exactly which rules failed. This is what FastAPI sends back to the client as a `422 Unprocessable Entity` response, making debugging frontends much easier.

---

## 3A.4: Production-Ready Logging

`print()` statements are great for quick debugging, but they are a terrible choice for a real application. A professional **logging** setup gives you much more power and control. When your application is running as a standalone executable, there will be no console to see `print()` statements. We need logs to be written to a file.

### Your Turn: Configure Production Logging

- Create a new file for our logging configuration: `backend/app/logging_config.py`.

  **File: `backend/app/logging_config.py`**

```python
import logging

# Define a custom log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

LOG_CONFIG = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "default": {
      "format": LOG_FORMAT,
      "datefmt": "%Y-%m-%d %H:%M:%S",
    },
  },
  "handlers": {
    # Handler for printing to the console (good for development)
    "console": {
      "class": "logging.StreamHandler",
      "formatter": "default",
      "level": "INFO",
    },
    # Handler for writing to a file (good for production)
    "file": {
      "class": "logging.handlers.RotatingFileHandler",
      "formatter": "default",
      "filename": "pdm_app.log", # The log file name
      "maxBytes": 1024 * 1024 * 5, # 5 MB
      "backupCount": 3, # Keep 3 old log files
      "level": "INFO",
    },
  },
  "root": {
    "handlers": ["console", "file"], # Use both handlers
    "level": "INFO",
  },
}
```

- Now, apply this configuration in `main.py`.

  **Modify `backend/app/main.py`**

```python
# Add these imports at the top
from logging.config import dictConfig
from app.logging_config import LOG_CONFIG

# Right at the top of the file, before creating the app instance, apply the config
dictConfig(LOG_CONFIG)

# ... rest of the main.py file ...
```

- Finally, let's replace our old `print()` statements with proper logging.

  **Modify `backend/app/services/file_service.py`**

```python
# Add this import at the top
import logging

# Get a logger instance for this specific file
logger = logging.getLogger(__name__)

# Now, find any `print()` statements or places where errors are caught
# and replace them with logger calls. For example:

# In LockManager.load_locks...
except (json.JSONDecodeError, IOError) as e:
  logger.error(f"Failed to load or parse locks file: {e}") # Use logger.error
  return {}

# In FileService.checkout_file...
self.audit_logger.log_action(...)
logger.info(f"User '{user}' checked out '{filename}'") # Use logger.info
```

Go through `file_service.py` and `auth_service.py` and replace any error handling `print()` calls with `logger.error()`, and any informational `print()` calls with `logger.info()`.

### ✅ Verification

- Stop and restart your `uvicorn` server.
- You should immediately see that the log messages in your console are now formatted with a timestamp (e.g., `2025-10-05 09:30:00 - uvicorn.error - INFO - ...`).
- Look in your `backend` directory. A new file, `pdm_app.log`, has been created\! Open it, and you'll see the same formatted log messages.
- Perform an action in the UI, like checking out a file. You will see the corresponding `logger.info` message appear in both the console and the log file.

Your application now has a robust, production-ready logging system.

---

## Stage 3A Complete ✓

We've solidified our understanding of several core technologies that underpin our application. This foundation will make building more complex features in the upcoming stages much easier and more reliable.

You now have a deeper understanding of JSON, `datetime`, Pydantic validation, and professional logging.

Ready to proceed with Stage 8, where we'll implement real-time updates with WebSockets?

# PDM Tutorial (New Format) - Stage 4: Professional Frontend State & UX

**Goal**: To refactor our frontend to use a professional state management pattern and to add UX improvements like toast notifications, search, filtering, and sorting.

**What You'll Learn**:

- The critical "why" behind **state management** and the problems with scattered state.
- How to implement the **Observer (Pub/Sub) pattern** to create a central "store".
- How to use **computed properties** to derive data without cluttering your state.
- How to build a non-blocking **toast notification** system from scratch.
- How a central store makes implementing features like **search, filter, and sort** incredibly simple.

---

## 4.1: The "Why" - The Chaos of Scattered State

Right now, our application state (the list of files, the loading status) is managed by loose variables and direct DOM manipulation in `app.js`. This works for a simple app, but as it grows, it leads to chaos.

Imagine trying to cook a complex meal, but your ingredients are scattered randomly throughout your house. 🍳 You have to run to the living room for flour, the bedroom for salt, and the garage for eggs. It's inefficient and you're likely to forget something.

This is what happens when every piece of your UI manages its own state. A central **store** is like having a perfectly organized kitchen counter (`mise en place`). All your ingredients (state) are in one place. Any "chef" (UI component) can look at the counter to see the current state, and when an ingredient changes, it's immediately obvious to everyone.

### Your Turn: Explore State Management in a Playground

Let's explore this concept in a self-contained "playground" file.

- Create a new file: `backend/static/js/modules/learn_state_management.js`.

- Add the following code. Read the comments to understand the evolution from a bad approach to a good one.

  **File: `backend/static/js/modules/learn_state_management.js`**

```javascript
/**
 * Understanding State Management in Frontend Applications
 */
console.log("--- Learning State Management ---");

// ============================================================================
// THE PROBLEM: Scattered global variables. Hard to track, hard to debug.
// ============================================================================
console.log("\n1. The Problem: Scattered State");
let scatteredFiles = [];
let isLoading = true;
// If another part of the app changes `isLoading`, how does everything else know?

// ============================================================================
// THE SOLUTION: A Centralized Store (The Observer Pattern)
// ============================================================================
console.log("\n2. The Solution: A Central Store");

class SimpleStore {
  constructor(initialState) {
    this._state = initialState;
    this._listeners = []; // A list of functions to call when state changes
  }

  // A way for UI components to "listen" for changes
  subscribe(listener) {
    this._listeners.push(listener);
  }

  // A way to get the current state
  getState() {
    return this._state;
  }

  // The ONLY way to update the state
  setState(newState) {
    this._state = { ...this._state, ...newState };
    // After updating, notify all listeners!
    this._listeners.forEach((listener) => listener(this._state));
  }
}

// --- Demo of the Store ---
const demoStore = new SimpleStore({ count: 0 });

// A "listener" is just a function that cares about the state.
const listener1 = (state) =>
  console.log(`Listener 1 sees new count: ${state.count}`);
const listener2 = (state) =>
  console.log(`Listener 2 sees new count: ${state.count}`);

demoStore.subscribe(listener1);
demoStore.subscribe(listener2);

console.log("Updating state to { count: 1 }...");
demoStore.setState({ count: 1 }); // Both listeners will fire automatically!

// ============================================================================
// A BETTER STORE: Actions and Computed Properties
// ============================================================================
console.log("\n3. A Better Store with Actions and Computed Properties");

class AppStore extends SimpleStore {
  // "Actions" are named methods for updating state.
  // This is better than calling `setState` directly all over your code.
  incrementCount() {
    const currentCount = this.getState().count;
    this.setState({ count: currentCount + 1 });
  }

  // A "Computed Property" is data that is DERIVED from state.
  // We don't store it in the state itself.
  isCountEven() {
    return this.getState().count % 2 === 0;
  }
}

const appStore = new AppStore({ count: 5 });
appStore.subscribe((state) => {
  console.log(`AppStore state updated. New count: ${state.count}`);
  console.log(` - Is the count even? ${appStore.isCountEven()}`);
});

console.log("Calling action 'incrementCount'...");
appStore.incrementCount(); // The count becomes 6
```

### ✅ Verification

- To test this, create a temporary `test.html` file in your `static` folder:

```html
<!DOCTYPE html>
<html>
  <body>
    <h1>Check the Console</h1>
    <script
      type="module"
      src="/static/js/modules/learn_state_management.js"
    ></script>
  </body>
</html>
```

- Visit **[http://127.0.0.1:8000/test.html](https://www.google.com/search?q=http://127.0.0.1:8000/test.html)** and open your browser's developer console.
- **Observe the output.** You'll see the logs demonstrating how the store notifies its listeners when the state changes. This is the core pattern we will now build for our app. You can delete `test.html` when you're done.

---

## 4.2: Building Our Application's Store

Let's create the real store for our PDM application. It will manage files, loading status, errors, and our new search/filter state.

### Your Turn: Create the Store

- Create a new file: `backend/static/js/modules/store.js`.

- Add the following code. This is the "kitchen counter" for our application.

  **File: `backend/static/js/modules/store.js`**

```javascript
/**
 * Application State Store
 * A single source of truth for the entire UI.
 */
class Store {
  constructor() {
    this._state = {
      allFiles: [],
      isLoading: true,
      error: null,
      searchTerm: "",
      statusFilter: "all", // 'all' | 'available' | 'checked_out'
      sortBy: "name-asc",
    };
    this._listeners = [];
  }

  // --- Subscription ---
  subscribe(listener) {
    this._listeners.push(listener);
  }

  _notify() {
    // Pass a copy of the state to prevent accidental direct mutation
    this._listeners.forEach((listener) => listener({ ...this._state }));
  }

  // --- Actions (methods for updating state) ---
  setLoading() {
    this._state.isLoading = true;
    this._state.error = null;
    this._notify();
  }

  setFiles(files) {
    this._state.allFiles = files;
    this._state.isLoading = false;
    this._notify();
  }

  setError(errorMessage) {
    this._state.error = errorMessage;
    this._state.isLoading = false;
    this._notify();
  }

  setSearchTerm(term) {
    this._state.searchTerm = term;
    this._notify();
  }

  setStatusFilter(filter) {
    this._state.statusFilter = filter;
    this._notify();
  }

  setSortBy(sortKey) {
    this._state.sortBy = sortKey;
    this._notify();
  }

  // --- Computed Properties (for deriving state) ---
  getDisplayFiles() {
    let filtered = [...this._state.allFiles];

    // 1. Apply search filter
    if (this._state.searchTerm) {
      const term = this._state.searchTerm.toLowerCase();
      filtered = filtered.filter((f) => f.name.toLowerCase().includes(term));
    }

    // 2. Apply status filter
    if (this._state.statusFilter !== "all") {
      filtered = filtered.filter((f) => f.status === this._state.statusFilter);
    }

    // 3. Apply sorting
    const [field, direction] = this._state.sortBy.split("-");
    filtered.sort((a, b) => {
      const aVal = a[field] || 0;
      const bVal = b[field] || 0;
      const comparison = aVal > bVal ? 1 : -1;
      return direction === "asc" ? comparison : -comparison;
    });

    return filtered;
  }
}

// Export a single, global instance of our store
export const store = new Store();
```

---

## 4.3: Polishing the UX - Toast Notifications

Before we refactor our main `app.js`, let's build a better notification system. `alert()` is blocking and ugly. A "toast" notification is a small message that appears and then fades away on its own.

### Your Turn: Build the Toast System

- Create a new file: `backend/static/js/modules/toast.js`.

- Add the `ToastManager` class. This will dynamically create and manage the notification elements.

  **File: `backend/static/js/modules/toast.js`**

```javascript
class ToastManager {
  constructor() {
    const container = document.createElement("div");
    container.id = "toast-container";
    document.body.appendChild(container);
    this.container = container;
  }

  show(message, type = "info", duration = 3000) {
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    this.container.appendChild(toast);

    // Animate in
    setTimeout(() => toast.classList.add("show"), 10);

    // Animate out and remove
    setTimeout(() => {
      toast.classList.remove("show");
      toast.addEventListener("transitionend", () => toast.remove());
    }, duration);
  }

  success(message) {
    this.show(message, "success");
  }
  error(message) {
    this.show(message, "error", 5000);
  }
}

export const toast = new ToastManager();
```

- Add the required CSS to the bottom of `backend/static/css/components.css`.

```css
/* === Toast Notifications === */
#toast-container {
  position: fixed;
  top: var(--spacing-4);
  right: var(--spacing-4);
  z-index: 2000;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-3);
}
.toast {
  padding: var(--spacing-3) var(--spacing-4);
  border-radius: 0.25rem;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border-left: 4px solid var(--color-gray-600);
  opacity: 0;
  transform: translateX(100%);
  transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
}
.toast.show {
  opacity: 1;
  transform: translateX(0);
}
.toast.toast-success {
  border-color: var(--color-success-500);
}
.toast.toast-error {
  border-color: var(--color-danger-500);
}
```

---

## 4.4: Refactoring `app.js` to Use the Store

This is the main event. We are going to rewire `app.js` to be driven entirely by our new store.

### Your Turn: Refactor `app.js`

- Open `backend/static/js/app.js`.

- Replace its entire content with this new, store-driven version. Read the comments to see how the logic has changed.

  **File: `backend/static/js/app.js`**

```javascript
import { apiClient } from "./modules/api-client.js";
import { ModalManager } from "./modules/modal-manager.js";
import { store } from "./modules/store.js"; // NEW: Import the store
import { toast } from "./modules/toast.js"; // NEW: Import the toast manager

// --- Modal Instances ---
const checkoutModal = new ModalManager("checkout-modal");
let currentFilename = null;

// ============================================================================
// THE RENDER FUNCTION - The heart of our new UI logic
// ============================================================================
/**
 * This single function is responsible for drawing the entire UI based on
 * the current state from the store. It's called automatically whenever
 * the state changes.
 * @param {object} state - The current state from the store.
 */
function render(state) {
  const fileListEl = document.getElementById("file-list");
  const loadingEl = document.getElementById("loading-indicator");

  // Render loading state
  loadingEl.style.display = state.isLoading ? "block" : "none";

  // Render error state
  if (state.error) {
    fileListEl.innerHTML = `<p style="color: red;">Error: ${state.error}</p>`;
    return;
  }

  // If not loading and no error, render the files
  if (!state.isLoading) {
    const displayFiles = store.getDisplayFiles(); // Use the computed property!
    fileListEl.innerHTML = ""; // Clear previous content

    if (displayFiles.length === 0) {
      fileListEl.innerHTML = "<p>No files match your criteria.</p>";
    } else {
      displayFiles.forEach((file) => {
        const fileElement = createFileElement(file);
        fileListEl.appendChild(fileElement);
      });
    }
  }
}

// The createFileElement function remains mostly the same as before
function createFileElement(file) {
  // ... (copy the createFileElement function from your old app.js) ...
  const div = document.createElement("div");
  div.className = "file-item";
  div.innerHTML = `
    <span class="file-name">${file.name}</span>
    <span class="file-status status-${file.status}">
      ${file.status.replace("_", " ")}
    </span>
  `;
  const actionButton = document.createElement("button");
  actionButton.className = "btn btn-primary btn-sm";

  if (file.status === "available") {
    actionButton.textContent = "Checkout";
    actionButton.onclick = () => handleCheckout(file.name);
  } else {
    actionButton.textContent = "Checkin";
    actionButton.onclick = () => handleCheckin(file.name);
  }
  div.appendChild(actionButton);
  return div;
}

// ============================================================================
// DATA LOGIC - Functions that change the state
// ============================================================================

async function loadFiles() {
  store.setLoading(); // ACTION: Tell the store we're loading
  try {
    const data = await apiClient.getFiles();
    store.setFiles(data.files); // ACTION: Update store with new files
  } catch (error) {
    store.setError(error.message); // ACTION: Update store with the error
  }
}

async function submitCheckoutForm(event) {
  event.preventDefault();
  const user = document.getElementById("checkout-user").value;
  const message = document.getElementById("checkout-message").value;

  try {
    await apiClient.post("/api/files/checkout", {
      filename: currentFilename,
      user,
      message,
    });
    toast.success(`'${currentFilename}' checked out!`); // NEW: Use toast
    checkoutModal.close();
    loadFiles(); // Just reload the data, the store will handle the UI update
  } catch (error) {
    toast.error(`Checkout failed: ${error.message}`); // NEW: Use toast
  }
}

// --- Event Handlers ---
function handleCheckout(filename) {
  /* ... same as before ... */
}
function handleCheckin(filename) {
  /* ... same as before ... */
}

// ============================================================================
// INITIALIZATION
// ============================================================================
document.addEventListener("DOMContentLoaded", () => {
  console.log("App initialized with central store.");

  // THE MAGIC LINE: Subscribe our render function to the store.
  // Now, whenever an action calls _notify(), render() will automatically run!
  store.subscribe(render);

  // Wire up forms
  document
    .getElementById("checkout-form")
    .addEventListener("submit", submitCheckoutForm);

  // Initial data load
  loadFiles();
});
```

_Note: You'll need to copy your `createFileElement`, `handleCheckout`, and `handleCheckin` functions from your previous `app.js` version to complete this file._

### ✅ Verification

Refresh your browser. The application should look and work exactly as it did before. **This is a good thing\!** It means our refactoring was successful.
Test the checkout flow. You should now see a sleek toast notification instead of the ugly `alert()`. This confirms the new architecture is working.

---

## 4.5: Adding Search, Filter, and Sort

Now that we have a central store, adding new UI features that depend on the state is incredibly easy.

### Your Turn: Add the Filter UI

- Open `backend/static/index.html`.

- Add the HTML for the controls right after the `<h2>Available Files</h2>` line.

```html
<div class="file-controls">
  <input type="search" id="file-search" placeholder="Search files..." />
  <select id="status-filter">
    <option value="all">All Statuses</option>
    <option value="available">Available</option>
    <option value="checked_out">Checked Out</option>
  </select>
  <select id="sort-select">
    <option value="name-asc">Sort by Name (A-Z)</option>
    <option value="name-desc">Sort by Name (Z-A)</option>
    <option value="size_bytes-desc">Sort by Size (Largest)</option>
  </select>
</div>
```

- Add the CSS for these controls to `backend/static/css/components.css`.

```css
.file-controls {
  display: flex;
  gap: var(--spacing-4);
  margin-bottom: var(--spacing-4);
}
.file-controls input,
.file-controls select {
  padding: var(--spacing-2);
  border: 1px solid var(--border-default);
  border-radius: 0.25rem;
}
```

### Your Turn: Wire up the Controls

This is the easy part. We just need to call our store's actions when the inputs change.

- Open `backend/static/js/app.js`.

- Add these event listeners inside your `DOMContentLoaded` block.

```javascript
// Inside document.addEventListener("DOMContentLoaded", ...)

// --- Filter and Sort Event Listeners ---
document.getElementById("file-search").addEventListener("input", (e) => {
  store.setSearchTerm(e.target.value);
});

document.getElementById("status-filter").addEventListener("change", (e) => {
  store.setStatusFilter(e.target.value);
});

document.getElementById("sort-select").addEventListener("change", (e) => {
  store.setSortBy(e.target.value);
});
```

### ✅ Final Verification

Refresh your browser.

- Type in the search box. The file list should filter instantly as you type.
- Use the "Status" dropdown. The list should update to show only available or checked-out files.
- Use the "Sort" dropdown. The order of the files should change.

Notice how we didn't have to write _any_ new DOM manipulation code. We just updated the state, and our `render` function, subscribed to the store, took care of the rest automatically. This is the power of centralized state management.

---

## Stage 4 Complete ✓

You've successfully refactored your frontend to a professional, state-driven architecture and added significant UX improvements.

### Verification Checklist

- [ ] The app uses a central `store.js` for all UI state.
- [ ] The old global state variables in `app.js` are gone.
- [ ] A single `render()` function, subscribed to the store, handles all UI updates.
- [ ] Functions like `loadFiles` and form submissions now call store actions instead of directly manipulating the DOM.
- [ ] Toast notifications have replaced `alert()`.
- [ ] The search input filters the file list in real-time.
- [ ] The status and sort dropdowns update the file list correctly.

You're now ready to tackle one of the most important parts of any real-world application: user authentication.

Ready for Stage 5?

Let's do it. Stage 5 is one of the most critical parts of any web application: **Authentication and Authorization**. We will build a complete, secure login system from scratch.

Following our new format, we'll start with the foundational concepts in a playground, build the backend services and endpoints incrementally, and then create the frontend login page to tie it all together.

---

# PDM Tutorial (New Format) - Stage 5: Authentication & Authorization

**Goal**: To secure our application by implementing a robust authentication system. We'll create a login flow, protect our API endpoints, and manage user sessions using modern, stateless JSON Web Tokens (JWTs).

**What You'll Learn**:

- The crucial difference between **Authentication ("Who are you?")** and **Authorization ("What are you allowed to do?")**.
- Why you **must never** store passwords in plain text and how modern password hashing with **bcrypt** works.
- The difference between stateful (sessions) and stateless (**JWT**) authentication, and why we're using JWTs.
- How to create, sign, and verify JWTs.
- How to create protected API endpoints and "dependency injection" for security in FastAPI.

---

## 5.1: The "Why" - A Deep Dive into Security Concepts

Before we write any login code, we need to understand the principles of modern web security. Mistakes here can have serious consequences. We'll explore these concepts in a playground file.

### Your Turn: Explore Authentication Concepts

- First, we need a library for password hashing. From your `backend` directory (with `venv` active), install `passlib` with its `bcrypt` dependencies:

```bash
pip install "passlib[bcrypt]"
```

- Create a new learning file: `backend/app/learn_auth_concepts.py`.

- Add the following code. Read through the comments and code carefully—this is the theoretical foundation for this entire stage.

  **File: `backend/app/learn_auth_concepts.py`**

```python
"""
A playground for understanding core security concepts:
- Authentication vs. Authorization
- Secure Password Hashing
- JSON Web Tokens (JWTs)
"""
from passlib.context import CryptContext
import base64
import json

print("--- Learning Authentication & Authorization ---")

# ============================================================================
# CONCEPT 1: Authentication (AuthN) vs. Authorization (AuthZ)
# ============================================================================
print("\n1. AuthN vs. AuthZ")
print("Authentication (AuthN) is proving who you are (e.g., logging in with a password).")
print("Authorization (AuthZ) is checking what you're allowed to do (e.g., are you an admin?).")
print("Analogy: Showing your ID to enter an office building is AuthN. Your keycard only opening certain doors is AuthZ.")

# ============================================================================
# CONCEPT 2: Secure Password Hashing with bcrypt
# ============================================================================
print("\n2. Secure Password Hashing")

# WHY NOT PLAINTEXT? If your database is ever leaked, all user passwords are stolen.
# WHY NOT A SIMPLE HASH (like SHA256)? It's too fast! Modern GPUs can guess
# billions of simple hashes per second, making it easy to crack common passwords.

# THE CORRECT WAY: A slow, salted, adaptive hashing algorithm like bcrypt.
# We use `passlib` to handle this for us.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "MySuperSecurePassword123!"

# HASHING: This takes the plain password and turns it into a secure hash.
# The hash automatically includes a random "salt," so the same password
# will produce a DIFFERENT hash every time. This defeats pre-computed "rainbow tables".
hashed_password = pwd_context.hash(password)

print(f"Original Password: {password}")
print(f"Securely Hashed: {hashed_password[:30]}...") # Only show the beginning

# VERIFYING: To check a login, you re-hash the user's input and see if it
# matches the stored hash. The `verify` function handles this for us.
is_correct = pwd_context.verify(password, hashed_password)
is_wrong = pwd_context.verify("WrongPassword", hashed_password)

print(f"Verification with correct password: {is_correct}") # True
print(f"Verification with wrong password:  {is_wrong}") # False

# ============================================================================
# CONCEPT 3: JSON Web Tokens (JWT) for Stateless Sessions
# ============================================================================
print("\n3. Understanding JWTs")

# A JWT is like a secure, self-contained VIP wristband for your API.
# Once you log in, the server gives you a token. You show this token
# with every subsequent request to prove you're authenticated.
# It's "stateless" because the server doesn't need to remember the token;
# it can verify it mathematically using a secret key.

# A JWT has three parts, separated by dots: header.payload.signature
# Example token (the signature part is fake here)
example_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZSIsInJvbGUiOiJ1c2VyIiwiZXhwIjoxNzM1Njg5NjAwfQ.fake_signature_string"

header_b64, payload_b64, signature = example_token.split('.')

# The header and payload are just Base64Url-encoded JSON. They are NOT encrypted!
# Anyone can decode and read them.
header = json.loads(base64.urlsafe_b64decode(header_b64 + '=='))
payload = json.loads(base64.urlsafe_b64decode(payload_b64 + '=='))

print(f"Decoded Header: {header}")
print(f"Decoded Payload: {payload}")
print(f"Signature:    The part that proves the token is authentic and wasn't tampered with.")
print("\nCRITICAL: Never put sensitive information in a JWT payload!")
```

### ✅ Verification

- Run the playground file from your `backend` directory:

```bash
python -m app.learn_auth_concepts
```

- **Observe the output.** Confirm that you understand the difference between AuthN and AuthZ, see how `bcrypt` hashes a password, and understand the three parts of a JWT.

---

## 5.2: Backend Setup for Authentication

Now let's add the necessary tools and configuration to our application.

### Your Turn: Install Dependencies

We need two more libraries: `python-jose` for creating and verifying JWTs, and `python-multipart` which FastAPI needs for handling login form data.

- Run the following `pip` command:

```bash
pip install "python-jose[cryptography]" python-multipart
```

- Update your `requirements.txt` file to lock in these new dependencies.

```bash
pip freeze > requirements.txt
```

### Your Turn: Update Configuration

We need to add a secret key to our configuration. This key is used to digitally "sign" our JWTs, proving that we were the ones who created them.

- Open `backend/app/config.py`.

- Add the new security-related settings.

  **File: `backend/app/config.py`**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  APP_NAME: str = "PDM Backend API"
  APP_VERSION: str = "0.1.0"

  # --- NEW: Security Settings ---
  # This key is used to sign JWTs. It MUST be kept secret.
  # In production, this should be loaded from an environment variable.
  # You can generate a new strong key with: openssl rand -hex 32
  SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

  class Config:
    env_file = ".env"

settings = Settings()
```

> **Security Note**: It's okay to have a default `SECRET_KEY` in the code for development, but in a real production environment, you would remove the default value and load it exclusively from an environment variable or a secure vault to prevent it from being checked into version control.

### Your Turn: Create Authentication Schemas

We need Pydantic models to define the shape of our authentication-related data, like user info and tokens.

- Create a new file: `backend/app/schemas/auth.py`.

- Add the following Pydantic models:

  **File: `backend/app/schemas/auth.py`**

```python
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
  """The response model for a successful login."""
  access_token: str
  token_type: str = "bearer"

class TokenData(BaseModel):
  """The data we encode inside the JWT payload."""
  username: Optional[str] = None

class User(BaseModel):
  """The user model that is safe to send to clients (no password hash)."""
  username: str
  full_name: str
  role: str

class UserInDB(User):
  """The user model as it is stored in our 'database' (users.json)."""
  password_hash: str
```

---

## 5.3: Building the Authentication Service & Endpoints

Now we'll build the core logic and the API endpoints for logging in and getting user information.

### Your Turn: Build the `auth_service`

This service will handle user storage (in a new `users.json` file), password hashing, and JWT creation.

- Create the file `backend/app/services/auth_service.py`.

- Add the code for the service. Notice how it uses the concepts from our playground file.

  **File: `backend/app/services/auth_service.py`**

```python
# This file contains all the business logic for authentication.
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.schemas.auth import UserInDB
# We will create a simplified UserService here for now
# We will expand this in Stage 8

# 1. Password Hashing Setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
  return pwd_context.hash(password)

# 2. JWT Creation
def create_access_token(data: dict) -> str:
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
  return encoded_jwt

# 3. Dummy User Database (for now)
# In a real app, this would be a real database. We are using a simple dict.
# We'll create a `users.json` file later. For now, this is enough.
DUMMY_USERS_DB = {
  "admin": UserInDB(
    username="admin",
    full_name="Administrator",
    role="admin",
    password_hash=get_password_hash("Admin123!") # Hash the password!
  ),
  "john": UserInDB(
    username="john",
    full_name="John Doe",
    role="user",
    password_hash=get_password_hash("Password123!")
  )
}

def get_user(username: str) -> Optional[UserInDB]:
  return DUMMY_USERS_DB.get(username)

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
  """Authenticates a user, returning the user object if successful, else None."""
  user = get_user(username)
  if not user:
    return None
  if not verify_password(password, user.password_hash):
    return None
  return user
```

### Your Turn: Create the Security Dependency

This is the most important part for securing our app. We will create a function `get_current_user` that FastAPI can use to protect endpoints.

- Create the file `backend/app/api/deps.py` (for "dependencies").

- Add the following code:

  **File: `backend/app/api/deps.py`**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config import settings
from app.schemas.auth import TokenData, User
from app.services import auth_service

# This creates a dependency that expects an "Authorization: Bearer <token>" header.
# It also tells the interactive docs to add a lock icon and an authorize button.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
  """
  Dependency to get the current user from a JWT token.
  This function will be added to every protected endpoint.
  """
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
    token_data = TokenData(username=username)
  except JWTError:
    raise credentials_exception

  user = auth_service.get_user(username=token_data.username)
  if user is None:
    raise credentials_exception

  # Return the User schema, which is safe to use (no password hash)
  return User(username=user.username, full_name=user.full_name, role=user.role)
```

### Your Turn: Create the Login Endpoints

Now we create the actual API endpoints for logging in and getting user info.

- Create the file `backend/app/api/auth.py`.

- Add the login router.

  **File: `backend/app/api/auth.py`**

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import Token, User
from app.services import auth_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
  """
  Takes a username and password from a form post and returns a JWT token.
  """
  user = auth_service.authenticate_user(form_data.username, form_data.password)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
    )
  # The 'sub' (subject) claim in JWT is standard for the user identifier.
  access_token = auth_service.create_access_token(data={"sub": user.username, "role": user.role})
  return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
  """
  Returns the information for the currently logged-in user.
  Simply adding `Depends(get_current_user)` PROTECTS this endpoint.
  """
  return current_user
```

### ✅ Verification (Part 1 - Backend)

- **Wire it up:** Open `backend/app/main.py`, import the new router, and include it in your app.

```python
# Add to imports
from app.api import auth

# In create_application(), after app.include_router(files.router)
app.include_router(auth.router)
```

- Go to your interactive docs at **[http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)**.

- You'll see the new "Authentication" section.
- Try to use the `/api/auth/me` endpoint. It will fail with a `403 Forbidden` error because you haven't provided a token.
- Now, use the `/api/auth/login` endpoint. Click "Try it out," enter `admin` for username and `Admin123!` for password, and execute. You'll get back an `access_token`.
- Copy the token string.
- At the top right of the page, click the "Authorize" button, paste `Bearer <your_token>` into the box, and authorize.
- Now try `/api/auth/me` again. It will succeed and return the admin user's information\!

You have successfully created a protected endpoint.

---

## 5.4: Securing the Files API

Now we'll apply the `get_current_user` dependency to our existing file endpoints to protect them.

### Your Turn: Protect the File Endpoints

- Open `backend/app/api/files.py`.

- Import `User` and `get_current_user`.

- Add `current_user: User = Depends(get_current_user)` to the signature of **every** endpoint function.

- Modify `checkout` and `checkin` to use the `current_user.username` from the token, which is much more secure than trusting the username sent from the client.

  **Modify `backend/app/api/files.py`**

```python
# Add to imports
from app.schemas.auth import User
from app.api.deps import get_current_user

# Modify get_files
@router.get("/", ...)
def get_files(
  file_service: FileService = Depends(get_file_service),
  current_user: User = Depends(get_current_user) # PROTECT
):
  # ...

# Modify checkout_file
@router.post("/checkout")
def checkout_file(
  request: FileCheckoutRequest,
  file_service: FileService = Depends(get_file_service),
  current_user: User = Depends(get_current_user) # PROTECT
):
  try:
    # Use the secure username from the token, not the request body
    file_service.checkout_file(request.filename, current_user.username, request.message)
    # ...
  # ...

# Do the same for your other file endpoints...
```

- Since the username now comes from the token, we can remove it from our request schemas.

  **Modify `backend/app/schemas/files.py`**

```python
class FileCheckoutRequest(BaseModel):
  filename: str = Field(..., min_length=1)
  # user: str = Field(..., min_length=3) # REMOVE THIS LINE
  message: str = Field(..., min_length=1, max_length=500)

class FileCheckinRequest(BaseModel):
  filename: str
  # user: str # REMOVE THIS LINE
```

### ✅ Verification

Go back to the docs at **[http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)**. Try to use `/api/files` without being authorized. It will now fail. Authorize with your token, and it will succeed. Your entire file API is now secure.

---

## 5.5: Building the Frontend Login Experience

The backend is secure. Now let's build the UI for logging in.

### Your Turn: Create the Login Page

- Create the file `backend/static/login.html`.

- Create the file `backend/static/js/login.js`.

- Add the HTML for the login form. This is a standalone page with its own simple styles.

  **File: `backend/static/login.html`**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Login - PDM System</title>
    <link rel="stylesheet" href="/static/css/main.css" />
    <style>
      /* Add the simple login page styles from my previous long response */
      body {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background: var(--bg-secondary);
      }
      .login-container {
        background: var(--bg-primary);
        padding: var(--spacing-8);
        border-radius: 0.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        width: 90%;
        max-width: 400px;
      }
      .error-message {
        background: #fee2e2;
        color: #991b1b;
        padding: var(--spacing-3);
        border-radius: 0.25rem;
        margin-bottom: var(--spacing-4);
        display: none;
      }
      .error-message.show {
        display: block;
      }
    </style>
  </head>
  <body>
    <div class="login-container">
      <h2>PDM System Login</h2>
      <div id="error-message" class="error-message"></div>
      <form id="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" name="username" required autofocus />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" name="password" required />
        </div>
        <button type="submit" class="btn btn-primary" style="width: 100%;">
          Login
        </button>
      </form>
      <div
        style="margin-top: 1rem; text-align: center; font-size: 0.8rem; color: #666;"
      >
        <p>Demo: admin / Admin123! or john / Password123!</p>
      </div>
    </div>
    <script type="module" src="/static/js/login.js"></script>
  </body>
</html>
```

- Add the JavaScript to handle the form submission. This is where we call our `/login` endpoint.

  **File: `backend/static/js/login.js`**

```javascript
document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const errorDiv = document.getElementById("error-message");
  errorDiv.classList.remove("show");

  const username = e.target.elements.username.value;
  const password = e.target.elements.password.value;

  try {
    // The /login endpoint expects 'x-www-form-urlencoded' data, NOT JSON.
    // We use URLSearchParams to create this format.
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const response = await fetch("/api/auth/login", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Login failed");
    }

    // SUCCESS! Store the token in localStorage.
    // localStorage persists data even after the browser is closed.
    localStorage.setItem("access_token", data.access_token);

    // Redirect to the main application page.
    window.location.href = "/";
  } catch (error) {
    errorDiv.textContent = error.message;
    errorDiv.classList.add("show");
  }
});
```

- Finally, tell FastAPI to serve this page.

  **Modify `backend/app/main.py`:**

```python
# In create_application(), add a new route for /login
@app.get("/login", response_class=FileResponse, tags=["Frontend"])
def serve_login_page():
  return FileResponse("static/login.html")
```

### Your Turn: Create the "Auth Guard"

We need to protect our main `index.html` page. We'll add a tiny script that runs immediately and redirects to the login page if no token is found.

- Open `backend/static/index.html`.

- Add this script block inside the `<head>` tag.

```html
<head>
  <script>
    // This is our "Auth Guard". It runs before the page loads.
    // It checks for the access token in localStorage.
    // If it's not there, it immediately redirects to the login page.
    if (!localStorage.getItem("access_token")) {
      window.location.href = "/login";
    }
  </script>
  <link rel="stylesheet" href="/static/css/main.css" />
</head>
```

### Your Turn: Update the API Client and App

Our `api-client.js` needs to be updated to send the token with every request. We also need a logout button.

- Modify `backend/static/js/modules/api-client.js`. Change the `request` function to automatically include the token.

```javascript
// In the APIClient class...
async request(endpoint, options = {}) {
  const url = `${this.baseURL}${endpoint}`;

  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  // NEW: Automatically add the Authorization header if a token exists
  const token = localStorage.getItem('access_token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config = { ...options, headers };

  try {
    const response = await fetch(url, config);

    // NEW: If we get a 401 Unauthorized, our token is bad. Log out.
    if (response.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
      throw new Error("Session expired. Please log in again.");
    }

    if (!response.ok) {
      // ... rest of error handling
    }
    return await response.json();
  } catch (error) {
    // ...
  }
}
```

- Modify `backend/static/js/app.js` to add a logout button.

```javascript
// Inside the DOMContentLoaded listener...
const headerActions = document.querySelector(".header-content div:last-child");
const logoutButton = document.createElement("button");
logoutButton.className = "btn btn-secondary btn-sm";
logoutButton.textContent = "Logout";
logoutButton.onclick = () => {
  localStorage.removeItem("access_token");
  window.location.href = "/login";
};
headerActions.appendChild(logoutButton);
```

---

## Stage 5 Complete ✓

You have now implemented a full, secure authentication and authorization system from scratch.

### Final Verification Workflow

- Make sure your `uvicorn` server is running.
- Clear your browser cache and cookies for `127.0.0.1`.
- Navigate to **[http://127.0.0.1:8000](https://www.google.com/search?q=http://127.0.0.1:8000)**.
- You should be **redirected** to `/login`.
- Try to log in with incorrect credentials. You should see an error message.
- Log in with `admin` and `Admin123!`.
- You should be **redirected** to the main application page (`/`).
- The file list should load correctly.
- Click the "Logout" button.

10. You should be redirected back to `/login`.

Congratulations\! Your application is now secure. Ready for Stage 6, where we will implement advanced authorization, roles, and an audit log?

Of course. Let's begin Stage 6.

We've built a secure login system, but right now, every logged-in user can do everything. That's not realistic. This stage is about implementing **Authorization**—the rules that define _what_ a user is allowed to do. We'll introduce user roles, enforce ownership rules, and create a comprehensive audit log to track every important action.

This is where your application starts to feel like a truly professional, secure system.

---

# PDM Tutorial (New Format) - Stage 6: Advanced Authorization & Auditing

**Goal**: To implement a fine-grained authorization system with user roles and ownership rules. We will also build a persistent audit trail to log every critical action, and create an admin-only section in the UI to manage the system.

**What You'll Learn**:

- The difference between **Role-Based Access Control (RBAC)** and **Resource Ownership**.
- How to combine these patterns to create a flexible and secure authorization system.
- How to create "Dependency Factories" in FastAPI to build reusable, role-based security checks.
- How to build a secure, append-only audit log from scratch.
- How to conditionally render UI elements based on a user's role.

---

## 6.1: The "Why" - Authorization Patterns

Authentication answers "Who are you?". Authorization answers "Okay, Alice, what are you allowed to do?". Let's explore the common patterns for answering this question.

### Your Turn: Explore Authorization Concepts

- Create a new learning file: `backend/app/learn_authorization.py`.

- Add the following code. This playground explains the difference between controlling access via roles versus via ownership.

  **File: `backend/app/learn_authorization.py`**

```python
print("--- Learning Authorization Patterns ---")

# ============================================================================
# PATTERN 1: Role-Based Access Control (RBAC)
# ============================================================================
print("\n1. Role-Based Access Control (RBAC)")
print("Concept: Access is determined by the user's role (e.g., 'admin', 'user', 'guest').")
print("Analogy: Your employee ID card's 'level' determines which floors of the building you can access.")

class RBACExample:
  PERMISSIONS = {
    'admin': ['delete_files', 'view_audit_logs'],
    'user': ['checkout_files', 'checkin_files'],
  }

  def can(self, role, action):
    return action in self.PERMISSIONS.get(role, [])

rbac_system = RBACExample()
print(f"Can an 'admin' delete files? {rbac_system.can('admin', 'delete_files')}") # True
print(f"Can a 'user' delete files? {rbac_system.can('user', 'delete_files')}")  # False

# ============================================================================
# PATTERN 2: Resource Ownership
# ============================================================================
print("\n2. Resource Ownership")
print("Concept: You can only modify things that you 'own'.")
print("Analogy: You can only unlock a gym locker that you put your own padlock on.")

class OwnershipExample:
  def can_checkin(self, user_trying_to_checkin, file_lock):
    # The owner of the lock is stored in the lock itself.
    return user_trying_to_checkin == file_lock['owner']

ownership_system = OwnershipExample()
file_lock_owned_by_alice = {'owner': 'alice'}

print(f"Can 'alice' check in the file? {ownership_system.can_checkin('alice', file_lock_owned_by_alice)}") # True
print(f"Can 'bob' check in the file?  {ownership_system.can_checkin('bob', file_lock_owned_by_alice)}")  # False

# ============================================================================
# OUR HYBRID APPROACH: RBAC + Ownership
# ============================================================================
print("\n3. Our Hybrid Approach")
print("We'll use a combination:")
print(" - Ownership: A 'user' can only check in a file they personally checked out.")
print(" - RBAC: An 'admin' can override ownership and check in any file.")
print("This provides both security for everyday use and flexibility for administration.")
```

### ✅ Verification

- Run the playground file from your `backend` directory:

```bash
python -m app.learn_authorization
```

- Read the output and make sure you understand the difference between the two patterns and how we'll combine them. You can delete this file when you're done.

---

## 6.2: Creating the System's "Black Box" - The Audit Log

An audit log is a chronological, append-only record of all important events in a system. It's essential for security, debugging, and compliance. We will build a service to log every checkout, check-in, and administrative action.

### Your Turn: Build the `AuditLogger`

We will add a new, dedicated class to our `file_service.py` to handle this.

- Open `backend/app/services/file_service.py`.

- Add the `AuditLogger` class at the **top** of the file, before the `FileService` class.

  **File: `backend/app/services/file_service.py` (Add this class)**

```python
class AuditLogger:
  """Records all sensitive file operations to an append-only log."""
  def __init__(self, audit_file: Path):
    self.audit_file = audit_file
    if not self.audit_file.exists():
      self.audit_file.write_text('[]')

  def log_action(self, action: str, user: str, filename: str, success: bool, details: dict = None):
    log_entry = {
      "timestamp": datetime.now(timezone.utc).isoformat(),
      "action": action,
      "user": user,
      "filename": filename,
      "success": success,
      "details": details or {}
    }
    try:
      # We use LockedFile to prevent race conditions even in our logging!
      with LockedFile(self.audit_file, 'r+') as f:
        # Reading is complex in r+ mode, we read, seek, then write.
        logs = json.load(f)
        logs.append(log_entry)
        f.seek(0)
        f.truncate()
        json.dump(logs, f, indent=2)
      logger.info(f"AUDIT: User '{user}' performed '{action}' on '{filename}'. Success: {success}")
    except Exception as e:
      logger.error(f"Failed to write to audit log: {e}")
```

### Your Turn: Integrate Auditing into `FileService`

Now, let's use our new `AuditLogger`.

- In `file_service.py`, modify the `FileService.__init__` method to accept an `audit_file` and create an `AuditLogger` instance.

```python
# In the FileService class...
def __init__(self, repo_path: Path, locks_file: Path, audit_file: Path):
  self.repo_path = repo_path
  self.locks_file = locks_file
  self.audit_logger = AuditLogger(audit_file) # NEW
  # ... rest of init
```

- Modify the `checkout_file` method to log both success and failure.

```python
# In the FileService class...
def checkout_file(self, filename: str, user: str, message: str):
  try:
    # ... existing checkout logic ...
    with LockedFile(self.locks_file, 'r+') as f:
      # ...
      locks[filename] = { ... }
      # ...
    # NEW: Log success
    self.audit_logger.log_action("checkout", user, filename, success=True, details={"message": message})
  except ValueError as e:
    # NEW: Log failure
    self.audit_logger.log_action("checkout", user, filename, success=False, details={"error": str(e)})
    raise e # Re-raise the exception
```

- Do the same for `checkin_file`, logging the action. We'll add more details to this log later.

---

## 6.3: Implementing Authorization Logic

Now let's enforce our rules: only admins or the file owner can check in a file.

### Your Turn: Add Ownership Checks to the Service

- In `file_service.py`, modify the `checkin_file` method. We'll add an `is_admin` flag to allow for an override.

  **Modify `FileService.checkin_file`**

```python
def checkin_file(self, filename: str, user: str, is_admin: bool = False):
  with LockedFile(self.locks_file, 'r+') as f:
    locks = json.load(f)

    if filename not in locks:
      raise ValueError(f"File '{filename}' is not currently checked out.")

    # === AUTHORIZATION LOGIC ===
    is_owner = locks[filename]['user'] == user
    if not is_owner and not is_admin:
      raise PermissionError(f"You cannot check in a file locked by '{locks[filename]['user']}'.")
    # ===========================

    del locks[filename]

    f.seek(0)
    f.truncate()
    json.dump(locks, f, indent=4)

    # Log the successful action, noting if it was an override
    self.audit_logger.log_action(
      "checkin", user, filename, success=True,
      details={"admin_override": not is_owner and is_admin}
    )
```

- Add a new method to `FileService` for admins to force-release a lock.

  **Add to `FileService` class**

```python
def force_checkin(self, filename: str, admin_user: str):
  """Forcibly removes a lock. Only for admins."""
  with LockedFile(self.locks_file, 'r+') as f:
    locks = json.load(f)
    if filename not in locks:
      raise ValueError(f"Cannot force check-in: file '{filename}' is not locked.")

    original_owner = locks[filename]['user']
    del locks[filename]

    f.seek(0)
    f.truncate()
    json.dump(locks, f, indent=4)

    self.audit_logger.log_action(
      "force_checkin", admin_user, filename, success=True,
      details={"original_owner": original_owner}
    )
```

### Your Turn: Create Reusable Authorization Dependencies

Let's create a flexible tool in `deps.py` to protect endpoints based on user roles.

- Open `backend/app/api/deps.py`.

- Add the `require_role` "dependency factory". This is a slightly advanced but very powerful pattern. It's a function that _returns_ a dependency.

  **Add to `backend/app/api/deps.py`**

```python
def require_role(allowed_roles: list[str]):
  """
  This is a dependency factory. It returns a dependency function
  that checks if the current user has one of the allowed roles.
  """
  def role_checker(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in allowed_roles:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"You do not have the required permissions. Requires one of: {allowed_roles}"
      )
    return current_user
  return role_checker

# Create specific dependencies we can use in our endpoints
require_admin = require_role(["admin"])
require_user = require_role(["admin", "user"]) # Admins are also users
```

### Your Turn: Secure the API Endpoints

Now, let's use our new dependencies to protect our API.

- Open `backend/app/api/files.py`.

- Import `require_admin` from `deps`.

- Modify the `checkin_file` endpoint to use the user's role.

- Add a new, admin-only endpoint for `force_checkin`.

  **Modify `backend/app/api/files.py`**

```python
# Add require_admin to imports from .deps
from app.api.deps import get_current_user, get_file_service, require_admin

# ... other endpoints ...

@router.post("/checkin")
def checkin_file(
  request: FileCheckinRequest,
  file_service: FileService = Depends(get_file_service),
  current_user: User = Depends(get_current_user)
):
  try:
    is_admin = current_user.role == 'admin' # Check the user's role
    file_service.checkin_file(request.filename, current_user.username, is_admin)
    # ... success response ...
  # ... error handling ...

# --- NEW ADMIN ENDPOINT ---
@router.post("/admin/force-checkin/{filename}", tags=["Admin"])
def force_checkin_file(
  filename: str,
  file_service: FileService = Depends(get_file_service),
  current_user: User = Depends(require_admin) # This endpoint is now admin-only!
):
  """Forcibly checks in a file. Requires admin privileges."""
  try:
    file_service.force_checkin(filename, current_user.username)
    return {"success": True, "message": f"Admin '{current_user.username}' force-checked-in '{filename}'."}
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
```

- Finally, tell `FileService` where to find the `audit.json` file.

  **Modify `backend/app/api/deps.py`**

```python
# In the get_file_service function...
def get_file_service() -> FileService:
  """This dependency creates and provides a FileService instance."""
  return FileService(
    repo_path=settings.BASE_DIR / 'repo',
    locks_file=settings.BASE_DIR / 'locks.json',
    audit_file=settings.BASE_DIR / 'audit.json' # NEW
  )
```

### ✅ Verification

- Go to the docs at **[http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)**.
- You'll see a new "Admin" tag with the `force-checkin` endpoint.
- Try to use it without being logged in as `admin`. It will fail with a `401 Unauthorized` or `403 Forbidden` error.
- Log in as `admin` and try again. It will now work (though it might return a `400 Bad Request` if the file isn't locked, which is correct). You've successfully created an admin-only endpoint\!

---

## 6.4: Building the Admin UI

An admin needs to see their special powers. We'll add an admin panel to the UI that is only visible to users with the "admin" role.

### Your Turn: Add Admin UI Elements

- Add the CSS for an admin panel and a "force check-in" button to `backend/static/css/components.css`.

```css
.admin-panel {
  background: #fffbeb;
  border: 1px solid #fde68a;
  padding: var(--spacing-4);
  margin-bottom: var(--spacing-6);
  border-radius: 0.5rem;
}
.btn-danger {
  background-color: var(--color-danger-500);
  color: white;
}
```

- In `index.html`, add a placeholder `div` for the admin panel, right after the `<header>` and before the `<main>` tag.

```html
<div id="admin-panel-container"></div>
```

- Modify `app.js` to show the admin panel and add the "Force Checkin" button _only if the user is an admin_.

  **Add to `backend/static/js/app.js`**

```javascript
// In your DOMContentLoaded listener, right at the top...
const userRole = localStorage.getItem("user_role"); // Get role from login
const username = localStorage.getItem("username");

if (userRole === "admin") {
  const adminPanelContainer = document.getElementById("admin-panel-container");
  adminPanelContainer.innerHTML = `
    <div class="container admin-panel">
      <strong>Admin Panel:</strong> You are logged in with administrative privileges.
    </div>
  `;
}

// Now, modify the createFileElement function...
function createFileElement(file) {
  // ... all the existing code to create the element ...

  if (file.status === "checked_out") {
    actionButton.textContent = "Checkin";
    actionButton.onclick = () => handleCheckin(file.name);

    // --- NEW AUTHORIZATION UI LOGIC ---
    const isOwner = file.locked_by === username;
    if (!isOwner && userRole !== "admin") {
      actionButton.disabled = true; // Disable if not owner and not admin
      actionButton.title = `Locked by ${file.locked_by}`;
    }

    // Add Force Checkin button for admins if they are not the owner
    if (userRole === "admin" && !isOwner) {
      const forceBtn = document.createElement("button");
      forceBtn.className = "btn btn-danger btn-sm";
      forceBtn.textContent = "Force Checkin";
      forceBtn.onclick = () => handleForceCheckin(file.name);
      actionsDiv.appendChild(forceBtn);
    }
  }
  // ... rest of the function
  return div;
}

// Add the new handler function for the force checkin button
async function handleForceCheckin(filename) {
  if (
    !confirm(
      `ADMIN ACTION: Are you sure you want to forcibly check in '${filename}'?`
    )
  ) {
    return;
  }
  try {
    await apiClient.post(`/api/files/admin/force-checkin/${filename}`);
    toast.success(`'${filename}' has been forcibly checked in.`);
    loadFiles();
  } catch (error) {
    toast.error(`Failed to force checkin: ${error.message}`);
  }
}
```

_(Note: You'll also need to add a generic `post` method to your `api-client.js` if it doesn't already have one that can handle URLs without a body.)_

---

## Stage 6 Complete ✓

You have now implemented a full authorization layer with roles, ownership, and a complete audit trail.

### Final Verification Workflow

- **Log in as the normal user (`john`)**:

- Verify you **do not** see the Admin Panel.
- Checkout a file. The "Checkin" button should be enabled for you.
- Log out.

- **Log in as the admin (`admin`)**:

- Verify you **do see** the Admin Panel.
- Look at the file checked out by `john`. The regular "Checkin" button should be enabled (because you're an admin), and you should also see a red "Force Checkin" button.
- Click "Force Checkin". The action should succeed.
- Verify the file is now "available".

- **Check the logs**:

- Open the `backend/audit.json` file. You should see a complete history of every checkout, check-in, and the "force_checkin" action you just performed, all stamped with the correct user and a timestamp.

**What You Learned**:

- How to implement **RBAC** and **Resource Ownership** for fine-grained control.
- How to create secure, reusable **authorization dependencies** in FastAPI.
- The importance of an **audit log** and how to build one safely.
- How to **conditionally render UI elements** for different user roles, enhancing the user experience.

Your application now has a robust security model ready for a production environment.

Ready for Stage 7, where we'll integrate Git for true version control of every file change?

Excellent. Let's begin Stage 7.

So far, we have a robust system for locking and unlocking files. But what happens _between_ the checkout and check-in? How do we track the changes a user makes? The answer is **version control**.

In this stage, we will integrate a full Git repository directly into our application's backend. Every time a user checks in a file, we won't just release the lock; we'll create a permanent, auditable **Git commit**. This gives us a complete history of every change, the ability to see exactly _what_ changed (a "diff"), and the power to roll back to any previous version.

---

# PDM Tutorial (New Format) - Stage 7: Full Version Control with Git

**Goal**: To transform our application from a simple file locker into a true version control system by integrating a programmatic Git backend.

**What You'll Learn**:

- A deeper understanding of **how Git works under the hood** (it's not just "tracking changes").
- How to use the **`GitPython`** library to initialize, commit to, and query a Git repository from your Python code.
- The correct way to integrate versioning into your application's business logic.
- How to build API endpoints and a frontend UI for viewing commit history, seeing line-by-line "diffs," and performing rollbacks.

---

## 7.1: The "Why" - How Git _Actually_ Works

Many people think Git "stores the differences" between files. This is a common misconception. Git's core is much simpler and more powerful: it's a **content-addressable database**.

- **Content-Addressable**: Instead of storing a file by its _name_ (like `/path/to/file.txt`), Git stores it by a unique hash of its _content_ (e.g., `8f35c79...`).
- **Database**: This system of storing content by its hash is essentially a simple key-value database.

This means if you have 10 identical files in your project, Git only stores the content **once**. It also means that if even a single bit changes in a file, it gets a completely new hash, making the system inherently secure against data corruption.

### Your Turn: Explore Git Internals in a Playground

- Create a new learning file: `backend/app/learn_git_internals.py`.

- Add the following code to see how Git's hashing works.

  **File: `backend/app/learn_git_internals.py`**

```python
import hashlib

print("--- Learning How Git Thinks About Content ---")

def git_hash_object(content_bytes: bytes) -> str:
  """
  This function simulates how Git calculates the hash for file content.
  It prepends a header ("blob <size>\0") to the content before hashing.
  """
  header = f"blob {len(content_bytes)}\0".encode()
  full_data = header + content_bytes
  return hashlib.sha1(full_data).hexdigest()

# --- DEMO ---
content1 = b"Hello, PDM World!"
content2 = b"Hello, PDM World!" # Identical content
content3 = b"Hello, PDM world!" # Tiny change (lowercase 'w')

hash1 = git_hash_object(content1)
hash2 = git_hash_object(content2)
hash3 = git_hash_object(content3)

print(f"\nContent 1: '{content1.decode()}'")
print(f" -> Hash: {hash1}")

print(f"\nContent 2: '{content2.decode()}'")
print(f" -> Hash: {hash2}")

print(f"\nContent 3: '{content3.decode()}'")
print(f" -> Hash: {hash3}")

print("\n--- Key Takeaways ---")
print(f"Content 1 and 2 are identical? {content1 == content2}")
print(f" -> Are their hashes identical? {hash1 == hash2} (This is why Git is efficient!)")

print(f"\nContent 1 and 3 are different? {content1 != content3}")
print(f" -> Are their hashes different? {hash1 != hash3} (This is why Git is secure!)")

print("\nGit's Structure:")
print(" - A 'blob' object stores file content (identified by its hash).")
print(" - A 'tree' object stores a directory listing (filenames pointing to blob hashes).")
print(" - A 'commit' object is a snapshot containing a pointer to a tree, author info, a message, and a pointer to the parent commit(s).")
print("This chain of commits is your project's history.")
```

### ✅ Verification

- Run the playground file from your `backend` directory:

```bash
python -m app.learn_git_internals
```

- **Observe the output.** Notice how the identical content produces the exact same hash, while the tiny change in `content3` results in a completely different hash. This is the core principle we'll be leveraging. You can delete this file when you're done.

---

## 7.2: Setting Up the Git Backend

Now, let's add the tools and configuration we need.

### Your Turn: Install Dependencies

- We need the `GitPython` library, which is a powerful Python wrapper around the Git command line.

```bash
pip install GitPython
```

- Update your `requirements.txt` file.

```bash
pip freeze > requirements.txt
```

> **Note**: `GitPython` requires that the `git` command-line tool is installed on your system. It's usually pre-installed on macOS/Linux. For Windows, you'll need to install it from [git-scm.com](https://git-scm.com/download/win).

### Your Turn: Update Configuration

We need to tell our app where to store its new Git repository.

- Open `backend/app/config.py`.

- Add a new setting for the Git repository path. We'll call it `git_repo` to keep it distinct from the user-facing `repo` directory.

  **File: `backend/app/config.py`**

```python
# Inside the Settings class...
class Settings(BaseSettings):
  # ... your existing settings ...

  # --- NEW: Git Settings ---
  GIT_REPO_PATH: Path = settings.BASE_DIR / "git_repo"
  GIT_SYSTEM_USER_NAME: str = "PDM System"
  GIT_SYSTEM_USER_EMAIL: str = "pdm@system.local"

  class Config:
    # ...
```

---

## 7.3: Building the `GitService`

This service will contain all the logic for interacting with our new Git repository.

### Your Turn: Create the `GitService`

- Create a new file: `backend/app/services/git_service.py`.

- Add the following code. This is a substantial piece, but it's broken down into logical sections. Read the comments to understand each part.

  **File: `backend/app/services/git_service.py`**

```python
import logging
from pathlib import Path
from git import Repo, GitCommandError
from git.exc import InvalidGitRepositoryError, NoSuchPathError

from app.config import settings

logger = logging.getLogger(__name__)

class GitService:
  """Manages all programmatic interactions with the Git repository."""

  def __init__(self, repo_path: Path):
    self.repo_path = repo_path
    self.repo: Repo = self._ensure_repo()

  def _ensure_repo(self) -> Repo:
    """
    Checks if a valid Git repo exists at the path. If not, it initializes one.
    This makes our service self-bootstrapping.
    """
    try:
      return Repo(self.repo_path)
    except (InvalidGitRepositoryError, NoSuchPathError):
      logger.warning(f"No Git repository found at {self.repo_path}. Initializing a new one.")
      self.repo_path.mkdir(parents=True, exist_ok=True)
      repo = Repo.init(self.repo_path)
      with repo.config_writer() as config:
        config.set_value("user", "name", settings.GIT_SYSTEM_USER_NAME)
        config.set_value("user", "email", settings.GIT_SYSTEM_USER_EMAIL)

      # Create an initial commit so the repo is valid
      readme_path = self.repo_path / ".pdm-repo"
      readme_path.write_text("This repository is managed by the PDM System.")
      repo.index.add([str(readme_path)])
      repo.index.commit("Initial commit: PDM repository setup")
      logger.info("New Git repository initialized successfully.")
      return repo

  def commit_file(self, filename: str, message: str, author_name: str) -> str:
    """
    Stages and commits a single file.

    Returns the SHA hash of the new commit.
    """
    if not (self.repo_path / filename).exists():
      raise FileNotFoundError(f"Cannot commit non-existent file: {filename}")

    try:
      self.repo.index.add([filename])
      # Only commit if there are actual changes
      if self.repo.is_dirty(path=filename):
        commit = self.repo.index.commit(message, author=f"{author_name} <{author_name}@pdm.local>")
        logger.info(f"Committed '{filename}' with SHA: {commit.hexsha[:7]}")
        return commit.hexsha
      else:
        logger.info(f"No changes to commit for '{filename}'.")
        return self.repo.head.commit.hexsha
    except GitCommandError as e:
      logger.error(f"Git commit failed for '{filename}': {e}")
      raise

  def get_file_history(self, filename: str, limit: int = 50) -> list:
    """
    Gets the commit history for a specific file.
    """
    history = []
    try:
      commits = list(self.repo.iter_commits(paths=filename, max_count=limit))
      for commit in commits:
        history.append({
          "sha": commit.hexsha,
          "message": commit.message.strip(),
          "author": commit.author.name,
          "date": commit.committed_datetime.isoformat(),
        })
    except Exception as e:
      logger.warning(f"Could not get history for '{filename}': {e}")
    return history
```

---

## 7.4: Integrating Git into the `FileService`

Now, let's connect our new `GitService` to our main business logic. The flow will be:

- When a file is checked **in**, we will create a Git **commit**.

### Your Turn: Update the `FileService`

- Open `backend/app/services/file_service.py`.

- Import the new `GitService`.

- Modify `FileService.__init__` to create a `GitService` instance.

- Modify `checkin_file` to copy the updated file into our git repo and create a commit.

  **Modify `backend/app/services/file_service.py`**

```python
# Add this import at the top
from app.services.git_service import GitService
import shutil

class FileService:
  def __init__(self, repo_path: Path, locks_file: Path, audit_file: Path, git_repo_path: Path): # Add git_repo_path
    self.repo_path = repo_path
    self.locks_file = locks_file
    self.audit_logger = AuditLogger(audit_file)
    self.git_service = GitService(git_repo_path) # NEW: Instantiate GitService
    # ...

  def checkin_file(self, filename: str, user: str, is_admin: bool = False):
    # We need the checkout message for our commit message
    lock_info = {}
    with LockedFile(self.locks_file, 'r') as f:
      locks = json.load(f)
      lock_info = locks.get(filename, {})

    commit_message = lock_info.get('message', 'File checked in')

    # ... existing checkin logic inside the with block ...
    with LockedFile(self.locks_file, 'r+') as f:
      # ...
      del locks[filename]
      # ...

    # --- NEW: GIT INTEGRATION ---
    try:
      # 1. Copy the file from the working 'repo' to our version-controlled 'git_repo'
      source_path = self.repo_path / filename
      dest_path = self.git_service.repo_path / filename
      shutil.copy2(source_path, dest_path)

      # 2. Create a commit
      commit_sha = self.git_service.commit_file(filename, commit_message, user)

      # Update the audit log with the commit hash
      self.audit_logger.log_action(
        "checkin", user, filename, success=True,
        details={"admin_override": not is_owner and is_admin, "commit_sha": commit_sha}
      )
    except Exception as e:
      logger.error(f"Git operation failed during check-in for '{filename}': {e}")
      # Log the failure but don't prevent the check-in from completing
      self.audit_logger.log_action(
        "checkin", user, filename, success=True,
        details={"admin_override": not is_owner and is_admin, "git_error": str(e)}
      )
```

- Finally, tell our dependency injector in `deps.py` to provide the new `git_repo_path`.

  **Modify `backend/app/api/deps.py`**

```python
# In get_file_service()
def get_file_service() -> FileService:
  return FileService(
    repo_path=settings.BASE_DIR / 'repo',
    locks_file=settings.BASE_DIR / 'locks.json',
    audit_file=settings.BASE_DIR / 'audit.json',
    git_repo_path=settings.GIT_REPO_PATH # NEW
  )
```

### ✅ Verification

- Stop and restart your `uvicorn` server. The first time it starts, you should see log messages about initializing a new Git repository. A `git_repo` folder will be created in your `backend` directory.
- In your browser, check out a file and then check it in.
- The operation should succeed. Now, check your terminal where `uvicorn` is running. You should see a log message like `INFO: Committed 'PN1001.mcam' with SHA: ...`.
- Open `backend/audit.json`. The log entry for the check-in should now contain the `commit_sha`\!

Our backend is now versioning every change. It's time to build the UI to see this history.

---

## 7.5: Building the Version History UI

We'll add a "History" button to each file item, which will open a modal showing every commit for that file.

### Your Turn: Create the History API Endpoint

- Create a new file for our version control endpoints: `backend/app/api/version_control.py`.

- Add a router and an endpoint to get the history for a specific file.

  **File: `backend/app/api/version_control.py`**

```python
from fastapi import APIRouter, Depends
from app.services.file_service import FileService
from app.api.deps import get_current_user, get_file_service
from app.schemas.auth import User

router = APIRouter(prefix="/api/vc", tags=["Version Control"])

@router.get("/history/{filename}")
def get_version_history(
  filename: str,
  file_service: FileService = Depends(get_file_service),
  current_user: User = Depends(get_current_user)
):
  """Gets the Git commit history for a single file."""
  history = file_service.git_service.get_file_history(filename)
  return {"filename": filename, "history": history}
```

- Wire up this new router in `backend/app/main.py`.

```python
# Add the import
from app.api import files, auth, version_control

# Include the router in create_application()
app.include_router(version_control.router)
```

### Your Turn: Build the Frontend History Modal

- Add the CSS for the history modal to `backend/static/css/components.css`.

```css
.commit-item {
  padding: var(--spacing-3);
  border: 1px solid var(--border-default);
  border-radius: 0.25rem;
  margin-bottom: var(--spacing-3);
}
.commit-message {
  font-weight: 600;
}
.commit-meta {
  font-size: 0.8rem;
  color: var(--text-secondary);
}
.commit-sha {
  font-family: monospace;
}
```

- Add the HTML for the history modal to `index.html` (before `</body>`).

```html
<div id="history-modal" class="modal-overlay hidden">
 <div class.modal-content" style="max-width: 800px;">
  <div class="modal-header">
   <h3>History for <span id="history-filename"></span></h3>
   <button class="modal-close">&times;</button>
  </div>
  <div id="history-list"></div>
 </div>
</div>
```

- Update your `api-client.js` with a new method to call our endpoint.

```javascript
// In APIClient class
async getFileHistory(filename) {
  return this.get(`/api/vc/history/${filename}`);
}
```

- Finally, update `app.js` to bring it all together.

  **Modify `backend/static/js/app.js`**

```javascript
// At the top, with other modal instances
const historyModal = new ModalManager("history-modal");

// Modify createFileElement to add the History button
function createFileElement(file) {
  // ... after creating the checkin/checkout button ...
  const historyButton = document.createElement("button");
  historyButton.className = "btn btn-secondary btn-sm";
  historyButton.textContent = "📜 History";
  historyButton.onclick = (e) => {
    e.stopPropagation(); // Prevent the item click from firing
    showHistory(file.name);
  };
  actionsDiv.appendChild(historyButton);
  // ...
}

// Add this new function to handle showing the history
async function showHistory(filename) {
  document.getElementById("history-filename").textContent = filename;
  const historyList = document.getElementById("history-list");
  historyList.innerHTML = "<p>Loading history...</p>";
  historyModal.open();

  try {
    const data = await apiClient.getFileHistory(filename);
    if (data.history.length === 0) {
      historyList.innerHTML = "<p>No version history for this file yet.</p>";
      return;
    }

    historyList.innerHTML = data.history
      .map(
        (commit) => `
      <div class="commit-item">
        <p class="commit-message">${commit.message}</p>
        <p class="commit-meta">
          by <strong>${commit.author}</strong> on ${new Date(
          commit.date
        ).toLocaleString()}
          <br>
          Commit: <span class="commit-sha">${commit.sha.substring(0, 7)}</span>
        </p>
      </div>
    `
      )
      .join("");
  } catch (error) {
    historyList.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
  }
}
```

---

## Stage 7 Complete ✓

You have now fully integrated a Git version control system into your application. Every change is tracked, providing a powerful and professional audit trail.

### Final Verification Workflow

- Make sure your server is running. Go to **[http://127.0.0.1:8000](https://www.google.com/search?q=http://127.0.0.1:8000)**.
- Check out a file, giving it a descriptive reason (e.g., "Adjusted toolpath for OP1").
- Check the file back in. A commit is created in the background.
- Click the "📜 History" button for that file.
- The history modal should appear, showing the commit you just made, complete with your username, the date, and the commit message\!

**What You Learned**:

- How Git's content-addressable system works.
- How to use `GitPython` to programmatically initialize, add to, and commit to a repository.
- How to cleanly integrate this versioning logic into your existing `FileService`.
- How to build an API and a UI to display version history to the user.

You're now ready for Stage 8, where we'll implement real-time updates using WebSockets, so that changes made by one user appear instantly for everyone else without needing to refresh the page.

Ready for Stage 8?
