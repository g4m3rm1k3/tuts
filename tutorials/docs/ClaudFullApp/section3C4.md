# Part 4: Building getRelativeTime() (35 minutes)

**Goal:** Build a function that converts dates into human-friendly relative phrases like "2 hours ago" or "just now".

**What You'll Learn:**

- How to calculate time differences
- Converting milliseconds to seconds/minutes/hours
- The `Object.entries()` method
- Array destructuring in loops
- How to build dynamic text

---

## Understanding Relative Time (5 minutes)

### What Is Relative Time?

**Relative time = "How long ago did this happen?"**

**Example scenario:**
Your coworker locked a file at 1:45 PM. It's now 3:45 PM.

**Two ways to show this:**

**Absolute time (what formatDate gives you):**

```
Locked: Oct 10, 2025, 1:45 PM
```

**Relative time (what we're building now):**

```
Locked: 2 hours ago
```

**Which is more useful?**

For **recent events**, relative time is better:

- "2 hours ago" is easier to understand than "1:45 PM"
- Gives immediate sense of recency
- Matches how humans think ("How long has this been locked?")

For **old events**, absolute time is better:

- "Jan 15, 2024" is clearer than "278 days ago"
- Easier to remember specific dates

**Our app will use both!**

- File list: "Modified 2 hours ago" (relative)
- File details: "Modified Oct 10, 2025, 1:45 PM" (absolute)

---

### Real-World Examples

**Social media:**

```
Posted just now
Posted 5 minutes ago
Posted 2 hours ago
Posted yesterday
Posted last week
```

**Email clients:**

```
Received 3 minutes ago
Received 1 hour ago
Received yesterday
Received Oct 10
```

**Your PDM system:**

```
File locked just now
File locked 30 minutes ago
File locked 2 hours ago
File locked yesterday
File locked 3 weeks ago
```

---

## Understanding Time Differences (10 minutes)

### The Core Concept

**To calculate "how long ago", we need to subtract two times:**

```
Now - Then = Time difference
```

**Example:**

```
Now:  3:45 PM (current time)
Then: 1:45 PM (when file was locked)
Difference: 2 hours
```

**But computers don't subtract "3:45 PM" directly. Remember: they work with milliseconds since 1970!**

---

### How JavaScript Subtracts Dates

**Let me show you step by step:**

```javascript
const now = new Date(); // Right now: 3:45 PM
const past = new Date(); // Some time in the past: 1:45 PM
past.setHours(past.getHours() - 2); // Go back 2 hours

const diff = now - past;
console.log(diff);
```

**What happens when you subtract dates:**

```
Step 1: JavaScript converts both dates to milliseconds

now = 1728583500000  (3:45 PM in milliseconds)
past = 1728576300000 (1:45 PM in milliseconds)

Step 2: Subtract the numbers

1728583500000 - 1728576300000 = 7200000

Step 3: The result is in milliseconds

7200000 milliseconds = difference
```

**That's 7,200,000 milliseconds!**

But what does that mean in human terms?

---

### Converting Milliseconds to Human Time

**Let me break down 7,200,000 milliseconds:**

```
7,200,000 milliseconds
    ↓ ÷ 1,000 (milliseconds per second)
7,200 seconds
    ↓ ÷ 60 (seconds per minute)
120 minutes
    ↓ ÷ 60 (minutes per hour)
2 hours
```

**So 7,200,000 milliseconds = 2 hours!**

**The conversion factors you need to memorize:**

```
1 second  = 1,000 milliseconds
1 minute  = 60 seconds = 60,000 milliseconds
1 hour    = 60 minutes = 3,600 seconds = 3,600,000 milliseconds
1 day     = 24 hours = 86,400 seconds = 86,400,000 milliseconds
```

---

### 🎥 Understanding Time Math

**Watch these before building the function:**

- 🎥 [JavaScript Date Math](https://www.youtube.com/watch?v=zwRdO9_GGhY) (6 min) - Calculating differences
- 🎥 [Working with Timestamps](https://www.youtube.com/watch?v=zwRdO9_GGhY) (8 min) - Time calculations
- 📚 [MDN: Date arithmetic](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date#date_time_string_format) - Reference

---

### Practice: Calculate a Time Difference

**Try this in your console:**

```javascript
// Create a date 5 minutes ago
const now = new Date();
const fiveMinutesAgo = new Date(Date.now() - 300000);
// 300000 = 5 minutes in milliseconds (5 × 60 × 1000)

// Calculate difference
const diffMs = now - fiveMinutesAgo;
console.log("Difference in milliseconds:", diffMs); // ~300000

// Convert to seconds
const diffSeconds = diffMs / 1000;
console.log("Difference in seconds:", diffSeconds); // ~300

// Convert to minutes
const diffMinutes = diffSeconds / 60;
console.log("Difference in minutes:", diffMinutes); // ~5
```

**You just calculated "5 minutes ago"!**

---

## Building getRelativeTime() - Version 1 (10 minutes)

### Step 1: Start Simple - Just Seconds

**Add to `formatting.js`:**

```javascript
/**
 * Gets relative time string (e.g., "2 hours ago")
 * Version 1: Only handles seconds
 */
export function getRelativeTime(date) {
  // Handle string dates
  if (typeof date === "string") {
    date = new Date(date);
  }

  // Get current time
  const now = new Date();

  // Calculate difference in milliseconds
  const diffMs = now - date;

  // Convert to seconds
  const seconds = Math.floor(diffMs / 1000);

  return seconds + " seconds ago";
}
```

---

### Understanding Each Line

**Line 1: Handle string input**

```javascript
if (typeof date === "string") {
  date = new Date(date);
}
```

Same pattern as formatDate - convert strings to Date objects.

---

**Line 2: Get current time**

```javascript
const now = new Date();
```

Creates a Date object for RIGHT NOW. This is our reference point.

---

**Line 3: Calculate difference**

```javascript
const diffMs = now - date;
```

**What happens here:**

```javascript
// Say now = Oct 10, 2025, 3:45 PM
// And date = Oct 10, 2025, 3:43 PM

// JavaScript converts to milliseconds:
now = 1728583500000
date = 1728583380000

// Subtract:
diffMs = 1728583500000 - 1728583380000
diffMs = 120000  (120,000 milliseconds)
```

**The variable `diffMs` = difference in milliseconds**

---

**Line 4: Convert to seconds**

```javascript
const seconds = Math.floor(diffMs / 1000);
```

**Breaking this down:**

### `diffMs / 1000`

- Divides milliseconds by 1,000
- Gives us seconds as a decimal

**Example:**

```javascript
120000 / 1000 = 120.0 seconds
```

### `Math.floor()`

- Rounds DOWN to nearest whole number
- Removes any decimal places

**Why Math.floor?**

```javascript
// 5432 milliseconds
5432 / 1000 = 5.432 seconds

Math.floor(5.432) = 5 seconds
```

We don't say "5.432 seconds ago" - we say "5 seconds ago"!

**Other rounding methods:**

```javascript
Math.floor(5.7); // 5 (always rounds DOWN)
Math.ceil(5.1); // 6 (always rounds UP)
Math.round(5.5); // 6 (rounds to nearest)
```

**Why floor instead of round?**

- "5.9 seconds ago" is closer to "5 seconds" than "6 seconds"
- It JUST happened, so show the smaller number
- Conservative estimate (under-promise, over-deliver)

---

**Line 5: Return the result**

```javascript
return seconds + " seconds ago";
```

Joins the number with the text " seconds ago".

**Examples:**

```javascript
5 + ' seconds ago'   →  '5 seconds ago'
30 + ' seconds ago'  →  '30 seconds ago'
```

---

### Test Version 1

**Update your test file:**

```javascript
import { getRelativeTime } from "./js/utils/formatting.js";

const testTimes = [
  new Date(Date.now() - 5000), // 5 seconds ago
  new Date(Date.now() - 30000), // 30 seconds ago
  new Date(Date.now() - 90000), // 90 seconds ago
  new Date(Date.now() - 300000), // 5 minutes (300 seconds)
];

const output = document.getElementById("output");

testTimes.forEach((time) => {
  const result = getRelativeTime(time);
  output.innerHTML += `<p>${result}</p>`;
});
```

**Output:**

```
5 seconds ago
30 seconds ago
90 seconds ago
300 seconds ago
```

**It works!** But we have problems:

- "90 seconds ago" should be "1 minute ago"
- "300 seconds ago" should be "5 minutes ago"

**Let's fix it!**

---

## Version 2: Adding Minutes and Hours (10 minutes)

### The Strategy

**We need to check which unit makes the most sense:**

```
0-59 seconds     →  "just now"
60-3599 seconds  →  "X minutes ago"
3600+ seconds    →  "X hours ago"
```

**Why "just now" for < 60 seconds?**

- More natural than "30 seconds ago"
- Common pattern in apps
- Users understand it immediately

---

### Update the Function

```javascript
/**
 * Gets relative time string
 * Version 2: Handles seconds, minutes, hours
 */
export function getRelativeTime(date) {
  // Handle string dates
  if (typeof date === "string") {
    date = new Date(date);
  }

  const now = new Date();
  const diffMs = now - date;
  const seconds = Math.floor(diffMs / 1000);

  // Less than 1 minute → "just now"
  if (seconds < 60) {
    return "just now";
  }

  // Calculate minutes
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) {
    return minutes + " minute" + (minutes > 1 ? "s" : "") + " ago";
  }

  // Calculate hours
  const hours = Math.floor(minutes / 60);
  if (hours < 24) {
    return hours + " hour" + (hours > 1 ? "s" : "") + " ago";
  }

  return "more than a day ago";
}
```

---

### Understanding the New Logic

**Check 1: Just now**

```javascript
if (seconds < 60) {
  return "just now";
}
```

**If less than 60 seconds, return immediately.**

**Why 60 as the cutoff?**

- 60 seconds = 1 minute
- Anything less than a minute is "just now"
- Standard pattern in apps

---

**Check 2: Calculate minutes**

```javascript
const minutes = Math.floor(seconds / 60);
```

**Let's trace through an example:**

```javascript
// Say we have 185 seconds
seconds = 185;

// Convert to minutes
minutes = Math.floor(185 / 60);
minutes = Math.floor(3.083);
minutes = 3;
```

**Visual breakdown:**

```
185 seconds
    ↓ ÷ 60 (seconds per minute)
3.083 minutes
    ↓ Math.floor() (round down)
3 minutes
```

**Why divide by 60?**
Because there are 60 seconds in a minute!

---

**Check 3: Return minutes if less than 60**

```javascript
if (minutes < 60) {
  return minutes + " minute" + (minutes > 1 ? "s" : "") + " ago";
}
```

**Let me break down that plural logic:**

```javascript
minutes > 1 ? "s" : "";
```

**This is a ternary operator (conditional expression).**

**Format:** `condition ? valueIfTrue : valueIfFalse`

**Examples:**

**If minutes = 1:**

```javascript
(1 > 1 ? "s" : "")(false ? "s" : "");
(""); // empty string (no 's')
// Result: "1 minute ago" ✅
```

**If minutes = 3:**

```javascript
(3 > 1 ? "s" : "")(true ? "s" : "");
("s"); // the letter s
// Result: "3 minutes ago" ✅
```

**If minutes = 0:**

```javascript
(0 > 1 ? "s" : "")(false ? "s" : "");
(""); // empty string
// Result: "0 minute ago" (but we won't hit this because of the seconds check)
```

**It automatically handles singular vs plural!**

---

### 🎥 Understanding Ternary Operators

**Watch this quick explainer:**

- 🎥 [Ternary Operator Explained](https://www.youtube.com/watch?v=s4sB1hm73tw) (4 min) - Simple guide
- 📚 [MDN: Conditional operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Conditional_Operator) - Reference

---

**Check 4: Calculate hours**

```javascript
const hours = Math.floor(minutes / 60);
```

**Same pattern as minutes!**

**Example:**

```javascript
// Say we have 185 minutes
minutes = 185;

// Convert to hours
hours = Math.floor(185 / 60);
hours = Math.floor(3.083);
hours = 3;
```

**Why divide by 60?**
Because there are 60 minutes in an hour!

---

**Check 5: Return hours if less than 24**

```javascript
if (hours < 24) {
  return hours + " hour" + (hours > 1 ? "s" : "") + " ago";
}
```

Same plural logic as minutes!

**Why 24 as the cutoff?**
Because there are 24 hours in a day!

---

**Final fallback:**

```javascript
return "more than a day ago";
```

If none of the conditions matched, it must be more than 24 hours (1 day) old.

---

### Test Version 2

```javascript
const testTimes = [
  new Date(Date.now() - 30000), // 30 seconds → "just now"
  new Date(Date.now() - 120000), // 2 minutes → "2 minutes ago"
  new Date(Date.now() - 3600000), // 1 hour → "1 hour ago"
  new Date(Date.now() - 7200000), // 2 hours → "2 hours ago"
  new Date(Date.now() - 90000000), // 25 hours → "more than a day ago"
];

testTimes.forEach((time) => {
  console.log(getRelativeTime(time));
});
```

**Output:**

```
just now
2 minutes ago
1 hour ago
2 hours ago
more than a day ago
```

**Much better!** But "more than a day ago" isn't very specific.

Let's add days, weeks, months, and years!

---

## Version 3: All Time Units (FINAL) (15 minutes)

### The Challenge

**Instead of checking each unit with if/else statements, we'll use a smarter approach:**

We'll create an **object of intervals** and loop through them!

---

### Understanding the Intervals Object

**First, let me show you the complete function, then explain each part:**

```javascript
/**
 * Gets relative time string (e.g., "2 hours ago")
 * FINAL VERSION: All time units
 *
 * @param {Date|string} date - Date to compare
 * @returns {string} Relative time like "2 hours ago" or "just now"
 *
 * @example
 * getRelativeTime(new Date())  // "just now"
 * getRelativeTime(new Date(Date.now() - 3600000))  // "1 hour ago"
 */
export function getRelativeTime(date) {
  // Handle string dates
  if (typeof date === "string") {
    date = new Date(date);
  }

  // Validate
  if (!(date instanceof Date) || isNaN(date)) {
    return "Invalid date";
  }

  const now = new Date();
  const diffMs = now - date;
  const seconds = Math.floor(diffMs / 1000);

  // Future dates (edge case)
  if (seconds < 0) {
    return "in the future";
  }

  // Just now (< 1 minute)
  if (seconds < 60) {
    return "just now";
  }

  // Define all time intervals in seconds
  const intervals = {
    year: 31536000,
    month: 2592000,
    week: 604800,
    day: 86400,
    hour: 3600,
    minute: 60,
  };

  // Loop through intervals from largest to smallest
  for (const [unit, secondsInUnit] of Object.entries(intervals)) {
    const interval = Math.floor(seconds / secondsInUnit);

    if (interval >= 1) {
      return `${interval} ${unit}${interval > 1 ? "s" : ""} ago`;
    }
  }

  return "just now";
}
```

**Now let me break down the new parts...**

---

### Understanding the Intervals Object

```javascript
const intervals = {
  year: 31536000,
  month: 2592000,
  week: 604800,
  day: 86400,
  hour: 3600,
  minute: 60,
};
```

**This object maps time units to seconds.**

**Let me show you how each number is calculated:**

---

### `minute: 60`

**1 minute = 60 seconds**

Simple!

---

### `hour: 3600`

**1 hour = 60 minutes**

**Calculation:**

```
60 minutes × 60 seconds = 3,600 seconds
```

---

### `day: 86400`

**1 day = 24 hours**

**Calculation:**

```
24 hours × 60 minutes × 60 seconds
= 24 × 3,600
= 86,400 seconds
```

**Manufacturing analogy:**

- A shop works 24 hours/day
- That's 24 × 60 = 1,440 minutes
- Or 86,400 seconds

---

### `week: 604800`

**1 week = 7 days**

**Calculation:**

```
7 days × 24 hours × 60 minutes × 60 seconds
= 7 × 86,400
= 604,800 seconds
```

---

### `month: 2592000`

**1 month ≈ 30 days**

**Calculation:**

```
30 days × 24 hours × 60 minutes × 60 seconds
= 30 × 86,400
= 2,592,000 seconds
```

**Why 30 days?**

- Months vary (28-31 days)
- We use 30 as an average
- Good enough for "X months ago" display
- Not meant to be exact (February = 28/29 days, but we show ~30)

---

### `year: 31536000`

**1 year ≈ 365 days**

**Calculation:**

```
365 days × 24 hours × 60 minutes × 60 seconds
= 365 × 86,400
= 31,536,000 seconds
```

**Why 365?**

- Leap years have 366 days
- We use 365 as average
- Again, good enough for display

---

### Understanding Object.entries()

```javascript
for (const [unit, secondsInUnit] of Object.entries(intervals)) {
  // ...
}
```

**Let me break down this line word by word:**

---

### `Object.entries(intervals)`

**This converts an object into an array of [key, value] pairs.**

**Example:**

```javascript
const intervals = {
  year: 31536000,
  month: 2592000,
  week: 604800,
};

const entries = Object.entries(intervals);
console.log(entries);
```

**Output:**

```javascript
[
  ["year", 31536000],
  ["month", 2592000],
  ["week", 604800],
];
```

**Visual representation:**

```
Object:
{
  year: 31536000,
  month: 2592000,
  week: 604800
}

    ↓ Object.entries()

Array of arrays:
[
  ['year', 31536000],
  ['month', 2592000],
  ['week', 604800]
]
```

---

### 🎥 Understanding Object.entries()

**Watch this for clarity:**

- 🎥 [Object.entries Explained](https://www.youtube.com/watch?v=VmicKaGcs5g) (5 min) - Quick guide
- 📚 [MDN: Object.entries](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/entries) - Reference

---

### `for...of` Loop

**This loops through each item in an array.**

**Format:**

```javascript
for (const item of array) {
  // Do something with item
}
```

**Example:**

```javascript
const colors = ["red", "green", "blue"];

for (const color of colors) {
  console.log(color);
}

// Output:
// red
// green
// blue
```

**Each time through the loop, `color` is the next item in the array.**

---

### Array Destructuring: `[unit, secondsInUnit]`

**This unpacks the array into separate variables.**

**Without destructuring:**

```javascript
for (const entry of Object.entries(intervals)) {
  const unit = entry[0]; // 'year'
  const secondsInUnit = entry[1]; // 31536000
  // ...
}
```

**With destructuring:**

```javascript
for (const [unit, secondsInUnit] of Object.entries(intervals)) {
  // unit = 'year'
  // secondsInUnit = 31536000
  // ...
}
```

**It's a shorthand!**

**Visual example:**

```javascript
const entry = ["year", 31536000];

// Destructuring unpacks it:
const [unit, secondsInUnit] = entry;

// Now:
unit = "year";
secondsInUnit = 31536000;
```

---

### 🎥 Understanding Destructuring

**Watch this to fully understand:**

- 🎥 [Array Destructuring in 100 Seconds](https://www.youtube.com/watch?v=UgEaJBz3bjY) (2 min) - Quick intro
- 📺 [JavaScript Destructuring](https://www.youtube.com/watch?v=NIq3qLaHCIs) (10 min) - Complete guide
- 📚 [MDN: Destructuring assignment](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment) - Reference

---

### Understanding the Loop Logic

```javascript
for (const [unit, secondsInUnit] of Object.entries(intervals)) {
  const interval = Math.floor(seconds / secondsInUnit);

  if (interval >= 1) {
    return `${interval} ${unit}${interval > 1 ? "s" : ""} ago`;
  }
}
```

**Let me trace through an example with 7,200 seconds (2 hours ago):**

---

**Loop iteration 1:**

```javascript
unit = 'year'
secondsInUnit = 31536000

interval = Math.floor(7200 / 31536000)
interval = Math.floor(0.000228)
interval = 0

if (0 >= 1)  // false, skip this one
```

**Not enough seconds to make a year!**

---

**Loop iteration 2:**

```javascript
unit = 'month'
secondsInUnit = 2592000

interval = Math.floor(7200 / 2592000)
interval = Math.floor(0.00278)
interval = 0

if (0 >= 1)  // false, skip
```

**Not enough seconds to make a month!**

---

**Loop iteration 3:**

```javascript
unit = 'week'
secondsInUnit = 604800

interval = Math.floor(7200 / 604800)
interval = Math.floor(0.0119)
interval = 0

if (0 >= 1)  // false, skip
```

**Not enough seconds to make a week!**

---

**Loop iteration 4:**

```javascript
unit = 'day'
secondsInUnit = 86400

interval = Math.floor(7200 / 86400)
interval = Math.floor(0.0833)
interval = 0

if (0 >= 1)  // false, skip
```

**Not enough seconds to make a day!**

---

**Loop iteration 5:**

```javascript
unit = "hour";
secondsInUnit = 3600;

interval = Math.floor(7200 / 3600);
interval = Math.floor(2);
interval = 2;

if (2 >= 1)
  // true! ✅
  return `${2} ${"hour"}${2 > 1 ? "s" : ""} ago`;
return `2 hours ago`;
```

**SUCCESS! We found the right unit!**

**The loop automatically stops here because of the `return` statement.**

---

### Visual Flow Diagram

```
7200 seconds
    ↓
Check: year?    7200 / 31536000 = 0.000228 → NO
Check: month?   7200 / 2592000 = 0.00278 → NO
Check: week?    7200 / 604800 = 0.0119 → NO
Check: day?     7200 / 86400 = 0.0833 → NO
Check: hour?    7200 / 3600 = 2 → YES! ✅
    ↓
Return "2 hours ago"
```

**The loop tries largest units first, then works down to smaller units!**

---

### Why This Approach Is Better

**Instead of this:**

```javascript
// Old way: Nested if/else (messy!)
if (seconds < 60) {
  return "just now";
} else if (seconds < 3600) {
  const minutes = Math.floor(seconds / 60);
  return minutes + " minute" + (minutes > 1 ? "s" : "") + " ago";
} else if (seconds < 86400) {
  const hours = Math.floor(seconds / 3600);
  return hours + " hour" + (hours > 1 ? "s" : "") + " ago";
} else if (seconds < 604800) {
  const days = Math.floor(seconds / 86400);
  return days + " day" + (days > 1 ? "s" : "") + " ago";
}
// ... and so on
```

**We use this:**

```javascript
// New way: Loop through intervals (clean!)
for (const [unit, secondsInUnit] of Object.entries(intervals)) {
  const interval = Math.floor(seconds / secondsInUnit);
  if (interval >= 1) {
    return `${interval} ${unit}${interval > 1 ? "s" : ""} ago`;
  }
}
```

**Benefits:**

- ✅ Less code
- ✅ Easy to add new units (just add to intervals object)
- ✅ No repeated logic
- ✅ Cleaner to read
- ✅ Harder to make mistakes

---

### Understanding Template Literals

```javascript
return `${interval} ${unit}${interval > 1 ? "s" : ""} ago`;
```

**This is a template literal (string with embedded expressions).**

**Old way (concatenation):**

```javascript
return interval + " " + unit + (interval > 1 ? "s" : "") + " ago";
```

**New way (template literal):**

```javascript
return `${interval} ${unit}${interval > 1 ? "s" : ""} ago`;
```

**Breaking it down:**

### Backticks ` ` `

- Uses backticks (not quotes!)
- Allows multi-line strings
- Allows embedded expressions

### `${expression}`

- Evaluates the expression
- Converts to string
- Inserts into the template

**Example:**

```javascript
const interval = 2;
const unit = 'hour';

`${interval} ${unit}s ago`
  ↓
`2 hours ago`
```

**Step by step:**

```
`${interval} ${unit}${interval > 1 ? 's' : ''} ago`
  ↓ Replace ${interval}
`2 ${unit}${interval > 1 ? 's' : ''} ago`
  ↓ Replace ${unit}
`2 hour${interval > 1 ? 's' : ''} ago`
  ↓ Evaluate ${interval > 1 ? 's' : ''} (2 > 1 = true = 's')
`2 hours ago`
```

---

### Edge Case: Future Dates

```javascript
// Future dates (edge case)
if (seconds < 0) {
  return "in the future";
}
```

**Why would seconds be negative?**

```javascript
const now = new Date(); // Oct 10, 2025, 3:45 PM
const future = new Date(Date.now() + 3600000); // 1 hour in the future

const diffMs = now - future; // negative number!
const seconds = Math.floor(diffMs / 1000); // negative!
```

**If the date is in the future, the difference is negative!**

**We handle this gracefully:** Show "in the future" instead of "-1 hours ago"

---

### Test the Final Version

```javascript
const testTimes = [
  new Date(), // just now
  new Date(Date.now() - 30000), // 30 seconds → just now
  new Date(Date.now() - 180000), // 3 minutes → 3 minutes ago
  new Date(Date.now() - 7200000), // 2 hours → 2 hours ago
  new Date(Date.now() - 172800000), // 2 days → 2 days ago
  new Date(Date.now() - 1209600000), // 2 weeks → 2 weeks ago
  new Date(Date.now() - 7776000000), // 3 months → 3 months ago
  new Date(Date.now() - 63072000000), // 2 years → 2 years ago
  new Date(Date.now() + 3600000), // 1 hour future → in the future
  "invalid date", // Invalid date
];

testTimes.forEach((time) => {
  console.log(getRelativeTime(time));
});
```

**Output:**

```
just now
just now
3 minutes ago
2 hours ago
2 days ago
2 weeks ago
3 months ago
2 years ago
in the future
Invalid date
```

**Perfect!** ✅

---

## getRelativeTime() Complete! 🎉

**You now have a production-ready relative time formatter that:**

- Handles all time units (seconds to years)
- Handles edge cases (future dates, invalid dates)
- Uses clean, maintainable code
- Never crashes

**More importantly, you understand:**

- How to calculate time differences
- How to convert between time units
- Object.entries() for iteration
- Array destructuring
- Template literals
- The ternary operator

---

## Quick Breather

**We've built two complex functions!**

**Before Part 5 (formatDuration), let me check:**

1. **Do you need a break?**
2. **Any questions about getRelativeTime()?**
3. **Ready to continue to formatDuration()?**

**Say "Continue to Part 5" when you're ready, or ask any questions!** 🚀

Part 5 will be shorter (formatDuration is simpler) and will introduce the modulo operator in depth!
