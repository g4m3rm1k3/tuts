# Part 5: When Things Go Wrong (Error Handling) (25 minutes)

## The Problem with Our Current Code

**Our Version 1 code looks clean, but it's FRAGILE:**

```javascript
export async function getFiles() {
  const response = await fetch("http://localhost:8000/files");
  const data = await response.json();
  return data;
}
```

**What could go wrong?**

Let me show you...

---

## Error Scenario 1: Server is Down

**What happens if the server isn't running?**

```javascript
const files = await getFiles();
// ERROR: Failed to fetch
// Your app crashes!
```

**The browser console shows:**

```
Uncaught (in promise) TypeError: Failed to fetch
```

**Your user sees:**

- Blank page
- Or frozen UI
- Or "An error occurred" (if you're lucky)

**NOT GOOD!**

---

## Error Scenario 2: Server Returns Error

**What if the server responds with 404 Not Found or 500 Server Error?**

```javascript
// Server responds: 404 Not Found
const response = await fetch("/files");
console.log(response.ok); // false (not OK!)

// But our code still tries to parse JSON:
const data = await response.json(); // This might work...

// Server sent:
// { "error": "Not Found" }

// So data = { error: "Not Found" }
// We return this as if it's valid file data!
```

**Your app shows "Not Found" as if it's a file!**

---

## Error Scenario 3: Invalid JSON

**What if the server sends bad JSON?**

```javascript
// Server sends: "<html>Error Page</html>" (HTML, not JSON!)
const data = await response.json();
// ERROR: Unexpected token < in JSON at position 0
// Your app crashes!
```

---

## Error Scenario 4: Network Timeout

**What if the request takes forever?**

```javascript
const response = await fetch("/files");
// (waiting...)
// (still waiting...)
// (user gets impatient and leaves)
```

**No error, just infinite waiting!**

---

## The Solution: try/catch Blocks

**We need to CATCH errors and handle them gracefully.**

**Version 2: With error handling:**

```javascript
export async function getFiles() {
  try {
    const response = await fetch("http://localhost:8000/files");

    // Check if response is OK
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to get files:", error);
    throw error; // Re-throw so caller can handle it
  }
}
```

**Now let me explain EVERY new piece...**

---

### Understanding try/catch - DEEP DIVE

```javascript
try {
  // Code that might fail
} catch (error) {
  // What to do if it fails
}
```

**Think of it like a safety net:**

```
You (JavaScript):
  "I'm going to try something risky..."

  try {
    walkTightrope();  ← Might fall!
  }

  "Oops, I fell!"

  catch (error) {
    landInSafetyNet();  ← Caught the fall!
    console.log("That was close!");
  }
```

---

### How try/catch Works (Step by Step)

**Scenario 1: NO error**

```javascript
try {
  console.log("Step 1");
  console.log("Step 2");
  console.log("Step 3");
} catch (error) {
  console.log("Error happened!");
}
console.log("Step 4");
```

**Output:**

```
Step 1
Step 2
Step 3
Step 4
```

**The catch block is SKIPPED because no error!**

---

**Scenario 2: Error occurs**

```javascript
try {
  console.log("Step 1");
  throw new Error("Something broke!"); // Error happens here!
  console.log("Step 2"); // This never runs!
} catch (error) {
  console.log("Error happened:", error.message);
}
console.log("Step 3");
```

**Output:**

```
Step 1
Error happened: Something broke!
Step 3
```

**When error occurs:**

1. JavaScript IMMEDIATELY jumps to catch block
2. Code after the error in try block is SKIPPED
3. After catch block, code continues normally

---

### Understanding `throw`

**`throw` creates an error and stops execution:**

```javascript
function divide(a, b) {
  if (b === 0) {
    throw new Error("Can't divide by zero!");
  }
  return a / b;
}

try {
  const result = divide(10, 0);
  console.log(result); // Never runs!
} catch (error) {
  console.log(error.message); // "Can't divide by zero!"
}
```

**What `throw` does:**

1. Creates an Error object
2. STOPS the current function immediately
3. Looks for the nearest catch block
4. Jumps there

**Like pulling the emergency brake on a train!**

---

### The Error Object

**When you throw or catch an error, you get an Error object:**

```javascript
const error = new Error("Something broke!");

console.log(error.message); // "Something broke!"
console.log(error.name); // "Error"
console.log(error.stack); // Stack trace (where it happened)
```

**Properties:**

**`message`** - Human-readable description

```javascript
error.message; // "Something broke!"
```

**`name`** - Type of error

```javascript
error.name; // "Error" or "TypeError" or "NetworkError"
```

**`stack`** - Where the error happened (file, line number)

```javascript
error.stack;
// "Error: Something broke!
//     at getFiles (api.js:5)
//     at loadData (main.js:12)"
```

---

### 🎥 Understanding try/catch

**Watch these for deeper understanding:**

- 🎥 [Try/Catch in 100 Seconds](https://www.youtube.com/watch?v=cFTFtuEQ-10) (2 min) - Quick overview
- 📺 [JavaScript Error Handling](https://www.youtube.com/watch?v=S9R1JscczLU) (14 min) - Complete guide
- 📚 [MDN: try...catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch) - Reference

---

### Checking response.ok

```javascript
if (!response.ok) {
  throw new Error(`HTTP ${response.status}: ${response.statusText}`);
}
```

**Breaking this down:**

### `response.ok`

**This is a boolean (true/false) property on the Response object.**

```javascript
// Status codes 200-299 → ok = true
Response { status: 200, ok: true }   // ✅ Success
Response { status: 201, ok: true }   // ✅ Created

// Status codes outside that range → ok = false
Response { status: 404, ok: false }  // ❌ Not Found
Response { status: 500, ok: false }  // ❌ Server Error
```

**So `response.ok` tells you: "Did the server say everything is fine?"**

---

### The `!` operator (NOT)

**`!` flips true/false:**

```javascript
!true; // false
!false; // true

const ok = true;
!ok; // false

const notOk = false;
!notOk; // true (double negative!)
```

**So `!response.ok` means: "Is the response NOT ok?"**

```javascript
if (!response.ok) {
  // "If the response is NOT ok, do this..."
}
```

**Examples:**

```javascript
// Status 200
response.ok = true
!response.ok = false
if (false) { ... }  // Skipped

// Status 404
response.ok = false
!response.ok = true
if (true) { ... }  // Runs!
```

---

### Building the Error Message

```javascript
throw new Error(`HTTP ${response.status}: ${response.statusText}`);
```

**Using template literals to build a helpful error message:**

```javascript
// If response.status = 404 and response.statusText = "Not Found"
`HTTP ${response.status}: ${response.statusText}`
= `HTTP 404: Not Found`
```

**Why include both status number and text?**

- Status number: For programmers (404, 500, etc.)
- Status text: For humans ("Not Found", "Server Error")

**Common HTTP status codes you'll see:**

```
200 OK              - Success
201 Created         - Resource created successfully
400 Bad Request     - Your request was invalid
401 Unauthorized    - You need to log in
403 Forbidden       - You don't have permission
404 Not Found       - Resource doesn't exist
500 Server Error    - Server crashed
503 Unavailable     - Server is overloaded/down
```

---

### The catch Block

```javascript
catch (error) {
  console.error('Failed to get files:', error);
  throw error;
}
```

**Breaking it down:**

### `catch (error)`

- `error` is a parameter (like a function parameter)
- It receives the Error object that was thrown
- You can name it anything: `err`, `e`, `exception`

### `console.error()`

**Like `console.log()` but for errors:**

- Shows in red in browser console
- Includes stack trace automatically
- Makes errors easy to spot

**Why log AND re-throw?**

```javascript
console.error("Failed to get files:", error); // Log it
throw error; // Re-throw it
```

**Two purposes:**

**1. Log for debugging**

- You (developer) can see what went wrong in console
- Helpful during development

**2. Re-throw for caller**

- The code that CALLED `getFiles()` should know it failed
- They can show user a message
- They can retry
- They can handle it their way

**Example:**

```javascript
// In main.js
try {
  const files = await getFiles();
  showFiles(files);
} catch (error) {
  // We can handle the error here!
  showUserMessage("Failed to load files. Please try again.");
}
```

---

### Practice: Understanding Error Flow

**Trace through this code. What gets logged?**

```javascript
async function test() {
  try {
    console.log("A");
    throw new Error("Oops!");
    console.log("B");
  } catch (error) {
    console.log("C");
  }
  console.log("D");
}

test();
console.log("E");
```

**Try to figure it out before looking at the answer!**

<details>
<summary>Click to see answer</summary>

**Output:**

```
A
C
D
E
```

**Explanation:**

```
Step 1: test() called
Step 2: console.log('A') → prints "A"
Step 3: throw new Error('Oops!') → error thrown!
Step 4: JavaScript jumps to catch block (skips console.log('B'))
Step 5: console.log('C') → prints "C"
Step 6: After catch, continue normally
Step 7: console.log('D') → prints "D"
Step 8: test() finishes, but it's async so continues
Step 9: console.log('E') → prints "E"
```

**Key points:**

- 'B' never prints (after error)
- 'C' does print (in catch block)
- 'D' does print (after catch)
- 'E' does print (outside test function)

</details>

---

## Testing Error Handling

**Let's test our improved code with errors!**

**Update `test-api.html`:**

```html
<script type="module">
  import { getFiles } from "./js/api.js";

  document.getElementById("test-btn").addEventListener("click", async () => {
    const output = document.getElementById("output");

    try {
      output.textContent = "Loading...";
      const files = await getFiles();
      output.textContent = JSON.stringify(files, null, 2);
    } catch (error) {
      // Show error to user
      output.textContent = `❌ Error: ${error.message}`;
      output.style.color = "red";
    }
  });
</script>
```

**Now errors are handled gracefully!**

---

# Part 6: Building the API Wrapper (30 minutes)

## The Problem: Repetitive Code

**If we add more API functions, we'll repeat the same pattern:**

```javascript
export async function getFiles() {
  try {
    const response = await fetch("http://localhost:8000/files");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Failed:", error);
    throw error;
  }
}

export async function getUsers() {
  try {
    const response = await fetch("http://localhost:8000/users");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Failed:", error);
    throw error;
  }
}

// Copy-paste for every endpoint... NOT GOOD!
```

**This is called "code duplication" - a BAD SMELL!**

**Problems:**

- If we fix a bug, we have to fix it 10 times
- Easy to forget one place
- Hard to maintain
- Lots of typing

---

## The Solution: A Wrapper Function

**Let's extract the common pattern into ONE function:**

```javascript
async function apiFetch(endpoint, options = {}) {
  // Common logic here
}

// Then use it:
export async function getFiles() {
  return apiFetch("/files");
}

export async function getUsers() {
  return apiFetch("/users");
}
```

**Much cleaner!**

---

## Building apiFetch - Version 1

**Add this to `api.js` BEFORE your other functions:**

```javascript
const API_BASE = "http://localhost:8000";

async function apiFetch(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;

  try {
    const response = await fetch(url, options);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
  }
}
```

**Now let me explain EVERY new concept here...**

---

### Understanding Constants at the Top

```javascript
const API_BASE = "http://localhost:8000";
```

**Why put this at the top of the file?**

**Configuration in one place!**

**When you deploy to production:**

```javascript
// Development
const API_BASE = "http://localhost:8000";

// Production
const API_BASE = "https://api.yourcompany.com";
```

**Change it once, affects all API calls!**

**Alternative: Environment variables (more advanced)**

```javascript
const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";
```

---

### Understanding Default Parameters

```javascript
async function apiFetch(endpoint, options = {}) {
```

**What does `options = {}` mean?**

**It's a DEFAULT PARAMETER.**

**If caller doesn't provide `options`, use `{}` (empty object).**

**Examples:**

```javascript
// Called with both parameters
apiFetch("/files", { method: "POST" });
// endpoint = '/files'
// options = { method: 'POST' }

// Called with only one parameter
apiFetch("/files");
// endpoint = '/files'
// options = {} (default!)
```

---

### Why Default to Empty Object?

**Because we'll use `options` later:**

```javascript
const response = await fetch(url, options);
```

**If `options` was `undefined`, fetch would break!**

```javascript
// Without default:
apiFetch("/files");
// options = undefined
fetch(url, undefined); // Works, but weird

// With default:
apiFetch("/files");
// options = {}
fetch(url, {}); // Clean!
```

---

### Practice: Default Parameters

**What gets logged?**

```javascript
function greet(name, greeting = "Hello") {
  console.log(`${greeting}, ${name}!`);
}

greet("Alice", "Hi");
greet("Bob");
```

<details>
<summary>Click to see answer</summary>

**Output:**

```
Hi, Alice!
Hello, Bob!
```

**Explanation:**

- First call: Both parameters provided, use 'Hi'
- Second call: Only name provided, use default 'Hello'

</details>

---

### Building the URL

```javascript
const url = `${API_BASE}${endpoint}`;
```

**This concatenates (joins) the base URL with the endpoint:**

```javascript
API_BASE = "http://localhost:8000";
endpoint = "/files";

url = "http://localhost:8000" + "/files";
url = "http://localhost:8000/files";
```

**Why not just use the full URL everywhere?**

```javascript
// Bad: Hardcoded everywhere
fetch("http://localhost:8000/files");
fetch("http://localhost:8000/users");
fetch("http://localhost:8000/checkout");
// Change localhost → production = update 50 places!

// Good: Configurable
apiFetch("/files");
apiFetch("/users");
apiFetch("/checkout");
// Change API_BASE once = updates everywhere!
```

---

### Passing Options to fetch()

```javascript
const response = await fetch(url, options);
```

**The `options` object configures the request:**

**Common options:**

```javascript
{
  method: 'GET',      // or 'POST', 'PUT', 'DELETE'
  headers: {          // Extra info to send
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token123'
  },
  body: JSON.stringify(data)  // Data to send (POST/PUT)
}
```

**Examples:**

**GET request (default):**

```javascript
apiFetch("/files");
// method defaults to GET, no options needed
```

**POST request with data:**

```javascript
apiFetch("/checkout", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    filename: "part1.mcam",
    user: "john",
  }),
});
```

---

### Logging Which Endpoint Failed

```javascript
console.error(`API Error (${endpoint}):`, error);
```

**Why include the endpoint in the log?**

**Without it:**

```
API Error: HTTP 404: Not Found
(Which endpoint failed? No idea!)
```

**With it:**

```
API Error (/files): HTTP 404: Not Found
(Ah, the /files endpoint failed!)
```

**Makes debugging MUCH easier!**

---

## Using apiFetch in Our Functions

**Now update `getFiles()` to use our wrapper:**

```javascript
export async function getFiles() {
  // Comment out mock data for now
  // return mockData...

  // Use real API call
  return apiFetch("/files");
}
```

**That's it! One line!**

**All the error handling is in `apiFetch()`!**

---

## Adding More API Functions

**Now adding new endpoints is EASY:**

```javascript
/**
 * Checkout a file (lock it for editing)
 */
export async function checkoutFile(filename, username) {
  return apiFetch("/checkout", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ filename, username }),
  });
}

/**
 * Check in a file (upload new version and unlock)
 */
export async function checkinFile(filename, fileData, message) {
  // Create form data for file upload
  const formData = new FormData();
  formData.append("file", fileData);
  formData.append("filename", filename);
  formData.append("message", message);

  return apiFetch("/checkin", {
    method: "POST",
    body: formData,
    // Note: Don't set Content-Type for FormData!
    // Browser sets it automatically with boundary
  });
}

/**
 * Cancel checkout (unlock without uploading)
 */
export async function cancelCheckout(filename, username) {
  return apiFetch("/cancel", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ filename, username }),
  });
}
```

---

### Understanding JSON.stringify()

**You see this pattern a lot:**

```javascript
body: JSON.stringify({ filename, username });
```

**What does `JSON.stringify()` do?**

**It converts JavaScript objects to JSON strings:**

```javascript
// JavaScript object
const data = {
  filename: "part1.mcam",
  username: "john",
};

// Convert to JSON string
const json = JSON.stringify(data);

console.log(json);
// '{"filename":"part1.mcam","username":"john"}'
```

**Why?**

**HTTP can only send TEXT, not JavaScript objects!**

```javascript
// This WON'T work:
fetch("/checkout", {
  body: { filename: "part1.mcam" }, // Object! Won't work!
});

// This WILL work:
fetch("/checkout", {
  body: '{"filename":"part1.mcam"}', // String! Works!
});
```

**The server receives the string and parses it back to an object.**

---

### Understanding Object Shorthand

**You might see this and wonder what it means:**

```javascript
JSON.stringify({ filename, username });
```

**This is SHORTHAND for:**

```javascript
JSON.stringify({ filename: filename, username: username });
```

**If the variable name matches the object key, you can omit the key:**

**Long form:**

```javascript
const filename = "part1.mcam";
const username = "john";

const obj = {
  filename: filename,
  username: username,
};
```

**Shorthand:**

```javascript
const filename = "part1.mcam";
const username = "john";

const obj = {
  filename,
  username,
};
```

**Both create the exact same object!**

---

### Understanding FormData (For File Uploads)

**When uploading files, we can't use JSON. We use `FormData`:**

```javascript
const formData = new FormData();
formData.append("file", fileData);
formData.append("filename", filename);
```

**What is FormData?**

**It's like packing items in a box to mail:**

```
FormData = Box
│
├─ file: (the actual file data)
├─ filename: "part1.mcam"
└─ message: "Fixed dimension"
```

**Why not JSON?**

**JSON can only handle TEXT and NUMBERS, not BINARY DATA (files)!**

```javascript
// This WON'T work:
JSON.stringify({
  file: fileData, // Binary data! JSON can't handle this!
});

// This WILL work:
const formData = new FormData();
formData.append("file", fileData); // FormData handles binary!
```

---

### Why No Content-Type Header for FormData?

**Notice we DON'T set Content-Type for FormData:**

```javascript
// NO headers!
return apiFetch("/checkin", {
  method: "POST",
  body: formData,
});
```

**Why not?**

**The browser automatically sets Content-Type with a special "boundary":**

```
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
```

**The boundary is like dividers in the box separating items:**

```
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"

(file data here)
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="filename"

part1.mcam
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

**If you manually set Content-Type, you'd have to generate the boundary yourself - a pain!**

**Let the browser do it automatically!**

---

## 🎥 Understanding HTTP Methods and Bodies

**Watch these:**

- 🎥 [HTTP Methods (GET, POST, etc)](https://www.youtube.com/watch?v=iYM2zFP3Zn0) (6 min)
- 📺 [JSON.stringify Explained](https://www.youtube.com/watch?v=vQzxCcLQIRA) (8 min)
- 📺 [FormData Explained](https://www.youtube.com/watch?v=Flj6go0ti4I) (12 min)
- 📚 [MDN: Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) - Complete guide

---

# Part 7: Advanced Error Handling (20 minutes)

## Getting Better Error Messages from the Server

**Right now, our error messages are generic:**

```javascript
throw new Error(`HTTP ${response.status}: ${response.statusText}`);
// "HTTP 404: Not Found"
```

**But the server might send MORE DETAILS in the response body!**

---

### FastAPI Error Format

**Your FastAPI backend sends errors like this:**

```json
{
  "detail": "File 'part1.mcam' is currently locked by user 'john_doe'"
}
```

**Let's extract that detail!**

---

## Version 2: Better Error Messages

**Update `apiFetch()`:**

```javascript
async function apiFetch(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;

  try {
    const response = await fetch(url, options);

    if (!response.ok) {
      // Try to get detailed error from server
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;

      try {
        const errorData = await response.json();
        if (errorData.detail) {
          errorMessage = errorData.detail;
        } else if (errorData.message) {
          errorMessage = errorData.message;
        }
      } catch {
        // Response wasn't JSON, use default message
      }

      throw new Error(errorMessage);
    }

    return await response.json();
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
  }
}
```

**Let me explain the new nested try/catch...**

---

### Understanding Nested try/catch

**Why do we have a try/catch INSIDE another try/catch?**

```javascript
try {
  // Outer try
  if (!response.ok) {
    try {
      // Inner try
      const errorData = await response.json();
    } catch {
      // Inner catch
    }
  }
} catch (error) {
  // Outer catch
}
```

**Because parsing the error response MIGHT fail!**

**Scenario 1: Server sends JSON error**

```
Status: 404
Body: { "detail": "File not found" }

Inner try: Successfully parses JSON
errorMessage = "File not found"
```

**Scenario 2: Server sends HTML error**

```
Status: 500
Body: <html><body>Server Error</body></html>

Inner try: await response.json() FAILS (not JSON!)
Inner catch: Caught! Use default message
errorMessage = "HTTP 500: Server Error"
```

**Without the inner try/catch, HTML errors would crash your app!**

---

### The Empty catch Block

**Notice the inner catch has no parameter:**

```javascript
catch {
  // No (error) parameter!
}
```

**Why?**

**We don't care WHAT went wrong, just that it did:**

```javascript
// With parameter (if you need it):
catch (error) {
  console.log('Parsing failed:', error);
}

// Without parameter (if you don't need it):
catch {
  // Just continue with default message
}
```

**Both are valid! Use the simpler version when you don't need the error details.**

---

### Checking Multiple Error Formats

```javascript
if (errorData.detail) {
  errorMessage = errorData.detail;
} else if (errorData.message) {
  errorMessage = errorData.message;
}
```

**Why check both?**

**Different backends use different formats:**

**FastAPI:**

```json
{ "detail": "Error message" }
```

**Express/Custom:**

```json
{ "message": "Error message" }
```

**Generic:**

```json
{ "error": "Error message" }
```

**We check the most common ones!**

**You could add more:**

```javascript
if (errorData.detail) {
  errorMessage = errorData.detail;
} else if (errorData.message) {
  errorMessage = errorData.message;
} else if (errorData.error) {
  errorMessage = errorData.error;
}
```

---

## Adding Request Headers

**Let's make our wrapper set default headers:**

```javascript
async function apiFetch(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;

  // Set default headers
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers  // Merge with any custom headers
  };

  try {
    const response = await fetch(url, {
      ...options,  // Spread existing options
      headers      // Use our headers
    });

    // ... rest of the code
```

**Let me explain the new syntax...**

---

### Understanding the Spread Operator (...)

**The `...` is called the "spread operator".**

**It "spreads out" an object's properties:**

```javascript
const obj1 = { a: 1, b: 2 };
const obj2 = { c: 3 };

const combined = { ...obj1, ...obj2 };
// combined = { a: 1, b: 2, c: 3 }
```

**Visual:**

```
obj1 = { a: 1, b: 2 }
         ↓ ...obj1 spreads it out
       { a: 1, b: 2, c: 3 }
                      ↑
                   ...obj2 adds this
```

---

### Why Spread Options?

```javascript
const response = await fetch(url, {
  ...options, // Spread user's options
  headers, // Add/override headers
});
```

**This merges the user's options with our defaults:**

**Example 1: User passes no options**

```javascript
apiFetch('/files')
// options = {}

// Becomes:
fetch(url, {
  ...{},      // Nothing
  headers: { 'Content-Type': 'application/json' }
})

// Result:
{ headers: { 'Content-Type': 'application/json' } }
```

**Example 2: User passes method**

```javascript
apiFetch('/checkout', { method: 'POST' })
// options = { method: 'POST' }

// Becomes:
fetch(url, {
  ...{ method: 'POST' },  // Spread this
  headers: { 'Content-Type': 'application/json' }
})

// Result:
{
  method: 'POST',
  headers: { 'Content-Type': 'application/json' }
}
```

---

### Merging Headers

```javascript
const headers = {
  "Content-Type": "application/json",
  ...options.headers,
};
```

**This sets a default but allows overriding:**

**Example 1: No custom headers**

```javascript
apiFetch("/files");
// options.headers = undefined

headers = {
  "Content-Type": "application/json",
  ...undefined, // Spreading undefined does nothing
};

// Result: { 'Content-Type': 'application/json' }
```

**Example 2: Custom Authorization header**

```javascript
apiFetch('/files', {
  headers: { 'Authorization': 'Bearer token123' }
})

headers = {
  'Content-Type': 'application/json',
  ...{ 'Authorization': 'Bearer token123' }
}

// Result:
{
  'Content-Type': 'application/json',
  'Authorization': 'Bearer token123'
}
```

**Example 3: Override Content-Type**

```javascript
apiFetch("/upload", {
  headers: { "Content-Type": "multipart/form-data" },
});

headers = {
  "Content-Type": "application/json", // Default
  ...{ "Content-Type": "multipart/form-data" }, // Override!
};

// Result: { 'Content-Type': 'multipart/form-data' }
// The spread OVERWRITES the default!
```

---

### 🎥 Understanding Spread Operator

**Watch these:**

- 🎥 [Spread Operator in 100 Seconds](https://www.youtube.com/watch?v=iLx4ma8ZqvQ) (2 min)
- 📺 [JavaScript Spread Operator](https://www.youtube.com/watch?v=1INe_jCWq1Q) (10 min)
- 📚 [MDN: Spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax)

---

## Complete apiFetch Function (Final Version)

**Here's the complete, production-ready wrapper:**

```javascript
/**
 * Base URL for all API requests
 */
const API_BASE = "http://localhost:8000";

/**
 * Wrapper around fetch with error handling and defaults
 *
 * @param {string} endpoint - API endpoint (e.g., '/files')
 * @param {Object} options - Fetch options (method, headers, body)
 * @returns {Promise<any>} Response data as JSON
 * @throws {Error} On network or API errors
 */
async function apiFetch(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;

  // Set default headers
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  try {
    // Make the request
    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Check if response is OK (status 200-299)
    if (!response.ok) {
      // Try to get detailed error message from server
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;

      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch {
        // Response wasn't JSON, use default message
      }

      throw new Error(errorMessage);
    }

    // Parse and return JSON response
    return await response.json();
  } catch (error) {
    // Log error for debugging
    console.error(`API Error (${endpoint}):`, error);

    // Re-throw so caller can handle it
    throw new Error(`API Error: ${error.message}`);
  }
}
```

---

# Part 8: Complete API Module (10 minutes)

## Your Final api.js File

**Here's the complete, ready-to-use API module:**

```javascript
/**
 * API Module - Handles all communication with backend
 */

// Configuration
const API_BASE = "http://localhost:8000";

/**
 * Base fetch wrapper with error handling
 */
async function apiFetch(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;

  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;

      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch {
        // Not JSON
      }

      throw new Error(errorMessage);
    }

    return await response.json();
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw new Error(`API Error: ${error.message}`);
  }
}

/**
 * Get list of all files
 */
export async function getFiles() {
  return apiFetch("/files");
}

/**
 * Check out a file (lock for editing)
 */
export async function checkoutFile(filename, username) {
  return apiFetch("/checkout", {
    method: "POST",
    body: JSON.stringify({ filename, username }),
  });
}

/**
 * Check in a file (upload new version and unlock)
 */
export async function checkinFile(filename, fileData, message) {
  const formData = new FormData();
  formData.append("file", fileData);
  formData.append("filename", filename);
  formData.append("message", message);

  return apiFetch("/checkin", {
    method: "POST",
    body: formData,
    headers: {}, // Let browser set Content-Type for FormData
  });
}

/**
 * Cancel checkout (unlock without uploading)
 */
export async function cancelCheckout(filename, username) {
  return apiFetch("/cancel", {
    method: "POST",
    body: JSON.stringify({ filename, username }),
  });
}

/**
 * Get file history
 */
export async function getFileHistory(filename) {
  return apiFetch(`/history/${filename}`);
}
```

---

## Using Your API Module

**In your main app code:**

```javascript
import { getFiles, checkoutFile, checkinFile } from "./js/api.js";

// Load files
async function loadFiles() {
  try {
    const files = await getFiles();
    displayFiles(files);
  } catch (error) {
    showError("Failed to load files: " + error.message);
  }
}

// Checkout a file
async function handleCheckout(filename) {
  try {
    await checkoutFile(filename, currentUser);
    showSuccess(`Checked out ${filename}`);
    await loadFiles(); // Refresh the list
  } catch (error) {
    showError("Checkout failed: " + error.message);
  }
}

// Check in a file
async function handleCheckin(filename, file, message) {
  try {
    await checkinFile(filename, file, message);
    showSuccess(`Checked in ${filename}`);
    await loadFiles(); // Refresh the list
  } catch (error) {
    showError("Check-in failed: " + error.message);
  }
}
```

**Clean, simple, error-handled!**

---

# Section 3D Complete! 🎉

## What You Mastered

### Core Concepts

✅ **HTTP Protocol** - How browsers talk to servers  
✅ **async/await** - Deep understanding of asynchronous code  
✅ **Promises** - The three states, how they work  
✅ **try/catch** - Error handling patterns  
✅ **fetch API** - Making HTTP requests  
✅ **Error handling** - Graceful degradation

### Advanced Patterns

✅ **API wrapper** - DRY principle in action  
✅ **Default parameters** - Clean function interfaces  
✅ **Spread operator** - Merging objects  
✅ **Nested try/catch** - Handling multiple failure points  
✅ **Error extraction** - Getting details from server

### Practical Skills

✅ **GET requests** - Fetching data  
✅ **POST requests** - Sending data  
✅ **File uploads** - Using FormData  
✅ **JSON handling** - stringify/parse  
✅ **Header management** - Content-Type, Authorization

---

## 📚 Complete Video Resource List

**HTTP & APIs:**

- 🎥 [HTTP Explained in 5 Minutes](https://www.youtube.com/watch?v=iYM2zFP3Zn0) (5 min)
- 📺 [HTTP Request/Response Cycle](https://www.youtube.com/watch?v=DrI2lUXL1no) (12 min)
- 🎬 [REST API Concepts](https://www.youtube.com/watch?v=7YcW25PHnAA) (8 min)

**Async/Await:**

- 🎥 [Async/Await in 100 Seconds](https://www.youtube.com/watch?v=vn3tm0quoqE) (2 min)
- 📺 [Async JavaScript Explained](https://www.youtube.com/watch?v=670f71LTWpM) (16 min)
- 🎬 [The Event Loop](https://www.youtube.com/watch?v=8aGhZQkoFbQ) (27 min)

**Error Handling:**

- 🎥 [Try/Catch in 100 Seconds](https://www.youtube.com/watch?v=cFTFtuEQ-10) (2 min)
- 📺 [JavaScript Error Handling](https://www.youtube.com/watch?v=S9R1JscczLU) (14 min)

**Advanced JavaScript:**

- 🎥 [Spread Operator in 100 Seconds](https://www.youtube.com/watch?v=iLx4ma8ZqvQ) (2 min)
- 📺 [JavaScript Spread Operator](https://www.youtube.com/watch?v=1INe_jCWq1Q) (10 min)
- 📺 [JSON.stringify Explained](https://www.youtube.com/watch?v=vQzxCcLQIRA) (8 min)
- 📺 [FormData Explained](https://www.youtube.com/watch?v=Flj6go0ti4I) (12 min)

**MDN References:**

- 📚 [HTTP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
- 📚 [Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- 📚 [async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)
- 📚 [try...catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch)
- 📚 [Spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax)

---

## Test Your Understanding

**Answer without looking back:**

1. What are the three states of a Promise?
2. What does `await` do?
3. Why do we need `try/catch`?
4. What does the spread operator `...` do?
5. Why check `response.ok` before parsing JSON?
6. When should you NOT set Content-Type header?
7. What's the difference between `throw error` and `console.error(error)`?

<details>
<summary>Answers</summary>

1. PENDING (waiting), FULFILLED (success), REJECTED (error)
2. Pauses the function, unwraps the Promise, returns the actual value
3. To catch errors gracefully instead of crashing the app
4. Spreads object properties into another object (merging)
5. Because non-OK responses might not have JSON, and we want to extract error details
6. When using FormData (browser sets it automatically with boundary)
7. `throw` stops execution and propagates the error up; `console.error` just logs it and continues

</details>

---

## What's Next: Section 3E

**Section 3E: Building the Main App**

We'll finally connect everything:

- Import all our utilities (formatDate, formatFileSize, etc.)
- Import all our API functions (getFiles, checkout, etc.)
- Build the UI components
- Handle user interactions
- Make everything work together
- See the COMPLETE app running!

**This is where it all comes together!** 🚀

---

**Ready for Section 3E?** Say **"Start Section 3E"** and we'll build the main application! 💪

Or do you:

- Need practice with any concepts?
- Have questions?
- Want to review anything?

**I'm proud of you for getting this far! You're not a copy-paste programmer anymore - you UNDERSTAND this stuff!** 🎉
