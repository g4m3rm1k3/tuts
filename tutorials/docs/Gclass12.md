# Step 12: Refactoring Round – Applying Principles (Code Improvement – 1.5hr)

**Big Picture Goal**: Refactor a "smelly" part (e.g., renderFiles—too long, mixed concerns) into smaller funcs (groupFiles, buildCard). Test before/after to see "clean smells better." Understand **refactoring** (improve code without changing behavior—safer, readable).

**Why Twelfth?** (Improvement Principle: **Refactor After Working – Polish the Diamond**). App runs; now "smells" (long funcs = hard change) = refactor time. **Deep Dive**: Refactor = "design debt paydown" (code debt = tech smells). Why test? Prove no break (red-green-refactor cycle). Resource: [Martin Fowler Refactoring](https://refactoring.com/) – 5min, "What is Refactoring?" (book free online).

**When**: After full app—smells emerge (e.g., 100-line renderFiles). Use for maint (e.g., G-code parser: Extract validate from parse).

**How**: Identify smell (long func), extract (new func), test (Jest before/after). Gotcha: No test = "works? Guess."

**Pre-Step**: Branch: `git checkout -b step-12-refactor`. Install Jest if not: `npm i -D jest`. Assume renderFiles is long (from Step 4)—we'll split.

---

### 12a: Spotting the Smell – Long Function Analysis

**Question**: How do we find "code smells" (e.g., renderFiles too long/mixed)? We need a way to measure (lines, concerns) before fix.

**Micro-Topic 1: Measure Current Code**  
**Type This (in ui/fileManager.js—assume long renderFiles from Step 4)**:

```javascript
// Smell: renderFiles = 50+ lines, loops + templates + events = mixed.
export function renderFiles(data = window.appState.files) {
  // ... long code from Step 4 (loops, html +=, etc.).
  console.log("renderFiles length:", renderFiles.toString().length); // Measure.
}
```

**Inline 3D Explain**:

- **What**: toString() = func as string. length = chars.
- **Why**: Measure = "quantify smell" (long = hard read). **Deep Dive**: Smells = "code hurt" (long = many reasons change). Resource: [Code Smells](https://refactoring.com/catalog/) – 2min, "Long Method."
- **How**: Console = quick. Gotcha: toString = source, minified = short. **Alternative**: ESLint "complexity" rule = auto-flag.

**Try This (10s)**: Refresh → console length > 500? Tweak: Comment half → shorter. Reflect: "Why measure? Gut 'long' = subjective—numbers = objective."

**Inline Lens (Maintainability Integration)**: Long = "many reasons change" (SRP violate). Fix = extract.

**Mini-Summary**: Measure = smell quantify. toString = code as data.

**Micro-Topic 2: List Concerns in Func**  
**Type This (add comment to renderFiles)**:

```javascript
export function renderFiles(data = window.appState.files) {
  // Concerns: 1. Fetch? No—loadFiles. 2. Group? Yes. 3. Template? Yes. 4. Inject? Yes. 5. Events? No—delegation.
  // Smell: 2-5 = mixed—split?
  // ... code.
}
```

**Inline 3D Explain**:

- **What**: Comment = note concerns (jobs func does).
- **Why**: List = "see overload" (SRP = one job). **Deep Dive**: SRP = "single reason change" (template change = only template func). Resource: [SRP Principle](https://en.wikipedia.org/wiki/Single-responsibility_principle) – 2min.
- **How**: // = line comment. Gotcha: No list = blind refactor. **Alternative**: Flowchart = visual smells.

**Try This (10s)**: Read comments → "Yes, mixed—group = one concern." Tweak: Add "6. Save state?" → more smells. Reflect: "Why list? Reveals 'god func' (does all)."

**Inline Lens (SRP Integration)**: Mixed = violate SRP (change group = test template). Fix = split.

**Mini-Summary**: Concern list = smell spot. SRP = one job.

**Git**: `git add fileManager.js && git commit -m "feat(step-12a): smell measure + list"`.

---

### 12b: Extracting a Sub-Func – Splitting the Load

**Question**: How do we break renderFiles (grouping logic too tangled)? Extract groupFiles to new func.

**Micro-Topic 1: Identify Extract Chunk**  
**Type This (in renderFiles, comment chunk)**:

```javascript
export function renderFiles(data = window.appState.files) {
  // Extract this: grouping loop.
  let groupedHtml = ""; // Temp for group.
  for (const groupName in data) {
    const files = data[groupName];
    groupedHtml += `<details><summary>${groupName}</summary><div>`; // Group shell.
    // ... file loop here.
    groupedHtml += "</div></details>";
  }
  // ... rest (inject).
}
```

**Inline 3D Explain**:

- **What**: Temp var = isolate chunk.
- **Why**: Extract = "pull out" (long = short funcs). **Deep Dive**: Chunk = "cohesive" (group = one job). Resource: [Extract Method Refactor](https://refactoring.com/catalog/extractMethod.html) – 2min.
- **How**: Comment = mark. Gotcha: No temp = cut-paste error. **Alternative**: Inline = tangled.

**Try This (10s)**: Run → same output? Tweak: Comment file loop → groups empty? Reflect: "Why temp? Safe isolate before move."

**Micro-Topic 2: Extract to New Func**  
**Type This (add to fileManager.js)**:

```javascript
function groupFiles(data) {
  // New: One job = group.
  let html = "";
  for (const groupName in data) {
    const files = data[groupName];
    html += `<details><summary>${groupName}</summary><div>`;
    // ... file loop (move from renderFiles).
    html += "</div></details>";
  }
  return html; // Output for use.
}

export function renderFiles(data = window.appState.files) {
  const fileList = document.getElementById("fileList");
  fileList.innerHTML = groupFiles(data); // Use new.
}
```

**Inline 3D Explain**:

- **What**: function = new. return = output string.
- **Why**: Extract = SRP (group = separate). **Deep Dive**: Test groupFiles alone = easy (mock data). Resource: [Refactor Extract](https://refactoring.com/catalog/extractMethod.html) – 2min, "Before/after."
- **How**: Move code = copy to new, delete old. Gotcha: Indent = break—VSCode format. **Alternative**: Inline = OK small, extract = scale.

**Try This (20s)**: Run → same groups? Console: `groupFiles({Misc: [{filename: 'test'}]})` → HTML string? Tweak: Bad data = empty? Reflect: "Why return? Render uses—loose coupling."

**Inline Lens (Maintainability Integration)**: Extract = readable (render = short). Violate? Long = "lost in scroll."

**Mini-Summary**: Extract = split job. New func = testable.

**Git**: `git add fileManager.js && git commit -m "feat(step-12b): extract groupFiles"`.

---

### 12c: Testing the Refactor – Before/After Proof

**Question**: How do we prove refactor no break (same output)? We need test before/after.

**Micro-Topic 1: Jest Test for Old Render**  
**Type This (create ui/fileManager.test.js)**:

```javascript
import { renderFiles, groupFiles } from "./fileManager.js"; // Import.

test("renderFiles groups data", () => {
  // What: Test = check output.
  document.body.innerHTML = '<div id="fileList"></div>'; // Mock DOM.
  const mockData = { Misc: [{ filename: "test.mcam" }] }; // Input.
  renderFiles(mockData); // Run.
  const list = document.getElementById("fileList").innerHTML; // Check.
  expect(list).toContain("Misc"); // Has group?
});
```

**Inline 3D Explain**:

- **What**: test = block. expect.toContain = matcher.
- **Why**: Before = baseline (prove works). **Deep Dive**: Mock DOM = isolate (no real page). Resource: [Jest DOM](https://jestjs.io/docs/dom-testing-library) – 3min, "innerHTML."
- **How**: innerHTML = get output. Gotcha: No mock = real elem error. **Alternative**: Snapshot = full HTML match.

**Try This (10s)**: `npm test` → PASS? Tweak: Change mockData → FAIL? Reflect: "Why expect? 'Works' = subjective—test = proof."

**Micro-Topic 2: Test New Extracted Func**  
**Type This (add test)**:

```javascript
test("groupFiles builds HTML", () => {
  const html = groupFiles({ Misc: [{ filename: "test.mcam" }] }); // Run isolated.
  expect(html).toContain("test.mcam"); // Has file?
  expect(html).toContain("<details>"); // Has group?
});
```

**Inline 3D Explain**:

- **What**: groupFiles = isolated call. toContain = substring check.
- **Why**: After = prove extract no break. **Deep Dive**: Unit = "func alone" (no DOM). Resource: [Jest Matchers](https://jestjs.io/docs/expect) – 2min, "toContain."
- **How**: No mock = pure. Gotcha: No test = "refactor broke? Guess." **Alternative**: Manual console.log(html) = no auto.

**Try This (15s)**: `npm test` → 2 PASS? Tweak: Bad data in mock → FAIL + fix. Reflect: "Why separate test? Render deps DOM—group = pure."

**Inline Lens (Testing Integration)**: Test before/after = "red-green-refactor" (fail → work → improve). Violate? No test = "it broke, whoops."

**Mini-Summary**: Before/after test = refactor safe. Isolated = unit.

**Git**: `git add fileManager.test.js && git commit -m "feat(step-12c): refactor tests"`.

---

**Step 12 Complete!** Refactored + tested. Reflect: "Smell fixed: Long func → small. Test = confidence (change = green). SRP: Group = one job, render = wire."

**Next**: Step 13: Testing Suite. Go? 🚀
