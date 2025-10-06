Excellent\! With our blueprint in place, we can start moving in.

This first stage is all about **scaffolding**. We're going to move existing code from the monolithic `mastercam_main.py` file into our new structure. We won't change the logic much yet; the primary goal is to organize everything into its proper "room."

Let's begin.

---

### Stage 1.1: Defining Project Dependencies

The first thing we'll create is the `requirements.txt` file.

#### The "Why"

Think of `requirements.txt` as the **ingredient list** for your application. It lists every external Python library your project needs to run.

- **Reproducibility:** This is a crucial concept in software engineering. Anyone (including your future self on a new computer) can take your code, run one command (`pip install -r requirements.txt`), and perfectly replicate the necessary environment. It removes all guesswork.
- **Dependency Management:** It provides a single, clear source of truth for what your project depends on. This is vital for security audits, upgrading libraries, and understanding the project's ecosystem.

#### Your Action Item

Create the file `backend/requirements.txt` and add the following content. I've gone through your original script's imports to identify every external library you need.

```txt
fastapi
uvicorn[standard]
GitPython
requests
pydantic
cryptography
psutil
bcrypt
PyJWT
```

---

### Stage 1.2: Creating the Server Entrypoint

Next, we'll create the `run.py` script. Its only job is to start the web server.

#### The "Why"

This is **Separation of Concerns** in action. The file that defines the application (`app/main.py`, which we'll make next) shouldn't be responsible for the logic of _how_ to run it. The `run.py` script is a simple, dedicated launcher. This separation is professional practice and makes the application more flexible for deployment.

#### Your Action Item

Create the file `backend/run.py` and add this code. This is the logic we're moving from the very bottom of your original `mastercam_main.py` file.

```python
import uvicorn
import webbrowser
import threading
import socket
import logging

# We will create app.main in the next step. This imports the 'app' variable from it.
from app.main import app

logger = logging.getLogger(__name__)

def find_available_port(start_port=8000, max_attempts=100):
  """Finds an open network port by checking ports sequentially."""
  for port in range(start_port, start_port + max_attempts):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      try:
        s.bind(("127.0.0.1", port))
        return port
      except OSError:
        logger.warning(f"Port {port} is in use, trying next...")
  raise IOError("Could not find an available port.")

def main():
  """Main entry point to run the application."""
  try:
    port = find_available_port(8000)
    logger.info(f"Found available port: {port}")

    # Open the web browser automatically after a short delay
    threading.Timer(1.5, lambda: webbrowser.open(f"http://localhost:{port}")).start()

    # Start the Uvicorn server
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")

  except IOError as e:
    logger.error(f"{e} Aborting startup.")
    return
  except Exception as e:
    logger.error(f"An unexpected error occurred during startup: {e}", exc_info=True)

if __name__ == "__main__":
  # This block ensures the code only runs when you execute `python run.py`
  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
  main()
```

---

### Stage 1.3: Creating the Core Application File

Finally for this step, let's create `app/main.py`. This file will be the heart of our web application, responsible for creating the main FastAPI object and attaching high-level configurations like middleware.

#### The "Why"

By moving the FastAPI app definition here, we create a clean, central point for application-wide settings. All the messy details of API endpoints and business logic will be handled elsewhere and imported into this file later. This makes the overall architecture much easier to grasp at a glance.

#### Your Action Item

Create the file `backend/app/main.py` and add the following code, which is extracted from your original script.

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
import sys

# --- NOTE ---
# We will add the 'initialize_application' function back in a later step.
# For now, we are just setting up the structure.
@asynccontextmanager
async def lifespan(app: FastAPI):
  """Handles application startup and shutdown events."""
  logging.info("Application starting up...")
  # await initialize_application() # We'll re-enable this later
  yield
  logging.info("Application shutting down.")


# --- FastAPI App Definition ---
app = FastAPI(
  title="Mastercam GitLab Interface",
  description="A comprehensive file management system for Mastercam and GitLab.",
  version="2.0.0", # Let's call our refactored version 2.0!
  lifespan=lifespan
)


# --- Middleware ---
# CORS (Cross-Origin Resource Sharing) allows the frontend (running on a different "origin")
# to communicate with this backend.
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"], # Allows all origins
  allow_credentials=True,
  allow_methods=["*"], # Allows all methods (GET, POST, etc.)
  allow_headers=["*"], # Allows all headers
)


# --- Static Files ---
# This function helps locate the 'static' and 'templates' folders, especially when
# the app is bundled into an executable.
def resource_path(relative_path):
  """ Get absolute path to resource, works for dev and for PyInstaller """
  base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
  return os.path.join(base_path, relative_path)

# This tells FastAPI to serve files from the 'static' directory (like css, js)
# under the '/static' URL path. We'll need to create this folder later.
# app.mount("/static", StaticFiles(directory=resource_path("static")), name="static")


# --- Root Endpoint ---
# This is a temporary simple endpoint to make sure our server runs.
@app.get("/")
async def root():
  return {"message": "Welcome to the Mastercam PDM Refactored API"}

```

---

We've now successfully laid the groundwork for our backend. We have a dependency list, a server runner, and a central application file. Even though we haven't moved much logic, the project is already infinitely more organized.

Confirm once you've created these three files, and we'll proceed to the next step: isolating all of our Pydantic data models.
