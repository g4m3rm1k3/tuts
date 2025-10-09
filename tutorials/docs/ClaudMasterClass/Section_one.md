# Section 1: UI Shell – Building the HTML Foundation

**Goal for This Section:** Create a basic HTML page that displays in the browser with proper structure. No styling, no interactivity yet—just understanding the skeleton.

**Time:** 15-20 minutes

**What You'll Learn:**

- HTML5 document structure
- Semantic HTML tags and why they matter
- The viewport meta tag (critical for responsive design)
- How browsers interpret HTML

---

## Why Start Here?

Every web application needs a foundation. Before we add Python backends, databases, or fancy JavaScript, we need a page that can load in a browser. Think of this like setting up your CNC machine before running a program—you need the basic structure in place first.

---

## Step 1.1: Create the Project Structure

**Type this in your terminal:**

```bash
mkdir mastercam-pdm
cd mastercam-pdm
mkdir ui
cd ui
touch index.html
```

**What this does:**

- Creates your project folder
- Creates a `ui` folder for all frontend code
- Creates an empty `index.html` file

**Why separate folders?** Later you'll have `backend/` for Python and `ui/` for HTML/JS. Separation of concerns from the start.

---

## Step 1.2: The DOCTYPE Declaration

**Open `ui/index.html` and type this EXACTLY:**

```html
<!DOCTYPE html>
```

**What this line does:**

- Tells the browser "use modern HTML5 standards"
- Without it, browsers enter "quirks mode" (1990s compatibility mode with weird bugs)

**Why it matters:**
In quirks mode, CSS box sizing breaks, JavaScript APIs behave differently, and your app will have mysterious bugs. This one line prevents all that.

**Deep Dive (Optional):** Read about quirks mode: [MDN: Quirks Mode](https://developer.mozilla.org/en-US/docs/Web/HTML/Quirks_Mode_and_Standards_Mode) (3 min)

---

## Step 1.3: The HTML Root Element

**Add this line below DOCTYPE:**

```html
<html lang="en"></html>
```

**What this does:**

- Creates the root container for your entire page
- `lang="en"` declares the page is in English

**Why `lang` matters:**

- Screen readers use it to pronounce words correctly
- Search engines use it for language-specific results
- Browsers can offer translation based on it

**CNC Analogy:** This is like declaring your machine's coordinate system at the start of a G-code program.

---

## Step 1.4: The Head Section (Metadata)

**Add this below the `<html>` tag:**

```html
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Mastercam PDM</title>
</head>
```

**Let's break down each line:**

### `<meta charset="UTF-8" />`

- Declares character encoding (how text is stored as bytes)
- UTF-8 supports all languages, symbols, emojis
- Without it: Special characters like `°` or `é` display as `�` (mojibake)

### `<meta name="viewport" content="width=device-width, initial-scale=1.0" />`

This is **critical** for responsive design on tablets/phones (important for shop floor tablets).

- `width=device-width`: Page width = device screen width (not a zoomed-out desktop view)
- `initial-scale=1.0`: Don't auto-zoom on mobile

**What happens without it:** On a tablet, your page renders at 980px width and zooms out, making everything tiny. Users have to pinch-zoom to read anything.

**Test it later:** Remove this line, view on a phone—everything is microscopic.

### `<title>Mastercam PDM</title>`

- Text shown in the browser tab
- Shows in bookmarks
- Used by search engines

---

## Step 1.5: The Body Section (Visible Content)

**Add this below the closing `</head>` tag:**

```html
<body>
  <header>
    <h1>Mastercam PDM</h1>
  </header>

  <main>
    <p>Loading files...</p>
  </main>
</body>
```

**Don't forget to close the `<html>` tag at the very end:**

```html
</html>
```

### Understanding Semantic HTML

**Why `<header>` instead of `<div>`?**

Both would display the same, but semantic tags are self-documenting:

- A developer reads `<header>` and immediately knows "navigation section"
- Screen readers announce "Banner" when entering `<header>`
- Search engines know this is the site header, not just a styled div

**Why `<main>`?**

- Marks the primary content of the page
- Only ONE `<main>` per page (tells browsers/readers "this is the main content")
- Accessibility tools can skip directly to `<main>` (skip navigation)

**Why `<h1>`?**

- Heading hierarchy: `<h1>` = most important, `<h6>` = least
- Search engines weight `<h1>` content heavily
- Screen readers use headings to navigate (users jump from heading to heading)
- **Rule:** Only one `<h1>` per page

**CNC Analogy:** Semantic HTML is like using proper G-code structure (G54 for work offsets, M03 for spindle) instead of just moving axes with G01 commands. Both work, but one is maintainable.

---

## Step 1.6: Your Complete HTML So Far

**Your `index.html` should look like this:**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Mastercam PDM</title>
  </head>
  <body>
    <header>
      <h1>Mastercam PDM</h1>
    </header>

    <main>
      <p>Loading files...</p>
    </main>
  </body>
</html>
```

---

## Step 1.7: View Your Page

**Option A: Double-click the file**

- Find `index.html` in your file explorer
- Double-click to open in your default browser

**Option B: Use VS Code Live Server (Recommended)**

- Install "Live Server" extension in VS Code
- Right-click `index.html` → "Open with Live Server"
- Page auto-refreshes when you save changes

**What you should see:**

- "Mastercam PDM" as a large bold heading
- "Loading files..." below it
- Plain white background, black text

**It's ugly—that's okay!** We haven't added any CSS yet. You're seeing pure HTML structure.

---

## Experiment (5 minutes)

Try these modifications to understand HTML:

### Experiment 1: Break the DOCTYPE

```html
<!-- Remove or comment out the DOCTYPE line -->
<!-- <!DOCTYPE html> -->
```

Save and refresh. Notice any differences? (Probably not visible yet, but the browser is now in quirks mode)

**Put it back before continuing.**

### Experiment 2: Multiple `<main>` tags

```html
<main>
  <p>Loading files...</p>
</main>
<main>
  <p>Another main section</p>
</main>
```

Save and refresh. It displays, but if you check the browser console (F12), you might see a warning. **HTML allows it but it's invalid—confuses accessibility tools.**

**Remove the second `<main>` before continuing.**

### Experiment 3: Remove viewport meta

Comment out the viewport line:

```html
<!-- <meta name="viewport" content="width=device-width, initial-scale=1.0" /> -->
```

If you have a phone/tablet, view the page. Everything is tiny. **Restore the line.**

---

## Key Takeaways

✅ **DOCTYPE** = modern standards mode (always include)  
✅ **`<head>`** = metadata (not visible on page)  
✅ **`<body>`** = visible content  
✅ **Semantic tags** (`<header>`, `<main>`) = self-documenting, accessible  
✅ **Viewport meta** = responsive design foundation  
✅ **`<h1>`** = one per page, primary heading

---

## What's Next?

In **Section 2**, we'll add Tailwind CSS to make this look professional:

- Full-height layout
- Modern styling
- Responsive flexbox

Then **Section 3** adds buttons and basic JavaScript event handling.

---

## Checkpoint Questions (Test Your Understanding)

1. What happens if you remove the DOCTYPE?
2. Why use `<header>` instead of `<div class="header">`?
3. What does `width=device-width` do?
4. How many `<main>` tags should a page have?

<details>
<summary>Answers</summary>

1. Browser enters quirks mode (1990s compatibility with bugs)
2. Semantic HTML is self-documenting and accessible to screen readers
3. Makes the page width match the device screen (no tiny zoom-out on mobile)
4. Exactly one per page
</details>

---

**Ready for Section 2?** Let me know and I'll write the Tailwind CSS styling section with the same depth and incremental approach.
