"""
File management business logic

Hanles:
- Reading files from filesystem
- Lock state management
- File metadata extraction
"""

from pathlib import Path
from typing import List, Dict, Optional
import json
import logging

from app.utils.file_locking import LockedFile

logger = logging.getLogger(__name__)

# Section 1 Lock management


class LockManager:
    """
    Manage file lock state
    """

    def __init__(self, locks_file: Path):
        self.locks_file = locks_file

        # Ensure file exists
        if not self.locks_file.exists():
            self.locks_file.write_text('{}')

    def load_locks(self) -> Dict[str, dict]:
        """
        Load current lock state.

        Returns:
            Dict mapping filename to lock info
        """
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
            logger.error(f"Faled to load locks: {e}")
            return {}

    def save_locks(self, locks: dict):
        """
        Save lock state atomatically.

        Args:
            locks: Dict mapping filename to lock info
        """
        try:
            with LockedFile(self.locks_file, 'w') as f:
                json.dump(locks, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save locks: {e}")
            raise

    def is_locked(self, filename: str) -> bool:
        """Checked if file is locked"""
        locks = self.load_locks()
        return filename in locks

    def get_lock_info(self, filename: str) -> Optional[dict]:
        """Get lock information for a file"""
        locks = self.load_locks()
        return locks.get(filename)

    def acquire_lock(self, filename: str, user: str, message: str):
        """ 
        Acquire lock on a file

        Raises:
            ValueError: If file i already locked
        """
        locks = self.load_locks()

        if filename in locks:
            existing = locks[filename]
            raise ValueError(
                f"File already locked by {existing['user']}"
            )
        # Add lock
        from datetime import datetime, timezone
        locks[filename] = {
            'user': user,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'message': message
        }

        self.save_locks(locks)
        logger.info(f"Lock acquired: {filename} by {user}")

    def release_lock(self, filename: str, user: str):
        """Release lock on a file.

        Args:
            filename: File to unlock
            user: User releasing lock (must own lock)

        Raises:
            ValueError: If file not locked or wrong user
        """
        locks = self.load_locks()

        if filename not in locks:
            raise ValueError("File is not locked")

        if locks[filename]["user"] != user:
            raise ValueError(
                f"Lock owned by {locks[filename]['user']}, not {user}"
            )
        # Remove lock
        del locks[filename]
        self.save_locks(locks)
        logger.info(f"Lock released: {filename} by {user}")


# SECTION 2 FILE REPO

class FileRepository:
    """
    Manage file operations on teh repositroy directory
    """

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path

    # Ensure repo directory exists
    self.repo_path.mkdir(parents=True, exists_ok=True)
