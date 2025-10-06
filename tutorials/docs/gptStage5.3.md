Perfect ✅ — let’s redo **Stage 5+ (Advanced Auth)** in the **micro-step, ground-up tutorial style**.

We’ll go **one tiny change at a time**, explain every line, and test as we go.

---

# 🔐 Stage 5+: Advanced Auth System

We already have:

- Login with JWT access tokens
- Password hashing with bcrypt
- Role stored per user

Now we’ll add **refresh tokens, logout, and role hierarchy** — the building blocks of a production system.

---

## 1️⃣ The Problem: Expiring Tokens

Right now, access tokens live **5 minutes**. That’s secure but bad UX — users get logged out constantly.

**Question:** How do real systems solve this?
**Answer:** With a second kind of token: a **refresh token**.

- Access token → short life (5–15 min), protects APIs.
- Refresh token → long life (days), used to get new access tokens.
- Store refresh tokens server-side → so we can revoke them on logout.

---

## 2️⃣ Create a Refresh Token Store

➡️ **Step: create a new file `token_store.py`**

```python
# token_store.py

# In-memory refresh token store
# Maps username -> list of active refresh tokens
refresh_tokens_db = {}
```

### Explanation:

- We’re starting **simple**: just a Python dictionary.
- Keys = usernames.
- Values = lists of active refresh tokens.
- In production, we’d use a DB or Redis — but a dict works for learning.

### Test it:

```bash
python
>>> import token_store
>>> token_store.refresh_tokens_db
{}
```

✅ Empty dict means it works.

---

## 3️⃣ Add Refresh Token Generator

➡️ Open `auth.py` and add:

```python
from datetime import timedelta, datetime
import jwt  # already used

REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_refresh_token(username: str):
    """Generate a refresh token valid for 7 days."""
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    token = jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return token
```

### Line-by-line:

- `REFRESH_TOKEN_EXPIRE_DAYS = 7` → refresh token lives longer than access tokens.
- `datetime.utcnow() + timedelta(...)` → calculate expiration date.
- `jwt.encode(...)` → create a signed token with:

  - `sub`: the username (subject).
  - `exp`: expiry time.

- Return it as a string.

### Test it:

```bash
python
>>> from auth import create_refresh_token
>>> token = create_refresh_token("alice")
>>> token
'eyJhbGciOiJIUzI1NiIs...'
```

✅ You got a token string.

---

## 4️⃣ Add Refresh Token Verifier

➡️ Still in `auth.py`:

```python
def verify_refresh_token(token: str):
    """Verify refresh token and return username if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return "Refresh token expired"
    except jwt.InvalidTokenError:
        return "Invalid refresh token"
```

### Line-by-line:

- `jwt.decode(...)` → checks signature + expiry.
- If expired → return string `"Refresh token expired"`.
- If invalid signature/format → return `"Invalid refresh token"`.
- Else → return the `sub` (username).

### Test it:

```bash
>>> from auth import create_refresh_token, verify_refresh_token
>>> t = create_refresh_token("bob")
>>> verify_refresh_token(t)
'bob'
```

✅ Works.
Now try:

```bash
>>> verify_refresh_token("not_a_token")
'Invalid refresh token'
```

---

## 5️⃣ Update Login Route

➡️ Open `main.py`, update `/login`:

```python
from token_store import refresh_tokens_db
from auth import create_refresh_token

@app.post("/login")
def login(user: User):
    db_user = users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        {"sub": user.username, "role": db_user["role"]},
        timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(user.username)

    # Store refresh token
    refresh_tokens_db.setdefault(user.username, []).append(refresh_token)

    return {"access_token": access_token, "refresh_token": refresh_token}
```

### Explanation:

- After login, we now generate **two tokens**.
- `refresh_tokens_db.setdefault(...)` → make sure the user has a list, then append the token.
- Return both in JSON.

### Test it:

```bash
curl -X POST http://127.0.0.1:8000/login -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "alicepw"}'
```

✅ Response should include both `access_token` and `refresh_token`.

---

## 6️⃣ Add Refresh Route

➡️ In `main.py`:

```python
from auth import verify_refresh_token

@app.post("/refresh")
def refresh(token: str):
    username = verify_refresh_token(token)
    if username in ["Refresh token expired", "Invalid refresh token"]:
        raise HTTPException(status_code=401, detail=username)
    if token not in refresh_tokens_db.get(username, []):
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    db_user = users_db[username]
    new_access = create_access_token(
        {"sub": username, "role": db_user["role"]},
        timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    )
    return {"access_token": new_access}
```

### Explanation:

- `verify_refresh_token` → decode + check expiry.
- If expired/invalid → reject.
- If not in `refresh_tokens_db` → means revoked, reject.
- Else → issue a new short-lived access token.

### Test it:

1. Login → save refresh token.
2. Wait for access token to expire.
3. Call refresh:

```bash
curl -X POST http://127.0.0.1:8000/refresh -H "Content-Type: application/json" \
  -d '{"token": "<refresh_here>"}'
```

✅ You get a new access token.

---

## 7️⃣ Add Logout (Revocation)

➡️ In `main.py`:

```python
@app.post("/logout")
def logout(token: str):
    username = verify_refresh_token(token)
    if username in ["Refresh token expired", "Invalid refresh token"]:
        raise HTTPException(status_code=401, detail=username)

    if token in refresh_tokens_db.get(username, []):
        refresh_tokens_db[username].remove(token)
    return {"message": "Logged out successfully"}
```

### Explanation:

- Verify token.
- If valid, remove it from store.
- Now it can’t be used to refresh again.

### Test it:

1. Login → get refresh token.
2. Logout with that token.
3. Try `/refresh` with the same token → should fail.

✅ Revocation works.

---

## 8️⃣ Add Role Hierarchy

➡️ In `database.py`:

```python
role_levels = {"user": 1, "manager": 2, "admin": 3}
```

➡️ In `main.py`:

```python
def role_required(min_role: str):
    def wrapper(authorization: str = Header(...)):
        token = authorization.split(" ")[1]
        payload = decode_access_token(token)
        if isinstance(payload, str):
            raise HTTPException(status_code=401, detail=payload)
        user_role = payload["role"]
        if role_levels[user_role] < role_levels[min_role]:
            raise HTTPException(status_code=403, detail=f"{min_role} access required")
        return payload
    return wrapper

@app.get("/manager")
def manager_route(payload=Depends(role_required("manager"))):
    return {"message": f"Hello {payload['sub']}! You have manager access."}
```

### Explanation:

- `role_levels` → simple integer ranking.
- `role_required(min_role)` → dependency factory.
- Checks if user’s role level >= required role.
- If not → `403 Forbidden`.

### Test it:

1. Login as `user` → call `/manager` → should fail.
2. Login as `manager` → call `/manager` → should succeed.

✅ Role hierarchy works.

---

## ✅ Wrap-up

We built:

- Refresh tokens (long-lived, revocable).
- Logout (remove refresh token).
- Role hierarchy (flexible authorization).

This now mirrors a **real-world auth system**.

---

👉 Do you want me to keep going like this for Stage 6 (incremental, line-by-line teaching), or do you want me to pause here and expand this Stage 5 tutorial with **side deep dives** (like JWT structure, why Redis is better, or how real-world RBAC works)?
