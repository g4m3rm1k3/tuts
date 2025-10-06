# PDM Tutorial - Stage 8: Hybrid Architecture - GitLab Integration for Both Modes (Part 3: Complete Test Script)

**Continuing from Part 2**: You've got encrypted PAT storage (test: encrypt/decrypt matches), GitLab-aware UserService (auto-register on PAT login), messaging service (send/get/mark/read/delete). Test: Login with PAT → Users in GitLab users.json (encrypted), send message → messages.json appends.
**Time for Part 3**: 2-3 hours
**What you'll build (Part 3)**: Frontend GitLab login tab, messaging panel/UI (slide-in, unread badge), config manager (YAML/env), PyInstaller spec/build script, full TESTING.md with e2e scripts. _Incremental_: One tab/event/build step, test login/exe. **Tailwind**: Yes—login tabs (`flex border-b-2`), message list (`flex flex-col gap-3`), badge (`bg-danger px-2 py-1 rounded-full text-xs font-bold`).

This wraps Stage 8 with a **complete test script** (bash + pytest)—run to verify hybrid modes.

---

### 8.11: Frontend - GitLab Login UI (Tabs Incremental)

**Step 1: Add Tabs Structure to login.html**
In <body> after header/error:

```html
<div class="login-tabs flex gap-2 mb-6 border-b-2 border-default">
  # NEW: Tailwind tabs
  <button
    class="tab-button active flex-1 p-3 bg-none border-none border-b-3 border-transparent text-secondary font-medium cursor-pointer transition-all"
    data-tab="password"
  >
    Password
  </button>
  # NEW
  <button
    class="tab-button flex-1 p-3 bg-none border-none border-b-3 border-transparent text-secondary font-medium cursor-pointer transition-all"
    data-tab="gitlab"
  >
    GitLab Token
  </button>
</div>
<!-- Password Tab (existing form) -->
<div id="password-tab" class="tab-content active">
  # NEW class
  <!-- Existing form -->
</div>
<!-- GitLab Tab (NEW) -->
<div id="gitlab-tab" class="tab-content">
  <div class="info-box bg-info/10 text-info p-3 rounded mb-4 text-sm">
    # NEW: Tailwind Login with GitLab PAT.
    <a
      href="https://gitlab.com/-/profile/personal_access_tokens"
      target="_blank"
      class="underline font-semibold"
      >Generate →</a
    >
  </div>
  <form id="gitlab-login-form">
    <div class="mb-5">
      <label
        for="gitlab-username"
        class="block mb-2 font-medium text-primary text-sm"
        >GitLab Username</label
      >
      <input
        type="text"
        id="gitlab-username"
        name="username"
        required
        class="w-full p-3 border border-default rounded bg-primary text-primary"
        placeholder="your-gitlab-username"
      />
    </div>
    <div class="mb-5">
      <label
        for="gitlab-token"
        class="block mb-2 font-medium text-primary text-sm"
        >Personal Access Token</label
      >
      <input
        type="password"
        id="gitlab-token"
        name="token"
        required
        class="w-full p-3 border border-default rounded bg-primary text-primary"
        placeholder="glpat-xxxx..."
      />
      <small class="text-secondary text-xs"
        >Scopes: api, read_repository, write_repository</small
      >
    </div>
    <button
      type="submit"
      class="w-full bg-primary text-inverse py-2 rounded hover:bg-primary-600"
    >
      Login with GitLab
    </button>
  </form>
</div>
```

- **Explanation**: flex gap-2 = tabs row (Tailwind). data-tab = JS hook. info-box = callout (app: guidance).
- **Test**: /login → Tabs + GitLab form.
- **Gotcha**: active class = selected state.

**Step 2: Add Tab Switching JS**
In login.js, after password submit:

```javascript
document.querySelectorAll(".tab-button").forEach((button) => {  # NEW
  button.addEventListener("click", () => {  # NEW
    const tabName = button.dataset.tab;
    document.querySelectorAll(".tab-button").forEach((b) => b.classList.remove("active", "border-primary", "text-primary"));
    button.classList.add("active", "border-primary", "text-primary");  # NEW: Style
    document.querySelectorAll(".tab-content").forEach((content) => content.classList.remove("active"));
    document.getElementById(`${tabName}-tab`).classList.add("active");
    document.getElementById("error-message").classList.remove("show");
  });
});
```

- **Explanation**: querySelectorAll = NodeList (CS: selector engine). classList = manip (add/remove/toggle).
- **Test**: Click tab—switches, clears error.
- **Gotcha**: dataset.tab = custom attr.

**Step 3: Add GitLab Submit Handler**
Add after password:

```javascript
document.getElementById("gitlab-login-form").addEventListener("submit", async (e) => {  # NEW
  e.preventDefault();
  const username = document.getElementById("gitlab-username").value;
  const token = document.getElementById("gitlab-token").value;
  const errorDiv = document.getElementById("error-message");
  const submitBtn = e.target.querySelector('button[type="submit"]');
  errorDiv.classList.remove("show");
  submitBtn.disabled = true;
  submitBtn.textContent = "Authenticating...";
  try {
    const formData = new URLSearchParams();  # NEW
    formData.append("username", username);
    formData.append("gitlab_token", token);
    const response = await fetch("/api/auth/login-gitlab", {  # NEW endpoint
      method: "POST",
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "GitLab failed");
    localStorage.setItem("access_token", data.access_token);
    const payload = JSON.parse(atob(data.access_token.split(".")[1]));
    localStorage.setItem("username", payload.sub);
    localStorage.setItem("user_role", payload.role);
    sessionStorage.setItem("gitlab_token", token);  # NEW: Temp for ops
    window.location.href = "/";
  } catch (error) {
    errorDiv.textContent = error.message;
    errorDiv.classList.add("show");
    submitBtn.disabled = false;
    submitBtn.textContent = "Login with GitLab";
  }
});
```

- **Explanation**: URLSearchParams = form encode (app: OAuth-like). sessionStorage = tab-only (CS: scoped storage).
- **Test**: /docs POST to /api/auth/login-gitlab → Token. JS submit → Redirects.
- **Gotcha**: sessionStorage = not persist across tabs (use for temp token).

**Step 4: Update main.py for /login-gitlab**
Add route:

```python
@app.post("/api/auth/login-gitlab", response_model=Token)  # NEW: In auth.py, but serve in main if needed
```

No—already in auth.py from Part 2. Test /login → Tabs work, GitLab submit calls endpoint.

**Full login.html** (End of Section—Verify):

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Login - PDM System</title>
    <link rel="stylesheet" href="/static/css/main.css" />
    <style>
      /* ... existing from previous */
    </style>
  </head>
  <body
    class="flex items-center justify-center min-h-screen bg-gradient-to-br from-primary-500 to-primary-700"
  >
    <div class="bg-card p-8 rounded-lg shadow-xl w-11/12 max-w-md border">
      <div class="text-center mb-6">
        <h1 class="text-4xl font-bold text-primary mb-2">PDM System</h1>
        <p class="text-inverse">Parts Data Management</p>
      </div>
      <div class="login-tabs flex gap-2 mb-6 border-b-2 border-default">
        <button
          class="tab-button active flex-1 p-3 bg-none border-none border-b-3 border-transparent text-secondary font-medium cursor-pointer transition-all"
          data-tab="password"
        >
          Password
        </button>
        <button
          class="tab-button flex-1 p-3 bg-none border-none border-b-3 border-transparent text-secondary font-medium cursor-pointer transition-all"
          data-tab="gitlab"
        >
          GitLab Token
        </button>
      </div>
      <div
        id="error-message"
        class="bg-danger/10 text-danger p-3 rounded mb-4 text-sm hidden"
      ></div>
      <div id="password-tab" class="tab-content active">
        <form id="password-login-form">
          <div class="mb-5">
            <label
              for="password-username"
              class="block mb-2 font-medium text-primary text-sm"
              >Username</label
            >
            <input
              type="text"
              id="password-username"
              name="username"
              required
              class="w-full p-3 border border-default rounded bg-primary text-primary"
              autofocus
              autocomplete="username"
            />
          </div>
          <div class="mb-5">
            <label
              for="password-password"
              class="block mb-2 font-medium text-primary text-sm"
              >Password</label
            >
            <input
              type="password"
              id="password-password"
              name="password"
              required
              class="w-full p-3 border border-default rounded bg-primary text-primary"
              autocomplete="current-password"
            />
          </div>
          <button
            type="submit"
            class="w-full bg-primary text-inverse py-2 rounded hover:bg-primary-600"
          >
            Login
          </button>
        </form>
      </div>
      <div id="gitlab-tab" class="tab-content">
        <div class="info-box bg-info/10 text-info p-3 rounded mb-4 text-sm">
          Login with GitLab PAT.
          <a
            href="https://gitlab.com/-/profile/personal_access_tokens"
            target="_blank"
            class="underline font-semibold"
            >Generate →</a
          >
        </div>
        <form id="gitlab-login-form">
          <div class="mb-5">
            <label
              for="gitlab-username"
              class="block mb-2 font-medium text-primary text-sm"
              >GitLab Username</label
            >
            <input
              type="text"
              id="gitlab-username"
              name="username"
              required
              class="w-full p-3 border border-default rounded bg-primary text-primary"
              placeholder="your-gitlab-username"
              autocomplete="username"
            />
          </div>
          <div class="mb-5">
            <label
              for="gitlab-token"
              class="block mb-2 font-medium text-primary text-sm"
              >Personal Access Token</label
            >
            <input
              type="password"
              id="gitlab-token"
              name="token"
              required
              class="w-full p-3 border border-default rounded bg-primary text-primary"
              placeholder="glpat-xxxx..."
            />
            <small class="text-secondary text-xs"
              >Scopes: api, read_repository, write_repository</small
            >
          </div>
          <button
            type="submit"
            class="w-full bg-primary text-inverse py-2 rounded hover:bg-primary-600"
          >
            Login with GitLab
          </button>
        </form>
      </div>
      <div
        class="demo-credentials mt-6 pt-6 border-t border-default text-center text-sm text-secondary"
      >
        <p><strong>Demo:</strong> admin/Admin123! or john/Password123!</p>
      </div>
    </div>
    <script type="module" src="/static/js/login.js"></script>
  </body>
</html>
```

**Full login.js** (End of Section—Verify):

```javascript
/**
 * Login Page Logic
 */
document.querySelectorAll(".tab-button").forEach((button) => {
  button.addEventListener("click", () => {
    const tabName = button.dataset.tab;
    document
      .querySelectorAll(".tab-button")
      .forEach((b) =>
        b.classList.remove("active", "border-primary", "text-primary")
      );
    button.classList.add("active", "border-primary", "text-primary");
    document
      .querySelectorAll(".tab-content")
      .forEach((content) => content.classList.remove("active"));
    document.getElementById(`${tabName}-tab`).classList.add("active");
    document.getElementById("error-message").classList.remove("show");
  });
});

document
  .getElementById("password-login-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("password-username").value;
    const password = document.getElementById("password-password").value;
    const errorDiv = document.getElementById("error-message");
    const submitBtn = e.target.querySelector('button[type="submit"]');
    errorDiv.classList.remove("show");
    submitBtn.disabled = true;
    submitBtn.textContent = "Logging in...";
    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
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

document
  .getElementById("gitlab-login-form")
  .addEventListener("submit", async (e) => {
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
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "GitLab failed");
      localStorage.setItem("access_token", data.access_token);
      const payload = JSON.parse(atob(data.access_token.split(".")[1]));
      localStorage.setItem("username", payload.sub);
      localStorage.setItem("user_role", payload.role);
      sessionStorage.setItem("gitlab_token", token);
      window.location.href = "/";
    } catch (error) {
      errorDiv.textContent = error.message;
      errorDiv.classList.add("show");
      submitBtn.disabled = false;
      submitBtn.textContent = "Login with GitLab";
    }
  });
```

**Verification**: /login → Tabs switch. Password login → Redirect. GitLab tab submit → Calls /login-gitlab, stores session token.

### 8.12: Frontend - Messaging UI (Panel Incremental)

**Step 1: Add Messages Button to Header**
In index.html .header-actions:

```html
<button
  id="messages-toggle"
  class="btn btn-secondary btn-sm relative"
  title="Messages"
>
  # NEW <span class="sr-only">Messages</span>📨
  <span
    id="message-badge"
    class="absolute -top-2 -right-2 bg-danger text-inverse text-xs rounded-full px-1.5 py-0.5 min-w-[20px] text-center hidden"
    >0</span
  >
  # NEW badge
</button>
```

- **Explanation**: relative/absolute = badge position (Tailwind). sr-only = a11y label.
- **Test**: Button with icon/badge (hidden).
- **Gotcha**: min-w = square badge.

**Step 2: Add Messages Panel**
Before </body>:

```html
<div
  id="messages-panel"
  class="fixed top-0 right-0 w-96 h-full bg-card shadow-xl border-l border-default z-modal transform translate-x-full transition-transform duration-300 flex flex-col"
>
  # NEW Tailwind slide
  <div
    class="p-4 border-b border-default flex justify-between items-center bg-secondary"
  >
    # Header
    <h3 class="m-0 text-primary">Messages</h3>
    <button
      class="text-secondary text-xl hover:text-primary"
      id="close-messages"
    >
      &times;
    </button>
  </div>
  <button
    class="mx-4 mt-4 w-full bg-primary text-inverse py-2 rounded hover:bg-primary-600"
    id="new-message-btn"
  >
    ✉️ New Message
  </button>
  # New btn
  <div class="flex-1 overflow-y-auto p-4">
    # Body
    <div id="messages-list"></div>
  </div>
</div>
```

- **Explanation**: translate-x-full = off-screen (transition = slide). flex-1 = grow (fills height).
- **Test**: Add .open (translate-x-0)—panel slides in.
- **Gotcha**: z-modal = over other (from tokens).

**Step 3: Add New Message Modal**
Add:

```html
<div id="new-message-modal" class="modal-overlay hidden">
  # NEW
  <div class="modal-content max-w-md">
    # Compact
    <div class="modal-header">
      <h3>New Message</h3>
      <button class="modal-close">&times;</button>
    </div>
    <div class="modal-body">
      <form id="new-message-form" class="space-y-4">
        # Tailwind space
        <div>
          <label
            for="message-to"
            class="block mb-2 font-medium text-primary text-sm"
            >To</label
          >
          <input
            type="text"
            id="message-to"
            name="to_user"
            required
            class="w-full p-3 border border-default rounded bg-primary text-primary"
            placeholder="username or 'all'"
          />
        </div>
        <div>
          <label
            for="message-subject"
            class="block mb-2 font-medium text-primary text-sm"
            >Subject</label
          >
          <input
            type="text"
            id="message-subject"
            name="subject"
            required
            class="w-full p-3 border border-default rounded bg-primary text-primary"
            maxlength="200"
          />
        </div>
        <div>
          <label
            for="message-body"
            class="block mb-2 font-medium text-primary text-sm"
            >Message</label
          >
          <textarea
            id="message-body"
            name="body"
            required
            rows="6"
            class="w-full p-3 border border-default rounded bg-primary text-primary"
            maxlength="5000"
          ></textarea>
        </div>
        <div>
          <label
            for="message-file"
            class="block mb-2 font-medium text-primary text-sm"
            >Related File</label
          >
          <input
            type="text"
            id="message-file"
            name="related_file"
            class="w-full p-3 border border-default rounded bg-primary text-primary"
            placeholder="PN1001.mcam"
          />
        </div>
        <div class="modal-actions flex gap-3 justify-end mt-6">
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

- **Explanation**: space-y-4 = vertical rhythm (Tailwind). rows=6 = height.
- **Test**: Open—form with labels/inputs.

**Step 4: Add View Message Modal**
Add:

```html
<div id="view-message-modal" class="modal-overlay hidden">
  # NEW
  <div class="modal-content max-w-lg">
    # Medium
    <div class="modal-header">
      <h3 id="view-message-subject" class="text-primary"></h3>
      <button class="modal-close">&times;</button>
    </div>
    <div class="modal-body p-6">
      <div class="mb-4 space-y-1 text-sm text-secondary">
        # Meta
        <div><strong>From:</strong> <span id="view-message-from"></span></div>
        <div><strong>Date:</strong> <span id="view-message-date"></span></div>
        <div id="view-message-file-info"></div>
      </div>
      <div
        id="view-message-body"
        class="whitespace-pre-wrap text-primary"
      ></div>
      # Body
      <div class="modal-actions flex gap-3 justify-end mt-6">
        <button class="btn btn-danger" id="delete-message-btn">Delete</button>
        <button class="btn btn-secondary" onclick="viewMessageModal.close()">
          Close
        </button>
      </div>
    </div>
  </div>
</div>
```

- **Explanation**: whitespace-pre-wrap = preserve formatting (app: message text). space-y-1 = meta lines.
- **Test**: Open—empty body/meta.

**Step 5: Add Panel CSS**
In input.css @layer components:

```css
@layer components {
  .messages-panel {
    @apply fixed top-0 right-0 w-96 h-full bg-card shadow-xl border-l border-default z-modal transform translate-x-full transition-transform duration-300 flex flex-col;
  }
  .messages-panel.open {
    @apply translate-x-0;
  }
  .messages-header {
    @apply p-4 border-b border-default flex justify-between items-center bg-secondary;
  }
  .messages-header h3 {
    @apply m-0 text-primary;
  }
  .messages-body {
    @apply flex-1 overflow-y-auto p-4;
  }
  .new-message-button {
    @apply mx-4 mt-4 w-full bg-primary text-inverse py-2 rounded hover:bg-primary-600;
  }
  .message-list {
    @apply flex flex-col gap-3;
  }
  .message-item {
    @apply p-4 border border-default rounded-md cursor-pointer transition-all;
  }
  .message-item:hover {
    @apply -translate-x-1 shadow-sm;
  }
  .message-item.unread {
    @apply border-l-4 border-primary bg-primary/10;
  }
  .message-from {
    @apply font-semibold text-primary mb-1;
  }
  .message-subject {
    @apply text-base text-primary mb-2;
  }
  .message-preview {
    @apply text-sm text-secondary overflow-hidden text-ellipsis whitespace-nowrap;
  }
  .message-time {
    @apply text-xs text-tertiary mt-2;
  }
  .message-badge {
    @apply absolute -top-2 -right-2 bg-danger text-inverse text-xs rounded-full px-1.5 py-0.5 min-w-[20px] text-center hidden;
  }
  .messages-empty {
    @apply text-center p-8 text-secondary;
  }
  .compose-form {
    @apply p-4;
  }
  .compose-form .form-group {
    @apply mb-4;
  }
}
```

Rebuild tailwind.css.

- **Explanation**: translate-x-full = off (open = 0). unread border-l-4 = highlight.
- **Test**: .open on panel—slides, styled messages.
- **Gotcha**: duration-300 = transition time.

**Full index.html** (End of Section—Verify):
[Full with messages button/panel/modals, Tailwind classes]

### 8.13: Frontend - Messaging JavaScript (Handlers Incremental)

**Step 1: Add Instances & Toggle**
In app.js after modals:

```javascript
const newMessageModal = new ModalManager("new-message-modal");  # NEW
const viewMessageModal = new ModalManager("view-message-modal");
let currentViewMessage = null;

function toggleMessagesPanel() {  # NEW
  const panel = document.getElementById("messages-panel");
  panel.classList.toggle("open");
  if (panel.classList.contains("open")) loadMessages();
}
```

- **Explanation**: Toggle class = CSS slide (revisit Stage 2 transitions).
- **Test**: Click button—panel opens/closes, calls load.

**Step 2: Add loadMessages (Fetch)**
Add:

```javascript
async function loadMessages() {  # NEW
  const container = document.getElementById("messages-list");
  container.innerHTML = '<div class="loading text-center py-8 text-secondary">Loading...</div>';
  try {
    const data = await apiClient.getMessages();  # NEW
    if (data.length === 0) {
      container.innerHTML = '<div class="messages-empty">No messages yet.</div>';
      return;
    }
    container.innerHTML = data.map((msg) => createMessageElement(msg)).join("");
    data.forEach((msg) => {  # NEW wire
      const el = document.getElementById(`message-${msg.id}`);
      if (el) el.onclick = () => viewMessage(msg);
    });
  } catch (error) {
    container.innerHTML = `<div class="messages-empty text-danger text-center py-8">Error: ${error.message}</div>`;
  }
}
```

- **Add to api-client.js**:
  ```javascript
  async getMessages() { return this.get('/api/messages'); }
  ```
- **Explanation**: Map = transform (CS: functor). forEach wire = delegation.
- **Test**: loadMessages() → Styled list, click opens view (stub).

**Step 3: Add createMessageElement**
Add:

```javascript
function createMessageElement(message) {  # NEW
  const date = new Date(message.timestamp);
  const isUnread = !message.read;
  return `
    <div class="message-item p-4 border border-default rounded-md cursor-pointer transition-all ${isUnread ? 'border-l-4 border-primary bg-primary/10' : ''}" id="message-${message.id}">
      <div class="message-from font-semibold text-primary mb-1">${message.from_user === 'all' ? '📢 Broadcast' : '👤 ' + message.from_user}</div>
      <div class="message-subject text-base text-primary mb-2">${escapeHtml(message.subject)}</div>
      <div class="message-preview text-sm text-secondary overflow-hidden text-ellipsis whitespace-nowrap">${escapeHtml(message.body.substring(0, 100))}...</div>
      <div class="message-time text-xs text-tertiary mt-2">${date.toLocaleString()}</div>
    </div>
  `;
}
function escapeHtml(text) {  # NEW util
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
```

- **Explanation**: Escape = XSS prevent (SE: security). text-ellipsis = truncate.
- **Test**: Render—unread highlighted.

**Step 4: Add viewMessage**
Add:

```javascript
async function viewMessage(message) {  # NEW
  currentViewMessage = message;
  document.getElementById("view-message-subject").textContent = message.subject;
  document.getElementById("view-message-from").textContent = message.from_user;
  document.getElementById("view-message-date").textContent = new Date(message.timestamp).toLocaleString();
  document.getElementById("view-message-file-info").innerHTML = message.related_file ? `<strong>Related:</strong> ${message.related_file}<br>` : '';
  document.getElementById("view-message-body").textContent = message.body;
  viewMessageModal.open();
  if (!message.read) {  # NEW
    try {
      await apiClient.markMessageRead(message.id);
      loadMessages();  # Refresh
    } catch (e) {
      console.error(e);
    }
  }
}
```

- **Add to api-client.js**:
  ```javascript
  async markMessageRead(messageId) { return this.post(`/api/messages/${messageId}/mark-read`); }
  ```
- **Explanation**: textContent = safe (no HTML). Await mark = optimistic (CS: eventual).
- **Test**: Click message—modal, marks read, refreshes.

**Step 5: Add sendNewMessage & delete**
Add:

```javascript
document.getElementById("new-message-form").addEventListener("submit", sendNewMessage);  # Wire in init
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
    await apiClient.sendMessage(data);  # NEW
    toast.success("Message sent!");
    newMessageModal.close();
    loadMessages();
  } catch (error) {
    toast.error(error.message);
  }
}
document.getElementById("delete-message-btn").addEventListener("click", deleteCurrentMessage);  # Wire
async function deleteCurrentMessage() {  # NEW
  if (!currentViewMessage || !confirm("Delete?")) return;
  try {
    await apiClient.deleteMessage(currentViewMessage.id);  # NEW
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
- **Explanation**: FormData = easy parse (JS: API). Confirm = consent (SE: UX safety).
- **Test**: New message → Sends, refreshes. Delete → Removes.

**Step 6: Add updateUnreadCount (Poll)**
Add in DOMContentLoaded:

```javascript
updateUnreadCount();  # NEW
setInterval(updateUnreadCount, 30000);  # Poll
```

Add:

```javascript
async function updateUnreadCount() {  # NEW
  try {
    const data = await apiClient.getUnreadCount();  # NEW
    const badge = document.getElementById("message-badge");
    badge.textContent = data.unread_count;
    badge.style.display = data.unread_count > 0 ? "block" : "none";
  } catch (e) {
    console.error(e);
  }
}
```

- **Add to api-client.js**:
  ```javascript
  async getUnreadCount() { return this.get('/api/messages/unread-count'); }
  ```
- **Explanation**: setInterval = poll (CS: heartbeat). Block/none = conditional display.
- **Test**: Send unread—badge shows, ticks down.

**Full app.js** (End of Section—Verify):
[Full with messaging functions, Tailwind in HTML, poll]

**Verification**: Toggle panel → Loads messages. Send → Appends. Badge updates.

### 8.14: Configuration Manager (YAML Incremental)

**Step 1: Create config_manager.py**

```bash
touch backend/app/config_manager.py
```

Paste:

```python
import yaml  # NEW: Parse
from pathlib import Path  # NEW
from typing import Optional, Dict  # NEW

DEFAULT_CONFIG = {  # NEW: Fallback
    'mode': 'server',
    'gitlab': {'enabled': True, 'url': 'https://gitlab.com', 'repo_url': '', 'branch': 'main', 'lfs_enabled': True},
    'server': {'host': '0.0.0.0', 'port': 8000, 'sync_interval': 60},
    'security': {'secret_key': '', 'encryption_key': ''},
    'paths': {'clone_path': './gitlab_repo_clone'}
}

class ConfigManager:  # NEW
    def __init__(self, config_file: Optional[Path] = None):
        self.config_file = config_file or Path('config.yaml')
        self.config = self._load_config()
```

- **Explanation**: yaml.safe_load = no eval (SE: secure). Defaults = robust.
- **Test**: Import—config = DEFAULT_CONFIG.
- **Gotcha**: safe_load = no arbitrary code.

**Step 2: Add \_load_config (Merge)**
Add:

```python
    def _load_config(self) -> Dict:  # NEW
        config = DEFAULT_CONFIG.copy()
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                file_config = yaml.safe_load(f) or {}
                self._merge_config(config, file_config)
        self._load_from_env(config)  # Stub
        return config
```

- **Explanation**: copy = shallow (CS: prototype). Merge recursive = deep update.
- **Test**: Create config.yaml mode: standalone, load → 'standalone'.

**Step 3: Add \_merge_config**
Add:

```python
    def _merge_config(self, base: Dict, override: Dict):  # NEW
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
```

- **Explanation**: Recursive = nested merge (CS: tree walk).
- **Test**: Merge {'a': {'b': 1}} with {'a': {'c': 2}} → {'a': {'b': 1, 'c': 2}}.

**Step 4: Add \_load_from_env (Override)**
Add:

```python
    def _load_from_env(self, config: Dict):  # NEW
        import os  # NEW
        if os.getenv('MODE'):
            config['mode'] = os.getenv('MODE')
        # Add all (gitlab.repo_url, etc.)
        if os.getenv('GITLAB_REPO_URL'):
            config['gitlab']['repo_url'] = os.getenv('GITLAB_REPO_URL')
        # ... similar for others
```

- **Explanation**: getenv = env pull (SE: 12-factor config).
- **Test**: .env MODE=standalone, load → Overrides YAML.

**Step 5: Add get/set/save**
Add:

```python
    def get(self, key_path: str, default=None):  # NEW
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set(self, key_path: str, value):  # NEW
        keys = key_path.split('.')
        target = self.config
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        target[keys[-1]] = value

    def save_config(self):  # NEW
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)  # Pretty
```

- **Explanation**: Dot path = config.get('gitlab.url') (JS-like). dump = serialize.
- **Test**: get('mode') → "server". set('mode', 'standalone'), save—config.yaml updates.

**Step 6: Add Mode Helpers & Singleton**
Add:

```python
    def is_standalone_mode(self) -> bool:
        return self.config['mode'] == 'standalone'

    def is_gitlab_enabled(self) -> bool:
        return self.config['gitlab']['enabled']
```

At end:

```python
config_manager = ConfigManager()  # NEW: Global
```

- **Explanation**: Helpers = abstraction (SE: API). Singleton = easy access.
- **Test**: config_manager.is_gitlab_enabled() → True.

**Full config_manager.py** (End of Section—Verify):

```python
import yaml
from pathlib import Path
from typing import Optional, Dict
import os

DEFAULT_CONFIG = {
    'mode': 'server',
    'gitlab': {'enabled': True, 'url': 'https://gitlab.com', 'repo_url': '', 'branch': 'main', 'lfs_enabled': True},
    'server': {'host': '0.0.0.0', 'port': 8000, 'sync_interval': 60},
    'security': {'secret_key': '', 'encryption_key': ''},
    'paths': {'clone_path': './gitlab_repo_clone'}
}

class ConfigManager:
    def __init__(self, config_file: Optional[Path] = None):
        self.config_file = config_file or Path('config.yaml')
        self.config = self._load_config()
    def _load_config(self) -> Dict:
        config = DEFAULT_CONFIG.copy()
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                file_config = yaml.safe_load(f) or {}
                self._merge_config(config, file_config)
        self._load_from_env(config)
        return config
    def _merge_config(self, base: Dict, override: Dict):
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    def _load_from_env(self, config: Dict):
        if os.getenv('MODE'):
            config['mode'] = os.getenv('MODE')
        if os.getenv('GITLAB_REPO_URL'):
            config['gitlab']['repo_url'] = os.getenv('GITLAB_REPO_URL')
        # ... add all other env
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
    def is_standalone_mode(self) -> bool:
        return self.config['mode'] == 'standalone'
    def is_gitlab_enabled(self) -> bool:
        return self.config['gitlab']['enabled']

config_manager = ConfigManager()
```

**Verification**: config_manager.get('mode') → "server". .env MODE=standalone, get → "standalone".

### 8.15: PyInstaller Packaging (Build Script Incremental)

**Step 1: Create pdm_app.py (Standalone Entry)**

```bash
touch backend/pdm_app.py
```

Paste:

```python
import sys  # NEW
import webbrowser  # NEW
import threading  # NEW
import time  # NEW
from pathlib import Path  # NEW

sys.path.insert(0, str(Path(__file__).parent))  # NEW: Import app

from app.main import app  # NEW
from app.config import settings  # NEW
import uvicorn  # NEW

def run_server():  # NEW
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, log_level="info")

def open_browser():  # NEW
    time.sleep(2)
    webbrowser.open(f'http://127.0.0.1:{settings.PORT}')

def main():  # NEW
    print("PDM System - Standalone Mode\\nServer on http://127.0.0.1:8000\\nBrowser opening...")
    browser_thread = threading.Thread(target=open_browser, daemon=True)  # NEW
    browser_thread.start()
    try:
        run_server()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
```

- **Explanation**: sys.path = module search (Python: import path). Thread = concurrent server/browser (CS: parallelism).
- **Test**: `python backend/pdm_app.py` → Server starts, browser opens /.
- **Gotcha**: daemon=True = main exit kills thread.

**Step 2: Create pdm.spec (Bundle)**

```bash
touch backend/pdm.spec
```

Paste:

```python
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['pdm_app.py'],  # NEW: Entry
    pathex=[], binaries=[], datas=[('static', 'static'), ('app', 'app')],  # NEW: Bundle
    hiddenimports=['passlib.handlers.bcrypt', 'git', 'yaml'],  # NEW: Force include
    hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=[], win_no_prefer_redirects=False,
    win_private_assemblies=False, cipher=block_cipher, noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],  # NEW: Exe
    name='PDM_System', debug=False, bootloader_ignore_signals=False, strip=False, upx=True,
    upx_exclude=[], runtime_tmpdir=None, console=True, disable_windowed_traceback=False,
    target_arch=None, codesign_identity=None, entitlements_file=None)
```

- **Explanation**: datas = copy folders (static/app to exe). hiddenimports = detect failures (PyInstaller scan misses).
- **Test**: `pip install pyinstaller; pyinstaller pdm.spec` → dist/PDM_System.exe.
- **Gotcha**: console=True = cmd window (set False for GUI).

**Step 3: Create build_standalone.py**

```bash
touch backend/build_standalone.py
```

Paste:

```python
import subprocess  # NEW
import sys  # NEW

def build():  # NEW
    print("Building PDM standalone...")
    spec_file = Path(__file__).parent / "pdm.spec"
    cmd = ["pyinstaller", str(spec_file), "--clean", "--noconfirm"]  # NEW
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print("Success! Exe in dist/PDM_System.exe")
    else:
        print("Failed!")
        sys.exit(1)

if __name__ == '__main__':
    build()
```

- **Explanation**: subprocess = shell call (CS: process spawn). --clean = fresh build.
- **Test**: `python backend/build_standalone.py` → Exe created.
- **Gotcha**: Run in venv (deps bundled).

**Step 4: Test Exe**
Copy config.yaml to dist/ (mode: standalone), double-click PDM_System.exe.

- **Explanation**: Exe bundles Python/ deps (SE: portable).
- **Test**: Opens browser to /, login works (local if GitLab off).
- **Gotcha**: No --reload in exe (debug=False).

**Full pdm_app.py/pdm.spec/build_standalone.py** (End of Section—Verify):
[Paste fulls]

**Verification**: Exe runs, opens /, /api/files works.

### 8.16: Complete Test Script (E2E + Unit)

**Step 1: Create TESTING.md**

```bash
touch TESTING.md
```

Paste your guide, expand with script section:

````markdown
## Complete Test Script

Run this bash script to test full app (server mode).

```bash
#!/bin/bash
# test_pdm.sh - E2E Test

cd backend

# Start server in background
uvicorn app.main:app --reload --port 8000 &
SERVER_PID=$!

sleep 3  # Wait start

# Test 1: Health
curl -f http://127.0.0.1:8000/api/files > /dev/null && echo "Health OK" || echo "Health FAIL"

# Test 2: Login
TOKEN=$(curl -s -X POST "http://127.0.0.1:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=Admin123!" | jq -r '.access_token')

if [ -n "$TOKEN" ]; then
  echo "Login OK"
else
  echo "Login FAIL"
  kill $SERVER_PID
  exit 1
fi

# Test 3: Protected Files
curl -f -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/api/files > /dev/null && echo "Protected OK" || echo "Protected FAIL"

# Test 4: Checkout (create dummy if no files)
# Assume repo/test.mcam exists or skip

# Test 5: Audit Logs (admin)
curl -f -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/api/files/admin/audit-logs | jq '.count' > /dev/null && echo "Audit OK" || echo "Audit FAIL"

# Cleanup
kill $SERVER_PID
echo "Tests complete"
```
````

````
- **Explanation**: curl = HTTP test (CS: client). jq = JSON parse (app: verify structure). &/PID = background (Unix).
- **Test**: `bash test_pdm.sh` → "OK" for all (add dummy file if needed).
- **Gotcha**: jq install (npm i -g jq).

**Step 2: Add Pytest Unit (backend/tests/test_auth.py)**
```bash
pip install pytest  # Add to requirements
touch backend/tests/test_auth.py
````

Paste:

```python
import pytest
from app.services.auth_service import UserService, verify_password
from pathlib import Path

@pytest.fixture
def user_service(tmp_path):
    file = tmp_path / "users.json"
    return UserService(file)

def test_create_user(user_service):
    user_service.create_default_users()
    user = user_service.get_user("admin")
    assert user.username == "admin"
    assert verify_password("Admin123!", user.password_hash)

def test_auth(user_service):
    user_service.create_default_users()
    user = user_service.authenticate_user("admin", "Admin123!")
    assert user is not None
    user = user_service.authenticate_user("admin", "wrong")
    assert user is None
```

- **Explanation**: Fixture = setup/teardown (CS: test isolation). assert = verify.
- **Test**: `pytest backend/tests/test_auth.py` → Passed.
- **Gotcha**: tmp_path = temp dir.

**Full TESTING.md** (End of Section—Verify):
[Your expanded guide with scripts]

**Verification**: bash test_pdm.sh → All OK. pytest → Units pass.

### Stage 8 Complete

**Test Full Hybrid**:

- Server: uvicorn with .env MODE=server, GITLAB_REPO_URL=yourrepo → Syncs.
- Standalone: build_standalone.py, config.yaml mode: standalone → Exe runs local, clones GitLab.

**Verification**:

- [ ] Login tabs: Password/GitLab work.
- [ ] Messages panel: Send/view/delete, badge.
- [ ] Config YAML/env overrides.
- [ ] Exe bundles/runs, opens browser.
- [ ] Test script passes.

**What You Learned (Depth)**:

- **CS**: Eventual consistency (pull/merge), Fernet (hybrid crypto).
- **App**: PAT flow (scopes), slide panels (off-canvas UX).
- **Python**: yaml (parse), subprocess (build).
- **JS**: FormData (encode), setInterval (poll).
- **SE**: Feature flags (GITLAB_ENABLED), portable exes (PyInstaller).

Tutorial done! App = full hybrid PDM. Questions or Stage 9 (e.g., WebSockets)?
