# Analyzing Your `run.py` - The Application Launcher

## What This File Does

**Purpose:** This is your application's **entry point** - the file you run to start everything. It's NOT the app itself, it's the launcher that:

1. Finds an available port (so you can run multiple instances)
2. Starts the server
3. Opens your browser automatically

Think of it like the ignition switch for your car - it's not the engine, but it starts the engine.

---

## Walking Through Your Code

### The Imports Section

```python
import uvicorn        # ASGI server that runs FastAPI
import webbrowser     # Opens browser automatically
import threading      # For delayed browser opening
import socket         # For checking if ports are available
import logging        # For proper logging instead of print()
```

**What's good here:**

- ✅ Using `logging` instead of `print()` - professional applications use logging
- ✅ All imports are from standard library (except uvicorn) - minimal dependencies

---

### The Port Finding Logic

```python
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
```

**Let me explain what's happening:**

**`range(start_port, start_port + max_attempts)`**

- Tries ports 8000, 8001, 8002... up to 8099 (100 attempts)
- Why? If you're running another app on 8000, it'll find 8001

**`with socket.socket(...) as s:`**

- This is a **context manager** - automatically closes the socket when done
- `AF_INET` = IPv4, `SOCK_STREAM` = TCP connection

**`s.bind(("127.0.0.1", port))`**

- Tries to claim the port
- If successful, nothing is using it - return this port
- If fails (OSError), something is using it - try next port

**Why this is clever:**

- Multi-developer teams can all run the app simultaneously
- No "port already in use" errors

---

### The Main Function

```python
def main():
    """Main entry point to run the application."""
    try:
        port = find_available_port(8000)
        logger.info(f"Found available port: {port}")

        threading.Timer(1.5, lambda: webbrowser.open(
            f"http://localhost:{port}")).start()

        # Pass the app location as a string
        uvicorn.run("app.main:app", host="127.0.0.1",
                    port=port, log_level="info")

    except IOError as e:
        logger.error(f"{e} Aborting startup.")
        return
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during startup: {e}", exc_info=True)
```

**Key line: `uvicorn.run("app.main:app", ...)`**

**Why the string `"app.main:app"` instead of importing directly?**

```python
# WRONG way (for hot-reload):
from app.main import app
uvicorn.run(app, ...)  # Won't auto-reload properly

# RIGHT way:
uvicorn.run("app.main:app", ...)  # Can reload the module
```

When you pass a string:

- Uvicorn imports the module itself
- Can watch for file changes
- Can reload the module without restarting the process
- Essential for development with `reload=True`

**The browser opening:**

```python
threading.Timer(1.5, lambda: webbrowser.open(
    f"http://localhost:{port}")).start()
```

- Waits 1.5 seconds, then opens browser
- Uses threading so it doesn't block the server startup
- `lambda:` is an anonymous function (shorthand for a simple function)

---

### The Entry Point Guard

```python
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    main()
```

**`if __name__ == "__main__":`** - This is crucial!

**When you run `python run.py`:**

- Python sets `__name__ = "__main__"`
- This block executes

**When another file does `import run`:**

- Python sets `__name__ = "run"`
- This block does NOT execute
- Prevents the server from starting unintentionally

**`logging.basicConfig(...)`:**

- Sets up logging format: timestamp, level, message
- Only needs to be done once at startup

---

## Issues and Improvements

### Issue 1: Browser Opens Before Server is Ready

**The problem:**

```python
threading.Timer(1.5, lambda: webbrowser.open(...)).start()
uvicorn.run(...)  # Might take 2+ seconds to start
```

If your app is slow to start (loading Git repo, etc.), the browser opens to an error page.

**Better approach:** Let uvicorn handle it, or wait longer.

---

### Issue 2: No Auto-Reload for Development

For development, you want auto-reload when you change code.

---

## Your Improved and Commented `run.py`

```python
"""
Application launcher - Finds an available port and starts the server.

This file is the entry point for running the application. It handles:
- Finding an available network port
- Starting the Uvicorn ASGI server
- Opening the browser automatically

Usage: python run.py
"""

import uvicorn
import webbrowser
import threading
import socket
import logging
import os

logger = logging.getLogger(__name__)


def find_available_port(start_port=8000, max_attempts=100):
    """
    Finds an available network port by checking sequentially.

    Args:
        start_port: Port to start checking from (default: 8000)
        max_attempts: How many ports to try before giving up (default: 100)

    Returns:
        int: An available port number

    Raises:
        IOError: If no available port is found within max_attempts

    How it works:
        - Tries to bind a socket to each port
        - If successful, that port is available
        - If OSError, port is in use, try next one
    """
    for port in range(start_port, start_port + max_attempts):
        # Create a TCP socket using IPv4
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                # Try to bind to this port on localhost
                s.bind(("127.0.0.1", port))
                logger.info(f"Port {port} is available")
                return port
            except OSError:
                # Port is in use, try next one
                logger.debug(f"Port {port} is in use, trying next...")

    # Exhausted all attempts
    raise IOError(
        f"Could not find an available port after {max_attempts} attempts. "
        f"Tried ports {start_port}-{start_port + max_attempts - 1}"
    )


def main():
    """
    Main entry point to run the application.

    This function:
    1. Finds an available port
    2. Schedules browser to open after server starts
    3. Starts the Uvicorn server
    4. Handles startup errors gracefully
    """
    try:
        # Find an available port (tries 8000 first, then 8001, 8002, etc.)
        port = find_available_port(8000)
        logger.info(f"Starting server on port {port}")

        # Determine if we're in development mode
        # In production, you'd set ENVIRONMENT=production
        is_dev = os.getenv("ENVIRONMENT", "development") == "development"

        # Open browser after server starts (2 seconds should be enough)
        # Only do this in development - production servers shouldn't open browsers!
        if is_dev:
            threading.Timer(
                2.0,  # Wait 2 seconds for server to fully start
                lambda: webbrowser.open(f"http://localhost:{port}")
            ).start()
            logger.info(f"Browser will open at http://localhost:{port} in 2 seconds...")

        # Start the Uvicorn server
        # NOTE: We pass "app.main:app" as a STRING, not imported directly
        # This is crucial for hot-reload to work properly
        uvicorn.run(
            "app.main:app",           # Module path to the FastAPI app
            host="127.0.0.1",         # Only accept local connections (secure for dev)
            port=port,                # Use the port we found
            reload=is_dev,            # Auto-reload on code changes (dev only)
            log_level="info"          # Show INFO level logs and above
        )

    except IOError as e:
        # Couldn't find an available port
        logger.error(f"Port finding failed: {e}")
        logger.error("Try closing other applications or specify a different port range.")
        return

    except Exception as e:
        # Catch any other unexpected errors
        logger.error(
            f"An unexpected error occurred during startup: {e}",
            exc_info=True  # Include full stack trace in logs
        )


if __name__ == "__main__":
    """
    Entry point guard - only runs when executing this file directly.

    If another module does 'import run', this block won't execute.
    This prevents the server from accidentally starting when imported.
    """

    # Configure logging for the entire application
    logging.basicConfig(
        level=logging.INFO,  # Show INFO, WARNING, ERROR, CRITICAL
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        # Added %(name)s to see which module logged each message
    )

    # Print a nice startup message
    logger.info("=" * 50)
    logger.info("Mastercam PDM Server Starting...")
    logger.info("=" * 50)

    # Start the application
    main()
```

---

## Key Improvements Made

### 1. Added Environment Detection

```python
is_dev = os.getenv("ENVIRONMENT", "development") == "development"
```

**Why?** In production, you don't want browsers opening on the server!

**Usage:**

- Development: `python run.py` (browser opens)
- Production: `ENVIRONMENT=production python run.py` (no browser)

---

### 2. Added Auto-Reload

```python
reload=is_dev,  # Auto-reload on code changes (dev only)
```

**Now when you edit code, the server restarts automatically!**

**Why only in dev?** Production restarts are handled by process managers (systemd, supervisor, etc.)

---

### 3. Better Error Messages

```python
raise IOError(
    f"Could not find an available port after {max_attempts} attempts. "
    f"Tried ports {start_port}-{start_port + max_attempts - 1}"
)
```

**Before:** "Could not find an available port"
**After:** "Could not find an available port after 100 attempts. Tried ports 8000-8099"

**Better for debugging!**

---

### 4. Longer Browser Delay

```python
threading.Timer(2.0, ...)  # Changed from 1.5 to 2.0
```

**Gives server more time to start before opening browser.**

---

## Testing Your Improved run.py

**Replace your `run.py` with the improved version above.**

**Test 1: Normal startup**

```bash
python run.py
```

**Should see:**

```
2024-10-11 10:30:00 - __main__ - INFO - ==================================================
2024-10-11 10:30:00 - __main__ - INFO - Mastercam PDM Server Starting...
2024-10-11 10:30:00 - __main__ - INFO - ==================================================
2024-10-11 10:30:00 - __main__ - INFO - Port 8000 is available
2024-10-11 10:30:00 - __main__ - INFO - Starting server on port 8000
2024-10-11 10:30:00 - __main__ - INFO - Browser will open at http://localhost:8000 in 2 seconds...
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

**Browser should open after 2 seconds.**

---

**Test 2: Port already in use**

Open TWO terminals, run `python run.py` in both.

**First one:** Uses port 8000
**Second one:** Should find port 8001

---

**Test 3: Auto-reload**

With the server running, edit `app/main.py` (add a comment or space).

**Should see:**

```
INFO:     Detected file change, reloading...
```

**Server restarts automatically!**

---

## Questions to Test Your Understanding

**Q1:** Why do we use `"app.main:app"` as a string instead of importing the app directly?

**Q2:** What would happen if we removed the `if __name__ == "__main__":` guard?

**Q3:** Why do we use `with socket.socket(...)` instead of just `socket.socket(...)`?

**Q4:** In production, would you want `reload=True`? Why or why not?

---

## What's Next?

**You have a working, well-commented launcher!**

**Next file to review:** Your `app/main.py` - the actual FastAPI application.

**When you're ready, share your `app/main.py` and I'll:**

- Explain how FastAPI apps are structured
- Show you how routers work
- Fix any issues
- Add helpful comments

**Ready to move to the next file?**
