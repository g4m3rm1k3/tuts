# PDM Tutorial - Stage 5: Authentication & Authorization

**Prerequisites**: Completed Stage 4. Your app should have reactive state (search/filter/sort updates UI), toasts on errors, and pretty Tailwind styling. Test: Search a file name—list filters instantly, toast on API fail.
**Time**: 5-6 hours
**What you'll build**: JWT auth (login/register), password hashing (bcrypt), role-based access (admin/user), protected endpoints, login page (dual: password/PAT). _Incremental_: One schema/method/endpoint at a time, test with curl/docs. **Tailwind**: Yes—login form with tabs (`flex gap-2`), buttons (`bg-primary px-4 py-2`).

---

### Deep Dive: Authentication vs Authorization (CS: Identity/Access, SE: Layers)

**CS Topic**: AuthN = "who are you?" (identity proof, e.g., hash challenge-response, CS: zero-knowledge proofs in advanced). AuthZ = "what can you do?" (permissions, CS: ACL graphs or RBAC matrices). JWT = stateless token (header.payload.signature, CS: HMAC for integrity, base64 not encrypt). **App Topic**: Hybrid auth (local + GitLab PAT)—PAT for Git ops (revisit Stage 8 sync). **SE Principle**: Least privilege (roles limit, defense in depth). **Python Specific**: Pydantic = schema validation (type-safe input). **JS Specific**: localStorage = session (but clear on logout, CS: client-side state). Gotcha: Tokens expire (refresh later).

Create `backend/app/learn_auth_concepts.py` (paste original)—run `python -m app.learn_auth_concepts` to see hashing/JWT demo.

---

### 5.1: Install Auth Dependencies (One at a Time)

**Step 1: Add passlib[bcrypt]**
In `requirements.txt`:

```
passlib[bcrypt]==1.7.4  # NEW: Password hashing
```

```bash
pip install -r requirements.txt
```

- **Explanation**: passlib = hash wrappers (CS: KDFs like bcrypt = slow, salted PBKDF2 variant). [bcrypt] = C bindings (fast).
- **Test**: `python -c "from passlib.context import CryptContext; print('OK')"` → OK.
- **Gotcha**: bcrypt needs compiler (Windows: pre-built wheels).

**Step 2: Add python-jose & multipart**
Add:

```
python-jose[cryptography]==3.3.0  # NEW: JWT
python-multipart==0.0.6  # NEW: Form data
```

Install: `pip install -r requirements.txt`.

- **Explanation**: jose = JWT encode/decode (CS: JOSE standard). Multipart = form parsing (app: login forms).
- **Test**: `python -c "from jose import jwt; print('OK')"` → OK.
- **Gotcha**: [cryptography] = secure random (no weak keys).

---

### 5.2: Authentication Schemas (Pydantic Incremental)

**Step 1: Create schemas/auth.py**

```bash
mkdir -p backend/app/schemas  # If missing
touch backend/app/schemas/auth.py
```

Paste base User:

```python
from pydantic import BaseModel, Field  # NEW: Validation

class User(BaseModel):  # NEW: Schema
    username: str = Field(..., min_length=3, max_length=50)  # NEW
    full_name: str  # NEW
    role: str = Field(..., description="User role: 'admin' or 'user'")  # NEW
```

- **Explanation**: BaseModel = dict with validation (CS: schema, like JSON Schema). Field = constraints (app: input safety).
- **Test**: `python -c "from app.schemas.auth import User; u = User(username='test', full_name='Test', role='user'); print(u)"` → Valid User.
- **Gotcha**: ... = required.

**Step 2: Add UserInDB (Sensitive)**
Add:

```python
class UserInDB(User):  # NEW: Inherit
    password_hash: str  # NEW: Internal only
```

- **Explanation**: Inherit = reuse (CS: composition). No expose hash (SE: least info).
- **Test**: `u = UserInDB(..., password_hash='hash'); print(u.password_hash)` → 'hash'.

**Step 3: Add UserCreate (Input)**
Add:

```python
class UserCreate(BaseModel):  # NEW
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)  # NEW
    full_name: str
    role: str = "user"
    @validator('username')  # NEW: Custom
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Must be alphanumeric')
        return v.lower()
    @validator('password')  # NEW
    def password_strength(cls, v):
        if len(v) < 8 or v.isdigit() or v.lower() == v:
            raise ValueError('At least 8 chars, not all numbers, one upper')
        return v
```

- **Explanation**: Validator = hook (CS: predicate functions). Lower = normalize (app: case-insensitive login).
- **Test**: UserCreate(username='Test1', password='Pass123', full_name='Test') → OK. Invalid → ValueError.
- **Gotcha**: Validator cls = classmethod.

**Step 4: Add Token Schemas**
Add:

```python
class Token(BaseModel):  # NEW
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):  # NEW
    username: str | None = None
    role: str | None = None
```

- **Explanation**: Token = response (app: JWT). TokenData = decoded claims (internal).
- **Test**: Token(access_token='jwt') → Valid.

**Step 5: Update **init**.py**
In `backend/app/schemas/__init__.py` (create if missing):

```python
from .auth import User, UserInDB, UserCreate, Token, TokenData  # NEW
```

- **Explanation**: Exports for import \* (SE: facade).
- **Test**: `from app.schemas import User` → OK.

**Full auth.py** (End of Section—Verify):

```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str
    role: str = Field(..., description="User role: 'admin' or 'user'")

class UserInDB(User):
    password_hash: str

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: str
    role: str = "user"
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Must be alphanumeric')
        return v.lower()
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8 or v.isdigit() or v.lower() == v:
            raise ValueError('At least 8 chars, not all numbers, one upper')
        return v

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
```

**Verification**: Invalid UserCreate → Errors.

### 5.3: Authentication Service (Hashing/JWT Incremental)

**Step 1: Create auth_service.py**

```bash
touch backend/app/services/auth_service.py
```

Paste hashing:

```python
from passlib.context import CryptContext  # NEW
from datetime import datetime, timedelta, timezone  # NEW
from typing import Optional  # NEW
from jose import jwt  # NEW
from app.config import settings  # NEW
from app.schemas.auth import UserInDB, User, Token, TokenData  # NEW

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # NEW

def verify_password(plain: str, hashed: str) -> bool:  # NEW
    return pwd_context.verify(plain, hashed)

def get_password_hash(password: str) -> str:  # NEW
    return pwd_context.hash(password)
```

- **Explanation**: CryptContext = handler (CS: adapter pattern). Bcrypt = slow hash (revisit deep dive).
- **Test**: `python -c "from app.services.auth_service import get_password_hash, verify_password; h = get_password_hash('pass'); print(verify_password('pass', h))"` → True.
- **Gotcha**: Hash idempotent (same input = different hash due to salt).

**Step 2: Add JWT Functions**
Add:

```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:  # NEW
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:  # NEW
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.JWTError:
        return None
```

- **Explanation**: encode = sign payload (CS: HMAC, header/payload/signature). Decode verifies (app: stateless auth).
- **Test**: `token = create_access_token({"sub": "test"}); decode_access_token(token)` → {'sub': 'test', 'exp': ...}.
- **Gotcha**: Exp = auto-expire (security).

**Step 3: Add UserService Skeleton**
Add:

```python
class UserService:  # NEW
    def __init__(self, users_file: Path):
        self.users_file = users_file
        if not self.users_file.exists():
            self.users_file.write_text('{}')
```

- **Explanation**: File-based users (JSON, revisit Stage 3 atomic).
- **Test**: Init—creates users.json {}.

**Step 4: Add load/save_users**
Add:

```python
    def load_users(self) -> dict:  # NEW
        try:
            with LockedFile(self.users_file, 'r') as f:  # Atomic
                content = f.read()
                if not content.strip():
                    return {}
                return json.loads(content)
        except Exception:
            return {}

    def save_users(self, users: dict):  # NEW
        try:
            with LockedFile(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            raise
```

- **Explanation**: LockedFile = concurrent safe (revisit Stage 3).
- **Test**: Load/save {}—file updates.

**Step 5: Add get_user/create_user**
Add:

```python
    def get_user(self, username: str) -> Optional[UserInDB]:  # NEW
        users = self.load_users()
        user_data = users.get(username)
        if user_data:
            return UserInDB(**user_data)
        return None

    def create_user(self, username: str, password: str, full_name: str, role: str = "user"):  # NEW
        users = self.load_users()
        if username in users:
            raise ValueError(f"User exists: {username}")
        password_hash = get_password_hash(password)
        users[username] = {
            "username": username,
            "password_hash": password_hash,
            "full_name": full_name,
            "role": role
        }
        self.save_users(users)
```

- **Explanation**: \*\* = unpack (Python: kwarg). ValueError = explicit.
- **Test**: Create user—users.json = {"test": {hash, ...}}. Get—UserInDB.

**Step 6: Add authenticate_user**
Add:

```python
    def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:  # NEW
        user = self.get_user(username)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user
```

- **Explanation**: And short-circuit = early fail (CS: lazy eval).
- **Test**: Auth valid/invalid—UserInDB/None.

**Step 7: Add create_default_users**
Add:

```python
    def create_default_users(self):  # NEW
        users = self.load_users()
        if users:
            return
        self.create_user("admin", "Admin123!", "Administrator", "admin")
        self.create_user("john", "Password123!", "John Doe", "user")
```

- **Explanation**: Idempotent (if users, skip).
- **Test**: Call—users.json = defaults.

**Full auth_service.py** (End of Section—Verify):

```python
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from app.config import settings
from app.schemas.auth import UserInDB, User, Token, TokenData
from app.utils.file_locking import LockedFile
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.JWTError:
        return None

class UserService:
    def __init__(self, users_file: Path):
        self.users_file = users_file
        if not self.users_file.exists():
            self.users_file.write_text('{}')
    def load_users(self) -> dict:
        try:
            with LockedFile(self.users_file, 'r') as f:
                content = f.read()
                if not content.strip():
                    return {}
                return json.loads(content)
        except Exception:
            return {}
    def save_users(self, users: dict):
        try:
            with LockedFile(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            raise
    def get_user(self, username: str) -> Optional[UserInDB]:
        users = self.load_users()
        user_data = users.get(username)
        if user_data:
            return UserInDB(**user_data)
        return None
    def create_user(self, username: str, password: str, full_name: str, role: str = "user"):
        users = self.load_users()
        if username in users:
            raise ValueError(f"User exists: {username}")
        password_hash = get_password_hash(password)
        users[username] = {
            "username": username,
            "password_hash": password_hash,
            "full_name": full_name,
            "role": role
        }
        self.save_users(users)
    def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        user = self.get_user(username)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user
    def create_default_users(self):
        users = self.load_users()
        if users:
            return
        self.create_user("admin", "Admin123!", "Administrator", "admin")
        self.create_user("john", "Password123!", "John Doe", "user")
```

**Verification**: create_default_users—users.json populated. Auth "admin"/"Admin123!" → UserInDB.

### 5.4: Authentication Dependencies (FastAPI Deps Incremental)

**Step 1: Create deps.py**

```bash
touch backend/app/api/deps.py
```

Paste OAuth:

```python
from fastapi.security import OAuth2PasswordBearer  # NEW
from app.services.auth_service import decode_access_token  # NEW

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")  # NEW: Header Bearer
```

- **Explanation**: OAuth2PasswordBearer = extracts "Authorization: Bearer <token>" (app: standard).
- **Test**: Import—no errors.

**Step 2: Add get_user_service**
Add:

```python
def get_user_service() -> UserService:  # NEW: Factory
    from app.config import settings  # NEW
    users_file = settings.BASE_DIR / 'users.json'
    return UserService(users_file)
```

- **Explanation**: Depends calls this (DI, SE: testable—mock factory).
- **Test**: `python -c "from app.api.deps import get_user_service; print(get_user_service())"` → <UserService>.

**Step 3: Add get_current_user**
Add:

```python
from fastapi import Depends, HTTPException, status  # NEW
from app.schemas.auth import User  # NEW

async def get_current_user(  # NEW: Async dep
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> User:
    credentials_exception = HTTPException(  # NEW
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)  # NEW
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user_in_db = user_service.get_user(username)
    if user_in_db is None:
        raise credentials_exception
    return User(  # NEW: Public model
        username=user_in_db.username,
        full_name=user_in_db.full_name,
        role=user_in_db.role
    )
```

- **Explanation**: Depends chain (user_service calls auth). payload.get = safe (CS: dict access). User = no hash (SE: info hiding).
- **Test**: Stub token, call—raises 401 if invalid.
- **Gotcha**: Async = for future DB (now sync OK).

**Step 4: Add require_role (RBAC)**
Add:

```python
def require_role(allowed_roles: list[str]):  # NEW: Factory
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:  # NEW: Inner dep
        if current_user.role not in allowed_roles:
            raise HTTPException(403, f"Requires {allowed_roles}. You have {current_user.role}")
        return current_user
    return role_checker

require_admin = require_role(["admin"])  # NEW: Alias
require_user = require_role(["admin", "user"])
```

- **Explanation**: Factory = closure (CS: higher-order function). 403 = forbidden (HTTP).
- **Test**: Stub user role='user', require_admin—raises.
- **Gotcha**: List not str (multiple roles).

**Full deps.py** (End of Section—Verify):

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app.schemas.auth import User
from app.services.auth_service import decode_access_token, UserService
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_user_service() -> UserService:
    users_file = settings.BASE_DIR / 'users.json'
    return UserService(users_file)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user_in_db = user_service.get_user(username)
    if user_in_db is None:
        raise credentials_exception
    return User(
        username=user_in_db.username,
        full_name=user_in_db.full_name,
        role=user_in_db.role
    )

def require_role(allowed_roles: list[str]):
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {allowed_roles}. You have {current_user.role}"
            )
        return current_user
    return role_checker

require_admin = require_role(["admin"])
require_user = require_role(["admin", "user"])
```

**Verification**: get_current_user with stub token—User or 401.

### 5.5: Authentication API Routes (Endpoints Incremental)

**Step 1: Create auth.py**

```bash
touch backend/app/api/auth.py
```

Paste router:

```python
from fastapi import APIRouter  # NEW
from fastapi.security import OAuth2PasswordRequestForm  # NEW: Form
from datetime import timedelta  # NEW
from app.schemas.auth import Token, User  # NEW
from app.services.auth_service import UserService, create_access_token  # NEW
from app.api.deps import get_user_service, get_current_user  # NEW
from app.config import settings  # NEW

router = APIRouter(prefix="/api/auth", tags=["authentication"])  # NEW
```

- **Explanation**: OAuth2PasswordRequestForm = username/password extract (app: standard login).
- **Test**: Import—no errors.

**Step 2: Add /login**
Add:

```python
@router.post("/login", response_model=Token)  # NEW
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username, "role": user.role}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
```

- **Explanation**: Depends form = auto-parse (app: secure, no raw body). Sub = standard claim (CS: JWT RFC).
- **Test**: /docs, POST username="admin" password="Admin123!" → Token.
- **Gotcha**: Headers for WWW-Auth (client hint).

**Step 3: Add /me**
Add:

```python
@router.get("/me", response_model=User)  # NEW
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user
```

- **Explanation**: Protected by dep (authZ chain).
- **Test**: With token header, /api/auth/me → User JSON.

**Step 4: Include in main.py**
Add:

```python
from app.api import files, auth  # NEW
app.include_router(auth.router)  # NEW
```

- **Test**: Restart, /docs → Auth endpoints. Call /login → Token, /me with Bearer → User.

**Full auth.py** (End of Section—Verify):

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.schemas.auth import Token, User
from app.services.auth_service import UserService, create_access_token
from app.api.deps import get_user_service, get_current_user
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return current_user
```

**Verification**: Login → Token, /me with Bearer → {"username": "admin", ...}.

### 5.6: Protect API Endpoints (Deps in Files Incremental)

**Step 1: Update files.py get_files (Add Dep)**
In `@router.get("/")`:

```python
def get_files(
    current_user: User = Depends(get_current_user),  # NEW: Protect
    file_service: FileService = Depends(get_file_service)
):
    # ... existing
```

- **Explanation**: Dep = middleware (CS: chain of responsibility). Now auth required.
- **Test**: /api/files without token → 401. With Bearer → List.
- **Gotcha**: Order = execution order.

**Step 2: Update checkout (User from Token)**
In checkout_file:

```python
file_service.checkout_file(
    filename=request.filename,
    user=current_user.username,  # NEW: From token, not request
    message=request.message
)
```

- **Explanation**: Token sub = trusted user (CS: principal propagation).
- **Test**: POST with token → Locks with "admin".

**Step 3: Add require_admin to Force (Stage 6 Preview)**
For force_checkin (if added):

```python
def force_checkin_file(
    filename: str,
    current_user: User = Depends(require_admin),  # NEW
    # ...
):
```

- **Explanation**: Role check (SE: policy as code).
- **Test**: As user → 403, admin → OK.

**Full files.py** (End of Section—Verify):
[Full with protected routes, user from token]

**Verification**: /api/files requires token. Checkout uses token user.

### 5.7: Frontend - Login Page (Dual Auth Incremental)

**Step 1: Create login.html**

```bash
touch backend/static/login.html
```

Paste skeleton:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Login - PDM</title>
    <link rel="stylesheet" href="/static/css/main.css" />
  </head>
  <body
    class="flex items-center justify-center min-h-screen bg-gradient-to-br from-primary-500 to-primary-700"
  >
    # Tailwind
    <div class="bg-card p-8 rounded-lg shadow-xl w-11/12 max-w-md border">
      # Login card
      <div class="text-center mb-6">
        # Header
        <h1 class="text-4xl font-bold text-primary mb-2">PDM System</h1>
        <p class="text-inverse">Parts Data Management</p>
      </div>
      <div
        id="error-message"
        class="bg-danger/10 text-danger p-3 rounded mb-4 text-sm hidden"
      ></div>
      # Error
      <form id="login-form">
        # Form
        <div class="mb-5">
          # Group
          <label
            for="username"
            class="block mb-2 font-medium text-primary text-sm"
            >Username</label
          >
          <input
            type="text"
            id="username"
            name="username"
            required
            class="w-full p-3 border border-default rounded bg-primary text-primary"
          />
        </div>
        <div class="mb-5">
          # Password
          <label
            for="password"
            class="block mb-2 font-medium text-primary text-sm"
            >Password</label
          >
          <input
            type="password"
            id="password"
            name="password"
            required
            class="w-full p-3 border border-default rounded bg-primary text-primary"
          />
        </div>
        <button
          type="submit"
          class="w-full bg-primary text-inverse py-2 rounded hover:bg-primary-dark"
        >
          Login
        </button>
        # Submit
      </form>
      <div
        class="mt-6 pt-6 border-t border-default text-center text-sm text-secondary"
      >
        # Demo
        <p><strong>Demo:</strong> admin/Admin123! or john/Password123!</p>
      </div>
    </div>
    <script type="module" src="/static/js/login.js"></script>
    # JS
  </body>
</html>
```

- **Explanation**: Tailwind classes = atomic layout (flex items-center = center). mb-5 = spacing.
- **Test**: /login → Pretty form.
- **Gotcha**: required = HTML5 validation.

**Step 2: Add login.js (Submit Stub)**

```bash
touch backend/static/js/login.js
```

Paste:

```javascript
document.getElementById("login-form").addEventListener("submit", async (e) => {  # NEW
  e.preventDefault();  # NEW: No reload
  const formData = new FormData(e.target);  # NEW
  const username = formData.get("username");  # NEW
  const password = formData.get("password");
  const errorDiv = document.getElementById("error-message");
  const submitBtn = e.target.querySelector('button[type="submit"]');
  errorDiv.classList.remove("show");
  submitBtn.disabled = true;
  submitBtn.textContent = "Logging in...";
  try {
    const response = await fetch("/api/auth/login", {  # NEW
      method: "POST",
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: new URLSearchParams(formData),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Login failed");
    localStorage.setItem("access_token", data.access_token);  # NEW
    const payload = JSON.parse(atob(data.access_token.split(".")[1]));
    localStorage.setItem("username", payload.sub);
    localStorage.setItem("user_role", payload.role);
    window.location.href = "/";  # NEW: Redirect
  } catch (error) {
    errorDiv.textContent = error.message;
    errorDiv.classList.add("show");
    submitBtn.disabled = false;
    submitBtn.textContent = "Login";
  }
});
```

- **Explanation**: FormData/URLSearchParams = form encode (app: OAuth2). atob = base64 decode (CS: JWT parse).
- **Test**: /login, submit admin/Admin123! → Redirects to /, token in localStorage.
- **Gotcha**: preventDefault = SPA (no page reload).

**Step 3: Update main.py for /login**
Add:

```python
from fastapi.responses import FileResponse  # NEW

@app.get("/login", response_class=FileResponse)  # NEW
async def serve_login():
    return FileResponse("static/login.html")
```

- **Test**: /login → Form loads.

**Full login.html** (End of Section—Verify):
[Full with Tailwind, tabs stub if dual, but single for now]

**Full login.js**:

```javascript
document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const username = formData.get("username");
  const password = formData.get("password");
  const errorDiv = document.getElementById("error-message");
  const submitBtn = e.target.querySelector('button[type="submit"]');
  errorDiv.classList.remove("show");
  submitBtn.disabled = true;
  submitBtn.textContent = "Logging in...";
  try {
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams(formData),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Login failed");
    localStorage.setItem("access_token", data.access_token);
    const payload = JSON.parse(atob(data.access_token.split(".")[1]));
    localStorage.setItem("username", payload.sub);
    localStorage.setItem("user_role", payload.role);
    window.location.href = "/";
  } catch (error) {
    errorDiv.textContent = error.message;
    errorDiv.classList.add("show");
    submitBtn.disabled = false;
    submitBtn.textContent = "Login";
  }
});
```

**Verification**: Login → Token stored, /me works with header.

### Stage 5 Complete

**Test Full**: Login → Protected /api/files requires token. Defaults created.

**Verification**:

- [ ] Login returns JWT.
- [ ] /me with Bearer → User.
- [ ] Protected endpoints 401 without token.
- [ ] users.json = hashed users.

**What You Learned (Depth)**:

- **CS**: JWT (signed tokens), bcrypt (KDF).
- **App**: OAuth2 flow (Bearer).
- **Python**: Pydantic validators, Depends DI.
- **JS**: FormData, localStorage (session).
- **SE**: RBAC (require_role), least privilege (no hash in User).

Ready for Stage 6 (Advanced AuthZ/Audit)?
