Perfect — that’s an **excellent foundation step** before diving any deeper.
Understanding **how to talk to your computer** — through its terminal or shell — is fundamental to all programming, automation, and development work.

Let’s build a **complete “Terminal Mastery” module** that’s deep enough to serve as a searchable reference for you later.
We’ll cover **Windows (PowerShell & CMD)**, **macOS (zsh/bash)**, and **cross-platform habits** so you can move comfortably between both environments.

---

# 🧠 Module 0 – Terminal & Shell Mastery

_(Prerequisite to Module 1: Git Plumbing)_

---

## 0.1 What Is a Terminal, Shell, and Command-Line?

### 🖥️ Terminal

A **terminal** (or console) is just a **window** where you type commands that your computer executes.
It’s not the thing doing the work — it’s the **interface**.

Examples:

- **Windows Terminal**, **PowerShell Console**, **CMD**, **macOS Terminal**, **iTerm2**

### 🐚 Shell

The **shell** is the **interpreter** — it reads what you type, parses it, and runs the command.

| OS      | Common Shells                                     | Notes                              |
| ------- | ------------------------------------------------- | ---------------------------------- |
| Windows | `cmd.exe`, `PowerShell`, `pwsh` (PowerShell Core) | PowerShell is modern, object-based |
| macOS   | `zsh` (default), `bash`, `fish`                   | Text-based, great for scripting    |
| Linux   | `bash`, `zsh`, `sh`                               | Core of most dev environments      |

### ⚙️ Command Interpreter

When you type:

```bash
ls -l
```

The shell:

1. Parses command (`ls`)
2. Passes arguments (`-l`)
3. Calls the executable (`/bin/ls`)
4. Displays output to **stdout** (screen)

---

## 0.2 CMD vs PowerShell vs Bash/zsh

| Feature             | CMD                | PowerShell                     | Bash/zsh            |
| ------------------- | ------------------ | ------------------------------ | ------------------- |
| Object vs Text      | Text only          | Object-based (.NET objects)    | Text only           |
| Piping              | Text stream        | Object stream                  | Text stream         |
| Aliases             | Limited            | Extensive (ls → Get-ChildItem) | Extensive           |
| Scripting           | Batch files (.bat) | PowerShell scripts (.ps1)      | Shell scripts (.sh) |
| Automation Strength | Basic              | Enterprise-level               | Dev-level           |
| Cross-platform      | No                 | Yes (PowerShell Core)          | Yes                 |

**Key idea:**

- PowerShell is closer to **Python** in structure (objects, functions, pipelines).
- Bash/zsh is more like **C-style syntax** and built for Unix tools.

---

## 0.3 PowerShell Basics

### 🔹 Getting Around

```powershell
pwd          # Print working directory
ls           # List directory (alias for Get-ChildItem)
cd ..        # Move up
cd path      # Move to folder
mkdir newDir # Make directory
rm file.txt  # Remove file
```

### 🔹 Commands (cmdlets)

PowerShell uses a **Verb-Noun** pattern:

```powershell
Get-Process
Start-Service
Stop-Computer
New-Item
```

Each command outputs **objects**, not plain text.
This means you can do:

```powershell
Get-Process | Where-Object {$_.CPU -gt 50} | Select-Object Name,CPU
```

That’s **object filtering**, not text parsing like in Bash.

---

## 0.4 Bash/zsh Basics (macOS & Linux)

### 🔹 Getting Around

```bash
pwd           # print working directory
ls -la        # list all files long format
cd ..         # move up
cd path       # move to folder
mkdir newDir  # make directory
rm file.txt   # remove file
```

### 🔹 Piping and Redirection

```bash
ls | grep ".txt"        # filter list for .txt
ls > files.txt          # redirect to file
cat files.txt | less    # scroll through file
```

### 🔹 Permissions & Execution

```bash
chmod +x script.sh    # make executable
./script.sh           # run script
```

---

## 0.5 Creating Bash-Like Commands in PowerShell

Since PowerShell doesn’t include all the small Unix utilities by default (like `touch`, `cat`, etc.), we can define **aliases** or **functions** in your PowerShell profile.

### 🧩 Find your PowerShell profile

```powershell
$PROFILE
```

You’ll see something like:

```
C:\Users\<you>\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
```

If it doesn’t exist:

```powershell
New-Item -Path $PROFILE -ItemType File -Force
```

Now open it:

```powershell
notepad $PROFILE
```

### 🔧 Add Custom Functions

```powershell
# touch equivalent – create empty file if not exists
function touch($path) {
    if (!(Test-Path $path)) {
        New-Item -ItemType File -Path $path | Out-Null
    } else {
        (Get-Item $path).LastWriteTime = Get-Date
    }
}

# cat equivalent – show file content
function cat($path) {
    Get-Content $path
}

# grep equivalent – case-insensitive search
function grep($pattern, $file) {
    Select-String -Pattern $pattern -Path $file
}

# clear alias for cls
Set-Alias clear Clear-Host
```

Save the file and reload your profile:

```powershell
. $PROFILE
```

Now you can use:

```powershell
touch test.txt
cat test.txt
grep "pattern" test.txt
clear
```

---

## 0.6 Useful PowerShell & Bash Utilities

| Task           | PowerShell                             | Bash/zsh               |
| -------------- | -------------------------------------- | ---------------------- |
| Show processes | `Get-Process`                          | `ps aux`               |
| Disk usage     | `Get-PSDrive`                          | `df -h`                |
| Find files     | `Get-ChildItem -Recurse -Filter *.txt` | `find . -name "*.txt"` |
| Search text    | `Select-String "foo"`                  | `grep "foo"`           |
| Copy files     | `Copy-Item`                            | `cp`                   |
| Move files     | `Move-Item`                            | `mv`                   |
| Delete         | `Remove-Item`                          | `rm`                   |
| Download file  | `Invoke-WebRequest`                    | `curl` or `wget`       |
| Permissions    | `icacls`                               | `chmod/chown`          |

---

## 0.7 Cross-Platform Tips

- Use **PowerShell Core (`pwsh`)** — runs the same on Windows/macOS/Linux.
- Store scripts in `.ps1` and `.sh` versions.
- Always test file path behavior (`/` vs `\`).
- Use environment variables (`$env:Path` in PowerShell, `$PATH` in Bash).

---

## 0.8 Practice Exercises

1. Create a PowerShell function to open your most-used project folder with one command.
2. Write a small script that lists all `.py` files larger than 1MB.
3. Write a Bash function called `mkcd` that makes a directory and jumps into it:

   ```bash
   mkcd() { mkdir -p "$1" && cd "$1"; }
   ```

4. Recreate that same function in PowerShell.

---

## 0.9 Resources

- 📘 [PowerShell Official Docs](https://learn.microsoft.com/en-us/powershell/)
- 📗 [Bash Manual](https://www.gnu.org/software/bash/manual/)
- 🧭 [Learn Command Line the Hard Way](https://learnpythonthehardway.org/book/appendixa.html)
- 🧰 [iTerm2 (macOS Terminal Replacement)](https://iterm2.com/)
- ⚙️ [Windows Terminal](https://github.com/microsoft/terminal)

---

Next, we can move to **Module 1: Git Plumbing** with a much stronger foundation — and we’ll use these new shell commands to explore Git’s internals interactively.

---

Would you like me to include a **PowerShell profile template** with a bunch of commonly used “bash-like” aliases and helper functions next?
(You can just drop it into `$PROFILE` to make your shell behave more like Linux.)
