**YOU'RE ABSOLUTELY RIGHT!** 🎯

I completely dropped the ball there. We did that beautiful npm setup with custom Mastercam colors in Section 3A, and then I reverted to CDN in Section 3E. That's confusing and inconsistent!

**Good catch fixing it by pointing to `public/output.css`!**

**Going forward, I'll:**

- ✅ Use the custom Mastercam colors we configured (`mastercam-500`, `dark-800`, etc.)
- ✅ Reference the built CSS file
- ✅ Keep the same masterclass depth
- ✅ Small code chunks with deep explanations
- ✅ Show how all pieces connect

**I'm thrilled you're finding this valuable!** Let's keep building. 💪

---

# Part 5: State Management Functions (Building the Traffic Controller) (20 minutes)

## Understanding State Management

**Think of your app like a traffic light:**

```
State 1: RED    → Show loading
State 2: YELLOW → (transition)
State 3: GREEN  → Show data
State 4: RED    → Show error
```

**Only ONE light is on at a time!**

**Same with our app:**

```
State 1: LOADING visible, error hidden, fileList hidden
State 2: LOADING hidden, error visible, fileList hidden
State 3: LOADING hidden, error hidden, fileList visible
```

**We need functions to switch between states cleanly.**

---

## Why We Need State Functions

**Without state functions (messy):**

```javascript
// Every time we load data:
document.getElementById("loading").classList.remove("hidden");
document.getElementById("error").classList.add("hidden");
document.getElementById("file-list").classList.add("hidden");

// Every time there's an error:
document.getElementById("loading").classList.add("hidden");
document.getElementById("error").classList.remove("hidden");
document.getElementById("file-list").classList.add("hidden");

// Every time data loads:
document.getElementById("loading").classList.add("hidden");
document.getElementById("error").classList.add("hidden");
document.getElementById("file-list").classList.remove("hidden");
```

**Problems:**

- Repeated code (violates DRY - Don't Repeat Yourself)
- Easy to forget to hide one
- Easy to make typos
- Hard to maintain

---

**With state functions (clean):**

```javascript
showLoading();
showError("Server is down");
showFileList();
```

**Benefits:**

- One line to change state
- Can't forget to hide others
- Easy to maintain
- Self-documenting code

---

## Building showLoading() - Step by Step

**Add this function to `main.js` after the `elements` object:**

```javascript
/**
 * Shows the loading state
 * Hides all other states
 */
function showLoading() {
  elements.loading.classList.remove("hidden");
  elements.error.classList.add("hidden");
  elements.fileList.classList.add("hidden");
}
```

**Let me explain EVERY piece of this function...**

---

### Function Declaration

```javascript
function showLoading() {
```

**Breaking it down:**

**`function`** - JavaScript keyword for creating a function

**`showLoading`** - The name we chose

- Uses camelCase (first word lowercase, rest capitalized)
- Starts with verb (`show`) - describes what it does
- Clear and descriptive

**`()`** - Parameters (empty - this function needs no input)

**`{`** - Start of function body

---

### Understanding classList

```javascript
elements.loading.classList.remove("hidden");
```

**What is `classList`?**

Every HTML element has a `classList` property that lets you manage CSS classes.

**The element:**

```html
<div id="loading" class="text-center py-8 hidden"></div>
```

**As JavaScript object:**

```javascript
elements.loading
  ├─ classList
  │   ├─ add(className)
  │   ├─ remove(className)
  │   ├─ toggle(className)
  │   └─ contains(className)
  ├─ style
  ├─ textContent
  └─ ...
```

---

### classList Methods

**`.add(className)`** - Adds a class

```javascript
element.classList.add("hidden");
// Before: <div class="text-center">
// After:  <div class="text-center hidden">
```

**`.remove(className)`** - Removes a class

```javascript
element.classList.remove("hidden");
// Before: <div class="text-center hidden">
// After:  <div class="text-center">
```

**`.toggle(className)`** - Adds if missing, removes if present

```javascript
element.classList.toggle("hidden");
// If hidden exists: removes it
// If hidden doesn't exist: adds it
```

**`.contains(className)`** - Checks if class exists

```javascript
if (element.classList.contains("hidden")) {
  console.log("Element is hidden");
}
```

---

### Why remove('hidden') vs add('hidden')?

**In Tailwind, `hidden` means invisible:**

```css
.hidden {
  display: none;
}
```

**To SHOW an element:** Remove the `hidden` class

```javascript
elements.loading.classList.remove("hidden");
// Element becomes visible
```

**To HIDE an element:** Add the `hidden` class

```javascript
elements.loading.classList.add("hidden");
// Element becomes invisible
```

**Think of it like:**

```
remove('hidden') = SHOW (uncover)
add('hidden') = HIDE (cover up)
```

---

### The Three-Line Pattern

```javascript
elements.loading.classList.remove("hidden"); // SHOW loading
elements.error.classList.add("hidden"); // HIDE error
elements.fileList.classList.add("hidden"); // HIDE file list
```

**What this does:**

**Line 1:** Make loading visible

```html
<!-- Before -->
<div id="loading" class="text-center py-8 hidden">
  <!-- After -->
  <div id="loading" class="text-center py-8"></div>
</div>
```

**Line 2 & 3:** Make sure other states are hidden

**Visual:**

```
Before calling showLoading():
[Loading: hidden] [Error: hidden] [FileList: visible]
         ↓
After calling showLoading():
[Loading: VISIBLE] [Error: hidden] [FileList: hidden]
```

**Only ONE state is visible!**

---

### Why Hide the Others?

**You might think:** "If I'm showing loading, the others should already be hidden!"

**But what if:**

**Scenario 1: User clicks refresh while viewing files**

```
Current state: FileList visible
User clicks refresh
Need to show: Loading
```

Without hiding fileList, you'd see BOTH loading AND files! (Confusing!)

**Scenario 2: Error occurred, user retries**

```
Current state: Error visible
User clicks retry
Need to show: Loading
```

Without hiding error, you'd see BOTH loading AND error!

**Solution:** ALWAYS explicitly set ALL states.

---

## Building showError() - With Parameters

**Add this function:**

```javascript
/**
 * Shows the error state
 * Hides all other states
 * @param {string} message - Error message to display
 */
function showError(message) {
  elements.loading.classList.add("hidden");
  elements.error.classList.remove("hidden");
  elements.fileList.classList.add("hidden");

  elements.errorMessage.textContent = message;
}
```

**New concepts to understand...**

---

### Function Parameters

```javascript
function showError(message) {
```

**What is `message`?**

It's a **parameter** - a placeholder for a value you'll pass in.

**When you call the function:**

```javascript
showError("Server is down");
//         ↑
//    This value becomes "message" inside the function
```

**Inside the function:**

```javascript
function showError(message) {
  // message = 'Server is down'
  elements.errorMessage.textContent = message;
  // Sets text to: 'Server is down'
}
```

---

### Why Parameters?

**Without parameter (bad):**

```javascript
function showError() {
  elements.errorMessage.textContent = "Error occurred";
  // Same message every time! Not helpful!
}
```

**With parameter (good):**

```javascript
function showError(message) {
  elements.errorMessage.textContent = message;
  // Different message each time!
}

showError("Server is down");
showError("File not found");
showError("Network error");
```

**Flexible and reusable!**

---

### Setting textContent

```javascript
elements.errorMessage.textContent = message;
```

**What is `textContent`?**

A property that lets you get or set the text inside an element.

**Getting text:**

```javascript
const text = elements.errorMessage.textContent;
console.log(text); // Whatever text is currently inside
```

**Setting text:**

```javascript
elements.errorMessage.textContent = "New text!";
// Element now contains: "New text!"
```

**Example:**

**Before:**

```html
<span id="error-message"></span>
```

**After running:**

```javascript
elements.errorMessage.textContent = "Server is down";
```

**Result:**

```html
<span id="error-message">Server is down</span>
```

---

### textContent vs innerHTML

**Two ways to set content:**

**`textContent` (safer):**

```javascript
element.textContent = "<strong>Hello</strong>";
// Shows literally: <strong>Hello</strong>
// HTML is treated as plain text
```

**`innerHTML` (dangerous):**

```javascript
element.innerHTML = "<strong>Hello</strong>";
// Shows: Hello (in bold)
// HTML is executed!
```

**Why textContent is safer:**

```javascript
// User input (could be malicious):
const userInput = '<script>alert("Hacked!")</script>';

// With textContent (safe):
element.textContent = userInput;
// Shows: <script>alert("Hacked!")</script>
// Just text, script doesn't run!

// With innerHTML (DANGEROUS):
element.innerHTML = userInput;
// Script RUNS! User can inject code!
```

**Rule:** Use `textContent` for plain text, `innerHTML` only when you control the content!

---

## Building showFileList()

**Add this function:**

```javascript
/**
 * Shows the file list state
 * Hides all other states
 */
function showFileList() {
  elements.loading.classList.add("hidden");
  elements.error.classList.add("hidden");
  elements.fileList.classList.remove("hidden");
}
```

**Same pattern as the others!**

**Now we have three clean functions:**

```javascript
showLoading(); // Show loading spinner
showError("Some message"); // Show error with message
showFileList(); // Show file list
```

---

## Testing State Functions

**Add this temporary test code at the bottom of `main.js`:**

```javascript
// TEMPORARY TEST CODE (remove later)
console.log("Testing state functions...");

// Test 1: Show loading
showLoading();
console.log("Showing loading state");

// Test 2: After 2 seconds, show error
setTimeout(() => {
  showError("This is a test error!");
  console.log("Showing error state");
}, 2000);

// Test 3: After 4 seconds, show file list
setTimeout(() => {
  showFileList();
  console.log("Showing file list state");
}, 4000);
```

**Save and refresh browser.**

**Watch what happens:**

1. Loading shows immediately
2. After 2 seconds → Error shows
3. After 4 seconds → File list shows (empty for now)

**Check console - should see the log messages!**

**This proves our state management works!** ✅

---

### Understanding setTimeout()

```javascript
setTimeout(() => {
  showError("Test error!");
}, 2000);
```

**What is `setTimeout()`?**

A built-in JavaScript function that runs code AFTER a delay.

**Breaking it down:**

**`setTimeout(`** - The function name

**`() => { ... }`** - An arrow function (the code to run)

**`, 2000`** - Delay in milliseconds (2000ms = 2 seconds)

**`)`** - Close the function call

---

**How it works:**

```javascript
console.log("Start");

setTimeout(() => {
  console.log("After 2 seconds");
}, 2000);

console.log("End");
```

**Output:**

```
Start
End
(wait 2 seconds...)
After 2 seconds
```

**Why this order?**

1. `console.log('Start')` runs immediately
2. `setTimeout()` SCHEDULES the function for later
3. `console.log('End')` runs immediately
4. After 2 seconds, the scheduled function runs

**setTimeout is ASYNCHRONOUS!**

---

### Arrow Function Syntax Review

**Old way:**

```javascript
setTimeout(function () {
  console.log("Hello");
}, 2000);
```

**New way (arrow function):**

```javascript
setTimeout(() => {
  console.log("Hello");
}, 2000);
```

**Both work the same!**

**Why arrow functions?**

- Shorter syntax
- Cleaner to read
- Modern standard

---

## Removing Test Code

**Now that we've verified state functions work, DELETE the test code:**

```javascript
// Delete everything from here:
console.log("Testing state functions...");
showLoading();
// ... all the setTimeout stuff ...
// To here
```

**Your main.js should now end with just the three state functions!**

---

## 🎥 Understanding DOM Manipulation

**Watch these to deepen your understanding:**

- 🎥 [classList Explained](https://www.youtube.com/watch?v=gMGVo10t-Sc) (5 min) - Using classList
- 📺 [textContent vs innerHTML](https://www.youtube.com/watch?v=ns1LX6mEvyM) (8 min) - Security
- 🎬 [JavaScript DOM Manipulation](https://www.youtube.com/watch?v=5fb2aPlgoys) (30 min) - Complete
- 📚 [MDN: classList](https://developer.mozilla.org/en-US/docs/Web/API/Element/classList) - Reference

---

# Part 6: Loading and Displaying Files (The Main Event!) (30 minutes)

## The Big Picture

**Here's what we're about to build:**

```
User opens page
    ↓
showLoading() → User sees spinner
    ↓
getFiles() → Calls API
    ↓
await (pauses here...)
    ↓
Server responds with files
    ↓
Loop through files
    ↓
For each file:
  - Format date
  - Format size
  - Build HTML card
    ↓
Insert all cards into DOM
    ↓
showFileList() → User sees files!
```

**Every function we built comes together!**

---

## Building the loadFiles() Function - Version 1

**Add this function to `main.js`:**

```javascript
/**
 * Loads files from the API and displays them
 * Version 1: Basic structure
 */
async function loadFiles() {
  try {
    // Show loading state
    showLoading();

    // Fetch files from API
    const files = await getFiles();

    // Log to see what we got
    console.log("Files loaded:", files);

    // Show success state
    showFileList();
  } catch (error) {
    // Show error state
    showError(error.message);
    console.error("Failed to load files:", error);
  }
}
```

**Let me explain EVERY new concept here...**

---

### The async Keyword

```javascript
async function loadFiles() {
```

**Why `async`?**

Because we're using `await` inside!

**Remember from Section 3D:**

- `async` marks function as asynchronous
- Allows use of `await` keyword
- Makes function return a Promise

**Without `async`:**

```javascript
function loadFiles() {
  const files = await getFiles();  // ❌ ERROR!
  // Can't use await in non-async function
}
```

**With `async`:**

```javascript
async function loadFiles() {
  const files = await getFiles(); // ✅ Works!
}
```

---

### The try/catch Block

```javascript
try {
  // Code that might fail
} catch (error) {
  // What to do if it fails
}
```

**Why wrap everything in try/catch?**

**Because `getFiles()` might throw an error:**

**Scenario 1: Network is down**

```javascript
const files = await getFiles();
// ❌ Error: Failed to fetch
```

**Scenario 2: Server returns 500**

```javascript
const files = await getFiles();
// ❌ Error: HTTP 500: Server Error
```

**Without try/catch:**

```javascript
async function loadFiles() {
  const files = await getFiles(); // ❌ Error thrown
  // App crashes! User sees nothing!
}
```

**With try/catch:**

```javascript
async function loadFiles() {
  try {
    const files = await getFiles();
  } catch (error) {
    showError(error.message); // User sees friendly error!
  }
}
```

---

### The Flow of Control

**Let me trace through the ENTIRE execution:**

```javascript
async function loadFiles() {
  try {
    showLoading(); // Step 1
    const files = await getFiles(); // Step 2 (pauses here)
    console.log("Files loaded:", files); // Step 3
    showFileList(); // Step 4
  } catch (error) {
    showError(error.message); // Only if error
  }
}
```

---

**SUCCESS PATH:**

```
Step 1: showLoading()
  → Loading spinner shows
  → User sees: ⏳ Loading files...

Step 2: await getFiles()
  → Function PAUSES here
  → HTTP request sent to server
  → (User still sees loading spinner)
  → Server responds with data
  → Function RESUMES

Step 3: console.log()
  → Logs data to console

Step 4: showFileList()
  → Hides loading
  → Shows file list container
  → (Empty for now, we'll fill it next)
```

---

**ERROR PATH:**

```
Step 1: showLoading()
  → Loading spinner shows

Step 2: await getFiles()
  → Function PAUSES
  → HTTP request sent
  → ❌ Server is down / Network error / 500 error
  → Error thrown
  → JavaScript JUMPS to catch block

Step 3 & 4: SKIPPED (never run)

catch block:
  → showError(error.message)
  → User sees: ⚠️ Error: Server is down
```

---

### Understanding error.message

```javascript
catch (error) {
  showError(error.message);
}
```

**What is `error`?**

When an error is thrown (or caught), it's an **Error object**.

**Error object structure:**

```javascript
Error {
  message: 'HTTP 500: Server Error',  // Human-readable description
  name: 'Error',                      // Type of error
  stack: 'Error: HTTP 500...'         // Stack trace
}
```

**`error.message`** extracts just the message:

```javascript
error.message; // 'HTTP 500: Server Error'
```

**Why use .message?**

**Without .message:**

```javascript
showError(error);
// Shows: [object Object]  (useless!)
```

**With .message:**

```javascript
showError(error.message);
// Shows: HTTP 500: Server Error  (helpful!)
```

---

## Calling loadFiles() on Page Load

**Add this at the very bottom of `main.js`:**

```javascript
/**
 * Initialize app when page loads
 */
document.addEventListener("DOMContentLoaded", () => {
  console.log("Page loaded, starting app...");
  loadFiles();
});
```

**Let me explain this deeply...**

---

### Understanding DOMContentLoaded

```javascript
document.addEventListener("DOMContentLoaded", () => {
  // Code here runs when HTML is ready
});
```

**What is DOMContentLoaded?**

An **event** that fires when the HTML is fully loaded.

**Timeline of page load:**

```
Step 1: Browser starts loading HTML
Step 2: Browser parses HTML
Step 3: ✅ DOMContentLoaded fires (HTML ready!)
Step 4: Images, CSS continue loading
Step 5: load event fires (everything ready)
```

**Why wait for DOMContentLoaded?**

**Without waiting:**

```javascript
// This might run BEFORE HTML is loaded:
document.getElementById("loading"); // null (element doesn't exist yet!)
```

**With waiting:**

```javascript
document.addEventListener("DOMContentLoaded", () => {
  // This runs AFTER HTML is loaded:
  document.getElementById("loading"); // ✅ Element exists!
});
```

---

### Understanding addEventListener()

```javascript
document.addEventListener("DOMContentLoaded", callback);
```

**What is addEventListener?**

It "listens" for events and runs a function when the event happens.

**Breaking it down:**

**`document`** - The entire page

**`.addEventListener(`** - Method to listen for events

**`'DOMContentLoaded'`** - Name of the event to listen for

**`, () => { ... }`** - Function to run when event fires

**`)`** - Close the method call

---

**Event listener pattern:**

```javascript
target.addEventListener("eventName", function () {
  // What to do when event happens
});
```

**Examples:**

**Click event:**

```javascript
button.addEventListener("click", () => {
  console.log("Button clicked!");
});
```

**Keyboard event:**

```javascript
document.addEventListener("keydown", (event) => {
  console.log("Key pressed:", event.key);
});
```

**Page load:**

```javascript
document.addEventListener("DOMContentLoaded", () => {
  console.log("Page ready!");
});
```

---

### Alternative: Why Not Just Put Code at Bottom?

**You might wonder:** "Our script tag is at the end of `<body>`. HTML is already loaded! Why do we need DOMContentLoaded?"

**Good question!**

**Option 1: Script at end of body (what we have)**

```html
<body>
  <!-- All HTML -->
  <script type="module" src="main.js"></script>
</body>
```

**Option 2: DOMContentLoaded listener**

```javascript
document.addEventListener("DOMContentLoaded", () => {
  // Code here
});
```

**With modules (`type="module"`), both work because:**

- Modules automatically defer
- HTML is loaded before module runs

**But DOMContentLoaded is SAFER because:**

- Explicit guarantee HTML is ready
- Works regardless of script location
- Industry standard
- Self-documenting code

**Best practice:** Use DOMContentLoaded even though our script is at the end.

---

## Testing loadFiles()

**Save everything and refresh browser.**

**What you should see:**

**If using mock data (from Section 3D):**

1. Loading spinner (brief)
2. Empty file list shows
3. Console shows: `Files loaded: {Active Jobs: Array(3)}`

**If not using mock data yet:**

1. Loading spinner (brief)
2. Error shows: "API Error: ..."
3. Console shows error

**Either way, the STATE CHANGES work!** ✅

---

## Adding Mock Data Back (If Needed)

**If you're seeing errors because backend isn't ready, let's add mock data.**

**Open `src/js/api.js` and update `getFiles()`:**

```javascript
export async function getFiles() {
  // TEMPORARY: Return mock data until backend is ready
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
            locked_at: null,
          },
          {
            filename: "1234568_DEF456.mcam",
            size: 1536000,
            modified_at: new Date(Date.now() - 7200000).toISOString(),
            status: "locked",
            locked_by: "john_doe",
            locked_at: new Date(Date.now() - 1800000).toISOString(),
          },
        ],
      });
    }, 1000); // 1 second delay to simulate network
  });
}
```

**Now refresh - you should see data in console!**

---

## Building renderFileCard() - Creating HTML from Data (15 minutes)

**Now let's turn file data into beautiful HTML cards!**

**Add this function to `main.js`:**

```javascript
/**
 * Renders a single file card
 * @param {Object} file - File data object
 * @returns {string} HTML string for the file card
 */
function renderFileCard(file) {
  return `
    <div class="bg-dark-800 rounded-lg p-4 border border-dark-500 mb-4">
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-lg font-semibold text-white">${file.filename}</h3>
        <span class="text-sm px-2 py-1 rounded bg-green-900 text-green-300">
          ${file.status}
        </span>
      </div>
      
      <div class="text-sm text-gray-400 space-y-1">
        <div>Size: ${formatFileSize(file.size)}</div>
        <div>Modified: ${getRelativeTime(file.modified_at)}</div>
      </div>
    </div>
  `;
}
```

**Let me break down EVERY piece...**

---

### The Function Signature

```javascript
function renderFileCard(file) {
```

**`file`** is a parameter - an object with file data:

```javascript
{
  filename: '1234567_ABC123.mcam',
  size: 2048576,
  modified_at: '2025-10-10T14:30:00Z',
  status: 'unlocked',
  locked_by: null
}
```

**This function transforms that object into HTML!**

---

### Template Literals for HTML

```javascript
return `
  <div class="...">
    ...
  </div>
`;
```

**Remember backticks (`) from Section 3C?**

They let us:

1. Write multi-line strings
2. Embed JavaScript expressions with `${}`

**Without template literals (ugly):**

```javascript
return (
  '<div class="bg-dark-800">' + "<h3>" + file.filename + "</h3>" + "</div>"
);
```

**With template literals (clean):**

```javascript
return `
  <div class="bg-dark-800">
    <h3>${file.filename}</h3>
  </div>
`;
```

---

### Using Our Custom Mastercam Colors

```javascript
<div class="bg-dark-800 rounded-lg p-4 border border-dark-500 mb-4">
```

**These are the colors we configured in Section 3A!**

**`bg-dark-800`** - Dark background (from our config)

```javascript
// In tailwind.config.js:
dark: {
  800: '#1a1d29'
}
```

**`border-dark-500`** - Lighter border

```javascript
dark: {
  500: '#4f5469'
}
```

**This is why we set up npm/Tailwind properly!**

---

### Understanding the Card Structure

**Let me break down the HTML structure visually:**

```html
<div class="bg-dark-800 ...">
  ← Card container

  <div class="flex ...">
    ← Header row
    <h3>filename</h3>
    ← Left: filename <span>status</span> ← Right: status badge
  </div>

  <div class="text-sm ...">
    ← Info section
    <div>Size: ...</div>
    ← File size
    <div>Modified: ...</div>
    ← Last modified
  </div>
</div>
```

**Visual layout:**

```
┌─────────────────────────────────────┐
│ filename              [status badge]│ ← flex (space-between)
│                                     │
│ Size: 2 MB                          │
│ Modified: 2 hours ago               │
└─────────────────────────────────────┘
```

---

### Flexbox for Header Layout

```html
<div class="flex items-center justify-between mb-2">
  <h3>...</h3>
  <span>...</span>
</div>
```

**Let me explain each class:**

**`flex`** - Makes this a flex container

```css
display: flex;
```

**`items-center`** - Aligns items vertically centered

```css
align-items: center;
```

**Visual:**

```
Without items-center:
[filename]
           [badge]  ← Not aligned

With items-center:
[filename] [badge]  ← Both centered
```

**`justify-between`** - Spreads items apart

```css
justify-content: space-between;
```

**Visual:**

```
Without justify-between:
[filename][badge]  ← Squished together

With justify-between:
[filename]         [badge]  ← Max space between
```

**`mb-2`** - Margin bottom (spacing below this row)

```css
margin-bottom: 0.5rem;
```

---

### Embedding JavaScript Expressions

```javascript
<h3>${file.filename}</h3>
```

**The `${}` syntax embeds JavaScript!**

**If `file.filename = '1234567_ABC123.mcam'`:**

```javascript
`<h3>${file.filename}</h3>`
    ↓
`<h3>1234567_ABC123.mcam</h3>`
```

**JavaScript runs inside the `${}` and the result is inserted!**

---

### Using Our Utility Functions

```javascript
<div>Size: ${formatFileSize(file.size)}</div>
```

**Remember `formatFileSize` from Section 3B?**

**If `file.size = 2048576`:**

```javascript
formatFileSize(2048576)
    ↓
'2 MB'
    ↓
`<div>Size: 2 MB</div>`
```

**Same with date:**

```javascript
<div>Modified: ${getRelativeTime(file.modified_at)}</div>
```

**If `file.modified_at = '2025-10-10T12:30:00Z'` (2 hours ago):**

```javascript
getRelativeTime('2025-10-10T12:30:00Z')
    ↓
'2 hours ago'
    ↓
`<div>Modified: 2 hours ago</div>`
```

**ALL OUR UTILITY FUNCTIONS ARE WORKING TOGETHER!** 🎉

---

### The Status Badge

```javascript
<span class="text-sm px-2 py-1 rounded bg-green-900 text-green-300">
  ${file.status}
</span>
```

**This creates a colored badge!**

**Classes breakdown:**

**`text-sm`** - Small text (14px)
**`px-2`** - Horizontal padding (left & right)
**`py-1`** - Vertical padding (top & bottom)
**`rounded`** - Rounded corners
**`bg-green-900`** - Dark green background
**`text-green-300`** - Light green text

**Visual result:**

```
┌─────────────┐
│  unlocked   │ ← Small badge with green colors
└─────────────┘
```

---

## Testing renderFileCard()

**Add this test code temporarily:**

```javascript
// TEMPORARY TEST (remove later)
const testFile = {
  filename: "TEST_FILE.mcam",
  size: 2048576,
  modified_at: new Date(Date.now() - 3600000).toISOString(),
  status: "unlocked",
};

const html = renderFileCard(testFile);
console.log("Generated HTML:", html);
```

**Save and check console. You should see the generated HTML!**

**Copy the HTML from console and inspect it - it's valid HTML!**

**Now DELETE the test code.**

---

## Your Progress So Far

**You've built:**

- ✅ State management (show/hide sections)
- ✅ API loading function (loadFiles)
- ✅ Card rendering function (renderFileCard)
- ✅ Error handling (try/catch)
- ✅ All utilities integrated (formatFileSize, getRelativeTime)

**Next up:**

- Loop through files
- Render ALL cards
- Insert into DOM
- See the complete UI!

---

**Ready to continue?** Say **"continue"** and I'll show you how to render ALL files and insert them into the page! 🚀

We're SO CLOSE to seeing the complete, working app!
