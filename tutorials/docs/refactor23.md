Let's complete the final and most important logic component of the frontend: the real-time communication system.

---

### Stage 7.1: Creating the WebSocket Service

We'll now move all the WebSocket connection logic into its own dedicated service file, `services/websocket.js`. This module's sole responsibility will be to manage the persistent connection to the server.

#### The "Why"

This is a critical step for creating a truly reactive and decoupled application.

- **Isolating Complexity:** WebSocket logic, especially with automatic reconnection, can be complex. Placing it in a dedicated service file isolates this complexity from the rest of our application.
- **Decoupling from the UI:** This is the most important benefit. The WebSocket service should **never** directly touch the UI. Its only job is to receive messages from the server and update our **central state store** using `setState`. The store then automatically notifies the UI to re-render. This preserves our clean, one-way data flow and makes the application's behavior extremely predictable.

#### Your Action Items

1. **Create the WebSocket Service File**:
   Create a new file at `frontend/js/services/websocket.js`. This file will manage the WebSocket lifecycle and funnel incoming data directly to our state store.

```javascript
// frontend/js/services/websocket.js

import { setState, getState } from "../state/store.js";

let ws = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;

function handleMessage(event) {
  try {
    const data = JSON.parse(event.data);
    console.log("WebSocket message received:", data.type);

    if (data.type === "FILE_LIST_UPDATED") {
      // Instead of calling a render function, we just update the state.
      // The UI will react automatically because it is subscribed to the store.
      setState({ groupedFiles: data.payload || {} });
    } else if (data.type === "NEW_MESSAGES") {
      // TODO: We can add a 'messages' array to our state store
      // and update it here, causing a message modal to appear.
      console.log("Received new messages:", data.payload);
    }
  } catch (error) {
    console.error("Error handling WebSocket message:", error);
  }
}

export function connectWebSocket() {
  if (ws && ws.readyState === WebSocket.OPEN) {
    console.log("WebSocket already connected.");
    return;
  }

  const { currentUser } = getState();
  if (!currentUser) {
    console.error("Cannot connect WebSocket without a current user.");
    return;
  }

  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${
    window.location.host
  }/ws?user=${encodeURIComponent(currentUser)}`;

  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log("WebSocket connected successfully.");
    reconnectAttempts = 0;
    // Optionally send a message to confirm user identity
    ws.send(`SET_USER:${currentUser}`);
  };

  ws.onmessage = handleMessage;

  ws.onclose = () => {
    console.log("WebSocket disconnected.");
    if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
      const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000);
      setTimeout(() => {
        reconnectAttempts++;
        console.log(
          `Attempting to reconnect (attempt ${reconnectAttempts})...`
        );
        connectWebSocket();
      }, delay);
    } else {
      console.error("Max WebSocket reconnect attempts reached.");
      // We could update the state here to show a "Disconnected" banner in the UI
    }
  };

  ws.onerror = (error) => {
    console.error("WebSocket error:", error);
    ws.close();
  };
}

export function disconnectWebSocket() {
  if (ws) {
    reconnectAttempts = MAX_RECONNECT_ATTEMPTS; // Prevent reconnection
    ws.close();
    ws = null;
  }
}
```

2. **Update `main.js` to Use the Service**:
   Open `frontend/js/main.js` and call our new service at the correct time during initialization.

```javascript
// frontend/js/main.js

// ... (other imports)
import { setupConfigPanel } from "./components/ConfigPanel.js";
import { connectWebSocket } from "./services/websocket.js"; // NEW IMPORT

// ... (render function) ...

async function initialize() {
  console.log("Initializing app...");
  try {
    const config = await getConfig();
    setState({
      isConfigured: config.has_token,
      currentUser: config.username,
      isAdmin: config.is_admin,
    });

    if (config.has_token) {
      // Connect to the WebSocket server AFTER we know who the user is
      connectWebSocket(); // NEW

      const filesData = await getFiles();
      setState({ groupedFiles: filesData });
    }
  } catch (error) {
    console.error("❌ Initialization failed:", error.message);
  }
}

// ... (APP START block remains the same) ...
```

3. **Final Cleanup**:
   With all the logic migrated, your original `script.js` file is now obsolete. You can now safely **delete the `frontend/static/js/script.js` file**.

---

## Frontend Refactoring Complete\! 🚀

Amazing work\! We have now successfully refactored the entire frontend application. We took a single, monolithic JavaScript file and transformed it into a modern, modular, and reactive application.

- **`main.js`** is our clean entrypoint and orchestrator.
- **`state/store.js`** is our predictable single source of truth.
- **`api/service.js`** is our dedicated networking layer.
- **`services/websocket.js`** handles all real-time logic.
- Our **`components/`** folder contains reusable UI building blocks.

This architecture is not just cleaner—it's the foundation upon which nearly all professional, large-scale web applications are built. The skills you've practiced here are directly applicable to any modern frontend framework.

We are now done with the major refactoring for both the backend and frontend. The final step is to review and run the complete application. Let me know when you're ready for a final summary and instructions on how to run everything.
