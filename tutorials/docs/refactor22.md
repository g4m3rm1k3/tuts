Great. Let's tackle the slide-out configuration panel next. This will follow the same pattern but for a slightly different type of UI element.

---

### Stage 6.5: Refactoring the Configuration Panel

We will now convert the configuration panel—the part of the UI that slides out from the right—into its own self-contained component. This component will manage its own visibility, tab switching, and data loading for things like the health check.

#### The "Why"

This step is about **encapsulation**. The configuration panel is a complex piece of the UI with its own internal state (which tab is active?) and its own behaviors (fetching health status, saving settings). By moving all of this logic into a dedicated `ConfigPanel.js` module, we hide that complexity from the rest of the application. Our main `main.js` file no longer needs to know anything about how the panel works; it only needs to know how to tell it to open or close.

#### Your Action Items

1. **Update `index.html`**:

- Find the settings button in the header and ensure it has an `id` and no `onclick` attribute.
  **Change this:**
  `<button onclick="toggleConfigPanel()" class="btn btn-secondary !px-3" title="Settings">`
  **To this:**
  `<button id="configBtn" class="btn btn-secondary !px-3" title="Settings">`

- Next, find the large `<div id="configPanel" ...>` and replace that entire `div` with a `<template>` tag.

```html
<template id="template-config-panel">
  <div
    class="fixed inset-y-0 right-0 w-full max-w-md transform translate-x-full transition-transform duration-300 panel-bg shadow-lg p-6 z-50 overflow-y-auto"
  >
    <div
      class="flex justify-between items-center pb-4 mb-4 border-b border-gray-200 dark:border-gray-700"
    >
      <h3 class="text-2xl font-semibold">Settings</h3>
      <button data-action="close">
        <i class="fa-solid fa-xmark text-2xl"></i>
      </button>
    </div>
  </div>
</template>
```

2. **Create the Config Panel Component**:
   Create a new file at `frontend/js/components/ConfigPanel.js`. This module will export a single function that sets up and controls the panel.

```javascript
// frontend/js/components/ConfigPanel.js

let panelElement = null; // This will hold the live DOM element for the panel

function closePanel() {
  if (panelElement) {
    panelElement.classList.add("translate-x-full");
    // Remove the element from the DOM after the transition is complete
    panelElement.addEventListener(
      "transitionend",
      () => {
        panelElement.remove();
        panelElement = null;
      },
      { once: true }
    );
  }
}

function openPanel() {
  if (panelElement) return; // Already open

  const template = document.getElementById("template-config-panel");
  const content = template.content.cloneNode(true);
  panelElement = content.firstElementChild;

  // Add event listeners for closing
  panelElement
    .querySelector('[data-action="close"]')
    .addEventListener("click", closePanel);

  // Add event listeners for tab switching
  panelElement.querySelectorAll(".config-tab").forEach((tabButton) => {
    tabButton.addEventListener("click", () => {
      const tabName = tabButton.id.replace("Tab", "");
      switchTab(tabName);
    });
  });

  document.body.appendChild(panelElement);

  // Trigger the slide-in animation
  requestAnimationFrame(() => {
    panelElement.classList.remove("translate-x-full");
  });
}

function switchTab(tabName) {
  if (!panelElement) return;

  // Update tab buttons
  panelElement.querySelectorAll(".config-tab").forEach((btn) => {
    btn.classList.toggle("active", btn.id === `${tabName}Tab`);
  });

  // Update tab content
  panelElement.querySelectorAll(".config-tab-content").forEach((content) => {
    content.classList.toggle("hidden", content.id !== `${tabName}Content`);
  });

  // Load data if switching to a data-heavy tab
  if (tabName === "health") {
    // TODO: Call a function to refresh health status
    console.log("Switched to Health tab. Need to load data.");
  }
}

// This is the main function we will export.
// It attaches the openPanel function to a trigger button.
export function setupConfigPanel(triggerButtonId) {
  const triggerButton = document.getElementById(triggerButtonId);
  if (triggerButton) {
    triggerButton.addEventListener("click", openPanel);
  }
}
```

3. **Update `main.js` to Use the Component**:
   Finally, open `frontend/js/main.js` and tell it to set up our new config panel.

```javascript
// frontend/js/main.js

// ... (other imports)
import { showDashboardDialog } from "./components/DashboardModal.js";
import { setupConfigPanel } from "./components/ConfigPanel.js"; // NEW IMPORT

// ... (render function and other logic) ...

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded and parsed.");

  // --- ADD EVENT LISTENERS FOR STATIC UI ELEMENTS ---
  document
    .getElementById("newFileBtn")
    ?.addEventListener("click", showNewUploadDialog);
  document
    .getElementById("dashboardBtn")
    ?.addEventListener("click", showDashboardDialog);

  // NEW: Set up the config panel and connect it to its trigger button
  setupConfigPanel("configBtn");

  // --- INITIALIZE APP ---
  initialize();
});
```

---

Now the logic for the entire configuration panel is encapsulated in its own module. Our `main.js` file remains clean, only responsible for telling the panel which button should trigger it.

We are nearing the end of the refactor. The last major piece of logic is handling the real-time updates. Ready to create our WebSocket service?
