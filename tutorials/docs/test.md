### Tutorial: File Management, Locking, and Repository Services in Python

This tutorial walks through **building a file management system** with **locking**, **repository operations**, and a **combined service** that merges both. Each section builds incrementally with explanations, common pitfalls, and deeper notes.

---

#### Section I: Lock Management

We want a system to ensure **only one user can modify a file at a time**, preventing conflicts in multi-user or multi-process environments.

##### Step 1: Class setup

```python
from pathlib import Path
from typing import Dict, Optional
import json
import logging

from app.utils.file_locking import LockedFile

logger = logging.getLogger(__name__)

class LockManager:
    """
    Manages file lock state.

    Stores locks in a JSON file with atomic read/write operations.
    """
```

**Explanation:**

- `Path` → modern way to handle filesystem paths.
- `Dict`, `Optional` → type hints, improves readability and static analysis.
- `json` → storing locks in a human-readable JSON file.
- `LockedFile` → context manager to safely lock the JSON file during read/write operations. Prevents race conditions.
- `logger` → structured logging is crucial for debugging concurrent access.

**Gotchas / Notes:**

- **Imports inside class methods** (`from datetime import datetime`) can cause issues with tools like **PyInstaller** because static analysis may not detect them. Consider moving imports to the top.
- Using JSON as storage is simple but **not suitable for very high-concurrency scenarios**; a database may be better.

---

##### Step 2: Constructor

```python
def __init__(self, locks_file: Path):
    self.locks_file = locks_file

    ### Ensure file exists
    if not self.locks_file.exists():
        self.locks_file.write_text('{}')
```

- Ensures a lock file exists before using it.
- Writing `'{}'` guarantees `json.load` won’t fail on an empty file.

**Python Concepts:**

- `write_text` → writes string content to a file; will create the file if it doesn’t exist.
- Using `Path` methods avoids OS-specific path issues.

---

##### Step 3: Loading locks

```python
def load_locks(self) -> Dict[str, dict]:
    if not self.locks_file.exists():
        return {}

    try:
        with LockedFile(self.locks_file, 'r') as f:
            content = f.read()
            if not content.strip():
                return {}
            return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse locks file: {e}")
        return {}
    except Exception as e:
        logger.error(f"Failed to load locks: {e}")
        return {}
```

**Explanation:**

- Acquires a **file lock** using `LockedFile`.
- Reads the JSON content and returns a dictionary mapping filenames → lock info.
- Handles empty files and JSON parsing errors gracefully.

**Gotchas:**

- Always handle `JSONDecodeError` to avoid crashing when the file is corrupted.
- `LockedFile` ensures **atomic read/write**, preventing race conditions if multiple processes access the file.

**Extra Concept:**

- `try/except` blocks are essential in file I/O. Returning an empty dict allows the system to continue instead of failing.

---

##### Step 4: Saving locks

```python
def save_locks(self, locks: dict):
    try:
        with LockedFile(self.locks_file, 'w') as f:
            json.dump(locks, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save locks: {e}")
        raise
```

- Opens the file with a lock, writes updated lock data.
- Raises exception if saving fails — important to prevent **silent lock inconsistencies**.

**Gotcha:** Never write locks without a file lock; concurrent writes can corrupt the file.

---

##### Step 5: Checking lock state

```python
def is_locked(self, filename: str) -> bool:
    locks = self.load_locks()
    return filename in locks

def get_lock_info(self, filename: str) -> Optional[dict]:
    locks = self.load_locks()
    return locks.get(filename)
```

- `is_locked` → returns `True` if the file has a lock.
- `get_lock_info` → returns lock details (user, timestamp, message).

**Python Tip:**

- Using `.get()` avoids KeyError when the file isn’t locked.

---

##### Step 6: Acquiring and releasing locks

```python
def acquire_lock(self, filename: str, user: str, message: str):
    locks = self.load_locks()
    if filename in locks:
        existing = locks[filename]
        raise ValueError(f"File already locked by {existing['user']}")
    from datetime import datetime, timezone
    locks[filename] = {
        'user': user,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'message': message
    }
    self.save_locks(locks)
    logger.info(f"Lock acquired: {filename} by {user}")

def release_lock(self, filename: str, user: str):
    locks = self.load_locks()
    if filename not in locks:
        raise ValueError("File is not locked")
    if locks[filename]['user'] != user:
        raise ValueError(f"Lock owned by {locks[filename]['user']}, not {user}")
    del locks[filename]
    self.save_locks(locks)
    logger.info(f"Lock released: {filename} by {user}")
```

**Explanation:**

- `acquire_lock` → checks if already locked, raises `ValueError` if so. Otherwise, adds lock info.
- `release_lock` → checks ownership before releasing; ensures only the lock owner can release it.

**Gotchas / Notes:**

- Always verify ownership before releasing a lock — prevents users from accidentally unlocking files they don’t own.
- Timestamp uses **UTC** for consistency in multi-timezone environments.
- Frequent `load_locks()` calls ensure latest state but may have **performance overhead** in very large repositories.

---

#### Section II: File Repository

Handles **filesystem operations** for your repository.

##### Step 1: Setup

```python
class FileRepository:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.repo_path.mkdir(parents=True, exist_ok=True)
```

- Ensures repository directory exists.
- `mkdir(parents=True, exist_ok=True)` → creates intermediate folders safely.

---

##### Step 2: Listing files with metadata

```python
def list_files(self, extension: str = '.mcam') -> List[Dict]:
    files = []
    for item in self.repo_path.iterdir():
        if not item.is_file():
            continue
        if not item.name.lower().endswith(extension):
            continue
        stat = item.stat()
        files.append({
            'name': item.name,
            'size_bytes': stat.st_size,
            'modified': stat.st_mtime,
        })
    return files
```

- Uses `iterdir()` → efficient iterator over directory contents.
- `stat()` → lightweight way to get file size and modified timestamp.
- Filters by extension, ignoring directories.

**Gotchas:**

- `item.name.lower()` ensures `.MCAM` is recognized as `.mcam`.
- `stat().st_mtime` is seconds since epoch — may need conversion to human-readable datetime.

---

##### Step 3: Helper methods

```python
def file_exists(self, filename: str) -> bool:
    return (self.repo_path / filename).exists()

def get_file_path(self, filename: str) -> Path:
    return self.repo_path / filename

def read_file(self, filename: str) -> bytes:
    return self.get_file_path(filename).read_bytes()

def write_file(self, filename: str, content: bytes):
    self.get_file_path(filename).write_bytes(content)
```

- `file_exists` → quick existence check.
- `read_bytes` / `write_bytes` → read/write entire file content.

**Python Tip:** Using `Path` instead of `open()` is simpler and cross-platform.

---

#### Section III: Combined File Service

This class **combines repository + locks** to provide high-level operations.

##### Step 1: Constructor

```python
class FileService:
    def __init__(self, repo_path: Path, locks_file: Path):
        self.repository = FileRepository(repo_path)
        self.lock_manager = LockManager(locks_file)
```

- Encapsulates both repository and lock manager.
- Encourages **separation of concerns**: repository handles filesystem, lock manager handles concurrency.

---

##### Step 2: Files with status

```python
def get_files_with_status(self) -> List[Dict]:
    files = self.repository.list_files()
    locks = self.lock_manager.load_locks()
    result = []
    for file_info in files:
        filename = file_info['name']
        lock_info = locks.get(filename)
        result.append({
            'name': filename,
            'size_bytes': file_info['size_bytes'],
            'status': 'checked_out' if lock_info else 'available',
            'locked_by': lock_info['user'] if lock_info else None,
        })
    return result
```

- Combines file metadata with lock state for display or API purposes.

**Gotchas:**

- Frequent `load_locks()` reads ensure up-to-date status but can be slow with many files.
- Optional chaining (`lock_info['user'] if lock_info else None`) avoids KeyError.

---

##### Step 3: Checkout / Checkin

```python
def checkout_file(self, filename: str, user: str, message: str):
    if not self.repository.file_exists(filename):
        raise ValueError(f"File not found: {filename}")
    self.lock_manager.acquire_lock(filename, user, message)

def checkin_file(self, filename: str, user: str):
    self.lock_manager.release_lock(filename, user)
```

- `checkout_file` → verify file exists, acquire lock.
- `checkin_file` → release lock safely.

**Python Concept:** By combining repository + lock manager, you create a **transactional workflow**: file access and locking are guaranteed to stay in sync.

---

##### ✅ Key Takeaways

- **File locking** prevents race conditions in multi-user / multi-process environments.
- **Pathlib** is modern and safer than raw strings for file operations.
- **Atomic JSON operations** are crucial when multiple processes read/write the same file.
- **Separation of concerns**: repository handles files, lock manager handles concurrency, combined service orchestrates both.

---

## Incremental Coding Tutorial: File Management with Locking

---

### SECTION I: Lock Management

#### Step 1: Imports and Logger

```python
from pathlib import Path
from typing import Dict, Optional
import json
import logging

from app.utils.file_locking import LockedFile

logger = logging.getLogger(__name__)
```

**Explanation:**

- `Path` → Modern path handling; cross-platform.
- `Dict` / `Optional` → Type hints improve readability and help static checkers.
- `json` → store lock state in a human-readable file.
- `logging` → structured logging, essential for debugging.
- `LockedFile` → context manager to safely lock JSON files during read/write. Prevents race conditions.

**Gotchas / Notes:**

- Make sure `LockedFile` is imported at the top. Imports inside functions or classes may break **PyInstaller** because it relies on static analysis.

---

#### Step 2: Start the LockManager Class

```python
class LockManager:
    """
    Manages file lock state.

    Stores locks in a JSON file with atomic read/write operations.
    """
```

- Encapsulates **all lock logic** in one class.
- Using a class makes it easy to reuse in multiple places, e.g., different services or scripts.

---

#### Step 3: Constructor

```python
def __init__(self, locks_file: Path):
    self.locks_file = locks_file

    ## Ensure file exists
    if not self.locks_file.exists():
        self.locks_file.write_text('{}')
```

**Explanation:**

- Stores path to the lock file.
- Creates an empty JSON `{}` if the file doesn’t exist. This avoids errors on `json.load`.

**Python Concepts:**

- `write_text()` → convenient for writing string content to a file.
- Using `Path` ensures paths are OS-independent.

**Gotcha:** Don’t forget to check file permissions. If Python can’t write the file, the code will fail silently here.

---

#### Step 4: Load Locks

```python
def load_locks(self) -> Dict[str, dict]:
    if not self.locks_file.exists():
        return {}

    try:
        with LockedFile(self.locks_file, 'r') as f:
            content = f.read()
            if not content.strip():
                return {}
            return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse locks file: {e}")
        return {}
    except Exception as e:
        logger.error(f"Failed to load locks: {e}")
        return {}
```

**Explanation:**

- `LockedFile` ensures **atomic access** to prevent concurrent read/write issues.
- `content.strip()` → handles empty files.
- `json.loads()` → converts string JSON into a Python dictionary.

**Gotchas:**

- Always handle `JSONDecodeError` — corrupted files are common when multiple processes write at the same time.

**Extra Concept:**

- Using `return {}` for errors allows the application to **continue running**, instead of crashing.

---

#### Step 5: Save Locks

```python
def save_locks(self, locks: dict):
    try:
        with LockedFile(self.locks_file, 'w') as f:
            json.dump(locks, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save locks: {e}")
        raise
```

- Writes the updated lock dictionary back to file safely.
- `indent=2` → makes JSON human-readable.

**Gotchas:** Never write locks without a **file lock**, or simultaneous writes will corrupt the file.

---

#### Step 6: Check Lock State

```python
def is_locked(self, filename: str) -> bool:
    locks = self.load_locks()
    return filename in locks

def get_lock_info(self, filename: str) -> Optional[dict]:
    locks = self.load_locks()
    return locks.get(filename)
```

- `is_locked` → returns True if the file has a lock.
- `get_lock_info` → returns lock metadata (user, timestamp, message) or `None`.

**Python Tip:** `.get()` avoids `KeyError` for missing keys.

---

#### Step 7: Acquire and Release Locks

```python
def acquire_lock(self, filename: str, user: str, message: str):
    locks = self.load_locks()
    if filename in locks:
        existing = locks[filename]
        raise ValueError(f"File already locked by {existing['user']}")

    from datetime import datetime, timezone
    locks[filename] = {
        'user': user,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'message': message
    }
    self.save_locks(locks)
    logger.info(f"Lock acquired: {filename} by {user}")

def release_lock(self, filename: str, user: str):
    locks = self.load_locks()
    if filename not in locks:
        raise ValueError("File is not locked")
    if locks[filename]['user'] != user:
        raise ValueError(f"Lock owned by {locks[filename]['user']}, not {user}")
    del locks[filename]
    self.save_locks(locks)
    logger.info(f"Lock released: {filename} by {user}")
```

- `acquire_lock` → checks existing locks, stores user, timestamp, message.
- `release_lock` → ensures **only the owner** can release a lock.
- `datetime.now(timezone.utc)` → use UTC for consistency across time zones.

**Gotchas:**

- Always verify ownership before releasing a lock.
- Frequent `load_locks()` reads ensure latest state but may impact performance for large repositories.

---

### SECTION II: File Repository

#### Step 1: Repository Class

```python
class FileRepository:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.repo_path.mkdir(parents=True, exist_ok=True)
```

- Ensures the repository folder exists.
- `mkdir(parents=True, exist_ok=True)` creates intermediate directories safely.

---

#### Step 2: List Files

```python
def list_files(self, extension: str = '.mcam') -> list[dict]:
    files = []
    for item in self.repo_path.iterdir():
        if not item.is_file():
            continue
        if not item.name.lower().endswith(extension):
            continue
        stat = item.stat()
        files.append({
            'name': item.name,
            'size_bytes': stat.st_size,
            'modified': stat.st_mtime,
        })
    return files
```

- Iterates through the directory.
- Filters **files only**, matches extension, gets metadata.
- `stat()` → fast access to file info.

---

#### Step 3: Helper Methods

```python
def file_exists(self, filename: str) -> bool:
    return (self.repo_path / filename).exists()

def get_file_path(self, filename: str) -> Path:
    return self.repo_path / filename

def read_file(self, filename: str) -> bytes:
    return self.get_file_path(filename).read_bytes()

def write_file(self, filename: str, content: bytes):
    self.get_file_path(filename).write_bytes(content)
```

- Encapsulates file operations.
- Using `Path` methods makes it **cross-platform**.

---

### SECTION III: Combined File Service

#### Step 1: Service Constructor

```python
class FileService:
    def __init__(self, repo_path: Path, locks_file: Path):
        self.repository = FileRepository(repo_path)
        self.lock_manager = LockManager(locks_file)
```

- Orchestrates **repository + lock manager**.
- Keeps code modular.

---

#### Step 2: Files with Status

```python
def get_files_with_status(self) -> list[dict]:
    files = self.repository.list_files()
    locks = self.lock_manager.load_locks()
    result = []
    for file_info in files:
        filename = file_info['name']
        lock_info = locks.get(filename)
        result.append({
            'name': filename,
            'size_bytes': file_info['size_bytes'],
            'status': 'checked_out' if lock_info else 'available',
            'locked_by': lock_info['user'] if lock_info else None,
        })
    return result
```

- Combines **file metadata + lock state**.
- Ideal for APIs or UI display.

---

#### Step 3: Checkout / Checkin

```python
def checkout_file(self, filename: str, user: str, message: str):
    if not self.repository.file_exists(filename):
        raise ValueError(f"File not found: {filename}")
    self.lock_manager.acquire_lock(filename, user, message)

def checkin_file(self, filename: str, user: str):
    self.lock_manager.release_lock(filename, user)
```

- Simple, high-level methods to **manage file access safely**.
- Throws `ValueError` if file doesn’t exist or lock is invalid.

---

✅ **Next Steps / Practice**

- Add **unit tests** for LockManager to simulate multiple users trying to acquire/release locks.
- Try **checking files in/out** from multiple scripts to see the locks in action.
- Consider **FileLock library** as a cross-platform alternative if you run into weird locking behavior on Windows
