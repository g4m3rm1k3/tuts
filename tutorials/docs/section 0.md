# PDM Tutorial - Complete Rewrite: Incremental Build with Deep Explanations

**Welcome Back!** You've got a working app from our previous sessions—great foundation. Now, let's expand it into a **new, more incremental tutorial** starting from Stage 0. I'll use your original content (e.g., Stages 7/8 details) as the base but break everything into **tiny, testable steps** (5-15 lines of code max per step). Each step includes:

- **Code Snippet**: Exact pasteable code.
- **Deep Explanation**: Why it works, CS concepts (e.g., data structures), app topics (e.g., UX flows), Python/JS specifics (e.g., async/await), SE principles (e.g., separation of concerns).
- **Test**: Quick verification (run this command, expect this output).
- **Gotcha**: Common pitfalls + fixes.

This keeps you engaged—build, test, understand, repeat. Total time: 20-30 hours (spread out). By end, you'll have the hybrid GitLab app, but _ingrained_ knowledge.

**Assumptions**: Python 3.12+, Git installed, VS Code/Notepad++. Run in empty folder: `mkdir pdm-tutorial && cd pdm-tutorial`.

---

## Stage 0: Professional Development Environment

**Prerequisites**: None—start from scratch.
**Time**: 1-2 hours
**What you'll build**: Folder structure + tools setup. _Why incremental?_ One dir/file at a time—test creation immediately.

### Deep Dive: Why Structure Matters (SE Revisit)

In SE, "convention over configuration" (Ruby on Rails influence) means predictable folders (e.g., `app/` for Python package). This avoids "where's that file?" chaos. CS: Tree data structure (directories as nodes). App: Separates concerns (backend/static). Python: `__init__.py` makes dirs importable packages.

**Step 1: Create Root & Backend Dir**

```bash
mkdir pdm-tutorial
cd pdm-tutorial
mkdir backend
```

- **Explanation**: Root for project, `backend` for Python/FastAPI. Why? Keeps frontend static separate (app: MVC pattern).
- **Test**: `ls` → "backend".
- **Gotcha**: Use Git: `git init` now (track from start).

**Step 2: Add app Package**

```bash
mkdir -p backend/app
touch backend/app/__init__.py
```

- **Explanation**: `app/` = Python package (importable). `__init__.py` = marker file (CS: module system). Empty for now.
- **Test**: `python -c "import sys; sys.path.append('backend'); from app import __version__ if hasattr(__import__('app'), '__version__') else print('OK')"` → "OK" (no version, but imports).
- **Gotcha**: Missing `__init__.py` → "No module named 'app'".

**Step 3: Add Static Assets Dirs**

```bash
mkdir -p backend/static/{css,js/modules}
touch backend/static/index.html backend/static/js/app.js
```

- **Explanation**: `static/` for served files (FastAPI mount). `css/js` organized (app: asset pipeline). `modules/` for ES6 imports (JS: modularity, revisit later).
- **Test**: `ls backend/static` → "css index.html js".
- **Gotcha**: Case-sensitive—use lowercase.

**Step 4: Add Tests & Config Placeholders**

```bash
mkdir -p backend/{tests,app/{api,services,utils,schemas}}
touch backend/tests/__init__.py backend/app/{api,services,utils,schemas}/__init__.py
touch backend/.env.example backend/.gitignore
```

- **Explanation**: `tests/` for TDD (SE: red-green-refactor). Subdirs for layers (api=controllers, services=business logic, utils=helpers, schemas=models). Placeholders for env/git (app: 12-factor).
- **Test**: `tree backend` (install tree if needed) → Shows structure.
- **Gotcha**: Nested `__init__.py` for subpackages.

**Step 5: Basic .gitignore & .env.example**
Edit `backend/.gitignore`:

```
.env
__pycache__/
*.pyc
.git/
```

Edit `backend/.env.example`:

```
# Copy to .env and fill in
SECRET_KEY=your-secret
DEBUG=True
```

- **Explanation**: Ignores secrets/temp (SE: security). .env.example templates (app: env vars over code).
- **Test**: `git add . && git status` → Clean (ignores .env).
- **Gotcha**: Commit .env.example, not .env.

**Step 6: README.md Start**

```bash
touch README.md
```

Paste:

```
# PDM Tutorial App

Incremental build of Parts Data Management system.

## Setup
cd backend
pip install -r requirements.txt  # Later
uvicorn app.main:app --reload

## Stages
- Stage 0: Structure (now)
- ... (add as we go)
```

- **Explanation**: Docs as code (SE: literate programming).
- **Test**: `cat README.md`—shows.

### Stage 0 Complete

**Test Full Structure**:

```bash
tree .  # Or ls -R
```

Expect:

```
pdm-tutorial/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   └── __init__.py
│   │   ├── utils/
│   │   │   └── __init__.py
│   │   └── schemas/
│   │       └── __init__.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   │   └── modules/
│   │   ├── index.html
│   │   └── app.js
│   ├── tests/
│   │   └── __init__.py
│   ├── .env.example
│   └── .gitignore
└── README.md
```

**Verification**: [ ] All dirs/files. [ ] Imports work. [ ] Git clean.

**What You Learned (Depth)**:

- **CS**: Tree structures (dirs as nodes).
- **App**: MVC separation (static vs app).
- **Python**: Packages (**init**.py).
- **SE**: Git from day 1, config placeholders.

Ready for Stage 1? (FastAPI basics, incremental.)
