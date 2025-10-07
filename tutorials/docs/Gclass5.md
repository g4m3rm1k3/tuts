# Step 5: File Actions – Checkout, Checkin, and Interactions (User Operations – 2hr)

**Big Picture Goal**: Add buttons to file cards for checkout (lock) and checkin (unlock + upload). JS calls /files/{filename}/checkout, backend creates lock file + commit. Understand **user interactions** (click → API → state update → re-render).

**Why Fifth?** (Interaction Principle: **View Before Actions – UI Feedback Loop**). Files render; now make them clickable (checkout = lock for edits). **Deep Dive**: Actions = "user intent to change state" (lock = prevent concurrent CNC edits). Why commit locks? Audit trail (Git history = who/when). Resource: [RESTful Actions](https://restfulapi.net/resource-naming/) – 3min, "POST for create" (checkout = new lock).

**When**: After render—data visible before ops. Use for CRUD apps (e.g., inventory: checkout tool).

**How**: Delegation catches data-action="checkout", fetch POST with user. Backend: Lock JSON + git commit. Gotcha: Race condition (two checkouts)—backend lock prevents.

**Pre-Step**: Branch: `git checkout -b step-5-actions`. Mock /files/test.mcam/checkout in endpoints.py: `@router.post("/files/{filename}/checkout") async def checkout(filename: str): return {"status": "locked"}` (test POST).

---

### 5a: Adding Action Buttons to Cards – Intent Flags

**Question**: How do we make file cards clickable for checkout? We need a button per card with data-action for delegation.

**Micro-Topic 1: Update Card Template with Button**  
**Type This (update buildFileCard in ui/fileManager.js)**:

```javascript
function buildFileCard(file) {
  return `<div class="p-4 border rounded bg-white">
    <h3 class="font-bold">${file.filename}</h3>
    <p>Status: ${file.status || "unlocked"}</p>
    <button data-action="checkout" data-filename="${
      file.filename
    }" class="bg-green-500 text-white px-2 py-1 rounded">Checkout</button>
  </div>`;
}
```

**Inline 3D Explain**:

- **What**: data-action = flag, data-filename = param (which file).
- **Why**: Delegation-ready (main.js catches). **Deep Dive**: Data attrs = pass context (filename = know which without ID). Resource: [MDN Dataset](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dataset) – 2min, "Custom data."
- **How**: `${file.filename}` = escape in attr. Gotcha: Spaces = URL bad—encodeURI if needed. **Alternative**: ID on div = querySelector, but data = explicit.

**Try This (10s)**: Refresh → cards have Checkout button? Inspect button → data-filename="test.mcam"? Tweak: Change text to "Lock" → updates? Reflect: "Why data-filename? Button click = know file without global search."

**Inline Lens (Coupling Integration)**: Button intent = data, handler = main.js (low coupling). Violate? onclick="checkout('${file.filename}')" = string mess (escape hell).

**Mini-Summary**: Data attrs = intent + param pass. Delegation prep.

**Micro-Topic 2: Conditional Button Text by Status**  
**Type This (update button in buildFileCard)**:

```javascript
const buttonText = file.status === "locked" ? "Check In" : "Checkout"; // If locked, change text.
<button
  data-action="checkout"
  data-filename="${file.filename}"
  class="bg-green-500 text-white px-2 py-1 rounded"
>
  ${buttonText}
</button>;
```

**Inline 3D Explain**:

- **What**: === = strict equal. Ternary = short if/else.
- **Why**: Dynamic = context-aware (locked = "unlock"). **Deep Dive**: Status from data = reactive (re-render = update). Resource: [MDN Ternary](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Conditional_operator) – 1min.
- **How**: Var before = reuse. Gotcha: Falsy status = "Checkout" (|| undefined = falsy). **Alternative**: if/else string = long, ternary = concise.

**Try This (15s)**: Mock data with status="locked" → button "Check In"? Refresh → changes? Tweak: status="unlocked" → "Checkout." Reflect: "Why conditional? Static = wrong UX (locked file shows Checkout = confusion)."

**Inline Lens (SRP Integration)**: buildFileCard = view only (status from state—no logic). Violate? Button logic here = fat func.

**Mini-Summary**: Ternary = dynamic text. Context-aware UI.

**Git**: `git add fileManager.js && git commit -m "feat(step-5a): action buttons + conditional"`.

---

### 5b: Handling Checkout Action – Client Fetch to Backend

**Question**: How do we call /files/{filename}/checkout on click? We need delegation to route to fetch + update status.

**Micro-Topic 1: Delegation Route for Checkout**  
**Type This (update main.js delegation)**:

```javascript
case "checkout":
  const filename = button.dataset.filename;  // Get param from data.
  await checkoutFile(filename);  // Call handler.
  break;
```

**Inline 3D Explain**:

- **What**: dataset.filename = attr value. await = wait result.
- **Why**: Delegation routes (action = "checkout" → specific func). **Deep Dive**: Dataset = camelCase (data-filename = filename). Resource: [MDN Dataset](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dataset) – 2min, "Read."
- **How**: button from closest. Gotcha: No data = undefined (check if (filename)). **Alternative**: Pass e.target = manual attr read—verbose.

**Try This (10s)**: Click Checkout → console "filename = test.mcam"? Tweak: Add alert(filename) → popup name. Reflect: "Why dataset? Delegation = param-free call."

**Micro-Topic 2: Checkout Fetch Function**  
**Type This (add to ui/fileManager.js)**:

```javascript
export async function checkoutFile(filename) {
  const response = await fetch(`/files/${filename}/checkout`, {
    method: "POST",
  });
  if (!response.ok) throw new Error("Checkout failed");
  showNotification(`Locked ${filename}`); // Feedback.
  loadFiles(); // Re-fetch to update UI.
}
```

**Inline 3D Explain**:

- **What**: `/files/${filename}` = template URL. POST = create (lock).
- **Why**: API call = state change (server locks). **Deep Dive**: Re-fetch = "optimistic update" later (assume success, rollback on fail). Resource: [MDN POST Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#supplying_request_options) – 2min, "POST body."
- **How**: No body = empty POST. Gotcha: No await = race (click twice = double lock). **Alternative**: Body with user = explicit (add JSON {user}).

**Try This (20s)**: Click Checkout → notify "Locked test.mcam"? Backend mock return 200 → success? Fail mock (response.ok = false) → error. Tweak: Add body JSON.stringify({user: 'test'}) → POST data. Reflect: "Why re-loadFiles? Local change = stale UI (others see lock via server)."

**Inline Lens (Error Handling Integration)**: Throw + catch (in delegation? Add try there) = handled. Violate? Fail silent = user confused ("Did it lock?").

**Mini-Summary**: Delegation + fetch = action call. Re-fetch = fresh UI.

**Git**: `git add main.js fileManager.js && git commit -m "feat(step-5b): checkout fetch"`.

---

### 5c: Backend Checkout – Creating Lock & Commit

**Question**: How does backend lock the file? We need JSON lock + Git commit for audit.

**Micro-Topic 1: Checkout Route Stub**  
**Type This (add to backend/endpoints.py)**:

```python
@router.post("/files/{filename}/checkout")
async def checkout_file(filename: str):
  # Mock lock—return success.
  return {"status": "locked"}
```

**Inline 3D Explain**:

- **What**: @router.post = handle POST. filename: str = path param.
- **Why**: Route = "API entry" (client calls, server acts). **Deep Dive**: Async = non-block (other requests wait not). Resource: [FastAPI Path Params](https://fastapi.tiangolo.com/tutorial/path-params/) – 2min, "{filename}."
- **How**: No body = simple. Gotcha: No async = sync block. **Alternative**: Query param (?file=) = GET-ish, but POST = mutate.

**Try This (10s)**: Backend run. Postman POST /files/test.mcam/checkout → {"status": "locked"}? Tweak: Add body JSON {user: 'test'} → ignore for now. Reflect: "Why path param? /files/{filename} = RESTful (resource-specific)."

**Micro-Topic 2: Create Lock JSON File**  
**Type This (add to checkout_file)**:

```python
import json
from pathlib import Path
from datetime import datetime, timezone

lock_dir = Path("locks")  // Dir for locks.
lock_dir.mkdir(exist_ok=True)
lock_file = lock_dir / f"{filename}.lock"  // File per lock.

lock_data = {
  "file": filename,
  "user": "test",  // From body later.
  "timestamp": datetime.now(timezone.utc).isoformat()
}
lock_file.write_text(json.dumps(lock_data, indent=2))  // Save JSON.

return {"status": "locked"}
```

**Inline 3D Explain**:

- **What**: mkdir = create dir. write_text = dump string.
- **Why**: Lock = file flag (simple DB). **Deep Dive**: JSON = readable (open = see locks). Resource: [Pathlib Write](https://docs.python.org/3/library/pathlib.html#pathlib.Path.write_text) – 2min, "JSON."
- **How**: isoformat = UTC string. Gotcha: No dir = error (mkdir fixes). **Alternative**: DB (SQLite) = concurrent-safe, but file = simple.

**Try This (15s)**: POST → locks/test.mcam.lock created? Read file → {"file": "test.mcam", ...}? Tweak: Add user from body (`user = request.json()["user"]`) → custom. Reflect: "Why timestamp? Expire old locks (clean stale)."

**Micro-Topic 3: Commit Lock to Git**  
**Type This (add to checkout_file, import git)**:

```python
import git

repo = git.Repo(".")  // Open current repo.
repo.git.add(str(lock_file))  // Stage file.
repo.index.commit(f"LOCK: {filename}")  // Commit msg.
repo.remotes.origin.push()  // Push to remote.

return {"status": "locked"}
```

**Inline 3D Explain**:

- **What**: Repo = git handle. add/commit/push = Git flow.
- **Why**: Commit = audit (history = who locked when). **Deep Dive**: Index = staging area (add = prep). Resource: [GitPython Basics](https://gitpython.readthedocs.io/en/stable/intro.html) – 3min, "Repo."
- **How**: str(lock_file) = path. Gotcha: No push = local only (others miss lock). **Alternative**: No Git = in-mem locks—lost on restart.

**Try This (20s)**: POST → git status clean? `git log --oneline` → "LOCK: test.mcam"? Tweak: No push → local commit only. Reflect: "Why commit? File = ephemeral—Git = permanent trail."

**Inline Lens (SRP Integration)**: endpoints = route only (git_repo.py = commit later). Violate? Commit here = fat route.

**Mini-Summary**: Route + JSON + commit = lock persist. Git = audit.

**Git**: `git add endpoints.py && git commit -m "feat(step-5c): backend checkout lock"`.

---

### 5d: Full Checkout Flow – Delegation to Re-Render

**Question**: How do we tie click → fetch → UI update? Delegation calls func, func fetches + re-renders.

**Micro-Topic 1: Delegation Route to Checkout**  
**Type This (update main.js delegation)**:

```javascript
case "checkout":
  const filename = button.dataset.filename;  // Param from data.
  if (!filename) return showNotification("No file", "error");
  await checkoutFile(filename);  // Call from fileManager.
  break;
```

**Inline 3D Explain**:

- **What**: dataset.filename = attr read. await = wait success.
- **Why**: Route = "action to func" (decoupled). **Deep Dive**: If check = guard (bad data = early fail). Resource: [MDN Dataset](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dataset) – 2min.
- **How**: button from closest. Gotcha: No data = undefined (guard fixes). **Alternative**: e.target = direct, but closest = nested-safe.

**Try This (10s)**: Click Checkout → console param? Mock checkoutFile = alert(filename) → "test.mcam"? Tweak: Remove data-filename → "No file." Reflect: "Why guard? Bad data = crash later."

**Micro-Topic 2: Checkout Func with Re-Render**  
**Type This (update fileManager.js checkoutFile)**:

```javascript
export async function checkoutFile(filename) {
  try {
    const response = await fetch(`/files/${filename}/checkout`, {
      method: "POST",
    });
    if (!response.ok) throw new Error("Checkout failed");
    showNotification(`Locked ${filename}`);
    await loadFiles(); // Re-fetch → update status in cards.
  } catch (error) {
    showNotification(error.message, "error");
  }
}
```

**Inline 3D Explain**:

- **What**: POST = mutate. await loadFiles = refresh data.
- **Why**: Re-fetch = "server truth" (status = locked). **Deep Dive**: Optimistic UI later (assume success, rollback fail). Resource: [Optimistic Updates](https://react.dev/learn/manipulating-the-dom#optimistic-updates) – 3min, vanilla version.
- **How**: No body = empty. Gotcha: No await = old UI (stale status). **Alternative**: Local update (status = "locked") = fast, but wrong if server fails.

**Try This (20s)**: Click Checkout → notify "Locked," cards re-render (status changes if backend mocks)? Fail mock (throw in backend) → error. Tweak: Remove await loadFiles → no update. Reflect: "Why re-fetch? Local change = others miss (no sync)."

**Inline Lens (Performance Integration)**: Await = sequential (lock → refresh). Violate? Parallel = race (update before lock = wrong status).

**Mini-Summary**: Delegation + fetch + re-render = action loop. Await = order.

**Git**: `git add main.js fileManager.js && git commit -m "feat(step-5d): full checkout flow"`.

---

**Step 5 Complete!** Files actionable. Reflect: "Flow: Click → delegation param → fetch POST → backend lock/commit → re-fetch → render update. SRP: fileManager = actions, endpoints = API."

**Next**: Step 6: Modals & Forms (dynamic UI). Go? 🚀
