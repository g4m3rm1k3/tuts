# Step 2: Authentication – The Secure Handshake (Client-Server Trust – 1.5hr)

**Big Picture Goal**: Build the login system where the user enters a username and password in a popup form. The frontend sends those credentials to the backend, the backend checks them securely without storing the plain password, and if good, sends back a token that proves the user is logged in. The frontend saves that token so the user stays logged in even if they refresh the page. By the end, you'll see how the frontend and backend "handshake" to build trust, and how to keep that trust going.

**Why Second?** (Layered Principle: **Secure the Door Before Entering the House – Defense in Depth**). The shell from Step 1 is just the front door—now we add the lock (login) so only trusted users can see the files or settings inside. **Deep Dive**: Authentication is the "who are you?" step (password check), and the token is the "ID badge" that lets you in later without re-proving. Why start with this? It gates everything else—test it early to make sure the house is safe. Resource: [Mozilla Developer Network on Authentication Basics](https://developer.mozilla.org/en-US/docs/Learn/Server-side/First_steps/Website_security) – 4-minute read, focus on the "Passwords" section for why hashing matters.

**When**: Right after the shell—protect features like files or settings from the start. Use this pattern for any app that needs users, like a G-code uploader where only logged-in people can submit files.

**How**: The frontend uses a form to collect username and password, bundles them safely, and sends them to the backend. The backend scrambles the password (hashing) to check it without seeing the real one, then creates a token if good. The frontend saves the token in the browser's memory that survives page refreshes. Gotcha: Tokens can expire, so we check them on every page load to kick out old sessions.

**Pre-Step**: Branch: `git checkout -b step-2-auth`. Add a simple login button to the header in index.html: `<button data-action="login" class="bg-green-500 text-white px-4 py-2 rounded">Login</button>`.

Create a basic popup div before </body>:

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
    <button data-action="submitLogin">Submit</button>
  </div>
</div>
```

---

### 2a: Client-Side State – Remembering the User (Persistence Basics)

**Question**: How do we "remember" who the user is after they log in, so they don't have to type their username and password every time they refresh the page? We need a simple way to store the login proof (token) and the user's name in the browser.

**Micro-Topic 1: Simple Variables for In-Memory State**  
**Type This (create ui/auth.js)**:

```javascript
// auth.js - Holds login state. What: Two variables—one for proof (token), one for name.

let authToken = null; // Login "receipt"—starts empty.
let currentUser = null; // Who is logged in—starts unknown.
```

**Inline 3D Explain**:

- **What**: `let` = a variable you can change later. `null` = "nothing here yet" (better than undefined, which means "forgot").
- **Why**: These are like sticky notes in the browser's short-term memory—they hold the token (proof you're logged in) and user (who you are) while the page is open. Separate them because the token is for security checks, and the user is for display (like "Welcome, Bob"). **Deep Dive**: Variables in JavaScript are "block-scoped," meaning they only live inside their { } block, but here they're at the top of the file, so they're shared across the whole auth.js module. Resource: [MDN on Variables](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types#variables) – 2-minute read, the "let" section for why it's better than "var."
- **How**: `null` = intentional empty (check with if (authToken) = false). Gotcha: Refresh the page = these vars reset to null (we fix with storage next). **Alternative**: Use "const" = unchangeable (good for fixed, but login changes, so let).

**Try This (10s)**: Open the browser console (F12 > Console tab). Type `authToken = 'fake-token'; currentUser = 'test-user';` then `console.log(authToken, currentUser);` → "fake-token test-user". Tweak: Type `authToken = null;` → logs null. Reflect: "Why two vars? If one big object, changing token messes user—separate = clean."

**Inline Lens (Single Responsibility Principle Integration)**: auth.js = "login state only" (no UI or fetch yet—that's later). Violate it by adding a button here = the file does too many jobs (hard to test state alone).

**Mini-Summary**: Let vars = changeable memory for token/user. Null = start empty.

**Micro-Topic 2: Persistence with localStorage**  
**Type This (add right after the vars in ui/auth.js)**:

```javascript
authToken = localStorage.getItem("auth_token") || null; // Load or empty.
currentUser = localStorage.getItem("current_user") || null; // Same for user.
```

**Inline 3D Explain**:

- **What**: localStorage.getItem = pull value by key (returns string or null).
- **Why**: localStorage = "long-term memory" in the browser—it survives page refreshes or closes, so the user stays logged in. The || null = fallback if nothing stored (first time = empty). **Deep Dive**: It's a key-value store (like a tiny database), but strings only (5MB limit—plenty for tokens). Why not cookies? Cookies = server-sent (good for sessions), localStorage = client-set (easy for tokens). Resource: [MDN localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) – 2-minute read, the "getItem" example for loading.
- **How**: getItem("auth_token") = look up key. || = "or" fallback. Gotcha: It only works in the same domain (localhost = fine, prod = match URL). **Alternative**: sessionStorage = tab-only (close tab = logout)—localStorage = device-wide.

**Try This (15s)**: In console: `localStorage.setItem("auth_token", "fake-saved");` then refresh the page → `localStorage.getItem("auth_token")` = "fake-saved"? Clear with `localStorage.clear();` → null on refresh. Tweak: Set "current_user" = "bob" → loads on refresh. Reflect: "Why getItem? Vars reset on refresh—storage bridges the gap."

**Inline Lens (Don't Repeat Yourself Integration)**: Load once here, use everywhere (main.js imports getAuthState = no re-load). Violate it by loading in every file = bugs if one forgets.

**Mini-Summary**: localStorage.getItem + || = refresh-proof load. Fallback = safe start.

**Git**: `git add auth.js && git commit -m "feat(step-2a): client auth state + persistence"`.

---

### 2b: Backend Auth – Hashing & Token Issuance (Server Verification)

**Question**: How does the server "trust" the password the user sends without ever storing the plain text password? We need a way to scramble (hash) it safely and issue a token as proof if it matches.

**Micro-Topic 1: Simple Password Hashing with Bcrypt**  
**Type This (create backend/auth.py)**:

```python
# auth.py - Server auth. What: Hash = scramble password (one-way).

import bcrypt  # Install with pip install bcrypt.

def hash_password(password: str) -> str:
  salt = bcrypt.gensalt()  # Random salt per hash.
  hashed = bcrypt.hashpw(password.encode(), salt)  # Scramble with salt.
  return hashed.decode()  # String for storage.
```

**Inline 3D Explain**:

- **What**: gensalt = random bits added to password. hashpw = the scrambling algorithm using that salt.
- **Why**: Hashing turns "secret123" into gibberish like "$2b$12$..."—you can't unscramble to get the original, so even if hackers steal the database, they can't get passwords. The salt makes each hash unique (same password = different gibberish). **Deep Dive**: Bcrypt is "slow on purpose"—it takes milliseconds to hash, making brute-force attacks (try millions of guesses) impractical. Resource: [Python Bcrypt Guide](https://www.python-engineer.com/posts/bcrypt-for-python/) – 3-minute read, the "Salt" part explains why random bits matter.
- **How**: encode = turn string to bytes (bcrypt needs bytes). decode = back to string for saving. Gotcha: Same password always hashes the same way (with salt = unique). **Alternative**: Use Python's built-in hashlib.sha256 = fast but crackable (no salt/slow)—bcrypt = secure choice.

**Try This (10s)**: Terminal: `python -c "from auth import hash_password; print(hash_password('pass'))"` → "$2b$12$..." (different each run)? Hash 'pass' twice → different strings? Reflect: "Why salt? Without = same hash, hackers pre-crack common passwords."

**Inline Lens (Single Responsibility Principle Integration)**: hash_password = "scramble only" (no save or check—that's next micro). Violate it by adding file write here = the function does too much (hard to test scrambling alone).

**Mini-Summary**: Bcrypt hashpw + salt = safe scramble. encode/decode = bytes/string bridge.

**Micro-Topic 2: Password Verification (Matching)**  
**Type This (add to backend/auth.py)**:

```python
def verify_password(plain_password: str, hashed: str) -> bool:
  # What: Re-scramble input, compare to stored.
  return bcrypt.checkpw(plain_password.encode(), hashed.encode())
```

**Inline 3D Explain**:

- **What**: checkpw = take plain password, scramble with stored salt, see if matches stored hash.
- **Why**: Verification = "prove knowledge" without storing plain (re-scramble = same gibberish?). **Deep Dive**: The stored hash includes the salt, so checkpw auto-uses it—no need to separate. Resource: [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) – 2-minute read, the "Bcrypt" recommendation for why it's standard.
- **How**: encode both = fair compare (bytes). Gotcha: Wrong password = False (no "why"—secure, no leak). **Alternative**: Compare plain = stupid (store plain = hack = all creds gone).

**Try This (15s)**: Terminal: `python -c "from auth import hash_password, verify_password; h = hash_password('pass'); print(verify_password('pass', h)); print(verify_password('wrong', h))"` → True False? Tweak: Change 'pass' to 'wrong' in first = False. Reflect: "Why re-scramble? Proves 'you know it' without server knowing plain."

**Inline Lens (Don't Repeat Yourself Integration)**: verify = "check only" (no hash call—reuse hash func). Violate it by re-hashing in verify = dup code (change algorithm = fix two places).

**Mini-Summary**: checkpw = match without plain. encode = consistent scramble.

**Git**: `git add auth.py && git commit -m "feat(step-2b): backend hashing + verify"`.

---

### 2c: Client-Server Wiring – The Login Fetch

**Question**: How do we send the form (username/password) to the backend safely? We need a button to open the popup, and a submit to bundle and send the data.

**Micro-Topic 1: Login Button to Open Popup**  
**Type This (add to ui/index.html header after `<h1>`)**:

```html
<button
  data-action="login"
  class="bg-green-500 text-white px-4 py-2 rounded ml-4"
>
  Login
</button>
```

**Inline 3D Explain**:

- **What**: data-action="login" = flag for JS to catch. ml-4 = left margin (Tailwind).
- **Why**: Button = "start login" (delegation in main.js catches it). **Deep Dive**: data-action keeps HTML "dumb" (just intent)—JS = "smart" (how to login). Resource: [MDN Data Attributes](https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes) – 2-minute read, "Custom data for JavaScript."
- **How**: px-4 py-2 rounded = padding/rounded (Tailwind short). Gotcha: No data-action = click ignored. **Alternative**: class="login-btn" = works, but data-action = explicit ("action" = clear what it does).

**Try This (10s)**: Save and refresh. See green "Login" button? Inspect it → data-action="login" in attributes? Tweak: Change text to "Sign In" → button updates, data stays. Reflect: "Why data-action? Button rename = no JS change—intent separate from look."

**Inline Lens (Coupling Integration)**: Button = "what" (login intent), main.js = "how" (open popup). Violate with onclick="openLogin()" = button knows how (change popup = edit button).

**Mini-Summary**: data-action button = intent flag. Easy rename.

**Micro-Topic 2: Simple Popup Form for Credentials**  
**Type This (add before </body> in ui/index.html)**:

```html
<div
  id="loginModal"
  class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center hidden z-50"
>
  <div class="bg-white p-6 rounded shadow-lg w-80">
    <h3>Login</h3>
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
      class="bg-blue-500 text-white w-full p-2 rounded"
    >
      Submit
    </button>
  </div>
</div>
```

**Inline 3D Explain**:

- **What**: fixed inset-0 = full-screen overlay. hidden = start invisible. input = text fields.
- **Why**: Popup = focused input (no page leave for login). **Deep Dive**: z-50 = layer above (z-index = stack order). Resource: [MDN Fixed Positioning](https://developer.mozilla.org/en-US/docs/Web/CSS/position#fixed) – 2-minute read, "Full-screen overlay."
- **How**: flex items-center = center content. type="password" = dots for security. Gotcha: No hidden = always shows. **Alternative**: Page redirect to /login = loses state (popup = stay on page).

**Try This (15s)**: Save and refresh. Click Login → black overlay with form? Type in fields → text shows? Tweak: Remove hidden → popup always on (annoying). Reflect: "Why fixed inset-0? Scroll = popup moves—bad UX."

**Inline Lens (Separation of Concerns Integration)**: HTML = form structure, JS = show/hide (next). Violate with `<input onclick="submit">` = mixed (change JS = edit HTML).

**Mini-Summary**: Popup div + inputs = credential form. fixed = overlay.

**Git**: `git add index.html && git commit -m "feat(step-2c): login button + form popup"`.

---

### 2d: Sending Credentials – FormData and Fetch POST

**Question**: How do we bundle the username and password from the form and send them to the backend safely? We need a way to package the data and make the POST request.

**Micro-Topic 1: Reading Form Values in JS**  
**Type This (create ui/auth.js – add performLogin)**:

```javascript
export async function performLogin() {
  const username = document.getElementById("loginUsername").value; // What: Get input text.
  const password = document.getElementById("loginPassword").value; // Same for password.
  console.log("Sending:", username, password); // Test log (remove later).
}
```

**Inline 3D Explain**:

- **What**: getElementById = find by ID. value = current text.
- **Why**: Read = "collect user input" before send. **Deep Dive**: ID = unique (no dup finds). Resource: [MDN getElementById](https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementById) – 1-minute read, "Finding elements."
- **How**: .value = string always. Gotcha: Empty input = "" (check if (!username)). **Alternative**: querySelector(".username") = class, but ID = fast/specific.

**Try This (10s)**: Update main.js delegation: `case "submitLogin": await performLogin(); break;`. Click Submit → console "Sending: test pass"? Tweak: Empty fields → "" log. Reflect: "Why value? Input = elem, value = what's typed."

**Inline Lens (Error Handling Integration)**: Read = first guard (empty = early error). Violate? Send empty = backend crash.

**Mini-Summary**: getElementById.value = input read. Console = debug.

**Micro-Topic 2: Bundle with FormData for Safe Send**  
**Type This (add to performLogin)**:

```javascript
const formData = new FormData(); // What: Bundle for POST (text + files later).
formData.append("username", username); // Add key-value.
formData.append("password", password);
console.log("Bundled formData"); // Test.
```

**Inline 3D Explain**:

- **What**: new FormData = empty bundle. append = add pair (like dict).
- **Why**: FormData = "safe package" (password in body, not URL/logs). **Deep Dive**: Auto Content-Type multipart (separates fields with boundaries). Resource: [MDN FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects) – 2-minute read, "Appending."
- **How**: Key = backend expects (Form("username")). Gotcha: No append = empty body. **Alternative**: JSON.stringify({user, pass}) = text-only (no files).

**Try This (15s)**: Submit → "Bundled formData"? Tweak: append("test", "extra") → more keys. Reflect: "Why FormData? URL params = password in logs—body = hidden."

**Inline Lens (Security Integration)**: FormData body = POST secure (no URL expose). Violate with GET = creds leak.

**Mini-Summary**: FormData.append = bundled send. Key-value = backend match.

**Micro-Topic 3: Fetch POST to Backend**  
**Type This (add to performLogin)**:

```javascript
try {
  const response = await fetch("/auth/login", {
    // What: Send to endpoint.
    method: "POST", // Change from GET = mutate.
    body: formData, // Package.
  });
  console.log("Response:", response.status); // Test status.
} catch (error) {
  console.error("Send failed:", error); // Log fail.
}
```

**Inline 3D Explain**:

- **What**: fetch = request. method: "POST" = create/change.
- **Why**: POST = "send data to act" (login = verify). **Deep Dive**: Body = payload (FormData auto-types). Resource: [MDN Fetch POST](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#supplying_request_options) – 2-minute read, "POST body."
- **How**: await = wait response. Gotcha: No body = empty POST. **Alternative**: GET = read-only (no body).

**Try This (20s)**: Submit → console "Response: 200"? Backend mock return 200 → yes? Tweak: Change /auth/login to /wrong → error log. Reflect: "Why POST? GET = URL params = password visible in dev tools."

**Inline Lens (Async Integration)**: Await fetch = "pause for answer" (no nest). Violate? .then = callback hell (hard read).

**Mini-Summary**: Fetch POST body = data send. Await = clean wait.

**Git**: `git add auth.js main.js && git commit -m "feat(step-2d): login send + fetch"`.

---

**Step 2 Complete!** Login sends to backend. Reflect: "Full: Button open → read values → bundle FormData → POST fetch → log response. SRP: auth.js = send, main = wire."

**Next**: Step 3: Config. Go? 🚀
