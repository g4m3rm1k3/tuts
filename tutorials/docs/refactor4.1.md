Excellent. In the previous stages, we built and secured the application's foundation. Now, we will implement the core PDM functionality—checking files in and out—and make the application truly collaborative by adding real-time updates with WebSockets.

This stage is where your application comes alive.

-----

## Stage 4: File Operations & Real-Time WebSocket Updates

**Goal:** To implement the full checkout/check-in workflow, including the frontend modals and backend logic. We will then integrate a WebSocket service to broadcast state changes, ensuring all connected users see updates instantly without needing to refresh.

**Time:** 4-5 hours

-----

### 4.1: The File Service (`file_service.py`)

First, we need a high-level service to orchestrate our core business logic. The `FileService` will use our lower-level `GitRepository` and `MetadataManager` services to perform complex actions like checking a file out, which involves creating a lock and committing it to Git.

**Action:** Create the file `backend/app/services/file_service.py`.

**File: `backend/app/services/file_service.py`**

```python
"""
File Service Module

This service acts as an orchestrator for file-related business logic. It combines
operations from lower-level services like GitRepository and MetadataManager to
execute complex workflows such as checking files in and out.
"""
import logging
import json
import re
from typing import Dict, List

from app.services.git_service import GitRepository
from app.services.metadata_service import MetadataManager
from app.schemas.file import FileInfo
from app.config import settings

logger = logging.getLogger(__name__)

class FileService:
  """
  Orchestrates file operations by coordinating the Git and Metadata services.
  """
  def __init__(self, git_repo: GitRepository, metadata_manager: MetadataManager):
    self.git_repo = git_repo
    self.metadata_manager = metadata_manager

  def get_files_with_status(self, current_user: str) -> Dict[str, List[FileInfo]]:
    """
    The core logic for listing all files. It performs an in-memory "JOIN"
    of data from three sources: the file list from Git, lock information,
    and metadata information.
    """
    if not self.git_repo or not self.metadata_manager:
      return {}

    # 1. Fetch raw data from all sources
    all_files_raw = []
    for ext in settings.ALLOWED_EXTENSIONS:
      all_files_raw.extend(self.git_repo.list_files(f"*{ext}"))
    
    # In later stages, we will add link file processing here

    grouped_files = {}
    for file_data in all_files_raw:
      path_for_meta = file_data['path']
      
      # 2. JOIN with metadata
      meta_path = self.git_repo.repo_path / f"{path_for_meta}.meta.json"
      description, revision = None, None
      if meta_path.exists():
        try:
          meta_content = json.loads(meta_path.read_text())
          description = meta_content.get('description')
          revision = meta_content.get('revision')
        except json.JSONDecodeError:
          logger.warning(f"Could not parse metadata for {path_for_meta}")
      
      # 3. JOIN with lock info
      lock_info = self.metadata_manager.get_lock_info(path_for_meta)
      status, locked_by, locked_at = "unlocked", None, None
      if lock_info:
        status = "locked"
        locked_by = lock_info.get('user')
        locked_at = lock_info.get('timestamp')
        if locked_by == current_user:
          status = "checked_out_by_user"
      
      # 4. Construct the final data object (schema)
      final_file_info = FileInfo(
        filename=file_data['name'],
        path=file_data['path'],
        status=status,
        locked_by=locked_by,
        locked_at=locked_at,
        size=file_data['size'],
        modified_at=file_data['modified_at'],
        description=description,
        revision=revision,
      )

      # 5. GROUP the results
      filename_str = final_file_info.filename.strip()
      group_name = "Miscellaneous"
      if re.match(r"^\d{7}.*", filename_str):
        group_name = f"{filename_str[:2]}XXXXX"
      
      if group_name not in grouped_files:
        grouped_files[group_name] = []
      grouped_files[group_name].append(final_file_info)

    return grouped_files
```

#### Deep Dive: The Orchestrator Service Pattern

 * The `FileService` is an **Orchestrator**. It doesn't perform low-level tasks itself; its job is to *coordinate* other, more specialized services.
 * **Workflow:** `get_files_with_status` executes a business workflow: "To get the file list, you must first get the raw files from Git, then get the lock status from the metadata manager, then merge them together, and finally group them."
 * **Analogy:** Think of a general contractor building a house. The contractor (Orchestrator Service) doesn't lay bricks or run wires. They hire and coordinate a bricklayer (`MetadataManager`) and an electrician (`GitRepository`) to do the specialized work.
 * **Benefits:** This pattern leads to highly maintainable code. The logic for getting the file list is in one place, but the details of how Git works or how locks are stored are neatly encapsulated in their own services.

-----

### 4.2: The WebSocket Service (`websocket_service.py`)

This service will manage our real-time connections. It will keep track of every user connected to the application via WebSockets.

**Action:** Create the file `backend/app/services/websocket_service.py`.

**File: `backend/app/services/websocket_service.py`**

```python
"""
WebSocket Service Module

This service manages all active WebSocket connections and provides a simple
interface for broadcasting messages to clients.
"""
import logging
import json
from typing import Dict, List
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class ConnectionManager:
  """
  Manages active WebSocket connections. This class is a singleton pattern,
  meaning there is only one instance of it for the entire application.
  """
  def __init__(self):
    # We store connections in a dictionary mapping username to the WebSocket object.
    self.active_connections: Dict[str, WebSocket] = {}

  async def connect(self, websocket: WebSocket, user: str):
    """Accepts and stores a new WebSocket connection."""
    await websocket.accept()
    self.active_connections[user] = websocket
    logger.info(f"WebSocket connected: {user} (Total: {len(self.active_connections)})")

  def disconnect(self, user: str):
    """Removes a WebSocket connection."""
    if user in self.active_connections:
      del self.active_connections[user]
      logger.info(f"WebSocket disconnected: {user} (Total: {len(self.active_connections)})")

  async def broadcast(self, message: dict):
    """
    Sends a JSON message to all connected clients.
    
    This is a core function for our real-time updates. It iterates through
    all active connections and sends the message. It also handles cleanup
    of any connections that have dropped unexpectedly.
    """
    disconnected_users = []
    # We create a list of items to iterate over, as the dictionary size
    # may change during the loop if a client disconnects.
    for user, connection in self.active_connections.items():
      try:
        await connection.send_text(json.dumps(message))
      except Exception:
        # If sending fails, the client has likely disconnected.
        disconnected_users.append(user)
    
    # Clean up any dead connections.
    for user in disconnected_users:
      self.disconnect(user)
```

-----

### 4.3: The WebSocket Router and Integration

Now we create the API endpoint for WebSocket connections and update our application's `lifespan` to manage our new services.

**Action:** Create the file `backend/app/api/v1/routers/websockets.py`.

**File: `backend/app/api/v1/routers/websockets.py`**

```python
"""
API Router for WebSocket Connections
"""
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.websocket_service import ConnectionManager
from app.state import app_state

logger = logging.getLogger(__name__)
router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user: str = "anonymous"):
  """
  The main WebSocket endpoint. It accepts a connection, associates it with
  a user, and then enters a loop to listen for incoming messages.
  """
  manager: ConnectionManager = app_state['connection_manager']
  await manager.connect(websocket, user)
  try:
    while True:
      # This loop keeps the connection alive.
      # We wait for messages from the client.
      data = await websocket.receive_text()
      logger.info(f"Received WebSocket message from {user}: {data}")
      # For now, we just log messages. In a later stage, we can add
      # client-to-server communication here.
      
  except WebSocketDisconnect:
    manager.disconnect(user)
  except Exception as e:
    logger.error(f"WebSocket error for {user}: {e}")
    manager.disconnect(user)
```

**Action:** Update the `lifespan.py` file to create and manage our new services.

**File: `backend/app/lifespan.py`**

```python
# ... (existing imports)
# Import all our new services
from app.services.git_service import GitRepository
from app.services.metadata_service import MetadataManager
from app.services.file_service import FileService
from app.services.websocket_service import ConnectionManager
from app.state import app_state
from app.config import settings

async def initialize_application():
  """Initializes all the core singleton services for the application."""
  logger.info("Initializing application state...")

  # Create and store the singleton ConnectionManager for WebSockets
  app_state['connection_manager'] = ConnectionManager()
  
  # The rest of the initialization remains the same for now
  if all([settings.GITLAB_URL, settings.GITLAB_TOKEN, settings.GITLAB_PROJECT_ID]):
    try:
      repo_path = settings.REPOS_BASE_DIR / settings.GITLAB_PROJECT_ID
      git_repo = GitRepository(repo_path, settings.GITLAB_URL, settings.GITLAB_TOKEN)
      app_state['git_repo'] = git_repo

      if git_repo.repo:
        metadata_manager = MetadataManager(git_repo.repo_path)
        app_state['metadata_manager'] = metadata_manager

        # Create the high-level FileService that uses the other services
        file_service = FileService(git_repo, metadata_manager)
        app_state['file_service'] = file_service
        
        app_state['initialized'] = True
        logger.info("Application fully initialized.")
      else:
        logger.error("Failed to initialize Git repository.")
    except Exception as e:
      logger.critical(f"Critical initialization error: {e}", exc_info=True)
  else:
    logger.warning("GitLab is not configured. App running in limited mode.")

# The rest of lifespan.py remains the same.
# @asynccontextmanager
# async def lifespan(app: FastAPI):
# ...
```

**Action:** Update `main.py` to include the WebSocket router.

**File: `backend/app/main.py`**

```python
# ...
from app.api.v1.routers import files, auth, websockets # Add websockets

# ...

app.include_router(files.router, prefix="/api/v1") # Correct the files prefix
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(websockets.router) # Add this line

# ...
```

-----

### 4.4: Frontend WebSocket Client (`websocket_service.js`)

Now for the client side. We'll create a dedicated service to manage the WebSocket connection, including automatic reconnection logic.

**Action:** Create `backend/static/js/modules/websocket_service.js`.

**File: `backend/static/js/modules/websocket_service.js`**

```javascript
/**
 * WebSocket Service Module
 *
 * Manages the real-time connection to the backend, handles incoming messages,
 * and implements a robust reconnection strategy with exponential backoff.
 */

class WebSocketClient {
  constructor() {
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 10;
    this.reconnectTimeout = null;
    this.messageHandlers = new Map(); // Stores handlers for different message types
  }

  connect(currentUser) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.log("WebSocket is already connected.");
      return;
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws?user=${encodeURIComponent(currentUser)}`;
    
    console.log(`Connecting to WebSocket at ${wsUrl}`);
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log("WebSocket connection established.");
      this.reconnectAttempts = 0; // Reset on successful connection
      document.getElementById('connection-status').textContent = 'Connected';
      document.getElementById('connection-status').className = 'status connected';
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        console.log("Received WebSocket message:", message);
        
        // Route the message to the correct handler based on its type
        if (this.messageHandlers.has(message.type)) {
          this.messageHandlers.get(message.type)(message.payload);
        }

      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };

    this.ws.onclose = () => {
      console.log("WebSocket connection closed.");
      document.getElementById('connection-status').textContent = 'Disconnected';
      document.getElementById('connection-status').className = 'status disconnected';
      this.scheduleReconnect(currentUser);
    };

    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  }

  /**
   * Schedules a reconnection attempt with exponential backoff and jitter.
   * This prevents overwhelming the server with reconnect attempts.
   */
  scheduleReconnect(currentUser) {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error("Max WebSocket reconnect attempts reached. Please refresh the page.");
      return;
    }
    
    // Exponential backoff: 1s, 2s, 4s, 8s, ... up to 30s
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
    // Jitter: Add randomness to prevent a "thundering herd" of clients reconnecting at once
    const jitter = delay * 0.2 * Math.random();
    
    this.reconnectAttempts++;
    console.log(`Attempting to reconnect in ${(delay + jitter) / 1000} seconds...`);
    
    clearTimeout(this.reconnectTimeout);
    this.reconnectTimeout = setTimeout(() => this.connect(currentUser), delay + jitter);
  }
  
  /**
   * Registers a callback function for a specific message type.
   * @param {string} type - The 'type' of the WebSocket message.
   * @param {Function} handler - The function to call with the message payload.
   */
  on(type, handler) {
    this.messageHandlers.set(type, handler);
  }
}

// Export a singleton instance of the client
export const wsClient = new WebSocketClient();
```

-----

### 4.5: Final Frontend Integration

Let's tie it all together in our main `app.js`. We'll connect to the WebSocket on startup and set up a handler to automatically re-render the UI when we receive a `FILE_LIST_UPDATED` message from the server.

**Action:** Update `backend/static/js/app.js`.

**File: `backend/static/js/app.js`**

```javascript
/**
 * Main Application Orchestrator
 */

// Import all our services
import { ThemeManager } from './modules/theme-manager.js';
import { api } from './modules/api_service.js';
import { ui } from './modules/ui_service.js';
import { wsClient } from './modules/websocket_service.js'; // New import

// ... (Global State and DOM Caching) ...

/**
 * Main data loading and rendering function.
 * Now, this function is primarily called on initial load and when a WebSocket
 * update is received, rather than after every single user action.
 */
async function loadFiles() {
  // ... (same as before) ...
}

// --- Event Handling ---
// We will implement the details of these handlers in the next stage.
function handleCheckout(filename) {
  alert(`Checkout for ${filename} will be implemented soon.`);
}

// ... (other handlers) ...


// --- Application Initialization ---

function initialize() {
  console.log("Application Initialized");
  
  // --- NEW: WebSocket Initialization ---
  const token = localStorage.getItem('auth_token');
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentUser = payload.sub;

      // Connect to the WebSocket server
      wsClient.connect(currentUser);

      // Set up the handler for real-time file list updates
      wsClient.on('FILE_LIST_UPDATED', (payload) => {
        console.log("Received real-time file list update.");
        // When an update is pushed from the server, just re-render the UI.
        ui.renderFileList(domCache.fileList, payload);
        // Re-attach listeners as the DOM has been replaced.
        attachFileActionListeners();
      });
      
    } catch (e) {
      console.error("Could not decode token to start WebSocket:", e);
    }
  }
  
  // ... (existing initialization logic) ...
}

document.addEventListener("DOMContentLoaded", initialize);
```

-----

## Stage 4 Complete ✓

This was a major stage. We've introduced the concept of services on both the backend and frontend and laid the entire foundation for real-time communication.

#### Verification Checklist

1. **Run the Server.**
2. **Open Two Browser Windows:** Navigate to `http://localhost:8000` in two separate browser windows or tabs and log in.
3. **Check WebSocket Connection:** In the developer console of both windows, you should see "WebSocket connection established." In the backend terminal, you should see log messages for two WebSocket connections.
4. **Trigger an Update (Simulated):** We haven't implemented the real checkout yet, so we'll simulate it.
   * Create a temporary test endpoint in `backend/app/api/v1/routers/files.py`:
    ```python
    @router.post("/test-broadcast")
    async def test_broadcast():
      from app.state import app_state
      manager = app_state['connection_manager']
      file_service = app_state['file_service']
      grouped_data = file_service.get_files_with_status("test_user")
      await manager.broadcast({
        "type": "FILE_LIST_UPDATED",
        "payload": grouped_data
      })
      return {"status": "broadcast sent"}
    ```
   * Go to your API docs (`/docs`), find `/api/v1/test-broadcast`, and execute it.
   * **Observe:** Both of your browser windows should instantly re-render the file list, and you should see "Received real-time file list update" in their consoles. This confirms the entire real-time pipeline is working\!
   * **Remember to delete the `/test-broadcast` endpoint when you're done.**

#### What You Learned

 * **Service Orchestration:** How to use a high-level service (`FileService`) to coordinate multiple low-level services.
 * **WebSocket Protocol:** The fundamentals of how WebSockets establish a persistent, bidirectional connection.
 * **Connection Management:** The **Singleton Pattern** for managing a shared resource like a connection pool across your entire application.
 * **Event-Driven Architecture:** How an HTTP request can trigger an event that is broadcast to all clients, decoupling actions from notifications.
 * **Robust Client-Side Connections:** How to build a WebSocket client that automatically reconnects using **exponential backoff with jitter**, a professional pattern for network resilience.

**Next Up: Stage 5 - Implementing Full CRUD and Real-Time Actions.** We will now replace all the placeholder `alert()` calls. We will build out the backend logic for `checkout`, `checkin`, and `cancel`, and make them broadcast `FILE_LIST_UPDATED` events on success. We will also build the frontend modals and forms to trigger these actions. By the end, your application will be fully interactive and collaborative.