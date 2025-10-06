Let's get into it.

We've now built out the core user-facing features. This part introduces actions that are typically reserved for administrators or have irreversible consequences. This will teach us about the `DELETE` HTTP method and the fundamental concept of controlling UI and API access based on a user's role.

---

### **Part 9: Admin Features - "Override" & "Delete" (Masterclass Edition)**

**The Goal:** To implement two powerful features: "Override Lock," which allows an admin to forcibly unlock a file, and "Delete File," which permanently removes a file.

---

### **Feature Slice 5A: The "Override Lock"**

This feature is for situations where a user has a file locked but is unavailable to unlock it themselves. An administrator needs a way to step in.

#### **🚩 Step 1: Backend - The Override Endpoint**

The endpoint will be very similar to "Cancel Checkout," but its business purpose and who is allowed to call it are different.

- **HTTP Method**: `POST`, as it's a state-changing action.
- **URL**: `/api/files/{filename}/override`
- **Implementation**: Add the new endpoint to `backend/main.py`.

<!-- end list -->

```python
# backend/main.py
# ... (imports and previous endpoints) ...

# --- NEW OVERRIDE ENDPOINT ---
@app.post("/api/files/{filename}/override", response_model=File)
async def override_lock(filename: str):
    """
    Forcibly unlocks a file (admin action).
    """
    target_file = None
    for f in mock_db["files"]:
        if f["filename"] == filename:
            target_file = f
            break

    if not target_file:
        raise HTTPException(status_code=404, detail="File not found")
    if target_file["status"] != "locked":
        raise HTTPException(status_code=409, detail="File is not locked, no need to override.")

    # Forcibly unlock the file
    target_file["status"] = "unlocked"
    target_file["locked_by"] = None
    target_file["locked_at"] = None

    return target_file

# ... (rest of the file) ...
```

---

#### **🚩 Step 2: Frontend - Role-Based UI**

An "Override" button should only be visible to an admin. For now, we'll simulate this with a simple JavaScript variable.

First, open `frontend/js/main.js` and add this constant at the top.

```javascript
// frontend/js/main.js
const IS_ADMIN = true; // In a real app, this would come from user authentication.
// ... (imports) ...
```

Next, modify `FileCard.js` to accept this admin status and conditionally show the button.

```javascript
// frontend/js/components/FileCard.js

// 1. Accept 'isAdmin' as an argument
export function createFileCard(file, isAdmin) {
  const isLocked = file.status === "locked";

  return `
        <div class="bg-white p-4 rounded-lg shadow-md ...">
            ...
            <div class="border-t pt-2 flex justify-end flex-wrap gap-2">
                <button class="bg-gray-500 ... history-btn" ...>History</button>
                
                ${
                  isLocked
                    ? `
                    ${
                      isAdmin
                        ? `
                        <button class="bg-orange-500 hover:bg-orange-700 ... override-btn" data-filename="${file.filename}">
                            Override
                        </button>
                    `
                        : ""
                    }
                    <button class="bg-green-500 ... checkin-btn" ...>Check-In</button>
                    <button class="bg-yellow-500 ... cancel-btn" ...>Cancel Checkout</button>
                `
                    : `
                    <button class="bg-blue-500 ... checkout-btn" ...>Checkout</button>
                `
                }
                
                ${
                  isAdmin
                    ? `
                    <button class="bg-red-600 hover:bg-red-800 ... delete-btn" data-filename="${file.filename}">
                        Delete
                    </button>
                `
                    : ""
                }
            </div>
        </div>
    `;
}
```

Now, update `main.js` to pass the `IS_ADMIN` flag when rendering cards.

```javascript
// frontend/js/main.js
// ... (inside initializeApp function) ...
files.forEach((file) => {
  // Pass the flag here
  const cardHTML = createFileCard(file, IS_ADMIN);
  fileListContainer.insertAdjacentHTML("beforeend", cardHTML);
});
```

Finally, add the `overrideLock` service function to `service.js` and wire it up in `main.js` just like the others.

```javascript
// frontend/js/api/service.js
export async function overrideLock(filename) {
  const response = await fetch(`/api/files/${filename}/override`, {
    method: "POST",
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Failed to override lock");
  }
  return await response.json();
}

// frontend/js/main.js
// Inside the fileListContainer event listener
if (event.target.matches(".override-btn")) {
  const filename = event.target.dataset.filename;
  try {
    await overrideLock(filename);
    await initializeApp();
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
}
```

---

### **Feature Slice 5B: The "Delete File"**

This is our first **destructive** action. It introduces the `DELETE` HTTP method and the critical need for user confirmation.

#### **🚩 Step 3: Backend - The `DELETE` Endpoint**

- **HTTP Method**: **`DELETE`**. This is the specific, semantically correct verb for destroying a resource.
- **URL**: `/api/files/{filename}`. We are targeting the resource itself.
- **Response**: A successful deletion means the resource is gone. There's no data to return. The standard practice is to return a **`204 No Content`** status code.

Add the `DELETE` endpoint to `backend/main.py`.

```python
# backend/main.py
from fastapi import FastAPI, HTTPException, Response # 1. Import Response

# ... (previous endpoints) ...

# --- NEW DELETE ENDPOINT ---
@app.delete("/api/files/{filename}", status_code=204)
async def delete_file(filename: str):
    """
    Deletes a file (admin action).
    """
    file_to_delete = None
    for f in mock_db["files"]:
        if f["filename"] == filename:
            file_to_delete = f
            break

    if not file_to_delete:
        raise HTTPException(status_code=404, detail="File not found")

    mock_db["files"].remove(file_to_delete)

    # 2. Return a Response object to ensure no body is sent
    return Response(status_code=204)
```

🔎 **Deep Explanation**:

- `@app.delete(...)`: We use the decorator for the `DELETE` HTTP method.
- `status_code=204`: We tell FastAPI that a successful response from this endpoint should have a `204` status code by default.
- `return Response(status_code=204)`: Unlike other endpoints, we don't return data. We return a `Response` object with no body, which is the correct implementation for a `204` response.

---

#### **🚩 Step 4: Frontend - The Destructive Action Flow**

We already added the "Delete" button to the UI in `FileCard.js`. Now let's wire it up.

First, add the service function to `frontend/js/api/service.js`.

```javascript
// frontend/js/api/service.js
export async function deleteFile(filename) {
  const response = await fetch(`/api/files/${filename}`, {
    method: "DELETE",
  });

  // A 204 response has no body, so we don't try to parse JSON
  if (response.status !== 204) {
    const err = await response.json(); // If there's an error, there might be a body
    throw new Error(err.detail || "Failed to delete file");
  }

  // On success, return nothing.
  return;
}
```

Now, add the final block to the event listener in `frontend/js/main.js`.

```javascript
// frontend/js/main.js
// ... inside fileListContainer.addEventListener('click', ...) ...

if (event.target.matches(".delete-btn")) {
  const filename = event.target.dataset.filename;

  // 1. CRITICAL: Confirm with the user before a destructive action.
  if (confirm(`Are you sure you want to permanently delete ${filename}?`)) {
    try {
      await deleteFile(filename);
      await initializeApp(); // Refresh UI to show the file is gone
    } catch (error) {
      alert(`Error: ${error.message}`);
    }
  }
}
```

🔎 **Deep Explanation**: The most important piece of frontend code here is `if (confirm(...))`. The built-in browser `confirm()` dialog is a simple but effective way to prevent users from accidentally deleting data. **Never implement a destructive action without a confirmation step.** .

#### **✅ Recap**

You've now implemented some of the most powerful and sensitive types of API endpoints. You have learned:

- The correct use of the **`DELETE`** HTTP method for destroying resources.
- How to return a **`204 No Content`** response for successful deletions.
- The core concept of **role-based UI**, showing/hiding elements based on user permissions.
- The absolute necessity of adding **user confirmation** for any destructive action.

#### **📌 What's Next:**

Our application is now feature-complete... using fake, in-memory data. In **Part 10**, we will take a massive step toward making this a real application. We will focus entirely on the backend, replacing all our mock database logic with the **`GitPython`** library to interact with a real Git repository on the server.
