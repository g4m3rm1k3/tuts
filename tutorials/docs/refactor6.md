Perfect, using stubs is a great way to focus on the architecture. Let's move on to the next service.

This step will be to create the service that manages file checkouts and metadata—essentially, the traffic cop for your file system.

---

### Stage 2.2: Building the Lock & Metadata Service

We will now create the file `app/services/lock_service.py`. This module will be responsible for all file locking operations: creating lock files when a user checks out a file, checking the status of locks, releasing them, and managing the associated `.meta.json` files.

#### The "Why"

Creating a dedicated service for locking is another direct application of the **Single Responsibility Principle (SRP)**.

- **Clear Responsibility:** This module's only job is to answer questions about the state of a file: Is it locked? Who locked it? When? It also handles the mechanics of creating and deleting the lock and metadata files that represent this state.
- **Decoupling:** Our `GitService` and our API endpoints will need to lock and unlock files, but they shouldn't care _how_ it's done. Is the lock information stored in a JSON file? A database? A cloud service? By creating a `LockService`, we hide these implementation details. This means if we ever wanted to change our locking strategy (for example, to use a more advanced system like Redis for a multi-server setup), we would only have to change this one file. The rest of the application would continue to work unchanged.
- **Code Cleanup:** This is also a great opportunity to clean up our code. Your original script had two locking classes: `FileLockManager` and `ImprovedFileLockManager`. We will move the superior one (`ImprovedFileLockManager`) and the `MetadataManager` here, and completely discard the old one.

#### Your Action Item

Create the file `backend/app/services/lock_service.py` and add the following code. It contains the `ImprovedFileLockManager` and `MetadataManager` classes from your original script, now organized as a cohesive service.

```python
import json
import logging
import os
import re
import socket
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

import psutil

logger = logging.getLogger(__name__)


class ImprovedFileLockManager:
  """
  Manages a repository-wide lock to prevent concurrent Git operations
  like 'git pull' and 'git commit' from conflicting.
  This is an OS-level lock for short, critical operations.
  """

  def __init__(self, lock_file_path: Path):
    self.lock_file_path = lock_file_path
    self.lock_file = None
    self.max_lock_age_seconds = 300 # 5 minutes

  # ... [Copy the full methods for ImprovedFileLockManager here: __enter__, __exit__, _is_stale_lock, etc.]
  # For brevity, I am using a placeholder.
  def __enter__(self):
    logger.debug(f"Attempting to acquire repository lock at {self.lock_file_path}...")
    # In your file, paste the full, robust __enter__ logic from the original script.
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    logger.debug(f"Releasing repository lock at {self.lock_file_path}...")
    # In your file, paste the full __exit__ logic from the original script.
    pass


class MetadataManager:
  """
  Manages the application-level concept of file checkouts (user locks).
  This creates/deletes '.lock' files in a dedicated '.locks' directory
  to represent a user having "checked out" a file for editing.
  """

  def __init__(self, repo_path: Path):
    self.repo_path = repo_path
    self.locks_dir = self.repo_path / '.locks'
    self.locks_dir.mkdir(parents=True, exist_ok=True)

  def _get_lock_file_path(self, file_path_str: str) -> Path:
    """Creates a sanitized, safe filename for the lock file."""
    sanitized = file_path_str.replace(os.path.sep, '_').replace('.', '_')
    return self.locks_dir / f"{sanitized}.lock"

  def create_lock(self, file_path: str, user: str, force: bool = False) -> Optional[Path]:
    """Creates a lock file for a user, indicating a checkout."""
    lock_file = self._get_lock_file_path(file_path)
    if lock_file.exists() and not force:
      logger.warning(f"Attempted to create lock for already-locked file: {file_path}")
      return None

    lock_data = {
      "file": file_path,
      "user": user,
      "timestamp": datetime.now(timezone.utc).isoformat()
    }
    lock_file.write_text(json.dumps(lock_data, indent=2))
    return lock_file

  def release_lock(self, file_path: str):
    """Releases a lock by deleting the lock file."""
    self._get_lock_file_path(file_path).unlink(missing_ok=True)

  def get_lock_info(self, file_path: str) -> Optional[Dict]:
    """Reads and returns the contents of a lock file if it exists."""
    lock_file = self._get_lock_file_path(file_path)
    if not lock_file.exists():
      return None

    try:
      return json.loads(lock_file.read_text())
    except (json.JSONDecodeError, FileNotFoundError):
      logger.warning(f"Could not read or parse lock file: {lock_file}")
      # Clean up corrupted/empty lock file
      lock_file.unlink(missing_ok=True)
      return None

  def get_all_locks(self) -> list[dict]:
    """Scans the .locks directory and returns all active locks."""
    active_locks = []
    if not self.locks_dir.exists():
      return active_locks

    now_utc = datetime.now(timezone.utc)
    for lock_file in self.locks_dir.glob('*.lock'):
      lock_info = self.get_lock_info(lock_file.stem) # Re-use get_lock_info to handle bad files
      if lock_info:
        locked_at_dt = datetime.fromisoformat(lock_info["timestamp"].replace('Z', '+00:00'))
        duration = (now_utc - locked_at_dt).total_seconds()
        lock_info['duration_seconds'] = duration
        active_locks.append(lock_info)
    return active_locks

```

---

Excellent. We've now finished scaffolding our "core" and "services" layers. All the heavy lifting and business logic for the application now have a proper home in `git_service.py` and `lock_service.py`. Our `mastercam_main.py` file should be getting significantly smaller\!

This completes Phase 2. We are now ready to begin **Phase 3**, where we will rebuild the API layer using Routers and Dependency Injection. This is where we'll see the true power of this new architecture.

Ready to start refactoring the API endpoints?
