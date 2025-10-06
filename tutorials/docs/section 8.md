# PDM Tutorial - Stage 8: Hybrid Architecture - GitLab Integration for Both Modes

**Prerequisites**: Completed Stage 7. Your app should commit to Git on checkin, show history/diffs, and rollback. Test: Checkout/checkin a file, view history—see commits.
**Time**: 7-8 hours
**What you'll build**: A hybrid app that runs as a central server _or_ standalone executable (PyInstaller). GitLab becomes the "single source of truth" for users.json, locks.json, and messages.json. Users auth with GitLab PATs (encrypted). Add messaging (user-to-user, broadcasts). Revisit topics: optimistic locking (Stage 3), hashing (Stage 5), config (Stage 0), deployment (SE best practices).

---

### Tutorial Approach: Incremental Revisit

Stage 8 revisits prior concepts deeply while building new ones:

- **Small steps**: 5-10 lines per change, test immediately.
- **Explanations**: CS (e.g., key derivation), app (e.g., sync conflicts), Python/JS (e.g., Fernet), SE (e.g., config management).
- **Ingrain**: Each section ties back (e.g., encryption builds on bcrypt from Stage 5).
- **Engagement**: Run/tests after each step—feel progress.

By end, run as server (`uvicorn`) or exe (double-click)—both sync to GitLab.

---

### 8.1: Deep Dive - Hybrid Architecture Patterns (Incremental Read)

**Step 1: Create the Learn File**

```bash
touch backend/app/learn_hybrid_architecture.py
```

Paste your full code (from message)—it's spot-on for depth.

**Step 2: Run & Engage (Revisit CS: Distributed Systems)**

```bash
cd backend
python -m app.learn_hybrid_architecture
```

- **Output**: Prints concepts (hybrid modes, conflicts).
- **CS Revisit**: Optimistic locking (Stage 3's race conditions)—pull before modify, merge locks (union, no overwrite). SE: GitLab as "source of truth" (single DB pattern, avoids eventual consistency bugs).
- **Gotcha**: PAT scopes (api/write_repo)—missing = push fails.
- **Test**: If runs without errors, good. Reflect: How does this solve Stage 6's local-only audits?

**Why incremental?**: Read/run now—primes for sync conflicts later.

---

### 8.2: Update Configuration for Hybrid Mode (One Field at a Time)

**Step 1: Add Mode Enum (Revisit Pydantic from Stage 5)**
Open `backend/app/config.py`, add _one import/line_ after existing:

```python
from typing import Literal  # NEW: For mode enum
```

Then in Settings class:

```python
MODE: Literal["standalone", "server"] = "server"  # NEW: Deployment mode
```

- **Explanation**: Literal enforces valid strings (Pydantic validation, revisit Stage 5 schemas). Defaults "server"—standalone for exes.
- **CS Revisit**: Enum-like (type safety, prevents typos like "standlaone").
- **Test**: Restart server—no crash? Shell: `python -c "from app.config import settings; print(settings.MODE)"` → "server".

**Step 2: Add GitLab Fields (One Group)**
Add section after MODE:

```python
## GitLab Configuration (NEW)
GITLAB_ENABLED: bool = True
GITLAB_URL: str = "https://gitlab.com"
GITLAB_REPO_URL: str = ""  # e.g., "https://gitlab.com/user/pdm.git"
GITLAB_BRANCH: str = "main"
GITLAB_LFS_ENABLED: bool = True
```

- **Explanation**: Toggles GitLab (fallback local if False). URL for API, repo for clone. LFS (Large File Storage)—stores big .mcam as pointers (revisit Stage 7 Git size issues).
- **SE Revisit**: Config as code—override in .env (env vars > YAML).
- **Test**: Add to .env: `GITLAB_REPO_URL=https://gitlab.com/test/pdm.git` (dummy). Restart—loads without error.

**Step 3: Add Encryption Key (Security Revisit)**
Add after GitLab:

```python
ENCRYPTION_KEY: str = "your-fernet-encryption-key-here"  # NEW: For PATs
```

- **Explanation**: Fernet key (symmetric AES)—encrypts PATs (revisit Stage 5 hashing, but reversible for Git ops).
- **CS Revisit**: Key derivation later (PBKDF2 from passwords).
- **Test**: Generate: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` → Copy to .env.

**Step 4: Add Server Fields (One Each)**
Add:

```python
HOST: str = "127.0.0.1"  # NEW: For standalone
PORT: int = 8000  # NEW
GITLAB_SYNC_INTERVAL: int = 60  # NEW: Pull seconds
```

- **Explanation**: Standalone: localhost (secure). Server: 0.0.0.0 (network). Interval: Background pulls (revisit Stage 3 atomicity).
- **Test**: Restart—`python -c "from app.config import settings; print(settings.HOST)"` → "127.0.0.1".

**Step 5: Auto-Adjust Host (Logic Snippet)**
After `settings = Settings()`:

```python
if settings.MODE == "standalone":
    settings.HOST = "127.0.0.1"  # NEW: Override for security
elif settings.MODE == "server":
    settings.HOST = "0.0.0.0"
```

- **Explanation**: Dynamic—standalone can't expose ports (SE: least privilege).
- **Test**: Set .env `MODE=standalone`, restart—HOST="127.0.0.1".

**Full config.py**: Now hybrid-ready. Test: No crashes, values load.

---

### 8.3: GitLab API Service (Build Class Step-by-Step)

**Step 1: Create File & Skeleton**

```bash
touch backend/app/services/gitlab_service.py
```

Paste:

```python
import gitlab  # NEW: pip install python-gitlab
from pathlib import Path
from typing import Optional, Dict
import logging

from app.config import settings

logger = logging.getLogger(__name__)

class GitLabService:
    def __init__(self):
        self.gitlab_url = settings.GITLAB_URL
        self.gl = None  # Connection
```

- **Explanation**: `python-gitlab` wraps GitLab REST API (CS: client lib for HTTP). `gl` for lazy connect.
- **Test**: `python -c "from app.services.gitlab_service import GitLabService; print('OK')"`—no import errors.

**Step 2: Add validate_token (Core Method)**
Add:

```python
    def validate_token(self, token: str) -> Optional[Dict]:
        try:
            gl = gitlab.Gitlab(self.gitlab_url, private_token=token)
            gl.auth()  # Validates token
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
            logger.error(f"GitLab validation failed: {e}")
            return None
```

- **Explanation**: Connects, `gl.auth()` tests token (CS: API auth, OAuth2-like). Returns user info or None.
- **SE Revisit**: Try/except for resilience (Stage 6 error handling).
- **Test**: Shell: `python -c "from app.services.gitlab_service import GitLabService; s = GitLabService(); print(s.validate_token('invalid'))"` → None.

**Step 3: Add check_repository_access**
Add:

```python
    def check_repository_access(self, token: str, repo_url: str) -> bool:
        try:
            gl = gitlab.Gitlab(self.gitlab_url, private_token=token)
            gl.auth()
            # Extract path: https://gitlab.com/user/repo.git → user/repo
            path = repo_url.replace('https://gitlab.com/', '').replace('.git', '')
            gl.projects.get(path)  # Tests access
            return True
        except gitlab.exceptions.GitlabGetError:
            logger.warning(f"No access to {repo_url}")
            return False
        except Exception as e:
            logger.error(f"Repo access check failed: {e}")
            return False
```

- **Explanation**: `projects.get()` throws if no access (CS: RBAC, Stage 6 roles).
- **Test**: Use real PAT/repo—returns True/False.

**Step 4: Add get_project_info**
Add:

```python
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

- **Explanation**: Fetches project metadata (SE: API caching—call once on setup).
- **Test**: Full flow: `python -c "s = GitLabService(); info = s.get_project_info('token', 'url'); print(info)"`.

**Full gitlab_service.py**: Now validates PATs/repos. Test: Invalid token → None.

---

### 8.4: GitLab Repository Sync Service (Incremental Sync)

**Step 1: Create File & Init**

```bash
touch backend/app/services/gitlab_sync_service.py
```

Paste:

```python
from pathlib import Path
from typing import Optional
import logging

from git import Repo, GitCommandError
from git.exc import InvalidGitRepositoryError

from app.config import settings
from app.utils.file_locking import LockedFile  # Revisit Stage 3

logger = logging.getLogger(__name__)

class GitLabSyncService:
    def __init__(self, clone_path: Path, repo_url: str, token: str):
        self.clone_path = clone_path
        self.repo_url = self._inject_token_to_url(repo_url, token)  # Token in URL
        self.token = token
        self.repo = None
        self._ensure_repository()
```

- **Explanation**: Clones/pulls to local (CS: eventual consistency—sync before/after ops).
- **Test**: Import—no errors.

**Step 2: Add \_inject_token_to_url**
Add:

```python
    def _inject_token_to_url(self, url: str, token: str) -> str:
        if '@' in url:
            return url
        if url.startswith('https://'):
            return url.replace('https://', f'https://oauth2:{token}@')
        return url
```

- **Explanation**: Embeds token in URL for `git clone` (SE: no separate auth).
- **Test**: `python -c "from app.services.gitlab_sync_service import GitLabSyncService; print(GitLabSyncService._inject_token_to_url('https://gitlab.com/user/repo.git', 'token'))"` → "https://oauth2:token@gitlab.com/user/repo.git".

**Step 3: Add \_ensure_repository (Clone/Init)**
Add:

```python
    def _ensure_repository(self):
        try:
            self.repo = Repo(self.clone_path)
            logger.info(f"Opened GitLab clone at {self.clone_path}")
            if self.repo.active_branch.name != settings.GITLAB_BRANCH:
                self.repo.git.checkout(settings.GITLAB_BRANCH)
        except (InvalidGitRepositoryError, Exception):
            logger.info(f"Cloning GitLab to {self.clone_path}")
            self.clone_path.parent.mkdir(parents=True, exist_ok=True)
            self.repo = Repo.clone_from(self.repo_url, self.clone_path, branch=settings.GITLAB_BRANCH)
            if settings.GITLAB_LFS_ENABLED:
                try:
                    self.repo.git.execute(['git', 'lfs', 'install'])
                except Exception as e:
                    logger.warning(f"LFS setup failed: {e}")
```

- **Explanation**: Clones if missing (CS: idempotent—safe re-run). LFS for big files (revisit Stage 7 size).
- **Test**: Run service init in shell—clones (check `backend/gitlab_repo_clone/.git/`).

**Step 4: Add pull()**
Add:

```python
    def pull(self) -> bool:
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

- **Explanation**: `origin.pull()` fetches/merges (revisit Stage 3 atomicity—pull before modify).
- **Test**: Manually push to GitLab, call pull—files update.

**Step 5: Add commit_and_push (Full Flow)**
Add:

```python
    def commit_and_push(self, files: list[str], message: str, author_name: str, author_email: str) -> bool:
        try:
            if not self.pull():  # Optimistic lock
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
                    origin.push(settings.GITLAB_BRANCH)  # Retry
                    return True
            return False
        except Exception as e:
            logger.error(f"Commit error: {e}")
            return False
```

- **Explanation**: Pull first (optimistic locking, revisit Stage 3 races), stage/commit/push. Retry on reject.
- **SE Revisit**: Idempotent (no changes? Skip).
- **Test**: Add file, call—pushes to GitLab.

**Step 6: Add JSON Helpers (Revisit Stage 3 JSON)**
Add:

```python
    def load_json_file(self, filename: str) -> dict:
        file_path = self.clone_path / filename
        if not file_path.exists():
            return {}
        with LockedFile(file_path, 'r') as f:  # Atomic (Stage 3)
            content = f.read()
            if not content.strip():
                return {}
            return json.loads(content)

    def save_json_file(self, filename: str, data: dict):
        file_path = self.clone_path / filename
        with LockedFile(file_path, 'w') as f:
            json.dump(data, f, indent=2)
```

- **Explanation**: Locked JSON (revisit Stage 3)—safe for users.json/locks.
- **Test**: Load/save 'test.json'—persists.

**Full gitlab_sync_service.py**: Now syncs JSON/files to GitLab.

---

### 8.5: Encrypted Token Storage (Incremental Crypto)

**Step 1: Create File & Imports**

```bash
touch backend/app/utils/encryption.py
```

Paste:

```python
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
import os
from typing import Optional

def derive_key_from_password(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100_000)
    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key)
```

- **Explanation**: PBKDF2 derives key from password+salt (CS: slow hash, anti-brute-force, revisit Stage 5 bcrypt).
- **Test**: `python -c "from app.utils.encryption import derive_key_from_password; print(len(derive_key_from_password('pass', b'salt'*8)))"` → 44 (base64).

**Step 2: Add encrypt_token**
Add:

```python
def encrypt_token(token: str, password: str) -> dict:
    salt = os.urandom(16)  # Random salt
    key = derive_key_from_password(password, salt)
    cipher = Fernet(key)
    encrypted = cipher.encrypt(token.encode())
    return {
        'encrypted_token': base64.urlsafe_b64encode(encrypted).decode('utf-8'),
        'salt': base64.urlsafe_b64encode(salt).decode('utf-8')
    }
```

- **Explanation**: Salt per token (CS: unique keys), Fernet = AES+HMAC (authenticated encryption).
- **Test**: `python -c "from app.utils.encryption import encrypt_token; print(encrypt_token('token', 'pass'))"` → Dict with strings.

**Step 3: Add decrypt_token**
Add:

```python
def decrypt_token(encrypted_token: str, salt: str, password: str) -> Optional[str]:
    try:
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_token)
        salt_bytes = base64.urlsafe_b64decode(salt)
        key = derive_key_from_password(password, salt_bytes)
        cipher = Fernet(key)
        decrypted = cipher.decrypt(encrypted_bytes)
        return decrypted.decode('utf-8')
    except (InvalidToken, Exception):
        return None
```

- **Explanation**: Wrong password = None (CS: forward secrecy—can't decrypt old tokens).
- **Test**: Encrypt, decrypt with right/wrong pass—match/None.

**Step 4: Add Test Block**
Add at end:

```python
if __name__ == "__main__":
    original_token = "glpat-test"
    user_password = "MySecurePassword123!"
    encrypted_data = encrypt_token(original_token, user_password)
    decrypted = decrypt_token(encrypted_data['encrypted_token'], encrypted_data['salt'], user_password)
    print(f"Match: {decrypted == original_token}")
    wrong_decrypted = decrypt_token(encrypted_data['encrypted_token'], encrypted_data['salt'], "Wrong")
    print(f"Wrong: {wrong_decrypted}")
```

- **Explanation**: Self-test—verifies round-trip.
- **Test**: `python backend/app/utils/encryption.py` → "Match: True", "Wrong: None".

**Full encryption.py**: Secure PAT storage ready.

---

### 8.6: GitLab-Aware User Service (Refactor auth_service Incrementally)

**Step 1: Add GitLab Imports**
Open `backend/app/services/auth_service.py`, add:

```python
from app.services.gitlab_service import GitLabService  # NEW
from app.services.gitlab_sync_service import GitLabSyncService  # NEW
from app.utils.encryption import encrypt_token, decrypt_token  # NEW
```

- **Explanation**: Ties services—sync for storage, GitLab for validation.
- **Test**: Import—no errors.

**Step 2: Update **init** (Optional Param)**
Change:

```python
def __init__(self, users_file: Optional[Path] = None, gitlab_sync: Optional[GitLabSyncService] = None):
    self.users_file = users_file
    self.gitlab_sync = gitlab_sync
    self.gitlab_service = GitLabService()  # NEW: Always have GitLab client
    self.use_gitlab = gitlab_sync is not None and settings.GITLAB_ENABLED
    if not self.use_gitlab and users_file:
        if not self.users_file.exists():
            self.users_file.write_text('{}')
```

- **Explanation**: Hybrid: GitLab if enabled, fallback local (SE: backward compat).
- **Test**: Restart—no crash.

**Step 3: Update load_users (Pull First)**
Replace:

```python
def load_users(self) -> dict:
    if self.use_gitlab:
        self.gitlab_sync.pull()  # NEW: Sync before load
        return self.gitlab_sync.load_json_file('users.json')
    else:
        try:
            with LockedFile(self.users_file, 'r') as f:
                content = f.read()
                if not content.strip():
                    return {}
                return json.loads(content)
        except Exception:
            return {}
```

- **Explanation**: Pull ensures fresh data (revisit Stage 3 atomicity—optimistic lock).
- **Test**: Manually edit GitLab users.json, call load—updated.

**Step 4: Update save_users (Push After)**
Replace:

```python
def save_users(self, users: dict):
    if self.use_gitlab:
        self.gitlab_sync.save_json_file('users.json', users)
        self.gitlab_sync.commit_and_push(  # NEW: Commit/push
            files=['users.json'],
            message="Update user database",
            author_name=settings.GIT_USER_NAME,
            author_email=settings.GIT_USER_EMAIL
        )
    else:
        with LockedFile(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
```

- **Explanation**: Save local, then push (CS: transaction—commit or abort).
- **Test**: Add user, call save—pushes to GitLab.

**Step 5: Add authenticate_with_gitlab_token (New Method)**
Add:

```python
def authenticate_with_gitlab_token(self, username: str, gitlab_token: str) -> Optional[UserInDB]:
    user_info = self.gitlab_service.validate_token(gitlab_token)  # NEW
    if not user_info or user_info['username'] != username:
        return None
    user = self.get_user(username)
    if not user:
        import secrets
        temp_password = secrets.token_urlsafe(32)  # NEW: Random temp
        self.create_user(username, temp_password, user_info['name'], 'user', gitlab_token)
        user = self.get_user(username)
    return user
```

- **Explanation**: Validates PAT, auto-registers (SE: zero-config onboarding).
- **Test**: Call with valid PAT—returns user or creates.

**Step 6: Add get_gitlab_token (Decrypt)**
Add:

```python
def get_gitlab_token(self, username: str, password: str) -> Optional[str]:
    user = self.get_user(username)
    if not user:
        return None
    users = self.load_users()
    user_data = users.get(username, {})
    encrypted_token = user_data.get('encrypted_gitlab_token')
    salt = user_data.get('token_salt')
    if not encrypted_token or not salt:
        return None
    return decrypt_token(encrypted_token, salt, password)  # NEW
```

- **Explanation**: Decrypts for session (CS: ephemeral—clears on logout).
- **Test**: Encrypt, decrypt—matches.

**Step 7: Update create_user (Encrypt Token)**
In `create_user`, after hash:

```python
if gitlab_token:  # NEW
    encrypted_data = encrypt_token(gitlab_token, password)
    user_data['encrypted_gitlab_token'] = encrypted_data['encrypted_token']
    user_data['token_salt'] = encrypted_data['salt']
```

- **Explanation**: Encrypts before store (revisit Step 5).
- **Test**: Create with token—users.json has encrypted fields.

**Full auth_service.py**: Now GitLab-aware.

---

### 8.7: Messaging System (Build from Scratch Incrementally)

**Step 1: Create File & Skeleton**

```bash
touch backend/app/services/message_service.py
```

Paste:

```python
from pathlib import Path
from typing import List, Dict, Optional
import json
from datetime import datetime, timezone
import logging

from app.services.gitlab_sync_service import GitLabSyncService
from app.utils.file_locking import LockedFile

logger = logging.getLogger(__name__)

class MessageService:
    def __init__(self, messages_file: Optional[Path] = None, gitlab_sync: Optional[GitLabSyncService] = None):
        self.messages_file = messages_file
        self.gitlab_sync = gitlab_sync
        self.use_gitlab = gitlab_sync is not None
        if not self.use_gitlab and messages_file:
            if not messages_file.exists():
                messages_file.write_text('[]')
```

- **Explanation**: Hybrid storage (revisit config hybrid). messages.json = array of dicts (id, from, to, etc.).
- **Test**: Import—no errors.

**Step 2: Add load_messages (Pull/Load)**
Add:

```python
def load_messages(self) -> List[Dict]:
    if self.use_gitlab:
        self.gitlab_sync.pull()
        messages = self.gitlab_sync.load_json_file('messages.json')
        if isinstance(messages, dict):
            return messages.get('messages', [])
        return messages if isinstance(messages, list) else []
    else:
        try:
            with LockedFile(self.messages_file, 'r') as f:
                content = f.read()
                if not content.strip():
                    return []
                return json.loads(content)
        except Exception:
            return []
```

- **Explanation**: Pulls for fresh (CS: eventual consistency). Handles dict/list formats.
- **Test**: Load—empty list.

**Step 3: Add save_messages (Push)**
Add:

```python
def save_messages(self, messages: List[Dict]):
    if self.use_gitlab:
        self.gitlab_sync.save_json_file('messages.json', messages)
        self.gitlab_sync.commit_and_push(
            files=['messages.json'],
            message="Update messages",
            author_name="PDM System",
            author_email="pdm@system.local"
        )
    else:
        with LockedFile(self.messages_file, 'w') as f:
            json.dump(messages, f, indent=2)
```

- **Explanation**: Saves + pushes (revisit sync commit).
- **Test**: Save list—commits to GitLab.

**Step 4: Add send_message (Core)**
Add:

```python
def send_message(self, from_user: str, to_user: str, subject: str, body: str, related_file: Optional[str] = None) -> str:
    import uuid  # NEW
    messages = self.load_messages()
    message = {
        'id': str(uuid.uuid4()),
        'from_user': from_user,
        'to_user': to_user,
        'subject': subject,
        'body': body,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'read': False,
        'related_file': related_file
    }
    messages.append(message)
    self.save_messages(messages)
    logger.info(f"Message sent from {from_user} to {to_user}: {subject}")
    return message['id']
```

- **Explanation**: UUID for ID (CS: uniqueness). Timestamp UTC (Stage 5).
- **Test**: Send—saves, returns ID.

**Step 5: Add get_messages_for_user (Filter)**
Add:

```python
def get_messages_for_user(self, username: str) -> List[Dict]:
    messages = self.load_messages()
    user_messages = [msg for msg in messages if msg['to_user'] == username or msg['to_user'] == 'all']
    user_messages.sort(key=lambda m: m['timestamp'], reverse=True)  # Newest first
    return user_messages
```

- **Explanation**: Filter + sort (CS: query optimization—load all, filter in mem for small data).
- **Test**: Send to "john", get for "john"—returns list.

**Step 6: Add get_unread_count**
Add:

```python
def get_unread_count(self, username: str) -> int:
    messages = self.get_messages_for_user(username)
    return sum(1 for msg in messages if not msg.get('read', False))
```

- **Explanation**: Count unread (revisit Stage 6 audit counts).
- **Test**: Send unread—count 1.

**Step 7: Add mark_as_read & delete_message**
Add:

```python
def mark_as_read(self, message_id: str, username: str):
    messages = self.load_messages()
    for msg in messages:
        if msg['id'] == message_id and (msg['to_user'] == username or msg['to_user'] == 'all'):
            msg['read'] = True
            self.save_messages(messages)
            break

def delete_message(self, message_id: str, username: str):
    messages = self.load_messages()
    messages = [msg for msg in messages if not (msg['id'] == message_id and (msg['from_user'] == username or msg['to_user'] == username))]
    self.save_messages(messages)
```

- **Explanation**: Owner-only delete (SE: ACL, Stage 6 roles).
- **Test**: Mark/read, delete—updates.

**Step 8: Add get_messages_for_file**
Add:

```python
def get_messages_for_file(self, filename: str) -> List[Dict]:
    messages = self.load_messages()
    return [msg for msg in messages if msg.get('related_file') == filename]
```

- **Explanation**: File-specific (app: tie to files, revisit Stage 3 repo).
- **Test**: Send with file—filters correctly.

**Full message_service.py**: Messaging ready.

---

### 8.8: Update API Authentication (Endpoints Incrementally)

**Step 1: Add GitLab Login Endpoint**
Open `backend/app/api/auth.py`, add _one endpoint_ after login:

```python
@router.post("/login-gitlab", response_model=Token)
def login_with_gitlab(
    username: str = Form(...),  # NEW: Form for token
    gitlab_token: str = Form(...),
    user_service: UserService = Depends(get_user_service)
):
    if not settings.GITLAB_ENABLED:
        raise HTTPException(400, "GitLab disabled")
    user = user_service.authenticate_with_gitlab_token(username, gitlab_token)
    if not user:
        raise HTTPException(401, "Invalid GitLab token")
    # ... create token (copy from login)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username, "role": user.role}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
```

- **Import**: Add `from fastapi import Form` at top.
- **Explanation**: Form for PAT (sensitive, no JSON). Calls new auth (revisit Stage 5 JWT).
- **Test**: `/docs`—call with username/token, returns token.

**Step 2: Update login (Fallback)**
In existing login, after local auth fails—add GitLab fallback (if enabled):

```python
user = user_service.authenticate_user(form_data.username, form_data.password)
if not user and settings.GITLAB_ENABLED:
    # Try GitLab (assume token in password field or separate)
    user = user_service.authenticate_with_gitlab_token(form_data.username, form_data.password)  # Treat password as token
```

- **Explanation**: Unified login—tries local, fallback GitLab (SE: UX—single form).
- **Test**: Login with PAT as password—works.

**Step 3: Add /validate-gitlab-token**
Add:

```python
@router.get("/validate-gitlab-token")
def validate_gitlab_token(token: str, gitlab_service: GitLabService = Depends()):
    user_info = gitlab_service.validate_token(token)
    if not user_info:
        raise HTTPException(401, "Invalid GitLab token")
    return user_info
```

- **Explanation**: Standalone: Validates before register (CS: pre-flight check).
- **Test**: Call with token—returns user info.

**Full auth.py**: Dual auth ready.

---

### 8.9: Messaging API (Endpoints Incrementally)

**Step 1: Create File & Schemas**

```bash
touch backend/app/api/messages.py
```

Paste:

```python
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from pydantic import BaseModel, Field

from app.schemas.auth import User
from app.services.message_service import MessageService  # NEW import
from app.api.deps import get_current_user

class MessageCreate(BaseModel):
    to_user: str = Field(..., description="Recipient or 'all'")
    subject: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1, max_length=5000)
    related_file: str | None = Field(None)

class Message(BaseModel):
    id: str
    from_user: str
    to_user: str
    subject: str
    body: str
    timestamp: str
    read: bool
    related_file: str | None = None

router = APIRouter(prefix="/api/messages", tags=["messages"])
```

- **Explanation**: Pydantic schemas (revisit Stage 5)—validates input.
- **Test**: Import—no errors.

**Step 2: Add get_my_messages**
Add:

```python
def get_message_service() -> MessageService:  # NEW dep
    # ... from earlier (GitLab or local)

@router.get("/", response_model=List[Message])
def get_my_messages(
    current_user: User = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
):
    try:
        messages = message_service.get_messages_for_user(current_user.username)
        return messages
    except Exception as e:
        raise HTTPException(500, f"Failed to load messages: {str(e)}")
```

- **Explanation**: Auth required, filters for user (CS: query filter).
- **Test**: `/docs`—call, expect [].

**Step 3: Add send_message**
Add:

```python
@router.post("/send")
def send_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
):
    try:
        message_id = message_service.send_message(
            from_user=current_user.username,
            to_user=message.to_user,
            subject=message.subject,
            body=message.body,
            related_file=message.related_file
        )
        return {"success": True, "message_id": message_id}
    except Exception as e:
        raise HTTPException(500, f"Failed to send: {str(e)}")
```

- **Explanation**: Uses current_user (revisit Stage 6 auth).
- **Test**: POST JSON—creates message.

**Step 4: Add get_unread_count**
Add:

```python
@router.get("/unread-count")
def get_unread_count(
    current_user: User = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
):
    count = message_service.get_unread_count(current_user.username)
    return {"unread_count": count}
```

- **Explanation**: Quick count (SE: efficient—no full list).
- **Test**: Call—returns 0 (or count).

**Step 5: Include in main.py**
In `backend/app/main.py`:

```python
from app.api import files, auth, version_control, messages  # NEW
app.include_router(messages.router)
```

- **Test**: Restart—`/docs` shows messages tag.

**Full messages.py**: API ready.

---

### 8.10: Update Dependencies for GitLab Mode (One Dep at a Time)

**Step 1: Add get_gitlab_sync**
In `backend/app/api/deps.py`, add:

```python
def get_gitlab_sync(token: str = Depends(oauth2_scheme)) -> GitLabSyncService:
    if not settings.GITLAB_ENABLED:
        raise HTTPException(503, "GitLab disabled")
    # TODO: Use token for user-specific clone
    gitlab_sync = GitLabSyncService(settings.GITLAB_CLONE_PATH, settings.GITLAB_REPO_URL, "placeholder-token")
    return gitlab_sync
```

- **Explanation**: Token for per-user (future), placeholder now (SE: stub for testing).
- **Test**: Import—works.

**Step 2: Update get_user_service (Hybrid)**
Replace:

```python
def get_user_service() -> UserService:
    if settings.GITLAB_ENABLED:
        try:
            gitlab_sync = get_gitlab_sync()
            return UserService(gitlab_sync=gitlab_sync)
        except:
            pass
    users_file = settings.BASE_DIR / 'users.json'
    return UserService(users_file=users_file)
```

- **Explanation**: Fallback local if GitLab fails (SE: resilience).
- **Test**: Restart—loads GitLab mode.

**Full deps.py**: Services now hybrid.

---

### 8.11: Frontend - GitLab Login UI (Incremental Tabs)

**Step 1: Add Tabs to login.html**
In `<body>`, after header:

```html
<div class="login-tabs">
  # NEW
  <button class="tab-button active" data-tab="password">Password</button>
  <button class="tab-button" data-tab="gitlab">GitLab Token</button>
</div>
<div id="error-message" class="error-message"></div>
<!-- Password Tab (existing form) -->
<div id="password-tab" class="tab-content active">
  <!-- Existing form -->
</div>
<!-- GitLab Tab (NEW) -->
<div id="gitlab-tab" class="tab-content">
  <div class="info-box">
    Login with GitLab PAT.
    <a
      href="https://gitlab.com/-/profile/personal_access_tokens"
      target="_blank"
      >Generate →</a
    >
  </div>
  <form id="gitlab-login-form">
    <div class="form-group">
      <label for="gitlab-username">GitLab Username</label>
      <input
        type="text"
        id="gitlab-username"
        name="username"
        required
        placeholder="your-gitlab-username"
      />
    </div>
    <div class="form-group">
      <label for="gitlab-token">Personal Access Token</label>
      <input
        type="password"
        id="gitlab-token"
        name="token"
        required
        placeholder="glpat-xxxx..."
      />
      <small>Required scopes: api, read_repository, write_repository</small>
    </div>
    <button type="submit" class="btn btn-primary" style="width: 100%;">
      Login with GitLab
    </button>
  </form>
</div>
```

- **Explanation**: Tabs for UX (JS: data-tab). Info box educates (SE: self-service).
- **Test**: Refresh login—tabs switch (no JS yet).

**Step 2: Add Tab CSS**
In `<style>`:

```css
.login-tabs {
  display: flex;
  gap: var(--spacing-2);
  margin-bottom: var(--spacing-6);
  border-bottom: 2px solid var(--border-default);
}
.tab-button {
  flex: 1;
  padding: var(--spacing-3);
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  color: var(--text-secondary);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-bottom: -2px;
}
.tab-button.active {
  color: var(--interactive-primary);
  border-bottom-color: var(--interactive-primary);
}
.tab-button:hover {
  color: var(--interactive-primary-hover);
}
.tab-content {
  display: none;
}
.tab-content.active {
  display: block;
}
.info-box {
  background: var(--status-info-bg);
  color: var(--status-info-text);
  padding: var(--spacing-3);
  border-radius: var(--radius-base);
  margin-bottom: var(--spacing-4);
  font-size: var(--font-size-sm);
}
.info-box a {
  color: var(--status-info-text);
  text-decoration: underline;
  font-weight: var(--font-weight-semibold);
}
```

- **Explanation**: Active tab underlined (CSS: stateful UI, revisit Stage 2 tokens).
- **Test**: Tabs style correctly.

**Step 3: Add Tab JS**
In `login.js`:

```javascript
document.querySelectorAll(".tab-button").forEach((button) => {
  button.addEventListener("click", () => {
    const tabName = button.dataset.tab;
    document
      .querySelectorAll(".tab-button")
      .forEach((b) => b.classList.remove("active"));
    button.classList.add("active");
    document
      .querySelectorAll(".tab-content")
      .forEach((content) => content.classList.remove("active"));
    document.getElementById(`${tabName}-tab`).classList.add("active");
    document.getElementById("error-message").classList.remove("show");
  });
});
```

- **Explanation**: Event delegation (JS: efficient, revisit Stage 2 events).
- **Test**: Click tabs—switches, clears error.

**Step 4: Add GitLab Form Submit**
After password submit:

```javascript
document.getElementById("gitlab-login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("gitlab-username").value;
  const token = document.getElementById("gitlab-token").value;
  const errorDiv = document.getElementById("error-message");
  const submitBtn = e.target.querySelector('button[type="submit"]');
  errorDiv.classList.remove("show");
  submitBtn.disabled = true;
  submitBtn.textContent = "Authenticating...";
  try {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("gitlab_token", token);
    const response = await fetch("/api/auth/login-gitlab", {
      method: "POST",
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "GitLab failed");
    }
    localStorage.setItem("access_token", data.access_token);
    const payload = JSON.parse(atob(data.access_token.split(".")[1]));
    localStorage.setItem("username", payload.sub);
    localStorage.setItem("user_role", payload.role);
    sessionStorage.setItem("gitlab_token", token);  # NEW: Session for ops
    window.location.href = "/";
  } catch (error) {
    errorDiv.textContent = error.message;
    errorDiv.classList.add("show");
    submitBtn.disabled = false;
    submitBtn.textContent = "Login with GitLab";
  }
});
```

- **Explanation**: Similar to password, but /login-gitlab. SessionStorage for temp token (CS: ephemeral).
- **Test**: Call API—logs in, stores token.

**Full login.html/js**: Dual auth UI ready.

---

### 8.12: Frontend - Messaging UI (Incremental Panel)

**Step 1: Add Messages Button to Header**
In `index.html` `<header>` `.header-actions`:

```html
<button id="messages-toggle" class="btn btn-secondary btn-sm" title="Messages">
  📨
  <span id="message-badge" class="message-badge" style="display: none;">0</span>
</button>
```

- **Explanation**: Toggle button with badge (revisit Stage 4 toasts for UX).
- **Test**: Refresh—button shows.

**Step 2: Add Messages Panel**
Add before `</body>`:

```html
<div id="messages-panel" class="messages-panel">
  <div class="messages-header">
    <h3>Messages</h3>
    <button class="modal-close" id="close-messages">&times;</button>
  </div>
  <button class="btn btn-primary new-message-button" id="new-message-btn">
    ✉️ New Message
  </button>
  <div class="messages-body">
    <div id="messages-list"></div>
  </div>
</div>
```

- **Explanation**: Slide-in panel (CSS: fixed, transition). New button for compose.
- **Test**: No JS—panel hidden.

**Step 3: Add CSS for Panel**
In `components.css`:

```css
.messages-panel {
  position: fixed;
  top: 0;
  right: -400px;
  width: 400px;
  height: 100vh;
  background: var(--bg-primary);
  box-shadow: var(--shadow-xl);
  border-left: 1px solid var(--border-default);
  z-index: var(--z-modal);
  transition: right var(--transition-base);
  display: flex;
  flex-direction: column;
}
.messages-panel.open {
  right: 0;
}
.messages-header {
  padding: var(--spacing-4);
  border-bottom: 1px solid var(--border-default);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-secondary);
}
.messages-header h3 {
  margin: 0;
  color: var(--text-primary);
}
.messages-body {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-4);
}
.new-message-button {
  margin: var(--spacing-4);
  width: calc(100% - var(--spacing-8));
}
```

- **Explanation**: Right-slide (JS: toggle class). Overflow for scroll.
- **Test**: Add `open` class manually—slides in.

**Step 4: Add New Message Modal**
Add:

```html
<div id="new-message-modal" class="modal-overlay hidden">
  <div class="modal-content">
    <div class="modal-header">
      <h3>New Message</h3>
      <button class="modal-close">&times;</button>
    </div>
    <div class="modal-body">
      <form id="new-message-form">
        <div class="form-group">
          <label for="message-to">To</label>
          <input
            type="text"
            id="message-to"
            name="to_user"
            required
            placeholder="username or 'all'"
          />
        </div>
        <div class="form-group">
          <label for="message-subject">Subject</label>
          <input
            type="text"
            id="message-subject"
            name="subject"
            required
            maxlength="200"
          />
        </div>
        <div class="form-group">
          <label for="message-body">Message</label>
          <textarea
            id="message-body"
            name="body"
            required
            rows="6"
            maxlength="5000"
          ></textarea>
        </div>
        <div class="form-group">
          <label for="message-file">Related File</label>
          <input
            type="text"
            id="message-file"
            name="related_file"
            placeholder="e.g., PN1001.mcam"
          />
        </div>
        <div class="modal-actions">
          <button
            type="button"
            class="btn btn-secondary"
            onclick="newMessageModal.close()"
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-primary">Send</button>
        </div>
      </form>
    </div>
  </div>
</div>
```

- **Explanation**: Standard form (revisit Stage 3 modals).
- **Test**: Modal opens (stub JS).

**Step 5: Add View Message Modal**
Add:

```html
<div id="view-message-modal" class="modal-overlay hidden">
  <div class="modal-content">
    <div class="modal-header">
      <h3 id="view-message-subject"></h3>
      <button class="modal-close">&times;</button>
    </div>
    <div class="modal-body">
      <div style="margin-bottom: var(--spacing-4);">
        <strong>From:</strong> <span id="view-message-from"></span><br />
        <strong>Date:</strong> <span id="view-message-date"></span><br />
        <span id="view-message-file-info"></span>
      </div>
      <div id="view-message-body"></div>
      <div class="modal-actions">
        <button class="btn btn-danger" id="delete-message-btn">Delete</button>
        <button class="btn btn-secondary" onclick="viewMessageModal.close()">
          Close
        </button>
      </div>
    </div>
  </div>
</div>
```

- **Explanation**: Read-only view with delete.
- **Test**: Modal ready.

**Full index.html**: Messaging UI scaffolded.

---

### 8.13: Frontend - Messaging JavaScript (Handlers Incrementally)

**Step 1: Add Modals & Toggle**
In `app.js`, after modals:

```javascript
const newMessageModal = new ModalManager("new-message-modal");
const viewMessageModal = new ModalManager("view-message-modal");
let currentViewMessage = null;

function toggleMessagesPanel() {  # NEW
  const panel = document.getElementById("messages-panel");
  panel.classList.toggle("open");
  if (panel.classList.contains("open")) {
    loadMessages();
  }
}
```

- **Explanation**: Toggle slide (revisit Stage 2 transitions).
- **Test**: Click button—panel opens, calls load (stub error OK).

**Step 2: Add loadMessages (Fetch List)**
Add:

```javascript
async function loadMessages() {  # NEW
  const container = document.getElementById("messages-list");
  container.innerHTML = '<div class="loading">Loading...</div>';
  try {
    const data = await apiClient.getMessages();  # NEW call
    if (data.length === 0) {
      container.innerHTML = '<div class="messages-empty">No messages yet.</div>';
      return;
    }
    container.innerHTML = data.map((msg) => createMessageElement(msg)).join("");
    // Wire clicks next
  } catch (error) {
    container.innerHTML = `<p>Error: ${error.message}</p>`;
  }
}
```

- **Add to api-client.js**:
  ```javascript
  async getMessages() {
    return this.get('/api/messages/');
  }
  ```
- **Explanation**: Fetches/sorts (revisit Stage 4 store filter).
- **Test**: Send test message (curl), load—shows list.

**Step 3: Add createMessageElement**
Add:

```javascript
function createMessageElement(message) {  # NEW
  const date = new Date(message.timestamp);
  const isUnread = !message.read;
  return `
    <div class="message-item ${isUnread ? "unread" : ""}" id="message-${message.id}">
      <div class="message-from">${message.from_user === "all" ? "📢 Broadcast" : "👤 " + message.from_user}</div>
      <div class="message-subject">${escapeHtml(message.subject)}</div>
      <div class="message-preview">${escapeHtml(message.body.substring(0, 100))}...</div>
      <div class="message-time">${date.toLocaleString()}</div>
    </div>
  `;
}
```

- **Explanation**: Unread styling (revisit Stage 2 tokens). EscapeHtml prevents XSS (SE: security).
- **Test**: Load—formatted list.

**Step 4: Wire ViewMessage**
Add to loadMessages after render:

```javascript
data.forEach((msg) => {
  const el = document.getElementById(`message-${msg.id}`);
  if (el) el.onclick = () => viewMessage(msg);
});
```

Add:

```javascript
async function viewMessage(message) {  # NEW
  currentViewMessage = message;
  document.getElementById("view-message-subject").textContent = message.subject;
  document.getElementById("view-message-from").textContent = message.from_user;
  document.getElementById("view-message-date").textContent = new Date(message.timestamp).toLocaleString();
  document.getElementById("view-message-body").textContent = message.body;
  const fileInfo = document.getElementById("view-message-file-info");
  fileInfo.innerHTML = message.related_file ? `<strong>Related:</strong> ${message.related_file}<br>` : "";
  viewMessageModal.open();
  if (!message.read) {
    try {
      await apiClient.markMessageRead(message.id);
      loadMessages();
    } catch (e) {
      console.error(e);
    }
  }
}
```

- **Add to api-client.js**:
  ```javascript
  async markMessageRead(messageId) {
    return this.post(`/api/messages/${messageId}/mark-read`);
  }
  ```
- **Explanation**: Marks read on view (CS: event sourcing—immutable messages).
- **Test**: Click message—opens, marks read.

**Step 5: Add Send & Delete**
Add:

```javascript
async function sendNewMessage(event) {  # NEW
  event.preventDefault();
  const formData = new FormData(event.target);
  const data = {
    to_user: formData.get("to_user"),
    subject: formData.get("subject"),
    body: formData.get("body"),
    related_file: formData.get("related_file") || null,
  };
  try {
    await apiClient.sendMessage(data);
    toast.success("Sent!");
    newMessageModal.close();
    loadMessages();
  } catch (error) {
    toast.error(error.message);
  }
}

async function deleteCurrentMessage() {  # NEW
  if (!currentViewMessage || !confirm("Delete?")) return;
  try {
    await apiClient.deleteMessage(currentViewMessage.id);
    toast.success("Deleted");
    viewMessageModal.close();
    loadMessages();
  } catch (error) {
    toast.error(error.message);
  }
}
```

- **Add to api-client.js**:
  ```javascript
  async sendMessage(data) { return this.post('/api/messages/send', data); }
  async deleteMessage(messageId) { return this.delete(`/api/messages/${messageId}`); }
  ```
- **Explanation**: POST/DELETE (REST, revisit Stage 3 API).
- **Test**: Send/delete—updates list.

**Step 6: Wire in DOMContentLoaded**
Add:

```javascript
document.getElementById("messages-toggle").addEventListener("click", toggleMessagesPanel);
document.getElementById("close-messages").addEventListener("click", toggleMessagesPanel);
document.getElementById("new-message-btn").addEventListener("click", () => newMessageModal.open());
document.getElementById("new-message-form").addEventListener("submit", sendNewMessage);
document.getElementById("delete-message-btn").addEventListener("click", deleteCurrentMessage);
updateUnreadCount();
setInterval(updateUnreadCount, 30000);  # Poll
```

Add:

```javascript
async function updateUnreadCount() {  # NEW
  try {
    const data = await apiClient.getUnreadCount();
    const badge = document.getElementById("message-badge");
    badge.textContent = data.unread_count;
    badge.style.display = data.unread_count > 0 ? "inline-block" : "none";
  } catch (e) { console.error(e); }
}
```

- **Add to api-client.js**: `async getUnreadCount() { return this.get('/api/messages/unread-count'); }`
- **Explanation**: Polls unread (JS: setInterval, revisit Stage 4 reactive).
- **Test**: Send unread—badge shows, updates.

**Full app.js**: Messaging integrated.

---

### 8.14: Configuration Manager (Incremental YAML)

**Step 1: Create File & Defaults**

```bash
touch backend/app/config_manager.py
```

Paste:

```python
import yaml
from pathlib import Path
from typing import Optional, Dict

DEFAULT_CONFIG = {  # NEW
    'mode': 'server',
    'gitlab': {'enabled': True, 'url': 'https://gitlab.com', 'repo_url': '', 'branch': 'main', 'lfs_enabled': True},
    'server': {'host': '0.0.0.0', 'port': 8000, 'sync_interval': 60},
    'security': {'secret_key': '', 'encryption_key': ''},
    'paths': {'clone_path': './gitlab_repo_clone'}
}

class ConfigManager:
    def __init__(self, config_file: Optional[Path] = None):
        self.config_file = config_file or Path('config.yaml')
        self.config = self._load_config()  # Call load

    def _load_config(self) -> Dict:
        config = DEFAULT_CONFIG.copy()
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                file_config = yaml.safe_load(f) or {}
                self._merge_config(config, file_config)  # Merge YAML
        self._load_from_env(config)  # Override env
        return config
```

- **Explanation**: YAML for human-editable (SE: config as code). Defaults fallback.
- **Test**: `python -c "from app.config_manager import ConfigManager; print(ConfigManager().config['mode'])"` → "server".

**Step 2: Add \_merge_config & \_load_from_env**
Add:

```python
def _merge_config(self, base: Dict, override: Dict):
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            self._merge_config(base[key], value)
        else:
            base[key] = value

def _load_from_env(self, config: Dict):
    if os.getenv('MODE'):
        config['mode'] = os.getenv('MODE')
    # ... add all env overrides (from your code)
```

- **Explanation**: Recursive merge (CS: tree traversal). Env > YAML > defaults (SE: 12-factor).
- **Test**: Create config.yaml with mode: standalone, load—overrides default.

**Step 3: Add get/set & save_config**
Add:

```python
def get(self, key_path: str, default=None):
    keys = key_path.split('.')
    value = self.config
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    return value

def set(self, key_path: str, value):
    keys = key_path.split('.')
    target = self.config
    for key in keys[:-1]:
        if key not in target:
            target[key] = {}
        target = target[key]
    target[keys[-1]] = value

def save_config(self):
    with open(self.config_file, 'w') as f:
        yaml.dump(self.config, f, default_flow_style=False)
```

- **Explanation**: Dot-notation (JS-like, revisit Stage 4 store). YAML dump pretty-prints.
- **Test**: Set 'mode' to 'standalone', save—config.yaml updates.

**Step 4: Add Mode Helpers**
Add:

```python
def is_standalone_mode(self) -> bool:
    return self.config['mode'] == 'standalone'

def is_gitlab_enabled(self) -> bool:
    return self.config['gitlab']['enabled']
```

- **Explanation**: Convenience (SE: abstraction).
- **Test**: True/False based on config.

**Singleton**:

```python
config_manager = ConfigManager()  # Global
```

**Full config_manager.py**: Manages hybrid configs.

---

### 8.15: PyInstaller Packaging (Build Steps)

**Step 1: Create pdm_app.py (Standalone Entry)**

```bash
touch backend/pdm_app.py
```

Paste:

```python
import sys
import webbrowser
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.main import app
from app.config import settings
import uvicorn

def run_server():
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, log_level="info")

def open_browser():
    time.sleep(2)
    webbrowser.open(f'http://127.0.0.1:{settings.PORT}')

def main():
    print("PDM System - Standalone Mode")
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    try:
        run_server()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
```

- **Explanation**: Threads server + browser (Python: concurrent, revisit events). Daemon thread auto-closes.
- **Test**: `python backend/pdm_app.py`—server starts, browser opens.

**Step 2: Create pdm.spec**

```bash
touch backend/pdm.spec
```

Paste your spec (with datas=['static', 'app'], hiddenimports for passlib/gitlab).

- **Explanation**: PyInstaller bundles (SE: packaging—includes static for exe).
- **Test**: No run yet.

**Step 3: Create build_standalone.py**

```bash
touch backend/build_standalone.py
```

Paste your build script.

- **Explanation**: Runs PyInstaller (SE: CI/CD—automate builds).
- **Test**: `python backend/build_standalone.py`—creates dist/PDM_System.exe.

**Step 4: Build & Test Exe**

```bash
pip install pyinstaller
python backend/build_standalone.py
```

- **Explanation**: --clean clears old builds.
- **Test**: Double-click exe—opens browser to login. Login works (local mode if GitLab off).

**Full packaging**: Standalone ready.

---

### 8.16: Testing Guide (Create & Use)

**Step 1: Create TESTING.md**

```bash
touch TESTING.md
```

Paste your guide—it's comprehensive.

**Step 2: Test Server Mode**
Set .env MODE=server, run uvicorn—test auth, files, messages, sync (edit GitLab, pull updates).

**Step 3: Test Standalone**
Set config.yaml mode: standalone, build exe—run, test same flows (clones GitLab).

**Full TESTING.md**: Guides verification.

---

### Stage 8 Complete

**Incremental Recap**:

- Each step: Add/test 1-2 features, revisit topics (e.g., encryption on hashing).
- Depth: CS (PBKDF2, optimistic locking), app (sync flows), Python (Fernet, yaml), JS (tabs, events), SE (config, packaging).

**Test Both Modes**:

- Server: uvicorn—multi-user.
- Standalone: exe—single-user, portable.

Your original Stage 8 is now incremental—engaging and deep! Ready for deployment or tweaks?
