Let's get it done. We'll now apply our component pattern to the "Dashboard Modal," which is a perfect example of a self-contained feature with its own data-fetching needs.

---

### Stage 6.4: Refactoring the Dashboard Modal

We will now convert the static "Dashboard Modal" into a component that fetches its own data when opened.

#### The "Why"

This step demonstrates how a component can be responsible for its entire lifecycle. The dashboard component doesn't need its data when the page first loads; it only needs it when the user clicks the "Dashboard" button. By encapsulating this data-fetching logic within the component itself, we make our application more efficient (loading data only when needed) and even more modular.

#### Your Action Items

1. **Update `index.html`**:

- Find the large `<div id="dashboardModal" ...>` and replace that entire `div` with this new `<template>` tag. We're just templating the "frame" of the dashboard; the content will be loaded dynamically.

```html
<template id="template-dashboard-modal">
  <div
    class="panel-bg rounded-xl shadow-lg w-full max-w-4xl flex flex-col max-h-[90vh]"
  >
    <div
      class="flex-shrink-0 flex justify-between items-center p-6 pb-4 border-b border-gray-200 dark:border-gray-700"
    >
      <h3 class="text-xl font-semibold text-gray-900 dark:text-accent">
        <i class="fa-solid fa-chart-line mr-2"></i>Activity Dashboard
      </h3>
      <button
        class="text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-white"
        data-action="close"
      >
        <i class="fa-solid fa-xmark text-2xl"></i>
      </button>
    </div>
    <div
      id="dashboardContent"
      class="flex-grow min-h-0 p-6 flex flex-col md:flex-row md:space-x-6"
    ></div>
  </div>
</template>
```

2. **Update the API Service**:
   Open `frontend/js/api/service.js` and add the new functions needed to fetch the dashboard data.

```javascript
// frontend/js/api/service.js
// ... (add these new functions to the end of the file)

/**
 * Fetches statistics for the dashboard, like active checkouts.
 */
export async function getDashboardStats() {
  const token = getAuthToken();
  const response = await fetch(`${BASE_URL}/dashboard/stats`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return handleResponse(response);
}

/**
 * Fetches the recent activity feed.
 */
export async function getActivityFeed(limit = 50, offset = 0) {
  const token = getAuthToken();
  const response = await fetch(
    `${BASE_URL}/dashboard/activity?limit=${limit}&offset=${offset}`,
    {
      headers: { Authorization: `Bearer ${token}` },
    }
  );
  return handleResponse(response);
}
```

3. **Create the Dashboard Modal Logic**:
   Create a new file at `frontend/js/components/DashboardModal.js`. This file will contain all the logic for showing the modal, fetching its data, and rendering the content.

```javascript
// frontend/js/components/DashboardModal.js

import { Modal } from "./Modal.js";
import { getDashboardStats, getActivityFeed } from "../api/service.js";
import { formatDate, formatDuration } from "../utils/helpers.js";

export async function showDashboardDialog() {
  const template = document.getElementById("template-dashboard-modal");
  const content = template.content.cloneNode(true);
  const modal = new Modal(content);
  modal.show();

  const dashboardContentEl =
    modal.modalElement.querySelector("#dashboardContent");
  dashboardContentEl.innerHTML = `<div class="flex justify-center items-center w-full h-full"><i class="fa-solid fa-spinner fa-spin text-4xl text-accent"></i></div>`;

  try {
    const statsData = await getDashboardStats();
    // We can fetch activity feed data here too if needed

    const checkoutsHtml = renderActiveCheckouts(statsData.active_checkouts);

    // In a full implementation, we'd render the activity feed as well
    dashboardContentEl.innerHTML = `
   <div class="md:w-1/2 flex flex-col">${checkoutsHtml}</div>
   <div class="md:w-1/2 flex flex-col mt-6 md:mt-0 md:border-l md:pl-6 border-gray-200 dark:border-gray-700">
     <h4 class="text-lg font-semibold mb-4">Recent Activity</h4>
     <p class="text-gray-500 text-sm">Activity feed rendering is pending refactor.</p>
   </div>
  `;
  } catch (error) {
    dashboardContentEl.innerHTML = `<p class="text-red-500">Error loading dashboard: ${error.message}</p>`;
  }
}

function renderActiveCheckouts(checkouts) {
  if (checkouts.length === 0) {
    return `<h4 class="text-lg font-semibold mb-4">Active Checkouts</h4><p>No files are currently checked out.</p>`;
  }

  const rows = checkouts
    .map(
      (item) => `
  <tr>
   <td class="px-4 py-3 text-sm font-medium">${item.filename}</td>
   <td class="px-4 py-3 text-sm">${item.locked_by}</td>
   <td class="px-4 py-3 text-sm">${formatDuration(item.duration_seconds)}</td>
  </tr>
 `
    )
    .join("");

  return `
  <h4 class="text-lg font-semibold mb-4 flex-shrink-0">Active Checkouts</h4>
  <div class="overflow-x-auto flex-grow">
   <table class="min-w-full">
    <thead class="bg-gray-50 dark:bg-gray-700">
     <tr>
      <th class="px-4 py-2 text-left text-xs font-medium uppercase">File</th>
      <th class="px-4 py-2 text-left text-xs font-medium uppercase">User</th>
      <th class="px-4 py-2 text-left text-xs font-medium uppercase">Duration</th>
     </tr>
    </thead>
    <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">${rows}</tbody>
   </table>
  </div>
 `;
}
```

4. **Update `main.js` to Trigger the Modal**:
   Finally, open `frontend/js/main.js` to wire up the "Dashboard" button in the header.

```javascript
// frontend/js/main.js

// ... (other imports)
import { showDashboardDialog } from "./components/DashboardModal.js"; // NEW IMPORT

// ... (render function and other logic) ...

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded and parsed.");

  // --- ADD EVENT LISTENERS FOR STATIC BUTTONS ---
  document
    .getElementById("newFileBtn")
    ?.addEventListener("click", showNewUploadDialog);

  // NEW: Add listener for the dashboard button
  document
    .getElementById("dashboardBtn")
    ?.addEventListener("click", showDashboardDialog);

  // --- INITIALIZE APP ---
  initialize();
});
```

---

Excellent. We've now converted another major piece of UI into a self-contained, on-demand component. The application is becoming significantly more modular and efficient.

Ready for the next step?
