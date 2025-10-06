Perfect! Let’s build a **full Stage 5 authentication mini-project** from scratch. I’ll explain every piece **line by line**, so you’ll understand both the code and the reasoning behind each step. We’ll include:

- User signup with **bcrypt password hashing**
- Login with JWT generation
- Protected routes that check JWT
- Role-based access control
- Token expiration handling

We’ll do it in **Python + FastAPI**, which is lightweight and beginner-friendly for backend development.

---

# **Stage 5 Mini Project: Authentication System**

### **1️⃣ Project Structure**

```
stage5_auth/
│
├─ main.py             # FastAPI app
├─ models.py           # Pydantic models (request/response schemas)
├─ auth.py             # Authentication helpers (hashing, JWT)
└─ database.py         # Simulated database
```

---

### **2️⃣ Step 1: Set up “database” (just a dict for now)**

```python
# database.py

# Simulate a user database
users_db = {}
```

**Explanation:**

- We’re using a Python dictionary to simulate a database for simplicity.
- Keys = usernames, Values = hashed passwords + role info.

---

### **3️⃣ Step 2: Models (Pydantic schemas)**

```python
# models.py
from pydantic import BaseModel

# User input for signup/login
class User(BaseModel):
    username: str
    password: str

# Response model
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

**Explanation:**

- `User` – validates login/signup input.
- `TokenResponse` – standard response for JWT login: token + type.

---

### **4️⃣ Step 3: Authentication Helpers**

```python
# auth.py
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super_secret_stage5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Create a JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Decode and verify JWT
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"
```

**Explanation:**

1. `hash_password` → bcrypt hash
2. `verify_password` → compare plaintext with hash
3. `create_access_token` → generate JWT, includes `exp`
4. `decode_access_token` → verify JWT and handle expiration

---

### **5️⃣ Step 4: Main FastAPI App**

```python
# main.py
from fastapi import FastAPI, HTTPException, Depends, Header
from models import User, TokenResponse
from auth import hash_password, verify_password, create_access_token, decode_access_token
from database import users_db
from datetime import timedelta

app = FastAPI(title="Stage 5 Auth System")

# Signup route
@app.post("/signup")
def signup(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = hash_password(user.password)
    users_db[user.username] = {"password": hashed, "role": "user"}
    return {"message": "User created successfully"}

# Login route
@app.post("/login", response_model=TokenResponse)
def login(user: User):
    db_user = users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username, "role": db_user["role"]})
    return {"access_token": token}

# Protected route
@app.get("/protected")
def protected_route(authorization: str = Header(...)):
    token = authorization.split(" ")[1]  # Expect "Bearer <token>"
    payload = decode_access_token(token)
    if isinstance(payload, str):
        raise HTTPException(status_code=401, detail=payload)
    return {"message": f"Hello {payload['sub']}, your role is {payload['role']}"}

# Admin-only route
@app.get("/admin")
def admin_route(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if isinstance(payload, str):
        raise HTTPException(status_code=401, detail=payload)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"message": f"Welcome Admin {payload['sub']}"}
```

**Explanation Line by Line:**

1. **Signup**

   - Check if user exists
   - Hash password with bcrypt
   - Save to “database” with role info

2. **Login**

   - Fetch user from database
   - Verify password
   - Generate JWT with `sub` (username) and `role`

3. **Protected route**

   - Extract token from `Authorization` header
   - Decode JWT
   - Check if valid / expired
   - Return user info

4. **Admin route**

   - Same as protected
   - Additionally check role → only admin allowed

---

### **6️⃣ Step 5: Mini Experiments**

1. Signup a user and login → get JWT
2. Call `/protected` with token → should succeed
3. Call `/protected` after 5 minutes → should fail (`Token expired`)
4. Call `/admin` as normal user → should fail (`Admin access required`)
5. Modify JWT payload manually → decoding fails → ensures token integrity

---

✅ **Key Learning Points**

- Passwords never stored in plaintext → use **bcrypt**
- JWT tokens carry user info → **stateless authentication**
- Expiration ensures **short-lived access**
- Role-based access can be enforced in backend
- Protect all routes → always verify JWT and roles

---

If you want, I can make a **next-level version** where we add:

- **Refresh tokens**
- **Role hierarchy**
- **Token revocation / logout system**

It would be a full Stage 5 authentication system like real-world production.

Do you want me to do that next?
