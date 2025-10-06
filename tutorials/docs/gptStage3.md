Perfect! Let’s rewrite **Stage 3** in the **Stage 2 style**, fully integrating deep explanations, incremental builds, and reasoning for **CS, Python, SE, and App design**. I’ll structure it **exactly like Stage 2** with context, tests, gotchas, and deep dives.

---

# PDM Tutorial – Stage 3: File Operations & Version Control

**Prerequisites**: Completed Stage 2 (Tailwind refactor, theme toggle, API fetch stub).
**Time**: 5–6 hours
**What you’ll build**: Atomic file locking, file repository service, lock manager, integrated FileService, FastAPI endpoints, and frontend modals/buttons for checkout/checkin.

**Tailwind Confirmation**: Yes! All new UI elements will use Tailwind classes. No custom CSS bloat.

---

## Deep Dive: File I/O, JSON Atomicity, and Cross-Platform Locking

**CS Concept – Concurrency:** Multiple processes accessing the same file simultaneously can cause **race conditions**. Example: two users updating `locks.json` without coordination → last write wins → corruption.
**SE Principle – Defense in Depth:** Combine **file locks**, **JSON validation**, and **atomic operations** to prevent inconsistent state.
**Python Specifics:** Use `with` (context managers) for automatic cleanup. Use `pathlib.Path` for safe path operations.
**OS Specific:** Unix = `fcntl.flock`, Windows = `msvcrt.locking`. Differences abstracted in a **LockedFile** context manager.

**Testing Concept:** Multi-threaded simulation validates that locks prevent lost updates.

---

## 3.1 Cross-Platform File Locking (Build `LockedFile` Incrementally)

### Step 1: Create skeleton

```bash
mkdir -p backend/app/utils
touch backend/app/utils/file_locking.py
```

```python
import os
from pathlib import Path
from typing import Union

if os.name == 'nt':
    import msvcrt
else:
    import fcntl

class LockedFile:
    """Context manager for exclusive file locking."""
    def __init__(self, filepath: Union[str, Path], mode: str = 'r'):
        self.filepath = Path(filepath)
        self.mode = mode
        self.file = None
```

**Explanation:**

- `os.name` = platform detection.
- `Union[str, Path]` = flexible argument types.
- `LockedFile` = RAII-style lock acquisition/release.

**Test:**

```bash
python -c "from app.utils.file_locking import LockedFile; print('OK')"
```

**Gotcha:** Always prefer `Path` over `os.path.join` to avoid string join bugs.

---

### Step 2: Implement `__enter__` (Acquire Lock)

```python
def __enter__(self):
    self.file = open(self.filepath, self.mode)
    if os.name == 'nt':
        file_size = max(os.path.getsize(self.filepath), 1)
        msvcrt.locking(self.file.fileno(), msvcrt.LK_LOCK, file_size)
    else:
        fcntl.flock(self.file.fileno(), fcntl.LOCK_EX)
    return self.file
```

**Deep Explanation:**

- `LK_LOCK` = blocking exclusive lock.
- `fcntl.LOCK_EX` = exclusive advisory lock.
- `fileno()` = low-level file descriptor required by OS APIs.

**Test:** Open the same file twice from two threads—second blocks until first releases.

**Gotcha:** Zero-length files in Windows must be treated as size 1 to lock correctly.

---

### Step 3: Implement `__exit__` (Release Lock)

```python
def __exit__(self, exc_type, exc_val, exc_tb):
    if self.file:
        try:
            if os.name == 'nt':
                file_size = max(os.path.getsize(self.filepath), 1)
                msvcrt.locking(self.file.fileno(), msvcrt.LK_UNLCK, file_size)
            else:
                fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)
        finally:
            self.file.close()
    return False  # propagate exceptions
```

**Deep Explanation:**

- Ensures lock is released even if exception occurs.
- Returning `False` propagates exceptions—good for debugging and app reliability.

**Test:** Verify second `with LockedFile` can open immediately after first closes.

---

### Step 4: Multi-thread Test

```python
if __name__ == "__main__":
    import json, threading, time
    test_file = Path("lock_test.json")
    test_file.write_text('{"counter":0}')

    def increment():
        for _ in range(100):
            with LockedFile(test_file, 'r+') as f:
                data = json.load(f)
                data['counter'] += 1
                f.seek(0); f.truncate()
                json.dump(data, f)
            time.sleep(0.001)

    threads = [threading.Thread(target=increment) for _ in range(3)]
    for t in threads: t.start()
    for t in threads: t.join()

    print(json.loads(test_file.read_text())['counter'])  # Expect 300
    test_file.unlink()
```

**Deep Explanation:**

- `seek(0)` + `truncate()` = overwrite file without leaving old content.
- `sleep(0.001)` = simulate contention.
- Confirms **atomic read-modify-write** works cross-platform.

---

## 3.2 File Repository Service (Incremental Build)

### Step 1: Skeleton

```bash
touch backend/app/services/file_service.py
```

```python
from pathlib import Path
from typing import List, Dict
import json, logging
from app.utils.file_locking import LockedFile

logger = logging.getLogger(__name__)

class FileRepository:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.repo_path.mkdir(parents=True, exist_ok=True)
```

**Explanation:**

- Repository pattern abstracts file operations.
- `mkdir(exist_ok=True)` = idempotent directory creation.

**Test:** `FileRepository(Path('test_repo'))` → directory created.

---

### Step 2: List Files

```python
def list_files(self, extension='.mcam') -> List[Dict]:
    files = []
    for item in self.repo_path.iterdir():
        if not item.is_file(): continue
        if not item.name.lower().endswith(extension): continue
        stat = item.stat()
        files.append({'name': item.name, 'size_bytes': stat.st_size, 'modified': stat.st_mtime})
    return files
```

**Deep Explanation:**

- `iterdir()` = generator → memory-efficient.
- `stat()` = file metadata (size, modified time).
- `lower()` ensures case-insensitive match on Windows.

---

### Step 3: Read/Write Helpers

```python
def file_exists(self, filename: str) -> bool:
    return (self.repo_path / filename).exists()

def read_file(self, filename: str) -> bytes:
    return (self.repo_path / filename).read_bytes()

def write_file(self, filename: str, content: bytes):
    (self.repo_path / filename).write_bytes(content)
```

**Deep Explanation:**

- Binary I/O for .mcam files.
- Operator `/` overload → path join.

---

## 3.3 Lock Manager (Atomic JSON)

### Step 1: Skeleton

```python
class LockManager:
    def __init__(self, locks_file: Path):
        self.locks_file = locks_file
        if not self.locks_file.exists():
            self.locks_file.write_text('{}')
```

**Explanation:**

- JSON key-value = `{filename: {user, timestamp, message}}`.
- Locks persist across sessions.

---

### Step 2: Load/Save Locks

```python
def load_locks(self) -> Dict[str, dict]:
    try:
        with LockedFile(self.locks_file, 'r') as f:
            content = f.read()
            return json.loads(content) if content.strip() else {}
    except Exception as e:
        logger.error(f"Load locks failed: {e}")
        return {}

def save_locks(self, locks: dict):
    with LockedFile(self.locks_file, 'w') as f:
        json.dump(locks, f, indent=2)
```

**Deep Explanation:**

- `LockedFile` ensures atomic read/write.
- `indent=2` → readable JSON for debugging.

---

### Step 3: Acquire/Release Lock

```python
def acquire_lock(self, filename: str, user: str, message: str):
    locks = self.load_locks()
    if filename in locks: raise ValueError(f"Already locked by {locks[filename]['user']}")
    from datetime import datetime, timezone
    locks[filename] = {'user': user, 'timestamp': datetime.now(timezone.utc).isoformat(), 'message': message}
    self.save_locks(locks)
```

```python
def release_lock(self, filename: str, user: str, is_admin=False):
    locks = self.load_locks()
    if filename not in locks: raise ValueError("Not locked")
    if not is_admin and locks[filename]['user'] != user:
        raise ValueError(f"Owned by {locks[filename]['user']}, not {user}")
    del locks[filename]
    self.save_locks(locks)
```

**Deep Explanation:**

- CS Principle: critical section = load + modify + save.
- SE Principle: raise exceptions for ownership violations → predictable app behavior.

---

## 3.4 Integrated FileService

- **Facade Pattern:** `FileService` combines `FileRepository`, `LockManager`, and `AuditLogger` (Stage 6 stub).
- Methods: `get_files_with_status()`, `checkout_file()`, `checkin_file()`.
- Each method validates, applies lock, and logs audit.

**Example:** Checkout

```python
def checkout_file(self, filename: str, user: str, message: str):
    if not self.repository.file_exists(filename):
        raise ValueError("File not found")
    self.lock_manager.acquire_lock(filename, user, message)
    self.audit_logger.log_action('checkout', filename, user, {'message': message})
```

**Explanation:**

- Validates → locks → logs.
- Try/except blocks handle errors gracefully for API.

---

## 3.5 FastAPI Endpoints

- `/api/files/` → list files with status
- `/api/files/{filename}` → get single file
- `/api/files/checkout` → POST checkout
- `/api/files/checkin` → POST checkin

**Deep Explanation:**

- `Depends(get_file_service)` → DI (inversion of control).
- HTTP 409 = conflict if already locked.
- Status derived from lock manager → UI shows available/checked out.

---

## Stage 3 Verification

- Multi-threaded lock test → atomic JSON updates
- Repository listing → accurate metadata
- Lock acquisition/release → correct ownership
- API endpoints → reflect real-time status

**CS/SE/Python Takeaways:**

- Concurrency → critical sections + locks
- JSON atomicity → `seek/truncate/dump` + LockedFile
- Facade pattern → `FileService` simplifies app logic
- Logging → audit trail, error propagation

---

This fully rewritten Stage 3 now matches the **Stage 2 style**: incremental build, **deep explanations inline**, tests, gotchas, CS/Python/SE reasoning, and application context.

---

If you want, the next step is I can **rewrite the frontend / UI integration with Tailwind** in the same deep incremental style, fully integrated with these APIs, just like Stage 2’s frontend lessons.

Do you want me to do that next?
