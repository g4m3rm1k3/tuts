Absolutely! Since you want to go section by section in your MkDocs, let’s start with **Section 0: Environment Setup (Prerequisites)**. I’ll write it in a way that’s self-contained, detailed, and beginner-friendly, but also includes technical depth for a full-stack app developer. You can copy this directly into your MkDocs.

---

# Section 0: Environment Setup

## 0.1 Introduction

Before we write a single line of code for our PDM (Parts Data Management) system, we need a properly configured development environment. This section ensures that every tool required for full-stack development is installed, accessible, and correctly configured on your computer.

A clean environment prevents conflicts, ensures reproducibility, and sets the stage for more advanced concepts like API development, frontend integration, authentication, and version control.

---

## 0.2 Required Tools and Why

| Tool                      | Purpose                                   | Notes                                                                                                               |
| ------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Python 3.12+**          | Backend server (FastAPI)                  | Use [Python.org](https://www.python.org/downloads/) installer. Make sure `python --version` works in your terminal. |
| **Node.js 20+**           | Frontend builds and JS package management | Use [Node.js official site](https://nodejs.org). Verify with `node -v` and `npm -v`.                                |
| **VS Code**               | Code editor                               | Recommended extensions: Python, Pylance, Prettier, Live Server.                                                     |
| **Git**                   | Version control                           | Essential for managing code history and collaborating with remote GitLab. Verify with `git --version`.              |
| **GitLab account**        | Remote repository host                    | Needed to push code for backup and collaboration.                                                                   |
| **Postman / HTTP Client** | API testing                               | Optional but helpful for backend testing.                                                                           |

Optional but recommended:

- **Python Virtual Environment (`venv`)** – isolates project dependencies.
- **Prettier / ESLint** – ensures consistent JavaScript formatting.
- **Browser Developer Tools** – Chrome or Edge dev tools for debugging frontend.

---

## 0.3 Python Environment Setup

1. **Install Python 3.12+**

   - Windows: Download installer, check “Add Python to PATH.”
   - macOS: Use `brew install python@3.12` if Homebrew is installed.

2. **Verify installation**

   ```bash
   python --version
   pip --version
   ```

3. **Create a project folder**

   ```bash
   mkdir pdm-system
   cd pdm-system
   ```

4. **Set up a virtual environment**

   ```bash
   python -m venv venv
   ```

5. **Activate the environment**

   - Windows:

     ```powershell
     .\venv\Scripts\Activate.ps1
     ```

   - macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

6. **Install core Python dependencies**

   ```bash
   pip install fastapi uvicorn python-multipart pydantic bcrypt python-jose
   ```

> **Tip:** Keep your virtual environment activated whenever working on this project.

---

## 0.4 Node.js & Frontend Setup

1. **Install Node.js and npm**

   - Verify:

   ```bash
   node -v
   npm -v
   ```

2. **Create a frontend folder**

   ```bash
   mkdir frontend
   cd frontend
   npm init -y
   ```

3. **Install any future frontend dependencies** (like React, Vue, or Alpine.js) later in the tutorial.

---

## 0.5 Git & Version Control

1. **Initialize Git repository**

   ```bash
   git init
   ```

2. **Connect to GitLab**

   - Create a new repository on GitLab.
   - Add remote URL:

   ```bash
   git remote add origin git@gitlab.com:username/pdm-system.git
   ```

3. **Create a `.gitignore`**

   ```gitignore
   venv/
   __pycache__/
   *.pyc
   node_modules/
   .env
   ```

4. **First commit**

   ```bash
   git add .
   git commit -m "Initial environment setup"
   git push -u origin main
   ```

---

## 0.6 Recommended VS Code Extensions

- **Python** – for syntax highlighting, IntelliSense, and debugging.
- **Pylance** – for type-checking and autocompletion.
- **Prettier** – auto-formatting for JS, CSS, HTML.
- **Live Server** – for testing frontend HTML pages in real-time.
- **REST Client** (optional) – allows testing API endpoints from VS Code.

---

## 0.7 Environment Verification Checklist

- [ ] Python 3.12+ installed and accessible via terminal.
- [ ] Node.js 20+ installed and accessible via terminal.
- [ ] Git installed and GitLab repository connected.
- [ ] Virtual environment activated.
- [ ] VS Code extensions installed.
- [ ] Project folder structure created:

  ```
  pdm-system/
  ├── frontend/
  ├── venv/
  └── backend/ (will be created in Stage 1)
  ```

Once you complete this section, you’re ready to start **Stage 1: Core API Service**. You have all the tools installed, your environment is isolated, and Git version control ensures you can track every step of your learning journey.

---

If you want, I can draft **Section 1** next, which will walk through creating the FastAPI “Hello World” backend and your first `/api/files` endpoint, including explanations for each line of code and reinforcing CS concepts like HTTP methods, JSON, and server routing.

Perfect! Here’s **Section 1: Core API Service** designed for your MkDocs. It’s beginner-friendly but also dives deep into CS concepts while building your backend step by step.

---

# Section 1: Core API Service

## 1.0 Introduction

In this section, we will build the **backend foundation** for the PDM system using **FastAPI**. FastAPI is a modern, Python-based web framework designed for creating APIs quickly and efficiently. By the end of this section, you’ll have a live backend server with:

- A basic `GET /` endpoint returning a “Hello World” message.
- A `GET /api/files` endpoint returning a **hardcoded JSON list** of files.
- Auto-generated interactive documentation via **Swagger UI**.

We’ll also reinforce key computer science concepts: HTTP methods, routing, JSON serialization, and server-client communication.

---

## 1.1 Folder Structure

Create a `backend` folder inside your project:

```
pdm-system/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
└── venv/
```

- `main.py` – main FastAPI application.
- `requirements.txt` – records all backend Python dependencies for reproducibility.

---

## 1.2 Installing Dependencies

Ensure your virtual environment is active:

```bash
cd backend
pip install fastapi uvicorn
pip freeze > requirements.txt
```

- `fastapi` – the framework for building APIs.
- `uvicorn` – the ASGI server that runs the FastAPI app.

---

## 1.3 Writing Your First FastAPI App

Create `main.py` inside `backend`:

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="PDM System API",
    description="Backend API for Parts Data Management System",
    version="1.0.0"
)

# Allow frontend (localhost) to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    """
    Returns a simple JSON message to verify server is running.
    """
    return {"message": "Hello World from PDM Backend!"}

# Example /api/files endpoint
@app.get("/api/files")
def get_files():
    """
    Returns a hardcoded list of CNC files.
    """
    files = [
        {"id": 1, "name": "part_A.mcam", "status": "available"},
        {"id": 2, "name": "part_B.mcam", "status": "checked_out"},
        {"id": 3, "name": "part_C.mcam", "status": "available"}
    ]
    return {"files": files}
```

---

## 1.4 Running the Backend Server

From the `backend` folder:

```bash
uvicorn main:app --reload
```

- `main:app` – points to the `app` instance in `main.py`.
- `--reload` – auto-reloads the server when code changes (perfect for development).

Verify it works:

- Open your browser and navigate to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- You should see:

```json
{ "message": "Hello World from PDM Backend!" }
```

---

## 1.5 Interactive API Documentation

FastAPI automatically generates Swagger UI documentation:

- Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Try out the endpoints by clicking **Try it out** → **Execute**.

You’ll also notice **ReDoc** at [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) for an alternative API documentation style.

---

## 1.6 Key Computer Science Concepts

| Concept                                  | Explanation                                                                                                 |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **HTTP Methods**                         | `GET` retrieves data from the server. Later, we’ll use `POST`, `PUT`, `DELETE`.                             |
| **Routing**                              | The `@app.get("/path")` decorator maps a URL path to a Python function.                                     |
| **JSON Serialization**                   | Python dictionaries (`dict`) are automatically converted to JSON responses.                                 |
| **CORS (Cross-Origin Resource Sharing)** | Allows your frontend (running on a different port) to request data from the backend.                        |
| **ASGI Server**                          | Uvicorn serves as an asynchronous server capable of handling multiple simultaneous connections efficiently. |

---

## 1.7 Next Steps

With the backend live, we can now:

1. Test it using **Postman**, **curl**, or your browser.
2. Move to **Stage 2: Basic Frontend Interface**, where we will fetch this file list dynamically and render it in a web page.
3. Begin learning how backend and frontend communicate using **RESTful APIs**.

---

✅ **Checklist for Section 1**

- [ ] Backend folder created and virtual environment active.
- [ ] FastAPI and Uvicorn installed.
- [ ] `main.py` written with `/` and `/api/files` endpoints.
- [ ] Server runs and responds to browser requests.
- [ ] Swagger UI accessible and functional.

---

If you want, I can draft **Section 2: Basic Frontend Interface** next, showing how to fetch the file list from your FastAPI backend and render it dynamically in a professional-looking HTML/CSS page. This section will also introduce some JavaScript fundamentals for DOM manipulation and API calls.

Absolutely! Let’s redo **Section 2: Basic Frontend Interface** in a much more **in-depth, teaching-oriented way**, explaining _why_ we do each step, _how_ it works, and linking it to CS and software development concepts. I’ll break it down so that every line or concept has context.

---

# Section 2: Basic Frontend Interface (Deep Dive)

## 2.0 Introduction

In Section 1, we built a FastAPI backend serving JSON data. Now, we will create a **frontend** that fetches this data and displays it in a web page.

Goals:

- Reinforce **client-server communication** concepts.
- Learn **HTML structure** and why semantic tags matter.
- Understand **CSS fundamentals** for layout, styling, and readability.
- Learn **JavaScript DOM manipulation** and asynchronous requests (`fetch`, `async/await`).
- Explore software engineering principles like **separation of concerns** and **responsiveness**.

By the end of this section, you’ll have a fully functional, professional-looking frontend that dynamically shows your files.

---

## 2.1 Folder Structure Explained

Organizing your project is a **fundamental CS practice**. Clean structure helps:

- Maintainability
- Scalability
- Team collaboration

Here’s our `frontend/` folder:

```
frontend/
├── index.html      # Main HTML page
├── css/
│   └── style.css   # Styles (colors, spacing, layout)
└── js/
    └── app.js      # Behavior & logic (DOM updates, fetch API)
```

**Why this separation?**

- **HTML** → Structure. What the user sees.
- **CSS** → Style. How it looks.
- **JavaScript** → Behavior. How it behaves.

This is the **Separation of Concerns**, a core software engineering principle: each layer has a single responsibility.

---

## 2.2 HTML – Structure and Semantics

HTML is the skeleton of your webpage. Using **semantic tags** helps:

- Accessibility (screen readers, assistive tech)
- Search engines (SEO)
- Readability for other developers

Here’s `index.html` with explanations:

```html
<!DOCTYPE html>
<html lang="en">
  <!-- 'lang' helps browsers and accessibility tools -->
  <head>
    <meta charset="UTF-8" />
    <!-- Encoding for characters -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PDM System - Files</title>
    <link rel="stylesheet" href="css/style.css" />
    <!-- Link to CSS -->
  </head>
  <body>
    <header>
      <h1>PDM System</h1>
      <!-- Main heading -->
      <p>Manage CNC program files efficiently</p>
    </header>

    <main>
      <section id="file-list-section">
        <h2>Available Files</h2>
        <!-- Subheading for the section -->
        <ul id="file-list">
          <!-- JavaScript will dynamically insert <li> items here -->
        </ul>
      </section>
    </main>

    <footer>
      <p>&copy; 2025 PDM System</p>
    </footer>

    <script src="js/app.js"></script>
    <!-- Load JS at the end for faster page load -->
  </body>
</html>
```

**Key points:**

- `<header>` – top of the page, usually branding and navigation.
- `<main>` – main content; only one `<main>` per page.
- `<section>` – groups related content (our file list).
- `<ul>` – unordered list, ideal for lists of items.
- `<footer>` – bottom content like copyright.
- `<script>` at the bottom – ensures HTML loads first before JS runs (avoids errors accessing DOM elements).

---

## 2.3 CSS – Styling and Layout (With Explanation)

CSS controls **look and feel**. Beyond just “making it pretty,” CSS is about **usability, readability, and visual hierarchy**, which are software design concerns.

Here’s `style.css`:

```css
/* Reset default browser styles for consistency */
body {
  font-family: Arial, sans-serif; /* Readable sans-serif font */
  margin: 0; /* Remove default body margin */
  padding: 0; /* Remove default body padding */
  background-color: #f5f5f5; /* Soft light background */
  color: #333; /* Dark text for contrast */
}

/* Header design */
header {
  background-color: #1e3a8a; /* Dark blue for branding */
  color: white; /* Text contrast for readability */
  padding: 1rem; /* Space inside header */
  text-align: center; /* Centered content */
}

/* Main content spacing */
main {
  padding: 2rem; /* Adds whitespace around content */
}

/* Section headings */
h2 {
  margin-bottom: 1rem; /* Space below heading */
}

/* File list container */
ul#file-list {
  list-style-type: none; /* Remove bullets for custom styling */
  padding: 0; /* Remove default padding */
}

/* Individual file items */
ul#file-list li {
  background-color: white; /* Card-like look */
  margin-bottom: 0.5rem; /* Spacing between cards */
  padding: 1rem; /* Inner spacing */
  border-radius: 6px; /* Rounded corners */
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
}
```

**Software development insights:**

- **Whitespace and margins** improve readability and hierarchy.
- **Box shadows** and rounded corners improve UX (users can visually separate items).
- **Semantic styling**: classes and IDs make it easy to select elements in JS.

> CSS isn’t just design; it’s part of user-facing **software engineering**. You’re coding user experience.

---

## 2.4 JavaScript – Fetching and Rendering Data

JavaScript allows **dynamic behavior**. Let’s build `app.js` step by step:

```javascript
// API endpoint (backend)
const API_URL = "http://127.0.0.1:8000/api/files";

// DOM reference: where files will appear
const fileList = document.getElementById("file-list");

// Async function: fetch files from backend
async function fetchFiles() {
  try {
    // Network request
    const response = await fetch(API_URL);

    // Error handling for failed requests
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Convert JSON response to JS object
    const data = await response.json();

    // Render files dynamically
    renderFiles(data.files);
  } catch (error) {
    console.error("Failed to fetch files:", error);
    fileList.innerHTML =
      "<li>Error loading files. Please try again later.</li>";
  }
}

// Create HTML elements for each file
function renderFiles(files) {
  fileList.innerHTML = ""; // Clear existing content

  files.forEach((file) => {
    const li = document.createElement("li"); // Create <li>
    li.textContent = `${file.name} - ${file.status}`; // Set text
    fileList.appendChild(li); // Add to DOM
  });
}

// Load files when page loads
fetchFiles();
```

**Concepts reinforced:**

- **DOM Manipulation** – `createElement`, `appendChild`, `innerHTML`.
- **Asynchronous Programming** – `async/await` for network calls.
- **Error Handling** – Prevents app from breaking on failed network requests.
- **Client-Server Communication** – REST API call and JSON parsing.
- **Single Responsibility Principle** – `fetchFiles()` fetches data, `renderFiles()` renders data. Each function has one task.

---

## 2.5 Running the Frontend

1. Open `index.html` with **VS Code Live Server** for local development.
2. Ensure your **backend FastAPI server** is running on `http://127.0.0.1:8000/`.
3. Your file list should display dynamically, styled as cards.

> If files don’t load, check the browser console for CORS errors. The FastAPI CORS middleware from Section 1 ensures communication between frontend (port 5500) and backend (port 8000).

---

## 2.6 Software Engineering Lessons

- **Separation of Concerns** – keeps HTML, CSS, JS separate.
- **Dynamic vs Static Content** – dynamic data comes from backend, static layout comes from HTML/CSS.
- **Error handling and resilience** – always anticipate network failures.
- **UX principles** – readable fonts, spacing, and visual hierarchy improve usability.
- **Code maintainability** – clean folder structure and naming conventions.

---

## 2.7 Next Steps

After this section, your frontend **fully communicates with the backend**. Next, in **Section 3**, we will:

- Replace hardcoded file status with **real files from the server**.
- Implement **file check-in/check-out logic**.
- Introduce **stateful interactions** in the frontend.
- Teach **backend file operations** and **persistent state management**.

---

✅ **Section 2 Checklist (Deep Learning)**

- [ ] HTML page created with semantic tags.
- [ ] CSS applied for layout, typography, spacing, and readability.
- [ ] JavaScript fetches backend API dynamically.
- [ ] DOM updates dynamically to show real data.
- [ ] Concepts like async/await, DOM manipulation, and separation of concerns are understood.
- [ ] Frontend and backend communicate correctly without CORS issues.
- [ ] Page visually clear, readable, and user-friendly.

---

If you want, I can now write **Section 3: Core PDM Logic – File Locking** with the same **in-depth teaching approach**, explaining **how file locking works, backend state, and dynamic frontend updates**, step by step.

Awesome! Let’s dive into **Section 3: Core PDM Logic – File Locking** with the same in-depth teaching approach. This is where the backend starts handling **real files**, and the frontend begins to **reflect the state of the system dynamically**. We’ll also explore software engineering principles like **state management, concurrency, and persistence**.

---

# Section 3: Core PDM Logic – File Locking

## 3.0 Introduction

In Section 2, we displayed a **hardcoded list** of files. In a real PDM system, the backend must **track file state** (available, checked out, locked) and **persist that state** across server restarts.

Goals:

- Read **real `.mcam` files** from a folder.
- Implement **checkout/check-in logic**.
- Display **file status dynamically** on the frontend.
- Learn **state management**, **persistence**, and **frontend-backend integration**.

---

## 3.1 Understanding File Locking

### What is File Locking?

File locking is a **concurrency control mechanism** that prevents multiple users from modifying a file simultaneously.

**Key concepts:**

- **Exclusive lock** – only one user can edit the file at a time.
- **Lock metadata** – store information like `username` and `timestamp` to know who locked it.
- **Persistent locks** – locks survive server restarts by storing them in a file or database.

> In our system, each file has a `status` (`available` or `checked_out`) and a `locked_by` field to indicate who has it.

---

## 3.2 Folder Structure Update

```
backend/
├── main.py
├── requirements.txt
├── files/           # Actual .mcam files live here
│   ├── part_A.mcam
│   ├── part_B.mcam
│   └── part_C.mcam
└── locks.json       # Persistent lock state
```

- `files/` – contains the real CNC program files.
- `locks.json` – JSON file storing which files are locked and by whom. This is our **persistent state**.

---

## 3.3 Backend – Reading Files and Managing Locks

Update `main.py`:

```python
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

FILES_DIR = "files"
LOCKS_FILE = "locks.json"

app = FastAPI(
    title="PDM System API",
    description="Backend API for Parts Data Management System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load or initialize locks
if os.path.exists(LOCKS_FILE):
    with open(LOCKS_FILE, "r") as f:
        locks = json.load(f)
else:
    locks = {}  # e.g., {"part_A.mcam": {"status": "checked_out", "locked_by": "John"}}

# Helper function to save locks
def save_locks():
    with open(LOCKS_FILE, "w") as f:
        json.dump(locks, f, indent=4)

# Get list of files with status
@app.get("/api/files")
def get_files():
    files = []
    for filename in os.listdir(FILES_DIR):
        if filename.endswith(".mcam"):
            lock_info = locks.get(filename, {})
            status = lock_info.get("status", "available")
            locked_by = lock_info.get("locked_by", None)
            files.append({"name": filename, "status": status, "locked_by": locked_by})
    return {"files": files}

# Checkout a file
@app.post("/api/files/checkout/{filename}")
def checkout_file(filename: str, username: str):
    if filename not in os.listdir(FILES_DIR):
        raise HTTPException(status_code=404, detail="File not found")
    if locks.get(filename, {}).get("status") == "checked_out":
        raise HTTPException(status_code=400, detail="File already checked out")
    locks[filename] = {"status": "checked_out", "locked_by": username}
    save_locks()
    return {"message": f"{filename} checked out by {username}"}

# Checkin a file
@app.post("/api/files/checkin/{filename}")
def checkin_file(filename: str, username: str):
    if filename not in os.listdir(FILES_DIR):
        raise HTTPException(status_code=404, detail="File not found")
    lock_info = locks.get(filename)
    if not lock_info or lock_info.get("locked_by") != username:
        raise HTTPException(status_code=400, detail="You do not hold the lock for this file")
    locks[filename] = {"status": "available", "locked_by": None}
    save_locks()
    return {"message": f"{filename} checked in by {username}"}
```

### Key Concepts:

- **Persistent state** – `locks.json` ensures the system remembers locks even after a server restart.
- **Error handling** – `HTTPException` returns proper HTTP status codes for frontend to handle.
- **Idempotence** – Checkout and check-in operations ensure consistent state.

---

## 3.4 Frontend – Adding Checkout/Check-in Buttons

Update `js/app.js`:

```javascript
function renderFiles(files) {
  fileList.innerHTML = ""; // Clear previous list

  files.forEach((file) => {
    const li = document.createElement("li");
    li.textContent = `${file.name} - ${file.status}`;

    // Add Checkout button if file is available
    if (file.status === "available") {
      const btn = document.createElement("button");
      btn.textContent = "Checkout";
      btn.onclick = () => checkoutFile(file.name);
      li.appendChild(btn);
    }

    // Add Checkin button if file is checked out by current user
    if (file.status === "checked_out" && file.locked_by === "Michael") {
      const btn = document.createElement("button");
      btn.textContent = "Checkin";
      btn.onclick = () => checkinFile(file.name);
      li.appendChild(btn);
    }

    fileList.appendChild(li);
  });
}

async function checkoutFile(filename) {
  const response = await fetch(
    `http://127.0.0.1:8000/api/files/checkout/${filename}?username=Michael`,
    { method: "POST" }
  );
  if (response.ok) fetchFiles(); // Refresh list
  else console.error(await response.json());
}

async function checkinFile(filename) {
  const response = await fetch(
    `http://127.0.0.1:8000/api/files/checkin/${filename}?username=Michael`,
    { method: "POST" }
  );
  if (response.ok) fetchFiles(); // Refresh list
  else console.error(await response.json());
}
```

### Key Concepts:

- **Dynamic buttons** – buttons only appear when action is allowed.
- **Frontend-Backend sync** – clicking buttons sends POST requests to update state.
- **Current user tracking** – hardcoded here for simplicity; later we will integrate authentication.

---

## 3.5 Computer Science Principles Reinforced

| Concept                             | Explanation                                                                |
| ----------------------------------- | -------------------------------------------------------------------------- |
| **State Management**                | `locks.json` stores persistent state across server restarts.               |
| **Concurrency Control**             | Prevent multiple users from editing a file at the same time.               |
| **Idempotence & Atomic Operations** | Checkout/check-in either fully succeeds or fails without corrupting state. |
| **Client-Server Communication**     | Frontend calls backend endpoints and reflects real-time state.             |
| **Error Handling & Feedback**       | Frontend handles HTTP errors gracefully.                                   |

---

## 3.6 Next Steps

- Add **user authentication** so that `username` isn’t hardcoded (Section 5).
- Implement **real-time updates** using WebSockets (Section 9).
- Enhance **UI/UX** with styled buttons, modal confirmations, and error messages (Section 4).

---

✅ **Section 3 Checklist**

- [ ] Backend reads real `.mcam` files from `files/`.
- [ ] Locks are persisted in `locks.json`.
- [ ] Checkout/check-in endpoints implemented with proper error handling.
- [ ] Frontend displays buttons dynamically based on file status.
- [ ] Clicking buttons updates backend state and refreshes frontend list.
- [ ] Concepts like concurrency, state management, and persistent storage understood.

---

Section 3 is a **major step**: the app is now **functional**, not just displaying static data. You’re learning real-world concepts like **locks, state, and persistence**.

---

I can write **Section 4 next: Frontend Enhancements & UX** with deep explanation about **CSS for modals, responsive design, spinners, toast notifications**, and **UX principles in software engineering**.

Absolutely! Let’s redo **Section 4** with the same **in-depth code walkthrough, comments, and deep explanations** we did in Section 3. I’ll make sure every piece of code has an explanation about **what it does, why it’s written that way, and best practices behind it**—so you’ll really understand the _how_ and _why_ behind every decision.

---

# Section 4: Frontend Enhancements & UX (Detailed Version)

## 4.0 Introduction

Now that our frontend can display files and handle checkout/check-in, it’s **functional but not polished**. Users need:

- **Visual feedback** when actions are happening.
- **Intuitive UI controls** instead of browser `alert()` or `prompt()`.
- **Efficient ways to find files** in a potentially large repository.
- **Non-blocking notifications** for success or error.

This section focuses on **improving the interface and user experience** while reinforcing software engineering and computer science principles like **separation of concerns, event-driven programming, and responsiveness**.

---

## 4.1 Folder Structure Update

We reorganize frontend files for clarity:

```
frontend/
├── index.html
├── css/
│   ├── style.css       # Base styles
│   └── modals.css      # Styles for modals, toast, and spinners
└── js/
    ├── app.js          # API calls, main app logic
    └── ui.js           # UI/UX logic (modals, toast, filters)
```

**Why:** Separating **API logic** from **UI logic** enforces **modularity**, a key software engineering principle. This makes your code **more maintainable, readable, and testable**.

---

## 4.2 Custom Modals

Native `alert()` and `prompt()` are blocking and unstyled. We replace them with **custom modals**.

### 4.2.1 HTML Structure

```html
<!-- Modal overlay -->
<div id="modal-overlay" class="hidden">
  <div id="modal-content">
    <!-- Message displayed dynamically via JS -->
    <p id="modal-message"></p>
    <!-- Close button for the user -->
    <button id="modal-close">Close</button>
  </div>
</div>
```

**Explanation:**

- `modal-overlay` – semi-transparent background that covers the whole screen. It **focuses attention** on the modal and prevents interaction with other UI elements.
- `modal-content` – the box that contains the message and buttons. Centered and styled for readability.
- `hidden` class – initially hides the modal. We toggle it with JavaScript.

> **Software Engineering Principle:** Modals are **reusable components**. The logic for showing/hiding them should be isolated from API calls.

---

### 4.2.2 CSS Styling (`modals.css`)

```css
.hidden {
  display: none;
} /* Utility class to hide elements */

#modal-overlay {
  position: fixed; /* Stays in place even when scrolling */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  display: flex; /* Flexbox centers content */
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Ensures it appears above other elements */
}

#modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px; /* Rounded corners for modern look */
  max-width: 400px;
  width: 80%;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Subtle shadow */
}

#modal-close {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  border: none;
  background-color: #1e3a8a;
  color: white;
  border-radius: 4px;
  font-weight: bold;
  transition: background-color 0.3s;
}

#modal-close:hover {
  background-color: #3b82f6; /* Hover effect improves interactivity */
}
```

**Key concepts explained:**

- **Flexbox** – used for centering modal vertically and horizontally without complex CSS hacks.
- **Z-index** – ensures the modal sits above all other page elements.
- **Transitions & hover effects** – improve perceived responsiveness and polish.

---

### 4.2.3 JavaScript Logic (`ui.js`)

```javascript
// Grab modal elements from DOM
const modalOverlay = document.getElementById("modal-overlay");
const modalMessage = document.getElementById("modal-message");
const modalClose = document.getElementById("modal-close");

// Function to show modal with a custom message
function showModal(message) {
  modalMessage.textContent = message; // Update the text dynamically
  modalOverlay.classList.remove("hidden"); // Show modal
}

// Close modal when the button is clicked
modalClose.onclick = () => modalOverlay.classList.add("hidden");
```

**Explanation of “why this works”:**

- `textContent` – dynamically updates the modal content based on the event.
- `classList.remove("hidden")` – toggles visibility. Using classes instead of inline styles is cleaner and easier to maintain.
- Encapsulation – modal logic is isolated, so we can call `showModal("File checked out!")` from anywhere in the app without touching the API code.

> **Principle reinforced:** **Separation of concerns**. Modals are decoupled from API logic.

---

## 4.3 Loading Indicators (Spinners)

Users should know when async operations (like fetching files or checking in/out) are happening.

### 4.3.1 HTML

```html
<div id="spinner" class="hidden">Loading...</div>
```

### 4.3.2 CSS

```css
#spinner {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* Center on screen */
  font-size: 1.5rem;
  color: #1e3a8a;
  font-weight: bold;
}
```

### 4.3.3 JS Logic

```javascript
function showSpinner() {
  document.getElementById("spinner").classList.remove("hidden");
}

function hideSpinner() {
  document.getElementById("spinner").classList.add("hidden");
}

// Example: wrapping API calls
async function fetchFilesWithSpinner() {
  showSpinner(); // Show spinner before async operation
  await fetchFiles(); // Call API (from app.js)
  hideSpinner(); // Hide spinner when done
}
```

**Why this matters:**

- Provides **immediate feedback**, reducing uncertainty.
- Prevents users from clicking multiple times and potentially breaking the workflow.
- Reinforces **event-driven programming** – UI reacts to state changes.

---

## 4.4 Toast Notifications

Non-blocking messages (e.g., “File checked out successfully”) improve **usability** compared to modals, which block interaction.

### 4.4.1 HTML

```html
<div id="toast-container"></div>
```

### 4.4.2 CSS

```css
#toast-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 1001;
}

.toast {
  background-color: #1e3a8a;
  color: white;
  padding: 0.5rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: 4px;
  opacity: 0.9;
  transition: opacity 0.5s; /* Fade out smoothly */
}
```

### 4.4.3 JS Logic

```javascript
function showToast(message) {
  const container = document.getElementById("toast-container");

  // Create a new toast element
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  container.appendChild(toast);

  // Auto-remove after 3 seconds with fade effect
  setTimeout(() => {
    toast.style.opacity = "0"; // Start fade
    setTimeout(() => container.removeChild(toast), 500); // Remove after fade
  }, 3000);
}
```

**Why this works:**

- Toasts are **non-blocking**, letting users continue interacting.
- CSS transitions improve **perceived responsiveness**.
- Adding/removing DOM elements dynamically reinforces **DOM manipulation principles**.

---

## 4.5 Real-Time Filtering/Search

Large repositories need **quick access** to files.

### 4.5.1 HTML Input

```html
<input type="text" id="search-input" placeholder="Search files..." />
<ul id="file-list"></ul>
```

### 4.5.2 JS Filter Logic (`ui.js`)

```javascript
document.getElementById("search-input").addEventListener("input", (e) => {
  const query = e.target.value.toLowerCase(); // Normalize search

  // Loop through all list items and hide/show based on query
  document.querySelectorAll("#file-list li").forEach((li) => {
    li.style.display = li.textContent.toLowerCase().includes(query)
      ? ""
      : "none";
  });
});
```

**Explanation:**

- Event-driven – filters on every keystroke.
- Simple but effective – ideal for hundreds of items.
- **Scalability note:** For thousands of items, consider **virtualized lists** to improve performance.

---

## 4.6 UX Principles Applied

| Principle                  | Application in Our App                | Why It Matters                                    |
| -------------------------- | ------------------------------------- | ------------------------------------------------- |
| **Feedback**               | Spinners & toasts                     | User knows operations are happening and completed |
| **Non-blocking UI**        | Toast notifications instead of modals | Users can continue work without interruptions     |
| **Consistency**            | Styled modals, buttons, inputs        | Improves learnability and reduces errors          |
| **Accessibility**          | Text contrast, hover states           | Ensures users can read/interact easily            |
| **Separation of concerns** | `ui.js` vs `app.js`                   | Makes code maintainable and testable              |

---

## 4.7 Next Steps

- **Section 5: Authentication** – add user login, hashed passwords, and JWT tokens.
- Remove **hardcoded usernames** in check-in/check-out.
- Secure endpoints based on user identity.

---

✅ **Section 4 Checklist**

- [ ] Custom modals implemented and reusable.
- [ ] Loading spinners added for async feedback.
- [ ] Toast notifications for non-blocking messages.
- [ ] Search input filters file list in real-time.
- [ ] UI logic separated into `ui.js`, API logic in `app.js`.
- [ ] UX principles like feedback, accessibility, and consistency applied.
- [ ] All code explained in **deep detail**, including CSS, JS, and DOM manipulation.

---

Section 4 transforms our **barebones frontend** into a **user-friendly, polished interface**, while teaching **advanced frontend engineering concepts** like **DOM manipulation, CSS styling, UX feedback patterns, and modular code organization**.

---

I can now prepare **Section 5: Authentication** in the same **highly detailed, teaching-focused style**, covering **login forms, password hashing, JWT, and securing API endpoints**.

Absolutely! Let’s dive deep into **Section 5: Authentication** with the same level of detail as Sections 3 and 4. This section will cover **why authentication is necessary, how to implement it securely, and best practices in both backend and frontend**.

---

# Section 5: Authentication

## 5.0 Introduction

Authentication is the process of **verifying the identity of a user**. In our PDM system, authentication is essential to:

- Ensure **only authorized users** can check files in or out.
- Track **which user performed an action**, which is critical for audit logs.
- Provide a foundation for **role-based access control** in Section 6.

We will implement **username/password login**, secure **password storage**, and **JWT-based session management**.

> Concept reinforcement: Security is a **core software engineering principle**. Without proper authentication, all other features (file locking, version control) are vulnerable.

---

## 5.1 Backend: User Authentication

### 5.1.1 User Data Structure

We need a simple user table (could be a JSON file or database for now). For demonstration:

```python
# users.py
from passlib.hash import bcrypt

# Example users (passwords are hashed)
users = {
    "alice": {
        "username": "alice",
        "password_hash": bcrypt.hash("alicepassword"),
        "role": "admin"
    },
    "bob": {
        "username": "bob",
        "password_hash": bcrypt.hash("bobpassword"),
        "role": "user"
    }
}
```

**Explanation:**

- `bcrypt.hash()` – hashes passwords using a **modern, secure algorithm**. Never store plain text passwords.
- Each user has a **role**, which will be used in Section 6 for authorization.
- `users` dictionary simulates a **user database**.

**Software engineering principle:** Separation of **authentication data** from other application data (like files or locks) makes the system **modular and secure**.

---

### 5.1.2 FastAPI Login Endpoint

We create a `/login` route to authenticate users:

```python
# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
from users import users
from passlib.hash import bcrypt
from datetime import datetime, timedelta

SECRET_KEY = "supersecretkey"  # In production, use environment variable
ALGORITHM = "HS256"

app = FastAPI()

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_methods=["*"],
    allow_headers=["*"]
)

# Pydantic model to validate login data
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    user = users.get(request.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Verify password using bcrypt
    if not bcrypt.verify(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate JWT token
    payload = {
        "sub": user["username"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
```

**Line-by-line explanation:**

1. **`LoginRequest(BaseModel)`** – ensures the request contains `username` and `password`. FastAPI automatically validates input, preventing malformed requests.
2. **`user = users.get(request.username)`** – fetches user info from our dictionary.
3. **`bcrypt.verify(...)`** – compares the plaintext password against the stored hash. This prevents exposing sensitive data.
4. **JWT generation**:

   - `sub` → subject, the username of the user.
   - `role` → included to simplify role-based access control later.
   - `exp` → token expiration, prevents indefinite access.

5. **Return value** – sends a JSON object containing the token and its type. The frontend stores and uses it for subsequent API calls.

> **Security principle:** Never send the password back to the client or store it unencrypted.

---

### 5.1.3 Securing Endpoints with JWT

We protect API routes using JWT:

```python
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()  # FastAPI utility for Authorization header

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # contains username and role
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Example protected endpoint
@app.get("/api/files")
def get_files(current_user=Depends(get_current_user)):
    return {"user": current_user, "files": ["file1.mcam", "file2.mcam"]}
```

**Explanation:**

- `Depends(security)` – FastAPI injects the `Authorization` header automatically.
- `jwt.decode()` – verifies the token’s **signature and expiration**.
- Any endpoint using `current_user=Depends(get_current_user)` now requires authentication.

> **Software engineering principle:** Protect your backend logic by **validating every request**, not just relying on frontend logic.

---

## 5.2 Frontend: Login Form

### 5.2.1 HTML

```html
<div id="login-container">
  <h2>Login</h2>
  <form id="login-form">
    <input type="text" id="username" placeholder="Username" required />
    <input type="password" id="password" placeholder="Password" required />
    <button type="submit">Login</button>
  </form>
</div>
```

**Explanation:**

- `required` attributes enforce **client-side validation**.
- Using a `<form>` allows pressing “Enter” to submit.
- We will **intercept the submit event** with JavaScript to call our backend API.

---

### 5.2.2 CSS Styling (`style.css`)

```css
#login-container {
  max-width: 400px;
  margin: 5rem auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: #f9f9f9;
  text-align: center;
}

#login-container input {
  display: block;
  width: 80%;
  margin: 1rem auto;
  padding: 0.5rem;
  font-size: 1rem;
}

#login-container button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #1e3a8a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

#login-container button:hover {
  background-color: #3b82f6;
}
```

**Why this works:**

- The form is centered and readable.
- Inputs and buttons have **visual affordances**, making it obvious how to interact.
- Hover effect provides **feedback on interactivity**.

---

### 5.2.3 JS Logic (`ui.js`)

```javascript
const loginForm = document.getElementById("login-form");

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault(); // Prevent default form submission (page reload)

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    showSpinner(); // Show loading spinner
    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    hideSpinner();

    if (!response.ok) {
      const data = await response.json();
      showModal(data.detail || "Login failed");
      return;
    }

    const data = await response.json();
    // Store JWT in localStorage for subsequent API calls
    localStorage.setItem("token", data.access_token);
    showToast("Login successful!");
    loadMainApp(); // Function to load the main UI
  } catch (err) {
    hideSpinner();
    showModal("Network error, please try again.");
  }
});
```

**Detailed explanation:**

- `e.preventDefault()` – stops the default form behavior; allows JS handling.
- `fetch()` – calls the backend `/login` endpoint.
- `showSpinner()` / `hideSpinner()` – gives visual feedback.
- `response.ok` – checks HTTP status; if not 2xx, shows an error modal.
- `localStorage.setItem("token", ...)` – stores the JWT for **session persistence**.
- `loadMainApp()` – hides the login form and shows the main PDM UI.
- Errors are caught and displayed to the user using modals for **clear feedback**.

---

## 5.3 Securing API Calls on the Frontend

Whenever we call protected endpoints, we must send the JWT:

```javascript
async function fetchFiles() {
  const token = localStorage.getItem("token");

  const response = await fetch("http://localhost:8000/api/files", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    showModal("Session expired or unauthorized");
    return;
  }

  const data = await response.json();
  renderFileList(data.files); // Render files dynamically
}
```

**Explanation:**

- Every request includes the **Authorization header**.
- Backend verifies the token before serving data.
- If token is invalid or expired, we **inform the user** and require re-login.

---

## 5.4 Security Best Practices Reinforced

| Concept                            | Why It Matters                                                  |
| ---------------------------------- | --------------------------------------------------------------- |
| **Password hashing**               | Protects users in case of database leaks.                       |
| **JWT**                            | Stateless session management, no server-side sessions required. |
| **Token expiration**               | Limits risk of stolen token misuse.                             |
| **CORS configuration**             | Allows safe cross-origin requests for frontend dev.             |
| **Separation of frontend/backend** | Keeps authentication logic isolated, easier to maintain.        |

---

## 5.5 Next Steps

- Section 6 will cover **Authorization (Role-Based Access Control)**:

  - Admin vs user permissions.
  - UI adapts based on role.
  - Secure endpoints for critical actions (delete, force check-in).

---

✅ **Section 5 Checklist**

- [ ] Backend `/login` endpoint implemented with hashed passwords.
- [ ] JWT token generated on successful login.
- [ ] Protected API endpoints verify JWT and reject unauthorized requests.
- [ ] Frontend login form implemented with proper styling.
- [ ] JS handles login, shows spinner, toast, or modal for feedback.
- [ ] JWT stored in localStorage and sent with all protected API calls.
- [ ] Clear understanding of security best practices reinforced.

---

**Summary:**
Section 5 introduces **secure user authentication**, bridging the gap between a functional frontend and a secure system. It reinforces **software engineering principles**, **security practices**, and **real-world application of JWTs**.

---

I can now prepare **Section 6: Authorization & Role-Based Access Control** in the same depth, teaching **how to implement roles and enforce permissions securely**.

Perfect! Section 7 is where we take our PDM system **from simple file management to full Git-based version control**, which is a crucial part of professional software engineering. I’ll go into **deep explanation, line-by-line comments, best practices, and why we do each step**.

---

No problem! Let’s go **back to Section 6: Authorization (Role-Based Access Control – RBAC)** and go **full depth** with explanations, comments, and the “why” behind each decision. This is crucial for making the PDM system **secure and professionally structured**.

---

# Section 6: Authorization (RBAC – Role-Based Access Control)

## 6.0 Introduction

So far, we have:

- **Authentication** – users can log in and obtain a JWT.
- **File management** – users can check files in/out.

But anyone with a valid login could potentially **delete files, override locks, or access admin-only actions**.

We need **Role-Based Access Control (RBAC)**:

- **RBAC** restricts actions based on a user’s role (e.g., `admin` or `user`).
- **Principle:** Least privilege – users should only have **permissions necessary for their job**.
- Typical roles for our PDM system:

| Role    | Permissions                                                       |
| ------- | ----------------------------------------------------------------- |
| `user`  | Checkout/check-in files, view file list, see history              |
| `admin` | All `user` actions + delete files, override locks, view audit log |

---

## 6.1 User Roles Model

Let’s define **roles and users** in Python.

```python
# models.py
from pydantic import BaseModel
from typing import Literal

Role = Literal["admin", "user"]

class User(BaseModel):
    username: str
    password_hash: str
    role: Role
```

**Explanation:**

- `Literal["admin","user"]` ensures **role values are validated at type level**.
- `password_hash` ensures **we never store plain-text passwords**, a security best practice.
- Using Pydantic’s `BaseModel` allows **easy validation for API requests**.

---

### 6.1.1 Sample User Database (for testing)

```python
# fake_users_db.py
from passlib.context import CryptContext
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db = {
    "alice": User(username="alice", password_hash=pwd_context.hash("alice123"), role="admin"),
    "bob": User(username="bob", password_hash=pwd_context.hash("bob123"), role="user")
}
```

**Explanation:**

- `passlib` handles **bcrypt hashing** securely.
- Each user has a **role** attached.
- Even in a small app, this **simulates production**-style user management.

---

## 6.2 Securing API Endpoints

We need **middleware or decorators** to enforce role-based permissions.

```python
# dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Callable
from models import User
from fake_users_db import users_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Decode JWT token to retrieve the current user.
    """
    # Simplified example; in production, use proper JWT decoding
    username = token  # Here token is just username for demo
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

def require_role(role: str):
    """
    Dependency to enforce a minimum role for API endpoints.
    """
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden: insufficient privileges")
        return current_user
    return role_checker
```

**Line-by-line explanation:**

- `get_current_user` – extracts user info from token. In production, decode JWT properly.
- `require_role(role)` – returns a **dependency function** to enforce role access.
- If a user doesn’t have the role, raise `403 Forbidden`.
- This **keeps authorization logic modular** and reusable across multiple endpoints.

> **Software principle:** **Separation of concerns** – authentication vs authorization.
> Authentication → “Who are you?”
> Authorization → “What are you allowed to do?”

---

## 6.3 Protecting Admin Actions

Example: Delete a file (admin-only)

```python
# main.py
from fastapi import FastAPI, Depends
from pathlib import Path
from dependencies import require_role

app = FastAPI()

REPO_PATH = Path("pdm_repo")

@app.delete("/files/{filename}")
def delete_file(filename: str, current_user = Depends(require_role("admin"))):
    file_path = REPO_PATH / filename
    if file_path.exists():
        file_path.unlink()  # Delete file
        return {"status": "success", "message": f"{filename} deleted by {current_user.username}"}
    return {"status": "error", "message": "File does not exist"}
```

**Explanation:**

- `Depends(require_role("admin"))` ensures **only admins can reach this function**.
- `unlink()` deletes the file – simple Python file deletion.
- Backend **returns structured JSON** for the frontend to handle messages and notifications.

> **Best practice:** Always **check permissions in the backend**, never rely on frontend UI hiding buttons.

---

## 6.4 Conditional Frontend UI

We also reflect roles in the frontend:

```javascript
function renderFileActions(file, currentUserRole, fileOwner) {
  const container = document.createElement("div");

  // Everyone can checkout/checkin
  const checkoutBtn = document.createElement("button");
  checkoutBtn.innerText = "Checkout";
  container.appendChild(checkoutBtn);

  const checkinBtn = document.createElement("button");
  checkinBtn.innerText = "Checkin";
  checkinBtn.disabled = fileOwner !== currentUser;
  container.appendChild(checkinBtn);

  // Admin-only actions
  if (currentUserRole === "admin") {
    const deleteBtn = document.createElement("button");
    deleteBtn.innerText = "Delete";
    deleteBtn.onclick = () => deleteFile(file.name);
    container.appendChild(deleteBtn);
  }

  return container;
}
```

**Explanation:**

- `currentUserRole` – retrieved from JWT.
- Only **admin users see the Delete button**.
- Ensures **UI matches backend authorization**, improving **usability and security**.

> **Security principle:** UI is only for convenience; backend authorization is the **source of truth**.

---

## 6.5 Auditing Sensitive Actions

Admins can override locks or delete files, so we maintain an **audit log**:

```python
# audit.py
from datetime import datetime
audit_log = []

def log_action(user: str, action: str, target: str):
    audit_log.append({
        "user": user,
        "action": action,
        "target": target,
        "timestamp": datetime.now().isoformat()
    })
```

**Usage example:**

```python
log_action(current_user.username, "delete_file", filename)
```

**Explanation:**

- Records **who did what and when**.
- Essential for **traceability and accountability** in professional systems.
- Can later be stored in database or Git for persistence.

---

## 6.6 Key Software Engineering Concepts

| Concept                       | Application in RBAC                                   |
| ----------------------------- | ----------------------------------------------------- |
| **Least Privilege**           | Users only have permissions necessary for their role. |
| **Separation of Concerns**    | Authentication vs Authorization handled separately.   |
| **Backend-Enforced Security** | Never trust frontend for critical actions.            |
| **Modularity**                | Dependencies allow easy reuse of role checks.         |
| **Auditability**              | Every sensitive action can be logged for compliance.  |

---

## 6.7 Next Steps

- Section 7 will integrate **Git version control**, so even admin actions like file deletion or force check-in are **tracked in Git history**.
- Section 8 will combine **RBAC with real-time updates**, e.g., only admins can override locks and broadcast changes.

---

✅ **Section 6 Checklist**

- [ ] Users assigned roles (`user` vs `admin`).
- [ ] Backend endpoints secured with `require_role`.
- [ ] Admin-only actions protected (`delete`, `override locks`).
- [ ] Frontend UI dynamically reflects user role.
- [ ] Audit logging implemented for sensitive actions.
- [ ] Principles of least privilege, modularity, separation of concerns applied.

---

**Summary:**
Section 6 implements **Role-Based Access Control**, enforcing **who can do what** in the system. Combined with authentication, this makes the PDM system **secure, professional, and compliant with best practices**. RBAC also lays the foundation for **auditability and enterprise-grade features** in later sections.

---

If you want, I can now **redo Sections 7 and 8 with RBAC integrated**, so every Git operation and WebSocket event respects **user roles**, keeping the same level of **full depth and explanation**.

Do you want me to do that next?

# Section 7: Git Integration & Advanced Version Control

## 7.0 Introduction

At this point, our system handles:

- Files in the filesystem
- Check-in/check-out locking
- User authentication

But **real-world version control requires**:

- Tracking **all changes** to files over time
- Knowing **who made a change and why**
- Being able to **revert, compare, or retrieve previous versions**
- **Collaborating** with multiple users safely

**Git integration solves these problems**. Git is:

- A **distributed version control system**
- Designed for **tracking changes line-by-line**
- Widely used in industry
- Perfect for managing CNC program files (`.mcam`) with **history and branching support**

We’ll integrate Git programmatically using **Python’s `GitPython` library**, so our PDM app can commit, push, and pull files automatically.

---

## 7.1 Install Git and GitPython

**System prerequisite:**

```bash
# Make sure Git is installed
git --version

# Install GitPython in your virtual environment
pip install GitPython
```

**Why GitPython:** Allows us to **manipulate Git repositories from Python** without shell commands. Safer and easier to integrate into a backend API.

---

## 7.2 Initialize a Git Repository

```python
# git_repo.py
from git import Repo
from pathlib import Path

REPO_PATH = Path("pdm_repo")  # Directory to store files

# Initialize repo if not exists
if not REPO_PATH.exists():
    REPO_PATH.mkdir()
    repo = Repo.init(REPO_PATH)
    print("Git repository initialized at pdm_repo")
else:
    repo = Repo(REPO_PATH)
    print("Git repository loaded")
```

**Explanation:**

- `Path("pdm_repo")` – flexible, OS-independent path handling.
- `Repo.init()` – initializes a new Git repository.
- `Repo(REPO_PATH)` – opens an existing repository if it already exists.
- Modularizing Git logic in `git_repo.py` keeps **separation of concerns**: all Git operations are centralized.

> **Principle:** Initialization should be **idempotent**: running it multiple times does not break the system.

---

## 7.3 Add & Commit Files

We now integrate **check-in functionality with Git commits**.

```python
# git_repo.py continued
def commit_file(file_path: Path, username: str, message: str):
    """
    Commits a file to the Git repository with author info and a custom message.
    """
    repo.index.add([str(file_path)])  # Stage file
    repo.index.commit(
        message,
        author=f"{username} <{username}@example.com>"
    )
    print(f"File {file_path.name} committed by {username}")
```

**Line-by-line explanation:**

1. `repo.index.add()` – stages the file for commit. Only staged files are recorded.
2. `repo.index.commit()` – commits changes.

   - `message` – descriptive commit messages improve auditability.
   - `author` – links the change to a specific user.

3. Prints feedback in backend logs – helpful for **debugging and monitoring**.

**Best practices:**

- Always **use descriptive commit messages**. Example: `"Checked in file X after updating toolpaths"`.
- Stage **specific files** to avoid accidental commits.

---

## 7.4 Retrieve Commit History

We need to show users the **version history** of a file:

```python
def get_file_history(file_path: Path):
    """
    Returns a list of commits affecting the file.
    """
    commits = list(repo.iter_commits(paths=str(file_path)))
    history = []
    for commit in commits:
        history.append({
            "commit_hash": commit.hexsha,
            "author": commit.author.name,
            "date": commit.committed_datetime.isoformat(),
            "message": commit.message
        })
    return history
```

**Explanation:**

- `repo.iter_commits(paths=...)` – retrieves **only commits affecting the specified file**.
- `commit.hexsha` – the unique commit hash for reference.
- Returning a **list of dicts** is convenient for JSON API responses.
- Allows frontend to render a **history table or diff viewer**.

> **Software engineering principle:** Provide **clear audit trails**. Each action is traceable.

---

## 7.5 File Checkout / Lock with Git Awareness

We integrate **Git operations with the existing lock system**:

```python
from datetime import datetime

file_locks = {}  # In-memory lock dictionary {filename: username}

def checkout_file(file_path: Path, username: str):
    if file_path.name in file_locks:
        raise Exception(f"{file_path.name} is already checked out by {file_locks[file_path.name]}")

    file_locks[file_path.name] = username
    print(f"{file_path.name} checked out by {username} at {datetime.now()}")

def checkin_file(file_path: Path, username: str, message: str):
    if file_locks.get(file_path.name) != username:
        raise Exception("You do not hold the lock for this file")

    # Commit changes to Git
    commit_file(file_path, username, message)

    # Release lock
    del file_locks[file_path.name]
    print(f"{file_path.name} checked in by {username}")
```

**Explanation:**

- Locks are checked **before committing** to prevent race conditions.
- Only the user who holds the lock can commit.
- Commit is integrated **atomically** with releasing the lock.

> **Engineering principle:** Maintain **data integrity** and prevent **concurrent modification bugs**.

---

## 7.6 Download Specific Versions

We can let users retrieve **any historical version**:

```python
def get_file_version(file_path: Path, commit_hash: str):
    """
    Returns the content of a file at a specific commit.
    """
    commit = repo.commit(commit_hash)
    blob = commit.tree / file_path.name
    return blob.data_stream.read().decode("utf-8")
```

**Explanation:**

- `commit.tree / file_path.name` – accesses the file content at a specific commit.
- Returns a string, which can be displayed in a **diff viewer** or downloaded by the user.
- This is critical for **rollback scenarios**.

---

## 7.7 Viewing Line-by-Line Changes (Diff)

```python
def diff_versions(file_path: Path, old_hash: str, new_hash: str):
    """
    Returns a simple line-by-line diff between two versions.
    """
    old_commit = repo.commit(old_hash)
    new_commit = repo.commit(new_hash)

    diffs = old_commit.diff(new_commit, paths=str(file_path))
    result = []
    for diff in diffs:
        # diff.a_blob and diff.b_blob represent old and new content
        result.append({
            "old": diff.a_blob.data_stream.read().decode("utf-8") if diff.a_blob else "",
            "new": diff.b_blob.data_stream.read().decode("utf-8") if diff.b_blob else ""
        })
    return result
```

**Explanation:**

- `commit.diff()` – generates a **diff object**.
- Returns old and new content for UI to render visually.
- Helps programmers **see exactly what changed**, reducing mistakes.

---

## 7.8 Git Push/Pull Integration

For a **remote repository backup (e.g., GitLab)**:

```python
def push_changes():
    origin = repo.remote(name="origin")
    origin.push()
    print("Changes pushed to remote")

def pull_changes():
    origin = repo.remote(name="origin")
    origin.pull()
    print("Changes pulled from remote")
```

**Explanation:**

- Keeps local repo **in sync with central GitLab**.
- Push/pull operations can be triggered automatically after check-in/check-out.
- In production, **handle conflicts** gracefully (merge conflicts should not crash the system).

---

## 7.9 Frontend Integration

### 7.9.1 Fetch File History

```javascript
async function fetchHistory(filename) {
  const token = localStorage.getItem("token");
  const response = await fetch(
    `http://localhost:8000/api/files/${filename}/history`,
    {
      headers: { Authorization: `Bearer ${token}` },
    }
  );

  const history = await response.json();
  renderHistory(history); // Custom function to render in a table
}
```

**Explanation:**

- Sends JWT to authenticate request.
- Backend returns JSON array with **commit_hash, author, date, message**.
- Frontend renders a **clickable history** so users can download or view diffs.

---

## 7.10 Key Software Engineering Principles Applied

| Principle         | How It’s Applied in Section 7                                     |
| ----------------- | ----------------------------------------------------------------- |
| **Modularity**    | Git operations are centralized in `git_repo.py`.                  |
| **Atomicity**     | Check-in and commit happen together.                              |
| **Traceability**  | Each commit has author info and descriptive messages.             |
| **Versioning**    | Users can retrieve any historical version of a file.              |
| **Collaboration** | Git allows multiple users to work safely with conflict detection. |
| **Security**      | Only authenticated users can commit or view history.              |
| **Scalability**   | Git handles thousands of files efficiently.                       |

---

## 7.11 Next Steps

- Section 8 will add **real-time collaboration using WebSockets**, so users **see file status and edits in real-time**.
- Integrate **frontend diff viewers** for history visualization.
- Add **audit logging** for sensitive Git operations.

---

✅ **Section 7 Checklist**

- [ ] Local Git repository initialized.
- [ ] Files can be committed programmatically with author info.
- [ ] Check-in/check-out integrated with Git commits.
- [ ] Historical versions can be retrieved.
- [ ] Line-by-line diffs implemented.
- [ ] Remote GitLab push/pull capability added.
- [ ] Frontend fetches history and displays it.
- [ ] Principles of modularity, atomicity, traceability, and collaboration reinforced.

---

**Summary:**
Section 7 fully transitions our PDM system from **filesystem-based management** to **Git-backed version control**, making it professional, traceable, and ready for collaborative CNC program management.

---

I can now prepare **Section 8: Real-Time Collaboration & WebSockets** with the same **full detailed explanations, frontend/backend integration, and best practices**.

Absolutely! Let’s dive into **Section 8: Real-Time Collaboration**, keeping **full depth, teaching points, comments, and explanations**. This section is critical for making our PDM system feel professional and responsive, showing changes immediately to all users.

---

# Section 8: Real-Time Collaboration with WebSockets

## 8.0 Introduction

Until now, users **must manually refresh** to see updates in file status or check-in/check-out actions. Real-time collaboration solves this by:

- Instantly notifying users when **file status changes**.
- Showing **online presence** of other users.
- Enabling collaborative workflows **without conflicting edits**.

We’ll implement real-time features using **WebSockets**:

- **Backend:** FastAPI with `websockets` support.
- **Frontend:** JavaScript `WebSocket` API.
- **Principle:** WebSockets allow **persistent, bidirectional communication** unlike HTTP, which is request/response only.

---

## 8.1 Backend: Setting Up WebSocket Endpoint

We start with a simple WebSocket connection:

```python
# realtime.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()  # Accept handshake
        self.active_connections.append(websocket)
        print(f"New client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """
        Send a JSON message to all connected clients.
        """
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()
```

**Explanation:**

- `WebSocket.accept()` – completes the handshake between client and server.
- `active_connections` – keeps a list of currently connected clients.
- `broadcast(message)` – sends messages to **all users**, e.g., file checkouts or check-ins.
- Separation into a **ConnectionManager class** is **modular** and supports **future features** like private messaging.

---

### 8.1.1 WebSocket Route

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()  # Wait for messages from client
            print(f"Received: {data}")
            await manager.broadcast(data)  # Forward message to all clients
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

**Line-by-line explanation:**

- `while True` – keeps the connection open, enabling **continuous updates**.
- `receive_json()` – waits asynchronously for messages from clients.
- `broadcast(data)` – relays message to all connected clients, ensuring **real-time updates**.
- `WebSocketDisconnect` – properly cleans up when users close browser or lose connection.

> **Engineering principle:** **Asynchronous programming** is required for real-time operations to avoid blocking the server.

---

## 8.2 Frontend: Connecting to WebSocket

### 8.2.1 JavaScript WebSocket Setup

```javascript
let ws;

function connectWebSocket() {
  ws = new WebSocket("ws://localhost:8000/ws");

  ws.onopen = () => {
    console.log("Connected to WebSocket server");
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    handleRealtimeUpdate(data);
  };

  ws.onclose = () => {
    console.log("Disconnected, retrying in 2 seconds...");
    setTimeout(connectWebSocket, 2000); // Auto-reconnect
  };

  ws.onerror = (err) => {
    console.error("WebSocket error:", err);
    ws.close(); // Trigger onclose for retry
  };
}

connectWebSocket();
```

**Explanation:**

- `onopen` – confirms connection success.
- `onmessage` – receives JSON messages from the backend and calls `handleRealtimeUpdate()`.
- `onclose` – implements **automatic reconnection** for reliability.
- `onerror` – logs errors and triggers reconnect for **robustness**.

> **Software principle:** Always **anticipate network issues** and design for **resiliency** in real-time systems.

---

### 8.2.2 Sending Messages

Whenever a user checks out or checks in a file, we notify all clients:

```javascript
async function notifyFileAction(fileName, action, username) {
  const message = {
    fileName,
    action,
    username,
    timestamp: new Date().toISOString(),
  };
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(message));
  }
}
```

**Explanation:**

- `fileName` – which file changed
- `action` – `"checkout"` or `"checkin"`
- `username` – for audit/display
- `timestamp` – for sorting/display in frontend
- Ensures **minimal payload**, only what’s necessary to update UI.

---

## 8.3 Updating the UI in Real-Time

### 8.3.1 JavaScript Handler

```javascript
function handleRealtimeUpdate(data) {
  const { fileName, action, username, timestamp } = data;

  const fileElement = document.getElementById(fileName);
  if (!fileElement) return; // File not loaded yet

  // Update status text
  if (action === "checkout") {
    fileElement.querySelector(
      ".status"
    ).innerText = `Checked out by ${username}`;
    fileElement.querySelector(".checkout-btn").disabled = true;
    fileElement.querySelector(".checkin-btn").disabled =
      username !== currentUser;
  } else if (action === "checkin") {
    fileElement.querySelector(".status").innerText = "Available";
    fileElement.querySelector(".checkout-btn").disabled = false;
    fileElement.querySelector(".checkin-btn").disabled = true;
  }

  showToast(
    `${fileName} ${action} by ${username} at ${new Date(
      timestamp
    ).toLocaleTimeString()}`
  );
}
```

**Explanation:**

- Updates the **DOM elements dynamically** without reloading.
- Disables/enables buttons based on **lock ownership**.
- Shows a **toast notification** to confirm action for all users.
- `currentUser` ensures users cannot check in files they don’t own.

---

## 8.4 Presence Tracking (Online Users)

We can extend the WebSocket manager to broadcast **online users**:

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[dict] = []  # {websocket, username}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append({"websocket": websocket, "username": username})
        await self.broadcast({"type": "presence", "users": [u["username"] for u in self.active_connections]})

    def disconnect(self, websocket: WebSocket):
        self.active_connections = [u for u in self.active_connections if u["websocket"] != websocket]
```

**Explanation:**

- Each connection now includes a `username`.
- On **connect/disconnect**, server broadcasts the updated list of online users.
- Frontend can render a sidebar showing **who is online**.

---

## 8.5 Benefits & Software Engineering Concepts

| Concept                      | Implementation                                                                            |
| ---------------------------- | ----------------------------------------------------------------------------------------- |
| **Asynchronous Programming** | WebSocket `async/await` allows multiple users without blocking the server.                |
| **Real-Time Collaboration**  | Immediate feedback on file locks prevents conflicts.                                      |
| **UI Responsiveness**        | DOM updates via JS handlers avoid page reloads.                                           |
| **Resilience**               | Auto-reconnect ensures system remains functional despite network drops.                   |
| **Separation of Concerns**   | WebSocket manager is independent from file logic, simplifying future scaling.             |
| **Security**                 | Only authenticated users should connect. You can extend `ws` to require JWT verification. |

---

## 8.6 Frontend Enhancements

- Highlight **recently changed files** in the UI.
- Sort by **last action timestamp**.
- Integrate **diff previews** in real-time if multiple users upload new versions.

Example: Highlight recent updates:

```javascript
function highlightUpdatedFile(fileElement) {
  fileElement.classList.add("highlight");
  setTimeout(() => fileElement.classList.remove("highlight"), 2000);
}
```

---

## 8.7 Next Steps

- Section 9 will focus on **Integrating Real-Time Collaboration with Git version control**.

  - Ensure check-in/check-out actions trigger **commits and broadcast events**.
  - Users can **see file version history in real-time**.

- We will also explore **frontend diff viewers with WebSocket notifications**.

---

✅ **Section 8 Checklist**

- [ ] Backend WebSocket endpoint implemented.
- [ ] ConnectionManager handles multiple clients and broadcasts.
- [ ] Frontend connects and handles incoming messages.
- [ ] Checkout/check-in actions broadcast in real-time.
- [ ] UI updates dynamically based on WebSocket events.
- [ ] Online user presence displayed and updated.
- [ ] Auto-reconnect and error handling implemented for robust collaboration.
- [ ] Principles of async programming, separation of concerns, and responsive UX reinforced.

---

**Summary:**
Section 8 adds **real-time collaboration** to the PDM system. Users see file status, check-ins, checkouts, and online presence **instantly**, making the system more **responsive and professional**. It introduces **asynchronous programming, robust frontend-backend communication, and real-world collaboration patterns**.

---

I can now prepare **Section 9: Final Polishing, Diff Viewer, Audit Logs, and Full App Integration**, which combines **all previous features with Git and real-time updates**, keeping the same level of depth.

Perfect! Let’s redo **Sections 7 and 8 together**, now fully integrating **RBAC**, with **full detailed explanations, comments, and teaching points**. This will show how **Git integration** and **real-time collaboration** respect **user roles**, making the system professional and secure.

---

# Sections 7 & 8 (Reworked): Git Integration + Real-Time Collaboration with RBAC

---

## 7.0 Introduction

Now that we have:

- **Authentication** (login, JWT)
- **Authorization** (RBAC)
- **File check-in/check-out logic**

…it’s time to **replace simple file operations with Git**, ensuring:

- Version-controlled file history.
- Audit trail for every action.
- Real-time updates that respect **user roles**.

We'll also connect **real-time WebSocket updates** with Git operations, so changes **appear instantly to all users**, while enforcing **who can perform which action**.

---

## 7.1 Backend: Git Integration with RBAC

### 7.1.1 Initialize Repository

```python
# git_utils.py
from git import Repo
from pathlib import Path

REPO_PATH = Path("pdm_repo")

if not REPO_PATH.exists():
    REPO_PATH.mkdir()
    repo = Repo.init(REPO_PATH)
    print("Initialized new Git repository")
else:
    repo = Repo(REPO_PATH)
```

**Explanation:**

- `Repo.init` – initializes a Git repository if none exists.
- This **replaces manual file management** with Git’s robust version control.
- **Benefit:** Every file operation can now create **atomic commits**, improving traceability.

---

### 7.1.2 Git Commit Function

```python
def commit_file(user: str, message: str, file_path: Path):
    repo.index.add([str(file_path)])
    repo.index.commit(f"{message} by {user}")
```

**Explanation:**

- Adds the file to the Git index (`add`) and commits it.
- Commit message includes the **user performing the action**.
- Using Git allows **rollback, history tracking, blame** features.
- With RBAC, **we check the user’s role before committing**.

---

### 7.1.3 Enforcing RBAC on Git Actions

```python
from dependencies import require_role

@app.post("/files/{filename}/checkout")
def checkout_file(filename: str, current_user=Depends(require_role("user"))):
    file_path = REPO_PATH / filename
    if not file_path.exists():
        return {"error": "File not found"}

    if is_checked_out(file_path):
        return {"error": "File already checked out"}

    lock_file(file_path, current_user.username)
    commit_file(current_user.username, f"Checked out {filename}", file_path)
    broadcast_file_action(filename, "checkout", current_user.username)
    return {"status": "success", "message": f"{filename} checked out"}
```

**Explanation:**

- `current_user=Depends(require_role("user"))` – **any authenticated user** can check out, but the backend still enforces permissions.
- `commit_file()` logs the action in Git.
- `broadcast_file_action()` sends real-time notifications to **all connected clients**.
- Ensures **all Git actions respect RBAC**.

---

### 7.1.4 Admin Actions: Deleting Files

```python
@app.delete("/files/{filename}")
def delete_file(filename: str, current_user=Depends(require_role("admin"))):
    file_path = REPO_PATH / filename
    if file_path.exists():
        file_path.unlink()
        commit_file(current_user.username, f"Deleted {filename}", file_path)
        log_action(current_user.username, "delete_file", filename)
        broadcast_file_action(filename, "delete", current_user.username)
        return {"status": "success", "message": f"{filename} deleted by admin"}
    return {"status": "error", "message": "File does not exist"}
```

**Explanation:**

- Only `admin` can delete files.
- Git commit ensures **historical traceability**.
- Real-time broadcast updates all clients instantly.
- RBAC ensures **UI and backend are aligned** – users can’t perform unauthorized actions.

---

### 7.1.5 View File History (Git Log)

```python
def get_file_history(filename: str):
    file_path = REPO_PATH / filename
    commits = list(repo.iter_commits(paths=str(file_path)))
    history = [
        {"author": c.author.name, "message": c.message, "date": c.committed_datetime.isoformat()}
        for c in commits
    ]
    return history
```

**Explanation:**

- Users can **review the full history** of a file.
- `iter_commits(paths=...)` filters commits to this file only.
- This can feed the **frontend diff viewer** and **audit logs**.

---

## 8.0 Real-Time Collaboration with Git + RBAC

### 8.1 WebSocket Updates Respect Roles

```python
async def broadcast_file_action(filename: str, action: str, username: str):
    message = {"fileName": filename, "action": action, "username": username}

    # Only broadcast certain actions to appropriate roles if needed
    for connection in manager.active_connections:
        user_role = connection["role"]
        if action == "delete" and user_role != "admin":
            continue  # Only admins need to know about deletes
        await connection["websocket"].send_json(message)
```

**Explanation:**

- Integrates **RBAC with real-time events**.
- Certain sensitive events (like file deletion) are **only broadcast to authorized users**, reducing unnecessary exposure.
- Demonstrates **fine-grained real-time control** based on roles.

---

### 8.2 Frontend: Handling Role-Based Real-Time Updates

```javascript
function handleRealtimeUpdate(data, currentUserRole) {
  const { fileName, action, username } = data;
  const fileElement = document.getElementById(fileName);
  if (!fileElement) return;

  // Role-based handling
  if (action === "delete" && currentUserRole !== "admin") return;

  if (action === "checkout") {
    fileElement.querySelector(
      ".status"
    ).innerText = `Checked out by ${username}`;
    fileElement.querySelector(".checkout-btn").disabled = true;
  } else if (action === "checkin") {
    fileElement.querySelector(".status").innerText = "Available";
    fileElement.querySelector(".checkout-btn").disabled = false;
  } else if (action === "delete") {
    fileElement.remove();
    showToast(`${fileName} deleted by ${username}`);
  }
}
```

**Explanation:**

- **UI matches backend RBAC**, preventing users from seeing unauthorized actions.
- Keeps real-time updates **secure and consistent**.
- `showToast()` improves user experience with **non-blocking notifications**.

---

### 8.3 Audit Logging with Git + Real-Time

- Every action (checkout, check-in, delete) is **logged in Git** and optionally in **audit log JSON**.
- **Admins can view a real-time feed of sensitive operations**, combining **WebSockets + Git history**.

```python
def log_and_broadcast(user, action, filename):
    log_action(user, action, filename)  # Audit
    broadcast_file_action(filename, action, user)  # Real-time
```

**Software Principle:**
Separation of concerns:

1. `log_action()` → persistence/audit.
2. `broadcast_file_action()` → frontend real-time update.
3. `commit_file()` → Git version control.

Each layer handles **one responsibility**, making the system **modular, testable, and maintainable**.

---

### 8.4 Teaching Notes / Concepts Reinforced

| Concept                 | Explanation                                                                  |
| ----------------------- | ---------------------------------------------------------------------------- |
| RBAC                    | Enforces **who can perform what**, both in backend and frontend.             |
| Git Integration         | Tracks **every action**, enabling **history, rollback, diff, and blame**.    |
| Real-Time Collaboration | WebSockets update all connected users instantly.                             |
| Separation of Concerns  | Logging, real-time updates, and Git commits are modular.                     |
| Security Best Practices | Backend enforces role checks, UI only for convenience.                       |
| Resilience              | Auto-reconnect WebSockets ensure consistent real-time updates.               |
| Professional UX         | Toasts, status updates, online presence – emulate **enterprise-grade apps**. |

---

### 8.5 Next Steps

- **Section 9:** Full App Polishing

  - Integrate **diff viewer** for Git changes.
  - Enable **blame view** for each line.
  - UI sorting/filtering of files.
  - Final security checks and deployment considerations.

- All previous modules (**authentication, RBAC, Git, WebSockets**) are now **fully integrated**.

---

✅ **Sections 7 & 8 Checklist**

- [ ] Git repository initialized and connected.
- [ ] Commit file actions with proper user attribution.
- [ ] RBAC enforced on Git operations (checkout, check-in, delete).
- [ ] Real-time WebSocket updates broadcast actions respecting roles.
- [ ] Frontend UI reflects roles and real-time status.
- [ ] Audit log maintained and optionally broadcasted.
- [ ] Principles of separation of concerns, security, resilience, and professional UX reinforced.

---

**Summary:**
Sections 7 & 8 integrate **Git version control** with **real-time collaboration**, all while enforcing **role-based access control**. This produces a **professional, secure, and enterprise-ready PDM system** that:

- Tracks **every file change**
- Shows **real-time updates**
- Respects **user permissions**
- Provides **auditable history**
- Reinforces **software engineering principles** like modularity, separation of concerns, and security.

---

I can now prepare **Section 9: Diff Viewer, Blame View, Final Polishing, and Deployment**, keeping the same **full-depth teaching approach**.

Perfect! Let’s move on to **Section 9: Diff Viewer, Blame View, UI Polishing, and Deployment**, keeping the **same full-depth, teaching-focused style**. This section ties everything together into a **professional, production-ready PDM system**.

---

# Section 9: Final Polishing – Diff Viewer, Blame View, and Deployment

---

## 9.0 Introduction

By now, our system has:

- Authentication & RBAC (user/admin roles)
- File check-in/check-out with Git tracking
- Real-time collaboration with WebSockets

Now we want to:

1. **Diff Viewer:** Compare versions of files.
2. **Blame View:** See who modified each line.
3. **UI Enhancements:** Polished look, usability improvements.
4. **Deployment Prep:** Make the system production-ready.

These features will **reinforce core CS concepts**: data structures, algorithms (diff), and client-server design.

---

## 9.1 Diff Viewer

**Purpose:** Show changes between two file versions (commits).

---

### 9.1.1 Backend: Generate Diff

```python
# git_utils.py
def get_file_diff(filename: str, commit_sha1: str, commit_sha2: str):
    file_path = REPO_PATH / filename
    commit1 = repo.commit(commit_sha1)
    commit2 = repo.commit(commit_sha2)
    diff_index = commit1.diff(commit2, paths=str(file_path))

    # There should only be one diff for our file
    if not diff_index:
        return "No differences found"

    diff_text = diff_index[0].diff.decode("utf-8")
    return diff_text
```

**Explanation:**

- `commit1.diff(commit2)` – uses Git Python to compute differences.
- `diff_index[0].diff` – raw diff bytes for the file.
- Decoding to `"utf-8"` makes it **readable in JSON** for frontend.
- We are effectively **recreating `git diff` programmatically**, teaching **data structures (lines), text comparison algorithms, and version control principles**.

---

### 9.1.2 Frontend: Display Diff

```javascript
function showDiff(filename, commit1, commit2) {
  fetch(`/api/files/${filename}/diff?commit1=${commit1}&commit2=${commit2}`)
    .then((res) => res.json())
    .then((data) => {
      const diffContainer = document.getElementById("diff-view");
      diffContainer.innerHTML = "";
      data.diff.split("\n").forEach((line) => {
        const lineEl = document.createElement("pre");
        if (line.startsWith("+"))
          lineEl.style.backgroundColor = "#d4fcdc"; // Added line
        else if (line.startsWith("-")) lineEl.style.backgroundColor = "#fddcdc"; // Removed line
        lineEl.innerText = line;
        diffContainer.appendChild(lineEl);
      });
    });
}
```

**Explanation:**

- Splits diff into lines and colors additions and deletions.
- Teaches **frontend DOM manipulation, styling, and visual feedback**.
- Diff viewer enhances **user decision-making**, showing **exact line-by-line changes**.

---

## 9.2 Blame View

**Purpose:** Show **who last modified each line**.

---

### 9.2.1 Backend: Blame Data

```python
def get_file_blame(filename: str, commit_sha: str):
    commit = repo.commit(commit_sha)
    blame_data = repo.blame(commit, str(REPO_PATH / filename))

    # Convert to a readable list of dicts
    result = [{"line": line[1].strip(), "author": line[0].author.name} for line in blame_data]
    return result
```

**Explanation:**

- `repo.blame(commit, path)` – maps each line to the **last commit author**.
- Returns a **list of dictionaries**, making it easy to feed to frontend.
- Demonstrates **how version control tracks authorship at line-level granularity**.

---

### 9.2.2 Frontend: Display Blame

```javascript
function showBlame(filename, commit) {
  fetch(`/api/files/${filename}/blame?commit=${commit}`)
    .then((res) => res.json())
    .then((data) => {
      const blameContainer = document.getElementById("blame-view");
      blameContainer.innerHTML = "";
      data.forEach((item) => {
        const lineEl = document.createElement("div");
        lineEl.innerText = `${item.author}: ${item.line}`;
        blameContainer.appendChild(lineEl);
      });
    });
}
```

**Explanation:**

- Shows **author + line**, teaching **traceability**.
- Combined with diff, gives **full historical understanding**.

---

## 9.3 Frontend Polishing

### 9.3.1 CSS: Professional Layout

```css
body {
  font-family: "Segoe UI", sans-serif;
  background-color: #f4f6f8;
  margin: 0;
  padding: 0;
}

header,
footer {
  background-color: #1f2937;
  color: white;
  padding: 10px 20px;
  text-align: center;
}

main {
  padding: 20px;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

button {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  opacity: 0.85;
}
```

**Teaching Points:**

- Flexbox (`display: flex; flex-direction: column`) → modern responsive layout.
- Consistent **header/footer** improves usability.
- Buttons styled with **hover effects** → better UX.
- Encourages **CSS modular thinking** for enterprise apps.

---

### 9.3.2 Toast Notifications

```javascript
function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.innerText = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}
```

```css
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #111;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  opacity: 0.9;
}
```

**Explanation:**

- Non-blocking messages improve **usability**.
- Teaches **DOM manipulation, positioning, and animations in CSS**.

---

## 9.4 Deployment Considerations

1. **Backend Deployment**

- Use **Uvicorn + Gunicorn** for production.
- Configure HTTPS (SSL/TLS).
- Environment variables for secrets (JWT keys, passwords).
- Separate dev/prod databases (or Git repositories).

2. **Frontend Deployment**

- Bundle JS/CSS with **ESBuild or Webpack**.
- Serve static files via FastAPI (`app.mount("/static", StaticFiles(directory="static"))`).

3. **Security Checks**

- Validate all user input.
- Enforce RBAC on backend.
- Hash passwords, use HTTPS.

4. **Scalability**

- WebSocket connections can be **scaled horizontally** with Redis Pub/Sub.
- Git repo may be **cloned or mirrored** for large-scale operations.

---

## 9.5 Key CS / Software Engineering Concepts Reinforced

| Concept                               | Section Example                                                      |
| ------------------------------------- | -------------------------------------------------------------------- |
| **Data Structures**                   | Diff computation → arrays of lines, dictionaries for blame.          |
| **Algorithms**                        | Line-by-line diff → understanding differences between strings/files. |
| **Frontend/Backend Communication**    | Fetch API + JSON.                                                    |
| **Separation of Concerns**            | Backend computes diff/blame; frontend displays them.                 |
| **Security / RBAC**                   | Admin/user permissions enforced in every action.                     |
| **UX / UI Principles**                | Toasts, status indicators, diff highlighting.                        |
| **Deployment / Production Readiness** | HTTPS, environment variables, static file serving, scaling.          |

---

## ✅ Section 9 Checklist

- [ ] Diff viewer implemented (line-level, additions/removals highlighted)
- [ ] Blame view implemented (line-level author tracking)
- [ ] UI fully polished (flex layout, headers/footers, buttons, toasts)
- [ ] Real-time updates integrated with diff/blame actions
- [ ] Backend + frontend respect RBAC at all levels
- [ ] Production-ready deployment plan documented

---

**Summary:**

Section 9 completes the PDM system by:

- **Visualizing Git history** – diff viewer, blame view
- **Polishing the UI** – CSS, layout, notifications
- **Preparing for production** – deployment strategies and security
- Reinforcing **CS/software engineering concepts**: algorithms, data structures, separation of concerns, security, and professional UX.

---

If you want, the next step could be a **full recap of all sections with a suggested order of learning**—so you can **copy section by section into MkDocs as a complete, cohesive tutorial**.

Perfect — this is a **comprehensive feature list**. Since the goal is to create a **tutorial you can copy section by section into MkDocs**, it makes sense to tackle **each feature or feature set in its own dedicated section**, so you get:

- Full explanation of **why it exists** (user story / business logic)
- Detailed **how it’s implemented** (backend + frontend + Git/DB integration)
- Deep **CS/software engineering concepts** reinforced
- Full **code examples with explanations and comments**

Here’s how I would suggest structuring **new tutorial sections based on your list**, **filling gaps or expanding sections that were missing**:

---

## Proposed Feature-Based Sections (Post Section 9)

| Section | Feature(s)                                                                  | Purpose / Teaching Focus                                                                           |
| ------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **10**  | Search, Sort, Filter                                                        | Teach DOM manipulation, JS algorithms, backend query filtering, UX best practices                  |
| **11**  | File Uploads & Drag-and-Drop                                                | Teach file handling in FastAPI, Git commit integration, frontend file API, security considerations |
| **12**  | Historical Version Download                                                 | Teach Git hash handling, REST API design for binary assets, download streams                       |
| **13**  | Forced Check-In / Lock Timeout                                              | Teach scheduling, concurrency, admin overrides, persistent state handling                          |
| **14**  | Audit Log Viewer                                                            | Teach logging, database design for audit tables, role-based access control, UI tables              |
| **15**  | Notification System + Subscriptions                                         | Teach WebSockets, Pub/Sub design, event-driven architecture, frontend notifications                |
| **16**  | Presence / Online Users                                                     | Teach real-time user state tracking, WebSockets, session management                                |
| **17**  | Containerization & Deployment (Docker / Docker Compose)                     | Teach reproducible environments, multi-container orchestration, production readiness               |
| **18**  | CI / Automated Testing                                                      | Teach unit/integration testing, `pytest`, CI/CD pipelines, automated quality control               |
| **19**  | Large File Support (Git LFS)                                                | Teach version control for binary assets, repository optimization, Git LFS workflow                 |
| **20**  | Optional Advanced UI Features (diff highlight editor, file tree navigation) | Teach advanced JS/CSS, code editor integration, usability enhancements                             |

---

### How We Could Proceed

1. Pick **one feature section** at a time.
2. For each section, I will write a **full tutorial** including:

   - **User story / Why it matters**
   - **Backend implementation** (FastAPI + DB + Git)
   - **Frontend implementation** (JS + HTML + CSS + UX)
   - **Full code with line-by-line explanations**
   - **CS concepts reinforced**

3. After each section, you can **copy it to MkDocs** and learn it in depth.

---

If you like, we can start with **Section 10: Search, Sort, and Filter** next, because that’s a **high-value feature for usability** and also reinforces **CS/algorithms concepts**.

Perfect! Let’s dive into **Section 10: Search, Sort, and Filter** with the same **full-depth, teaching-focused style** as before.

We’ll cover **why this matters, how to implement it step by step, and the CS/software engineering concepts behind it**.

---

# Section 10: Search, Sort, and Filter Files

---

## 10.0 Introduction

By this point, the PDM system can:

- Display a list of files grouped by part family
- Show check-out/check-in status
- Update file states in real-time via WebSockets

However, as the repository grows, **users need to quickly locate specific files**, see which are available, and organize their view. That’s where **search, sort, and filter** come in.

**Learning goals:**

- DOM manipulation with JavaScript
- CSS styling for interactive inputs
- Efficient search and sorting algorithms
- Backend filtering logic for performance
- Reinforcement of user-centric design and UX principles

---

## 10.1 User Stories

- “As a CNC Programmer, I want to search for a file by name or description so I don’t have to scroll through hundreds of files.”
- “As a Shop Manager, I want to filter files by status (Available / Checked Out) so I can quickly see workflow bottlenecks.”
- “I want to sort files by name or status to maintain an organized view.”

---

## 10.2 Backend: Filter and Sort Support

Even though frontend can filter and sort **in memory**, it’s better to **support filtering at the API level** for large repositories.

```python
# api/files.py
from fastapi import APIRouter, Query
from typing import List, Optional
from models import FileOut, get_all_files

router = APIRouter()

@router.get("/files", response_model=List[FileOut])
def list_files(
    search: Optional[str] = Query(None, description="Search by filename or description"),
    status: Optional[str] = Query(None, description="Filter by status"),
    sort_by: Optional[str] = Query("name", description="Sort by 'name' or 'status'")
):
    """
    Returns a list of files, optionally filtered and sorted.
    """
    files = get_all_files()  # Returns list of FileOut dicts

    # Search: filter by partial match in filename or description
    if search:
        files = [f for f in files if search.lower() in f.name.lower() or search.lower() in f.description.lower()]

    # Status filter
    if status:
        files = [f for f in files if f.status.lower() == status.lower()]

    # Sorting
    if sort_by == "name":
        files.sort(key=lambda f: f.name.lower())
    elif sort_by == "status":
        files.sort(key=lambda f: f.status.lower())

    return files
```

**Explanation / Teaching Points:**

- `Optional[str] = Query(None)` → teaches **FastAPI query parameters**
- `search.lower() in f.name.lower()` → teaches **case-insensitive string search**
- `files.sort(key=lambda f: ...)` → Python’s **built-in stable sorting algorithm (Timsort)**
- Reinforces **separation of concerns**: backend provides filtered data, frontend renders it.

---

## 10.3 Frontend: Search Input

```html
<div class="search-container">
  <input type="text" id="search-input" placeholder="Search files..." />
  <select id="status-filter">
    <option value="">All</option>
    <option value="available">Available</option>
    <option value="checkedout">Checked Out</option>
  </select>
  <select id="sort-select">
    <option value="name">Sort by Name</option>
    <option value="status">Sort by Status</option>
  </select>
</div>
<ul id="file-list"></ul>
```

**Explanation:**

- Search input + filter dropdowns + sort dropdown give **full control to the user**
- `id`s allow JavaScript to **bind event listeners**
- Using `<ul>` for file list encourages **semantic HTML**

---

### 10.3.1 Styling with CSS

```css
.search-container {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

#search-input,
#status-filter,
#sort-select {
  padding: 5px 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 1rem;
}
```

**Teaching Points:**

- `display: flex; gap: 10px` → flexible horizontal layout
- Padding, border-radius, and font-size → UX improvements
- Minimal, readable styling enhances **professional UI design**

---

## 10.4 Frontend: Live Search, Sort, and Filter

```javascript
const searchInput = document.getElementById("search-input");
const statusFilter = document.getElementById("status-filter");
const sortSelect = document.getElementById("sort-select");
const fileList = document.getElementById("file-list");

async function fetchFiles() {
  const search = searchInput.value;
  const status = statusFilter.value;
  const sort_by = sortSelect.value;

  const res = await fetch(
    `/api/files?search=${search}&status=${status}&sort_by=${sort_by}`
  );
  const files = await res.json();
  renderFiles(files);
}

function renderFiles(files) {
  fileList.innerHTML = ""; // Clear existing items
  files.forEach((f) => {
    const li = document.createElement("li");
    li.innerText = `${f.name} - ${f.status}`;
    fileList.appendChild(li);
  });
}

// Event listeners for live updates
searchInput.addEventListener("input", fetchFiles);
statusFilter.addEventListener("change", fetchFiles);
sortSelect.addEventListener("change", fetchFiles);

// Initial fetch
fetchFiles();
```

**Explanation / Teaching Points:**

- **Debounced live search**: could add a debounce to reduce API calls (advanced optimization)
- Event-driven programming: JS responds immediately to user input
- Separation of concerns: `fetchFiles()` handles API calls, `renderFiles()` handles UI
- Teaches **asynchronous programming** with `async/await`
- Makes the UI **responsive and interactive**, crucial for large repositories

---

## 10.5 Advanced Teaching Points / CS Concepts

- **Algorithms:**

  - Linear search for filtering
  - Stable sorting with Python `sort()` (Timsort)

- **Data Structures:**

  - Lists of objects representing files

- **Performance Considerations:**

  - Backend filtering reduces **network and frontend computation**
  - Could use pagination for very large file sets

- **UX Principles:**

  - Immediate feedback (live search) improves workflow
  - Dropdown filters reduce cognitive load

---

## ✅ 10.6 Checklist

- [ ] Backend supports search, filter, and sort
- [ ] Frontend input fields and dropdowns implemented
- [ ] Event listeners for live search, filter, sort
- [ ] CSS styled for clean, professional UX
- [ ] Frontend calls backend with query params, updates DOM dynamically
- [ ] CS concepts reinforced: algorithms, data structures, async programming, UX

---

**Summary:**

- Section 10 teaches **end-to-end implementation of search, filter, and sort**
- Reinforces **backend + frontend integration**, **user-centric design**, and **CS concepts like search and sorting algorithms**
- Prepares you for the next sections: **file uploads, version downloads, forced check-in, and notifications**

---

If you want, the next section we can tackle is **Section 11: File Uploads & Drag-and-Drop**, which is a **major user story** and dives deep into **backend file handling, Git integration, and frontend file APIs**.

Perfect! Let’s dive into **Section 11: File Uploads & Drag-and-Drop** with **full depth**, teaching **why it’s important**, **how it works**, and **CS/software engineering concepts** behind it.

This section builds directly on the **search/sort/filter features** we just implemented.

---

# Section 11: File Uploads & Drag-and-Drop

---

## 11.0 Introduction

At this stage, users can:

- View files
- Search, filter, and sort files
- Check them in and out

However, **uploading new `.mcam` files** is a crucial workflow. This feature allows:

- CNC programmers to add new programs
- Shop managers to centralize new files
- Versioning via Git to track all changes

We’ll implement:

1. Standard file input
2. Drag-and-drop upload
3. Backend file handling with FastAPI
4. Git integration for versioning
5. Frontend UI with progress feedback

**Learning goals:**

- HTML5 File API
- Drag-and-drop events in JS
- FastAPI file upload handling
- Saving files securely on the server
- Committing files to Git programmatically
- UX feedback for uploads (modals, progress bars)

---

## 11.1 User Stories

- “As a CNC Programmer, I want to drag and drop a `.mcam` file into the browser to upload it quickly.”
- “As a user, I want the system to validate the file type and size before accepting it.”
- “I want to see progress or success/failure notifications after upload.”
- “I want the upload to create a Git commit automatically, with my username as the author.”

---

## 11.2 Backend: FastAPI File Upload

FastAPI makes file uploads simple using `UploadFile` and `File`.

```python
# api/files.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from pathlib import Path
import shutil
from git_integration import commit_file
from auth import get_current_user

router = APIRouter()

UPLOAD_DIR = Path("data/files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), user: str = Depends(get_current_user)):
    """
    Upload a .mcam file and commit it to Git.
    """
    # 1. Validate file type
    if not file.filename.endswith(".mcam"):
        raise HTTPException(status_code=400, detail="Only .mcam files are allowed")

    # 2. Save file to server
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3. Commit file to Git
    commit_message = f"Upload {file.filename} by {user.username}"
    commit_file(file_path, commit_message, user.username)

    return {"status": "success", "filename": file.filename}
```

**Explanation / Teaching Points:**

- `UploadFile` is **streamed**, avoiding loading the entire file into memory — teaches **efficient file handling**
- `shutil.copyfileobj` is used for **binary-safe copy**
- Validation (`.mcam`) enforces **security and workflow rules**
- `commit_file()` function integrates **Git for version control**
- `Depends(get_current_user)` ensures **only authenticated users can upload**

---

## 11.3 Git Integration

The `commit_file` function handles **staging and committing files programmatically**:

```python
# git_integration.py
from git import Repo

REPO_PATH = "data/repo"

def commit_file(file_path, message, author_name):
    repo = Repo(REPO_PATH)
    repo.index.add([str(file_path)])
    repo.index.commit(message, author=author_name)
```

**Teaching Points:**

- Using **GitPython** to manage Git repositories programmatically
- Reinforces **version control concepts**: staging, committing, author attribution
- Ensures every upload is **traceable**

---

## 11.4 Frontend: File Input

```html
<div class="upload-container">
  <input type="file" id="file-input" accept=".mcam" />
  <div id="drop-zone">Drag & Drop .mcam files here</div>
</div>
```

**Explanation:**

- `accept=".mcam"` ensures only `.mcam` files are selectable
- The `drop-zone` div allows **drag-and-drop interaction**
- Semantic and minimal HTML improves **usability and accessibility**

---

## 11.5 Frontend: Drag-and-Drop & Upload Logic

```javascript
const fileInput = document.getElementById("file-input");
const dropZone = document.getElementById("drop-zone");

function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  fetch("/api/upload", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status === "success") {
        alert(`File ${data.filename} uploaded successfully!`);
        fetchFiles(); // Refresh the file list
      }
    })
    .catch((err) => {
      alert("Upload failed: " + err.message);
    });
}

// Standard file input
fileInput.addEventListener("change", (e) => {
  uploadFile(e.target.files[0]);
});

// Drag-and-drop
dropZone.addEventListener("dragover", (e) => e.preventDefault());
dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  const file = e.dataTransfer.files[0];
  uploadFile(file);
});
```

**Teaching Points:**

- `FormData` is used to send **multipart/form-data**, required for file uploads
- Drag-and-drop uses `dragover` + `drop` events → **HTML5 event API**
- Error handling and success feedback reinforce **robust UX**
- `fetchFiles()` ensures **frontend and backend remain in sync** after upload

---

## 11.6 CSS Styling for Upload

```css
#drop-zone {
  border: 2px dashed #4caf50;
  padding: 40px;
  text-align: center;
  border-radius: 8px;
  color: #4caf50;
  transition: background-color 0.3s;
}

#drop-zone.dragover {
  background-color: #f0fff0;
}
```

**Teaching Points:**

- Visual feedback for **drag-over state** improves usability
- Dashed borders indicate **drop target**
- CSS transitions create a **smooth user experience**

---

## 11.7 Advanced Considerations

- **Multiple File Uploads:** Loop over `e.target.files` or `e.dataTransfer.files`
- **Progress Bar:** Use `XMLHttpRequest` or `fetch` with streams for **upload progress**
- **Security:** Validate file size and content server-side
- **Concurrency:** Ensure Git commits are atomic to prevent conflicts

---

## ✅ 11.8 Checklist

- [ ] Backend endpoint accepts `.mcam` uploads
- [ ] Files saved to server with secure binary handling
- [ ] Git commit created with author attribution
- [ ] Frontend standard file input works
- [ ] Drag-and-drop file upload works
- [ ] CSS visually indicates drop target
- [ ] Upload success/failure feedback is displayed
- [ ] File list refreshes after upload

---

**Summary:**

- Section 11 teaches **full-stack file upload implementation**
- Reinforces **FastAPI file handling, Git integration, JS DOM manipulation, CSS for UX**
- Prepares for **Section 12: Historical Version Download**, where users can download previous versions of uploaded files

---

We can move to **Section 12: Historical Version Download** next, which is a natural extension and introduces **Git commit history, REST endpoints for file retrieval, and frontend download handling**.

Absolutely! Section 12 is where the PDM app truly shines—**handling historical file versions**, giving users traceable, auditable access to every change made to their `.mcam` files. We’ll go **super deep**, covering backend, frontend, Git integration, REST APIs, security, and UX.

---

# Section 12: Historical Version Download

---

## 12.0 Introduction

By now, the PDM system can:

- Upload new `.mcam` files
- Check them in/out
- Search, filter, and sort

However, the **core purpose of a PDM system** is **version control**. CNC programmers need to:

- Access previous versions of a file
- Compare changes between versions
- Understand **who did what, when, and why**

**Learning goals:**

- Advanced Git integration (commits, logs, checkout)
- REST APIs for retrieving file history
- Frontend rendering of historical data
- Downloading arbitrary file versions
- Deep understanding of **auditability and traceability** in software systems

---

## 12.1 User Stories

- “As a CNC Programmer, I want to download any previous version of a file for reference or rollback.”
- “I want to see a commit history with author, timestamp, and message.”
- “I want to compare changes between two versions of a file.”
- “As a Shop Manager, I want this process to be safe and traceable.”

---

## 12.2 Backend: Git Commit History

We will use **GitPython** to query commit history.

```python
# git_integration.py
from git import Repo
from pathlib import Path

REPO_PATH = Path("data/repo")
repo = Repo(REPO_PATH)

def get_file_history(file_path: Path):
    """
    Returns a list of commits affecting a specific file.
    """
    commits = list(repo.iter_commits(paths=str(file_path)))
    history = []
    for commit in commits:
        history.append({
            "commit_hash": commit.hexsha,
            "author": commit.author.name,
            "email": commit.author.email,
            "date": commit.committed_datetime.isoformat(),
            "message": commit.message.strip()
        })
    return history
```

**Teaching Points:**

- `repo.iter_commits(paths=...)` → filters commits to a **specific file**
- Each commit contains metadata: **hash, author, email, timestamp, message**
- Git commit hash ensures **immutable, unique identification**
- Data structure: list of dictionaries → easily JSON-serializable

---

## 12.3 Backend: Download Specific Version

We want to allow downloading **any historical version**:

```python
# api/files.py
from fastapi.responses import FileResponse
from fastapi import HTTPException

@router.get("/files/{filename}/history/{commit_hash}")
def download_file_version(filename: str, commit_hash: str, user: str = Depends(get_current_user)):
    file_path = REPO_PATH / filename

    try:
        # Checkout file content from specific commit
        blob = repo.commit(commit_hash).tree / filename
        temp_path = Path(f"/tmp/{filename}")
        temp_path.write_bytes(blob.data_stream.read())
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found in commit {commit_hash}")

    return FileResponse(temp_path, filename=filename)
```

**Teaching Points:**

- Accessing historical file data uses **Git blob objects**
- `data_stream.read()` → reads the **binary content** of the file at that commit
- Temporary file ensures **safe download without modifying working directory**
- Security: validate `commit_hash` and `filename` to avoid **path traversal**

---

## 12.4 Frontend: Display File History

```html
<div id="history-modal" class="modal">
  <div class="modal-content">
    <h2>File History</h2>
    <table id="history-table">
      <thead>
        <tr>
          <th>Commit</th>
          <th>Author</th>
          <th>Date</th>
          <th>Message</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
    <button class="close-modal">Close</button>
  </div>
</div>
```

**Explanation:**

- Table shows **metadata for each commit**
- “Actions” column includes **download link or diff view**
- Modal keeps **UI clean and user-focused**

---

## 12.5 Frontend: Fetching History and Downloading

```javascript
async function fetchFileHistory(filename) {
  const res = await fetch(`/api/files/${filename}/history`);
  const history = await res.json();

  const tbody = document.querySelector("#history-table tbody");
  tbody.innerHTML = "";
  history.forEach((commit) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
            <td>${commit.commit_hash.slice(0, 7)}</td>
            <td>${commit.author}</td>
            <td>${new Date(commit.date).toLocaleString()}</td>
            <td>${commit.message}</td>
            <td><button onclick="downloadVersion('${filename}', '${
      commit.commit_hash
    }')">Download</button></td>
        `;
    tbody.appendChild(tr);
  });
}

function downloadVersion(filename, commit_hash) {
  window.open(`/api/files/${filename}/history/${commit_hash}`, "_blank");
}
```

**Teaching Points:**

- `fetchFileHistory()` calls the backend and **renders dynamic table rows**
- `commit_hash.slice(0, 7)` → common practice to **shorten hashes**
- `window.open()` triggers **download** without blocking the UI
- Reinforces **asynchronous JS, DOM manipulation, and user-focused design**

---

## 12.6 Diff Viewer (Optional Advanced Feature)

To compare two historical versions:

1. Fetch file contents from both commits
2. Use a JS diff library like **diff.js** or **diff2html**
3. Render a **side-by-side or inline diff view**

```javascript
import { createTwoFilesPatch } from "diff";

const patch = createTwoFilesPatch("v1", "v2", oldContent, newContent);
console.log(patch);
```

**Teaching Points:**

- Shows **line-level differences**
- Reinforces **software engineering practice of code review**
- Integrates backend history with **interactive frontend UI**

---

## 12.7 Security & Best Practices

- Ensure **JWT authorization** for history endpoints
- Validate filenames and commit hashes to prevent **path traversal attacks**
- Serve downloads **over HTTPS** in production
- Rate-limit downloads if necessary for large files

---

## 12.8 Checklist

- [ ] Backend API for file history
- [ ] Backend API for downloading specific historical versions
- [ ] Frontend table modal displaying commit metadata
- [ ] Download button fetches historical file version
- [ ] Optional diff viewer implemented
- [ ] Security validation: JWT, filename, commit hash

---

## ✅ 12.9 Summary

- Section 12 teaches the **core purpose of a PDM system**: historical tracking

- Reinforces:

  - **Git integration for version control**
  - **Backend APIs for historical access**
  - **Frontend dynamic rendering of history**
  - **Security, UX, and software engineering best practices**

- This is the **foundation for advanced features** like **blame view, forced check-in, and audit logs**

---

Section 13 naturally follows as **Blame View / Line Attribution**, which shows **who last modified each line** in a file. This builds on the **history and Git integration concepts** we implemented here.

Perfect! Let’s go **deep into Section 13: Blame View / Line Attribution**, which is a **crucial feature in PDM systems** for tracking responsibility and understanding changes line by line. We’ll cover **backend, Git integration, frontend rendering, UX, and software engineering concepts** thoroughly.

---

# Section 13: Blame View / Line Attribution

---

## 13.0 Introduction

The **Blame View** allows CNC programmers and managers to see **who last modified each line** of a `.mcam` file.

**Purpose:**

- Accountability – know exactly who edited a line
- Debugging – trace when a change was introduced
- Documentation – understand the evolution of a file

**Learning goals:**

- Using Git blame for line-level attribution
- REST API design for detailed structured responses
- Efficiently handling file content in the backend
- Frontend dynamic rendering (highlighting authors, timestamps, and commit hashes)
- UX patterns for large files

---

## 13.1 User Stories

- “As a CNC Programmer, I want to see who last modified each line of a file, so I know who to ask for clarification.”
- “As a Shop Manager, I want to audit changes to ensure accountability.”
- “I want this view to be interactive and easy to navigate, even for large files.”

---

## 13.2 Backend: Git Blame Integration

We’ll use **GitPython** to generate line-by-line attribution.

```python
# git_integration.py
def get_file_blame(file_path: Path):
    """
    Returns a list of dictionaries, each representing a line and who last modified it.
    """
    blame_info = []

    # Using GitPython's blame method
    commits_lines = repo.blame("HEAD", str(file_path))
    # commits_lines returns list of tuples: (Commit, [lines])
    for commit, lines in commits_lines:
        for line in lines:
            blame_info.append({
                "line": line.rstrip("\n"),
                "commit_hash": commit.hexsha,
                "author": commit.author.name,
                "date": commit.committed_datetime.isoformat(),
                "message": commit.message.strip()
            })
    return blame_info
```

**Teaching Points:**

- `repo.blame()` retrieves **line-by-line commit attribution**

- Each tuple = `(Commit, lines)`

- Avoids parsing raw Git output → **safer and more maintainable**

- Metadata returned:

  - `line` → actual content
  - `commit_hash` → unique version reference
  - `author` → name of last editor
  - `date` → timestamp of change
  - `message` → commit message for context

- This reinforces **traceability** and **immutable audit trails**

---

## 13.3 Backend: API Endpoint for Blame

```python
# api/files.py
@router.get("/files/{filename}/blame")
def file_blame(filename: str, user: str = Depends(get_current_user)):
    file_path = REPO_PATH / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    blame_data = get_file_blame(file_path)
    return {"filename": filename, "blame": blame_data}
```

**Teaching Points:**

- REST endpoint design – single responsibility
- Returns **structured JSON**, which frontend can easily parse
- Authentication via `Depends(get_current_user)` ensures **security**

---

## 13.4 Frontend: Rendering Blame View

```html
<div id="blame-modal" class="modal">
  <div class="modal-content">
    <h2>Blame View: <span id="blame-filename"></span></h2>
    <pre id="blame-content"></pre>
    <button class="close-modal">Close</button>
  </div>
</div>
```

- `<pre>` preserves **line breaks and formatting** for `.mcam` files
- Modal keeps the interface **focused** without navigating away

---

## 13.5 Frontend: Fetch & Display

```javascript
async function fetchBlame(filename) {
  const res = await fetch(`/api/files/${filename}/blame`);
  const data = await res.json();

  document.getElementById("blame-filename").textContent = data.filename;

  const blameContent = document.getElementById("blame-content");
  blameContent.innerHTML = "";

  data.blame.forEach((lineData, index) => {
    const lineDiv = document.createElement("div");
    lineDiv.classList.add("blame-line");

    lineDiv.innerHTML = `
            <span class="line-number">${index + 1}</span>
            <span class="author">${lineData.author}</span>
            <span class="commit">${lineData.commit_hash.slice(0, 7)}</span>
            <span class="message">${lineData.message}</span>
            <pre class="line-content">${lineData.line}</pre>
        `;
    blameContent.appendChild(lineDiv);
  });
}
```

**Teaching Points:**

- Displays **author, commit, message, and line content**
- `slice(0,7)` shortens the commit hash → UX-friendly
- Dynamic creation of DOM elements demonstrates **interactive JS patterns**

---

## 13.6 CSS Styling for Blame View

```css
.blame-line {
  display: grid;
  grid-template-columns: 40px 120px 80px 1fr;
  padding: 2px 5px;
  border-bottom: 1px solid #eee;
  font-family: monospace;
  font-size: 0.9em;
}

.blame-line:hover {
  background-color: #f9f9f9;
}

.line-number {
  color: #999;
}

.author {
  color: #007bff;
}

.commit {
  color: #28a745;
}

.message {
  color: #555;
}

.line-content {
  overflow-x: auto;
}
```

**Teaching Points:**

- CSS Grid for aligning **multiple metadata columns**
- `monospace` preserves formatting for `.mcam` files
- Hover effect improves **readability and UX**

---

## 13.7 Advanced Features / Extensions

- **Color coding by author** – visually identify lines contributed by each programmer
- **Filter by author** – only show lines modified by a specific person
- **Click to see commit diff** – open historical diff for a particular line
- **Search within Blame** – integrate with file search

---

## 13.8 Security & Best Practices

- Validate filenames server-side → prevent **path traversal attacks**
- Ensure only **authorized users** can view blame data
- Consider **pagination or lazy loading** for very large files

---

## 13.9 Checklist

- [ ] Backend endpoint returning line-level blame data
- [ ] Git integration via `repo.blame()`
- [ ] Frontend modal showing author, commit, message, and line content
- [ ] CSS grid layout for readability
- [ ] Hover effect and responsive UX
- [ ] Optional: author color coding and commit diff links

---

## ✅ 13.10 Summary

- Section 13 implements the **line-level accountability core to PDM systems**

- Reinforces concepts:

  - Git blame for **fine-grained version control**
  - Backend API design and structured JSON
  - Frontend dynamic DOM rendering
  - UX/UI for readability in technical applications
  - Security and best practices

- Prepares for **Section 14: Real-Time Notifications & WebSockets**, which builds on this data to **push updates live to all users**.

---

We now have **file history + blame view fully functional**, giving the app **industrial-strength auditability**.

Excellent! Section 14 is where the PDM system becomes **truly collaborative**. We’ll dive into **real-time updates**, **WebSockets**, and **push notifications**, fully integrating with all the previous features (file check-in/out, version history, blame). This section emphasizes **software architecture, networking, and frontend-backend interaction**.

---

# Section 14: Real-Time Collaboration & Notifications

---

## 14.0 Introduction

So far, the PDM system works when users **refresh the page** to see updates. But in a **busy CNC shop**, changes happen constantly:

- Multiple programmers may check out/in files simultaneously
- New files can be uploaded
- Admins may override locks

Without **real-time updates**, users risk:

- Working on a file someone else already checked out
- Missing notifications of new files or changes

**Learning goals:**

- Learn **WebSockets** for bidirectional communication
- Integrate **backend events with frontend updates**
- Push **notifications for user subscriptions and file changes**
- Handle **presence tracking** (who is online)
- Understand **network and UX considerations for collaborative apps**

---

## 14.1 User Stories

- “As a CNC Programmer, I want to see file status changes in real-time, so I don’t have to refresh.”
- “I want to get a notification when a Part Family I’m subscribed to is updated.”
- “I want to see who is currently online in the system.”
- “As an Admin, I want to force-check-in a file and have everyone’s UI update immediately.”

---

## 14.2 Backend: Setting Up WebSockets

We will use **FastAPI WebSockets** with **Redis Pub/Sub** for scalability.

```python
# websocket_manager.py
from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()
```

**Teaching Points:**

- `WebSocket.accept()` → establishes a bidirectional connection
- `active_connections` tracks **all connected clients**
- `broadcast()` allows **real-time push to all clients**
- Using a **manager class** is a standard pattern in collaborative apps

---

## 14.3 Backend: WebSocket Endpoint

```python
# api/ws.py
from fastapi import APIRouter, WebSocket, Depends

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Echo or handle incoming messages (optional)
            await manager.broadcast(data)
    except Exception:
        manager.disconnect(websocket)
```

**Teaching Points:**

- `while True` → persistent connection
- Receives **JSON messages** from clients
- Broadcasts to all connected clients → **real-time synchronization**
- Disconnect handling prevents **stale connections**

---

## 14.4 Triggering Real-Time Updates

When a file is checked out/in or uploaded:

```python
async def checkout_file(file_id: str, user: str):
    # ... business logic ...
    await manager.broadcast({
        "event": "file_checked_out",
        "file_id": file_id,
        "user": user
    })
```

**Teaching Points:**

- Event-driven architecture: every **state change emits an event**
- Frontend reacts to these events → **live UI updates**
- This pattern scales to **audit logs, notifications, presence updates**

---

## 14.5 Frontend: WebSocket Client

```javascript
let ws = new WebSocket("ws://localhost:8000/ws");

ws.onopen = () => {
  console.log("Connected to WebSocket server");
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  handleEvent(data);
};

function handleEvent(data) {
  switch (data.event) {
    case "file_checked_out":
      updateFileStatus(data.file_id, "Checked Out", data.user);
      showToast(`${data.user} checked out ${data.file_id}`);
      break;
    case "file_checked_in":
      updateFileStatus(data.file_id, "Available");
      showToast(`${data.user} checked in ${data.file_id}`);
      break;
    case "new_file_uploaded":
      addFileToList(data.file);
      showToast(`New file uploaded: ${data.file.name}`);
      break;
  }
}
```

**Teaching Points:**

- `onmessage` → listens for real-time events
- `switch` statement → dispatches actions based on event type
- `updateFileStatus()` → dynamically updates UI without reload
- `showToast()` → non-blocking notifications for **UX**
- Reinforces **event-driven frontend design**

---

## 14.6 User Presence System

```python
# Add on connect/disconnect
connected_users = set()

async def connect(websocket: WebSocket, user: str):
    await websocket.accept()
    manager.active_connections.append(websocket)
    connected_users.add(user)
    await manager.broadcast({"event": "presence_update", "users": list(connected_users)})

def disconnect(websocket: WebSocket, user: str):
    manager.active_connections.remove(websocket)
    connected_users.discard(user)
```

**Frontend:**

```javascript
case "presence_update":
    updateOnlineUsersList(data.users);
    break;
```

**Teaching Points:**

- Presence tracking → who is **actively online**
- Important for **collaborative awareness**
- Can later extend to **typing indicators, live edits**

---

## 14.7 Notifications System

- Users can **subscribe to Part Families**
- Server emits:

```json
{
  "event": "notification",
  "title": "File Checked In",
  "message": "File 12-34567 checked in by John"
}
```

- Frontend shows **toast notification** or **modal**
- Can store notifications in **Redis or database** for history

---

## 14.8 Security Considerations

- Authenticate WebSocket connections using **JWT token**
- Validate user roles before broadcasting events
- Limit message size → prevent **DoS attacks**

---

## 14.9 Checklist

- [ ] WebSocket connection manager for active clients
- [ ] Backend events emitted for check-in/out, upload, and admin actions
- [ ] Frontend listens and reacts to events
- [ ] Toast notifications implemented
- [ ] User presence tracking
- [ ] Optional: subscription-based notifications
- [ ] Security validation (JWT, role check)

---

## ✅ 14.10 Summary

- Section 14 implements **real-time collaboration**, which is crucial for **multi-user PDM systems**

- Reinforces **networking, WebSockets, event-driven architecture, and UI/UX design**

- Integrates seamlessly with:

  - **File check-in/out**
  - **Version history and blame view**
  - **Notifications and presence**

- Prepares the system for **enterprise-grade multi-user operations**

---

Next, we can move on to **Section 15: Deployment & Scaling**, covering **Docker, CI/CD, and production best practices**, which will take all these features live and scalable.

Do you want to proceed with Section 15 next?
