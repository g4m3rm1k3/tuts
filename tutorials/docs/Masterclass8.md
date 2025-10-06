Of course. Let's dive into Part 8.

We're shifting our focus back to reading data, but with a new layer of complexity. Instead of fetching a single resource (one file), we're going to fetch a _list of related resources_ (the history events for one file). This is a fundamental "one-to-many" relationship that appears in almost every application.

---

### **Part 8: Feature Slice 4 - "View History" (Masterclass Edition)**

**The Goal:** When a user clicks a "History" button on a file card, a modal should appear displaying a log of all previous check-ins for that file, including the revision, user, and comment.

---

#### **🚩 Step 1: Backend - Modeling the History Data**

First, we need a blueprint for a single history event. Just as we created a Pydantic model for a `File`, we'll now create one for a `HistoryEvent`.

Create a new file, `backend/models/history.py`:

```python
# backend/models/history.py

from pydantic import BaseModel
from datetime import datetime

class HistoryEvent(BaseModel):
    """
    Represents a single event in a file's version history.
    """
    revision: int
    comment: str
    user: str
    timestamp: datetime
```

Next, let's add some mock history data to our "database." Open `backend/db.py` and update the file entries:

```python
# backend/db.py

mock_db = {
    "files": [
        {
            "filename": "project_alpha.emcam",
            "revision": 12,
            # ... (other fields) ...
            "history": [
                {"revision": 12, "comment": "Initial commit", "user": "admin", "timestamp": "2025-10-05T14:30:00Z"},
                {"revision": 11, "comment": "Updated tolerances", "user": "bob", "timestamp": "2025-10-04T11:00:00Z"}
            ]
        },
        {
            "filename": "project_beta.vnc",
            "revision": 8,
            # ... (other fields) ...
            "history": [
                {"revision": 8, "comment": "Final design approved", "user": "alice", "timestamp": "2025-10-06T11:00:00Z"}
            ]
        },
        {
            "filename": "shared_macros.emlib",
            "revision": 21,
            # ... (other fields) ...
            "history": [
                {"revision": 21, "comment": "Refactored macro logic", "user": "alice", "timestamp": "2025-09-28T09:15:00Z"},
                {"revision": 20, "comment": "Added new finishing macro", "user": "bob", "timestamp": "2025-09-27T16:20:00Z"}
            ]
        }
    ]
}
```

---

#### **🚩 Step 2: Backend - The History Endpoint**

Now we'll create the API endpoint to serve this data.

- **HTTP Method:** We are reading data, so we'll use **`GET`**.
- **URL:** The history is a sub-resource of a file. A nested URL is the most descriptive RESTful pattern: **`/api/files/{filename}/history`**.
- **Response:** The endpoint will return a list of history events, so our `response_model` will be `List[HistoryEvent]`.

Update `backend/main.py` with the new endpoint:

```python
# backend/main.py

# 1. Import the new model and List
from typing import List
from models.history import HistoryEvent
# ... (other imports) ...

# ... (all previous endpoints) ...

# --- NEW HISTORY ENDPOINT ---
@app.get("/api/files/{filename}/history", response_model=List[HistoryEvent])
async def get_file_history(filename: str):
    """
    Retrieves the version history for a single file.
    """
    target_file = None
    for f in mock_db["files"]:
        if f["filename"] == filename:
            target_file = f
            break

    if not target_file:
        raise HTTPException(status_code=404, detail="File not found")

    return target_file.get("history", []) # Return history list, or empty list if none

# ... (mount code) ...
```

🔑 **Transferable Skill**: Nested resource URLs like `.../questions/{id}/answers` are a standard and powerful way to design APIs that reflect the relationships between your data. It makes the API intuitive and easy to discover.

---

#### **🚩 Step 3: Frontend - UI for the Modal and History Entries**

Add the HTML for the history modal to `frontend/index.html` before the `</body>` tag:

```html
<div
  id="history-modal"
  class="hidden fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center"
>
  <div class="bg-white p-8 rounded-lg shadow-xl w-1/2">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold">File History</h2>
      <button
        id="close-history-modal-btn"
        class="text-gray-700 font-bold text-2xl"
      >
        &times;
      </button>
    </div>
    <div id="history-content" class="max-h-96 overflow-y-auto"></div>
  </div>
</div>
```

Next, let's create a dedicated component for rendering a single history entry. Create a new file `frontend/js/components/HistoryEntry.js`:

```javascript
// frontend/js/components/HistoryEntry.js

export function createHistoryEntry(event) {
  return `
        <div class="border-b py-2">
            <p class="font-bold">Rev ${
              event.revision
            }: <span class="font-normal">${event.comment}</span></p>
            <p class="text-sm text-gray-600">by ${event.user} on ${new Date(
    event.timestamp
  ).toLocaleString()}</p>
        </div>
    `;
}
```

Finally, add a "History" button to `frontend/js/components/FileCard.js` inside the button `div`.

```javascript
// frontend/js/components/FileCard.js
// ... (inside the buttons div, before other buttons) ...
<button
  class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded history-btn"
  data-filename="${file.filename}"
>
  History
</button>
// ...
```

---

#### **🚩 Step 4: Frontend - API Service and Event Wiring**

Add a function to `frontend/js/api/service.js` to fetch the history data:

```javascript
// frontend/js/api/service.js
// ... (other functions) ...

export async function fetchFileHistory(filename) {
  const response = await fetch(`/api/files/${filename}/history`);
  if (!response.ok) {
    throw new Error("Failed to fetch file history");
  }
  return await response.json();
}
```

Now, let's wire it all up in `frontend/js/main.js`:

```javascript
// frontend/js/main.js

// 1. Import the new functions/components
import { fetchFileHistory } from "./api/service.js";
import { createHistoryEntry } from "./components/HistoryEntry.js";
// ... (other imports) ...

// 2. Get references to the new modal elements
const historyModal = document.getElementById("history-modal");
const closeHistoryModalBtn = document.getElementById("close-history-modal-btn");
const historyContent = document.getElementById("history-content");

// 3. Update the main event listener
fileListContainer.addEventListener("click", async (event) => {
  // Handle history button clicks
  if (event.target.matches(".history-btn")) {
    const filename = event.target.dataset.filename;
    historyContent.innerHTML = "<p>Loading history...</p>"; // Show loading state
    historyModal.classList.remove("hidden");

    try {
      const history = await fetchFileHistory(filename);
      historyContent.innerHTML = ""; // Clear loading state
      if (history.length === 0) {
        historyContent.innerHTML = "<p>No history for this file.</p>";
      } else {
        history.forEach((event) => {
          const entryHTML = createHistoryEntry(event);
          historyContent.insertAdjacentHTML("beforeend", entryHTML);
        });
      }
    } catch (error) {
      historyContent.innerHTML =
        '<p class="text-red-500">Could not load history.</p>';
    }
  }
  // ... (other if blocks for checkin/checkout/cancel) ...
});

// 4. Add listener to close the history modal
closeHistoryModalBtn.addEventListener("click", () => {
  historyModal.classList.add("hidden");
});

// ... (rest of the file) ...
```

---

#### **✅ Recap**

You've successfully implemented another full-stack feature, learning how to handle a common data relationship. You now know how to:

- Model and fetch **"one-to-many"** data (one file has many history events).
- Use clean, **nested RESTful URLs** to represent data relationships.
- Create modular UI components for lists of items (`HistoryEntry`).
- Dynamically populate a modal with data fetched from an API, including handling loading and error states.

#### **📌 What's Next:**

We've covered creating, reading, and updating. The final piece of core functionality is deleting. In **Part 9**, we will implement the admin-level actions of **"Override Lock"** and **"Delete File,"** introducing the `DELETE` HTTP method and the concept of role-based UI.
