# Section 4: Code Organization with ES6 Modules

**Goal for This Section:** Split your JavaScript into organized, reusable modules using `import` and `export`. Learn how to structure code for a large application.

**Time:** 30-35 minutes

**What You'll Learn:**

- What ES6 modules are and why they matter
- How `import` and `export` work
- Code organization patterns (separation of concerns)
- Creating a utility module
- Creating an API module (preparation for backend communication)
- The `type="module"` attribute

---

## Why Modules Matter

Right now, all your JavaScript is in one file (`main.js`). For a 10,000-line app, this becomes unmanageable:

**Problems with one giant file:**

- Hard to find specific functions (Ctrl+F through thousands of lines)
- Multiple developers editing the same file = merge conflicts
- Can't reuse code in other projects easily
- All variables are global (namespace pollution)
- Hard to test individual pieces

**Solution: Modules**

Break code into logical files:

```
ui/
├── main.js           (entry point, wires everything together)
├── api.js            (all backend communication)
├── utils.js          (helper functions)
├── state.js          (app state management) - later
└── components/       (UI components) - later
    ├── FileCard.js
    └── Modal.js
```

**CNC Analogy:** Instead of one massive G-code file with 10,000 lines, you organize it into main program + subroutines (M98 calls). Each subroutine does one thing well. Same principle here.

---

## Step 4.1: Understanding ES6 Modules

**Old JavaScript (pre-2015):** All scripts shared one global namespace.

```html
<script src="file1.js"></script>
<script src="file2.js"></script>
```

If both files have `var user = ...`, they conflict. Last one wins.

**Modern JavaScript (ES6 modules):** Each file is isolated.

```javascript
// file1.js
export const user = "Alice";

// file2.js
import { user } from "./file1.js";
```

**Key differences:**

- Variables in modules are **private by default** (not global)
- Must explicitly `export` to share
- Must explicitly `import` to use
- No global namespace pollution

**Browser support:** All modern browsers (Chrome, Firefox, Safari, Edge) support ES6 modules natively.

**Read more:** [MDN: JavaScript Modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) (15-minute comprehensive guide - bookmark this!)

---

## Step 4.2: Create New Files

**In your terminal (in the `ui/` directory):**

```bash
touch api.js
touch utils.js
```

**Your `ui/` folder structure should now be:**

```
ui/
├── index.html
├── main.js
├── api.js
└── utils.js
```

---

## Step 4.3: Enable Modules in HTML

**Modify your `<script>` tag in `index.html`:**

**Old:**

```html
<script src="main.js"></script>
```

**New:**

```html
<script type="module" src="main.js"></script>
```

**What `type="module"` does:**

- Tells browser to treat this script as an ES6 module
- Enables `import` and `export` keywords
- Automatically defers script execution (like `defer` attribute)
- Runs in strict mode by default

**Critical:** Without `type="module"`, `import` statements will cause syntax errors.

**Save `index.html`.**

---

## Step 4.4: Create a Utility Function

Let's create a simple utility function to understand exports.

**Open `ui/utils.js` and type:**

```javascript
/**
 * Formats a date into a readable string
 * @param {Date} date - JavaScript Date object
 * @returns {string} Formatted date like "Oct 8, 2025, 2:30 PM"
 */
export function formatDate(date) {
  return date.toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });
}

/**
 * Formats file size from bytes to human-readable format
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted size like "1.5 MB"
 */
export function formatFileSize(bytes) {
  if (bytes === 0) return "0 Bytes";

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
}
```

**Understanding this code:**

### The `export` Keyword

**Syntax:**

```javascript
export function functionName() { ... }
export const variableName = ...;
export class ClassName { ... }
```

**What it does:**

- Makes the function/variable/class available to other files
- Without `export`, the function is private to this file

### JSDoc Comments

The `/** ... */` comments are **JSDoc** format:

```javascript
/**
 * Description of what the function does
 * @param {Type} paramName - Description of parameter
 * @returns {Type} Description of return value
 */
```

**Benefits:**

- Documents your code
- IDEs (VS Code) use this for autocomplete and hints
- Can generate documentation automatically

**Not required, but professional practice.**

### `formatDate` Function

```javascript
date.toLocaleString('en-US', { ... })
```

- `toLocaleString` converts Date to string based on locale
- `'en-US'` = American English format
- Options object customizes output format

**Example:**

```javascript
const now = new Date();
formatDate(now); // "Oct 8, 2025, 2:30 PM"
```

### `formatFileSize` Function

Converts bytes to human-readable format:

- 1024 bytes = 1 KB
- 1024 KB = 1 MB
- 1024 MB = 1 GB

**Math breakdown:**

```javascript
const i = Math.floor(Math.log(bytes) / Math.log(k));
```

This finds which unit to use:

- `Math.log(bytes) / Math.log(1024)` = how many times 1024 fits into bytes
- `Math.floor()` rounds down to get the index
- Use index to pick from `['Bytes', 'KB', 'MB', 'GB']`

**Example:**

```javascript
formatFileSize(0); // "0 Bytes"
formatFileSize(1024); // "1 KB"
formatFileSize(1536); // "1.5 KB"
formatFileSize(1048576); // "1 MB"
formatFileSize(5242880); // "5 MB"
```

**Save `utils.js`.**

---

## Step 4.5: Import and Use Utilities

**Open `ui/main.js` and ADD this at the very top:**

```javascript
// Import utility functions
import { formatDate, formatFileSize } from "./utils.js";
```

**Understanding this import:**

### Import Syntax

```javascript
import { functionName } from "./path/to/file.js";
```

**Key points:**

- Curly braces `{ }` = **named imports** (importing specific exports)
- `'./utils.js'` = relative path (`./ ` means "current directory")
- **Must include `.js` extension** in browsers (unlike Node.js)

**Multiple imports:**

```javascript
import { func1, func2, func3 } from "./file.js";
```

**Import everything:**

```javascript
import * as Utils from "./utils.js";
// Use as: Utils.formatDate(), Utils.formatFileSize()
```

### Relative Paths

- `'./utils.js'` = same directory
- `'../utils.js'` = parent directory
- `'./subfolder/utils.js'` = subfolder

**Common mistake:** Forgetting the `./` prefix:

```javascript
import { formatDate } from "utils.js"; // ❌ Won't work!
import { formatDate } from "./utils.js"; // ✅ Correct
```

---

## Step 4.6: Test the Utilities

**In `main.js`, AFTER the import, ADD this test code (temporarily):**

```javascript
// Test utilities (temporary)
console.log("Current time:", formatDate(new Date()));
console.log("File size:", formatFileSize(5242880));
```

**Your `main.js` should now look like:**

```javascript
// Import utility functions
import { formatDate, formatFileSize } from "./utils.js";

// Test utilities (temporary)
console.log("Current time:", formatDate(new Date()));
console.log("File size:", formatFileSize(5242880));

// Event delegation: One listener for all buttons
document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-action]");
  if (!button) return;
  const action = button.dataset.action;
  console.log("Button clicked:", action);
});
```

**Save and refresh your browser. Open console (F12).**

**You should see:**

```
Current time: Oct 8, 2025, 2:30 PM
File size: 5 MB
```

**It works!** Your module import is functioning.

**Remove the test code lines after verifying.**

---

## Step 4.7: Create the API Module Structure

Now let's create a module for all backend communication. Even though we don't have a backend yet, we'll create the structure.

**Open `ui/api.js` and type:**

```javascript
/**
 * API Module - Handles all communication with the backend server
 */

// Base URL for API requests (will be configured later)
const API_BASE = ""; // Empty for now, means same origin

/**
 * Fetches the list of all files from the backend
 * @returns {Promise<Object>} Object with grouped files
 */
export async function getFiles() {
  // For now, return mock data
  // Later, this will be: const response = await fetch(`${API_BASE}/files`);

  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        "Active Jobs": [
          {
            filename: "PART-001.mcam",
            size: 2048576,
            lastModified: new Date("2025-10-07T14:30:00"),
            checkedOutBy: null,
            revision: "R3",
          },
          {
            filename: "FIXTURE-A.mcam",
            size: 1536000,
            lastModified: new Date("2025-10-06T09:15:00"),
            checkedOutBy: "john_doe",
            revision: "R1",
          },
        ],
        Archive: [
          {
            filename: "OLD-PART.mcam",
            size: 3145728,
            lastModified: new Date("2025-09-15T11:00:00"),
            checkedOutBy: null,
            revision: "R12",
          },
        ],
      });
    }, 500); // Simulate network delay
  });
}

/**
 * Checks out a file (locks it for editing)
 * @param {string} filename - Name of the file to checkout
 * @param {string} username - Username performing the checkout
 * @returns {Promise<Object>} Response from server
 */
export async function checkoutFile(filename, username) {
  console.log(`Checking out ${filename} for ${username}`);
  // TODO: Implement when backend is ready
  return { success: true };
}

/**
 * Checks in a file (uploads new version and unlocks)
 * @param {string} filename - Name of the file
 * @param {File} fileData - File object from input[type=file]
 * @param {string} commitMessage - Description of changes
 * @returns {Promise<Object>} Response from server
 */
export async function checkinFile(filename, fileData, commitMessage) {
  console.log(`Checking in ${filename}: ${commitMessage}`);
  // TODO: Implement when backend is ready
  return { success: true };
}
```

**Understanding this code:**

### Mock Data Strategy

Right now, we're returning **fake data** so we can build the UI without a working backend. This is a professional development practice called **"mocking"**.

**Benefits:**

- Frontend and backend teams can work in parallel
- Can test UI without server running
- Easy to test edge cases (large files, many files, errors)

Later, we'll replace the mock with real `fetch()` calls.

### `async` and `await` Keywords

This is **critical to understand** for your app. Let's break it down.

**The Problem (Synchronous Thinking):**

```javascript
const data = getFiles(); // ❌ Doesn't work!
console.log(data); // Logs "Promise" not the actual data
```

**Why?** Network requests take time (100ms to seconds). JavaScript doesn't wait—it continues executing immediately.

**The Solution (Promises and async/await):**

```javascript
const data = await getFiles(); // ✅ Waits for data
console.log(data); // Logs actual data
```

**What `async` does:**

- Marks a function as asynchronous
- Function automatically returns a Promise
- Enables use of `await` inside the function

**What `await` does:**

- Pauses execution until the Promise resolves
- Only works inside `async` functions
- Makes async code look synchronous (easier to read)

**Example flow:**

```javascript
async function loadData() {
  console.log("1. Starting...");
  const files = await getFiles(); // Waits here
  console.log("2. Got files:", files);
  console.log("3. Done!");
}

loadData();
console.log("4. Outside function");
```

**Output order:**

```
1. Starting...
4. Outside function
(500ms delay)
2. Got files: {...}
3. Done!
```

**Notice:** Line 4 runs before line 2! This is asynchronous execution.

**Read more:** [MDN: async/await](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Async_await) (15-minute tutorial - ESSENTIAL for your app)

### Understanding Promises

A **Promise** is an object representing a future value.

**Three states:**

1. **Pending:** Operation in progress
2. **Fulfilled:** Operation succeeded (has a value)
3. **Rejected:** Operation failed (has an error)

**Creating a Promise manually:**

```javascript
new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve("Success!"); // Fulfill with this value
    // or: reject(new Error('Failed!'));  // Reject with error
  }, 1000);
});
```

**In our code:**

```javascript
return new Promise((resolve) => {
  setTimeout(() => {
    resolve({
      /* mock data */
    });
  }, 500);
});
```

This creates a Promise that resolves after 500ms with fake file data.

**Read more:** [MDN: Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) (20-minute guide)

### Function Parameter Documentation

```javascript
/**
 * @param {string} filename - Name of the file
 * @param {File} fileData - File object from input[type=file]
 */
```

**Types:**

- `{string}` = text
- `{number}` = number
- `{boolean}` = true/false
- `{Object}` = any object
- `{Array}` = array
- `{File}` = browser File object (from file input)
- `{Promise<Object>}` = Promise that resolves to Object

VS Code uses these for autocomplete and type checking.

**Save `api.js`.**

---

## Step 4.8: Use the API Module

**Open `ui/main.js` and ADD this import at the top:**

```javascript
import { formatDate, formatFileSize } from "./utils.js";
import { getFiles } from "./api.js";
```

**Now ADD this code BEFORE the event listener:**

```javascript
// Load and display files
async function loadFiles() {
  console.log("Loading files...");

  const files = await getFiles();
  console.log("Files loaded:", files);

  // TODO: Render files in UI (next section)
}

// Load files when page loads
loadFiles();
```

**Your complete `main.js` should now be:**

```javascript
import { formatDate, formatFileSize } from "./utils.js";
import { getFiles } from "./api.js";

// Load and display files
async function loadFiles() {
  console.log("Loading files...");

  const files = await getFiles();
  console.log("Files loaded:", files);

  // TODO: Render files in UI (next section)
}

// Load files when page loads
loadFiles();

// Event delegation: One listener for all buttons
document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-action]");
  if (!button) return;
  const action = button.dataset.action;
  console.log("Button clicked:", action);
});
```

**Save and refresh browser. Open console.**

**You should see:**

```
Loading files...
(500ms delay)
Files loaded: { 'Active Jobs': [...], 'Archive': [...] }
```

**It works!** You've successfully:

- Created modular code
- Used import/export
- Simulated an async API call
- Used async/await

---

## Step 4.9: Understanding Module Loading Order

**Important concept:** Modules load in dependency order.

When browser loads `main.js`:

1. Sees `import ... from './utils.js'` → loads utils.js first
2. Sees `import ... from './api.js'` → loads api.js second
3. Then executes main.js code

**Visual:**

```
Browser loads main.js
  ↓
  Loads utils.js (exports formatDate, formatFileSize)
  ↓
  Loads api.js (imports nothing, exports getFiles, etc.)
  ↓
  Executes main.js (all imports available)
```

**This is automatic!** You don't manage load order manually.

---

## Step 4.10: Export Patterns

There are two export styles in JavaScript:

### Named Exports (what we're using)

```javascript
// utils.js
export function formatDate() { ... }
export function formatFileSize() { ... }

// main.js
import { formatDate, formatFileSize } from './utils.js';
```

**Pros:**

- Can export multiple things from one file
- Must use exact names when importing (helps prevent typos)
- Can import only what you need

### Default Export

```javascript
// config.js
export default {
  apiUrl: "http://localhost:8000",
  timeout: 5000,
};

// main.js
import config from "./config.js"; // No curly braces!
import myConfig from "./config.js"; // Can name it anything
```

**Pros:**

- One main thing per file
- Can rename on import

**Cons:**

- Only one default per file
- Easy to rename inconsistently

**Our convention:** Use named exports for everything. More explicit, less confusion.

---

## Step 4.11: Common Module Errors and Fixes

### Error 1: CORS Error (in console)

```
Access to script at 'file:///...' from origin 'null' has been blocked by CORS policy
```

**Cause:** Opened `index.html` by double-clicking (file:// protocol). ES6 modules require HTTP.

**Fix:** Use a local server:

- VS Code Live Server extension (recommended)
- Python: `python -m http.server` in ui/ folder
- Node.js: `npx serve` in ui/ folder

### Error 2: Module not found

```
Failed to load module script: Expected a JavaScript module script but the server responded with a MIME type of "text/plain"
```

**Cause:** Server not configured to send `.js` files with correct MIME type.

**Fix:** Use a proper development server (Live Server handles this automatically).

### Error 3: Syntax error on import

```
Uncaught SyntaxError: Cannot use import statement outside a module
```

**Cause:** Forgot `type="module"` in `<script>` tag.

**Fix:**

```html
<script type="module" src="main.js"></script>
```

### Error 4: Can't find export

```
Uncaught SyntaxError: The requested module './utils.js' does not provide an export named 'formatdate'
```

**Cause:** Typo in import (case-sensitive!). Should be `formatDate` not `formatdate`.

**Fix:** Match exact export name (case-sensitive).

---

## Step 4.12: Code Organization Best Practices

**One responsibility per file:**

- ✅ `api.js` = all backend communication
- ✅ `utils.js` = general helper functions
- ❌ Don't put API calls in utils.js or UI code in api.js

**Clear naming:**

- ✅ `formatDate`, `getFiles` = verb + noun, clear purpose
- ❌ `helper`, `doStuff` = vague

**Group related functions:**

- ✅ All date formatting in utils.js
- ✅ All API calls in api.js
- ❌ Random functions scattered across files

**Keep files focused:**

- ✅ utils.js with 5-10 small utilities
- ❌ utils.js with 50 unrelated functions (split into date-utils.js, string-utils.js, etc.)

**Your eventual structure will be:**

```
ui/
├── main.js              (entry point, wires app together)
├── api.js               (backend communication)
├── utils.js             (date, file size, validation helpers)
├── state.js             (app state management)
├── components/
│   ├── FileCard.js      (file display component)
│   ├── Modal.js         (modal dialog component)
│   └── Notification.js  (toast notifications)
└── styles.css           (custom CSS if needed)
```

---

## Experiments (10 minutes)

### Experiment 1: Break an Import

Change the import in main.js to wrong name:

```javascript
import { formatDate, formatFileSize } from "./util.js"; // Typo: util not utils
```

**Result:** Error in console: `Failed to load module script`.

**Fix it before continuing.**

### Experiment 2: Add a New Utility

In `utils.js`, add:

```javascript
export function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}
```

In `main.js`, import and use it:

```javascript
import { formatDate, formatFileSize, capitalize } from "./utils.js";

console.log(capitalize("hello")); // "Hello"
```

This shows how easy it is to add and use new utilities.

### Experiment 3: Import Everything

Change main.js import to:

```javascript
import * as Utils from "./utils.js";

console.log(Utils.formatDate(new Date()));
console.log(Utils.formatFileSize(1024));
```

This imports all exports as properties of `Utils` object. Useful when a file exports many related functions.

**Restore to named imports before continuing:**

```javascript
import { formatDate, formatFileSize } from "./utils.js";
```

---

## Key Takeaways

✅ **ES6 modules** = isolated, reusable code files  
✅ **`export`** = make function/variable available to other files  
✅ **`import`** = bring in exports from other files  
✅ **`type="module"`** = required in script tag to enable modules  
✅ **`async/await`** = handle asynchronous operations cleanly  
✅ **Promises** = objects representing future values  
✅ **Mock data** = fake data for building UI without backend  
✅ **Code organization** = one responsibility per file

---

## What's Next?

In **Section 5**, we'll:

- Create a file card component to display files
- Learn about HTML templates
- Dynamically create and insert HTML elements
- Use the utility functions to format data
- Display the mock file data in the UI

This is where the app starts looking like a real application!

---

## Checkpoint Questions

1. What does `type="module"` do in a script tag?
2. What's the difference between `export function` and `export default`?
3. What does `await` do?
4. Why use mock data before the backend is ready?
5. What's the correct import syntax for a file in the same directory?

<details>
<summary>Answers</summary>

1. Enables ES6 module features (import/export) and automatically defers script execution
2. Named exports can have multiple per file and must be imported with exact names; default export is one per file and can be imported with any name
3. Pauses execution until a Promise resolves, making async code read like synchronous code
4. Allows frontend development to proceed in parallel with backend development, and makes testing UI easier
5. `import { thing } from './file.js';` (must include `./` prefix and `.js` extension)
</details>

---

**Ready for Section 5?** We'll start building the visual file list! Let me know when you're ready to continue.
