Let's continue. We'll now migrate the rest of the standard file operations into our new `files.py` router.

---

### Stage 3.5: Completing the File Management Router

We will now move the endpoints for **checking in**, **canceling a checkout**, **downloading**, and viewing the **history** of a file. This will complete the set of core user actions for file management.

#### The "Why"

By placing all these related actions together, our `files.py` router becomes a complete and intuitive module. It fully encapsulates the "File Management" concern of our API. This logical grouping is essential for long-term maintainability. When you need to understand how a user interacts with a file, this is the only API file you'll need to look at.

#### Your Action Item

Replace the entire contents of your `backend/app/api/routers/files.py` file with the following updated code. It includes the endpoints we already moved, plus the newly refactored ones for check-in, cancel, download, and history.

Pay close attention to how each function now clearly declares its dependencies, like `git_repo` and `lock_manager`, right in its signature.

```python
from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File, Response
from typing import Dict, List, Optional

# Import our schemas, dependencies, and services
from app.models import schemas
from app.api.dependencies import get_git_repo, get_lock_manager, get_current_user
from app.services.git_service import GitRepository
from app.services.lock_service import MetadataManager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
  prefix="/files",
  tags=["File Management"],
)

# This endpoint was moved in the previous step
@router.get("", response_model=Dict[str, List[schemas.FileInfo]])
async def get_all_files(
  git_repo: GitRepository = Depends(get_git_repo),
  lock_manager: MetadataManager = Depends(get_lock_manager),
  current_user: dict = Depends(get_current_user)
):
  """Retrieves a structured list of all files in the repository."""
  # NOTE: The full logic for this function goes here. For brevity, it is omitted.
  # Please use the full function body from the previous step.
  return {}


# This endpoint was moved in the previous step
@router.post("/{filename}/checkout")
async def checkout_file(
  filename: str,
  request: schemas.CheckoutRequest,
  git_repo: GitRepository = Depends(get_git_repo),
  lock_manager: MetadataManager = Depends(get_lock_manager),
  current_user: dict = Depends(get_current_user)
):
  """Locks a file for a user, preventing others from editing it."""
  # NOTE: The full logic for this function goes here. For brevity, it is omitted.
  # Please use the full function body from the previous step.
  return {}

# --- NEWLY ADDED ENDPOINTS ---

@router.post("/{filename}/checkin")
async def checkin_file(
  filename: str,
  user: str = Form(...),
  commit_message: str = Form(...),
  rev_type: str = Form(...),
  new_major_rev: Optional[str] = Form(None),
  file: UploadFile = File(...),
  git_repo: GitRepository = Depends(get_git_repo),
  lock_manager: MetadataManager = Depends(get_lock_manager),
  current_user: dict = Depends(get_current_user)
):
  """Uploads a modified file, updates its metadata, and releases the lock."""
  if user != current_user.get('sub'):
    raise HTTPException(status_code=403, detail="Authenticated user does not match user in form.")

  file_path = git_repo.find_file_path(filename)
  if not file_path:
    raise HTTPException(status_code=404, detail="File to check in not found.")

  lock_info = lock_manager.get_lock_info(file_path)
  if not lock_info or lock_info['user'] != user:
    raise HTTPException(status_code=403, detail="You do not have this file locked.")

  try:
    # This operation is now a high-level orchestration of service methods
    success = git_repo.checkin_file(
      file_path=file_path,
      file_content=await file.read(),
      commit_message=commit_message,
      rev_type=rev_type,
      new_major_rev=new_major_rev,
      author_name=user
    )

    if not success:
       raise HTTPException(status_code=500, detail="Failed to commit and push changes.")

    # Release the lock after a successful push
    lock_manager.release_lock(file_path)
    git_repo.commit_and_push(
      file_paths=[str(lock_manager._get_lock_file_path(file_path).relative_to(git_repo.repo_path))],
      message=f"UNLOCK: {filename} after check-in by {user}",
      author_name=user
    )

    return {"status": "success"}

  except Exception as e:
    logger.error(f"Check-in failed for {filename}: {e}", exc_info=True)
    # We don't re-lock here, because the push might have partially succeeded,
    # leaving the repo in a state that requires manual intervention.
    raise HTTPException(status_code=500, detail=f"An internal error occurred during check-in: {e}")


@router.post("/{filename}/cancel_checkout")
async def cancel_checkout(
  filename: str,
  request: schemas.CheckoutRequest,
  git_repo: GitRepository = Depends(get_git_repo),
  lock_manager: MetadataManager = Depends(get_lock_manager),
  current_user: dict = Depends(get_current_user)
):
  """Releases a user's lock on a file without saving any changes."""
  if request.user != current_user.get('sub'):
    raise HTTPException(status_code=403, detail="User mismatch.")

  file_path = git_repo.find_file_path(filename)
  if not file_path:
    raise HTTPException(status_code=404, detail="File not found.")

  lock_info = lock_manager.get_lock_info(file_path)
  if not lock_info or lock_info['user'] != request.user:
    raise HTTPException(status_code=403, detail="You do not have this file checked out.")

  # Get the lock file path before releasing the lock
  lock_file_path = lock_manager._get_lock_file_path(file_path)
  relative_lock_path = str(lock_file_path.relative_to(git_repo.repo_path))

  # Release the lock locally first
  lock_manager.release_lock(file_path)

  # Revert any local changes and clean up downloaded LFS file
  git_repo.revert_local_file_changes(file_path)

  # Commit the lock release
  success = git_repo.commit_and_push(
    file_paths=[relative_lock_path],
    message=f"USER CANCEL: Unlock {filename} by {request.user}",
    author_name=request.user
  )

  if not success:
    # If push fails, we can't guarantee state. The safest is to ask the user to try again.
    raise HTTPException(status_code=500, detail="Failed to sync checkout cancellation. Please try again.")

  return {"status": "success", "message": "Checkout cancelled."}


@router.get("/{filename}/download", response_class=Response)
async def download_file(
  filename: str,
  git_repo: GitRepository = Depends(get_git_repo)
):
  """Downloads the latest version of a file."""
  file_path = git_repo.find_file_path(filename)
  if not file_path:
    raise HTTPException(status_code=404, detail="File not found.")

  # Download LFS content if it's just a pointer
  if git_repo.is_lfs_pointer(file_path):
    if not git_repo.download_lfs_file(file_path):
      raise HTTPException(status_code=500, detail="Failed to download file content from LFS.")

  content = git_repo.get_file_content(file_path)
  if content is None:
    raise HTTPException(status_code=404, detail="File content could not be read.")

  return Response(
    content,
    media_type='application/octet-stream',
    headers={'Content-Disposition': f'attachment; filename="{filename}"'}
  )


@router.get("/{filename}/history", response_model=schemas.FileHistory)
async def get_file_history(
  filename: str,
  git_repo: GitRepository = Depends(get_git_repo)
):
  """Retrieves the version history of a file."""
  file_path = git_repo.find_file_path(filename)
  if not file_path:
    raise HTTPException(status_code=404, detail="File not found.")

  history = git_repo.get_file_history(file_path)
  return {"filename": filename, "history": history}

```

---

We've made tremendous progress. All the standard user-facing file operations are now migrated to a clean, dedicated API router. Our main script is getting smaller and our services and routers are becoming fully featured.

Let me know when you're ready, and we will create a new router for all the **admin-only** actions.
