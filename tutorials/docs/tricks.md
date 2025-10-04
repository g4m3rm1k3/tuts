from fastapi import FastAPI
Absolutely — let’s make a comprehensive, in -depth tutorial on managing Python projects with FastAPI, tests, MkDocs, virtual environments, and import issues on Windows and macOS, including common pitfalls and fixes. I’ll structure it logically so you can keep it as a reference.

⸻

Python Project Setup & Troubleshooting: FastAPI + Tests + MkDocs

This guide covers: 1. Project structure best practices 2. Virtual environments(venv) 3. Running FastAPI with uvicorn 4. Testing with pytest and TestClient 5. MkDocs setup 6. Common pitfalls on Windows and macOS 7. Fixes for imports, PYTHONPATH, and virtual environment conflicts

⸻

1. Recommended Project Structure

A clean layout avoids most import issues:

project_root/
├── app/
│ ├── **init**.py
│ └── main.py # FastAPI instance defined here
├── tests/
│ └── test_main.py
├── templates/
│ └── index.html # MkDocs or FastAPI templates
├── docs/
│ └── index.md # MkDocs content
├── pyproject.toml # Optional for pdm/poetry
└── requirements.txt # or pdm.toml, poetry.lock

    •	app/__init__.py makes app a Python package.
    •	app/main.py contains:

app = FastAPI()

@app.get("/")
async def read_root():
return {"message": "Hello from the PDM Backend!"}

    •	tests/test_main.py uses:

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_root():
response = client.get("/")
assert response.status_code == 200
assert response.json()["message"] == "Hello from the PDM Backend!"

⸻

2. Virtual Environments (venv)

Virtual environments isolate dependencies. You can have one venv for multiple projects if dependencies overlap.

Creating a venv

Windows:

python -m venv .venv
.\.venv\Scripts\Activate.ps1 # PowerShell

# or

.\.venv\Scripts\activate.bat # cmd

macOS/Linux:

python3 -m venv .venv
source .venv/bin/activate

    •	Install dependencies inside the venv:

pip install fastapi uvicorn pytest mkdocs

Common venv pitfalls 1. Multiple venvs in parent folders → Python may use the wrong one, causing ModuleNotFoundError. 2. IDE interpreters may default to system Python instead of your venv. Check PyCharm/VSCode interpreter settings.

⸻

3. Running FastAPI with uvicorn

From project root:

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Breakdown
• app.main → Python module path (folder.package)
• :app → variable in main.py

Optional: shorter import if you export app in **init**.py:

# app/**init**.py

from .main import app
**all** = ["app"]

Then run:

uvicorn app:app --reload

⸻

4. Testing with pytest and TestClient

Minimal test

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_root():
response = client.get("/")
assert response.status_code == 200
assert response.json()["message"] == "Hello from the PDM Backend!"

Common import issues
• ModuleNotFoundError: No module named 'app' → caused by Python not finding the project root in PYTHONPATH.

Fix:

# Windows PowerShell

$env:PYTHONPATH = (Get-Location)
pytest

# macOS/Linux bash

export PYTHONPATH=$(pwd)
pytest

    •	Always run pytest from the project root.

⸻

5. MkDocs Setup
   1. Install:

pip install mkdocs

    2.	Initialize:

mkdocs new docs

    3.	Serve site locally:

mkdocs serve

    4.	Build static site:

mkdocs build

Common MkDocs issues
• File changes not detected → run mkdocs serve from project root.
• Cannot import Python modules in MkDocs plugins → ensure venv is activated, or set PYTHONPATH in the same session.

⸻

6. Common Pitfalls on Windows and macOS

Problem Cause Fix
ModuleNotFoundError Python can’t find your package Run pytest from project root; set PYTHONPATH if needed
Wrong venv used Multiple venvs on machine Activate correct venv
Imports work in REPL but fail in pytest Different working directory Always run from project root
uvicorn: command not found venv not activated Activate venv first, or run python -m uvicorn app.main:app
MkDocs can’t find Python modules Different venv or path Activate venv; optional $env:PYTHONPATH
Windows path issues Backslashes, spaces, OneDrive paths Use quotes "C:\Path With Spaces"; PowerShell handles \
macOS/Linux permission issues Executable not found Use chmod +x or prefix python3 -m

⸻

7. Tips & Tricks
   1. Always run commands from project root.
   2. Keep one venv per machine/project combination to avoid conflicts.
   3. Use absolute imports (from app.main import app) rather than relative imports for tests and uvicorn.
   4. Optional: create a run.ps1 (Windows) or run.sh (macOS/Linux) to activate venv and run uvicorn/tests in one command.

Example run.ps1 for Windows:

# Activate venv

.\.venv\Scripts\Activate.ps1

# Set PYTHONPATH

$env:PYTHONPATH = (Get-Location)

# Run uvicorn

uvicorn app.main:app --reload

# Run tests

pytest

⸻

✅ Summary
• Project structure: app/ package + tests/ folder
• Imports: use absolute imports from app.main import app
• vPython path: $env:PYTHONPATH = (Get-Location) temporarily fixes import issues
• Run everything from project root
• Uvicorn/MkDocs: don’t need PYTHONPATH unless importing local packages in MkDocs plugins
• Avoid multiple venvs unnecessarily

⸻

If you want, I can also create a diagram showing the workflow with uvicorn, tests, MkDocs, and PYTHONPATH, including what breaks and why, so you can use it as a quick troubleshooting map.

Absolutely! Let’s do a full, step-by-step deep dive into asynchronous JavaScript, from the old-school AJAX days to modern async/await. I’ll explain how it works under the hood, why it evolved, and give examples. I’ll keep it concise but thorough, so you can reference it later.

⸻

JavaScript Asynchronous Programming Tutorial: AJAX → Promises → Async/Await

⸻

1. Why Asynchronous JavaScript Exists

JavaScript runs in a single-threaded environment, meaning it can only do one thing at a time.
• If you make a network request synchronously, the browser “freezes” until the request finishes.
• To avoid this, JS introduced asynchronous programming—allowing long operations to happen in the background while the main thread keeps running.

⸻

2. The Old-School Way: AJAX (XMLHttpRequest)

Before fetch or promises, we used XMLHttpRequest:

const xhr = new XMLHttpRequest();

// Step 1: Setup the request
xhr.open("GET", "/api/files");

// Step 2: Setup a callback for when it finishes
xhr.onload = function() {
if (xhr.status === 200) {
const files = JSON.parse(xhr.responseText);
console.log(files);
} else {
console.error("Request failed", xhr.status);
}
};

// Step 3: Send the request
xhr.send();

Problems with this approach:
• Callback hell: nesting multiple callbacks quickly becomes unreadable.
• Hard to handle errors cleanly.
• No composability (easy chaining of multiple async tasks).

⸻

3. Enter Callbacks

A simpler example of callbacks:

function fetchFiles(callback) {
setTimeout(() => {
const files = ["file1.txt", "file2.txt"];
callback(files);
}, 1000);
}

fetchFiles((files) => {
console.log("Files loaded:", files);
});

Downsides:
• Easy to get into “callback hell”:

loadUser(userId, (user) => {
loadPosts(user.id, (posts) => {
loadComments(posts[0].id, (comments) => {
console.log(comments);
});
});
});

⸻

4. Promises

Promises solve callback hell by representing an async operation that will eventually finish (resolve or reject).

Creating a promise:

function fetchFiles() {
return new Promise((resolve, reject) => {
setTimeout(() => {
const success = true;
if (success) resolve(["file1.txt", "file2.txt"]);
else reject("Failed to load files");
}, 1000);
});
}

fetchFiles()
.then(files => console.log("Files:", files))
.catch(err => console.error(err));

Key points:
• Promise has three states: pending → fulfilled → rejected
• .then() handles success, .catch() handles errors.
• Can chain promises easily:

fetchFiles()
.then(files => fetchDetails(files[0]))
.then(details => console.log(details))
.catch(err => console.error(err));

⸻

5. Fetch API (Modern Replacement for XMLHttpRequest)

fetch() returns a promise, so it works naturally with .then():

fetch("/api/files")
.then(response => {
if (!response.ok) throw new Error("Network error");
return response.json();
})
.then(files => console.log(files))
.catch(err => console.error(err));

    •	Default method is GET.
    •	Returns a Response object, which needs response.json() to parse JSON.
    •	Still promise-based, can chain .then().

⸻

6. Async/Await

async/await is syntactic sugar over promises. It allows async code to look synchronous.

async function loadFiles() {
try {
const response = await fetch("/api/files");
if (!response.ok) throw new Error("Network error");
const files = await response.json();
console.log(files);
} catch (err) {
console.error(err);
}
}

loadFiles();

Key points:
• async functions always return a promise.
• await pauses execution until the promise resolves or rejects.
• Makes error handling simple with try/catch.
• Can be combined with Promise.all for parallel async tasks:

async function loadAllFiles() {
const urls = ["/api/files1", "/api/files2"];
const results = await Promise.all(urls.map(url => fetch(url).then(r => r.json())));
console.log(results);
}

⸻

7. Error Handling Differences

Method Error Handling
Callbacks Manual (if (err) ...)
Promises .catch()
Async/Await try/catch

Example with async/await:

async function getData() {
try {
const data = await fetch("/api/missing").then(res => res.json());
} catch (error) {
console.error("Something went wrong:", error);
}
}

⸻

8. Advanced: Promises Under the Hood
   • Promises are objects with internal states.
   • Each .then() returns a new promise, enabling chaining.
   • Example:

const promise = new Promise((resolve) => resolve(1));

promise
.then(value => value + 1)
.then(value => value \* 2)
.then(console.log); // Outputs 4

    •	You can also create deferred promises manually:

function deferred() {
let resolve, reject;
const promise = new Promise((res, rej) => {
resolve = res;
reject = rej;
});
return { promise, resolve, reject };
}

const d = deferred();
d.promise.then(console.log);
d.resolve("Hello World"); // Logs "Hello World"

⸻

9. Combining Async Techniques
   • Sequential vs Parallel:

// Sequential
const a = await fetch("/a").then(r => r.json());
const b = await fetch("/b").then(r => r.json());

// Parallel
const [a, b] = await Promise.all([
fetch("/a").then(r => r.json()),
fetch("/b").then(r => r.json())
]);

    •	Timeout helper (simulate async delay):

const delay = ms => new Promise(res => setTimeout(res, ms));

async function run() {
console.log("Start");
await delay(1000);
console.log("After 1 second");
}

⸻

10. Bonus: AbortController
    • Cancel fetch requests:

const controller = new AbortController();
fetch("/api/files", { signal: controller.signal })
.then(r => r.json())
.then(console.log)
.catch(err => console.error(err));

controller.abort(); // Cancel the request

⸻

Summary Timeline

Era How to do async Pros Cons
2000s XMLHttpRequest Works Callback hell, messy
2010s Callbacks Simple for 1 task Nested callbacks
2015 Promises Chainable, readable Slightly verbose
2015+ Fetch API + Promises Cleaner network calls Still chaining
2017+ Async/Await Synchronous style, easy error handling Must use in async function

⸻

11. Tips for Mastery
    1.  Always handle errors—network requests fail often.
    2.  Use Promise.all for parallel requests, await for sequential.
    3.  Don’t overuse innerHTML += in loops—build a string first.
    4.  Remember: async/await is just promises under the hood.
    5.  Understand event loop and microtasks—promises always run after synchronous code completes.

⸻

I can also make a diagram showing how callbacks → promises → async/await flow in the event loop, which helps visually understand what happens under the hood.

It looks like you're running into a syntax issue because you're using a `curl` command designed for a Unix-style shell (like Bash on Linux/macOS) inside of **Windows PowerShell**. PowerShell has its own way of handling commands and line continuation.

The error `The term '-H' is not recognized as a name of a cmdlet` is the key clue. PowerShell isn't seeing `curl` as one single command; it's trying to interpret `-H` and `-d` as separate commands.

---

### The PowerShell Way (Recommended) 💡

The best way to make API requests in PowerShell is to use its native command, `Invoke-RestMethod`. It's cleaner and designed for this environment.

Here is the equivalent of your `curl` command:

```powershell
# 1. Define the request body as a PowerShell object (hashtable)
$body = @{
    filename = "PN1001_OP1.mcam"
    user     = "mmclean"
    message  = "Editing fixture plate"
}

# 2. Convert the object to a JSON string
$jsonBody = $body | ConvertTo-Json

# 3. Send the request
Invoke-RestMethod -Uri http://127.0.0.1:8080/api/checkout -Method Post -ContentType "application/json" -Body $jsonBody
```

This is the idiomatic PowerShell approach and is much easier to read and debug.

---

### Fixing Your `curl` Command for PowerShell ✅

If you want to make the original `curl` command work in PowerShell, you need to make two changes:

1.  **Line Continuation:** PowerShell uses a backtick (`` ` ``) to continue a command on the next line, not a backslash (`\`).
2.  **Quotes:** PowerShell can be tricky with nested quotes. It's often safer to write the JSON on a single line.

Here is the corrected version of your command:

```powershell
curl -X POST http://127.0.0.1:8080/api/checkout `
-H "Content-Type: application/json" `
-d '{ "filename": "PN1001_OP1.mcam", "user": "mmclean", "message": "Editing fixture plate" }'
```

**Alternatively, and often easier, is to write it all on one line to avoid continuation issues:**

```powershell
curl -X POST http://127.0.0.1:8080/api/checkout -H "Content-Type: application/json" -d '{"filename": "PN1001_OP1.mcam", "user": "mmclean", "message": "Editing fixture plate"}'
```

### Summary of the Problem

| Shell                    | Line Continuation | How it sees `-H`, `-d`                     |
| :----------------------- | :---------------- | :----------------------------------------- |
| **Bash** (Linux/macOS)   | Backslash `\`     | As flags/options for `curl`.               |
| **PowerShell** (Windows) | Backtick `` ` ``  | As separate, unknown commands (`cmdlets`). |
