You've got it. We're now moving into a critical module that transforms our application from a single-user tool into a true multi-user platform. This part is dense, but it's one of the most important and transferable skill sets in all of web development.

---

### **Part 12: Fort Knox - Authentication & User Security (Masterclass Edition)**

**The Goal:** To allow users to register and log in, and to secure our API so that only authenticated users can perform actions like checking out or deleting files. We will implement the industry-standard **JWT (JSON Web Tokens)** authentication scheme.

#### **🚩 Step 1: The "Why" - Hashing & Stateless Authentication**

Before we write code, we must understand two core principles:

1.  **Never, EVER store plain-text passwords.** If your database is ever compromised, all your users' passwords would be stolen. Instead, we store a **hash** of the password—a one-way cryptographic signature that cannot be reversed. When a user logs in, we hash the password they provide and compare it to the stored hash.
2.  **APIs should be stateless.** A server shouldn't have to remember who is logged in from one request to the next. After a user logs in, we give them a **JSON Web Token (JWT)**. This token is like a secure, self-contained passport. The user sends this token with every subsequent request. The server can instantly verify the token's signature to know who the user is without needing to look them up in a database session. .

🔑 **Transferable Skill**: This pattern of hashing passwords and using stateless tokens (like JWTs) is the universal standard for securing modern web and mobile APIs, regardless of the language or framework.

---

#### **🚩 Step 2: Setup & The User Model**

Let's install the libraries for hashing and for creating JWTs.

1.  **Install Libraries**:

    ```bash
    pip install "passlib[bcrypt]" "python-jose[cryptography]" "python-multipart"
    pip freeze > requirements.txt
    ```

    (`python-multipart` is needed for FastAPI to handle the OAuth2 form data).

2.  **Create the User Model**: We need a database table to store our users. Create `backend/models/user.py`:

    ```python
    # backend/models/user.py
    from sqlalchemy import Column, String, Boolean
    from database import Base

    class User(Base):
        __tablename__ = "users"

        username = Column(String, primary_key=True, index=True, unique=True)
        hashed_password = Column(String)
        is_admin = Column(Boolean, default=False)
    ```

    Remember to import this model in `main.py`'s startup event so the table gets created.

---

#### **🚩 Step 3: The Security Module**

It's best practice to keep all security-related helper functions in one place. Create `backend/security.py`:

```python
# backend/security.py
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# --- Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY", "a_super_secret_dev_key") # Use environment variables in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# --- JWT Creation ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

---

#### **🚩 Step 4: The Auth Endpoints**

We'll create a dedicated router for authentication to keep `main.py` clean. This introduces FastAPI's `APIRouter`.

Create `backend/routers/auth.py`:

```python
# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from security import verify_password, create_access_token
from crud import get_user
from database import get_db

router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await get_user(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

Now, include this router in `main.py`:

```python
# backend/main.py
from routers import auth # Import the router

# ... (app = FastAPI()) ...

app.include_router(auth.router, prefix="/auth", tags=["auth"]) # Include the router

# ... (rest of the API endpoints) ...
```

🔎 **Deep Explanation**: The `/token` endpoint is special. By depending on `OAuth2PasswordRequestForm`, FastAPI automatically creates an endpoint that expects a `x-www-form-urlencoded` body with `username` and `password` fields. This is part of the **OAuth2 standard** and makes your API compatible with many existing tools.

---

#### **🚩 Step 5: Protecting Our Endpoints**

This is the payoff. We'll create a dependency that requires a valid JWT and gives us the current user.

1.  **Add User CRUD functions** to `crud.py` to create and fetch users.

2.  **Create the dependency** in `security.py`:

    ```python
    # backend/security.py
    # ... (add these imports)
    from fastapi import Depends, HTTPException, status
    from fastapi.security import OAuth2PasswordBearer
    from crud import get_user
    from database import get_db
    from sqlalchemy.ext.asyncio import AsyncSession
    from models.user import User as UserModel

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

    async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
    ) -> UserModel:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user
    ```

3.  **Apply the dependency** to a protected route in `main.py`:

    ```python
    # backend/main.py
    from security import get_current_user
    from models.user import User as UserModel

    # Update the checkout endpoint
    @app.post("/api/files/{filename}/checkout", response_model=File)
    async def checkout_file(
        filename: str,
        db: AsyncSession = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
    ):
        # Now we know who the user is!
        return await git_service.checkout_file(db, filename, user=current_user.username)
    ```

Now, if you try to make a `POST` request to `/api/files/.../checkout` without a valid `Authorization: Bearer <token>` header, FastAPI will automatically reject it with a `401 Unauthorized` error.

---

#### **✅ Recap**

You have just implemented a complete, professional-grade authentication system. This is a massive step. You've learned:

- How to securely store user credentials using **password hashing**.
- The principles of **stateless API authentication** with **JSON Web Tokens (JWTs)**.
- How to implement the standard **OAuth2 password flow** for logging in.
- To organize code into layers using `APIRouter` and a dedicated `security` module.
- The power of **FastAPI's dependency injection** to create reusable security dependencies that protect your endpoints.

#### **📌 What's Next:**

Our application is now secure and multi-user. Now that we know _who_ our users are, we can build features that let them interact in real time. In **Part 13**, we will introduce **WebSockets** to broadcast events, allowing one user to see instantly when another user has locked or unlocked a file.
