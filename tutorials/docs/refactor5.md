Alright, let's dive into **Phase 2: Extracting Core Services**.

This is where our application's architecture really starts to take shape. We're moving from organizing files to organizing _logic_. We'll be creating "services"—specialized modules that handle the application's core business logic.

First up is the heart of the application: the code that interacts with Git.

---

### Stage 2.1: Building the Git Service

We will now create `app/services/git_service.py`. This file's sole responsibility will be to manage the Git repository, including all regular Git commands and all the complex Git-LFS (Large File Storage) logic.

#### The "Why": The Service Layer

In software architecture, a **Service Layer** is a crucial component that acts as the "brains" of the operation. It sits between the API layer (which talks to the web) and the core logic.

- **Orchestration:** A single user action might require multiple steps. For example, "checking in a file" involves updating the file on disk, creating metadata, removing a lock file, committing the changes, and pushing to the remote. The `GitService` will contain a method that orchestrates all these steps in the correct order.
- **Reusability:** Once we have a `git_service.checkin_file()` method, we can reuse it anywhere—not just from a web request. We could use it in a future command-line tool or an automated script without rewriting the logic.
- **Testability:** This is a huge benefit. We can write automated tests for our `checkin_file()` method directly, without having to simulate a fake web request. We can test the core logic of our application in isolation, which is much faster and more reliable.

As we build this, you'll see our first step in eliminating the global `app_state` dictionary. We will use a professional pattern called **Dependency Injection**, where we pass necessary components (like the config manager) directly to the class when we create it.

#### Your Action Item

Create the file `backend/app/services/git_service.py`. Add the following code. This contains the `GitRepository` class and all the Git-LFS helper functions from your original script.

```python
import os
import sys
import subprocess
import logging
import shutil
import time
import re
import socket
import json
from pathlib import Path
from typing import List, Optional, Dict, Any, TYPE_CHECKING

import git
from git import Actor, Repo
import psutil

# We use TYPE_CHECKING to import classes just for type hints,
# preventing circular import errors at runtime.
if TYPE_CHECKING:
  from app.core.config import ConfigManager
  from app.services.lock_service import ImprovedFileLockManager

logger = logging.getLogger(__name__)


# --- Git LFS Utility Functions ---

def get_bundled_git_lfs_path() -> Optional[Path]:
  """Return the Path to a bundled git-lfs executable if it exists."""
  try:
    # Path when running as a packaged executable (e.g., with PyInstaller)
    if getattr(sys, "frozen", False) and hasattr(sys, '_MEIPASS'):
      base_path = Path(sys._MEIPASS)
    # Path when running as a .py script
    else:
      base_path = Path(__file__).resolve().parents[2] # From /app/services to /backend

    git_lfs_exe = base_path / "libs" / "git-lfs.exe"
    return git_lfs_exe if git_lfs_exe.is_file() else None
  except Exception as e:
    logger.error(f"Error finding bundled git-lfs: {e}")
    return None

def setup_git_lfs_path() -> bool:
  """Ensure git-lfs is in the system's PATH, preferring the bundled version."""
  bundled_lfs = get_bundled_git_lfs_path()
  if bundled_lfs:
    lfs_dir = str(bundled_lfs.parent)
    # Add the directory to the start of the PATH to give it priority.
    if lfs_dir not in os.environ.get('PATH', ''):
      os.environ['PATH'] = f"{lfs_dir}{os.pathsep}{os.environ['PATH']}"
      logger.info(f"Temporarily added bundled Git LFS directory to PATH: {lfs_dir}")

    try:
      result = subprocess.run(
        [str(bundled_lfs), "version"], capture_output=True, text=True, check=True, timeout=5
      )
      logger.info(f"Using bundled Git LFS: {result.stdout.strip()}")
      return True
    except Exception as e:
      logger.warning(f"Bundled Git LFS found but failed verification: {e}")
      return False

  # Fallback to checking for a system-wide installation
  try:
    result = subprocess.run(
      ["git-lfs", "version"], capture_output=True, text=True, check=True, timeout=5
    )
    logger.info(f"Using system Git LFS: {result.stdout.strip()}")
    return True
  except Exception as e:
    logger.error(f"FATAL: No Git LFS found on the system or bundled with the application: {e}")
    return False


class GitRepository:
  """A class to manage all interactions with a local Git repository."""

  def __init__(self, repo_path: Path, remote_url: str, token: str, config_manager: 'ConfigManager', lock_manager: 'ImprovedFileLockManager'):
    self.repo_path = repo_path
    self.lock_manager = lock_manager
    self.config_manager = config_manager
    self.remote_url_with_token = f"https://oauth2:{token}@{remote_url.split('://')[-1]}"
    self.git_env = self._create_git_environment()

    # Initialize the repository (clone if needed)
    self.repo: Optional[Repo] = self._init_repo()

    if self.repo:
      self._configure_lfs()

  def _create_git_environment(self) -> Dict[str, str]:
    """Creates a customized environment dictionary for running Git commands."""
    git_env = os.environ.copy()
    bundled_lfs = get_bundled_git_lfs_path()

    if bundled_lfs:
      lfs_dir = str(bundled_lfs.parent)
      git_env["PATH"] = f"{lfs_dir}{os.pathsep}{git_env.get('PATH', '')}"
      git_env["GIT_LFS_PATH"] = str(bundled_lfs)
      logger.info(f"Git environment will use bundled Git LFS at {bundled_lfs}")
    else:
      logger.warning("No bundled Git LFS found, relying on system installation.")

    # Configure SSL verification based on app settings
    allow_insecure = self.config_manager.config.security.get("allow_insecure_ssl", False)
    if allow_insecure:
      git_env["GIT_SSL_NO_VERIFY"] = "true"
      logger.warning("GIT_SSL_NO_VERIFY is enabled. SSL verification is turned off.")

    return git_env

  def _init_repo(self) -> Optional[Repo]:
    """
    Initializes the repository. Clones it if it doesn't exist,
    or opens it if it does. Includes retry logic for robustness.
    """
    # ... [The extensive _init_repo, _cleanup_corrupted_repo, etc. methods from the original file go here]
    # This logic is highly specific and can be moved directly.
    # For brevity in this response, we'll represent it as a placeholder.
    # In your file, you should copy the full methods:
    # _init_repo, _cleanup_corrupted_repo, _kill_git_processes, _remove_git_locks,
    # _force_remove_directory, and _wait_for_directory_removal

    # This is a simplified version for demonstration:
    if not (self.repo_path / ".git").exists():
      logger.info(f"Cloning repository to {self.repo_path}...")
      try:
        return Repo.clone_from(self.remote_url_with_token, self.repo_path, env=self.git_env)
      except git.exc.GitCommandError as e:
        logger.error(f"Failed to clone repository: {e.stderr}")
        return None
    else:
      logger.info(f"Opening existing repository at {self.repo_path}")
      try:
        return Repo(self.repo_path)
      except git.exc.InvalidGitRepositoryError:
        logger.error("Invalid Git repository. Consider a manual reset.")
        return None

  def _configure_lfs(self):
    """Configures Git LFS for the repository to only download files on demand."""
    # ... [The full _configure_lfs method from the original file goes here]
    pass

  # --- Public API Methods of the Service ---

  def pull_latest_changes(self):
    """Fetches the latest changes from the remote and resets the local branch."""
    # ... [Code from the original `pull` method]
    pass

  def commit_and_push(self, file_paths: List[str], message: str, author_name: str) -> bool:
    """Commits files and pushes them to the remote repository."""
    # ... [Code from the original `commit_and_push` method]
    return True # Placeholder

  def list_files(self) -> List[Dict[str, Any]]:
    """Lists all relevant files in the repository."""
    # ... [Code from the original `list_files` method, but improved to be more generic]
    return [] # Placeholder

  def get_file_history(self, file_path: str) -> List[Dict[str, Any]]:
    """Retrieves the commit history for a specific file."""
    # ... [Code from the original `get_file_history` method]
    return [] # Placeholder

  # ... and so on for all other public methods like `download_lfs_file`, `is_lfs_pointer`, etc.
```

_Note: For brevity, I've omitted the full code for some of the very long, complex methods like `_init_repo`. Please copy the full, original methods into your new file. The key change is the class structure and the use of dependency injection in `__init__`._

---

We have now created the most important service in our application. We've taken a huge chunk of logic out of the main script and given it a clear, defined home. We also took a major step toward eliminating `app_state` by passing the `ConfigManager` directly into our `GitRepository`.

Please confirm once you've created this file. Next, we will create the `LockService`, which this `GitService` depends on.
