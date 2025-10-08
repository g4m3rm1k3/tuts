# Step 10: State Upgrade – Proxy for Reactivity (Smart State – 1hr)

**Big Picture Goal**: Upgrade appState to a Proxy—automatic re-renders on changes (e.g., lock update → files re-paint). Wrap simple object in Proxy to trap sets (change files → call renderFiles). Understand **reactive state** (data changes trigger UI without manual).

**Why Tenth?** (State Principle: **Reactivity After Basics – Automation Layer**). Files/actions/WS work; now auto-update (no manual loadFiles everywhere). **Deep Dive**: Proxy = "trap operations" (set/get = hooks). Why? Manual calls = forget (stale UI); reactive = "set it and forget." Resource: [MDN Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy) – 4min, "Handler" section.

**When**: After WS—live data needs auto-UI. Use for apps (e.g., G-code live preview: Change param → re-render plot).

**How**: new Proxy({}, handler) with set trap (if prop = "files", render). Gotcha: Shallow—deep changes need recurse.

**Pre-Step**: Branch: `git checkout -b step-10-proxy`. Test manual: Change appState.files in console → no auto-render (yet).

---

### 10a: Understanding Simple State Limits

**Question**: How does current appState cause stale UI (e.g., WS updates files, but render not called)? We need to detect changes.

**Micro-Topic 1: Manual State Check**  
**Type This (add to ui/main.js initApp)**:

```javascript
window.appState = {}; // Simple object.

function updateUI() {
  // Manual trigger.
  console.log("UI updated"); // Stub render.
}

// Test manual.
appState.files = { test: [] }; // Change—no update.
updateUI(); // Call to refresh.
```

**Inline 3D Explain**:

- **What**: appState.files = assign. updateUI = call on change.
- **Why**: Simple = easy start. **Deep Dive**: Manual = explicit (know when change). Resource: [JS Objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_Objects) – 2min, "Assign."
- **How**: {} = empty. Gotcha: No notify = forget call (stale). **Alternative**: Array = ordered data—object = key lookup.

**Try This (10s)**: Refresh → console nothing? Set appState.files in console → no "updated"? Call updateUI → logs. Tweak: appState.user = 'test' → no trigger. Reflect: "Why manual? Control, but error-prone (forget = bug)."

**Inline Lens (SRP Integration)**: main.js = wiring (call updateUI), fileManager = data (loadFiles sets). Violate? Set + update in one = mixed.

**Mini-Summary**: Simple object = basic state. Manual call = explicit change.

**Micro-Topic 2: Problem of Forgotten Updates**  
**Type This (add to main.js)**:

```javascript
// Simulate forget.
appState.files = { new: [] }; // Change—no call.
console.log("State changed, UI stale?"); // Yes—manual miss.
```

**Inline 3D Explain**:

- **What**: = = mutate object.
- **Why**: Show limit (set = no auto). **Deep Dive**: Objects mutable = shared ref (change one place = all see). Resource: [MDN Mutability](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object) – 1min.
- **How**: {} ref = same. Gotcha: No trap = silent. **Alternative**: Immutable (spread copy) = safe, but verbose.

**Try This (10s)**: Console: appState.files = {updated: []}; → "stale" log? Reflect: "Why stale? No listener—manual = human error."

**Inline Lens (Performance Integration)**: Manual = optimize (call only needed). Violate? Auto on every set = over-render (slow).

**Mini-Summary**: Mutable = easy change. Forget call = stale bug.

**Git**: `git add main.js && git commit -m "feat(step-10a): simple state + manual update"`.

---

### 10b: Proxy Basics – Trapping Changes

**Question**: How do we "listen" to state changes without manual calls? We need Proxy to hook sets (change files → auto-render).

**Micro-Topic 1: Create Proxy Wrapper**  
**Type This (update ui/main.js appState)**:

```javascript
window.appState = new Proxy(
  {},
  {
    // What: Proxy = object wrapper with traps.
    set(target, prop, value) {
      // Trap set = "on change."
      target[prop] = value; // Do original.
      console.log(`Changed ${prop}:`, value); // Log trap.
      return true; // Success.
    },
  }
);
```

**Inline 3D Explain**:

- **What**: new Proxy = intercepted object. set = handler (prop = key, value = new).
- **Why**: Trap = auto-act (set files = log). **Deep Dive**: Handler methods = hooks (get/set/delete). Resource: [MDN Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy) – 3min, "set trap."
- **How**: {} = target (wrapped). return true = allow. Gotcha: No return = block set. **Alternative**: No proxy = manual (forget = bug).

**Try This (15s)**: Refresh → console nothing? `appState.files = {test: []};` → "Changed files: {test: []}"? Tweak: return false → set fails (console error). Reflect: "Why trap? Manual call = 'where to put?' Proxy = automatic."

**Inline Lens (SRP Integration)**: Proxy = state enhancer (no logic—trap calls render). Violate? Trap does render = tight (state = data only).

**Mini-Summary**: Proxy set trap = change detect. Log = proof.

**Micro-Topic 2: Route Trap to Action**  
**Type This (update set handler)**:

```javascript
set(target, prop, value) {
  target[prop] = value;
  if (prop === "files") {  // Specific key.
    renderFiles(value);  // Auto-call from fileManager.
  }
  return true;
}
```

**Inline 3D Explain**:

- **What**: if prop = "files" = conditional act.
- **Why**: Route = smart (files change = re-render). **Deep Dive**: Trap = "meta-programming" (JS intercepts ops). Resource: [Proxy Examples](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy/Proxy) – 2min, "Revocable."
- **How**: value = new (use it). Gotcha: Deep change (files[0].status) = no trap (shallow). **Alternative**: Deep proxy = recurse (complex).

**Try This (20s)**: Import renderFiles in main.js: `import { renderFiles } from './fileManager.js';`. Set appState.files = mock object → renderFiles called (console in render)? Tweak: if "user" = showNotification("User changed"). Reflect: "Why if? Trap all = over-act (user change = no re-render)."

**Inline Lens (Reactivity Integration)**: Trap = auto-update (data → UI). Violate? Manual everywhere = forget.

**Mini-Summary**: Conditional trap = targeted react. Specific prop = efficient.

**Git**: `git add main.js && git commit -m "feat(step-10b): proxy trap + route"`.

---

**Step 10 Complete!** State reactive. Reflect: "Upgrade: Manual call → proxy trap = auto. Flow: Set files → trap if → renderFiles. SRP: Proxy = enhancer, fileManager = render."

**Next**: Step 11: Error Handling & Testing. Go? 🚀
