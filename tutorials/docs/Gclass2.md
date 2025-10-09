# Step 2: Authentication – The Secure Handshake (Client-Server Trust – 1.5hr)

**Big Picture Goal**: Build login: JS form sends credentials, backend verifies/hashes with bcrypt, returns JWT token. Store/validate for "logged in" state. Understand **client-server trust** (request proof → server checks → token as receipt).

**Why Second?** (Layered Principle: **Defense in Depth – Secure Before Expose**). Shell clicks work; now protect with auth (no leaks). **Deep Dive**: Trust = "prove identity" (password hash) + "prove ongoing" (token). Why JWT? Self-contained (no DB per request)—scales for multiple users. Resource: [Auth0 JWT Basics](https://auth0.com/learn/json-web-tokens) – 4min, "Claims" section (payload = user info).

**When**: After shell—gate features. Use for any API (e.g., G-code upload: Auth before send).

**How**: JS FormData (safe POST), backend bcrypt (hash), JWT (token). Gotcha: Tokens expire—validate on load.

**Pre-Step**: Branch: `git checkout -b step-2-auth`. Add to header: `<button data-action="login">Login</button>`. Create simple modal in index.html:

```html
<div
  id="loginModal"
  class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center hidden z-50"
>
  <div class="bg-white p-6 rounded">
    <input
      id="loginUsername"
      placeholder="Username"
      class="block w-full mb-2 p-2 border"
    />
    <input
      id="loginPassword"
      type="password"
      placeholder="Password"
      class="block w-full mb-2 p-2 border"
    />
    <button data-action="submitLogin">Submit</button>
  </div>
</div>
```

---

## 2a: Client-Side State – Remembering the User (Persistence Basics)

**Question**: How do we "remember" login across refreshes? We need a spot for the token (login proof) and user name, without re-sending passwords.

**Micro-Topic 1: Simple Variables for In-Memory State**  
**Type This (create ui/auth.js)**:

```javascript
// auth.js - Holds login state. What: Two variables—one for proof (token), one for name.

let authToken = null; // Login "receipt"—starts empty.
let currentUser = null; // Who is logged in—starts unknown.
```

**Inline 3D Explain**:

- **What**: `let` = block-scoped variable (changeable). `null` = intentional "no value" (vs undefined = forget).
- **Why**: In-memory = instant access (no fetch). Separate token/user = SRP (token = security, user = display—change one, no ripple).
- **How**: Browser vars = current tab only. Gotcha: Refresh = reset—persistence next. **Alternative**: Const = unchangeable (bad for dynamic).

**Try This (10s)**: Console: `authToken = 'fake'; currentUser = 'test'; console.log(authToken, currentUser)` = "fake test"? Tweak: `let bad = 'wrong';` → TypeError if redeclare. Reflect: "Why separate vars? Bundle in object = good, but simple = clear for now."

**Inline Lens (SRP Integration)**: auth.js = state only (no fetch—next micro). Violate? Add UI here = fat file (test state alone? Hard).

**Mini-Summary**: Vars = quick in-memory hold. Null = "empty on purpose."

**Micro-Topic 2: Persistence with localStorage**  
**Type This (add to auth.js)**:

```javascript
authToken = localStorage.getItem("auth_token") || null; // Load or empty.
currentUser = localStorage.getItem("current_user") || null; // Same for user.
```

**Inline 3D Explain**:

- **What**: getItem = retrieve by key (string value).
- **Why**: Persistence = UX (refresh = stay logged). **Deep Dive**: localStorage = 5MB quota, sync (blocks if big, tokens tiny). Resource: [MDN localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) – 2min, "getItem example."
- **How**: || null = fallback (empty string = falsy). Gotcha: Only strings—JSON.parse for objects. **Alternative**: sessionStorage = tab-only (logout on close).

**Try This (15s)**: Console: `localStorage.setItem("auth_token", "fake123");` → Refresh → `localStorage.getItem("auth_token")` = "fake123"? Clear (`localStorage.clear()`) → null. Reflect: "Why getItem? Vars reset on refresh—storage = bridge."

**Inline Lens (DRY Integration)**: Load once (here), use everywhere (main.js imports). Violate? Load in every file = bugs on change.

**Mini-Summary**: localStorage = refresh-proof memory. getItem = restore.

**Git**: `git add auth.js && git commit -m "feat(step-2a): client auth state + persistence"`.

---

### 2b: Backend Auth – Hashing & Token Issuance (Server Verification)

**Question**: How does the server "trust" the password without storing plain text? We need hashing (scramble) + token (receipt).

**Micro-Topic 1: Simple Password Hashing with Bcrypt**  
**Type This (create backend/auth.py)**:

```python
# auth.py - Server auth. What: Hash = scramble password (one-way).

import bcrypt  # pip install bcrypt.

def hash_password(password: str) -> str:
  salt = bcrypt.gensalt()  // Random salt per hash.
  return bcrypt.hashpw(password.encode(), salt).decode()  // Bytes → string.
```

**Inline 3D Explain**:

- **What**: gensalt = random bits. hashpw = algorithm run.
- **Why**: Plain = leak disaster (DB hack = creds gone). **Deep Dive**: Salt = unique scramble (same pass = different hash). Resource: [Bcrypt Python](https://www.python-engineer.com/posts/bcrypt-for-python/) – 3min, "Salt why."
- **How**: encode/decode = bytes/string (bcrypt needs bytes). Gotcha: Same input = same output (for verify). **Alternative**: hashlib.sha256 = fast/bad (no salt = crackable).

**Try This (10s)**: `python backend/auth.py` (or console): `from auth import hash_password; print(hash_password("pass"))` → $2b$12$... ? Hash "pass" twice → different? Reflect: "Why salt? No salt = dictionary attack easy."

**Micro-Topic 2: Password Verification**  
**Type This (add to auth.py)**:

```python
def verify_password(plain: str, hashed: str) -> bool:
  return bcrypt.checkpw(plain.encode(), hashed.encode())  // Re-hash, match.
```

**Inline 3D Explain**:

- **What**: checkpw = input scramble + compare.
- **Why**: Verify without reverse (one-way = secure). **Deep Dive**: Auto-uses stored salt (no re-salt). Resource: [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) – 2min, "Bcrypt."
- **How**: encode both = fair compare. Gotcha: Wrong = False (no "why"). **Alternative**: == on plain = insane (no hash = no security).

**Try This (15s)**: Console: `hashed = hash_password("pass"); verify_password("pass", hashed)` → True? `verify_password("wrong", hashed)` → False? Reflect: "Why re-hash? Matches stored—proves knowledge without plain."

**Micro-Topic 3: JWT Token Generation**  
**Type This (add to auth.py)**:

```python
import jwt  # pip install pyjwt.
from datetime import datetime, timezone, timedelta

SECRET_KEY = "change-me-in-prod"  // Signing key—env var later.

def generate_token(username: str) -> str:
  payload = {"username": username, "exp": datetime.now(timezone.utc) + timedelta(hours=8)}
  return jwt.encode(payload, SECRET_KEY, algorithm="HS256")  // Sign = tamper-proof.
```

**Inline 3D Explain**:

- **What**: payload = claims dict. encode = base64(signed string).
- **Why**: Token = portable proof (decode = trust). **Deep Dive**: Exp = auto-kill (stolen = limited). Resource: [JWT.io](https://jwt.io) – 2min, paste token → decode.
- **How**: timezone.utc = no DST. Gotcha: Secret leak = fakes. **Alternative**: UUID = simple ID (stateful DB lookup).

**Try This (20s)**: Console: `token = generate_token("test"); print(token)` → eyJ... ? `jwt.decode(token, SECRET_KEY, algorithms=["HS256"])` → {'username': 'test', 'exp': ...}? Tweak: timedelta(minutes=1) → decode after 2min = expired error. Reflect: "Why payload? Embeds user—no extra fetch."

**Inline Lens (Security Integration)**: Hash + token = layered (hash = no plain, token = no re-check). Violate? Plain store = breach. Principle: Least Privilege (short exp = minimal access).

**Mini-Summary**: Bcrypt + JWT = trust chain. Hash verifies, token carries.

**Git**: `git add backend/auth.py && git commit -m "feat(step-2b): backend hashing + token"`.

---

### 2c: Client-Server Wiring – The Login Fetch

**Question**: How do we send form to backend? We need safe POST (password in body) + state update on success.

**Micro-Topic 1: Login Button & Modal Stub**  
**Type This (update ui/index.html header)**:

```html
<button data-action="login" class="bg-green-500 text-white px-4 py-2 rounded">
  Login
</button>
```

**Inline 3D Explain**:

- **What**: data-action = custom flag for delegation.
- **Why**: Intent = "login action" (decouples from text). **Deep Dive**: Data attrs = HTML5 standard (dataset in JS). Resource: [MDN Data Attr](https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes) – 2min, "Access."
- **How**: Closest finds it. Gotcha: No data = ignore. **Alternative**: class="login-btn" = works, but data = explicit.

**Try This (10s)**: Refresh → button? (No JS yet = no action.) Reflect: "Why data-action? Button rename = no JS change."

**Micro-Topic 2: Modal Overlay for Form**  
**Type This (add before `</body>` in index.html)**:

```html
<div
  id="loginModal"
  class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center hidden z-50"
>
  <div class="bg-white p-6 rounded shadow-lg">
    <input
      id="loginUsername"
      placeholder="Username"
      class="block w-full mb-2 p-2 border rounded"
    />
    <input
      id="loginPassword"
      type="password"
      placeholder="Password"
      class="block w-full mb-2 p-2 border rounded"
    />
    <button
      data-action="submitLogin"
      class="bg-blue-500 text-white px-4 py-2 rounded"
    >
      Submit
    </button>
  </div>
</div>
```

**Inline 3D Explain**:

- **What**: fixed/inset-0 = full-screen. hidden = start off.
- **Why**: Modal = focused (no page leave). **Deep Dive**: z-50 = layer (above shell). Resource: [MDN Modal](https://developer.mozilla.org/en-US/docs/Learn/Accessibility/HTML#building_modals) – 3min, "ARIA role."
- **How**: flex center = auto-pos. Gotcha: No hidden = always show. **Alternative**: Alert = blocking (bad UX).

**Try This (15s)**: Refresh → modal hidden? Tweak: Remove hidden → overlays? Add role="dialog" → screen reader "dialog." Reflect: "Why fixed? Scroll = modal moves—bad."

**Micro-Topic 3: Fetch POST with FormData**  
**Type This (add to ui/auth.js)**:

```javascript
export async function performLogin() {
  const username = document.getElementById("loginUsername").value;
  const password = document.getElementById("loginPassword").value;
  if (!username || !password) return showNotification("Fill fields", "error");

  const formData = new FormData(); // Package fields safely.
  formData.append("username", username);
  formData.append("password", password);

  try {
    const response = await fetch("/auth/login", {
      method: "POST",
      body: formData,
    });
    if (!response.ok) throw new Error("Login failed");
    const data = await response.json();
    setAuthState(data.token, data.username);
    document.getElementById("loginModal").classList.add("hidden");
    showNotification("Logged in!");
  } catch (error) {
    showNotification(error.message, "error");
  }
}
```

**Inline 3D Explain**:

- **What**: FormData = body builder. append = add pair.
- **Why**: POST body = secure (no URL log). **Deep Dive**: Multipart = auto-headers (boundary = field separator). Resource: [MDN FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) – 2min, "POST example."
- **How**: await = wait response. Gotcha: No body = GET. **Alternative**: JSON.stringify = text-only (no files).

**Try This (25s)**: Update main.js delegation: `case "login": document.getElementById("loginModal").classList.remove("hidden"); break; case "submitLogin": await performLogin(); break;`. Click Login → modal? Submit test/pass → notify "Logged in!", hidden? Mock fetch return {token: 'fake', username: 'test'} → state update? Tweak: Empty fields → "Fill fields." Reflect: "Why FormData? Password safe in body—URL = logged."

**Inline Lens (Async Integration)**: Await = "pause for result" (readable). Violate? .then chain = callback hell.

**Mini-Summary**: FormData + fetch = safe send. Await = clean flow.

**Git**: `git add index.html auth.js main.js && git commit -m "feat(step-2c): login form + fetch"`.

---

### 2d: Token Validation & Error Polish (Full Circle – Refresh Check)

**Question**: How do we check token on load (expired = relogin)? Add validation + better errors.

**Micro-Topic 1: Backend Validate Route**  
**Type This (add to backend/auth.py)**:

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

security = HTTPBearer()  // Extract header.

@router.post("/auth/validate")
async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
  try:
    payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
    return {"username": payload["username"]}
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token expired")
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=401, detail="Invalid token")
```

**Inline 3D Explain**:

- **What**: Depends = run first (gets token). decode = verify sig/exp.
- **Why**: Validate = fresh check (expiry = revoke). **Deep Dive**: HTTPBearer = auto-401 no header. Resource: [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) – 3min, "Bearer."
- **How**: algorithms = secure list. Gotcha: No try = crash. **Alternative**: Custom header parser = verbose.

**Try This (15s)**: Postman POST /auth/validate (Headers: Authorization Bearer fake) → 401? Real token → username? Tweak: Expired payload → "expired." Reflect: "Why Depends? Auto-wire token—route clean."

**Micro-Topic 2: Client Validation on Load**  
**Type This (add to ui/auth.js)**:

```javascript
export async function checkAuth() {
  if (!authToken) return false;
  try {
    const response = await fetch("/auth/validate", {
      headers: { Authorization: `Bearer ${authToken}` },
    });
    if (!response.ok) throw new Error("Invalid token");
    const data = await response.json();
    setAuthState(authToken, data.username);
    return true;
  } catch (error) {
    localStorage.removeItem("auth_token");
    showNotification("Session expired—login again", "error");
    return false;
  }
}
```

**Inline 3D Explain**:

- **What**: Bearer = standard header. throw = bubble error.
- **Why**: Check = "verify on start" (stale = relogin). **Deep Dive**: Clear on fail = "fail closed" (secure). Resource: [MDN Fetch Errors](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#supplying_request_options) – 2min, "Handling errors."
- **How**: headers = object. Gotcha: Offline = catch too. **Alternative**: No check = stale UI (user thinks logged).

**Try This (20s)**: Update main.js initApp: `if (await checkAuth()) showNotification("Welcome back!"); else showNotification("Please login");`. Login → refresh → "Welcome"? Junk token → clear + "expired." Tweak: Network off → error. Reflect: "Why clear? Bad token = security risk."

**Inline Lens (Error Handling Integration)**: Catch = "plan fail" (network/auth = same handler). Violate? Uncaught = crash tab.

**Mini-Summary**: Validate = trust refresh. Clear bad = secure default.

**Git**: `git add . && git commit -m "feat(step-2d): token validation + errors"`. Merge main—diff: "Clean additions?"

---

**Step 2 Complete!** Login full-stack. Reflect: "Flow: Click → modal → FormData POST → hash verify → token state → validate on load. SRP: auth.js = logic, main = wiring."

**Next**: Step 3: Config. Go? 🚀
