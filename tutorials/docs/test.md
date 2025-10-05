### Step 12: Fetching Files from the Repository with Locking

We previously learned how to scan a repository and return a list of files. Now, we’ll **safely manage locks** when reading/writing the `locks.json` file.

---

## 12.1 Step 1: Define Paths

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REPO_PATH = BASE_DIR / 'repo'
LOCKS_FILE = BASE_DIR / 'locks.json'
VALID_EXTENSIONS = {".mcam", ".vnc"}
```

- `BASE_DIR` → directory containing our script
- `REPO_PATH` → folder where the CAM files are stored
- `LOCKS_FILE` → stores lock info in JSON format
- `VALID_EXTENSIONS` → only return files we care about

---

## 12.2 Step 2: Load Locks Safely

```python
import json

def load_locks() -> dict:
    """Load locks.json safely using LockedFile"""
    if not LOCKS_FILE.exists():
        # If locks file does not exist, return empty dict
        return {}

    try:
        with LockedFile(LOCKS_FILE, 'r') as f:
            locks = json.load(f)
        return locks
    except json.JSONDecodeError:
        # If the file is corrupt, return empty dict
        return {}
```

**Explanation:**

- By using `with LockedFile(...)`, we **ensure no other process is reading or writing** at the same time.
- Even if `json.load` fails, the file is properly closed and unlocked.
- This prevents **race conditions**, where multiple users might overwrite each other’s changes.

---

## 12.3 Step 3: Save Locks Safely

```python
def save_locks(locks: dict):
    """Save locks.json safely using LockedFile"""
    with LockedFile(LOCKS_FILE, 'w') as f:
        json.dump(locks, f, indent=4)
```

- Always **use LockedFile** when writing
- Indent 4 for readability
- Guarantees that **other processes cannot read partial data** while writing

---

## 12.4 Step 4: Fetch Files with Lock Status

```python
import os

def get_files():
    """Return all CAM files in the repository with lock info"""
    # Load current locks
    locks = load_locks()

    # Check that repository exists
    if not REPO_PATH.exists():
        raise FileNotFoundError(f"Repository path not found: {REPO_PATH}")

    all_items = os.listdir(REPO_PATH)

    files = []
    for filename in all_items:
        full_path = REPO_PATH / filename

        # Only consider files with valid extensions
        if full_path.is_file() and Path(filename).suffix in VALID_EXTENSIONS:
            if filename in locks:
                status = "checked_out"
                locked_by = locks[filename]["user"]
            else:
                status = "available"
                locked_by = None

            files.append({
                "name": filename,
                "status": status,
                "locked_by": locked_by,
                "size": full_path.stat().st_size
            })

    return files
```

**Explanation:**

- Each file is checked against `locks.json`
- Lock status is included in the result
- If a file is **checked out**, the UI can display **who has it locked**

---

## 12.5 Step 5: Checking Out a File

```python
from datetime import datetime, timezone

def checkout_file(filename: str, user: str, message: str):
    """Acquire a lock for a specific file"""
    locks = load_locks()

    if filename in locks:
        # Someone else has already checked it out
        raise Exception(f"{filename} is already checked out by {locks[filename]['user']}")

    # Add lock
    locks[filename] = {
        "user": user,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": message
    }

    save_locks(locks)
    return f"{filename} successfully checked out by {user}"
```

**Explanation / Gotchas:**

- Without locking `locks.json`, two processes could **check out the same file simultaneously**, leading to a **race condition**.
- Always load and save inside **`LockedFile`** to ensure atomicity.

---

## 12.6 Step 6: Checking In a File

```python
def checkin_file(filename: str, user: str):
    """Release a lock on a file"""
    locks = load_locks()

    if filename not in locks:
        raise Exception(f"{filename} is not checked out")

    if locks[filename]["user"] != user:
        raise Exception(f"{filename} is locked by {locks[filename]['user']}, not {user}")

    del locks[filename]
    save_locks(locks)
    return f"{filename} successfully checked in by {user}"
```

**Explanation:**

- Only the **user who locked** the file can check it back in.
- Prevents accidental overwrites
- LockedFile ensures **atomic read/write** of `locks.json`

---

## 12.7 Step 7: Real-World Gotchas

1. **Windows PermissionError**

   - Opening `locks.json` with `'r'` will fail if using `msvcrt.LK_LOCK`. Use `'r+'` or `'w+'` when acquiring exclusive locks.

2. **Corrupted JSON**

   - If a process crashes during write, `locks.json` could be incomplete. Consider **writing to a temp file first**, then renaming.

3. **Deadlocks**

   - Multiple processes waiting on each other indefinitely. Avoid by **locking only when necessary**, **locking minimally**, and optionally using **timeouts**.

4. **Advisory vs Mandatory Locking**

   - Unix locks are advisory: all processes must cooperate. Windows locks are mandatory.

5. **Nested Locks**

   - Locking the same file twice in a single process can fail on Windows. Avoid nested `LockedFile` on same file.

---

## 12.8 Step 8: Full Flow Example

```python
### Fetch files and print status
for f in get_files():
    print(f"{f['name']} - {f['status']} - {f['locked_by']}")

### User "Alice" checks out a file
checkout_file("4801247.mcam", "Alice", "Working on revisions")

### User "Alice" checks it back in
checkin_file("4801247.mcam", "Alice")
```

- Demonstrates the **full lifecycle**: fetch → lock → unlock
- Safe for **multi-user environments**

---

✅ **Outcome**

- Atomic, safe locking with **cross-platform support**
- Proper exception handling
- Avoids race conditions, file corruption, and permission errors
- Explains **why your previous PermissionError happened** (Windows byte-level locking + read-only mode)

---
