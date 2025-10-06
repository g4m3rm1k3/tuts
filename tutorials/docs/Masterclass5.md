Excellent. Let's build our first piece of interactive functionality. We're about to complete our first full "vertical slice"—touching every layer of the stack, from the backend logic to the button a user clicks in their browser.

---

### **Part 5: Feature Slice 1 - The "Checkout" Workflow (Masterclass Edition)**

Our application is currently read-only. The "checkout" feature is our first "write" operation. Conceptually, checking out a file means a user is locking it to prevent others from editing it. We need to create a backend endpoint to handle this logic and a button on the frontend to trigger it.

---

#### **🚩 Step 1: Backend - Designing the API Endpoint**

First, we design the contract for our new API endpoint.

- **Action:** We are changing the state of a file (locking it). This is a "write" operation, not a "read" operation.
- **HTTP Method:** For actions that modify data, we typically use `POST`, `PUT`, or `DELETE`. `GET` is strictly for reading data. For an action like "checkout," **`POST` is the perfect choice**.
- **URL:** The action is performed on a _specific_ file. Therefore, the URL should identify that resource. A clean, RESTful URL pattern is `/api/files/{filename}/checkout`.
- **Response:** After a successful checkout, the frontend will need the updated file data to refresh the UI. So, our endpoint should return the modified file object.

---

#### **🚩 Step 2: Backend - Implementing the Endpoint**

Let's translate that design into code. Open `backend/main.py` and add the new endpoint.

```python
# backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from typing import List
from datetime import datetime  # Make sure datetime is imported
from models.file import File
from db import mock_db

app = FastAPI()

# --- API ROUTES ---
# (Existing GET routes are here...)
@app.get("/api/files", response_model=List[File])
async def list_files():
    # ... (code from before)

@app.get("/api/files/{filename}", response_model=File)
async def get_file(filename: str):
    # ... (code from before)

# --- NEW CHECKOUT ENDPOINT ---
@app.post("/api/files/{filename}/checkout", response_model=File)
async def checkout_file(filename: str):
    """
    Checks out (locks) a file for the current user.
    """
    target_file = None
    for f in mock_db["files"]:
        if f["filename"] == filename:
            target_file = f
            break

    if not target_file:
        raise HTTPException(status_code=404, detail="File not found")

    if target_file["status"] != "unlocked":
        raise HTTPException(
            status_code=409, detail=f"File is already locked by {target_file['locked_by']}"
        )

    # Update the file's status in our mock DB
    target_file["status"] = "locked"
    target_file["locked_by"] = "test_user"  # We'll hardcode the user for now
    target_file["locked_at"] = datetime.now().isoformat()

    return target_file


# --- MOUNT STATIC FILES ---
app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")

```

🔎 **Deep Explanation**

- **`@app.post(...)`**: We use the `post` decorator because this endpoint changes data on the server.
- **Business Logic:** We first check if the file exists. Then, crucially, we check if it's already locked. You can't check out a file that someone else has.
- **`HTTPException(status_code=409, ...)`**: This is a new, important status code. **`409 Conflict`** is the standard way to tell a client, "Your request is valid, but I can't complete it because it conflicts with the current state of the resource." This is much more informative than a generic "Bad Request" error.

🔑 **Transferable Skill:** Using specific HTTP methods (`POST` for actions) and specific status codes (`409 Conflict` for state conflicts) is a hallmark of a professional, well-designed API. It creates a predictable and robust contract for any client that uses it.

---

#### **🚩 Step 3: Frontend - Updating the UI Component**

Now, let's add a "Checkout" button to our file card, but _only_ if the file is available to be checked out.

Open `frontend/js/components/FileCard.js` and modify it.

```javascript
// frontend/js/components/FileCard.js

export function createFileCard(file) {
  const isLocked = file.status !== "unlocked";

  return `
        <div class="bg-white p-4 rounded-lg shadow-md flex flex-col justify-between">
            <div>
                <h2 class="text-xl font-bold mb-2">${file.filename}</h2>
                <p class="text-gray-600 mb-4">${
                  file.description || "No description available."
                }</p>
            </div>
            <div class="text-sm text-gray-500 mb-4">
                <p>Revision: ${file.revision}</p>
                <p>Status: <span class="font-semibold">${file.status}</span></p>
                ${isLocked ? `<p>Locked by: ${file.locked_by}</p>` : ""}
                <p>Modified: ${new Date(file.modified_at).toLocaleString()}</p>
            </div>
            <div class="border-t pt-2 flex justify-end">
                ${
                  !isLocked
                    ? `
                    <button 
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded checkout-btn"
                        data-filename="${file.filename}"
                    >
                        Checkout
                    </button>
                `
                    : ""
                }
            </div>
        </div>
    `;
}
```

🔎 **Deep Explanation**

- **Conditional Rendering:** We use a JavaScript ternary operator (`${!isLocked ? ... : ''}`) to conditionally render the button. The UI should only present actions that the user can actually take. This is a fundamental principle of good UX.
- **`data-filename` Attribute:** We embed the file's name directly into the button using a `data-*` attribute. This is a clean, standard way to associate data with a specific HTML element, making it easy to retrieve in our JavaScript event handler.

---

#### **🚩 Step 4: Frontend - Updating the API Service**

We need a function in our service to call the new backend endpoint.

Open `frontend/js/api/service.js` and add the new `checkoutFile` function.

```javascript
// frontend/js/api/service.js

// ... (fetchFiles function is here) ...

/**
 * Sends a request to check out a file.
 * @param {string} filename - The name of the file to check out.
 * @returns {Promise<object>} A promise that resolves to the updated file object.
 */
export async function checkoutFile(filename) {
  const response = await fetch(`/api/files/${filename}/checkout`, {
    method: "POST",
  });

  if (!response.ok) {
    // We'll get the error details from the server's response
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to check out file");
  }

  return await response.json();
}
```

🔎 **Deep Explanation**: The key difference here is the second argument to `fetch`. We pass an options object, `{ method: 'POST' }`, to specify the HTTP method. If you don't provide this, `fetch` defaults to `GET`. Our error handling is also more robust; we now try to parse the JSON body of an error response to get the detailed message from our FastAPI `HTTPException`.

---

#### **🚩 Step 5: Frontend - Wiring the Event Listener**

Finally, let's make the button do something when clicked.

Open `frontend/js/main.js` and add the event listener logic.

```javascript
// frontend/js/main.js

import { fetchFiles, checkoutFile } from "./api/service.js"; // Import checkoutFile
import { createFileCard } from "./components/FileCard.js";

const fileListContainer = document.getElementById("file-list-container");

// --- EVENT LISTENER USING EVENT DELEGATION ---
fileListContainer.addEventListener("click", async (event) => {
  // Check if a checkout button was clicked
  if (event.target.matches(".checkout-btn")) {
    const filename = event.target.dataset.filename;

    try {
      console.log(`Checking out ${filename}...`);
      await checkoutFile(filename);
      console.log(`${filename} checked out successfully.`);
      // Easiest way to see the change is to re-initialize the app
      await initializeApp();
    } catch (error) {
      console.error("Checkout failed:", error);
      alert(`Error: ${error.message}`); // Show error to the user
    }
  }
});

async function initializeApp() {
  // ... (rest of the function is the same) ...
}

initializeApp();
```

🔎 **Deep Explanation**: We are using **event delegation**. Instead of adding a click listener to every single button, we add one listener to their parent, `fileListContainer`. When a click occurs inside the container, the event "bubbles up." We then check `if (event.target.matches('.checkout-btn'))` to see if the element that was _actually_ clicked is one of our buttons. This is far more efficient and automatically works for buttons we add to the page dynamically. After a successful API call, we simply call `initializeApp()` again to refresh the entire list.

---

#### **🚩 Step 6: Testing the Full Feature**

1.  Make sure your `uvicorn` server is running.
2.  Refresh your browser at `http://127.0.0.1:8000`.
3.  You should now see "Checkout" buttons on the two unlocked files.
4.  Click the "Checkout" button on "project_alpha.emcam".
5.  The page will refresh. The card for "project_alpha.emcam" will now say its status is "locked," it will list "test_user" as the one who locked it, and the "Checkout" button will be gone. .
6.  Open your browser's dev tools to the Network tab to see the `POST` request being made.

#### **✅ Recap**

Congratulations\! You've just implemented your first full-stack, interactive feature. You learned how to:

- Design and implement a `POST` endpoint for actions that modify data.
- Use appropriate HTTP status codes like `409 Conflict` for business logic errors.
- Conditionally render UI elements based on application state.
- Use `data-*` attributes to associate data with elements.
- Handle events on dynamic content using **event delegation**.
- Trigger a UI refresh after a successful state change.

#### **📌 What's Next:**

Now, we will reinforce this entire pattern. In **Part 6**, we will implement the "Cancel Checkout" feature. It will follow the exact same vertical slice, solidifying the concepts you just learned.
