# Section 3: Project Setup & Building Your First Feature

**Goal for This Section:** Set up the actual project structure and build your first working feature - a file list that fetches data and displays it. You'll see ALL the Section 2 concepts working together in real code.

**Time:** 1.5 hours

**What You'll Build:**

- Complete project structure (folders, files)
- API module (handles all backend calls)
- Utils module (helper functions)
- File list component (displays files)
- **A working feature you can see in the browser!**

**What You'll Learn:**

- How to structure a real project
- Where different code belongs (and why)
- How modules work together
- How async/await fits into user interactions
- Common pitfalls and how to avoid them

**Prerequisites:**

- Completed Section 2 (or comfortable with modern JS)
- Text editor (VS Code recommended)
- Modern browser
- Basic terminal/command line knowledge

---

## Part 1: Project Structure Setup (15 minutes)

### Creating the Folder Structure

**Open your terminal and create this structure:**

```bash
mkdir mastercam-pdm
cd mastercam-pdm

# Create folders
mkdir frontend
mkdir frontend/js
mkdir frontend/js/components
mkdir frontend/js/utils
mkdir frontend/css
mkdir backend

# Create files
touch frontend/index.html
touch frontend/js/main.js
touch frontend/js/api.js
touch frontend/js/utils/formatting.js
touch frontend/js/utils/validation.js
touch frontend/js/components/FileCard.js
touch frontend/css/styles.css
```

**Your structure should look like:**

```
mastercam-pdm/
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── main.js           (entry point - wires everything)
│       ├── api.js            (all backend communication)
│       ├── components/
│       │   └── FileCard.js   (file display component)
│       └── utils/
│           ├── formatting.js (date/size formatting)
│           └── validation.js (file name validation)
└── backend/
    └── (we'll build this later)
```

---

### Why This Structure?

**Let me explain each piece:**

**`frontend/` - All user-facing code**

- Everything the browser loads
- HTML, CSS, JavaScript

**`js/main.js` - Entry point**

- Like `index.js` in React
- Initializes the app
- Wires everything together
- Loads other modules

**`js/api.js` - API layer**

- ALL backend communication goes here
- Separates network logic from UI logic
- Easy to mock for testing
- Single place to change API endpoints

**Why separate?** If you change backend, you only edit `api.js`, not 50 different files.

**`js/components/` - UI components**

- Reusable pieces of UI
- Each file = one component
- Like React components, but vanilla JS

**`js/utils/` - Helper functions**

- Pure functions (no side effects)
- Used across the app
- Easy to test
- Examples: formatting, validation, calculations

**Manufacturing analogy:**

```
Shop Floor (frontend)
├── Main Assembly Station (main.js)
├── Supplier Interface (api.js)
├── Workstations (components/)
└── Tool Crib (utils/)
```

---

## Part 2: Building the HTML Foundation (10 minutes)

**Open `frontend/index.html` and create this:**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Mastercam PDM</title>

    <!-- Tailwind CSS (for styling - same as your current app) -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Font Awesome (for icons) -->
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    />
  </head>
  <body class="bg-gray-900 text-white min-h-screen">
    <!-- Header -->
    <header class="bg-gray-800 border-b border-gray-700 p-4">
      <div class="container mx-auto">
        <h1 class="text-2xl font-bold">Mastercam PDM System</h1>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto p-4">
      <!-- Loading State -->
      <div id="loading" class="text-center py-8">
        <i class="fas fa-spinner fa-spin text-4xl text-blue-500"></i>
        <p class="mt-2 text-gray-400">Loading files...</p>
      </div>

      <!-- Error State -->
      <div
        id="error"
        class="hidden bg-red-900 border border-red-700 rounded p-4 mb-4"
      >
        <i class="fas fa-exclamation-triangle"></i>
        <span id="error-message"></span>
      </div>

      <!-- File List Container -->
      <div id="file-list" class="hidden">
        <!-- Files will be inserted here by JavaScript -->
      </div>
    </main>

    <!-- JavaScript - type="module" enables imports! -->
    <script type="module" src="js/main.js"></script>
  </body>
</html>
```

**Key points to understand:**

### 1. Three States (Pattern You'll Use Everywhere)

```html
<div id="loading">...</div>
<!-- Shown while fetching -->
<div id="error">...</div>
<!-- Shown on error -->
<div id="file-list">...</div>
<!-- Shown on success -->
```

**This is a CRITICAL pattern:**

```
Initial:    loading=visible, error=hidden, file-list=hidden
Success:    loading=hidden,  error=hidden, file-list=visible
Error:      loading=hidden,  error=visible, file-list=hidden
```

**You'll use this pattern for EVERY async operation.**

### 2. The `type="module"` Script Tag

```html
<script type="module" src="js/main.js"></script>
```

**What this does:**

- Enables `import` and `export` keywords
- JavaScript runs in strict mode automatically
- Script is deferred (runs after HTML loads)
- Each module has its own scope (no global pollution)

**Without `type="module"`, imports won't work!**

### 3. IDs for JavaScript Access

```html
<div id="loading">
  <div id="error">
    <div id="file-list"></div>
  </div>
</div>
```

**We'll target these from JavaScript:**

```javascript
document.getElementById("loading"); // Get the element
```

**Naming convention:** Use kebab-case for IDs (`file-list`, not `fileList`)

---

## Part 3: Building the Utils Module (15 minutes)

### File: `frontend/js/utils/formatting.js`

**This contains pure, reusable functions. Open it and type:**

```javascript
/**
 * Formatting utilities for dates, file sizes, etc.
 * Pure functions - no side effects
 */

/**
 * Formats a date into readable string
 * @param {Date|string} date - Date to format
 * @returns {string} Formatted date like "Oct 10, 2025, 2:30 PM"
 *
 * @example
 * formatDate(new Date()) // "Oct 10, 2025, 2:30 PM"
 * formatDate("2025-10-10T14:30:00Z") // "Oct 10, 2025, 2:30 PM"
 */
export function formatDate(date) {
  // Handle string dates (from backend)
  if (typeof date === "string") {
    date = new Date(date);
  }

  // Validate it's a valid date
  if (!(date instanceof Date) || isNaN(date)) {
    return "Invalid date";
  }

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
 * Formats bytes into human-readable file size
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted size like "1.5 MB"
 *
 * @example
 * formatFileSize(0)       // "0 Bytes"
 * formatFileSize(1024)    // "1 KB"
 * formatFileSize(1536)    // "1.5 KB"
 * formatFileSize(2097152) // "2 MB"
 */
export function formatFileSize(bytes) {
  // Edge case: zero bytes
  if (bytes === 0) return "0 Bytes";

  // Edge case: negative (shouldn't happen, but defensive)
  if (bytes < 0) return "Invalid size";

  // Edge case: not a number
  if (typeof bytes !== "number" || isNaN(bytes)) {
    return "Invalid size";
  }

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB"];

  // Calculate which unit to use
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  // Prevent array out of bounds (files over 1 PB!)
  const index = Math.min(i, sizes.length - 1);

  // Calculate value and round to 2 decimals
  const value = bytes / Math.pow(k, index);
  const rounded = Math.round(value * 100) / 100;

  return `${rounded} ${sizes[index]}`;
}

/**
 * Formats time duration in seconds to readable string
 * @param {number} seconds - Duration in seconds
 * @returns {string} Formatted duration like "2h 30m" or "45s"
 *
 * @example
 * formatDuration(30)    // "30s"
 * formatDuration(90)    // "1m 30s"
 * formatDuration(3665)  // "1h 1m"
 */
export function formatDuration(seconds) {
  // Edge cases
  if (typeof seconds !== "number" || isNaN(seconds) || seconds < 0) {
    return "Invalid duration";
  }

  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);

  const parts = [];
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);
  if (secs > 0 || parts.length === 0) parts.push(`${secs}s`);

  return parts.join(" ");
}

/**
 * Gets relative time string (e.g., "2 hours ago")
 * @param {Date|string} date - Date to compare
 * @returns {string} Relative time like "2 hours ago" or "just now"
 *
 * @example
 * getRelativeTime(new Date()) // "just now"
 * getRelativeTime(new Date(Date.now() - 3600000)) // "1 hour ago"
 */
export function getRelativeTime(date) {
  // Handle string dates
  if (typeof date === "string") {
    date = new Date(date);
  }

  // Validate
  if (!(date instanceof Date) || isNaN(date)) {
    return "Invalid date";
  }

  const seconds = Math.floor((new Date() - date) / 1000);

  // Future dates (edge case)
  if (seconds < 0) {
    return "in the future";
  }

  // Just now
  if (seconds < 60) {
    return "just now";
  }

  const intervals = {
    year: 31536000,
    month: 2592000,
    week: 604800,
    day: 86400,
    hour: 3600,
    minute: 60,
  };

  for (const [unit, secondsInUnit] of Object.entries(intervals)) {
    const interval = Math.floor(seconds / secondsInUnit);
    if (interval >= 1) {
      return `${interval} ${unit}${interval > 1 ? "s" : ""} ago`;
    }
  }

  return "just now";
}
```

**Let's break down the key concepts:**

---

### Understanding Edge Cases (Why We Check Everything)

**Example: formatFileSize**

```javascript
export function formatFileSize(bytes) {
  // Edge case 1: Zero
  if (bytes === 0) return '0 Bytes';
```

**Why check?** Without this:

```javascript
Math.log(0); // -Infinity
Math.floor(-Infinity / Math.log(1024)); // -Infinity
sizes[-Infinity]; // undefined
// Result: "NaN undefined" 💥
```

---

```javascript
// Edge case 2: Negative
if (bytes < 0) return "Invalid size";
```

**Why check?** File sizes should never be negative. If you see this, something's wrong with the data.

**Better to show "Invalid size" than "-5 KB"**

---

```javascript
// Edge case 3: Not a number
if (typeof bytes !== "number" || isNaN(bytes)) {
  return "Invalid size";
}
```

**Why check?** JavaScript is loosely typed:

```javascript
formatFileSize("hello"); // Without check: "NaN undefined"
formatFileSize(null); // Without check: "0 Bytes" (null == 0!)
formatFileSize(undefined); // Without check: "NaN undefined"
```

**These are REAL bugs that happen in production!**

---

```javascript
// Calculate which unit to use
const i = Math.floor(Math.log(bytes) / Math.log(k));

// Edge case 4: Prevent array out of bounds
const index = Math.min(i, sizes.length - 1);
```

**Why?** Our sizes array is `['Bytes', 'KB', 'MB', 'GB', 'TB']`.

What if someone uploads a 1 PB file? (1024 TB)

```javascript
i = 5; // Would try to access sizes[5]
sizes[5]; // undefined
// Result: "1024 undefined" 💥
```

**With Math.min:**

```javascript
index = Math.min(5, 4); // 4
sizes[4]; // "TB"
// Result: "1024 TB" ✅
```

---

### Understanding Pure Functions

**What makes these functions "pure"?**

✅ **Same input = Same output**

```javascript
formatFileSize(1024); // Always returns "1 KB"
```

✅ **No side effects**

```javascript
// Doesn't modify external variables
// Doesn't make API calls
// Doesn't change the DOM
// Just takes input, returns output
```

✅ **Easy to test**

```javascript
// Test is simple:
expect(formatFileSize(1024)).toBe("1 KB");
```

✅ **Reusable anywhere**

```javascript
// Can use in:
// - Main app
// - Admin panel
// - CLI tools
// - Other projects
```

**Manufacturing analogy:** A measuring tool. Give it a part, get a measurement. Doesn't change the part, doesn't affect anything else.

---

### Save and Test

**You can test these immediately in the browser console!**

Open `index.html` in browser, open console (F12), and try:

```javascript
// Won't work yet! Need to serve with a local server
```

**Wait - why not?** ES6 modules require HTTP, not `file://`.

**Quick fix - Use VS Code Live Server:**

1. Install "Live Server" extension in VS Code
2. Right-click `index.html` → "Open with Live Server"
3. Browser opens at `http://localhost:5500`

**Now you can test!** (But we haven't imported them yet, so wait for main.js)

---

## Part 4: Building the API Module (20 minutes)

### File: `frontend/js/api.js`

**This handles ALL communication with the backend:**

```javascript
/**
 * API Module - All backend communication
 * Separates network logic from UI logic
 */

// API base URL - will be configured later
const API_BASE = ""; // Empty = same origin (localhost:8000)

/**
 * Base fetch wrapper with error handling
 * @param {string} endpoint - API endpoint (e.g., '/files')
 * @param {Object} options - Fetch options
 * @returns {Promise<any>} Response data
 * @throws {Error} On network or API errors
 */
async function apiFetch(endpoint, options = {}) {
  try {
    const url = `${API_BASE}${endpoint}`;

    // Set default headers
    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    // Make request
    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Check if response is OK (status 200-299)
    if (!response.ok) {
      // Try to get error message from backend
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;

      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch {
        // Response wasn't JSON, use default message
      }

      throw new Error(errorMessage);
    }

    // Parse and return JSON
    return await response.json();
  } catch (error) {
    // Re-throw with more context
    throw new Error(`API Error: ${error.message}`);
  }
}

/**
 * Gets list of all files
 * @returns {Promise<Object>} Grouped files object
 *
 * @example
 * const files = await getFiles();
 * // { "Active Jobs": [...], "Archive": [...] }
 */
export async function getFiles() {
  // FOR NOW: Return mock data (until backend is ready)
  // We'll replace this with real API call later
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        "Active Jobs": [
          {
            filename: "1234567_ABC123.mcam",
            path: "1234567_ABC123.mcam",
            size: 2048576,
            modified_at: new Date(Date.now() - 3600000).toISOString(), // 1 hour ago
            status: "unlocked",
            locked_by: null,
            locked_at: null,
            description: "Main housing part",
            revision: "2.0",
            is_link: false,
          },
          {
            filename: "1234568_DEF456.mcam",
            path: "1234568_DEF456.mcam",
            size: 1536000,
            modified_at: new Date(Date.now() - 7200000).toISOString(), // 2 hours ago
            status: "locked",
            locked_by: "john_doe",
            locked_at: new Date(Date.now() - 1800000).toISOString(), // 30 min ago
            description: "Fixture plate",
            revision: "1.5",
            is_link: false,
          },
          {
            filename: "1234569_GHI789.mcam",
            path: "1234569_GHI789.mcam",
            size: 4096000,
            modified_at: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
            status: "checked_out_by_user",
            locked_by: "current_user",
            locked_at: new Date(Date.now() - 600000).toISOString(), // 10 min ago
            description: "Cover plate",
            revision: "3.2",
            is_link: false,
          },
        ],
        Archive: [
          {
            filename: "1234560_OLD001.mcam",
            path: "1234560_OLD001.mcam",
            size: 3145728,
            modified_at: new Date(Date.now() - 2592000000).toISOString(), // 30 days ago
            status: "unlocked",
            locked_by: null,
            locked_at: null,
            description: "Old prototype",
            revision: "12.0",
            is_link: false,
          },
        ],
      });
    }, 1000); // Simulate network delay
  });
}

/**
 * Checks out a file (locks it for editing)
 * @param {string} filename - Name of file to checkout
 * @param {string} username - User performing checkout
 * @returns {Promise<Object>} Result object
 */
export async function checkoutFile(filename, username) {
  // FOR NOW: Mock implementation
  console.log(`Checking out ${filename} for ${username}`);
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ success: true, message: "File checked out" });
    }, 500);
  });
}

/**
 * Checks in a file (uploads new version and unlocks)
 * @param {string} filename - Name of file
 * @param {File} fileData - File object from input
 * @param {string} message - Commit message
 * @returns {Promise<Object>} Result object
 */
export async function checkinFile(filename, fileData, message) {
  // FOR NOW: Mock implementation
  console.log(`Checking in ${filename}: ${message}`);
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ success: true, message: "File checked in" });
    }, 1000);
  });
}

/**
 * Cancels a checkout (unlocks without uploading)
 * @param {string} filename - Name of file
 * @param {string} username - User canceling checkout
 * @returns {Promise<Object>} Result object
 */
export async function cancelCheckout(filename, username) {
  // FOR NOW: Mock implementation
  console.log(`Canceling checkout of ${filename} by ${username}`);
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ success: true, message: "Checkout canceled" });
    }, 500);
  });
}
```

**Let's break down the key patterns:**

---

### Pattern 1: The apiFetch Wrapper

**Why wrap fetch()?**

```javascript
async function apiFetch(endpoint, options = {}) {
  // Centralized error handling
  // Centralized header management
  // Centralized base URL
  // One place to add authentication later
}
```

**Without wrapper (scattered everywhere):**

```javascript
// In 20 different files:
const response = await fetch(`http://localhost:8000/files`);
if (!response.ok) throw new Error(...);
const data = await response.json();
```

**With wrapper (clean):**

```javascript
// In 20 different files:
const data = await apiFetch("/files");
```

**Benefits:**

- Change base URL once
- Add auth token once
- Fix error handling once
- DRY (Don't Repeat Yourself)

---

### Pattern 2: Error Handling Chain

```javascript
// Check if response is OK
if (!response.ok) {
  // Try to get detailed error from backend
  try {
    const errorData = await response.json();
    errorMessage = errorData.detail || errorData.message || errorMessage;
  } catch {
    // Backend didn't send JSON, use default
  }
  throw new Error(errorMessage);
}
```

**Why this complexity?**

**Backend might send:**

```json
// Option 1: FastAPI error
{ "detail": "File not found" }

// Option 2: Custom error
{ "message": "File is locked" }

// Option 3: No JSON (500 server error)
<html>Internal Server Error</html>
```

**Our code handles ALL three cases!**

---

### Pattern 3: Mock Data Structure

**Why such detailed mock data?**

```javascript
{
  filename: '1234567_ABC123.mcam',
  path: '1234567_ABC123.mcam',
  size: 2048576,
  modified_at: new Date(Date.now() - 3600000).toISOString(),
  status: 'unlocked',
  // ... lots more fields
}
```

**Because we need to build the UI!**

Without realistic data, we can't:

- Test edge cases (long filenames, huge files)
- Design the UI properly
- Test status indicators
- Test relative timestamps

**Mock data = Real data structure**

---

### Pattern 4: Promises for Mocking

```javascript
export async function getFiles() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        /* data */
      });
    }, 1000); // Simulate network delay
  });
}
```

**Why the setTimeout?**

**Real networks have delays!** Instant responses hide bugs:

- Loading states never show
- Race conditions don't appear
- Users see "flash of loading"

**1 second delay = realistic testing**

---

## Part 5: Building the Main Entry Point (15 minutes)

### File: `frontend/js/main.js`

**This is where everything comes together:**

```javascript
/**
 * Main Entry Point
 * Initializes the app and wires everything together
 */

// Import utilities
import {
  formatDate,
  formatFileSize,
  getRelativeTime,
} from "./utils/formatting.js";

// Import API functions
import { getFiles } from "./api.js";

// DOM elements (cached for performance)
const elements = {
  loading: document.getElementById("loading"),
  error: document.getElementById("error"),
  errorMessage: document.getElementById("error-message"),
  fileList: document.getElementById("file-list"),
};

/**
 * Shows loading state
 */
function showLoading() {
  elements.loading.classList.remove("hidden");
  elements.error.classList.add("hidden");
  elements.fileList.classList.add("hidden");
}

/**
 * Shows error state
 * @param {string} message - Error message to display
 */
function showError(message) {
  elements.loading.classList.add("hidden");
  elements.error.classList.remove("hidden");
  elements.errorMessage.textContent = message;
  elements.fileList.classList.add("hidden");
}

/**
 * Shows success state (file list)
 */
function showFileList() {
  elements.loading.classList.add("hidden");
  elements.error.classList.add("hidden");
  elements.fileList.classList.remove("hidden");
}

/**
 * Renders a single file card
 * @param {Object} file - File data object
 * @returns {string} HTML string for file card
 */
function renderFileCard(file) {
  // Determine status color and icon
  const statusConfig = {
    unlocked: {
      color: "green",
      icon: "unlock",
      text: "Available",
    },
    locked: {
      color: "red",
      icon: "lock",
      text: `Locked by ${file.locked_by}`,
    },
    checked_out_by_user: {
      color: "blue",
      icon: "edit",
      text: "Checked out by you",
    },
  };

  const status = statusConfig[file.status] || statusConfig["unlocked"];

  // Build HTML using template literals
  return `
    <div class="bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-gray-600 transition-colors">
      <!-- Header -->
      <div class="flex items-center justify-between mb-3">
        <h3 class="text-lg font-semibold text-white truncate flex-1">
          ${file.filename}
        </h3>
        <span class="ml-2 px-2 py-1 text-xs rounded bg-${
          status.color
        }-900 text-${status.color}-300 border border-${status.color}-700">
          <i class="fas fa-${status.icon} mr-1"></i>
          ${status.text}
        </span>
      </div>
      
      <!-- Info -->
      <div class="space-y-1 text-sm text-gray-400">
        <div>
          <i class="fas fa-file-alt w-4"></i>
          ${formatFileSize(file.size)}
        </div>
        <div>
          <i class="fas fa-clock w-4"></i>
          Modified ${getRelativeTime(file.modified_at)}
        </div>
        <div>
          <i class="fas fa-code-branch w-4"></i>
          Rev ${file.revision}
        </div>
        ${
          file.description
            ? `
          <div class="mt-2 pt-2 border-t border-gray-700">
            <i class="fas fa-comment w-4"></i>
            ${file.description}
          </div>
        `
            : ""
        }
      </div>
      
      <!-- Actions -->
      <div class="mt-4 flex gap-2">
        ${
          file.status === "unlocked"
            ? `
          <button class="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm transition-colors">
            <i class="fas fa-download mr-1"></i>
            Checkout
          </button>
        `
            : ""
        }
        
        ${
          file.status === "checked_out_by_user"
            ? `
          <button class="px-3 py-1 bg-green-600 hover:bg-green-700 rounded text-sm transition-colors">
            <i class="fas fa-upload mr-1"></i>
            Check In
          </button>
          <button class="px-3 py-1 bg-gray-600 hover:bg-gray-700 rounded text-sm transition-colors">
            <i class="fas fa-times mr-1"></i>
            Cancel
          </button>
        `
            : ""
        }
        
        <button class="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm transition-colors ml-auto">
          <i class="fas fa-history mr-1"></i>
          History
        </button>
      </div>
    </div>
  `;
}

/**
 * Renders all files grouped by category
 * @param {Object} groupedFiles - Files grouped by category
 */
function renderFiles(groupedFiles) {
  let html = "";

  // Iterate through each group
  for (const [groupName, files] of Object.entries(groupedFiles)) {
    html += `
      <div class="mb-6">
        <h2 class="text-xl font-bold mb-3 text-gray-300">
          ${groupName}
          <span class="text-sm font-normal text-gray-500">(${
            files.length
          })</span>
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          ${files.map((file) => renderFileCard(file)).join("")}
        </div>
      </div>
    `;
  }

  elements.fileList.innerHTML = html;
}

/**
 * Loads and displays files
 */
async function loadFiles() {
  try {
    // Show loading state
    showLoading();

    // Fetch files from API
    const groupedFiles = await getFiles();

    // Render files
    renderFiles(groupedFiles);

    // Show success state
    showFileList();
  } catch (error) {
    // Show error state
    console.error("Failed to load files:", error);
    showError(error.message);
  }
}

/**
 * Initialize app on page load
 */
document.addEventListener("DOMContentLoaded", () => {
  console.log("App initializing...");
  loadFiles();
});
```

---

### Understanding the Flow

**Let's trace what happens when you load the page:**

```
1. Browser loads index.html
   ↓
2. Browser sees <script type="module" src="js/main.js">
   ↓
3. Browser loads main.js
   ↓
4. main.js has imports:
   - import from './utils/formatting.js' → Browser loads formatting.js
   - import from './api.js' → Browser loads api.js
   ↓
5. All imports loaded, main.js executes
   ↓
6. DOMContentLoaded event fires
   ↓
7. Event listener calls loadFiles()
   ↓
8. loadFiles() runs:
   - Calls showLoading()
   - Calls await getFiles() (pauses here)
   - getFiles() waits 1 second (mock delay)
   - getFiles() resolves with data
   - Calls renderFiles(data)
   - Calls showFileList()
   ↓
9. User sees file list!
```

---

### The State Machine Pattern

```javascript
function showLoading() {
  elements.loading.classList.remove("hidden");
  elements.error.classList.add("hidden");
  elements.fileList.classList.add("hidden");
}
```

**This ensures only ONE state is visible:**

```
State: LOADING
  loading:   visible
  error:     hidden
  fileList:  hidden

State: ERROR
  loading:   hidden
  error:     visible
  fileList:  hidden

State: SUCCESS
  loading:   hidden
  error:     hidden
  fileList:  visible
```

**No overlaps, no confusion!**

---

### Template Literals for HTML

**This is where template literals shine:**

```javascript
return `
  <div class="bg-gray-800 rounded-lg p-4">
    <h3>${file.filename}</h3>
    <div>${formatFileSize(file.size)}</div>
    ${file.description ? `<p>${file.description}</p>` : ""}
  </div>
`;
```

**Notice:**

- Multi-line strings (no `+` concatenation)
- Variables inserted with `${}`
- Function calls inside `${formatFileSize(file.size)}`
- Conditional rendering `${condition ? html : ''}`

**This is basically React JSX, but in vanilla JS!**

---

## Part 6: See It Work! (5 minutes)

**Open in browser with Live Server. You should see:**

1. **Loading spinner** (1 second)
2. **File list appears** with:
   - Active Jobs group (3 files)
   - Archive group (1 file)
   - Different status colors
   - Formatted sizes ("2 MB", etc.)
   - Relative times ("1 hour ago", etc.)
   - Action buttons

**Open the console (F12) - you should see:**

```
App initializing...
```

**No errors!**

---

## Part 7: Testing the Components (10 minutes)

**Let's test individual functions in the console:**

### Test 1: Formatting functions

```javascript
// Import utils (console supports imports in modules!)
import {
  formatFileSize,
  formatDate,
  getRelativeTime,
} from "./js/utils/formatting.js";

// Test formatFileSize
formatFileSize(0); // "0 Bytes"
formatFileSize(1024); // "1 KB"
formatFileSize(2048576); // "2 MB"
formatFileSize(-100); // "Invalid size"
formatFileSize("hello"); // "Invalid size"

// Test formatDate
formatDate(new Date()); // "Oct 10, 2025, 3:45 PM"
formatDate("invalid"); // "Invalid date"

// Test getRelativeTime
getRelativeTime(new Date()); // "just now"
getRelativeTime(new Date(Date.now() - 60000)); // "1 minute ago"
```

**Everything works!** ✅

### Test 2: API functions

```javascript
import { getFiles } from "./js/api.js";

// This returns a Promise
const filesPromise = getFiles();
console.log(filesPromise); // Promise { <pending> }

// To get the data, use await (only in async context)
// In console, top-level await works:
const files = await getFiles();
console.log(files); // { 'Active Jobs': [...], 'Archive': [...] }
```

**You see the data!** ✅

---

## Section 3 Complete! 🎉

### What You Just Built

✅ **Project structure** - organized folders and files  
✅ **Utils module** - pure, reusable functions  
✅ **API module** - centralized backend communication  
✅ **Main app** - wires everything together  
✅ **Working feature** - file list that displays real(ish) data

### The "Aha!" Moments

**1. Async/await in action:**

```javascript
async function loadFiles() {
  const files = await getFiles(); // Pauses here!
  renderFiles(files); // Then continues
}
```

**2. Array methods transforming data:**

```javascript
files.map((file) => renderFileCard(file)).join("");
```

**3. Template literals building UI:**

```javascript
`<div>${file.filename}</div>`;
```

**4. Modules organizing code:**

```javascript
import { formatDate } from "./utils/formatting.js";
```

**5. All the concepts working TOGETHER!**

---

## Checkpoint Questions

1. Why do we use three separate state elements (loading, error, fileList)?
2. Why wrap fetch() in an apiFetch function?
3. What makes the formatting functions "pure"?
4. Why do we check for edge cases like negative file sizes?
5. How does the file card know which buttons to show?

<details>
<summary>Answers</summary>

1. To ensure only ONE state is visible at a time - prevents UI glitches where loading AND content show simultaneously
2. Centralized error handling, base URL, headers - change once instead of everywhere
3. Same input = same output, no side effects, don't modify external state
4. Defensive programming - better to show "Invalid size" than crash with "NaN undefined"
5. Conditional rendering based on `file.status` - uses ternary operator in template literal

</details>

---

## What's Next: Section 4 Preview

**Section 4: Event Handling & User Interactions**

**What we'll build:**

- Click handlers for buttons
- Checkout/checkin flow
- Form handling
- Real-time updates
- Error handling
- Loading states

**This is where it gets REALLY interactive!**

---

**Ready for Section 4?** Say **"Start Section 4"** and we'll make those buttons actually DO something! 🚀

Or if you have questions about Section 3, ask away! This was a LOT of code. 💪
