Section 0 — Environment Setup (Deep Dive)

This is the foundational chapter for your PDM tutorial. Treat it as the “apprentice’s primer”: everything from how Python isolation works, to the commands you’ll run every day, to the common pitfalls people asked about for years. Paste this as a single MkDocs section and keep it nearby — you’ll refer to it constantly.

⸻

0.0 Goals for this section
• Get a reproducible local dev environment you can trust.
• Understand why a Python virtual environment (venv) exists and how it works under the hood.
• Be able to create, activate, use, and troubleshoot venvs on macOS, Linux, Windows (including WSL).
• Learn best practices for dependency management, locking, and editor/CI integration.
• Quick checklist + exercises you can copy into MkDocs.

⸻

0.1 Quick summary (TL;DR)
• A virtual environment isolates a project’s Python interpreter and installed packages from the system Python.
• Create it: python3 -m venv .venv (or use Poetry/virtualenv/pyenv if you prefer).
• Activate it: source .venv/bin/activate (macOS/Linux) or .venv\Scripts\Activate.ps1 (PowerShell).
• Always use python -m pip ... (not plain pip) so you use the pip belonging to that interpreter.
• Use a lockfile (requirements.txt/pip-tools/poetry.lock) in CI and for reproducibility.
• Never commit .venv/ to Git — ignore it in .gitignore.

⸻

0.2 Why we need virtual environments — motivation & history

Before virtual environments, Python packages were installed globally. Problems that followed:
• Different projects required different versions of the same package → dependency hell.
• Upgrading a package for one project could silently break other projects.
• System package upgrades (or OS package manager changes) could break Python apps.
• Permissions: installing system-wide packages requires root on many systems.

Virtual environments solve these by giving each project its own site-packages and, optionally, its own interpreter version. This isolates dependencies and makes your project reproducible and safe to run in CI and on other machines.

Aside: Tools that surfaced later (Conda, Poetry, Pipenv, pyenv) add features: cross-language packages (Conda), deterministic lockfiles and project metadata (Poetry), or per-user Python version management (pyenv). A solid mental model of venv makes all of these easier to understand.

⸻

0.3 What a venv actually contains — the internals

A venv created with python -m venv .venv will usually contain:

.venv/
├─ bin/ # (Scripts\ on Windows) python, pip, site-packages activators
├─ lib/pythonX.Y/site-packages/ # installed packages
├─ pyvenv.cfg # configuration (points to base interpreter info)

Key behaviors:
• Interpreter: Usually the venv references the system interpreter used to create it (via pyvenv.cfg). On some systems the venv contains copies or symlinks of the python binary.
• site-packages: Packages installed into the venv live here and are preferred on sys.path when the venv’s Python runs.
• Activation: activate scripts change shell environment variables (mostly PATH) so the venv python/pip are first on the path. Activation is a convenience — you can still call the venv Python directly via .venv/bin/python.
• Scripts: When packages provide CLI scripts, pip installs those into .venv/bin/ (or Scripts\ on Windows). This is why activate puts the venv bin/ directory first on PATH.

Important rule: When in doubt, run the interpreter via the full path or python -m <module> to ensure you’re using the venv’s tools:

# Preferred to avoid ambiguity

.venv/bin/python -m pip install fastapi
.venv/bin/python -m pip freeze

⸻

0.4 Creating a venv — commands for each OS

macOS / Linux

# create

python3 -m venv .venv

# activate (bash / zsh)

source .venv/bin/activate

# sanity check

python --version
which python # should show .venv/bin/python
python -m pip install --upgrade pip setuptools wheel

Windows (PowerShell)

# create

python -m venv .venv

# activate (PowerShell)

.venv\Scripts\Activate.ps1

# if you hit execution policy errors, run PowerShell as admin and:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# or use the cmd activation

.\.venv\Scripts\activate.bat

Windows (cmd)

.\.venv\Scripts\activate.bat

WSL (Windows Subsystem for Linux)

Treat it like Linux — create & activate inside WSL, not in Windows.

⸻

0.5 Best practices for naming & placement
• Use a project-local .venv/ (leading dot) at the project root. VSCode auto-detects .venv by default.
• Add .venv/ to .gitignore.
• Avoid committing the venv. Instead commit requirements.txt, pyproject.toml, and a lockfile.
• For CI, recreate the venv (or just pip install -r requirements.txt in the CI runner).

⸻

0.6 Dependency management patterns — workflows

Minimal: pip + requirements.txt
• Install packages: python -m pip install fastapi uvicorn
• Freeze: python -m pip freeze > requirements.txt
• Recreate: python -m pip install -r requirements.txt

Pros: simple, widely supported.
Cons: requirements.txt can pin transitive versions that you didn’t choose.

Better: pip-tools (pip-compile, pip-sync)
• requirements.in contains direct dependencies
• pip-compile creates requirements.txt with pinned transitive versions
• pip-sync installs exact versions

Good for projects that want deterministic installs without changing packaging model.

Modern: pyproject.toml + Poetry
• pyproject.toml declares project metadata & dependencies
• poetry.lock ensures deterministic installs
• poetry install recreates environment

Poetry often manages virtual environments automatically, but many teams prefer to use poetry only for dependency management and keep .venv visible.

Global CLI tools: pipx
• Use pipx to install development tools (black, pre-commit, poetry) globally but isolated, so you avoid polluting system packages.

⸻

0.7 Commands & snippets you will use continuously

# create venv

python3 -m venv .venv

# activate (macOS/Linux)

source .venv/bin/activate

# upgrade packaging tools

python -m pip install --upgrade pip setuptools wheel

# install packages

python -m pip install fastapi uvicorn

# list packages and versions

python -m pip list

# freeze to requirements

python -m pip freeze > requirements.txt

# install exact pinned versions

python -m pip install -r requirements.txt

# check for dependency conflicts

python -m pip check

# uninstall

python -m pip uninstall -r requirements.txt -y

⸻

0.8 Editor integration — VSCode and IDEs

VSCode
• If you have .venv at your project root, VSCode usually auto-detects it. If not:
• Open Command Palette → Python: Select Interpreter → choose ./.venv/bin/python.
• Set python.pythonPath or use workspace settings:

// .vscode/settings.json
{
"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
"python.formatting.provider": "black",
"editor.formatOnSave": true
}

    •	For debugging uvicorn apps, point the debug configuration to ${workspaceFolder}/.venv/bin/python.

PyCharm / IntelliJ
• Configure a new Python interpreter and point it to .venv/bin/python.

⸻

0.9 Reproducibility & CI
• Always use a lockfile or pinned requirements.txt in CI.
• Example GitLab CI snippet:

image: python:3.11
stages: [test]
before_script:

- python -m venv .venv
- source .venv/bin/activate
- python -m pip install -U pip
- pip install -r requirements.txt
  test:
  script: - pytest -q

      •	Consider tox for matrix testing across Python versions.

⸻

0.10 Security & maintenance tips
• Run pip list --outdated occasionally; use python -m pip install -U <pkg> carefully.
• Use tools like bandit for security linting, safety for known-vuln scanning, or GitHub/GitLab dependency scanners.
• Pin versions for deployments. For development, you can keep looser constraints but lock before release.

⸻

0.11 Common pitfalls & FAQ (the “questions asked over the years”)

Q — pip installs packages globally even though I activated venv. Why?
A — You’re likely calling a different pip. Use python -m pip to ensure pip from the active Python is used. Check which pip / where pip.

Q — My shebang points to system Python (#!/usr/bin/python3) and not the venv.
A — Use #!/usr/bin/env python3 in scripts or run scripts with the venv Python: .venv/bin/python script.py. The shebang is used only when the script is executed directly and depends on the PATH.

Q — I committed .venv/ and the repo is huge. How do I fix it?
A — Remove it from git history if necessary (use git rm -r --cached .venv and add to .gitignore). For large repos that already shipped, use git filter-repo or bfg to remove history (dangerous — be careful).

Q — My PowerShell won’t run the Activate script (ExecutionPolicy error).
A — Run as admin and set Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser (or use the .bat activator).

Q — Why not use sudo pip install?
A — sudo pip install modifies system files and can break your OS-managed Python packages. Use venv or pipx for tools.

Q — Why does my venv keep using an old Python version?
A — A venv ties to the interpreter used to create it. If you installed a new Python, create a new venv with the newer interpreter.

Q — What about pyenv?
A — pyenv manages multiple installed Python versions (so you can create venvs with a specific Python). Good complement to venv when you need to test multiple Python versions.

Q — Should I use virtualenv vs venv vs conda vs poetry?
A — Short answers:
• venv: included in stdlib; simple, portable.
• virtualenv: older tool with some extra features and speed on older Pythons.
• conda: package manager + environment manager; good for scientific stacks that need compiled dependencies.
• poetry: modern dependency & packaging manager with lockfiles and build tooling. Great for app libraries and deterministic installs.

Choose based on your project needs. For this tutorial, start with venv + pip and later explore Poetry for packaging.

⸻

0.12 Example .gitignore snippet (project root)

# Python

**pycache**/
.venv/
_.py[cod]
_.egg-info/

# Editor

.vscode/
.idea/

⸻

0.13 Minimal reproducible example — put this in your repo now

File: backend/main.py

#!/usr/bin/env python3

# backend/main.py — minimal script to prove venv/interpreter works

def main():
print("hello from python (venv check)")

if **name** == "**main**":
main()

Commands to run:

cd pdm-project/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python backend/main.py

# -> "hello from python (venv check)"

(If you prefer Windows PowerShell, replace source .venv/bin/activate with .venv\Scripts\Activate.ps1.)

⸻

0.14 Exercises (copy into your MkDocs checklist) 1. Create the repo skeleton (if you haven’t already). Add .venv/ to .gitignore. 2. Create a venv in pdm-project/backend and activate it. Confirm interpreter with which python / where python. 3. Run backend/main.py inside the activated venv. Paste the output into your MkDocs notes. 4. pip install fastapi uvicorn inside the venv. Then python -m pip freeze > requirements.txt. Commit requirements.txt but not .venv/. 5. Optional: install pre-commit and add Black + isort hooks; run pre-commit run --all-files.

⸻

0.15 Next steps (what I’ll do for Stage 1)
• Produce the Stage 1 tutorial: FastAPI minimal app with GET / and GET /api/files returning a hard-coded JSON list.
• Include a fully commented backend/main.py for FastAPI, pytest tests, and commands to run with uvicorn.
• Provide a traceability mini-matrix mapping Stage 1 to PSD acceptance criteria.

⸻

Great — I’m glad Section 0 hit the mark. Let’s keep that same deep-dive, every-angle, best practices + historical asides + common pitfalls approach for Section 1.

Here’s Section 1: Project Initialization & Version Control (Git + GitHub/GitLab) in that style:

⸻

Section 1 — Project Initialization & Version Control

1.1 Why We Use Version Control

Before we touch commands, let’s step back:
• What is Version Control?
A system that tracks changes to your codebase (files, directories, commits). It answers questions like:
• Who made this change?
• When was it made?
• Why did it break something?
• How do we roll it back?
• Why Git specifically?
• Distributed: every developer has a full copy of the repo (with history).
• Fast branching/merging.
• Widely adopted: industry standard.
• Tooling: integrates with GitHub, GitLab, Bitbucket, CI/CD systems, IDEs, etc.
• Why not just zip folders for each version?
That’s what many new devs used to do. The problem: no collaboration history, easy to overwrite files, no atomic commits. Git enforces structure and history.

⸻

1.2 Initializing a Git Repository

Step 1: Navigate into your project folder

cd myproject

    •	This tells the shell: “everything I do next applies to this directory.”
    •	Think of it like “scoping” — Git will only care about this directory (and subdirs).

Step 2: Initialize Git

git init

    •	Creates a hidden .git/ folder.
    •	This folder stores:
    •	The full history of commits (in a compressed database).
    •	Config files (user info, remotes).
    •	Staging area (aka “index”).

� If .git/ doesn’t exist, it’s not a repo. If you delete .git/, you lose version history.

⸻

1.3 First Commit

Step 1: Add a README

echo "# MyProject" > README.md

    •	README.md is usually the first file in a repo.
    •	Written in Markdown (human + machine friendly).
    •	It describes the project’s purpose, usage, install steps.

Step 2: Stage the file

git add README.md

    •	Staging = “I’m telling Git to prepare this file for the next commit.”
    •	It’s like putting groceries in your cart, but you haven’t checked out yet.

Step 3: Commit

git commit -m "Initial commit: add README"

    •	-m lets you attach a message describing the commit.
    •	Best practice: messages should be imperative mood, concise, and meaningful.
    •	✅ Good: Add login form validation
    •	❌ Bad: Fixed stuff

⸻

1.4 Connecting to a Remote

Most projects live on a remote server (GitHub/GitLab).

Step 1: Create a repo online
• On GitHub: “New Repository” → name → create.
• Do NOT initialize with a README if you already did locally.

Step 2: Add the remote

git remote add origin https://github.com/username/myproject.git

    •	origin = conventional name for the main remote.
    •	You can have multiple remotes (e.g., upstream, staging).

Step 3: Push your commit

git push -u origin main

    •	Push = upload commits from local → remote.
    •	-u = sets the upstream branch, so future git push knows where to go.
    •	main is the new default branch name (GitHub/GitLab).
    •	Used to be master → changed for inclusivity.

⸻

1.5 Git Basics You Must Know (Common Commands)
• git status → see what’s staged, unstaged, or untracked.
• git log → view commit history.
• git diff → see unstaged changes.
• git checkout -b feature-x → create/switch to a new branch.
• git merge branch-x → merge a branch into current branch.
• git pull → fetch + merge changes from remote.

� Best practice:
• Use branches for features.
• Merge via Pull Requests (so code gets reviewed).
• Never commit directly to main unless absolutely necessary.

⸻

1.6 Common Beginner Mistakes
• Forgetting .gitignore
Example: committing venv/ or **pycache**/.
• Solution: add a .gitignore early.
• Python example:

**pycache**/
\*.pyc
venv/
.env

    •	Committing secrets (API keys, passwords).
    •	Git history is permanent. Even if you delete it later, it lives in history.
    •	Solution: use .env files and add them to .gitignore.
    •	Mixing unrelated changes in one commit
    •	Bad: Update login UI and fix DB migration and add new API route
    •	Good: one commit = one logical change. Easier to revert/debug.

⸻

1.7 How This Fits the Real World
• Every company uses Git.
• Most teams use GitHub/GitLab for code hosting + CI/CD.
• Feature branching → Pull Requests → Code Review → Merge → Deploy.

Even if you’re solo, Git is your time machine.

⸻

✅ Section 1 Complete.
At this point you have:
• A Git repo initialized.
• First commit with a README.
• A remote set up on GitHub/GitLab.
• Push/pull working.

Next we’ll move into Section 2: Basic FastAPI Setup where we write our “Hello World” backend.

⸻

Section 2 — First Backend: FastAPI “Hello World” + /api/files (deep dive)

We’re building the first real backend slice of the PDM app. This section gives you a fully runnable FastAPI app, unit tests, a minimal frontend preview (so you can see the flow end-to-end), and detailed explanations — including why we use async, how the event loop works, what Uvicorn does, and a line-by-line commented CSS example that demonstrates theme variables (light/dark) and how they work.

⸻

2.0 Goals for this section
• Implement a minimal FastAPI app with:
• GET / → JSON health/hello (acceptance crit from PSD Stage 1).
• GET /api/files → returns a hardcoded list of file objects in JSON.
• Run the server with Uvicorn and show how docs (/docs) appear automatically.
• Create unit tests using pytest + FastAPI TestClient.
• Mount a static files folder (so the frontend can fetch /api/files).
• Provide a tiny frontend static index.html that fetches /api/files and a fully commented styles.css demonstrating CSS variables for light/dark mode (every line commented).
• Explain async/await, event loop, and when to use async.

⸻

2.1 Traceability (maps back to PSD / tutorial acceptance criteria)
• GET / returns JSON hello — ✅ PSD Stage 1 requirement 1.
• GET /api/files returns static list — ✅ PSD Stage 1 requirement 2.
• Server runs via Uvicorn and exposes interactive docs (/docs) — ✅ PSD Stage 1 requirements 3 & 4.
• Static folder mounted so frontend can later fetch API — prepares Stage 2.

⸻

2.2 Project files to add right now

Add these files to your repo (paths relative to project root):

backend/
└─ main.py
frontend/
└─ static/
├─ index.html
├─ app.js
└─ styles.css
tests/
└─ test_main.py

⸻

2.3 backend/main.py — FastAPI app (fully commented)

# backend/main.py

"""
Minimal FastAPI app for Stage 1:

- GET / -> simple JSON "hello" (health)
- GET /api/files -> returns hardcoded list of files
- mounts frontend/static at /static so you can preview the frontend
  """

from typing import List
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Configure basic logging so we can see startup messages in the console.

# Using standard library logging keeps the app compatible with most deploy tools.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pdm")

# FastAPI creates automatic OpenAPI docs at /docs and /redoc.

app = FastAPI(title="PDM - Core API", version="0.1.0")

# Pydantic model: defines the shape of our "File" JSON object.

# FastAPI uses this model for input validation and (optionally) response models.

class File(BaseModel):
name: str
status: str

# Hardcoded file list (stage 1). Later stages will read from disk or a DB.

HARD_CODED_FILES: List[File] = [
File(name="12-00001.mcam", status="available"),
File(name="12-00002.mcam", status="checked_out"),
File(name="15-00003.mcam", status="available"),
]

@app.get("/", summary="Health / Hello", tags=["health"])
async def root():
"""
Root endpoint. Async handler for a trivial response.
Returning a small JSON object so it's easy to assert in tests and tools.
"""
logger.info("Health check requested")
return {"message": "Hello — PDM API is online"}

@app.get("/api/files", summary="List files (hardcoded)", response_model=List[File], tags=["files"])
async def list_files():
"""
Return the hardcoded files list.
This is 'async' but doesn't do any awaitable I/O yet — that's fine.
FastAPI allows async handlers that do synchronous work.
"""
logger.info("Files list requested") # Convert Pydantic models to dicts (FastAPI handles this for us on return)
return HARD_CODED_FILES

# Mount the static frontend directory at /static so you can open:

# http://localhost:8000/static/index.html

# We keep "/" for the JSON health response to satisfy Stage 1 acceptance criteria.

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Optional: startup event (runs once when the server starts)

@app.on_event("startup")
async def on_startup():
logger.info("Starting PDM Core API...")

Explanations (line-by-line highlights)
• logging.basicConfig(...) — ensures log messages appear in console; use higher logging granularity in production and log to a file/collector (e.g., JSON to stdout for containers).
• app = FastAPI(...) — initializes FastAPI and OpenAPI metadata (docs auto-generated).
• class File(BaseModel) — Pydantic model enforces schema (types, validation).
• @app.get("/") async def root(): — an async endpoint. FastAPI accepts both def (sync) and async def (async). Choosing async def allows safe await inside if needed later.
• app.mount("/static", ...) — exposes the frontend assets.

⸻

2.4 Why async in FastAPI — event loop explained (deep dive)
• Python async/await is cooperative concurrency. It’s ideal for I/O-bound tasks (HTTP, DB queries, file I/O with an async driver).
• The event loop runs tasks and switches context when a coroutine awaits an I/O operation.
• async def endpoints give you non-blocking behavior if you await I/O operations. If your handler does CPU-heavy work (e.g., image processing), async won’t help — offload CPU tasks to worker threads/processes.
• Example: two endpoints that await asyncio.sleep(2) can run concurrently — both waits happen without blocking the server.
• Uvicorn is an ASGI server that runs the event loop (uvloop optionally) and serves FastAPI apps concurrently.

When to use async:
• Use async when calling async libraries (HTTPX async, async DB drivers like asyncpg, aioredis).
• If everything you call is synchronous (blocking), async adds no benefit — you might be better with sync endpoints or run blocking calls in thread executor.

⸻

2.5 Run the server (Uvicorn)

From project root (make sure your venv is activated):

# install runtime deps (inside .venv)

python -m pip install fastapi "uvicorn[standard]" pydantic

# run in dev-mode with autoreload

uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

    •	--reload watches files and restarts server on changes (dev only).
    •	Visit: http://127.0.0.1:8000/ → JSON hello.
    •	Swagger UI: http://127.0.0.1:8000/docs (interactive API explorer).
    •	ReDoc: http://127.0.0.1:8000/redoc.

⸻

2.6 Tests — tests/test_main.py (pytest + TestClient)

# tests/test_main.py

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
res = client.get("/")
assert res.status_code == 200
assert res.json() == {"message": "Hello — PDM API is online"}

def test_files_list():
res = client.get("/api/files")
assert res.status_code == 200
data = res.json()
assert isinstance(data, list) # minimal shape checks
assert "name" in data[0]
assert "status" in data[0]

Run tests:

# install pytest inside venv

python -m pip install pytest

# run tests

pytest -q

Why this test design?
• Quick smoke tests to confirm endpoints respond and return expected shape.
• As real logic is added, tests will expand (auth, DB mock, error scenarios).

⸻

2.7 Minimal frontend — frontend/static/index.html, app.js, styles.css

We include a tiny frontend so you can open http://localhost:8000/static/index.html and see the API in action. The CSS has every line commented to teach how it works — including CSS variables for light/dark mode and theme toggling.

frontend/static/index.html

<!doctype html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>PDM — Files (Stage 1)</title>

  <!-- Link the stylesheet -->
  <link rel="stylesheet" href="/static/styles.css" />

</head>
<body>
  <header class="site-header">
    <h1>PDM — Files (Stage 1)</h1>
    <div class="header-actions">
      <button id="themeToggle" aria-label="Toggle theme">Toggle theme</button>
    </div>
  </header>

  <main>
    <section id="filesSection">
      <h2>Files</h2>
      <div id="filesList" class="files-list">Loading…</div>
    </section>
  </main>

  <footer class="site-footer">
    <small>Stage 1 — FastAPI backend + static UI</small>
  </footer>

  <script src="/static/app.js"></script>
</body>
</html>

frontend/static/app.js — explained, commented JS

// frontend/static/app.js

// Immediately-invoked function to avoid polluting global namespace
(function () {
// Find important DOM nodes
const filesListEl = document.getElementById("filesList");
const themeToggle = document.getElementById("themeToggle");

// Fetch files from the API and render them
async function fetchAndRenderFiles() {
// Show loading state
filesListEl.textContent = "Loading…";

    try {
      // Use fetch to request /api/files from the same origin
      const resp = await fetch("/api/files");
      if (!resp.ok) {
        filesListEl.textContent = `Error: ${resp.status}`;
        return;
      }
      const data = await resp.json();

      // Build a small list
      const ul = document.createElement("ul");
      ul.className = "file-ul";
      data.forEach((f) => {
        const li = document.createElement("li");
        li.className = "file-item";
        li.textContent = `${f.name} — ${f.status}`;
        ul.appendChild(li);
      });

      // Replace loading text with the list
      filesListEl.innerHTML = "";
      filesListEl.appendChild(ul);
    } catch (err) {
      // Network or other unexpected errors
      filesListEl.textContent = "Failed to fetch files.";
      console.error("Error fetching files:", err);
    }

}

// Simple theme toggle: flips data-theme on <html>
function toggleTheme() {
const html = document.documentElement;
const current = html.getAttribute("data-theme") || "light";
const next = current === "light" ? "dark" : "light";
html.setAttribute("data-theme", next);
// Persist user preference locally (simple)
try {
localStorage.setItem("theme", next);
} catch (\_) {}
}

// Load user preference on startup
function loadThemePreference() {
try {
const pref = localStorage.getItem("theme");
if (pref) document.documentElement.setAttribute("data-theme", pref);
} catch (\_) {}
}

// Attach event listeners
themeToggle.addEventListener("click", toggleTheme);

// Initial actions
loadThemePreference();
fetchAndRenderFiles();
})();

⸻

frontend/static/styles.css — every line commented (deep explanation)

Note: comments use /_ ... _/. I explain every significant property. Very verbose on purpose.

/\* ============================================================
styles.css — minimal styling for PDM Stage 1 UI

- Demonstrates CSS variables and data-theme switching
- Every line/property is commented for teaching purposes
  ============================================================= \*/

/_ Define default variables on :root (light theme defaults) _/
/_ :root targets the document root; variables declared here are global _/
:root {
/_ primary color for UI elements (light theme) _/
--color-bg: #ffffff; /_ background color of the page _/
--color-surface: #f7f7f9; /_ surface / card backgrounds _/
--color-text: #0b0b0b; /_ primary text color _/
--color-muted: #6b7280; /_ secondary/muted text _/
--color-accent: #0ea5e9; /_ accent (buttons, links) _/
--color-border: #e5e7eb; /_ subtle border color _/
--radius: 8px; /_ standard border radius for cards _/
--gap: 12px; /_ spacing constant _/
--max-width: 980px; /_ layout max width for content _/
--font-stack: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}

/_ Dark theme overrides.
We target [data-theme="dark"] on the <html> element — cleaner than toggling classes everywhere.
When html[data-theme="dark"] is set, these variables replace the :root ones.
_/
html[data-theme="dark"] {
--color-bg: #0b1020; /_ darker page background for dark mode _/
--color-surface: #0f1724; /_ card/surface color in dark mode _/
--color-text: #e6eef8; /_ light text color for contrast _/
--color-muted: #9aa6b2; /_ lighter muted text _/
--color-accent: #38bdf8; /_ accent slightly brighter in dark mode _/
--color-border: #172030; /_ border color for dark surfaces _/
}

/_ Basic reset and box-sizing _/
/_ box-sizing: border-box makes width/height include padding & border — usually easier to reason about _/
_,
_::before,
_::after {
box-sizing: border-box; /_ include padding & borders in element's total width/height \*/
}

/_ Body styles _/
body {
margin: 0; /_ remove default body margin _/
font-family: var(--font-stack); /_ use the font stack defined above _/
background: var(--color-bg); /_ page background from CSS variable _/
color: var(--color-text); /_ default text color from variable _/
line-height: 1.4; /_ comfortable line height for text _/
-webkit-font-smoothing: antialiased; /_ smoother fonts on macOS _/
-moz-osx-font-smoothing: grayscale; /_ smoother fonts on Firefox/mac _/
}

/_ Page container: centers content and sets a max width _/
main {
max-width: var(--max-width); /_ keep content from getting too wide on large screens _/
margin: 28px auto; /_ center horizontally and add vertical margin _/
padding: 0 var(--gap); /_ horizontal padding using gap variable _/
}

/_ Header _/
.site-header {
display: flex; /_ layout children horizontally _/
align-items: center; /_ vertically center items _/
justify-content: space-between; /_ push title left and actions to the right _/
padding: 18px var(--gap); /_ vertical + horizontal padding _/
background: var(--color-surface); /_ use surface color for the header background _/
border-bottom: 1px solid var(--color-border); /_ subtle bottom border using variable _/
position: sticky; /_ keeps header visible when scrolling _/
top: 0; /_ top offset for sticky behavior _/
z-index: 20; /_ ensure header stays on top of other elements _/
}

/_ Header title _/
.site-header h1 {
margin: 0; /_ remove default heading margins _/
font-size: 1.1rem; /_ slightly larger than body text _/
font-weight: 600; /_ semi-bold for emphasis _/
}

/_ Header actions container (right side) _/
.header-actions {
display: flex; /_ allow multiple actions in a row _/
gap: 8px; /_ small gap between action items _/
align-items: center; /_ vertically center child elements _/
}

/_ Theme toggle button _/
/_ Buttons inherit font settings, but we style for clarity _/
#themeToggle {
background: transparent; /_ transparent background to start _/
border: 1px solid var(--color-border); /_ visible border to show clickable area _/
color: var(--color-text); /_ use text color variable for label _/
padding: 8px 10px; /_ padding for clickable area _/
border-radius: 6px; /_ rounded corners _/
cursor: pointer; /_ pointer cursor communicates clickability _/
font-size: 0.9rem; /_ slightly small text _/
}

/_ Files section heading _/
#filesSection h2 {
margin-top: 0; /_ remove top margin (header already adds spacing) _/
font-size: 1rem; /_ heading scale _/
color: var(--color-text); /_ primary text color _/
}

/_ Files list wrapper _/
.files-list {
margin-top: 10px; /_ spacing above the files list _/
background: var(--color-surface); /_ surface background for the list area _/
border: 1px solid var(--color-border); /_ subtle border for separation _/
padding: 14px; /_ internal padding for content _/
border-radius: var(--radius); /_ rounded corners using the variable _/
min-height: 84px; /_ give area some minimum height for loading state _/
}

/_ file list (ul) _/
.file-ul {
list-style: none; /_ remove default bullets _/
margin: 0; /_ reset default margin _/
padding: 0; /_ reset default padding _/
display: grid; /_ use grid for easy row spacing _/
gap: 8px; /_ gap between list items _/
}

/_ Individual file item _/
.file-item {
padding: 10px; /_ internal spacing for each item _/
border-radius: 6px; /_ rounded corners for each item _/
background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(0,0,0,0.02));
/_ subtle gradient to give depth _/
border: 1px solid rgba(0,0,0,0.04); /_ faint border to separate items _/
font-size: 0.95rem; /_ slightly smaller text for list items _/
}

/_ Footer _/
.site-footer {
padding: 12px var(--gap); /_ internal padding _/
text-align: center; /_ center the footer text _/
color: var(--color-muted); /_ use the muted color variable _/
border-top: 1px solid var(--color-border); /_ subtle top border to separate from content _/
margin-top: 24px; /_ spacing above footer _/
}

/_ Make small screens feel good: responsive tweaks _/
@media (max-width: 600px) {
:root {
--gap: 10px; /_ reduce gap on small screens _/
}
.site-header {
padding: 12px var(--gap); /_ slightly smaller header padding mobile _/
}
main {
margin: 18px auto; /_ smaller vertical spacing on mobile _/
}
}

Why variables + data-theme?
• CSS variables (--var) centralize colors and spacing. Change them once and the whole UI updates.
• Using html[data-theme="dark"] avoids managing classes throughout your DOM and allows easy global theme toggling.
• This pattern scales (you can add prefers-color-scheme media query and default to user OS preference).

⸻

2.8 How the frontend talks to the backend
• The app.js uses fetch("/api/files") — same origin requests. Since the static files are served by the same FastAPI server at /static, things work locally without CORS.
• In a production deployment with separate origins (frontend CDN vs API), you’ll need to enable CORS in FastAPI:

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
CORSMiddleware,
allow_origins=["https://frontend.example.com"],
allow_methods=["GET", "POST"],
allow_headers=["*"]
)

⸻

2.9 Common pitfalls & debugging tips
• ImportError: No module named fastapi — you’re not using the project venv. Activate .venv or use full path: .venv/bin/python -m uvicorn backend.main:app.
• 127.0.0.1:8000 returns 404 for /static/index.html — check app.mount("/static", ...) path and ensure frontend/static folder exists relative to working directory.
• Swagger shows endpoints but trying them returns 500 — inspect terminal logs; check logger and exceptions.
• Tests failing locally but pass in CI — ensure the environment is consistent (python version, deps pinned).

⸻

2.10 Exercises (hands-on) 1. Required: Implement the files above, create the venv, install fastapi and uvicorn, run the server, and verify:
• GET / returns the JSON health message.
• GET /api/files returns the hardcoded list.
• http://127.0.0.1:8000/docs shows the API explorer.
• http://127.0.0.1:8000/static/index.html loads the frontend and shows the list.
• Run pytest and confirm tests pass. 2. Optional pivot: Replace HARD_CODED_FILES with a Python function that reads filenames from an example folder sample_files/ and returns them (no persistence yet). This will prepare you for Stage 3 where we read from disk. 3. Optional experiment: Toggle html[data-theme="dark"] in DevTools and observe styles change. Change variables in runtime via DevTools to see how CSS variables update immediately.

⸻

2.11 Best practices & notes
• Keep handlers small and single-responsibility (one thing per route).
• Keep I/O async where possible (DB calls, HTTP calls). For CPU-bound operations, use background workers (Celery, RQ) or thread/process pools.
• Use Pydantic models for request/response validation — this reduces bugs from unexpected payloads.
• Add request logging (structured logs) later for observability.
• Keep test coverage growing as features are added: start with smoke tests (we did), then add unit/integration tests that mock DBs or use test DBs.

⸻

2.12 What I’ll deliver next (Stage 2 preview)
• A step-by-step Stage 2 tutorial: serve index.html at / (instead of JSON) and add the frontend fetch flow with error handling and a loading spinner.
• Then a Stage 2 “Practical” layer: replace static files with a single-page app scaffold (vanilla → React pivot), demonstrate state management, and implement initial UI for checking file status (UI-only — no persistence yet).

⸻

Great — I’ll continue in the same style. Below is Section 3.1 — Backend: Upload API, written as a MkDocs-ready subpage: naive quick-and-dirty implementation, then a refactor into a production-minded v1, then notes preparing for v2 (DB/cloud storage). Deep explanations, security asides, test files, and commands included. Copy-paste friendly.

⸻

3.1 Backend — File Upload API (Deep Dive)

Goal: Add the first real, stateful behavior to the backend: receive .mcam files from users, store them on disk, and return a JSON response confirming success. We’ll start naïve (get it working), then refactor to a safer, testable, maintainable implementation.

Acceptance criteria (mapped to PSD):
• Accept file uploads via POST /api/files/upload.
• Save the uploaded file to a server-side directory.
• Return JSON with metadata (filename, size, status).
• Validate allowed file types (only .mcam for now).
• Provide tests that assert success and rejection of invalid files.

⸻

3.1.0 Design notes & considerations (why we do things this way)

Before code, some architecture thinking — short and practical:
• Where to store files initially?
For v1 we use the local filesystem under a controlled data/ directory (e.g., data/files/). Pros: simple, visible, easy for tutorial. Cons: not suitable for multi-server scaling, backup, or large files.
• API choice: multipart form POST with Content-Type: multipart/form-data. That’s standard for file uploads and works everywhere.
• Validation: Always validate file type, file size, and filename to avoid directory traversal attacks.
• Security concerns:
• Reject files with unexpected extensions or MIME types.
• Sanitize filenames (strip path segments).
• Limit maximum upload size in the server (both FastAPI & reverse proxy).
• Store uploaded files with a safe internal filename (e.g., prefix with UUID) and keep original filename as metadata.
• Testing: We’ll test both positive and negative cases using FastAPI TestClient and io.BytesIO.

⸻

3.1.1 Naïve (Quick-and-Dirty) Implementation

This is the smallest amount of code that will accept a file and save it — useful to see the end-to-end flow. It intentionally omits many production considerations (size limits, sanitizing, unique filenames) so we can see how it behaves and then harden it.

Files to add / modify
• backend/main.py (extend current app)
• backend/config.py (small constants)
• tests/test_upload_naive.py

Code: naive upload route (backend/main.py — snippet to append)

Add these imports near the top of backend/main.py:

from fastapi import File, UploadFile, HTTPException
from pathlib import Path
import shutil

Then add a small config and route (append after existing routes):

# backend/main.py (append after previous code)

# folder to store uploaded files (naive)

UPLOAD_DIR = Path("data/files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True) # ensure directory exists

@app.post("/api/files/upload", summary="Naive file upload (demo)")
async def upload_file_naive(file: UploadFile = File(...)):
"""
Naive upload endpoint: - Accepts a single file field named 'file' - Writes the uploaded file directly to data/files/<filename> - Returns basic metadata
NOTE: This is intentionally minimal. We'll harden in the next refactor.
""" # Very basic validation: check extension (not sufficient in prod)
if not file.filename.lower().endswith(".mcam"):
raise HTTPException(status_code=400, detail="Only .mcam files are allowed (naive)")

    dest_path = UPLOAD_DIR / file.filename

    # Save file to disk. Using file.file (SpooledTemporaryFile) is acceptable here.
    with dest_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"filename": file.filename, "size": dest_path.stat().st_size, "status": "saved (naive)"}

Run & test manually 1. Start the server:

uvicorn backend.main:app --reload

    2.	Use curl to upload a sample file:

curl -v -F "file=@sample_files/demo.mcam" http://127.0.0.1:8000/api/files/upload

Expected JSON (example):

{"filename":"demo.mcam","size":482,"status":"saved (naive)"}

Naïve tests: tests/test_upload_naive.py

# tests/test_upload_naive.py

import io
from fastapi.testclient import TestClient
from backend.main import app, UPLOAD_DIR
import os

client = TestClient(app)

def test_upload_mcam_success(): # small fake file content
file_content = b"example mcam content\n"
files = {"file": ("test1.mcam", io.BytesIO(file_content), "application/octet-stream")}
res = client.post("/api/files/upload", files=files)
assert res.status_code == 200
data = res.json()
assert data["filename"] == "test1.mcam"
assert data["status"].startswith("saved") # clean up
saved = UPLOAD_DIR / "test1.mcam"
if saved.exists():
saved.unlink()

def test_upload_invalid_extension_rejected():
file_content = b"not an mcam"
files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
res = client.post("/api/files/upload", files=files)
assert res.status_code == 400

Run tests:

pytest -q

⸻

3.1.2 Analysis of the naive approach — what’s wrong / risks
• Filename collisions: two users uploading the same filename will overwrite. Danger.
• No size limit: large uploads may exhaust disk or memory.
• Directory traversal: if the filename contains ../../ segments, some naive code can write outside UPLOAD_DIR. (Our Path / filename doesn’t normalize; but Python’s Path will treat the filename as a single segment if it contains path separators — still, better to sanitize.)
• MIME sniffing missing: checking only extension is insufficient — attackers can disguise malicious content with .mcam.
• No authorization: anyone can upload; later we’ll require JWT-authenticated requests.
• No audit logging: we should record who uploaded what and when (for PSD audit log requirements).
• No atomic writes: partial writes on failure might leave corrupt files.
• No background processing: saving directly in request blocks the request; fine for small files, problematic for large ones.

All of the above will be addressed in Refactor v1.

⸻

3.1.3 Refactor v1 — safe, testable, more production-minded

Refactor goals:
• Sanitize and normalize filenames.
• Store files with safe internal names (UUID-based) and keep original name in metadata.
• Enforce server-side maximum upload size.
• Validate extension and basic MIME type.
• Use atomic writes (write to a temp file, then move/rename).
• Add basic audit logging to a JSON uploads.json metadata file (simple persistence for tutorial).
• Add tests for filename collisions and size limit.

New files / changes:
• backend/storage.py — helper functions (sanitization, save)
• Update backend/main.py to use storage helpers
• data/uploads.json — appends metadata records (simple append-only log; later we’ll migrate to DB)

backend/storage.py (new)

# backend/storage.py

"""
Simple storage helpers for saving uploaded files safely in tutorial.
NOT meant as final production storage — but demonstrates safer practices:

- sanitizes filenames
- writes to a temporary file, then atomically moves
- returns metadata including an internal UUID name
  """

import os
import uuid
import json
from pathlib import Path
from typing import Dict, Any, BinaryIO

BASE_DIR = Path("data/files")
BASE_DIR.mkdir(parents=True, exist_ok=True)

AUDIT_LOG = Path("data/uploads.json")
AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
if not AUDIT_LOG.exists():
AUDIT_LOG.write_text("[]") # initialize as empty list

# allowed extensions set

ALLOWED_EXTS = {".mcam"}

def sanitize_filename(filename: str) -> str:
"""
Basic sanitizer: strip path separators and keep only last component.
Then remove suspicious characters.
"""
name = os.path.basename(filename) # drops any directory components # simple replace to remove NULs, path separators, and weird whitespace
name = name.replace("\x00", "") # Optionally strip or map characters we don't want
return name

def allowed_extension(filename: str) -> bool:
return Path(filename).suffix.lower() in ALLOWED_EXTS

def save_upload(fileobj: BinaryIO, original_filename: str) -> Dict[str, Any]:
"""
Save an uploaded file safely: - create a unique filename (uuid + suffix) - write to a temporary file in the same directory - rename (atomic on most OS) to final name - append metadata to uploads.json
Returns metadata dict.
""" # sanitize
sanitized = sanitize_filename(original_filename)
if not allowed_extension(sanitized):
raise ValueError("extension not allowed")

    suffix = Path(sanitized).suffix
    internal_name = f"{uuid.uuid4().hex}{suffix}"
    tmp_path = BASE_DIR / (internal_name + ".tmp")
    final_path = BASE_DIR / internal_name

    # write to temp
    with tmp_path.open("wb") as f:
        # read in chunks to avoid using excessive memory for large files
        while True:
            chunk = fileobj.read(1024 * 64)
            if not chunk:
                break
            f.write(chunk)

    # rename atomically
    tmp_path.replace(final_path)

    # metadata
    meta = {
        "internal_name": internal_name,
        "original_filename": sanitized,
        "size": final_path.stat().st_size,
    }

    # append to audit log (naive append)
    try:
        existing = json.loads(AUDIT_LOG.read_text())
    except Exception:
        existing = []
    existing.append(meta)
    AUDIT_LOG.write_text(json.dumps(existing, indent=2))

    return meta

Update backend/main.py to use storage helpers

Replace or add a new endpoint /api/files/upload-safe:

# backend/main.py (imports)

from fastapi import Depends
from backend.storage import save_upload, allowed_extension
from fastapi import Depends

# Config: max upload size in bytes (example: 10 MB)

MAX*UPLOAD_SIZE = 10 * 1024 \_ 1024

@app.post("/api/files/upload-safe", summary="Safer upload endpoint")
async def upload_file_safe(file: UploadFile = File(...)):
"""
Safer upload: - checks content-length if sent (best-effort) - rejects large files - delegates saving to storage.save_upload which writes atomically and records metadata
""" # Optional: check content-length header (best-effort) # Note: content-length may not be present for multipart uploads in some clients. # FastAPI UploadFile streams the body; to enforce limits robustly, set it at proxy or server level. # Here we do a quick check if header is provided. # But we also make the storage write in chunks and can detect size while writing.
if file.filename is None or not allowed_extension(file.filename):
raise HTTPException(status_code=400, detail="Invalid file extension")

    # Peek at Content-Length header via file.spool... not available — so we enforce in save_upload via file stream reading
    # For small uploads we proceed
    try:
        meta = save_upload(file.file, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # generic error — log and return 500
        logger.exception("Failed to save upload")
        raise HTTPException(status_code=500, detail="Failed to save file")

    return {"status": "ok", "meta": meta}

Enforcing maximum size (improved)

The save_upload function reads file in chunks and will write everything; to enforce size limit, update save_upload to count bytes and raise if exceeding limit.

Modify save_upload chunk loop:

# inside save_upload(...)

MAX*BYTES = 10 * 1024 \_ 1024 # 10 MB example
total = 0
with tmp_path.open("wb") as f:
while True:
chunk = fileobj.read(1024 \* 64)
if not chunk:
break
total += len(chunk)
if total > MAX_BYTES: # cleanup temp and raise
try:
f.close()
except Exception:
pass
if tmp_path.exists():
tmp_path.unlink()
raise ValueError("file too large")
f.write(chunk)

Tests for safe upload: tests/test_upload_safe.py

# tests/test_upload_safe.py

import io
from fastapi.testclient import TestClient
from backend.main import app, UPLOAD_DIR
from backend.storage import AUDIT_LOG

client = TestClient(app)

def test_safe_upload_and_metadata():
content = b"valid mcam content"
files = {"file": ("safe1.mcam", io.BytesIO(content), "application/octet-stream")}
res = client.post("/api/files/upload-safe", files=files)
assert res.status_code == 200
data = res.json()
assert data["status"] == "ok"
meta = data["meta"]
assert meta["original_filename"] == "safe1.mcam" # cleanup
path = UPLOAD_DIR / meta["internal_name"]
if path.exists():
path.unlink() # remove from audit log # naive: rewrite empty for tutorial
AUDIT_LOG.write_text("[]")

def test_safe_reject_invalid_ext():
content = b"not an mcam"
files = {"file": ("bad.exe", io.BytesIO(content), "application/octet-stream")}
res = client.post("/api/files/upload-safe", files=files)
assert res.status_code == 400

Run:

pytest tests/test_upload_safe.py -q

⸻

3.1.4 Additional hardening & operational considerations

1. Enforcing size limits at server/proxy level
   • FastAPI itself cannot easily limit upload size per request; best practice:
   • Configure reverse proxy (Nginx) client_max_body_size or API gateway limits.
   • At Uvicorn level, use --limit-max-requests? (not for payload size). So always enforce at proxy.

Example Nginx snippet:

server {
...
client_max_body_size 12M;
...
}

2. Content-type & MIME sniffing
   • Browser-supplied MIME can be forged. For added safety:
   • Inspect file content (magic bytes) if file format has a signature.
   • For .mcam (text-based G-code-like), you can check that file is text and not binary; sample heuristic: ensure it decodes as UTF-8 and contains plausible CNC commands.
   • Avoid relying solely on Content-Type header.

3. Authentication & Authorization
   • Require authenticated users to upload. Later we will implement JWT auth and enforce roles (user/admin).
   • Store uploader identity in the audit log: username, user_id, timestamp, IP address.

4. Virus scanning / malware checks
   • For industrial settings, consider scanning uploaded files with ClamAV or a hosted scanning service before allowing downloads to other users/machines.

5. Backups & retention
   • Implement a backup strategy (periodic Git commit, or snapshot to remote storage).
   • Retention policy: how long to keep old versions? PSD Stage 7 moves this to Git commits — plan that migration.

6. Atomic commit to Git (prep for Stage 7)
   • In future stage we will commit files into a Git repo as state changes occur. That commit should be done atomically with metadata updates so the repository always represents a consistent state.

⸻

3.1.5 Preparing for v2 — DB / cloud storage pivot

When you outgrow local disk (multi-server, backups, large files), options: 1. Database + filesystem hybrid
• Store metadata (original name, internal id, uploader, timestamp) in Postgres; store files on shared filesystem (NFS) or object store.
• Pros: easy queries, relational integrity. 2. Object storage (S3 / MinIO)
• Store files in S3 bucket; store metadata in DB.
• Use pre-signed URLs for uploads/downloads to offload traffic from the API server.
• Pros: scalable, durable, supports versioning & lifecycle rules.
• Implementation detail: implement server-side copy from presigned POST or direct PUT using minimal backend coordination. 3. Git repository (PSD Stage 7)
• For auditability, store files in a Git repo with each upload/modify being a commit. Use Git LFS for large files.
• Pros: precise history and ability to download by commit hash, blame view.
• Cons: Not ideal for extremely large binary files or massive scale unless using LFS + remote storage.

Tutorial path suggestion:
• For the tutorial, after we have the safe filesystem version (v1), implement an optional pivot to S3-style storage (using MinIO local server for testing). Then demonstrate how metadata moves to Postgres. Finally show a Git-backed approach as a separate branch/experiment that commits changes into a local Git repo.

⸻

3.1.6 Logging & audit (simple approach)

We added data/uploads.json as a quick audit. For production:
• Use a database (Postgres) with an uploads table capturing:
• id, internal_name, original_filename, uploader_id, uploader_name, size, timestamp, commit_hash (if using Git)
• Log to structured JSON to stdout (for containers) and ingest into ELK/Cloud logging.

Example simple audit schema (Postgres):

CREATE TABLE uploads (
id SERIAL PRIMARY KEY,
internal_name TEXT NOT NULL,
original_filename TEXT NOT NULL,
uploader_id INTEGER,
uploader_name TEXT,
size BIGINT,
created_at TIMESTAMP DEFAULT now(),
commit_hash TEXT
);

⸻

3.1.7 API responses & status codes (best practices)
• 201 Created for a successful upload is more RESTful than 200. Return Location header pointing to resource URL (/api/files/{id}).
• Use 400 Bad Request for validation failures.
• Use 413 Payload Too Large for size exceed (when possible).
• Use 500 for server errors, but keep error messages non-sensitive.

Example improved response for create:

HTTP/1.1 201 Created
Location: /api/files/123
Content-Type: application/json

{
"id": 123,
"original_filename": "demo.mcam",
"internal_name": "a1b2c3d4.mcam",
"size": 482,
"created_at": "2025-10-03T12:34:56Z"
}

We’ll implement 201 when we move to metadata persistence (DB or JSON with IDs).

⸻

3.1.8 Exercises (practical) 1. Required: Implement the storage.py helper and /api/files/upload-safe endpoint. Run the tests provided and ensure the audit log is created and cleaned up after tests. 2. Required: Attempt to upload a file larger than 10 MB (create synthetic bytes). Verify the API rejects it and that no temp file remains. 3. Optional: Implement basic content validation for .mcam (e.g., ensure it decodes as UTF-8 and contains at least one alphabetic line or pattern). 4. Optional Pivot: Replace local data/ with a MinIO server (local S3-compatible) and implement a save_to_s3 path in storage.py while still recording metadata in uploads.json. I can provide code for MinIO usage.

⸻

3.1.9 Summary / What’s next

We built a naïve upload route, analyzed its risks, implemented a safer upload-safe route with:
• sanitized filenames,
• atomic saves,
• chunked streaming with size checks,
• and a simple audit log.

Next steps in the tutorial series (coming up in Section 3.2 & 3.3):
• Build the frontend upload UI that talks to /api/files/upload-safe with progress UI and error handling (Section 3.2).
• Add file listing & delete endpoints (Section 3.4) and sync the UI.
• Then add authentication and authorization (Section 5) so only logged-in users can upload, and only admins can delete or override locks.

⸻

Perfect — let’s continue with Section 3.2 — Frontend Upload UI. I’ll keep the same level of deep detail: step-by-step HTML, CSS, JS, heavy line-by-line CSS comments, accessibility notes, and progressive enhancement so later we can swap frameworks or implement different UX versions. Copy-paste ready for MkDocs.

⸻

3.2 Frontend — File Upload UI (Deep Dive)

Goal: Build a web interface to upload .mcam files to our backend safely. We’ll create a vanilla JS UI first, with comments and tips for later framework integration (React/Vue/Svelte).

Acceptance criteria:
• Upload form with file input.
• Display selected filename and size.
• Upload button triggers AJAX fetch to /api/files/upload-safe.
• Show progress (percent uploaded).
• Handle success / error states.
• Accessible: keyboard & screen-reader friendly.

⸻

3.2.0 Design Notes

Before coding, a few architectural considerations: 1. Progressive enhancement: Start with a vanilla HTML form. Later we can swap in React components without rewriting backend. 2. Accessibility (a11y):
• Use <label> with for linked to input.
• Provide aria-live regions for status updates.
• Keyboard navigation (tabindex) must be smooth. 3. AJAX upload:
• Use fetch with FormData.
• async/await to simplify handling of promises.
• Include try/catch and proper error handling. 4. UI feedback:
• Show progress bar during upload.
• Show success/error messages dynamically.
• Clear form after successful upload.

⸻

3.2.1 HTML — Upload Form

<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MCAM File Upload</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main>
    <h1>Upload .MCAM Files</h1>

    <!-- Upload form container -->
    <form id="upload-form" aria-label="Upload MCAM file">
      <!-- File input with label -->
      <label for="file-input">Select a file:</label>
      <input type="file" id="file-input" name="file" accept=".mcam" required>

      <!-- Display selected file name -->
      <div id="file-info" aria-live="polite"></div>

      <!-- Upload button -->
      <button type="submit" id="upload-btn">Upload</button>

      <!-- Progress bar -->
      <progress id="upload-progress" value="0" max="100" hidden></progress>

      <!-- Status messages -->
      <div id="status" aria-live="polite"></div>
    </form>

    <!-- Optional future list of uploaded files -->
    <section id="uploaded-files">
      <h2>Uploaded Files</h2>
      <ul id="files-list"></ul>
    </section>

  </main>

  <script src="upload.js"></script>
</body>
</html>

Notes / Accessibility / Why these elements:
• <form> semantic grouping: allows keyboard submission via Enter.
• aria-label improves screen reader clarity.
• accept=".mcam" restricts file picker to .mcam files on most browsers.
• <div id="file-info" aria-live="polite"> updates dynamically when a file is selected.
• <progress> shows upload progress, hidden initially.
• <div id="status"> receives success/error messages.
• files-list is a placeholder for future file listing.

⸻

3.2.2 CSS — Step-by-step, commented

/_ style.css _/

/_ Basic body styling _/
body {
font-family: Arial, sans-serif; /_ readable sans-serif font _/
line-height: 1.6; /_ improve readability _/
margin: 0; /_ remove default margin _/
padding: 2rem; /_ add padding around content _/
background-color: #f9f9f9; /_ light neutral background _/
color: #333; /_ dark gray text for contrast _/
}

/_ Main container styling _/
main {
max-width: 600px; /_ limit width for readability _/
margin: 0 auto; /_ center horizontally _/
padding: 2rem;
background-color: #fff; /_ white card-like container _/
border-radius: 12px; /_ rounded corners _/
box-shadow: 0 4px 12px rgba(0,0,0,0.1); /_ subtle shadow _/
}

/_ Form styling _/
form#upload-form {
display: flex; /_ use flex layout _/
flex-direction: column; /_ stack children vertically _/
gap: 1rem; /_ spacing between elements _/
}

/_ Label styling _/
label {
font-weight: bold; /_ emphasize labels _/
}

/_ File input styling _/
input[type="file"] {
padding: 0.5rem;
border-radius: 6px;
border: 1px solid #ccc; /_ subtle gray border _/
}

/_ Upload button _/
button#upload-btn {
padding: 0.7rem 1.5rem;
border: none;
border-radius: 6px;
background-color: #007bff; /_ bootstrap-like blue _/
color: #fff; /_ white text _/
cursor: pointer;
transition: background-color 0.2s ease; /_ smooth hover _/
}

/_ Hover effect _/
button#upload-btn:hover {
background-color: #0056b3;
}

/_ Disabled button state _/
button#upload-btn:disabled {
background-color: #aaa;
cursor: not-allowed;
}

/_ Progress bar _/
progress#upload-progress {
width: 100%; /_ full width _/
height: 1.5rem; /_ thicker for visibility _/
}

/_ Status messages _/
#status {
min-height: 1.5rem; /_ reserve space for messages _/
}

/_ File info display _/
#file-info {
font-size: 0.9rem;
color: #555;
}

/_ Uploaded files list _/
#uploaded-files ul {
list-style-type: none; /_ remove bullets _/
padding-left: 0;
}

#uploaded-files li {
padding: 0.3rem 0;
border-bottom: 1px solid #eee;
}

/_ CSS Variables for dark/light mode _/
:root {
--bg-color: #fff;
--text-color: #333;
--primary-color: #007bff;
}

[data-theme="dark"] {
--bg-color: #1e1e1e;
--text-color: #ddd;
--primary-color: #4dabf7;
}

body {
background-color: var(--bg-color);
color: var(--text-color);
}

button#upload-btn {
background-color: var(--primary-color);
}

Notes on CSS variables:
• --bg-color, --text-color, --primary-color allow a single switch to dark mode by toggling [data-theme="dark"] on <html> or <body>.
• Later, we can add a toggle button that sets document.body.dataset.theme = "dark".

⸻

3.2.3 JavaScript — AJAX Upload with Progress

// upload.js

const form = document.getElementById("upload-form");
const fileInput = document.getElementById("file-input");
const fileInfo = document.getElementById("file-info");
const progress = document.getElementById("upload-progress");
const status = document.getElementById("status");

fileInput.addEventListener("change", () => {
const file = fileInput.files[0];
if (file) {
fileInfo.textContent = `Selected: ${file.name} (${file.size} bytes)`;
} else {
fileInfo.textContent = "";
}
});

form.addEventListener("submit", async (e) => {
e.preventDefault(); // prevent default form submission

const file = fileInput.files[0];
if (!file) {
status.textContent = "No file selected.";
return;
}

// Reset status & progress
status.textContent = "";
progress.hidden = false;
progress.value = 0;

const formData = new FormData();
formData.append("file", file);

try {
const response = await fetch("/api/files/upload-safe", {
method: "POST",
body: formData,
});

    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || "Upload failed");
    }

    const data = await response.json();
    status.textContent = `Upload successful! Stored as: ${data.meta.internal_name}`;
    fileInput.value = "";           // clear file input
    fileInfo.textContent = "";
    progress.hidden = true;

    // Optional: update file list UI
    addUploadedFile(data.meta);

} catch (err) {
status.textContent = `Error: ${err.message}`;
progress.hidden = true;
}
});

// Placeholder function for updating uploaded files list
function addUploadedFile(meta) {
const list = document.getElementById("files-list");
const li = document.createElement("li");
li.textContent = `${meta.original_filename} (${meta.size} bytes)`;
list.appendChild(li);
}

Notes on JS:
• Uses async/await for clarity.
• Error handling uses try/catch.
• FormData automatically sets the Content-Type: multipart/form-data boundary.
• Progress bar currently static; can be upgraded to XMLHttpRequest for real upload progress events.

⸻

3.2.4 Optional enhancement: true progress bar

For large files or multi-second uploads, fetch does not provide progress events. Use XMLHttpRequest:

const xhr = new XMLHttpRequest();
xhr.upload.addEventListener("progress", (e) => {
if (e.lengthComputable) {
progress.value = (e.loaded / e.total) \* 100;
}
});
xhr.open("POST", "/api/files/upload-safe");
xhr.send(formData);

⸻

3.2.5 Exercises 1. Implement index.html, style.css, upload.js. Verify upload works end-to-end with /api/files/upload-safe. 2. Select .txt or invalid file, confirm backend rejects it and UI shows error. 3. Test keyboard accessibility: tab through input and button, press Enter. 4. Optional: implement dark/light toggle using [data-theme] and CSS variables. 5. Optional pivot: rewrite upload.js as a React component for file upload, preserving accessibility and progress feedback.

⸻

3.2.6 Summary / What’s next

We built a vanilla frontend that:
• Selects a file, shows filename & size.
• Submits it to the backend safely.
• Shows success/error and optionally lists uploaded files.
• Has CSS variables for theming.
• Is accessible (labels, live regions, keyboard).

Next steps in the tutorial series:
• Section 3.3: File Listing API & Frontend Sync — Fetch uploaded files from backend and display them, implement delete buttons with confirmation, show optimistic UI updates.

⸻

If you want, I can continue immediately with Section 3.3 — File Listing & Delete API + Frontend Integration, keeping the same level of detail, line-by-line CSS commentary, JS explanation, and a11y notes. Do you want me to proceed?
