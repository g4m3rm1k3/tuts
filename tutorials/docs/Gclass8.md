# Step 8: Dashboard – Stats & Activity Feed (Admin Insights – 1.5hr)

**Big Picture Goal**: Build the dashboard modal with active checkouts table and activity list. JS fetches /dashboard/stats and /dashboard/activity, renders responsive table/list with filter. Understand **admin views** (aggregated data for monitoring).

**Why Eighth?** (Insights Principle: **Observe Before Optimize – Analytics After Core**). Files/actions sync; now admin sees "who locked what" (table) + "recent changes" (feed). **Deep Dive**: Dashboard = "system pulse" (checkouts = conflict detect, activity = audit). Why paginate? Scale (1000 events = no load all). Resource: [MDN Tables](https://developer.mozilla.org/en-US/docs/Learn/HTML/Tables) – 4min, "Responsive tables."

**When**: After WS—live updates feed dashboard. Use for monitoring (e.g., G-code queue: "Who's editing?").

**How**: Promise.all for parallel fetches, template for table/list, select for filter. Gotcha: Sort client-side = fast for small, server for big.

**Pre-Step**: Branch: `git checkout -b step-8-dashboard`. Mock /dashboard/stats in endpoints.py: `@router.get("/dashboard/stats") async def stats(): return {"active_checkouts": [{"filename": "test.mcam", "locked_by": "user1", "duration_seconds": 3600}]}`. Mock /dashboard/activity: `@router.get("/dashboard/activity") async def activity(): return {"activities": [{"event_type": "CHECKOUT", "filename": "test.mcam", "user": "user1", "timestamp": "2023-01-01T00:00:00Z"}]}`. Add to delegation: `case "dashboard": openDashboard(); break;`.

---

### 8a: Dashboard Modal Shell – Opening the View

**Question**: How do we open a full-screen modal for dashboard (table + list)? We need a manager to inject shell + data later.

**Micro-Topic 1: Basic Modal Open with Shell**  
**Type This (update ui/modalManager.js open)**:

```javascript
open(type, data = {}) {
  const modal = document.createElement("div");  // New overlay.
  modal.className = "fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50";  // Full-screen.
  modal.innerHTML = '<div class="bg-white p-6 rounded shadow-lg w-full max-w-4xl max-h-[90vh] flex flex-col"><h3>Dashboard</h3><div id="dashboardContent">Loading...</div><button data-action="closeDashboard">&times;</button></div>';  // Shell.
  document.body.appendChild(modal);  // Add to page.
  this.openModals.push(modal);  // Track.
}
```

**Inline 3D Explain**:

- **What**: createElement = div. innerHTML = fill shell.
- **Why**: Shell = placeholder (load data inside). **Deep Dive**: max-w-4xl = responsive (small screen = fit). Resource: [MDN Flex Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox) – 2min, "justify-center."
- **How**: z-50 = above all. Gotcha: No flex = centered bad. **Alternative**: Position absolute = manual calc—flex = auto.

**Try This (10s)**: Add case "dashboard": modalManager.open('dashboard'); break; in main.js. Click Dashboard → modal with "Loading..."? Tweak: Add <div id="activeCheckouts">Table here</div> → sees ID? Reflect: "Why shell? Data load = async—show fast, fill later."

**Inline Lens (SRP Integration)**: open = UI shell only (data = next). Violate? Load data here = mixed.

**Mini-Summary**: Modal shell = quick open. Flex = responsive center.

**Micro-Topic 2: Close Button Wiring**  
**Type This (add to open, after appendChild)**:

```javascript
modal.addEventListener("click", (e) => {
  // Listen for close.
  if (e.target.dataset.action === "closeDashboard") {
    // Check attr.
    this.close(type); // Call close.
  }
});
```

**Inline 3D Explain**:

- **What**: addEventListener = hook. dataset.action = read attr.
- **Why**: Scoped = modal-only (not global). **Deep Dive**: e.target = exact click (button). Resource: [MDN Click Event](https://developer.mozilla.org/en-US/docs/Web/API/Element/click_event) – 2min, "Target."
- **How**: if = specific. Gotcha: No e.target = wrong elem. **Alternative**: onclick in HTML = inline coupling.

**Try This (15s)**: Click × → closes? Tweak: Change "closeDashboard" to "cancel" → no close (wrong attr). Reflect: "Why scoped listener? Global = catches everywhere—modal = contained."

**Inline Lens (Coupling Integration)**: Listener = modal life (close = remove). Violate? Global close = all modals.

**Mini-Summary**: Scoped click = close wire. Target = precise.

**Git**: `git add modalManager.js main.js && git commit -m "feat(step-8a): dashboard modal shell + close"`.

---

### 8b: Fetching Stats – Active Checkouts Table

**Question**: How do we get "locked files" data? Fetch /dashboard/stats parallel with activity, render table.

**Micro-Topic 1: Parallel Fetches with Promise.all**  
**Type This (add ui/dashboard.js)**:

```javascript
// dashboard.js - Admin views. What: Promise.all = parallel calls.

export async function loadDashboardData() {
  const [statsResponse, activityResponse] = await Promise.all([
    // Two fetches at once.
    fetch("/dashboard/stats"),
    fetch("/dashboard/activity"),
  ]);
  const stats = await statsResponse.json(); // Parse each.
  const activity = await activityResponse.json();
  console.log("Stats:", stats); // Test.
  return { stats, activity }; // Bundle for render.
}
```

**Inline 3D Explain**:

- **What**: Promise.all = array of promises → array of results.
- **Why**: Parallel = fast (2 calls = 200ms vs 400ms seq). **Deep Dive**: Await all = error if any fails (one down = stop). Resource: [MDN Promise.all](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all) – 2min, "Parallel."
- **How**: [fetch, fetch] = array. Gotcha: No await = race (wrong order). **Alternative**: Sequential await = slow.

**Try This (10s)**: Update main.js: `case "dashboard": const data = await loadDashboardData(); console.log(data); modalManager.open('dashboard', data); break;`. Click → console stats/activity? Tweak: One fetch fail (block /stats) → error? Reflect: "Why all? Independent = no wait."

**Inline Lens (Performance Integration)**: Parallel = "non-blocking" (UI smooth). Violate? Sequential = laggy.

**Mini-Summary**: Promise.all = fast multi-fetch. Await = ordered results.

**Micro-Topic 2: Render Checkouts Table**  
**Type This (add to dashboard.js)**:

```javascript
function renderCheckouts(stats) {
  const container =
    document.getElementById("activeCheckoutsContainer") ||
    document.createElement("div"); // Create if no.
  let html = '<table class="w-full border">'; // Basic table.
  html += "<thead><tr><th>File</th><th>User</th><th>Duration</th></tr></thead>"; // Headers.
  stats.active_checkouts.forEach((item) => {
    // Loop rows.
    html += `<tr><td>${item.filename}</td><td>${
      item.locked_by
    }</td><td>${formatDuration(item.duration_seconds)}</td></tr>`;
  });
  html += "</table>";
  container.innerHTML = html; // Inject.
  return container; // For append.
}
```

**Inline 3D Explain**:

- **What**: forEach = array loop. innerHTML = table build.
- **Why**: Table = structured data (rows = checkouts). **Deep Dive**: formatDuration from utils = DRY (reuse). Resource: [MDN Tables](https://developer.mozilla.org/en-US/docs/Learn/HTML/Tables/Basic_table) – 2min, "thead/tbody."
- **How**: w-full = width. Gotcha: No border = plain—add classes. **Alternative**: createElement = safe, slow (loop = 100 rows lag).

**Try This (15s)**: Update open in modalManager: `renderCheckouts(data.stats);` (append to #dashboardContent). Click Dashboard → table with rows? Tweak: Empty stats → no rows? Reflect: "Why forEach? Map = transform, forEach = side-effect (build)."

**Inline Lens (DRY Integration)**: formatDuration = shared (utils). Violate? Hardcode in render = dup on change.

**Mini-Summary**: forEach + template = table rows. innerHTML = quick inject.

**Git**: `git add dashboard.js && git commit -m "feat(step-8b): stats fetch + table"`.

---

### 8c: Activity Feed – List with Filter

**Question**: How do we show recent events (checkouts) in a list, filter by user? Fetch /dashboard/activity, render ul + select.

**Micro-Topic 1: Render Activity List**  
**Type This (add to dashboard.js)**:

```javascript
function renderActivity(activity) {
  const container =
    document.getElementById("activityFeedContainer") ||
    document.createElement("div");
  let html = '<ul class="space-y-2">'; // List shell.
  activity.activities.forEach((item) => {
    html += `<li class="p-2 border rounded">${item.user} checked out ${
      item.filename
    } at ${formatDate(item.timestamp)}</li>`; // Row.
  });
  html += "</ul>";
  container.innerHTML = html;
  return container;
}
```

**Inline 3D Explain**:

- **What**: ul/li = list. forEach = loop.
- **Why**: List = readable events. **Deep Dive**: formatDate = utils DRY. Resource: [MDN Lists](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ul) – 1min.
- **How**: space-y-2 = gaps. Gotcha: Empty = empty ul—add check. **Alternative**: Table = structured, list = flow.

**Try This (10s)**: Update open: `renderActivity(data.activity);`. Click → list items? Tweak: Add icon <i class="fa-solid fa-lock"></i> → styled. Reflect: "Why ul? Semantic = screen reader 'list of 3 items'."

**Micro-Topic 2: User Filter Select**  
**Type This (add before ul in renderActivity)**:

```javascript
const users = [...new Set(activity.activities.map((a) => a.user))]; // Unique users.
html +=
  '<select id="activityFilter" class="mb-2 p-1 border"><option value="all">All Users</option>'; // Select.
users.forEach((user) => (html += `<option value="${user}">${user}</option>`));
html += "</select>";
// Add listener after inject.
document.getElementById("activityFilter").addEventListener("change", (e) => {
  const filter = e.target.value;
  document.querySelectorAll("li").forEach((li) => {
    li.style.display =
      filter === "all" || li.textContent.includes(filter) ? "block" : "none"; // Hide/show.
  });
});
```

**Inline 3D Explain**:

- **What**: Set = unique. map = transform. addEventListener = wire change.
- **Why**: Filter = interactive (admin sees per-user). **Deep Dive**: includes = simple text match. Resource: [MDN Filter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter) – 2min, "String."
- **How**: value = option key. Gotcha: Case-sensitive—lowercase both. **Alternative**: Server filter = less data (big feed).

**Try This (20s)**: Click → select + list? Change "user1" → hides others? Tweak: All = show all. Reflect: "Why Set? Dup users = dup options."

**Inline Lens (Performance Integration)**: Client filter = fast (small data). Violate? Server for 10k = load all = slow.

**Mini-Summary**: List + select = feed + filter. Set = unique.

**Git**: `git add dashboard.js && git commit -m "feat(step-8c): activity list + filter"`.

---

**Step 8 Complete!** Dashboard fetches/renders. Reflect: "Flow: Open → parallel fetch → table/list inject → filter change → hide/show. SRP: dashboard.js = data/UI."

**Next**: Step 9: Tooltips (UX hints). Go? 🚀
