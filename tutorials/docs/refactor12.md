Let's get started. Now we'll create a dedicated router for all the privileged, administrator-only actions.

---

### Stage 3.6: Creating the Admin Router

Separating standard user actions from admin actions is a critical security and design practice. We will create a new file, `app/api/routers/admin.py`, to house all endpoints that require elevated privileges, like overriding a lock or deleting a file.

#### The "Why"

This isn't just about organization; it's about **security and clarity**.

- **Principle of Least Privilege:** By moving admin endpoints to a dedicated router, we create a clear security boundary. It's immediately obvious which parts of our API are sensitive. We can apply stricter security checks to this entire group of routes easily.
- **Clarity of Intent:** When another developer (or you, in six months) looks at the project structure, the purpose of `admin.py` is instantly clear. This reduces the risk of accidentally exposing a powerful endpoint.
- **Simplified Maintenance:** When you need to add a new admin feature, you know exactly where the code should go.

For these routes, we'll use the `get_current_admin_user` dependency we created earlier. This single line will automatically ensure that only an authenticated admin can ever access these endpoints.

#### Your Action Items

1. Create a new file at `backend/app/api/routers/admin.py`. Add the code below to it.
2. Update your existing `backend/app/main.py` file to include this new router.

---

### Code for `backend/app/api/routers/admin.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status

# Import our schemas, dependencies, and services
from app.models import schemas
from app.api.dependencies import (
  get_git_repo,
  get_lock_manager,
  get_current_admin_user
)
from app.services.git_service import GitRepository
from app.services.lock_service import MetadataManager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
  prefix="/admin", # All routes here will start with /admin
  tags=["Administration"],
  dependencies=[Depends(get_current_admin_user)] # IMPORTANT: This protects ALL routes in this file
)

@router.post("/files/{filename}/override", response_model=schemas.StandardResponse)
async def admin_override_lock(
  filename: str,
  request: schemas.AdminOverrideRequest,
  admin_user: dict = Depends(get_current_admin_user), # We can still get the user info if needed
  git_repo: GitRepository = Depends(get_git_repo),
  lock_manager: MetadataManager = Depends(get_lock_manager)
):
  """(Admin) Forcibly removes a lock from a file."""
  if request.admin_user != admin_user.get('sub'):
    raise HTTPException(status_code=403, detail="Admin username mismatch.")

  file_path = git_repo.find_file_path(filename)
  if not file_path:
    raise HTTPException(status_code=404, detail="File not found.")

  lock_info = lock_manager.get_lock_info(file_path)
  if not lock_info:
    return {"status": "success", "message": "File was already unlocked."}

  lock_file_path = lock_manager._get_lock_file_path(file_path)
  relative_lock_path = str(lock_file_path.relative_to(git_repo.repo_path))

  lock_manager.release_lock(file_path)

  success = git_repo.commit_and_push(
    file_paths=[relative_lock_path],
    message=f"ADMIN OVERRIDE: Unlock {filename} by {request.admin_user}",
    author_name=request.admin_user
  )

  if not success:
    # Best effort to restore the lock if push fails
    lock_manager.create_lock(file_path, lock_info['user'], force=True)
    raise HTTPException(status_code=500, detail="Failed to commit lock override.")

  return {"status": "success", "message": f"Lock on '{filename}' has been overridden."}


@router.delete("/files/{filename}/delete", response_model=schemas.StandardResponse)
async def admin_delete_file(
  filename: str,
  admin_user: dict = Depends(get_current_admin_user),
  git_repo: GitRepository = Depends(get_git_repo),
  lock_manager: MetadataManager = Depends(get_lock_manager)
):
  """(Admin) Permanently deletes a file and its metadata."""
  file_path = git_repo.find_file_path(filename)
  if not file_path:
    raise HTTPException(status_code=404, detail="File not found.")

  if lock_manager.get_lock_info(file_path):
    raise HTTPException(status_code=409, detail="Cannot delete a file that is currently checked out.")

  files_to_remove = git_repo.delete_file_and_metadata(file_path)

  success = git_repo.commit_and_push(
    file_paths=files_to_remove,
    message=f"ADMIN DELETE: Remove {filename} by {admin_user.get('sub')}",
    author_name=admin_user.get('sub')
  )

  if not success:
    raise HTTPException(status_code=500, detail="Failed to commit file deletion.")

  return {"status": "success", "message": f"File '{filename}' permanently deleted."}

# We will add the other admin endpoints (revert, reset repo, etc.) here later.
```

---

### Update `backend/app/main.py`

Now, let's register our new admin router with the main application.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Import all of our routers
from app.api.routers import auth, files, admin

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

# Include all routers in our main application
app.include_router(auth.router)
app.include_router(files.router)
app.include_router(admin.router)


@app.get("/")
async def root():
  return {"message": "Welcome to the Mastercam PDM Refactored API"}

```

---

We have now successfully segregated our API based on user roles. Standard file operations are in one place, and privileged admin actions are in another, protected place.

Once you're ready, we'll create our final router for handling application configuration.
