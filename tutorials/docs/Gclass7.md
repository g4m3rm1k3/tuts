# Step 7: WebSocket – Live Updates (Real-Time Sync – 1.5hr)

**Big Picture Goal**: Add WebSocket for live changes (e.g., user A checkouts → user B sees "locked" instantly). JS connects to /ws, handles messages (e.g., "FILE_LIST_UPDATED" → re-render). Backend broadcasts on changes. Understand **real-time communication** (push vs pull—faster sync).

**Why Seventh?** (Sync Principle: **Feedback Loop – React to Change**). Files/actions work; now real-time (no manual refresh). **Deep Dive**: WebSocket = full-duplex (bi-way chat)—pull (poll) = battery drain, push = instant. Why? Manufacturing = collaborative (lock conflict = immediate notify). Resource: [MDN WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) – 4min, "Connecting" section.

**When**: After actions—changes need broadcast. Use for collab (e.g., G-code edit: Others see update).

**How**: JS new WebSocket(url), onopen/onmessage/onclose. Backend manager broadcasts. Gotcha: Reconnect on drop (exponential backoff = gentle retry).

**Pre-Step**: Branch: `git checkout -b step-7-websocket`. Mock backend /ws (in endpoints.py): Use simple print for onmessage. Add to main.js initApp: `connectWebSocket();` (test connect).

---

### 7a: WebSocket Connection – Establishing the Channel

**Question**: How do we open a persistent connection to server for live messages? We need a URL with user param + basic handlers (open/close).

**Micro-Topic 1: Basic WebSocket Creation**  
**Type This (create ui/websocket.js)**:

```javascript
// websocket.js - Live sync. What: WebSocket = persistent connection.

export function connectWebSocket() {
  const protocol = location.protocol === "https:" ? "wss:" : "ws:"; // Secure if HTTPS.
  const wsUrl = `${protocol}//${location.host}/ws?user=${currentUser}`; // User param for backend.
  const ws = new WebSocket(wsUrl); // Create socket.
  console.log("Connecting to", wsUrl); // Test log.
}
```

**Inline 3D Explain**:

- **What**: new WebSocket = open channel. wss: = secure WS.
- **Why**: Persistent = push messages (no poll spam). **Deep Dive**: Query param = backend ID (user-specific broadcast). Resource: [MDN WebSocket Constructor](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/WebSocket) – 2min, "URL."
- **How**: location = current URL. Gotcha: No user = anonymous (backend default). **Alternative**: Poll fetch = simple, but slow (1s = laggy).

**Try This (10s)**: Update main.js initApp: `connectWebSocket();`. Refresh → console "Connecting to ws://localhost:5500/ws?user=..."? Tweak: Add &test=1 to URL → ?user=test&test=1. Reflect: "Why protocol check? HTTP = ws, HTTPS = wss (secure)."

**Inline Lens (SRP Integration)**: websocket.js = connection only (no message handle—next). Violate? Handle in main = bloat.

**Mini-Summary**: new WebSocket = channel open. URL param = context.

**Micro-Topic 2: Open Handler – Connection Confirmed**  
**Type This (add to connectWebSocket)**:

```javascript
ws.onopen = () => {
  // What: Callback on connect.
  console.log("WebSocket open"); // Confirm.
  ws.send("ping"); // Test message—backend echoes.
};
```

**Inline 3D Explain**:

- **What**: onopen = event listener (connect fires it).
- **Why**: Confirm = "ready to send" (no send before = fail). **Deep Dive**: send = text/binary—start simple. Resource: [MDN onopen](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/onopen) – 1min.
- **How**: () => = arrow func (short). Gotcha: No onopen = silent fail. **Alternative**: onerror for fail.

**Try This (15s)**: Backend mock onopen print. Refresh → "open" log + "ping" sent? Tweak: ws.send("user:" + currentUser) → backend sees. Reflect: "Why send? Heartbeat = alive check."

**Inline Lens (Error Handling Integration)**: onopen = success path. Violate? No log = "connected?" guess.

**Mini-Summary**: onopen = ready signal. send = first message.

**Git**: `git add websocket.js main.js && git commit -m "feat(step-7a): websocket connect + open"`.

---

### 7b: Handling Messages – Receiving & Routing Updates

**Question**: How do we receive server messages (e.g., "file updated")? We need onmessage to parse + act (e.g., re-render files).

**Micro-Topic 1: Basic Message Listener**  
**Type This (add to connectWebSocket)**:

```javascript
ws.onmessage = (event) => {
  // What: Callback on receive.
  const message = event.data; // Raw string.
  console.log("Received:", message); // Test.
};
```

**Inline 3D Explain**:

- **What**: onmessage = event with data (string/Blob).
- **Why**: Receive = "server push" (live lock change). **Deep Dive**: event.data = payload (JSON usually). Resource: [MDN onmessage](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/onmessage) – 2min, "Parsing."
- **How**: (event) = param. Gotcha: No listener = drop messages. **Alternative**: ondata for binary (images)—text for JSON.

**Try This (10s)**: Backend mock send "hello" on connect. Refresh → "Received: hello"? Tweak: event.data.toUpperCase() → "HELLO." Reflect: "Why event? Data = payload, event = meta (timestamp)."

**Micro-Topic 2: Parse JSON & Route by Type**  
**Type This (update onmessage)**:

```javascript
ws.onmessage = (event) => {
  try {
    const data = JSON.parse(event.data); // Parse string → object.
    const type = data.type; // Extract type.
    console.log("Type:", type); // Test route.
    switch (
      type // Route = act by type.
    ) {
      case "FILE_LIST_UPDATED":
        // Re-render files—next micro.
        break;
      default:
        console.warn("Unknown type:", type);
    }
  } catch (error) {
    console.error("Parse failed:", error); // Bad JSON.
  }
};
```

**Inline 3D Explain**:

- **What**: JSON.parse = string → object. switch = multi-route.
- **Why**: Route = "act smart" (type = "update files"). **Deep Dive**: Try/catch = parse errors (malformed = no crash). Resource: [MDN JSON.parse](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse) – 2min, "Reviver."
- **How**: data.type = assume structure. Gotcha: No try = crash on bad. **Alternative**: if/else = same, switch = clean for 5+ types.

**Try This (15s)**: Backend mock send '{"type": "test"}'. Refresh → "Type: test"? Bad JSON ('{bad') → "Parse failed." Tweak: Add case "ping": console.log("Pong!"). Reflect: "Why switch? If chain = nest—switch = flat."

**Inline Lens (Error Handling Integration)**: Catch = "bad data safe" (malformed = warn, not crash). Violate? Parse error = tab dead.

**Mini-Summary**: onmessage + parse + switch = receive/route. Try = robust.

**Git**: `git add websocket.js && git commit -m "feat(step-7b): message receive + route"`.

---

### 7c: Reconnect Logic – Handling Drops & Offline

**Question**: What if connection drops (WiFi flickers)? We need retry (backoff = gentle) + offline UI.

**Micro-Topic 1: Close Handler with Retry**  
**Type This (add to connectWebSocket)**:

```javascript
let reconnectAttempts = 0; // Track tries.
const MAX_ATTEMPTS = 5;

ws.onclose = (event) => {
  // What: Fired on disconnect.
  console.log("Closed:", event.code); // Code = reason (1000 = normal).
  if (reconnectAttempts < MAX_ATTEMPTS) {
    const delay = 1000 * Math.pow(2, reconnectAttempts); // 1s, 2s, 4s...
    setTimeout(() => {
      reconnectAttempts++;
      connectWebSocket(); // Retry.
    }, delay);
  }
};
```

**Inline 3D Explain**:

- **What**: onclose = end event. setTimeout = delay call.
- **Why**: Retry = resilient (drops happen). **Deep Dive**: Exponential backoff = "kind to server" (no flood retries). Resource: [MDN onclose](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/onclose) – 2min, "Codes."
- **How**: pow(2, n) = expo. Gotcha: No max = infinite loop. **Alternative**: Linear delay = thundering herd (all retry same time).

**Try This (10s)**: Dev tools Network → block WS → "Closed: ..." + retry logs? Unblock → reconnects? Tweak: MAX=1 → stops after one. Reflect: "Why expo? Short = spam, long = slow recovery."

**Micro-Topic 2: Offline UI on Max Attempts**  
**Type This (update onclose if block)**:

```javascript
} else {
  showNotification("Offline—retrying...", "error");  // User feedback.
  // Update status dot red—next.
}
```

**Inline 3D Explain**:

- **What**: Else = max fail.
- **Why**: UI = "tell user" (no guess). **Deep Dive**: navigator.onLine = browser hint (not always accurate). Resource: [MDN Offline](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/onLine) – 1min.
- **How**: showNotification from utils. Gotcha: No notify = silent fail. **Alternative**: Full offline page = PWA (service worker).

**Try This (15s)**: Set MAX=1, block WS → "Offline..."? Tweak: Add window.addEventListener("online", connectWebSocket) → auto-reconnect. Reflect: "Why notify? User thinks 'broken' vs 'wait.'"

**Inline Lens (Error Handling Integration)**: onclose = "expected fail" (networks drop). Violate? No retry = manual refresh.

**Mini-Summary**: onclose + backoff = resilient. UI on fail = kind.

**Git**: `git add websocket.js && git commit -m "feat(step-7c): reconnect + offline"`.

---

### 7d: Integrating with UI – Message Route to Re-Render

**Question**: How do we act on messages (e.g., "FILE_LIST_UPDATED" → refresh files)? Route type to func (re-render).

**Micro-Topic 1: Route to File Re-Render**  
**Type This (update onmessage switch)**:

```javascript
case "FILE_LIST_UPDATED":
  const files = data.payload;  // Extract data.
  window.appState.files = files;  // Update state.
  renderFiles(files);  // Call from fileManager—re-paint UI.
  break;
```

**Inline 3D Explain**:

- **What**: payload = message body. renderFiles = UI update.
- **Why**: Route = "type to action" (update = refresh). **Deep Dive**: State first = separation (update data → UI reacts). Resource: [Event-Driven MDN](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Introducing_workers#event_driven) – 3min, "Handlers."
- **How**: data from parse. Gotcha: No state update = stale UI. **Alternative**: Direct DOM = bypass state (hard sync).

**Try This (20s)**: Backend mock send {"type": "FILE_LIST_UPDATED", "payload": {"Misc": [{"filename": "new.mcam"}]}}. Refresh → re-render with new file? Tweak: Wrong type → warn. Reflect: "Why state first? Direct render = dup code (search/filter breaks)."

**Inline Lens (SRP Integration)**: websocket = route only (render = fileManager). Violate? Render here = mixed concerns.

**Mini-Summary**: Route + state update = live react. Payload = data extract.

**Git**: `git add websocket.js fileManager.js && git commit -m "feat(step-7d): message route to re-render"`.

---

**Step 7 Complete!** WebSocket live. Reflect: "Flow: Connect → open send ping → message parse → route type → state/UI update. SRP: websocket = channel, fileManager = render."

**Next**: Step 8: Dashboard (stats/activity). Go? 🚀
