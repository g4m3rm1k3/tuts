Yes, those are perfect additions. They round out Stage 0 beautifully by introducing key developer tools and providing a great hook for what's next. It's a fantastic idea to lock this in as our definitive blueprint.

I will rewrite Stage 0 one last time to fold in those three tweaks. This will be our "final edition" that we'll use as the starting point for the rest of the tutorial.

---

# PDM Tutorial (Definitive Edition) - Stage 0: The Professional Environment

**Goal**: To establish a professional, scalable, and maintainable project environment from the ground up. We will not just run commands; we will understand _why_ each part of this structure is an industry best practice, building the mental models you need for all future projects.

**What You'll Learn**:

- Core terminology like **project root**, **dependencies**, and **packages**.
- The "why" behind a professional Python project layout, including the role of `__init__.py`.
- How virtual environments (`venv`) work to prevent dependency chaos.
- The fundamentals of package management with `pip` and `requirements.txt`.
- The essential Git commands to initialize a repository and make your first commits.
- How to run a basic "Hello, World" FastAPI application and verify it with a browser, `curl`, and the automatic documentation.

---

## 0.1: Laying the Foundation - Project Structure

First, we create our project's folder structure. A clean structure is like the foundation of a house; getting it right from the start prevents major headaches later.

### Your Turn: Create the Directory Tree

1.  Open your terminal or command prompt.

2.  Navigate to a directory where you like to keep your projects (e.g., `Documents/Projects`).

3.  Run these commands one by one to build our project's skeleton.

    ```bash
    # 1. Create the 'project root' and enter it.
    # The project root is the top-level folder for everything.
    mkdir pdm-tutorial
    cd pdm-tutorial

    # 2. Create the 'backend' folder for our Python app
    mkdir backend

    # 3. Create the Python 'package' folder 'app' inside 'backend'
    mkdir backend/app

    # 4. Create folders for our frontend assets (HTML, CSS, JS)
    mkdir -p backend/static/css
    mkdir -p backend/static/js

    # 5. Create the folder for our automated tests
    mkdir backend/tests

    # 6. Create the essential starting files
    touch backend/app/__init__.py
    touch backend/app/main.py
    touch backend/.gitignore
    touch backend/requirements.txt
    touch README.md
    ```

### ✅ Verification

Your project structure should now look exactly like this:

```
pdm-tutorial/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── tests/
│   ├── .gitignore
│   └── requirements.txt
└── README.md
```

### Deep Dive: The "Why" Behind This Structure

- `pdm-tutorial/`: The **project root**. This is the main container for your entire project. Your version control (`.git` folder) will live here.
- `backend/`: Contains everything related to our Python server application. This clearly separates our backend code from other potential top-level folders like `documentation/`.
- `app/`: This is our main **Python package**.
  - `app/__init__.py`: This empty file is crucial. It's a "magic" file that tells Python: "This folder is not just a folder; it's a package of code that you can import from." This is what allows us to write clean imports like `from app.services import ...` later on.
- `static/`: This folder holds files served _directly_ to the user's browser without being processed by Python: HTML, CSS, JavaScript, images, etc.
- `tests/`: A dedicated, separate place for automated tests. Professional projects always include tests to prevent regressions.
- `.gitignore`: Tells the Git version control system which files and folders to **ignore**. This is critical for security and for keeping your repository clean.

---

## 0.2: The Isolated Toolbox - Virtual Environments (`venv`)

Before we install any **dependencies** (external packages our project depends on), we need to create an isolated **virtual environment**.

### Deep Dive: The `venv` Mental Model

Think of a virtual environment as a **clean, dedicated toolbox for a single project** 🧰.

- **Without a `venv`**: Every package you install (`pip install fastapi`) is thrown into one giant, global toolbox on your computer. If Project A needs `library-v1.0` and Project B needs `library-v2.0`, you have a conflict. This is "dependency hell."
- **With a `venv`**: Each project gets its own private `venv` folder. Project A's toolbox can have `library-v1.0`, and Project B's toolbox can have `library-v2.0` without ever conflicting. This is a non-negotiable best practice.

### Your Turn: Create and Activate Your `venv`

1.  In your terminal, make sure you are inside the `backend` directory.

2.  Run the command to create the virtual environment. This will create a new folder named `venv` inside `backend`.

    ```bash
    # This command means: "Python, run the 'venv' module to create a new environment named 'venv'."
    python -m venv venv
    ```

3.  **Activate** the environment. This tells your current terminal session to use this project's specific Python toolbox.

    **On macOS/Linux:**

    ```bash
    source venv/bin/activate
    ```

    **On Windows (PowerShell):**

    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

    _(Note: If you get a script execution error on Windows, you may need to run this command once in your terminal: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`)_

### ✅ Verification

Your terminal prompt will change to show `(venv)` at the beginning, confirming the environment is active.

- **Before**: `C:\Users\You\pdm-tutorial\backend>`
- **After**: `(venv) C:\Users\You\pdm-tutorial\backend>`

---

## 0.3: The Project's Shopping List - `requirements.txt`

The `requirements.txt` file lists all the external packages your project needs to run.

### Your Turn: Define and Install Requirements

1.  Make sure you are in the `backend` directory with your `venv` active.

2.  Open the `backend/requirements.txt` file and add our first two dependencies.

    **File: `backend/requirements.txt`**

    ```
    # The modern, high-performance web framework for our API
    fastapi==0.104.1

    # The high-speed ASGI server that will run our FastAPI application
    uvicorn[standard]==0.24.0
    ```

3.  Now, tell `pip` (Python's package installer) to install everything on this list.

    ```bash
    pip install -r requirements.txt
    ```

### ✅ Verification

1.  You will see `pip` download and install the packages.
2.  To confirm a package is installed correctly _inside your virtual environment_, run:
    ```bash
    pip show fastapi
    ```
3.  You should see output detailing the package version, its location inside your `venv` folder, and its own dependencies. This confirms your setup is isolated and correct.

---

## 0.4: Saving Your Work - Git Version Control

A **repository** (or "repo") is a project whose history is tracked by Git. Let's turn our project folder into one.

### Your Turn: Initialize and Configure Git

1.  Navigate to the **project root** (`pdm-tutorial` folder).

2.  Configure Git with your name and email. This only needs to be done once per machine.

    ```bash
    git config --global user.name "Your Name"
    git config --global user.email "your.email@example.com"
    ```

3.  Initialize the repository. This creates the hidden `.git` folder where Git stores all the project's history.

    ```bash
    git init
    ```

### Your Turn: Configure `.gitignore`

Now, let's tell Git what _not_ to track.

1.  Open the `.gitignore` file in your `backend` directory.

2.  Add the following rules. The comments explain why we're ignoring each.

    **File: `backend/.gitignore`**

    ```
    # Python temporary files that are generated automatically
    __pycache__/

    # The Virtual Environment folder.
    # Why ignore? It's huge, machine-specific, and can be rebuilt from requirements.txt.
    venv/

    # Environment files containing secrets!
    # Why ignore? For security. NEVER commit passwords or API keys.
    .env

    # IDE and editor configuration files
    .vscode/
    .idea/
    ```

### Your Turn: Make Your First Commit

A **commit** is a saved snapshot of your project's state. Let's save our initial structure.

1.  **Stage** your changes. This tells Git you want to include these changes in the next snapshot.

    ```bash
    # Make sure you are in the 'pdm-tutorial' root folder
    git add .
    ```

2.  **Commit** your staged changes with a descriptive message.

    ```bash
    git commit -m "Initial commit: Set up project structure and environment"
    ```

### ✅ Verification

Run `git log`. You will see your first commit, stamped with your name and the date.

---

## 0.5: The First Win - "Hello, FastAPI\!"

All this setup is pointless if we don't see something working. Let's create the simplest possible FastAPI application to get our first rewarding "win" and confirm everything is wired up correctly.

### Your Turn: Write the "Hello, World" App

1.  Open `backend/app/main.py`.

2.  Add the following Python code.

    **File: `backend/app/main.py`**

    ```python
    from fastapi import FastAPI

    # Create an instance of the FastAPI application
    app = FastAPI()

    # Define an endpoint for the root URL ("/")
    # @app.get("/") is a "decorator" that tells FastAPI that the function
    # below it should handle GET requests to the root path.
    @app.get("/")
    def read_root():
        """This function will run when a user visits the main page."""
        return {"message": "Hello, Stage 0!"}
    ```

### Your Turn: Run the Server

1.  Make sure you are in the `backend` directory with your `venv` active.

2.  Run the **Uvicorn** server, pointing it to your `app` instance.

    ```bash
    # This command means: "Uvicorn, run the 'app' object,
    # which you can find in the 'app.main' module.
    # Also, --reload the server automatically when I save code changes."
    uvicorn app.main:app --reload
    ```

### ✅ Verification (Part 1: The Visual Check)

1.  Your terminal will show that Uvicorn is running on `http://127.0.0.1:8000`.
2.  Open your web browser and navigate to **[http://127.0.0.1:8000](http://127.0.0.1:8000)**.
3.  You should see the JSON response in your browser: `{"message":"Hello, Stage 0!"}`

### ✅ Verification (Part 2: The Developer Check with `curl`)

While a browser is great for visual checks, developers often use command-line tools like `curl` to test APIs. Let's try it.

1.  Open a **new terminal window** (leave your server running).
2.  Run the following command:
    ```bash
    curl http://127.0.0.1:8000/
    ```
3.  You will see the same JSON response printed directly to your terminal. This is a fast, scriptable way to test your endpoints, which will become essential in later stages.

### ✅ Verification (Part 3: The FastAPI "Wow" Moment - Auto-Docs)

This is one of the best features of FastAPI. Because you used Python type hints (even simple ones), FastAPI has automatically generated interactive documentation for your API.

1.  In your browser, go to **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**. You'll see the Swagger UI, an interactive page where you can see and test your endpoints.
2.  Now go to **[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)**. This is an alternative documentation view.

This "free" documentation is a massive productivity boost and ensures your API docs can never be out-of-date with your code.

---

## 0.6: Saving Our Progress

Now that we have a working application, we must save this milestone in our version control.

### Your Turn: Commit the Working App

1.  Go back to your terminal (you can stop the server with `Ctrl+C` for now).

2.  Navigate to the `pdm-tutorial` root directory.

3.  Stage and commit your new and modified files.

    ```bash
    git add .
    git commit -m "feat: Add initial 'Hello, World' FastAPI application"
    ```

    _(Note: `feat:` is a common convention for commit messages that add a new **feat**ure.)_

---

## Stage 0 Complete ✓

You've successfully set up a professional environment and launched a live web server. This is a huge first step that lays a solid foundation for everything we'll build next.

Right now, our app always returns the same simple message. In Stage 1, we’ll build on this foundation to create real API endpoints that can list data, retrieve specific items, and handle user input—just like the apps you use every day.

This is fantastic feedback. You're absolutely right on all points. These refinements will make the transition from setup to application-building much clearer and more rewarding. Integrating these small "aha\!" moments and professional habits is what turns a good tutorial into a great one.

I will incorporate all of your suggestions. Let's lock in this definitive, polished version of Stage 1.

---

# PDM Tutorial (Definitive Edition) - Stage 1: Building a Professional API

**Goal**: To build our first real API endpoints for the PDM system. We'll replace the "Hello, World" with endpoints that can list files and retrieve a single file's details, all based on a professional, organized structure.

**What You'll Learn**:

- How to define data "shapes" for your API using **Pydantic models (schemas)**.
- How to organize your code with **API Routers**.
- How to handle **path parameters** (e.g., `/files/{filename}`).
- The meaning of common **HTTP Status Codes** (200, 404, 500).
- How to raise proper HTTP errors and see Pydantic validation in action.
- How your code automatically updates the interactive **API documentation**.
- To continue the professional **Git workflow** by committing your features.

---

## 1.1: Defining Our Data Contracts with Schemas

Before our API can send data, we must define its structure. In FastAPI, we do this with Pydantic models, which we call **schemas**.

### Deep Dive: What is a Schema?

Think of a schema as a **blueprint or a strict "data contract"** for your API. It guarantees that any data leaving (or entering) your API will always have a specific, predictable shape. This practice eliminates a huge number of common bugs and makes your API reliable and easy for others (and your own frontend) to use.

### Your Turn: Create the Schema Files

Let's create a dedicated `schemas` directory for these blueprints.

1.  In your terminal, navigate to the `backend` directory.
2.  Create the new directory and files:
    ```bash
    mkdir app/schemas
    touch app/schemas/__init__.py
    touch app/schemas/files.py
    ```

### Your Turn: Build the File Schemas

Now, let's define the contracts for our file data.

1.  Open `backend/app/schemas/files.py`.

2.  Add the following code to define our two models.

    **File: `backend/app/schemas/files.py`**

    ```python
    from pydantic import BaseModel
    from typing import Optional, List

    class FileInfo(BaseModel):
        """This is our 'data contract' for a single file."""
        name: str
        status: str
        size_bytes: int
        locked_by: Optional[str] = None # 'Optional' means it can be str or None

        class Config:
            # Provide an example that will show up in our API documentation.
            json_schema_extra = {
                "example": {
                    "name": "PN1001_OP1.mcam",
                    "status": "available",
                    "size_bytes": 1234567,
                    "locked_by": None
                }
            }

    class FileListResponse(BaseModel):
        """The contract for the response when a user asks for all files."""
        files: List[FileInfo]
        total: int
    ```

### Your Turn: See Validation in Action (An Experiment)

Let's do a quick experiment to see _why_ schemas are so powerful.

1.  Open `backend/app/api/files.py` (we'll create it in the next step, but you can create it now).

2.  Temporarily add this mock data, but notice that `size_bytes` for the first file is a **string**, not an integer, which violates our `FileInfo` schema.

    ```python
    # Temporary code for the experiment
    MOCK_FILES_BROKEN = [
        {"name": "PN1001_OP1.mcam", "status": "available", "size_bytes": "a very large file", "locked_by": None},
    ]
    ```

3.  When you later run the server and try to access `/api/files`, FastAPI will stop and raise a `500 Internal Server Error`. In your terminal, you will see a detailed **ValidationError** from Pydantic, telling you exactly where the data failed to match the contract (`size_bytes` is not a valid integer).

4.  This immediate, clear feedback is invaluable. **Remember to delete this broken mock data** before proceeding to the next step.

---

## 1.2: Organizing Endpoints with an API Router

As our app grows, putting all API endpoints in `main.py` becomes messy. FastAPI provides `APIRouter` to solve this.

### Deep Dive: API Routers

Think of an `APIRouter` as a **mini-FastAPI application** or a department in a large company. It allows you to group related endpoints (your "employees") into their own file. You then tell your main `app` instance to include these routers. This keeps your code clean, organized, and easy to navigate.

### Your Turn: Create the API Router Files

1.  In your `backend` directory, create the `api` directory and its files:
    ```bash
    mkdir app/api
    touch app/api/__init__.py
    touch app/api/files.py
    ```

### Your Turn: Build the File Endpoints

Now we'll create our file-related API endpoints in their own dedicated file.

1.  Open `backend/app/api/files.py`.

2.  Add the following code.

    **File: `backend/app/api/files.py`**

    ```python
    from fastapi import APIRouter, HTTPException, status
    from app.schemas.files import FileInfo, FileListResponse

    # 1. Create a router instance.
    router = APIRouter(
        prefix="/api/files",  # All routes in this file will start with /api/files
        tags=["Files"],       # Group these endpoints under a "Files" heading in the docs
    )

    # 2. Create correct temporary mock data.
    MOCK_FILES = [
        {"name": "PN1001_OP1.mcam", "status": "available", "size_bytes": 1234567, "locked_by": None},
        {"name": "PN1002_OP1.mcam", "status": "checked_out", "size_bytes": 2345678, "locked_by": "john"},
        {"name": "PN1003_OP1.mcam", "status": "available", "size_bytes": 987654, "locked_by": None},
    ]

    # 3. Create the "List Files" endpoint.
    @router.get("/", response_model=FileListResponse)
    def get_files():
        return FileListResponse(files=MOCK_FILES, total=len(MOCK_FILES))

    # 4. Create the "Get Single File" endpoint.
    @router.get("/{filename}", response_model=FileInfo)
    def get_file(filename: str):
        # A 'path parameter' like {filename} is taken from the URL.
        # A 'query parameter' would be different, like /api/files?status=available
        for file in MOCK_FILES:
            if file["name"] == filename:
                return file

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File '{filename}' not found",
        )
    ```

---

## 1.3: Wiring It All Together

We've created our schemas and router, but our main application doesn't know about them yet. Let's connect them.

### Your Turn: Update the Main App

1.  Open `backend/app/main.py`.

2.  We'll replace our old "Hello, World" code and tell our main `app` to include the new `files` router.

    **File: `backend/app/main.py`**

    ```python
    from fastapi import FastAPI
    from app.api import files # NEW: Import our new router

    app = FastAPI(title="PDM System")

    # NEW: Tell the main app to include all the routes from our files router.
    # This one line makes '/api/files' and '/api/files/{filename}' live.
    app.include_router(files.router)

    @app.get("/")
    def read_root():
        """A simple health-check endpoint for the root."""
        return {"status": "ok", "message": "Welcome to the PDM API!"}
    ```

### ✅ Verification

Your `uvicorn` server has been auto-reloading. Let's test the new endpoints.

1.  **Test the error case with `curl`**. Open a new terminal and run:
    ```bash
    curl -i http://127.0.0.1:8000/api/files/fakefile.mcam
    ```
    The `-i` flag includes the HTTP headers in the response. You should see `HTTP/1.1 404 Not Found`.

### Deep Dive: Common HTTP Status Codes

What you just saw is a standard way servers communicate. Here are the most common codes:

- `200 OK`: Success\! The server successfully fulfilled your request.
- `404 Not Found`: You (the client) asked for a resource that doesn't exist.
- `401 Unauthorized`: You need to log in to access this.
- `403 Forbidden`: You are logged in, but you don't have permission for this specific action.
- `500 Internal Server Error`: A bug or crash happened on our server. This is our fault, not yours.

---

## 1.4: The Payoff - Interactive Docs, Upgraded

All the work we just did with schemas and routers has automatically upgraded our API documentation.

### Your Turn: Explore Your New Docs

1.  Refresh your browser tab at **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.

You'll now see a **"Files"** section with your two new endpoints.

- Expand the `/api/files/{filename}` endpoint.
- Notice the **"Schemas"** section at the bottom. You can see the exact structure of `FileInfo` and `FileListResponse`, including the helpful example we provided in the schema\!
- Click **"Try it out"**, enter `PN1002_OP1.mcam`, and click **"Execute"**. You can test your entire API right from this page.

---

## 1.5: Saving Our Progress

We've built a significant new feature. It's time to save a snapshot of our work in Git.

### Your Turn: Commit Your Feature

1.  Stop the server (`Ctrl+C`).

2.  Navigate to the `pdm-tutorial` root directory.

3.  Stage and commit your changes.

    ```bash
    git add .
    git commit -m "feat: Add File schemas and API endpoints for listing and retrieval"
    ```

---

## Stage 1 Complete ✓

You've successfully built a well-structured, multi-endpoint API. You are now using the professional patterns of schemas and routers that will allow this project to scale cleanly.

### Final File Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── files.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── files.py
│   ├── __init__.py
│   └── main.py
└── ... (other files)
```

### Verification Checklist

- [ ] The `get_files` endpoint (`/api/files`) returns the list of mock files.
- [ ] The `get_file` endpoint (`/api/files/{filename}`) returns a single file or a `404 Not Found` error.
- [ ] The interactive API docs at `/docs` are updated and show your new "Files" endpoints and schemas.
- [ ] You have successfully made a new Git commit for this feature.

Right now, our API returns data but we're still looking at raw JSON in the browser. In **Stage 2**, we’ll build a dynamic frontend with CSS and JavaScript to consume this API, so instead of text dumps, you’ll see interactive UI components.

This is excellent, detailed feedback. You're thinking like a tutorial author now—focusing on the "aha\!" moments, reinforcing good habits, and connecting new concepts to what the learner already knows.

You are absolutely correct. These refinements will make Stage 2 even stronger and more complete. I will integrate every one of your suggestions to create the definitive, polished version of Stage 2. Let's lock it in.

---

# PDM Tutorial (Definitive Edition) - Stage 2: Building the Frontend

**Goal**: To build a dynamic, professional-grade frontend that communicates with our API. We'll focus on a scalable CSS architecture and modular JavaScript, building and testing one component at a time.

**What You'll Learn**:

- **CSS Architecture**: How to organize CSS using a **Design Token** system for easy theming and maintenance.
- **DOM Manipulation**: How to use JavaScript to create, modify, and display HTML elements dynamically.
- **ES6 Modules**: How to write clean, modular, and reusable JavaScript.
- **API Communication**: How to use the `fetch` API and see how it relates to `curl`.
- **Frontend Error Handling**: How to build a resilient UI that can handle API failures gracefully.

---

## 2.1: The CSS Foundation - Architecture & Skeletons

Before writing styles, we need a strategy. We'll follow the **ITCSS (Inverted Triangle CSS)** methodology, a professional approach for organizing CSS from the most generic styles to the most specific. This prevents "CSS specificity wars" where styles conflict and become hard to manage.

### Deep Dive: Design Tokens & The Cascade

The heart of our CSS architecture is **Design Tokens**. Think of them as a "single source of truth" for your design, like a brand's official style guide. Instead of writing a color like `#667eea` in 20 different places, you define it once as a variable (token). If you need to rebrand, you change it in **one place**, and the entire UI updates.

We will organize our CSS files to follow a logical cascade, from broadest to most specific.

**ITCSS Layers (Our Simplified Version):**

```
┌───────────────────────────────┐
│ Tokens (Variables)            │  <- Most generic, widest impact
├───────────────────────────────┤
│ Base (Reset, body, h1 styles) │
├───────────────────────────────┤
│ Components (Buttons, Cards)   │  <- Most specific, narrow impact
└───────────────────────────────┘
```

### Your Turn: Create the CSS Files

1.  Navigate to `backend/static/css` in your project.
2.  If they don't already exist, create the empty files:
    ```bash
    touch tokens.css base.css components.css main.css
    ```

### Your Turn: Define the Design Tokens

Let's build our design system's foundation in `tokens.css`.

1.  Open `backend/static/css/tokens.css`.

2.  Add the `:root` selector and our tokens.

    **File: `backend/static/css/tokens.css`**

    ```css
    /**
     * Design Tokens - The Single Source of Truth for our UI
     * The :root selector is a pseudo-class that represents the <html> element.
     * It's the perfect place to declare global CSS variables that will be
     * available everywhere in our document.
     */
    :root {
      /* ==================================
         PRIMITIVE TOKENS (The Raw Values)
         ================================== */
      --color-primary-500: #667eea;
      --color-primary-700: #4453b8;
      --color-gray-50: #f9fafb;
      --color-gray-200: #e5e7eb;
      --color-gray-900: #111827;
      --color-success-fg: #059669;
      --color-success-bg: #d1fae5;
      --color-warning-fg: #d97706;
      --color-warning-bg: #fef3c7;

      --spacing-4: 1rem; /* 16px */
      --spacing-6: 1.5rem; /* 24px */
      --spacing-8: 2rem; /* 32px */

      /* ===================================================
         SEMANTIC TOKENS (The Purpose of the Values)
         =================================================== */
      --bg-primary: #ffffff;
      --bg-secondary: var(--color-gray-50);
      --text-primary: var(--color-gray-900);
      --border-default: var(--color-gray-200);
    }
    ```

---

## 2.2: Setting the Global Style Baseline

Now we'll add styles to `base.css` to set up sensible, consistent defaults for our entire application.

### Your Turn: Add Base and Body Styles

1.  Open `backend/static/css/base.css`.

2.  Add a "CSS Reset" and styles for the `<body>`, using our new tokens.

    **File: `backend/static/css/base.css`**

    ```css
    /* A simple "CSS Reset" for a consistent baseline across browsers. */
    *,
    *::before,
    *::after {
      box-sizing: border-box;
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

## 2.3: The HTML Skeleton & First Visuals

It's time to see our work in the browser.

### Your Turn: Create the HTML and Link CSS

1.  Open `backend/static/index.html`. If it has any content, replace it with this basic structure.

2.  In the `<head>`, link to `main.css`, which will be our single entry point for all styles.

    **File: `backend/static/index.html`**

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
      </body>
    </html>
    ```

3.  Now, open `backend/static/css/main.css` and use it to import the other CSS files in the correct order. The order is critical for the cascade to work properly.

    **File: `backend/static/css/main.css`**

    ```css
    /* 1. Design Tokens - Must load first so variables are available */
    @import "tokens.css";

    /* 2. Base Styles - Sets defaults for raw HTML elements */
    @import "base.css";

    /* 3. Components - We'll add styles here soon */
    @import "components.css";
    ```

### Your Turn: Update FastAPI to Serve the Frontend

Let's tell our Python server to serve these new files.

1.  Open `backend/app/main.py`.

2.  Modify your `main.py` to mount the `static` directory and change the root endpoint to serve the `index.html` file.

    **File: `backend/app/main.py`**

    ```python
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse
    from app.api import files

    app = FastAPI(title="PDM System")

    # This tells FastAPI to serve any file in the 'static' directory
    # if the URL starts with /static. This is how our CSS and JS will be loaded.
    app.mount("/static", StaticFiles(directory="static"), name="static")

    app.include_router(files.router)

    # We change the root endpoint to serve our main HTML file.
    @app.get("/", response_class=FileResponse, include_in_schema=False)
    def read_root():
        """Serves the main application frontend."""
        return FileResponse("static/index.html")
    ```

    _(Note: `include_in_schema=False` just hides this from our API docs, as it's not a data endpoint.)_

### ✅ Verification Point 1

1.  If your `uvicorn` server isn't running, start it from the `backend` directory: `uvicorn app.main:app --reload`.
2.  Go to **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

You should see a very plain page with "PDM System". But crucially, the page has our light gray background color and dark text. Our CSS architecture is working\!

---

## 2.4: Building the UI, Component by Component

Now we'll add styles to `components.css` and the corresponding HTML to `index.html`, building up the UI one piece at a time.

### Your Turn: Style and Build the Header & Main Content Area

1.  **Add the CSS** for our main layout components to `backend/static/css/components.css`.

    ```css
    /* === Layout Components === */
    .container {
      width: 100%;
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 var(--spacing-4);
    }

    header {
      background: linear-gradient(
        135deg,
        var(--color-primary-500),
        var(--color-primary-700)
      );
      color: #ffffff;
      padding: var(--spacing-6) 0;
    }

    .file-list-card {
      background: var(--bg-primary);
      border-radius: 0.5rem;
      padding: var(--spacing-6);
      margin-top: var(--spacing-8);
    }
    ```

2.  **Update the HTML** in `backend/static/index.html` to use these new classes.

    ```html
    <body>
      <header>
        <div class="container">
          <h1>PDM System</h1>
          <p>Parts Data Management</p>
        </div>
      </header>

      <main class="container">
        <section class="file-list-card">
          <h2>Available Files</h2>
          <div id="loading-indicator"><p>Loading files from API...</p></div>
          <div id="file-list"></div>
        </section>
      </main>
    </body>
    ```

### ✅ Verification Point 2

Refresh your browser. You should now see the styled gradient header and a clean, white "card" where our file list will soon appear.

---

## 2.5: Bringing It to Life with JavaScript

It's time to fetch data from our API and build the file list dynamically.

### Deep Dive: `curl` vs. `fetch` - Two Doors to the Same House

In Stage 1, we used `curl` to test our API from the terminal. In the browser, JavaScript uses the `fetch` function to do the exact same thing.

- `curl http://127.0.0.1:8000/api/files` (in your terminal)
- `fetch('/api/files')` (in your JavaScript)

Both are **HTTP clients** sending a `GET` request to the same endpoint on your server. One is a command-line tool, the other is a browser API.

### Your Turn: Build the API Client Module

We'll create a dedicated module whose only job is to talk to our backend. This keeps our code organized.

1.  Open `backend/static/js/modules/api-client.js`.

2.  Add the `APIClient` class.

    **File: `backend/static/js/modules/api-client.js`**

    ```javascript
    /**
     * A centralized module for all communication with our backend API.
     */
    export class APIClient {
      async getFiles() {
        try {
          const response = await fetch("/api/files");
          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(
              errorData.detail || `HTTP error! status: ${response.status}`
            );
          }
          return await response.json();
        } catch (error) {
          console.error("Failed to fetch files:", error);
          throw error; // Re-throw so the UI can handle it
        }
      }
    }

    export const apiClient = new APIClient();
    ```

### Your Turn: Write the Main Application Logic

Now let's use our API client in `app.js` to fetch data and update the **DOM** (the live HTML structure of the page).

1.  Open `backend/static/js/app.js`.

2.  Replace its content with this logic.

    **File: `backend/static/js/app.js`**

    ```javascript
    // Import the apiClient we just created
    import { apiClient } from "./modules/api-client.js";

    const fileListEl = document.getElementById("file-list");
    const loadingEl = document.getElementById("loading-indicator");

    /**
     * Creates the HTML for a single file item.
     * @param {object} file - The file data from the API.
     */
    function createFileElement(file) {
      const div = document.createElement("div");
      // We will style this class in the next step
      div.className = "file-item";
      div.innerHTML = `<span>${file.name}</span>`;
      return div;
    }

    async function loadAndDisplayFiles() {
      try {
        loadingEl.style.display = "block";
        fileListEl.innerHTML = "";

        const data = await apiClient.getFiles();
        loadingEl.style.display = "none";

        data.files.forEach((file) => {
          const fileElement = createFileElement(file);
          fileListEl.appendChild(fileElement);
        });
      } catch (error) {
        loadingEl.style.display = "none";
        fileListEl.innerHTML = `<p style="color: red;">Error loading files: ${error.message}</p>`;
      }
    }

    // This runs when the browser has finished building the page.
    document.addEventListener("DOMContentLoaded", () => {
      loadAndDisplayFiles();
    });
    ```

3.  Add `type="module"` to your `<script>` tag in `index.html` so it can use `import`.

    **Modify `index.html`:**

    ```html
    <script type="module" src="/static/js/app.js"></script>
    ```

### ✅ Verification Point 3 (The "It Works\!" Moment)

1.  Refresh your browser. You should see the "Loading..." message, followed by a simple, unstyled list of the file names from your API\!
2.  **For the curious**: Open your browser's Developer Tools (F12 or Ctrl+Shift+I), go to the **Network** tab, and refresh the page. You will see the actual `GET` request being made to `/api/files` and the JSON response from your server.

### Your Turn: Style the Final File List

Our last step is to apply the styles we wrote earlier.

1.  Open `backend/static/css/components.css` and add the styles for `.file-item` and its children.

    **File: `backend/static/css/components.css`**

    ```css
    /* Add to the bottom of the file */
    .file-item {
      padding: var(--spacing-4);
      border-bottom: 1px solid var(--border-default);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .file-item:last-child {
      border-bottom: none;
    }

    .file-name {
      font-weight: 600;
    }

    .file-status {
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.875rem;
      font-weight: 500;
      text-transform: capitalize;
    }
    .status-available {
      background-color: var(--color-success-bg);
      color: var(--color-success-fg);
    }
    .status-checked_out {
      background-color: var(--color-warning-bg);
      color: var(--color-warning-fg);
    }
    ```

2.  Update `createFileElement` in `app.js` to use these new classes.

    **Modify `app.js`:**

    ```javascript
    function createFileElement(file) {
      const div = document.createElement("div");
      div.className = "file-item";

      const nameSpan = document.createElement("span");
      nameSpan.className = "file-name";
      nameSpan.textContent = file.name;

      const statusSpan = document.createElement("span");
      statusSpan.className = `file-status status-${file.status}`;
      statusSpan.textContent = file.status.replace("_", " ");

      div.appendChild(nameSpan);
      div.appendChild(statusSpan);
      return div;
    }
    ```

### ✅ Verification Point 4 (Error Handling Demo)

1.  Go to your terminal where `uvicorn` is running and stop the server (`Ctrl+C`).
2.  Refresh your browser.
3.  You should now see the red error message: "Error loading files: Failed to fetch". This proves your `try...catch` block is working correctly\!
4.  Restart your server (`uvicorn app.main:app --reload`) and refresh the page to see the file list again.

---

## 2.6: Saving Our Progress

We've built a complete, styled, data-driven frontend. It's time to commit this major feature.

### Your Turn: Commit Your Feature

1.  Stop the server.
2.  Navigate to the `pdm-tutorial` root directory.
3.  Stage and commit your changes.
    ```bash
    git add .
    git commit -m "feat: Build dynamic frontend with CSS architecture and API integration"
    ```

---

## Stage 2 Complete ✓

You've successfully built a dynamic frontend with a professional and scalable architecture. You've connected it to a live backend API, and you're now manipulating the DOM based on real data.

### Final File Structure

```
backend/
├── app/
│   └── (unchanged from Stage 1)
├── static/
│   ├── css/
│   │   ├── base.css
│   │   ├── components.css
│   │   ├── main.css
│   │   └── tokens.css
│   ├── js/
│   │   ├── modules/
│   │   │   └── api-client.js
│   │   └── app.js
│   └── index.html
└── ... (other files)
```

### Verification Checklist

- [ ] The page loads a styled header and a main content "card".
- [ ] JavaScript is modular, with a separate `api-client.js`.
- [ ] On page load, the file list is dynamically fetched and displayed with correct styling.
- [ ] Stopping the backend server causes a user-friendly error message to appear on the frontend.
- [ ] A new Git commit for this feature has been made.

So far, our frontend is "read-only." In **Stage 3**, we’ll make it interactive by replacing our backend's mock data with real filesystem logic and building a robust locking system. We'll then wire up buttons on the frontend, turning this into a real tool, not just a viewer.

This is a perfect set of refinements. You’ve pinpointed exactly how to elevate this from a good tutorial to a great one by reinforcing the core concepts with visuals, command-line parallels, and explicit testing of failure cases.

Let's do it. I will integrate every one of your suggestions to create the definitive, polished edition of Stage 3. This will be our new blueprint.

---

Absolutely possible. Let me rebuild Stage 3 to be **incremental, explanatory, and comprehensive** - a teaching tool that builds understanding at every step.

---

# PDM Tutorial (Complete Edition) - Stage 3: Real Files & Atomic Locking

**Goal**: To transform our application from displaying mock data to managing real files with a robust, race-condition-proof locking system. We'll build this incrementally, understanding each piece before moving to the next.

**What You'll Learn**:

- What **race conditions** are and why they cause data corruption
- How **atomic operations** prevent race conditions
- Python **context managers** and the `with` statement
- The **Service Layer** architectural pattern
- **Dependency Injection** in FastAPI
- Building interactive **modal dialogs** on the frontend
- Testing APIs with both browser and command-line tools

---

## 3.1: Understanding the Problem - Race Conditions

Before we write any code, we need to understand **why** our current approach won't work when multiple users use our app simultaneously.

### Deep Dive: What is a Race Condition?

A **race condition** occurs when two or more operations try to access and modify shared data at the same time, and the final result depends on the unpredictable timing ("racing") of these operations.

**Real-world analogy**: Imagine you and your roommate both see an empty milk carton. You both write "milk" on the shopping list at the same time. Now "milk" appears twice, or worse, one person's writing overwrites the other's, and the list is corrupted.

### The Three-Step Problem

Every file operation has three steps:

1. **READ** - Load the current data from disk
2. **MODIFY** - Change the data in memory
3. **WRITE** - Save the modified data back to disk

When two users perform these steps at overlapping times, chaos ensues:

```
Timeline: What happens without locks
─────────────────────────────────────────────────────────

Alice: READ {"locks": []}
                ↓
                MODIFY (add Alice's lock)
                         ↓
Bob:                     READ {"locks": []} ← Still empty!
                         ↓
                         MODIFY (add Bob's lock)
                                  ↓
Alice:                            WRITE {"locks": ["Alice"]}
                                           ↓
Bob:                                       WRITE {"locks": ["Bob"]} ← Overwrites Alice!

Result: Alice's lock disappeared! Data corruption.
```

### Your Turn: Prove the Problem Exists

Let's write a simulation that demonstrates this problem in action.

1. Create a new directory for utility experiments:

   ```bash
   mkdir backend/app/utils
   touch backend/app/utils/__init__.py
   ```

2. Create the learning script:

   ```bash
   touch backend/app/learn_race_condition.py
   ```

3. Add this code to **understand** the problem before we solve it:

**File: `backend/app/learn_race_condition.py`**

```python
"""
A demonstration of why race conditions are dangerous.
This script simulates two users trying to increment a counter simultaneously.
"""
import threading
import json
import time
from pathlib import Path

# Create a temporary file for our experiment
TEMP_FILE = Path("temp_counter.json")
TEMP_FILE.write_text('{"counter": 0}')

def unsafe_increment(user_name, iterations):
    """
    This function has the race condition bug.
    It reads, modifies, and writes without any protection.
    """
    for i in range(iterations):
        # STEP 1: READ
        data = json.loads(TEMP_FILE.read_text())
        current = data["counter"]

        # STEP 2: MODIFY (in memory)
        new_value = current + 1

        # Simulate some processing time
        # This makes the race condition more obvious
        time.sleep(0.001)  # 1 millisecond

        # STEP 3: WRITE
        data["counter"] = new_value
        TEMP_FILE.write_text(json.dumps(data))

        if i % 10 == 0:
            print(f"  {user_name} incremented to {new_value}")

# Run the experiment
print("Starting race condition demonstration...")
print("Two 'users' will each try to increment the counter 50 times.")
print("Expected final value: 100")
print()

# Create two threads (simulating two simultaneous users)
thread1 = threading.Thread(target=unsafe_increment, args=("Alice", 50))
thread2 = threading.Thread(target=unsafe_increment, args=("Bob", 50))

# Start both threads at the same time
thread1.start()
thread2.start()

# Wait for both to finish
thread1.join()
thread2.join()

# Check the result
final_data = json.loads(TEMP_FILE.read_text())
print()
print(f"Expected final counter: 100")
print(f"Actual final counter:   {final_data['counter']}")
print()

if final_data['counter'] < 100:
    print("❌ DATA LOSS! Some increments were overwritten.")
    print(f"   Lost updates: {100 - final_data['counter']}")
else:
    print("✓ No data loss (but this is just luck - the bug still exists)")

# Clean up
TEMP_FILE.unlink()
```

4. Run the demonstration:
   ```bash
   python -m app.learn_race_condition
   ```

### ✅ Verification

You should see output showing that the final counter is **less than 100**. This proves that updates were lost due to the race condition.

**Example output:**

```
Expected final counter: 100
Actual final counter:   73
❌ DATA LOSS! Some increments were overwritten.
   Lost updates: 27
```

---

## 3.2: The Solution - File Locking

Now that we've proven the problem exists, let's build the solution: a **lock** that ensures only one operation can happen at a time.

### Deep Dive: What is a Lock?

A **lock** is like a bathroom key. When Alice wants to use the bathroom (modify the file), she takes the key. Bob has to wait outside until Alice is done and returns the key. This guarantees that only one person can be inside at a time.

In programming terms:

- **Acquire the lock** = Take the key
- **Do the work** = Use the bathroom
- **Release the lock** = Return the key

The critical guarantee: The entire READ → MODIFY → WRITE sequence happens **atomically** (as one indivisible unit).

### Your Turn: Build the Lock - Part 1 (The Foundation)

We'll build our `LockedFile` class incrementally, understanding each piece.

1. Create the file:

   ```bash
   touch backend/app/utils/file_locking.py
   ```

2. Start with the **imports and basic structure**:

**File: `backend/app/utils/file_locking.py`**

```python
"""
Cross-platform file locking utility.

This module provides a context manager for safe, concurrent file access.
It prevents race conditions by ensuring that only one process can read/write
a file at a time.
"""
import fcntl  # Unix/Linux/Mac file locking
import msvcrt  # Windows file locking
import platform
from pathlib import Path
from typing import Any
import json

class LockedFile:
    """
    A context manager that provides exclusive access to a JSON file.

    Usage:
        with LockedFile('data.json') as data:
            data['key'] = 'value'
        # File is automatically saved and unlocked here
    """

    def __init__(self, filepath: Path | str):
        """
        Initialize the LockedFile.

        Args:
            filepath: Path to the JSON file to lock
        """
        self.filepath = Path(filepath)
        self.file_handle = None
        self.data = None
```

**Deep Dive: Why a Context Manager?**

We're building a **context manager** - a Python object that works with the `with` statement. This pattern ensures:

1. Resources are properly acquired (lock is taken)
2. Your code runs in a "safe zone"
3. Resources are properly released (lock is freed) **even if an error occurs**

---

### Your Turn: Build the Lock - Part 2 (Entering the Safe Zone)

Now let's add the `__enter__` method, which runs when you write `with LockedFile(...) as data:`.

**Add to `backend/app/utils/file_locking.py`:**

```python
    def __enter__(self):
        """
        Called when entering the 'with' block.

        This method:
        1. Opens the file
        2. Acquires an exclusive lock
        3. Reads and parses the JSON data
        4. Returns the data for you to modify
        """
        # Step 1: Open the file
        # Mode 'r+' means: open for reading AND writing, file must exist
        # Mode 'a+' means: create if missing, open for reading AND writing
        mode = 'r+' if self.filepath.exists() else 'a+'
        self.file_handle = open(self.filepath, mode)

        # Step 2: Acquire the lock (blocks until available)
        self._acquire_lock()

        # Step 3: Read the current contents
        self.file_handle.seek(0)  # Go to start of file
        content = self.file_handle.read()

        # Step 4: Parse JSON (or start with empty dict if file is new)
        if content.strip():
            self.data = json.loads(content)
        else:
            self.data = {}

        # Step 5: Return the data so the user can modify it
        return self.data
```

**What's happening here?**

- `open(...)` gives us a file handle (like opening a book)
- `_acquire_lock()` takes the exclusive lock (we'll write this next)
- `seek(0)` moves to the beginning (like going to page 1)
- We parse the JSON and return it for the user to modify

---

### Your Turn: Build the Lock - Part 3 (Platform-Specific Locking)

Different operating systems lock files differently. Let's add the cross-platform lock acquisition:

**Add to `backend/app/utils/file_locking.py`:**

```python
    def _acquire_lock(self):
        """
        Acquire an exclusive lock on the file.
        This is cross-platform: works on Windows, Mac, and Linux.
        """
        system = platform.system()

        if system == "Windows":
            # Windows: Use msvcrt to lock the file
            # LK_NBLCK means "non-blocking lock" - we'll wait if needed
            msvcrt.locking(
                self.file_handle.fileno(),
                msvcrt.LK_LOCK,  # Exclusive lock, wait if unavailable
                1  # Lock 1 byte (enough to prevent other access)
            )
        else:
            # Unix/Linux/Mac: Use fcntl to lock the file
            # LOCK_EX means "exclusive lock"
            # (Blocks until available)
            fcntl.flock(self.file_handle.fileno(), fcntl.LOCK_EX)
```

**Deep Dive: Why Two Different Methods?**

Windows and Unix-like systems (Mac, Linux) use different system calls for file locking:

- **Windows**: `msvcrt` module
- **Unix/Mac**: `fcntl` module

Our code automatically detects which OS you're running and uses the correct method. This is what "cross-platform" means.

---

### Your Turn: Build the Lock - Part 4 (Exiting Safely)

Finally, let's add the `__exit__` method, which runs when the `with` block ends:

**Add to `backend/app/utils/file_locking.py`:**

```python
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when exiting the 'with' block.

        This method:
        1. Writes the modified data back to the file
        2. Releases the lock
        3. Closes the file

        This runs EVEN IF an exception occurred in the 'with' block.
        """
        try:
            # Step 1: Write the (possibly modified) data back to file
            self.file_handle.seek(0)  # Go to beginning
            self.file_handle.truncate()  # Clear old content
            json_str = json.dumps(self.data, indent=2)
            self.file_handle.write(json_str)
            self.file_handle.flush()  # Force write to disk immediately

        finally:
            # Step 2 & 3: Release lock and close file
            # The 'finally' ensures this happens even if step 1 failed
            if self.file_handle:
                self._release_lock()
                self.file_handle.close()

    def _release_lock(self):
        """Release the exclusive lock on the file."""
        system = platform.system()

        if system == "Windows":
            msvcrt.locking(
                self.file_handle.fileno(),
                msvcrt.LK_UNLCK,  # Unlock
                1
            )
        else:
            fcntl.flock(self.file_handle.fileno(), fcntl.LOCK_UN)
```

**Deep Dive: The `finally` Block**

The `finally` block is Python's safety net. Code in `finally` **always runs**, even if:

- An exception occurred
- The code returned early
- The universe collapsed (okay, not that one)

This guarantees our lock is **always released**, preventing deadlocks where a file stays locked forever.

---

### Your Turn: Test the Lock

Let's prove our lock works by creating a **safe** version of our race condition script.

**Create: `backend/app/learn_lock_safety.py`**

```python
"""
Demonstration that our LockedFile utility prevents race conditions.
"""
import threading
import time
from pathlib import Path
from app.utils.file_locking import LockedFile

TEMP_FILE = Path("temp_counter_safe.json")
TEMP_FILE.write_text('{"counter": 0}')

def safe_increment(user_name, iterations):
    """
    This function uses our LockedFile utility.
    The lock prevents race conditions.
    """
    for i in range(iterations):
        # The entire read-modify-write is now atomic!
        with LockedFile(TEMP_FILE) as data:
            current = data["counter"]
            time.sleep(0.001)  # Same delay as before
            data["counter"] = current + 1
            new_value = data["counter"]

        if i % 10 == 0:
            print(f"  {user_name} incremented to {new_value}")

print("Starting SAFE increment demonstration...")
print("Two 'users' will each try to increment the counter 50 times.")
print("Expected final value: 100")
print()

thread1 = threading.Thread(target=safe_increment, args=("Alice", 50))
thread2 = threading.Thread(target=safe_increment, args=("Bob", 50))

thread1.start()
thread2.start()
thread1.join()
thread2.join()

with LockedFile(TEMP_FILE) as data:
    final = data["counter"]

print()
print(f"Expected final counter: 100")
print(f"Actual final counter:   {final}")

if final == 100:
    print("✓ SUCCESS! No data loss. The lock worked!")
else:
    print(f"❌ Something went wrong: {final}")

TEMP_FILE.unlink()
```

Run it:

```bash
python -m app.learn_lock_safety
```

### ✅ Verification

You should see `Actual final counter: 100` and `✓ SUCCESS!`. Our lock prevents the race condition!

---

## 3.3: Commit the Foundation

We've built a critical piece of infrastructure. Let's save it.

```bash
git add .
git commit -m "feat: Add cross-platform file locking utility with demonstrations"
```

---

I'll continue with the rest of Stage 3 in the next response. This shows the incremental, explanatory approach. Should I continue building out:

- The Service Layer (FileService class)
- Updating the API endpoints
- Building the modal UI
- Connecting it all together

## Each with the same level of detail and incremental building?

# PDM Tutorial (Definitive Edition) - Stage 4: Professional Frontend State & UX

**Goal**: To refactor our frontend to use a professional state management pattern, making it more robust and easier to extend. We will also add UX improvements like toast notifications and client-side search and filtering.

**What You'll Learn**:

- The core concepts of **frontend state management** and the **Observer pattern**.
- How to build a central **"store"** as a single source of truth for your UI.
- How **computed properties** derive data from state without cluttering it.
- How to build a non-blocking **toast notification** system.
- How a central store makes implementing features like **search and filtering** incredibly simple.

Continuing Stage 3 from where we left off...

---

## 3.4: The Service Layer Architecture

Now that we have a safe way to access files, we need to organize our **business logic** - the rules about how files can be checked out, who can check them in, what happens when someone tries to check out a locked file, etc.

### Deep Dive: What is the Service Layer?

The **Service Layer** is an architectural pattern that separates your code into distinct responsibilities:

```
┌─────────────────────────────────────────┐
│  API Layer (files.py)                   │  <- Handles HTTP requests/responses
│  "What data came in? What should go out?"│     Knows about FastAPI, status codes
└─────────────────────────────────────────┘
              ↓ calls
┌─────────────────────────────────────────┐
│  Service Layer (file_service.py)        │  <- Contains business rules
│  "What are the rules? What's allowed?"  │     Knows nothing about HTTP
└─────────────────────────────────────────┘
              ↓ uses
┌─────────────────────────────────────────┐
│  Utility Layer (file_locking.py)        │  <- Low-level operations
│  "How do we safely read/write files?"   │     Cross-platform file handling
└─────────────────────────────────────────┘
```

**Why separate these?**

1. **Testability**: You can test business logic without running a web server
2. **Reusability**: Business logic can be used by different interfaces (API, CLI, GUI)
3. **Clarity**: Each layer has one clear responsibility
4. **Maintainability**: Changes to HTTP handling don't affect business rules

**Real-world analogy**:

- **Service Layer** = The restaurant manager who knows the rules ("No substitutions", "Kitchen closes at 10pm")
- **API Layer** = The waiter who takes orders and brings food
- **Utility Layer** = The kitchen equipment (oven, knives, etc.)

---

### Your Turn: Build the Service - Part 1 (Setup & Structure)

Let's create the `FileService` class incrementally.

1. Create the services directory:

   ```bash
   mkdir backend/app/services
   touch backend/app/services/__init__.py
   touch backend/app/services/file_service.py
   ```

2. Start with the **basic structure and initialization**:

**File: `backend/app/services/file_service.py`**

```python
"""
File Service Layer

This module contains all the business logic for managing files in the PDM system.
It knows the RULES but doesn't know anything about HTTP, APIs, or web requests.
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.utils.file_locking import LockedFile


class FileService:
    """
    Manages file operations and locking state for the PDM system.

    This service is responsible for:
    - Listing files with their lock status
    - Checking out files (acquiring locks)
    - Checking in files (releasing locks)
    - Validating operations according to business rules
    """

    def __init__(self, repo_path: Path, locks_file: Path):
        """
        Initialize the FileService.

        Args:
            repo_path: Directory containing the CAM files to manage
            locks_file: JSON file storing the lock state
        """
        self.repo_path = Path(repo_path)
        self.locks_file = Path(locks_file)

        # Ensure the repo directory exists
        self.repo_path.mkdir(parents=True, exist_ok=True)

        # Initialize locks file if it doesn't exist
        if not self.locks_file.exists():
            self.locks_file.write_text('{"locks": {}}')
```

**What's happening here?**

- `repo_path`: The folder where our actual `.mcam` files live
- `locks_file`: A JSON file tracking which files are locked and by whom
- `mkdir(parents=True, exist_ok=True)`: Create the directory if needed, no error if it exists
- We initialize an empty locks file structure if this is the first run

---

### Your Turn: Build the Service - Part 2 (Listing Files)

Now let's add the method to list all files with their current status.

**Add to `backend/app/services/file_service.py`:**

```python
    def get_files_with_status(self) -> List[Dict[str, Any]]:
        """
        Get a list of all files in the repository with their lock status.

        Returns:
            List of dictionaries, each containing:
            - name: filename
            - status: "available" or "checked_out"
            - size_bytes: file size in bytes
            - locked_by: username if checked out, None if available
            - locked_at: ISO timestamp when locked, None if available
        """
        # Step 1: Load the current lock state
        with LockedFile(self.locks_file) as locks_data:
            locks = locks_data.get("locks", {})

        # Step 2: Find all .mcam files in the repo
        files = []
        for filepath in self.repo_path.glob("*.mcam"):
            filename = filepath.name

            # Step 3: Check if this file is locked
            lock_info = locks.get(filename)

            # Step 4: Build the file info dictionary
            file_info = {
                "name": filename,
                "size_bytes": filepath.stat().st_size,
            }

            if lock_info:
                # File is locked
                file_info["status"] = "checked_out"
                file_info["locked_by"] = lock_info.get("user")
                file_info["locked_at"] = lock_info.get("timestamp")
            else:
                # File is available
                file_info["status"] = "available"
                file_info["locked_by"] = None
                file_info["locked_at"] = None

            files.append(file_info)

        return files
```

**Deep Dive: The `glob` Method**

`Path.glob("*.mcam")` is a powerful pattern-matching function:

- `*` means "any characters"
- `*.mcam` means "any filename ending in .mcam"
- It returns an iterator of matching Path objects

Examples:

- `"*.mcam"` matches: `PN1001.mcam`, `test.mcam`, `file123.mcam`
- `"PN*.mcam"` would match only files starting with "PN"
- `"**/*.mcam"` would search subdirectories too (recursive)

---

### Your Turn: Build the Service - Part 3 (Checkout Logic)

This is the heart of our system - the checkout operation. We'll build it step by step.

**Add to `backend/app/services/file_service.py`:**

```python
    def checkout_file(
        self,
        filename: str,
        user: str,
        message: str
    ) -> Dict[str, Any]:
        """
        Check out a file, acquiring an exclusive lock.

        Business Rules:
        1. File must exist in the repository
        2. File must not already be locked
        3. User and message are required

        Args:
            filename: Name of the file to check out
            user: Username requesting the checkout
            message: Reason for checkout

        Returns:
            Dictionary with operation details

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is already checked out
        """
        # RULE 1: File must exist
        file_path = self.repo_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File '{filename}' does not exist in repository")

        # RULE 2: File must not be locked (check atomically with lock)
        with LockedFile(self.locks_file) as locks_data:
            locks = locks_data.get("locks", {})

            # Check if file is already locked
            if filename in locks:
                existing_lock = locks[filename]
                raise ValueError(
                    f"File '{filename}' is already checked out by "
                    f"{existing_lock['user']} at {existing_lock['timestamp']}"
                )

            # RULE 3: Acquire the lock
            timestamp = datetime.utcnow().isoformat()
            locks[filename] = {
                "user": user,
                "message": message,
                "timestamp": timestamp
            }

            # Update the locks data (will be written when context exits)
            locks_data["locks"] = locks

        return {
            "success": True,
            "filename": filename,
            "locked_by": user,
            "locked_at": timestamp,
            "message": message
        }
```

**Deep Dive: Exception Handling Strategy**

Notice we **raise exceptions** instead of returning error dictionaries. This is intentional:

**Bad approach** (mixing success and failure):

```python
if file_not_found:
    return {"success": False, "error": "Not found"}
return {"success": True, "data": ...}
```

**Good approach** (exceptions for errors):

```python
if file_not_found:
    raise FileNotFoundError("File not found")
return {"success": True, "data": ...}
```

**Why is this better?**

1. **Forces callers to handle errors**: Can't accidentally ignore a `success: False`
2. **Separates happy path from error path**: Normal flow is clearer
3. **Python convention**: Standard library uses exceptions for errors
4. **FastAPI integration**: FastAPI can automatically convert exceptions to HTTP error responses

---

### Your Turn: Build the Service - Part 4 (Checkin Logic)

Now the complementary operation - releasing a lock.

**Add to `backend/app/services/file_service.py`:**

```python
    def checkin_file(self, filename: str, user: str) -> Dict[str, Any]:
        """
        Check in a file, releasing its lock.

        Business Rules:
        1. File must exist in the repository
        2. File must be currently locked
        3. Only the user who checked it out can check it in

        Args:
            filename: Name of the file to check in
            user: Username requesting the checkin

        Returns:
            Dictionary with operation details

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not locked or user doesn't own the lock
        """
        # RULE 1: File must exist
        file_path = self.repo_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File '{filename}' does not exist in repository")

        # RULES 2 & 3: File must be locked by this user
        with LockedFile(self.locks_file) as locks_data:
            locks = locks_data.get("locks", {})

            # Check if file is locked at all
            if filename not in locks:
                raise ValueError(f"File '{filename}' is not currently checked out")

            # Check if this user owns the lock
            current_lock = locks[filename]
            if current_lock["user"] != user:
                raise ValueError(
                    f"File '{filename}' is checked out by {current_lock['user']}, "
                    f"not {user}. Only the user who checked it out can check it in."
                )

            # Release the lock
            del locks[filename]
            locks_data["locks"] = locks

        return {
            "success": True,
            "filename": filename,
            "message": f"File checked in by {user}"
        }
```

**Deep Dive: Authorization Logic**

Notice the checkin has a security check: `if current_lock["user"] != user`. This is **authorization**.

- **Authentication**: "Who are you?" (We're just trusting the `user` parameter for now)
- **Authorization**: "Are you allowed to do this?" (Only the owner can unlock)

In a real production system, you'd have:

1. A proper authentication system (login, sessions, JWT tokens)
2. The authenticated user's identity verified by middleware
3. This service method receives the verified user identity

For our tutorial, we're simplifying by trusting the `user` parameter, but the authorization logic is production-ready.

---

## 3.5: Updating the API Layer

Now we connect our Service Layer to FastAPI's API Layer.

### Deep Dive: Dependency Injection in FastAPI

**Dependency Injection** is a pattern where you don't create objects directly. Instead, you declare what you need, and FastAPI provides it.

**Without DI** (bad - creates new service every time):

```python
@router.get("/files")
def get_files():
    service = FileService(...)  # Creating it here!
    return service.get_files_with_status()
```

**With DI** (good - reuses configured service):

```python
def get_file_service():
    return FileService(...)

@router.get("/files")
def get_files(service: FileService = Depends(get_file_service)):
    return service.get_files_with_status()
```

**Benefits:**

1. **Testability**: You can inject a mock service for testing
2. **Configuration**: Service configuration in one place
3. **Reusability**: All endpoints use the same service instance
4. **Type safety**: FastAPI validates the dependency

---

### Your Turn: Update the Schemas First

Before updating the API, we need schemas for the new checkout/checkin operations.

**Add to `backend/app/schemas/files.py`:**

```python
# Add these new classes to the existing file

class FileCheckoutRequest(BaseModel):
    """Schema for checking out a file."""
    filename: str
    user: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "filename": "PN1001_OP1.mcam",
                "user": "john",
                "message": "Modifying toolpath for new part revision"
            }
        }


class FileCheckinRequest(BaseModel):
    """Schema for checking in a file."""
    filename: str
    user: str

    class Config:
        json_schema_extra = {
            "example": {
                "filename": "PN1001_OP1.mcam",
                "user": "john"
            }
        }


class OperationResponse(BaseModel):
    """Generic response for file operations."""
    success: bool
    message: str
    filename: str
    locked_by: Optional[str] = None
    locked_at: Optional[str] = None
```

---

### Your Turn: Replace the API Endpoints

Now let's completely replace `backend/app/api/files.py` with the new version that uses our service.

**File: `backend/app/api/files.py`** (replace entire file)

```python
"""
File API Endpoints

This module handles HTTP requests for file operations.
It delegates all business logic to the FileService.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from pathlib import Path
from app.schemas.files import (
    FileInfo,
    FileListResponse,
    FileCheckoutRequest,
    FileCheckinRequest,
    OperationResponse
)
from app.services.file_service import FileService


# Router configuration
router = APIRouter(
    prefix="/api/files",
    tags=["Files"],
)


# Dependency: Provides the FileService to endpoints
def get_file_service() -> FileService:
    """
    Dependency injection function.
    Creates and configures the FileService.
    """
    repo_path = Path("repo")
    locks_file = Path("locks.json")
    return FileService(repo_path, locks_file)


@router.get("/", response_model=FileListResponse)
def list_files(service: FileService = Depends(get_file_service)):
    """
    List all files in the repository with their lock status.

    This endpoint:
    1. Uses dependency injection to get the FileService
    2. Calls the service method to get files
    3. Returns them in the API response format
    """
    files = service.get_files_with_status()
    return FileListResponse(files=files, total=len(files))


@router.get("/{filename}", response_model=FileInfo)
def get_file(
    filename: str,
    service: FileService = Depends(get_file_service)
):
    """
    Get details for a specific file.

    Path parameters:
    - filename: The name of the file (e.g., "PN1001.mcam")
    """
    files = service.get_files_with_status()

    for file in files:
        if file["name"] == filename:
            return FileInfo(**file)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"File '{filename}' not found"
    )


@router.post("/checkout", response_model=OperationResponse)
def checkout_file(
    request: FileCheckoutRequest,
    service: FileService = Depends(get_file_service)
):
    """
    Check out a file, acquiring an exclusive lock.

    Request body should contain:
    - filename: File to check out
    - user: Username
    - message: Reason for checkout
    """
    try:
        result = service.checkout_file(
            filename=request.filename,
            user=request.user,
            message=request.message
        )
        return OperationResponse(**result, message="File checked out successfully")

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        # File already locked
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/checkin", response_model=OperationResponse)
def checkin_file(
    request: FileCheckinRequest,
    service: FileService = Depends(get_file_service)
):
    """
    Check in a file, releasing its lock.

    Request body should contain:
    - filename: File to check in
    - user: Username (must match the user who checked it out)
    """
    try:
        result = service.checkin_file(
            filename=request.filename,
            user=request.user
        )
        return OperationResponse(**result)

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        # File not locked, or wrong user
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

**Deep Dive: HTTP Status Codes in Detail**

Notice how we map different exceptions to different HTTP status codes:

- `FileNotFoundError` → **404 Not Found**: "The resource you asked for doesn't exist"
- `ValueError` (already locked) → **409 Conflict**: "Your request conflicts with the current state"
- `ValueError` (wrong user) → **400 Bad Request**: "Your request is invalid"

This is called **semantic HTTP**. The status code communicates the type of problem:

- **2xx**: Success
- **4xx**: Client error (bad request, not found, unauthorized, etc.)
- **5xx**: Server error (our code crashed, database is down, etc.)

Clients can check the status code to handle errors appropriately without parsing error messages.

---

### ✅ Verification Checkpoint - Test the Backend

Let's test our backend with real files and `curl`.

1. **Create test files**:

   ```bash
   mkdir -p backend/repo
   echo "Test content" > backend/repo/PN1001.mcam
   echo "Test content" > backend/repo/PN1002.mcam
   echo "Test content" > backend/repo/PN1003.mcam
   ```

2. **Start the server**:

   ```bash
   cd backend
   source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
   uvicorn app.main:app --reload
   ```

3. **Test listing files**:

   ```bash
   curl http://127.0.0.1:8000/api/files
   ```

   You should see JSON with all three files, all showing `"status": "available"`.

4. **Test checkout** (Mac/Linux):

   ```bash
   curl -X POST http://127.0.0.1:8000/api/files/checkout \
     -H "Content-Type: application/json" \
     -d '{"filename":"PN1001.mcam","user":"alice","message":"Testing checkout"}'
   ```

   **Windows PowerShell**:

   ```powershell
   curl.exe -X POST http://127.0.0.1:8000/api/files/checkout `
     -H "Content-Type: application/json" `
     -d '{\"filename\":\"PN1001.mcam\",\"user\":\"alice\",\"message\":\"Testing checkout\"}'
   ```

   You should see `"success": true`.

5. **Test duplicate checkout** (should fail):
   Run the same curl command again. You should see a **409 Conflict** error with a message about the file already being checked out.

6. **Test checkin**:

   ```bash
   curl -X POST http://127.0.0.1:8000/api/files/checkin \
     -H "Content-Type: application/json" \
     -d '{"filename":"PN1001.mcam","user":"alice"}'
   ```

   You should see `"success": true`.

7. **Verify the lock file**:

   ```bash
   cat backend/locks.json
   ```

   After checkout it should show Alice's lock. After checkin it should be empty: `{"locks": {}}`.

If all these tests pass, your backend is fully functional!

---

## 3.6: Building the Interactive Frontend

Now let's build the modal dialog system and connect the UI to our new backend endpoints.

### Your Turn: Add Modal CSS

**Add to the end of `backend/static/css/components.css`:**

```css
/* === Modal Dialog System === */

/* Overlay that darkens the background */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* The modal card itself */
.modal-content {
  background: var(--bg-primary);
  border-radius: 0.5rem;
  padding: var(--spacing-6);
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  margin-bottom: var(--spacing-4);
}

.modal-header h3 {
  margin: 0;
  color: var(--text-primary);
}

.modal-body {
  margin-bottom: var(--spacing-6);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

/* Form elements inside modals */
.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 500;
  color: var(--text-primary);
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--border-default);
  border-radius: 0.25rem;
  font-family: inherit;
  font-size: 1rem;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

/* Button styles */
.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background-color: var(--color-primary-500);
  color: white;
}

.btn-primary:hover {
  background-color: var(--color-primary-700);
}

.btn-secondary {
  background-color: var(--color-gray-200);
  color: var(--text-primary);
}

.btn-secondary:hover {
  background-color: var(--color-gray-300);
}

.btn-small {
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
}

/* Hidden state */
.hidden {
  display: none;
}
```

---

### Your Turn: Add Modal HTML

**Add to `backend/static/index.html`** right before the closing `</body>` tag:

```html
    <!-- Checkout Modal -->
    <div id="checkout-modal" class="modal-overlay hidden">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Check Out File</h3>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="checkout-filename">File:</label>
            <input type="text" id="checkout-filename" readonly>
          </div>
          <div class="form-group">
            <label for="checkout-user">Your Name:</label>
            <input type="text" id="checkout-user" placeholder="Enter your name">
          </div>
          <div class="form-group">
            <label for="checkout-message">Reason for Checkout:</label>
            <textarea id="checkout-message" placeholder="What are you working on?"></textarea>
          </div>
          <div id="checkout-error" class="hidden" style="color: red; margin-top: 0.5rem;"></div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" onclick="closeCheckoutModal()">Cancel</button>
          <button class="btn btn-primary" onclick="confirmCheckout()">Check Out</button>
        </div>
      </div>
    </div>

    <!-- Checkin Modal -->
    <div id="checkin-modal" class="modal-overlay hidden">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Check In File</h3>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="checkin-filename">File:</label>
            <input type="text" id="checkin-filename" readonly>
          </div>
          <div class="form-group">
            <label for="checkin-user">Your Name:</label>
            <input type="text" id="checkin-user" placeholder="Enter your name">
          </div>
          <p>Checking in this file will release the lock and make it available to others.</p>
          <div id="checkin-error" class="hidden" style="color: red; margin-top: 0.5rem;"></div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" onclick="closeCheckinModal()">Cancel</button>
          <button class="btn btn-primary" onclick="confirmCheckin()">Check In</button>
        </div>
      </div>
    </div>

    <script type="module" src="/static/js/app.js"></script>
  </body>
</html>
```

---

### Your Turn: Update api-client.js with POST support

**Replace `backend/static/js/modules/api-client.js`** with:

```javascript
/**
 * API Client Module
 *
 * Centralized module for all communication with the backend API.
 * Handles both GET and POST requests.
 */
export class APIClient {
  /**
   * Fetch the list of all files.
   */
  async getFiles() {
    try {
      const response = await fetch("/api/files");
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP error! status: ${response.status}`
        );
      }
      return await response.json();
    } catch (error) {
      console.error("Failed to fetch files:", error);
      throw error;
    }
  }

  /**
   * Generic POST method for sending data to the API.
   *
   * @param {string} endpoint - The API endpoint (e.g., "/api/files/checkout")
   * @param {object} data - The data to send in the request body
   */
  async post(endpoint, data) {
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const responseData = await response.json();

      if (!response.ok) {
        // The server returned an error status
        throw new Error(
          responseData.detail || `HTTP error! status: ${response.status}`
        );
      }

      return responseData;
    } catch (error) {
      console.error(`POST request to ${endpoint} failed:`, error);
      throw error;
    }
  }

  /**
   * Check out a file.
   */
  async checkoutFile(filename, user, message) {
    return this.post("/api/files/checkout", { filename, user, message });
  }

  /**
   * Check in a file.
   */
  async checkinFile(filename, user) {
    return this.post("/api/files/checkin", { filename, user });
  }
}

export const apiClient = new APIClient();
```

---

### Your Turn: Build the Complete Interactive app.js

**Replace `backend/static/js/app.js`** with:

```javascript
/**
 * Main Application Logic
 *
 * This is the "controller" that connects the UI to the API.
 * It handles user interactions and updates the DOM.
 */
import { apiClient } from "./modules/api-client.js";

// DOM element references
const fileListEl = document.getElementById("file-list");
const loadingEl = document.getElementById("loading-indicator");
const checkoutModal = document.getElementById("checkout-modal");
const checkinModal = document.getElementById("checkin-modal");

// Current state (we'll improve this in Stage 4)
let currentFilename = null;

/**
 * Creates the HTML for a single file item.
 * Now with action buttons!
 */
function createFileElement(file) {
  const div = document.createElement("div");
  div.className = "file-item";

  // File name
  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  // Status badge
  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ");

  // Action button (checkout or checkin depending on status)
  const actionBtn = document.createElement("button");
  actionBtn.className = "btn btn-primary btn-small";

  if (file.status === "available") {
    actionBtn.textContent = "Check Out";
    actionBtn.onclick = () => openCheckoutModal(file.name);
  } else {
    actionBtn.textContent = "Check In";
    actionBtn.onclick = () => openCheckinModal(file.name, file.locked_by);
  }

  // Assemble the file item
  div.appendChild(nameSpan);
  div.appendChild(statusSpan);
  div.appendChild(actionBtn);

  return div;
}

/**
 * Loads files from the API and displays them.
 */
async function loadAndDisplayFiles() {
  try {
    loadingEl.style.display = "block";
    fileListEl.innerHTML = "";

    const data = await apiClient.getFiles();
    loadingEl.style.display = "none";

    if (data.files.length === 0) {
      fileListEl.innerHTML = "<p>No files found in repository.</p>";
      return;
    }

    data.files.forEach((file) => {
      const fileElement = createFileElement(file);
      fileListEl.appendChild(fileElement);
    });
  } catch (error) {
    loadingEl.style.display = "none";
    fileListEl.innerHTML = `<p style="color: red;">Error loading files: ${error.message}</p>`;
  }
}

/* ============================================
   CHECKOUT MODAL FUNCTIONS
   ============================================ */

/**
 * Opens the checkout modal for a specific file.
 */
function openCheckoutModal(filename) {
  currentFilename = filename;
  document.getElementById("checkout-filename").value = filename;
  document.getElementById("checkout-user").value = "";
  document.getElementById("checkout-message").value = "";
  document.getElementById("checkout-error").classList.add("hidden");
  checkoutModal.classList.remove("hidden");
}

/**
 * Closes the checkout modal.
 */
function closeCheckoutModal() {
  checkoutModal.classList.add("hidden");
  currentFilename = null;
}

/**
 * Handles the checkout confirmation.
 */
async function confirmCheckout() {
  const user = document.getElementById("checkout-user").value.trim();
  const message = document.getElementById("checkout-message").value.trim();
  const errorEl = document.getElementById("checkout-error");

  // Validation
  if (!user || !message) {
    errorEl.textContent = "Please fill in all fields.";
    errorEl.classList.remove("hidden");
    return;
  }

  try {
    await apiClient.checkoutFile(currentFilename, user, message);
    closeCheckoutModal();
    await loadAndDisplayFiles(); // Refresh the list
  } catch (error) {
    errorEl.textContent = error.message;
    errorEl.classList.remove("hidden");
  }
}

/* ============================================
   CHECKIN MODAL FUNCTIONS
   ============================================ */

/**
 * Opens the checkin modal for a specific file.
 */
function openCheckinModal(filename, lockedBy) {
  currentFilename = filename;
  document.getElementById("checkin-filename").value = filename;
  document.getElementById("checkin-user").value = lockedBy || "";
  document.getElementById("checkin-error").classList.add("hidden");
  checkinModal.classList.remove("hidden");
}

/**
 * Closes the checkin modal.
 */
function closeCheckinModal() {
  checkinModal.classList.add("hidden");
  currentFilename = null;
}

/**
 * Handles the checkin confirmation.
 */
async function confirmCheckin() {
  const user = document.getElementById("checkin-user").value.trim();
  const errorEl = document.getElementById("checkin-error");

  if (!user) {
    errorEl.textContent = "Please enter your name.";
    errorEl.classList.remove("hidden");
    return;
  }

  try {
    await apiClient.checkinFile(currentFilename, user);
    closeCheckinModal();
    await loadAndDisplayFiles(); // Refresh the list
  } catch (error) {
    errorEl.textContent = error.message;
    errorEl.classList.remove("hidden");
  }
}

/* ============================================
   INITIALIZATION
   ============================================ */

// Make modal functions globally available (needed for onclick handlers)
window.openCheckoutModal = openCheckoutModal;
window.closeCheckoutModal = closeCheckoutModal;
window.confirmCheckout = confirmCheckout;
window.openCheckinModal = openCheckinModal;
window.closeCheckinModal = closeCheckinModal;
window.confirmCheckin = confirmCheckin;

// Initialize the app when the page loads
document.addEventListener("DOMContentLoaded", () => {
  loadAndDisplayFiles();
});
```

**Deep Dive: Why `window.functionName`?**

Notice lines like `window.closeCheckoutModal = closeCheckoutModal`. Here's why:

When you use `onclick="functionName()"` in HTML, the browser looks for that function in the **global scope** (the `window` object). But our functions are in a **module**, which has its own private scope.

**The problem:**

```html
<button onclick="closeModal()">Close</button>
<!-- ❌ Browser error: "closeModal is not defined" -->
```

**The solution:**

```javascript
window.closeModal = closeModal; // Expose to global scope
```

**Alternative approach** (better, but more code):

```javascript
// Instead of onclick in HTML, add listeners in JS:
document.getElementById("close-btn").addEventListener("click", closeModal);
```

For this tutorial we use `window.functionName` for simplicity, but in Stage 4 we'll refactor to event listeners.

---

### ✅ Final Verification - The Complete Flow

1. **Ensure your server is running**:

   ```bash
   uvicorn app.main:app --reload
   ```

2. **Open your browser** to http://127.0.0.1:8000

3. **Test the checkout flow**:

   - Click "Check Out" on an available file
   - Fill in your name and a message
   - Click "Check Out"
   - The modal should close
   - The file list should refresh showing the file as "checked out"

4. **Test error handling**:

   - Try to check out the same file again (different browser tab or user)
   - You should see an error message in the modal

5. **Test the checkin flow**:

   - Click "Check In" on a checked-out file
   - Enter the same username
   - The file should become available again

6. **Test authorization**:

   - Check out a file as "alice"
   - Try to check it in as "bob"
   - You should see an error message

7. **Watch the network tab**:
   - Open Developer Tools (F12)
   - Go to the Network tab
   - Perform a checkout
   - You'll see the POST request and response, just like with `curl`!

---

## 3.7: Commit the Complete Feature

This is a major milestone - a fully functional checkout/checkin system!

```bash
git add .
git commit -m "feat: Implement complete file checkout/checkin system with locking and modal UI"
```

---

## Stage 3 Complete ✓

You've built a production-ready file locking system from the ground up. You now have:

- A **race-condition-proof** file locking utility
- A clean **Service Layer** architecture
- **Dependency Injection** in your API
- An **interactive modal system** on the frontend
- Full **error handling** throughout the stack

### Final File Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── files.py (updated with checkout/checkin)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── files.py (added request/response schemas)
│   ├── services/
│   │   ├── __init__.py
│   │   └── file_service.py (NEW - business logic)
│   ├── utils/
│   │   ├── __init__.py
│   │   └── file_locking.py (NEW - atomic file operations)
│   ├── __init__.py
│   ├── main.py
│   ├── learn_race_condition.py (educational demo)
│   └── learn_lock_safety.py (educational demo)
├── static/
│   ├── css/
│   │   ├── components.css (added modal styles)
│   │   └── (other CSS files)
│   ├── js/
│   │   ├── modules/
│   │   │   └── api-client.js (added POST methods)
│   │   └── app.js (now fully interactive)
│   └── index.html (added modals)
├── repo/
│   ├── PN1001.mcam
│   ├── PN1002.mcam
│   └── PN1003.mcam
├── locks.json (created at runtime)
└── (other files)
```

### Verification Checklist

- [ ] Files can be checked out with user and message
- [ ] Checked-out files cannot be checked out again (409 error)
- [ ] Only the user who checked out a file can check it in
- [ ] The `locks.json` file correctly tracks lock state
- [ ] Modals open and close properly
- [ ] Error messages display in modals when operations fail
- [ ] The file list refreshes after checkout/checkin
- [ ] Both `curl` and browser interface work correctly

### What We Learned

**Concepts:**

- Race conditions and why they matter
- Atomic operations and file locking
- Context managers (`with` statement)
- Service Layer architecture
- Dependency Injection pattern
- Exception handling strategy
- Authorization vs Authentication

**Skills:**

- Building cross-platform Python utilities
- Writing testable business logic
- Creating modal dialogs
- Making POST requests from JavaScript
- Testing APIs with `curl` and browser tools

---

# PDM Tutorial (Complete Edition) - Stage 4: Professional Frontend State Management

**Goal**: To refactor our frontend to use a centralized state management pattern, making it more maintainable, reactive, and easier to extend. We'll keep all our Stage 3 functionality (modals, checkout/checkin) while making the architecture cleaner and adding new features like search and filtering.

**What You'll Learn**:

- The **Observer Pattern** and how it powers reactive UIs
- Building a **central store** as a single source of truth
- **Computed properties** for derived data
- How proper state management makes adding features trivially easy
- Refactoring existing code to a better architecture without breaking it

---

## 4.1: The Problem - Why Refactor?

Our Stage 3 code works, but it has growing pains:

### Current Issues

1. **Manual UI updates everywhere:**

   ```javascript
   await apiClient.checkoutFile(...);
   await loadAndDisplayFiles();  // Have to remember this!
   ```

2. **Scattered state:**

   - `currentFilename` is a global variable
   - File data is fetched repeatedly
   - No single source of truth

3. **Adding features is messy:**
   - Want search? Have to thread it through multiple functions
   - Want filtering? Same problem
   - Each feature increases complexity

### Deep Dive: What is "State" in Frontend Development?

**State** is any data that can change over time and affects what the user sees. In our app:

- **Data state**: The list of files from the API
- **UI state**: Is a modal open? What's in the search box?
- **Loading state**: Are we waiting for an API response?
- **Error state**: Did something go wrong?

Right now, this state is scattered across:

- Variables (`currentFilename`)
- The DOM itself (what's currently displayed)
- Function parameters
- API responses

This is called **implicit state** - it exists, but it's not organized or managed.

**Explicit state management** means:

- One central place holds all state
- State changes are tracked and controlled
- UI automatically updates when state changes
- Adding features means updating state, not rewriting UI code

---

## 4.2: The Solution - The Observer Pattern

We'll implement a pattern that's at the heart of React, Vue, Angular, and every modern frontend framework: **the Observer Pattern** (also called Pub/Sub).

### Deep Dive: How the Observer Pattern Works

Think of it like a newsletter subscription:

```
┌─────────────────────┐
│   Store (Subject)   │  <- Holds the state
│   "I have news!"    │
└─────────────────────┘
         │
         ├─ notifies ──> Subscriber 1 (UI Component)
         ├─ notifies ──> Subscriber 2 (Another Component)
         └─ notifies ──> Subscriber 3 (Logger, etc.)
```

**The flow:**

1. Components **subscribe** to the store ("Tell me when things change")
2. Something **changes the state** (user action, API response)
3. Store **notifies all subscribers** automatically
4. Each subscriber **re-renders itself** with the new state

**Why this is powerful:**

- Components don't need to know about each other
- State changes in one place trigger updates everywhere
- Adding a new subscriber doesn't change existing code
- Debugging is easier - state changes are centralized

---

### Your Turn: Understand the Pattern - A Mini Exercise

Before building our real store, let's see the pattern in action with a tiny example.

**Create: `backend/static/js/modules/learn_observer.js`**

```javascript
/**
 * A minimal demonstration of the Observer Pattern.
 * This is the core concept behind React, Vue, and our store.
 */

class ObservableCounter {
  constructor(initialValue) {
    this._value = initialValue;
    this._subscribers = [];
  }

  // Subscribe to changes
  subscribe(callback) {
    this._subscribers.push(callback);
    // Immediately call with current value
    callback(this._value);
  }

  // Get current value
  getValue() {
    return this._value;
  }

  // Change the value and notify everyone
  setValue(newValue) {
    this._value = newValue;
    console.log(
      `[Store] Value changed to ${newValue}, notifying ${this._subscribers.length} subscribers...`
    );
    this._subscribers.forEach((callback) => callback(this._value));
  }
}

// Create a counter
const counter = new ObservableCounter(0);

// Subscribe various "components"
counter.subscribe((value) => {
  console.log(`  [UI Component] Received update: ${value}`);
});

counter.subscribe((value) => {
  console.log(`  [Logger] Recording: ${value}`);
});

// Now watch what happens when we change the value
console.log("\n--- Changing value to 5 ---");
counter.setValue(5);

console.log("\n--- Changing value to 10 ---");
counter.setValue(10);
```

**Run it** (in browser console or with Node):

```bash
node backend/static/js/modules/learn_observer.js
```

You'll see both subscribers automatically get notified each time the value changes. This is **reactive programming** - the UI reacts to state changes automatically.

---

## 4.3: Building Our Application Store - Part 1 (Foundation)

Now let's build the real store for our PDM application. We'll do this incrementally.

**Create: `backend/static/js/modules/store.js`**

```javascript
/**
 * Application Store
 *
 * This is the single source of truth for all application state.
 * It implements the Observer pattern to notify UI components of changes.
 */

class Store {
  constructor() {
    // The state object - all app data lives here
    this._state = {
      // Data from the API
      allFiles: [],

      // UI state
      isLoading: false,
      error: null,
      searchTerm: "",
      statusFilter: "all", // "all", "available", "checked_out"

      // Modal state
      isCheckoutModalOpen: false,
      isCheckinModalOpen: false,
      selectedFile: null, // The file currently selected in a modal
    };

    // Array of subscriber functions
    this._subscribers = [];
  }

  /**
   * Subscribe to state changes.
   * The callback will be called immediately with current state,
   * and again whenever state changes.
   */
  subscribe(callback) {
    this._subscribers.push(callback);
    // Immediately invoke with current state
    callback(this._getPublicState());
  }

  /**
   * Get a copy of the state (read-only for subscribers).
   */
  _getPublicState() {
    return { ...this._state };
  }

  /**
   * Notify all subscribers of state changes.
   */
  _notify() {
    const state = this._getPublicState();
    this._subscribers.forEach((callback) => callback(state));
  }
}

// Export a singleton instance
export const store = new Store();
```

**Deep Dive: Why `_getPublicState()`?**

Notice we return `{ ...this._state }` instead of `this._state` directly. The `...` is the **spread operator** - it creates a **shallow copy**.

**Why?**

```javascript
// Without spread - BAD
const state = this._state;
state.searchTerm = "hack"; // Directly modifies store state! 😱

// With spread - GOOD
const state = { ...this._state };
state.searchTerm = "hack"; // Only modifies the copy ✓
```

This prevents subscribers from accidentally modifying state directly. State should only change through the store's methods (which we'll add next).

---

## 4.4: Building Our Application Store - Part 2 (Actions)

Now let's add methods to **change** the state. These are called **actions**.

**Add to `store.js` inside the Store class:**

```javascript
  /* ==========================================
     ACTIONS - Methods that modify state
     ========================================== */

  /**
   * Set loading state (typically before an API call).
   */
  setLoading(isLoading) {
    this._state.isLoading = isLoading;
    if (isLoading) {
      this._state.error = null; // Clear errors when starting new load
    }
    this._notify();
  }

  /**
   * Update the files list (typically after API response).
   */
  setFiles(files) {
    this._state.allFiles = files;
    this._state.isLoading = false;
    this._state.error = null;
    this._notify();
  }

  /**
   * Set an error state (typically after API failure).
   */
  setError(errorMessage) {
    this._state.error = errorMessage;
    this._state.isLoading = false;
    this._notify();
  }

  /**
   * Update the search term filter.
   */
  setSearchTerm(term) {
    this._state.searchTerm = term;
    this._notify();
  }

  /**
   * Update the status filter.
   */
  setStatusFilter(filter) {
    this._state.statusFilter = filter;
    this._notify();
  }

  /**
   * Open the checkout modal for a specific file.
   */
  openCheckoutModal(file) {
    this._state.isCheckoutModalOpen = true;
    this._state.selectedFile = file;
    this._notify();
  }

  /**
   * Close the checkout modal.
   */
  closeCheckoutModal() {
    this._state.isCheckoutModalOpen = false;
    this._state.selectedFile = null;
    this._notify();
  }

  /**
   * Open the checkin modal for a specific file.
   */
  openCheckinModal(file) {
    this._state.isCheckinModalOpen = true;
    this._state.selectedFile = file;
    this._notify();
  }

  /**
   * Close the checkin modal.
   */
  closeCheckinModal() {
    this._state.isCheckinModalOpen = false;
    this._state.selectedFile = null;
    this._notify();
  }
```

**Deep Dive: Why Actions Instead of Direct Access?**

Compare these approaches:

**Bad - Direct state modification:**

```javascript
store._state.searchTerm = "new value";
// UI doesn't update! Forgot to call _notify()
```

**Good - Using actions:**

```javascript
store.setSearchTerm("new value");
// Action handles the update AND notification
```

Actions ensure:

1. State changes are **tracked** (could add logging, undo, etc.)
2. Notifications **always happen**
3. Related state updates happen **together** (atomically)
4. Code is **self-documenting** (clear intent)

---

## 4.5: Building Our Application Store - Part 3 (Computed Properties)

Sometimes you need to **derive** data from state without storing it redundantly. These are **computed properties** (or "selectors").

**Add to `store.js` inside the Store class:**

```javascript
  /* ==========================================
     COMPUTED PROPERTIES - Derived state
     ========================================== */

  /**
   * Get the filtered and searched list of files to display.
   * This is computed from the state, not stored in it.
   *
   * Why? Because it's derived from allFiles + searchTerm + statusFilter.
   * If we stored it, we'd have to keep it in sync manually.
   */
  getDisplayFiles() {
    let files = this._state.allFiles;

    // Apply status filter
    if (this._state.statusFilter !== "all") {
      files = files.filter(file => file.status === this._state.statusFilter);
    }

    // Apply search filter
    if (this._state.searchTerm) {
      const term = this._state.searchTerm.toLowerCase();
      files = files.filter(file =>
        file.name.toLowerCase().includes(term)
      );
    }

    return files;
  }

  /**
   * Get the currently selected file (for modals).
   */
  getSelectedFile() {
    return this._state.selectedFile;
  }
```

**Deep Dive: Why Computed Instead of Stored?**

Imagine we stored filtered files in state:

```javascript
// BAD APPROACH
this._state = {
  allFiles: [...],
  displayFiles: [...],  // Duplicate data!
  searchTerm: ""
}
```

**Problems:**

1. When `allFiles` changes, must update `displayFiles`
2. When `searchTerm` changes, must update `displayFiles`
3. When `statusFilter` changes, must update `displayFiles`
4. Easy to forget, causing bugs

**With computed properties:**

```javascript
// GOOD APPROACH
getDisplayFiles() {
  return this._state.allFiles.filter(...);  // Always correct
}
```

The filtered list is **always derived from current state** - can't get out of sync!

**This is a key principle:** Store the minimal state needed, compute everything else.

---

## 4.6: Refactoring app.js to Use the Store

Now comes the magic - refactoring our Stage 3 code to use the store. The functionality stays identical, but the architecture becomes cleaner.

**Replace `backend/static/js/app.js` entirely:**

```javascript
/**
 * Main Application Logic (Store-Driven Version)
 *
 * This is now much simpler:
 * 1. Subscribe to the store
 * 2. Render based on current state
 * 3. Dispatch actions on user interactions
 */
import { store } from "./modules/store.js";
import { apiClient } from "./modules/api-client.js";

/* ==========================================
   RENDERING - The UI is a function of state
   ========================================== */

/**
 * The main render function.
 * This is called automatically whenever the store state changes.
 *
 * It's the ONLY place we manipulate the DOM.
 */
function render(state) {
  renderFileList(state);
  renderModals(state);
}

/**
 * Render the file list section.
 */
function renderFileList(state) {
  const listEl = document.getElementById("file-list");
  const loadingEl = document.getElementById("loading-indicator");

  // Show/hide loading indicator
  loadingEl.style.display = state.isLoading ? "block" : "none";

  // Show error if present
  if (state.error) {
    listEl.innerHTML = `<p style="color: red;">Error: ${state.error}</p>`;
    return;
  }

  // Don't render if still loading
  if (state.isLoading) {
    return;
  }

  // Get the filtered files from the store
  const filesToDisplay = store.getDisplayFiles();

  // Clear and rebuild the list
  listEl.innerHTML = "";

  if (filesToDisplay.length === 0) {
    listEl.innerHTML = "<p>No files match your filters.</p>";
    return;
  }

  filesToDisplay.forEach((file) => {
    const fileEl = createFileElement(file);
    listEl.appendChild(fileEl);
  });
}

/**
 * Create a single file list item element.
 */
function createFileElement(file) {
  const div = document.createElement("div");
  div.className = "file-item";

  // File name
  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  // Status badge
  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ");

  // Action button
  const actionBtn = document.createElement("button");
  actionBtn.className = "btn btn-primary btn-small";

  if (file.status === "available") {
    actionBtn.textContent = "Check Out";
    actionBtn.onclick = () => store.openCheckoutModal(file);
  } else {
    actionBtn.textContent = "Check In";
    actionBtn.onclick = () => store.openCheckinModal(file);
  }

  div.appendChild(nameSpan);
  div.appendChild(statusSpan);
  div.appendChild(actionBtn);

  return div;
}

/**
 * Render modal states (show/hide).
 */
function renderModals(state) {
  const checkoutModal = document.getElementById("checkout-modal");
  const checkinModal = document.getElementById("checkin-modal");

  // Checkout modal
  if (state.isCheckoutModalOpen) {
    checkoutModal.classList.remove("hidden");
    populateCheckoutModal(state.selectedFile);
  } else {
    checkoutModal.classList.add("hidden");
  }

  // Checkin modal
  if (state.isCheckinModalOpen) {
    checkinModal.classList.remove("hidden");
    populateCheckinModal(state.selectedFile);
  } else {
    checkinModal.classList.add("hidden");
  }
}

/**
 * Populate the checkout modal with file data.
 */
function populateCheckoutModal(file) {
  if (!file) return;
  document.getElementById("checkout-filename").value = file.name;
  document.getElementById("checkout-user").value = "";
  document.getElementById("checkout-message").value = "";
  document.getElementById("checkout-error").classList.add("hidden");
}

/**
 * Populate the checkin modal with file data.
 */
function populateCheckinModal(file) {
  if (!file) return;
  document.getElementById("checkin-filename").value = file.name;
  document.getElementById("checkin-user").value = file.locked_by || "";
  document.getElementById("checkin-error").classList.add("hidden");
}

/* ==========================================
   API INTERACTIONS
   ========================================== */

/**
 * Load files from the API and update the store.
 */
async function loadFiles() {
  store.setLoading(true);
  try {
    const data = await apiClient.getFiles();
    store.setFiles(data.files);
  } catch (error) {
    store.setError(error.message);
  }
}

/**
 * Handle checkout confirmation.
 */
async function handleCheckoutConfirm() {
  const user = document.getElementById("checkout-user").value.trim();
  const message = document.getElementById("checkout-message").value.trim();
  const errorEl = document.getElementById("checkout-error");

  if (!user || !message) {
    errorEl.textContent = "Please fill in all fields.";
    errorEl.classList.remove("hidden");
    return;
  }

  const file = store.getSelectedFile();
  if (!file) return;

  try {
    await apiClient.checkoutFile(file.name, user, message);
    store.closeCheckoutModal();
    await loadFiles(); // Refresh the file list
  } catch (error) {
    errorEl.textContent = error.message;
    errorEl.classList.remove("hidden");
  }
}

/**
 * Handle checkin confirmation.
 */
async function handleCheckinConfirm() {
  const user = document.getElementById("checkin-user").value.trim();
  const errorEl = document.getElementById("checkin-error");

  if (!user) {
    errorEl.textContent = "Please enter your name.";
    errorEl.classList.remove("hidden");
    return;
  }

  const file = store.getSelectedFile();
  if (!file) return;

  try {
    await apiClient.checkinFile(file.name, user);
    store.closeCheckinModal();
    await loadFiles(); // Refresh the file list
  } catch (error) {
    errorEl.textContent = error.message;
    errorEl.classList.remove("hidden");
  }
}

/* ==========================================
   EVENT HANDLERS
   ========================================== */

/**
 * Initialize event handlers.
 */
function initEventHandlers() {
  // Search input
  document.getElementById("file-search").addEventListener("input", (e) => {
    store.setSearchTerm(e.target.value);
  });

  // Status filter
  document.getElementById("status-filter").addEventListener("change", (e) => {
    store.setStatusFilter(e.target.value);
  });

  // Modal buttons - using event listeners instead of onclick in HTML
  document
    .getElementById("checkout-cancel-btn")
    .addEventListener("click", () => {
      store.closeCheckoutModal();
    });

  document
    .getElementById("checkout-confirm-btn")
    .addEventListener("click", () => {
      handleCheckoutConfirm();
    });

  document
    .getElementById("checkin-cancel-btn")
    .addEventListener("click", () => {
      store.closeCheckinModal();
    });

  document
    .getElementById("checkin-confirm-btn")
    .addEventListener("click", () => {
      handleCheckinConfirm();
    });
}

/* ==========================================
   INITIALIZATION
   ========================================== */

document.addEventListener("DOMContentLoaded", () => {
  // Subscribe to store - render will be called on every state change
  store.subscribe(render);

  // Set up event handlers
  initEventHandlers();

  // Load initial data
  loadFiles();
});
```

**Deep Dive: What Changed?**

Let's compare the architectures:

**Stage 3 (Imperative):**

```javascript
// State is scattered
let currentFilename = null;

// UI updates are manual
function openModal(filename) {
  currentFilename = filename;
  modal.classList.remove("hidden");  // Manual DOM update
}

function confirmCheckout() {
  // ... do checkout ...
  modal.classList.add("hidden");     // Manual DOM update
  await loadAndDisplayFiles();        // Manual refresh
}
```

**Stage 4 (Declarative with Store):**

```javascript
// State is centralized
store = {
  selectedFile: null,
  isModalOpen: false,
  files: []
}

// UI updates are automatic
function render(state) {
  // UI is rebuilt from state
  modal.classList.toggle("hidden", !state.isModalOpen);
  renderFiles(state.files);
}

function confirmCheckout() {
  // ... do checkout ...
  store.closeModal();   // Changes state
  await loadFiles();    // Changes state
  // render() is called automatically!
}
```

The Stage 4 approach is **declarative** - you declare what the UI should look like for a given state, and it updates automatically.

---

## 4.7: Adding Search and Filter UI

Now let's add the UI controls. Because we're using the store, this is trivial.

**Add to `backend/static/index.html`** inside the `file-list-card` section, right after the `<h2>`:

```html
<div
  class="file-controls"
  style="display: flex; gap: 1rem; margin-bottom: 1rem;"
>
  <input
    id="file-search"
    type="text"
    placeholder="Search files..."
    style="padding: 0.5rem; flex-grow: 1; border: 1px solid var(--border-default); border-radius: 0.25rem;"
  />
  <select
    id="status-filter"
    style="padding: 0.5rem; border: 1px solid var(--border-default); border-radius: 0.25rem;"
  >
    <option value="all">All Files</option>
    <option value="available">Available</option>
    <option value="checked_out">Checked Out</option>
  </select>
</div>
```

**Update the modal buttons in HTML** to use IDs instead of onclick:

In the checkout modal, replace:

```html
<!-- OLD -->
<button class="btn btn-secondary" onclick="closeCheckoutModal()">Cancel</button>
<button class="btn btn-primary" onclick="confirmCheckout()">Check Out</button>

<!-- NEW -->
<button id="checkout-cancel-btn" class="btn btn-secondary">Cancel</button>
<button id="checkout-confirm-btn" class="btn btn-primary">Check Out</button>
```

In the checkin modal, replace:

```html
<!-- OLD -->
<button class="btn btn-secondary" onclick="closeCheckinModal()">Cancel</button>
<button class="btn btn-primary" onclick="confirmCheckin()">Check In</button>

<!-- NEW -->
<button id="checkin-cancel-btn" class="btn btn-secondary">Cancel</button>
<button id="checkin-confirm-btn" class="btn btn-primary">Check In</button>
```

---

## 4.8: Final Verification

Let's test everything works:

1. **Start the server**:

   ```bash
   uvicorn app.main:app --reload
   ```

2. **Open the browser** to http://127.0.0.1:8000

3. **Test search**:

   - Type "PN1001" in the search box
   - The list should instantly filter to show only matching files
   - Clear the search - all files return

4. **Test status filter**:

   - Select "Available" - only available files show
   - Select "Checked Out" - only checked-out files show
   - Select "All" - all files show

5. **Test checkout flow**:

   - Click "Check Out" on a file
   - Modal opens with the file name pre-filled
   - Fill in user and message
   - Click "Check Out"
   - Modal closes automatically
   - File list refreshes showing the file as checked out

6. **Test search + filter combination**:

   - Check out "PN1001"
   - Set filter to "Checked Out"
   - Type "PN1001" in search
   - Should show only PN1001
   - Change filter to "Available"
   - PN1001 disappears (it's checked out)

7. **Test checkin flow**:
   - Click "Check In" on a checked-out file
   - Modal opens with username pre-filled
   - Confirm
   - File becomes available again

**Open the browser console (F12)** and watch as you interact - you won't see any errors. The store is managing everything cleanly.

---

## 4.9: Commit the Refactor

```bash
git add .
git commit -m "refactor: Implement centralized state management with search and filter"
```

---

## Stage 4 Complete ✓

You've successfully refactored to a professional state management architecture while keeping all functionality intact and adding new features.

### What Changed

**Before (Stage 3):**

- State scattered across variables and DOM
- Manual DOM updates everywhere
- Adding features meant rewriting UI code
- 150+ lines of imperative code

**After (Stage 4):**

- Centralized state in store
- Single render function subscribed to state
- Adding features means updating state
- Clearer separation of concerns
- Search and filter added with ~10 lines of code

### Final File Structure

```
backend/
├── app/
│   └── (unchanged - backend is solid)
├── static/
│   ├── js/
│   │   ├── modules/
│   │   │   ├── api-client.js (unchanged)
│   │   │   ├── store.js (NEW - state management)
│   │   │   └── learn_observer.js (educational)
│   │   └── app.js (refactored to use store)
│   └── index.html (added search/filter UI)
└── ...
```

### Verification Checklist

- [ ] Search filters files as you type
- [ ] Status filter dropdown works correctly
- [ ] Search and filter work together
- [ ] All checkout/checkin functionality still works
- [ ] Modals open and close properly
- [ ] File list refreshes after operations
- [ ] No console errors
- [ ] State changes trigger automatic UI updates

### What We Learned

**Concepts:**

- Observer Pattern (Pub/Sub)
- Centralized state management
- Computed properties vs stored state
- Declarative vs imperative programming
- Single source of truth principle

**Skills:**

- Building a reactive store from scratch
- Refactoring without breaking functionality
- Implementing efficient filters and search
- Managing complex UI state
- Event-driven architecture

### The Power of This Architecture

Notice how easy it was to add search and filter:

1. Added `searchTerm` and `statusFilter` to state
2. Added actions to update them
3. Added a computed `getDisplayFiles()` method
4. Added two HTML inputs
5. Done!

The store handles all the complexity:

- Tracks what changed
- Notifies the UI
- Ensures consistency
- Makes bugs harder to introduce

---

**Next Steps:** In a Stage 5, you might add:

- Toast notifications (using the store pattern)
- Undo/redo (easy with centralized state)
- Real-time updates with WebSockets (subscribe the store to a socket)
- Offline support (persist state to localStorage)
- User authentication (add user state to store)

The store pattern scales beautifully to handle all of these features.
