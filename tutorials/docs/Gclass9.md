# Step 9: Tooltips – UX Hints (Helpful Hover Guidance – 1hr)

**Big Picture Goal**: Add hover tooltips to buttons/inputs (e.g., "Search filters files"). JS attaches on mouseenter, shows popup with title/content, positions smart (top/bottom). Understand **progressive enhancement** (base UI works, hints = bonus UX).

**Why Ninth?** (Enhancement Principle: **Polish After Core – Accessibility Layer**). Files/actions/modals solid; now hints for discoverability (new user = "What's checkout?"). **Deep Dive**: Tooltips = "just-in-time help" (no clutter, on-demand). Why lazy? Attach only visible (perf—don't load for off-screen). Resource: [MDN Tooltip Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/ARIA_1.1/aria-describedby) – 3min, "Title vs custom."

**When**: After dashboard—UI complete, add niceties. Use for forms (e.g., G-code input: "Units in mm").

**How**: Mouse events + position calc, cache for reuse. Gotcha: Overflow = flip pos (top if bottom off-screen).

**Pre-Step**: Branch: `git checkout -b step-9-tooltips`. Add to a button: `title="Basic hint"` (native test). Create ui/tooltipSystem.js.

---

### 9a: Tooltip Data – Defining Hints

**Question**: How do we store what each element's hint says? We need a map of elem ID → {title, content, position}.

**Micro-Topic 1: Simple Object Map for Hints**  
**Type This (create ui/tooltipSystem.js)**:

```javascript
// tooltipSystem.js - Hover hints. What: Object = key-value hints.

const tooltips = {
  // Map = ID to hint.
  searchInput: {
    // Key = elem ID.
    title: "Search Files", // Short label.
    content: "Type to filter by name/path.", // Detail.
    position: "bottom", // Where to show.
  },
};
console.log(tooltips.searchInput); // Test lookup.
```

**Inline 3D Explain**:

- **What**: {key: value} = object. Nested = sub-obj.
- **Why**: Map = fast lookup (ID → hint). **Deep Dive**: Position = dir (top = above elem). Resource: [MDN Objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_Objects) – 2min, "As maps."
- **How**: console.log = inspect. Gotcha: Typo key = undefined. **Alternative**: Array = search slow (forEach).

**Try This (10s)**: Console: `import('./tooltipSystem.js')` → log {title: "...", ...}? Tweak: Add checkoutBtn: {title: "Lock File", ...} → logs new. Reflect: "Why object? Array = 'find by ID' loop—slow for 50 hints."

**Inline Lens (SRP Integration)**: tooltips = data only (no show logic—next). Violate? Add events here = mixed.

**Mini-Summary**: Object map = quick hint lookup. Nested = structured.

**Micro-Topic 2: Toggle Enabled Flag**  
**Type This (add to tooltipSystem.js)**:

```javascript
let tooltipsEnabled = localStorage.getItem("tooltipsEnabled") === "true"; // Load pref or false.

export function toggleTooltips() {
  tooltipsEnabled = !tooltipsEnabled; // Flip.
  localStorage.setItem("tooltipsEnabled", tooltipsEnabled); // Save.
  console.log("Tooltips:", tooltipsEnabled ? "on" : "off"); // Test.
}
```

**Inline 3D Explain**:

- **What**: === "true" = strict (string vs bool). ! = not.
- **Why**: Toggle = opt-in (perf/access). **Deep Dive**: localStorage = persist pref. Resource: [MDN Toggle](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Logical_NOT) – 1min.
- **How**: setItem = save. Gotcha: No save = forget on refresh. **Alternative**: No toggle = always on—user choice = better.

**Try This (15s)**: Console: `import('./tooltipSystem.js').then(t => { t.toggleTooltips(); t.toggleTooltips(); console.log(t.tooltipsEnabled); });` → false (back)? Tweak: localStorage.clear() → false default. Reflect: "Why save? Pref = user control—on = hints, off = clean."

**Inline Lens (User-Centric Integration)**: Enabled = accessibility (hints overload = off). Violate? Always on = assume user needs.

**Mini-Summary**: Flag + toggle = opt-in hints. localStorage = remember.

**Git**: `git add tooltipSystem.js && git commit -m "feat(step-9a): tooltip data + toggle"`.

---

### 9b: Attaching Listeners – Hover Events

**Question**: How do we show hint on hover? We need mouseenter/leave on elems with data-tooltip-key.

**Micro-Topic 1: Data Key on Elem**  
**Type This (add to index.html search input)**:

```html
<input
  id="searchInput"
  data-tooltip-key="searchInput"
  placeholder="Search..."
  class="px-4 py-2 border rounded"
/>
```

**Inline 3D Explain**:

- **What**: data-tooltip-key = flag + key (match map).
- **Why**: Key = lookup (id = searchInput → tooltips.searchInput). **Deep Dive**: Data = non-visual (no class bloat). Resource: [MDN Data Attr](https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes) – 2min, "Custom."
- **How**: dataset.tooltipKey = JS read. Gotcha: No key = no hint. **Alternative**: class="has-tooltip" = flag, but key = specific.

**Try This (10s)**: Refresh → inspect input → data-tooltip-key? Tweak: Change to "badKey" → no match later. Reflect: "Why data? class = style, data = logic."

**Micro-Topic 2: Mouse Events for Hover**  
**Type This (add to tooltipSystem.js)**:

```javascript
function attachTooltip(elem) {
  elem.addEventListener("mouseenter", () => {
    // What: Hover in.
    console.log("Hover on", elem.id); // Test.
  });
  elem.addEventListener("mouseleave", () => {
    // Hover out.
    console.log("Hover off", elem.id);
  });
}

// Attach to search.
const search = document.getElementById("searchInput");
attachTooltip(search);
```

**Inline 3D Explain**:

- **What**: addEventListener = hook event. mouseenter = cursor in.
- **Why**: Hover = "on-demand" (no clutter). **Deep Dive**: mouseleave = out (mouseenter = no bubble). Resource: [MDN Mouse Events](https://developer.mozilla.org/en-US/docs/Web/API/Element/mouseenter_event) – 2min, "vs mouseover."
- **How**: () => = no param. Gotcha: No attach = no event. **Alternative**: onmouseenter = inline—coupling bad.

**Try This (15s)**: Refresh → hover input → "Hover on searchInput"? Leave → "off"? Tweak: Add to button → works too. Reflect: "Why two events? Enter = show, leave = hide—complete cycle."

**Inline Lens (Performance Integration)**: Attach once = no dup listeners. Violate? Attach on every render = mem leak.

**Mini-Summary**: Events + attach = hover detect. mouseenter = in trigger.

**Git**: `git add tooltipSystem.js index.html && git commit -m "feat(step-9b): hover events + attach"`.

---

### 9c: Showing the Tooltip – Popup Creation

**Question**: How do we create the hint popup on hover? We need a div with content from map, positioned near elem.

**Micro-Topic 1: Create Popup Div**  
**Type This (add to tooltipSystem.js, update mouseenter)**:

```javascript
function showTooltip(event) {
  const elem = event.currentTarget; // Hovered elem.
  const key = elem.dataset.tooltipKey; // Lookup.
  if (!key) return; // Guard.

  const tooltip = document.createElement("div"); // New popup.
  tooltip.innerHTML = `<div class="p-2 bg-gray-800 text-white rounded shadow">${tooltips[key].content}</div>`; // Fill from map.
  document.body.appendChild(tooltip); // Global pos.
  console.log("Tooltip shown"); // Test.
}
```

**Inline 3D Explain**:

- **What**: currentTarget = listener elem. createElement = div.
- **Why**: Popup = temporary (append = show). **Deep Dive**: innerHTML = parse string (fast). Resource: [MDN createElement](https://developer.mozilla.org/en-US/docs/Web/API/Document/createElement) – 2min, "Dynamic."
- **How**: tooltips[key] = map access. Gotcha: No guard = crash on null. **Alternative**: Pre-create = mem waste (one per hint = 50 = OK).

**Try This (10s)**: Hover input → console "Tooltip shown," body has div? Leave → still there (hide next). Tweak: Add title: tooltips[key].title → <h4>${title}</h4>. Reflect: "Why body.append? Relative to elem = pos hard—body = absolute easy."

**Micro-Topic 2: Position Near Elem**  
**Type This (add to showTooltip after append)**:

```javascript
const rect = elem.getBoundingClientRect(); // Elem box (x/y/width/height).
tooltip.style.position = "absolute"; // Fixed pos.
tooltip.style.top = `${rect.bottom}px`; // Below elem.
tooltip.style.left = `${rect.left}px`; // Left align.
```

**Inline 3D Explain**:

- **What**: getBoundingClientRect = viewport coords. style = inline CSS.
- **Why**: Position = "near hover" (UX). **Deep Dive**: rect.bottom = elem bottom Y. Resource: [MDN getBoundingClientRect](https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect) – 2min, "Viewport."
- **How**: absolute = from parent (body = page). Gotcha: Scroll = wrong—add window.scrollY. **Alternative**: Transform translate = GPU fast.

**Try This (15s)**: Hover → tooltip below input? Scroll page → stays (fixed? Change to absolute + scrollY). Tweak: top = rect.top - tooltip.offsetHeight → above. Reflect: "Why rect? Hardcode px = breaks resize."

**Inline Lens (User-Centric Integration)**: Position = accessible (near focus). Violate? Center screen = hunt.

**Mini-Summary**: Create + position = visible hint. rect = coord smart.

**Git**: `git add tooltipSystem.js && git commit -m "feat(step-9c): tooltip show + position"`.

---

### 9d: Hiding & Cleanup – Event Cleanup

**Question**: How do we hide tooltip on leave? We need mouseleave + remove from DOM.

**Micro-Topic 1: Hide on Mouseleave**  
**Type This (add to attachTooltip, update mouseleave)**:

```javascript
elem.addEventListener("mouseleave", (event) => {
  const tooltip = document.querySelector(".tooltip"); // Find current.
  if (tooltip) tooltip.remove(); // Delete.
  console.log("Tooltip hidden"); // Test.
});
```

**Inline 3D Explain**:

- **What**: querySelector = find class. remove = delete node.
- **Why**: Hide = clean (no trail). **Deep Dive**: .tooltip = class (unique? Assume one active). Resource: [MDN Element.remove](https://developer.mozilla.org/en-US/docs/Web/API/Element/remove) – 1min.
- **How**: event not used = simple. Gotcha: Multiple = wrong one. **Alternative**: ID on tooltip = precise.

**Try This (10s)**: Hover/leave input → "shown/hidden," div appears/disappears? Tweak: Add class="tooltip" to div → targets. Reflect: "Why remove? Hide class = anim, but mem stays."

**Micro-Topic 2: Cleanup Listeners on Unhover**  
**Type This (add to attachTooltip)**:

```javascript
function attachTooltip(elem) {
  // ... events from 9b.
  elem.cleanup = () => {
    // Stored func = custom clean.
    elem.removeEventListener("mouseenter", showTooltip);
    elem.removeEventListener("mouseleave", hideTooltip);
  };
}
```

**Inline 3D Explain**:

- **What**: cleanup = stored method. removeEventListener = unhook.
- **Why**: Cleanup = mem safe (no leak on re-attach). **Deep Dive**: Listeners = refs (forget = slow page). Resource: [MDN removeEventListener](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/removeEventListener) – 2min, "Same func."
- **How**: Same func ref = match. Gotcha: Arrow vs named = diff refs. **Alternative**: No clean = leak (100 hovers = 100 listeners).

**Try This (15s)**: Hover multiple times → no dup logs? Tweak: Call elem.cleanup() in console → no more hover? Reflect: "Why stored? remove needs exact func ref."

**Inline Lens (Performance Integration)**: Cleanup = no leak. Violate? Page slow (listeners pile).

**Mini-Summary**: Leave + remove = hide clean. Stored cleanup = safe.

**Git**: `git add tooltipSystem.js && git commit -m "feat(step-9d): tooltip hide + cleanup"`.

---

**Step 9 Complete!** Hints hover/show/hide. Reflect: "Flow: Hover → attach event → create/pos → leave → remove/clean. SRP: tooltipSystem = hints only, modalManager = popups."

**Next**: Step 10: State Upgrade (Proxy). Go? 🚀
