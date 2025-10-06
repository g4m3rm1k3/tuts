Let's do it. We are now entering **Phase 6: Rebuilding the UI with Components**. This is where our frontend will transform from a single script manipulating a static page into a dynamic, modern application.

---

### Stage 6.1: Building Your First Component

Our first goal is to stop building massive HTML strings in JavaScript. Instead, we'll create our first reusable UI "component"—the `FileCard`. We'll use the `<template>` tag we discussed earlier to define its HTML structure.

#### The "Why": A LEGO® Brick Approach

Think of your current UI as a sculpture carved from a single, giant block of wood. If you want to change the nose, you have to carefully carve the whole face again.

A **component-based architecture** is like building with LEGO® bricks.

- **Reusable:** We'll design one `FileCard` "brick." Then we can reuse it for every single file in our list.
- **Maintainable:** If you want to change how a file is displayed (e.g., add a new button), you just modify the single `FileCard` brick. You don't have to rebuild the entire wall.
- **Isolated:** The `FileCard` component will contain its own HTML structure and the JavaScript logic to populate it. This makes it self-contained and much easier to understand and debug.

#### Your Action Items

1. **Create the HTML Template in `index.html`**: Open `frontend/index.html`. Just before the closing `</body>` tag (after all the modal `<div>`s), add the following `<template>` block. This is the HTML blueprint for a single file card.

```html
<template id="file-card-template">
  <div
    class="py-6 px-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-300 dark:border-gray-600 hover:shadow-lg transition-shadow"
    data-file-id=""
  >
    <div
      class="flex flex-col md:flex-row md:items-start md:justify-between space-y-4 md:space-y-0"
    >
      <div class="flex-grow">
        <div class="flex items-center space-x-3 mb-2 flex-wrap">
          <h4
            class="text-lg font-semibold text-gray-900 dark:text-white"
            data-field="filename"
          ></h4>
          <span
            class="text-xs font-semibold px-2.5 py-1 rounded-full"
            data-field="revision"
          ></span>
          <span
            class="text-xs font-semibold px-2.5 py-1 rounded-full"
            data-field="status"
          ></span>
        </div>
        <p
          class="italic text-gray-700 dark:text-gray-300 text-sm mb-3"
          data-field="description"
        ></p>
        <div
          class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-gray-600 dark:text-gray-400"
        >
          <div class="flex items-center space-x-2" data-field="size-container">
            <i class="fa-solid fa-hard-drive"></i
            ><span data-field="size"></span>
          </div>
          <div class="flex items-center space-x-2">
            <i class="fa-solid fa-clock"></i
            ><span data-field="modified_at"></span>
          </div>
        </div>
        <div
          class="flex items-center space-x-2 text-sm mt-2"
          data-field="lock-info"
        ></div>
      </div>
      <div
        class="flex items-center space-x-2 flex-wrap"
        data-field="action-buttons"
      ></div>
    </div>
  </div>
</template>
```

2. **Create the JavaScript Component**: Create a new file at `frontend/js/components/FileCard.js`. This function will be our component. Its job is to take file data, stamp it into the template, and return a live HTML element.

```javascript
// frontend/js/components/FileCard.js
import { formatDate, formatBytes } from "../utils/helpers.js";

// Get the template from the DOM once and reuse it
const template = document.getElementById("file-card-template");

export function createFileCard(file, currentUser, isAdminMode) {
  // Create a fresh copy of the template's content
  const card = template.content.cloneNode(true).firstElementChild;

  // --- Populate the static data ---
  card.dataset.fileId = file.filename;
  card.querySelector('[data-field="filename"]').textContent = file.filename;
  card.querySelector('[data-field="description"]').textContent =
    file.description || "";
  card.querySelector(
    '[data-field="modified_at"]'
  ).textContent = `Modified: ${formatDate(file.modified_at)}`;

  // --- Handle conditional visibility and content ---
  const revisionEl = card.querySelector('[data-field="revision"]');
  if (file.revision) {
    revisionEl.textContent = `REV ${file.revision}`;
    revisionEl.classList.remove("hidden");
  } else {
    revisionEl.classList.add("hidden");
  }

  const sizeContainer = card.querySelector('[data-field="size-container"]');
  if (file.is_link) {
    sizeContainer.classList.add("hidden");
  } else {
    card.querySelector(
      '[data-field="size"]'
    ).textContent = `Size: ${formatBytes(file.size)}`;
    sizeContainer.classList.remove("hidden");
  }

  // --- Handle complex state: Status Badge and Lock Info ---
  const statusEl = card.querySelector('[data-field="status"]');
  const lockInfoEl = card.querySelector('[data-field="lock-info"]');

  statusEl.className = "text-xs font-semibold px-2.5 py-1 rounded-full"; // Reset classes
  lockInfoEl.innerHTML = "";

  if (file.is_link) {
    statusEl.classList.add(
      "bg-purple-100",
      "text-purple-900",
      "dark:bg-purple-900",
      "dark:text-purple-200"
    );
    statusEl.innerHTML = `<i class="fa-solid fa-link mr-1"></i>Links to ${file.master_file}`;
  } else {
    switch (file.status) {
      case "unlocked":
        statusEl.classList.add(
          "bg-green-100",
          "text-green-900",
          "dark:bg-green-900",
          "dark:text-green-200"
        );
        statusEl.textContent = "Available";
        break;
      case "locked":
        statusEl.classList.add(
          "bg-red-100",
          "text-red-900",
          "dark:bg-red-900",
          "dark:text-red-200"
        );
        statusEl.textContent = `Locked by ${file.locked_by}`;
        lockInfoEl.innerHTML = `<i class="fa-solid fa-lock text-red-500"></i><span>Locked by: <strong>${
          file.locked_by
        }</strong> at ${formatDate(file.locked_at)}</span>`;
        break;
      case "checked_out_by_user":
        statusEl.classList.add(
          "bg-blue-100",
          "text-blue-900",
          "dark:bg-blue-900",
          "dark:text-blue-200"
        );
        statusEl.textContent = "Checked out by you";
        lockInfoEl.innerHTML = `<i class="fa-solid fa-lock-open text-blue-500"></i><span>You checked this out at ${formatDate(
          file.locked_at
        )}</span>`;
        break;
    }
  }

  // --- Generate Action Buttons ---
  // For now, we'll keep this logic here. In a more advanced setup,
  // buttons could even be their own components!
  const buttonsContainer = card.querySelector('[data-field="action-buttons"]');
  buttonsContainer.innerHTML = getActionButtons(file, currentUser, isAdminMode);

  return card;
}

// This function can stay here for now as a helper for the FileCard component.
function getActionButtons(file, currentUser, isAdminMode) {
  // NOTE: This is the same `getActionButtons` function from your original script.
  // Copy the full function here. For brevity, I've added a placeholder.
  return `<button class="btn btn-secondary js-history-btn" data-filename="${file.filename}">History</button>`;
}
```

3. **Update `main.js` to Use the Component**: Finally, replace the `render` function in `frontend/js/main.js` with this new version. Notice it no longer builds any HTML strings. It's now an orchestrator that uses our `createFileCard` component.

```javascript
// frontend/js/main.js

import { formatDate } from "./utils/helpers.js";
import { getConfig, getFiles } from "./api/service.js";
import { setState, subscribe, getState } from "./state/store.js";
import { createFileCard } from "./components/FileCard.js"; // NEW IMPORT

const fileListEl = document.getElementById("fileList");

function render(state) {
  console.log("🚀 Render triggered!", state);

  // Clear the current file list
  fileListEl.innerHTML = "";

  if (!state.isConfigured) {
    fileListEl.innerHTML = `<p class="text-center text-gray-500">Application is not configured.</p>`;
    return;
  }

  const fileGroups = Object.keys(state.groupedFiles).sort();
  if (fileGroups.length === 0) {
    fileListEl.innerHTML = `<p class="text-center text-gray-500">No files found.</p>`;
    return;
  }

  // Loop through the state and render components
  for (const groupName of fileGroups) {
    const groupDetails = document.createElement("details");
    groupDetails.className = "bg-white dark:bg-gray-800 rounded-lg shadow-md";
    groupDetails.open = true; // Keep groups open for now

    groupDetails.innerHTML = `
     <summary class="cursor-pointer p-4 font-semibold text-lg">
       <i class="fa-solid fa-folder mr-2 text-amber-500"></i>${groupName}
     </summary>
     <div class="p-4 space-y-4"></div>
   `;

    const filesContainer = groupDetails.querySelector(".space-y-4");

    for (const file of state.groupedFiles[groupName]) {
      // HERE is the magic: we create a component for each file
      const fileCardElement = createFileCard(
        file,
        state.currentUser,
        state.isAdmin
      );
      filesContainer.appendChild(fileCardElement);
    }

    fileListEl.appendChild(groupDetails);
  }
}

// ... the rest of your main.js file (initialize, subscribe, etc.) remains the same ...
```

---

With this step, you've officially built your first reusable UI component\! We've cleanly separated the **structure** (the HTML `<template>`) from the **behavior** (the JavaScript `createFileCard` function). This is a massive leap forward in making your code organized and maintainable.

Let me know when you're ready, and we'll apply this same pattern to refactor the modals.
