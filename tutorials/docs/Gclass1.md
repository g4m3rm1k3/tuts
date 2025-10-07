# Redone Steps 1 & 2: Masterclass Style (Micro-Bites, Typed Learning)

Absolutely—Step 3 nailed the sweet spot (question → snippet → explain → test → lens), so let's retro-fit Steps 1 & 2 the same way. This keeps the flow tight: **Question pose** (problem for curiosity), **1-3 line type** (muscle memory), **inline 3D** (what/why/how right after), **Try/Tweak** (10-20s hands-on), **inline Lens** (principle tie to code), **Mini-Summary** (1-line retain). Jargon? Plain (e.g., "dependencies = modules imported"). Density? One concept/micro. Visuals? Mermaid for flows.

Pre: Same setup (folder, Git branch `git checkout -b step-1-redo`). Type each snippet—test immediate. Ready? Let's rewind and rebuild.

---

# Step 1: UI Shell – From Blank Page to Clickable Prototype (Engineer Mindset: Design for Change – 1hr)

**Big Picture Goal**: Build a responsive page with header, main content, and settings panel. No data yet—just structure + one interactive button (Refresh). By end, you'll understand **separation of concerns** (HTML = structure, JS = behavior) and **event delegation** (one listener for many buttons).

**Why First?** (Foundation Principle: **Design Before Code – YAGNI in Action**). Every app needs a frame (header/main)—rush features = shaky base. **Deep Dive**: Separation = "HTML what, CSS how, JS when" (W3C layers). Why? Change style = no JS hunt. Resource: [MDN HTML Basics](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/HTML_basics) – 3min, "Structure" section.

**When**: Always—prototype layout before logic. Use for any UI (e.g., G-code viewer shell).

**How**: Semantic tags + Tailwind CDN. Gotcha: Viewport meta = mobile scale (shop tablet).

**Pre-Step**: Branch: `git checkout -b step-1-ui-redo`. Create empty `ui/index.html`, `ui/main.js`, `ui/utils.js`.

---

### 1a: The Blank Canvas – Semantic HTML Doctype & Head

**Question**: How do we tell browsers "use modern standards" and set up basics (charset, mobile zoom)? Without, page breaks on old browsers.

**Micro-Topic 1: Doctype & Basic Head**  
**Type This (start ui/index.html)**:

```html
<!DOCTYPE html>
<!-- What: Triggers standards mode. -->
<html lang="en">
  <!-- Lang = English—helps screen readers. -->
  <head>
    <!-- Head = meta, no body content. -->
    <meta charset="UTF-8" />
    <!-- UTF-8 = special chars (e.g., ° for degrees). -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <!-- Mobile: No auto-zoom. -->
    <title>Mastercam PDM</title>
    <!-- Tab text. -->
  </head>
</html>
```

**Inline 3D Explain**:

- **What**: Doctype = declaration (no tag). meta = key-value (charset = encoding).
- **Why**: Standards mode = consistent render (no IE quirks). Viewport = responsive (tablet = full size). **Deep Dive**: Without doctype = "quirks mode" (1990s bugs). Resource: [MDN Doctype](https://developer.mozilla.org/en-US/docs/Glossary/Doctype) – 2min, "Why HTML5?"
- **How**: lang="en" = i18n prep (translate later). Gotcha: No charset = mojibake (garbled text). **Alternative**: XHTML (strict tags)—dead, HTML5 = forgiving.

**Try This (10s)**: Save, Live Server → clean page (no title bar mess)? Tweak: Remove doctype → browser warns "quirks"? Reflect: "Why meta first? Head loads before body—fast basics."

**Inline Lens (SRP Integration)**: Head = setup only (no content—body owns that). Violate? Title in body = invalid HTML.

**Mini-Summary**: Doctype/head = "rules + setup"—consistent base.

---

### 1b: Body Structure – Header & Main Tags

**Question**: How do we stack header (nav) + main (content) full-height, without fixed pixels (breaks mobile)?

**Micro-Topic 1: Body with Semantic Tags**  
**Type This (add to index.html)**:

```html
<body>
  <!-- Body = visible content. -->
  <header>
    <!-- Semantic = "navigation section". -->
    <h1>Mastercam PDM</h1>
    <!-- Heading = hierarchy. -->
  </header>
  <main>
    <!-- Semantic = "primary content". -->
    Loading files...
  </main>
</body>
```

**Inline 3D Explain**:

- **What**: <header> = block for logos/nav. <main> = unique content (one per page).
- **Why**: Semantic = readable (engineers scan: "Ah, header"). Screen readers announce ("Heading: Mastercam"). **Deep Dive**: ARIA role="main" = explicit for old tools. Resource: [MDN Semantic HTML](https://developer.mozilla.org/en-US/docs/Glossary/Semantics) – 3min, "Why semantic?"
- **How**: No class = default styles. Gotcha: Multiple <main> = invalid (only one primary). **Alternative**: <div class="header"> = fast, but un-semantic (no announce).

**Try This (15s)**: Refresh → header above main? Add <footer>Test</footer> → stacks below? Tweak: Remove <header> tags → same look? (Yes—semantics invisible but useful). Reflect: "Why `<h1>`? Hierarchy—search engines rank it high."

**Inline Lens (Separation of Concerns Integration)**: HTML = "what" (structure). CSS = "how" (look). Violate? Inline style = tight coupling (change color = hunt HTML).

**Mini-Summary**: Semantic tags = self-documenting structure. One <main> = focus.

---

### 1c: Responsive Layout with Tailwind Flex

**Question**: How do we make it full-screen, stacked vertically, with scroll in main (header fixed)?

**Micro-Topic 1: Tailwind CDN & Flex Classes**  
**Type This (add to <head> + <body>)**:

```html
<head>
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- CDN = utility classes. -->
</head>
<body class="min-h-screen flex flex-col bg-gray-100">
  <!-- Full height, column stack. -->
  <header class="flex-shrink-0 bg-white shadow-md p-4">
    <!-- Fixed, no grow. -->
    <h1 class="text-xl font-bold">Mastercam PDM</h1>
  </header>
  <main class="flex-1 overflow-y-auto p-4">
    <!-- Grow to fill, scroll if big. -->
    Loading files...
  </main>
</body>
```

**Inline 3D Explain**:

- **What**: min-h-screen = full viewport. flex-col = vertical stack. flex-1 = grow (main fills).
- **Why**: Responsive = auto (no media queries yet). **Deep Dive**: Tailwind = atomic classes (p-4 = padding 1rem)—fast prototype. Resource: [Tailwind Flexbox](https://tailwindcss.com/docs/flexbox) – 3min, "flex-1" example.
- **How**: flex-shrink-0 = header fixed size. Gotcha: No flex = default block (margins add up). **Alternative**: CSS Grid = 2D layout—flex = 1D simple.

**Try This (20s)**: Refresh → full height? Resize window → stacks? Add long text to main → scroll (header stays)? Tweak: Remove flex-1 → main shrinks. Reflect: "Why overflow-y-auto? Content big = scroll, not stretch."

**Inline Lens (DRY Integration)**: Classes = reuse (p-4 = padding everywhere—no custom CSS copy). Violate? Per-elem style = bloat.

**Mini-Summary**: Flex + utilities = responsive stack. flex-1 = smart fill.

---

### 1d: Event Delegation – One Listener for All Buttons

**Question**: How do we wire clicks on buttons (e.g., "Settings") without a listener per button (scales bad for many)?

**Micro-Topic 1: Data Attributes for Intent**  
**Type This (add to header in index.html)**:

```html
<header>
  <button data-action="refresh">Refresh</button>
  <!-- Data attr = "intent flag". -->
  <button data-action="config">Settings</button>
</header>
```

**Inline 3D Explain**:

- **What**: data-action = custom HTML attr (dataset in JS).
- **Why**: Decouples (HTML = "what to do," JS = "how"). **Deep Dive**: Data attrs = standard (data-\*)—browsers ignore. Resource: [MDN Data Attributes](https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes) – 2min, "Accessing."
- **How**: dataset.action = JS read (camelCase). Gotcha: Typos = silent fail. **Alternative**: class="refresh-btn" = semantic, but data = explicit.

**Try This (10s)**: Refresh → buttons visible? Console: `document.querySelector('[data-action="refresh"]').dataset.action` = "refresh"? Tweak: Add data-filename="test.mcam" → dataset.filename. Reflect: "Why data-action? Button text change = no JS update."

**Micro-Topic 2: Delegation Listener on Document**  
**Type This (create ui/main.js)**:

```javascript
// main.js - Event wiring. What: One listener catches all data-action clicks.

document.addEventListener("click", (event) => {
  // Listen on document.
  const button = event.target.closest("[data-action]"); // Find nearest with attr.
  if (!button) return; // No match = ignore.
  const action = button.dataset.action; // Read intent.
  console.log(`Action: ${action}`); // Log for test.
});
```

**Inline 3D Explain**:

- **What**: addEventListener = hook event. closest = bubble up to attr.
- **Why**: Delegation = scalable (100 buttons = one listener). **Deep Dive**: Bubbling = event travels target → ancestors (unless stopPropagation). Resource: [MDN Bubbling](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events#bubbling_and_capturing) – 3min, demo.
- **How**: event.target = clicked elem. Gotcha: Nested buttons = closest finds outer. **Alternative**: Per-button = `button.addEventListener`—fine for 3, slow for 300.

**Try This (20s)**: Save, refresh → click Refresh → console "Action: refresh"? Click Settings → "config"? Add new button data-action="test" → logs? Tweak: Nested `<span> inside button` → still catches? Reflect: "Why document? Catches dynamic buttons (JS add = auto-wire)."

**Inline Lens (Coupling Integration)**: Low coupling—HTML intent, JS how. Violate? onclick="..." = tight (change JS = hunt HTML).

**Mini-Summary**: Delegation + data attrs = efficient wiring. One listener = scale.

**Git**: `git add main.js index.html && git commit -m "feat(step-1d): delegation listener"`.

---

**Step 1 Complete!** Clickable shell. Reflect: "Full: HTML structure → Tailwind layout → delegation wiring. SRP: Each micro = one job (e.g., 1d = events only)."

**Next**: Step 2: Auth (login state → backend hash → fetch wire → validate). Ready? 🚀
