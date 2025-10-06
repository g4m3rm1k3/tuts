Excellent. Let's apply the same component-based pattern to our modals. This will dramatically clean up both our `index.html` and our JavaScript.

---

## Stage 6.2: Creating a Reusable Modal Component

Instead of having unique JavaScript logic for every single modal, we'll create a generic, reusable `Modal` component. Its only job is to handle the common behavior of all modals: showing an overlay, displaying a content panel, and closing. We'll start by refactoring the "Check-in Modal".

### The "Why"

This is the **Don't Repeat Yourself (DRY)** principle in action. We'll write the logic for showing and hiding a modal _once_ inside our `Modal.js` component. Then, for every new modal we need, we simply provide a different HTML template for its content.

This makes our code:

- **Consistent:** All modals will look and behave exactly the same.
- **Efficient:** We're not writing redundant code to toggle classes for every single modal.
- **Maintainable:** If we want to change the modal's closing animation, we only have to edit one file: `Modal.js`.

### Your Action Items

1. **Update `index.html` to Use a Template**:
   Find the large `<div id="checkinModal" ...>` in your `index.html` file. We are going to convert it into a `<template>`. Replace that entire `div` with this `<template>` tag. Notice we only need the _inner_ content of the modal, not the background overlay.

```html
<template id="template-checkin-modal">
  <div class="panel-bg rounded-xl shadow-lg p-6 w-full max-w-lg">
    <form id="checkinForm">
      <h3
        id="checkinModalTitle"
        class="text-xl font-semibold text-gray-900 dark:text-accent mb-4"
      >
        Check In File
      </h3>
      <div class="mb-4">
        <label for="commitMessage" class="block text-sm font-medium mb-1"
          >Describe your changes:</label
        >
        <textarea
          id="commitMessage"
          name="commitMessage"
          rows="3"
          required
          class="input-field"
        ></textarea>
      </div>
      <div class="mb-4">
        <label for="checkinFileUpload" class="block text-sm font-medium mb-1"
          >Upload the updated file:</label
        >
        <input
          id="checkinFileUpload"
          name="file"
          type="file"
          required
          class="w-full text-sm text-gray-500 dark:text-gray-400"
        />
      </div>
      <div class="mb-6">
        <label class="block text-sm font-medium mb-2"
          >Revision Increment:</label
        >
      </div>
      <div class="flex justify-end space-x-3">
        <button type="button" class="btn btn-secondary" data-action="close">
          Cancel
        </button>
        <button type="submit" class="btn btn-info">Submit Check-in</button>
      </div>
    </form>
  </div>
</template>
```

2. **Create the Generic Modal Component**:
   Create a new file at `frontend/js/components/Modal.js`. This class will be our reusable modal engine.

```javascript
// frontend/js/components/Modal.js

export class Modal {
  constructor(contentElement) {
    this.contentElement = contentElement;
    this.modalElement = null;
  }

  show() {
    const modalHtml = `
   <div class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center p-4 z-50">
   </div>
  `;
    const modalFragment = document
      .createRange()
      .createContextualFragment(modalHtml);
    this.modalElement = modalFragment.firstElementChild;

    // Append the user-provided content into our modal panel
    this.modalElement.appendChild(this.contentElement);

    // Add event listeners for closing the modal
    this.modalElement.addEventListener("click", (e) => {
      if (
        e.target === this.modalElement ||
        e.target.closest('[data-action="close"]')
      ) {
        this.close();
      }
    });

    document.body.appendChild(this.modalElement);
  }

  close() {
    if (this.modalElement) {
      this.modalElement.remove();
      this.modalElement = null;
    }
  }
}
```

3. **Create the Specific Check-in Modal Logic**:
   Now, create another new file at `frontend/js/components/CheckinModal.js`. This file will contain the specific logic just for the check-in modal, using our generic `Modal` component.

```javascript
// frontend/js/components/CheckinModal.js

import { Modal } from "./Modal.js";

export function showCheckinDialog(file) {
  const template = document.getElementById("template-checkin-modal");
  const content = template.content.cloneNode(true);

  // Populate the title with the filename
  content.querySelector(
    "#checkinModalTitle"
  ).textContent = `Check In: ${file.filename}`;

  const modal = new Modal(content);

  // Add the specific logic for this form
  const form = modal.modalElement.querySelector("#checkinForm");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    // TODO: Add logic to call the API service to check in the file.
    console.log(`Submitting check-in for ${file.filename}`);
    modal.close();
  });

  modal.show();
}
```

4. **Connect the Button in `FileCard.js`**:
   Finally, we need to make the "Check In" button actually open our new modal. Open `frontend/js/components/FileCard.js` and make these two changes:

```javascript
// frontend/js/components/FileCard.js

import { formatDate, formatBytes } from "../utils/helpers.js";
// NEW: Import the function to show our modal
import { showCheckinDialog } from "./CheckinModal.js";

// ... (rest of the file is the same until the end) ...

export function createFileCard(file, currentUser, isAdminMode) {
  // ... (all the code to create and populate the card) ...

  // --- Generate Action Buttons ---
  const buttonsContainer = card.querySelector('[data-field="action-buttons"]');
  buttonsContainer.innerHTML = getActionButtons(file, currentUser, isAdminMode);

  // --- NEW: Add Event Listeners ---
  const checkinBtn = buttonsContainer.querySelector(".js-checkin-btn");
  if (checkinBtn) {
    checkinBtn.addEventListener("click", () => {
      showCheckinDialog(file);
    });
  }

  // We will add more listeners here for other buttons later.

  return card;
}

function getActionButtons(file, currentUser, isAdminMode) {
  // Your getActionButtons function remains the same. Just ensure it adds
  // a `js-checkin-btn` class to the check-in button.
  // e.g., <button class="btn ... js-checkin-btn" ...>Check In</button>
  return `<button class="btn btn-info js-checkin-btn" data-filename="${file.filename}">Check In</button>`;
}
```

---

Now, when you click the "Check In" button on a file card, it should open our new, refactored modal\!

We have successfully created a generic, reusable modal system. We can now apply this same pattern to the other modals (`newUploadModal`, `dashboardModal`, etc.) very quickly.

Let me know when you're ready to refactor the "New Upload" modal next.
