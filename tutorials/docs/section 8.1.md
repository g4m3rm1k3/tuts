# PDM Tutorial - Stage 8: Hybrid Architecture - GitLab Integration for Both Modes

**Prerequisites**: Completed Stage 7. Your app should commit to Git on checkin, show history/diffs in modal, and rollback as admin. Test: Checkin file—git log shows commit; history modal lists with View Diff button (console for now).
**Time**: 7-8 hours
**What you'll build**: Hybrid mode (server/standalone exe), GitLab as source of truth (sync users/locks/messages.json), PAT auth (encrypted), messaging (user/broadcast). _Incremental_: One config field/service method/UI tab at a time, test with curl/exe. **Tailwind**: Yes—login tabs (`flex gap-2 border-b`), messages panel (`fixed right-0 h-full bg-card shadow-xl` slide-in), badges (`bg-danger px-2 py-1 rounded-full text-xs`).

---

### Deep Dive - Hybrid Architecture Patterns (CS: Distributed Systems, SE: Config as Code)

**CS Topic**: Distributed = eventual consistency (CS: CAP theorem—availability over consistency for PDM sync). Optimistic locking = pull/modify/push with merge on conflict (revisit Stage 3 races, but GitLab as coordinator). **App Topic**: PAT = API key (CS: OAuth2 bearer, scopes limit access). Encryption = Fernet (AES + HMAC, CS: symmetric with salt for key deriv). **SE Principle**: Config as code (YAML/env, 12-factor)—modes switch without recompile. **Python Specific**: yaml.safe_load = secure parse (no exec). **JS Specific**: sessionStorage = temp (clears tab close, vs localStorage persist). Gotcha: Sync conflicts = auto-merge locks (union, no overwrite).

Run your `learn_hybrid_architecture.py`—demo shows pull-before-modify (avoids lost updates).

---

### 8.1: Update Configuration for Hybrid Mode (Fields Incremental)

**Step 1: Add Mode Literal**
In `config.py` Settings, after DEBUG:

```python
from typing import Literal  # NEW: For enum
MODE: Literal["standalone", "server"] = "server"  # NEW: Switch
```

- **Explanation**: Literal = validated string (Pydantic, CS: type narrowing). Defaults server (multi-user).
- **Test**: Restart—no crash. Shell: `python -c "from app.config import settings; print(settings.MODE)"` → "server".
- **Gotcha**: Literal enforces at runtime (IDE hints).

**Step 2: Add GitLab Group**
Add:

```python
GITLAB_ENABLED: bool = True  # NEW
GITLAB_URL: str = "https://gitlab.com"  # NEW
GITLAB_REPO_URL: str = ""  # NEW: Your repo
GITLAB_BRANCH: str = "main"  # NEW
GITLAB_LFS_ENABLED: bool = True  # NEW: Large files
```

- **Explanation**: Enabled toggle = feature flag (SE: gradual rollout). LFS = pointers for big .mcam (revisit Stage 7 size).
- **Test**: .env GITLAB_REPO_URL=https://gitlab.com/test/pdm.git, restart—loads.
- **Gotcha**: Empty URL = disabled fallback.

**Step 3: Add Encryption Key**
Add:

```python
ENCRYPTION_KEY: str = "your-fernet-key-here"  # NEW: PAT encrypt
```

- **Explanation**: Fernet key = 32-byte base64 (CS: symmetric, generate once).
- **Test**: Shell print—string.
- **Gotcha**: Keep secret (env only).

**Step 4: Add Server Fields**
Add:

```python
HOST: str = "127.0.0.1"  # NEW: Standalone local
PORT: int = 8000  # NEW
GITLAB_SYNC_INTERVAL: int = 60  # NEW: Pull secs
```

- **Explanation**: Host local for exe (security, no expose). Interval = cron-like (CS: polling).
- **Test**: .env PORT=8080, restart—binds 8080.

**Step 5: Add Auto-Adjust Logic**
After settings = Settings():

```python
if settings.MODE == "standalone":  # NEW
    settings.HOST = "127.0.0.1"
elif settings.MODE == "server":
    settings.HOST = "0.0.0.0"
```

- **Explanation**: Dynamic override (Python: mutable attrs). Standalone = secure.
- **Test**: .env MODE=standalone—HOST="127.0.0.1".

**Full config.py** (End of Section—Verify):

```python
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Literal

class Settings(BaseSettings):
    APP_NAME: str = "PDM Backend API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    MODE: Literal["standalone", "server"] = "server"
    GITLAB_ENABLED: bool = True
    GITLAB_URL: str = "https://gitlab.com"
    GITLAB_REPO_URL: str = ""
    GITLAB_BRANCH: str = "main"
    GITLAB_LFS_ENABLED: bool = True
    ENCRYPTION_KEY: str = "your-fernet-key-here"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    GITLAB_SYNC_INTERVAL: int = 60
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

if settings.MODE == "standalone":
    settings.HOST = "127.0.0.1"
elif settings.MODE == "server":
    settings.HOST = "0.0.0.0"
```

**Verification**: .env MODE=standalone—HOST local. GitLab fields load.

### 8.2: GitLab API Service (Validate PAT Incremental)

**Step 1: Create gitlab_service.py**

```bash
touch backend/app/services/gitlab_service.py
```

Paste:

```python
import gitlab  # NEW: pip install python-gitlab
from typing import Optional, Dict  # NEW
import logging  # NEW

from app.config import settings  # NEW

logger = logging.getLogger(__name__)

class GitLabService:  # NEW
    def __init__(self):
        self.gitlab_url = settings.GITLAB_URL
```

- **Explanation**: gitlab = client lib (CS: HTTP wrapper, reduces boilerplate).
- **Test**: Import—OK.
- **Gotcha**: pip install python-gitlab.

**Step 2: Add validate_token (Core)**
Add:

```python
    def validate_token(self, token: str) -> Optional[Dict]:  # NEW
        try:
            gl = gitlab.Gitlab(self.gitlab_url, private_token=token)  # NEW: Connect
            gl.auth()  # NEW: Test
            current_user = gl.user  # NEW
            return {  # NEW
                'username': current_user.username,
                'name': current_user.name,
                'email': current_user.email,
                'id': current_user.id
            }
        except gitlab.exceptions.GitlabAuthenticationError:  # NEW
            logger.warning("Invalid GitLab token")
            return None
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return None
```

- **Explanation**: auth() = challenge (CS: token validation). Returns profile (app: auto-register).
- **Test**: Shell with real PAT—dict or None.
- **Gotcha**: exceptions.GitlabAuthenticationError = 401.

**Step 3: Add check_repository_access**
Add:

```python
    def check_repository_access(self, token: str, repo_url: str) -> bool:  # NEW
        try:
            gl = gitlab.Gitlab(self.gitlab_url, private_token=token)
            gl.auth()
            path = repo_url.replace('https://gitlab.com/', '').replace('.git', '')  # NEW: Extract
            gl.projects.get(path)  # NEW: Test access
            return True
        except gitlab.exceptions.GitlabGetError:  # NEW
            logger.warning(f"No access to {repo_url}")
            return False
        except Exception as e:
            logger.error(f"Access check failed: {e}")
            return False
```

- **Explanation**: projects.get = RBAC test (CS: permission query).
- **Test**: Valid/invalid repo—True/False.

**Step 4: Add get_project_info**
Add:

```python
    def get_project_info(self, token: str, repo_url: str) -> Optional[Dict]:  # NEW
        try:
            gl = gitlab.Gitlab(self.gitlab_url, private_token=token)
            gl.auth()
            path = repo_url.replace('https://gitlab.com/', '').replace('.git', '')
            project = gl.projects.get(path)
            return {  # NEW
                'id': project.id,
                'name': project.name,
                'path': project.path_with_namespace,
                'http_url': project.http_url_to_repo,
                'lfs_enabled': project.lfs_enabled,
            }
        except Exception as e:
            logger.error(f"Project info failed: {e}")
            return None
```

- **Explanation**: Metadata for UI (app: repo details).
- **Test**: Call—project dict.

**Full gitlab_service.py** (End of Section—Verify):

```python
import gitlab
from typing import Optional, Dict
import logging

from app.config import settings

logger = logging.getLogger(__name__)

class GitLabService:
    def __init__(self):
        self.gitlab_url = settings.GITLAB_URL
    def validate_token(self, token: str) -> Optional[Dict]:
        try:
            gl = gitlab.Gitlab(self.gitlab_url, private_token=token)
            gl.auth()
            current_user = gl.user
            return {
                'username': current_user.username,
                'name': current_user.name,
                'email': current_user.email,
                'id': current_user.id
            }
        except gitlab.exceptions.GitlabAuthenticationError:
            logger.warning("Invalid GitLab token")
            return None
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return None
    def check_repository_access(self, token: str, repo_url: str) -> bool:
        try:
            gl = gitlab.Gitlab(self.gitlab_url, private_token=token)
            gl.auth()
            path = repo_url.replace('https://gitlab.com/', '').replace('.git', '')
            gl.projects.get(path)
            return True
        except gitlab.exceptions.GitlabGetError:
            logger.warning(f"No access to {repo_url}")
            return False
        except Exception as e:
            logger.error(f"Access check failed: {e}")
            return False
    def get_project_info(self, token: str, repo_url: str) -> Optional[Dict]:
        try:
            gl = gitlab.Gitlab(self.gitlab_url, private_token=token)
            gl.auth()
            path = repo_url.replace('https://gitlab.com/', '').replace('.git', '')
            project = gl.projects.get(path)
            return {
                'id': project.id,
                'name': project.name,
                'path': project.path_with_namespace,
                'http_url': project.http_url_to_repo,
                'lfs_enabled': project.lfs_enabled,
            }
        except Exception as e:
            logger.error(f"Project info failed: {e}")
            return None
```

**Verification**: validate_token(real PAT) → User dict.

### 8.3: GitLab Repository Sync Service (Sync Incremental)

**Step 1: Create gitlab_sync_service.py**

```bash
touch backend/app/services/gitlab_sync_service.py
```

Paste:

```python
from pathlib import Path  # NEW
from typing import Optional  # NEW
import logging  # NEW

from git import Repo, GitCommandError  # NEW
from git.exc import InvalidGitRepositoryError  # NEW

from app.config import settings  # NEW
from app.utils.file_locking import LockedFile  # NEW

logger = logging.getLogger(__name__)

class GitLabSyncService:  # NEW
    def __init__(self, clone_path: Path, repo_url: str, token: str):
        self.clone_path = clone_path
        self.repo_url = self._inject_token_to_url(repo_url, token)  # Stub
        self.token = token
        self.repo = None
        self._ensure_repository()  # Stub
```

- **Explanation**: Sync = bridge local/GitLab (CS: replication).
- **Test**: Import OK.

**Step 2: Add \_inject_token_to_url**
Add:

```python
    def _inject_token_to_url(self, url: str, token: str) -> str:  # NEW
        if '@' in url:
            return url
        if url.startswith('https://'):
            return url.replace('https://', f'https://oauth2:{token}@')
        return url
```

- **Explanation**: oauth2: = Git scheme (app: auth in URL for clone).
- **Test**: Call—embeds token.

**Step 3: Add \_ensure_repository (Clone)**
Add:

```python
    def _ensure_repository(self):  # NEW
        try:
            self.repo = Repo(self.clone_path)
            logger.info(f"Opened clone at {self.clone_path}")
            if self.repo.active_branch.name != settings.GITLAB_BRANCH:
                self.repo.git.checkout(settings.GITLAB_BRANCH)
        except (InvalidGitRepositoryError, Exception):
            logger.info(f"Cloning to {self.clone_path}")
            self.clone_path.parent.mkdir(parents=True, exist_ok=True)
            self.repo = Repo.clone_from(self.repo_url, self.clone_path, branch=settings.GITLAB_BRANCH)
            if settings.GITLAB_LFS_ENABLED:
                try:
                    self.repo.git.execute(['git', 'lfs', 'install'])
                except Exception as e:
                    logger.warning(f"LFS failed: {e}")
```

- **Explanation**: clone_from = full repo (CS: shallow for perf, but full for history).
- **Test**: Init with path—clones (check clone_path/.git).
- **Gotcha**: LFS install = global (run once).

**Step 4: Add pull**
Add:

```python
    def pull(self) -> bool:  # NEW
        try:
            origin = self.repo.remote('origin')
            origin.pull(settings.GITLAB_BRANCH)
            logger.info("Pulled from GitLab")
            return True
        except GitCommandError as e:
            logger.error(f"Pull failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Pull error: {e}")
            return False
```

- **Explanation**: pull = fetch + merge (CS: three-way merge).
- **Test**: Manual push to GitLab, pull—updates.

**Step 5: Add commit_and_push**
Add:

```python
    def commit_and_push(self, files: list[str], message: str, author_name: str, author_email: str) -> bool:  # NEW
        try:
            if not self.pull():  # Optimistic
                logger.warning("Pull failed before commit")
            self.repo.index.add(files)
            if not self.repo.index.diff("HEAD"):
                return True
            commit = self.repo.index.commit(message, author=f"{author_name} <{author_email}>")
            origin = self.repo.remote('origin')
            origin.push(settings.GITLAB_BRANCH)
            logger.info(f"Pushed {commit.hexsha[:8]}")
            return True
        except GitCommandError as e:
            logger.error(f"Commit/push failed: {e}")
            if 'rejected' in str(e).lower():
                if self.pull():
                    origin = self.repo.remote('origin')
                    origin.push(settings.GITLAB_BRANCH)
                    return True
            return False
        except Exception as e:
            logger.error(f"Commit error: {e}")
            return False
```

- **Explanation**: Retry on reject = optimistic concurrency (CS: version check).
- **Test**: Add file, commit/push—GitLab updates.

**Step 6: Add JSON Helpers**
Add:

```python
    def load_json_file(self, filename: str) -> dict:  # NEW
        file_path = self.clone_path / filename
        if not file_path.exists():
            return {}
        with LockedFile(file_path, 'r') as f:
            content = f.read()
            if not content.strip():
                return {}
            return json.loads(content)
    def save_json_file(self, filename: str, data: dict):  # NEW
        file_path = self.clone_path / filename
        with LockedFile(file_path, 'w') as f:
            json.dump(data, f, indent=2)
```

- **Explanation**: Locked JSON = concurrent (revisit Stage 3).
- **Test**: Load/save 'test.json'—persists.

**Full gitlab_sync_service.py** (End of Section—Verify):
[Full with all]

**Verification**: Clone, pull, commit/push—GitLab syncs.

### Stage 8 Complete (Part 1)

**Test**: Config MODE=server, login—/api/files from GitLab clone (if setup).

Continue Part 2 (Auth/Messaging)? Or full test?
