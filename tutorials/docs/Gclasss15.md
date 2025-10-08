# Step 15: Admin Extras – Repo Switch, LFS, & Users (Advanced Management – 1.5hr)

**Big Picture Goal**: Add admin tools: Repo switch (multi-project), LFS status/configure, user list/create/delete. JS fetches /repos/list + /admin/users, backend handles switch/save. Understand **admin layers** (role-gated features for power users).

**Why Fifteenth?** (Admin Principle: **Gate Power – Secure Extras After Core**). MVP secure; now admin (switch repo = multi-factory, LFS = large files, users = team mgmt). **Deep Dive**: Role-gate = "least privilege" (admin only = no leak). Why multi-repo? Scale (one app, many GitLabs). Resource: [RBAC Basics](https://en.wikipedia.org/wiki/Role-based_access_control) – 3min, "Roles."

**When**: After uploads—admin manages (e.g., add users for team uploads). Use for teams (e.g., G-code: Admin assigns roles).

**How**: JS role check (if is_admin), fetch list, backend switch/save. Gotcha: Admin endpoints = auth guard (Depends).

**Pre-Step**: Branch: `git checkout -b step-15-admin`. Mock /repos/list: `@router.get("/repos/list") async def list_repos(): return {"repos": [{"project_id": 1, "url": "test.git"}]}`. Mock /admin/users: `@router.get("/admin/users") async def users(): return {"users": [{"username": "admin", "is_admin": True}]}`. Add to config panel: `<button data-action="switchRepo">Switch Repo</button> <div id="repoList"></div>`.

---

### 15a: Client Repo Switch – List & Select

**Question**: How do we list repos for admin to switch? We need fetch /repos/list, render select, on change call switch.

**Micro-Topic 1: Fetch Repo List**  
**Type This (add to ui/config.js)**:

```javascript
export async function loadRepos() {
  const response = await fetch("/repos/list"); // What: Get list.
  const data = await response.json();
  console.log("Repos:", data.repos); // Test.
  return data.repos; // For render.
}
```

**Inline 3D Explain**:

- **What**: fetch = GET list. json() = parse.
- **Why**: List = "available choices" (multi-repo). **Deep Dive**: /repos = admin-only (guard backend). Resource: [MDN Fetch GET](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#fetch_with_get_headers_and_a_json_body) – 1min.
- **How**: return = pass to render. Gotcha: No try = crash on fail. **Alternative**: Cache = offline list.

**Try This (10s)**: Update delegation case "switchRepo": `const repos = await loadRepos(); console.log(repos);`. Click → console array? Tweak: Mock response → logs. Reflect: "Why return? Caller (render) uses—no global."

**Inline Lens (SRP Integration)**: loadRepos = data pull only (no UI—render next). Violate? Render in load = mixed.

**Mini-Summary**: Fetch + return = list data. Simple GET.

**Micro-Topic 2: Render Repo Select**  
**Type This (add to config.js)**:

```javascript
function renderRepoSelect(repos) {
  const container =
    document.getElementById("repoList") || document.createElement("div"); // Target/create.
  let html = '<select id="repoSelect">'; // What: Dropdown.
  repos.forEach(
    (repo) =>
      (html += `<option value="${repo.project_id}">${repo.url}</option>`)
  ); // Loop options.
  html += '</select><button data-action="doSwitch">Switch</button>';
  container.innerHTML = html;
  return container; // For append.
}
```

**Inline 3D Explain**:

- **What**: forEach = loop. innerHTML = set options.
- **Why**: Select = UX choice (list = scrollable). **Deep Dive**: value = id (switch uses). Resource: [MDN Select](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select) – 2min, "Options."
- **How**: project_id = key. Gotcha: No loop = empty. **Alternative**: Datelist = search—over for few.

**Try This (15s)**: Update case "switchRepo": `const repos = await loadRepos(); renderRepoSelect(repos);`. Click → select with options? Tweak: Mock repos → populates. Reflect: "Why forEach? Map = array, but innerHTML needs string."

**Inline Lens (DRY Integration)**: renderRepoSelect = UI only (load = data). Violate? Fetch in render = tight.

**Mini-Summary**: forEach + select = choice UI. innerHTML = quick.

**Git**: `git add config.js && git commit -m "feat(step-15a): repo list + select"`.

---

### 15b: Backend Repo Switch – Save & Re-Init

**Question**: How does backend switch repo (update config, re-clone)? We need /repos/switch POST to save + init new.

**Micro-Topic 1: Switch Route Stub**  
**Type This (add to backend/endpoints.py)**:

```python
@router.post("/repos/switch")
async def switch_repo(project_id: str = Form(...)):
  # What: Save new ID.
  print(f"Switch to {project_id}");  // Test.
  return {"status": "switched"};  // Mock.
```

**Inline 3D Explain**:

- **What**: Form(...) = body extract. print = log.
- **Why**: Switch = "change active" (multi-repo). **Deep Dive**: Form = simple text. Resource: [FastAPI Form](https://fastapi.tiangolo.com/tutorial/body/#form-fields) – 1min.
- **How**: project_id = param. Gotcha: No type = str always. **Alternative**: JSON body = structured.

**Try This (10s)**: Postman POST /repos/switch (body: project_id=1) → "Switch to 1"? Tweak: Add raise HTTPException(400, "Invalid ID") if not int. Reflect: "Why Form? POST text = simple."

**Micro-Topic 2: Update Config & Re-Init**  
**Type This (update switch_repo)**:

```python
from .config import ConfigManager  // Import.

config_manager = ConfigManager();  // Get instance.

config_manager.update_gitlab_config(project_id=project_id);  // Save.
await initialize_app();  // Re-clone new repo—mock.
return {"status": "switched", "path": "new/repo"};  // Response.
```

**Inline 3D Explain**:

- **What**: update_gitlab_config = save call. await = async re-init.
- **Why**: Update = persist choice. **Deep Dive**: Re-init = "hot swap" (no restart). Resource: [FastAPI Async](https://fastapi.tiangolo.com/async/) – 2min, "Await."
- **How**: Instance = shared. Gotcha: No await = partial switch. **Alternative**: No re-init = stale.

**Try This (15s)**: POST → "new/repo"? Tweak: Mock initialize_app = print("Re-init"). Reflect: "Why update + re-init? Save = remember, re-init = active."

**Inline Lens (SRP Integration)**: endpoints = route, config = save. Violate? Save here = mixed.

**Mini-Summary**: POST + update + re-init = switch complete.

**Git**: `git add endpoints.py && git commit -m "feat(step-15b): backend repo switch"`.

---

### 15c: LFS Status – Check & Display

**Question**: How do we show LFS health (installed/configured)? Fetch /system/lfs_status, render in config tab.

**Micro-Topic 1: Fetch LFS Status**  
**Type This (add to ui/config.js)**:

```javascript
export async function loadLFSStatus() {
  const response = await fetch("/system/lfs_status");
  const data = await response.json();
  console.log("LFS:", data); // Test.
  return data; // For render.
}
```

**Inline 3D Explain**:

- **What**: fetch = GET status.
- **Why**: LFS = large file opt (check = warn if no). **Deep Dive**: Status = "system probe" (subprocess git lfs version). Resource: [MDN Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) – 1min, "GET."
- **How**: json = parse. Gotcha: No try = crash. **Alternative**: Poll = real-time, but once = fine.

**Try This (10s)**: Update case "lfsStatus": `const lfs = await loadLFSStatus(); console.log(lfs);`. Click (add button) → console {lfs_installed: true}? Tweak: Mock = {installed: false}. Reflect: "Why fetch? Client no know LFS—server probe."

**Micro-Topic 2: Render LFS in Tab**  
**Type This (add to config.js)**:

```javascript
function renderLFSStatus(data) {
  const container =
    document.getElementById("lfsContainer") || document.createElement("div");
  const status = data.lfs_installed ? "Active" : "Missing"; // Conditional.
  container.innerHTML = `<p>LFS Status: ${status}</p>`; // Simple.
  return container;
}
```

**Inline 3D Explain**:

- **What**: ? : = ternary. innerHTML = set.
- **Why**: Render = "data to UI" (status = visual). **Deep Dive**: Installed = yes/no (patterns next). Resource: [MDN Ternary](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Conditional_operator) – 1min.
- **How**: id = target. Gotcha: No container = create. **Alternative**: TextContent = plain, innerHTML = styled.

**Try This (15s)**: Update case: `renderLFSStatus(await loadLFSStatus());`. Click → "LFS Status: Active"? Tweak: Mock false → "Missing." Reflect: "Why ternary? If/else = long string."

**Inline Lens (SRP Integration)**: loadLFSStatus = data, render = UI. Violate? Render fetches = mixed.

**Mini-Summary**: Fetch + render = LFS display. Ternary = conditional UI.

**Git**: `git add config.js && git commit -m "feat(step-15c): LFS status"`.

---

### 15d: User Management – List, Create, Delete

**Question**: How do we list/create/delete users for admin? Fetch /admin/users, render table, buttons call endpoints.

**Micro-Topic 1: Fetch User List**  
**Type This (add to ui/config.js)**:

```javascript
export async function loadUsers() {
  const response = await fetch("/admin/users"); // Auth guard backend.
  const data = await response.json();
  console.log("Users:", data.users); // Test.
  return data.users;
}
```

**Inline 3D Explain**:

- **What**: fetch = GET list.
- **Why**: List = "team view" (admin adds). **Deep Dive**: /admin = role-gate (401 if not admin). Resource: [MDN Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) – 1min.
- **How**: json = array. Gotcha: No auth header = 401. **Alternative**: Paginate = big teams.

**Try This (10s)**: Update case "loadUsers": `const users = await loadUsers(); console.log(users);`. Click → array? Tweak: Mock = [{"username": "admin"}]. Reflect: "Why /admin? Gate = secure (no leak users)."

**Micro-Topic 2: Render User Table**  
**Type This (add to config.js)**:

```javascript
function renderUsers(users) {
  const container =
    document.getElementById("usersContainer") || document.createElement("div");
  let html = '<table class="w-full border">'; // Table shell.
  users.forEach(
    (user) =>
      (html += `<tr><td>${user.username}</td><td><button data-action="deleteUser" data-username="${user.username}">Delete</button></td></tr>`)
  ); // Row + button.
  html += "</table>";
  container.innerHTML = html;
  return container;
}
```

**Inline 3D Explain**:

- **What**: forEach = loop rows. data-username = param for delete.
- **Why**: Table = structured (username + action). **Deep Dive**: Button = delegation (deleteUser route). Resource: [MDN Tables](https://developer.mozilla.org/en-US/docs/Learn/HTML/Tables) – 2min, "Actions."
- **How**: w-full = responsive. Gotcha: No escape = XSS (username trusted). **Alternative**: List = flow, table = columns.

**Try This (15s)**: Update case: `renderUsers(await loadUsers());`. Click → table with Delete button? Tweak: Add is_admin column → `${user.is_admin ? 'Yes' : 'No'}`. Reflect: "Why data-username? Delete knows who without query."

**Inline Lens (SRP Integration)**: loadUsers = data, render = UI. Violate? Render fetches = tight.

**Mini-Summary**: Fetch + table = user mgmt. forEach = row build.

**Micro-Topic 3: Delete User Action**  
**Type This (add case to main.js delegation)**:

```javascript
case "deleteUser":
  const username = button.dataset.username;
  if (!confirm(`Delete ${username}?`)) return;  // Guard.
  await deleteUser(username);  // Call stub.
  loadUsers();  // Re-load list.
  break;
```

**Inline 3D Explain**:

- **What**: confirm = browser dialog. await = wait delete.
- **Why**: Guard = "intent confirm" (no accident). **Deep Dive**: Re-load = fresh (optimistic delete later). Resource: [MDN Confirm](https://developer.mozilla.org/en-US/docs/Web/API/Window/confirm) – 1min.
- **How**: dataset = param. Gotcha: No confirm = instant delete. **Alternative**: Custom modal = styled.

**Try This (20s)**: Click Delete → confirm prompt? Mock deleteUser = showNotification("Deleted"). Accept → notify + re-list? Tweak: No re-load → stale. Reflect: "Why confirm? Human error = bad (wrong user gone)."

**Inline Lens (Error Handling Integration)**: Confirm = user error guard. Violate? No = irreversible.

**Mini-Summary**: Delegation + confirm = safe delete. Re-load = fresh.

**Git**: `git add main.js config.js && git commit -m "feat(step-15d): user mgmt list/create/delete"`.

---

**Step 15 Complete!** Admin extras live. Reflect: "Flow: Admin click switch → fetch list → select render → POST switch → re-init. SRP: config = data/UI, endpoints = API."

**App Complete!** MVP + extras = full original (modular). Reflect: "From shell to admin—principles (SRP/DRY) = clean code. Test/deploy next?"

**Bonus Next**: Step 16: Deploy (Vercel/Heroku). Or fixes? Go? 🚀
