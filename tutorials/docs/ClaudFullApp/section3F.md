# Section 3F: Adding Interactivity - Making the App Come Alive! (120+ minutes)

**This is where your app becomes REAL!**

**So far, your app:**

- ✅ Loads and displays files
- ✅ Shows loading states
- ✅ Handles errors
- ❌ Users can't DO anything yet!

**After this section, users will:**

- ✅ Click buttons to checkout files
- ✅ Upload new versions
- ✅ Cancel checkouts
- ✅ See real-time updates
- ✅ Get confirmation dialogs
- ✅ Experience smooth interactions

**Time:** 120+ minutes (this is the BIGGEST section - lots of interactivity!)

---

# Part 1: Understanding Event-Driven Programming (15 minutes)

## How User Interactions Work

**Your app is like a vending machine:**

```
State 1: Idle (showing files)
    ↓
User clicks "Checkout" button
    ↓
Event fires (click event)
    ↓
Event listener runs
    ↓
Call checkoutFile() API
    ↓
Update UI
    ↓
State 2: File is locked
```

**Without events, your app just sits there!**

---

## The Event Loop (Understanding the Foundation)

**JavaScript runs in a single thread but handles many things at once through the EVENT LOOP.**

**Manufacturing analogy:**

**You're a machine operator:**

```
1. Machine running (code executing)
2. Part finishes → Event (machine beeps)
3. You handle it → Event listener
4. Load next part → Action
5. Machine running again
```

**JavaScript:**

```
1. Code running
2. User clicks button → Event
3. Event listener fires → Callback function
4. Perform action → checkoutFile()
5. Code continues
```

---

## Understanding Events and Listeners

**An event is something that HAPPENS:**

- User clicks a button
- User types in input
- Mouse moves over element
- Page finishes loading
- Timer expires

**An event listener WAITS for the event:**

```javascript
button.addEventListener("click", () => {
  console.log("Button was clicked!");
});
```

**Think of it like:**

```
Event = Doorbell rings
Listener = Person waiting to answer door
Callback = What they do when door rings
```

---

## The Pattern We'll Use

**Throughout this section, we'll follow this pattern:**

```javascript
// 1. Get the button element
const button = document.getElementById("checkout-btn");

// 2. Add event listener
button.addEventListener("click", async () => {
  // 3. Get necessary data
  const filename = "part1.mcam";
  const username = "john_doe";

  try {
    // 4. Call API
    await checkoutFile(filename, username);

    // 5. Update UI
    loadFiles(); // Refresh the list
  } catch (error) {
    // 6. Handle errors
    showError(error.message);
  }
});
```

**Simple pattern, repeated for each action!**

---

## 🎥 Understanding Events

**Watch these first:**

- 🎥 [JavaScript Events in 100 Seconds](https://www.youtube.com/watch?v=0tEW kadWPec) (2 min) - Quick overview
- 📺 [Event Listeners Explained](https://www.youtube.com/watch?v=XF1_MlZ5l6M) (10 min) - Complete guide
- 🎬 [JavaScript Event Loop](https://www.youtube.com/watch?v=8aGhZQkoFbQ) (27 min) - How it works internally
- 📚 [MDN: addEventListener](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener) - Reference

---

# Part 2: Adding Buttons to File Cards (20 minutes)

## Current State - Read-Only Cards

**Right now, our file cards just DISPLAY information:**

```html
<div class="bg-dark-800 rounded-lg p-4 border border-dark-500 mb-4">
  <h3>filename.mcam</h3>
  <div>Size: 2 MB</div>
  <div>Modified: 2 hours ago</div>
</div>
```

**We need to ADD BUTTONS so users can interact!**

---

## Designing the Button Layout

**Think about what users need to do:**

**If file is UNLOCKED:**

- ✅ Checkout (lock it for editing)

**If file is LOCKED by someone else:**

- ❌ Can't do anything (show who has it)

**If file is LOCKED by current user:**

- ✅ Check In (upload new version)
- ✅ Cancel Checkout (unlock without uploading)

**Our buttons need to be SMART - show different actions based on file state!**

---

## Understanding File States

**A file can be in THREE states:**

```javascript
// State 1: Unlocked (available)
{
  status: 'unlocked',
  locked_by: null,
  locked_at: null
}

// State 2: Locked by someone else
{
  status: 'locked',
  locked_by: 'john_doe',      // Not the current user
  locked_at: '2025-10-11T10:00:00Z'
}

// State 3: Locked by current user
{
  status: 'locked',
  locked_by: 'current_user',  // The current user
  locked_at: '2025-10-11T10:00:00Z'
}
```

**We need to render DIFFERENT buttons for each state!**

---

## Adding Current User to Our App

**First, we need to track WHO the current user is.**

**Add this at the top of `main.js`, after the imports:**

```javascript
/**
 * Current logged-in user
 * TODO: In production, get this from authentication system
 */
const CURRENT_USER = "john_doe";
```

**Let me explain why we need this...**

---

### Why Track Current User?

**The app needs to know WHO is using it to:**

1. **Show appropriate buttons**

   - If you locked it → show "Check In" and "Cancel"
   - If someone else locked it → show nothing

2. **Send username with API calls**

   - Checkout: "john_doe checked out part1.mcam"
   - Check in: "john_doe checked in part1.mcam"

3. **Display personalized info**
   - "You checked out this file 2 hours ago"
   - vs "Alice checked out this file 2 hours ago"

---

### Production vs Development

**Right now (development):**

```javascript
const CURRENT_USER = "john_doe"; // Hardcoded
```

**In production (with authentication):**

```javascript
// Get from auth system:
const CURRENT_USER = await getCurrentUser();

// Or from session:
const CURRENT_USER = sessionStorage.getItem("username");

// Or from JWT token:
const CURRENT_USER = parseJWT(authToken).username;
```

**For now, hardcoded is fine for learning!**

---

## Building renderFileButtons() - Step by Step

**Add this function to `main.js`:**

```javascript
/**
 * Renders action buttons based on file status
 * @param {Object} file - File data object
 * @returns {string} HTML string for buttons
 */
function renderFileButtons(file) {
  // If file is unlocked, show checkout button
  if (file.status === "unlocked") {
    return `
      <button 
        class="px-4 py-2 bg-mastercam-500 text-white rounded hover:bg-mastercam-600 transition-colors"
        onclick="handleCheckout('${file.filename}')">
        🔓 Checkout
      </button>
    `;
  }

  // If file is locked by current user, show check-in and cancel buttons
  if (file.status === "locked" && file.locked_by === CURRENT_USER) {
    return `
      <div class="flex gap-2">
        <button 
          class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
          onclick="handleCheckin('${file.filename}')">
          ✅ Check In
        </button>
        <button 
          class="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors"
          onclick="handleCancelCheckout('${file.filename}')">
          ❌ Cancel
        </button>
      </div>
    `;
  }

  // If file is locked by someone else, show who has it
  if (file.status === "locked") {
    return `
      <div class="text-sm text-gray-400">
        🔒 Locked by <span class="font-semibold">${file.locked_by}</span>
        <span class="text-xs">(${getRelativeTime(file.locked_at)})</span>
      </div>
    `;
  }

  return "";
}
```

**This has LOTS of new concepts. Let me break down EVERY piece...**

---

### Understanding the if/else Chain

**We have THREE conditions to check:**

```javascript
if (file.status === "unlocked") {
  // Condition 1
}

if (file.status === "locked" && file.locked_by === CURRENT_USER) {
  // Condition 2
}

if (file.status === "locked") {
  // Condition 3
}
```

**Wait, why not if/else if/else?**

**Good question! Let me show you why...**

---

### if vs if/else if Pattern

**Option 1: if/else if/else (connected)**

```javascript
if (condition1) {
  // This runs
} else if (condition2) {
  // OR this runs
} else {
  // OR this runs
}
// Only ONE block runs
```

**Option 2: separate ifs (independent)**

```javascript
if (condition1) {
  // This might run
}

if (condition2) {
  // This might ALSO run
}

if (condition3) {
  // This might ALSO run
}
// Multiple blocks can run!
```

---

**For our case, we WANT early return:**

```javascript
if (file.status === "unlocked") {
  return "..."; // ← Function STOPS here if unlocked
}

// This code only runs if NOT unlocked:
if (file.status === "locked" && file.locked_by === CURRENT_USER) {
  return "..."; // ← Function STOPS here if locked by me
}

// This code only runs if locked by someone else:
if (file.status === "locked") {
  return "..."; // ← Function STOPS here
}
```

**Each `return` EXITS the function immediately!**

---

**Why this pattern is better:**

```javascript
// Our pattern (early returns - clean):
if (unlocked) return buttonA;
if (lockedByMe) return buttonB;
if (lockedByOther) return infoC;

// Alternative (nested else - messy):
if (unlocked) {
  return buttonA;
} else {
  if (lockedByMe) {
    return buttonB;
  } else {
    return infoC;
  }
}
```

**Early returns = flatter code = easier to read!**

---

### Understanding the === Operator

```javascript
file.status === "unlocked";
```

**The `===` is "strict equality" - checks if values are EXACTLY equal.**

**Examples:**

```javascript
5 === 5; // true
5 === "5"; // false (number !== string)
"hello" === "hello"; // true
"hello" === "Hello"; // false (case-sensitive)
null === null; // true
undefined === undefined; // true
```

**vs the == operator (loose equality - avoid this!):**

```javascript
5 == "5"; // true (converts types!)
0 == false; // true (converts!)
"" == false; // true (converts!)
null == undefined; // true (converts!)
```

**Always use `===` for safety!**

---

### The && (AND) Operator

```javascript
file.status === "locked" && file.locked_by === CURRENT_USER;
```

**`&&` means BOTH conditions must be true.**

**Truth table:**

```javascript
true  && true   → true   ✅
true  && false  → false  ❌
false && true   → false  ❌
false && false  → false  ❌
```

**In our case:**

```javascript
// Example 1: File locked by me
file.status = 'locked'            → true
file.locked_by = 'john_doe'       → true (equals CURRENT_USER)
true && true                      → true ✅

// Example 2: File locked by someone else
file.status = 'locked'            → true
file.locked_by = 'alice'          → false (not equal to CURRENT_USER)
true && false                     → false ❌

// Example 3: File unlocked
file.status = 'unlocked'          → false
// && short-circuits, doesn't check second condition
false                             → false ❌
```

---

### Understanding Short-Circuit Evaluation

**`&&` is SMART - it stops as soon as it knows the answer!**

```javascript
false && anythingElse; // Doesn't evaluate "anythingElse"
```

**Why?**

If first condition is FALSE, the result will ALWAYS be FALSE (AND requires both to be true).

**Example:**

```javascript
let called = false;

function checkSomething() {
  called = true;
  return true;
}

false && checkSomething();

console.log(called); // false (function never ran!)
```

**This is called "short-circuit evaluation" - saves work!**

---

### Button HTML Breakdown

**Let's dissect a single button:**

```html
<button
  class="px-4 py-2 bg-mastercam-500 text-white rounded hover:bg-mastercam-600 transition-colors"
  onclick="handleCheckout('${file.filename}')"
>
  🔓 Checkout
</button>
```

---

### Button Tailwind Classes

**`px-4 py-2`** - Padding

```
px-4 = padding-x (left & right) = 1rem (16px)
py-2 = padding-y (top & bottom) = 0.5rem (8px)
```

**Visual:**

```
┌──────────────┐
│ ↕ py-2       │
│ ← px-4 → Text│
│              │
└──────────────┘
```

**`bg-mastercam-500`** - Background color

Our custom Mastercam green! (From Section 3A config)

**`text-white`** - Text color

White text on green background (good contrast)

**`rounded`** - Rounded corners

```css
border-radius: 0.25rem;
```

---

### The hover: Prefix

```html
hover:bg-mastercam-600
```

**This is a Tailwind PSEUDO-CLASS modifier!**

**What it does:**

```css
/* Without hover prefix */
.bg-mastercam-500 {
  background-color: #00a651;
}

/* With hover prefix */
.hover\:bg-mastercam-600:hover {
  background-color: #008c44; /* Darker green */
}
```

**In action:**

```
Normal state:  bg-mastercam-500 (bright green)
Mouse over:    bg-mastercam-600 (darker green)
Mouse leaves:  bg-mastercam-500 (bright green again)
```

**User sees button "light up" when they hover! Great UX!**

---

### The transition-colors Class

```html
transition-colors
```

**What it does:**

```css
.transition-colors {
  transition-property: color, background-color, border-color;
  transition-duration: 150ms;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
```

**Translation:** "Smoothly animate color changes over 150ms"

**Without transition:**

```
Hover → INSTANT color change (jarring)
```

**With transition:**

```
Hover → SMOOTH fade to new color (professional)
```

**Try it:** Remove `transition-colors` and the hover will be INSTANT. Add it back and it's SMOOTH!

---

### The onclick Attribute

```html
onclick="handleCheckout('${file.filename}')"
```

**This is the OLD WAY of handling clicks, but it works well for dynamically generated HTML.**

**What it does:**

When button is clicked, run the JavaScript code in the string.

**Example:**

```javascript
file.filename = "part1.mcam";

// Template literal becomes:
onclick = "handleCheckout('part1.mcam')";

// When clicked, JavaScript runs:
handleCheckout("part1.mcam");
```

---

### Why onclick for Dynamic HTML?

**Two ways to handle clicks:**

**Option 1: addEventListener (best for static elements)**

```javascript
const button = document.getElementById("my-button");
button.addEventListener("click", () => {
  console.log("Clicked!");
});
```

**Problem:** The button must exist when code runs!

```javascript
// This FAILS:
const button = document.getElementById('future-button');  // null!
button.addEventListener('click', ...);  // ERROR!

// Later:
element.innerHTML = '<button id="future-button">Click Me</button>';
// Button exists NOW, but listener was never added!
```

---

**Option 2: onclick attribute (works for dynamic HTML)**

```javascript
element.innerHTML = '<button onclick="handleClick()">Click Me</button>';
// When HTML is inserted, onclick is automatically connected!
```

**That's why we use onclick for buttons we generate with template literals!**

---

### Modern Alternative: Event Delegation

**There's a BETTER way we'll implement later:**

```javascript
// Add ONE listener to parent (that exists at page load)
elements.fileList.addEventListener('click', (event) => {
  // Check what was clicked
  if (event.target.matches('.checkout-btn')) {
    handleCheckout(...);
  }
});
```

**Benefits:**

- One listener instead of hundreds
- Works with dynamic content
- Better performance

**For now, onclick is simpler to learn!**

---

### The Flex Container for Multiple Buttons

```html
<div class="flex gap-2">
  <button>Check In</button>
  <button>Cancel</button>
</div>
```

**`flex`** - Makes this a flex container (side-by-side layout)

**`gap-2`** - Space between buttons

```css
gap: 0.5rem; /* 8px space between items */
```

**Visual:**

```
Without gap:
[Button1][Button2]  ← Touching

With gap-2:
[Button1]  [Button2]  ← Nice space
```

---

### Using Emojis in Buttons

```html
🔓 Checkout ✅ Check In ❌ Cancel 🔒 Locked
```

**Why emojis?**

1. **Visual indicators** - Instant recognition
2. **No icon library needed** - Just use Unicode
3. **Accessible** - Screen readers read them
4. **Fun** - Makes UI friendly

**Alternatives:**

```html
<!-- Icon library (more work) -->
<i class="fas fa-lock"></i> Checkout

<!-- SVG icons (more control) -->
<svg>...</svg> Checkout

<!-- Text only (boring) -->
Checkout
```

**For our tutorial, emojis are perfect!**

---

## Updating renderFileCard() to Include Buttons

**Now update the `renderFileCard()` function to use our new button function:**

```javascript
function renderFileCard(file) {
  return `
    <div class="bg-dark-800 rounded-lg p-4 border border-dark-500 mb-4">
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-lg font-semibold text-white">${file.filename}</h3>
        <span class="text-sm px-2 py-1 rounded ${
          file.status === "locked"
            ? "bg-red-900 text-red-300"
            : "bg-green-900 text-green-300"
        }">
          ${file.status}
        </span>
      </div>
      
      <div class="text-sm text-gray-400 space-y-1 mb-3">
        <div>Size: ${formatFileSize(file.size)}</div>
        <div>Modified: ${getRelativeTime(file.modified_at)}</div>
      </div>
      
      ${renderFileButtons(file)}
    </div>
  `;
}
```

**Changes:**

1. Added `mb-3` to info section (margin bottom for spacing)
2. Called `${renderFileButtons(file)}` to insert buttons
3. Made status badge color dynamic (green for unlocked, red for locked)

---

### Understanding the Ternary Operator

```javascript
${file.status === 'locked' ? 'bg-red-900 text-red-300' : 'bg-green-900 text-green-300'}
```

**This is a TERNARY OPERATOR - a shorthand if/else!**

**Syntax:**

```javascript
condition ? valueIfTrue : valueIfFalse;
```

**Examples:**

```javascript
const age = 20;
const canDrink = age >= 21 ? "Yes" : "No";
// canDrink = 'No'

const score = 85;
const grade = score >= 90 ? "A" : "B";
// grade = 'B'

const isLoggedIn = true;
const message = isLoggedIn ? "Welcome back!" : "Please log in";
// message = 'Welcome back!'
```

---

**Breaking down our usage:**

```javascript
file.status === "locked"
  ? "bg-red-900 text-red-300" // If locked (true)
  : "bg-green-900 text-green-300"; // If unlocked (false)
```

**If file is locked:**

```html
<span class="... bg-red-900 text-red-300">locked</span>
```

**If file is unlocked:**

```html
<span class="... bg-green-900 text-green-300">unlocked</span>
```

**Visual:**

```
Locked:   [🔴 locked]   (red badge)
Unlocked: [🟢 unlocked] (green badge)
```

---

### Long Form vs Ternary

**Without ternary (verbose):**

```javascript
let classes;
if (file.status === "locked") {
  classes = "bg-red-900 text-red-300";
} else {
  classes = "bg-green-900 text-green-300";
}
return `<span class="${classes}">${file.status}</span>`;
```

**With ternary (concise):**

```javascript
return `<span class="${
  file.status === "locked"
    ? "bg-red-900 text-red-300"
    : "bg-green-900 text-green-300"
}">${file.status}</span>`;
```

**Both work the same! Ternary is shorter for simple conditions.**

---

## Testing the Updated Cards

**Save and refresh your browser!**

**You should now see:**

1. File cards with BUTTONS! 🎉
2. Different buttons based on file status
3. Green "Checkout" button for unlocked files
4. Green "Check In" and gray "Cancel" buttons for files locked by you
5. Info message for files locked by others

**Click a button...**

**You'll see an error in console:**

```
Uncaught ReferenceError: handleCheckout is not defined
```

**That's expected! We haven't created the handler functions yet!**

**That's next... 🚀**

---

# Part 3: Implementing Click Handlers (30 minutes)

## Understanding Global Functions

**Our onclick attributes call functions:**

```html
onclick="handleCheckout('part1.mcam')"
```

**These functions must be GLOBAL (accessible from HTML).**

**Why?**

---

### Module Scope vs Global Scope

**Our code is in a MODULE:**

```html
<script type="module" src="main.js"></script>
```

**Modules have their own scope:**

```javascript
// main.js
function handleCheckout(filename) {
  console.log("Checkout:", filename);
}

// This function is NOT global!
// It's only available inside main.js module
```

**HTML can't see it:**

```html
<button onclick="handleCheckout('part1.mcam')">
  <!-- ERROR: handleCheckout is not defined -->
</button>
```

---

### Making Functions Global

**Option 1: Attach to window (quick fix)**

```javascript
window.handleCheckout = function (filename) {
  console.log("Checkout:", filename);
};

// Now HTML can see it!
```

**Option 2: Event delegation (better, we'll do later)**

**For now, we'll use Option 1 to get things working quickly!**

---

## Building handleCheckout() - Version 1

**Add this function to `main.js`:**

```javascript
/**
 * Handles checkout button click
 * @param {string} filename - Name of file to checkout
 */
async function handleCheckout(filename) {
  console.log("Checkout clicked:", filename);

  try {
    // Show loading state (we'll improve this later)
    showLoading();

    // Call API to checkout file
    await checkoutFile(filename, CURRENT_USER);

    // Success! Reload files to show updated state
    await loadFiles();
  } catch (error) {
    // Show error to user
    showError(`Failed to checkout ${filename}: ${error.message}`);
  }
}

// Make it globally accessible
window.handleCheckout = handleCheckout;
```

**Let me explain EVERY piece...**

---

### The async Keyword (Review)

```javascript
async function handleCheckout(filename) {
```

**Why async?**

Because we use `await` inside!

```javascript
await checkoutFile(...)  // ← Pauses here
await loadFiles()        // ← And here
```

**Without async:**

```javascript
function handleCheckout(filename) {
  await checkoutFile(...);  // ❌ ERROR!
  // Can't use await in non-async function
}
```

---

### The Function Parameter

```javascript
async function handleCheckout(filename) {
  // filename comes from onclick attribute
}
```

**Remember the onclick:**

```html
onclick="handleCheckout('part1.mcam')" ↓ When clicked, calls:
handleCheckout('part1.mcam') ↓ Parameter receives: filename = 'part1.mcam'
```

---

### Why Show Loading State?

```javascript
showLoading();
```

**Think about the user experience:**

**Without loading state:**

```
User clicks "Checkout"
(nothing happens...)
(user confused...)
(2 seconds later...)
File suddenly changes to locked
```

**With loading state:**

```
User clicks "Checkout"
→ Shows loading spinner immediately
→ User knows something is happening
→ File updates when ready
```

**Always give instant feedback!**

---

### The API Call

```javascript
await checkoutFile(filename, CURRENT_USER);
```

**Remember this function from Section 3D:**

```javascript
// In api.js:
export async function checkoutFile(filename, username) {
  return apiFetch("/checkout", {
    method: "POST",
    body: JSON.stringify({ filename, username }),
  });
}
```

**What happens:**

1. Sends HTTP POST to `/checkout`
2. Server locks the file
3. Server responds with success or error
4. If success, function returns
5. If error, throws exception (caught by our try/catch)

---

### Reloading Files After Success

```javascript
await loadFiles();
```

**Why reload?**

**The file state changed on the server!**

```
Before checkout:
{
  filename: 'part1.mcam',
  status: 'unlocked',
  locked_by: null
}

After checkout:
{
  filename: 'part1.mcam',
  status: 'locked',
  locked_by: 'john_doe',
  locked_at: '2025-10-11T14:30:00Z'
}
```

**Our UI needs to reflect the new state:**

- Status badge changes to red "locked"
- Checkout button disappears
- Check In and Cancel buttons appear

**Reloading fetches the updated data and re-renders!**

---

### Making the Function Global

```javascript
window.handleCheckout = handleCheckout;
```

**What is `window`?**

**The global object in browsers!**

Everything attached to `window` is globally accessible.

**Examples:**

```javascript
window.alert("Hello"); // alert() is on window
window.console.log("Hi"); // console is on window
window.document.body; // document is on window

// When you write:
alert("Hello");
// JavaScript looks for: window.alert('Hello');
```

---

**By attaching our function:**

```javascript
window.handleCheckout = handleCheckout;
```

**We make it global:**

```javascript
// Before:
handleCheckout("part1.mcam"); // Only works inside this module

// After:
window.handleCheckout("part1.mcam"); // Works anywhere!
handleCheckout("part1.mcam"); // Also works (window is implicit)
```

**Now HTML can call it!**

---

## Testing handleCheckout()

**Save and refresh browser.**

**Click a "Checkout" button!**

**You should see:**

1. Loading spinner shows
2. Brief pause
3. File list reloads
4. File is now LOCKED
5. Buttons changed to "Check In" and "Cancel"

**Check the console - should see:**

```
Checkout clicked: part1.mcam
```

**IT WORKS!** 🎉

---

## Building handleCancelCheckout()

**Add this function:**

```javascript
/**
 * Handles cancel checkout button click
 * @param {string} filename - Name of file to cancel checkout
 */
async function handleCancelCheckout(filename) {
  // Ask for confirmation
  const confirmed = confirm(
    `Cancel checkout of ${filename}?\n\nAny local changes will be lost.`
  );

  if (!confirmed) {
    return; // User clicked "Cancel", do nothing
  }

  try {
    showLoading();

    await cancelCheckout(filename, CURRENT_USER);

    await loadFiles();
  } catch (error) {
    showError(`Failed to cancel checkout: ${error.message}`);
  }
}

window.handleCancelCheckout = handleCancelCheckout;
```

**New concept: confirmation dialogs!**

---

### Understanding confirm()

```javascript
const confirmed = confirm("Are you sure?");
```

**What is `confirm()`?**

A built-in browser function that shows a dialog with OK/Cancel buttons.

**What it returns:**

```javascript
User clicks OK:     confirmed = true
User clicks Cancel: confirmed = false
```

**Example:**

```javascript
const confirmed = confirm("Delete this file?");

if (confirmed) {
  console.log("User said yes");
} else {
  console.log("User said no");
}
```

---

### Why Confirmation for Cancel?

**Think about the consequences:**

**Without confirmation:**

```
User clicks "Cancel" by mistake
File is unlocked
Their local changes are orphaned
No way to get file back
😭 User is upset
```

**With confirmation:**

```
User clicks "Cancel"
→ "Are you sure?" dialog
→ User can back out
→ Only proceeds if they confirm
😊 User feels safe
```

**Confirmation for DESTRUCTIVE actions!**

---

### Multi-Line Strings in confirm()

```javascript
confirm(`Cancel checkout of ${filename}?\n\nAny local changes will be lost.`);
```

**`\n` means "newline" (line break):**

```javascript
"Line 1\nLine 2";
// Shows:
// Line 1
// Line 2

"Line 1\n\nLine 3"; // Two \n = blank line
// Shows:
// Line 1
//
// Line 3
```

**Our dialog shows:**

```
Cancel checkout of part1.mcam?

Any local changes will be lost.

[OK] [Cancel]
```

---

### Early Return Pattern

```javascript
if (!confirmed) {
  return;
}

// Rest of code only runs if confirmed is true
```

**This is the "guard clause" pattern!**

**Check for reasons to STOP early, then continue with main logic.**

**Without early return (nested):**

```javascript
if (confirmed) {
  try {
    showLoading();
    await cancelCheckout(...);
    await loadFiles();
  } catch (error) {
    showError(...);
  }
}
```

**With early return (flatter):**

```javascript
if (!confirmed) return;

try {
  showLoading();
  await cancelCheckout(...);
  await loadFiles();
} catch (error) {
  showError(...);
}
```

**Second version is easier to read!**

---

## Testing handleCancelCheckout()

**Save and refresh.**

**To test:**

1. Checkout a file (it becomes locked)
2. Click "Cancel" button
3. Confirmation dialog appears!
4. Click "Cancel" on dialog → nothing happens ✅
5. Click "Cancel" button again
6. Click "OK" on dialog → file unlocks ✅

**Perfect!**

---

## Building handleCheckin() - The Complex One (25 minutes)

**Check-in is MORE COMPLEX because it needs to:**

1. Ask user for a file to upload
2. Ask for a commit message
3. Upload the file
4. Update the UI

**This is the most realistic, production-like handler!**

---

### The File Upload Flow

```
User clicks "Check In"
    ↓
Show file picker dialog
    ↓
User selects a file
    ↓
Ask for commit message
    ↓
User enters message
    ↓
Upload file + message to server
    ↓
Server processes
    ↓
Success! Update UI
```

**Let's build it step by step...**

---

## Version 1: Basic Structure

**Add this function:**

```javascript
/**
 * Handles check-in button click
 * @param {string} filename - Name of file to check in
 */
async function handleCheckin(filename) {
  console.log("Check-in clicked:", filename);

  try {
    // Step 1: Get file from user
    const file = await selectFile();
    if (!file) return; // User cancelled

    // Step 2: Get commit message
    const message = prompt("Enter a description of your changes:");
    if (!message) return; // User cancelled

    // Step 3: Upload
    showLoading();
    await checkinFile(filename, file, message);

    // Step 4: Success!
    await loadFiles();
  } catch (error) {
    showError(`Failed to check in: ${error.message}`);
  }
}

window.handleCheckin = handleCheckin;
```

**Now we need to build the `selectFile()` function...**

---

## Building selectFile() Helper Function

**Add this function BEFORE handleCheckin:**

```javascript
/**
 * Opens file picker and returns selected file
 * @returns {Promise<File|null>} Selected file or null if cancelled
 */
function selectFile() {
  return new Promise((resolve) => {
    // Create a hidden file input
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".mcam,.MCam"; // Only Mastercam files

    // When user selects a file
    input.addEventListener("change", () => {
      const file = input.files[0];
      resolve(file || null);
    });

    // When user cancels
    input.addEventListener("cancel", () => {
      resolve(null);
    });

    // Trigger the file picker
    input.click();
  });
}
```

**This has LOTS of new concepts! Let me explain thoroughly...**

---

### Understanding Promises (Deep Review)

```javascript
return new Promise((resolve) => {
  // Code that takes time
  resolve(result); // When done, call resolve with result
});
```

**Why use Promise here?**

**File selection is ASYNCHRONOUS - we don't know when user will pick a file!**

```
Call selectFile()
    ↓
File dialog opens
    ↓
(User thinking... 5 seconds)
    ↓
User selects file
    ↓
Function can continue
```

**Promise lets us `await` for user's action!**

---

### Creating an Input Element Dynamically

```javascript
const input = document.createElement("input");
```

**What does this do?**

Creates a NEW `<input>` element in JavaScript (not in HTML yet).

**It's like:**

```javascript
// This JavaScript:
const input = document.createElement('input');

// Creates this (in memory):
<input>
```

**The element exists but isn't visible yet!**

---

### Setting Element Properties

```javascript
input.type = "file";
input.accept = ".mcam,.MCam";
```

**This sets HTML attributes:**

```javascript
// After setting properties:
<input type="file" accept=".mcam,.MCam">
```

**`type="file"`** - Makes it a file picker

**`accept=".mcam,.MCam"`** - Only shows .mcam files in dialog

**Why .MCam with capital M?**
Some systems are case-sensitive! This covers both.

---

### Adding Event Listeners to Dynamic Elements

```javascript
input.addEventListener("change", () => {
  const file = input.files[0];
  resolve(file || null);
});
```

**The 'change' event fires when user selects a file.**

**`input.files`** is a FileList (array-like) of selected files.

**`input.files[0]`** gets the first (and only) file.

---

### Understanding the File Object

**When user selects a file, we get a File object:**

```javascript
File {
  name: 'part1.mcam',
  size: 2048576,
  type: 'application/octet-stream',
  lastModified: 1697040000000,
  // And more...
}
```

**This is a REAL file object that we can upload!**

---

### The || (OR) Operator for Default Values

```javascript
resolve(file || null);
```

**Why use `||`?**

**If `input.files[0]` is undefined (no file selected), use `null` instead.**

**Examples:**

```javascript
const value = someVar || 'default';

// If someVar is:
someVar = 'hello'      → value = 'hello'
someVar = undefined    → value = 'default'
someVar = null         → value = 'default'
someVar = ''           → value = 'default'
someVar = 0            → value = 'default'
```

**It uses the first "truthy" value!**

---

### Triggering the File Picker

```javascript
input.click();
```

**This simulates a click on the input, opening the file dialog!**

**Visual flow:**

```javascript
const input = document.createElement('input');  // Create
input.type = 'file';                            // Configure
input.addEventListener('change', ...);          // Set up listener
input.click();                                  // Open dialog!
```

**User sees the system file picker open!**

---

### Why Not Add Input to DOM?

**You might wonder:** "Why not append the input to the page?"

**We could:**

```javascript
document.body.appendChild(input);
input.click();
```

**But we don't need to!**

- `input.click()` works without appending
- Keeps DOM clean
- No need to remove it later

**Cleaner this way!**

---

## Understanding prompt() for Commit Message

```javascript
const message = prompt("Enter a description of your changes:");
```

**`prompt()` shows a dialog with a text input:**

```
┌─────────────────────────────────────┐
│ Enter a description of your changes │
│                                     │
│ [________________]                  │
│                                     │
│        [OK]  [Cancel]               │
└─────────────────────────────────────┘
```

**Returns:**

- String of what user typed (if clicked OK)
- null (if clicked Cancel)

---

### Checking if User Cancelled

```javascript
if (!message) return;
```

**Why this works:**

```javascript
// User clicked OK and entered text:
message = 'Fixed bug in calculation'
!message = false
if (false) → Code doesn't run ✅

// User clicked OK but entered nothing:
message = ''
!message = true (empty string is falsy)
if (true) → Return ✅ (we want commit message!)

// User clicked Cancel:
message = null
!message = true
if (true) → Return ✅
```

**Guards against both cancel AND empty input!**

---

## Testing handleCheckin()

**Save and refresh!**

**Test the flow:**

1. Checkout a file first (so you can check it in)
2. Click "Check In" button
3. File picker opens!
4. Select a file (any file for testing)
5. Prompt appears for commit message
6. Enter "Test checkin"
7. Loading spinner shows
8. File becomes unlocked again!

**FULL WORKFLOW WORKING!** 🎉🎉🎉

---

## 🎥 Understanding File Uploads and Promises

**Watch these:**

- 🎥 [JavaScript Promises in 100 Seconds](https://www.youtube.com/watch?v=RvYYCGs45L4) (2 min) - Quick review
- 📺 [File Upload in JavaScript](https://www.youtube.com/watch?v=hnCmSXCZEpU) (15 min) - File API
- 🎬 [Understanding Promises](https://www.youtube.com/watch?v=DHvZLI7Db8E) (18 min) - Deep dive
- 📚 [MDN: File API](https://developer.mozilla.org/en-US/docs/Web/API/File) - Reference
- 📚 [MDN: Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) - Reference

---

**Your progress is AMAZING! We have:**
✅ File display with state-based buttons
✅ Checkout functionality
✅ Cancel checkout with confirmation
✅ Check-in with file upload and commit message
✅ Full error handling
✅ Loading states

**Next up: Improving UX with loading indicators, better error messages, and polish!**

**Ready to continue?** Say **"continue"** and we'll add the finishing touches! 🎨
