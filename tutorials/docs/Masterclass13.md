Let's get started on one of the most exciting features in modern web development.

Our application is now secure and multi-user, but it's not yet interactive _between_ users. If you check out a file, another user won't know unless they manually refresh their browser. We're going to fix that by introducing **WebSockets**, which will enable real-time, instantaneous updates for every connected user.

---

### **Part 13: Going Live - Real-Time Updates with WebSockets (Masterclass Edition)**

#### **🚩 Step 1: The "Why" - HTTP vs. WebSockets**

First, we need to understand why a new technology is needed for this.

- **HTTP is a "pull" protocol.** The client must always initiate the conversation. It's like sending a text message: you send a request ("What's the file status?") and you get a response ("It's unlocked."). The server can't text you out of the blue to say the status has changed. To get updates, the client would have to constantly text the server every few seconds ("polling"), which is incredibly inefficient.
- **WebSockets are a "push" protocol.** The client and server establish a persistent, two-way connection. It's like opening a phone line. Once the line is open, either side can speak at any time. The server can now "push" updates to all connected clients the instant an event happens.

For real-time features like live chats, notifications, and collaborative editing, WebSockets are the professional standard.

---

#### **🚩 Step 2: Backend - The Connection Manager**

The first step on the backend is to create a manager that keeps track of every user currently connected via a WebSocket.

Create a new file, `backend/websockets.py`:

```python
# backend/websockets.py
from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

# Create a single instance to be used across the application
manager = ConnectionManager()
```

🔎 **Deep Explanation**: This is a simple but powerful class. It maintains a list of `active_connections`. When a user connects, they are added to the list. When they disconnect, they are removed. The `broadcast` method is the key: it loops through every active connection and sends the same JSON message to all of them.

---

#### **🚩 Step 3: Backend - The WebSocket Endpoint**

Next, we need an endpoint for clients to connect to. This uses a special decorator in FastAPI.

Update `backend/main.py`:

```python
# backend/main.py
from fastapi import WebSocket, WebSocketDisconnect
from websockets import manager # 1. Import the manager

# ... (app = FastAPI()) ...
# ... (API endpoints) ...

# 2. Add the WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We are not expecting messages from client in this app, just broadcasting
            # A simple 'await websocket.receive_text()' would listen for messages
            # For now, we'll just keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

---

#### **🚩 Step 4: Backend - Broadcasting Events**

Now, we'll integrate the broadcast functionality into our existing service layer. After any action that changes a file's state, we'll notify all connected clients.

Update `backend/services/git_service.py`:

```python
# backend/services/git_service.py
from websockets import manager # 1. Import the manager

# ...

async def checkout_file(db, filename, user):
    # ... (existing checkout logic) ...
    updated_file = await _get_file_details(db, filename)

    # 2. Broadcast the update!
    await manager.broadcast({
        "event": "file_updated",
        "data": updated_file
    })

    return updated_file

# --- You will now do the SAME for every other state-changing function ---
# - cancel_checkout
# - checkin_file
# - override_lock
# - delete_file (here you can broadcast an event like "file_deleted", "data": {"filename": "..."})
```

---

#### **🚩 Step 5: Frontend - Connecting to the WebSocket**

The frontend now needs to open that "phone line" to the server. We'll create a new module for this.

Create `frontend/js/ws.js`:

```javascript
// frontend/js/ws.js
import { createFileCard } from "./components/FileCard.js";
import { IS_ADMIN } from "./main.js"; // We'll need to export this from main.js

function connectWebSocket() {
  const socket = new WebSocket(`ws://${window.location.host}/ws`);

  socket.onmessage = function (event) {
    const message = JSON.parse(event.data);
    console.log("WebSocket message received:", message);

    if (message.event === "file_updated") {
      const updatedFile = message.data;
      const cardId = `file-card-${updatedFile.filename.replace(/\./g, "-")}`;
      const existingCard = document.getElementById(cardId);

      if (existingCard) {
        // Generate the new HTML for the card
        const newCardHTML = createFileCard(updatedFile, IS_ADMIN);
        // Create a temporary element to hold the new HTML
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = newCardHTML.trim();
        const newCardElement = tempDiv.firstChild;

        // Replace the old card with the new one
        existingCard.replaceWith(newCardElement);
      }
    }
    // Add logic for 'file_deleted' event here if you implemented it
  };

  socket.onopen = function (event) {
    console.log("WebSocket connection established.");
  };

  socket.onclose = function (event) {
    console.log("WebSocket connection closed. Attempting to reconnect...");
    setTimeout(connectWebSocket, 3000); // Try to reconnect every 3 seconds
  };
}

export { connectWebSocket };
```

To make this work, you'll need to slightly modify `FileCard.js` to add a unique ID to each card's container div, and `main.js` to `export const IS_ADMIN` and call `connectWebSocket()`.

---

#### **🚩 Step 6: Testing the Real-Time Magic ✨**

This is the best part.

1.  Make sure your server is running.
2.  Open **two separate browser windows** (not two tabs in the same window, as that can sometimes share resources) and navigate both to `http://127.0.0.1:8000`.
3.  Arrange the windows side-by-side so you can see both.
4.  In **Window A**, click "Checkout" on a file.
5.  Watch **Window B**. The moment you click in Window A, the card in Window B should instantly update to show the "locked" status, and its "Checkout" button will disappear, replaced by "Check-In" and "Cancel."

You have just witnessed a real-time, server-pushed update\!

#### **✅ Recap**

You've now added a truly dynamic, multi-user layer to your application. This is a massive professional skill. You learned:

- The fundamental difference between **HTTP (pull)** and **WebSockets (push)**.
- How to implement a **Connection Manager** on the backend to track clients.
- To create a WebSocket endpoint in FastAPI and **broadcast** events.
- How to connect to a WebSocket from the frontend and listen for messages.
- The complete flow for receiving a pushed event and **updating the UI in real-time** without a page refresh.

#### **📌 What's Next:**

Our application is now architecturally complete and fully featured. The final two modules focus on making it robust and ready for the world. In **Part 14**, we'll dive into **Testing**, learning how to write automated tests to ensure our application is reliable and bug-free.
