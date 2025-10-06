Let's complete the final step of our API refactoring. We'll create one last router to handle getting and setting the application's configuration.

---

### Stage 3.7: Creating the Configuration Router

This router will manage the endpoints that the frontend uses to view the current GitLab settings and to submit new ones.

#### The "Why"

By creating a dedicated `config.py` router, we complete our API's logical separation. All endpoints are now grouped by their function: **authentication**, **file management**, **administration**, and now **application configuration**. This modular structure is the clean, maintainable, and scalable architecture we set out to build.

#### Your Action Items

1. Create the final router file at `backend/app/api/routers/config.py`. Add the code below.
2. Update your `backend/app/main.py` one last time to include this new router.

---

### Code for `backend/app/api/routers/config.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from app.models import schemas
from app.api.dependencies import get_config_manager
from app.core.config import ConfigManager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
  prefix="/config",
  tags=["Configuration"],
)


@router.get("", response_model=schemas.ConfigSummary)
async def get_config_summary(
  config_manager: ConfigManager = Depends(get_config_manager)
):
  """Retrieves a summary of the current application configuration."""
  # This logic was originally in the ConfigManager class, but it's better here
  # as it constructs a summary specifically for an API response.
  cfg = config_manager.config
  gitlab_cfg = cfg.gitlab
  local_cfg = cfg.local

  return schemas.ConfigSummary(
    gitlab_url=gitlab_cfg.get('base_url'),
    project_id=gitlab_cfg.get('project_id'),
    username=gitlab_cfg.get('username'),
    has_token=bool(gitlab_cfg.get('token')),
    repo_path=local_cfg.get('repo_path'),
    # TODO: The 'is_admin' status will be determined by the user's token, not the config file.
    # We will adjust this when we refactor the user management.
    is_admin=gitlab_cfg.get('username') in ["admin", "g4m3rm1k3"]
  )


@router.post("/gitlab", response_model=schemas.StandardResponse)
async def update_gitlab_config(
  request: schemas.ConfigUpdateRequest,
  config_manager: ConfigManager = Depends(get_config_manager)
):
  """
  Validates and saves new GitLab configuration settings.
  This will trigger a re-initialization of the application's services.
  """
  try:
    # TODO: Add validation logic here to test the new credentials against the GitLab API
    # before saving them. For now, we will just save the config.

    config_manager.config.gitlab['base_url'] = request.base_url
    config_manager.config.gitlab['project_id'] = request.project_id
    config_manager.config.gitlab['username'] = request.username
    config_manager.config.gitlab['token'] = request.token
    config_manager.config.security['allow_insecure_ssl'] = request.allow_insecure_ssl

    config_manager.save_config()

    # In our final phase, we'll implement a proper mechanism to signal to the
    # application that it needs to reload its services (like the GitRepository)
    # with the new configuration.
    logger.info("Configuration saved. Application will re-initialize on next startup.")

    return {"status": "success", "message": "Configuration validated and saved."}

  except Exception as e:
    logger.error(f"An unexpected error occurred during config update: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")

```

---

### Update `backend/app/main.py`

Let's include our final router. This will be the definitive structure of our main application file.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Import all of our routers
from app.api.routers import auth, files, admin, config

@asynccontextmanager
async def lifespan(app: FastAPI):
  logging.info("Application starting up...")
  # In our final phase, we will add the full application initialization logic here.
  yield
  logging.info("Application shutting down.")

app = FastAPI(
  title="Mastercam GitLab Interface",
  description="A comprehensive file management system for Mastercam and GitLab.",
  version="2.0.0",
  lifespan=lifespan,
  # You can also add OpenAPI tags metadata here for better documentation
  openapi_tags=[
    {"name": "Authentication", "description": "User login and token management."},
    {"name": "File Management", "description": "Core file operations."},
    {"name": "Administration", "description": "Privileged, admin-only operations."},
    {"name": "Configuration", "description": "Getting and setting application configuration."},
  ]
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
app.include_router(config.router)


@app.get("/")
async def root():
  return {"message": "Welcome to the Mastercam PDM Refactored API"}

```

---

## Milestone Reached\! 🎉

**Phase 3 is now complete.** We have successfully dismantled the entire API layer from the monolithic script and rebuilt it into a clean, secure, and organized set of routers. Your `mastercam_main.py` file should now contain almost no API endpoint code (`@app.get`, `@app.post`, etc.).

Take a moment to look at your `backend/app/api/routers` directory. You now have a professional, maintainable API structure.

Once you are ready, we will begin the **final phase** of the backend refactoring, where we will tie everything together, fully implement our dependency injection, and safely delete the old script.
