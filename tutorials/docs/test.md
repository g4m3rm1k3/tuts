## Tutorial: File Locking in Python with `filelock`

File locking is an essential technique when multiple processes or threads need **safe, exclusive access** to a resource — in our case, a `locks.json` file tracking checked-out files. Python provides low-level options (`fcntl`, `msvcrt`) but they are platform-specific. The [`filelock`](https://pypi.org/project/filelock/) library abstracts those details and provides a simple, cross-platform interface.

We’ll cover:

1. **Why file locks are necessary**
2. **Installation and basic usage**
3. **Context managers in Python**
4. **Refactoring your custom `LockedFile`**
5. **Integrating `filelock` into FastAPI file checkout/checkin**
6. **Advanced usage: timeouts, exceptions, and best practices**
7. **Common pitfalls and gotchas**

---

### 1. Why File Locks are Necessary

Imagine two users trying to checkout the same CAM file at the same time:

```text
User A reads locks.json -> sees file is available
User B reads locks.json -> also sees file is available
User A writes lock -> file now locked
User B writes lock -> overwrites User A's lock!
```

This is called a **race condition** — multiple processes accessing a shared resource simultaneously without proper synchronization. **Locks prevent this.**

Concepts introduced:

- **Critical section:** Code that must not be run by multiple processes at the same time.
- **Mutex:** Mutual exclusion, a mechanism to protect critical sections.
- **Deadlock:** When two processes wait on each other’s locks forever. Can happen if we are careless with lock acquisition order or timeouts.

---

### 2. Installing `filelock`

Install via `pip`:

```bash
pip install filelock
```

You now have the `FileLock` class for cross-platform file locking.

---

### 3. Basic Usage

```python
from filelock import FileLock
import json

LOCK_FILE = "locks.json.lock"

with FileLock(LOCK_FILE):
    with open("locks.json", "r+") as f:
        locks = json.load(f)
        # Modify locks safely
        locks["file1.mcam"] = {"user": "Alice"}
        f.seek(0)
        json.dump(locks, f, indent=4)
        f.truncate()
```

**Key points:**

- The `.lock` file acts as a **mutex**.
- The `with` statement ensures that the lock is **acquired** and automatically **released**.
- `f.seek(0)` and `f.truncate()` ensure the file is **overwritten safely**.

---

### 4. Context Managers in Python

`FileLock` works as a **context manager** using the `__enter__` and `__exit__` methods:

```python
class MyContext:
    def __enter__(self):
        print("Entering")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting")
        if exc_type:
            print(f"Exception: {exc_type}, {exc_val}")
        return False  # False means propagate exception
```

- `__enter__` → code executed when entering `with` block.
- `__exit__` → code executed on exit, receives:

  - `exc_type` → exception class (e.g., `FileNotFoundError`)
  - `exc_val` → exception instance
  - `exc_tb` → traceback object

- Return `False` → **propagate exception**
- Return `True` → **suppress exception**

This is why `FileLock` is safer than rolling your own: it handles **exceptions** and ensures **release of the lock**.

---

### 5. Refactoring Your Custom `LockedFile`

Current issues with your `LockedFile`:

- Platform-specific (`msvcrt` vs `fcntl`)
- Locks only a single byte on Windows — fragile
- Permission errors (like `PermissionError: [Errno 13]`) can occur
- Manual exception handling

We can refactor using `filelock`:

```python
from filelock import FileLock, Timeout
from pathlib import Path
import json
import logging

LOCK_FILE = Path("locks.json.lock")
LOCKS_JSON = Path("locks.json")

logger = logging.getLogger(__name__)

def load_locks(timeout=5):
    """Load locks.json safely using FileLock"""
    lock = FileLock(LOCK_FILE, timeout=timeout)
    try:
        with lock:
            if not LOCKS_JSON.exists():
                logger.info("Locks file doesn't exist, returning empty dict")
                return {}
            with open(LOCKS_JSON, "r") as f:
                locks = json.load(f)
            logger.info(f"Loaded {len(locks)} locks")
            return locks
    except Timeout:
        logger.error("Could not acquire lock on locks.json")
        raise
```

```python
def save_locks(locks, timeout=5):
    lock = FileLock(LOCK_FILE, timeout=timeout)
    try:
        with lock:
            with open(LOCKS_JSON, "w") as f:
                json.dump(locks, f, indent=4)
            logger.info(f"Saved {len(locks)} locks")
    except Timeout:
        logger.error("Could not acquire lock on locks.json for saving")
        raise
```

**Notes:**

- `timeout` prevents deadlocks — waits up to N seconds for lock.
- Logging shows who successfully acquired the lock.
- `FileLock` automatically handles **exceptions** and releases lock.

---

### 6. Integrating into FastAPI File Checkout/Checkin

Example **checkout**:

```python
from fastapi import HTTPException

def checkout_file(filename: str, user: str, message: str):
    locks = load_locks()

    if filename in locks:
        existing = locks[filename]
        raise HTTPException(
            status_code=409,
            detail=f"File is already checked out by {existing['user']}"
        )

    locks[filename] = {
        "user": user,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": message
    }

    save_locks(locks)
    return {"success": True, "message": f"File '{filename}' checked out by {user}"}
```

Checkin is similar — just delete the key in `locks` and call `save_locks`.

---

### 7. Advanced Usage: Timeouts & Exceptions

```python
from filelock import Timeout

lock = FileLock(LOCK_FILE, timeout=10)

try:
    with lock:
        # Critical section
        pass
except Timeout:
    print("Could not acquire lock in 10 seconds")
```

- Prevents **long-running or hanging locks**.
- Combine with `asyncio.to_thread()` if using in FastAPI async endpoints.

---

### 8. Common Pitfalls / Gotchas

1. **Windows vs Unix differences**

   - Solved by `filelock` — no need to manually use `msvcrt` or `fcntl`.

2. **Partial locks**

   - Windows: locking single bytes is fragile.

3. **Permission errors**

   - Lock files in OneDrive, network drives, or restricted directories may fail.

4. **Not releasing lock on exception**

   - Always use `with FileLock(...)`.

5. **Overwriting files incorrectly**

   - Remember `seek(0)` and `truncate()` if modifying in-place.

---

### 9. Additional Python Concepts Sprinkled In

- **Pathlib** → `Path("locks.json")` is better than raw strings.
- **Logging** → `logging.getLogger(__name__)` gives flexible debug info.
- **JSON serialization** → `json.load()` and `json.dump()`.
- **Exception handling** → `try/except Timeout:` for robust error reporting.
- **Context managers** → `with FileLock()` ensures resource cleanup.

---

#### ✅ Summary

- `filelock` provides **cross-platform, safe, and simple file locks**.
- Replace manual `msvcrt` / `fcntl` code with `FileLock`.
- Always use **context managers** for automatic cleanup.
- Handle **timeouts** to prevent deadlocks.
- Integrate into your FastAPI endpoints (`checkout`/`checkin`) seamlessly.

---
