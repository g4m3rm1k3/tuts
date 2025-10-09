# Step 3: Configuration – Loading & Saving Settings (User Preferences – 1hr)

**Big Picture Goal**: Build the settings panel where the user can enter their GitLab URL and token. The frontend loads the current settings from the backend, fills the form fields, and saves changes back when the user submits. By the end, you'll see how data flows from the server to the form (load) and back (save), and how to keep things safe with basic checks like "URL must start with https."

**Why Third?** (Data Principle: **Preferences Before Features – Personalize the House**). The shell and login from Steps 1-2 let users in; now they customize their "house" (GitLab connection for their repo). **Deep Dive**: Configuration is the "app's brain"—it holds user-specific choices like API keys, so the app adapts (your token = your files). Why load/save? Load = "remember last time," save = "update for next." Resource: [MDN on Local Storage for Prefs](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) – 3-minute read, the "Storing form data" example for why persist settings.

**When**: After login—users personalize post-auth. Use this for any app with options, like a G-code tool where users set units (mm/inch).

**How**: The frontend fetches /config to load, fills form inputs, and uses FormData to send changes to /config/gitlab on submit. The backend stores in a JSON file (simple "database"). Gotcha: Tokens are secrets—never log them plain (backend encrypts).

**Pre-Step**: Branch: `git checkout -b step-3-config`. Add a simple form to the #configPanel in index.html: `<form id="configForm"><input id="gitlabUrl" placeholder="GitLab URL (https://...)" class="block w-full mb-2 p-2 border rounded" /><input id="token" type="password" placeholder="Personal Access Token" class="block w-full mb-2 p-2 border rounded" /><button data-action="saveConfig" type="submit">Save</button></form>`.

---

### 3a: Client-Side Config State – Storing Preferences

**Question**: How do we keep the GitLab URL and token in one place so the form can read them and other parts of the app can use them? We need a simple storage spot for these settings.

**Micro-Topic 1: Simple Object for Config Storage**  
**Type This (create ui/config.js)**:

```javascript
// config.js - Holds app settings. What: Object = key-value storage for prefs.

let config = {}; // Empty object to start—filled on load.
```

**Inline 3D Explain**:

- **What**: `{}` = empty object (like a dictionary: key = "url", value = "https://...").
- **Why**: One spot = easy access (form reads config.url, no hunt). **Deep Dive**: Objects are mutable (change values without new object)—perfect for settings that update. Resource: [MDN JavaScript Objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_Objects) – 2-minute read, the "Object literals" section for why {} is simple storage.
- **How**: let = changeable (vs const = fixed). Gotcha: Refresh = lost (persist next). **Alternative**: Array = ordered list (good for files, bad for keys like "url"—slow lookup).

**Try This (10s)**: Open console (F12). Type `config = {url: 'https://test.com'}; console.log(config.url);` → "https://test.com"? Tweak: `config.token = 'secret'; console.log(config);` → {url: '...', token: 'secret'}. Reflect: "Why object? Keys like 'url' = fast find (config.url = instant)."

**Inline Lens (Single Responsibility Principle Integration)**: config.js = "settings storage only" (no form fill or save—that's later). If you violate this by adding a button here, the file does too many jobs (hard to test storage alone).

**Mini-Summary**: Empty object = simple key-value hold. let = ready for change.

**Micro-Topic 2: Helper Functions to Read & Write Config**  
**Type This (add to ui/config.js)**:

```javascript
export function getConfig() {
  // What: Read function.
  return config; // Return copy for use.
}

export function setConfig(newSettings) {
  // What: Write function.
  config = { ...newSettings }; // Copy keys from new.
  console.log("Config set:", config); // Test log.
}
```

**Inline 3D Explain**:

- **What**: getConfig = return object. setConfig = update with spread {...} (copy keys).
- **Why**: Helpers = "easy access" (call getConfig = no poke config directly). Spread = shallow copy (fast, changes newSettings don't affect old). **Deep Dive**: Export = share (main.js imports = use). Resource: [MDN Spread Operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) – 2-minute read, the "Object spread" example for copying.
- **How**: ...newSettings = "unpack keys" (url from new = url in config). Gotcha: Deep nests = shared ref (change nested = both change—JSON.parse/stringify for full copy). **Alternative**: config = newSettings = reference (change new = change config—bad).

**Try This (15s)**: Console: `import('./config.js').then(c => { c.setConfig({url: 'test.com'}); console.log(c.getConfig()); });` → {url: 'test.com'}? Tweak: `c.setConfig({url: 'new', token: 'secret'});` → updates. Reflect: "Why spread {...}? Direct = reference—new change = old breaks."

**Inline Lens (Don't Repeat Yourself Integration)**: Helpers = "one way to read/write" (no dup in main/config). Violate? Each file sets config = bugs on change (add version = fix all).

**Mini-Summary**: get/set helpers = safe access. Spread = copy without link.

**Git**: `git add config.js && git commit -m "feat(step-3a): client config state + helpers"`.

---

### 3b: Backend Config – Storing & Retrieving JSON

**Question**: How does the server store the URL and token so it remembers them between restarts? We need a simple file to save/load the settings.

**Micro-Topic 1: Simple JSON File for Storage**  
**Type This (create backend/config.py)**:

```python
# config.py - Server settings. What: JSON file = easy save/load.

from pathlib import Path  // What: Path = safe file handle (cross-platform).
import json  // What: JSON = parse/dump dicts.

CONFIG_FILE = Path("config.json")  // What: File name.
```

**Inline 3D Explain**:

- **What**: Path = object for files (like string but smarter). json = built-in for dict <-> string.
- **Why**: JSON = human-readable (open in editor = see "url": "https://..."). **Deep Dive**: Path vs plain string = no path attacks (../ = up dir). Resource: [Python Pathlib Docs](https://docs.python.org/3/library/pathlib.html) – 2-minute read, "Basic use" for why Path("file.json") is better than "file.json".
- **How**: Path("config.json") = current dir file. Gotcha: No dir = error (mkdir later). **Alternative**: YAML = comments (nice for humans), but JSON = standard (all langs support).

**Try This (10s)**: Terminal: `python -c "from pathlib import Path; p = Path('test.json'); p.write_text('{\"url\": \"test\"}'); print(p.read_text())"` → {"url": "test"}? Tweak: Change to 'bad.json' → writes. Reflect: "Why Path? String 'test.json' = Windows path break ('\t' = tab)."

**Inline Lens (Single Responsibility Principle Integration)**: config.py = "storage only" (no routes or UI—that's endpoints). If you violate this by adding a fetch here, the file does too much (hard to test save alone).

**Mini-Summary**: Path + json = file bridge. Human-readable = easy debug.

**Micro-Topic 2: Load Config from File**  
**Type This (add to backend/config.py)**:

```python
def load_config():  // What: Read function.
  if CONFIG_FILE.exists():  // Check file there.
    with open(CONFIG_FILE, 'r') as f:  // Open read.
      return json.loads(f.read())  // String → dict.
  return {}  // Empty if new.
```

**Inline 3D Explain**:

- **What**: exists() = check file. with open = auto-close file. loads = string to dict.
- **Why**: Load = "get saved" (URL from last time). **Deep Dive**: with = "context manager" (close even on error—no leak). Resource: [Python JSON](https://docs.python.org/3/library/json.html) – 2-minute read, "loads" for string parse.
- **How**: f.read() = full text. Gotcha: Bad JSON = ValueError (catch later). **Alternative**: TOML = typed (numbers = int)—JSON = loose (all string-ish).

**Try This (15s)**: Terminal: `python -c "from config import load_config; print(load_config())"` → {} (new)? Write config.json {"url": "test"} → reload terminal → {'url': 'test'}. Tweak: Bad JSON ('{bad') → error. Reflect: "Why with? Forget close = file locked (can't delete)."

**Inline Lens (Error Handling Integration)**: exists() = guard (no file = empty, no crash). Violate? Open missing = FileNotFoundError.

**Mini-Summary**: load_config = read or empty. with = safe open.

**Git**: `git add config.py && git commit -m "feat(step-3b): backend config load"`.

---

### 3c: Client-Server Wiring – Fetch Load & Form Save

**Question**: How do we pull config from backend to fill the form, and push changes back on submit? We need fetch for load and FormData for save.

**Micro-Topic 1: Client Fetch for Load**  
**Type This (add to ui/config.js)**:

```javascript
export async function loadConfig() {
  // What: Pull from server.
  try {
    const response = await fetch("/config"); // GET = read.
    if (!response.ok) throw new Error("Load failed"); // Check status.
    const data = await response.json(); // Text → object.
    setConfig(data); // Store.
    showNotification("Config loaded"); // Feedback.
  } catch (error) {
    showNotification(error.message, "error");
  }
}
```

**Inline 3D Explain**:

- **What**: fetch = request. json() = parse body to object.
- **Why**: Load = "get current" (fill form with saved URL). **Deep Dive**: !ok = 400/500 = throw (early fail). Resource: [MDN Fetch GET](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#fetch_with_get_headers_and_a_json_body) – 2-minute read, "GET example."
- **How**: /config = endpoint. Gotcha: No try = unhandled error (crash). **Alternative**: Cache in localStorage = offline load (stale risk).

**Try This (10s)**: Update main.js delegation: `case "config": await loadConfig(); document.getElementById("configPanel").classList.toggle("translate-x-full"); break;`. Click Settings → notify "Config loaded"? Backend mock /config = {"url": "test"} → console data? Tweak: Block /config → error. Reflect: "Why json()? Response = raw text—parse = usable object."

**Inline Lens (Async Integration)**: Await fetch = "pause until answer" (readable). Violate? .then() chain = hard follow (nest deep).

**Mini-Summary**: Fetch + json = load data. setConfig = store.

**Micro-Topic 2: Fill Form from State**  
**Type This (add to loadConfig after setConfig)**:

```javascript
document.getElementById("gitlabUrl").value = config.gitlab_url || ""; // What: Set input text.
document.getElementById("token").value = config.token || ""; // Same for token.
```

**Inline 3D Explain**:

- **What**: .value = set input's text.
- **Why**: Fill = "show saved" (user sees last URL). **Deep Dive**: || '' = empty if null (no blank input). Resource: [MDN Input Value](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/value) – 1-minute read.
- **How**: getElementById = find. Gotcha: Wrong ID = null error. **Alternative**: querySelector("[name='url']") = flexible.

**Try This (15s)**: Refresh → click Settings → form fields filled with mock data? Tweak: config = {gitlab_url: 'new'} in console → re-click → updates. Reflect: "Why .value? Input = elem, .value = what's shown—set = populate."

**Inline Lens (Single Responsibility Principle Integration)**: loadConfig = "data + fill" (state + UI tie). Violate? Save here = mixed (load = read only).

**Mini-Summary**: .value = form populate. || = safe empty.

**Git**: `git add config.js main.js && git commit -m "feat(step-3c): load + form fill"`.

---

### 3d: Saving Form – POST Back to Backend

**Question**: How do we send the form changes (URL/token) to the backend? We need to read the inputs and bundle them for the POST request.

**Micro-Topic 1: Read Form Inputs for Save**  
**Type This (add to ui/config.js)**:

```javascript
export async function saveConfig(form) {
  // What: Form param = the <form> elem.
  const urlInput = form.querySelector("#gitlabUrl"); // Find input.
  const tokenInput = form.querySelector("#token"); // Same for token.
  const url = urlInput.value; // Read text.
  const token = tokenInput.value;
  console.log("Saving:", url, token); // Test.
}
```

**Inline 3D Explain**:

- **What**: querySelector = find by ID. .value = current text.
- **Why**: Read = "get user changes" before send. **Deep Dive**: # = ID selector (fast). Resource: [MDN querySelector](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector) – 2-minute read, "ID selector."
- **How**: form.param = scope to form (no global hunt). Gotcha: Empty = '' (validate next). **Alternative**: getElementById = same, but query = flexible (class too).

**Try This (10s)**: Update main.js: `case "saveConfig": await saveConfig(document.getElementById("configForm")); break;`. Click Save → console "Saving: https://test.com secret"? Tweak: Fill form → logs values. Reflect: "Why querySelector? ID = unique—wrong = null crash."

**Micro-Topic 2: Bundle & POST with FormData**  
**Type This (add to saveConfig)**:

```javascript
const formData = new FormData(); // What: Bundle for POST.
formData.append("gitlab_url", url); // Add key-value.
formData.append("token", token);
try {
  const response = await fetch("/config/gitlab", {
    method: "POST",
    body: formData,
  }); // Send.
  if (!response.ok) throw new Error("Save failed");
  showNotification("Saved!");
  await loadConfig(); // Reload to confirm.
} catch (error) {
  showNotification(error.message, "error");
}
```

**Inline 3D Explain**:

- **What**: FormData = package. append = add pair. fetch POST = send.
- **Why**: POST = "update server" (body = safe for secrets). **Deep Dive**: FormData auto Content-Type multipart (handles text/files). Resource: [MDN FormData Append](https://developer.mozilla.org/en-US/docs/Web/API/FormData/append) – 2-minute read, "Sending to server."
- **How**: /config/gitlab = endpoint. Gotcha: No body = empty update. **Alternative**: JSON.stringify = text-only (no future files).

**Try This (20s)**: Fill form, click Save → "Saved!" + reload fills same? Backend mock /config/gitlab = 200 → yes? Tweak: Block endpoint → "Save failed." Reflect: "Why append? Key = backend expects—mismatch = ignore."

**Inline Lens (Error Handling Integration)**: Try/catch = "send safe" (fail = notify). Violate? No throw = silent fail (user thinks saved).

**Mini-Summary**: FormData + POST = change send. Reload = confirm.

**Git**: `git add config.js main.js && git commit -m "feat(step-3d): form save + POST"`.

---

**Step 3 Complete!** Settings load/fill/save. Reflect: "Full: Click config → load fetch → fill .value → submit read/bundle/POST → notify + reload. SRP: config.js = data, main = wire."

**Next**: Step 4: File Listing. Go? 🚀
