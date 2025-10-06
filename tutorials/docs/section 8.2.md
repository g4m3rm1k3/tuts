# PDM Tutorial - Stage 8: Hybrid Architecture - GitLab Integration for Both Modes (Part 2: Complete)

**Recap from Part 1**: You've configured hybrid mode (.env MODE=server, GitLab fields), installed python-gitlab/cryptography, and built GitLabService (validate*token returns user dict on real PAT). Test: Shell `python -c "from app.services.gitlab_service import GitLabService; s = GitLabService(); print(s.validate_token('your-pat'))"` → User info or None.
**Time for Part 2**: 3-4 hours (complete now)
**What you'll build (Part 2)**: Encrypted PAT storage (Fernet + PBKDF2 for users.json), GitLab-aware UserService (PAT auth + auto-register), messaging service/API (send/get/mark/read/delete, tied to files/audits). \_Incremental*: One method/UI per step, test with curl/login. **Tailwind**: Yes—login tabs (`flex gap-2 border-b`), messages (`fixed right-0 h-full bg-card shadow-xl` slide-in).

Sorry for the cutoff last time—here's the full Part 2, incremental as before.

---

### 8.5: Encrypted Token Storage (Build encryption.py Incrementally)

**Step 1: Create encryption.py**

```bash
touch backend/app/utils/encryption.py
```

Paste imports/skeleton:

```python
from cryptography.fernet import Fernet, InvalidToken  # NEW: Cipher
from cryptography.hazmat.primitives import hashes  # NEW: SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2  # NEW: Deriv
import base64  # NEW: Encode
import os  # NEW: Random
from typing import Optional  # NEW

def derive_key_from_password(password: str, salt: bytes) -> bytes:  # NEW: Stub
    pass
```

- **Explanation**: hazmat = low-level primitives (CS: building blocks, no high-level like passlib for custom). os.urandom = OS CSPRNG (secure entropy).
- **Test**: `python -c "from app.utils.encryption import derive_key_from_password; print('OK')"` → OK.
- **Gotcha**: pip install cryptography (wheels for Windows).

**Step 2: Implement derive_key_from_password**
Replace pass:

```python
    kdf = PBKDF2(  # NEW
        algorithm=hashes.SHA256(),
        length=32,  # AES key size
        salt=salt,
        iterations=100_000,  # Slow for security
    )
    key = kdf.derive(password.encode())  # UTF-8 to bytes
    return base64.urlsafe_b64encode(key)  # Web-safe
```

- **Explanation**: PBKDF2 = iterated HMAC (CS: work factor, 100k iterations ~0.3s, anti-parallel attacks). base64.urlsafe = no /+ chars (URL-safe).
- **Test**: `python -c "from app.utils.encryption import derive_key_from_password; key = derive_key_from_password('pass', b'salt' * 8); print(len(key))"` → 44 (base64 32 bytes).
- **Gotcha**: Salt 16 bytes = standard (unique per token).

**Step 3: Add encrypt_token**
Add:

```python
def encrypt_token(token: str, password: str) -> dict:  # NEW
    salt = os.urandom(16)  # Random per token
    key = derive_key_from_password(password, salt)
    cipher = Fernet(key)  # AES + HMAC
    encrypted = cipher.encrypt(token.encode())  # Pad/auth
    return {
        'encrypted_token': base64.urlsafe_b64encode(encrypted).decode('utf-8'),
        'salt': base64.urlsafe_b64encode(salt).decode('utf-8')
    }
```

- **Explanation**: urandom = crypt secure (CS: forward secrecy per token). Fernet.encrypt = authenticated (tamper-detect).
- **Test**: `python -c "from app.utils.encryption import encrypt_token; enc = encrypt_token('glpat-test', 'pass'); print(enc['encrypted_token'][:20])"` → gAAAAABl... (base64).
- **Gotcha**: encode() = str to bytes (UTF-8).

**Step 4: Add decrypt_token**
Add:

```python
def decrypt_token(encrypted_token: str, salt: str, password: str) -> Optional[str]:  # NEW
    try:
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_token)
        salt_bytes = base64.urlsafe_b64decode(salt)
        key = derive_key_from_password(password, salt_bytes)
        cipher = Fernet(key)
        decrypted = cipher.decrypt(encrypted_bytes)  # Verify/pad check
        return decrypted.decode('utf-8')
    except (InvalidToken, Exception):  # Wrong key/tamper
        return None
```

- **Explanation**: InvalidToken = HMAC fail (CS: integrity). Except = catch all (log in prod).
- **Test**: enc = encrypt_token('test', 'pass'); decrypt_token(enc['encrypted_token'], enc['salt'], 'pass') → 'test'. Wrong pass → None.
- **Gotcha**: decode errors='ignore' not needed (Fernet strict).

**Step 5: Add Test Block**
Add at end:

```python
if __name__ == "__main__":
    token = "glpat-test"
    password = "MySecurePassword123!"
    enc = encrypt_token(token, password)
    dec = decrypt_token(enc['encrypted_token'], enc['salt'], password)
    print(f"Match: {dec == token}")
    wrong = decrypt_token(enc['encrypted_token'], enc['salt'], "Wrong")
    print(f"Wrong: {wrong is None}")
```

- **Explanation**: Round-trip test (SE: unit test inline).
- **Test**: `python backend/app/utils/encryption.py` → Match: True\nWrong: True.

**Full encryption.py** (End of Section—Verify):

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

def encrypt_token(token: str, password: str) -> dict:
    salt = os.urandom(16)
    key = derive_key_from_password(password, salt)
    cipher = Fernet(key)
    encrypted = cipher.encrypt(token.encode())
    return {
        'encrypted_token': base64.urlsafe_b64encode(encrypted).decode('utf-8'),
        'salt': base64.urlsafe_b64encode(salt).decode('utf-8')
    }

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

if __name__ == "__main__":
    token = "glpat-test"
    password = "MySecurePassword123!"
    enc = encrypt_token(token, password)
    dec = decrypt_token(enc['encrypted_token'], enc['salt'], password)
    print(f"Match: {dec == token}")
    wrong = decrypt_token(enc['encrypted_token'], enc['salt'], "Wrong")
    print(f"Wrong: {wrong is None}")
```

**Verification**: Run script → Match: True, Wrong: True. Encrypt/decrypt round-trip.

### 8.6: GitLab-Aware User Service (Refactor auth_service Incrementally)

**Step 1: Add Imports to auth_service.py**
At top:

```python
from app.services.gitlab_service import GitLabService  # NEW
from app.services.gitlab_sync_service import GitLabSyncService  # NEW
from app.utils.encryption import encrypt_token, decrypt_token  # NEW
import secrets  # NEW: Random
```

- **Explanation**: Ties services (SE: composition). secrets = crypt random (CS: secure tokens).
- **Test**: Import—no errors.

**Step 2: Update **init** (Hybrid Params)**
Replace **init**:

```python
def __init__(self, users_file: Optional[Path] = None, gitlab_sync: Optional[GitLabSyncService] = None):  # NEW optional
    self.users_file = users_file
    self.gitlab_sync = gitlab_sync
    self.gitlab_service = GitLabService()  # NEW: Always
    self.use_gitlab = gitlab_sync is not None and settings.GITLAB_ENABLED
    if not self.use_gitlab and users_file:
        if not self.users_file.exists():
            self.users_file.write_text('{}')
```

- **Explanation**: Optional = fallback local (SE: graceful degradation).
- **Test**: Init with/without gitlab_sync—use_gitlab True/False.

**Step 3: Update load_users (Pull in GitLab)**
Replace:

```python
def load_users(self) -> dict:
    if self.use_gitlab:
        self.gitlab_sync.pull()  # NEW: Fresh
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

- **Explanation**: pull = optimistic lock (CS: version check before read).
- **Test**: Manual edit GitLab users.json, load → Updated.

**Step 4: Update save_users (Push in GitLab)**
Replace:

```python
def save_users(self, users: dict):
    if self.use_gitlab:
        self.gitlab_sync.save_json_file('users.json', users)
        self.gitlab_sync.commit_and_push(  # NEW
            files=['users.json'],
            message="Update users",
            author_name=settings.GIT_USER_NAME,
            author_email=settings.GIT_USER_EMAIL
        )
    else:
        with LockedFile(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
```

- **Explanation**: commit_and_push = transaction (SE: all or nothing).
- **Test**: Save—GitLab users.json updates + commit.

**Step 5: Add authenticate_with_gitlab_token**
Add:

```python
def authenticate_with_gitlab_token(self, username: str, gitlab_token: str) -> Optional[UserInDB]:  # NEW
    user_info = self.gitlab_service.validate_token(gitlab_token)  # NEW
    if not user_info or user_info['username'] != username:
        return None
    user = self.get_user(username)
    if not user:
        temp_password = secrets.token_urlsafe(32)  # NEW: Temp
        self.create_user(username, temp_password, user_info['name'], 'user', gitlab_token)  # NEW: Auto-register
        user = self.get_user(username)
    return user
```

- **Explanation**: token_urlsafe = URL-safe random (CS: base64). Auto-register = seamless (app: onboarding).
- **Test**: Call with valid PAT—creates user if new, returns UserInDB.

**Step 6: Update create_user (Encrypt Token)**
In create_user, after password_hash:

```python
user_data = {  # NEW
    "username": username,
    "password_hash": password_hash,
    "full_name": full_name,
    "role": role
}
if gitlab_token:  # NEW
    encrypted_data = encrypt_token(gitlab_token, password)
    user_data['encrypted_gitlab_token'] = encrypted_data['encrypted_token']
    user_data['token_salt'] = encrypted_data['salt']
```

- **Explanation**: Encrypt before save (SE: never plain in JSON).
- **Test**: Create with token—users.json has encrypted/salt.

**Step 7: Add get_gitlab_token (Decrypt)**
Add:

```python
def get_gitlab_token(self, username: str, password: str) -> Optional[str]:  # NEW
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

- **Explanation**: Decrypt for session (CS: derive on-demand).
- **Test**: Create with token, get_gitlab_token → Original PAT.

**Full auth_service.py** (End of Section—Verify):

```python:disable-run
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from app.config import settings
from app.schemas.auth import UserInDB, User, Token, TokenData
from app.utils.file_locking import LockedFile
import json
from app.services.gitlab_service import GitLabService
from app.services.gitlab_sync_service import GitLabSyncService
from app.utils.encryption import encrypt_token, decrypt_token
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire
```

### 8.7: Messaging System (Build message_service.py Incrementally)

**Step 1: Create message_service.py**

```bash
touch backend/app/services/message_service.py
```

Paste skeleton:

```python
from pathlib import Path  # NEW
from typing import List, Dict, Optional  # NEW
import json  # NEW
from datetime import datetime, timezone  # NEW
import logging  # NEW

from app.services.gitlab_sync_service import GitLabSyncService  # NEW: Hybrid
from app.utils.file_locking import LockedFile  # NEW: Atomic

logger = logging.getLogger(__name__)

class MessageService:  # NEW
    def __init__(self, messages_file: Optional[Path] = None, gitlab_sync: Optional[GitLabSyncService] = None):
        self.messages_file = messages_file
        self.gitlab_sync = gitlab_sync
        self.use_gitlab = gitlab_sync is not None
        if not self.use_gitlab and messages_file:
            if not messages_file.exists():
                messages_file.write_text('[]')
```

- **Explanation**: Hybrid storage (messages.json array in GitLab/local, revisit Stage 3 JSON). use_gitlab = flag (SE: feature toggle).
- **Test**: `python -c "from app.services.message_service import MessageService; print('OK')"` → OK.
- **Gotcha**: [] = empty array (append-only).

**Step 2: Add load_messages (Pull/Load)**
Add:

```python
    def load_messages(self) -> List[Dict]:  # NEW
        if self.use_gitlab:
            self.gitlab_sync.pull()  # Fresh
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

- **Explanation**: pull = sync (CS: optimistic lock). isinstance = type guard (Python: duck typing safe).
- **Test**: Load—[] or list.
- **Gotcha**: Dict fallback = schema evolve.

**Step 3: Add save_messages (Push)**
Add:

```python
    def save_messages(self, messages: List[Dict]):  # NEW
        if self.use_gitlab:
            self.gitlab_sync.save_json_file('messages.json', messages)
            self.gitlab_sync.commit_and_push(
                files=['messages.json'],
                message="Update messages",
                author_name=settings.GIT_USER_NAME,
                author_email=settings.GIT_USER_EMAIL
            )
        else:
            with LockedFile(self.messages_file, 'w') as f:
                json.dump(messages, f, indent=2)
```

- **Explanation**: Push after save = transaction (SE: durability).
- **Test**: Save [{}]—file/ GitLab updates.

**Step 4: Add send_message (Core)**
Add:

```python:disable-run
    def send_message(self, from_user: str, to_user: str, subject: str, body: str, related_file: Optional[str] = None) -> str:  # NEW
        import uuid  # NEW
        messages
```
