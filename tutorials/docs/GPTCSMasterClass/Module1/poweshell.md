Nice — let’s build a practically useful, **line-by-line PowerShell masterclass** you can type along with, remember, and drop into your `$PROFILE` or module when you need it. I’ll explain _why_ each bit exists, _how_ it behaves differently from bash, and give safe, legitimate workarounds for common corporate restrictions (but **I will not** show ways to bypass workplace security or privilege restrictions — I’ll explain safe alternatives instead).

---

# PowerShell Masterclass — hands-on, bite-sized, explain-every-line

## 0 — Safety first (short)

You asked about bypassing permissions at work. I won’t help with instructions to evade security controls or gain unauthorized access.
What I _will_ show:

- Legitimate ways to work inside restricted environments (create venvs in user folders, use `--user` installs, use WSL/Docker if allowed, use `python` inside venv without activation).
- How to request admin changes or sign scripts properly.
  If your company blocks running activation scripts or installing modules, the correct route is to ask IT for exception or use an allowed environment (WSL/Docker/portable Python). I’ll show practical workarounds that don’t require changing policies.

---

## 1 — Quick PowerShell concepts you must know (3 things)

1. **PowerShell pipes objects, not text.** Everything you pipe is a .NET object with properties. That changes how you filter/format.

   - Example: `Get-Process | Where-Object {$_.CPU -gt 100} | Select-Object Name,CPU`

2. **Cmdlets follow `Verb-Noun`** naming. They have parameters, not ad-hoc flags like many UNIX tools.

   - Example: `Get-ChildItem -Recurse -Filter *.py`

3. **Profiles are just scripts that run at shell start.** Put functions, aliases, and import-module calls there.

---

## 2 — Create and live-edit your PowerShell profile (type, explain, run)

### 2.1 Check where your profile lives

```powershell
# Shows the path PowerShell uses for your current shell/profile
$PROFILE
```

**Why:** There are several profiles (AllUsers, CurrentUser, CurrentHost). `$PROFILE` points to the current user + current host file, e.g. `C:\Users\<you>\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`.

### 2.2 Create the file if missing

```powershell
# Create the profile file (creates path if missing)
if (!(Test-Path -Path $PROFILE)) {
  New-Item -ItemType File -Path $PROFILE -Force | Out-Null
}
notepad $PROFILE   # open it for editing (Windows). On macOS: code $PROFILE or open -a TextEdit $PROFILE
```

**Why:** `$PROFILE` runs every time you start PowerShell (or VSCode integrated terminal). Putting functions here makes them available every session.

---

## 3 — Minimal, safe `$PROFILE` structure (step-by-step)

We’ll build this incrementally. Type each block, save, then reload with `. $PROFILE` to see the effects without restarting.

### 3.1 A header and strictness

```powershell
# ~~~ profile header ~~~
Set-StrictMode -Version Latest     # catches uninitialized variables and bad access
$ErrorActionPreference = 'Stop'    # treat errors as terminating by default (safer scripts)
```

**Why:** `Set-StrictMode` helps you catch silly bugs early. `ErrorActionPreference` reduces silent failures.

### 3.2 Load a helpers file (we’ll create it)

```powershell
$MyModuleDir = Join-Path $HOME 'Documents\PowerShell\MyProfile'  # central place for your functions
if (!(Test-Path $MyModuleDir)) { New-Item -ItemType Directory -Path $MyModuleDir | Out-Null }
$helpers = Join-Path $MyModuleDir 'helpers.ps1'
if (Test-Path $helpers) { . $helpers }   # dot-source the file (load its functions into session)
```

**Why:** Keep large bodies of work in a separate file (`helpers.ps1`) and dot-source it into `$PROFILE`. Clean and modular.

Reload:

```powershell
. $PROFILE
```

---

## 4 — Build `helpers.ps1` piece-by-piece (no dumps — tiny bits, explained)

Create `helpers.ps1` at the path above. We’ll add small functions one at a time and explain.

### 4.1 `touch` — create-or-update a file

Type this into `helpers.ps1`:

```powershell
function touch {
    param([string]$Path)
    # If file doesn't exist, New-Item creates it. If it exists, update LastWriteTime.
    if (!(Test-Path -LiteralPath $Path)) {
        New-Item -ItemType File -Path $Path | Out-Null
    } else {
        # Get-Item returns a FileInfo object; set its LastWriteTime to now.
        (Get-Item -LiteralPath $Path).LastWriteTime = Get-Date
    }
}
```

**Explain each line**

- `function touch { ... }` defines a named function.
- `param([string]$Path)` declares an input parameter (type-safe).
- `Test-Path` checks existence.
- `New-Item` creates the file.
- `Get-Item` gives access to the file object whose `LastWriteTime` property we update.

Try it:

```powershell
. $PROFILE        # reload helpers
touch .\foo.txt
ls -l foo.txt
```

### 4.2 `mkcd` — make directory and go there

Add to `helpers.ps1`:

```powershell
function mkcd {
    param([string]$Dir)
    # -Force avoids errors if exists; -ErrorAction Stop makes it throw on unexpected failures
    New-Item -ItemType Directory -Path $Dir -Force -ErrorAction Stop | Out-Null
    Set-Location -Path $Dir
}
```

**Why:** Duplicate UNIX convenience. `New-Item -Force` acts like `mkdir -p`.

Test:

```powershell
mkcd my/new/project
pwd
```

### 4.3 `cat` — show file content (alias for Get-Content)

Add:

```powershell
function cat { param([string]$Path) Get-Content -LiteralPath $Path }
Set-Alias -Name cat -Value Get-Content -Scope Global -Option AllScope
```

**Why:** `Get-Content` is the proper cmdlet; alias makes it familiar.

### 4.4 `grep` — wrapper for Select-String

Add:

```powershell
function grep {
    param(
        [Parameter(Mandatory=$true, Position=0)] [string]$Pattern,
        [Parameter(Position=1)] [string[]]$Paths = @('.')
    )
    # Select-String returns MatchInfo objects (file, line, lineNumber)
    Select-String -Pattern $Pattern -Path $Paths -SimpleMatch
}
```

**Why:** `Select-String` is the PowerShell analog to `grep`. We return objects, so downstream can be processed (e.g., `.Line`, `.Filename`).

Test:

```powershell
'one','two','three' | Out-File sample.txt
grep two sample.txt
```

### 4.5 `head` and `tail` (efficient top/bottom lines)

Add:

```powershell
function head { param([string]$Path, [int]$Lines=10) Get-Content -LiteralPath $Path -TotalCount $Lines }
function tail { param([string]$Path, [int]$Lines=10) Get-Content -LiteralPath $Path -Tail $Lines }
```

**Why:** `Get-Content` supports `-TotalCount` and `-Tail`; no external `head`/`tail` needed.

---

## 5 — Virtual environments (venv) in PowerShell — robust, cross-platform

### 5.1 Create a venv (safe, user-space)

Type:

```powershell
function New-Venv {
    param(
        [Parameter(Mandatory=$false)] [string]$Path = '.venv',
        [switch]$Force
    )

    if ((Test-Path -Path $Path) -and ( -not $Force )) {
        throw "Path already exists; use -Force to recreate."
    }

    # Use python -m venv so it works across platforms/py installs
    & python -m venv $Path
    Write-Output "Created venv at $Path"
}
```

**Why each line:**

- `& python -m venv $Path` ensures the `python` in PATH runs the venv creation.
- We don’t attempt to change execution policy or run activation scripts — we only create the venv.

Test:

```powershell
New-Venv -Path .venv
```

### 5.2 Activate venv _without_ relying on execution-policy-sensitive activation script

PowerShell activation uses `Activate.ps1`, which may be blocked by org policies. **Don’t** attempt to break policy. Instead use one of these safe options:

**Option A — run Python from venv directly (works if you only need to run scripts):**

```powershell
$venv = Join-Path (Get-Location) '.venv'
$py = Join-Path $venv 'Scripts\python.exe'    # Windows path
# then run:
& $py script.py
```

**Why:** You call venv's Python directly; no activation script is required.

**Option B — temporarily add venv Scripts to PATH in the session**

```powershell
# This only affects the current PowerShell session
$venvScripts = Join-Path (Get-Location) '.venv\Scripts'
$env:PATH = "$venvScripts;$env:PATH"
# Now running 'python' resolves to venv python for current session
python -V
```

**Why:** Short-lived PATH tweak avoids changing machine policy. When you close the session, PATH reverts.

**Option C — use `pip install --user` or `pipx` for global user-level executables**

- `pip install --user <package>` installs binaries to user-profile paths.
- `pipx install <cli>` installs CLI tools in an isolated environment (great for tools like `black`, `httpie`).

---

## 6 — Advanced function example — `New-Venv` with activation helper (advanced, safe)

Add to `helpers.ps1`:

```powershell
function Use-Venv {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true, Position=0)] [string]$Path
    )

    $scripts = Join-Path $Path 'Scripts'
    if (-not (Test-Path $scripts)) { throw "No venv Scripts folder found at $scripts" }

    # Temporarily adjust PATH for this session
    $originalPath = $env:PATH
    $env:PATH = "$scripts;$env:PATH"
    Write-Host "Activated venv for this session. Run 'deactivate' to restore PATH."

    # Provide a deactivation helper inside the session
    function global:deactivate {
        $env:PATH = $originalPath
        Remove-Item Function:deactivate
        Write-Host "Deactivated venv (session PATH restored)."
    }
}
```

**Explain:**

- `Use-Venv .venv` modifies current session PATH to prefer venv python.
- It creates a `deactivate` function inside session to revert PATH. This avoids running `Activate.ps1` and respects execution policy. It’s session-local and non-persistent.

Test:

```powershell
Use-Venv .venv
python -V   # should show venv python
deactivate
python -V   # original python restored
```

---

## 7 — Scripts vs Functions vs Modules — when to use what

- **Function**: Small utilities you type frequently. Put in `helpers.ps1`.
- **Script (.ps1)**: A runnable file for a task (e.g., deploy.ps1). Users call it directly. Might be blocked by execution policy.
- **Module (.psm1 + .psd1)**: Reusable package with exported functions. Place under `Documents\PowerShell\Modules\YourModule\YourModule.psm1` then `Import-Module YourModule`.

Create a tiny module (explained steps):

1. Create folder:

```powershell
$modPath = Join-Path $HOME 'Documents\PowerShell\Modules\MyTools'
New-Item -ItemType Directory -Path $modPath -Force | Out-Null
```

2. Put this in `MyTools.psm1`:

```powershell
function Get-Hello { param($Name='World') "Hello, $Name" }
Export-ModuleMember -Function Get-Hello
```

3. Use it:

```powershell
Import-Module MyTools
Get-Hello -Name Michael
```

**Why modules:** cleaner namespace, easier to distribute, autoloading, and easier to unit-test.

---

## 8 — Parameter validation, help, and good script hygiene (single bite)

Create an advanced function example:

```powershell
function Invoke-Safe {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true, Position=0)]
        [ValidateNotNullOrEmpty()]
        [string]$Command
    )

    Write-Verbose "Running: $Command"
    try {
        Invoke-Expression $Command
    } catch {
        Write-Error "Command failed: $_"
        throw
    }
}
```

**Why:**

- `[CmdletBinding()]` makes the function behave like a cmdlet (supports `-Verbose`, `-ErrorAction`, etc.).
- `[ValidateNotNullOrEmpty()]` early checks.
- `try/catch` for controlled error handling.

**Best practice:** avoid `Invoke-Expression` when possible (it executes arbitrary string code). Use direct cmdlet invocation for safety.

---

## 9 — Debugging & introspection utilities

- Put `Set-PSDebug -Trace 1` if you want to trace each line executed (useful for learning but noisy).
- Use `Write-Verbose`, `Write-Debug`, and pass `-Verbose`/`-Debug` when calling functions.
- Inspect function code: `Get-Command touch | Select-Object -ExpandProperty ScriptBlock`.

---

## 10 — Tab completion & argument completers (small example)

Add a simple completer that suggests directories for `mkcd`:

```powershell
Register-ArgumentCompleter -CommandName mkcd -ParameterName Dir -ScriptBlock {
    param($commandName, $parameterName, $wordToComplete, $commandAst, $fakeBoundParameters)
    Get-ChildItem -Directory -Name -ErrorAction SilentlyContinue | Where-Object { $_ -like "$wordToComplete*" } |
        ForEach-Object { [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_) }
}
```

**Why:** Makes custom functions feel native with tab completion.

---

## 11 — Useful modules & ecosystem (install per-user)

Install per-user (no admin):

```powershell
Install-Module -Name PSReadLine -Scope CurrentUser -Force
Install-Module -Name Pscx -Scope CurrentUser -Force   # community extensions (optional)
Install-Module -Name posh-git -Scope CurrentUser -Force
```

**Why:** `PSReadLine` improves history/navigation. `posh-git` integrates git status into your prompt. These are installed into user scope and don’t need admin rights (unless corporate policy forbids module install).

---

## 12 — Cheatsheet — common conversions (bash → PowerShell)

| Bash           | PowerShell                            |
| -------------- | ------------------------------------- |
| `ls -la`       | `Get-ChildItem -Force` or `ls -Force` |
| `cat file`     | `Get-Content file` or `cat file`      |
| `grep`         | `Select-String -Pattern 'foo'`        |
| `head -n 10`   | `Get-Content -TotalCount 10`          |
| `tail -f`      | `Get-Content -Wait -Tail 10`          |
| `export VAR=1` | `$env:VAR = '1'`                      |
| `which cmd`    | `Get-Command cmd`                     |

---

## 13 — Exercises to lock it in (do these & commit)

1. Create `helpers.ps1` and implement `touch`, `mkcd`, `cat`, `grep`, `head`, `tail`. Reload profile and use them on some sample files.
2. Create a `.venv` with `New-Venv`, then run Python from the venv using `Use-Venv` and `deactivate`.
3. Make a tiny module `MyTools` with `Get-Hello`, install it under `Documents\PowerShell\Modules`, `Import-Module`, and call `Get-Hello`.
4. Add `posh-git` and `PSReadLine` with `Install-Module -Scope CurrentUser`. Configure a simple prompt in profile to show git branch (posh-git docs walk-through).
5. Add an argument completer for `mkcd` and test tab completion.

Commit each step to a git repo and add short commit messages like `feat(profile): add touch and mkcd`.

---

## 14 — Where to read next (exact search phrases)

- `PowerShell profile path $PROFILE`
- `PowerShell dot-sourcing vs import-module`
- `PowerShell advanced function CmdletBinding example`
- `PowerShell Register-ArgumentCompleter example`
- `python venv activation windows powershell executionpolicy`
- `PowerShell Set-StrictMode examples`
- `PowerShell Install-Module CurrentUser`

---

## Closing and next steps

I didn’t show ways to evade execution policy or escalate privileges. If activation scripts are blocked at work, use the safe alternatives above:

- call the venv python directly,
- temporarily add the venv `Scripts` folder to `$env:PATH` for the session,
- install packages with `pip install --user` or `pipx`,
- request IT to sign your scripts or provide a permitted dev environment (WSL or Docker).

If you want, I’ll:

- produce a ready-to-paste `helpers.ps1` and `$PROFILE` template (with comments) you can import, or
- generate a short interactive lab (one file) you can run to create all functions and test them step-by-step.

Which do you want next — the **profile + helpers template** to paste into `$PROFILE`, or the **interactive lab script** that walks you through each step?
