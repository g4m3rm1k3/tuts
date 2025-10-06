Of course. Let's tackle the largest part of the API: the endpoints for managing files.

---

### Stage 3.4: Creating the File Management Router

We'll now create a new router, `files.py`, to handle all the core operations of the application: listing, checking out, checking in, downloading, and viewing the history of files. This will be the busiest "department" in our application.

#### The "Why"

By grouping all file-related endpoints, we create a clear and logical structure. When you need to change anything about how users interact with files, you'll know that `api/routers/files.py` is the place to go. This colocation of related logic is a hallmark of a well-organized and maintainable project.

We will start by moving just the first couple of endpoints: the one to **list all files** and the one to **checkout a file**. The checkout endpoint is a perfect example of how dependency injection simplifies complex operations.

#### Your Action Items

1. Create a new file at `backend/app/api/routers/files.py`. Add the code below to it.
2. Update your existing `backend/app/main.py` file to include this new router.

---

### Code for `backend/app/api/routers/files.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List

# Import our schemas, dependencies, and services
from app.models import schemas
from app.api.dependencies import get_git_repo, get_lock_manager, get_current_user
from app.services.git_service import GitRepository
from app.services.lock_service import MetadataManager

router = APIRouter(
  prefix="/files",
  tags=["File Management"],
)

@router.get("", response_model=Dict[str, List[schemas.FileInfo]])
async def get_all_files(
  git_repo: GitRepository = Depends(get_git_repo),
  lock_manager: MetadataManager = Depends(get_lock_manager),
  current_user: dict = Depends(get_current_user)
):
  """
  Retrieves a structured list of all files in the repository,
  enriched with metadata and lock status.
  """
  if not git_repo or not lock_manager:
    raise HTTPException(status_code=503, detail="Repository not initialized.")

  # This complex logic was originally the global _get_current_file_state function.
  # It's now properly encapsulated within an API endpoint. In a future refactor,
  # we could even move this logic into its own service method.
  try:
    # 1. Get all raw files from the git repository
    all_physical_files = git_repo.list_files()

    # 2. Get all active locks from the lock manager
    all_locks = {lock['file']: lock for lock in lock_manager.get_all_locks()}

    # 3. Process and enrich the file data
    processed_files = {}
    for file_data in all_physical_files:
      file_path = file_data['path']

      # Enrich with lock status
      lock_info = all_locks.get(file_path)
      if lock_info:
        file_data['locked_by'] = lock_info['user']
        file_data['locked_at'] = lock_info['timestamp']
        file_data['status'] = "checked_out_by_user" if lock_info['user'] == current_user.get('sub') else "locked"
      else:
        file_data['status'] = "unlocked"

      # TODO: Enrich with metadata (revision, description) by reading .meta.json files.

      # Group files by the first two digits of their name
      group_name = "Miscellaneous"
      if file_data['filename'].isdigit() and len(file_data['filename']) >= 7:
         group_name = f"{file_data['filename'][:2]}XXXXX"

      if group_name not in processed_files:
        processed_files[group_name] = []

      processed_files[group_name].append(schemas.FileInfo(**file_data))

    return processed_files

  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Failed to retrieve file list: {e}")


@router.post("/{filename}/checkout")
async def checkout_file(
  filename: str,
  request: schemas.CheckoutRequest,
  git_repo: GitRepository = Depends(get_git_repo),
  lock_manager: MetadataManager = Depends(get_lock_manager),
  current_user: dict = Depends(get_current_user)
):
  """
  Locks a file for a user, preventing others from editing it.
  This demonstrates injecting multiple services into one endpoint.
  """
  if not git_repo or not lock_manager:
    raise HTTPException(status_code=503, detail="Repository not initialized.")

  # Ensure the requesting user matches the token user
  if request.user != current_user.get('sub'):
    raise HTTPException(status_code=403, detail="User in request does not match authenticated user.")

  # 1. Find the file in the repository
  file_path = git_repo.find_file_path(filename) # We'll need to add this helper method to GitRepository
  if not file_path:
    raise HTTPException(status_code=404, detail="File not found")

  # 2. Check for an existing lock
  existing_lock = lock_manager.get_lock_info(file_path)
  if existing_lock:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail=f"File is already locked by {existing_lock['user']}"
    )

  # 3. Download the LFS file content if it's a pointer
  if git_repo.is_lfs_pointer(file_path):
    logger.info(f"Downloading LFS file on-demand for checkout: {file_path}")
    if not git_repo.download_lfs_file(file_path):
      raise HTTPException(status_code=500, detail="Failed to download file content from LFS.")

  # 4. Create the lock
  lock_file_path = lock_manager.create_lock(file_path, request.user)
  if not lock_file_path:
    raise HTTPException(status_code=500, detail="Failed to create lock file.")

  # 5. Commit and push the new lock file to the remote repository
  try:
    relative_lock_path = str(lock_file_path.relative_to(git_repo.repo_path))
    commit_message = f"LOCK: {filename} by {request.user}"

    success = git_repo.commit_and_push([relative_lock_path], commit_message, request.user)
    if not success:
      # If the push fails, we must roll back the local lock creation
      lock_manager.release_lock(file_path)
      raise HTTPException(status_code=500, detail="Failed to push lock file to remote repository.")

    return {"status": "success", "message": f"File '{filename}' checked out successfully."}
  except Exception as e:
    # General error handling, ensure rollback
    lock_manager.release_lock(file_path)
    raise HTTPException(status_code=500, detail=f"An error occurred during checkout: {e}")

```

---

### Update `backend/app/main.py`

Now, tell your main application to use this new router. Replace the contents of `backend/app/main.py` with this:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Import both of our new routers
from app.api.routers import auth, files

@asynccontextmanager
async def lifespan(app: FastAPI):
  logging.info("Application starting up...")
  yield
  logging.info("Application shutting down.")

app = FastAPI(
  title="Mastercam GitLab Interface",
  description="A comprehensive file management system for Mastercam and GitLab.",
  version="2.0.0",
  lifespan=lifespan
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  methods=["*"],
  allow_headers=["*"],
)

# Include both routers in our main application
app.include_router(auth.router)
app.include_router(files.router)

@app.get("/")
async def root():
  return {"message": "Welcome to the Mastercam PDM Refactored API"}

```

---

We've now started building our primary API module. The `checkout_file` endpoint is a perfect illustration of the service-oriented architecture: it accepts a web request, then acts as an orchestrator, telling the `GitService` and `LockService` what to do.

Let me know when you're ready, and we'll migrate the remaining file management endpoints.
