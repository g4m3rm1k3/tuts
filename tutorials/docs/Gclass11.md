# Step 11: Error Handling & Testing – Robust & Verifiable Code (Resilience & Confidence – 1.5hr)

**Big Picture Goal**: Add comprehensive error handling (try/catch for fetches, validation for inputs, offline fallback) and basic testing (manual checks + simple Jest/pytest stubs for loadFiles/login). Understand **resilience** (code survives fails) and **verification** (tests prove it works).

**Why Eleventh?** (Resilience Principle: **Test After Build – Defense After Offense**). App runs; now make it unbreakable (fetch fail = notify, not crash) + provable (test loadFiles = green = trust). **Deep Dive**: Errors = "expected" (network = 50% apps fail first load). Testing = "prove assumptions" (manual = slow, automated = fast/regression-free). Resource: [MDN Error Handling](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Control_flow_and_error_handling) – 4min, "Try/catch" section.

**When**: After reactivity—state changes need safe. Use for prod (e.g., G-code parser: Test parse bad file = no crash).

**How**: Try/catch + guards (if !ok), offline listener. Tests: Jest for JS (npm i -D jest), pytest for Python (pip install pytest). Gotcha: Tests = slow if no mocks (fake fetch = fast).

**Pre-Step**: Branch: `git checkout -b step-11-errors-tests`. Install: Frontend `npm init -y && npm i -D jest` (add "test": "jest" to package.json). Backend `pip install pytest`. Add to main.js: `window.addEventListener("offline", () => showNotification("Offline", "error"));` (stub test).

---

### 11a: Client Error Handling – Graceful Fetches

**Question**: How do we handle fetch fails (network down, 404)? We need try/catch + user notify, not crash.

**Micro-Topic 1: Try/Catch Around Fetch**  
**Type This (update ui/fileManager.js loadFiles)**:

```javascript
export async function loadFiles() {
  try {
    // What: Block for "try this, catch fail."
    const response = await fetch("/files");
    if (!response.ok) throw new Error(`HTTP ${response.status}`); // Guard status.
    const data = await response.json();
    window.appState.files = data;
    renderFiles(data);
  } catch (error) {
    // Catch = all errors (network, parse).
    console.error("Load error:", error); // Log for dev.
    showNotification("Files failed—check network", "error"); // User msg.
    // Fallback UI.
    document.getElementById("fileList").innerHTML =
      "<p>Error loading—retry?</p>";
  }
}
```

**Inline 3D Explain**:

- **What**: try = attempt, catch = handle fail. throw = manual error.
- **Why**: Graceful = "fail safe" (notify vs blank). **Deep Dive**: Catch = broad (fetch reject = network, json = parse). Resource: [MDN Try/Catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch) – 2min, "Throw."
- **How**: Error obj = message. Gotcha: No catch = unhandled (console + crash). **Alternative**: .catch on fetch = same, but try = multi-line.

**Try This (10s)**: Refresh → loads? Dev tools Network → block /files → "Files failed" notify + fallback p? Tweak: Throw custom (`throw new Error("Mock")`) → same catch. Reflect: "Why console.error? Dev debug—user sees notify only."

**Inline Lens (Error Handling Integration)**: Try/catch = "expect fail" (network = common). Violate? No throw = parse bad JSON = crash.

**Mini-Summary**: Try/catch + throw = safe fetch. Notify = UX.

**Micro-Topic 2: Offline Detection Listener**  
**Type This (add to ui/main.js initApp)**:

```javascript
window.addEventListener("offline", (event) => {
  // What: Browser event on disconnect.
  showNotification("Went offline—some features limited", "warning");
  // Disable buttons or fallback.
});
window.addEventListener("online", (event) => {
  showNotification("Back online!");
  loadFiles(); // Re-try.
});
```

**Inline 3D Explain**:

- **What**: addEventListener("offline") = hook browser signal.
- **Why**: Proactive = "tell before ask" (fetch fail = expected). **Deep Dive**: navigator.onLine = hint (not always accurate—test with dev tools). Resource: [MDN Offline Event](https://developer.mozilla.org/en-US/docs/Web/API/Window/offline_event) – 2min, "Handler."
- **How**: event = optional (no use = fine). Gotcha: No listener = silent drop. **Alternative**: Ping interval = custom detect.

**Try This (15s)**: Dev tools Network → Offline → "Went offline"? Online → "Back" + re-load? Tweak: Add disable to buttons (e.dataset.disabled = true). Reflect: "Why online listener? Auto-recover = resilient."

**Inline Lens (Resilience Integration)**: Listener = "reactive to env" (offline = adapt). Violate? No detect = user "broken app."

**Mini-Summary**: Offline/online = env react. Auto-retry = smart.

**Git**: `git add fileManager.js main.js && git commit -m "feat(step-11a): client error handling + offline"`.

---

### 11b: Backend Error Handling – Validate & Respond

**Question**: How does backend handle bad requests (e.g., invalid filename)? We need HTTPException for 400/500 + logs.

**Micro-Topic 1: HTTPException for Validation**  
**Type This (update backend/endpoints.py checkout route)**:

```python
@router.post("/files/{filename}/checkout")
async def checkout_file(filename: str):
  if not filename.endswith(".mcam"):  // What: Guard input.
    raise HTTPException(status_code=400, detail="Invalid filename—must end .mcam")  // 400 = bad request.
  # ... lock logic.
  return {"status": "locked"}
```

**Inline 3D Explain**:

- **What**: raise HTTPException = auto-response (JSON error).
- **Why**: Validate = "bad in, no bad out" (crash-proof). **Deep Dive**: 400 = client fault, 500 = server. Resource: [FastAPI Exceptions](https://fastapi.tiangolo.com/tutorial/handling-errors/) – 2min, "HTTPException."
- **How**: detail = user msg. Gotcha: No raise = proceed bad = downstream crash. **Alternative**: if/return = manual JSON.

**Try This (10s)**: Postman POST /files/bad.txt/checkout → 400 "Invalid..."? Good .mcam → 200? Tweak: 500 = raise HTTPException(500, "Server error"). Reflect: "Why 400? Blame client—log 500 for dev."

**Micro-Topic 2: Logging for Debugging**  
**Type This (add to checkout_file)**:

```javascript
import logging
logger = logging.getLogger(__name__)  // What: Logger instance.

logger.info(f"Checkout {filename} by user")  // Log success.
# In try/catch around lock.
try:
  # Lock logic.
except Exception as e:
  logger.error(f"Checkout fail {filename}: {e}")  // Log fail.
  raise HTTPException(500, "Internal error")
```

**Inline 3D Explain**:

- **What**: logger.info/error = levelled log. **name** = module name.
- **Why**: Log = "past debug" (file: "Checkout fail: lock error"). **Deep Dive**: Levels = filter (info = normal, error = alert). Resource: [Python Logging](https://docs.python.org/3/tutorial/stdlib2.html#logging) – 3min, "Basic."
- **How**: f-string = format. Gotcha: No log = blind fail. **Alternative**: print = console only (log = file/email).

**Try This (15s)**: Run backend with logging (add basicConfig in app.py). POST bad → error log? Tweak: logger.warning("Suspicious filename") → mid-level. Reflect: "Why log? Console = ephemeral—file = persistent trace."

**Inline Lens (Debugging Integration)**: Log = "why failed?" (error + context). Violate? No log = "works on my machine" hell.

**Mini-Summary**: HTTPException = status error. Log = trace fail.

**Git**: `git add endpoints.py && git commit -m "feat(step-11b): backend validation + logging"`.

---

### 11c: Testing – Unit Tests for Functions

**Question**: How do we prove loadFiles works (fetch success = data set)? We need automated checks (run = green/red).

**Micro-Topic 1: Jest Setup for JS**  
**Type This (ui/package.json add)**:

```json
{
  "scripts": {
    "test": "jest"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}
```

**Inline 3D Explain**:

- **What**: scripts.test = run command. devDependencies = test-only.
- **Why**: Automate = fast/regression (change code = re-test). **Deep Dive**: Jest = matcher lib (expect = assert). Resource: [Jest Getting Started](https://jestjs.io/docs/getting-started) – 3min, "npm test."
- **How**: npm i -D = install dev. Gotcha: No = manual test (slow). **Alternative**: Mocha = similar, Jest = mocks easy.

**Try This (10s)**: Terminal ui/: `npm i -D jest && npm test` → "No tests"? Reflect: "Why dev? Prod no need—test = dev tool."

**Micro-Topic 2: Simple Unit Test for loadFiles**  
**Type This (create ui/fileManager.test.js)**:

```javascript
// fileManager.test.js - What: Test = "prove func works."

import { loadFiles } from "./fileManager.js"; // Import to test.

test("loadFiles sets data", async () => {
  // What: test = block.
  global.fetch = jest.fn(() =>
    Promise.resolve({
      // Mock fetch = fake response.
      ok: true,
      json: () => Promise.resolve({ files: "mock" }),
    })
  ); // Setup mock.
  await loadFiles(); // Run func.
  expect(window.appState.files).toBe("mock"); // Assert = check.
});
```

**Inline 3D Explain**:

- **What**: test = describe block. jest.fn = fake func.
- **Why**: Unit = isolate (mock fetch = no real server). **Deep Dive**: expect.toBe = matcher (== deep). Resource: [Jest Mocks](https://jestjs.io/docs/mock-functions) – 3min, "Async."
- **How**: global.fetch = override. Gotcha: No async test = wrong (await inside). **Alternative**: Manual console.assert = no auto-run.

**Try This (20s)**: ui/ `npm test` → "PASS 1 test"? Tweak: Change toBe("wrong") → FAIL? Reflect: "Why mock? Real fetch = server up—test anytime."

**Inline Lens (Testing Integration)**: Unit = "func alone" (mock deps). Violate? Integration = slow (server spin-up).

**Mini-Summary**: Jest test = prove + mock. Async = await inside.

**Git**: `git add package.json fileManager.test.js && git commit -m "feat(step-11c): unit tests setup"`.

---

### 11d: Integration Testing – Full Flows

**Question**: How do we test login + loadFiles together (end-to-end)? We need flow checks (click login → data loads).

**Micro-Topic 1: Simple Integration Test**  
**Type This (create ui/integration.test.js)**:

```javascript
// integration.test.js - What: Test flow (login → files).

test("login then load files", async () => {
  // Mock login success.
  global.fetch = jest
    .fn()
    .mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ token: "fake", username: "test" }),
    }) // /auth/login.
    .mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ files: "data" }),
    }); // /files.

  // Simulate click - stub.
  document.body.innerHTML = '<button data-action="login"></button>'; // Mock DOM.
  // Trigger delegation - call performLogin.
  await performLogin(); // From auth.js.

  expect(window.appState.currentUser).toBe("test"); // State updated.
  await loadFiles(); // Follow flow.
  expect(window.appState.files).toBe("data"); // End state.
});
```

**Inline 3D Explain**:

- **What**: mockResolvedValueOnce = fake response (once).
- **Why**: Integration = "flow works" (login sets token → files use). **Deep Dive**: Chain mocks = sequence. Resource: [Jest Sequential Mocks](https://jestjs.io/docs/mock-functions#mocking-modules) – 3min.
- **How**: innerHTML = mock DOM. Gotcha: No mock = real call. **Alternative**: Cypress = browser E2E (slower).

**Try This (15s)**: `npm test` → PASS? Tweak: Mock fail first → expect error. Reflect: "Why chain? Simulates real sequence (login before files)."

**Inline Lens (Testing Integration)**: Integration = "parts together." Violate? Unit only = misses flow bugs.

**Mini-Summary**: Mock chain = flow test. Sequence = real sim.

**Git**: `git add integration.test.js && git commit -m "feat(step-11d): integration tests"`.

---

**Step 11 Complete!** Errors handled, tests verify. Reflect: "Full: Try/catch = safe, offline = adapt, unit = prove func, integration = prove flow. SRP: Tests = separate (no prod code)."

**Next**: Step 12: Refactoring Round. Go? 🚀
