# PDM Tutorial - Stage 4: State Management & UX Polish

**Prerequisites**: Completed Stage 3. Your app should lock/unlock files via API, update UI status, and log audits. Test: Checkout a file—status changes to "checked_out", locks.json updates.
**Time**: 4-5 hours
**What you'll build**: Centralized state (Observer pattern), toast notifications, search/filter/sort, reactive renders. _Incremental_: One method/property at a time, test with console/logs. **Tailwind**: Yes—classes like `bg-green-100 text-green-800` for toasts, `flex gap-4` for controls. Keeps pretty without custom CSS hell.

---

### Deep Dive: State Management Patterns (CS: Observer/Redux, SE: Reactivity)

**CS Topic**: State = data that changes UI (e.g., files list). Naive globals = bugs (stale data, race conditions, CS: shared mutable state hell). Observer pattern = pub-sub (subject notifies observers on change, CS: decoupling like events in OS). Redux = centralized store (immutable updates, time-travel debug). **App Topic**: Reactive UI = state change → auto-rerender (no manual DOM diffs). **SE Principle**: Single source of truth (avoid props drilling, like SOLID single responsibility). **Python/JS Specific**: JS Proxy/Reflect for reactivity (advanced), but we'll use subscribe/notify (simple, no deps). Gotcha: Re-renders = perf hit (memoize later).

Create `backend/static/js/modules/learn_state_management.js` (paste your original)—run in browser console or Node: Shows scattered vs centralized (subscribe notifies all).

---

### 4.1: Production Store Implementation (Build store.js Incrementally)

**Step 1: Create store.js Skeleton**

```bash
touch backend/static/js/modules/store.js
```

Paste:

```javascript
/**
 * Application State Store
 */
class Store {  # NEW: Observer class
  constructor(initialState = {}) {  # NEW
    this.state = initialState;  # NEW: Central data
    this.listeners = [];  # NEW: Subscribers
  }
}
```

- **Explanation**: Constructor = init (CS: factory). Listeners = array of callbacks (pub-sub queue).
- **Test**: In console: `import { Store } from './js/modules/store.js'; const s = new Store(); console.log(s.state);` → {}.
- **Gotcha**: {} spreadable (immutable updates later).

**Step 2: Add subscribe (Notify Setup)**
Add inside class:

```javascript
  subscribe(listener) {  # NEW: Add observer
    this.listeners.push(listener);  # NEW
    listener({ ...this.state });  # NEW: Immediate call + copy (immutable)
    return () => {  # NEW: Unsub
      const index = this.listeners.indexOf(listener);
      if (index > -1) this.listeners.splice(index, 1);
    };
  }
```

- **Explanation**: Push = O(1) add. {...state} = shallow copy (CS: immutability, avoid mutation bugs). Return unsub = cleanup (SE: resource management).
- **Test**: `s.subscribe((state) => console.log(state));` → Logs {}, unsub works (splice removes).
- **Gotcha**: Shallow copy—nested objects mutate (deep clone later).

**Step 3: Add \_notify (Private Publisher)**
Add:

```javascript
  _notify() {  # NEW: Private (underscore convention)
    const stateCopy = { ...this.state };  # NEW
    this.listeners.forEach((listener) => {  # NEW: Notify all
      try {
        listener(stateCopy);  # NEW
      } catch (error) {
        console.error("Error in listener:", error);  # NEW
      }
    });
  }
```

- **Explanation**: forEach = loop (CS: iteration). Try/catch = fault-tolerant (SE: one bad listener doesn't break all).
- **Test**: Subscribe two, setState (stub)—both called.
- **Gotcha**: forEach sync—async listeners need Promise.all later.

**Step 4: Add setState (Update & Notify)**
Add:

```javascript
  setState(newState) {  # NEW: Mutator
    this.state = { ...this.state, ...newState };  # NEW: Merge immutable
    this._notify();  # NEW
  }
```

- **Explanation**: ... = spread merge (CS: functional update). Calls notify (observer trigger).
- **Test**: `s.setState({files: []});` → Subscribers see {files: []}.
- **Gotcha**: Shallow—use immer for deep.

**Step 5: Add Actions (Named Updates)**
Add:

```javascript
  setLoading(loading = true) {  # NEW: Action
    console.log("ACTION: setLoading");  # NEW: Debug
    this.setState({ isLoading: loading, error: null });  # NEW
  }
  setFiles(files) {  # NEW
    console.log("ACTION: setFiles", files.length);
    this.setState({ allFiles: files, isLoading: false });
  }
  setError(error) {  # NEW
    console.log("ACTION: setError", error);
    this.setState({ error, isLoading: false });
  }
```

- **Explanation**: Actions = semantic (SE: intent over data). Logs = debug (CS: tracing).
- **Test**: s.setLoading() → Logs, state updates.

**Step 6: Add Computed (Derived State)**
Add:

```javascript
  getFilteredFiles() {  # NEW: Getter
    let result = [...this.state.allFiles];  # NEW: Copy
    if (this.state.searchTerm) {  # NEW: Filter
      const term = this.state.searchTerm.toLowerCase();
      result = result.filter((file) => file.name.toLowerCase().includes(term));
    }
    if (this.state.statusFilter !== "all") {  # NEW
      result = result.filter((file) => file.status === this.state.statusFilter);
    }
    return result;
  }
```

- **Explanation**: Getter = computed on-demand (CS: lazy eval, no stale). Spread/filter = immutable.
- **Test**: Set searchTerm="test", getFilteredFiles → Filters.
- **Gotcha**: ... = shallow copy array.

**Step 7: Add getDisplayFiles (Full Computed)**
Add:

```javascript
  getDisplayFiles() {  # NEW
    const filtered = this.getFilteredFiles();
    return this.getSortedFiles(filtered);  # Chain
  }
  getSortedFiles(files) {  # NEW
    const [field, direction] = this.state.sortBy.split("-");
    return [...files].sort((a, b) => {  # NEW
      let aVal = a[field] || 0, bVal = b[field] || 0;  # Stub
      const comparison = aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
      return direction === "asc" ? comparison : -comparison;
    });
  }
```

- **Explanation**: Chain = compose (functional). Sort stable (CS: comparator).
- **Test**: Set sortBy="name-asc", getDisplayFiles → Sorted.

**Step 8: Export Singleton**
Add:

```javascript
export const store = new Store({ isLoading: true });  # NEW: Instance with initial
```

- **Explanation**: Initial loading = good UX.
- **Test**: Import store—state has isLoading: true.

**Full store.js** (End of Section—Verify):

```javascript
/**
 * Application State Store
 */
class Store {
  constructor(initialState = {}) {
    this.state = initialState;
    this.listeners = [];
  }
  subscribe(listener) {
    this.listeners.push(listener);
    listener({ ...this.state });
    return () => {
      const index = this.listeners.indexOf(listener);
      if (index > -1) this.listeners.splice(index, 1);
    };
  }
  _notify() {
    const stateCopy = { ...this.state };
    this.listeners.forEach((listener) => {
      try {
        listener(stateCopy);
      } catch (error) {
        console.error("Error in listener:", error);
      }
    });
  }
  setState(newState) {
    this.state = { ...this.state, ...newState };
    this._notify();
  }
  setLoading(loading = true) {
    console.log("ACTION: setLoading");
    this.setState({ isLoading: loading, error: null });
  }
  setFiles(files) {
    console.log("ACTION: setFiles", files.length);
    this.setState({ allFiles: files, isLoading: false });
  }
  setError(error) {
    console.log("ACTION: setError", error);
    this.setState({ error, isLoading: false });
  }
  getFilteredFiles() {
    let result = [...this.state.allFiles];
    if (this.state.searchTerm) {
      const term = this.state.searchTerm.toLowerCase();
      result = result.filter((file) => file.name.toLowerCase().includes(term));
    }
    if (this.state.statusFilter !== "all") {
      result = result.filter((file) => file.status === this.state.statusFilter);
    }
    return result;
  }
  getSortedFiles(files) {
    const [field, direction] = this.state.sortBy.split("-");
    return [...files].sort((a, b) => {
      let aVal = a[field] || 0,
        bVal = b[field] || 0;
      const comparison = aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
      return direction === "asc" ? comparison : -comparison;
    });
  }
  getDisplayFiles() {
    const filtered = this.getFilteredFiles();
    return this.getSortedFiles(filtered);
  }
}
export const store = new Store({ isLoading: true });
```

**Verification**: Subscribe, setFiles([{}])—logs, filtered/sorted works.

### 4.2: Toast Notification System (Build toast.js Incremental)

**Step 1: Create toast.js**

```bash
touch backend/static/js/modules/toast.js
```

Paste:

```javascript
/**
 * Toast Notification System
 */
class ToastManager {  # NEW
  constructor() {  # NEW
    this.container = null;
    this.toasts = [];
    this.nextId = 1;
    this.init();  # NEW
  }
}
```

- **Explanation**: Manager = singleton (SE: global UI). toasts = array for queue.
- **Test**: Import—instance OK.

**Step 2: Add init (Container)**
Add:

```javascript
  init() {  # NEW
    if (!document.getElementById("toast-container")) {  # NEW
      this.container = document.createElement("div");
      this.container.id = "toast-container";
      this.container.className = "toast-container";
      document.body.appendChild(this.container);
    } else {
      this.container = document.getElementById("toast-container");
    }
  }
```

- **Explanation**: Append to body (CS: DOM insertion). Id check = idempotent.
- **Test**: Call init—<div id="toast-container"> added.
- **Gotcha**: Body = root (late append = flash).

**Step 3: Add show (Create Toast)**
Add:

```javascript
  show(message, type = "info", duration = 4000) {  # NEW
    const id = this.nextId++;
    const toast = document.createElement("div");  # NEW
    toast.className = `toast toast-${type}`;
    toast.dataset.toastId = id;
    const icons = { success: "✓", error: "✕", warning: "⚠", info: "ℹ" };
    toast.innerHTML = `
      <div class="toast-icon">${icons[type]}</div>
      <div class="toast-message">${message}</div>
      <button class="toast-close" aria-label="Close">&times;</button>
    `;
    const closeBtn = toast.querySelector(".toast-close");  # NEW
    closeBtn.addEventListener("click", () => this.dismiss(id));
    this.container.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add("toast-show"));  # NEW: Animate
    this.toasts.push({ id, element: toast, type });
    if (duration > 0) setTimeout(() => this.dismiss(id), duration);
    return id;
  }
```

- **Explanation**: innerHTML = quick (but escape message in prod). rAF = next frame (CS: smooth anim). SetTimeout = auto-dismiss.
- **Test**: toast.show("Test") → Toast appears.
- **Gotcha**: Dataset = custom attr (querySelector).

**Step 4: Add dismiss (Animate Out)**
Add:

```javascript
  dismiss(id) {  # NEW
    const toast = this.toasts.find((t) => t.id === id);
    if (!toast) return;
    toast.element.classList.remove("toast-show");
    toast.element.classList.add("toast-hide");
    setTimeout(() => {
      if (toast.element.parentNode) {
        toast.element.parentNode.removeChild(toast.element);
      }
      this.toasts = this.toasts.filter((t) => t.id !== id);
    }, 300);  # NEW: Delay for anim
  }
```

- **Explanation**: Find = O(n) search (fine for few toasts). Class toggle = CSS anim.
- **Test**: toast.show("Test"); toast.dismiss(1)—fades out.
- **Gotcha**: Timeout = anim duration match.

**Step 5: Add Convenience Methods**
Add:

```javascript
  success(message, duration) { return this.show(message, "success", duration); }  # NEW
  error(message, duration = 6000) { return this.show(message, "error", duration); }
  warning(message, duration) { return this.show(message, "warning", duration); }
  info(message, duration) { return this.show(message, "info", duration); }
```

- **Explanation**: Semantic wrappers (SE: intent-revealing).
- **Test**: toast.success("OK") → Green toast.

**Step 6: Export Singleton**
Add:

```javascript
export const toast = new ToastManager();  # NEW
```

- **Test**: Import toast.success("Hi")—shows.

**Step 7: Add Toast CSS (Tailwind + Custom)**
In `backend/static/css/input.css` (Tailwind):

```css
@layer base {
  #NEW: Base layer .toast-container {
    @apply fixed top-6 right-6 z-tooltip flex flex-col gap-3 max-w-md;
  }
  # NEW .toast {
    @apply flex items-center gap-3 p-4 bg-card border border-default rounded-lg shadow-lg transform translate-x-full opacity-0 transition-all;
  }
  # NEW .toast-show {
    @apply translate-x-0 opacity-100;
  }
  .toast-hide {
    @apply translate-x-full opacity-0;
  }
  .toast-icon {
    @apply text-xl font-bold flex-shrink-0 w-6 h-6 items-center justify-center;
  }
  .toast-message {
    @apply flex-1 text-sm text-primary;
  }
  .toast-close {
    @apply bg-none border-none text-xl text-secondary cursor-pointer p-0 w-6 h-6 flex items-center justify-center rounded-sm transition-all;
  }
  .toast-close:hover {
    @apply bg-secondary text-primary;
  }
  .toast-success {
    @apply border-l-4 border-success;
  }
  .toast-success .toast-icon {
    @apply text-success;
  }
  .toast-error {
    @apply border-l-4 border-danger;
  }
  .toast-error .toast-icon {
    @apply text-danger;
  }
  /* ... warning/info */
}
```

Rebuild: `npx tailwindcss -i input.css -o tailwind.css --minify`.

- **Explanation**: @layer base = after Tailwind base (order). @apply = compose (your custom to Tailwind).
- **Test**: toast.success("Test") → Pretty green toast with icon/close.
- **Gotcha**: border-l-4 = left 4 (Tailwind spacing).

**Full toast.js** (End of Section—Verify):

```javascript
/**
 * Toast Notification System
 */
class ToastManager {
  constructor() {
    this.container = null;
    this.toasts = [];
    this.nextId = 1;
    this.init();
  }
  init() {
    if (!document.getElementById("toast-container")) {
      this.container = document.createElement("div");
      this.container.id = "toast-container";
      this.container.className = "toast-container";
      document.body.appendChild(this.container);
    } else {
      this.container = document.getElementById("toast-container");
    }
  }
  show(message, type = "info", duration = 4000) {
    const id = this.nextId++;
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.dataset.toastId = id;
    const icons = { success: "✓", error: "✕", warning: "⚠", info: "ℹ" };
    toast.innerHTML = `
      <div class="toast-icon">${icons[type]}</div>
      <div class="toast-message">${message}</div>
      <button class="toast-close" aria-label="Close">&times;</button>
    `;
    const closeBtn = toast.querySelector(".toast-close");
    closeBtn.addEventListener("click", () => this.dismiss(id));
    this.container.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add("toast-show"));
    this.toasts.push({ id, element: toast, type });
    if (duration > 0) setTimeout(() => this.dismiss(id), duration);
    return id;
  }
  dismiss(id) {
    const toast = this.toasts.find((t) => t.id === id);
    if (!toast) return;
    toast.element.classList.remove("toast-show");
    toast.element.classList.add("toast-hide");
    setTimeout(() => {
      if (toast.element.parentNode) {
        toast.element.parentNode.removeChild(toast.element);
      }
      this.toasts = this.toasts.filter((t) => t.id !== id);
    }, 300);
  }
  success(message, duration) {
    return this.show(message, "success", duration);
  }
  error(message, duration = 6000) {
    return this.show(message, "error", duration);
  }
  warning(message, duration) {
    return this.show(message, "warning", duration);
  }
  info(message, duration) {
    return this.show(message, "info", duration);
  }
}
export const toast = new ToastManager();
```

**Verification**: toast.success("Test") → Fades in/out, pretty with Tailwind.

### 4.3: Add Search, Filter, Sort UI (Tailwind Controls)

**Step 1: Add Controls to index.html**
In <section> after <h2>:

```html
<div class="file-controls flex gap-4 mb-6 flex-wrap">
  # NEW: Tailwind
  <div class="form-group mb-0 flex-1 min-w-[200px]">
    # NEW
    <input
      type="search"
      id="file-search"
      placeholder="Search files..."
      class="w-full"
    />
    # NEW
  </div>
  <div class="form-group mb-0 min-w-[150px]">
    # NEW
    <select id="status-filter" class="w-full">
      <option value="all">All Files</option>
      <option value="available">Available Only</option>
      <option value="checked_out">Locked Only</option>
    </select>
  </div>
  <div class="form-group mb-0 min-w-[150px]">
    # NEW
    <select id="sort-select" class="w-full">
      <option value="name-asc">Name (A→Z)</option>
      <option value="name-desc">Name (Z→A)</option>
      <option value="size-desc">Size (Largest)</option>
      <option value="size-asc">Size (Smallest)</option>
      <option value="status-asc">Status (A→Z)</option>
    </select>
  </div>
</div>
<div id="results-info" class="text-sm text-secondary mb-4 py-2"></div>
# NEW
```

- **Explanation**: Flex gap = layout (Tailwind). mb-0 = no bottom margin on group.
- **Test**: Controls show, responsive wrap.
- **Gotcha**: min-w = prevent squash.

**Step 2: Wire Search/Filter in app.js**
In DOMContentLoaded, after loadFiles():

```javascript
document.getElementById("file-search").addEventListener("input", (e) => store.setSearchTerm(e.target.value));  # NEW
document.getElementById("status-filter").addEventListener("change", (e) => store.setStatusFilter(e.target.value));
document.getElementById("sort-select").addEventListener("change", (e) => store.setSortBy(e.target.value));
```

- **Add to store initial state**: `{ searchTerm: "", statusFilter: "all", sortBy: "name-asc" }`.
- **Explanation**: Input/change = real-time (JS: event-driven). setSearchTerm calls setState/notify.
- **Test**: Type in search—console logs, but no filter yet (render next).
- **Gotcha**: input = keystroke-by-keystroke (debounce later).

**Step 3: Update render in app.js (Use Computed)**
In render(state), replace displayFiles(allFiles):

```javascript
const displayFiles = store.getDisplayFiles();  # NEW: Computed
// ... resultsInfo with filteredCount = displayFiles.length
renderFileList(displayFiles, state.selectedFile);  # NEW: Pass computed
```

Add renderFileList:

```javascript
function renderFileList(files, selectedFile) {  # NEW
  const container = document.getElementById("file-list");
  container.innerHTML = "";
  if (files.length === 0) {
    container.innerHTML = '<div class="text-center py-8 text-secondary">No files match your search.</div>';
    return;
  }
  files.forEach((file) => {
    const element = createFileElement(file, selectedFile);  # Stub create
    container.appendChild(element);
  });
}
```

- **Explanation**: Computed = derive (CS: pure function). renderFileList = separate concern.
- **Test**: Set searchTerm="nonexistent" in console— "No files".
- **Gotcha**: ...files = copy (immutable).

**Step 4: Add createFileElement (Tailwind)**
Add:

```javascript
function createFileElement(file, selectedFile) {  # NEW
  const div = document.createElement("div");
  div.className = `file-item p-4 border border-default rounded-md flex justify-between items-center gap-4 bg-secondary transition-all ${selectedFile?.name === file.name ? 'border-primary bg-primary/10 translate-x-1' : ''}`;  # NEW: Tailwind
  div.onclick = (e) => { if (e.target.tagName !== "BUTTON") store.setSelectedFile(file); };  # NEW
  const infoDiv = document.createElement("div");
  infoDiv.className = "file-info flex items-center gap-4 flex-1";
  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name font-semibold text-primary";
  nameSpan.textContent = file.name;
  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status px-3 py-1 rounded-full text-xs font-medium ${file.status === 'available' ? 'bg-success/10 text-success' : 'bg-warning/10 text-warning'}`;
  statusSpan.textContent = file.status.replace("_", " ").toUpperCase();
  infoDiv.appendChild(nameSpan);
  infoDiv.appendChild(statusSpan);
  const actionsDiv = document.createElement("div");
  actionsDiv.className = "file-actions flex items-center gap-2";
  // Buttons stub
  const checkoutBtn = document.createElement("button");
  checkoutBtn.className = "btn btn-primary btn-sm";
  checkoutBtn.textContent = "Checkout";
  actionsDiv.appendChild(checkoutBtn);
  div.appendChild(infoDiv);
  div.appendChild(actionsDiv);
  return div;
}
```

- **Explanation**: Tailwind classes = atomic (e.g., flex gap-4 = layout). Conditional class = state (selected highlight).
- **Test**: loadFiles—files as pretty rows.
- **Gotcha**: ? = optional chaining (JS 2020).

**Step 5: Update resultsInfo**
In render:

```javascript
const totalFiles = state.allFiles.length;
const filteredCount = displayFiles.length;
resultsInfo.textContent =
  state.searchTerm || state.statusFilter !== "all"
    ? `Showing ${filteredCount} of ${totalFiles} files`
    : `${totalFiles} file${totalFiles !== 1 ? "s" : ""}`;
```

- **Explanation**: Ternary = conditional (CS: expression). Plural = i18n stub.
- **Test**: Filter—shows "Showing X of Y".

**Full app.js** (End of Section—Verify):
[Full code with store integration, render using computed, Tailwind in createFileElement]

**Verification**: Search/filter/sort—UI updates reactive. Toasts on error.

### Stage 4 Complete

**Test Full**: Search "PN", filter "available"—list filters/sorts. State changes trigger re-render.

**Verification**:

- [ ] Store subscribe notifies on setFiles.
- [ ] Computed filters/sorts.
- [ ] Toasts show on error.
- [ ] Tailwind pretty (no custom).

**What You Learned (Depth)**:

- **CS**: Observer (pub-sub), computed (memoization).
- **App**: Reactive renders (no manual DOM).
- **Python/JS**: Getters (lazy), forEach (iter).
- **SE**: Single truth (store), utilities (Tailwind).

Ready for Stage 5 (Auth)?
