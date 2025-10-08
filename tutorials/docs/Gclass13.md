# Step 13: Testing Suite – Proving & Protecting Code (Verification Layer – 1.5hr)

**Big Picture Goal**: Add automated tests for MVP (unit for utils/loadFiles, integration for login → render). Run `npm test` (JS) and `pytest` (Python) = green/pass. Understand **testing pyramid** (unit fast/isolated, integration slow/full-flow).

**Why Thirteenth?** (Verification Principle: **Test After MVP – Confidence Before Scale**). App works manually; tests = "prove it" (change code = re-test = safe). **Deep Dive**: Pyramid = "many unit (cheap), few integration (expensive)"—unit = func alone, integration = parts together. Why? Regression = "old bug returns"—tests catch. Resource: [Testing Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) – 5min, "Layers."

**When**: After refactor—prove no break. Use for any (e.g., G-code: Test parse good/bad input = no crash).

**How**: Jest for JS (mock fetch), pytest for Python (mock git). Gotcha: Mocks = fake deps (no real server).

**Pre-Step**: Branch: `git checkout -b step-13-testing`. Frontend: `cd ui && npm i -D jest @jest/globals` (add "test": "jest" to package.json). Backend: `pip install pytest`. Run `npm test` → "No tests"? `pytest` → same.

---

### 13a: Unit Testing JS – Isolate Funcs

**Question**: How do we test loadFiles alone (no real fetch)? We need mock fetch = fake response + expect data set.

**Micro-Topic 1: Jest Setup & Basic Test**  
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

- **What**: scripts.test = run cmd. devDependencies = test tools.
- **Why**: Setup = "automate run" (npm test = all green/red). **Deep Dive**: Jest = Node-based (no browser). Resource: [Jest Install](https://jestjs.io/docs/getting-started) – 2min, "npm."
- **How**: -D = dev-only (prod no). Gotcha: No = manual console. **Alternative**: Mocha = similar—Jest = easy mocks.

**Try This (10s)**: ui/ `npm i -D jest && npm test` → "No tests found"? Reflect: "Why dev? Prod = runtime, test = build-time."

**Micro-Topic 2: Unit Test for loadFiles**  
**Type This (create ui/fileManager.test.js)**:

```javascript
// fileManager.test.js - What: Unit = "func alone."

import { loadFiles } from "./fileManager.js"; // Import to test.
import { jest } from "@jest/globals"; // Global expect.

test("loadFiles fetches and sets data", async () => {
  // What: test block.
  const mockData = { Misc: [{ filename: "test.mcam" }] }; // Fake response.
  global.fetch = jest.fn(() =>
    Promise.resolve({
      // Mock = fake fetch.
      ok: true,
      json: () => Promise.resolve(mockData), // Return mock.
    })
  );

  await loadFiles(); // Run func.

  expect(window.appState.files).toBe(mockData); // Check = set?
  expect(global.fetch).toHaveBeenCalledWith("/files"); // Called right URL?
});
```

**Inline 3D Explain**:

- **What**: test = describe. jest.fn = fake func. expect.toBe = assert equal.
- **Why**: Unit = isolate (mock = no server). **Deep Dive**: toHaveBeenCalledWith = "called with args?" (prove intent). Resource: [Jest Mocks](https://jestjs.io/docs/mock-functions) – 3min, "Async."
- **How**: global.fetch = override. Gotcha: No await = test ends before run. **Alternative**: Manual if/throw = no auto-report.

**Try This (20s)**: `npm test` → PASS (1 test)? Tweak: Change toBe({wrong}) → FAIL + diff. Reflect: "Why mock? Real fetch = server up—test anytime/anywhere."

**Inline Lens (Testing Integration)**: Unit = "prove func" (mock deps = focus). Violate? No test = "works? Hope so."

**Mini-Summary**: Mock + expect = unit proof. Jest.fn = fake call.

**Git**: `git add package.json fileManager.test.js && git commit -m "feat(step-13a): JS unit tests"`.

---

### 13b: Integration Testing JS – Flows Like Login → Load

**Question**: How do we test login + loadFiles together (token set → files fetch)? We need mock sequence for full flow.

**Micro-Topic 1: Integration Test Setup**  
**Type This (create ui/integration.test.js)**:

```javascript
// integration.test.js - What: Integration = "parts together."

import { login, checkAuth } from "./auth.js";
import { loadFiles } from "./fileManager.js";

test("login then load files", async () => {
  // Flow test.
  // Mock login success.
  global.fetch = jest
    .fn()
    .mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ token: "fake", username: "test" }),
    }) // Login.
    .mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ files: "data" }),
    }); // Files.

  await login(); // Run login (mock inputs? Stub for now).

  expect(window.appState.currentUser).toBe("test"); // State set.

  await loadFiles(); // Follow with files.

  expect(window.appState.files).toBe("data"); // End result.
});
```

**Inline 3D Explain**:

- **What**: mockResolvedValueOnce = sequence (first login, second files).
- **Why**: Integration = "flow real" (login token → files use). **Deep Dive**: Chain = order (login before files). Resource: [Jest Sequential](https://jestjs.io/docs/mock-functions#sequential-mocks) – 2min.
- **How**: await = step. Gotcha: Wrong order = wrong mock. **Alternative**: Cypress = browser full (slower).

**Try This (15s)**: `npm test` → PASS? Tweak: Mock login fail (ok: false) → expect error? Reflect: "Why chain? Simulates real (auth first)."

**Inline Lens (Testing Integration)**: Integration = "system parts." Violate? Unit only = misses chain bugs.

**Mini-Summary**: Mock sequence = flow test. Await = step order.

**Git**: `git add integration.test.js && git commit -m "feat(step-13b): JS integration tests"`.

---

### 13c: Backend Testing with Pytest – Unit for Hash

**Question**: How do we test backend hash/verify alone? We need pytest mock for isolated func.

**Micro-Topic 1: Pytest Setup**  
**Type This (backend/pyproject.toml or just run)**:

```toml
# No file—pip install pytest.
# Run: pytest backend/test_auth.py
```

**Inline 3D Explain**:

- **What**: pytest = test runner (finds test\_\*.py).
- **Why**: Backend = separate verify (no frontend dep). **Deep Dive**: Discovery = auto (test\_ prefix). Resource: [Pytest Quickstart](https://docs.pytest.org/en/stable/getting-started.html) – 2min.
- **How**: pip install. Gotcha: No = manual run func. **Alternative**: unittest = stdlib—pytest = mocks easy.

**Try This (10s)**: `pip install pytest && pytest --version` → shows? Reflect: "Why pytest? Auto-discover = no boilerplate."

**Micro-Topic 2: Unit Test for Hash/Verify**  
**Type This (create backend/test_auth.py)**:

```python
# test_auth.py - What: Unit = func alone.

from auth import hash_password, verify_password  // Import to test.

def test_hash_verify():  // What: def test = pytest block.
  password = "secret"
  hashed = hash_password(password)  // Run hash.
  assert verify_password(password, hashed) == True  // Assert = check.
  assert verify_password("wrong", hashed) == False  // Fail case.
```

**Inline 3D Explain**:

- **What**: assert = if false = FAIL. def test = auto-run.
- **Why**: Prove = "hash round-trip works." **Deep Dive**: == True = explicit (pytest shows diff). Resource: [Pytest Assert](https://docs.pytest.org/en/stable/assert.html) – 2min, "Rewrite."
- **How**: No mock = pure func. Gotcha: No test = unproven. **Alternative**: print("pass") = no auto.

**Try This (20s)**: `pytest backend/test_auth.py` → "1 passed"? Tweak: Change "wrong" to "secret" → FAIL? Reflect: "Why assert? Manual print = no report—pytest = green/red + why."

**Inline Lens (Testing Integration)**: Unit = "prove hash" (no deps). Violate? No test = "works? Hope."

**Mini-Summary**: Pytest def test + assert = backend proof. Auto-run = easy.

**Git**: `git add test_auth.py && git commit -m "feat(step-13c): backend unit tests"`.

---

**Step 13 Complete!** MVP tested. Reflect: "Full: Errors caught, tests green—change safe. Pyramid: Unit = base, integration = top."

**Next**: Step 14: Full Forms & Uploads. Go? 🚀
