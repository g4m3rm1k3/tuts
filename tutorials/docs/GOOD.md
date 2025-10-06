# Professional PDM System - Chapter 1 (with learning resources)

## Chapter 1.1: Project Structure

```bash
pdm-system/
├── backend/
│   ├── core/              # Cross-cutting concerns
│   ├── domain/            # Business logic (framework-agnostic)
│   ├── adapters/          # External system integrations
│   ├── api/               # HTTP interface
│   └── schemas/           # Data validation
└── frontend/
```

**Learn more:**

- [Hexagonal Architecture (Ports & Adapters)](https://alistair.cockburn.us/hexagonal-architecture/) - Why business logic is isolated
- [Domain-Driven Design basics](https://martinfowler.com/bliki/DomainDrivenDesign.html) - Organizing by domain, not tech
- [The Dependency Rule](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) - Why dependencies point inward

---

## Chapter 1.2: Configuration

**File**: `backend/core/config.py`

```python
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Literal

class Settings(BaseSettings):
    # App
    app_name: str = "PDM System"
    environment: Literal["dev", "staging", "prod"] = "dev"

    # Security
    secret_key: str  # Required
    token_expire_minutes: int = 30

    # Paths
    base_dir: Path = Path(__file__).parent.parent.parent
    data_dir: Path = base_dir / "data"

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_dir.mkdir(parents=True, exist_ok=True)

settings = Settings()
```

**Learn more:**

- [12-Factor App: Config](https://12factor.net/config) - Why environment variables
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) - Type-safe configuration

---

## Chapter 1.3: Custom Exceptions

**File**: `backend/core/exceptions.py`

```python
class PDMException(Exception):
    """Base exception for domain errors."""
    pass

class FileNotFoundError(PDMException):
    pass

class FileLockedException(PDMException):
    def __init__(self, filename: str, locked_by: str):
        self.filename = filename
        self.locked_by = locked_by
        super().__init__(f"{filename} locked by {locked_by}")

class UnauthorizedError(PDMException):
    pass

class OwnershipError(PDMException):
    pass
```

**Learn more:**

- [Python Exception Hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy) - Standard patterns
- [Domain Exceptions](https://enterprisecraftsmanship.com/posts/exceptions-for-flow-control/) - When to use them

---

## Chapter 1.4: Domain Layer (Pure Business Logic)

**File**: `backend/domain/locks.py`

```python
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict
from core.exceptions import FileLockedException, OwnershipError

@dataclass(frozen=True)
class FileLock:
    """Immutable lock record."""
    filename: str
    locked_by: str
    locked_at: datetime
    message: str

class LockManager:
    """Pure business logic for locks."""

    def __init__(self, locks: Dict[str, FileLock]):
        self._locks = locks

    def acquire(self, filename: str, user: str, message: str) -> Dict[str, FileLock]:
        """
        Returns: New state (doesn't mutate)
        Raises: FileLockedException if already locked
        """
        if filename in self._locks:
            raise FileLockedException(filename, self._locks[filename].locked_by)

        new_lock = FileLock(
            filename=filename,
            locked_by=user,
            locked_at=datetime.now(timezone.utc),
            message=message
        )

        return {**self._locks, filename: new_lock}

    def release(self, filename: str, user: str, is_admin: bool = False) -> Dict[str, FileLock]:
        """Returns: New state without this lock"""
        if filename not in self._locks:
            raise FileNotFoundError(f"{filename} not locked")

        lock = self._locks[filename]
        if not is_admin and lock.locked_by != user:
            raise OwnershipError(f"Locked by {lock.locked_by}")

        new_state = self._locks.copy()
        del new_state[filename]
        return new_state

    def get_lock(self, filename: str) -> FileLock | None:
        return self._locks.get(filename)
```

**Learn more:**

- [Immutability in Python](https://docs.python.org/3/library/dataclasses.html) - `frozen=True`
- [Pure Functions](https://en.wikipedia.org/wiki/Pure_function) - No side effects
- [Value Objects (DDD)](https://martinfowler.com/bliki/ValueObject.html) - Why FileLock is immutable

---

## Chapter 1.5: Adapter Layer (Storage Abstraction)

**File**: `backend/adapters/storage.py`

```python
from typing import Protocol, Dict
from pathlib import Path
import json
from datetime import datetime
from core.config import settings
from domain.locks import FileLock

class LockStorage(Protocol):
    """Interface for lock persistence."""
    def load(self) -> Dict[str, FileLock]: ...
    def save(self, locks: Dict[str, FileLock]) -> None: ...

class JSONLockStorage:
    """JSON file implementation."""

    def __init__(self, file_path: Path = settings.data_dir / "locks.json"):
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self):
        if not self.file_path.exists():
            self.file_path.write_text('{}')

    def load(self) -> Dict[str, FileLock]:
        data = json.loads(self.file_path.read_text())
        return {
            filename: FileLock(
                filename=lock_data['filename'],
                locked_by=lock_data['locked_by'],
                locked_at=datetime.fromisoformat(lock_data['locked_at']),
                message=lock_data['message']
            )
            for filename, lock_data in data.items()
        }

    def save(self, locks: Dict[str, FileLock]) -> None:
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

**Learn more:**

- [Protocol (PEP 544)](https://peps.python.org/pep-0544/) - Structural typing
- [Adapter Pattern](https://refactoring.guru/design-patterns/adapter) - Why abstractions matter
- [Dependency Inversion](https://en.wikipedia.org/wiki/Dependency_inversion_principle) - High-level doesn't depend on low-level

---

## Chapter 1.6: Service Layer

**File**: `backend/domain/locks.py` (add to same file)

```python
from adapters.storage import LockStorage

class LockService:
    """Orchestrates domain + storage."""

    def __init__(self, storage: LockStorage):
        self.storage = storage

    def checkout_file(self, filename: str, user: str, message: str) -> None:
        locks = self.storage.load()
        manager = LockManager(locks)
        new_locks = manager.acquire(filename, user, message)
        self.storage.save(new_locks)

    def checkin_file(self, filename: str, user: str, is_admin: bool = False) -> None:
        locks = self.storage.load()
        manager = LockManager(locks)
        new_locks = manager.release(filename, user, is_admin)
        self.storage.save(new_locks)

    def get_lock_info(self, filename: str) -> FileLock | None:
        locks = self.storage.load()
        manager = LockManager(locks)
        return manager.get_lock(filename)
```

**Learn more:**

- [Service Layer Pattern](https://martinfowler.com/eaaCatalog/serviceLayer.html) - Orchestration vs business logic
- [Transaction Script](https://martinfowler.com/eaaCatalog/transactionScript.html) - When to use services

---

## What We've Built

**Layers:**

```
API (FastAPI) ← next chapter
    ↓
Service (orchestration)
    ↓
Domain (business rules)
    ↓
Adapter (storage)
```

**Key benefits:**

- Domain logic testable without FastAPI/database
- Can swap JSON → Postgres by changing one class
- Business rules documented in code, not scattered

**Continue?** Next up: Chapter 1.7-1.10 will add the API layer (FastAPI routes, dependency injection, error handling).
