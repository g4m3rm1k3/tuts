Excellent. Let's proceed to the next step in our scaffolding phase. We're going to create a "data dictionary" for our application by isolating all the Pydantic models.

---

### Stage 1.4: Isolating Data Models (Schemas)

Right now, the definitions for your data structures (like `FileInfo`, `CheckoutRequest`, etc.) are mixed in with all the other logic. We're going to pull them out and give them their own dedicated file. In professional development, these are often called "schemas."

#### The "Why"

This is a crucial organizational step for several reasons:

- **Single Source of Truth:** This file becomes the definitive reference for the shape of data in your application. Anyone working on the project can look at `schemas.py` to understand exactly what a "file object" or a "user object" looks like.
- **API Contract:** These models define the **contract** between your frontend and backend. The `schemas.py` file clearly states, "To check out a file, you _must_ send me data that looks like the `CheckoutRequest` model." This prevents a whole class of bugs and makes the API predictable.
- **The DRY Principle ("Don't Repeat Yourself"):** By defining these models in one place, they can be imported and used by any other part of the application that needs them (like the API layer and the service layer) without having to redefine them.

#### Your Action Item

Create the file `backend/app/models/schemas.py`. Copy all of the classes that inherit from `BaseModel` from your original `mastercam_main.py` file into this new file.

Here is the complete code for `backend/app/models/schemas.py`:

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Note: We are only moving the Pydantic models here.
# The validation functions will be moved to a different 'utils' file later.

class FileInfo(BaseModel):
    filename: str = Field(..., description="The name of the file")
    path: str = Field(..., description="The relative path of the file in the repository")
    status: str = Field(..., description="File status: 'locked', 'unlocked', or 'checked_out_by_user'")
    locked_by: Optional[str] = Field(None, description="Username of the user who has the file locked")
    locked_at: Optional[str] = Field(None, description="ISO timestamp when the file was locked")
    size: Optional[int] = Field(None, description="File size in bytes")
    modified_at: Optional[str] = Field(None, description="ISO timestamp of last modification")
    description: Optional[str] = Field(None, description="File description from metadata")
    revision: Optional[str] = Field(None, description="Current revision number (e.g., '1.5')")
    is_link: bool = Field(False, description="True if this is a linked/virtual file")
    master_file: Optional[str] = Field(None, description="The master file this link points to")

class CheckoutInfo(BaseModel):
    filename: str = Field(..., description="Name of the checked out file")
    path: str = Field(..., description="Repository path of the file")
    locked_by: str = Field(..., description="User who has the file checked out")
    locked_at: str = Field(..., description="ISO timestamp when checkout occurred")
    duration_seconds: float = Field(..., description="How long the file has been checked out in seconds")

class DashboardStats(BaseModel):
    active_checkouts: List[CheckoutInfo] = Field(..., description="List of currently checked out files")

class CheckoutRequest(BaseModel):
    user: str = Field(..., description="Username requesting the checkout")

class AdminOverrideRequest(BaseModel):
    admin_user: str = Field(..., description="Admin username performing the override")

class AdminDeleteRequest(BaseModel):
    admin_user: str = Field(..., description="Admin username performing the deletion")

class SendMessageRequest(BaseModel):
    recipient: str = Field(..., description="Username of the message recipient")
    message: str = Field(..., description="Message content to send")
    sender: str = Field(..., description="Username of the message sender")

class AckMessageRequest(BaseModel):
    message_id: str = Field(..., description="Unique identifier of the message to acknowledge")
    user: str = Field(..., description="Username acknowledging the message")

class ConfigUpdateRequest(BaseModel):
    base_url: str = Field(alias="gitlab_url", description="GitLab instance URL (e.g., https://gitlab.example.com)")
    project_id: str = Field(..., description="GitLab project ID")
    username: str = Field(..., description="GitLab username")
    token: str = Field(..., description="GitLab personal access token")
    allow_insecure_ssl: bool = Field(False, description="Whether to allow insecure SSL connections")

class AdminRevertRequest(BaseModel):
    admin_user: str = Field(..., description="Admin username performing the revert")
    commit_hash: str = Field(..., description="Git commit hash to revert")

class ActivityItem(BaseModel):
    event_type: str = Field(..., description="Type of activity")
    filename: str = Field(..., description="Name of the file involved")
    user: str = Field(..., description="Username who performed the action")
    timestamp: str = Field(..., description="ISO timestamp of the activity")
    commit_hash: str = Field(..., description="Git commit hash associated with the activity")
    message: str = Field(..., description="Commit message or activity description")
    revision: Optional[str] = Field(None, description="File revision if applicable")

class ActivityFeed(BaseModel):
    activities: List[ActivityItem] = Field(..., description="List of recent activities")

class AppConfig(BaseModel):
    version: str = "1.0.0"
    gitlab: dict = Field(default_factory=dict)
    local: dict = Field(default_factory=dict)
    ui: dict = Field(default_factory=dict)
    security: dict = Field(default_factory=lambda: {"allow_insecure_ssl": False})
    polling: dict = Field(default_factory=lambda: {"enabled": True, "interval_seconds": 15, "check_on_activity": True})

class StandardResponse(BaseModel):
    status: str = Field(..., description="Response status: 'success' or 'error'")
    message: Optional[str] = Field(None, description="Human-readable message")

class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=8)
    gitlab_token: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    is_admin: bool

class ConfigSummary(BaseModel):
    gitlab_url: Optional[str] = Field(None, description="Configured GitLab URL")
    project_id: Optional[str] = Field(None, description="Configured GitLab project ID")
    username: Optional[str] = Field(None, description="Configured GitLab username")
    has_token: bool = Field(..., description="Whether a GitLab token is configured")
    repo_path: Optional[str] = Field(None, description="Local repository path")
    is_admin: bool = Field(..., description="Whether the current user has admin privileges")

class AdminRequest(BaseModel):
    admin_user: str

class UserList(BaseModel):
    users: List[str] = Field(..., description="List of usernames from Git history")

class FileHistory(BaseModel):
    filename: str = Field(..., description="Name of the file")
    history: List[Dict[str, Any]] = Field(..., description="List of historical commits for this file")
```

---

Great\! We've now successfully extracted our application's "dictionary." Our `mastercam_main.py` file is already getting smaller, and our new structure is starting to take shape.

Let me know when you're ready, and we will move on to the next step: separating the configuration logic.
