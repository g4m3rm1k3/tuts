Let's get started on the frontend. We're going to apply the exact same principles—**Separation of Concerns**, **Modularity**, and **Single Responsibility**—to our JavaScript code.

---

## Phase 4: Structuring the Frontend Application

Just as we did with the backend, our first move is to create a clean, professional directory structure. Then, we'll start by moving the most generic, reusable pieces of code into their own module.

---

### Stage 4.1: Creating the Frontend Structure & Utility Module

We'll begin by creating our folder structure and a "toolbox" module for our helper functions (`formatDate`, `debounce`, etc.).

#### The "Why"

Creating a dedicated `helpers.js` file is a great first step. These utility functions are not tied to any specific feature; they're general-purpose tools we might need anywhere in the application. Isolating them makes our main logic files cleaner and promotes reusability. It’s the difference between having a well-organized toolbox and leaving your tools scattered all over the workshop floor.

To make this work, we'll start using modern JavaScript Modules (`import`/`export`). This is the standard, professional way to share code between different JavaScript files, replacing the old approach of having everything in one giant global scope.

#### Your Action Items

1. **Create the Folder Structure**: Inside your `frontend` directory, create a `js` folder. Inside `js`, create the following subfolders:

- `api`
- `components`
- `services`
- `state`
- `utils`

2. **Create the Helpers Module**: Create a new file at `frontend/js/utils/helpers.js`. Move all the utility functions from the bottom of your `script.js` file into it. We'll add the `export` keyword to each one to make it available to other files.

```javascript
// frontend/js/utils/helpers.js

export function formatBytes(bytes) {
  if (!bytes || bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

export function debounce(func, delay) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), delay);
  };
}

export function formatDate(dateString) {
  if (!dateString) return "Unknown";
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return "Invalid Date";
    const options = {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    };
    return date.toLocaleString(undefined, options);
  } catch (error) {
    console.error("Error formatting date:", dateString, error);
    return "Date Error";
  }
}

export function formatDuration(totalSeconds) {
  if (totalSeconds < 60) {
    return `${Math.round(totalSeconds)}s`;
  }
  const days = Math.floor(totalSeconds / 86400);
  totalSeconds %= 86400;
  const hours = Math.floor(totalSeconds / 3600);
  totalSeconds %= 3600;
  const minutes = Math.floor(totalSeconds / 60);

  let parts = [];
  if (days > 0) parts.push(`${days}d`);
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);

  return parts.join(" ") || "0m";
}
```

3. **Create the Main Entrypoint**: Create a new file at `frontend/js/main.js`. For now, this file will be simple. It will be the central starting point for our application.

```javascript
// frontend/js/main.js

// We use the 'import' keyword to use functions from other modules.
import { formatDate } from "./utils/helpers.js";

console.log("Application main.js loaded!");

// Example of using an imported function:
console.log("Current date formatted:", formatDate(new Date()));

document.addEventListener("DOMContentLoaded", async function () {
  console.log(
    "DOM fully loaded and parsed. App initialization will start here."
  );
  // All the logic from your old 'DOMContentLoaded' will eventually move here.
});
```

4. **Update `index.html`**: This is a crucial step. In your `index.html` file, find the `<script>` tag at the very bottom and change it to load our new `main.js` file **as a module**.

   **Change this:**
   `<script src="/static/js/script.js"></script>`

   **To this:**
   `<script src="/static/js/main.js" type="module"></script>`

Adding `type="module"` is what enables the `import` and `export` syntax and unlocks a modern, modular workflow.

---

We have now officially started our frontend refactor. We've established our project structure and created our first reusable module.

Confirm you've made these changes, and then we'll move on to the next major step: creating a dedicated API service to handle all communication with our backend.
