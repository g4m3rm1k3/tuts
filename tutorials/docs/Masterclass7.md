Let's get started. This part introduces a significant new challenge and a powerful new skill: handling file uploads and form data. We're moving beyond simple actions to transactions that carry a payload.

---

### **Part 7: Feature Slice 3 - "Check-In" (Masterclass Edition)**

**The Goal:** A user who has a file checked out needs to upload a new version and provide a comment explaining their changes. This is the core "save" operation of our version control system.

This feature is more complex because the frontend isn't just telling the backend _to do_ something; it's sending _data_ (a file and a comment) for the backend to process.

---

#### **🚩 Step 1: Backend - Designing the Endpoint**

- **Action:** Creating a new version of a resource. This is a "write" operation that includes data.
- **HTTP Method:** **`POST`** is the correct choice. We are submitting data to create a new sub-resource (a new revision).
- **URL:** The action is on a specific file, so `/api/files/{filename}/checkin` is a perfect RESTful URL.
- **Request Body:** This is the new part. The request needs to contain two different pieces of data: the file itself and a text comment. The standard way to send mixed content like this is with a `Content-Type` of **`multipart/form-data`**. Think of it like sending a package with multiple items inside, each with its own label.
- **Response:** As always, we'll return the updated file object after the check-in is successful.

---

#### **🚩 Step 2: Backend - Implementing the Endpoint**

Handling `multipart/form-data` requires new tools from FastAPI: **`UploadFile`** and **`Form`**.

Update `backend/main.py`:

```python
# backend/main.py

# 1. Import new tools from FastAPI and shutil
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
import shutil
# ... other imports ...

# ... (all previous endpoints) ...

# --- NEW CHECK-IN ENDPOINT ---
@app.post("/api/files/{filename}/checkin", response_model=File)
async def checkin_file(filename: str, file: UploadFile = File(...), comment: str = Form(...)):
    """
    Checks in a new version of a file.
    """
    target_file = None
    for f in mock_db["files"]:
        if f["filename"] == filename:
            target_file = f
            break

    if not target_file:
        raise HTTPException(status_code=404, detail="File not found")
    if target_file["status"] != "locked":
        raise HTTPException(status_code=409, detail="File must be checked out to check in")

    # --- File Handling Logic ---
    # In a real app, this is where you'd save the file to your Git repo.
    # For now, we'll just save it to a temporary 'uploads' directory.
    upload_dir = "uploads"
    import os
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # --- Update Mock DB ---
    target_file["status"] = "unlocked"
    target_file["locked_by"] = None
    target_file["locked_at"] = None
    target_file["revision"] = (target_file.get("revision") or 0) + 1
    target_file["modified_at"] = datetime.now().isoformat()
    # In a real app, you'd store the comment in the Git commit message.

    return target_file

# ... (mount code) ...
```

🔎 **Deep Explanation**

- **`file: UploadFile = File(...)`** and **`comment: str = Form(...)`**: This is FastAPI's dependency injection at its best. By type-hinting the parameters with `UploadFile` and providing a default value of `Form(...)`, you tell FastAPI: "I expect a `multipart/form-data` request. Find the part named 'file' and treat it as a file upload. Find the part named 'comment' and treat it as form data." It handles all the complex parsing for you.
- **File Handling**: An `UploadFile` object is a file-like object. The standard way to save it is to read from it and write its contents to a new file on the server's disk. We're creating a temporary `uploads` folder for this.
- **State Update**: We update the file's metadata in our mock DB, incrementing the revision and setting the status back to "unlocked."

---

#### **🚩 Step 3: Frontend - Building the UI (Modal)**

A check-in requires more than a simple button; it needs a form. A **modal dialog** is the perfect UI for this.

First, add the HTML for the modal to `frontend/index.html`, right before the closing `</body>` tag. It will be hidden by default.

```html
<div id="checkin-modal" class="hidden fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center">
    <div class="bg-white p-8 rounded-lg shadow-xl w-1/3">
        <h2 class="text-2xl font-bold mb-4">Check-In File</h2>
        <form id="checkin-form">
            <div class="mb-4">
                <label for="checkin-comment" class="block text-gray-700 text-sm font-bold mb-2">Comment:</label>
                <textarea id="checkin-comment" name="comment" required class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" rows="3"></textarea>
            </div>
            <div class="mb-6">
                <label for="checkin-file" class="block text-gray-700 text-sm font-bold mb-2">File:</label>
                <input type="file" id="checkin-file" name="file" required class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
            </div>
            <div class="flex items-center justify-end space-x-2">
                <button id="cancel-modal-btn" type="button" class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">Cancel</button>
                <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Submit</button>
            </div>
        </form>
    </div>
</div>

<script src="/js/main.js" type="module"></script>
</body>
```

Next, add a "Check-In" button to our `FileCard.js` component.

```javascript
// frontend/js/components/FileCard.js
// ... (inside the template literal's button div) ...
${isLocked ? `
    <button class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded checkin-btn" data-filename="${file.filename}">
        Check-In
    </button>
    <button class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded cancel-btn" data-filename="${file.filename}">
        Cancel Checkout
    </button>
` : `
// ... (checkout button) ...
`}
```

---

#### **🚩 Step 4: Frontend - The API Service and `FormData`**

We need a service function that can send `multipart/form-data`. We'll use the browser's built-in **`FormData`** object for this.

Open `frontend/js/api/service.js` and add the new function.

```javascript
// frontend/js/api/service.js
// ... (other functions) ...

/**
 * Checks in a new file version using FormData.
 * @param {string} filename - The name of the file being checked in.
 * @param {FormData} formData - The FormData object containing the file and comment.
 * @returns {Promise<object>} A promise that resolves to the updated file object.
 */
export async function checkinFile(filename, formData) {
  const response = await fetch(`/api/files/${filename}/checkin`, {
    method: "POST",
    body: formData, // Pass FormData directly as the body
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to check in file");
  }
  return await response.json();
}
```

🔑 **Transferable Skill**: `FormData` is the standard JavaScript interface for building form data to send to a server. When you use `FormData` as the `body` of a `fetch` request, the browser automatically sets the correct `Content-Type: multipart/form-data` header, including the complex "boundary" delimiter. **Never set this header manually when using `FormData`\!**

---

#### **🚩 Step 5: Frontend - Wiring It All Together**

This is the most complex wiring yet. We need to handle opening the modal, closing it, and submitting the form.

Update `frontend/js/main.js`:

```javascript
// frontend/js/main.js

import {
  fetchFiles,
  checkoutFile,
  cancelCheckout,
  checkinFile,
} from "./api/service.js";
// ... (other code) ...

// Get references to modal elements
const checkinModal = document.getElementById("checkin-modal");
const checkinForm = document.getElementById("checkin-form");
const cancelModalBtn = document.getElementById("cancel-modal-btn");

// --- Event Listeners ---

// Main listener for file card buttons
fileListContainer.addEventListener("click", (event) => {
  if (event.target.matches(".checkin-btn")) {
    const filename = event.target.dataset.filename;
    // Store filename on the form and show the modal
    checkinForm.dataset.filename = filename;
    checkinModal.classList.remove("hidden");
  }
  // ... (other if blocks for checkout/cancel) ...
});

// Listener to close the modal
cancelModalBtn.addEventListener("click", () => {
  checkinModal.classList.add("hidden");
});

// Listener for the form submission
checkinForm.addEventListener("submit", async (event) => {
  event.preventDefault(); // Prevent default browser form submission

  const filename = event.target.dataset.filename;
  const commentInput = document.getElementById("checkin-comment");
  const fileInput = document.getElementById("checkin-file");

  // 1. Create a FormData object
  const formData = new FormData();
  formData.append("comment", commentInput.value);
  formData.append("file", fileInput.files[0]);

  try {
    // 2. Call the API service
    await checkinFile(filename, formData);

    // 3. Clean up and refresh
    checkinModal.classList.add("hidden");
    checkinForm.reset();
    await initializeApp();
  } catch (error) {
    console.error("Check-in failed:", error);
    alert(`Error: ${error.message}`);
  }
});

// ... (initializeApp) ...
```

🔎 **Deep Explanation**

1.  **Opening the Modal**: When a "Check-In" button is clicked, we grab the filename, store it on the form's `dataset` for later, and remove the `hidden` class to show the modal.
2.  **Submitting the Form**: We listen for the `submit` event. `event.preventDefault()` is essential to stop the browser from trying to navigate to a new page.
3.  **Building `FormData`**: We create a new `FormData` object and `append` our form fields to it. The key names (`'comment'`, `'file'`) must exactly match the parameter names in our FastAPI endpoint.

---

#### **✅ Recap**

This was a major leap in complexity and skill. You've now mastered one of the most common and critical tasks in full-stack development. You learned:

- How to handle **`multipart/form-data`** requests in a FastAPI backend.
- To use **`UploadFile`** and **`Form`** for robust data parsing.
- The standard practice of building a **modal dialog** for complex user input.
- How to use the JavaScript **`FormData`** object to prepare data for submission.
- The complete, end-to-end flow for features involving file uploads.

#### **📌 What's Next:**

We've focused on actions that change data. In **Part 8**, we'll return to reading data, but with more complexity. We will implement the **"View History"** feature, which involves fetching and displaying a _list_ of related data for a single resource.
