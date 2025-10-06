Perfect 👍 Let’s fully **rewrite Stage 6** into a real **teaching tutorial**, not just a “paste this code” section. We’ll integrate the **RBAC deep dive** and the **audit logging aside** you just liked. The style will be:

- **Tiny code increments** (5–10 lines)
- **Deep explanations** (from SE + CS + real-world perspective)
- **Tests** (so student confirms each step works)
- **Gotchas** (pitfalls & why professionals avoid them)

---

# **Stage 6: Real-World RBAC + Audit Logging**

> By now you have login, JWT tokens, and protected routes (Stage 5). But real apps need **granular permissions** and **audit trails**. This stage will make our app feel like something you’d see at a real company.

---

## **Step 1: Role Hierarchy Setup**

Let’s assign **levels** to roles so we can say “managers ≥ users, admins ≥ managers.”

```python
# database.py

users_db = {
    "admin": {"password": "<hashed_pw>", "role": "admin"},
    "manager": {"password": "<hashed_pw>", "role": "manager"},
    "alice": {"password": "<hashed_pw>", "role": "user"}
}

role_levels = {
    "user": 1,
    "manager": 2,
    "admin": 3
}
```

**Explanation:**

- We keep the user table **flat** (username → role).
- `role_levels` encodes hierarchy numerically.
- This avoids lots of “if role == …” branching.
- CS concept: mapping to integers → constant-time comparisons.
- SE principle: **separation of concerns** (data about users vs logic about hierarchy).

**Test:**

```bash
python -c "from database import role_levels; print(role_levels['admin'] > role_levels['user'])"
```

Output → `True`.

**Gotcha:**
Hardcoding roles works for now, but in production you’d store them in a DB table or RBAC policy file.

---

## **Step 2: Audit Logger**

Every **critical action** must be logged. Create a dedicated audit logger.

```python
# audit.py
import json
from datetime import datetime

LOG_FILE = "audit.log"

def log_event(user: str, action: str, resource: str, details: dict = None):
    """Append a structured audit log entry."""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "action": action,
        "resource": resource,
        "details": details or {}
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
```

**Explanation:**

- We use JSON lines → each log entry = one JSON object per line.
- This format is **machine-readable** (ELK, Splunk, SIEM tools love it).
- Append-only → satisfies **non-repudiation** (you can’t silently erase mistakes).
- App tie-in: PDM systems **must know who did what and when**.

**Test:**

```python
from audit import log_event
log_event("alice", "checkout", "file1.txt")
```

Check `audit.log` → should see JSON.

**Gotcha:**
Never use `print()` for logs in real apps → you’ll lose data. Always use structured logging.

---

## **Step 3: Lock Manager (Ownership)**

We need a system to **lock files** (checkout) and **release** them (checkin).

```python
# lock_manager.py
class LockManager:
    def __init__(self):
        self.locks = {}  # filename -> username

    def lock(self, filename: str, user: str) -> bool:
        if filename in self.locks:
            return False
        self.locks[filename] = user
        return True

    def unlock(self, filename: str, user: str) -> bool:
        if self.locks.get(filename) == user:
            del self.locks[filename]
            return True
        return False
```

**Explanation:**

- Dictionary → O(1) lookups for lock ownership.
- Only **owner** can unlock → enforces **ownership consistency**.
- This is how Perforce or ClearCase enforce “exclusive checkout.”

**Test:**

```python
from lock_manager import LockManager
lm = LockManager()
print(lm.lock("file1", "alice"))  # True
print(lm.unlock("file1", "bob"))  # False (bob doesn’t own it)
```

**Gotcha:**
If you forget the `get()` check, any user could unlock → breaking integrity.

---

## **Step 4: Force Unlock (Admin Override)**

Admins sometimes need to override (e.g., Alice went home and left file locked).

```python
# lock_manager.py (add method)
    def force_unlock(self, filename: str, admin: str) -> bool:
        if filename in self.locks:
            del self.locks[filename]
            return True
        return False
```

And log it:

```python
# main.py (snippet)
@app.post("/force-checkin")
def force_checkin(admin: str, filename: str):
    if lock_manager.force_unlock(filename, admin):
        log_event(admin, "force-checkin", filename, {"override": True})
        return {"message": f"{filename} forcibly unlocked by {admin}"}
    return {"error": "File not locked"}
```

**Explanation:**

- Force unlock = **break glass procedure**.
- Always logged with `{"override": True}` → so admins can’t hide misuse.
- In distributed systems, this is called a **consensus override**.

**Test:**
Lock file as Alice, then call `/force-checkin` as admin → check logs.

**Gotcha:**
Frontend should **hide** force-checkin for normal users, but backend must **enforce** it with role checks.

---

## **Step 5: Role-Protected Routes**

Now enforce roles.

```python
# main.py (snippet)
from fastapi import Depends, HTTPException, Header
from database import role_levels
from auth import decode_access_token

def role_required(min_role: str):
    def wrapper(authorization: str = Header(...)):
        token = authorization.split(" ")[1]
        payload = decode_access_token(token)
        if isinstance(payload, str):
            raise HTTPException(status_code=401, detail=payload)
        user_role = payload["role"]
        if role_levels[user_role] < role_levels[min_role]:
            raise HTTPException(status_code=403, detail=f"{min_role} required")
        return payload
    return wrapper

@app.get("/manager")
def manager_route(payload=Depends(role_required("manager"))):
    return {"message": f"Hello {payload['sub']}! You’re a manager."}
```

**Explanation:**

- Decorator pattern: `role_required("manager")` wraps the route.
- `role_levels` → simple numeric compare (user ≥ required?).
- This mimics AWS IAM policies, Kubernetes RBAC, etc.

**Test:**
Login as user → hit `/manager` → 403.
Login as manager → success.

**Gotcha:**
Don’t just hide UI buttons → always enforce backend checks.

---

## ✅ What You Learned in Stage 6

- **RBAC Hierarchy** → roles mapped to levels for easy checks.
- **Ownership Enforcement** → users can only unlock their own locks.
- **Admin Overrides** → allowed but always logged.
- **Audit Logging** → structured JSON logs → real-world observability.
- **Separation of Concerns** → user DB, locks, audit logs are distinct.

---

This makes your PDM app feel **enterprise-grade** — where actions are enforceable, traceable, and recoverable.

---

👉 Do you want me to **add frontend changes** here too (e.g., conditionally showing/hiding buttons based on role + wiring logs to UI), or keep Stage 6 backend-only for now?
