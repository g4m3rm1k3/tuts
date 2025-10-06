## Stage 2: Professional Frontend Architecture

**Prerequisites**: You have a working FastAPI backend from Stage 1.

**Goal**: Transform our basic API into a visually appealing, interactive, and professionally structured web application.

---

### 2.1: The HTML Skeleton - Structuring the Document

Our first step is to create the HTML file that will be the skeleton of our entire frontend. HTML provides the **content** and **structure**—think of it as the framing of a house.

#### Step 1: Create the `index.html` file

**Action**: Create the main HTML file for our frontend.

**File**: `backend/static/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PDM System</title>
  </head>
  <body>
    <header>
      <h1>PDM System</h1>
    </header>
    <main>
      <section>
        <h2>Available Files</h2>
        <div id="file-list">
          <p>Loading files...</p>
        </div>
      </section>
    </main>
    <footer>
      <p>&copy; 2025 PDM Tutorial Project</p>
    </footer>
  </body>
</html>
```

#### Deep Dive: Understanding the HTML Structure 🧠

- `<!DOCTYPE html>`: This is the **document type declaration**. It's not a tag but an instruction to the browser that says, "Hey, interpret this document using the HTML5 standard." It must always be the very first line.

- `<html lang="en">`: This is the **root element** of the page. The `lang="en"` attribute is crucial for **accessibility** and **SEO**; it tells screen readers and search engines that the page's primary language is English.

- `<head>`: This section contains **metadata**—data about your HTML document that is not displayed on the page itself.

  - `<meta charset="UTF-8" />`: Sets the character encoding to UTF-8. This is a universal standard that can represent virtually any character from any language, preventing issues with special symbols or international text.
  - `<meta name="viewport" ...>`: This is the cornerstone of **responsive design**. `width=device-width` tells the browser to make the page width equal to the screen width of the device (like a phone or tablet). `initial-scale=1.0` sets the initial zoom level to 100%. Without this, mobile browsers would show a zoomed-out desktop version of your site.
  - `<title>`: This text appears in the browser tab and is used for bookmarks and search engine results.

- `<body>`: This contains all the **visible content** of your webpage.

- **Semantic Tags (`<header>`, `<main>`, `<section>`, `<footer>`):**

  - **Why not just use `<div>` for everything?** While you could, semantic tags give your content meaning.
  - `<header>`: Represents introductory content, typically a group of introductory or navigational aids.
  - `<main>`: Specifies the main, dominant content of the document. There should only be one `<main>` element per page.
  - `<section>`: Represents a standalone thematic grouping of content.
  - **Benefit**: This structure is invaluable for screen readers, which can use it to help visually impaired users navigate your page (e.g., "Jump to main content"). It also helps search engines understand your page's structure.

#### Deep Dive: The DOM (Document Object Model) 🌳

When the browser reads your `index.html` file, it doesn't just display it. It builds an in-memory tree structure called the **DOM**. Each HTML tag becomes an "object" or "node" in this tree.

Our simple HTML becomes this tree in the browser's memory:

```
(Document)
└── html
    ├── head
    │   ├── meta
    │   └── title
    └── body
        ├── header
        │   └── h1
        ├── main
        │   └── section
        │       ├── h2
        │       └── div#file-list
        └── footer
            └── p
```

JavaScript's primary job on the frontend is to interact with and manipulate this DOM tree to make the page dynamic. The `id="file-list"` is a unique identifier we'll use later to find that specific `div` and insert our file data into it.

---

### 2.2: Connecting Backend to Frontend

Now that we have an HTML file, we need to tell our FastAPI backend how to serve it to the user.

#### Step 1: Update `main.py` to serve static files

**Action**: Modify your main application file to mount the `static` directory and serve `index.html` at the root URL.

**File**: `backend/app/main.py`

```python
## Add these imports at the top
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings ## We'll use this for paths

## ... inside your create_application() function ...

def create_application() -> FastAPI:
    ## ... after your app = FastAPI(...) line and middleware ...

    ## ====================================================================
    ## SECTION 2.5: Static Files & Frontend Entry Point
    ## ====================================================================

    ## 1. Mount the 'static' directory
    ## This tells FastAPI: "Any URL that starts with '/static' should be treated
    ## as a request for a file from the 'backend/static' folder on disk."
    app.mount(
        "/static",
        StaticFiles(directory=settings.BASE_DIR / "static"),
        name="static"
    )

    ## 2. Serve the main index.html file for the root URL ("/")
    ## This creates a special endpoint for the homepage.
    @app.get("/", response_class=FileResponse, include_in_schema=False)
    async def serve_frontend():
        """Serves the main application's HTML entry point."""
        ## FileResponse is an efficient way to send a file directly from disk.
        ## 'include_in_schema=False' hides this from our API docs, as it's for the UI.
        return FileResponse(settings.BASE_DIR / "static/index.html")

    ## ... keep the rest of the function (startup/shutdown events, routers) ...
```

#### Deep Dive: `mount` vs. `get` and MIME Types ⚙️

- **`app.mount(...)`**: This is for serving an **entire directory**. It's highly optimized for static files. When a request comes in for `/static/css/style.css`, the `StaticFiles` application handles it directly, bypassing most of FastAPI's complex routing logic for better performance.

- **`@app.get("/")` with `FileResponse`**: This is for serving a **single, specific file** at a specific endpoint. We use it for our `index.html` because it's the entry point to our entire Single Page Application (SPA).

- **MIME Types**: When the server sends a file, it includes a `Content-Type` header (also called a MIME type). This tells the browser how to handle the file.

  - `text/html`: The browser renders it as a webpage.
  - `text/css`: The browser parses it as a stylesheet.
  - `application/javascript`: The browser executes it as a script.
  - `image/jpeg`: The browser displays it as an image.
    `StaticFiles` and `FileResponse` automatically guess the correct MIME type based on the file extension (`.html`, `.css`, etc.), which is crucial for the frontend to work correctly.

**Test your changes**: Restart your server (`uvicorn app.main:app --reload`) and visit `http://127.0.0.1:8000`. You should now see your unstyled HTML page.

---

### 2.3: Building the Design System (CSS)

A professional frontend is built on a **design system**—a single source of truth for all design decisions. We'll create ours using **CSS Custom Properties** (variables). This makes our application themeable, consistent, and easy to maintain. We'll organize our CSS files using the **ITCSS (Inverted Triangle CSS)** architecture.

#### Step 1: Create the Design Tokens (Settings Layer)

Design tokens are the fundamental building blocks of your UI. They are named variables for colors, spacing, fonts, etc.

**Action**: Create a new CSS file for our tokens.

**File**: `backend/static/css/tokens.css`

```css
/**
 * Design Tokens - The Single Source of Truth for our UI
 *
 * These CSS custom properties (variables) are defined in the :root selector,
 * which makes them globally available throughout the entire application.
 * They are the "atoms" of our design system.
 */

:root {
  /* =========================================================================
     COLOR PALETTE - These are the raw, primitive colors available.
     We use a 50-900 scale (e.g., --color-primary-50 to --color-primary-900),
     where 500 is the base color. This is a professional standard that allows
     for a wide range of shades for different UI states (backgrounds, borders, text).
     ========================================================================= */

  /* Primary Brand Color: A professional, cool-toned indigo. */
  --color-primary-50: #f5f7ff; /* For very subtle hover states or backgrounds. */
  --color-primary-100: #ebf0ff;
  --color-primary-200: #d6e0ff;
  --color-primary-300: #b3c7ff;
  --color-primary-400: #8da9ff;
  --color-primary-500: #667eea; /* The main brand color for primary buttons and links. */
  --color-primary-600: #5568d3; /* A slightly darker shade for hover states. */
  --color-primary-700: #4453b8; /* Even darker, for active/pressed states. */
  --color-primary-800: #353f8f;
  --color-primary-900: #2a3166; /* Darkest shade, suitable for text on light backgrounds. */

  /* Neutral Grays: The backbone of any UI for text, borders, and backgrounds. */
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

  /* Semantic Colors: Colors that have a specific meaning. */
  --color-success-500: #10b981; /* For success states, "available" status. */
  --color-success-600: #059669;
  --color-warning-500: #f59e0b; /* For warnings, "checked-out" status. */
  --color-warning-600: #d97706;
  --color-danger-500: #ef4444; /* For errors and destructive actions. */
  --color-danger-600: #dc2626;
  --color-info-500: #3b82f6; /* For informational messages and highlights. */
  --color-info-600: #2563eb;

  /* =========================================================================
     SPACING SCALE - A consistent scale for margins, padding, and gaps.
     Using a mathematical scale (like 4px or 8px increments) creates visual harmony.
     The 'rem' unit is relative to the root font size, making the UI scalable.
     ========================================================================= */
  --spacing-1: 0.25rem; /* 4px (assuming root font-size is 16px) */
  --spacing-2: 0.5rem; /* 8px */
  --spacing-3: 0.75rem; /* 12px */
  --spacing-4: 1rem; /* 16px - our most common base unit. */
  --spacing-6: 1.5rem; /* 24px */
  --spacing-8: 2rem; /* 32px */

  /* =========================================================================
     TYPOGRAPHY SCALE - For a consistent and readable text hierarchy.
     ========================================================================= */
  /* Font Families */
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif; /* Uses the native font of the user's OS for a familiar feel. */
  --font-mono: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas,
    "Courier New", monospace; /* For code or other fixed-width text. */

  /* Font Sizes - Using a modular scale makes the hierarchy look intentional and professional. */
  --font-size-sm: 0.875rem; /* 14px - For small text like hints or metadata. */
  --font-size-base: 1rem; /* 16px - The default body text size. */
  --font-size-lg: 1.125rem; /* 18px */
  --font-size-xl: 1.25rem; /* 20px */
  --font-size-2xl: 1.5rem; /* 24px - For subheadings. */
  --font-size-3xl: 1.875rem; /* 30px */
  --font-size-4xl: 2.25rem; /* 36px - For main headings. */

  /* Font Weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Line Heights - For optimal text readability. */
  --line-height-tight: 1.25; /* For headings. */
  --line-height-base: 1.5; /* For body text. */

  /* =========================================================================
     SEMANTIC TOKENS - LIGHT THEME (Default)
     These tokens give our primitive tokens meaning. Instead of using a raw color
     like '--color-gray-900', we'll use '--text-primary'. This abstraction
     is what allows us to create themes easily.
     ========================================================================= */
  /* Backgrounds */
  --bg-primary: #ffffff; /* The main page background. */
  --bg-secondary: var(
    --color-gray-50
  ); /* A slightly off-white for subtle contrast. */
  --bg-tertiary: var(--color-gray-100); /* Background for cards and sections. */

  /* Text */
  --text-primary: var(--color-gray-900); /* Main body text. High contrast. */
  --text-secondary: var(
    --color-gray-600
  ); /* Lighter text for subtitles, metadata. */
  --text-inverse: #ffffff; /* Text used on dark/colored backgrounds. */
  --text-link: var(--color-primary-600); /* The color for hyperlinks. */

  /* Borders */
  --border-default: var(--color-gray-200); /* The default color for borders. */
  --border-focus: var(--color-primary-500); /* The color for focused inputs. */

  /* Statuses */
  --status-success-bg: rgba(
    16,
    185,
    129,
    0.1
  ); /* Background for the 'available' badge. */
  --status-success-text: var(
    --color-success-600
  ); /* Text color for the 'available' badge. */
  --status-warning-bg: rgba(
    245,
    158,
    11,
    0.1
  ); /* Background for the 'checked-out' badge. */
  --status-warning-text: var(
    --color-warning-600
  ); /* Text color for the 'checked-out' badge. */
}
```

#### Step 2: Create the Base Styles (Generic & Elements Layers)

This file will contain our CSS reset and default styles for raw HTML tags like `<body>`, `<h1>`, `p`, etc., using our new design tokens.

**Action**: Create a new CSS file for our base styles.

**File**: `backend/static/css/base.css`

```css
/**
 * Base Styles & CSS Reset
 *
 * This file normalizes browser styles and sets defaults for raw HTML elements
 * using the design tokens we defined in tokens.css.
 */

/* A modern, targeted CSS reset to ensure cross-browser consistency. */
*,
*::before,
*::after {
  box-sizing: border-box; /* This makes layout math predictable. width + padding + border = total width. */
  margin: 0; /* Removes inconsistent default margins. */
  padding: 0; /* Removes inconsistent default padding. */
}

/* Base styles for the entire page. */
body {
  font-family: var(--font-sans); /* Use our defined sans-serif font stack. */
  font-size: var(--font-size-base); /* Set the default font size. */
  line-height: var(
    --line-height-base
  ); /* Improve readability with a good line height. */
  color: var(
    --text-primary
  ); /* Use our semantic token for primary text color. */
  background-color: var(
    --bg-primary
  ); /* Use our semantic token for the main background. */
}

/* Default styles for headings. */
h1 {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  margin-bottom: var(
    --spacing-2
  ); /* Consistent spacing below the main heading. */
}

h2 {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  margin-bottom: var(--spacing-6); /* More space below section headings. */
  color: var(--text-link); /* Use the link color for emphasis. */
}

/* Default style for paragraphs. */
p {
  margin-bottom: var(--spacing-4); /* Consistent spacing between paragraphs. */
  color: var(
    --text-secondary
  ); /* Use the secondary text color for less emphasis. */
}

/* Default style for links. */
a {
  color: var(--text-link);
  text-decoration: none; /* Remove the default underline. */
  transition: color 150ms ease-in-out; /* Smooth color transition on hover. */
}
a:hover {
  text-decoration: underline; /* Add underline back on hover for affordance. */
}
```

#### Step 3: Create the Component Styles

Now we style our specific UI components.

**Action**: Create a new CSS file for our component styles.

**File**: `backend/static/css/components.css`

```css
/**
 * Component Styles
 *
 * This file contains styles for our reusable UI components, like the header,
 * main layout, and the file list.
 */

.container {
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--spacing-4);
  padding-right: var(--spacing-4);
}

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
  gap: var(--spacing-4);
  flex-wrap: wrap;
  max-width: 1200px; /* To align with the main container */
  margin: 0 auto;
}
.header-content h1 {
  color: var(--text-inverse); /* Override the default h1 color */
  font-size: var(--font-size-3xl);
  margin-bottom: 0;
}
.header-content p {
  color: var(--text-inverse);
  opacity: 0.8;
  margin-bottom: 0;
}

main {
  padding: var(--spacing-8) 0;
}

footer {
  text-align: center;
  padding: var(--spacing-8);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  border-top: 1px solid var(--border-default);
}

section {
  background: var(--bg-primary);
  padding: var(--spacing-6);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-base);
  border: 1px solid var(--border-default);
  margin-bottom: var(--spacing-8);
}

#file-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}

.file-item {
  padding: var(--spacing-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-base);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-secondary);
  transition: all 150ms ease-in-out;
}
.file-item:hover {
  border-color: var(--border-focus);
  transform: translateX(5px);
  box-shadow: var(--shadow-sm);
}

.file-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
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
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.status-available {
  background: var(--status-success-bg);
  color: var(--status-success-text);
}
.status-checked_out {
  background: var(--status-warning-bg);
  color: var(--status-warning-text);
}

.loading {
  text-align: center;
  padding: var(--spacing-8);
  color: var(--text-secondary);
  font-style: italic;
}
```

#### Step 4: Create the CSS Entry Point

This file will combine all our CSS files in the correct order.

**Action**: Create the main CSS entry point.

**File**: `backend/static/css/main.css`

```css
/**
 * Main CSS Entry Point
 *
 * Imports all CSS files in the correct ITCSS order. This is the only
 * file that needs to be linked in the HTML.
 */

@import "tokens.css";
@import "base.css";
@import "components.css";
```

#### Step 5: Link the CSS in HTML

Finally, let's link our new `main.css` file in our HTML.

**Action**: Update the `<head>` of your `index.html`.

**File**: `backend/static/index.html`

```html
<head>
  <title>PDM System</title>
  <link rel="stylesheet" href="/static/css/main.css" />
</head>
```

**Test your changes**: Refresh your browser. Your application should now be beautifully styled using your new design system\!

---

### 2.4: The JavaScript Brains

Now, let's write the JavaScript to fetch data from our API and dynamically render the file list. We'll build this in a modular way.

#### Step 1: Create the API Client Module

This module will handle all communication with our backend.

**Action**: Create the API client file.

**File**: `backend/static/js/modules/api-client.js`

```javascript
/**
 * API Client Module
 * A centralized place for all backend communication. This abstraction makes our
 * code cleaner and easier to maintain.
 */
export class APIClient {
  constructor(baseURL = "") {
    this.baseURL = baseURL;
  }

  /**
   * A generic method for making HTTP requests.
   * It handles common tasks like setting headers and parsing errors.
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      ...options,
      headers: { "Content-Type": "application/json", ...options.headers },
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP Error: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`API Error on ${endpoint}:`, error);
      throw error;
    }
  }

  // A specific method for getting the file list.
  async getFiles() {
    return this.request("/api/files", { method: "GET" });
  }
}

// Export a single instance for the whole application to use.
export const apiClient = new APIClient();
```

#### Step 2: Create the Theme Manager Module

This module will manage our light/dark mode functionality.

**Action**: Create the theme manager file.

**File**: `backend/static/js/modules/theme-manager.js`

```javascript
/**
 * Theme Management Module
 * Handles light/dark theme switching, system preference detection,
 * and saving the user's choice to localStorage.
 */
class ThemeManager {
  constructor() {
    this.STORAGE_KEY = "pdm-theme";
    this.init();
  }

  // Determines the initial theme based on localStorage or system settings.
  getInitialTheme() {
    const storedTheme = localStorage.getItem(this.STORAGE_KEY);
    if (storedTheme) return storedTheme;
    if (
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
    ) {
      return "dark";
    }
    return "light";
  }

  // Applies a theme by setting the 'data-theme' attribute on the <html> element.
  applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    const toggleButton = document.getElementById("theme-toggle");
    if (toggleButton) {
      toggleButton.innerHTML = theme === "dark" ? "☀️" : "🌙";
      toggleButton.setAttribute(
        "aria-label",
        `Switch to ${theme === "dark" ? "light" : "dark"} mode`
      );
    }
  }

  // Toggles the theme and saves the new preference.
  toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    this.applyTheme(newTheme);
    localStorage.setItem(this.STORAGE_KEY, newTheme);
  }

  // Initializes the theme system.
  init() {
    this.applyTheme(this.getInitialTheme());
  }
}

// Create and export a single instance of the ThemeManager.
export const themeManager = new ThemeManager();
```

#### Step 3: Create the Main Application Logic

This is our main script. It will import the modules and orchestrate the application.

**Action**: Create the main app logic file.

**File**: `backend/static/js/app.js`

```javascript
/**
 * Main Application Logic
 * Initializes the app, fetches data, renders the UI, and handles events.
 */
import { apiClient } from "./modules/api-client.js";
import { themeManager } from "./modules/theme-manager.js";

// The 'DOMContentLoaded' event ensures our script runs only after the full HTML is loaded.
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM loaded. Initializing PDM app.");

  // Set up the theme toggle button.
  const toggleButton = document.getElementById("theme-toggle");
  if (toggleButton) {
    toggleButton.addEventListener("click", () => themeManager.toggleTheme());
  }

  loadFiles(); // Fetch and display the initial file list.
});

/**
 * Fetches files from the API and calls the function to display them.
 */
async function loadFiles() {
  const fileListEl = document.getElementById("file-list");
  fileListEl.innerHTML = `<div class="loading"><p>Loading files...</p></div>`;

  try {
    const data = await apiClient.getFiles();
    displayFiles(data.files);
  } catch (error) {
    fileListEl.innerHTML = `<p style="color: var(--color-danger-500);">Error: ${error.message}</p>`;
  }
}

/**
 * Renders the list of files into the DOM.
 */
function displayFiles(files) {
  const container = document.getElementById("file-list");
  container.innerHTML = ""; // Clear the loading message.

  if (!files || files.length === 0) {
    container.innerHTML = "<p>No files found.</p>";
    return;
  }

  const fragment = document.createDocumentFragment();
  files.forEach((file) => {
    fragment.appendChild(createFileElement(file));
  });
  container.appendChild(fragment);
}

/**
 * Creates and returns a DOM element for a single file.
 */
function createFileElement(file) {
  const div = document.createElement("div");
  div.className = "file-item";

  const infoDiv = document.createElement("div");
  infoDiv.className = "file-info";

  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ");

  infoDiv.appendChild(nameSpan);
  infoDiv.appendChild(statusSpan);
  div.appendChild(infoDiv);

  return div;
}
```

#### Step 4: Add the Theme Toggle Button

Let's add the button to our HTML so the JavaScript can find it.

**Action**: Add the button to `index.html`.

**File**: `backend/static/index.html`
_Inside the `<div class="header-actions">`_

```html
<button
  id="theme-toggle"
  class="btn"
  title="Toggle light/dark mode"
  aria-label="Switch to dark mode"
></button>
```

---

### Stage 2 Complete ✅

**Final Check**: Run your server and visit `http://127.0.0.1:8000`. You should see a professional, styled web page that fetches your file list from the API and allows you to toggle between light and dark themes.

#### What You've Built

- A professionally structured frontend using HTML, CSS, and modular JavaScript.
- A complete, themeable design system using CSS Custom Properties.
- A dynamic UI that fetches data from a backend API and renders it to the DOM.

#### Key Concepts Mastered

- **CSS Architecture (ITCSS)**: Organizing styles for scalability.
- **Design Systems**: Using design tokens as a single source of truth.
- **Theming**: Implementing light/dark mode with CSS variables.
- **JavaScript Modules**: Separating concerns into reusable classes like `APIClient` and `ThemeManager`.
- **Asynchronous JavaScript**: Using `async/await` and `fetch` for non-blocking network requests.
- **DOM Manipulation**: Dynamically creating and updating HTML elements with JavaScript.
