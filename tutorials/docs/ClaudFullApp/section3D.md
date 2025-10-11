

# Section 3D: Building the API Module - For People Who Fear async/await

**This tutorial is for YOU if:**

- ✅ You see `async/await` and panic
- ✅ You copy fetch() code and pray it works
- ✅ Promises confuse you
- ✅ You don't understand why your API call "doesn't work"
- ✅ Network errors make your app crash
- ✅ You want to ACTUALLY understand backend communication

**By the end, you will:**

- Understand EXACTLY how browsers talk to servers
- Know what async/await REALLY does
- Build a bulletproof API layer
- Handle every possible error scenario
- Never copy-paste fetch code again

**Time:** 90-120 minutes (we're going DEEP)

---

# Part 1: What Problem Are We Solving? (10 minutes)

## The Real-World Scenario

**You're building a PDM system. Your React frontend needs to:**

1. Show a list of files from the database
2. Lock a file when someone clicks "Checkout"
3. Upload a new version when they click "Check In"

**Problem:** Your JavaScript code runs in the BROWSER.  
**The database lives on a SERVER.**

**They're literally different computers!**

```
Your Browser                      The Server
┌─────────────┐                  ┌──────────────┐
│             │                  │              │
│  Frontend   │  ← How do → ?   │   Backend    │
│  (React)    │    they talk?    │  (FastAPI)   │
│             │                  │              │
└─────────────┘                  └──────────────┘
```

**Your browser can't directly access:**

- The database
- The file system
- Other computers

**It needs to ASK the server to do things for it.**

**That's what an API does.**

---

## Real-World Analogy: The Restaurant

**Imagine you're at a restaurant (the client/browser).**

**You can't walk into the kitchen and cook your own food!**

**Instead:**

1. You read the MENU (API documentation)
2. You tell the WAITER what you want (make an API request)
3. The waiter goes to the KITCHEN (backend server)
4. The chef COOKS your food (database query, file operations)
5. The waiter BRINGS you the food (API response)

**If something goes wrong:**

- Kitchen is closed (server down)
- They're out of an ingredient (resource not found)
- Your order is unclear (bad request)
- Takes too long (timeout)

**Your API module is the WAITER - handling communication between you and the kitchen.**

---

## What We're Building

**By the end of this section, you'll have:**

```javascript
// Simple, clean API calls:
const files = await getFiles();
await checkoutFile("part1.mcam", "john");
await checkinFile("part1.mcam", fileData, "Fixed dimension");

// With built-in error handling:
// - Network failures
// - Server errors
// - Invalid responses
// - Timeouts
```

**All the ugly details hidden in ONE module!**

---

## Manufacturing Analogy

**Your PDM system is like a shop floor with a parts crib:**

**Parts Crib (Backend Server):**

- Stores all the parts (files)
- Tracks who has what
- Records who checked out what part

**Machinist (Frontend User):**

- Requests parts from crib
- Can't just walk in and grab parts
- Must follow checkout procedures

**Crib Attendant (API):**

- Handles all requests
- Verifies permissions
- Updates records
- Returns parts or error messages

---

# Part 2: Understanding How Computers Talk (15 minutes)

## HTTP: The Language of the Web

**When your browser talks to a server, they use HTTP (Hypertext Transfer Protocol).**

**Think of it like a postal service:**

---

### The HTTP Request (Sending a Letter)

**You write a letter and put it in the mail:**

```
┌──────────────────────────────┐
│  FROM: Your Browser          │
│  TO: api.yourcompany.com     │
│                               │
│  REQUEST TYPE: GET            │
│  PATH: /files                 │
│                               │
│  (Optional) BODY:            │
│  { user: "john" }            │
└──────────────────────────────┘
```

**Parts of a request:**

**1. METHOD (what you want to do)**

```
GET     = "Give me information"
POST    = "Create something new"
PUT     = "Update something"
DELETE  = "Remove something"
```

**2. URL (where to send it)**

```
http://localhost:8000/files
  │         │         │
  │         │         └─ Path (which resource)
  │         └─ Server address
  └─ Protocol (how to talk)
```

**3. HEADERS (extra info)**

```
Content-Type: application/json
Authorization: Bearer token123
```

**4. BODY (data you're sending)**

```json
{
  "filename": "part1.mcam",
  "user": "john"
}
```

---

### The HTTP Response (Getting a Reply)

**The server reads your letter and sends back a reply:**

```
┌──────────────────────────────┐
│  FROM: Server                │
│  TO: Your Browser            │
│                               │
│  STATUS: 200 OK               │
│                               │
│  BODY:                        │
│  {                           │
│    "files": [...]            │
│  }                           │
└──────────────────────────────┘
```

**Parts of a response:**

**1. STATUS CODE (what happened)**

```
200 OK           = Success!
201 Created      = Successfully created
400 Bad Request  = You sent bad data
401 Unauthorized = You're not logged in
404 Not Found    = Resource doesn't exist
500 Server Error = Server crashed
```

**2. HEADERS (metadata)**

```
Content-Type: application/json
Content-Length: 1234
```

**3. BODY (the actual data)**

```json
{
  "files": [{ "name": "part1.mcam", "size": 2048 }]
}
```

---

### Visual Timeline: What Happens When You Make a Request

```
Time →

Browser                                    Server
   │                                          │
   │  1. User clicks "Show Files"            │
   │                                          │
   ├──── 2. Send GET /files ───────────────→ │
   │                                          │
   │                                          │  3. Query database
   │                                          │  4. Get file list
   │                                          │  5. Format as JSON
   │                                          │
   │ ←──── 6. Send back data ────────────────┤
   │         Status: 200                      │
   │         Body: {...}                      │
   │                                          │
   7. Parse JSON                              │
   8. Update UI                               │
   9. Show files to user                      │
```

**IMPORTANT: Steps 2-6 take TIME!**

- Your code PAUSES at step 2
- Waits for step 6
- Then continues with step 7

**This is why we need async/await!**

---

## 🎥 Understanding HTTP

**Watch these to understand the foundation:**

- 🎥 [HTTP Explained in 5 Minutes](https://www.youtube.com/watch?v=iYM2zFP3Zn0) (5 min) - Perfect intro
- 📺 [HTTP Request/Response Cycle](https://www.youtube.com/watch?v=DrI2lUXL1no) (12 min) - Detailed
- 🎬 [REST API Concepts](https://www.youtube.com/watch?v=7YcW25PHnAA) (8 min) - REST basics
- 📚 [MDN: HTTP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview) - Reference

**Watch at least the first two before continuing!**

---

# Part 3: The Problem with Timing (Understanding Async) (20 minutes)

## Why Can't We Just Do This?

**You might think:**

```javascript
const files = getFiles(); // Get files from server
console.log(files); // Show them
```

**Try it and you get:**

```javascript
console.log(files); // Promise { <pending> }
```

**WHAT?! Why not the actual files?**

---

## The Coffee Shop Analogy

**Imagine ordering coffee:**

**WRONG WAY (Blocking - what you tried):**

```
You: "I'd like a latte"
Cashier: "Okay, wait right here"
You: (stand frozen, can't do anything)
Cashier: (makes your coffee)
Cashier: (makes 10 other orders)
Cashier: "Here's your latte" (5 minutes later)
You: (finally unfreeze and take it)
```

**If JavaScript worked this way, your entire browser would FREEZE for 5 minutes!**

- Can't click anything
- Can't scroll
- Can't type
- Just frozen

**That would be terrible UX!**

---

**RIGHT WAY (Non-blocking - how JavaScript actually works):**

```
You: "I'd like a latte"
Cashier: "Sure! Here's a number. I'll call you when it's ready"
You: (take number, sit down, check phone, do other things)
Barista: (makes coffee)
Cashier: "Order 42!"
You: (go grab your coffee)
```

**You can do other things while you wait!**

**JavaScript does this with PROMISES.**

---

## What is a Promise?

**A Promise is like the number they give you at the coffee shop.**

**It says:**

- "I don't have your coffee YET"
- "But I PROMISE to get it for you"
- "When it's ready, I'll let you know"

**In JavaScript:**

```javascript
const coffeePromise = orderCoffee();
// coffeePromise = "I'll get you coffee eventually"

// Later when it's ready:
coffeePromise.then((coffee) => {
  drink(coffee);
});
```

---

## Three States of a Promise

**A promise is always in one of three states:**

### 1. PENDING (waiting)

```javascript
const promise = fetch("/files");
// Status: PENDING
// "I'm working on it, not done yet"
```

### 2. FULFILLED (success)

```javascript
// When server responds successfully
// Status: FULFILLED
// Value: { files: [...] }
```

### 3. REJECTED (failure)

```javascript
// When something goes wrong
// Status: REJECTED
// Reason: "Network error"
```

**Visual:**

```
PENDING
   ├─→ FULFILLED (got data) ✅
   └─→ REJECTED (error) ❌
```

**Once fulfilled or rejected, it NEVER changes again!**

---

## The Old Way: .then() Chains

**Before async/await, you had to do this:**

```javascript
fetch("/files")
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
    return fetch("/users");
  })
  .then((response) => response.json())
  .then((users) => {
    console.log(users);
  })
  .catch((error) => {
    console.error(error);
  });
```

**This is called "callback hell" or "promise chaining".**

**Problems:**

- Hard to read (nested callbacks)
- Hard to debug
- Hard to handle errors properly
- Looks messy

---

## The New Way: async/await

**async/await makes promises look like normal code:**

```javascript
async function loadData() {
  const response = await fetch("/files");
  const data = await response.json();
  console.log(data);

  const userResponse = await fetch("/users");
  const users = await userResponse.json();
  console.log(users);
}
```

**MUCH cleaner!**

**But what do `async` and `await` actually DO?**

---

## Understanding `async` Keyword - DEEP DIVE

```javascript
async function loadData() {
  // ...
}
```

**What `async` does:**

### 1. Marks the function as asynchronous

**Meaning:** "This function will do things that take time"

### 2. Makes the function ALWAYS return a Promise

**Even if you return a regular value!**

```javascript
async function test() {
  return 5;
}

const result = test();
console.log(result); // Promise { 5 } (not just 5!)
```

**JavaScript automatically wraps it in a promise!**

### 3. Allows you to use `await` inside

**You CAN'T use `await` in a regular function:**

```javascript
function loadData() {
  await fetch('/files');  // ERROR! Can't use await here
}
```

**You CAN use `await` in an async function:**

```javascript
async function loadData() {
  await fetch("/files"); // ✅ Works!
}
```

---

## Understanding `await` Keyword - DEEP DIVE

```javascript
const response = await fetch("/files");
```

**What `await` does:**

### 1. Pauses the function

**The function STOPS at this line and waits.**

### 2. Unwraps the Promise

**Instead of getting Promise { ... }, you get the actual value.**

```javascript
// Without await:
const promise = fetch("/files");
console.log(promise); // Promise { <pending> }

// With await:
const response = await fetch("/files");
console.log(response); // Response { ok: true, ... } (actual response!)
```

### 3. Lets other code run

**While waiting, JavaScript can do other things.**

**Your function is paused, but the browser isn't frozen!**

- Other functions can run
- User can click buttons
- Animations continue

### 4. Resumes when Promise resolves

**When the promise is ready, your function continues from where it paused.**

---

## Visual: What Happens with await

**Let me trace through this code:**

```javascript
async function loadFiles() {
  console.log("1. Starting");

  const response = await fetch("/files");

  console.log("2. Got response");
}

console.log("3. Before calling loadFiles");
loadFiles();
console.log("4. After calling loadFiles");
```

**What order do the console.logs happen?**

**Guess before looking at the answer!**

<details>
<summary>Click to see the order</summary>

**Output:**

```
3. Before calling loadFiles
1. Starting
4. After calling loadFiles
(wait for network...)
2. Got response
```

**Why this order?**

```
Step 1: console.log('3. Before calling loadFiles')
        ↓
Step 2: loadFiles() called
        ↓
Step 3: console.log('1. Starting')
        ↓
Step 4: await fetch('/files') ← Function PAUSES here
        ↓ (function paused, JavaScript continues other code)
Step 5: console.log('4. After calling loadFiles')
        ↓
        (wait for network request...)
        ↓
Step 6: Network responds, function RESUMES
        ↓
Step 7: console.log('2. Got response')
```

**Key insight:** `await` pauses THAT FUNCTION, but not all JavaScript!

</details>

---

## 🎥 Understanding Async/Await

**Watch these for deep understanding:**

- 🎥 [Async/Await in 100 Seconds](https://www.youtube.com/watch?v=vn3tm0quoqE) (2 min) - Quick overview
- 📺 [Async JavaScript Explained](https://www.youtube.com/watch?v=670f71LTWpM) (16 min) - Complete guide
- 🎬 [The Event Loop](https://www.youtube.com/watch?v=8aGhZQkoFbQ) (27 min) - How it works internally
- 📚 [MDN: async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function) - Reference

**The Event Loop video is LONG but will change how you understand JavaScript!**

---

# Part 4: Building Our First API Call (20 minutes)

## Version 1: The Absolute Simplest Code That Works

**Let's start with the MINIMUM code to fetch files:**

**Create `src/js/api.js`:**

```javascript
/**
 * Get list of files from server
 */
export async function getFiles() {
  const response = await fetch("http://localhost:8000/files");
  const data = await response.json();
  return data;
}
```

**That's it! 3 lines of actual code.**

**But I'm going to explain EVERY SINGLE PIECE of those 3 lines...**

---

### Line 1: The Function Declaration

```javascript
export async function getFiles() {
```

**Breaking down EVERY word:**

### `export`

- Makes this function available to other files
- Without `export`, it's private to this file
- Lets you do: `import { getFiles } from './api.js'`

### `async`

- Marks this as an asynchronous function
- Means: "This function does things that take time"
- Allows us to use `await` inside
- Makes the function return a Promise automatically

### `function`

- JavaScript keyword for defining a function
- A function is a reusable block of code

### `getFiles`

- The NAME of our function
- We chose this name because it describes what it does
- Could be anything: `fetchFiles`, `loadFiles`, `getAllFiles`
- Convention: use `get` for retrieving data

### `()`

- Parentheses for parameters
- Empty = no parameters needed for this function
- Later we'll add parameters: `getFiles(username)`

### `{`

- Curly brace starts the function body
- All the function's code goes between `{` and `}`

---

### Line 2: The Fetch Call

```javascript
const response = await fetch("http://localhost:8000/files");
```

**Breaking it down piece by piece:**

### `const`

- Creates a variable (constant)
- Can't be reassigned after created
- Stores the value on the right

### `response`

- Variable name we chose
- Stores the server's response
- Could call it anything: `result`, `data`, `serverResponse`
- Convention: call it `response` when it's the fetch response

### `=`

- Assignment operator
- "Take what's on the right, store it in the variable on the left"

### `await`

- **THIS IS THE KEY PART**
- Pauses the function RIGHT HERE
- Waits for `fetch()` to complete
- Unwraps the Promise to get the actual Response object
- Without `await`, you'd get Promise { <pending> } instead of the response

### `fetch()`

- Built-in JavaScript function
- Makes HTTP requests
- Returns a Promise
- Has been in browsers since 2015

### `'http://localhost:8000/files'`

- The URL to request
- `http://` = protocol (how to talk)
- `localhost` = this computer
- `:8000` = port number (where the server is listening)
- `/files` = the path (which resource we want)

---

### Understanding What fetch() Returns

**`fetch()` returns a Response object that looks like this:**

```javascript
Response {
  ok: true,              // Was it successful?
  status: 200,           // HTTP status code
  statusText: 'OK',      // Status as text
  headers: {...},        // Response headers
  body: ReadableStream,  // The actual data (not readable yet!)
  // Methods:
  json(),               // Parse body as JSON
  text(),               // Get body as text
  blob(),               // Get body as binary data
}
```

**IMPORTANT:** The `body` is a stream (like a river of data). We need to READ it.

---

### Line 3: Parsing the Response

```javascript
const data = await response.json();
```

**Breaking it down:**

### `const data`

- Another variable
- Will store the parsed JSON data
- Could call it: `files`, `result`, `jsonData`

### `await`

- Again, we're waiting!
- `.json()` is ALSO asynchronous (returns a Promise)
- We need to wait for it to finish parsing

### `response.json()`

- Method on the Response object
- Reads the body stream
- Parses it as JSON
- Returns a Promise that resolves to JavaScript object

---

### Why Two awaits?

**You might wonder: "Why do we need TWO awaits?"**

```javascript
const response = await fetch("/files"); // await #1
const data = await response.json(); // await #2
```

**Because there are TWO asynchronous steps:**

**Step 1: Wait for network request**

```javascript
await fetch("/files");
// Waits for server to respond with headers
// Returns Response object
// But body hasn't been read yet!
```

**Step 2: Wait to read the body**

```javascript
await response.json();
// Reads the body (could be large!)
// Parses the JSON
// Returns JavaScript object
```

**Visual:**

```
fetch('/files')
    ↓ (network request)
Response received (headers)
    ↓
response.json()
    ↓ (reading & parsing body)
JavaScript object
```

---

### Line 4: Return the Data

```javascript
return data;
```

**Simple enough, right?**

### `return`

- Sends the value back to whoever called this function
- Stops executing the function

### `data`

- The variable we created with the parsed JSON

**But remember:** Because this is an `async` function, JavaScript automatically wraps the return value in a Promise!

```javascript
// You write:
return data;

// JavaScript actually returns:
return Promise.resolve(data);
```

**This is why you need `await` when calling `getFiles()`:**

```javascript
const files = await getFiles(); // await unwraps the Promise
```

---

## Testing Version 1

**Let's test it! Create `src/test-api.html`:**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Test API</title>
  </head>
  <body>
    <h1>API Test</h1>
    <button id="test-btn">Load Files</button>
    <pre id="output"></pre>

    <script type="module">
      import { getFiles } from "./js/api.js";

      document
        .getElementById("test-btn")
        .addEventListener("click", async () => {
          try {
            console.log("Fetching files...");
            const files = await getFiles();
            console.log("Got files:", files);

            document.getElementById("output").textContent = JSON.stringify(
              files,
              null,
              2
            );
          } catch (error) {
            console.error("Error:", error);
            document.getElementById("output").textContent =
              "Error: " + error.message;
          }
        });
    </script>
  </body>
</html>
```

**What this test does:**

1. Imports our `getFiles` function
2. When you click the button, calls `getFiles()`
3. Shows the result on the page

---

### But Wait - We Don't Have a Server Yet!

**Try clicking the button. You'll see an error:**

```
Error: Failed to fetch
```

**Why?** No server is running at `localhost:8000`!

**Let's fix that with MOCK DATA...**

---

## Adding Mock Data (For Development)

**While building the frontend, we don't want to depend on the backend being ready.**

**Solution:** Return fake data when there's no server.

**Update `api.js`:**

```javascript
/**
 * Get list of files from server
 */
export async function getFiles() {
  // FOR NOW: Return mock data (until backend is ready)
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        "Active Jobs": [
          {
            filename: "1234567_ABC123.mcam",
            size: 2048576,
            modified_at: new Date(Date.now() - 3600000).toISOString(),
            status: "unlocked",
            locked_by: null,
          },
          {
            filename: "1234568_DEF456.mcam",
            size: 1536000,
            modified_at: new Date(Date.now() - 7200000).toISOString(),
            status: "locked",
            locked_by: "john_doe",
          },
        ],
      });
    }, 1000); // Simulate network delay
  });
}
```

**Now test again - it works!**

---

### Understanding the Mock Data Pattern

**Let me break down this Promise pattern:**

```javascript
return new Promise((resolve) => {
  setTimeout(() => {
    resolve(data);
  }, 1000);
});
```

**What each part does:**

### `new Promise((resolve) => { ... })`

- Creates a new Promise manually
- `resolve` is a function that "fulfills" the promise
- Think: "resolve = mark as complete with this value"

### `setTimeout(() => { ... }, 1000)`

- Waits 1000 milliseconds (1 second)
- Then runs the function inside
- Simulates network delay (real requests take time!)

### `resolve(data)`

- Fulfills the promise with the mock data
- Like saying "the request is done, here's the result"

**Why simulate delay?**

- Tests loading states
- Makes UI feel realistic
- Catches timing bugs

---

**Ready to continue? Say "continue" and I'll keep building Section 3D with this same deep level of explanation!**

Or would you like me to adjust anything about this approach first?

I'm committed to making this deeper and better than that tutorial you shared! 🎯
