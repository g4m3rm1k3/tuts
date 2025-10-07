# Professional PDM System - Chapter 1: Architecture & Foundation

**Goal**: Build a production-grade file management system with proper architecture from day one. No tutorial fluff—just patterns, principles, and pragmatic decisions.

**What we're building**: A collaborative file locking system where multiple users can checkout/checkin files, with version control and audit trails.

**Core principles we'll follow**:

- **Separation of Concerns**: UI ↔ State ↔ Services ↔ API
- **Single Responsibility**: Each module does ONE thing well
- **DRY**: Shared logic lives in one place
- **Composition over Inheritance**: Build with small, reusable pieces
- **Fail Fast**: Validate early, error explicitly

---

## Chapter 1.1: Project Structure (5 minutes)

**Why this structure?** Mirrors how professionals organize code: by feature/domain, not file type.

```bash
pdm-system/
├── backend/
│   ├── core/              # Shared utilities, no business logic
│   │   ├── config.py      # Single source of config
│   │   ├── exceptions.py  # Custom exceptions
│   │   └── security.py    # Auth helpers
│   ├── domain/            # Business logic, pure functions
│   │   ├── files.py       # File operations logic
│   │   ├── locks.py       # Lock management logic
│   │   └── users.py       # User management logic
│   ├── adapters/          # External integrations (DBs, Git, APIs)
│   │   ├── storage.py     # File storage abstraction
│   │   └── git.py         # Git operations
│   ├── api/               # HTTP layer ONLY
│   │   ├── routes/        # Grouped by resource
│   │   │   ├── files.py
│   │   │   ├── auth.py
│   │   │   └── locks.py
│   │   └── dependencies.py # FastAPI deps
│   ├── schemas/           # Pydantic models
│   │   ├── requests.py    # Input validation
│   │   └── responses.py   # Output serialization
│   └── main.py            # App factory
├── frontend/
│   ├── src/
│   │   ├── lib/           # Shared utilities
│   │   ├── stores/        # State management
│   │   ├── services/      # API clients
│   │   ├── components/    # Reusable UI
│   │   └── routes/        # Pages
│   └── static/
└── pyproject.toml         # Modern Python deps

```

**Key insight**: `domain/` has ZERO dependencies on FastAPI, Git, or databases. Pure business logic. Easy to test, easy to reuse.

**Read more**:

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Clean Architecture (Uncle Bob)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

## Chapter 1.2: Configuration as Code (10 minutes)

**The problem**: Hardcoded values, scattered configs, secrets in code.

**The solution**: Pydantic Settings with environment override.

**File**: `backend/core/config.py`

```python
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Literal

class Settings(BaseSettings):
    """
    Configuration with validation and type safety.

    Priority: ENV vars > .env file > defaults
    """
    # App
    app_name: str = "PDM System"
    environment: Literal["dev", "staging", "prod"] = "dev"
    debug: bool = True

    # Security
    secret_key: str  # REQUIRED in ENV
    token_expire_minutes: int = 30

    # Paths
    base_dir: Path = Path(__file__).parent.parent.parent
    data_dir: Path = base_dir / "data"

    # Git
    git_repo_path: Path = data_dir / "git_repo"

    # Performance
    max_file_size_mb: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.git_repo_path.mkdir(parents=True, exist_ok=True)

# Singleton
settings = Settings()
```

**Why Pydantic?**

- Type validation (catches `PORT=abc` at startup, not runtime)
- Auto-converts types (`"8000"` → `8000`)
- Clear errors: `"field required: secret_key"`

**Usage everywhere**:

```python
from core.config import settings

if settings.debug:
    print("Dev mode")
```

**Read more**: [Pydantic Settings Docs](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

---

## Chapter 1.3: Custom Exceptions (5 minutes)

**Why?** Don't raise generic `ValueError` or `Exception`. Create semantic exceptions.

**File**: `backend/core/exceptions.py`

```python
class PDMException(Exception):
    """Base exception for all PDM errors."""
    pass

class FileNotFoundError(PDMException):
    """Raised when file doesn't exist."""
    pass

class FileLockedException(PDMException):
    """Raised when attempting to lock an already-locked file."""
    def __init__(self, filename: str, locked_by: str):
        self.filename = filename
        self.locked_by = locked_by
        super().__init__(f"{filename} is locked by {locked_by}")

class UnauthorizedError(PDMException):
    """Raised when user lacks permission."""
    pass

class OwnershipError(PDMException):
    """Raised when user doesn't own the resource."""
    pass
```

**Usage**:

```python
# Bad
if file_locked:
    raise Exception("File is locked")  # Generic, no context

# Good
if file_locked:
    raise FileLockedException(filename, owner)  # Semantic, actionable
```

**Benefits**:

- Can catch specific exceptions: `except FileLockedException:`
- Self-documenting code
- Easier to map to HTTP status codes later

---

## Chapter 1.4: Domain Models (Pure Business Logic)

**Philosophy**: Domain layer knows NOTHING about HTTP, databases, or UI. Just business rules.

**File**: `backend/domain/locks.py`

```python
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict
from core.exceptions import FileLockedException, OwnershipError

@dataclass(frozen=True)  # Immutable
class FileLock:
    """
    Represents a file lock.

    Immutable: Once created, can't be modified.
    Why? Easier to reason about, thread-safe.
    """
    filename: str
    locked_by: str
    locked_at: datetime
    message: str

class LockManager:
    """
    Manages file locks using pure functions.

    No I/O here—just business logic.
    Storage is injected (dependency inversion).
    """

    def __init__(self, locks: Dict[str, FileLock]):
        """Initialize with current state."""
        self._locks = locks

    def acquire(self, filename: str, user: str, message: str) -> Dict[str, FileLock]:
        """
        Attempt to acquire lock.

        Returns: New lock state (doesn't mutate!)
        Raises: FileLockedException if already locked
        """
        if filename in self._locks:
            existing = self._locks[filename]
            raise FileLockedException(filename, existing.locked_by)

        new_lock = FileLock(
            filename=filename,
            locked_by=user,
            locked_at=datetime.now(timezone.utc),
            message=message
        )

        # Return NEW state (immutable pattern)
        return {**self._locks, filename: new_lock}

    def release(self, filename: str, user: str, is_admin: bool = False) -> Dict[str, FileLock]:
        """
        Release lock.

        Returns: New lock state
        Raises: OwnershipError if user doesn't own lock
        """
        if filename not in self._locks:
            raise FileNotFoundError(f"{filename} is not locked")

        lock = self._locks[filename]

        # Ownership check
        if not is_admin and lock.locked_by != user:
            raise OwnershipError(f"Lock owned by {lock.locked_by}, not {user}")

        # Return new state without this lock
        new_state = self._locks.copy()
        del new_state[filename]
        return new_state

    def get_lock(self, filename: str) -> FileLock | None:
        """Get lock info for a file."""
        return self._locks.get(filename)

    def is_locked_by(self, filename: str, user: str) -> bool:
        """Check if file is locked by specific user."""
        lock = self._locks.get(filename)
        return lock is not None and lock.locked_by == user
```

**Key patterns**:

1. **Immutable data** (`@dataclass(frozen=True)`) - prevents accidental mutation
2. **Pure functions** - same input = same output, no side effects
3. **Return new state** - don't mutate `self._locks`, return new dict
4. **Dependency inversion** - `LockManager` doesn't know HOW locks are stored

**Why this matters**: You can test this WITHOUT FastAPI, databases, or HTTP. Just call functions.

---

## Chapter 1.5: Storage Adapter (Hexagonal Architecture)

**The problem**: Domain logic shouldn't know about JSON files, databases, or Git. It should work with ANY storage.

**Solution**: Define an interface (Protocol), implement adapters.

**File**: `backend/adapters/storage.py`

```python
from typing import Protocol, Dict
from pathlib import Path
import json
from core.config import settings
from domain.locks import FileLock

class LockStorage(Protocol):
    """
    Interface for lock storage.

    Any class with these methods can be a LockStorage.
    No inheritance needed (duck typing with type safety).
    """
    def load(self) -> Dict[str, FileLock]: ...
    def save(self, locks: Dict[str, FileLock]) -> None: ...

class JSONLockStorage:
    """Stores locks in JSON file."""

    def __init__(self, file_path: Path = settings.data_dir / "locks.json"):
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self):
        """Create empty file if doesn't exist."""
        if not self.file_path.exists():
            self.file_path.write_text('{}')

    def load(self) -> Dict[str, FileLock]:
        """Load locks from JSON."""
        data = json.loads(self.file_path.read_text())

        # Convert dict to FileLock objects
        return {
            filename: FileLock(**lock_data)
            for filename, lock_data in data.items()
        }

    def save(self, locks: Dict[str, FileLock]) -> None:
        """Save locks to JSON."""
        # Convert FileLock objects to dicts
        data = {
            filename: {
                'filename': lock.filename,
                'locked_by': lock.locked_by,
                'locked_at': lock.locked_at.isoformat(),
                'message': lock.message
            }
            for filename, lock in locks.items()
        }

        self.file_path.write_text(json.dumps(data, indent=2))
```

**Why Protocol?** Later you can add `PostgresLockStorage`, `RedisLockStorage`, etc. Domain logic doesn't change.

---

## Chapter 1.6: Service Layer (Orchestration)

**Purpose**: Coordinate domain logic + storage. Still no HTTP knowledge.

**File**: `backend/domain/locks.py` (add this class)

```python
class LockService:
    """
    Orchestrates lock operations.

    Combines domain logic + storage.
    Still framework-agnostic.
    """

    def __init__(self, storage: LockStorage):
        self.storage = storage

    def checkout_file(self, filename: str, user: str, message: str) -> None:
        """Checkout a file (acquire lock)."""
        # Load current state
        locks = self.storage.load()
        manager = LockManager(locks)

        # Apply business logic
        new_locks = manager.acquire(filename, user, message)

        # Persist new state
        self.storage.save(new_locks)

    def checkin_file(self, filename: str, user: str, is_admin: bool = False) -> None:
        """Checkin a file (release lock)."""
        locks = self.storage.load()
        manager = LockManager(locks)

        new_locks = manager.release(filename, user, is_admin)

        self.storage.save(new_locks)

    def get_lock_info(self, filename: str) -> FileLock | None:
        """Get lock info for a file."""
        locks = self.storage.load()
        manager = LockManager(locks)
        return manager.get_lock(filename)
```

**Pattern**: Load → Transform → Save. Clean separation.

---

## Checkpoint: What We've Built

**Architecture**:

```
API Layer (FastAPI)
    ↓
Service Layer (orchestration)
    ↓
Domain Layer (business rules)
    ↓
Adapter Layer (storage)
```

**Benefits**:

- Can test domain logic in isolation
- Can swap storage (JSON → Postgres) without changing business logic
- Can add GraphQL API without touching domain code
- Clear responsibilities: each layer has ONE job

**Next in Chapter 1.7-1.10**:

- API layer (FastAPI routes)
- Dependency injection
- Error handling
- Request/response schemas

Want to continue with Chapter 1 (backend completion) or see this tested first?
