# Step 16: Full Assembly & Run – Bringing It All Together (Integration Mastery – 1hr)

**Big Picture Goal**: Assemble the modular pieces into a complete, runnable app (frontend + backend). We'll go file-by-file, pasting snippets from previous steps, testing each (e.g., "Run npm test → green?"). Understand **integration** (modules wire without mess) and **end-to-end run** (local → full flow).

**Why Sixteenth?** (Integration Principle: **Whole Before Parts – System Test**). Pieces work isolated; now connect (auth → files → actions → sync). **Deep Dive**: Assembly = "dependency graph" (main imports all)—break one = trace. Why test per file? Catches wire bugs early. Resource: [Modular JS Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) – 3min, "Integration."

**When**: After all—prove modular pays (easy connect). Use for any (e.g., G-code: Assemble parse → validate → render).

**How**: Copy skeletons from earlier, paste snippets, run/test. Gotcha: Import typos = "not defined."

**Pre-Step**: Branch: `git checkout -b step-16-assembly`. Folders ready (ui/, backend/) from Step 0. Run backend `uvicorn app:app --reload`, frontend Live Server.

---

### 16a: Frontend Assembly – ui/ Files (30min)

**Question**: How do we wire all JS modules (main imports auth/config/etc.)? Start with utils (shared), add one-by-one, test.

**Micro-Topic 1: utils.js – Paste & Test Helpers**  
**Type This (create ui/utils.js – paste full from Step 1d)**:

```javascript
// utils.js - Helpers. What: Shared funcs (debounce, notify)—DRY across modules.

export function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

export function showNotification(message, type = "info") {
  const div = document.createElement("div");
  div.className = `fixed bottom-4 right-4 p-4 rounded shadow-lg z-50 ${
    type === "error" ? "bg-red-500" : "bg-blue-500"
  } text-white`;
  div.textContent = message;
  document.body.appendChild(div);
  setTimeout(() => div.remove(), 3000);
}

// Add formatBytes, formatDate, formatDuration from Step 4b.
export function formatBytes(bytes) {
  if (!bytes || bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

export function formatDate(dateString) {
  if (!dateString) return "Unknown";
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return "Invalid Date";
    const options = {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    };
    return date.toLocaleString(undefined, options);
  } catch (error) {
    console.error("Error formatting date:", dateString, error);
    return "Date Error";
  }
}

export function formatDuration(totalSeconds) {
  if (totalSeconds < 60) return `${Math.round(totalSeconds)}s`;
  const days = Math.floor(totalSeconds / 86400);
  totalSeconds %= 86400;
  const hours = Math.floor(totalSeconds / 3600);
  totalSeconds %= 3600;
  const minutes = Math.floor(totalSeconds / 60);
  let parts = [];
  if (days > 0) parts.push(`${days}d`);
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);
  return parts.join(" ") || "0m";
}
```

**Inline 3D Explain**:

- **What**: export = share (import in main). formatBytes = bytes to KB/MB.
- **Why**: DRY = no dup (formatDate in dashboard/fileManager). **Deep Dive**: log = math for units (1024 = binary K). Resource: [MDN Math.log](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/log) – 1min.
- **How**: toFixed(2) = decimal. Gotcha: bytes = 0 = "0 Bytes." **Alternative**: Intl.NumberFormat = locale (e.g., 1,000 KB).

**Try This (10s)**: Console: `import('./utils.js').then(u => console.log(u.formatBytes(1024)))` → "1 KB"? Tweak: 0 → "0 Bytes." Reflect: "Why export? main imports = use without copy."

**Inline Lens (DRY Integration)**: Utils = "once, use many" (change format = all update). Violate? Dup in files = bug fest.

**Mini-Summary**: Utils = shared tools. Export = module share.

**Micro-Topic 2: main.js – Import & Init Chain**  
**Type This (create ui/main.js – paste full from Step 1c + updates)**:

```javascript
// main.js - Orchestrator. What: Import + wire (delegation).

import { showNotification, debounce, formatDuration } from "./utils.js"; // Shared.
import { checkAuth, performLogin } from "./auth.js"; // Auth.
import { loadConfig, saveConfig } from "./config.js"; // Config.
import {
  loadFiles,
  renderFiles,
  checkoutFile,
  checkinFile,
} from "./fileManager.js"; // Files.
import { modalManager } from "./modalManager.js"; // UI popups.
import { connectWebSocket, handleWebSocketMessage } from "./websocket.js"; // Sync.
import { loadDashboardData } from "./dashboard.js"; // Admin.
import { initLazyTooltipSystem } from "./tooltipSystem.js"; // Hints.

window.appState = new Proxy(
  {},
  {
    // Reactive.
    set(target, prop, value) {
      target[prop] = value;
      if (prop === "files") renderFiles(value);
      return true;
    },
  }
);

export async function initApp() {
  showNotification("App starting...");
  applyThemePreference();
  if (!(await checkAuth())) {
    showNotification("Please login");
  } else {
    await loadConfig();
    connectWebSocket(handleWebSocketMessage);
    await loadFiles();
  }
  initLazyTooltipSystem();
}

document.addEventListener("DOMContentLoaded", initApp);

// Delegation - one listener.
document.addEventListener("click", async (e) => {
  const btn = e.target.closest("[data-action]");
  if (!btn) return;
  const { action, filename, username } = btn.dataset;
  switch (action) {
    case "login":
      document.getElementById("loginModal").classList.remove("hidden");
      break;
    case "submitLogin":
      await performLogin();
      break;
    case "config":
      await loadConfig();
      document
        .getElementById("configPanel")
        .classList.toggle("translate-x-full");
      break;
    case "saveConfig":
      await saveConfig(document.getElementById("configForm"));
      break;
    case "newFile":
      modalManager.open("newUpload");
      break;
    case "checkout":
      await checkoutFile(filename);
      break;
    case "submitCheckin":
      await checkinFile(filename);
      modalManager.close("checkin");
      break;
    case "dashboard":
      const data = await loadDashboardData();
      modalManager.open("dashboard", data);
      break;
    case "closeDashboard":
      modalManager.close("dashboard");
      break;
    case "refresh":
      await loadFiles();
      break;
    case "darkMode":
      toggleDarkMode();
      break;
    case "closeConfig":
      document.getElementById("configPanel").classList.add("translate-x-full");
      break;
    default:
      console.warn("Unknown:", action);
  }
});

// Search.
const searchInput = document.getElementById("searchInput");
if (searchInput) {
  searchInput.addEventListener(
    "input",
    debounce((e) => {
      const term = e.target.value.toLowerCase();
      renderFiles(appState.files, term);
    }, 150)
  );
}

function toggleDarkMode() {
  document.documentElement.classList.toggle("dark");
  localStorage.setItem(
    "theme",
    document.documentElement.classList.contains("dark") ? "dark" : "light"
  );
}

function applyThemePreference() {
  const savedTheme = localStorage.getItem("theme");
  if (
    savedTheme === "dark" ||
    (!savedTheme && window.matchMedia("(prefers-color-scheme: dark)").matches)
  ) {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }
}
```

**Inline 3D Explain**:

- **What**: import = pull modules. Proxy = trap.
- **Why**: Chain = sequential (auth → config → files). **Deep Dive**: Delegation = one listener (scale). Resource: [ES6 Imports](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import) – 2min.
- **How**: switch = route. Gotcha: Missing import = error. **Alternative**: Require = CommonJS—import = modern.

**Try This (20s)**: Refresh → "starting" toast? Login → config load? Tweak: Comment connectWebSocket → no WS. Reflect: "Why chain? Auth fail = no files (secure)."

**Inline Lens (SRP Integration)**: main = wiring (import + switch), modules = jobs.

**Mini-Summary**: Imports + chain = full init. Delegation = wire all.

**Git**: `git add main.js && git commit -m "feat(step-16a): main orchestrator"`.

---

### 16b: Backend Assembly – app.py & Modules (30min)

**Question**: How do we wire backend modules (app imports config/auth/endpoints)? Start with app.py, add one-by-one, test /config.

**Micro-Topic 1: app.py Skeleton**  
**Type This (create backend/app.py)**:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from .config import ConfigManager  // Import modules.
from .auth import UserAuth
from .endpoints import router

app_state = {}  // Shared.

@asynccontextmanager
async def lifespan(app: FastAPI):
  await initialize_application()  // Init.
  yield
  // Shutdown.

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"])

app.include_router(router)  // Wire routes.

async def initialize_application():
  app_state['config_manager'] = ConfigManager()
  app_state['user_auth'] = UserAuth(Path("."))  // Init auth.

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Inline 3D Explain**:

- **What**: @asynccontextmanager = startup/shutdown. include_router = add routes.
- **Why**: Lifespan = "app life" (init once). **Deep Dive**: app_state = DI (inject to routes). Resource: [FastAPI Lifespan](https://fastapi.tiangolo.com/advanced/events/#lifespan-event) – 2min.
- **How**: from . = relative. Gotcha: No yield = no shutdown. **Alternative**: No lifespan = init in route = slow.

**Try This (10s)**: `pip install -r requirements.txt && python app.py` → "Uvicorn running on http://0.0.0.0:8000"? /config → 503 (no data)? Reflect: "Why lifespan? Init = once (config load = expensive)."

**Micro-Topic 2: Add Config to Endpoints**  
**Type This (update backend/endpoints.py)**:

```python
from .app import app_state, router  // Import state.

@router.get("/config")
async def get_config():
  config_manager = app_state.get('config_manager')
  if config_manager:
    return config_manager.get_config_summary()  // From config.py.
  raise HTTPException(503, "Not initialized")
```

**Inline 3D Explain**:

- **What**: get = return dict.
- **Why**: Endpoint = API door (client fetch). **Deep Dive**: app_state.get = safe (no KeyError). Resource: [FastAPI GET](https://fastapi.tiangolo.com/tutorial/first-steps/#first-steps) – 1min.
- **How**: raise = error response. Gotcha: No if = crash. **Alternative**: Always return {} = silent fail.

**Try This (15s)**: Run backend, Postman GET /config → {"has_token": false}? Tweak: Mock return {"token": true} → updates. Reflect: "Why app_state? Shared = no param pass (DI)."

**Inline Lens (SRP Integration)**: endpoints = API, config = data. Violate? Get in endpoint = mixed.

**Mini-Summary**: app.py = wiring, endpoints = doors. app_state = shared.

**Git**: `git add app.py endpoints.py && git commit -m "feat(step-16b): backend assembly"`.

---

### 16c: Run & Test Full App (10min)

**Question**: How do we verify everything wires (login → files → checkout → dashboard)? Run both, end-to-end flow.

**Micro-Topic 1: Frontend Run**  
**Type This (terminal ui/)**:

```bash
# Live Server = auto-reload.
# Right-click index.html → "Open with Live Server" in VSCode.
# Or npx live-server . --port=5500
```

**Inline 3D Explain**:

- **What**: Live Server = local host + reload on save.
- **Why**: Test = "see changes live." **Deep Dive**: Port 5500 = avoid conflict. Resource: [VSCode Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) – 1min.
- **How**: . = current dir. Gotcha: No = manual F5. **Alternative**: BrowserSync = same.

**Try This (5s)**: Open → app loads? Click login → modal? Reflect: "Why live? Save = instant test—no F5."

**Micro-Topic 2: Backend Run & Flow Test**  
**Type This (terminal backend/)**:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Inline 3D Explain**:

- **What**: --reload = watch changes. host 0.0.0.0 = all IPs.
- **Why**: Run = "server up." **Deep Dive**: Port 8000 = standard. Resource: [Uvicorn Run](https://www.uvicorn.org/deployment/#running-programmatically) – 1min.
- **How**: app:app = module:class. Gotcha: No --reload = manual restart. **Alternative**: Gunicorn = prod (multi-worker).

**Try This (5min)**: Backend up? Frontend /config → JSON? Login → "Logged in!" Files → list? Checkout → "Locked" + re-render? Dashboard → table? Reflect: "Full flow = integrated (auth gates files)."

**Inline Lens (Deployment Integration)**: Local run = "simulate prod." Violate? No test = "works local, breaks deploy."

**Mini-Summary**: Live + uvicorn = full run. Flow test = wire check.

**Git**: `git add . && git commit -m "feat(step-16c): full app assembly + test"`.

---

**Tutorial Complete!** App engineered. Reflect: "Modular = easy change (add feature = new module). Principles = habits (SRP = clean)."

**Next?** Fixes (e.g., "full backups"), deploy, or new (G-code module)? You've mastered—iterate! 🚀
