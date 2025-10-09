# Step 3: Configuration – Loading & Saving Settings (User Preferences – 1hr)

**Big Picture Goal**: Add a settings panel for GitLab URL/token. JS loads from /config, fills form; submit saves to /config/gitlab. Understand **data flow** (fetch → state → UI → save).

**Why Third?** (Layered Principle: **Data Before Interactions** – SRP repeat: Config = data, auth = security). Shell + auth work; now user prefs (repo URL) to unlock files. **Deep Dive**: Config = "app brain" (keys/values persist prefs). Why JSON? Human-readable, easy parse. Resource: [JSON in Apps](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON) – 3min, "Parsing" section.

**When**: After auth—user-specific data. Use for dashboards (API keys, themes).

**How**: Fetch GET /config, FormData POST save. Gotcha: Encrypt token backend-side (plain = leak risk).

**Pre-Step**: Branch: `git checkout -b step-3-config`. Add to #configPanel:

```html
<form id="configForm">
  <input id="gitlabUrl" placeholder="GitLab URL" />
  <input id="token" type="password" placeholder="Token" />
  <button data-action="saveConfig">Save</button>
</form>
```

(stub for test).

---

## 3a: Client-Side Config State – Storing Preferences

**Question**: How do we keep GitLab URL/token in one place for easy access (e.g., fileManager uses it)?

**Micro-Topic 1: Variable for Config Object**  
**Type This (create ui/config.js)**:

```javascript
// config.js - Holds app settings. What: Object for key-value prefs.

let config = {}; // Empty start—filled on load.
```

**Inline 3D Explain**:

- **What**: `{}` = object (key: value pairs, like dict).
- **Why**: Central spot = easy access (other modules read config.url). SRP: config.js = data only.
- **How**: Mutable = change keys (config.url = "https://..."). Gotcha: Refresh = lost—persist next. **Alternative**: Array = ordered, but object = lookup fast (O(1)).

**Try This (10s)**: Console: `config = {url: 'test'}; console.log(config.url)` = "test"? Tweak: `config.token = 'secret';` → object grows. Reflect: "Why object? Map-like—fast 'get URL'."

**Mini-Summary**: Object = simple store for prefs. One reason to change = SRP win.

**Micro-Topic 2: Helper to Load/Save Config**  
**Type This (add to config.js)**:

```javascript
export function getConfig() {
  return config; // Read-only view—why? Prevent accidental changes elsewhere.
}

export function setConfig(newConfig) {
  config = { ...newConfig }; // Spread = copy (shallow—fine for primitives).
  localStorage.setItem("config", JSON.stringify(config)); // Persist as string.
}
```

**Inline 3D Explain**:

- **What**: ... = spread (copy keys). JSON.stringify = object → string (storage needs).
- **Why**: Helpers = abstraction (call getConfig, no poke config). DRY: Save once, use everywhere. **Deep Dive**: Shallow copy = fast; deep for nests (JSON.parse/stringify = full clone). Resource: [MDN Spread](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) – 2min, "Copy objects."
- **How**: localStorage.setItem = save string. Gotcha: JSON = no functions/dates (stringify loses them—parse back). **Alternative**: No persist = reload = reset—bad UX.

**Try This (15s)**: Console: `import('./config.js').then(c => { c.setConfig({url: 'test'}); console.log(c.getConfig()); });` → {url: 'test'}? Refresh → still? Tweak: `localStorage.clear()` → gone on next get. Reflect: "Why stringify? Storage strings only—parse to object."

**Inline Lens (DRY Integration)**: Helpers = no copy-paste saves across files. Violate? Each module saves = bugs on change (e.g., add expiry = hunt all).

**Mini-Summary**: Helpers + localStorage = persistent prefs. Easy read/write = low coupling.

**Git**: `git add config.js && git commit -m "feat(step-3a): client config state"`.

---

## 3b: Backend Config – Storing & Retrieving JSON

**Question**: How does the server store URL/token (persistent across restarts)? We need a simple JSON file + load/save.

**Micro-Topic 1: Simple JSON File for Config**  
**Type This (create backend/config.py)**:

```python
# config.py - Server settings. What: JSON = easy read/write file.

from pathlib import Path
import json

CONFIG_FILE = Path("config.json")  // Path = cross-platform file handle.
```

**Inline 3D Explain**:

- **What**: Path = object for files (join, exists). json = parse/dump.
- **Why**: JSON = human-editable (open in editor). **Deep Dive**: Path vs string = safe (no /../ attacks). Resource: [Pathlib Docs](https://docs.python.org/3/library/pathlib.html) – 3min, "Basic use."
- **How**: Path("file.json") = absolute. Gotcha: No dir = current working—use absolute (Path.home() / "app" / "config.json"). **Alternative**: YAML = comments, but JSON = std.

**Try This (10s)**: Python console: `from pathlib import Path; p = Path("test.json"); p.write_text('{"url": "test"}')` → file created? `p.read_text()` → '{"url": "test"}'? Tweak: `json.loads(p.read_text())` → dict. Reflect: "Why Path? String 'test.json' breaks on Windows ('\t' = tab)."

**Micro-Topic 2: Load Config from File**  
**Type This (add to config.py)**:

```python
def load_config():
  if CONFIG_FILE.exists():
    with open(CONFIG_FILE, 'r') as f:  // 'r' = read.
      return json.loads(f.read())  // Parse string → dict.
  return {}  // Empty if new.
```

**Inline 3D Explain**:

- **What**: open = file handle, with = auto-close (no leak).
- **Why**: Load = "restore state" (URL from last save). **Deep Dive**: json.loads = safe (throws on bad JSON). Resource: [JSON Python](https://docs.python.org/3/library/json.html) – 2min, "loads/dumps."
- **How**: f.read() = string. Gotcha: UTF-8 default = special chars OK. **Alternative**: TOML = typed (numbers as int)—JSON = loose.

**Try This (15s)**: Console: `load_config()` → {} (new)? Write test.json → reload console → {'url': 'test'}? Tweak: Bad JSON ('{bad') → ValueError? Reflect: "Why with? Forget close = file locked."

**Micro-Topic 3: Save Config to File**  
**Type This (add to config.py)**:

```python
def save_config(data):
  with open(CONFIG_FILE, 'w') as f:  // 'w' = write (overwrite).
    f.write(json.dumps(data, indent=2))  // indent = pretty-print.
```

**Inline 3D Explain**:

- **What**: dumps = dict → string. indent=2 = readable (2 spaces/line).
- **Why**: Save = persist (reload = same). **Deep Dive**: indent = dev nice, minify for prod (indent=None). Resource: [dumps Options](https://docs.python.org/3/library/json.html#json.dump) – 2min, "indent."
- **How**: 'w' = create/overwrite. Gotcha: No dir = error—CONFIG_FILE.parent.mkdir(parents=True). **Alternative**: YAML dump = comments.

**Try This (20s)**: `save_config({"url": "save-test"}); load_config()` → {'url': 'save-test'}? Edit file manually → reload → changes? Tweak: No indent (`indent=None`) → compact JSON. Reflect: "Why dumps? write raw string = error-prone (escapes)."

**Inline Lens (SRP Integration)**: config.py = data only (no routes—endpoints imports). Violate? Save in route = test hard (mock file?).

**Mini-Summary**: JSON + Path = simple persist. Load/save = state round-trip.

**Git**: `git add backend/config.py && git commit -m "feat(step-3b): backend config JSON"`.

---

### 3c: Wiring Client to Server – Fetch & Form Submit

**Question**: How do we load config on panel open (fill form) and save on submit (POST to server)?

**Micro-Topic 1: Client Fetch for Load**  
**Type This (add to ui/config.js)**:

```javascript
export async function loadConfig() {
  try {
    const response = await fetch("/config"); // GET = read.
    if (!response.ok) throw new Error("Load failed");
    const data = await response.json(); // Parse → object.
    setConfig(data); // Update state.
    showNotification("Config loaded"); // Feedback.
  } catch (error) {
    showNotification(error.message, "error");
  }
}
```

**Inline 3D Explain**:

- **What**: fetch = request, json() = parse body.
- **Why**: Load = "pull from server" (fresh data). **Deep Dive**: await = "pause until done"—readable vs .then(). Resource: [MDN Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) – 3min, "GET example."
- **How**: /config = your endpoint. Gotcha: No headers = public (add auth later). **Alternative**: Cache in localStorage = offline, but stale risk.

**Try This (15s)**: Update main.js delegation: `case "config": loadConfig(); document.getElementById("configPanel").classList.toggle("translate-x-full"); break;`. Click Settings → notify "loaded"? Mock response in dev tools → see data? Tweak: Offline (Network off) → error. Reflect: "Why try/catch? Fetch fail = network down—graceful."

**Micro-Topic 2: Form Submit for Save**  
**Type This (add to ui/config.js)**:

```javascript
export async function saveConfig(form) {
  const formData = new FormData(form); // Extract fields.
  try {
    const response = await fetch("/config/gitlab", {
      method: "POST",
      body: formData,
    });
    if (!response.ok) throw new Error("Save failed");
    await loadConfig(); // Reload to confirm.
    showNotification("Saved!");
  } catch (error) {
    showNotification(error.message, "error");
  }
}
```

**Inline 3D Explain**:

- **What**: FormData(form) = read inputs (name= value). POST = write.
- **Why**: Save = "push to server" (persist for all users). **Deep Dive**: FormData = multipart (handles files later). Resource: [FormData MDN](https://developer.mozilla.org/en-US/docs/Web/API/FormData/FormData) – 2min, "From form."
- **How**: body = auto-type. Gotcha: No JSON = use JSON.stringify for objects. **Alternative**: Patch (PUT /config/url) = partial updates—overkill for full form.

**Try This (20s)**: Add to #configPanel form: `<button data-action="saveConfig" type="submit">Save</button>`. Update delegation: `case "saveConfig": await saveConfig(document.getElementById("configForm")); break;`. Fill input, click Save → notify? Backend mock return 200? Tweak: Bad response (edit fetch to throw) → error. Reflect: "Why reload after save? Confirm (state = server truth)."

**Inline Lens (Error Handling Integration)**: Catch = "plan for fail" (network = error notify). Violate? Unhandled = console dump—user confused.

**Mini-Summary**: Fetch + FormData = data round-trip. Load/save = state sync.

**Git**: `git add config.js && git commit -m "feat(step-3c): client-server config wiring"`.

---

### 3d: Validation & Error Polish (Robust Save)

**Question**: What if URL invalid or save fails (token bad)? Add client check + backend validate.

**Micro-Topic 1: Client Validation Before Save**  
**Type This (update saveConfig in ui/config.js)**:

```javascript
export async function saveConfig(form) {
  const url = form.querySelector("#gitlabUrl").value; // Get field.
  if (!url.startsWith("https://")) {
    // Simple check.
    showNotification("URL must be https", "error");
    return; // Early out.
  }
  const formData = new FormData(form);
  // ... rest from 3c.
}
```

**Inline 3D Explain**:

- **What**: querySelector = find by id. startsWith = string check.
- **Why**: Client validate = fast UX (no server round-trip). **Deep Dive**: Early return = "guard clause" (clean code). Resource: [Form Validation MDN](https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation) – 3min, "Client-side."
- **How**: form.querySelector = scope to form. Gotcha: No check = server error (slow). **Alternative**: HTML pattern attr = browser auto-validate.

**Try This (10s)**: Add id="gitlabUrl" to input. Submit bad URL (http://) → "URL must be https"? Good URL → proceeds? Tweak: Add token check (`if (!token) return;`). Reflect: "Why client? Instant feedback—server = backup."

**Micro-Topic 2: Backend Validation on Save**  
**Type This (create backend/endpoints.py, add route)**:

```python
# endpoints.py - Routes. What: Validate URL on POST.

from fastapi import Form, HTTPException

@router.post("/config/gitlab")
async def update_config(gitlab_url: str = Form(...), token: str = Form(...)):
  if not gitlab_url.startswith("https://"):  // Server check.
    raise HTTPException(status_code=400, detail="URL must be https")
  if not token:  // Basic.
    raise HTTPException(status_code=400, detail="Token required")
  # Save to JSON - paste from config.py later.
  return {"status": "saved"}
```

**Inline 3D Explain**:

- **What**: Form(...) = body extract. raise = FastAPI error (JSON response).
- **Why**: Server validate = secure (client tamper-proof). **Deep Dive**: HTTPException = auto 400 JSON ({"detail": "msg"}). Resource: [FastAPI Validation](https://fastapi.tiangolo.com/tutorial/body-fields/) – 3min, "Form models."
- **How**: startswith = string method. Gotcha: No check = bad data saved. **Alternative**: Pydantic model = auto-validate (type hints).

**Try This (15s)**: Backend run. Postman POST /config/gitlab (body: I gitlab_url=http://bad, token=ok) → 400 "URL must be https"? Good → 200? Tweak: Remove check → saves bad. Reflect: "Why server too? Client = fast, server = truth."

**Inline Lens (Validation Integration)**: Guard clauses = "fail fast" (early return on bad). Violate? Deep nesting = unreadable.

**Mini-Summary**: Client/server validate = layered (fast + secure). Errors = user-friendly.

**Git**: `git add endpoints.py && git commit -m "feat(step-3d): config validation"`.

---

**Step 3 Complete!** Settings load/save with checks. Reflect: "Full flow: Open panel → fetch → fill → validate → POST → reload. SRP: config.js = data, endpoints = API."

**Next**: Step 4: File Listing (fetch /files, render groups). Ready? Or "tweak Step 3 naming"? Typing mastery—keep going. 🚀
