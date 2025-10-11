# Deep Dive: Your `websocket.py` - Real-Time Communication

## Overview: What This File Should Do

**Purpose:** WebSockets enable **real-time, bidirectional communication** between your frontend and backend.

**Your use case:** When User A checks out a file, User B's screen should update immediately to show the file is locked - WITHOUT User B refreshing the page.

**Current state:** Your code has the authentication working, but it's **not actually broadcasting updates** yet. Let's understand why and fix it.

---

## Part 1: Understanding WebSockets

### HTTP vs WebSocket

**Traditional HTTP (what we've been using):**

```
Frontend: "Give me the file list"  →  Backend
Frontend:                          ←  Backend: "Here's the list"
[Connection closes]

Frontend: "Give me the file list"  →  Backend (5 seconds later)
Frontend:                          ←  Backend: "Here's the list"
[Connection closes]
```

**Polling:** Frontend asks "anything new?" every few seconds. Wasteful!

---

**WebSocket (persistent connection):**

```
Frontend: "Connect to WebSocket"   →  Backend
Frontend:                          ←  Backend: "Connected!"
[Connection stays open]

Backend:  "File locked by john"    →  Frontend (instant notification!)
Backend:  "New file checked in"    →  Frontend (instant notification!)
```

**Key difference:** Connection stays open. Server can PUSH updates to client.

📚 **Learn more:**

- [MDN WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)

---

### Why You Need a Connection Manager

**The problem:** When User A checks out a file, how do you notify User B?

**You need:**

1. A list of all connected users
2. A way to send a message to all of them (broadcast)
3. A way to send to specific users (targeted messages)

**Your current `ConnectionManager` doesn't do any of this!**

---

## Part 2: Walking Through Your Current Code

### The Imports

```python
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status
from app.core.security import UserAuth
import logging
```

**`WebSocket`** - The WebSocket connection object (like `Request` for HTTP)

**`WebSocketDisconnect`** - Exception raised when client disconnects

- User closes browser tab
- Network failure
- Client explicitly calls `websocket.close()`

**`status`** - WebSocket close codes (like HTTP status codes)

- `1000` = Normal closure
- `1008` = Policy violation (auth failed)
- `1011` = Internal error

📚 **Learn more:** [WebSocket Close Codes](https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code)

---

### Your Connection Manager (Current)

```python
class ConnectionManager:
    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    def disconnect(self, websocket: WebSocket):
        pass
```

**What it does:**

- `connect()` - Accepts the connection (required to establish WebSocket)
- `disconnect()` - Does nothing! Just `pass`

**What it DOESN'T do:**

- ❌ Track connected clients
- ❌ Broadcast to all clients
- ❌ Target specific users
- ❌ Handle errors

**This is a placeholder!** It works for auth testing but not for actual features.

---

### The Authentication Dependency

```python
async def get_current_user_from_ws(websocket: WebSocket) -> dict | None:
    """Dependency to get user from cookie for WebSockets."""
    token = websocket.cookies.get("auth_token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    auth_service: UserAuth = websocket.app.state.user_auth
    if not auth_service:
        logger.error("UserAuth service not initialized.")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        return None

    payload = auth_service.verify_token(token)
    if not payload:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None
    return payload
```

**This is REALLY GOOD!** Let me explain why:

---

**Line 1: `websocket.cookies.get("auth_token")`**

Just like HTTP requests, WebSocket connections send cookies in the initial handshake. You're reading your JWT cookie.

**Why this works:** When the frontend does:

```javascript
const ws = new WebSocket("ws://localhost:8000/ws");
```

The browser automatically includes cookies (including your `auth_token`).

---

**Line 2-4: Token validation**

```python
if not token:
    await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return None
```

**`WS_1008_POLICY_VIOLATION`** - Tells the client "you're not authenticated."

**Why close immediately?** No point keeping an unauthenticated connection open. Security best practice.

---

**Line 6-9: Service availability check**

```python
auth_service: UserAuth = websocket.app.state.user_auth
if not auth_service:
    logger.error("UserAuth service not initialized.")
    await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
    return None
```

**`websocket.app.state.user_auth`** - Accessing the service from app state (same pattern as `main.py`)

**Why check if it exists?** Remember, if GitLab isn't configured, services are `None`. This prevents crashes.

---

**Line 11-14: Token verification**

```python
payload = auth_service.verify_token(token)
if not payload:
    await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return None
return payload
```

Uses your `UserAuth` service to decode and validate the JWT. Same logic as your HTTP auth.

**✅ This dependency is well-written!** It handles all error cases and uses proper WebSocket close codes.

---

### The WebSocket Endpoint

```python
@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user: dict = Depends(get_current_user_from_ws)
):
    if not user:
        return

    username = user.get("sub", "unknown")
    await manager.connect(websocket)
    logger.info(f"WebSocket connected for user: {username}")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"WebSocket disconnected for user: {username}")
```

**Let's trace the flow:**

**1. User connects:**

```python
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user: dict = Depends(...)):
```

- Frontend opens connection to `ws://localhost:8000/ws`
- FastAPI calls `get_current_user_from_ws()` dependency
- If auth succeeds, `user` contains the JWT payload
- If auth fails, dependency closes connection and returns `None`

---

**2. Accept the connection:**

```python
await manager.connect(websocket)
```

Calls your manager's `connect()` which does `await websocket.accept()`.

**What's `accept()`?** WebSocket handshake completion. Connection goes from "pending" to "open."

---

**3. The message loop:**

```python
try:
    while True:
        await websocket.receive_text()
```

**This is where your code does nothing useful!**

**What it currently does:**

- Waits for client to send a message
- Receives it
- Does NOTHING with it
- Waits for next message

**What it SHOULD do:**

- Send file updates to client
- Broadcast changes from other users
- Handle client requests

---

**4. Disconnect handling:**

```python
except WebSocketDisconnect:
    manager.disconnect(websocket)
    logger.info(f"WebSocket disconnected for user: {username}")
```

When client disconnects (closes tab, network fails, etc.), this exception is raised.

Your manager's `disconnect()` does nothing, so the connection just... disappears.

---

## Part 3: What's Missing for Real-Time Updates

### Missing Feature 1: Connection Tracking

**You need to track WHO is connected:**

```python
active_connections: Dict[str, WebSocket] = {}
# Key: username, Value: their websocket
```

**Why?** So you can send updates to specific users or broadcast to all.

---

### Missing Feature 2: Broadcasting

**When User A checks out a file, you need to:**

```python
# In your files.py router, after checkout:
await manager.broadcast({
    "type": "file_locked",
    "filename": "part_123.mcam",
    "locked_by": "john_doe"
})
```

**Then ALL connected users' screens update instantly.**

---

### Missing Feature 3: Message Types

**Your frontend needs different types of messages:**

- `file_locked` - Someone checked out a file
- `file_unlocked` - Someone checked in a file
- `file_deleted` - Admin deleted a file
- `user_connected` - Someone joined
- `ping` - Keep-alive to prevent timeout

**Your current code has no message structure!**

---

## Part 4: Your Improved, Professional `websocket.py`

Here's a complete, production-ready version with full comments:

```python
"""
WebSocket router for real-time updates.

This module provides:
1. Persistent connections for real-time communication
2. Broadcasting file changes to all connected users
3. Targeted messages to specific users
4. Connection management and cleanup

Architecture:
- ConnectionManager tracks all active WebSocket connections
- Each connection is authenticated via JWT cookie
- When files change, other routers call manager.broadcast()
- All connected clients receive instant updates
"""

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status
from typing import Dict, List
from app.core.security import UserAuth
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()


class ConnectionManager:
    """
    Manages WebSocket connections for real-time updates.

    Responsibilities:
    - Track all active connections
    - Broadcast messages to all users
    - Send messages to specific users
    - Clean up disconnected clients

    Thread safety: Not currently thread-safe. If using workers > 1,
    you'd need Redis or similar for cross-process communication.
    """

    def __init__(self):
        # Store active connections: {username: websocket}
        # Using dict (not list) so we can identify users by name
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, username: str, websocket: WebSocket):
        """
        Accept a new WebSocket connection and track it.

        Args:
            username: The authenticated user's username
            websocket: The WebSocket connection object

        Note: If user already connected, this replaces their old connection.
        This handles cases where user refreshes page without proper disconnect.
        """
        # Accept the WebSocket handshake
        await websocket.accept()

        # If user already connected (e.g., opened app in two tabs), close old connection
        if username in self.active_connections:
            old_ws = self.active_connections[username]
            try:
                await old_ws.close(code=status.WS_1000_NORMAL_CLOSURE)
            except Exception:
                pass  # Old connection might already be dead

        # Track the new connection
        self.active_connections[username] = websocket
        logger.info(f"WebSocket connected: {username} (total: {len(self.active_connections)})")

        # Notify all users that someone connected
        await self.broadcast({
            "type": "user_connected",
            "username": username,
            "timestamp": datetime.utcnow().isoformat()
        })

    def disconnect(self, username: str):
        """
        Remove a user's connection from tracking.

        Args:
            username: The user who disconnected

        Note: This doesn't close the connection (that's already happened),
        it just removes it from our tracking dict.
        """
        if username in self.active_connections:
            del self.active_connections[username]
            logger.info(f"WebSocket disconnected: {username} (remaining: {len(self.active_connections)})")

    async def send_personal_message(self, username: str, message: dict):
        """
        Send a message to a specific user.

        Args:
            username: Target user
            message: Dict that will be JSON-serialized

        Use cases:
        - Admin sends a message to one user
        - Notify user their checkout succeeded
        - User-specific notifications
        """
        if username in self.active_connections:
            websocket = self.active_connections[username]
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send to {username}: {e}")
                # Connection might be dead, remove it
                self.disconnect(username)

    async def broadcast(self, message: dict, exclude: List[str] = None):
        """
        Send a message to all connected users.

        Args:
            message: Dict that will be JSON-serialized
            exclude: List of usernames to NOT send to (optional)

        Use cases:
        - File was checked out -> notify everyone
        - File was checked in -> notify everyone
        - New file added -> notify everyone

        Note: If sending fails to a user, we remove their connection.
        This handles "zombie" connections that appear alive but aren't.
        """
        exclude = exclude or []

        # Build list of users to notify
        recipients = [
            username for username in self.active_connections.keys()
            if username not in exclude
        ]

        # Send to each recipient
        # We iterate over a copy of the keys because we might remove dead connections
        dead_connections = []
        for username in recipients:
            websocket = self.active_connections[username]
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Failed to broadcast to {username}: {e}")
                dead_connections.append(username)

        # Clean up dead connections
        for username in dead_connections:
            self.disconnect(username)

        logger.debug(f"Broadcast to {len(recipients)} users: {message.get('type', 'unknown')}")

    def get_connected_users(self) -> List[str]:
        """
        Get list of currently connected usernames.

        Returns:
            List of usernames

        Useful for:
        - Dashboard showing who's online
        - Admin features
        - Debugging
        """
        return list(self.active_connections.keys())


# Create a single instance of the manager
# All WebSocket connections share this manager
manager = ConnectionManager()


async def get_current_user_from_ws(websocket: WebSocket) -> dict | None:
    """
    Dependency to authenticate WebSocket connections.

    Reads JWT from cookie, validates it, and returns user payload.
    If anything fails, closes the WebSocket with appropriate error code.

    Args:
        websocket: The WebSocket connection being authenticated

    Returns:
        User payload dict (with 'sub' for username) or None if auth failed

    WebSocket close codes used:
        1008 (Policy Violation): Authentication failed
        1011 (Internal Error): Server not properly configured
    """
    # 1. Extract JWT from cookie
    token = websocket.cookies.get("auth_token")
    if not token:
        logger.warning("WebSocket connection attempt without auth token")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    # 2. Get the auth service from app state
    auth_service: UserAuth = websocket.app.state.user_auth
    if not auth_service:
        # This means GitLab isn't configured or service failed to initialize
        logger.error("UserAuth service not initialized - WebSocket rejected")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        return None

    # 3. Verify the token
    payload = auth_service.verify_token(token)
    if not payload:
        logger.warning("Invalid token in WebSocket connection attempt")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    return payload


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user: dict = Depends(get_current_user_from_ws)
):
    """
    WebSocket endpoint for real-time updates.

    Flow:
    1. Client connects with JWT cookie
    2. Auth dependency validates token
    3. Connection accepted and tracked
    4. Client can send/receive messages
    5. On disconnect, cleanup happens

    Message types FROM client:
        - ping: Keep-alive
        - request_update: Request fresh file list

    Message types TO client:
        - file_locked: Someone checked out a file
        - file_unlocked: Someone checked in a file
        - file_deleted: Admin deleted a file
        - user_connected: Someone connected
        - user_disconnected: Someone disconnected
        - pong: Response to ping
    """
    # If auth failed, dependency returns None and closes connection
    if not user:
        return

    username = user.get("sub", "unknown")

    # Connect and track this user
    await manager.connect(username, websocket)

    try:
        # Main message loop - wait for messages from client
        while True:
            # Receive message from client (as JSON)
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
                message_type = message.get("type", "unknown")

                # Handle different message types
                if message_type == "ping":
                    # Client is checking if we're alive
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    })

                elif message_type == "request_update":
                    # Client wants a fresh file list
                    # We could fetch and send it here, or just acknowledge
                    await websocket.send_json({
                        "type": "update_requested",
                        "message": "Refresh your file list via API"
                    })

                else:
                    logger.warning(f"Unknown message type from {username}: {message_type}")

            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON from {username}: {data}")

    except WebSocketDisconnect:
        # Client disconnected (normal or abnormal)
        manager.disconnect(username)

        # Notify other users
        await manager.broadcast({
            "type": "user_disconnected",
            "username": username,
            "timestamp": datetime.utcnow().isoformat()
        })

    except Exception as e:
        # Unexpected error - log it and clean up
        logger.error(f"WebSocket error for {username}: {e}", exc_info=True)
        manager.disconnect(username)


# Helper function for other routers to broadcast updates
async def broadcast_file_update(event_type: str, file_data: dict):
    """
    Broadcast a file update to all connected users.

    This function is called by other routers (files.py, admin.py)
    when something changes.

    Args:
        event_type: Type of event (file_locked, file_unlocked, etc.)
        file_data: Information about the file that changed

    Example usage in files.py:
        from app.api.routers.websocket import broadcast_file_update

        # After checking out a file:
        await broadcast_file_update("file_locked", {
            "filename": filename,
            "locked_by": username,
            "timestamp": datetime.utcnow().isoformat()
        })
    """
    await manager.broadcast({
        "type": event_type,
        "data": file_data,
        "timestamp": datetime.utcnow().isoformat()
    })
```

---

## Part 5: How to Use This in Other Routers

**In your `files.py` router, after checking out a file:**

```python
from app.api.routers.websocket import broadcast_file_update

@router.post("/{filename}/checkout")
async def checkout_file(filename: str, ...):
    # ... your existing checkout logic ...

    # After successful checkout, notify all users
    await broadcast_file_update("file_locked", {
        "filename": filename,
        "locked_by": username,
        "path": file_path
    })

    return {"status": "success"}
```

**This broadcasts to ALL connected users instantly!**

---

## Part 6: Frontend Connection (For Reference)

**Your frontend JavaScript should do:**

```javascript
// Connect to WebSocket
const ws = new WebSocket("ws://localhost:8000/ws");

// Handle incoming messages
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);

  if (message.type === "file_locked") {
    // Update UI to show file is locked
    updateFileStatus(message.data.filename, "locked", message.data.locked_by);
  } else if (message.type === "file_unlocked") {
    // Update UI to show file is available
    updateFileStatus(message.data.filename, "available", null);
  }
};

// Send ping every 30 seconds to keep connection alive
setInterval(() => {
  ws.send(JSON.stringify({ type: "ping" }));
}, 30000);
```

---

## Issues Fixed

### ✅ Issue 1: Connection Tracking

**Before:** No tracking
**After:** `active_connections` dict tracks all users

### ✅ Issue 2: Broadcasting

**Before:** No broadcast method
**After:** `broadcast()` sends to all users

### ✅ Issue 3: Message Structure

**Before:** No message types
**After:** Structured JSON messages with types

### ✅ Issue 4: Cleanup

**Before:** Disconnect did nothing
**After:** Removes dead connections, notifies users

### ✅ Issue 5: Keep-Alive

**Before:** No ping/pong
**After:** Handles ping messages

---

## Testing Your WebSocket

**Test 1: Connect and see logs**

Start server, open browser console:

```javascript
const ws = new WebSocket("ws://localhost:8000/ws");
ws.onopen = () => console.log("Connected!");
ws.onmessage = (e) => console.log("Message:", e.data);
```

Check server logs - should see "WebSocket connected"

---

**Test 2: Open two browser tabs**

Both should connect. Check server logs for connection count.

---

**Test 3: Broadcast test**

In Python console (while server running):

```python
from app.api.routers.websocket import manager
import asyncio

asyncio.run(manager.broadcast({"type": "test", "message": "Hello!"}))
```

All connected browsers should receive the message.

---

## Understanding Questions

**Q1:** Why use a dict for `active_connections` instead of a list?

**Q2:** What happens if a user opens the app in two tabs?

**Q3:** Why do we remove dead connections when broadcasting?

**Q4:** Why does the frontend need to send ping messages?

---

## What's Next?

Now you understand WebSockets, but you mentioned two other issues:

1. **"Even though I made a password, it's asking for Git token again"** - This is in your auth flow
2. **Admin and Dashboard don't work** - These likely depend on other services

**📁 Next File to Share:** Choose one:

- `backend/app/api/routers/auth.py` - To fix the password/token issue
- `backend/app/api/routers/dashboard.py` - To fix dashboard
- `backend/app/api/routers/admin.py` - To fix admin features

Which issue bothers you most? Share that file next!
