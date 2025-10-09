# Step 3: Config – Loading & Saving Settings (User Preferences – 1hr)

**Big Picture Goal**: Build the settings panel where the user can enter their GitLab URL and token. The frontend fetches the current settings from the backend, fills the form, and saves changes with a POST request. By the end, you'll see how user preferences flow from the server to the UI and back, keeping the app personalized across sessions.

**Why Third?** (Data Principle: **Preferences Before Features – State After Security**). Authentication from Step 2 secures the app; now add user settings (GitLab URL/token) to make it personal (e.g., connect to your repo). **Deep Dive**: Config = "app brain" (keys/values like URL = where data lives). Why JSON? Human-readable and easy to parse/save. Resource: [MDN on JSON in JavaScript](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON) – 3-minute read, the "Parsing" section for how browsers turn strings into objects.

**When**: After authentication—settings are user-specific (logged-in people have their own URL/token). Use this pattern for any app with preferences, like a G-code tool where users set units (mm/inch).

**How**: The frontend fetches GET /config to load, uses FormData to bundle form fields for POST /config/gitlab to save. The backend stores in a JSON file. Gotcha: Tokens are sensitive—encrypt them on save (plain = leak risk if file hacked).

**Pre-Step**: Branch: `git checkout -b step-3-config`. Add a simple form to the #configPanel in index.html (inside the panel div):

```html
<form id="configForm">
  <input
    id="gitlabUrl"
    placeholder="GitLab URL"
    class="block w-full mb-2 p-2 border rounded"
  />
  <input
    id="token"
    type="password"
    placeholder="Token"
    class="block w-full mb-2 p-2 border rounded"
  />
  <button data-action="saveConfig" type="submit">Save</button>
</form>
```

Create empty ui/config.js and backend/config.py.

---

### 3a: Client-Side Config State – Storing Preferences

**Question**: How do we keep the GitLab URL and token in one place so the app remembers them (e.g., for file fetches)? We need a simple object to hold the settings.

**Micro-Topic 1: Simple Object for Config Storage**  
**Type This (create ui/config.js)**:

```javascript
// config.js - Holds app settings. What: Object for key-value preferences.

let config = {}; // Empty object—filled on load.
```

**Inline 3D Explain**:

- **What**: `{}` = an object, like a dictionary (keys like "url" map to values like "`https://gitlab.com`").

- **Why**: One central spot = easy access (fileManager reads config.url—no hunting). **Deep Dive**: Objects are mutable (change keys anytime), great for settings that update (save new token = config.token = "new"). Resource: [MDN on JavaScript Objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_Objects) – 2-minute read, the "Creating objects" section for why {} is simple.
- **How**: let = changeable (config.url = "test" later). Gotcha: Refresh = lost (next micro fixes). **Alternative**: Array = ordered list (good for files, bad for "get url" lookup—slow search).

**Try This (10s)**: Open console (F12 > Console). Type `config = {url: 'test'}; console.log(config.url);` → "test"? Tweak: `config.token = 'secret'; console.log(config);` → {url: 'test', token: 'secret'}. Reflect: "Why object? Like a phone book—fast lookup by name (url), not number (array index)."

**Inline Lens (Single Responsibility Principle Integration)**: config.js = "settings storage only" (no fetch or UI yet—that's later). If you violate this by adding a button here, the file does too many jobs (hard to test storage alone).

**Mini-Summary**: Let object = changeable storage for prefs. {} = empty start.

**Micro-Topic 2: Helper Functions to Read/Write Config**  
**Type This (add to ui/config.js)**:

```javascript
export function getConfig() {
  return config; // What: Return a copy for reading.
}

export function setConfig(newConfig) {
  config = { ...newConfig }; // Spread = copy keys (shallow).
  localStorage.setItem("config", JSON.stringify(config)); // What: Save as string.
}
```

**Inline 3D Explain**:

- **What**: getConfig = getter (read). setConfig = setter (write + save). ... = spread (copy all keys from newConfig).
- **Why**: Helpers = "safe access" (call getConfig = no direct poke, easy to log/track). localStorage = persistence (survives refresh). **Deep Dive**: JSON.stringify turns object to string (storage needs strings); spread prevents mutating old (newConfig change = config safe). Resource: [MDN JSON.stringify](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify) – 2-minute read, the "Simple example" for object to string.
- **How**: export = share (import in main.js). Gotcha: No stringify = storage error (objects not strings). **Alternative**: No helpers = poke config directly = accidental changes (e.g., typo config.url = null).

**Try This (15s)**: Console: `import('./config.js').then(c => { c.setConfig({url: 'test'}); console.log(c.getConfig()); });` → {url: 'test'}? Refresh → still? Tweak: localStorage.clear() → next getConfig = {}. Reflect: "Why spread {...}? Without = reference (newConfig change = config changes too—bad)."

**Inline Lens (Don't Repeat Yourself Integration)**: Helpers = "write once, call from main/config" (change save = all update). Violate it by saving in every file = if you add expiry, fix everywhere.

**Mini-Summary**: get/set helpers + stringify = safe read/write. Spread = copy protect.

**Git**: `git add config.js && git commit -m "feat(step-3a): client config state + helpers"`.

---

### 3b: Backend Config – Storing & Retrieving JSON

**Question**: How does the server store the URL and token so it remembers them across restarts? We need a way to save to a file and load from it.

**Micro-Topic 1: Simple JSON File Path**  
**Type This (create backend/config.py)**:

```python
# config.py - Server settings. What: JSON file for persistent prefs.

from pathlib import Path  # What: Safe file paths (cross-OS).
import json  # What: Parse/dump objects.

CONFIG_FILE = Path("config.json")  # What: File name.
```

**Inline 3D Explain**:

- **What**: Path = file object (like string but smart). json = built-in for object/string convert.
- **Why**: JSON file = easy (text editor open, human read). **Deep Dive**: Path vs string = no /../ bugs (secure). Resource: [Python Pathlib Docs](https://docs.python.org/3/library/pathlib.html) – 2-minute read, "Basic use" for why it's better than os.path.
- **How**: "config.json" = current dir. Gotcha: No dir = error (next micro fixes). **Alternative**: YAML = comments (nice for docs), but JSON = standard (every lang supports).

**Try This (10s)**: Terminal: `python -c "from pathlib import Path; p = Path('test.json'); p.write_text('{\"url\": \"test\"}'); print(p.read_text())"` → {"url": "test"}? Tweak: p.write_text('bad') → still saves (no validate). Reflect: "Why Path? String 'test.json' = Windows \t tab error—Path = cross-OS."

**Inline Lens (Single Responsibility Principle Integration)**: config.py = "file handling only" (no routes—endpoints imports it). Violate it by adding a web server here = the file does too much (hard to test save alone).

**Mini-Summary**: Path + json = file setup. Safe paths = cross-OS.

**Micro-Topic 2: Load Config from File**  
**Type This (add to backend/config.py)**:

```python
def load_config():
  if CONFIG_FILE.exists():  # What: Check file there.
    with open(CONFIG_FILE, 'r') as f:  # 'r' = read mode.
      return json.loads(f.read())  # What: String to object.
  return {}  # What: Empty if new.
```

**Inline 3D Explain**:

- **What**: exists = bool check. with open = auto-close file. loads = parse string to dict.
- **Why**: Load = "get saved prefs" (URL from last). **Deep Dive**: with = "context manager" (forget close = leak). Resource: [Python with Statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement) – 2-minute read, "Auto cleanup."
- **How**: f.read() = full text. Gotcha: Bad JSON = ValueError (try/except next). **Alternative**: open/readlines = lines, but loads = easy object.

**Try This (15s)**: Terminal: `python -c "from config import load_config; print(load_config())"` → {} (new)? Write test.json {"url": "test"} → reload terminal → {'url': 'test'}. Tweak: Bad JSON in file ('{bad') → error. Reflect: "Why with? No = file open forever—leak memory."

**Inline Lens (Error Handling Integration)**: exists + {} = "fail soft" (no file = empty, not crash). Violate it with always open = file not found error.

**Mini-Summary**: load_config + with = safe read. {} = default.

**Micro-Topic 3: Save Config to File**  
**Type This (add to backend/config.py)**:

```python
def save_config(data):
  CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)  # What: Make dir if needed.
  with open(CONFIG_FILE, 'w') as f:  # 'w' = write/overwrite.
    f.write(json.dumps(data, indent=2))  # What: Object to pretty string.
```

**Inline 3D Explain**:

- **What**: mkdir = create folder. dumps = object to string (indent=2 = readable lines).
- **Why**: Save = "keep changes" (new token = persist). **Deep Dive**: parents=True = auto-parent folders (no manual). Resource: [JSON Dumps Options](https://docs.python.org/3/library/json.html#json.dump) – 2-minute read, "indent" for pretty.
- **How**: 'w' = create or replace. Gotcha: No mkdir = dir error. **Alternative**: 'a' = append = wrong (overwrites JSON).

**Try This (20s)**: Terminal: `python -c "from config import save_config; save_config({'url': 'test'}); from config import load_config; print(load_config())"` → {'url': 'test'}? Edit file manually {"url": "edit"} → reload → "edit." Tweak: No indent (indent=None) → compact one-line. Reflect: "Why dumps? Write raw string = escape hell (quotes in quotes)."

**Inline Lens (Don't Repeat Yourself Integration)**: save_config = "write once" (use from endpoints). Violate it by writing in every route = if change format, fix all.

**Mini-Summary**: save_config + mkdir + dumps = persist write. indent = readable.

**Git**: `git add config.py && git commit -m "feat(step-3b): backend config load/save"`.

---

### 3c: Client to Server Wiring – Fetch Load & Form Save

**Question**: How do we get the settings from the backend to fill the form, and send changes back? We need a button to load and one to save.

**Micro-Topic 1: Load Button to Fetch Config**  
**Type This (add to ui/index.html #configPanel after `<h2>`)**:

```html
<button
  data-action="loadConfig"
  class="bg-gray-500 text-white px-4 py-2 rounded mb-2"
>
  Load
</button>
```

**Inline 3D Explain**:

- **What**: data-action = flag for delegation (main.js catches).
- **Why**: Load = "pull current" (fill form from server). **Deep Dive**: Button = explicit (user clicks = fresh). Resource: [MDN Buttons](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button) – 1-minute read.
- **How**: mb-2 = margin bottom (Tailwind). Gotcha: No action = no JS. **Alternative**: Auto-load on open = surprise (button = control).

**Try This (10s)**: Save, refresh → Load button in panel? Tweak: Change text to "Refresh Settings" → updates. Reflect: "Why data-action? Delegation = one listener catches all—no per-button code."

**Inline Lens (Coupling Integration)**: Button = intent (load), config.js = how (fetch). Violate with onclick="load()" = button knows details.

**Mini-Summary**: Load button = fetch trigger. data-action = catch ready.

**Micro-Topic 2: Fetch to Load Config**  
**Type This (add to ui/config.js)**:

```javascript
export async function loadConfig() {
  try {
    const response = await fetch("/config"); // What: GET from backend.
    if (!response.ok) throw new Error(`Load failed: ${response.status}`); // Guard bad.
    const data = await response.json(); // What: Parse to object.
    setConfig(data); // Save to state.
    showNotification("Settings loaded"); // Feedback.
  } catch (error) {
    console.error("Load error:", error); // Dev log.
    showNotification("Load failed—try again", "error"); // User msg.
  }
}
```

**Inline 3D Explain**:

- **What**: fetch = request. json() = string to object.
- **Why**: Load = "get saved" (URL/token from backend). **Deep Dive**: !ok = 400/500 check (throw = bubble to catch). Resource: [MDN Fetch with Error Handling](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#handling_errors) – 2-minute read, the "try...catch" example.
- **How**: /config = endpoint. Gotcha: No try = crash on bad network. **Alternative**: No guard = parse 404 = extra error.

**Try This (15s)**: Update main.js delegation: `case "loadConfig": await loadConfig(); break;`. Open panel, click Load → "Settings loaded"? Backend mock /config = {"url": "test"} → state updates? Tweak: Block /config → "Load failed." Reflect: "Why json()? Response = raw string—parse = usable object."

**Inline Lens (Error Handling Integration)**: Try/catch = "plan for bad" (network = common). Violate? No throw = silent fail (user "why no load?").

**Mini-Summary**: fetch + json + setConfig = load flow. try = safe.

**Micro-Topic 3: Fill Form from State**  
**Type This (add to loadConfig after setConfig)**:

```javascript
document.getElementById("gitlabUrl").value = config.gitlab_url || ""; // What: Set input text.
document.getElementById("token").value = config.token || ""; // Same for token.
```

**Inline 3D Explain**:

- **What**: .value = set field text.
- **Why**: Fill = "show current" (user sees saved). **Deep Dive**: || '' = empty if null (no blank input). Resource: [MDN Input Value](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/value) – 1-minute read.
- **How**: ID = target. Gotcha: Wrong ID = no fill. **Alternative**: Loop all fields = dynamic (for 50 = good).

**Try This (10s)**: Click Load → form fills with mock data? Tweak: config = {gitlab_url: 'test'} in console → refresh load → 'test' in input. Reflect: "Why .value? Input = elem, .value = what's shown/edited."

**Inline Lens (Single Responsibility Principle Integration)**: loadConfig = "data + fill" (load = data, fill = UI—borderline SRP). Violate? UI in auth = mixed files.

**Mini-Summary**: .value = form fill. || = default empty.

**Git**: `git add config.js main.js index.html && git commit -m "feat(step-3c): config load + fill"`.

---

### 3d: Saving Form – POST Back to Backend

**Question**: How do we send the form changes (new URL/token) to the backend? We need to bundle the fields and POST them.

**Micro-Topic 1: Save Button to Bundle Form**  
**Type This (update ui/index.html configForm)**:

```html
<form id="configForm">
  <input
    id="gitlabUrl"
    placeholder="GitLab URL"
    class="block w-full mb-2 p-2 border rounded"
  />
  <input
    id="token"
    type="password"
    placeholder="Token"
    class="block w-full mb-2 p-2 border rounded"
  />
  <button
    data-action="saveConfig"
    type="submit"
    class="bg-green-500 text-white w-full p-2 rounded"
  >
    Save
  </button>
</form>
```

**Inline 3D Explain**:

- **What**: type="submit" = form send trigger. data-action = delegation flag.
- **Why**: Button = "intent to save" (submit = bundle all fields). **Deep Dive**: type="submit" = auto FormData from form. Resource: [MDN Submit Button](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#attr-type) – 1-minute read.
- **How**: w-full = full width. Gotcha: No type="submit" = no auto-bundle. **Alternative**: onclick = manual, but submit = standard.

**Try This (10s)**: Save, open panel → Save button? Tweak: Click without delegation → no action (yet). Reflect: "Why submit? Button click = send all inputs—no manual read."

**Micro-Topic 2: FormData to Bundle & POST**  
**Type This (add to ui/config.js)**:

```javascript
export async function saveConfig(form) {
  const formData = new FormData(form); // What: Bundle all fields auto.
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

- **What**: new FormData(form) = read all inputs (name=value). POST body = send bundle.
- **Why**: FormData = "easy package" (text + files later). **Deep Dive**: Auto Content-Type = multipart (fields separated). Resource: [MDN FormData with Form](https://developer.mozilla.org)
