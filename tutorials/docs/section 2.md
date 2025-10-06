# PDM Tutorial - Stage 2: Professional Frontend Architecture

**Prerequisites**: Completed Stage 1. Your server should run with /api/files returning JSON. Test: `curl http://127.0.0.1:8000/api/files` → [] or files list.
**Time**: 4-5 hours
**What you'll build**: CSS system (ITCSS methodology), design tokens for theming, base styles, components, theme manager JS, basic HTML, API client, and app.js. _Incremental_: One file/section at a time, with small CSS/JS additions. Revisit Stage 0 structure (static/).

---

### Deep Dive: CSS Architecture & Design Systems (CS: Modular Design, SE: Scalability)

**CS Topic**: CSS as a language suffers from global namespace (one style sheet = specificity wars, like global variables in JS). ITCSS (Inverted Triangle CSS) = layered modularity (generic to specific, CS: dependency graph—base depends on nothing, components on base). **App Topic**: Design tokens = variables for consistency (e.g., --color-primary used everywhere—change once). **SE Principle**: DRY (Don't Repeat Yourself)—tokens avoid duplication. **Python/JS Specific**: CSS vars cascade (like JS props), JS modules (ES6 import/export) for theme logic.

Create `backend/static/css/learn_css_architecture.css` now (paste your original)—run `cat backend/static/css/learn_css_architecture.css` to read. Why? Primes for ITCSS layers.

---

### 2.1: Design Token System (Build tokens.css Incrementally)

**Step 1: Create tokens.css Skeleton**

```bash
touch backend/static/css/tokens.css
```

Paste root block:

```css
:root {
  /* NEW: Root vars cascade to all elements */
}
```

- **Explanation**: `:root` = HTML element (highest specificity, CS: global scope). Custom props (--var) = CSS vars (modern, runtime changeable via JS).
- **Test**: Link in placeholder `index.html`: `<link rel="stylesheet" href="css/tokens.css">` (create empty if needed). Inspect :root—no vars yet.
- **Gotcha**: --var names kebab-case (CSS convention).

**Step 2: Add Color Palette (One Scale)**
Inside :root:

```css
/* Primary Brand Color (NEW) */
--color-primary-50: #f5f7ff;
--color-primary-100: #ebf0ff;
--color-primary-200: #d6e0ff;
--color-primary-300: #b3c7ff;
--color-primary-400: #8da9ff;
--color-primary-500: #667eea; /* Main */
--color-primary-600: #5568d3;
--color-primary-700: #4453b8;
--color-primary-800: #353f8f;
--color-primary-900: #2a3166;
```

- **Explanation**: Tailwind-like scale (50=lightest, 900=darkest, CS: perceptual uniformity—human eyes see midtones better). Semantic (primary=brand).
- **App Revisit**: Ties to Stage 1 JSON (colors as data).
- **Test**: Add to `index.html` body: `<p style="color: var(--color-primary-500);">Test</p>`. Reload—blue text.
- **Gotcha**: Fallbacks (var(--color-primary-500, #000)) for old browsers.

**Step 3: Add Neutrals & Semantics (One Group)**
Add after primary:

```css
/* Neutral Grays (NEW) */
--color-gray-50: #fafafa;
--color-gray-100: #f5f5f5;
--color-gray-200: #e5e5e5;
--color-gray-300: #d4d4d4;
--color-gray-400: #a3a3a3;
--color-gray-500: #737373;
--color-gray-600: #525252;
--color-gray-700: #404040;
--color-gray-800: #262626;
--color-gray-900: #171717;
/* Semantic Colors (NEW) */
--color-success-500: #10b981;
--color-success-600: #059669;
--color-warning-500: #f59e0b;
--color-warning-600: #d97706;
--color-danger-500: #ef4444;
--color-danger-600: #dc2626;
--color-info-500: #3b82f6;
--color-info-600: #2563eb;
```

- **Explanation**: Neutrals for text/bgs (CS: grayscale perception). Semantics = meaning (success=green, app: accessible UX).
- **SE Revisit**: Single source (change --success once, all green).
- **Test**: `<p style="color: var(--color-success-500);">Success</p>` → Green.
- **Gotcha**: 500 = default shade (balance visibility/contrast).

**Step 4: Add Spacing Scale**
Add:

```css
/* Spacing Scale - Based on 4px (NEW) */
--spacing-1: 0.25rem; /* 4px */
--spacing-2: 0.5rem; /* 8px */
--spacing-3: 0.75rem; /* 12px */
--spacing-4: 1rem; /* 16px */
--spacing-5: 1.25rem; /* 20px */
--spacing-6: 1.5rem; /* 24px */
--spacing-8: 2rem; /* 32px */
--spacing-10: 2.5rem; /* 40px */
--spacing-12: 3rem; /* 48px */
--spacing-16: 4rem; /* 64px */
```

- **Explanation**: Rem-based (relative to font-size, CS: responsive). 4px base = modular (multiples for rhythm).
- **App Revisit**: Ties to Stage 1 JSON spacing.
- **Test**: `<div style="padding: var(--spacing-4);">Padded</div>` → 16px pad.
- **Gotcha**: Rem vs px (rem scales with user font settings, accessibility).

**Step 5: Add Typography (One Category)**
Add:

```css
/* Font Families (NEW) */
--font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue",
  Arial, sans-serif;
--font-mono: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas,
  "Courier New", monospace;
```

- **Explanation**: Sans = readable body (system fonts = fast, native look). Mono = code (fixed-width, CS: alignment for diffs).
- **Test**: `<body style="font-family: var(--font-sans);">Sans</body>` → System font.
- **Gotcha**: Fallback chain (if font missing).

**Step 6: Add Font Sizes/Weights**
Add:

```css
/* Font Sizes - Modular scale (1.25 ratio) (NEW) */
--font-size-xs: 0.75rem; /* 12px */
--font-size-sm: 0.875rem; /* 14px */
--font-size-base: 1rem; /* 16px */
--font-size-lg: 1.125rem; /* 18px */
--font-size-xl: 1.25rem; /* 20px */
--font-size-2xl: 1.5rem; /* 24px */
--font-size-3xl: 1.875rem; /* 30px */
--font-size-4xl: 2.25rem; /* 36px */
--font-size-5xl: 3rem; /* 48px */
/* Font Weights (NEW) */
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

- **Explanation**: Modular scale = golden ratio-ish (1.25x base, CS: harmonic proportions). Weights for hierarchy.
- **Test**: `<h1 style="font-size: var(--font-size-3xl); font-weight: var(--font-weight-bold);">Big Bold</h1>` → 30px bold.
- **Gotcha**: Rem = scalable (user zoom).

**Step 7: Add Line Heights & Radius/Shadows**
Add:

```css
/* Line Heights (NEW) */
--line-height-tight: 1.25;
--line-height-base: 1.5;
--line-height-relaxed: 1.75;
/* Border Radius (NEW) */
--radius-sm: 0.125rem; /* 2px */
--radius-base: 0.25rem; /* 4px */
--radius-md: 0.375rem; /* 6px */
--radius-lg: 0.5rem; /* 8px */
--radius-xl: 0.75rem; /* 12px */
--radius-full: 9999px; /* Pill */
/* Shadows (NEW) */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-base: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
```

- **Explanation**: Line-height = readability (1.5 = standard, CS: golden ratio for text). Radius = modern UI (app: accessibility—rounded reduces sharp edges). Shadows = depth (CSS: box-shadow, layers).
- **Test**: `<div style="box-shadow: var(--shadow-md); border-radius: var(--radius-lg);">Shadowed</div>` → Rounded shadow.
- **Gotcha**: RGBA opacity (0.1 = subtle, overdo = lag).

**Step 8: Add Transitions/Z-Index & Semantic Tokens**
Add:

```css
/* Transitions (NEW) */
--transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
/* Z-Index Scale (NEW) */
--z-dropdown: 1000;
--z-sticky: 1020;
--z-fixed: 1030;
--z-modal-backdrop: 1040;
--z-modal: 1050;
--z-popover: 1060;
--z-tooltip: 1070;
/* Semantic Tokens - Light Theme (NEW) */
--bg-primary: #ffffff;
--bg-secondary: var(--color-gray-50);
--text-primary: var(--color-gray-900);
--text-secondary: var(--color-gray-600);
--border-default: var(--color-gray-200);
--interactive-primary: var(--color-primary-500);
```

- **Explanation**: Cubic-bezier = easing (CS: bezier curves, smooth animation). Z-index = stacking (app: modal > backdrop). Semantics = aliases (e.g., --bg-primary = white light/dark switch later).
- **Test**: `<button style="transition: var(--transition-base);">Hover</button>` → Smooth.
- **Gotcha**: Z-index integers (avoid !important).

**Step 9: Close Root & Add Dark Theme**
Add after semantics:

```css
}  /* Close :root */

/* Dark Theme (NEW) */
[data-theme="dark"] {
  --bg-primary: var(--color-gray-900);
  --bg-secondary: var(--color-gray-800);
  --text-primary: var(--color-gray-50);
  --text-secondary: var(--color-gray-300);
  --interactive-primary: var(--color-primary-400);
}
```

- **Explanation**: [data-theme] attribute selector (JS sets, CSS responds). Overrides semantics (app: theming, revisit later).
- **Test**: `<html data-theme="dark"><body style="--bg-primary: black;">Dark</body></html>` in temp file—dark bg.
- **Gotcha**: Cascade order—dark after light.

**Full tokens.css** (End of Section—Verify):

```css
:root {
  /* Primary Brand Color */
  --color-primary-50: #f5f7ff;
  --color-primary-100: #ebf0ff;
  --color-primary-200: #d6e0ff;
  --color-primary-300: #b3c7ff;
  --color-primary-400: #8da9ff;
  --color-primary-500: #667eea;
  --color-primary-600: #5568d3;
  --color-primary-700: #4453b8;
  --color-primary-800: #353f8f;
  --color-primary-900: #2a3166;
  /* Neutral Grays */
  --color-gray-50: #fafafa;
  --color-gray-100: #f5f5f5;
  --color-gray-200: e5e5e5;
  --color-gray-300: #d4d4d4;
  --color-gray-400: #a3a3a3;
  --color-gray-500: #737373;
  --color-gray-600: #525252;
  --color-gray-700: #404040;
  --color-gray-800: #262626;
  --color-gray-900: #171717;
  /* Semantic Colors */
  --color-success-500: #10b981;
  --color-success-600: #059669;
  --color-warning-500: #f59e0b;
  --color-warning-600: #d97706;
  --color-danger-500: #ef4444;
  --color-danger-600: #dc2626;
  --color-info-500: #3b82f6;
  --color-info-600: #2563eb;
  /* Spacing Scale */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-3: 0.75rem;
  --spacing-4: 1rem;
  --spacing-5: 1.25rem;
  --spacing-6: 1.5rem;
  --spacing-8: 2rem;
  --spacing-10: 2.5rem;
  --spacing-12: 3rem;
  --spacing-16: 4rem;
  /* Font Families */
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  --font-mono: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas,
    "Courier New", monospace;
  /* Font Sizes */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;
  --font-size-4xl: 2.25rem;
  --font-size-5xl: 3rem;
  /* Font Weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  /* Line Heights */
  --line-height-tight: 1.25;
  --line-height-base: 1.5;
  --line-height-relaxed: 1.75;
  /* Border Radius */
  --radius-sm: 0.125rem;
  --radius-base: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-full: 9999px;
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-base: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  /* Transitions */
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
  /* Z-Index */
  --z-dropdown: 1000;
  --z-sticky: 1020;
  --z-fixed: 1030;
  --z-modal-backdrop: 1040;
  --z-modal: 1050;
  --z-popover: 1060;
  --z-tooltip: 1070;
  /* Semantic Tokens - Light Theme */
  --bg-primary: #ffffff;
  --bg-secondary: var(--color-gray-50);
  --text-primary: var(--color-gray-900);
  --text-secondary: var(--color-gray-600);
  --border-default: var(--color-gray-200);
  --interactive-primary: var(--color-primary-500);
}

/* Dark Theme */
[data-theme="dark"] {
  --bg-primary: var(--color-gray-900);
  --bg-secondary: var(--color-gray-800);
  --text-primary: var(--color-gray-50);
  --text-secondary: var(--color-gray-300);
  --interactive-primary: var(--color-primary-400);
}
```

**Verification**: Save, link in index.html, inspect—vars present, dark switches.

### 2.2: Base Styles (Build base.css Incrementally)

**Step 1: Create base.css**

```bash
touch backend/static/css/base.css
```

Paste reset:

```css
/* Reset & Box Model (NEW) */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
```

- **Explanation**: Box-sizing = include padding/border in width (CS: layout model, prevents surprises). \*::before/after = pseudo-elements.
- **Test**: Add to main.css `@import "base.css";`, <div style="width:100px; padding:10px;">Test</div> → 100px total (not 120).
- **Gotcha**: Default content-box = overflow issues.

**Step 2: Add HTML/Body Base**
Add:

```css
html {
  font-size: 100%; /* NEW: 1rem = 16px base */
  scroll-behavior: smooth;
  -webkit-font-smoothing: antialiased; /* NEW: Crisp text */
  -moz-osx-font-smoothing: grayscale;
}
body {
  font-family: var(--font-sans); /* NEW: Apply token */
  font-size: var(--font-size-base);
  line-height: var(--line-height-base);
  color: var(--text-primary);
  background-color: var(--bg-primary);
  transition: background-color var(--transition-base), color var(--transition-base); /* NEW: Theme smooth */
  overflow-x: hidden;
}
```

- **Explanation**: Font-size 100% = rem base (CS: relative units). Smoothing = subpixel rendering (app: legibility). Transition for theme (revisit tokens).
- **Test**: Body text = 16px sans-serif, white bg.
- **Gotcha**: Overflow-x hidden = no horizontal scroll (mobile).

**Step 3: Add Typography Hierarchy**
Add:

```css
/* Typography (NEW) */
h1,
h2,
h3,
h4,
h5,
h6 {
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  color: var(--text-primary);
  margin-bottom: var(--spacing-4);
}
h1 {
  font-size: var(--font-size-4xl);
  margin-bottom: var(--spacing-6);
}
h2 {
  font-size: var(--font-size-3xl);
  color: var(--interactive-primary);
}
h3 {
  font-size: var(--font-size-2xl);
}
h4 {
  font-size: var(--font-size-xl);
}
h5 {
  font-size: var(--font-size-lg);
}
h6 {
  font-size: var(--font-size-base);
}
p {
  margin-bottom: var(--spacing-4);
}
```

- **Explanation**: Hierarchy = visual scan (CS: tree traversal for eyes). Tokens for consistency.
- **Test**: `<h1>Test</h1><p>Para</p>` → Scaled, spaced.
- **Gotcha**: Margin-bottom on h1/p = vertical rhythm.

**Step 4: Add Links & Lists**
Add:

```css
/* Links (NEW) */
a {
  color: var(--text-link);
  text-decoration: none;
  transition: color var(--transition-fast);
}
a:hover {
  color: var(--text-link-hover);
  text-decoration: underline;
}
a:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}
/* Lists (NEW) */
ul,
ol {
  margin-bottom: var(--spacing-4);
  padding-left: var(--spacing-6);
}
li {
  margin-bottom: var(--spacing-2);
}
```

- **Explanation**: Focus-visible = keyboard users (accessibility, SE: inclusive design). Underline on hover = feedback.
- **Test**: `<a href="#">Link</a><ul><li>Item</li></ul>` → Blue, indented.
- **Gotcha**: Focus for a11y (screen readers).

**Step 5: Add Code & Forms**
Add:

```css
/* Code (NEW) */
code,
pre {
  font-family: var(--font-mono);
  font-size: 0.9em;
}
code {
  background: var(--bg-secondary);
  padding: 0.125rem 0.25rem;
  border-radius: var(--radius-sm);
  color: var(--color-danger-500);
}
pre {
  background: var(--bg-secondary);
  padding: var(--spacing-4);
  border-radius: var(--radius-base);
  overflow-x: auto;
  margin-bottom: var(--spacing-4);
}
pre code {
  background: none;
  padding: 0;
  color: inherit;
}
/* Forms (NEW) */
input,
textarea,
select,
button {
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
}
```

- **Explanation**: Inherit = consistent sizing (CS: cascade inheritance). Overflow-x = horizontal scroll for code.
- **Test**: `<code>code</code><pre>pre</pre><input type="text">` → Mono, inherited font.
- **Gotcha**: Inherit prevents zoom issues.

**Step 6: Add Media & Tables**
Add:

```css
/* Images & Media (NEW) */
img,
video,
svg {
  display: block;
  max-width: 100%;
  height: auto;
}
/* Tables (NEW) */
table {
  border-collapse: collapse;
  width: 100%;
}
th,
td {
  padding: var(--spacing-3);
  text-align: left;
  border-bottom: 1px solid var(--border-default);
}
th {
  font-weight: var(--font-weight-semibold);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

- **Explanation**: Block + max-width = responsive images (CS: fluid layout). Collapse = no double borders.
- **Test**: `<table><tr><th>Head</th></tr></table>` → Styled table.
- **Gotcha**: Width:100% on table = full-width.

**Step 7: Add Utilities**
Add:

```css
/* Utilities (NEW) */
.hidden {
  display: none !important;
}
.sr-only {
  /* Screen reader only */
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

- **Explanation**: !important for overrides (rare, CS: specificity 0,0,0,0). SR-only = accessible hidden (app: a11y, SE: WCAG).
- **Test**: `<span class="hidden">Hidden</span>` → Invisible.
- **Gotcha**: SR-only for labels (not display:none—screen readers ignore).

**Full base.css** (End of Section—Verify):

```css
/* Reset & Box Model */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
html {
  font-size: 100%;
  scroll-behavior: smooth;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
body {
  font-family: var(--font-sans);
  font-size: var(--font-size-base);
  line-height: var(--line-height-base);
  color: var(--text-primary);
  background-color: var(--bg-primary);
  transition: background-color var(--transition-base), color var(--transition-base);
  overflow-x: hidden;
}
/* Typography */
h1,
h2,
h3,
h4,
h5,
h6 {
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  color: var(--text-primary);
  margin-bottom: var(--spacing-4);
}
h1 {
  font-size: var(--font-size-4xl);
  margin-bottom: var(--spacing-6);
}
h2 {
  font-size: var(--font-size-3xl);
  color: var(--interactive-primary);
}
h3 {
  font-size: var(--font-size-2xl);
}
h4 {
  font-size: var(--font-size-xl);
}
h5 {
  font-size: var(--font-size-lg);
}
h6 {
  font-size: var(--font-size-base);
}
p {
  margin-bottom: var(--spacing-4);
}
/* Links */
a {
  color: var(--text-link);
  text-decoration: none;
  transition: color var(--transition-fast);
}
a:hover {
  color: var(--text-link-hover);
  text-decoration: underline;
}
a:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}
/* Lists */
ul,
ol {
  margin-bottom: var(--spacing-4);
  padding-left: var(--spacing-6);
}
li {
  margin-bottom: var(--spacing-2);
}
/* Code */
code,
pre {
  font-family: var(--font-mono);
  font-size: 0.9em;
}
code {
  background: var(--bg-secondary);
  padding: 0.125rem 0.25rem;
  border-radius: var(--radius-sm);
  color: var(--color-danger-500);
}
pre {
  background: var(--bg-secondary);
  padding: var(--spacing-4);
  border-radius: var(--radius-base);
  overflow-x: auto;
  margin-bottom: var(--spacing-4);
}
pre code {
  background: none;
  padding: 0;
  color: inherit;
}
/* Forms */
input,
textarea,
select,
button {
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
}
/* Images & Media */
img,
video,
svg {
  display: block;
  max-width: 100%;
  height: auto;
}
/* Tables */
table {
  border-collapse: collapse;
  width: 100%;
}
th,
td {
  padding: var(--spacing-3);
  text-align: left;
  border-bottom: 1px solid var(--border-default);
}
th {
  font-weight: var(--font-weight-semibold);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
/* Utilities */
.hidden {
  display: none !important;
}
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

**Verification**: Link in main.css, add sample HTML—resets apply, tokens cascade.

### 2.3: Component Styles (Build components.css Incrementally)

**Step 1: Create components.css**

```bash
touch backend/static/css/components.css
```

Paste layout:

```css
/* Layout Components (NEW) */
.container {
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--spacing-4);
  padding-right: var(--spacing-4);
}
```

- **Explanation**: Max-width = readable line length (app: 75chars ~1200px). Auto margins = center (CS: flexbox alternative).
- **Test**: `<div class="container">Test</div>` → Centered, padded.
- **Gotcha**: Mobile: No media yet (later).

**Step 2: Add Header**
Add:

```css
/* Header (NEW) */
header {
  background: linear-gradient(
    135deg,
    var(--color-primary-500),
    var(--color-primary-700)
  );
  color: var(--text-inverse);
  padding: var(--spacing-6);
  box-shadow: var(--shadow-md);
}
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  gap: var(--spacing-4);
  flex-wrap: wrap;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}
```

- **Explanation**: Gradient = visual appeal (CSS: linear-gradient). Flex = responsive layout (CS: box model evolution). Wrap = mobile stack.
- **Test**: `<header><div class="header-content"><h1>Title</h1><div class="header-actions"><button>Test</button></div></div></header>` → Gradient header, flex actions.
- **Gotcha**: Gap = modern spacing (IE11 fallback: margins).

**Step 3: Add Main & Footer**
Add:

```css
/* Main content area (NEW) */
main {
  padding: var(--spacing-8) 0;
  min-height: calc(100vh - 200px);
}
/* Footer (NEW) */
footer {
  text-align: center;
  padding: var(--spacing-8) var(--spacing-4);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  border-top: 1px solid var(--border-default);
}
```

- **Explanation**: Calc = viewport units (CS: relative sizing). Border-top = separator.
- **Test**: `<main>Test</main><footer>Foot</footer>` → Padded, bordered.
- **Gotcha**: 100vh includes bars (use 100dvh for dynamic).

**Step 4: Add Card Section**
Add:

```css
/* Card Component (NEW) */
section {
  background: var(--card-bg);
  padding: var(--card-padding);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  margin-bottom: var(--spacing-6);
  transition: background-color var(--transition-base), border-color var(--transition-base),
    box-shadow var(--transition-base);
}
```

- **Explanation**: Tokens for theme (revisit tokens). Transition for hover (app: interactive).
- **Test**: `<section>Card</section>` → Shadowed box.
- **Gotcha**: Transition all = smooth.

**Step 5: Add Button Component (Variants)**
Add:

```css
/* Button Component (NEW) */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
  padding: var(--button-padding-y) var(--button-padding-x);
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-base);
  text-decoration: none;
  white-space: nowrap;
  border: none;
  border-radius: var(--button-border-radius);
  cursor: pointer;
  transition: all var(--button-transition);
  user-select: none;
}
.btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.btn:active {
  transform: translateY(0);
}
.btn:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}
/* Variants (NEW) */
.btn-primary {
  background: var(--button-primary-bg);
  color: var(--button-primary-text);
}
.btn-primary:hover {
  background: var(--button-primary-bg-hover);
}
.btn-secondary {
  background: var(--button-secondary-bg);
  color: var(--button-secondary-text);
}
.btn-secondary:hover {
  background: var(--button-secondary-bg-hover);
}
.btn-danger {
  background: var(--status-danger);
  color: var(--text-inverse);
}
.btn-danger:hover {
  background: var(--color-danger-600);
}
/* Sizes (NEW) */
.btn-sm {
  padding: var(--spacing-1) var(--spacing-3);
  font-size: var(--font-size-sm);
}
.btn-lg {
  padding: var(--spacing-3) var(--spacing-6);
  font-size: var(--font-size-lg);
}
```

- **Explanation**: Inline-flex = button with icon (CS: flexbox alignment). Disabled state = accessibility.
- **Test**: `<button class="btn btn-primary">Primary</button>` → Styled, hover lift.
- **Gotcha**: User-select none = no text select on button.

**Step 6: Add Form Groups**
Add:

```css
/* Form Components (NEW) */
.form-group {
  margin-bottom: var(--spacing-5);
}
.form-group label {
  display: block;
  margin-bottom: var(--spacing-2);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
}
.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: var(--spacing-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-base);
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: var(--font-size-base);
  transition: all var(--transition-fast);
}
.form-group input:hover,
.form-group textarea:hover,
.form-group select:hover {
  border-color: var(--border-hover);
}
.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px var(--interactive-primary-alpha);
}
.form-group textarea {
  resize: vertical;
  min-height: 100px;
}
```

- **Explanation**: Width 100% = full form (app: responsive). Focus ring = a11y (SE: WCAG 2.2).
- **Test**: `<div class="form-group"><label>Label</label><input type="text"></div>` → Styled, focus glow.
- **Gotcha**: Resize vertical = user control.

**Step 7: Add File List Components**
Add:

```css
/* File List Component (NEW) */
#file-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}
.file-item {
  padding: var(--spacing-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--spacing-4);
  background: var(--bg-secondary);
  transition: all var(--transition-base);
}
.file-item:hover {
  transform: translateX(5px);
  border-color: var(--interactive-primary);
  box-shadow: var(--shadow-sm);
}
.file-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
  flex: 1;
}
.file-name {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}
.file-status {
  padding: var(--spacing-1) var(--spacing-3);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}
.status-available {
  background: var(--status-success-bg);
  color: var(--status-success-text);
}
.status-checked_out {
  background: var(--status-warning-bg);
  color: var(--status-warning-text);
}
.file-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}
.loading {
  text-align: center;
  padding: var(--spacing-8);
  color: var(--text-secondary);
}
```

- **Explanation**: Flex gap = spacing (CS: box alignment). Status badges = semantic (app: visual state).
- **Test**: `<ul id="file-list"><li class="file-item"><div class="file-info"><span class="file-name">File</span><span class="file-status status-available">Available</span></div></li></ul>` → List with hover.
- **Gotcha**: Flex-wrap for mobile (add media later).

**Step 8: Add Modal Components**
Add:

```css
/* Modal Component (NEW) */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--modal-backdrop);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: var(--z-modal-backdrop);
  animation: fadeIn var(--transition-base);
}
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
.modal-content {
  background: var(--modal-bg);
  border-radius: var(--modal-border-radius);
  box-shadow: var(--modal-shadow);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid var(--border-default);
  animation: slideUp var(--transition-base);
}
@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
.modal-header {
  padding: var(--spacing-6);
  border-bottom: 1px solid var(--border-default);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.modal-header h3 {
  margin: 0;
  color: var(--text-primary);
}
.modal-close {
  background: none;
  border: none;
  font-size: var(--font-size-2xl);
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-base);
  transition: all var(--transition-fast);
}
.modal-close:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}
.modal-body {
  padding: var(--spacing-6);
}
.modal-actions {
  display: flex;
  gap: var(--spacing-3);
  justify-content: flex-end;
  margin-top: var(--spacing-6);
}
```

- **Explanation**: Fixed = viewport overlay (CS: coordinate systems). Animations = keyframe (app: UX delight).
- **Test**: `<div class="modal-overlay hidden"><div class="modal-content"><div class="modal-header"><h3>Title</h3><button class="modal-close">&times;</button></div></div></div>` → Overlay.
- **Gotcha**: Z-index for stacking.

**Full components.css** (End of Section—Verify):

```css
/* Layout Components */
.container {
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--spacing-4);
  padding-right: var(--spacing-4);
}
/* Header */
header {
  background: linear-gradient(
    135deg,
    var(--color-primary-500),
    var(--color-primary-700)
  );
  color: var(--text-inverse);
  padding: var(--spacing-6);
  box-shadow: var(--shadow-md);
}
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  gap: var(--spacing-4);
  flex-wrap: wrap;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}
/* Main */
main {
  padding: var(--spacing-8) 0;
  min-height: calc(100vh - 200px);
}
/* Footer */
footer {
  text-align: center;
  padding: var(--spacing-8) var(--spacing-4);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  border-top: 1px solid var(--border-default);
}
/* Card */
section {
  background: var(--card-bg);
  padding: var(--card-padding);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  margin-bottom: var(--spacing-6);
  transition: background-color var(--transition-base), border-color var(--transition-base),
    box-shadow var(--transition-base);
}
/* Button */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
  padding: var(--button-padding-y) var(--button-padding-x);
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-base);
  text-decoration: none;
  white-space: nowrap;
  border: none;
  border-radius: var(--button-border-radius);
  cursor: pointer;
  transition: all var(--button-transition);
  user-select: none;
}
.btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.btn:active {
  transform: translateY(0);
}
.btn:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}
.btn-primary {
  background: var(--button-primary-bg);
  color: var(--button-primary-text);
}
.btn-primary:hover {
  background: var(--button-primary-bg-hover);
}
.btn-secondary {
  background: var(--button-secondary-bg);
  color: var(--button-secondary-text);
}
.btn-secondary:hover {
  background: var(--button-secondary-bg-hover);
}
.btn-danger {
  background: var(--status-danger);
  color: var(--text-inverse);
}
.btn-danger:hover {
  background: var(--color-danger-600);
}
.btn-sm {
  padding: var(--spacing-1) var(--spacing-3);
  font-size: var(--font-size-sm);
}
.btn-lg {
  padding: var(--spacing-3) var(--spacing-6);
  font-size: var(--font-size-lg);
}
/* Form */
.form-group {
  margin-bottom: var(--spacing-5);
}
.form-group label {
  display: block;
  margin-bottom: var(--spacing-2);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
}
.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: var(--spacing-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-base);
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: var(--font-size-base);
  transition: all var(--transition-fast);
}
.form-group input:hover,
.form-group textarea:hover,
.form-group select:hover {
  border-color: var(--border-hover);
}
.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px var(--interactive-primary-alpha);
}
.form-group textarea {
  resize: vertical;
  min-height: 100px;
}
/* File List */
#file-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}
.file-item {
  padding: var(--spacing-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--spacing-4);
  background: var(--bg-secondary);
  transition: all var(--transition-base);
}
.file-item:hover {
  transform: translateX(5px);
  border-color: var(--interactive-primary);
  box-shadow: var(--shadow-sm);
}
.file-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
  flex: 1;
}
.file-name {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}
.file-status {
  padding: var(--spacing-1) var(--spacing-3);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}
.status-available {
  background: var(--status-success-bg);
  color: var(--status-success-text);
}
.status-checked_out {
  background: var(--status-warning-bg);
  color: var(--status-warning-text);
}
.file-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}
.loading {
  text-align: center;
  padding: var(--spacing-8);
  color: var(--text-secondary);
}
/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--modal-backdrop);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: var(--z-modal-backdrop);
  animation: fadeIn var(--transition-base);
}
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
.modal-content {
  background: var(--modal-bg);
  border-radius: var(--modal-border-radius);
  box-shadow: var(--modal-shadow);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid var(--border-default);
  animation: slideUp var(--transition-base);
}
@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
.modal-header {
  padding: var(--spacing-6);
  border-bottom: 1px solid var(--border-default);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.modal-header h3 {
  margin: 0;
  color: var(--text-primary);
}
.modal-close {
  background: none;
  border: none;
  font-size: var(--font-size-2xl);
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-base);
  transition: all var(--transition-fast);
}
.modal-close:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}
.modal-body {
  padding: var(--spacing-6);
}
.modal-actions {
  display: flex;
  gap: var(--spacing-3);
  justify-content: flex-end;
  margin-top: var(--spacing-6);
}
```

**Verification**: Save, test sample elements—buttons, forms, modals style correctly.

### 2.4: CSS Entry Point (main.css)

**Step 1: Create main.css**

```bash
touch backend/static/css/main.css
```

Paste:

```css
/**
 * Main CSS Entry Point
 */
/* 1. Tokens first (NEW) */
@import "tokens.css";
/* 2. Base (NEW) */
@import "base.css";
/* 3. Components (NEW) */
@import "components.css";
```

- **Explanation**: @import order = cascade (CS: dependency order, tokens > base > components). ITCSS triangle.
- **Test**: Link in index.html `<link rel="stylesheet" href="css/main.css">`—all styles apply.
- **Gotcha**: Import cycles = infinite loop (avoid).

**Full main.css** (End of Section—Verify):

```css
/**
 * Main CSS Entry Point
 */
/* 1. Design Tokens - Must load first */
@import "tokens.css";
/* 2. Base Styles - Raw HTML elements */
@import "base.css";
/* 3. Components - Reusable UI pieces */
@import "components.css";
```

**Verification**: index.html with sample HTML—full styles (header gradient, buttons).

### 2.5: Theme Manager JavaScript (ES6 Module Incremental)

**Step 1: Create theme-manager.js**

```bash
touch backend/static/js/modules/theme-manager.js
```

Paste class skeleton:

```javascript
/**
 * Theme Management Module
 */
export class ThemeManager {  # NEW: Export class
  constructor() {  # NEW: Init
    this.STORAGE_KEY = "pdm-theme";  # NEW: localStorage key
    this.theme = this.getInitialTheme();  # NEW: Set initial
    this.init();  # NEW: Setup
  }
}
```

- **Explanation**: ES6 class = blueprint (CS: OOP encapsulation). Export = module (JS: tree-shaking).
- **Test**: `index.html` <script type="module" src="js/modules/theme-manager.js"></script>—no errors.
- **Gotcha**: type=module for import.

**Step 2: Add getInitialTheme**
Add inside class:

```javascript
  getInitialTheme() {  # NEW
    const stored = localStorage.getItem(this.STORAGE_KEY);
    if (stored) return stored;  # NEW: Persist
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {  # NEW: System
      return "dark";
    }
    return "light";  # NEW: Default
  }
```

- **Explanation**: localStorage = persist (CS: key-value store). matchMedia = OS pref (app: a11y).
- **Test**: Console: `localStorage.setItem('pdm-theme', 'dark');` reload—uses stored.
- **Gotcha**: matchMedia = media query API.

**Step 3: Add init & applyTheme**
Add:

```javascript
  init() {  # NEW
    this.applyTheme(this.theme);  # NEW: Apply
    this.listenForSystemChanges();  # NEW: Watch
  }
  applyTheme(theme) {  # NEW
    document.documentElement.setAttribute("data-theme", theme);  # NEW: Set attr
    this.theme = theme;
    this.updateThemeButton();  # NEW: UI
  }
```

- **Explanation**: setAttribute = CSS [data-theme] trigger (revisit tokens dark). this.theme = state (CS: closure).
- **Test**: Add <html data-theme="light">, call applyTheme('dark') in console—switches.
- **Gotcha**: documentElement = <html> (root).

**Step 4: Add toggle & updateThemeButton**
Add:

```javascript
  toggle() {  # NEW
    const newTheme = this.theme === "dark" ? "light" : "dark";
    this.applyTheme(newTheme);
    localStorage.setItem(this.STORAGE_KEY, newTheme);  # NEW: Save
  }
  updateThemeButton() {  # NEW
    const button = document.getElementById("theme-toggle");
    if (!button) return;
    button.textContent = this.theme === "dark" ? "☀️" : "🌙";  # NEW: Icon
    button.setAttribute("aria-label", `Switch to ${this.theme === "dark" ? "light" : "dark"} theme`);
  }
```

- **Explanation**: Toggle flips (app: state machine). Aria-label = screen reader (a11y, SE: inclusive).
- **Test**: Add <button id="theme-toggle">, call toggle()—icon flips, saved.
- **Gotcha**: Emoji = Unicode (universal).

**Step 5: Add listenForSystemChanges**
Add:

```javascript
  listenForSystemChanges() {  # NEW
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {  # NEW: Listener
      if (!localStorage.getItem(this.STORAGE_KEY)) {  # NEW: If no pref
        this.applyTheme(e.matches ? "dark" : "light");
      }
    });
  }
```

- **Explanation**: addEventListener = observer (CS: pub-sub). Only if no stored (user override).
- **Test**: Toggle OS dark—switches if no localStorage.
- **Gotcha**: matches = bool (true for dark).

**Step 6: Export Instance**
Add at end:

```javascript
export const themeManager = new ThemeManager();  # NEW: Singleton
```

- **Explanation**: Instance = ready-to-use (SE: factory pattern).
- **Test**: In index.html <script type="module"> import { themeManager } from './js/modules/theme-manager.js'; themeManager.toggle(); </script>—applies.

**Full theme-manager.js** (End of Section—Verify):

```javascript
/**
 * Theme Management Module
 */
export class ThemeManager {
  constructor() {
    this.STORAGE_KEY = "pdm-theme";
    this.theme = this.getInitialTheme();
    this.init();
  }
  getInitialTheme() {
    const stored = localStorage.getItem(this.STORAGE_KEY);
    if (stored) return stored;
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      return "dark";
    }
    return "light";
  }
  init() {
    this.applyTheme(this.theme);
    this.listenForSystemChanges();
  }
  applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    this.theme = theme;
    this.updateThemeButton();
  }
  toggle() {
    const newTheme = this.theme === "dark" ? "light" : "dark";
    this.applyTheme(newTheme);
    localStorage.setItem(this.STORAGE_KEY, newTheme);
  }
  updateThemeButton() {
    const button = document.getElementById("theme-toggle");
    if (!button) return;
    button.textContent = this.theme === "dark" ? "☀️" : "🌙";
    button.setAttribute(
      "aria-label",
      `Switch to ${this.theme === "dark" ? "light" : "dark"} theme`
    );
  }
  listenForSystemChanges() {
    window
      .matchMedia("(prefers-color-scheme: dark)")
      .addEventListener("change", (e) => {
        if (!localStorage.getItem(this.STORAGE_KEY)) {
          this.applyTheme(e.matches ? "dark" : "light");
        }
      });
  }
}
export const themeManager = new ThemeManager();
```

**Verification**: Import in temp script, toggle—dark/light switches, persists.

### 2.6: HTML Structure (Build index.html Incrementally)

**Step 1: Basic HTML Skeleton**
Edit `backend/static/index.html`:

```html
<!DOCTYPE html> # NEW: Standards mode
<html lang="en">
  # NEW: Language for a11y
  <head>
    # NEW: Metadata
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PDM System</title>
    # NEW
    <link rel="stylesheet" href="/static/css/main.css" />
    # NEW: Styles
  </head>
  <body>
    # NEW: Content
    <h1>Hello PDM</h1>
    # NEW: Test
  </body>
</html>
```

- **Explanation**: Doctype = HTML5 (CS: parsing mode). Viewport = mobile (app: responsive). Link = cascade.
- **Test**: /static/index.html → "Hello PDM" styled (from base).
- **Gotcha**: Charset first = correct encoding.

**Step 2: Add Theme Script (Before Body)**
In <head>, before </head>:

```html
<script type="module">
  # NEW: ES6
  import { themeManager } from "/static/js/modules/theme-manager.js";  # NEW: Import
</script>
```

- **Explanation**: type=module = import support (JS: bundler-less). Runs early = no flash (unstyled content).
- **Test**: Toggle OS dark—body switches (if matchMedia).
- **Gotcha**: Path /static = server mount.

**Step 3: Add Header**
In <body>:

```html
<header>
  # NEW
  <div class="header-content">
    # NEW
    <div>
      <h1>PDM System</h1>
      <p>Parts Data Management</p>
    </div>
    <div class="header-actions">
      # NEW
      <button id="theme-toggle" class="btn btn-secondary" title="Toggle theme">
        🌙
      </button>
    </div>
  </div>
</header>
```

- **Explanation**: Semantic <header> (app: SEO/a11y). Classes from components.
- **Test**: Header gradient, button.
- **Gotcha**: Title attr = tooltip.

**Step 4: Add Main & Footer**
Add:

```html
<main>
  # NEW
  <div class="container">
    <section>
      <h2>Available Files</h2>
      <div id="loading-indicator" class="loading">Loading...</div>
      <div id="file-list"></div>
      # NEW: For JS
    </section>
  </div>
</main>
<footer>
  # NEW
  <p>&copy; 2025 PDM Tutorial</p>
</footer>
```

- **Explanation**: <main> = landmark (a11y). IDs for JS (CS: DOM query).
- **Test**: Padded main, centered footer.
- **Gotcha**: ID unique.

**Step 5: Add Modals (One)**
Add before </body>:

```html
<div id="checkout-modal" class="modal-overlay hidden">
  # NEW
  <div class="modal-content">
    <div class="modal-header">
      <h3>Check Out File</h3>
      <button class="modal-close">&times;</button>
    </div>
    <div class="modal-body">
      <p>Checking out: <strong id="checkout-filename"></strong></p>
      <form id="checkout-form">
        <div class="form-group">
          <label for="checkout-user">Your Name</label>
          <input
            type="text"
            id="checkout-user"
            name="user"
            required
            minlength="3"
          />
        </div>
        <div class="form-group">
          <label for="checkout-message">Reason</label>
          <textarea
            id="checkout-message"
            name="message"
            required
            minlength="5"
            rows="3"
          ></textarea>
        </div>
        <div class="modal-actions">
          <button
            type="button"
            class="btn btn-secondary"
            onclick="checkoutModal.close()"
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-primary">Confirm</button>
        </div>
      </form>
    </div>
  </div>
</div>
```

- **Explanation**: One modal for checkout (app: progressive disclosure). Form IDs for JS.
- **Test**: Add .open class—modal shows.
- **Gotcha**: onclick global = simple (later events).

**Full index.html** (End of Section—Verify):

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PDM System</title>
    <link rel="stylesheet" href="/static/css/main.css" />
    <script type="module">
      import { themeManager } from "/static/js/modules/theme-manager.js";
    </script>
  </head>
  <body>
    <header>
      <div class="header-content">
        <div>
          <h1>PDM System</h1>
          <p>Parts Data Management</p>
        </div>
        <div class="header-actions">
          <button
            id="theme-toggle"
            class="btn btn-secondary"
            title="Toggle theme"
          >
            🌙
          </button>
        </div>
      </div>
    </header>
    <main>
      <div class="container">
        <section>
          <h2>Available Files</h2>
          <div id="loading-indicator" class="loading">Loading...</div>
          <div id="file-list"></div>
        </section>
      </div>
    </main>
    <footer>
      <p>&copy; 2025 PDM Tutorial</p>
    </footer>
    <div id="checkout-modal" class="modal-overlay hidden">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Check Out File</h3>
          <button class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
          <p>Checking out: <strong id="checkout-filename"></strong></p>
          <form id="checkout-form">
            <div class="form-group">
              <label for="checkout-user">Your Name</label>
              <input
                type="text"
                id="checkout-user"
                name="user"
                required
                minlength="3"
              />
            </div>
            <div class="form-group">
              <label for="checkout-message">Reason</label>
              <textarea
                id="checkout-message"
                name="message"
                required
                minlength="5"
                rows="3"
              ></textarea>
            </div>
            <div class="modal-actions">
              <button
                type="button"
                class="btn btn-secondary"
                onclick="checkoutModal.close()"
              >
                Cancel
              </button>
              <button type="submit" class="btn btn-primary">Confirm</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </body>
</html>
```

**Verification**: /static/index.html → Styled page with header/main/footer/modal.

### 2.7: API Client Module (JS Fetch Incremental)

**Step 1: Create api-client.js**

```bash
touch backend/static/js/modules/api-client.js
```

Paste:

```javascript
/**
 * API Client Module
 */
export class APIClient {  # NEW: Class
  constructor(baseURL = "") {  # NEW
    this.baseURL = baseURL;  # NEW
  }
}
```

- **Explanation**: Class for methods (JS: encapsulation). baseURL = /api (app: central calls).
- **Test**: Import in console—class OK.
- **Gotcha**: Export default vs named (named for tree-shake).

**Step 2: Add request (Core Fetch)**
Add:

```javascript
  async request(endpoint, options = {}) {  # NEW: Async for HTTP
    const url = `${this.baseURL}${endpoint}`;  # NEW
    const config = {  # NEW
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    };
    try {
      const response = await fetch(url, config);  # NEW: Fetch API
      if (!response.ok) {  # NEW
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}`);  # NEW
      }
      const data = await response.json();  # NEW
      return data;
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);  # NEW
      throw error;
    }
  }
```

- **Explanation**: Async/await = promise chain (CS: non-blocking I/O). Fetch = native HTTP (no axios dep).
- **Test**: Add to index.html <script> import { APIClient } from './js/modules/api-client.js'; const client = new APIClient(); client.request('/api/files').then(console.log); </script> → Fetches /api/files.
- **Gotcha**: Await in async only.

**Step 3: Add get/post**
Add:

```javascript
  async get(endpoint, options = {}) {  # NEW
    return this.request(endpoint, { ...options, method: "GET" });
  }
  async post(endpoint, data, options = {}) {  # NEW
    return this.request(endpoint, {
      ...options,
      method: "POST",
      body: JSON.stringify(data),
    });
  }
```

- **Explanation**: Convenience wrappers (SE: facade pattern).
- **Test**: client.get('/api/files') → Same as request.

**Step 4: Add getFiles**
Add:

```javascript
  async getFiles() {  # NEW: App-specific
    return this.get("/api/files");
  }
```

- **Explanation**: Domain method (app: PDM files).
- **Test**: client.getFiles() → List.

**Step 5: Export Instance**
Add:

```javascript
export const apiClient = new APIClient();  # NEW
```

- **Explanation**: Singleton (SE: global client).
- **Test**: Import { apiClient }—ready.

**Full api-client.js** (End of Section—Verify):

```javascript
/**
 * API Client Module
 */
export class APIClient {
  constructor(baseURL = "") {
    this.baseURL = baseURL;
  }
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    };
    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `HTTP ${response.status}: ${response.statusText}`
        );
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }
  async get(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: "GET" });
  }
  async post(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "POST",
      body: JSON.stringify(data),
    });
  }
  async getFiles() {
    return this.get("/api/files");
  }
}
export const apiClient = new APIClient();
```

**Verification**: In temp script, apiClient.getFiles() → Fetches.

### 2.8: Main Application JavaScript (app.js Incremental)

**Step 1: Import & State**
Edit `backend/static/js/app.js`:

```javascript
import { themeManager } from "./modules/theme-manager.js";  # NEW
import { apiClient } from "./modules/api-client.js";  # NEW

let allFiles = [];  # NEW: State
let isLoading = true;  # NEW
```

- **Explanation**: Imports = modules (JS: dependency injection). State vars = app data (CS: mutable state).
- **Test**: <script type="module" src="js/app.js"></script>—no errors.
- **Gotcha**: Relative paths (./ for same dir).

**Step 2: Add loadFiles (Fetch & Render Stub)**
Add:

```javascript
async function loadFiles() {  # NEW: Async
  const loadingEl = document.getElementById("loading-indicator");  # NEW
  const fileListEl = document.getElementById("file-list");  # NEW
  loadingEl.classList.remove("hidden");  # NEW: Show
  fileListEl.innerHTML = "";  # NEW: Clear
  try {
    const data = await apiClient.getFiles();  # NEW: Call
    allFiles = data.files;  # NEW: Store
    loadingEl.classList.add("hidden");  # NEW: Hide
    displayFiles(allFiles);  # NEW: Stub
  } catch (error) {  # NEW
    loadingEl.classList.add("hidden");
    fileListEl.innerHTML = `<p>Error: ${error.message}</p>`;
  }
}
```

- **Explanation**: Await fetch (CS: promises). ClassList = DOM manipulation (app: dynamic UI).
- **Test**: Call loadFiles() in console—loads/hides, renders stub (error if no displayFiles).
- **Gotcha**: Try/catch for network (SE: resilient).

**Step 3: Add displayFiles (Simple Render)**
Add:

```javascript
function displayFiles(files) {  # NEW
  const container = document.getElementById("file-list");
  container.innerHTML = "";  # NEW
  if (!files || files.length === 0) {  # NEW
    container.innerHTML = '<p>No files.</p>';
    return;
  }
  files.forEach((file) => {  # NEW: Loop
    const div = document.createElement("div");  # NEW: DOM
    div.textContent = file.name;  # NEW
    container.appendChild(div);  # NEW
  });
}
```

- **Explanation**: forEach = functional (CS: iteration). createElement = dynamic DOM (vs innerHTML for security).
- **Test**: loadFiles() → Files as divs.
- **Gotcha**: textContent = safe (no HTML inject).

**Step 4: Add DOMContentLoaded**
Add at end:

```javascript
document.addEventListener("DOMContentLoaded", () => {  # NEW: Wait DOM
  console.log("App ready");  # NEW
  document.getElementById("theme-toggle").addEventListener("click", () => themeManager.toggle());  # NEW: Wire
  loadFiles();  # NEW: Init
});
```

- **Explanation**: DOMContentLoaded = ready event (CS: event loop). addEventListener = delegation.
- **Test**: Reload—console log, theme toggle, files load.
- **Gotcha**: No () on listener = passes event.

**Full app.js** (End of Section—Verify):

```javascript
import { themeManager } from "./modules/theme-manager.js";
import { apiClient } from "./modules/api-client.js";

let allFiles = [];
let isLoading = true;

async function loadFiles() {
  const loadingEl = document.getElementById("loading-indicator");
  const fileListEl = document.getElementById("file-list");
  loadingEl.classList.remove("hidden");
  fileListEl.innerHTML = "";
  try {
    const data = await apiClient.getFiles();
    allFiles = data.files;
    loadingEl.classList.add("hidden");
    displayFiles(allFiles);
  } catch (error) {
    loadingEl.classList.add("hidden");
    fileListEl.innerHTML = `<p>Error: ${error.message}</p>`;
  }
}

function displayFiles(files) {
  const container = document.getElementById("file-list");
  container.innerHTML = "";
  if (!files || files.length === 0) {
    container.innerHTML = "<p>No files.</p>";
    return;
  }
  files.forEach((file) => {
    const div = document.createElement("div");
    div.textContent = file.name;
    container.appendChild(div);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("App ready");
  document
    .getElementById("theme-toggle")
    .addEventListener("click", () => themeManager.toggle());
  loadFiles();
});
```

**Verification**: / → Loads files list, theme toggles, no errors.

### Stage 2 Complete

**Test Full Frontend**:

- /static/index.html → Styled page, files from API, theme switch (dark vars apply).
- Console: "App ready", no errors.

**Verification**:

- [ ] Tokens cascade (inspect vars).
- [ ] Base resets (no margins).
- [ ] Components style (buttons, forms).
- [ ] JS fetches/renders files.
- [ ] Theme persists/switches.

**What You Learned (Depth)**:

- **CS**: Cascade (dependency order), flexbox (layout algos), event loop (DOMContentLoaded).
- **App**: ITCSS layers (modularity), tokens (theming), fetch (HTTP client).
- **Python/JS**: CSS vars (runtime), ES6 modules (import), async/await (promises).
- **SE**: DRY (tokens), a11y (focus, sr-only), responsive (rem, flex-wrap).

**Next: Stage 3** (Locking, incremental file ops). Ready?
