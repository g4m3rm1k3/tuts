Excellent. This next part is one of the most significant upgrades in our entire masterclass. We are about to perform a "heart transplant" on our application. We'll be removing the "mock database" engine and replacing it with a real, functioning Git engine.

The most important goal here is that the **frontend will not change at all**. The user experience should be identical. This demonstrates the power of a well-defined API contract: you can completely revolutionize your backend's internal workings without breaking the client applications that depend on it.

This part will be entirely focused on the backend.

---

### **Part 10: The Real Git Engine (Masterclass Edition)**

**The Goal:** To replace all our in-memory `mock_db` logic with actual Git operations using the powerful `GitPython` library. Our app will now interact directly with a real Git repository on the file system.

---

#### **🚩 Step 1: Setup & Configuration**

First, let's install our new tool and set up the repository our app will manage.

1.  **Install `GitPython`**: In your `backend` directory with the `(venv)` active, run:

    ```bash
    pip install GitPython
    pip freeze > requirements.txt
    ```

2.  **Create the Git Repository**: In the root of your project (`vcs_app/`), create a new directory that will hold the version-controlled files.

    ```bash
    # In vcs_app/
    mkdir repo_data
    cd repo_data
    git init
    ```

    Now, create a couple of dummy files inside `repo_data` so we have something to work with:

    ```bash
    echo "This is the first version of project alpha." > project_alpha.emcam
    echo "Some shared macros go here." > shared_macros.emlib
    git add .
    git commit -m "Initial repository setup"
    ```

3.  **Create a Configuration File**: It's bad practice to hardcode paths in your application logic. Let's create a central place for configuration. In your `backend` directory, create `config.py`:

    ```python
    # backend/config.py
    import os

    # Go up one level from the backend directory to the project root
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPO_PATH = os.path.join(PROJECT_ROOT, "repo_data")
    ```

---

#### **🚩 Step 2: The Service Layer Abstraction**

We will not put Git logic directly into our `main.py` API routes. That would mix our web layer with our business logic layer. Instead, we'll create an abstraction—a **service layer**—that handles all Git operations.

Create a new directory and file: `backend/services/git_service.py`.

```python
# backend/services/git_service.py
import os
import git
from datetime import datetime
from config import REPO_PATH

# Initialize the repository object
repo = git.Repo(REPO_PATH)

def get_all_files():
    # ... we will implement this ...
    pass

# ... other functions will go here ...
```

🔑 **Transferable Skill**: Separating your application into layers (e.g., API/Routing Layer, Service/Business Logic Layer, Data Layer) is a cornerstone of professional software architecture. It makes your code cleaner, easier to test, and vastly more maintainable.

---

#### **🚩 Step 3: Refactoring "List Files"**

Let's implement the first real function. We need to get the status of all files in our `repo_data` directory.

In `git_service.py`, implement `get_all_files`:

```python
# backend/services/git_service.py
# ... (imports and repo init) ...

def _get_file_details(filename):
    """Helper function to get details for a single file."""
    filepath = os.path.join(REPO_PATH, filename)
    lock_path = f"{filepath}.lock"

    status = "unlocked"
    locked_by = None
    locked_at = None

    if os.path.exists(lock_path):
        status = "locked"
        with open(lock_path, 'r') as f:
            lock_data = f.read().split(',')
            locked_by = lock_data[0]
            locked_at = datetime.fromisoformat(lock_data[1])

    # Get revision and modified_at from the latest git commit for this file
    latest_commit = next(repo.iter_commits(paths=filepath, max_count=1), None)

    return {
        "filename": filename,
        "description": "Description from DB (later)", # Placeholder
        "status": status,
        "revision": latest_commit.count() if latest_commit else 1,
        "size": os.path.getsize(filepath),
        "modified_at": datetime.fromtimestamp(latest_commit.committed_date) if latest_commit else datetime.now(),
        "locked_by": locked_by,
        "locked_at": locked_at,
    }

def get_all_files():
    """Returns a list of details for all tracked files."""
    files = []
    # List files tracked by Git, excluding submodules
    for item in repo.tree().traverse():
        if item.type == 'blob': # 'blob' means it's a file
            files.append(_get_file_details(item.path))
    return files
```

🔎 **Deep Explanation - The "Lock" File**: Git itself doesn't have a file-locking mechanism like centralized systems (Perforce, SVN). We simulate it using a common pattern: creating an empty "lock" file (`myfile.txt.lock`). If this file exists, the file is considered locked. The lock file itself can contain information about who locked it and when. This is a simple but effective concurrency control strategy.

---

#### **🚩 Step 4: Connecting the Service to the API**

Now, we replace the mock data call in `main.py` with a call to our new service.

```python
# backend/main.py
# 1. Remove mock_db import, import the new service
from services import git_service
# ... other imports ...

@app.get("/api/files", response_model=List[File])
async def list_files():
    # 2. Replace the call to the mock database
    return git_service.get_all_files()

# ... (rest of the file will be updated step-by-step) ...
```

If you restart your server now and load the webpage, it should already be working, but this time, it's pulling real data from your Git repository directory\!

---

#### **🚩 Step 5: Refactoring the "Write" Operations**

Now, we'll implement the logic for the `POST` and `DELETE` actions in `git_service.py` and then wire them up in `main.py`. This involves creating and deleting our `.lock` files, and using `repo.index.commit` to create new versions.

It's a lot of code, but the pattern is the same for each function:

1.  Define the logic in `git_service.py`.
2.  Call the service function from the corresponding endpoint in `main.py`.

_You can now go through each of your endpoints in `main.py` (`checkout_file`, `cancel_checkout`, `checkin_file`, `delete_file`, etc.) and replace the mock DB logic with the equivalent call to a new function you'll write in `git_service.py`._

Here is the complete `git_service.py` with all the logic:

\<details\>
\<summary\>Click to see the complete git_service.py\</summary\>

```python
# backend/services/git_service.py
import os
import git
import shutil
from datetime import datetime
from config import REPO_PATH
from fastapi import UploadFile

# Custom exception for business logic errors
class GitServiceError(Exception):
    pass

repo = git.Repo(REPO_PATH)

def _get_file_details(filename):
    # ... (same as before) ...

def get_all_files():
    # ... (same as before) ...

def checkout_file(filename, user="test_user"):
    filepath = os.path.join(REPO_PATH, filename)
    lock_path = f"{filepath}.lock"
    if not os.path.exists(filepath):
        raise GitServiceError("File not found")
    if os.path.exists(lock_path):
        raise GitServiceError("File is already locked")

    with open(lock_path, 'w') as f:
        f.write(f"{user},{datetime.now().isoformat()}")
    return _get_file_details(filename)

def cancel_checkout(filename, user="test_user"):
    filepath = os.path.join(REPO_PATH, filename)
    lock_path = f"{filepath}.lock"
    if not os.path.exists(lock_path):
        raise GitServiceError("File is not locked")
    # In a real app, you'd check if `user` is the one who locked it.
    os.remove(lock_path)
    return _get_file_details(filename)

def checkin_file(filename: str, file: UploadFile, comment: str, user="test_user"):
    filepath = os.path.join(REPO_PATH, filename)
    lock_path = f"{filepath}.lock"
    if not os.path.exists(lock_path):
        raise GitServiceError("File must be checked out to check in")

    # Save the uploaded file, overwriting the old one
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Git add and commit
    repo.index.add([filepath])
    commit_message = f"[{user}] {comment}"
    repo.index.commit(commit_message)

    # Remove the lock
    os.remove(lock_path)
    return _get_file_details(filename)

def get_file_history(filename):
    filepath = os.path.join(REPO_PATH, filename)
    history = []
    for commit in repo.iter_commits(paths=filepath):
        history.append({
            "revision": commit.count(),
            "comment": commit.message.strip(),
            "user": str(commit.author),
            "timestamp": datetime.fromtimestamp(commit.committed_date)
        })
    return history

def delete_file(filename):
    filepath = os.path.join(REPO_PATH, filename)
    if not os.path.exists(filepath):
        raise GitServiceError("File not found")

    repo.index.remove([filepath])
    repo.index.commit(f"[admin] Deleted file: {filename}")
    # The file is removed by the commit, no need for os.remove
    return True

# Override is just a cancel action with different permissions,
# so we can reuse the logic for now.
override_lock = cancel_checkout

```

\</details\>

Your final `main.py` will be much cleaner, acting only as a routing layer that translates HTTP requests and exceptions into service layer calls.

---

#### **✅ Recap**

This was a monumental backend refactoring. The application is now real. You have learned:

- How to use the **`GitPython`** library to programmatically interact with a repository.
- The critical architectural pattern of a **Service Layer** to separate business logic from the web layer.
- How to use a **config file** to manage application settings like file paths.
- A practical strategy for simulating **file locking** in a Git-based system.
- The power of a stable API contract, allowing for a complete backend overhaul with **zero changes to the frontend**.

#### **📌 What's Next:**

Our application is now fully functional and real. But Git isn't a database. What if we want to store descriptions for our files? Or manage user permissions? Committing a file just to change its description is inefficient. In **Part 11**, we will address this by integrating a lightweight **SQLite database** using **SQLAlchemy** to manage the metadata _about_ our files, making our application truly robust.
