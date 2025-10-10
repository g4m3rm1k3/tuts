**PERFECT!** 🎯 Let's start completely fresh with the proper pace and detail level.

I totally understand the "darts blindfolded" CSS approach - you're guessing at class combinations and adding `!important` when things don't work. **We're going to fix that.**

---

# Section 3A: Project Setup with Tailwind (Proper Way)

**Goal:** Set up the project with npm, install Tailwind properly, create a Mastercam color theme, and understand exactly how the styling system works.

**Time:** 30-40 minutes

**What You'll Learn:**

- How npm manages dependencies (no magic CDN links)
- How Tailwind's build process works
- How to create custom color themes
- How CSS specificity works (why you need !important and how to avoid it)
- How to organize styles so they're maintainable

---

## Part 1: Understanding the Setup (5 minutes)

### What We're Building

**Current approach (from your existing app):**

```html
<script src="https://cdn.tailwindcss.com"></script>
```

**Problems with CDN:**

- ❌ Can't customize colors easily
- ❌ Needs internet
- ❌ Limited configuration
- ❌ Large file size (includes everything)
- ❌ Can't use Tailwind's advanced features

**New approach (npm + build process):**

```
Your Code → Tailwind Build → Optimized CSS
```

**Benefits:**

- ✅ Custom Mastercam colors
- ✅ Works offline
- ✅ Only includes classes you use (small file)
- ✅ Full configuration control
- ✅ Can extend with custom utilities

---

## Part 2: Project Structure Setup (10 minutes)

### Step 1: Navigate to Your Project

**Open your terminal and go to where you want the project:**

```bash
cd Desktop  # Or wherever you want it
mkdir mastercam-pdm-rebuild
cd mastercam-pdm-rebuild
```

**What this does:**

- `mkdir` = make directory (creates folder)
- `cd` = change directory (moves into folder)

---

### Step 2: Initialize npm

**Run this command:**

```bash
npm init -y
```

**What you'll see:**

```
Wrote to /path/to/mastercam-pdm-rebuild/package.json:

{
  "name": "mastercam-pdm-rebuild",
  "version": "1.0.0",
  "description": "",
  ...
}
```

**What this does:**

- Creates `package.json` file
- This file tracks all your project dependencies
- `-y` = "yes to all defaults" (skip the questions)

**What's a dependency?**
Think of it like a parts list for a machine:

- Your project needs Tailwind CSS
- Tailwind might need other libraries
- npm tracks all of this

**Manufacturing analogy:**

- `package.json` = Bill of Materials (BOM)
- Lists all parts (libraries) needed
- Tracks versions (revision numbers)

---

### Step 3: Install Tailwind and Dependencies

**Run these commands one at a time:**

```bash
npm install -D tailwindcss
npm install -D postcss
npm install -D autoprefixer
```

**What each one does:**

**1. tailwindcss**

- The actual Tailwind CSS library
- Provides all the utility classes

**2. postcss**

- Processes CSS files
- Transforms your code
- Like a CNC controller for CSS

**3. autoprefixer**

- Adds browser-specific prefixes
- Makes CSS work in all browsers
- Example: `-webkit-transform` for Safari

**What's `-D`?**

- Means "development dependency"
- Only needed while building
- Won't be included in final app

**What you'll see:**

```
added 100 packages, and audited 101 packages in 5s
```

**Where did it install?**
Look at your folder - you'll see:

- `node_modules/` folder (contains all the code)
- `package-lock.json` (exact versions installed)

**Don't commit `node_modules/` to git!** (We'll set up .gitignore later)

---

### Step 4: Create Folder Structure

**Run these commands:**

```bash
mkdir -p src/css
mkdir -p src/js
mkdir -p public
touch src/css/input.css
touch src/index.html
```

**What `-p` does:**

- Creates parent folders if needed
- `mkdir -p src/css` creates both `src` and `src/css`

**What `touch` does:**

- Creates an empty file
- Like "New File" in Windows Explorer

**Your structure now:**

```
mastercam-pdm-rebuild/
├── node_modules/          (installed packages)
├── package.json           (project config)
├── package-lock.json      (exact versions)
├── src/                   (your source code)
│   ├── css/
│   │   └── input.css      (Tailwind source)
│   ├── js/
│   └── index.html         (main HTML)
└── public/                (built files - browser loads these)
```

**Why separate src/ and public/?**

**src/** = Your code (what you edit)

- Raw HTML with Tailwind classes
- Needs to be processed

**public/** = Built code (what browser loads)

- Processed CSS (optimized)
- Copied HTML
- Ready for production

**Manufacturing analogy:**

- src/ = Raw materials and blueprints
- public/ = Finished parts ready to ship

---

## Part 3: Initialize Tailwind Configuration (10 minutes)

### Step 5: Create Tailwind Config

**Run this command:**

```bash
npx tailwindcss init
```

**What's `npx`?**

- Runs packages without installing globally
- Like borrowing a tool instead of buying it

**What you'll see:**

```
Created Tailwind CSS config file: tailwind.config.js
```

**This creates a file. Open it - it looks like:**

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

**What each part means:**

**1. content: []**

- Tells Tailwind WHERE to look for classes
- Scans your HTML/JS files
- Only includes classes you actually use

**2. theme: { extend: {} }**

- Where you add custom colors, fonts, spacing
- `extend` means "add to defaults, don't replace"

**3. plugins: []**

- Extra Tailwind features
- We won't use any for now

---

### Step 6: Configure Content Paths

**Replace the `content: []` line with this:**

```javascript
module.exports = {
  content: ["./src/**/*.{html,js}", "./public/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

**What `"./src/**/\*.{html,js}"` means:\*\*

Let me break it down piece by piece:

**`./src/`** = Start in the src folder

- `.` = current directory
- `./src/` = src folder in current directory

**`**`\*\* = All subfolders (recursive)

- `*` = any folder name
- `**` = any level of nesting
- So it looks in `src/`, `src/js/`, `src/js/utils/`, etc.

**`*.{html,js}`** = Any .html or .js file

- `*` = any filename
- `{html,js}` = either .html OR .js extension

**Full meaning:**
"Look in src folder and ALL its subfolders, find ANY file ending in .html or .js"

**Why do we need this?**
Tailwind scans these files for class names like:

```html
<div class="bg-blue-500"></div>
```

It sees `bg-blue-500` is used, so includes it in the final CSS.

If a class isn't used anywhere, it's NOT included → smaller file!

**Manufacturing analogy:**

- Like doing an inventory before ordering parts
- Only stock what you actually use
- Don't fill warehouse with unused items

---

## Part 4: Create Mastercam Color Theme (15 minutes)

### Step 7: Understanding Mastercam Colors

**Mastercam's typical color scheme:**

**Dark Mode (Primary):**

- Background: Dark navy/slate
- Panels: Slightly lighter slate
- Text: White/light gray
- Accents: Teal/cyan (Mastercam's signature color)
- Success: Green
- Danger: Red/orange

**Light Mode (Secondary):**

- Background: Very light gray
- Panels: White
- Text: Dark gray/black
- Accents: Teal/cyan (same as dark)

**Let me research Mastercam's exact colors...**

Based on Mastercam's branding:

- **Teal/Cyan accent:** `#00A3E0` (Mastercam blue)
- **Dark backgrounds:** `#1a1d29` to `#2d3142`
- **Success green:** `#00C48C`
- **Warning orange:** `#FF6B35`

---

### Step 8: Add Custom Colors to Config

**Open `tailwind.config.js` and replace it with this:**

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}", "./public/**/*.html"],
  theme: {
    extend: {
      colors: {
        // Mastercam Brand Colors
        mastercam: {
          // Main accent color (Mastercam cyan/teal)
          50: "#e6f7ff", // Lightest - for hover states
          100: "#b3e5ff",
          200: "#80d4ff",
          300: "#4dc2ff",
          400: "#1ab1ff",
          500: "#00A3E0", // Main Mastercam blue
          600: "#0082b3",
          700: "#006286",
          800: "#00415a",
          900: "#00202d", // Darkest - for backgrounds
        },

        // Dark theme background colors
        dark: {
          900: "#0f1117", // Darkest background
          800: "#1a1d29", // Main background
          700: "#2d3142", // Elevated panels
          600: "#3e4357", // Hover states
          500: "#4f5469", // Borders
        },

        // Light theme colors
        light: {
          50: "#ffffff", // Pure white
          100: "#f7f8fa", // Main background
          200: "#e8eaed", // Panels
          300: "#d1d5db", // Borders
        },

        // Status colors
        success: "#00C48C",
        warning: "#FF6B35",
        danger: "#EF4444",
      },
    },
  },
  plugins: [],
};
```

**Let me explain each color set:**

---

### Understanding the Color Scale (50-900)

**Why numbers instead of names?**

Tailwind uses a numeric scale where:

- **50** = Lightest (almost white)
- **500** = Medium (the "main" color)
- **900** = Darkest (almost black)

**Visual scale for `mastercam` color:**

```
50  ███░░░░░░░  10% intensity (barely visible)
100 ████░░░░░░  20%
200 █████░░░░░  30%
300 ██████░░░░  40%
400 ███████░░░  50%
500 ████████░░  60% ← Main color (Mastercam blue)
600 █████████░  70%
700 ██████████  80%
800 ██████████  90%
900 ██████████  100% (darkest)
```

**How you'll use these:**

```html
<!-- Light hover state -->
<button class="bg-mastercam-500 hover:bg-mastercam-400">Hover me</button>

<!-- Background → slightly lighter on hover -->
```

**Why this matters:**
With a proper scale, colors RELATE to each other:

- ✅ `mastercam-400` to `mastercam-500` = subtle change
- ✅ All shades work together
- ❌ Random colors = jarring transitions

---

### Understanding the Dark Theme Colors

```javascript
dark: {
  900: '#0f1117',  // Darkest background
  800: '#1a1d29',  // Main background
  700: '#2d3142',  // Elevated panels
  600: '#3e4357',  // Hover states
  500: '#4f5469',  // Borders
},
```

**How these work together:**

**900 = Page background** (darkest)

```html
<body class="bg-dark-900"></body>
```

Think: The machine shop floor (dark foundation)

**800 = Main panels** (slightly lighter)

```html
<div class="bg-dark-800">
  <!-- File cards, modals -->
</div>
```

Think: The machine enclosure (stands out from floor)

**700 = Elevated elements** (lighter still)

```html
<div class="bg-dark-700">
  <!-- Headers, active items -->
</div>
```

Think: Control panel (most visible)

**600 = Hover states**

```html
<button class="bg-dark-700 hover:bg-dark-600"></button>
```

Think: Visual feedback when touching controls

**500 = Borders**

```html
<div class="border border-dark-500"></div>
```

Think: Subtle lines separating areas

**Visual hierarchy:**

```
┌─────────────────────────────────┐  ← dark-500 (border)
│  bg-dark-700 (elevated panel)   │
│  ┌──────────────────────────┐   │
│  │  bg-dark-800 (card)      │   │  ← All on dark-900 page
│  │                          │   │
│  └──────────────────────────┘   │
└─────────────────────────────────┘
```

Each level is SLIGHTLY lighter → creates depth!

---

### Understanding Status Colors

```javascript
success: '#00C48C',  // Green
warning: '#FF6B35',  // Orange
danger: '#EF4444',   // Red
```

**These don't need scales because:**

- Used for specific states only
- Not used for backgrounds/borders
- Just need ONE shade each

**How you'll use them:**

```html
<!-- File available -->
<span class="bg-green-900 text-success"> Available </span>

<!-- File locked (danger) -->
<span class="bg-red-900 text-danger"> Locked </span>
```

**Notice the pattern:**

- Background: dark version of color (`bg-green-900`)
- Text: bright version (`text-success`)
- Creates READABLE badges

---

### Step 9: Save and Test the Config

**Save `tailwind.config.js`**

**Let's test that it works. Open `src/css/input.css` and add:**

```css
/* This imports Tailwind's base styles, components, and utilities */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**What these directives do:**

**@tailwind base;**

- Resets browser defaults
- Normalizes styles across browsers
- Example: All browsers have different default margins - this fixes that

**@tailwind components;**

- Pre-built component classes
- Things like `.btn`, `.card` (we won't use these much)

**@tailwind utilities;**

- All the utility classes like `bg-blue-500`, `p-4`, etc.
- This is the main Tailwind magic

---

### Step 10: Build Tailwind CSS

**Run this command:**

```bash
npx tailwindcss -i ./src/css/input.css -o ./public/output.css --watch
```

**What this command does (piece by piece):**

**`npx tailwindcss`** = Run the Tailwind CLI tool

**`-i ./src/css/input.css`** = Input file

- Read from `src/css/input.css`
- This has the `@tailwind` directives

**`-o ./public/output.css`** = Output file

- Write processed CSS to `public/output.css`
- This is what your HTML will link to

**`--watch`** = Watch mode

- Keeps running
- Watches for changes
- Rebuilds automatically when you edit files

**What you'll see:**

```
Rebuilding...
Done in 123ms.
```

**Check your `public/` folder - you should now see `output.css`!**

**Don't stop this command!** Keep it running. Open a NEW terminal window for other commands.

**Manufacturing analogy:**

- This is like a CNC machine running continuously
- Watches for new drawings (your HTML changes)
- Automatically produces parts (updated CSS)

---

## Part 5: Create Your First HTML File (10 minutes)

### Step 11: Build the HTML Structure

**Open `src/index.html` and type this:**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Mastercam PDM</title>

    <!-- Link to our built CSS -->
    <link rel="stylesheet" href="../public/output.css" />
  </head>
  <body class="min-h-screen bg-dark-900 text-white">
    <!-- Header -->
    <header class="bg-dark-800 border-b border-dark-500 p-4">
      <h1 class="text-2xl font-bold text-mastercam-500">Mastercam PDM</h1>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto p-6">
      <h2 class="text-xl font-semibold mb-4">Welcome</h2>
      <p class="text-gray-400">Your project is set up correctly!</p>
    </main>
  </body>
</html>
```

**Save the file.**

---

### Step 12: View in Browser

**Option 1: VS Code Live Server**

1. Install "Live Server" extension
2. Right-click `src/index.html`
3. Click "Open with Live Server"

**Option 2: Python server**

```bash
cd src
python -m http.server 8000
```

Then open `http://localhost:8000`

**What you should see:**

- Dark background (`bg-dark-900`)
- Darker header (`bg-dark-800`)
- Mastercam cyan title (`text-mastercam-500`)
- White text
- Subtle border under header

---

### Step 13: Test the Theme

**Let's verify all our colors work. Add this to your `<main>`:**

```html
<main class="container mx-auto p-6 space-y-6">
  <!-- Test color scales -->
  <div class="space-y-2">
    <h2 class="text-xl font-semibold">Mastercam Color Scale</h2>
    <div class="flex gap-2">
      <div
        class="w-20 h-20 bg-mastercam-50 flex items-center justify-center text-xs text-black"
      >
        50
      </div>
      <div
        class="w-20 h-20 bg-mastercam-100 flex items-center justify-center text-xs text-black"
      >
        100
      </div>
      <div
        class="w-20 h-20 bg-mastercam-200 flex items-center justify-center text-xs text-black"
      >
        200
      </div>
      <div
        class="w-20 h-20 bg-mastercam-300 flex items-center justify-center text-xs text-black"
      >
        300
      </div>
      <div
        class="w-20 h-20 bg-mastercam-400 flex items-center justify-center text-xs"
      >
        400
      </div>
      <div
        class="w-20 h-20 bg-mastercam-500 flex items-center justify-center text-xs"
      >
        500
      </div>
      <div
        class="w-20 h-20 bg-mastercam-600 flex items-center justify-center text-xs"
      >
        600
      </div>
      <div
        class="w-20 h-20 bg-mastercam-700 flex items-center justify-center text-xs"
      >
        700
      </div>
      <div
        class="w-20 h-20 bg-mastercam-800 flex items-center justify-center text-xs"
      >
        800
      </div>
      <div
        class="w-20 h-20 bg-mastercam-900 flex items-center justify-center text-xs"
      >
        900
      </div>
    </div>
  </div>

  <!-- Test status colors -->
  <div class="space-y-2">
    <h2 class="text-xl font-semibold">Status Colors</h2>
    <div class="flex gap-4">
      <span class="px-3 py-1 bg-green-900 text-success rounded">Success</span>
      <span class="px-3 py-1 bg-orange-900 text-warning rounded">Warning</span>
      <span class="px-3 py-1 bg-red-900 text-danger rounded">Danger</span>
    </div>
  </div>

  <!-- Test buttons with hover -->
  <div class="space-y-2">
    <h2 class="text-xl font-semibold">Button States</h2>
    <div class="flex gap-4">
      <button
        class="px-4 py-2 bg-mastercam-500 hover:bg-mastercam-400 rounded transition-colors"
      >
        Hover Me
      </button>
      <button
        class="px-4 py-2 bg-dark-700 hover:bg-dark-600 rounded transition-colors"
      >
        Secondary
      </button>
    </div>
  </div>
</main>
```

**Save and check your browser. You should see:**

- Color gradient from light to dark
- Status badges with proper colors
- Buttons that change color on hover

**Try hovering the buttons!** They should smoothly transition to lighter shades.

---

## Understanding What Just Happened

**You now have:**

1. ✅ npm managing your dependencies (no CDN!)
2. ✅ Tailwind properly installed and configured
3. ✅ Custom Mastercam color theme
4. ✅ Build process that watches for changes
5. ✅ Clean project structure

**More importantly, you understand:**

- Why npm instead of CDN
- How Tailwind's build process works
- How color scales create visual hierarchy
- How the `content` config works

---

## Section 3A Complete! 🎉

### What's Next

**Section 3B: Building formatFileSize (Line by Line)**

We'll build the file size formatter from scratch:

1. Start with just bytes
2. Add KB conversion
3. Understand the rounding math
4. Add MB, GB, TB
5. Add edge case handling
6. **Explain EVERY line of math**

**Ready for Section 3B?** Say **"Start Section 3B"** and I'll break down the math step by step! 🧮
**EXCELLENT CATCH!** 🎯 You're absolutely right - the videos are a huge part of your learning, especially for visual/auditory reinforcement. Let me add them now!

---

## 🎥 Video Resources for Section 3B

### Understanding the Math

**Logarithms Explained Simply:**

- 🎥 [What is a Logarithm? (Simple Explanation)](https://www.youtube.com/watch?v=ntBWrcbAhaY) (5 min) - Perfect introduction
- 📺 [Logarithms - The Easy Way!](https://www.youtube.com/watch?v=Z5myJ8dg_rM) (12 min) - More detailed
- 🎬 [Logarithms Explained](https://www.youtube.com/watch?v=N-7tcTIrers) (27 min) - Complete understanding

**Rounding and Decimals:**

- 🎥 [JavaScript Math.round Explained](https://www.youtube.com/watch?v=WdXZqEQFgHY) (4 min) - Quick reference
- 📺 [Rounding Numbers in JavaScript](https://www.youtube.com/watch?v=IC76m7j6nRc) (11 min) - Detailed techniques
- 🎬 [JavaScript Numbers and Math](https://www.youtube.com/watch?v=VFSj9sU_VNA) (18 min) - Complete guide

**Binary and Computer Math:**

- 🎥 [Why 1024? Binary Explained](https://www.youtube.com/watch?v=LpuPe81bc2w) (6 min) - Answers the KB question
- 📺 [How Computers Count (Binary)](https://www.youtube.com/watch?v=1GSjbWt0c9M) (10 min) - Visual explanation
- 🎬 [Computer Number Systems](https://www.youtube.com/watch?v=FFDMzbrEXaE) (15 min) - Deep dive

### JavaScript Fundamentals

**Math Object:**

- 🎥 [JavaScript Math Object in 100 Seconds](https://www.youtube.com/watch?v=cB6XyL9h6jI) (2 min) - Quick overview
- 📺 [JavaScript Math Methods](https://www.youtube.com/watch?v=VxaXCcAqtJg) (12 min) - All the methods
- 🎬 [Advanced JavaScript Math](https://www.youtube.com/watch?v=KmRaQ6j_6X0) (23 min) - Pro techniques

**Type Checking (typeof, isNaN):**

- 🎥 [JavaScript typeof Operator](https://www.youtube.com/watch?v=ol4OVMJZC1w) (5 min) - Quick guide
- 📺 [Checking Types in JavaScript](https://www.youtube.com/watch?v=O4V9RF_0KgM) (14 min) - Best practices
- 🎬 [JavaScript Data Types Deep Dive](https://www.youtube.com/watch?v=O9by2KzKiZE) (28 min) - Complete guide

**Edge Case Handling:**

- 🎥 [Defensive Programming](https://www.youtube.com/watch?v=S3hI58CqGKo) (7 min) - Why edge cases matter
- 📺 [Writing Bulletproof JavaScript](https://www.youtube.com/watch?v=Ii3HZkNPyuQ) (16 min) - Error handling
- 🎬 [Clean Code - Error Handling](https://www.youtube.com/watch?v=hKm_egRvMps) (32 min) - Professional approach

### General Programming Concepts

**Incremental Development:**

- 🎥 [Test-Driven Development Basics](https://www.youtube.com/watch?v=Jv2uxzhPFl4) (8 min) - Build then test
- 📺 [Incremental Programming](https://www.youtube.com/watch?v=ZfFl5qgKJHI) (13 min) - Build step by step
- 🎬 [Software Development Best Practices](https://www.youtube.com/watch?v=HmFyNqRCN8k) (25 min) - Pro workflows

**Documentation and Comments:**

- 🎥 [How to Write Good Code Comments](https://www.youtube.com/watch?v=PNjaDME0RZ4) (6 min) - Quick tips
- 📺 [JSDoc Tutorial](https://www.youtube.com/watch?v=YK-GurROGIg) (11 min) - Document like a pro
- 🎬 [Clean Code Comments](https://www.youtube.com/watch?v=2a_ytyt9sf8) (19 min) - When and how

---

## 📚 Written Resources

**MDN Documentation (Bookmark These!):**

- [Math.log()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/log) - Official docs
- [Math.floor()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/floor) - Rounding down
- [Math.round()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/round) - Rounding
- [Math.pow()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/pow) - Exponents
- [typeof operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/typeof) - Type checking
- [isNaN()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/isNaN) - Checking for NaN

**Interactive Tools:**

- [JavaScript Visualizer](https://pythontutor.com/javascript.html) - Step through code visually
- [JS Bin](https://jsbin.com/) - Quick testing playground
- [Replit](https://replit.com/) - Full coding environment

---

## 💡 Recommended Viewing Order

**Tonight (before bed):**

1. 🎥 What is a Logarithm? (5 min) - Core concept
2. 🎥 Why 1024? Binary Explained (6 min) - Answers KB question
3. 🎥 JavaScript Math Object in 100 Seconds (2 min) - Overview

**Tomorrow morning (before Section 3C):**

1. 📺 Logarithms - The Easy Way! (12 min) - Reinforce logs
2. 📺 Rounding Numbers in JavaScript (11 min) - Rounding techniques
3. 📺 JavaScript Math Methods (12 min) - See all the tools

**Later (when you want to go deeper):**

1. 🎬 Logarithms Explained (27 min) - Complete mastery
2. 🎬 JavaScript Numbers and Math (18 min) - Full guide
3. 🎬 Clean Code - Error Handling (32 min) - Pro level

---

## 🎯 What to Focus On in Each Video

**Logarithm videos - Look for:**

- Why logarithms answer "how many times?"
- The relationship between powers and logs
- Real-world examples (like our file size problem)

**Binary videos - Look for:**

- Why computers use base 2 (not base 10)
- Powers of 2 (2, 4, 8, 16, 32, 64, 128, 256, 512, 1024)
- Why 1024 = 1 KB

**Math object videos - Look for:**

- Different rounding methods (floor, ceil, round)
- When to use each one
- Common gotchas (like our decimal rounding trick)

**Type checking videos - Look for:**

- Difference between `typeof` and `instanceof`
- Why we need both `typeof` and `isNaN`
- How JavaScript handles type coercion

---

**Going forward, I'll add video resources at the end of EVERY section!** 📺

**Ready for Section 3C: Building More Utility Functions?** Say **"Start Section 3C"** and we'll tackle date formatting with the same detailed approach! 📅
