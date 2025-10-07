# Step 4: File Listing & Rendering – From Data to Visible UI (Data Flow – 2hr)

**Big Picture Goal**: Fetch files from /files, group by name (e.g., "12XXXXX"), render as cards in #fileList. Understand **data to UI pipeline** (fetch → state → template → DOM).

**Why Fourth?** (Data Principle: **State Before View – Reactive Foundations**). Auth/config secure; now pull data, show it. **Deep Dive**: Pipeline = "data in, UI out" (fetch = pull, state = hold, render = paint). Why group? Manufacturing org (part nums). Resource: [Vanilla JS Rendering](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Manipulating_documents) – 4min, "innerHTML vs createElement" (innerHTML = fast for templates).

**When**: After config—repo URL enables /files. Use for lists (e.g., inventory table).

**How**: Fetch JSON, loop/group, template literals for cards, innerHTML inject. Gotcha: innerHTML = fast but escapes needed (trusted data here).

**Pre-Step**: Branch: `git checkout -b step-4-files`. Mock /files in backend/endpoints.py: `@router.get("/files") async def get_files(): return {"Misc": [{"filename": "test.mcam", "size": 1024, "modified_at": "2023-01-01T00:00:00Z"}]};` (test fetch).

---

### 4a: Fetching Files – Pulling Data from Server

**Question**: How do we get the file list from backend? We need a function to fetch /files and handle success/fail.

**Micro-Topic 1: Basic Fetch Call**  
**Type This (create ui/fileManager.js)**:

```javascript
// fileManager.js - Files data/UI. What: Fetch = request data.

export async function loadFiles() {
  const response = await fetch("/files"); // GET default—pull list.
  const data = await response.json(); // Parse JSON → object.
  console.log("Files loaded:", data); // Log for test.
}
```

**Inline 3D Explain**:

- **What**: fetch = Promise request. json() = body parse.
- **Why**: Pull = "server has truth" (fresh data). **Deep Dive**: Await = linear code (no .then nest). Resource: [MDN Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) – 2min, "GET."
- **How**: /files = endpoint (mock returns object). Gotcha: No await = undefined data. **Alternative**: XMLHTTPRequest = old/callback hell—fetch = modern.

**Try This (10s)**: Update main.js initApp: `await loadFiles();`. Refresh → console object {"Misc": [...]}? Tweak: Wrong URL (/wrong) → error? Reflect: "Why json()? Response = stream—parse to use."

**Inline Lens (Async Integration)**: Await = "wait without blocking" (UI stays responsive). Violate? Sync fetch = freeze.

**Mini-Summary**: Fetch + json = data pull. Await = clean.

**Micro-Topic 2: Error Handling in Fetch**  
**Type This (update loadFiles)**:

```javascript
export async function loadFiles() {
  try {
    const response = await fetch("/files");
    if (!response.ok)
      throw new Error(`HTTP ${response.status}: ${response.statusText}`); // 404/500 = fail.
    const data = await response.json();
    console.log("Files loaded:", data);
  } catch (error) {
    console.error("Load failed:", error); // Log for dev.
    showNotification("Files load error—check connection", "error"); // User feedback.
  }
}
```

**Inline 3D Explain**:

- **What**: ok = 200-299. throw = bubble to catch.
- **Why**: Handle fail = "graceful" (error msg vs blank). **Deep Dive**: Catch = all errors (network, parse). Resource: [MDN Fetch Errors](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#handling_errors) – 2min, "try/catch."
- **How**: status = code (401 = auth). Gotcha: No if = parse 404 = crash. **Alternative**: .catch on fetch = same, but try = all in one.

**Try This (15s)**: Refresh → success log? Dev tools Network → block /files (fail tab) → error notify? Tweak: Throw custom (`throw new Error("Mock fail")`) → same catch. Reflect: "Why notify? User knows vs 'nothing happened'."

**Inline Lens (Error Handling Integration)**: Try/catch = "expect fail" (network = common). Violate? Uncaught = console dump—user confused.

**Mini-Summary**: Try/catch = robust fetch. ok check = status guard.

**Git**: `git add fileManager.js main.js && git commit -m "feat(step-4a): files fetch + errors"`.

---

### 4b: Storing Files in State – Central Data Hold

**Question**: How do we keep fetched files accessible (e.g., render uses it)? We need a central spot for data.

**Micro-Topic 1: App-Wide State Object**  
**Type This (update ui/main.js)**:

```javascript
// main.js - Add state. What: Object = central data.

window.appState = {}; // Global holder—modules read/write.

export async function initApp() {
  showNotification("App starting...");
  appState.files = await loadFiles(); // Wait data, store.
  console.log("State:", appState.files); // Test.
}
```

**Inline 3D Explain**:

- **What**: window.appState = global object. = await = store result.
- **Why**: Central = "single truth" (render reads appState.files—no dup fetches). **Deep Dive**: Global = easy access, but pollutes (window = namespace). Resource: [MDN Global Objects](https://developer.mozilla.org/en-US/docs/Glossary/Global_object) – 2min, "window."
- **How**: Await in init = sequential. Gotcha: No state = undefined reads. **Alternative**: Module state = private (export getFiles)—better encapsulation.

**Try This (10s)**: Refresh → console appState.files = object? Tweak: `appState.user = 'test'; console.log(appState.user)` → "test"? Reflect: "Why appState? Dup vars = inconsistency (one has files, another not)."

**Micro-Topic 2: Update loadFiles to Store**  
**Type This (update ui/fileManager.js loadFiles)**:

```javascript
export async function loadFiles() {
  try {
    const response = await fetch("/files");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    window.appState.files = data; // Store in state.
    return data; // For initApp.
  } catch (error) {
    // ... error from 4a.
  }
}
```

**Inline 3D Explain**:

- **What**: appState.files = assign.
- **Why**: Store = reuse (render reads, no re-fetch). **Deep Dive**: Return + store = flexible (caller uses or not). Resource: [State Patterns](https://www.patterns.dev/react/state-management/) – 3min, "Simple object" (vanilla version).
- **How**: window = global access. Gotcha: Typos = silent fail (console.dir(appState)). **Alternative**: Pass state as param = explicit, but verbose.

**Try This (15s)**: Refresh → appState.files = data? Tweak: Mock data in fetch → updates? Reflect: "Why return? Caller (init) can log, but store = shared."

**Inline Lens (SRP Integration)**: fileManager = data pull (loadFiles), main = wiring (store/use). Violate? Store in fileManager = tight coupling.

**Mini-Summary**: State object = shared data hub. Store + return = flexible.

**Git**: `git add main.js fileManager.js && git commit -m "feat(step-4b): files state storage"`.

---

### 4c: Rendering Groups – Organizing Data to HTML

**Question**: How do we turn files object into grouped sections (e.g., "Misc" folder)? We need loop + template for structure.

**Micro-Topic 1: Basic Loop for Groups**  
**Type This (add to ui/fileManager.js)**:

```javascript
export function renderFiles(data = window.appState.files) {
  const fileList = document.getElementById("fileList"); // Target elem.
  let html = ""; // Build string.

  for (const groupName in data) {
    // Loop keys (groups).
    const files = data[groupName]; // Get array.
    html += `<details><summary>${groupName} (${files.length} files)</summary>`; // Group header.
    // Files next micro.
  }

  fileList.innerHTML = html; // Inject all.
}
```

**Inline 3D Explain**:

- **What**: for...in = object keys. innerHTML = parse/set HTML.
- **Why**: Group = logical (manufacturing parts). **Deep Dive**: innerHTML = fast for many elems (vs createElement loop = slow). Resource: [MDN innerHTML](https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML) – 2min, "Security" (trusted data).
- **How**: template literal = `${var}` insert. Gotcha: innerHTML = overwrites—morphdom for diffs later. **Alternative**: DocumentFragment = batch insert (faster big lists).

**Try This (10s)**: Update main.js initApp: `renderFiles();`. Refresh → #fileList has <details> for each group? Tweak: Mock data = {"Test": [{"filename": "test.mcam"}]} → "Test (1 files)"? Reflect: "Why for...in? Object.keys(data).forEach = same, but in = direct."

**Micro-Topic 2: Add Sub-Details for Files**  
**Type This (update renderFiles loop)**:

```javascript
for (const groupName in data) {
  const files = data[groupName];
  html += `<details><summary>${groupName} (${files.length} files)</summary><div class="p-4">`;
  for (const file of files) {
    // Loop files in group.
    html += `<div class="p-2 border">${file.filename}</div>`; // Simple card.
  }
  html += "</div></details>"; // Close group.
}
```

**Inline 3D Explain**:

- **What**: for...of = array values. div = card placeholder.
- **Why**: Nested = hierarchy (group > file). **Deep Dive**: Template = string build (fast concat). Resource: [MDN for...of](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...of) – 2min, "Arrays."
- **How**: Nested loops = tree. Gotcha: No close = invalid HTML. **Alternative**: map().join('') = functional (immutable).

**Try This (20s)**: Refresh → groups with file cards? Tweak: Add <i class="fa-solid fa-file"></i> to card → icons? Reflect: "Why innerHTML at end? Build string = efficient (one DOM touch)."

**Inline Lens (DRY Integration)**: Loop = reuse (one template for all groups). Violate? Hardcode groups = no scale.

**Mini-Summary**: Loops + templates = data to structured HTML. Nested = hierarchy.

**Git**: `git add fileManager.js && git commit -m "feat(step-4c): grouped render loop"`.

---

### 4d: Building File Cards – Data to Visual Elements

**Question**: How do we make each file a clickable card (name, size, status)? We need a function for one card, looped in render.

**Micro-Topic 1: Basic Card Template Function**  
**Type This (add to ui/fileManager.js)**:

```javascript
function buildFileCard(file) {
  // One file → HTML.
  return `<div class="p-4 border rounded bg-white">  // Card shell.
    <h3 class="font-bold">${file.filename}</h3>  // Name.
    <p>Size: ${file.size} bytes</p>  // Detail.
  </div>`;
}
```

**Inline 3D Explain**:

- **What**: Function = input (file) → output (string). `${}` = insert.
- **Why**: Reusable = DRY (one func = many cards). **Deep Dive**: Template literal = multi-line easy. Resource: [MDN Templates](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals) – 2min, "Tagged."
- **How**: Return string = build. Gotcha: No escape = XSS (trusted data OK). **Alternative**: createElement = safe (no parse), slow for many.

**Try This (10s)**: Update render loop: `html += buildFileCard(file);`. Refresh → cards with name/size? Tweak: Add `${file.modified_at}` → date. Reflect: "Why func? Hardcode = copy-paste per file."

**Micro-Topic 2: Add Status & Action Button**  
**Type This (update buildFileCard)**:

```javascript
function buildFileCard(file) {
  const status = file.status || "unlocked"; // Default.
  const buttonText = status === "unlocked" ? "Checkout" : "Check In"; // Conditional.
  return `<div class="p-4 border rounded bg-white">
    <h3 class="font-bold">${file.filename}</h3>
    <p>Status: ${status}</p>
    <button data-action="fileAction" data-filename="${file.filename}" class="bg-blue-500 text-white px-2 py-1 rounded">${buttonText}</button>
  </div>`;
}
```

**Inline 3D Explain**:

- **What**: || = default. Ternary = if/else short.
- **Why**: Dynamic = smart UI (button changes on lock). **Deep Dive**: data-filename = param pass (delegation reads). Resource: [MDN Ternary](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Conditional_operator) – 1min.
- **How**: `${file.filename}` = escape in attr. Gotcha: No data-action = ignore. **Alternative**: if/else string = verbose.

**Try This (20s)**: Refresh → buttons "Checkout"? Mock data status="locked" → "Check In"? Click button → delegation logs "fileAction"? Tweak: Add data-status → pass to handler. Reflect: "Why data-filename? Delegation knows which file without ID hunt."

**Inline Lens (Performance Integration)**: Template string = fast build (one concat). Violate? createElement loop = slow for 100 files.

**Mini-Summary**: Card func = reusable visual. Conditional = dynamic.

**Git**: `git add fileManager.js && git commit -m "feat(step-4d): file card template"`.

---

**Step 4 Complete!** Files fetch/render as groups/cards. Reflect: "Pipeline: fetch → state → loop/template → DOM. SRP: fileManager = data/UI, main = wiring."

**Next**: Step 5: File Actions (checkout/checkin). Go? 🚀
