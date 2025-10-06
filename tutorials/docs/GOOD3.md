# Chapter 2: Authentication & Authorization

## Chapter 2.1: Password Hashing & User Domain

**File**: `backend/core/security.py`

```python
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain, hashed)

# JWT tokens
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")

def decode_access_token(token: str) -> dict | None:
    """Decode and verify JWT token."""
    try:
        return jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except JWTError:
        return None
```

**Learn more:**

- [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) - OWASP guide
- [JWT Introduction](https://jwt.io/introduction) - How tokens work
- [Passlib Documentation](https://passlib.readthedocs.io/en/stable/) - Bcrypt details

---

**File**: `backend/domain/users.py`

```python
from dataclasses import dataclass
from typing import Dict
from core.exceptions import UnauthorizedError
from core.security import hash_password, verify_password

@dataclass(frozen=True)
class User:
    """Immutable user record."""
    username: str
    password_hash: str
    full_name: str
    role: str  # 'admin' or 'user'

class UserManager:
    """User business logic."""

    def __init__(self, users: Dict[str, User]):
        self._users = users

    def create_user(
        self,
        username: str,
        password: str,
        full_name: str,
        role: str = "user"
    ) -> Dict[str, User]:
        """
        Create new user.
        Returns: New state with user added
        """
        if username in self._users:
            raise ValueError(f"Username {username} already exists")

        user = User(
            username=username,
            password_hash=hash_password(password),
            full_name=full_name,
            role=role
        )

        return {**self._users, username: user}

    def authenticate(self, username: str, password: str) -> User:
        """
        Authenticate user.
        Returns: User if valid
        Raises: UnauthorizedError if invalid
        """
        user = self._users.get(username)
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid credentials")
        return user

    def get_user(self, username: str) -> User | None:
        """Get user by username."""
        return self._users.get(username)
```

---

## Chapter 2.2: User Storage Adapter

**File**: `backend/adapters/storage.py` (add to existing file)

```python
from domain.users import User

class UserStorage(Protocol):
    """Interface for user persistence."""
    def load(self) -> Dict[str, User]: ...
    def save(self, users: Dict[str, User]) -> None: ...

class JSONUserStorage:
    """JSON file implementation for users."""

    def __init__(self, file_path: Path = settings.data_dir / "users.json"):
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self):
        if not self.file_path.exists():
            # Create default admin user
            from core.security import hash_password
            default_admin = {
                "admin": {
                    "username": "admin",
                    "password_hash": hash_password("admin123"),
                    "full_name": "Administrator",
                    "role": "admin"
                }
            }
            self.file_path.write_text(json.dumps(default_admin, indent=2))

    def load(self) -> Dict[str, User]:
        data = json.loads(self.file_path.read_text())
        return {
            username: User(**user_data)
            for username, user_data in data.items()
        }

    def save(self, users: Dict[str, User]) -> None:
        data = {
            username: {
                'username': user.username,
                'password_hash': user.password_hash,
                'full_name': user.full_name,
                'role': user.role
            }
            for username, user in users.items()
        }
        self.file_path.write_text(json.dumps(data, indent=2))
```

---

## Chapter 2.3: User Service

**File**: `backend/domain/users.py` (add to same file)

```python
from adapters.storage import UserStorage
from core.security import create_access_token

class UserService:
    """User operations orchestration."""

    def __init__(self, storage: UserStorage):
        self.storage = storage

    def register(self, username: str, password: str, full_name: str) -> None:
        """Register new user."""
        users = self.storage.load()
        manager = UserManager(users)
        new_users = manager.create_user(username, password, full_name)
        self.storage.save(new_users)

    def login(self, username: str, password: str) -> str:
        """
        Authenticate and return JWT token.
        Raises: UnauthorizedError if invalid
        """
        users = self.storage.load()
        manager = UserManager(users)
        user = manager.authenticate(username, password)

        # Create token with user info
        token_data = {
            "sub": user.username,
            "role": user.role
        }
        return create_access_token(token_data)

    def get_user(self, username: str) -> User | None:
        """Get user by username."""
        users = self.storage.load()
        manager = UserManager(users)
        return manager.get_user(username)
```

---

## Chapter 2.4: Auth Schemas

**File**: `backend/schemas/requests.py` (add to existing)

```python
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()
```

**File**: `backend/schemas/responses.py` (add to existing)

```python
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    username: str
    full_name: str
    role: str
```

---

## Chapter 2.5: Auth Dependencies

**File**: `backend/api/dependencies.py` (add to existing)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from domain.users import UserService, User
from adapters.storage import JSONUserStorage
from core.security import decode_access_token
from core.exceptions import UnauthorizedError

security = HTTPBearer()

def get_user_storage():
    return JSONUserStorage()

def get_user_service(
    storage: Annotated[JSONUserStorage, Depends(get_user_storage)]
) -> UserService:
    return UserService(storage)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_service: UserServiceDep
) -> User:
    """
    Extract and validate JWT token, return current user.

    Used in routes that require authentication:
    def protected_route(current_user: CurrentUser):
        ...
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    username = payload.get("sub")
    user = user_service.get_user(username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

# Type alias for route signatures
CurrentUser = Annotated[User, Depends(get_current_user)]

def require_admin(current_user: CurrentUser) -> User:
    """Dependency for admin-only routes."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

AdminUser = Annotated[User, Depends(require_admin)]
```

**Learn more:**

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/) - OAuth2, JWT
- [HTTP Bearer Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) - Standard

---

## Chapter 2.6: Auth Routes

**File**: `backend/api/routes/auth.py`

```python
from fastapi import APIRouter, HTTPException, status
from schemas.requests import LoginRequest, RegisterRequest
from schemas.responses import TokenResponse, UserResponse
from api.dependencies import UserServiceDep, CurrentUser
from core.exceptions import UnauthorizedError

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, service: UserServiceDep):
    """Authenticate and receive JWT token."""
    try:
        token = service.login(request.username, request.password)
        return TokenResponse(access_token=token)
    except UnauthorizedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, service: UserServiceDep):
    """Register new user."""
    try:
        service.register(
            request.username,
            request.password,
            request.full_name
        )
        user = service.get_user(request.username)
        return UserResponse(
            username=user.username,
            full_name=user.full_name,
            role=user.role
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: CurrentUser):
    """Get current authenticated user info."""
    return UserResponse(
        username=current_user.username,
        full_name=current_user.full_name,
        role=current_user.role
    )
```

---

## Chapter 2.7: Protect Lock Routes

**File**: `backend/api/routes/locks.py` (update existing)

```python
from api.dependencies import LockServiceDep, CurrentUser, AdminUser

@router.post("/checkout", status_code=status.HTTP_201_CREATED)
def checkout_file(
    request: CheckoutRequest,
    service: LockServiceDep,
    current_user: CurrentUser  # Now requires auth!
) -> dict:
    """Checkout a file (requires authentication)."""
    try:
        service.checkout_file(
            request.filename,
            current_user.username,  # Use actual user
            request.message
        )
        return {"message": f"Checked out {request.filename}"}
    except FileLockedException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"File locked by {e.locked_by}"
        )

@router.post("/checkin")
def checkin_file(
    request: CheckinRequest,
    service: LockServiceDep,
    current_user: CurrentUser
) -> dict:
    """Checkin a file (requires authentication)."""
    try:
        # Regular users can only checkin their own files
        # This is enforced in domain layer (OwnershipError)
        service.checkin_file(request.filename, current_user.username)
        return {"message": f"Checked in {request.filename}"}
    except OwnershipError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@router.post("/force-checkin", dependencies=[Depends(require_admin)])
def force_checkin(
    request: CheckinRequest,
    service: LockServiceDep,
    admin_user: AdminUser
) -> dict:
    """Force checkin (admin only)."""
    service.checkin_file(request.filename, admin_user.username, is_admin=True)
    return {"message": f"Force checked in {request.filename}"}
```

---

## Chapter 2.8: Register Auth Routes

**File**: `backend/main.py` (update)

```python
from api.routes import locks, auth  # Add auth

def create_app() -> FastAPI:
    app = FastAPI(...)

    # Register routes
    app.include_router(auth.router)  # Add this
    app.include_router(locks.router)

    return app
```

---

## Chapter 2 Complete: Test Authentication

**Install dependencies**:

```bash
pip install "passlib[bcrypt]" "python-jose[cryptography]"
```

**Test flow**:

```bash
# 1. Login (default admin user)
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' \
  | jq -r '.access_token')

# 2. Get user info
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"

# 3. Checkout file (now requires token)
curl -X POST http://localhost:8000/api/locks/checkout \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filename": "part001.mcam", "message": "Editing"}'

# 4. Try without token (should fail)
curl -X POST http://localhost:8000/api/locks/checkout \
  -H "Content-Type: application/json" \
  -d '{"filename": "part002.mcam", "message": "Editing"}'
```

---

## Architecture Review

**Auth flow**:

```
1. User submits credentials
2. UserService validates via UserManager (domain)
3. Create JWT token with user claims
4. Client stores token
5. Client sends token in Authorization header
6. get_current_user dependency validates token
7. Routes receive authenticated User object
```

**Security layers**:

- Password hashing (bcrypt)
- JWT tokens (signed, expiring)
- Role-based access (admin vs user)
- Ownership validation (domain layer)

**Next**: Chapter 3 will add file management (upload, download, list files) with proper authorization. Continue?
