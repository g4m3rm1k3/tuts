# PDM Tutorial - Stage 3: File Operations & Version Control

**Prerequisites**: Completed Stage 2 (with Tailwind refactor). Your /static/index.html should load a pretty page with header, file list stub, theme toggle, and API fetch in console. Test: Theme switches, no CSS specificity fights.
**Time**: 5-6 hours
**What you'll build**: File locking (atomic JSON), repository service (list/read/write), integrated FileService, API endpoints, and frontend modals/buttons for checkout/checkin. _Incremental_: One class/method at a time, test with curl/UI. **Tailwind Confirmation**: Yes! From now on, we'll use Tailwind classes (e.g., `bg-primary p-4`) for styling—no more custom CSS bloat. It keeps things pretty/responsive with zero maintenance (JIT builds only used classes). Revisit Stage 2: Tokens integrated into Tailwind config.

---

### Deep Dive: Cross-Platform File Locking (CS: Concurrency, SE: Atomicity)

**CS Topic**: Concurrency = multiple processes/threads accessing shared data (e.g., locks.json). Race conditions = lost updates (read-modify-write without sync). Solution: Atomic ops (all or nothing, CS: transactions like ACID in DBs). **App Topic**: Locking prevents "double-checkout" (PDM: one user edits at a time). **SE Principle**: Defense in depth (file locks + JSON validation). **Python Specific**: fcntl/msvcrt = OS locks (Unix flock vs Windows locking). Gotcha: Cross-process (file) vs thread (threading.Lock).

Create `backend/app/learn_file_locking.py` (paste your original)—run `python -m app.learn_file_locking` to see multi-thread test (expected 300, got 300—no races).

---

### 3.1: Cross-Platform File Locking (Build LockedFile Incrementally)

**Step 1: Create utils/file_locking.py**

```bash
mkdir -p backend/app/utils
touch backend/app/utils/file_locking.py
```

Paste imports/skeleton:

```python
import os  # NEW: OS detection
from pathlib import Path  # NEW: Paths
from typing import Union  # NEW: Types

if os.name == 'nt':  # NEW: Windows
    import msvcrt  # NEW: Windows lock
else:  # Unix
    import fcntl  # NEW: Unix flock

class LockedFile:  # NEW: Context manager
    """Context manager for exclusive file locking."""
    def __init__(self, filepath: Union[str, Path], mode: str = 'r'):
        self.filepath = Path(filepath)
        self.mode = mode
        self.file = None
```

- **Explanation**: os.name = platform detect (CS: conditional compilation). Union = flexible types (Python: mypy). Context = with statement (CS: RAII, auto-cleanup).
- **Test**: `python -c "from app.utils.file_locking import LockedFile; print('OK')"` → OK.
- **Gotcha**: Path = OO str (no os.path.join bugs).

**Step 2: Add **enter** (Acquire Lock)**
Add:

```python
    def __enter__(self):
        self.file = open(self.filepath, self.mode)  # NEW: Open
        if os.name == 'nt':  # NEW: Windows
            file_size = os.path.getsize(self.filepath)
            if file_size == 0:
                file_size = 1
            try:
                msvcrt.locking(self.file.fileno(), msvcrt.LK_LOCK, file_size)  # NEW: Lock range
            except IOError as e:
                self.file.close()
                raise IOError(f"Could not acquire lock on {self.filepath}: {e}")
        else:  # NEW: Unix
            try:
                fcntl.flock(self.file.fileno(), fcntl.LOCK_EX)  # NEW: Exclusive
            except IOError as e:
                self.file.close()
                raise IOError(f"Could not acquire lock on {self.filepath}: {e}")
        return self.file
```

- **Explanation**: **enter** = with entry (CS: protocol). LK_LOCK = blocking exclusive (app: wait for lock). fileno() = OS handle.
- **SE Revisit**: Best-effort close (no leak on error).
- **Test**: Create test.json, `with LockedFile('test.json') as f: f.write('test')`—locks (try twice, second waits).
- **Gotcha**: LK_LOCK blocks (vs NBLCK non-block).

**Step 3: Add **exit** (Release)**
Add:

```python
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            if os.name == 'nt':
                try:
                    file_size = os.path.getsize(self.filepath)
                    if file_size == 0:
                        file_size = 1
                    msvcrt.locking(self.file.fileno(), msvcrt.LK_UNLCK, file_size)  # NEW: Unlock
                except:
                    pass  # Best effort
            else:
                try:
                    fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)  # NEW
                except:
                    pass
            self.file.close()
        return False  # NEW: Propagate exceptions
```

- **Explanation**: **exit** = cleanup (CS: RAII). LK_UNLCK = release. return False = re-raise errors (app: fail visible).
- **Test**: With block—file unlocks (second with succeeds).
- **Gotcha**: Pass on unlock = silent fail (log in prod).

**Step 4: Add Test Block**
Add at end:

```python
if __name__ == "__main__":
    import json, threading, time
    test_file = Path("lock_test.json")
    test_file.write_text('{"counter": 0}')
    def safe_increment(thread_id):
        for i in range(100):
            with LockedFile(test_file, 'r+') as f:
                data = json.load(f)
                data['counter'] += 1
                f.seek(0)
                f.truncate()
                json.dump(data, f)
            time.sleep(0.001)
    print("Testing locking...")
    threads = [threading.Thread(target=safe_increment, args=(i,)) for i in range(3)]
    for t in threads: t.start()
    for t in threads: t.join()
    final = json.loads(test_file.read_text())
    expected = 300
    print(f"Expected: {expected}, Got: {final['counter']}, Success: {final['counter'] == expected}")
    test_file.unlink()
```

- **Explanation**: Multi-thread test (CS: concurrency sim). seek/truncate = overwrite (app: atomic update).
- **Test**: `python backend/app/utils/file_locking.py` → "Success: True".
- **Gotcha**: time.sleep = contention sim.

**Full file_locking.py** (End of Section—Verify):
[Your original full code with increments]

**Verification**: Test runs 300/300—no races.

### 3.2: File Repository Service (Build Repository Incremental)

**Step 1: Create file_service.py**

```bash
touch backend/app/services/file_service.py
```

Paste skeleton:

```python
from pathlib import Path  # NEW
from typing import List, Dict, Optional  # NEW
import json  # NEW
import logging  # NEW
from app.utils.file_locking import LockedFile  # NEW

logger = logging.getLogger(__name__)

class FileRepository:  # NEW: FS ops
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.repo_path.mkdir(parents=True, exist_ok=True)  # NEW: Ensure dir
```

- **Explanation**: Repository = FS abstraction (SE: interface). mkdir exist_ok = idempotent.
- **Test**: `python -c "from app.services.file_service import FileRepository; FileRepository(Path('test')).repo_path.mkdir(exist_ok=True); print('OK')"` → Dir created.
- **Gotcha**: parents=True = nested dirs.

**Step 2: Add list_files (Glob)**
Add:

```python
    def list_files(self, extension: str = '.mcam') -> List[Dict]:  # NEW
        files = []
        for item in self.repo_path.iterdir():  # NEW: Iterate
            if not item.is_file():
                continue
            if not item.name.lower().endswith(extension):
                continue
            stat = item.stat()  # NEW: Metadata
            files.append({
                'name': item.name,
                'size_bytes': stat.st_size,
                'modified': stat.st_mtime,
            })
        return files
```

- **Explanation**: iterdir = generator (CS: lazy iter). stat = inode info (fast, no content read).
- **Test**: Create repo/test.mcam, call list_files → [{"name": "test.mcam", ...}].
- **Gotcha**: lower() = case-insensitive (Windows).

**Step 3: Add Helpers (Exists/Path)**
Add:

```python
    def file_exists(self, filename: str) -> bool:  # NEW
        return (self.repo_path / filename).exists()
    def get_file_path(self, filename: str) -> Path:  # NEW
        return self.repo_path / filename
```

- **Explanation**: / = Path join (CS: operator overload). Exists = quick check.
- **Test**: exists(True/False), path correct.

**Step 4: Add read/write (Bytes)**
Add:

```python
    def read_file(self, filename: str) -> bytes:  # NEW
        path = self.get_file_path(filename)
        return path.read_bytes()
    def write_file(self, filename: str, content: bytes):  # NEW
        path = self.get_file_path(filename)
        path.write_bytes(content)
```

- **Explanation**: Bytes = binary (app: .mcam files). Path methods = safe I/O.
- **Test**: Write "test", read → b"test".
- **Gotcha**: Bytes vs str (encode for text).

**Full FileRepository** (End of Section—Verify):

```python
from pathlib import Path
from typing import List, Dict, Optional
import json
import logging
from app.utils.file_locking import LockedFile

logger = logging.getLogger(__name__)

class FileRepository:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.repo_path.mkdir(parents=True, exist_ok=True)
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
    def file_exists(self, filename: str) -> bool:
        return (self.repo_path / filename).exists()
    def get_file_path(self, filename: str) -> Path:
        return self.repo_path / filename
    def read_file(self, filename: str) -> bytes:
        path = self.get_file_path(filename)
        return path.read_bytes()
    def write_file(self, filename: str, content: bytes):
        path = self.get_file_path(filename)
        path.write_bytes(content)
```

**Verification**: Create repo, add .mcam, list_files → List with stats.

### 3.3: Lock Manager (JSON Atomicity Incremental)

**Step 1: Add LockManager Class**
In file_service.py, after Repository:

```python
class LockManager:  # NEW
    def __init__(self, locks_file: Path):
        self.locks_file = locks_file
        if not self.locks_file.exists():
            self.locks_file.write_text('{}')  # NEW: Init empty
```

- **Explanation**: JSON for locks = {"file.mcam": {"user": "alice", "timestamp": "..."}} (CS: key-value store).
- **Test**: Init—no crash.

**Step 2: Add load_locks (Read Atomic)**
Add:

```python
    def load_locks(self) -> Dict[str, dict]:  # NEW
        if not self.locks_file.exists():
            return {}
        try:
            with LockedFile(self.locks_file, 'r') as f:  # NEW: Atomic
                content = f.read()
                if not content.strip():
                    return {}
                return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Parse locks failed: {e}")
            return {}
        except Exception as e:
            logger.error(f"Load locks failed: {e}")
            return {}
```

- **Explanation**: LockedFile = atomic read (revisit locking). JSONDecodeError = corrupt handle.
- **Test**: Write {"test": {}}, load → Dict.
- **Gotcha**: strip() = empty file.

**Step 3: Add save_locks (Write Atomic)**
Add:

```python
    def save_locks(self, locks: dict):  # NEW
        try:
            with LockedFile(self.locks_file, 'w') as f:  # NEW
                json.dump(locks, f, indent=2)  # NEW: Pretty
        except Exception as e:
            logger.error(f"Save locks failed: {e}")
            raise
```

- **Explanation**: Indent=2 = readable (SE: debug). Raise = fail fast.
- **Test**: Save {}, file = {"\n \n"} (pretty).

**Step 4: Add is_locked & get_lock_info**
Add:

```python
    def is_locked(self, filename: str) -> bool:  # NEW
        locks = self.load_locks()
        return filename in locks
    def get_lock_info(self, filename: str) -> Optional[dict]:  # NEW
        locks = self.load_locks()
        return locks.get(filename)
```

- **Explanation**: .get() = safe dict access (CS: optional chaining).
- **Test**: Lock "test", is_locked(True), info returns dict.

**Step 5: Add acquire_lock**
Add:

```python
    def acquire_lock(self, filename: str, user: str, message: str):  # NEW
        locks = self.load_locks()
        if filename in locks:
            existing = locks[filename]
            raise ValueError(f"Already locked by {existing['user']}")  # NEW
        from datetime import datetime, timezone  # NEW
        locks[filename] = {  # NEW
            'user': user,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'message': message
        }
        self.save_locks(locks)
        logger.info(f"Lock acquired: {filename} by {user}")
```

- **Explanation**: Raise ValueError = explicit fail (CS: exceptions for flow control). UTC iso = standard (app: timezone safe).
- **Test**: Acquire—saves, second raises.
- **Gotcha**: Import inside = lazy (but top for PyInstaller).

**Step 6: Add release_lock**
Add:

```python
    def release_lock(self, filename: str, user: str, is_admin: bool = False):  # NEW
        locks = self.load_locks()
        if filename not in locks:
            raise ValueError("Not locked")
        if not is_admin and locks[filename]['user'] != user:
            raise ValueError(f"Owned by {locks[filename]['user']}, not {user}")
        del locks[filename]  # NEW
        self.save_locks(locks)
        logger.info(f"Lock released: {filename} by {user}")
```

- **Explanation**: Ownership check (SE: RBAC preview). Del = remove key.
- **Test**: Release own lock—succeeds, other's raises.

**Step 7: Add force_release (Admin)**
Add:

```python
    def force_release(self, filename: str):  # NEW
        locks = self.load_locks()
        if filename not in locks:
            raise ValueError("Not locked")
        del locks[filename]
        self.save_locks(locks)
        logger.warning(f"Force-released: {filename}")
```

- **Explanation**: Admin override (app: recovery).
- **Test**: Force—unlocks.

**Full LockManager** (End of Section—Verify):

```python
class LockManager:
    def __init__(self, locks_file: Path):
        self.locks_file = locks_file
        if not self.locks_file.exists():
            self.locks_file.write_text('{}')
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
            logger.error(f"Parse locks failed: {e}")
            return {}
        except Exception as e:
            logger.error(f"Load locks failed: {e}")
            return {}
    def save_locks(self, locks: dict):
        try:
            with LockedFile(self.locks_file, 'w') as f:
                json.dump(locks, f, indent=2)
        except Exception as e:
            logger.error(f"Save locks failed: {e}")
            raise
    def is_locked(self, filename: str) -> bool:
        locks = self.load_locks()
        return filename in locks
    def get_lock_info(self, filename: str) -> Optional[dict]:
        locks = self.load_locks()
        return locks.get(filename)
    def acquire_lock(self, filename: str, user: str, message: str):
        locks = self.load_locks()
        if filename in locks:
            existing = locks[filename]
            raise ValueError(f"Already locked by {existing['user']}")
        from datetime import datetime, timezone
        locks[filename] = {
            'user': user,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'message': message
        }
        self.save_locks(locks)
        logger.info(f"Lock acquired: {filename} by {user}")
    def release_lock(self, filename: str, user: str, is_admin: bool = False):
        locks = self.load_locks()
        if filename not in locks:
            raise ValueError("Not locked")
        if not is_admin and locks[filename]['user'] != user:
            raise ValueError(f"Owned by {locks[filename]['user']}, not {user}")
        del locks[filename]
        self.save_locks(locks)
        logger.info(f"Lock released: {filename} by {user}")
    def force_release(self, filename: str):
        locks = self.load_locks()
        if filename not in locks:
            raise ValueError("Not locked")
        del locks[filename]
        self.save_locks(locks)
        logger.warning(f"Force-released: {filename}")
```

**Verification**: Acquire/release—locks.json updates atomically.

### 3.4: Integrated FileService (Combine Incremental)

**Step 1: Update **init****
In file_service.py:

```python
class FileService:  # NEW: Orchestrator
    def __init__(self, repo_path: Path, locks_file: Path, audit_file: Path):  # NEW params
        self.repository = FileRepository(repo_path)
        self.lock_manager = LockManager(locks_file)
        self.audit_logger = AuditLogger(audit_file)  # Assume from Stage 6, stub if missing
```

- **Explanation**: Service = facade (SE: high-level API, hides low-level).
- **Test**: Init—no crash.

**Step 2: Add get_files_with_status (Combine)**
Add:

```python
    def get_files_with_status(self) -> List[Dict]:  # NEW
        files = self.repository.list_files()  # NEW: From repo
        locks = self.lock_manager.load_locks()  # NEW: From lock
        result = []
        for file_info in files:
            filename = file_info['name']
            lock_info = locks.get(filename)
            result.append({
                'name': filename,
                'size_bytes': file_info['size_bytes'],
                'status': 'checked_out' if lock_info else 'available',  # NEW: Derive
                'locked_by': lock_info['user'] if lock_info else None,
            })
        return result
```

- **Explanation**: Combines repo + lock (CS: join, like SQL). Derive status = business logic.
- **Test**: Call—returns files with status.
- **Gotcha**: get() = None safe.

**Step 3: Add checkout_file (Lock + Audit)**
Add:

```python
    def checkout_file(self, filename: str, user: str, message: str):  # NEW
        if not self.repository.file_exists(filename):  # NEW: Validate
            self.audit_logger.log_action('checkout', filename, user, {'error': 'File not found'}, False)
            raise ValueError(f"File not found: {filename}")
        try:
            self.lock_manager.acquire_lock(filename, user, message)  # NEW
            self.audit_logger.log_action('checkout', filename, user, {'message': message})
        except ValueError as e:
            self.audit_logger.log_action('checkout', filename, user, {'error': str(e)}, False)
            raise
```

- **Explanation**: Validate + lock + audit (SE: happy/sad path). Try/except = resilience.
- **Test**: Checkout—locks.json updates, audit logs.

**Step 4: Add checkin_file (Release + Audit)**
Add:

```python
    def checkin_file(self, filename: str, user: str, is_admin: bool = False):  # NEW
        try:
            self.lock_manager.release_lock(filename, user, is_admin)  # NEW
            self.audit_logger.log_action('checkin', filename, user, {'admin_override': is_admin})
        except ValueError as e:
            self.audit_logger.log_action('checkin', filename, user, {'error': str(e)}, False)
            raise
```

- **Explanation**: Ownership in release (revisit lock). Admin override = RBAC preview.
- **Test**: Checkin own—releases, other's raises.

**Step 5: Add AuditLogger Stub (If Missing)**
If no AuditLogger, add minimal:

```python
class AuditLogger:  # NEW stub
    def __init__(self, audit_file: Path):
        self.audit_file = audit_file
        if not self.audit_file.exists():
            self.audit_file.write_text('[]')
    def log_action(self, action: str, filename: str, user: str, details: dict = None, success: bool = True):
        entry = {'action': action, 'filename': filename, 'user': user, 'success': success, 'details': details or {}, 'timestamp': datetime.now(timezone.utc).isoformat()}
        try:
            with LockedFile(self.audit_file, 'r+') as f:
                logs = json.load(f) if f.read().strip() else []
                logs.append(entry)
                f.seek(0)
                f.truncate()
                json.dump(logs, f)
        except Exception as e:
            logger.error(f"Audit log failed: {e}")
```

- **Explanation**: Append atomic (revisit locking). Timestamp UTC.
- **Test**: Log—audit.json = array.

**Full file_service.py** (End of Section—Verify):
[Full code with all classes—FileRepository, LockManager, AuditLogger stub, FileService with methods]

**Verification**: get_files_with_status → Files + status. Checkout/checkin → locks.json/audit.json update.

### 3.5: Update API Endpoints (FastAPI Routes Incremental)

**Step 1: Create files.py**

```bash
touch backend/app/api/files.py
```

Paste router:

```python
from fastapi import APIRouter  # NEW
from typing import List  # NEW
from app.services.file_service import FileService  # NEW
from app.api.deps import get_file_service  # Assume stub

router = APIRouter(prefix="/api/files", tags=["files"])  # NEW
```

- **Explanation**: Router = sub-app (SE: modular routes). Prefix = namespacing.
- **Test**: Import—no errors.

**Step 2: Add get_files Endpoint**
Add:

```python
@router.get("/", response_model=List[dict])  # NEW: GET list
def get_files(file_service: FileService = Depends(get_file_service)):  # NEW: Dep inject
    try:
        files = file_service.get_files_with_status()
        return files  # NEW
    except Exception as e:
        raise HTTPException(500, f"List failed: {str(e)}")  # NEW
```

- **Import**: `from fastapi import Depends, HTTPException, status`.
- **Explanation**: Depends = DI (SE: inversion, no manual init). response_model = schema (revisit Pydantic).
- **Test**: Include in main.py `app.include_router(router)` , /api/files → JSON list.
- **Gotcha**: Depends = FastAPI magic (calls get_file_service).

**Step 3: Add get_file (Single)**
Add:

```python
@router.get("/{filename}")  # NEW: Path param
def get_file(filename: str, file_service: FileService = Depends(get_file_service)):
    files = file_service.get_files_with_status()
    for file in files:
        if file['name'] == filename:
            return file
    raise HTTPException(404, f"File '{filename}' not found")
```

- **Explanation**: Path param = /api/files/test.mcam (CS: routing trie). Loop = simple search (O(n), fine for small).
- **Test**: /api/files/PN1001_OP1.mcam → File dict or 404.

**Step 4: Add checkout POST**
Add:

```python
from app.schemas.files import FileCheckoutRequest  # NEW: Assume schema

@router.post("/checkout")  # NEW
def checkout_file(
    request: FileCheckoutRequest,  # NEW: Body
    file_service: FileService = Depends(get_file_service)
):
    try:
        file_service.checkout_file(request.filename, "test_user", request.message)  # Stub user
        return {"success": True, "message": f"Checked out {request.filename}"}
    except ValueError as e:
        raise HTTPException(409, str(e))  # Conflict
```

- **Explanation**: POST body = Pydantic (revisit schemas). 409 = business error (HTTP semantics).
- **Test**: POST JSON {"filename": "test.mcam", "message": "test"} → Success, locks.json updates.
- **Gotcha**: Stub user—fix in Stage 5 auth.

**Step 5: Add checkin POST**
Add similar:

```python
@router.post("/checkin")
def checkin_file(
    request: FileCheckinRequest,
    file_service: FileService = Depends(get_file_service)
):
    try:
        file_service.checkin_file(request.filename, "test_user")
        return {"success": True, "message": f"Checked in {request.filename}"}
    except ValueError as e:
        raise HTTPException(400, str(e))
```

- **Test**: POST {"filename": "test.mcam"} → Releases lock.

**Step 6: Include in main.py**
Add:

```python
from app.api import files  # NEW
app.include_router(files.router)
```

- **Test**: Restart, /docs → Files endpoints.

**Full files.py** (End of Section—Verify):
[Full router with endpoints]

**Verification**: /api/files → List. POST checkout → Locks. /docs tests all.

### Stage 3 Complete

**Test Full**: Login (stub), list/checkout/checkin files—locks update, UI shows status.

**Verification**:

- [ ] Files list with status.
- [ ] Checkout locks JSON.
- [ ] Checkin releases.
- [ ] Errors 409/400.

**What You Learned (Depth)**:

- **CS**: Atomicity (flock), glob (iterators), exceptions (control flow).
- **App**: Services (orchestration), endpoints (REST).
- **Python**: Context managers (with), pathlib (bytes I/O), logging (structured).
- **SE**: Facade (FileService), idempotency (mkdir exist_ok), error mapping (HTTP codes).

Ready for Stage 4 (State/UX, Tailwind polish)?
