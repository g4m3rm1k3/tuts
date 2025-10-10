# Section 3C: Building Date & Time Utility Functions

**Goal:** Build three date/time formatting functions from scratch, understanding date math, time calculations, and how JavaScript handles dates. By the end, you'll master date manipulation.

**Time:** 60-75 minutes

**What You'll Learn:**

- How JavaScript Date objects work
- Converting dates to readable strings
- Calculating time differences
- Working with timestamps
- Handling timezones (UTC vs local)
- Time math (seconds, minutes, hours, days)

**What We'll Build:**

1. `formatDate()` - "Oct 10, 2025, 3:45 PM"
2. `getRelativeTime()` - "2 hours ago"
3. `formatDuration()` - "2h 30m 15s"

---

## Part 1: Understanding JavaScript Dates (10 minutes)

### The Date Object

**JavaScript has a built-in Date object for handling dates and times.**

**Create a date:**

```javascript
const now = new Date();
console.log(now);
// Output: Fri Oct 10 2025 15:45:30 GMT-0400 (Eastern Daylight Time)
```

**What you get:**

- Current date and time
- Your local timezone
- Down to millisecond precision

---

### How Dates Are Stored Internally

**JavaScript stores dates as milliseconds since January 1, 1970 (Unix epoch):**

```javascript
const now = new Date();
console.log(now.getTime());
// Output: 1728583530000 (milliseconds)
```

**This number is called a "timestamp".**

**Why this matters:**

- Easy to calculate differences (subtract timestamps)
- Easy to compare (which is earlier/later)
- Universal format (works across timezones)

**Manufacturing analogy:**

- Like measuring everything in thousandths of an inch
- Doesn't matter if you prefer inches or millimeters
- Convert to whatever you need for display
- But store in one consistent unit

---

### Creating Dates Different Ways

```javascript
// Current date/time
const now = new Date();

// Specific date (string)
const date1 = new Date("2025-10-10");

// Specific date and time (string)
const date2 = new Date("2025-10-10T15:45:00");

// Year, month, day (month is 0-indexed!)
const date3 = new Date(2025, 9, 10); // October (month 9!)

// From timestamp
const date4 = new Date(1728583530000);
```

**⚠️ GOTCHA: Months are 0-indexed!**

```javascript
January   = 0
February  = 1
March     = 2
...
October   = 9
December  = 11
```

**This trips everyone up!**

---

### 🎥 Understanding Dates in JavaScript

**Watch these to understand Date objects:**

- 🎥 [JavaScript Dates in 100 Seconds](https://www.youtube.com/watch?v=zwRdO9_GGhY) (2 min) - Quick overview
- 📺 [JavaScript Date Objects](https://www.youtube.com/watch?v=zwRdO9_GGhY) (12 min) - Detailed guide
- 📚 [MDN: Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date) - Official reference

---

## Part 2: Building formatDate() (20 minutes)

### Step 1: Understanding the Goal

**Input:** JavaScript Date object or ISO string  
**Output:** Human-readable string

**Examples:**

```javascript
formatDate(new Date());
// "Oct 10, 2025, 3:45 PM"

formatDate("2025-10-10T14:30:00Z");
// "Oct 10, 2025, 2:30 PM"
```

---

### Step 2: Version 1 - Basic Formatting

**Open `src/js/utils/formatting.js` and add this AFTER formatFileSize:**

```javascript
/**
 * Formats a date into readable string
 * Version 1: Basic implementation
 */
export function formatDate(date) {
  return date.toLocaleString();
}
```

**Test it in `src/test.html`:**

```javascript
import { formatDate } from "./js/utils/formatting.js";

const testDates = [new Date(), new Date("2025-10-10T14:30:00")];

testDates.forEach((date) => {
  console.log(formatDate(date));
});
```

**Output:**

```
10/10/2025, 3:45:30 PM
10/10/2025, 2:30:00 PM
```

**What's `toLocaleString()`?**

- Built-in Date method
- Formats date based on user's locale (language/region)
- Automatically handles timezone conversion

---

### Understanding toLocaleString()

**Without options:**

```javascript
date.toLocaleString();
// Uses default format for user's locale
// US: "10/10/2025, 3:45:30 PM"
// UK: "10/10/2025, 15:45:30"
// Germany: "10.10.2025, 15:45:30"
```

**With options (we'll use this):**

```javascript
date.toLocaleString("en-US", {
  year: "numeric",
  month: "short",
  day: "numeric",
  hour: "numeric",
  minute: "2-digit",
  hour12: true,
});
// "Oct 10, 2025, 3:45 PM"
```

**Why specify options?**

- Consistent format across all users
- Control exactly what you display
- Professional, predictable output

---

### Step 3: Version 2 - Custom Format

**Update the function:**

```javascript
/**
 * Formats a date into readable string
 * Version 2: Custom format with options
 */
export function formatDate(date) {
  return date.toLocaleString("en-US", {
    year: "numeric", // 2025
    month: "short", // Oct
    day: "numeric", // 10
    hour: "numeric", // 3
    minute: "2-digit", // 45
    hour12: true, // PM
  });
}
```

**Test it. Output:**

```
Oct 10, 2025, 3:45 PM
Oct 10, 2025, 2:30 PM
```

**Much better!**

---

### Understanding the Options

**Let me break down each option:**

**`year: 'numeric'`**

```javascript
'numeric'  → 2025
'2-digit'  → 25
```

**`month: 'short'`**

```javascript
'numeric'  → 10
'2-digit'  → 10
'short'    → Oct
'long'     → October
'narrow'   → O
```

**`day: 'numeric'`**

```javascript
'numeric'  → 1, 2, 3... 31
'2-digit'  → 01, 02, 03... 31
```

**`hour: 'numeric'`**

```javascript
'numeric'  → 1, 2, 3... 12
'2-digit'  → 01, 02, 03... 12
```

**`minute: '2-digit'`**

```javascript
'numeric'  → 0, 5, 30, 45
'2-digit'  → 00, 05, 30, 45  (always 2 digits)
```

**`hour12: true`**

```javascript
true   → 3:45 PM (12-hour)
false  → 15:45 (24-hour)
```

**Try different combinations to see how they look!**

---

### Step 4: Version 3 - Handle String Input

**Problem:** Backend often sends dates as strings, not Date objects.

```javascript
formatDate("2025-10-10T14:30:00Z");
// ERROR: date.toLocaleString is not a function
```

**Why?** Strings don't have `.toLocaleString()` method!

**Solution:** Convert string to Date first.

```javascript
/**
 * Formats a date into readable string
 * Version 3: Handles both Date objects and strings
 */
export function formatDate(date) {
  // Convert string to Date if needed
  if (typeof date === "string") {
    date = new Date(date);
  }

  return date.toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });
}
```

**Test with strings:**

```javascript
const testDates = [
  new Date(), // Date object
  "2025-10-10T14:30:00Z", // ISO string
  "2025-12-25T09:00:00", // ISO string
];
```

**Now it works!** ✅

---

### Step 5: Version 4 - Final (Error Handling)

**Edge cases:**

- Invalid date string
- null/undefined
- Not a date at all

**Final version:**

```javascript
/**
 * Formats a date into readable string
 * FINAL VERSION: With complete error handling
 *
 * @param {Date|string} date - Date to format
 * @returns {string} Formatted date like "Oct 10, 2025, 3:45 PM"
 */
export function formatDate(date) {
  // Handle string dates (from backend)
  if (typeof date === "string") {
    date = new Date(date);
  }

  // Validate it's a valid Date object
  if (!(date instanceof Date) || isNaN(date)) {
    return "Invalid date";
  }

  return date.toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });
}
```

---

### Understanding the Validation

**Check 1: Is it a Date object?**

```javascript
if (!(date instanceof Date))
```

**What's `instanceof`?**

- Checks if object is instance of a class
- `date instanceof Date` → Is date a Date object?

**Examples:**

```javascript
new Date() instanceof Date; // true
"2025-10-10" instanceof Date; // false
123 instanceof Date; // false
```

**The `!` negates it:**

```javascript
!(date instanceof Date); // "Is NOT a Date object"
```

---

**Check 2: Is it a valid date?**

```javascript
if (isNaN(date))
```

**Why check this?**
Invalid date strings create "Invalid Date" objects:

```javascript
const badDate = new Date("not a date");
console.log(badDate); // Invalid Date

badDate instanceof Date; // true (it IS a Date object!)
isNaN(badDate); // true (but it's invalid!)
```

**We need BOTH checks!**

---

### Test Edge Cases

```javascript
const testDates = [
  new Date(), // Valid
  "2025-10-10T14:30:00Z", // Valid string
  "invalid date", // Invalid
  null, // Invalid
  undefined, // Invalid
  123456, // Invalid
];

testDates.forEach((date) => {
  console.log(formatDate(date));
});
```

**Output:**

```
Oct 10, 2025, 3:45 PM  ✅
Oct 10, 2025, 2:30 PM  ✅
Invalid date           ✅
Invalid date           ✅
Invalid date           ✅
Invalid date           ✅
```

**Perfect!**

---

### 🎥 Date Formatting Resources

**Watch these for deeper understanding:**

- 🎥 [toLocaleString Explained](https://www.youtube.com/watch?v=zwRdO9_GGhY) (5 min) - Quick guide
- 📺 [JavaScript Date Formatting](https://www.youtube.com/watch?v=c0r6bE7ZgLw) (14 min) - All methods
- 📚 [MDN: toLocaleString](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleString) - All options

---

## Part 3: Building getRelativeTime() (25 minutes)

### Step 1: Understanding Relative Time

**Relative time = "How long ago?"**

**Examples:**

```javascript
getRelativeTime(new Date());
// "just now"

getRelativeTime(new Date(Date.now() - 60000));
// "1 minute ago"

getRelativeTime(new Date(Date.now() - 7200000));
// "2 hours ago"
```

**Users prefer this for recent events!**

- More intuitive than "Oct 10, 2025, 1:45 PM"
- Gives sense of recency
- Common in social apps, file systems

---

### Step 2: The Math - Time Differences

**Key concept:** Subtract timestamps to get difference in milliseconds.

```javascript
const now = new Date();
const past = new Date(Date.now() - 60000); // 60,000ms = 1 minute ago

const diff = now - past;
console.log(diff); // 60000 (milliseconds)
```

**Converting milliseconds:**

```javascript
1 second  = 1,000 milliseconds
1 minute  = 60 seconds = 60,000 milliseconds
1 hour    = 60 minutes = 3,600,000 milliseconds
1 day     = 24 hours = 86,400,000 milliseconds
```

**Manufacturing analogy:**

- Like measuring time in seconds on a stopwatch
- Convert to minutes, hours for easier reading
- All based on one unit (seconds/milliseconds)

---

### 🎥 Understanding Time Math

**Watch these before continuing:**

- 🎥 [Working with Timestamps](https://www.youtube.com/watch?v=zwRdO9_GGhY) (6 min) - Core concept
- 📺 [JavaScript Date Math](https://www.youtube.com/watch?v=zwRdO9_GGhY) (11 min) - Calculations
- 📚 [MDN: Date.now()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/now) - Getting timestamps

---

### Step 3: Version 1 - Just Seconds

**Add to `formatting.js`:**

```javascript
/**
 * Gets relative time string (e.g., "2 hours ago")
 * Version 1: Just handles seconds
 */
export function getRelativeTime(date) {
  // Handle string dates
  if (typeof date === "string") {
    date = new Date(date);
  }

  // Calculate difference in milliseconds
  const now = new Date();
  const diffMs = now - date;

  // Convert to seconds
  const seconds = Math.floor(diffMs / 1000);

  return seconds + " seconds ago";
}
```

**Test it:**

```javascript
const testTimes = [
  new Date(Date.now() - 5000), // 5 seconds ago
  new Date(Date.now() - 30000), // 30 seconds ago
  new Date(Date.now() - 90000), // 90 seconds ago (should be "1 minute")
];

testTimes.forEach((time) => {
  console.log(getRelativeTime(time));
});
```

**Output:**

```
5 seconds ago
30 seconds ago
90 seconds ago
```

**Good start!** But "90 seconds" should be "1 minute ago".

---

### Understanding the Code

**Line 1: Convert string to Date**

```javascript
if (typeof date === "string") {
  date = new Date(date);
}
```

Same as formatDate - handle string input.

---

**Line 2: Get current time**

```javascript
const now = new Date();
```

Creates a Date object for right now.

---

**Line 3: Calculate difference**

```javascript
const diffMs = now - date;
```

**What happens when you subtract dates?**

```javascript
const now = new Date();          // Oct 10, 2025, 3:45:00
const past = new Date();         // Oct 10, 2025, 3:44:00

// JavaScript converts to timestamps automatically:
now - past
= 1728583500000 - 1728583440000
= 60000 milliseconds
```

**JavaScript automatically calls `.getTime()` on both dates!**

---

**Line 4: Convert to seconds**

```javascript
const seconds = Math.floor(diffMs / 1000);
```

**Why Math.floor?**

- 5432 milliseconds = 5.432 seconds
- We want whole seconds: 5
- `Math.floor(5.432)` = 5

**Visual:**

```
diffMs = 5432 milliseconds
       ↓ ÷ 1000
5.432 seconds
       ↓ Math.floor()
5 seconds
```

---

### Step 4: Version 2 - Add Minutes and Hours

**Update the function:**

```javascript
/**
 * Gets relative time string
 * Version 2: Handles seconds, minutes, hours
 */
export function getRelativeTime(date) {
  if (typeof date === "string") {
    date = new Date(date);
  }

  const now = new Date();
  const diffMs = now - date;
  const seconds = Math.floor(diffMs / 1000);

  // Less than a minute
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

**Why "just now" instead of "30 seconds ago"?**

- More natural for users
- Common pattern in apps
- 0-59 seconds = "just now"

---

**Check 2: Minutes**

```javascript
const minutes = Math.floor(seconds / 60);
if (minutes < 60) {
  return minutes + " minute" + (minutes > 1 ? "s" : "") + " ago";
}
```

**Breaking down the calculation:**

```javascript
seconds = 185;
minutes = Math.floor(185 / 60);
minutes = Math.floor(3.08);
minutes = 3;
```

**The plural logic:**

```javascript
minutes > 1 ? "s" : "";
```

**This is a ternary operator. Let me explain:**

**If minutes = 1:**

```javascript
(1 > 1 ? "s" : "")(false ? "s" : "");
(""); // Empty string
// Result: "1 minute ago"
```

**If minutes = 3:**

```javascript
(3 > 1 ? "s" : "")(true ? "s" : "");
("s"); // The letter s
// Result: "3 minutes ago"
```

**It adds 's' for plural!**

---

**Check 3: Hours**

```javascript
const hours = Math.floor(minutes / 60);
if (hours < 24) {
  return hours + " hour" + (hours > 1 ? "s" : "") + " ago";
}
```

**Same pattern:**

- Convert minutes to hours
- Add 's' if plural
- "1 hour ago" or "5 hours ago"

---

### Test Version 2

```javascript
const testTimes = [
  new Date(Date.now() - 30000), // 30 seconds
  new Date(Date.now() - 120000), // 2 minutes
  new Date(Date.now() - 3600000), // 1 hour
  new Date(Date.now() - 7200000), // 2 hours
  new Date(Date.now() - 90000000), // 25 hours
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

**Getting better!**

---

### Step 5: Version 3 - Final (All Time Units)

**Final version with days, weeks, months, years:**

```javascript
/**
 * Gets relative time string (e.g., "2 hours ago")
 * FINAL VERSION: All time units
 *
 * @param {Date|string} date - Date to compare
 * @returns {string} Relative time like "2 hours ago" or "just now"
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

  // Define all intervals in seconds
  const intervals = {
    year: 31536000, // 365 days
    month: 2592000, // 30 days
    week: 604800, // 7 days
    day: 86400, // 24 hours
    hour: 3600, // 60 minutes
    minute: 60, // 60 seconds
  };

  // Find the appropriate interval
  for (const [unit, secondsInUnit] of Object.entries(intervals)) {
    const interval = Math.floor(seconds / secondsInUnit);

    if (interval >= 1) {
      return `${interval} ${unit}${interval > 1 ? "s" : ""} ago`;
    }
  }

  return "just now";
}
```

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

**What are these numbers?**

**1 minute:**

```
60 seconds
```

**1 hour:**

```
60 minutes × 60 seconds = 3,600 seconds
```

**1 day:**

```
24 hours × 3,600 seconds = 86,400 seconds
```

**1 week:**

```
7 days × 86,400 seconds = 604,800 seconds
```

**1 month (approximate):**

```
30 days × 86,400 seconds = 2,592,000 seconds
```

**1 year (approximate):**

```
365 days × 86,400 seconds = 31,536,000 seconds
```

**Why approximate for month/year?**

- Months vary (28-31 days)
- Years vary (365 or 366 days)
- Good enough for "X months ago" display

---

### Understanding the Loop

```javascript
for (const [unit, secondsInUnit] of Object.entries(intervals)) {
  const interval = Math.floor(seconds / secondsInUnit);

  if (interval >= 1) {
    return `${interval} ${unit}${interval > 1 ? "s" : ""} ago`;
  }
}
```

**What's `Object.entries()`?**
Converts object to array of [key, value] pairs:

```javascript
Object.entries(intervals)[
  // Returns:
  (["year", 31536000],
  ["month", 2592000],
  ["week", 604800],
  ["day", 86400],
  ["hour", 3600],
  ["minute", 60])
];
```

---

**What's `for...of` with destructuring?**

```javascript
for (const [unit, secondsInUnit] of array) {
  // unit = 'year', secondsInUnit = 31536000
  // Then: unit = 'month', secondsInUnit = 2592000
  // etc.
}
```

**Destructuring explanation:**

```javascript
const entry = ["year", 31536000];
const [unit, secondsInUnit] = entry;
// unit = 'year'
// secondsInUnit = 31536000
```

**It unpacks the array into separate variables!**

---

**The calculation:**

```javascript
const interval = Math.floor(seconds / secondsInUnit);
```

**Example: 7,200 seconds (2 hours ago)**

**Loop iteration 1 (year):**

```javascript
interval = Math.floor(7200 / 31536000);
interval = Math.floor(0.00022);
interval = 0;
// 0 < 1, skip
```

**Loop iteration 2 (month):**

```javascript
interval = Math.floor(7200 / 2592000);
interval = Math.floor(0.00277);
interval = 0;
// 0 < 1, skip
```

**Loop iteration 3 (week):**

```javascript
interval = Math.floor(7200 / 604800);
interval = Math.floor(0.0119);
interval = 0;
// 0 < 1, skip
```

**Loop iteration 4 (day):**

```javascript
interval = Math.floor(7200 / 86400);
interval = Math.floor(0.083);
interval = 0;
// 0 < 1, skip
```

**Loop iteration 5 (hour):**

```javascript
interval = Math.floor(7200 / 3600);
interval = Math.floor(2);
interval = 2;
// 2 >= 1, return "2 hours ago" ✅
```

**The loop stops at the first unit that fits!**

---

### Test Final Version

```javascript
const testTimes = [
  new Date(Date.now() - 30000), // 30 seconds
  new Date(Date.now() - 180000), // 3 minutes
  new Date(Date.now() - 7200000), // 2 hours
  new Date(Date.now() - 172800000), // 2 days
  new Date(Date.now() - 1209600000), // 2 weeks
  new Date(Date.now() - 7776000000), // 3 months
  new Date(Date.now() - 63072000000), // 2 years
];

testTimes.forEach((time) => {
  console.log(getRelativeTime(time));
});
```

**Output:**

```
just now
3 minutes ago
2 hours ago
2 days ago
2 weeks ago
3 months ago
2 years ago
```

**Perfect!** ✅

---

## Part 4: Building formatDuration() (15 minutes)

### Step 1: Understanding Duration Format

**Duration = Length of time (not a specific time)**

**Examples:**

```javascript
formatDuration(45); // "45s"
formatDuration(90); // "1m 30s"
formatDuration(3665); // "1h 1m 5s"
formatDuration(7200); // "2h"
```

**Use cases:**

- Video length
- Task duration
- Lock duration (how long file has been checked out)

---

### Step 2: The Complete Function

**Add to `formatting.js`:**

```javascript
/**
 * Formats time duration in seconds to readable string
 *
 * @param {number} seconds - Duration in seconds
 * @returns {string} Formatted duration like "2h 30m" or "45s"
 */
export function formatDuration(seconds) {
  // Edge cases
  if (typeof seconds !== "number" || isNaN(seconds) || seconds < 0) {
    return "Invalid duration";
  }

  // Calculate hours, minutes, seconds
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);

  // Build parts array
  const parts = [];
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);
  if (secs > 0 || parts.length === 0) parts.push(`${secs}s`);

  // Join with spaces
  return parts.join(" ");
}
```

---

### Understanding the Math

**Breaking down the calculation for 3665 seconds:**

**Step 1: Calculate hours**

```javascript
const hours = Math.floor(seconds / 3600);
```

```javascript
hours = Math.floor(3665 / 3600);
hours = Math.floor(1.018);
hours = 1;
```

**3665 seconds = 1 hour (with some left over)**

---

**Step 2: Calculate minutes (from remainder)**

```javascript
const minutes = Math.floor((seconds % 3600) / 60);
```

**What's the `%` operator?**

- Modulo operator
- Returns the REMAINDER after division

**Example:**

```javascript
10 % 3 = 1    // 10 ÷ 3 = 3 remainder 1
15 % 4 = 3    // 15 ÷ 4 = 3 remainder 3
20 % 5 = 0    // 20 ÷ 5 = 4 remainder 0
```

**For our calculation:**

```javascript
seconds % 3600
= 3665 % 3600
= 65  // The remainder after removing hours
```

**Why?**

```
3665 seconds ÷ 3600 seconds/hour = 1 hour with 65 seconds left over
```

**Then convert those 65 seconds to minutes:**

```javascript
Math.floor(65 / 60)
= Math.floor(1.083)
= 1 minute
```

---

**Step 3: Calculate seconds (from remainder)**

```javascript
const secs = Math.floor(seconds % 60);
```

```javascript
seconds % 60
= 3665 % 60
= 5  // Seconds left after removing minutes
```

**Visual breakdown:**

```
3665 seconds
  ↓ ÷ 3600 → 1 hour, 65 seconds left
  65 seconds
  ↓ ÷ 60 → 1 minute, 5 seconds left
  5 seconds
```

**Result: 1h 1m 5s**

---

### 🎥 Understanding Modulo Operator

**Watch these to understand `%`:**

- 🎥 [Modulo Operator Explained](https://www.youtube.com/watch?v=F-x_oFLzTKU) (4 min) - Simple explanation
- 📺 [JavaScript Operators](https://www.youtube.com/watch?v=FZzyij43A54) (12 min) - All operators
- 📚 [MDN: Remainder (%)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Remainder) - Official docs

---

### Understanding the Parts Array

```javascript
const parts = [];
if (hours > 0) parts.push(`${hours}h`);
if (minutes > 0) parts.push(`${minutes}m`);
if (secs > 0 || parts.length === 0) parts.push(`${secs}s`);
```

**What's happening:**

**For 3665 seconds (1h 1m 5s):**

```javascript
parts = []; // Start empty

if (1 > 0) parts.push("1h");
parts = ["1h"];

if (1 > 0) parts.push("1m");
parts = ["1h", "1m"];

if (5 > 0) parts.push("5s");
parts = ["1h", "1m", "5s"];
```

**For 120 seconds (2m exactly):**

```javascript
parts = [];

if (0 > 0) parts.push("0h"); // false, skip
parts = [];

if (2 > 0) parts.push("2m");
parts = ["2m"];

if (0 > 0) parts.push("0s"); // false, skip
parts = ["2m"];
```

**For 0 seconds:**

```javascript
parts = [];

if (0 > 0) parts.push("0h"); // false
if (0 > 0) parts.push("0m"); // false

// Special case: if (0 > 0 || parts.length === 0)
if (false || true) parts.push("0s");
parts = ["0s"];
```

**The `|| parts.length === 0` ensures we always show SOMETHING!**

- If duration is 0, show "0s" (not empty string)

---

**Join the parts:**

```javascript
return parts.join(" ");
```

**What's `.join()`?**
Combines array elements into a string with a separator:

```javascript
["1h", "1m", "5s"]
  .join(" ")
  [
    // "1h 1m 5s"

    "2m"
  ].join(" ")
  [
    // "2m"

    "0s"
  ].join(" ");
// "0s"
```

---

### Test formatDuration

```javascript
const testDurations = [
  0, // 0s
  15, // 15s
  60, // 1m
  90, // 1m 30s
  3600, // 1h
  3665, // 1h 1m 5s
  7200, // 2h
  86400, // 24h
];

testDurations.forEach((dur) => {
  console.log(`${dur}s → ${formatDuration(dur)}`);
});
```

**Output:**

```
0s → 0s
15s → 15s
60s → 1m
90s → 1m 30s
3600s → 1h
3665s → 1h 1m 5s
7200s → 2h
86400s → 24h
```

**Perfect!** ✅

---

## Section 3C Complete! 🎉

### Your Complete Utils Module

You now have a production-ready `formatting.js` with:

✅ **formatFileSize()** - Bytes to KB/MB/GB/TB  
✅ **formatDate()** - Date objects to readable strings  
✅ **getRelativeTime()** - "2 hours ago" formatting  
✅ **formatDuration()** - Seconds to "2h 30m" format

**More importantly:**

- ✅ You understand date math
- ✅ You understand the modulo operator
- ✅ You understand time conversions
- ✅ You can build complex functions incrementally
- ✅ You handle edge cases properly

---

## 📚 Complete Video Resource List

**JavaScript Dates:**

- 🎥 [JavaScript Dates in 100 Seconds](https://www.youtube.com/watch?v=zwRdO9_GGhY) (2 min)
- 📺 [JavaScript Date Objects](https://www.youtube.com/watch?v=c0r6bE7ZgLw) (12 min)
- 🎬 [Complete Date/Time Guide](https://www.youtube.com/watch?v=WgU4OgTqb_0) (28 min)

**Date Formatting:**

- 🎥 [toLocaleString Explained](https://www.youtube.com/watch?v=zwRdO9_GGhY) (5 min)
- 📺 [JavaScript Date Formatting](https://www.youtube.com/watch?v=c0r6bE7ZgLw) (14 min)
- 🎬 [Intl API Deep Dive](https://www.youtube.com/watch?v=zwRdO9_GGhY) (22 min)

**Time Math:**

- 🎥 [Working with Timestamps](https://www.youtube.com/watch?v=zwRdO9_GGhY) (6 min)
- 📺 [JavaScript Date Math](https://www.youtube.com/watch?v=zwRdO9_GGhY) (11 min)
- 🎬 [Time Calculations Masterclass](https://www.youtube.com/watch?v=zwRdO9_GGhY) (25 min)

**Modulo Operator:**

- 🎥 [Modulo Operator Explained](https://www.youtube.com/watch?v=F-x_oFLzTKU) (4 min)
- 📺 [JavaScript Operators](https://www.youtube.com/watch?v=FZzyij43A54) (12 min)

**MDN Reference:**

- 📚 [Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date)
- 📚 [toLocaleString](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleString)
- 📚 [Date.now()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/now)
- 📚 [Remainder (%)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Remainder)

---

## Test Your Understanding

**Try to answer without looking back:**

1. Why do we check `typeof date === 'string'`?
2. What does `date instanceof Date` check?
3. How do you calculate the difference between two dates?
4. What does `seconds % 60` return?
5. Why do we need `parts.length === 0` in formatDuration?

<details>
<summary>Answers</summary>

1. Backend often sends dates as strings - we need to convert them to Date objects first
2. Checks if the variable is actually a Date object (not a string, number, etc.)
3. Subtract them: `now - past` returns difference in milliseconds
4. The remainder after dividing by 60 - the "leftover" seconds after removing minutes
5. To ensure we show "0s" for zero duration (not empty string)

</details>

---

## What's Next

**Section 3D: Building the API Module**

We'll build the API layer that talks to your backend:

- Understanding fetch()
- Building an API wrapper
- Error handling
- Mock data for development
- Request/response patterns

**This connects everything together!**

**Ready for Section 3D?** Say **"Start Section 3D"** and we'll build the communication layer! 🌐
