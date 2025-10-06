# PDM Tutorial - Stage 0: Professional Development Environment

**Prerequisites**: None. We start from scratch.

**Time**: 2-4 hours

**What you'll build**: A properly configured development environment with professional project structure.

---

### 0.1: Initial Project Structure

Create this exact structure:

```bash
## Create root directory
mkdir pdm-tutorial
cd pdm-tutorial

## Create backend structure
mkdir -p backend/app
mkdir -p backend/static/css
mkdir -p backend/static/js/modules
mkdir -p backend/tests

## Create placeholder files
touch backend/app/__init__.py
touch backend/app/main.py
touch backend/static/index.html
touch backend/static/js/app.js
touch backend/.env.example
touch backend/.gitignore
touch README.md
```

**Why this structure now?**

- `backend/app/`: Makes your code a proper Python package, not just scripts
- `static/css/`, `static/js/modules/`: Organized assets from the start
- `tests/`: Professional projects have tests from day one
- `.env.example`: Template for configuration (never commit secrets)

---

### 0.2: Python Installation & Virtual Environments

#### Install Python 3.11+

- **Windows**: Download from python.org, **CHECK "Add Python to PATH"**
- **macOS**: `brew install python@3.11`
- **Linux**: `sudo apt install python3.11 python3.11-venv`

#### Create Virtual Environment

```bash
cd backend
python -m venv venv
```

**Deep Dive: What is `venv`?**

`venv` creates an isolated Python environment. Here's what actually happens:

1. **Copies Python interpreter** into `venv/bin/python` (or `venv/Scripts/python.exe` on Windows)
2. **Creates `site-packages` directory** at `venv/lib/python3.11/site-packages` where packages install
3. **Modifies `sys.path`** when activated to prioritize this directory

**Activation modifies your shell's `PATH` environment variable** to prepend the venv's binary directory, so `python` resolves to the venv's interpreter.

#### Activate Virtual Environment

```bash
## Windows PowerShell
.\venv\Scripts\Activate.ps1

## macOS/Linux
source venv/bin/activate
```

You'll see `(venv)` in your prompt.

---

### 0.3: Deep Dive - Python's Import System

**Before writing code, understand how Python finds modules.**

#### The `sys.path` List

When you `import something`, Python searches these locations in order:

```python
## backend/app/understanding_imports.py
import sys
print("Python searches these directories for modules:")
for i, path in enumerate(sys.path, 1):
    print(f"{i}. {path}")
```

Run this:

```bash
python app/understanding_imports.py
```

You'll see:

1. The script's directory
2. Standard library location
3. `site-packages` (where pip installs go)
4. Your venv's `site-packages`

**Why `app/__init__.py` matters**: It tells Python "this directory is a package." Without it, you can't do `from app.services import something`.

#### Absolute vs Relative Imports

```python
## Absolute import (preferred)
from app.services.auth_service import verify_password

## Relative import (use sparingly)
from ..services.auth_service import verify_password  ## Go up one level, then into services

## Why absolute is better: Clear, works from anywhere, refactor-friendly
```

---

### 0.4: Type Hints - Python's Type System

**Python is dynamically typed but supports optional static type hints (PEP 484).**

Create this file to learn typing:

**File: `backend/app/learn_typing.py`**

## 🐍 Deep Dive into Python Typing

Python is dynamically typed: variables can change type at runtime. But sometimes we **want hints** to make code safer, easier to read, and easier to check before running. That’s where the `typing` module comes in.

---

### **Section 0: Introduction to `typing`**

```python
"""
Deep dive into Python's typing module.

Type hints don't enforce types at runtime - they are mainly for:
1. IDE autocomplete and error detection
2. Static analysis tools like mypy
3. Documentation
4. Optional runtime validation with libraries like Pydantic
"""
```

**Explanation:**

- These are **docstring comments** explaining the purpose of typing.
- Python itself won’t stop you from passing a `str` to a function expecting an `int`.
- Typing helps **humans and tools**: autocomplete, error catching, documentation generation.
- Later, frameworks like **Pydantic** can enforce types **at runtime**.

---

### **Section 1: Importing Typing and Other Modules**

```python
from typing import (
    List, Dict, Tuple, Set,        ## Generic container types
    Optional, Union,               ## Type combinations
    Any, TypeVar,                  ## Special types
    Callable,                      ## Function types
    Literal,                       ## Exact literal values
    Protocol                        ## Structural typing (duck typing)
)

from pathlib import Path           ## Filesystem paths, type-safe
from datetime import datetime     ## Working with timestamps
```

**Explanation:**

- `List[str]` means a list of strings.
- `Optional[str]` = `Union[str, None]`.
- `TypeVar` allows **generic functions** (functions that work with any type).
- `Protocol` allows **structural typing**, similar to duck typing but type-safe.

`Path` and `datetime` are **real-world modules** used in file handling and timestamps.

---

### **Section 2: Basic Type Hints**

```python
def greet(name: str) -> str:
    """
    Simple function with type hints.

    :param name: expects a string
    :return: returns a string
    """
    return f"Hello, {name}!"
```

**Explanation:**

- `name: str` → The parameter `name` must be a string.
- `-> str` → The function returns a string.
- Type hints **don’t enforce runtime types** but will give IDE errors if misused.
- The `f""` string is a **formatted string literal** (f-string) in Python 3.6+.

---

### **Section 3: Collections (`List`, `Dict`, `Tuple`)**

```python
def process_files(filenames: List[str]) -> Dict[str, int]:
    """
    Takes a list of filenames (strings) and returns a dictionary
    mapping filename to its length.
    """
    return {name: len(name) for name in filenames}
```

**Explanation:**

- `List[str]`: A list where all elements are strings.
- `Dict[str, int]`: A dictionary with string keys and integer values.
- The dictionary comprehension `{name: len(name) for name in filenames}` is **Pythonic** for mapping a transformation to a collection.

```python
def get_coordinates() -> Tuple[float, float]:
    """Return a tuple of two floats."""
    return (40.7128, -74.0060)  ## NYC latitude and longitude
```

**Explanation:**

- `Tuple[float, float]` → Exactly two floats in a tuple.
- Useful for **fixed-size collections**.

---

### **Section 4: Optional and Union**

```python
def find_user(user_id: int) -> Optional[Dict[str, str]]:
    """
    Might return a dictionary or None.
    Optional[X] is shorthand for Union[X, None]
    """
    if user_id == 1:
        return {"name": "Alice", "role": "admin"}
    return None
```

- `Optional[Dict[str, str]]` = `Dict[str, str]` or `None`.
- Helps **signal that a function might fail to find something**.

```python
def process_data(value: Union[int, str, List[int]]) -> str:
    """Handle multiple possible types with Union"""
    if isinstance(value, int):
        return f"Got integer: {value}"
    elif isinstance(value, str):
        return f"Got string: {value}"
    else:
        return f"Got list of {len(value)} integers"
```

**Explanation:**

- `Union[int, str, List[int]]` → `value` can be an int, str, or list of ints.
- Use `isinstance()` to check the type **safely**.
- Typing helps **document expectations** and allows tools to warn if you forget cases.

---

### **Section 5: Callable (Function Types)**

```python
def execute_twice(func: Callable[[int], int], value: int) -> int:
    """
    Executes a function twice: func(func(value))
    Callable[[int], int]: function takes int, returns int
    """
    return func(func(value))

def double(x: int) -> int:
    return x * 2
```

**Explanation:**

- `Callable[[int], int]` → A function that **takes an int and returns an int**.
- Typing functions allows **higher-order functions** safely.
- `execute_twice(double, 5)` → returns `20` because `double(5)` = 10, then `double(10)` = 20.

---

### **Section 6: TypeVar (Generics)**

```python
T = TypeVar('T')  ## Generic type variable

def get_first(items: List[T]) -> Optional[T]:
    """Return first item from a list, works with any type."""
    return items[0] if items else None
```

**Explanation:**

- `T` is a **placeholder type**.
- Works with `List[int]`, `List[str]`, etc.
- `Optional[T]` = might return `T` or `None`.

---

### **Section 7: Literal (Exact Values)**

```python
UserRole = Literal["admin", "user", "guest"]

def check_permission(role: UserRole) -> bool:
    """Check permission only for valid roles."""
    return role == "admin"
```

**Explanation:**

- `Literal["admin", "user", "guest"]` → Only accepts these exact strings.
- IDE will **autocomplete these values**, preventing typos.
- Useful for **enums without creating a full Enum class**.

---

### **Section 8: Protocol (Structural Typing)**

```python
from typing import Protocol

class Readable(Protocol):
    """Any object with a read() method matches this protocol."""
    def read(self) -> str: ...

def read_data(source: Readable) -> str:
    """Accepts anything with a read() method."""
    return source.read()
```

**Explanation:**

- Protocol allows **duck typing with type safety**.
- Any object with a `read()` method will match `Readable`.
- Works for **files, StringIO, custom classes**, etc.

---

### **Section 9: Real-World Example – File Lock**

```python
class FileLockData:
    """Represents a file lock entry."""
    filename: str
    user: str
    timestamp: datetime
    message: str

def create_lock(filename: str, user: str, message: str) -> Dict[str, Union[str, datetime]]:
    """
    Create a dictionary representing a file lock.
    IDEs and mypy will check types; runtime validation can use Pydantic.
    """
    return {
        "filename": filename,
        "user": user,
        "timestamp": datetime.now(),
        "message": message
    }
```

**Explanation:**

- Combines **basic types, collections, and datetime**.
- Typing allows **IDE hints** before runtime.
- Pydantic can **enforce these types at runtime**.

---

### **Section 10: Testing Your Understanding**

```python
if __name__ == "__main__":
    print(greet("World"))  ## Basic type hint

    files = ["file1.txt", "file2.txt"]
    print(process_files(files))  ## Collection types

    user = find_user(1)
    print(f"Found user: {user}")  ## Optional

    print(process_data(42))
    print(process_data("hello"))
    print(process_data([1, 2, 3]))  ## Union

    result = execute_twice(double, 5)
    print(f"Double twice: {result}")  ## Callable

    first_str = get_first(["a", "b", "c"])
    first_int = get_first([1, 2, 3])
    print(f"First string: {first_str}, First int: {first_int}")  ## Generic
```

**Explanation:**

- `__name__ == "__main__"` → Python idiom for **script entry point**.
- Prints test results for **all sections**, so you can see type hints in action.
- Helps **connect theory to real output**.

---

```python
"""
Deep dive into Python's typing module.
Type hints don't enforce types at runtime - they're for:
1. IDE autocomplete and error detection
2. Static analysis tools (mypy)
3. Documentation
4. Runtime validation (with Pydantic)
"""

from typing import (
    List, Dict, Tuple, Set,  ## Generic types
    Optional, Union,          ## Type combinations
    Any, TypeVar,            ## Special types
    Callable,                ## Function types
    Literal,                 ## Exact values
    Protocol                 ## Structural subtyping
)
from pathlib import Path
from datetime import datetime

## ============================================================================
## SECTION 1: Basic Type Hints
## ============================================================================

def greet(name: str) -> str:
    """
    Simple type hints: parameter 'name' must be str, returns str.
    """
    return f"Hello, {name}!"

## ============================================================================
## SECTION 2: Collection Types
## ============================================================================

def process_files(filenames: List[str]) -> Dict[str, int]:
    """
    List[str]: A list containing strings
    Dict[str, int]: A dictionary with string keys and integer values
    """
    return {name: len(name) for name in filenames}

def get_coordinates() -> Tuple[float, float]:
    """
    Tuple[float, float]: Exactly 2 floats
    """
    return (40.7128, -74.0060)  ## NYC coordinates

## ============================================================================
## SECTION 3: Optional and Union
## ============================================================================

def find_user(user_id: int) -> Optional[Dict[str, str]]:
    """
    Optional[X] is shorthand for Union[X, None]
    This function might return a dict or None.
    """
    if user_id == 1:
        return {"name": "Alice", "role": "admin"}
    return None  ## Not found

def process_data(value: Union[int, str, List[int]]) -> str:
    """
    Union[int, str, List[int]]: Can be int OR str OR List[int]
    Must handle all cases.
    """
    if isinstance(value, int):
        return f"Got integer: {value}"
    elif isinstance(value, str):
        return f"Got string: {value}"
    else:
        return f"Got list of {len(value)} integers"

## ============================================================================
## SECTION 4: Callable (Function Types)
## ============================================================================

def execute_twice(func: Callable[[int], int], value: int) -> int:
    """
    Callable[[int], int] means:
    - Takes a function that accepts one int parameter
    - That function returns an int
    """
    return func(func(value))

def double(x: int) -> int:
    return x * 2

## Usage: execute_twice(double, 5)  ## Returns 20

## ============================================================================
## SECTION 5: TypeVar (Generic Functions)
## ============================================================================

T = TypeVar('T')  ## Define a type variable

def get_first(items: List[T]) -> Optional[T]:
    """
    Generic function: works with any type.
    If you pass List[str], it returns Optional[str]
    If you pass List[int], it returns Optional[int]
    """
    return items[0] if items else None

## ============================================================================
## SECTION 6: Literal (Exact Values)
## ============================================================================

from typing import Literal

UserRole = Literal["admin", "user", "guest"]

def check_permission(role: UserRole) -> bool:
    """
    role can ONLY be "admin", "user", or "guest"
    IDE will autocomplete these exact values
    """
    return role == "admin"

## ============================================================================
## SECTION 7: Protocol (Structural Typing)
## ============================================================================

class Readable(Protocol):
    """
    Protocol defines a structure - any class with a read() method
    matches this protocol, even without inheritance.
    This is "duck typing" but type-safe.
    """
    def read(self) -> str: ...

def read_data(source: Readable) -> str:
    """
    Accepts anything with a read() method
    """
    return source.read()

## Works with files, StringIO, custom classes, etc.

## ============================================================================
## SECTION 8: Real-World Example - Our PDM App
## ============================================================================

from datetime import datetime

class FileLockData:
    """This is what we'll store in our locks.json"""
    filename: str
    user: str
    timestamp: datetime
    message: str

def create_lock(
    filename: str,
    user: str,
    message: str
) -> Dict[str, Union[str, datetime]]:
    """
    In our actual app, we'll use Pydantic which validates these
    types at runtime, but the hints help IDEs and mypy catch errors.
    """
    return {
        "filename": filename,
        "user": user,
        "timestamp": datetime.now(),
        "message": message
    }

## ============================================================================
## TESTING YOUR UNDERSTANDING
## ============================================================================

if __name__ == "__main__":
    ## Test basic types
    print(greet("World"))

    ## Test collections
    files = ["file1.txt", "file2.txt"]
    print(process_files(files))

    ## Test Optional
    user = find_user(1)
    print(f"Found user: {user}")

    ## Test Union
    print(process_data(42))
    print(process_data("hello"))
    print(process_data([1, 2, 3]))

    ## Test Callable
    result = execute_twice(double, 5)
    print(f"Double twice: {result}")

    ## Test generic
    first_str = get_first(["a", "b", "c"])
    first_int = get_first([1, 2, 3])
    print(f"First string: {first_str}, First int: {first_int}")
```

Run it:

```bash
python app/learn_typing.py
```

**Install mypy for static type checking:**

```bash
pip install mypy
mypy app/learn_typing.py
```

---

### 0.5: Path Management - The `pathlib` Module

**Never use string concatenation for paths. Use `pathlib.Path`.**

**File: `backend/app/learn_pathlib.py`**

## 🐍 Section 0.5: Path Management with `pathlib` – Tutorial Version

**Goal:**
Learn how to **handle filesystem paths safely and consistently** across platforms while building applications. You’ll also learn Python concepts like **object-oriented APIs**, **properties**, **methods**, and **real-world app folder structure**.

---

### **SECTION 1: Why `pathlib` exists**

```text
Old way: os.path, string-based paths
Problem: error-prone, platform differences, string concatenation issues

Modern way: pathlib
- Object-oriented API
- Safe path operations
- Works on Windows, macOS, Linux
- Makes code more readable and maintainable
```

**Tip:** Think of a path like an **object representing a file or folder**, not just a string. This allows **methods and properties**.

---

### **SECTION 2: Creating Paths**

```python
from pathlib import Path

## Current working directory
cwd = Path.cwd()

## Home directory
home = Path.home()

## Explicit path
manual = Path("/usr/local/bin")

print(f"Current directory: {cwd}")
print(f"Home directory: {home}")
```

**Deep dive:**

- `Path.cwd()` → Python figures out your current working directory.
- `Path.home()` → Always points to the user’s home folder.
- `Path("/usr/local/bin")` → Hardcoded path (useful for system paths).

**Repetition for learning:**
Try creating a **relative path** to a folder in your project and print it.

---

### **SECTION 3: Joining Paths Safely**

```python
project_root = Path.cwd()
backend = project_root / "backend"
app = backend / "app"
main = app / "main.py"

print(f"Main file: {main}")
```

**Key concepts:**

- The `/` operator replaces `os.path.join()`.
- Platform-agnostic (works with `/` on macOS/Linux and `\` on Windows).
- **Readable and chainable**, unlike `os.path.join()` with multiple arguments.

**Mini exercise:**
Create a path to a `logs` folder inside `app` and print it.

---

### **SECTION 4: Accessing Path Properties**

```python
example = Path("/home/user/project/backend/app/main.py")

print(example.name)      ## main.py
print(example.stem)      ## main
print(example.suffix)    ## .py
print(example.parent)    ## /home/user/project/backend/app
print(example.parents[1])## /home/user/project/backend
print(example.is_absolute()) ## True
```

**Why it matters:**

- `name` → file name with extension
- `stem` → name without extension
- `suffix` → extension
- `parent` → directory containing the file
- `parents[n]` → nth-level parent (helps traverse project folders)
- `is_absolute()` → checks if path is absolute (useful for resolving paths dynamically)

**Tip for apps:** You’ll often traverse **from current file to project root** — this is how large Python projects manage paths.

---

### **SECTION 5: Checking Existence and Type**

```python
path = Path(".")

if path.exists():
    print(f"{path} exists")

if path.is_file():
    print("It's a file")
elif path.is_dir():
    print("It's a directory")
```

**Explanation:**

- `exists()` → checks if the path exists on the filesystem
- `is_file()` → true if it’s a file
- `is_dir()` → true if it’s a directory

**Computer science takeaway:** This is **runtime validation**, useful for robust programs and preventing errors like trying to read a folder as a file.

---

### **SECTION 6: Reading and Writing Files**

```python
test_file = Path("test.txt")
test_file.write_text("Hello from pathlib!")  ## Write or overwrite
content = test_file.read_text()               ## Read as string
print(content)

test_file.write_bytes(b"Binary data")        ## Write bytes
binary = test_file.read_bytes()              ## Read bytes

test_file.unlink()  ## Delete file
```

**Notes:**

- `.write_text()` / `.read_text()` are **text-specific**, encoding default is UTF-8
- `.write_bytes()` / `.read_bytes()` for binary data
- `.unlink()` deletes the file — equivalent to `os.remove()`

**Mini exercise:**
Create `notes.txt`, write a few lines, read them back, then delete the file. Observe differences between text and bytes.

---

### **SECTION 7: Iterating Directory Contents**

```python
for item in Path(".").iterdir():
    print(f"Found: {item}")

for py_file in Path(".").rglob("*.py"):
    print(f"Python file: {py_file}")
```

- `.iterdir()` → iterates **only top-level files/folders**
- `.rglob()` → recursive glob; finds all matching patterns
- **App usage:** Useful for searching project files dynamically

---

### **SECTION 8: Creating Directories Safely**

```python
new_dir = Path("temp/nested/deep")
new_dir.mkdir(parents=True, exist_ok=True)  ## Create all parents if missing
```

- `parents=True` → creates missing intermediate directories
- `exist_ok=True` → prevents error if directory exists

**CS concept:** Avoid race conditions; always check existence or allow “exist_ok” for safety.

---

### **SECTION 9: Resolving Paths**

```python
relative = Path("../backend/app")
absolute = relative.resolve()

print(f"Relative: {relative}")
print(f"Absolute: {absolute}")
```

- `.resolve()` → converts relative paths to absolute paths
- Handles `..` and `.` automatically

**Why it matters for apps:** Always resolve paths **before reading/writing**, especially when scripts run from different working directories.

---

### **SECTION 10: Real-World App Example**

```python
def setup_project_paths():
    this_file = Path(__file__).resolve()
    backend_dir = this_file.parent.parent

    return {
        "backend": backend_dir,
        "app": backend_dir / "app",
        "static": backend_dir / "static",
        "repo": backend_dir / "repo"
    }

if __name__ == "__main__":
    paths = setup_project_paths()
    for name, path in paths.items():
        print(f"{name}: {path}")
```

**Key lessons:**

- Use `__file__` to **anchor paths to script location**
- Navigate dynamically to **project folders**
- Avoid hardcoding paths → makes the project **portable**

---

### **SECTION 11: Path vs String**

```python
path = Path("config.txt")

## Works directly
with open(path, "r") as f:
    data = f.read()

## Some old libraries require strings
import json
with open(str(path), "r") as f:
    data = json.load(f)
```

- Modern libraries accept **Path objects directly**
- Old code may require `str(path)`
- Python projects increasingly favor `pathlib` for clarity and safety

---

✅ **What this tutorial teaches:**

- Beginner: Creating, joining, and inspecting paths
- Intermediate: Reading/writing files, iterating directories
- Advanced: Resolving paths, app folder structures, dynamic project setup
- Computer science principles: abstraction, OOP design, cross-platform safety, runtime validation

```python
"""
Deep dive into pathlib - the modern way to handle filesystem paths.
Replaces os.path with an object-oriented API.
"""

from pathlib import Path
import os

## ============================================================================
## SECTION 1: Creating Paths
## ============================================================================

## Three ways to create a Path object
cwd = Path.cwd()  ## Current working directory
home = Path.home()  ## User's home directory
manual = Path("/usr/local/bin")  ## Explicit path

print(f"Current directory: {cwd}")
print(f"Home directory: {home}")

## ============================================================================
## SECTION 2: Path Operations (Cross-Platform)
## ============================================================================

## The `/` operator joins paths - works on all OS
project_root = Path.cwd()
backend = project_root / "backend"
app = backend / "app"
main = app / "main.py"

print(f"Main file: {main}")
## Windows: C:\Users\You\pdm-tutorial\backend\app\main.py
## macOS:   /Users/You/pdm-tutorial/backend/app/main.py

## ============================================================================
## SECTION 3: Path Properties
## ============================================================================

example = Path("/home/user/project/backend/app/main.py")

print(f"Name: {example.name}")           ## main.py
print(f"Stem: {example.stem}")           ## main (without extension)
print(f"Suffix: {example.suffix}")       ## .py
print(f"Parent: {example.parent}")       ## /home/user/project/backend/app
print(f"Parents[0]: {example.parents[0]}")  ## Immediate parent
print(f"Parents[1]: {example.parents[1]}")  ## Grandparent
print(f"Is absolute: {example.is_absolute()}")  ## True

## ============================================================================
## SECTION 4: Checking Existence and Type
## ============================================================================

path = Path(".")

if path.exists():
    print(f"{path} exists")

if path.is_file():
    print("It's a file")
elif path.is_dir():
    print("It's a directory")

## ============================================================================
## SECTION 5: Reading and Writing Files
## ============================================================================

## Create a test file
test_file = Path("test.txt")

## Write (creates or overwrites)
test_file.write_text("Hello from pathlib!")

## Read
content = test_file.read_text()
print(f"Content: {content}")

## Binary mode
test_file.write_bytes(b"Binary data")
binary = test_file.read_bytes()

## Clean up
test_file.unlink()  ## Delete file

## ============================================================================
## SECTION 6: Iterating Directory Contents
## ============================================================================

## List all files in current directory
for item in Path(".").iterdir():
    print(f"Found: {item}")

## Recursively find all .py files
for py_file in Path(".").rglob("*.py"):
    print(f"Python file: {py_file}")

## ============================================================================
## SECTION 7: Creating Directories
## ============================================================================

new_dir = Path("temp/nested/deep")

## parents=True: create parent directories if needed
## exist_ok=True: don't raise error if already exists
new_dir.mkdir(parents=True, exist_ok=True)

## Clean up
new_dir.rmdir()  ## Only works if empty
new_dir.parent.rmdir()
new_dir.parent.parent.rmdir()

## ============================================================================
## SECTION 8: Resolving Paths
## ============================================================================

relative = Path("../backend/app")
absolute = relative.resolve()  ## Converts to absolute, resolves .. and .

print(f"Relative: {relative}")
print(f"Absolute: {absolute}")

## ============================================================================
## SECTION 9: Real-World Example - Our PDM App Paths
## ============================================================================

def setup_project_paths():
    """
    How we'll actually set up paths in our PDM application.
    __file__ is the path to the current script.
    """
    ## Get the absolute path to this script
    this_file = Path(__file__).resolve()

    ## Navigate to project root
    ## main.py -> app/ -> backend/ -> pdm-tutorial/
    backend_dir = this_file.parent.parent

    ## Define all our important paths
    app_dir = backend_dir / "app"
    static_dir = backend_dir / "static"
    repo_dir = backend_dir / "repo"

    return {
        "backend": backend_dir,
        "app": app_dir,
        "static": static_dir,
        "repo": repo_dir
    }

## ============================================================================
## SECTION 10: Path vs String - When to Convert
## ============================================================================

path = Path("config.txt")

## Many functions accept Path objects directly
with open(path, 'r') as f:  ## Works!
    data = f.read()

## Some old libraries need strings
import json
## json.load() needs a string path in older versions
with open(str(path), 'r') as f:  ## Convert with str()
    data = json.load(f)

## Modern libraries accept Path objects
import shutil
shutil.copy(path, Path("backup.txt"))  ## Both are Paths

if __name__ == "__main__":
    paths = setup_project_paths()
    for name, path in paths.items():
        print(f"{name}: {path}")
```

Run it:

```bash
python app/learn_pathlib.py
```

---

### 0.6: Git Configuration

```bash
## Set your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

## Set default branch name
git config --global init.defaultBranch main

## Verify
git config --list
```

**Initialize repository:**

```bash
cd pdm-tutorial
git init
```

**File: `.gitignore`**

```
## Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/

## Environment
.env
.env.local

## IDEs
.vscode/
.idea/
*.swp
*.swo

## OS
.DS_Store
Thumbs.db

## Project specific
backend/repo/
backend/git_repo/
backend/*.json
!backend/.env.example
```

**First commit:**

```bash
git add .gitignore README.md
git commit -m "Initial commit: Project structure"
```

---

### 0.7: Package Management & Requirements

**File: `backend/requirements.txt`**

```
## Core framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

## We'll add more as we progress:
## passlib[bcrypt]  ## Stage 5
## python-jose[cryptography]  ## Stage 5
## sqlalchemy  ## Stage 11
## alembic  ## Stage 11
## redis  ## Stage 13
```

Install:

```bash
pip install -r requirements.txt
```

---

### Stage 0 Complete ✓

**Verification Checklist:**

- [ ] Directory structure matches exactly
- [ ] Virtual environment created and activated
- [ ] Python 3.11+ installed
- [ ] Git configured with your identity
- [ ] `.gitignore` created
- [ ] Initial commit made
- [ ] Ran `learn_typing.py` and understood type hints
- [ ] Ran `learn_pathlib.py` and understood Path operations

**What you learned:**

- Professional project structure from day one
- Python's import system and packages
- Type hints and the `typing` module
- Path manipulation with `pathlib`
- Virtual environment isolation
- Git basics

**Next**: Stage 1 - We'll create our first FastAPI application with proper organization.

---

Ready for Stage 1? Reply "Stage 1" and I'll give you the next section.

## Stage 1: First Backend - FastAPI Fundamentals

**Prerequisites**: Completed Stage 0

**Time**: 3-4 hours

**What you'll build**: A working FastAPI backend with proper architecture, understanding HTTP, ASGI, and FastAPI's core concepts.

---

### 1.1: Deep Dive - ASGI vs WSGI

**Before writing code, understand what FastAPI actually is.**

#### The Evolution of Python Web Servers

## **Section 1.1: Understanding ASGI and FastAPI Performance – Tutorial Version**

**Goal:**
Understand **why ASGI exists**, why FastAPI is faster for I/O-bound tasks, and the software engineering principles behind async programming.

---

### **SECTION 1: The Problem with WSGI (Synchronous)**

```python
def wsgi_application(environ, start_response):
    """
    WSGI (Web Server Gateway Interface) - The old standard.

    Problem: Synchronous. Each request blocks until complete.
    If one request takes 5 seconds, it blocks the worker.

    Used by: Flask, Django (traditional), Bottle
    """
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)

    ## Blocking operation - worker can't handle other requests
    import time
    time.sleep(1)  ## Simulating slow database query

    return [b'Hello World']
```

#### **Deep dive – Software Engineering and CS**

1. **WSGI is synchronous**

   - Each HTTP request **uses one worker**.
   - While that worker waits (e.g., database call, network), it **cannot process other requests**.

2. **Blocking behavior**

   - `time.sleep(1)` simulates a slow I/O operation.
   - During this second, the worker is completely idle.

3. **Scalability problem**

   - Real-world apps might have 1000 simultaneous requests.
   - If you have 4 workers, requests beyond the 4th **queue up**, increasing latency.
   - Classic concurrency problem in CS: **limited resources + blocking operations = poor throughput**.

4. **CS Concept: Threads vs Event Loops**

   - WSGI servers often rely on **multiple threads or processes** to handle concurrency.
   - Threads = heavier (memory + context switching).
   - Processes = safe isolation but expensive.

**Parallel in JavaScript:**

- Node.js uses a **single-threaded event loop**, non-blocking I/O to avoid these bottlenecks.
- Python async tries to achieve similar concurrency for I/O-bound tasks.

---

### **SECTION 2: ASGI (Asynchronous) – The Modern Standard**

```python
async def asgi_application(scope, receive, send):
    """
    ASGI - Asynchronous Server Gateway Interface

    Benefit: Non-blocking. While waiting for I/O (database, file read),
    the worker can handle other requests.

    Used by: FastAPI, Starlette, Django 3.0+, Quart
    """
    import asyncio
    await asyncio.sleep(1)  ## Waiting for I/O

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [[b'content-type', b'text/plain']],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello World',
    })
```

#### **Deep dive – Python async mechanics**

1. **`async def`**

   - Declares a coroutine — a function that can **pause its execution** at `await` points.
   - Unlike regular functions, it **does not block the event loop**.

2. **`await`**

   - Pauses the coroutine until the awaited operation completes.
   - Meanwhile, the **event loop schedules other coroutines**.

3. **`send` / `receive`**

   - Low-level ASGI interface: communicates with the server.
   - `send()` transmits response events.

4. **Key advantage:**

   - ASGI allows a **single worker to manage thousands of I/O-bound requests efficiently**.

**Parallel in JavaScript:**

- `async` / `await` works similarly in JS/Node.js.
- Non-blocking I/O is essential for scalable web servers.

---

### **SECTION 3: Real Performance Difference**

```text
Scenario: 1000 requests, each waits 1 second

WSGI (4 workers):
- 4 requests handled immediately
- Remaining 996 requests queue
- Total time: 250 seconds

ASGI (4 workers):
- All 1000 requests start immediately
- Event loop handles waiting requests efficiently
- Total time: ~1-2 seconds
```

#### **CS Principles**

1. **Throughput vs Latency**

   - WSGI: High latency under load
   - ASGI: High throughput and low latency

2. **Concurrency models**

   - WSGI → Process/thread-based concurrency
   - ASGI → Event-loop-based concurrency (like Node.js)

3. **Software engineering takeaway**

   - Choosing the right concurrency model depends on **application workload**.
   - I/O-heavy apps benefit from async.
   - CPU-heavy apps may still need threads or multiprocessing.

---

### **SECTION 4: When to Use `async/await`**

#### **Good use cases (I/O bound)**

```python
async def good_async():
    ## Example: Database queries
    result = await db.fetch_one("SELECT * FROM users")

    ## Example: HTTP requests to external APIs
    response = await http_client.get("https://api.example.com")

    ## Example: File I/O
    data = await file.read()

    return result
```

- Use `async` when operations **wait for external resources**.
- Non-blocking behavior allows **high concurrency without extra threads**.

#### **Bad use cases (CPU bound)**

```python
def bad_async():
    ## Heavy computation
    result = sum(range(10_000_000))  ## Blocks event loop
    return result
```

- Async **does not make CPU-bound tasks faster**.
- For CPU-heavy operations, use **threads, multiprocessing, or offload to C extensions**.

---

#### **Rule of Thumb – Software Engineering Perspective**

| Operation Type                            | Recommended Function Type |
| ----------------------------------------- | ------------------------- |
| I/O-bound (DB, network, file)             | `async def` with `await`  |
| CPU-bound (math, loops, heavy processing) | Regular `def`             |

- Start with synchronous functions.
- Profile your app to identify bottlenecks.
- Use async selectively for **I/O-heavy parts**.

---

#### ✅ **Key Takeaways**

1. **WSGI is synchronous** → blocks requests, limits scalability.
2. **ASGI is asynchronous** → event loop handles many requests efficiently.
3. **`async/await`** is Python’s way to write non-blocking code.
4. **FastAPI** leverages ASGI to provide **high-performance I/O-bound web services**.
5. **CS concepts reinforced:** concurrency, throughput, latency, event loops, and choosing the right model based on workload.
6. **Software engineering principles:**

   - Build modular, scalable apps
   - Profile before optimizing
   - Avoid unnecessary complexity

---

```python
## backend/app/learn_asgi.py
"""
Understanding ASGI (Asynchronous Server Gateway Interface)
and why FastAPI is fast.
"""

## ============================================================================
## SECTION 1: The Problem with WSGI (Synchronous)
## ============================================================================

def wsgi_application(environ, start_response):
    """
    WSGI (Web Server Gateway Interface) - The old standard.

    Problem: Synchronous. Each request blocks until complete.
    If one request takes 5 seconds, it blocks the worker.

    Used by: Flask, Django (traditional), Bottle
    """
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)

    ## Blocking operation - worker can't handle other requests
    import time
    time.sleep(1)  ## Simulating slow database query

    return [b'Hello World']

## ============================================================================
## SECTION 2: ASGI (Asynchronous) - The Modern Standard
## ============================================================================

async def asgi_application(scope, receive, send):
    """
    ASGI - Asynchronous Server Gateway Interface

    Benefit: Non-blocking. While waiting for I/O (database, file read),
    the worker can handle other requests.

    Used by: FastAPI, Starlette, Django 3.0+, Quart
    """
    ## This doesn't block the worker
    import asyncio
    await asyncio.sleep(1)  ## Waiting for I/O

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [[b'content-type', b'text/plain']],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello World',
    })

## ============================================================================
## SECTION 3: Real Performance Difference
## ============================================================================

"""
Scenario: 1000 requests, each needs to wait 1 second for database

WSGI (4 workers):
- Request 1-4: Handle immediately
- Request 5: Waits for worker to free up (1 second)
- Request 6: Waits (1 second)
- ...
- Total time: 250 seconds (1000 requests / 4 workers)

ASGI (4 workers):
- Request 1-1000: All start immediately
- While waiting for I/O, workers handle other requests
- Total time: ~1-2 seconds

This is why FastAPI is fast for I/O-bound operations.
"""

## ============================================================================
## SECTION 4: When to Use async/await
## ============================================================================

## Good use cases (I/O bound):
async def good_async():
    """Use async for I/O operations"""
    ## Database queries
    result = await db.fetch_one("SELECT * FROM users")

    ## HTTP requests to external APIs
    response = await http_client.get("https://api.example.com")

    ## File I/O
    data = await file.read()

    return result

## Bad use cases (CPU bound):
def bad_async():
    """Don't use async for CPU-intensive tasks"""
    ## Heavy computation - this blocks regardless
    result = sum(range(10_000_000))  ## No await needed
    return result

"""
Rule of thumb:
- I/O operations (database, network, files): Use async
- CPU operations (math, loops, data processing): Regular functions
- When in doubt: Start with regular functions, profile, optimize
"""
```

---

### 1.2: HTTP Protocol Deep Dive

**File: `backend/app/learn_http.py`**

## **Section 1.2: HTTP Protocol Deep Dive – Tutorial Version**

**Goal:**
Understand **how HTTP works**, why RESTful APIs follow conventions, and how this knowledge informs building **robust, maintainable web applications**. Also connects to **software engineering concepts** like idempotency, client-server separation, and API design.

---

### **SECTION 1: HTTP Request Structure**

An HTTP request has **four main parts**:

1. **Request Line** – method, path, and version

```
GET /api/files HTTP/1.1
```

- **Method** → what action the client wants (`GET`, `POST`, etc.)
- **Path** → resource being accessed (`/api/files`)
- **Version** → HTTP version (`HTTP/1.1` or `HTTP/2`)

**CS Concept:**

- HTTP is a **protocol** defining a contract between client and server.
- Parsing the request line is the first step in request handling.

---

2. **Headers** – key-value metadata

```
Host: localhost:8000
User-Agent: Mozilla/5.0
Accept: application/json
Authorization: Bearer <token>
Content-Type: application/json
Content-Length: 42
```

- Provide **context and instructions** for the server
- Examples:

  - `Accept` → desired response format
  - `Content-Type` → type of body content
  - `Authorization` → security token

**Software Engineering Insight:**

- Headers implement **separation of concerns**: metadata vs payload
- They allow **extensible communication** without changing the body format

---

3. **Blank Line**

- Separates headers from body
- Mandatory to signal the start of content

4. **Body** (optional)

```
{"filename": "PN1001.mcam", "user": "john"}
```

- Contains **payload** for requests that modify data (`POST`, `PUT`, `PATCH`)
- JSON is the most common format for APIs

**Parallel in JS/Node.js:**

- In Express, `req.body` holds the parsed JSON data
- FastAPI automatically parses JSON into Python dicts

---

### **SECTION 2: HTTP Methods (Verbs)**

RESTful conventions define **how to manipulate resources**:

| Method | Example        | Safe?  | Idempotent? | Body?         | Purpose                 |
| ------ | -------------- | ------ | ----------- | ------------- | ----------------------- |
| GET    | /api/files     | ✅ Yes | ✅ Yes      | ❌ No         | Read resource(s)        |
| POST   | /api/files     | ❌ No  | ❌ No       | ✅ Yes        | Create resource         |
| PUT    | /api/files/123 | ❌ No  | ✅ Yes      | ✅ Yes        | Replace resource        |
| PATCH  | /api/files/123 | ❌ No  | ❌ Maybe    | ✅ Yes        | Modify part of resource |
| DELETE | /api/files/123 | ❌ No  | ✅ Yes      | ❌ Usually no | Delete resource         |

#### **CS Concepts**

1. **Safe vs Unsafe**

   - Safe → does not modify server state (`GET`)
   - Unsafe → modifies server state (`POST`, `PUT`, `DELETE`)

2. **Idempotency**

   - Idempotent → repeated calls produce the **same result**
   - Non-idempotent → each call may produce different effects
   - Critical in **distributed systems** for retries and fault tolerance

---

### **SECTION 3: HTTP Status Codes**

| Class | Examples                     | Meaning                                                                  |
| ----- | ---------------------------- | ------------------------------------------------------------------------ |
| 1xx   | 101                          | Informational (rare in APIs, e.g., WebSocket upgrade)                    |
| 2xx   | 200, 201, 204                | Success (OK, Created, No Content)                                        |
| 3xx   | 301, 302, 304                | Redirection (resource moved, cache handling)                             |
| 4xx   | 400, 401, 403, 404, 409, 422 | Client errors (invalid input, unauthorized, not found, validation error) |
| 5xx   | 500, 502, 503                | Server errors (exceptions, downtime)                                     |

**Python/FastAPI Note:**

- FastAPI sets most status codes automatically based on **return values or exceptions**.
- Understanding them helps **debugging, logging, and client design**.

**Parallel in JS/Node.js:**

- Express uses `res.status(404).send('Not Found')`
- Concepts of 2xx, 4xx, 5xx are identical

---

### **SECTION 4: Content Negotiation**

- Client tells server **what format it wants** using `Accept` header:

```
Request: Accept: application/json
Response: Content-Type: application/json
{"result": "data"}
```

**FastAPI feature:**

- Detects client preference
- Automatically converts Python objects (dict, list) to JSON
- Sets `Content-Type` header

**CS Concept:**

- **Content negotiation** allows APIs to be **flexible and extensible** without changing endpoints
- Encourages **interoperability** across clients

---

### **SECTION 5: Important Headers in Our App**

| Header                         | Purpose                                          |
| ------------------------------ | ------------------------------------------------ |
| Authorization: Bearer <JWT>    | Carries authentication token                     |
| Content-Type: application/json | Tells server body is JSON                        |
| Accept: application/json       | Client wants JSON back                           |
| Content-Length                 | Indicates body size, prevents truncated requests |

**Software Engineering Insight:**

- Proper use of headers is essential for **security, reliability, and protocol compliance**
- JWT tokens → stateless authentication, aligns with **modern API architecture**

---

### ✅ **Key Takeaways**

1. **HTTP defines a structured contract** between client and server.
2. **Verbs (GET, POST, PUT, PATCH, DELETE)** convey intent and define side-effects.
3. **Status codes** communicate outcome of operations.
4. **Headers and content negotiation** enable metadata-driven, interoperable APIs.
5. **FastAPI abstracts most boilerplate**, but understanding HTTP is critical for **debugging, client design, and real-world software engineering**.
6. **CS principles reinforced:** idempotency, separation of concerns, stateless protocols, distributed system considerations.

---

```python
"""
Understanding HTTP - The protocol that powers the web.
"""

## ============================================================================
## SECTION 1: HTTP Request Structure
## ============================================================================

"""
An HTTP request has 4 parts:

1. REQUEST LINE
   GET /api/files HTTP/1.1

   Method: GET, POST, PUT, DELETE, PATCH, etc.
   Path: /api/files
   Version: HTTP/1.1

2. HEADERS (Key-Value metadata)
   Host: localhost:8000
   User-Agent: Mozilla/5.0
   Accept: application/json
   Authorization: Bearer eyJhbGc...
   Content-Type: application/json
   Content-Length: 42

3. BLANK LINE (separates headers from body)

4. BODY (optional, for POST/PUT/PATCH)
   {"filename": "PN1001.mcam", "user": "john"}
"""

## ============================================================================
## SECTION 2: HTTP Methods (Verbs)
## ============================================================================

"""
RESTful API conventions:

GET /api/files
- Retrieve a list of files
- Safe (no side effects)
- Idempotent (calling twice = calling once)
- No request body

GET /api/files/123
- Retrieve a specific file
- Safe, Idempotent

POST /api/files
- Create a new file
- NOT safe (creates data)
- NOT idempotent (creates new resource each time)
- Has request body with file data

PUT /api/files/123
- Replace entire file 123
- NOT safe
- Idempotent (replacing twice = same result)
- Has request body with complete new data

PATCH /api/files/123
- Update part of file 123
- NOT safe
- May or may not be idempotent
- Has request body with partial data

DELETE /api/files/123
- Delete file 123
- NOT safe
- Idempotent (deleting twice = same as once)
- Usually no request body
"""

## ============================================================================
## SECTION 3: HTTP Status Codes
## ============================================================================

"""
FastAPI automatically sets these, but you should understand them:

1xx: Informational (rare in APIs)
  101 Switching Protocols (WebSocket upgrade)

2xx: Success
  200 OK - Standard success
  201 Created - Successfully created resource
  204 No Content - Success but no response body (DELETE)

3xx: Redirection
  301 Moved Permanently
  302 Found (temporary redirect)
  304 Not Modified (caching)

4xx: Client Error (user did something wrong)
  400 Bad Request - Invalid data
  401 Unauthorized - Not authenticated (no/bad token)
  403 Forbidden - Authenticated but not authorized (wrong role)
  404 Not Found - Resource doesn't exist
  409 Conflict - Resource state conflict (file already locked)
  422 Unprocessable Entity - Validation error (Pydantic uses this)

5xx: Server Error (our code broke)
  500 Internal Server Error - Unhandled exception
  502 Bad Gateway - Proxy/gateway error
  503 Service Unavailable - Server overloaded/down
"""

## ============================================================================
## SECTION 4: Content Negotiation
## ============================================================================

"""
Client tells server what format it wants:

Request:
  Accept: application/json

Response:
  Content-Type: application/json
  {"result": "data"}

FastAPI handles this automatically:
- Sees Accept: application/json
- Returns dict/list → FastAPI converts to JSON
- Sets Content-Type: application/json
"""

## ============================================================================
## SECTION 5: Headers We'll Use
## ============================================================================

"""
Important headers in our PDM app:

Authorization: Bearer <JWT>
- Carries authentication token
- Format: "Bearer eyJhbGciOiJIUzI1NiIs..."

Content-Type: application/json
- Tells server: body is JSON
- Server knows to parse as JSON

Accept: application/json
- Tells server: I want JSON back
- Server formats response as JSON

Content-Length: 1234
- Size of request body in bytes
- Prevents incomplete requests
"""

if __name__ == "__main__":
    print("HTTP concepts explained. No code to run.")
    print("These concepts will make sense as we build endpoints.")
```

---

### 1.3: Create Your First FastAPI Application

**File: `backend/app/config.py`**

## **Section 1.3: Application Configuration – Tutorial Version**

**Goal:**
Understand **how to centralize and manage application settings**, why it matters in **software engineering**, and how **Python + Pydantic** helps you enforce types and defaults safely. We’ll also cover **environment variables, config patterns, and path management**.

---

### **Why Centralized Configuration Matters**

In software engineering, **hardcoding values** (like database URLs, file paths, API keys) is a bad idea:

- Makes apps **less flexible** (hard to deploy to multiple environments: dev, staging, prod).
- Creates **maintenance issues** (if a value changes, you have to search the code).
- Introduces **security risks** (sensitive info in code repository).

**Solution:** Centralized configuration:

- **One place for all settings**
- **Override per environment** (e.g., `.env` for dev, environment variables for prod)
- **Typed values** to catch errors early

This is a common **software engineering best practice** in modern backend systems.

---

### **SECTION 1: Using Pydantic Settings**

```python
from pydantic_settings import BaseSettings
from pathlib import Path
```

- `BaseSettings` → special Pydantic class for **typed, validated settings**
- `Path` → modern way to manage filesystem paths (object-oriented, cross-platform)

**CS/Engineering note:**

- We’re combining **type safety** (Python typing + Pydantic) with **config abstraction**, making apps **reliable and maintainable**.

---

### **SECTION 2: Define Your Settings Class**

```python
class Settings(BaseSettings):
    """
    Application settings with sensible defaults for development.
    Override via environment variables or .env file.
    """
```

- **Class-based config** → a common pattern in backend engineering
- `BaseSettings` automatically reads **environment variables** to override defaults

#### **Application-level settings**

```python
APP_NAME: str = "PDM Backend API"
APP_VERSION: str = "0.1.0"
DEBUG: bool = True
```

- `APP_NAME` → displayed in logs, docs, API metadata
- `APP_VERSION` → versioning for clients or migrations
- `DEBUG` → controls whether **detailed errors** and **auto-reload** are enabled

**CS/Engineering principle:**

- Centralized, typed constants reduce **magic values** scattered across the codebase.
- Enables **consistent, environment-specific behavior**.

---

#### **Path Configuration**

```python
BASE_DIR: Path = Path(__file__).resolve().parent.parent
```

- Dynamically computes **project root** based on file location
- `__file__` → current file path
- `resolve()` → absolute path
- `.parent.parent` → go **two levels up** (e.g., from `backend/app/config.py` → `backend/`)

**Why important:**

- Avoids hardcoding paths → portable across machines
- Ensures all file operations (logs, templates, uploads) use **consistent base directory**

**CS Concept:**

- Relative paths can break in deployment; computing absolute paths dynamically is **defensive programming**.

---

### **SECTION 3: Environment File Support**

```python
class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"
```

- `.env` → a **plain-text file with environment variables**
- Example `.env`:

```
APP_NAME=PDM API Production
DEBUG=False
```

- FastAPI / Pydantic automatically reads these at runtime
- Allows **safe overrides** without changing code

**Software engineering principle:**

- **12-factor apps** recommend storing config in environment variables, not code.
- Decouples **config from logic**, improves **security and portability**.

---

### **SECTION 4: Singleton Instance**

```python
settings = Settings()
```

- Creates **one instance of Settings** used across the entire backend
- Ensures **consistent configuration** without repeated reads
- Other modules can import:

```python
from config import settings
print(settings.APP_NAME)
```

**CS Concept – Singleton Pattern:**

- Ensures **only one instance** manages global state/config
- Avoids duplicated config logic and inconsistent values

---

### ✅ **Key Takeaways**

1. **Centralized configuration** is critical for maintainable, secure, deployable apps.
2. **Pydantic + BaseSettings** combines:

   - **Type safety** → early error detection
   - **Validation** → ensures values match expected type
   - **Environment overrides** → easy dev/staging/prod switching

3. **Path management** ensures **portable, robust filesystem access**
4. **Singleton instance** guarantees **consistent configuration** across modules
5. **CS + software engineering concepts reinforced:**

   - Separation of concerns
   - Environment-aware applications
   - Singleton pattern for shared state
   - Defensive programming (computed paths)

---

**Parallel in JavaScript / Node.js:**

- Common pattern: `config.js` with:

```javascript
const path = require("path");

module.exports = {
  APP_NAME: process.env.APP_NAME || "PDM Backend API",
  DEBUG: process.env.DEBUG === "true",
  BASE_DIR: path.resolve(__dirname, "..", ".."),
};
```

- Conceptually identical: type checking is looser, but environment-based config is the same.

---

This section **sets the foundation for building endpoints and services** in FastAPI while keeping **config centralized, typed, and environment-aware**.

```python
"""
Application configuration.
Centralized settings loaded from environment variables.
"""

from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """
    Application settings with sensible defaults for development.
    Override via environment variables or .env file.
    """

    ## ========================================================================
    ## Application Settings
    ## ========================================================================
    APP_NAME: str = "PDM Backend API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    ## ========================================================================
    ## Path Configuration
    ## ========================================================================
    ## Computed at runtime - where is this config.py file?
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

## Create singleton instance
settings = Settings()
```

**Why a separate config file?**

- **Single source of truth** for settings
- **Environment-aware**: Different values for dev/staging/production
- **Type-safe**: Pydantic validates config on startup
- **12-factor app**: Configuration in environment, not code

---

**File: `backend/app/main.py`**

## **Section 1.3 (Part 2): FastAPI Application Initialization – Tutorial Version**

**Goal:**
Understand how to properly structure a **FastAPI backend**, why we use an **application factory**, middleware, startup/shutdown events, and separation of concerns. We’ll include **CS/software engineering insights** and **Python best practices**.

---

### **SECTION 1: Application Factory Pattern**

```python
def create_application() -> FastAPI:
```

- **Purpose:** Encapsulates **app creation logic** in a function rather than at module level
- Returns a **FastAPI instance**
- This pattern is widely used in **Flask**, **FastAPI**, and **other Python frameworks**

#### **Benefits**

1. **Multiple instances** → useful for testing:

   - You can spin up a separate app instance for **unit tests** without interfering with your main app.

2. **Centralized configuration** → app settings come from `settings` object
3. **Startup/shutdown hooks** → easy to attach lifecycle events

**Software Engineering Insight:**

- Using an application factory follows **modular design principles**
- Promotes **decoupling** and **testability**, critical in professional backend systems

---

### **SECTION 2: Middleware Configuration**

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### **Why middleware?**

- Middleware intercepts requests/responses **before and after hitting routes**
- Common uses: **CORS, authentication, logging, error handling**

#### **CORS Explained (Cross-Origin Resource Sharing)**

- Browsers enforce the **Same-Origin Policy**: JavaScript can’t call APIs on a different domain by default
- CORS headers **tell the browser which origins are allowed**
- In production, only allow your **frontend domain** for security

**CS Concept:**

- Middleware demonstrates **intercepting layers** → a classic **pipeline pattern** in software engineering
- Allows cross-cutting concerns without polluting business logic

---

### **SECTION 3: Startup and Shutdown Events**

```python
@app.on_event("startup")
async def startup_event():
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
```

- **Startup events**: run once **when the server starts**
- Good for:

  - Connecting to databases
  - Loading caches
  - Logging server info

```python
@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down gracefully...")
```

- **Shutdown events**: run once **when the server stops**
- Good for:

  - Closing DB connections
  - Flushing logs
  - Cleanup tasks

**Python/CS Concept:**

- ASGI allows **async startup/shutdown** → non-blocking operations
- Mimics **resource management patterns** in OS-level programming

---

### **SECTION 4: Root Route (Health Check)**

```python
@app.get("/")
def read_root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "message": "Welcome to the PDM Backend API"
    }
```

- Simple **GET endpoint** to check server health and API metadata
- **Best practice:** every API should have a **root or health check route**

**Software Engineering Insight:**

- Useful for **monitoring tools** or load balancers
- Communicates **version and operational status** → key for CI/CD pipelines

---

### **SECTION 5: Create App Instance**

```python
app = create_application()
```

- Calls the **factory** to create a **singleton FastAPI instance**
- Other modules import `app` for **routing, middleware, and testing**

**CS Concept:**

- Follows **dependency injection principles**: app configuration is **externalized** and **passed in**, improving flexibility

---

### **SECTION 6: Development Server Entry Point**

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
```

#### **Key points**

- `__name__ == "__main__"` → standard Python idiom to run **module as script**
- `uvicorn.run()` → launches **ASGI server**
- `reload=True` → **auto-reload** in development (not for production)
- `log_level="info"` → controls verbosity for debugging

**Best practice:**

- **Keep entry point thin** → all **business logic** belongs in `services/` or `routes/`
- **Separation of concerns** → easier maintenance and testing

**JavaScript Parallel:**

- Node/Express apps often use:

```javascript
const app = require("./app");
app.listen(3000, () => console.log("Server running"));
```

- Same idea: thin entry point, main logic elsewhere

---

### ✅ **Key Takeaways**

1. **Application Factory Pattern** → promotes modularity, testability, and centralized configuration
2. **Middleware** → intercept requests/responses for cross-cutting concerns
3. **Startup/Shutdown hooks** → manage resources reliably
4. **Root route** → health check & API metadata, best practice for monitoring
5. **Thin entry point** → separates server bootstrap from business logic
6. **CS/Software Engineering Concepts:**

   - Modular design & separation of concerns
   - Pipeline pattern (middleware)
   - Dependency injection & singleton instance
   - Resource lifecycle management

---

This structure sets you up for **scaling your app**, **testing endpoints**, and integrating **business logic in services and routes**.

```python
"""
Main FastAPI application entry point.

This file should be thin - just app initialization and router inclusion.
Business logic goes in services/, routes go in api/.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

## ============================================================================
## SECTION 1: Application Factory
## ============================================================================

def create_application() -> FastAPI:
    """
    Application factory pattern.

    Benefits:
    - Can create multiple app instances (useful for testing)
    - Configuration centralized
    - Easy to add startup/shutdown logic
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Parts Data Management System - A collaborative file locking system",
        debug=settings.DEBUG,
    )

    ## ====================================================================
    ## SECTION 2: Middleware Configuration
    ## ====================================================================

    ## CORS: Allow frontend to call our API
    ## In production, restrict origins to your actual frontend domain
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    ## ====================================================================
    ## SECTION 3: Startup/Shutdown Events
    ## ====================================================================

    @app.on_event("startup")
    async def startup_event():
        """
        Runs once when the server starts.
        Use for: database connections, cache setup, etc.
        """
        print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
        print(f"Debug mode: {settings.DEBUG}")
        print(f"Base directory: {settings.BASE_DIR}")

    @app.on_event("shutdown")
    async def shutdown_event():
        """
        Runs once when the server stops.
        Use for: closing database connections, cleanup
        """
        print("Shutting down gracefully...")

    ## ====================================================================
    ## SECTION 4: Root Route
    ## ====================================================================

    @app.get("/")
    def read_root():
        """
        Root endpoint - health check and API info.
        """
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "operational",
            "message": "Welcome to the PDM Backend API"
        }

    return app

## ============================================================================
## SECTION 5: Create App Instance
## ============================================================================

app = create_application()

## ============================================================================
## SECTION 6: Development Server Entry Point
## ============================================================================

if __name__ == "__main__":
    """
    For development: python -m app.main
    For production: Use gunicorn/uvicorn directly
    """
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
```

**Test it:**

```bash
cd backend
uvicorn app.main:app --reload
```

Visit: http://127.0.0.1:8000

You should see JSON response with API info.

---

### 1.4: Deep Dive - Pydantic Models

**File: `backend/app/learn_pydantic.py`**

## **Section 1.4: Pydantic & Data Validation – Tutorial Version**

**Goal:**
Understand how **Pydantic** uses **Python type hints** to:

1. Validate input and output data
2. Ensure type safety
3. Serialize/deserialize JSON
4. Enforce business rules in a **FastAPI backend**

We’ll go from **basic models** to **nested models and validators**, then tie it to **real-world app usage**.

---

### **SECTION 1: Basic Pydantic Model**

```python
class UserBasic(BaseModel):
    username: str
    age: int
    email: str
```

#### **Key Points**

1. **`BaseModel`** → All Pydantic models inherit from this class
2. **Type hints automatically enforce validation**
3. **Access fields like regular Python objects**

```python
user = UserBasic(username="john", age=30, email="john@example.com")
print(user.username)  ## 'john'
```

- **CS Insight:** Pydantic **implements declarative data validation** using **Python's type hints**
- Similar in spirit to **TypeScript interfaces**, but validated at **runtime**

#### **Validation Example**

```python
try:
    bad_user = UserBasic(username="john", age="thirty", email="john@example.com")
except Exception as e:
    print(f"Validation error: {e}")
```

- Throws `ValidationError` → Python **enforces types dynamically**, protecting downstream code

---

### **SECTION 2: Optional Fields and Defaults**

```python
class UserWithDefaults(BaseModel):
    username: str
    age: int = 18        ## default if not provided
    email: Optional[str] = None
    is_active: bool = True
```

- `Optional[str]` → can be `str` or `None`
- Defaults make **some fields optional**, supporting **partial input**
- **Python Insight:** Type hints + default values are a **declarative form of input constraints**

```python
user1 = UserWithDefaults(username="alice")  ## age=18, email=None
user2 = UserWithDefaults(username="bob", age=25, email="bob@example.com")
```

- Reduces boilerplate, keeps **business logic clean**

---

### **SECTION 3: Field Constraints**

```python
class UserConstrained(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    age: int = Field(..., ge=0, le=150)
    email: str = Field(..., regex=r"^[\w\.-]+@[\w\.-]+\.\w+$")
```

- `Field(...)` → makes a field **required**
- Additional arguments → **validation rules**:

  - `min_length`, `max_length`
  - `pattern` → regex validation
  - `ge`/`le` → numeric ranges

```python
try:
    bad = UserConstrained(username="ab", age=200, email="invalid")
except Exception as e:
    print(f"Validation error: {e}")
```

- Protects against **invalid input early** → avoids downstream errors

**CS Insight:**

- **Declarative validation** is a **design pattern**: define **what data should be**, not how to check it
- Reduces **imperative boilerplate validation code**

---

### **SECTION 4: Enums for Fixed Choices**

```python
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
```

- `Enum` → restricts values to a **finite set**
- `str` inheritance → automatically **serializable to JSON**
- Prevents **magic strings** and **typos** in code

```python
class UserWithRole(BaseModel):
    username: str
    role: UserRole = UserRole.USER

user = UserWithRole(username="alice", role="admin")
print(user.role.value)  ## 'admin'
```

**Software Engineering Insight:**

- Using Enums increases **type safety** and **readability**
- Analogous to **TypeScript union types**, but validated at runtime

---

### **SECTION 5: Custom Validators**

```python
class UserWithValidation(BaseModel):
    username: str
    password: str
    password_confirm: str

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()

    @root_validator
    def passwords_match(cls, values):
        if values.get('password') != values.get('password_confirm'):
            raise ValueError('Passwords do not match')
        return values
```

- `@validator` → per-field validation
- `@root_validator` → cross-field validation (e.g., passwords match)
- Automatically runs **after type validation**

**CS Insight:**

- Implements **defensive programming** → ensures data integrity
- Promotes **separation of concerns**: model handles validation, services handle logic

---

### **SECTION 6: Nested Models**

```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class UserWithAddress(BaseModel):
    username: str
    address: Address
```

- Nested models → **hierarchical validation**
- Supports **complex data structures**
- Access fields naturally:

```python
user = UserWithAddress(username="alice", address={"street": "123 Main St", "city": "NYC", "country": "USA"})
print(user.address.city)  ## NYC
```

**Python Insight:**

- Demonstrates **composition over inheritance**
- Avoids deep manual validation for nested dicts

---

### **SECTION 7: Serialization**

```python
class UserComplete(BaseModel):
    username: str
    email: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
```

- `.dict()` → convert model to Python dict
- `.json()` → convert to JSON string
- `.parse_raw()` → create model from JSON string

```python
user = UserComplete(username="alice", email="alice@example.com")
print(user.dict())
print(user.json())
json_str = '{"username": "bob", "email": "bob@example.com"}'
user2 = UserComplete.parse_raw(json_str)
```

**CS Insight:**

- Serialization/deserialization is **essential for APIs**
- Pydantic handles this automatically, ensuring **type safety**

---

### **SECTION 8: Real-World Example – File Checkout Request**

```python
class FileCheckoutRequest(BaseModel):
    filename: str = Field(..., min_length=1, max_length=255, pattern=r"^[\w\-. ]+\.mcam$")
    user: str = Field(..., min_length=3, max_length=50)
    message: str = Field(..., min_length=1, max_length=500)

    @validator('filename')
    def sanitize_filename(cls, v):
        if '..' in v or '/' in v or '\\' in v:
            raise ValueError('Invalid filename: contains path separators')
        return v
```

- **Purpose:** Protects against **directory traversal attacks**
- Validates **input length, pattern, and business rules**
- Example usage:

```python
try:
    request = FileCheckoutRequest(filename="../../etc/passwd", user="hacker", message="test")
except Exception as e:
    print(f"Blocked attack: {e}")

valid_request = FileCheckoutRequest(filename="PN1001.mcam", user="john", message="Editing part dimensions")
print(valid_request.dict())
```

**Software Engineering Insight:**

- Pydantic enables **secure, declarative input validation**
- Reduces need for **manual checks in business logic**

---

### ✅ **Key Takeaways**

1. **Pydantic models**: central for **request validation** and **response serialization**
2. **Type hints** + runtime checks → **data integrity**
3. **Field constraints** and **validators** prevent invalid or malicious data
4. **Enums & nested models** → enforce structure and reduce errors
5. **Serialization** → automatic, safe, and JSON-ready
6. Real-world apps benefit from **centralized validation** for security and maintainability

---

This section sets you up for **Stage 3** in your app: **API endpoints** that validate requests and enforce business rules **without repeating validation code**.

```python
"""
Pydantic: Data validation using Python type hints.

FastAPI uses Pydantic for:
1. Request body validation
2. Response serialization
3. Settings management
4. Automatic API documentation
"""

from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

## ============================================================================
## SECTION 1: Basic Model
## ============================================================================

class UserBasic(BaseModel):
    """
    Most basic Pydantic model.
    Validates types automatically.
    """
    username: str
    age: int
    email: str

## Usage:
user = UserBasic(username="john", age=30, email="john@example.com")
print(user.username)  ## Access like a regular object

## Type validation happens automatically:
try:
    bad_user = UserBasic(username="john", age="thirty", email="john@example.com")
except Exception as e:
    print(f"Validation error: {e}")
    ## ValidationError: age must be an integer

## ============================================================================
## SECTION 2: Optional Fields and Defaults
## ============================================================================

class UserWithDefaults(BaseModel):
    username: str
    age: int = 18  ## Default value if not provided
    email: Optional[str] = None  ## Can be None
    is_active: bool = True

## Valid:
user1 = UserWithDefaults(username="alice")  ## Uses defaults
user2 = UserWithDefaults(username="bob", age=25, email="bob@example.com")

## ============================================================================
## SECTION 3: Field Constraints
## ============================================================================

class UserConstrained(BaseModel):
    """
    Field() adds validation rules and documentation.
    """
    username: str = Field(
        ...,  ## Required (ellipsis means no default)
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_]+$",  ## Regex: alphanumeric and underscore only
        description="Unique username for the user"
    )
    age: int = Field(
        ...,
        ge=0,  ## Greater than or equal to 0
        le=150,  ## Less than or equal to 150
        description="User's age in years"
    )
    email: str = Field(
        ...,
        regex=r"^[\w\.-]+@[\w\.-]+\.\w+$"
    )

## Try invalid data:
try:
    bad = UserConstrained(username="ab", age=200, email="invalid")
except Exception as e:
    print(f"Validation error: {e}")

## ============================================================================
## SECTION 4: Enums for Fixed Choices
## ============================================================================

class UserRole(str, Enum):
    """
    Enum limits values to specific choices.
    Inheriting from str makes it JSON-serializable.
    """
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class UserWithRole(BaseModel):
    username: str
    role: UserRole = UserRole.USER  ## Must be one of the enum values

user = UserWithRole(username="alice", role="admin")  ## Automatically converts string to enum
print(user.role)  ## UserRole.ADMIN
print(user.role.value)  ## "admin"

## ============================================================================
## SECTION 5: Custom Validators
## ============================================================================

class UserWithValidation(BaseModel):
    username: str
    password: str
    password_confirm: str

    @validator('username')
    def username_alphanumeric(cls, v):
        """
        Custom validator for a single field.
        Runs after type validation.
        """
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()  ## Can transform the value

    @root_validator
    def passwords_match(cls, values):
        """
        Root validator: validates across multiple fields.
        """
        pw1 = values.get('password')
        pw2 = values.get('password_confirm')
        if pw1 != pw2:
            raise ValueError('Passwords do not match')
        return values

## ============================================================================
## SECTION 6: Nested Models
## ============================================================================

class Address(BaseModel):
    street: str
    city: str
    country: str

class UserWithAddress(BaseModel):
    username: str
    address: Address  ## Nested model

user = UserWithAddress(
    username="alice",
    address={
        "street": "123 Main St",
        "city": "NYC",
        "country": "USA"
    }
)

print(user.address.city)  ## Access nested fields

## ============================================================================
## SECTION 7: Serialization
## ============================================================================

class UserComplete(BaseModel):
    username: str
    email: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        ## Control JSON serialization
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

user = UserComplete(username="alice", email="alice@example.com")

## To dict
print(user.dict())

## To JSON string
print(user.json())

## From JSON string
json_str = '{"username": "bob", "email": "bob@example.com"}'
user2 = UserComplete.parse_raw(json_str)

## ============================================================================
## SECTION 8: Real-World Example - Our PDM App
## ============================================================================

class FileCheckoutRequest(BaseModel):
    """
    This is what we'll use in Stage 3 for checkout requests.
    """
    filename: str = Field(
        ...,
        min_length=1,
        max_length=255,
        pattern=r"^[\w\-. ]+\.mcam$",  ## Must end in .mcam
        description="Name of the file to checkout"
    )
    user: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username performing the checkout"
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Reason for checking out the file"
    )

    @validator('filename')
    def sanitize_filename(cls, v):
        """Prevent directory traversal attacks"""
        if '..' in v or '/' in v or '\\' in v:
            raise ValueError('Invalid filename: contains path separators')
        return v

## Test it
try:
    request = FileCheckoutRequest(
        filename="../../etc/passwd",  ## Attack attempt
        user="hacker",
        message="test"
    )
except Exception as e:
    print(f"Blocked attack: {e}")

valid_request = FileCheckoutRequest(
    filename="PN1001.mcam",
    user="john",
    message="Editing part dimensions"
)
print(f"Valid request: {valid_request.dict()}")

if __name__ == "__main__":
    print("Pydantic models explained and tested.")
```

Run it:

```bash
python -m app.learn_pydantic
```

---

### 1.5: Adding Real API Endpoints

**Create schemas directory:**

```bash
mkdir -p backend/app/schemas
touch backend/app/schemas/__init__.py
```

**File: `backend/app/schemas/files.py`**

## **Section 1.5: Pydantic Schemas for File Operations – Tutorial Version**

**Goal:**
Understand how to structure **request and response models** for an API using **Pydantic**, and why **this improves maintainability, security, and clarity** in a FastAPI backend.

---

### **SECTION 1: Response Models**

#### **FileInfo: Representing a Single File**

```python
class FileInfo(BaseModel):
    name: str = Field(..., description="Filename")
    status: str = Field(..., description="available or checked_out")
    size_bytes: int = Field(..., description="File size in bytes")
    locked_by: Optional[str] = Field(None, description="Username who locked the file")
```

**Key Points:**

1. **`BaseModel` inheritance** → all Pydantic models derive validation, serialization, and documentation automatically.
2. **Field descriptors (`Field`)**:

   - `description` → used in **API docs** (`/docs`)
   - `...` → required field (ellipsis)

3. **Optional fields (`Optional[str]`)**:

   - Indicates the field may be `None`
   - Matches real-world scenarios: a file may or may not be locked

```python
file = FileInfo(name="PN1001_OP1.mcam", status="available", size_bytes=1234567)
print(file.locked_by)  ## None
```

**CS Insight:**

- Response models **define the API contract**, separating **internal logic** from **external representation**.
- Using strongly typed response models reduces **runtime errors** and improves **frontend/backend integration**.

---

#### **Schema Examples for Auto-Docs**

```python
class Config:
    schema_extra = {
        "example": {
            "name": "PN1001_OP1.mcam",
            "status": "available",
            "size_bytes": 1234567,
            "locked_by": None
        }
    }
```

- `schema_extra` → FastAPI uses this to **auto-generate OpenAPI docs**
- Example values make **Swagger UI** and **Redoc** interactive and understandable

**Software Engineering Insight:**

- This promotes **self-documenting code** and **reduces cognitive load** for frontend developers consuming your API.

---

#### **FileListResponse: Lists of Files**

```python
class FileListResponse(BaseModel):
    files: List[FileInfo]
    total: int = Field(..., description="Total number of files")
```

- `List[FileInfo]` → **type hints for collections**
- Ensures every item in the list **matches the FileInfo model**
- `total` → provides metadata for **pagination or frontend display**

```python
response = FileListResponse(files=[file], total=1)
print(response.dict())
```

**CS Insight:**

- Validating **collections** ensures consistent **data structures** for APIs
- Reduces **edge-case bugs** when frontend renders a list of files

---

### **SECTION 2: Request Models**

Request models define **expected payloads** from clients. Using Pydantic ensures **input is valid** before reaching your business logic.

#### **FileCheckoutRequest**

```python
class FileCheckoutRequest(BaseModel):
    filename: str = Field(..., min_length=1)
    user: str = Field(..., min_length=3)
    message: str = Field(..., min_length=1, max_length=500)
```

- **Validates string lengths** → prevents empty or malicious input
- **Enforces API contract** → you know the backend will always receive the required fields

```python
request = FileCheckoutRequest(filename="PN1001.mcam", user="john", message="Editing part dimensions")
print(request.dict())
```

**Security Insight:**

- Declarative validation at model level reduces **manual checks** and prevents **basic injection attacks**

---

#### **FileCheckinRequest**

```python
class FileCheckinRequest(BaseModel):
    filename: str
    user: str
```

- Simplified request model for **checking files back in**
- Only the necessary fields are required → **minimal payload**
- Demonstrates **principle of least privilege** in API design

**Software Engineering Insight:**

- Using separate models for **checkout vs checkin** ensures **clear responsibilities**
- Changes in one operation do not affect the other → reduces **coupling**

---

### ✅ **Key Takeaways from Section 1.5**

1. **Response models** (`FileInfo`, `FileListResponse`) define **what your API sends**
2. **Request models** (`FileCheckoutRequest`, `FileCheckinRequest`) define **what your API expects**
3. **Pydantic ensures input/output integrity** automatically: type validation, length checks, optional fields
4. **Schema examples** improve **developer experience** (Swagger/OpenAPI)
5. Clear separation between **internal logic and API contract** → a core **software engineering best practice**
6. Strong typing + declarative validation = fewer runtime errors, easier debugging, more secure code

---

**CS Insight Recap:**

- Pydantic models enforce **data contracts**, a fundamental concept in **distributed systems and API design**
- They combine **type safety (Python), declarative validation (software engineering), and runtime checks (CS)**
- Preparing for **Stage 3** of our PDM app: endpoints that **expect validated inputs** and **return well-structured outputs**

```python
"""
Pydantic schemas for file operations.
These define the shape of request/response data.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

## ============================================================================
## SECTION 1: Response Models
## ============================================================================

class FileInfo(BaseModel):
    """
    Represents a single file in the repository.
    This is what we send to the client.
    """
    name: str = Field(..., description="Filename")
    status: str = Field(..., description="available or checked_out")
    size_bytes: int = Field(..., description="File size in bytes")
    locked_by: Optional[str] = Field(None, description="Username who locked the file")

    class Config:
        ## Example for API documentation
        schema_extra = {
            "example": {
                "name": "PN1001_OP1.mcam",
                "status": "available",
                "size_bytes": 1234567,
                "locked_by": None
            }
        }

class FileListResponse(BaseModel):
    """
    Response for GET /api/files endpoint.
    """
    files: List[FileInfo]
    total: int = Field(..., description="Total number of files")

## ============================================================================
## SECTION 2: Request Models (for future stages)
## ============================================================================

class FileCheckoutRequest(BaseModel):
    """Request body for checking out a file."""
    filename: str = Field(..., min_length=1)
    user: str = Field(..., min_length=3)
    message: str = Field(..., min_length=1, max_length=500)

class FileCheckinRequest(BaseModel):
    """Request body for checking in a file."""
    filename: str
    user: str
```

**File: `backend/app/schemas/__init__.py`**

```python
"""
Export all schemas for easy importing.
"""

from app.schemas.files import (
    FileInfo,
    FileListResponse,
    FileCheckoutRequest,
    FileCheckinRequest
)

__all__ = [
    "FileInfo",
    "FileListResponse",
    "FileCheckoutRequest",
    "FileCheckinRequest"
]
```

---

**Create API directory:**

```bash
mkdir -p backend/app/api
touch backend/app/api/__init__.py
```

**File: `backend/app/api/files.py`**

## **Section 1.5 `files.py` – File Management API Endpoints**

**Goal:**
Understand how to define **API routes in FastAPI**, return **typed responses**, and structure a backend for maintainability. This file is intentionally **thin**, focusing on **route definitions only**, leaving business logic for later (services/ stage).

---

### **SECTION 1: Router Setup**

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/files",
    tags=["files"],
)
```

**Key Points:**

1. **`APIRouter`**:

   - Modular way to define endpoints separate from the main app.
   - Promotes **separation of concerns**, making code **scalable and testable**.

2. **`prefix="/api/files"`**:

   - All routes in this router will be prefixed automatically.
   - E.g., `GET /api/files/` instead of repeating the path in every endpoint.

3. **`tags=["files"]`**:

   - Groups routes in **OpenAPI documentation**.
   - Improves developer experience for anyone using Swagger UI or Redoc.

**Software Engineering Insight:**

- Using routers is a **common pattern in backend frameworks** (like Flask Blueprints or Django apps) to avoid **monolithic code**.
- Encourages **modularity and maintainability**, which is key in real-world software projects.

---

### **SECTION 2: Hardcoded Data (Temporary)**

```python
MOCK_FILES = [
    {"name": "PN1001_OP1.mcam", "status": "available", "size_bytes": 1234567, "locked_by": None},
    {"name": "PN1002_OP1.mcam", "status": "checked_out", "size_bytes": 2345678, "locked_by": "john"},
    {"name": "PN1003_OP1.mcam", "status": "available", "size_bytes": 987654, "locked_by": None}
]
```

**Key Points:**

1. **Temporary hardcoded data** is useful for:

   - **Prototyping endpoints** before implementing actual services
   - Ensuring **API contracts** are working and returning correct types

2. **`locked_by` as `None`** → consistent with `Optional[str]` in Pydantic schemas

**CS Insight:**

- Using mock data is a **standard practice in Test-Driven Development (TDD)**: write your tests/routes before connecting to the database.
- Separates **API behavior** from **business logic**, making incremental development smoother.

---

### **SECTION 3: GET Endpoints**

#### **Get all files**

```python
@router.get("/", response_model=FileListResponse)
def get_files():
    return FileListResponse(files=MOCK_FILES, total=len(MOCK_FILES))
```

**Key Points:**

1. **`@router.get("/")`** → HTTP GET method

2. **`response_model=FileListResponse`**:

   - FastAPI **validates the returned object** against the model
   - Automatically generates **OpenAPI docs**
   - Ensures the frontend **always gets the expected structure**

3. **Return object** is **typed**:

   ```python
   FileListResponse(files=MOCK_FILES, total=len(MOCK_FILES))
   ```

**Software Engineering Insight:**

- Typed responses **reduce runtime errors** and **improve developer confidence**
- This aligns with **interface segregation principle**: the endpoint only exposes what it needs to.

---

#### **Get a single file**

```python
@router.get("/{filename}", response_model=FileInfo)
def get_file(filename: str):
    for file in MOCK_FILES:
        if file["name"] == filename:
            return FileInfo(**file)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"File '{filename}' not found"
    )
```

**Key Points:**

1. **Path parameter `{filename}`**:

   - Passed as a function argument
   - FastAPI automatically converts and validates it as a `str`

2. **Data validation**:

   - `FileInfo(**file)` → ensures mock data conforms to Pydantic model

3. **Error handling**:

   - `HTTPException` with `status_code` and `detail` ensures **RESTful error reporting**
   - FastAPI automatically serializes this to JSON

**CS Insight:**

- Separating **normal flow** vs **exceptional flow** is a core principle of robust backend design.
- Consistent **HTTP status codes** improve API usability and make integrations predictable.

---

### **SECTION 4: Placeholder Endpoints**

```python
@router.post("/checkout")
def checkout_file():
    return {"message": "Checkout endpoint - coming in Stage 3"}

@router.post("/checkin")
def checkin_file():
    return {"message": "Checkin endpoint - coming in Stage 3"}
```

**Key Points:**

1. These endpoints are **stubs**:

   - Defined now to complete the **API contract**
   - Implementation comes later in **services/**

2. **Why placeholders?**

   - Allows **frontend development** to start
   - Enables **integration testing** without full backend logic
   - Encourages **iterative development** (Agile principle)

---

### ✅ **Key Takeaways from `files.py`**

1. **Routers modularize endpoints**, keeping main app clean
2. **Response models enforce type safety** and **generate docs** automatically
3. **Path parameters + validation** ensure endpoints are robust and predictable
4. **Mock data** allows early-stage testing before implementing business logic
5. **Placeholder endpoints** help maintain a **working API contract** for frontend/backend integration
6. **Error handling via HTTPException** is crucial for **RESTful API design**

---

**CS & SE Insight Recap:**

- **Modularity** → `APIRouter` promotes separation of concerns
- **Type safety** → Pydantic models enforce contracts at runtime
- **Iterative development** → mock data + stubs enable early testing and frontend integration
- **Error handling** → clear and predictable API responses
- **Documentation** → auto-generated OpenAPI docs improve developer experience

```python
"""
File management API endpoints.

This file contains ONLY route definitions.
Business logic will go in services/ (Stage 3).
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.files import FileInfo, FileListResponse
from typing import List

## ============================================================================
## SECTION 1: Router Setup
## ============================================================================

router = APIRouter(
    prefix="/api/files",
    tags=["files"],  ## Groups endpoints in OpenAPI docs
)

## ============================================================================
## SECTION 2: Hardcoded Data (Temporary - Stage 3 will read from filesystem)
## ============================================================================

MOCK_FILES = [
    {
        "name": "PN1001_OP1.mcam",
        "status": "available",
        "size_bytes": 1234567,
        "locked_by": None
    },
    {
        "name": "PN1002_OP1.mcam",
        "status": "checked_out",
        "size_bytes": 2345678,
        "locked_by": "john"
    },
    {
        "name": "PN1003_OP1.mcam",
        "status": "available",
        "size_bytes": 987654,
        "locked_by": None
    }
]

## ============================================================================
## SECTION 3: GET Endpoints
## ============================================================================

@router.get("/", response_model=FileListResponse)
def get_files():
    """
    Get list of all files in the repository.

    Returns:
        FileListResponse: List of files with metadata

    Future improvements (Stage 3):
    - Read from actual filesystem
    - Add pagination
    - Add filtering by status
    - Add sorting
    """
    return FileListResponse(
        files=MOCK_FILES,
        total=len(MOCK_FILES)
    )

@router.get("/{filename}", response_model=FileInfo)
def get_file(filename: str):
    """
    Get details for a specific file.

    Args:
        filename: The filename (path parameter)

    Returns:
        FileInfo: File metadata

    Raises:
        404: File not found
    """
    ## Find file in our mock data
    for file in MOCK_FILES:
        if file["name"] == filename:
            return FileInfo(**file)

    ## Not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"File '{filename}' not found"
    )

## ============================================================================
## SECTION 4: Placeholder Endpoints (Will implement in Stage 3)
## ============================================================================

@router.post("/checkout")
def checkout_file():
    """
    Check out a file for editing.

    Implementation coming in Stage 3.
    """
    return {"message": "Checkout endpoint - coming in Stage 3"}

@router.post("/checkin")
def checkin_file():
    """
    Check in a file after editing.

    Implementation coming in Stage 3.
    """
    return {"message": "Checkin endpoint - coming in Stage 3"}
```

**File: `backend/app/api/__init__.py`**

```python
"""
API router aggregation.
"""

from app.api import files

__all__ = ["files"]
```

---

**Update `backend/app/main.py` to include the router:**

```python
## Add this import at the top
from app.api import files

## Add this after middleware configuration, before startup events:

## ====================================================================
## SECTION 2.5: Include Routers
## ====================================================================

app.include_router(files.router)
```

**Test the endpoints:**

```bash
## Restart server
uvicorn app.main:app --reload

## In another terminal or browser:
curl http://127.0.0.1:8000/api/files
curl http://127.0.0.1:8000/api/files/PN1001_OP1.mcam
curl http://127.0.0.1:8000/api/files/nonexistent.mcam  ## Should return 404
```

---

### 1.6: Interactive API Documentation

FastAPI automatically generates interactive API docs.

**Visit these URLs:**

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

**In the Swagger UI (/docs):**

1. Click on "GET /api/files"
2. Click "Try it out"
3. Click "Execute"
4. See the response

**Why this is powerful:**

- **No extra work**: Generated from your code
- **Always accurate**: Can't drift from implementation
- **Interactive testing**: Try endpoints without curl
- **Client generation**: Can generate client libraries from openapi.json

---

### Stage 1 Complete

**File structure you now have:**

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 ## App entry point
│   ├── config.py               ## Configuration
│   ├── learn_asgi.py           ## Educational - ASGI concepts
│   ├── learn_http.py           ## Educational - HTTP concepts
│   ├── learn_pydantic.py       ## Educational - Pydantic
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── files.py            ## Data models
│   └── api/
│       ├── __init__.py
│       └── files.py            ## File endpoints
├── static/                     ## Ready for Stage 2
├── tests/
├── venv/
└── requirements.txt
```

**Verification Checklist:**

- [ ] Server runs: `uvicorn app.main:app --reload`
- [ ] Root endpoint works: http://127.0.0.1:8000
- [ ] Files endpoint works: http://127.0.0.1:8000/api/files
- [ ] Single file endpoint works: http://127.0.0.1:8000/api/files/PN1001_OP1.mcam
- [ ] 404 error works: http://127.0.0.1:8000/api/files/fake.mcam
- [ ] API docs load: http://127.0.0.1:8000/docs
- [ ] Ran and understood `learn_asgi.py`
- [ ] Ran and understood `learn_http.py`
- [ ] Ran and understood `learn_pydantic.py`

**What you learned:**

- ASGI vs WSGI and why FastAPI is fast
- HTTP protocol fundamentals
- Pydantic models for data validation
- FastAPI routing and path operations
- Response models and automatic documentation
- Professional code organization (routes in api/, models in schemas/)

**Next**: Stage 2 - Building the frontend with proper CSS architecture and theme system.

Ready for Stage 2?

## Stage 2: Professional Frontend Architecture

**Prerequisites**: You have a working FastAPI backend from Stage 1.

**Goal**: Transform our basic API into a visually appealing, interactive, and professionally structured web application.

---

### 2.1: The HTML Skeleton - Structuring the Document

Our first step is to create the HTML file that will be the skeleton of our entire frontend. HTML provides the **content** and **structure**—think of it as the framing of a house.

#### Step 1: Create the `index.html` file

**Action**: Create the main HTML file for our frontend.

**File**: `backend/static/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PDM System</title>
  </head>
  <body>
    <header>
      <h1>PDM System</h1>
    </header>
    <main>
      <section>
        <h2>Available Files</h2>
        <div id="file-list">
          <p>Loading files...</p>
        </div>
      </section>
    </main>
    <footer>
      <p>&copy; 2025 PDM Tutorial Project</p>
    </footer>
  </body>
</html>
```

#### Deep Dive: Understanding the HTML Structure 🧠

- `<!DOCTYPE html>`: This is the **document type declaration**. It's not a tag but an instruction to the browser that says, "Hey, interpret this document using the HTML5 standard." It must always be the very first line.

- `<html lang="en">`: This is the **root element** of the page. The `lang="en"` attribute is crucial for **accessibility** and **SEO**; it tells screen readers and search engines that the page's primary language is English.

- `<head>`: This section contains **metadata**—data about your HTML document that is not displayed on the page itself.

  - `<meta charset="UTF-8" />`: Sets the character encoding to UTF-8. This is a universal standard that can represent virtually any character from any language, preventing issues with special symbols or international text.
  - `<meta name="viewport" ...>`: This is the cornerstone of **responsive design**. `width=device-width` tells the browser to make the page width equal to the screen width of the device (like a phone or tablet). `initial-scale=1.0` sets the initial zoom level to 100%. Without this, mobile browsers would show a zoomed-out desktop version of your site.
  - `<title>`: This text appears in the browser tab and is used for bookmarks and search engine results.

- `<body>`: This contains all the **visible content** of your webpage.

- **Semantic Tags (`<header>`, `<main>`, `<section>`, `<footer>`):**

  - **Why not just use `<div>` for everything?** While you could, semantic tags give your content meaning.
  - `<header>`: Represents introductory content, typically a group of introductory or navigational aids.
  - `<main>`: Specifies the main, dominant content of the document. There should only be one `<main>` element per page.
  - `<section>`: Represents a standalone thematic grouping of content.
  - **Benefit**: This structure is invaluable for screen readers, which can use it to help visually impaired users navigate your page (e.g., "Jump to main content"). It also helps search engines understand your page's structure.

#### Deep Dive: The DOM (Document Object Model) 🌳

When the browser reads your `index.html` file, it doesn't just display it. It builds an in-memory tree structure called the **DOM**. Each HTML tag becomes an "object" or "node" in this tree.

Our simple HTML becomes this tree in the browser's memory:

```
(Document)
└── html
    ├── head
    │   ├── meta
    │   └── title
    └── body
        ├── header
        │   └── h1
        ├── main
        │   └── section
        │       ├── h2
        │       └── div#file-list
        └── footer
            └── p
```

JavaScript's primary job on the frontend is to interact with and manipulate this DOM tree to make the page dynamic. The `id="file-list"` is a unique identifier we'll use later to find that specific `div` and insert our file data into it.

---

### 2.2: Connecting Backend to Frontend

Now that we have an HTML file, we need to tell our FastAPI backend how to serve it to the user.

#### Step 1: Update `main.py` to serve static files

**Action**: Modify your main application file to mount the `static` directory and serve `index.html` at the root URL.

**File**: `backend/app/main.py`

```python
## Add these imports at the top
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings ## We'll use this for paths

## ... inside your create_application() function ...

def create_application() -> FastAPI:
    ## ... after your app = FastAPI(...) line and middleware ...

    ## ====================================================================
    ## SECTION 2.5: Static Files & Frontend Entry Point
    ## ====================================================================

    ## 1. Mount the 'static' directory
    ## This tells FastAPI: "Any URL that starts with '/static' should be treated
    ## as a request for a file from the 'backend/static' folder on disk."
    app.mount(
        "/static",
        StaticFiles(directory=settings.BASE_DIR / "static"),
        name="static"
    )

    ## 2. Serve the main index.html file for the root URL ("/")
    ## This creates a special endpoint for the homepage.
    @app.get("/", response_class=FileResponse, include_in_schema=False)
    async def serve_frontend():
        """Serves the main application's HTML entry point."""
        ## FileResponse is an efficient way to send a file directly from disk.
        ## 'include_in_schema=False' hides this from our API docs, as it's for the UI.
        return FileResponse(settings.BASE_DIR / "static/index.html")

    ## ... keep the rest of the function (startup/shutdown events, routers) ...
```

#### Deep Dive: `mount` vs. `get` and MIME Types ⚙️

- **`app.mount(...)`**: This is for serving an **entire directory**. It's highly optimized for static files. When a request comes in for `/static/css/style.css`, the `StaticFiles` application handles it directly, bypassing most of FastAPI's complex routing logic for better performance.

- **`@app.get("/")` with `FileResponse`**: This is for serving a **single, specific file** at a specific endpoint. We use it for our `index.html` because it's the entry point to our entire Single Page Application (SPA).

- **MIME Types**: When the server sends a file, it includes a `Content-Type` header (also called a MIME type). This tells the browser how to handle the file.

  - `text/html`: The browser renders it as a webpage.
  - `text/css`: The browser parses it as a stylesheet.
  - `application/javascript`: The browser executes it as a script.
  - `image/jpeg`: The browser displays it as an image.
    `StaticFiles` and `FileResponse` automatically guess the correct MIME type based on the file extension (`.html`, `.css`, etc.), which is crucial for the frontend to work correctly.

**Test your changes**: Restart your server (`uvicorn app.main:app --reload`) and visit `http://127.0.0.1:8000`. You should now see your unstyled HTML page.

---

### 2.3: Building the Design System (CSS)

A professional frontend is built on a **design system**—a single source of truth for all design decisions. We'll create ours using **CSS Custom Properties** (variables). This makes our application themeable, consistent, and easy to maintain. We'll organize our CSS files using the **ITCSS (Inverted Triangle CSS)** architecture.

#### Step 1: Create the Design Tokens (Settings Layer)

Design tokens are the fundamental building blocks of your UI. They are named variables for colors, spacing, fonts, etc.

**Action**: Create a new CSS file for our tokens.

**File**: `backend/static/css/tokens.css`

```css
/**
 * Design Tokens - The Single Source of Truth for our UI
 *
 * These CSS custom properties (variables) are defined in the :root selector,
 * which makes them globally available throughout the entire application.
 * They are the "atoms" of our design system.
 */

:root {
  /* =========================================================================
     COLOR PALETTE - These are the raw, primitive colors available.
     We use a 50-900 scale (e.g., --color-primary-50 to --color-primary-900),
     where 500 is the base color. This is a professional standard that allows
     for a wide range of shades for different UI states (backgrounds, borders, text).
     ========================================================================= */

  /* Primary Brand Color: A professional, cool-toned indigo. */
  --color-primary-50: #f5f7ff; /* For very subtle hover states or backgrounds. */
  --color-primary-100: #ebf0ff;
  --color-primary-200: #d6e0ff;
  --color-primary-300: #b3c7ff;
  --color-primary-400: #8da9ff;
  --color-primary-500: #667eea; /* The main brand color for primary buttons and links. */
  --color-primary-600: #5568d3; /* A slightly darker shade for hover states. */
  --color-primary-700: #4453b8; /* Even darker, for active/pressed states. */
  --color-primary-800: #353f8f;
  --color-primary-900: #2a3166; /* Darkest shade, suitable for text on light backgrounds. */

  /* Neutral Grays: The backbone of any UI for text, borders, and backgrounds. */
  --color-gray-50: #fafafa;
  --color-gray-100: #f5f5f5;
  --color-gray-200: #e5e5e5;
  --color-gray-300: #d4d4d4;
  --color-gray-400: #a3a3a3;
  --color-gray-500: #737373;
  --color-gray-600: #525252;
  --color-gray-700: #404040;
  --color-gray-800: #262626;
  --color-gray-900: #171717;

  /* Semantic Colors: Colors that have a specific meaning. */
  --color-success-500: #10b981; /* For success states, "available" status. */
  --color-success-600: #059669;
  --color-warning-500: #f59e0b; /* For warnings, "checked-out" status. */
  --color-warning-600: #d97706;
  --color-danger-500: #ef4444; /* For errors and destructive actions. */
  --color-danger-600: #dc2626;
  --color-info-500: #3b82f6; /* For informational messages and highlights. */
  --color-info-600: #2563eb;

  /* =========================================================================
     SPACING SCALE - A consistent scale for margins, padding, and gaps.
     Using a mathematical scale (like 4px or 8px increments) creates visual harmony.
     The 'rem' unit is relative to the root font size, making the UI scalable.
     ========================================================================= */
  --spacing-1: 0.25rem; /* 4px (assuming root font-size is 16px) */
  --spacing-2: 0.5rem; /* 8px */
  --spacing-3: 0.75rem; /* 12px */
  --spacing-4: 1rem; /* 16px - our most common base unit. */
  --spacing-6: 1.5rem; /* 24px */
  --spacing-8: 2rem; /* 32px */

  /* =========================================================================
     TYPOGRAPHY SCALE - For a consistent and readable text hierarchy.
     ========================================================================= */
  /* Font Families */
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif; /* Uses the native font of the user's OS for a familiar feel. */
  --font-mono: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas,
    "Courier New", monospace; /* For code or other fixed-width text. */

  /* Font Sizes - Using a modular scale makes the hierarchy look intentional and professional. */
  --font-size-sm: 0.875rem; /* 14px - For small text like hints or metadata. */
  --font-size-base: 1rem; /* 16px - The default body text size. */
  --font-size-lg: 1.125rem; /* 18px */
  --font-size-xl: 1.25rem; /* 20px */
  --font-size-2xl: 1.5rem; /* 24px - For subheadings. */
  --font-size-3xl: 1.875rem; /* 30px */
  --font-size-4xl: 2.25rem; /* 36px - For main headings. */

  /* Font Weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Line Heights - For optimal text readability. */
  --line-height-tight: 1.25; /* For headings. */
  --line-height-base: 1.5; /* For body text. */

  /* =========================================================================
     SEMANTIC TOKENS - LIGHT THEME (Default)
     These tokens give our primitive tokens meaning. Instead of using a raw color
     like '--color-gray-900', we'll use '--text-primary'. This abstraction
     is what allows us to create themes easily.
     ========================================================================= */
  /* Backgrounds */
  --bg-primary: #ffffff; /* The main page background. */
  --bg-secondary: var(
    --color-gray-50
  ); /* A slightly off-white for subtle contrast. */
  --bg-tertiary: var(--color-gray-100); /* Background for cards and sections. */

  /* Text */
  --text-primary: var(--color-gray-900); /* Main body text. High contrast. */
  --text-secondary: var(
    --color-gray-600
  ); /* Lighter text for subtitles, metadata. */
  --text-inverse: #ffffff; /* Text used on dark/colored backgrounds. */
  --text-link: var(--color-primary-600); /* The color for hyperlinks. */

  /* Borders */
  --border-default: var(--color-gray-200); /* The default color for borders. */
  --border-focus: var(--color-primary-500); /* The color for focused inputs. */

  /* Statuses */
  --status-success-bg: rgba(
    16,
    185,
    129,
    0.1
  ); /* Background for the 'available' badge. */
  --status-success-text: var(
    --color-success-600
  ); /* Text color for the 'available' badge. */
  --status-warning-bg: rgba(
    245,
    158,
    11,
    0.1
  ); /* Background for the 'checked-out' badge. */
  --status-warning-text: var(
    --color-warning-600
  ); /* Text color for the 'checked-out' badge. */
}
```

#### Step 2: Create the Base Styles (Generic & Elements Layers)

This file will contain our CSS reset and default styles for raw HTML tags like `<body>`, `<h1>`, `p`, etc., using our new design tokens.

**Action**: Create a new CSS file for our base styles.

**File**: `backend/static/css/base.css`

```css
/**
 * Base Styles & CSS Reset
 *
 * This file normalizes browser styles and sets defaults for raw HTML elements
 * using the design tokens we defined in tokens.css.
 */

/* A modern, targeted CSS reset to ensure cross-browser consistency. */
*,
*::before,
*::after {
  box-sizing: border-box; /* This makes layout math predictable. width + padding + border = total width. */
  margin: 0; /* Removes inconsistent default margins. */
  padding: 0; /* Removes inconsistent default padding. */
}

/* Base styles for the entire page. */
body {
  font-family: var(--font-sans); /* Use our defined sans-serif font stack. */
  font-size: var(--font-size-base); /* Set the default font size. */
  line-height: var(
    --line-height-base
  ); /* Improve readability with a good line height. */
  color: var(
    --text-primary
  ); /* Use our semantic token for primary text color. */
  background-color: var(
    --bg-primary
  ); /* Use our semantic token for the main background. */
}

/* Default styles for headings. */
h1 {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  margin-bottom: var(
    --spacing-2
  ); /* Consistent spacing below the main heading. */
}

h2 {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  margin-bottom: var(--spacing-6); /* More space below section headings. */
  color: var(--text-link); /* Use the link color for emphasis. */
}

/* Default style for paragraphs. */
p {
  margin-bottom: var(--spacing-4); /* Consistent spacing between paragraphs. */
  color: var(
    --text-secondary
  ); /* Use the secondary text color for less emphasis. */
}

/* Default style for links. */
a {
  color: var(--text-link);
  text-decoration: none; /* Remove the default underline. */
  transition: color 150ms ease-in-out; /* Smooth color transition on hover. */
}
a:hover {
  text-decoration: underline; /* Add underline back on hover for affordance. */
}
```

#### Step 3: Create the Component Styles

Now we style our specific UI components.

**Action**: Create a new CSS file for our component styles.

**File**: `backend/static/css/components.css`

```css
/**
 * Component Styles
 *
 * This file contains styles for our reusable UI components, like the header,
 * main layout, and the file list.
 */

.container {
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--spacing-4);
  padding-right: var(--spacing-4);
}

header {
  background: linear-gradient(
    135deg,
    var(--color-primary-500),
    var(--color-primary-700)
  );
  color: var(--text-inverse);
  padding: var(--spacing-6);
  box-shadow: var(--shadow-md);
}
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--spacing-4);
  flex-wrap: wrap;
  max-width: 1200px; /* To align with the main container */
  margin: 0 auto;
}
.header-content h1 {
  color: var(--text-inverse); /* Override the default h1 color */
  font-size: var(--font-size-3xl);
  margin-bottom: 0;
}
.header-content p {
  color: var(--text-inverse);
  opacity: 0.8;
  margin-bottom: 0;
}

main {
  padding: var(--spacing-8) 0;
}

footer {
  text-align: center;
  padding: var(--spacing-8);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  border-top: 1px solid var(--border-default);
}

section {
  background: var(--bg-primary);
  padding: var(--spacing-6);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-base);
  border: 1px solid var(--border-default);
  margin-bottom: var(--spacing-8);
}

#file-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}

.file-item {
  padding: var(--spacing-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-base);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-secondary);
  transition: all 150ms ease-in-out;
}
.file-item:hover {
  border-color: var(--border-focus);
  transform: translateX(5px);
  box-shadow: var(--shadow-sm);
}

.file-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
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
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.status-available {
  background: var(--status-success-bg);
  color: var(--status-success-text);
}
.status-checked_out {
  background: var(--status-warning-bg);
  color: var(--status-warning-text);
}

.loading {
  text-align: center;
  padding: var(--spacing-8);
  color: var(--text-secondary);
  font-style: italic;
}
```

#### Step 4: Create the CSS Entry Point

This file will combine all our CSS files in the correct order.

**Action**: Create the main CSS entry point.

**File**: `backend/static/css/main.css`

```css
/**
 * Main CSS Entry Point
 *
 * Imports all CSS files in the correct ITCSS order. This is the only
 * file that needs to be linked in the HTML.
 */

@import "tokens.css";
@import "base.css";
@import "components.css";
```

#### Step 5: Link the CSS in HTML

Finally, let's link our new `main.css` file in our HTML.

**Action**: Update the `<head>` of your `index.html`.

**File**: `backend/static/index.html`

```html
<head>
  <title>PDM System</title>
  <link rel="stylesheet" href="/static/css/main.css" />
</head>
```

**Test your changes**: Refresh your browser. Your application should now be beautifully styled using your new design system\!

---

### 2.4: The JavaScript Brains

Now, let's write the JavaScript to fetch data from our API and dynamically render the file list. We'll build this in a modular way.

#### Step 1: Create the API Client Module

This module will handle all communication with our backend.

**Action**: Create the API client file.

**File**: `backend/static/js/modules/api-client.js`

```javascript
/**
 * API Client Module
 * A centralized place for all backend communication. This abstraction makes our
 * code cleaner and easier to maintain.
 */
export class APIClient {
  constructor(baseURL = "") {
    this.baseURL = baseURL;
  }

  /**
   * A generic method for making HTTP requests.
   * It handles common tasks like setting headers and parsing errors.
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      ...options,
      headers: { "Content-Type": "application/json", ...options.headers },
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP Error: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`API Error on ${endpoint}:`, error);
      throw error;
    }
  }

  // A specific method for getting the file list.
  async getFiles() {
    return this.request("/api/files", { method: "GET" });
  }
}

// Export a single instance for the whole application to use.
export const apiClient = new APIClient();
```

#### Step 2: Create the Theme Manager Module

This module will manage our light/dark mode functionality.

**Action**: Create the theme manager file.

**File**: `backend/static/js/modules/theme-manager.js`

```javascript
/**
 * Theme Management Module
 * Handles light/dark theme switching, system preference detection,
 * and saving the user's choice to localStorage.
 */
class ThemeManager {
  constructor() {
    this.STORAGE_KEY = "pdm-theme";
    this.init();
  }

  // Determines the initial theme based on localStorage or system settings.
  getInitialTheme() {
    const storedTheme = localStorage.getItem(this.STORAGE_KEY);
    if (storedTheme) return storedTheme;
    if (
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
    ) {
      return "dark";
    }
    return "light";
  }

  // Applies a theme by setting the 'data-theme' attribute on the <html> element.
  applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    const toggleButton = document.getElementById("theme-toggle");
    if (toggleButton) {
      toggleButton.innerHTML = theme === "dark" ? "☀️" : "🌙";
      toggleButton.setAttribute(
        "aria-label",
        `Switch to ${theme === "dark" ? "light" : "dark"} mode`
      );
    }
  }

  // Toggles the theme and saves the new preference.
  toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    this.applyTheme(newTheme);
    localStorage.setItem(this.STORAGE_KEY, newTheme);
  }

  // Initializes the theme system.
  init() {
    this.applyTheme(this.getInitialTheme());
  }
}

// Create and export a single instance of the ThemeManager.
export const themeManager = new ThemeManager();
```

#### Step 3: Create the Main Application Logic

This is our main script. It will import the modules and orchestrate the application.

**Action**: Create the main app logic file.

**File**: `backend/static/js/app.js`

```javascript
/**
 * Main Application Logic
 * Initializes the app, fetches data, renders the UI, and handles events.
 */
import { apiClient } from "./modules/api-client.js";
import { themeManager } from "./modules/theme-manager.js";

// The 'DOMContentLoaded' event ensures our script runs only after the full HTML is loaded.
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM loaded. Initializing PDM app.");

  // Set up the theme toggle button.
  const toggleButton = document.getElementById("theme-toggle");
  if (toggleButton) {
    toggleButton.addEventListener("click", () => themeManager.toggleTheme());
  }

  loadFiles(); // Fetch and display the initial file list.
});

/**
 * Fetches files from the API and calls the function to display them.
 */
async function loadFiles() {
  const fileListEl = document.getElementById("file-list");
  fileListEl.innerHTML = `<div class="loading"><p>Loading files...</p></div>`;

  try {
    const data = await apiClient.getFiles();
    displayFiles(data.files);
  } catch (error) {
    fileListEl.innerHTML = `<p style="color: var(--color-danger-500);">Error: ${error.message}</p>`;
  }
}

/**
 * Renders the list of files into the DOM.
 */
function displayFiles(files) {
  const container = document.getElementById("file-list");
  container.innerHTML = ""; // Clear the loading message.

  if (!files || files.length === 0) {
    container.innerHTML = "<p>No files found.</p>";
    return;
  }

  const fragment = document.createDocumentFragment();
  files.forEach((file) => {
    fragment.appendChild(createFileElement(file));
  });
  container.appendChild(fragment);
}

/**
 * Creates and returns a DOM element for a single file.
 */
function createFileElement(file) {
  const div = document.createElement("div");
  div.className = "file-item";

  const infoDiv = document.createElement("div");
  infoDiv.className = "file-info";

  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ");

  infoDiv.appendChild(nameSpan);
  infoDiv.appendChild(statusSpan);
  div.appendChild(infoDiv);

  return div;
}
```

#### Step 4: Add the Theme Toggle Button

Let's add the button to our HTML so the JavaScript can find it.

**Action**: Add the button to `index.html`.

**File**: `backend/static/index.html`
_Inside the `<div class="header-actions">`_

```html
<button
  id="theme-toggle"
  class="btn"
  title="Toggle light/dark mode"
  aria-label="Switch to dark mode"
></button>
```

---

### Stage 2 Complete ✅

**Final Check**: Run your server and visit `http://127.0.0.1:8000`. You should see a professional, styled web page that fetches your file list from the API and allows you to toggle between light and dark themes.

#### What You've Built

- A professionally structured frontend using HTML, CSS, and modular JavaScript.
- A complete, themeable design system using CSS Custom Properties.
- A dynamic UI that fetches data from a backend API and renders it to the DOM.

#### Key Concepts Mastered

- **CSS Architecture (ITCSS)**: Organizing styles for scalability.
- **Design Systems**: Using design tokens as a single source of truth.
- **Theming**: Implementing light/dark mode with CSS variables.
- **JavaScript Modules**: Separating concerns into reusable classes like `APIClient` and `ThemeManager`.
- **Asynchronous JavaScript**: Using `async/await` and `fetch` for non-blocking network requests.
- **DOM Manipulation**: Dynamically creating and updating HTML elements with JavaScript.

## Stage 2: Professional Frontend Architecture

**Prerequisites**: Completed Stage 1

**Time**: 4-5 hours

**What you'll build**: A production-ready frontend with design system, theme switching, and API integration.

---

### 2.1: Deep Dive - CSS Architecture & Design Systems

**File: `backend/static/css/learn_css_architecture.css`**

```css
/*
Understanding CSS Architecture: Why we split CSS into multiple files

THE PROBLEM:
One big CSS file becomes unmaintainable:
- Hard to find styles
- Duplicate code
- Specificity wars
- Can't reuse across projects

THE SOLUTION: ITCSS (Inverted Triangle CSS)
A methodology for organizing CSS from generic to specific:

1. Settings     - Variables, design tokens (--color-primary)
2. Tools        - Mixins, functions (not needed with CSS variables)
3. Generic      - Resets, normalize
4. Elements     - Raw HTML elements (h1, p, a)
5. Objects      - Layout primitives (.container, .grid)
6. Components   - UI components (.button, .card)
7. Utilities    - Single-purpose (.text-center, .mt-4)

We'll use: Settings (tokens) → Generic (base) → Components

WHY DESIGN TOKENS?
Design tokens are the "single source of truth" for design decisions.
Change one token, update entire site.

Example:
--color-primary: #667eea;

Used in:
- Buttons
- Links  
- Headers
- Focus states
- Icons

Change to --color-primary: #ff0000; → Everything updates

SPECIFICITY RULES:
0,0,0,1   - element selector (h1)
0,0,1,0   - class selector (.button)
0,1,0,0   - id selector (#header)
1,0,0,0   - inline style

Keep specificity low for maintainability.
Use classes, avoid IDs for styling.
*/
```

---

### 2.2: Design Token System

**File: `backend/static/css/tokens.css`**

```css
/**
 * Design Tokens - Single Source of Truth
 * 
 * These CSS custom properties define our design system.
 * They cascade through the entire application.
 */

:root {
  /* =========================================================================
     COLOR PALETTE - Base Colors
     ========================================================================= */

  /* Primary Brand Color */
  --color-primary-50: #f5f7ff;
  --color-primary-100: #ebf0ff;
  --color-primary-200: #d6e0ff;
  --color-primary-300: #b3c7ff;
  --color-primary-400: #8da9ff;
  --color-primary-500: #667eea; /* Main brand color */
  --color-primary-600: #5568d3;
  --color-primary-700: #4453b8;
  --color-primary-800: #353f8f;
  --color-primary-900: #2a3166;

  /* Neutral Grays */
  --color-gray-50: #fafafa;
  --color-gray-100: #f5f5f5;
  --color-gray-200: #e5e5e5;
  --color-gray-300: #d4d4d4;
  --color-gray-400: #a3a3a3;
  --color-gray-500: #737373;
  --color-gray-600: #525252;
  --color-gray-700: #404040;
  --color-gray-800: #262626;
  --color-gray-900: #171717;

  /* Semantic Colors */
  --color-success-500: #10b981;
  --color-success-600: #059669;
  --color-warning-500: #f59e0b;
  --color-warning-600: #d97706;
  --color-danger-500: #ef4444;
  --color-danger-600: #dc2626;
  --color-info-500: #3b82f6;
  --color-info-600: #2563eb;

  /* =========================================================================
     SPACING SCALE - Based on 4px
     ========================================================================= */

  --spacing-1: 0.25rem; /* 4px */
  --spacing-2: 0.5rem; /* 8px */
  --spacing-3: 0.75rem; /* 12px */
  --spacing-4: 1rem; /* 16px */
  --spacing-5: 1.25rem; /* 20px */
  --spacing-6: 1.5rem; /* 24px */
  --spacing-8: 2rem; /* 32px */
  --spacing-10: 2.5rem; /* 40px */
  --spacing-12: 3rem; /* 48px */
  --spacing-16: 4rem; /* 64px */

  /* =========================================================================
     TYPOGRAPHY SCALE
     ========================================================================= */

  /* Font Families */
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  --font-mono: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas,
    "Courier New", monospace;

  /* Font Sizes - Modular scale (1.250 ratio) */
  --font-size-xs: 0.75rem; /* 12px */
  --font-size-sm: 0.875rem; /* 14px */
  --font-size-base: 1rem; /* 16px */
  --font-size-lg: 1.125rem; /* 18px */
  --font-size-xl: 1.25rem; /* 20px */
  --font-size-2xl: 1.5rem; /* 24px */
  --font-size-3xl: 1.875rem; /* 30px */
  --font-size-4xl: 2.25rem; /* 36px */
  --font-size-5xl: 3rem; /* 48px */

  /* Font Weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Line Heights */
  --line-height-tight: 1.25;
  --line-height-base: 1.5;
  --line-height-relaxed: 1.75;

  /* =========================================================================
     BORDER RADIUS
     ========================================================================= */

  --radius-sm: 0.125rem; /* 2px */
  --radius-base: 0.25rem; /* 4px */
  --radius-md: 0.375rem; /* 6px */
  --radius-lg: 0.5rem; /* 8px */
  --radius-xl: 0.75rem; /* 12px */
  --radius-2xl: 1rem; /* 16px */
  --radius-full: 9999px; /* Pill shape */

  /* =========================================================================
     SHADOWS
     ========================================================================= */

  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-base: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);

  /* =========================================================================
     TRANSITIONS
     ========================================================================= */

  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);

  /* =========================================================================
     Z-INDEX SCALE
     ========================================================================= */

  --z-dropdown: 1000;
  --z-sticky: 1020;
  --z-fixed: 1030;
  --z-modal-backdrop: 1040;
  --z-modal: 1050;
  --z-popover: 1060;
  --z-tooltip: 1070;

  /* =========================================================================
     SEMANTIC TOKENS - Light Theme (Default)
     These reference the base colors above
     ========================================================================= */

  /* Backgrounds */
  --bg-primary: #ffffff;
  --bg-secondary: var(--color-gray-50);
  --bg-tertiary: var(--color-gray-100);
  --bg-inverse: var(--color-gray-900);

  /* Text */
  --text-primary: var(--color-gray-900);
  --text-secondary: var(--color-gray-600);
  --text-tertiary: var(--color-gray-500);
  --text-inverse: #ffffff;
  --text-link: var(--color-primary-600);
  --text-link-hover: var(--color-primary-700);

  /* Borders */
  --border-default: var(--color-gray-200);
  --border-hover: var(--color-gray-300);
  --border-focus: var(--color-primary-500);

  /* Interactive */
  --interactive-primary: var(--color-primary-500);
  --interactive-primary-hover: var(--color-primary-600);
  --interactive-primary-active: var(--color-primary-700);
  --interactive-primary-alpha: rgba(102, 126, 234, 0.1);

  /* Status */
  --status-success: var(--color-success-500);
  --status-success-bg: rgba(16, 185, 129, 0.1);
  --status-success-text: var(--color-success-600);

  --status-warning: var(--color-warning-500);
  --status-warning-bg: rgba(245, 158, 11, 0.1);
  --status-warning-text: var(--color-warning-600);

  --status-danger: var(--color-danger-500);
  --status-danger-bg: rgba(239, 68, 68, 0.1);
  --status-danger-text: var(--color-danger-600);

  --status-info: var(--color-info-500);
  --status-info-bg: rgba(59, 130, 246, 0.1);
  --status-info-text: var(--color-info-600);

  /* Cards & Components */
  --card-bg: var(--bg-primary);
  --card-border: var(--border-default);
  --card-shadow: var(--shadow-base);
  --card-padding: var(--spacing-6);
  --card-border-radius: var(--radius-lg);

  /* Buttons */
  --button-padding-x: var(--spacing-4);
  --button-padding-y: var(--spacing-2);
  --button-border-radius: var(--radius-base);
  --button-transition: var(--transition-base);

  --button-primary-bg: var(--interactive-primary);
  --button-primary-bg-hover: var(--interactive-primary-hover);
  --button-primary-text: var(--text-inverse);

  --button-secondary-bg: var(--bg-secondary);
  --button-secondary-bg-hover: var(--bg-tertiary);
  --button-secondary-text: var(--text-primary);

  /* Modals */
  --modal-backdrop: rgba(0, 0, 0, 0.5);
  --modal-bg: var(--bg-primary);
  --modal-shadow: var(--shadow-xl);
  --modal-border-radius: var(--radius-xl);
}

/* =========================================================================
   DARK THEME
   Override semantic tokens for dark mode
   ========================================================================= */

[data-theme="dark"] {
  /* Backgrounds - Inverted */
  --bg-primary: var(--color-gray-900);
  --bg-secondary: var(--color-gray-800);
  --bg-tertiary: var(--color-gray-700);
  --bg-inverse: var(--color-gray-50);

  /* Text - Inverted */
  --text-primary: var(--color-gray-50);
  --text-secondary: var(--color-gray-300);
  --text-tertiary: var(--color-gray-400);
  --text-inverse: var(--color-gray-900);
  --text-link: var(--color-primary-400);
  --text-link-hover: var(--color-primary-300);

  /* Borders - Lighter in dark mode */
  --border-default: var(--color-gray-700);
  --border-hover: var(--color-gray-600);
  --border-focus: var(--color-primary-400);

  /* Interactive - Lighter variants for dark bg */
  --interactive-primary: var(--color-primary-400);
  --interactive-primary-hover: var(--color-primary-300);
  --interactive-primary-active: var(--color-primary-200);
  --interactive-primary-alpha: rgba(102, 126, 234, 0.2);

  /* Cards */
  --card-bg: var(--bg-secondary);
  --card-border: var(--border-default);
  --card-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);

  /* Modal backdrop - darker */
  --modal-backdrop: rgba(0, 0, 0, 0.7);
}

/* =========================================================================
   SYSTEM PREFERENCE DETECTION
   Apply dark theme if user's OS prefers dark
   ========================================================================= */

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    /* Apply dark theme variables */
    --bg-primary: var(--color-gray-900);
    --bg-secondary: var(--color-gray-800);
    --bg-tertiary: var(--color-gray-700);
    --text-primary: var(--color-gray-50);
    --text-secondary: var(--color-gray-300);
    /* ... etc (copy from [data-theme="dark"] above) */
  }
}
```

---

### 2.3: Base Styles

**File: `backend/static/css/base.css`**

```css
/**
 * Base Styles - HTML Element Defaults
 * 
 * Styles for raw HTML elements with no classes.
 * Creates consistent foundation across browsers.
 */

/* =========================================================================
   RESET & BOX MODEL
   ========================================================================= */

*,
*::before,
*::after {
  box-sizing: border-box; /* Include padding/border in width calculations */
  margin: 0;
  padding: 0;
}

/* =========================================================================
   ROOT & BODY
   ========================================================================= */

html {
  /* 62.5% of 16px = 10px, makes rem calculations easier */
  /* 1rem = 10px, 1.6rem = 16px */
  /* Actually, let's keep it simple: 1rem = 16px */
  font-size: 100%;

  /* Smooth scrolling for anchor links */
  scroll-behavior: smooth;

  /* Better text rendering */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: var(--font-sans);
  font-size: var(--font-size-base);
  line-height: var(--line-height-base);
  color: var(--text-primary);
  background-color: var(--bg-primary);

  /* Smooth theme transitions */
  transition: background-color var(--transition-base), color var(--transition-base);

  /* Prevent horizontal scroll */
  overflow-x: hidden;
}

/* =========================================================================
   TYPOGRAPHY
   ========================================================================= */

h1,
h2,
h3,
h4,
h5,
h6 {
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  color: var(--text-primary);
  margin-bottom: var(--spacing-4);
}

h1 {
  font-size: var(--font-size-4xl);
  margin-bottom: var(--spacing-6);
}

h2 {
  font-size: var(--font-size-3xl);
  color: var(--interactive-primary);
}

h3 {
  font-size: var(--font-size-2xl);
}

h4 {
  font-size: var(--font-size-xl);
}

h5 {
  font-size: var(--font-size-lg);
}

h6 {
  font-size: var(--font-size-base);
}

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

a:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}

/* Lists */
ul,
ol {
  margin-bottom: var(--spacing-4);
  padding-left: var(--spacing-6);
}

li {
  margin-bottom: var(--spacing-2);
}

/* Code */
code,
pre {
  font-family: var(--font-mono);
  font-size: 0.9em;
}

code {
  background: var(--bg-secondary);
  padding: 0.125rem 0.25rem;
  border-radius: var(--radius-sm);
  color: var(--color-danger-500);
}

pre {
  background: var(--bg-secondary);
  padding: var(--spacing-4);
  border-radius: var(--radius-base);
  overflow-x: auto;
  margin-bottom: var(--spacing-4);
}

pre code {
  background: none;
  padding: 0;
  color: inherit;
}

/* =========================================================================
   FORMS
   ========================================================================= */

input,
textarea,
select,
button {
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
}

/* =========================================================================
   IMAGES & MEDIA
   ========================================================================= */

img,
video,
svg {
  display: block;
  max-width: 100%;
  height: auto;
}

/* =========================================================================
   TABLES
   ========================================================================= */

table {
  border-collapse: collapse;
  width: 100%;
}

th,
td {
  padding: var(--spacing-3);
  text-align: left;
  border-bottom: 1px solid var(--border-default);
}

th {
  font-weight: var(--font-weight-semibold);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* =========================================================================
   UTILITY CLASSES (Minimal set)
   ========================================================================= */

.hidden {
  display: none !important;
}

.sr-only {
  /* Screen reader only - visually hidden but accessible */
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

---

### 2.4: Component Styles

**File: `backend/static/css/components.css`**

```css
/**
 * Component Styles
 * 
 * Reusable UI components with BEM-like naming.
 * Each component is self-contained.
 */

/* =========================================================================
   LAYOUT COMPONENTS
   ========================================================================= */

.container {
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--spacing-4);
  padding-right: var(--spacing-4);
}

/* Header */
header {
  background: linear-gradient(
    135deg,
    var(--color-primary-500),
    var(--color-primary-700)
  );
  color: var(--text-inverse);
  padding: var(--spacing-6);
  box-shadow: var(--shadow-md);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  gap: var(--spacing-4);
  flex-wrap: wrap;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}

/* Main content area */
main {
  padding: var(--spacing-8) 0;
  min-height: calc(100vh - 200px);
}

/* Footer */
footer {
  text-align: center;
  padding: var(--spacing-8) var(--spacing-4);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  border-top: 1px solid var(--border-default);
}

/* =========================================================================
   CARD COMPONENT
   ========================================================================= */

section {
  background: var(--card-bg);
  padding: var(--card-padding);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  margin-bottom: var(--spacing-6);

  transition: background-color var(--transition-base), border-color var(--transition-base),
    box-shadow var(--transition-base);
}

/* =========================================================================
   BUTTON COMPONENT
   ========================================================================= */

.btn {
  /* Layout */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);

  /* Spacing */
  padding: var(--button-padding-y) var(--button-padding-x);

  /* Typography */
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-base);
  text-decoration: none;
  white-space: nowrap;

  /* Visual */
  border: none;
  border-radius: var(--button-border-radius);
  cursor: pointer;

  /* Interaction */
  transition: all var(--button-transition);
  user-select: none;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.btn:active {
  transform: translateY(0);
}

.btn:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

/* Button Variants */
.btn-primary {
  background: var(--button-primary-bg);
  color: var(--button-primary-text);
}

.btn-primary:hover {
  background: var(--button-primary-bg-hover);
}

.btn-secondary {
  background: var(--button-secondary-bg);
  color: var(--button-secondary-text);
}

.btn-secondary:hover {
  background: var(--button-secondary-bg-hover);
}

.btn-danger {
  background: var(--status-danger);
  color: var(--text-inverse);
}

.btn-danger:hover {
  background: var(--color-danger-600);
}

/* Button Sizes */
.btn-sm {
  padding: var(--spacing-1) var(--spacing-3);
  font-size: var(--font-size-sm);
}

.btn-lg {
  padding: var(--spacing-3) var(--spacing-6);
  font-size: var(--font-size-lg);
}

/* =========================================================================
   FORM COMPONENTS
   ========================================================================= */

.form-group {
  margin-bottom: var(--spacing-5);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-2);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: var(--spacing-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-base);
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: var(--font-size-base);
  transition: all var(--transition-fast);
}

.form-group input:hover,
.form-group textarea:hover,
.form-group select:hover {
  border-color: var(--border-hover);
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px var(--interactive-primary-alpha);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

/* =========================================================================
   FILE LIST COMPONENT
   ========================================================================= */

#file-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}

.file-item {
  padding: var(--spacing-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--spacing-4);
  background: var(--bg-secondary);

  transition: all var(--transition-base);
}

.file-item:hover {
  transform: translateX(5px);
  border-color: var(--interactive-primary);
  box-shadow: var(--shadow-sm);
}

.file-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
  flex: 1;
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
  background: var(--status-success-bg);
  color: var(--status-success-text);
}

.status-checked_out {
  background: var(--status-warning-bg);
  color: var(--status-warning-text);
}

.file-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}

/* =========================================================================
   LOADING INDICATOR
   ========================================================================= */

.loading {
  text-align: center;
  padding: var(--spacing-8);
  color: var(--text-secondary);
}

/* =========================================================================
   MODAL COMPONENT
   ========================================================================= */

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

  /* Fade in animation */
  animation: fadeIn var(--transition-base);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: var(--modal-bg);
  border-radius: var(--modal-border-radius);
  box-shadow: var(--modal-shadow);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid var(--border-default);

  /* Slide up animation */
  animation: slideUp var(--transition-base);
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
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
}

.modal-close {
  background: none;
  border: none;
  font-size: var(--font-size-2xl);
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-base);
  transition: all var(--transition-fast);
}

.modal-close:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.modal-body {
  padding: var(--spacing-6);
}

.modal-actions {
  display: flex;
  gap: var(--spacing-3);
  justify-content: flex-end;
  margin-top: var(--spacing-6);
}
```

---

### 2.5: CSS Entry Point

**File: `backend/static/css/main.css`**

```css
/**
 * Main CSS Entry Point
 * 
 * Imports all CSS files in correct order (cascade matters!)
 * Order: Settings → Base → Components
 */

/* 1. Design Tokens - Must load first */
@import "tokens.css";

/* 2. Base Styles - Raw HTML elements */
@import "base.css";

/* 3. Components - Reusable UI pieces */
@import "components.css";
```

---

### 2.6: Theme Manager JavaScript

**File: `backend/static/js/modules/theme-manager.js`**

```javascript
/**
 * Theme Management Module
 *
 * Handles light/dark theme switching with:
 * - System preference detection
 * - localStorage persistence
 * - Smooth transitions
 */

export class ThemeManager {
  constructor() {
    this.STORAGE_KEY = "pdm-theme";
    this.theme = this.getInitialTheme();
    this.init();
  }

  /**
   * Determine initial theme from:
   * 1. localStorage (user preference)
   * 2. System preference
   * 3. Default to light
   */
  getInitialTheme() {
    const stored = localStorage.getItem(this.STORAGE_KEY);
    if (stored) return stored;

    // Check system preference
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      return "dark";
    }

    return "light";
  }

  /**
   * Initialize theme system
   */
  init() {
    // Apply initial theme
    this.applyTheme(this.theme);

    // Listen for system theme changes
    this.listenForSystemChanges();
  }

  /**
   * Apply theme to DOM
   */
  applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    this.theme = theme;

    // Update button icon if it exists
    this.updateThemeButton();
  }

  /**
   * Toggle between light and dark
   */
  toggle() {
    const newTheme = this.theme === "dark" ? "light" : "dark";
    this.applyTheme(newTheme);
    localStorage.setItem(this.STORAGE_KEY, newTheme);
  }

  /**
   * Update theme toggle button icon
   */
  updateThemeButton() {
    const button = document.getElementById("theme-toggle");
    if (!button) return;

    // Change emoji based on current theme
    button.textContent = this.theme === "dark" ? "☀️" : "🌙";
    button.setAttribute(
      "aria-label",
      `Switch to ${this.theme === "dark" ? "light" : "dark"} theme`
    );
  }

  /**
   * Listen for OS theme changes
   * Only applies if user hasn't set explicit preference
   */
  listenForSystemChanges() {
    window
      .matchMedia("(prefers-color-scheme: dark)")
      .addEventListener("change", (e) => {
        // Only auto-switch if user hasn't set preference
        if (!localStorage.getItem(this.STORAGE_KEY)) {
          this.applyTheme(e.matches ? "dark" : "light");
        }
      });
  }
}

// Export singleton instance
export const themeManager = new ThemeManager();
```

---

### 2.7: HTML Structure

**File: `backend/static/index.html`**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="PDM - Parts Data Management System" />

    <title>PDM System</title>

    <!-- CSS -->
    <link rel="stylesheet" href="/static/css/main.css" />

    <!-- Theme script - Must load BEFORE body to prevent flash -->
    <script type="module">
      import { themeManager } from "/static/js/modules/theme-manager.js";
      // Theme is applied immediately on import
    </script>
  </head>
  <body>
    <!-- ===================================================================
       HEADER
       =================================================================== -->
    <header>
      <div class="header-content">
        <div>
          <h1>PDM System</h1>
          <p>Parts Data Management</p>
        </div>

        <div class="header-actions">
          <button
            id="theme-toggle"
            class="btn btn-secondary"
            title="Toggle theme"
            aria-label="Toggle theme"
          >
            🌙
          </button>
        </div>
      </div>
    </header>

    <!-- ===================================================================
       MAIN CONTENT
       =================================================================== -->
    <main>
      <div class="container">
        <!-- File List Section -->
        <section>
          <h2>Available Files</h2>

          <!-- Loading state -->
          <div id="loading-indicator" class="loading">
            <p>Loading files...</p>
          </div>

          <!-- File list container -->
          <div id="file-list"></div>
        </section>
      </div>
    </main>

    <!-- ===================================================================
       FOOTER
       =================================================================== -->
    <footer>
      <p>&copy; 2025 PDM Tutorial Project</p>
    </footer>

    <!-- ===================================================================
       JAVASCRIPT
       =================================================================== -->
    <script type="module" src="/static/js/app.js"></script>
  </body>
</html>
```

---

### 2.8: API Client Module

**File: `backend/static/js/modules/api-client.js`**

```javascript
/**
 * API Client Module
 *
 * Centralized HTTP communication with the backend.
 * Handles authentication, error handling, and retries.
 */

export class APIClient {
  constructor(baseURL = "") {
    this.baseURL = baseURL;
  }

  /**
   * Make HTTP request
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;

    const config = {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);

      // Handle different status codes
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `HTTP ${response.status}: ${response.statusText}`
        );
      }

      // Parse JSON response
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  /**
   * GET request
   */
  async get(endpoint, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "GET",
    });
  }

  /**
   * POST request
   */
  async post(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  // =========================================================================
  // FILE ENDPOINTS
  // =========================================================================

  /**
   * Get all files
   */
  async getFiles() {
    return this.get("/api/files");
  }

  /**
   * Get single file
   */
  async getFile(filename) {
    return this.get(`/api/files/${encodeURIComponent(filename)}`);
  }
}

// Export singleton instance
export const apiClient = new APIClient();
```

---

### 2.9: Main Application JavaScript

**File: `backend/static/js/app.js`**

```javascript
/**
 * Main Application Entry Point
 *
 * Coordinates all frontend functionality.
 */

import { themeManager } from "./modules/theme-manager.js";
import { apiClient } from "./modules/api-client.js";

// ============================================================================
// SECTION 1: Application State
// ============================================================================

let allFiles = [];
let isLoading = true;

// ============================================================================
// SECTION 2: Data Loading
// ============================================================================

/**
 * Load files from API
 */
async function loadFiles() {
  const loadingEl = document.getElementById("loading-indicator");
  const fileListEl = document.getElementById("file-list");

  // Show loading state
  loadingEl.classList.remove("hidden");
  fileListEl.innerHTML = "";

  try {
    // Fetch from API
    const data = await apiClient.getFiles();
    allFiles = data.files;

    // Hide loading
    loadingEl.classList.add("hidden");

    // Render files
    displayFiles(allFiles);
  } catch (error) {
    // Show error state
    loadingEl.classList.add("hidden");
    fileListEl.innerHTML = `
      <div style="text-align: center; padding: 2rem; color: var(--status-danger-text);">
        <p><strong>Error loading files:</strong></p>
        <p>${error.message}</p>
        <button class="btn btn-primary" onclick="location.reload()">
          Retry
        </button>
      </div>
    `;
  }
}

// ============================================================================
// SECTION 3: DOM Rendering
// ============================================================================

/**
 * Display files in the UI
 */
function displayFiles(files) {
  const container = document.getElementById("file-list");

  // Clear container
  container.innerHTML = "";

  // Handle empty state
  if (!files || files.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
        <p>No files found in the repository.</p>
      </div>
    `;
    return;
  }

  // Render each file
  files.forEach((file) => {
    const fileElement = createFileElement(file);
    container.appendChild(fileElement);
  });
}

/**
 * Create DOM element for a single file
 */
function createFileElement(file) {
  // Create container
  const div = document.createElement("div");
  div.className = "file-item";

  // File info section
  const infoDiv = document.createElement("div");
  infoDiv.className = "file-info";

  // File name
  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  // File status badge
  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ").toUpperCase();

  infoDiv.appendChild(nameSpan);
  infoDiv.appendChild(statusSpan);

  // Actions section
  const actionsDiv = document.createElement("div");
  actionsDiv.className = "file-actions";

  // Add appropriate button based on status
  if (file.status === "available") {
    const checkoutBtn = document.createElement("button");
    checkoutBtn.className = "btn btn-primary btn-sm";
    checkoutBtn.textContent = "Checkout";
    checkoutBtn.onclick = () => handleCheckout(file.name);
    actionsDiv.appendChild(checkoutBtn);
  } else {
    const checkinBtn = document.createElement("button");
    checkinBtn.className = "btn btn-secondary btn-sm";
    checkinBtn.textContent = "Checkin";
    checkinBtn.onclick = () => handleCheckin(file.name);
    actionsDiv.appendChild(checkinBtn);

    // Show who has it locked
    if (file.locked_by) {
      const lockedBySpan = document.createElement("span");
      lockedBySpan.style.fontSize = "var(--font-size-sm)";
      lockedBySpan.style.color = "var(--text-secondary)";
      lockedBySpan.textContent = `Locked by: ${file.locked_by}`;
      actionsDiv.appendChild(lockedBySpan);
    }
  }

  // Assemble element
  div.appendChild(infoDiv);
  div.appendChild(actionsDiv);

  return div;
}

// ============================================================================
// SECTION 4: Event Handlers (Placeholders for Stage 3)
// ============================================================================

function handleCheckout(filename) {
  alert(`Checkout functionality coming in Stage 3!\nFile: ${filename}`);
}

function handleCheckin(filename) {
  alert(`Checkin functionality coming in Stage 3!\nFile: ${filename}`);
}

// ============================================================================
// SECTION 5: Initialization
// ============================================================================

document.addEventListener("DOMContentLoaded", () => {
  console.log("PDM App initialized");

  // Wire up theme toggle button
  document.getElementById("theme-toggle").addEventListener("click", () => {
    themeManager.toggle();
  });

  // Load initial data
  loadFiles();
});
```

---

### 2.10: Update FastAPI to Serve Static Files

**Update `backend/app/main.py`:**

```python
## Add these imports at the top
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

## In create_application(), after middleware, before startup events:

## ====================================================================
## SECTION 2.5: Static Files & Frontend
## ====================================================================

## Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

## Serve index.html at root
@app.get("/", response_class=FileResponse)
async def serve_frontend():
    """Serve the main application frontend."""
    return FileResponse("static/index.html")
```

---

### Stage 2 Complete

**Test your application:**

```bash
## Start server
uvicorn app.main:app --reload

## Visit
http://127.0.0.1:8000
```

**You should see:**

- Professional styled page with gradient header
- File list loading from API
- Theme toggle button that switches light/dark mode
- Smooth transitions
- Responsive design

**File structure:**

```
backend/
├── app/
│   ├── main.py (updated)
│   ├── config.py
│   ├── schemas/
│   └── api/
├── static/
│   ├── css/
│   │   ├── tokens.css
│   │   ├── base.css
│   │   ├── components.css
│   │   ├── main.css
│   │   └── learn_css_architecture.css
│   ├── js/
│   │   ├── modules/
│   │   │   ├── theme-manager.js
│   │   │   └── api-client.js
│   │   └── app.js
│   └── index.html
```

**Verification:**

- [ ] Page loads with files from API
- [ ] Theme toggle switches light/dark mode
- [ ] Theme persists on page reload
- [ ] All styles render correctly
- [ ] No console errors
- [ ] Mobile responsive (resize browser)

**What you learned:**

- CSS architecture (ITCSS methodology)
- Design token systems
- CSS custom properties for theming
- ES6 modules in JavaScript
- Fetch API for HTTP requests
- DOM manipulation
- Event handling
- localStorage for persistence

Ready for Stage 3?

## Stage 3: File Operations & Version Control

**Prerequisites**: Completed Stage 2

**Time**: 5-6 hours

**What you'll build**: Real file system integration, atomic locking mechanism, Git-backed version control.

---

### 3.1: Deep Dive - File System Operations

**File: `backend/app/learn_filesystem.py`**

## **Section 3.1: File System Operations – Full Deep Dive**

**Purpose:**
This is a **learning module**. We aren’t building the app here. The goal is to **understand how Python interacts with the filesystem**, why performance, atomicity, and concurrency matter, and how to **write robust and safe code**.

---

### **SECTION 1: OS Module vs Pathlib**

```python
def os_style():
    import os.path
    path = os.path.join("backend", "repo", "file.txt")
    exists = os.path.exists(path)
    abs_path = os.path.abspath(path)
    files = os.listdir(".")
    return path, exists, abs_path, files
```

```python
def pathlib_style():
    from pathlib import Path
    path = Path("backend") / "repo" / "file.txt"
    exists = path.exists()
    abs_path = path.resolve()
    files = list(Path(".").iterdir())
    return path, exists, abs_path, files
```

#### **Explanation**

1. **`os.path.join()` vs `/` in pathlib**

   - `os.path.join()` concatenates strings using the correct separator (`\` for Windows, `/` for Unix).
   - `Path("a") / "b"` is **more readable**, and **operator overloading** makes it intuitive.
   - **CS insight:** pathlib encapsulates path logic as **objects** with methods — better OO design.

2. **Checking existence**

   - `os.path.exists(path)` vs `path.exists()`
   - Always check if a file exists before reading/writing to avoid exceptions.

3. **Absolute paths**

   - `os.path.abspath()` vs `path.resolve()`
   - Absolute paths are crucial when working with relative paths across different directories.

4. **Listing directories**

   - `os.listdir(".")` → returns strings only
   - `Path(".").iterdir()` → returns **Path objects**, enabling further OO operations (like `.is_file()` or `.name`).

---

**Takeaways:**

- `pathlib` is **modern, expressive, cross-platform, and object-oriented**.
- Writing robust code benefits from **abstraction over raw strings**.

---

### **SECTION 2: File System Performance – Metadata vs Content**

```python
def demonstrate_inode_speed():
    test_file = Path("large_test.txt")
    test_file.write_text("x" * 10_000_000)  ## 10 MB

    ## Metadata read
    start = time.perf_counter()
    for _ in range(10000):
        size = test_file.stat().st_size
    metadata_time = time.perf_counter() - start

    ## Content read
    start = time.perf_counter()
    for _ in range(10):
        content = test_file.read_text()
    content_time = time.perf_counter() - start

    print(f"10,000 metadata reads: {metadata_time:.4f}s")
    print(f"10 content reads: {content_time:.4f}s")
    print(f"Metadata is {content_time/metadata_time:.0f}x faster")

    test_file.unlink()
```

#### **Concepts**

1. **Inode (metadata)**

   - Contains: file size, permissions, timestamps, owner/group, link count
   - Reading metadata is **O(1)** — independent of file size

2. **Content read**

   - Reading file contents is **O(n)** — depends on file size

3. **Why this matters**

   - When building systems like a PDM backend:

     - **Use metadata for listing, locking, sorting**
     - Only **read file contents when necessary**

   - Optimizing this saves time and memory in **I/O-heavy applications**.

---

### **SECTION 3: Atomic Operations**

#### **Theory**

- **Atomic operation**: completes fully or doesn’t happen at all.
- Prevents **partial writes and corrupted states**, especially in multi-process environments.

**Atomic operations (most filesystems):**

- `Path.rename()` → moving/renaming files
- `os.link()` → hard links

**Non-atomic operations:**

- `open(file, 'w').write()`
- `shutil.copy()`
- Directory creation/deletion

**Why important:**
If multiple processes write simultaneously, **race conditions** can corrupt data.

---

#### **Race Condition Example**

```python
def demonstrate_race_condition():
    import threading, json
    test_file = Path("race_test.json")
    test_file.write_text('{"counter": 0}')

    def increment_counter(thread_id):
        for _ in range(1000):
            data = json.loads(test_file.read_text())
            data['counter'] += 1
            test_file.write_text(json.dumps(data))

    t1 = threading.Thread(target=increment_counter, args=(1,))
    t2 = threading.Thread(target=increment_counter, args=(2,))

    t1.start(); t2.start()
    t1.join(); t2.join()

    final = json.loads(test_file.read_text())
    print(f"Expected: 2000, Got: {final['counter']}")

    test_file.unlink()
```

**Observation:**

- Expected: 2000
- Actual: less than 2000 → due to **race condition**
- **CS Insight:** Non-atomic read-modify-write sequences are unsafe in **concurrent applications**.

---

### **SECTION 4: File Locking Mechanisms**

#### **OS-Level File Locks**

| OS      | Function           | Type      | Notes                                    |
| ------- | ------------------ | --------- | ---------------------------------------- |
| POSIX   | `fcntl.flock()`    | Advisory  | Cooperative, fast, network FS compatible |
| Windows | `msvcrt.locking()` | Mandatory | OS-enforced, local FS only               |

**Best Practice:**

- Use **file locks + atomic operations** to prevent race conditions.
- Abstract locks in a class (`LockedFile`) for **cross-platform safety**.

---

### **SECTION 5: Key Concepts Recap**

1. **Path handling**: prefer `pathlib` for OO, readable, cross-platform code
2. **Metadata vs content**: metadata is cheap; content is expensive
3. **Atomicity**: ensures **consistent state**
4. **Race conditions**: can silently corrupt data
5. **File locking**: required for safe concurrent file access

---

### **CS + SE Lessons**

1. **Abstraction:**

   - Encapsulate low-level filesystem operations into functions/classes
   - Example: `LockedFile`, `AtomicWriter`

2. **Concurrency:**

   - Understand threading/multiprocessing limits
   - Atomic operations + locks prevent corruption

3. **Performance awareness:**

   - Distinguish **O(1) metadata** vs **O(n) content** reads
   - Scale your solution efficiently

4. **Error handling:**

   - Always check file existence, permissions, etc.
   - Prepare for I/O errors in production

5. **Design for testability:**

   - Separate **filesystem access** from business logic
   - Allows mocking in tests without touching real files

---

Perfect — let’s continue with the rest of the **3.1 filesystem teaching code**, covering **everything fully** and connecting it to **CS concepts, Python, and software engineering lessons**.

---

## **SECTION 6: Putting It All Together – Safe File Operations**

The previous sections demonstrated:

1. Path handling (`os` vs `pathlib`)
2. Metadata vs content performance
3. Atomicity and race conditions
4. File locking

Now let's combine these into **practical, safe patterns**.

---

#### **Atomic Write Pattern**

In Python, writing files atomically is not built-in for arbitrary writes, but we can implement it safely:

```python
from pathlib import Path
import tempfile
import os

def atomic_write(path: Path, data: str):
    """
    Safely write data to a file using a temporary file.
    Steps:
    1. Write to a temp file
    2. Move temp file to target (atomic on most OSes)
    """
    temp_path = path.with_suffix(".tmp")

    ## Step 1: Write to temporary file
    temp_path.write_text(data)

    ## Step 2: Atomic rename
    temp_path.replace(path)  ## replace() is atomic on most OSes
```

**CS Insight:**

- **Atomic operations** prevent race conditions.
- By writing to a **temporary file** first, we ensure partial writes never overwrite the original file.
- `replace()` is guaranteed atomic in POSIX, Windows handles atomic rename differently but generally safe locally.

---

#### **File Locking Wrapper**

For multi-threaded or multi-process safety:

```python
import platform

if platform.system() == "Windows":
    import msvcrt
else:
    import fcntl

class LockedFile:
    """
    Cross-platform file locking abstraction
    """
    def __init__(self, path: Path, mode: str = "r+"):
        self.path = path
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.path, self.mode)
        if platform.system() == "Windows":
            msvcrt.locking(self.file.fileno(), msvcrt.LK_LOCK, os.path.getsize(self.path))
        else:
            fcntl.flock(self.file.fileno(), fcntl.LOCK_EX)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if platform.system() == "Windows":
            self.file.seek(0)
            msvcrt.locking(self.file.fileno(), msvcrt.LK_UNLCK, os.path.getsize(self.path))
        else:
            fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)
        self.file.close()
```

**CS & SE Lessons:**

- Locks are **cooperative on POSIX**, **mandatory on Windows**. Always check which OS you’re targeting.
- Using a **context manager (`__enter__`, `__exit__`)** ensures **locks are released**, even if exceptions occur.
- Encapsulating file locks in a **class** follows the **single responsibility principle (SRP)** — the class only manages safe access.

---

#### **Safe Counter Increment with Locking**

We can now fix the **race condition** demo:

```python
import json

test_file = Path("counter.json")
test_file.write_text('{"counter": 0}')

def increment_counter_safe():
    for _ in range(1000):
        with LockedFile(test_file, "r+") as f:
            data = json.load(f)
            data["counter"] += 1
            f.seek(0)
            f.truncate()
            json.dump(data, f)
```

**Key points:**

1. Lock ensures **no two threads/processes modify the file simultaneously**.
2. Seek + truncate + dump ensures **complete overwrite**, avoiding leftover partial data.
3. Atomicity + locking = **robust, concurrent-safe filesystem access**.

---

#### **Performance Considerations**

- Avoid reading large files if only metadata is needed. Use `.stat()` (O(1)).
- Use **batch operations** for filesystem I/O where possible (e.g., `os.scandir()` for directory listing).
- Avoid global locks in high-performance apps — consider **per-file locks or async-friendly locks**.

---

#### **Python + CS Insights**

| Concept               | Lesson                                                               |
| --------------------- | -------------------------------------------------------------------- |
| Pathlib               | OO abstraction, cross-platform paths                                 |
| Metadata vs Content   | Understand **algorithmic complexity** for file access (O(1) vs O(n)) |
| Atomic write          | Prevent partial writes and data corruption                           |
| File locking          | Avoid race conditions in multi-thread/multi-process scenarios        |
| Context managers      | Ensure deterministic cleanup (locks released, files closed)          |
| Concurrency           | Multi-threaded access needs synchronization                          |
| Cross-platform design | Always consider Windows vs Linux differences in file handling        |

---

#### **Section 3.1 Summary**

- **Pathlib** → readable, cross-platform
- **Metadata reads** → fast (O(1)), content reads → slow (O(n))
- **Atomic operations** → avoid partial writes
- **Race conditions** → common in naive concurrent writes
- **File locking** → safe multi-thread/multi-process access
- **Best practice** → combine **atomic writes + locking** for safety

---

Absolutely — we can go **much deeper**. Right now, the code and explanations cover **practical Python filesystem use**, atomicity, and locking, but there’s a lot more to unpack at the **CS, software engineering, and Python systems level**. Here’s how we could go deeper, step by step:

---

### **1. Operating System and Filesystem Fundamentals**

#### **Inodes and Metadata**

- Every file has an inode (metadata structure) storing:

  - Size
  - Permissions (rwx for owner/group/other)
  - Timestamps: `ctime`, `mtime`, `atime`
  - Link count
  - Owner and group

- **Implications for performance**:

  - `.stat()` → O(1) read of inode
  - Reading file contents → O(n) proportional to file size

- **CS concept**: Understand the **cost of operations**; some operations are cheap, some are expensive.

#### **Directory Structures**

- Filesystems organize data in trees (directories, subdirectories)
- Path traversal involves:

  - Parsing components (`/` separators)
  - Looking up directory entries in inode tables

- **Pathlib vs os.path**:

  - Pathlib abstracts the traversal into OO methods
  - Handles **OS-specific differences** automatically (slashes vs backslashes, symlinks)

---

### **2. Concurrency Deep Dive**

#### **Race Conditions**

- Occur when **multiple threads/processes access the same resource** without proper synchronization
- **Example**: Two threads incrementing a counter in JSON
- **CS insight**: This is a **classic shared-memory concurrency problem**.

  - Solutions: locks, atomic operations, transactional writes

#### **Atomic Operations**

- Atomic = indivisible, cannot be interrupted
- In Python/OS context:

  - `rename()` → atomic on most filesystems
  - Writes via `write()` are **not atomic**

- **Why it matters**: Prevents **data corruption** in concurrent environments

#### **Locks**

- POSIX: advisory locks (must cooperate)
- Windows: mandatory locks (OS-enforced)
- **Python abstraction**: use context managers for deterministic lock handling
- **CS insight**: Locking is **mutual exclusion (mutex)** — a fundamental concurrency concept

---

### **3. Python-Specific Insights**

#### **Context Managers**

- `with open(...) as f:` ensures **deterministic cleanup**
- Extending `__enter__` / `__exit__` for locks enforces safety even during exceptions
- **Software engineering lesson**: follows **RAII (resource acquisition is initialization)** pattern

#### **Temp Files for Atomic Writes**

- Writing to a temporary file, then renaming ensures **atomic replacement**
- Python approach:

  ```python
  with tempfile.NamedTemporaryFile(delete=False) as tmp:
      tmp.write(data)
  os.replace(tmp.name, target_path)
  ```

- **CS insight**: Mimics **transaction commit** in databases

#### **Serialization Cost**

- Using JSON (`json.load`/`json.dump`) introduces overhead
- Large files → consider **binary formats** (`pickle`, `msgpack`) or memory-mapped files
- **CS insight**: Serialization/deserialization is a **CPU-bound task**, not I/O-bound

---

### **4. Performance Measurement**

#### **Metadata vs Content**

```python
## Metadata read
time_start = time.perf_counter()
for _ in range(10000):
    size = test_file.stat().st_size
time_end = time.perf_counter()

## Content read
time_start2 = time.perf_counter()
for _ in range(10):
    content = test_file.read_text()
time_end2 = time.perf_counter()
```

- Profiling shows **metadata reads can be orders of magnitude faster than content reads**
- **CS concept**: Think in **algorithmic complexity (O(1) vs O(n))** when designing file-heavy apps

#### **Concurrency Profiling**

- Threads in Python have **GIL limitation** for CPU-bound tasks
- I/O-bound tasks (disk or network) → threads still effective
- **Lesson**: Choose threading vs multiprocessing wisely

---

### **5. Advanced Topics**

#### **File Locking Patterns**

- Advisory vs mandatory
- Lock granularity:

  - **File-level locks**: simple, coarse-grained
  - **Record-level locks**: complex, used in databases

- **Deadlocks**: multiple locks acquired in wrong order can freeze the program

#### **Error Handling in File Operations**

- Atomic + lock does not protect against:

  - Disk full
  - Permission errors
  - Filesystem corruption

- **Software engineering principle**: Always **catch exceptions**, log, and fail gracefully

#### **Async Filesystem Operations**

- Python `asyncio` has limited filesystem support (`aiofiles`)
- **Use case**: When doing many file reads/writes in **async web servers**, blocking I/O can degrade performance

---

#### **Summary of Deeper Concepts**

| Layer                 | Concept / Lesson                                                            |
| --------------------- | --------------------------------------------------------------------------- |
| OS / Filesystem       | Inodes, atomic rename, advisory vs mandatory locks, race conditions         |
| CS / Concurrency      | Mutex, deadlock, shared-memory concurrency, thread safety                   |
| Python / SE           | Pathlib, context managers, temp files, atomic writes, exception safety      |
| Performance           | Metadata vs content access, serialization overhead, profiling               |
| Architecture / Design | Layer separation (atomic writes + locks), robustness, cross-platform design |

---

```python
"""
Understanding filesystem operations and their performance characteristics.
"""

import os
import time
from pathlib import Path

## ============================================================================
## SECTION 1: OS Module vs Pathlib
## ============================================================================

"""
Two ways to work with filesystem:
1. os module - Lower level, procedural
2. pathlib - Higher level, object-oriented (PREFERRED)

Performance: Nearly identical (pathlib uses os internally)
Readability: pathlib wins
Cross-platform: pathlib handles OS differences automatically
"""

def os_style():
    """Old style - functional approach"""
    import os.path

    ## Join paths
    path = os.path.join("backend", "repo", "file.txt")

    ## Check existence
    exists = os.path.exists(path)

    ## Get absolute path
    abs_path = os.path.abspath(path)

    ## List directory
    files = os.listdir(".")

    return path, exists, abs_path, files

def pathlib_style():
    """Modern style - object-oriented"""
    from pathlib import Path

    ## Join paths
    path = Path("backend") / "repo" / "file.txt"

    ## Check existence
    exists = path.exists()

    ## Get absolute path
    abs_path = path.resolve()

    ## List directory
    files = list(Path(".").iterdir())

    return path, exists, abs_path, files

## ============================================================================
## SECTION 2: File System Performance
## ============================================================================

def demonstrate_inode_speed():
    """
    File metadata (inode) vs file content access.

    Inode contains:
    - File size
    - Permissions
    - Timestamps
    - Owner/group
    - Links count

    Accessing inode is O(1) - extremely fast
    Reading file content is O(n) - depends on file size
    """

    ## Create a large test file
    test_file = Path("large_test.txt")
    test_file.write_text("x" * 10_000_000)  ## 10MB file

    ## Timing metadata access (inode read)
    start = time.perf_counter()
    for _ in range(10000):
        size = test_file.stat().st_size
    metadata_time = time.perf_counter() - start

    print(f"10,000 metadata reads: {metadata_time:.4f}s")

    ## Timing content read
    start = time.perf_counter()
    for _ in range(10):
        content = test_file.read_text()
    content_time = time.perf_counter() - start

    print(f"10 content reads: {content_time:.4f}s")
    print(f"Metadata is {content_time/metadata_time:.0f}x faster")

    ## Cleanup
    test_file.unlink()

## ============================================================================
## SECTION 3: Atomic Operations
## ============================================================================

"""
CRITICAL CONCEPT: Atomicity

An operation is atomic if it appears to happen instantaneously:
- Either completes fully
- Or doesn't happen at all
- Never leaves partial/corrupted state

File operations that ARE atomic (on most filesystems):
- os.rename() / Path.rename() - moving files
- os.link() - creating hard links

File operations that are NOT atomic:
- open(file, 'w').write() - write can fail midway
- shutil.copy() - can fail during copy
- Directory operations

Why this matters:
If two processes modify the same file simultaneously without locking,
you get race conditions and data corruption.
"""

def demonstrate_race_condition():
    """
    Shows how concurrent writes corrupt data without locking.
    """
    import threading
    import json

    test_file = Path("race_test.json")
    test_file.write_text('{"counter": 0}')

    def increment_counter(thread_id):
        """Non-atomic read-modify-write"""
        for _ in range(1000):
            ## Read
            data = json.loads(test_file.read_text())

            ## Modify
            data['counter'] += 1

            ## Write
            test_file.write_text(json.dumps(data))

    ## Run two threads simultaneously
    t1 = threading.Thread(target=increment_counter, args=(1,))
    t2 = threading.Thread(target=increment_counter, args=(2,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    ## Expected: 2000
    ## Actual: Much less due to race condition
    final = json.loads(test_file.read_text())
    print(f"Expected: 2000, Got: {final['counter']}")

    test_file.unlink()

## ============================================================================
## SECTION 4: File Locking Mechanisms
## ============================================================================

"""
Operating systems provide file locking to prevent race conditions:

POSIX (Linux/macOS): fcntl.flock()
- Advisory locks (cooperative)
- Processes must voluntarily check locks
- Fast, works across network filesystems

Windows: msvcrt.locking()
- Mandatory locks
- OS enforces locks
- Works with local files

Our LockedFile class abstracts these differences.
"""

if __name__ == "__main__":
    print("Filesystem concepts explained.")
    print("\nDemonstrating metadata vs content speed:")
    demonstrate_inode_speed()

    print("\nDemonstrating race condition:")
    demonstrate_race_condition()
```

Run it:

```bash
python -m app.learn_filesystem
```

---

### 3.2: Cross-Platform File Locking

**File: `backend/app/utils/file_locking.py`**

### Tutorial: Building a File Lock Manager in Python

We’re going to build a small Python module that manages locks using JSON files. The goal is to safely share resources between processes (or threads) without conflicts.

Along the way, we’ll learn about:

- Python imports and _why location matters_
- Classes and encapsulation
- File I/O and JSON handling
- Exception handling (try/except/finally)
- Gotchas with PyInstaller and dynamic imports
- Why locking is important

---

#### Step 1: Imports

Let’s start simple — just the imports.

```python
import os
import json
import threading
```

##### Explanation:

- `os` → gives us operating system utilities (file paths, existence checks, etc.).
- `json` → lets us read/write structured data to a `.json` file (instead of raw text).
- `threading` → lets us create a lock object (`threading.Lock`) to prevent two threads in the same process from messing with the file at the same time.

⚠️ **PyInstaller Gotcha**:
When building with PyInstaller, imports inside a _function or class_ body can be skipped if PyInstaller doesn’t detect them as needed. That’s why we typically keep core imports at the _top of the file_.

---

#### Step 2: Starting the Class

Now, let’s create a class to wrap our lock logic.

```python
class LockManager:
    def __init__(self, filename="locks.json"):
        self.filename = filename
        self.lock = threading.Lock()
        self._ensure_file_exists()
```

##### Explanation:

- `class LockManager:` → defines a new class. Think of it like a blueprint for “managing locks.”
- `__init__` → this is the constructor, called when we make an object (e.g., `lm = LockManager()`).
- `filename` → default lock file name (`locks.json`). You can override this if needed.
- `self.lock` → a `threading.Lock` object. Even though we’ll use a JSON file for _cross-process_ locks, this local lock ensures thread safety _within_ one Python process.
- `self._ensure_file_exists()` → helper method to create the file if it doesn’t exist.

---

#### Step 3: Ensuring the File Exists

Let’s define `_ensure_file_exists`.

```python
    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({}, f)
```

##### Explanation:

- `if not os.path.exists(...)` → check if the lock file already exists.
- `with open(...) as f:` → safely open the file (will auto-close).
- `json.dump({}, f)` → write an empty JSON object `{}`.

  - This gives us a clean file we can read/write locks to later.

⚠️ **Why JSON instead of plain text?**
Because JSON can hold structured data (e.g., multiple named locks), while text would just be a string.

---

#### Step 4: Reading and Writing the File

Now we need helper functions to read/write the JSON safely.

```python
    def _read_file(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def _write_file(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f)
```

##### Explanation:

- `_read_file` → opens the JSON file in **read mode** and returns the parsed object (likely a dictionary).
- `_write_file` → opens the JSON file in **write mode** and replaces its contents with whatever dictionary we pass in.
- Using `json.load` and `json.dump` ensures consistency (always valid JSON).

⚠️ **Gotcha**: If your app crashes mid-write, you could end up with a corrupted file. Later we can discuss atomic writes (using `tempfile` + `os.replace`).

---

#### Step 5: Acquiring a Lock

Now, let’s write the method to _acquire_ a lock.

```python
    def acquire(self, name):
        with self.lock:
            data = self._read_file()
            if name in data:
                raise RuntimeError(f"Lock '{name}' already held.")
            data[name] = True
            self._write_file(data)
```

##### Explanation:

- `with self.lock:` → ensures that only **one thread in this process** can execute this block at once.
- `data = self._read_file()` → load current lock state from the JSON file.
- `if name in data:` → check if someone already holds the lock.
- `raise RuntimeError(...)` → if so, fail fast.
- `data[name] = True` → mark this lock as “taken.”
- `self._write_file(data)` → save updated state back to disk.

---

#### Step 6: Releasing a Lock

Now the opposite — releasing.

```python
    def release(self, name):
        with self.lock:
            data = self._read_file()
            if name not in data:
                raise RuntimeError(f"Lock '{name}' not found.")
            del data[name]
            self._write_file(data)
```

##### Explanation:

- Again, use `with self.lock` for safety.
- Load the current locks.
- If the lock doesn’t exist, raise an error.
- Otherwise, remove it (`del data[name]`) and save the file.

---

#### Step 7: Putting It All Together

Here’s the full class now:

```python
import os
import json
import threading

class LockManager:
    def __init__(self, filename="locks.json"):
        self.filename = filename
        self.lock = threading.Lock()
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({}, f)

    def _read_file(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def _write_file(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f)

    def acquire(self, name):
        with self.lock:
            data = self._read_file()
            if name in data:
                raise RuntimeError(f"Lock '{name}' already held.")
            data[name] = True
            self._write_file(data)

    def release(self, name):
        with self.lock:
            data = self._read_file()
            if name not in data:
                raise RuntimeError(f"Lock '{name}' not found.")
            del data[name]
            self._write_file(data)
```

---

#### Step 8: Example Usage

```python
if __name__ == "__main__":
    lm = LockManager()

    try:
        lm.acquire("my_resource")
        print("Lock acquired! Doing work...")
        ### simulate work
        import time; time.sleep(2)
    finally:
        lm.release("my_resource")
        print("Lock released.")
```

---

#### Key Takeaways

1. **Imports inside classes/functions**: PyInstaller might miss them → keep imports at top-level.
2. **Locks**: We used `threading.Lock` (for threads) + JSON file (for processes).
3. **Error Handling**: Use exceptions instead of silently failing.
4. **Incremental Build**: Writing piece by piece avoids “copy-paste without thinking.”

---

```python
"""
Cross-platform file locking implementation.

Provides atomic read-modify-write operations on files.
Essential for preventing race conditions in concurrent environments.
"""

import os
from pathlib import Path
from typing import Union

## Platform-specific imports
if os.name == 'nt':  ## Windows
    import msvcrt
else:  ## Unix-like (Linux, macOS)
    import fcntl

## ============================================================================
## SECTION 1: Context Manager Implementation
## ============================================================================

class LockedFile:
    """
    Context manager for exclusive file locking.

    Usage:
        with LockedFile(path, 'r+') as f:
            data = json.load(f)
            data['key'] = 'value'
            f.seek(0)
            f.truncate()
            json.dump(data, f)

    Why this is safe:
    1. Lock is acquired before any I/O
    2. Lock is held for entire read-modify-write
    3. Lock is released even if exception occurs
    4. Other processes wait for lock before accessing
    """

    def __init__(self, filepath: Union[str, Path], mode: str = 'r'):
        """
        Initialize locked file handler.

        Args:
            filepath: Path to file
            mode: File open mode ('r', 'w', 'r+', etc.)
        """
        self.filepath = Path(filepath)
        self.mode = mode
        self.file = None

    def __enter__(self):
        """
        Acquire lock when entering context.

        Returns:
            Open file handle with lock acquired
        """
        ## Open file
        self.file = open(self.filepath, self.mode)

        ## Acquire exclusive lock
        if os.name == 'nt':
            ## Windows: Lock entire file
            ## msvcrt.locking() locks a byte range
            ## We lock from position 0 to EOF
            file_size = os.path.getsize(self.filepath)
            if file_size == 0:
                file_size = 1  ## Lock at least 1 byte

            ## LK_NBLCK: Non-blocking exclusive lock
            ## Will raise IOError if already locked
            try:
                msvcrt.locking(
                    self.file.fileno(),
                    msvcrt.LK_LOCK,  ## Blocking lock
                    file_size
                )
            except IOError as e:
                self.file.close()
                raise IOError(f"Could not acquire lock on {self.filepath}: {e}")
        else:
            ## Unix: flock() is simpler and more reliable
            ## LOCK_EX: Exclusive lock
            ## Blocks until lock is available
            try:
                fcntl.flock(self.file.fileno(), fcntl.LOCK_EX)
            except IOError as e:
                self.file.close()
                raise IOError(f"Could not acquire lock on {self.filepath}: {e}")

        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Release lock when exiting context.

        Called even if exception occurs in the with block.
        """
        if self.file:
            ## Release lock
            if os.name == 'nt':
                try:
                    file_size = os.path.getsize(self.filepath)
                    if file_size == 0:
                        file_size = 1
                    msvcrt.locking(
                        self.file.fileno(),
                        msvcrt.LK_UNLCK,
                        file_size
                    )
                except:
                    pass  ## Best effort unlock
            else:
                try:
                    fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)
                except:
                    pass

            ## Close file
            self.file.close()

        ## Propagate exceptions (return False)
        return False

## ============================================================================
## SECTION 2: Testing the Lock
## ============================================================================

if __name__ == "__main__":
    """
    Test the file locking mechanism.
    """
    import json
    import threading
    import time

    test_file = Path("lock_test.json")
    test_file.write_text('{"counter": 0}')

    def safe_increment(thread_id):
        """Atomic increment using LockedFile"""
        for i in range(100):
            with LockedFile(test_file, 'r+') as f:
                ## Read
                data = json.load(f)

                ## Modify
                data['counter'] += 1

                ## Write (must seek to beginning and truncate)
                f.seek(0)
                f.truncate()
                json.dump(data, f)

            ## Small delay to increase chance of contention
            time.sleep(0.001)

    print("Testing file locking with multiple threads...")

    ## Run three threads simultaneously
    threads = [
        threading.Thread(target=safe_increment, args=(i,))
        for i in range(3)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    ## Verify correctness
    final = json.loads(test_file.read_text())
    expected = 300  ## 3 threads × 100 increments

    print(f"Expected: {expected}")
    print(f"Got: {final['counter']}")
    print(f"Success: {final['counter'] == expected}")

    test_file.unlink()
```

Test it:

```bash
python -m app.utils.file_locking
```

#### Tutorial: File Management, Locking, and Repository Services in Python

This tutorial walks through **building a file management system** with **locking**, **repository operations**, and a **combined service** that merges both. Each section builds incrementally with explanations, common pitfalls, and deeper notes.

---

##### Section I: Lock Management

We want a system to ensure **only one user can modify a file at a time**, preventing conflicts in multi-user or multi-process environments.

###### Step 1: Class setup

```python
from pathlib import Path
from typing import Dict, Optional
import json
import logging

from app.utils.file_locking import LockedFile

logger = logging.getLogger(__name__)

class LockManager:
    """
    Manages file lock state.

    Stores locks in a JSON file with atomic read/write operations.
    """
```

**Explanation:**

- `Path` → modern way to handle filesystem paths.
- `Dict`, `Optional` → type hints, improves readability and static analysis.
- `json` → storing locks in a human-readable JSON file.
- `LockedFile` → context manager to safely lock the JSON file during read/write operations. Prevents race conditions.
- `logger` → structured logging is crucial for debugging concurrent access.

**Gotchas / Notes:**

- **Imports inside class methods** (`from datetime import datetime`) can cause issues with tools like **PyInstaller** because static analysis may not detect them. Consider moving imports to the top.
- Using JSON as storage is simple but **not suitable for very high-concurrency scenarios**; a database may be better.

---

###### Step 2: Constructor

```python
def __init__(self, locks_file: Path):
    self.locks_file = locks_file

    #### Ensure file exists
    if not self.locks_file.exists():
        self.locks_file.write_text('{}')
```

- Ensures a lock file exists before using it.
- Writing `'{}'` guarantees `json.load` won’t fail on an empty file.

**Python Concepts:**

- `write_text` → writes string content to a file; will create the file if it doesn’t exist.
- Using `Path` methods avoids OS-specific path issues.

---

###### Step 3: Loading locks

```python
def load_locks(self) -> Dict[str, dict]:
    if not self.locks_file.exists():
        return {}

    try:
        with LockedFile(self.locks_file, 'r') as f:
            content = f.read()
            if not content.strip():
                return {}
            return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse locks file: {e}")
        return {}
    except Exception as e:
        logger.error(f"Failed to load locks: {e}")
        return {}
```

**Explanation:**

- Acquires a **file lock** using `LockedFile`.
- Reads the JSON content and returns a dictionary mapping filenames → lock info.
- Handles empty files and JSON parsing errors gracefully.

**Gotchas:**

- Always handle `JSONDecodeError` to avoid crashing when the file is corrupted.
- `LockedFile` ensures **atomic read/write**, preventing race conditions if multiple processes access the file.

**Extra Concept:**

- `try/except` blocks are essential in file I/O. Returning an empty dict allows the system to continue instead of failing.

---

###### Step 4: Saving locks

```python
def save_locks(self, locks: dict):
    try:
        with LockedFile(self.locks_file, 'w') as f:
            json.dump(locks, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save locks: {e}")
        raise
```

- Opens the file with a lock, writes updated lock data.
- Raises exception if saving fails — important to prevent **silent lock inconsistencies**.

**Gotcha:** Never write locks without a file lock; concurrent writes can corrupt the file.

---

###### Step 5: Checking lock state

```python
def is_locked(self, filename: str) -> bool:
    locks = self.load_locks()
    return filename in locks

def get_lock_info(self, filename: str) -> Optional[dict]:
    locks = self.load_locks()
    return locks.get(filename)
```

- `is_locked` → returns `True` if the file has a lock.
- `get_lock_info` → returns lock details (user, timestamp, message).

**Python Tip:**

- Using `.get()` avoids KeyError when the file isn’t locked.

---

###### Step 6: Acquiring and releasing locks

```python
def acquire_lock(self, filename: str, user: str, message: str):
    locks = self.load_locks()
    if filename in locks:
        existing = locks[filename]
        raise ValueError(f"File already locked by {existing['user']}")
    from datetime import datetime, timezone
    locks[filename] = {
        'user': user,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'message': message
    }
    self.save_locks(locks)
    logger.info(f"Lock acquired: {filename} by {user}")

def release_lock(self, filename: str, user: str):
    locks = self.load_locks()
    if filename not in locks:
        raise ValueError("File is not locked")
    if locks[filename]['user'] != user:
        raise ValueError(f"Lock owned by {locks[filename]['user']}, not {user}")
    del locks[filename]
    self.save_locks(locks)
    logger.info(f"Lock released: {filename} by {user}")
```

**Explanation:**

- `acquire_lock` → checks if already locked, raises `ValueError` if so. Otherwise, adds lock info.
- `release_lock` → checks ownership before releasing; ensures only the lock owner can release it.

**Gotchas / Notes:**

- Always verify ownership before releasing a lock — prevents users from accidentally unlocking files they don’t own.
- Timestamp uses **UTC** for consistency in multi-timezone environments.
- Frequent `load_locks()` calls ensure latest state but may have **performance overhead** in very large repositories.

---

##### Section II: File Repository

Handles **filesystem operations** for your repository.

###### Step 1: Setup

```python
class FileRepository:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.repo_path.mkdir(parents=True, exist_ok=True)
```

- Ensures repository directory exists.
- `mkdir(parents=True, exist_ok=True)` → creates intermediate folders safely.

---

###### Step 2: Listing files with metadata

```python
def list_files(self, extension: str = '.mcam') -> List[Dict]:
    files = []
    for item in self.repo_path.iterdir():
        if not item.is_file():
            continue
        if not item.name.lower().endswith(extension):
            continue
        stat = item.stat()
        files.append({
            'name': item.name,
            'size_bytes': stat.st_size,
            'modified': stat.st_mtime,
        })
    return files
```

- Uses `iterdir()` → efficient iterator over directory contents.
- `stat()` → lightweight way to get file size and modified timestamp.
- Filters by extension, ignoring directories.

**Gotchas:**

- `item.name.lower()` ensures `.MCAM` is recognized as `.mcam`.
- `stat().st_mtime` is seconds since epoch — may need conversion to human-readable datetime.

---

###### Step 3: Helper methods

```python
def file_exists(self, filename: str) -> bool:
    return (self.repo_path / filename).exists()

def get_file_path(self, filename: str) -> Path:
    return self.repo_path / filename

def read_file(self, filename: str) -> bytes:
    return self.get_file_path(filename).read_bytes()

def write_file(self, filename: str, content: bytes):
    self.get_file_path(filename).write_bytes(content)
```

- `file_exists` → quick existence check.
- `read_bytes` / `write_bytes` → read/write entire file content.

**Python Tip:** Using `Path` instead of `open()` is simpler and cross-platform.

---

##### Section III: Combined File Service

This class **combines repository + locks** to provide high-level operations.

###### Step 1: Constructor

```python
class FileService:
    def __init__(self, repo_path: Path, locks_file: Path):
        self.repository = FileRepository(repo_path)
        self.lock_manager = LockManager(locks_file)
```

- Encapsulates both repository and lock manager.
- Encourages **separation of concerns**: repository handles filesystem, lock manager handles concurrency.

---

###### Step 2: Files with status

```python
def get_files_with_status(self) -> List[Dict]:
    files = self.repository.list_files()
    locks = self.lock_manager.load_locks()
    result = []
    for file_info in files:
        filename = file_info['name']
        lock_info = locks.get(filename)
        result.append({
            'name': filename,
            'size_bytes': file_info['size_bytes'],
            'status': 'checked_out' if lock_info else 'available',
            'locked_by': lock_info['user'] if lock_info else None,
        })
    return result
```

- Combines file metadata with lock state for display or API purposes.

**Gotchas:**

- Frequent `load_locks()` reads ensure up-to-date status but can be slow with many files.
- Optional chaining (`lock_info['user'] if lock_info else None`) avoids KeyError.

---

###### Step 3: Checkout / Checkin

```python
def checkout_file(self, filename: str, user: str, message: str):
    if not self.repository.file_exists(filename):
        raise ValueError(f"File not found: {filename}")
    self.lock_manager.acquire_lock(filename, user, message)

def checkin_file(self, filename: str, user: str):
    self.lock_manager.release_lock(filename, user)
```

- `checkout_file` → verify file exists, acquire lock.
- `checkin_file` → release lock safely.

**Python Concept:** By combining repository + lock manager, you create a **transactional workflow**: file access and locking are guaranteed to stay in sync.

---

###### ✅ Key Takeaways

- **File locking** prevents race conditions in multi-user / multi-process environments.
- **Pathlib** is modern and safer than raw strings for file operations.
- **Atomic JSON operations** are crucial when multiple processes read/write the same file.
- **Separation of concerns**: repository handles files, lock manager handles concurrency, combined service orchestrates both.

---

### Incremental Coding Tutorial: File Management with Locking

---

#### SECTION I: Lock Management

##### Step 1: Imports and Logger

```python
from pathlib import Path
from typing import Dict, Optional
import json
import logging

from app.utils.file_locking import LockedFile

logger = logging.getLogger(__name__)
```

**Explanation:**

- `Path` → Modern path handling; cross-platform.
- `Dict` / `Optional` → Type hints improve readability and help static checkers.
- `json` → store lock state in a human-readable file.
- `logging` → structured logging, essential for debugging.
- `LockedFile` → context manager to safely lock JSON files during read/write. Prevents race conditions.

**Gotchas / Notes:**

- Make sure `LockedFile` is imported at the top. Imports inside functions or classes may break **PyInstaller** because it relies on static analysis.

---

##### Step 2: Start the LockManager Class

```python
class LockManager:
    """
    Manages file lock state.

    Stores locks in a JSON file with atomic read/write operations.
    """
```

- Encapsulates **all lock logic** in one class.
- Using a class makes it easy to reuse in multiple places, e.g., different services or scripts.

---

##### Step 3: Constructor

```python
def __init__(self, locks_file: Path):
    self.locks_file = locks_file

    ### Ensure file exists
    if not self.locks_file.exists():
        self.locks_file.write_text('{}')
```

**Explanation:**

- Stores path to the lock file.
- Creates an empty JSON `{}` if the file doesn’t exist. This avoids errors on `json.load`.

**Python Concepts:**

- `write_text()` → convenient for writing string content to a file.
- Using `Path` ensures paths are OS-independent.

**Gotcha:** Don’t forget to check file permissions. If Python can’t write the file, the code will fail silently here.

---

##### Step 4: Load Locks

```python
def load_locks(self) -> Dict[str, dict]:
    if not self.locks_file.exists():
        return {}

    try:
        with LockedFile(self.locks_file, 'r') as f:
            content = f.read()
            if not content.strip():
                return {}
            return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse locks file: {e}")
        return {}
    except Exception as e:
        logger.error(f"Failed to load locks: {e}")
        return {}
```

**Explanation:**

- `LockedFile` ensures **atomic access** to prevent concurrent read/write issues.
- `content.strip()` → handles empty files.
- `json.loads()` → converts string JSON into a Python dictionary.

**Gotchas:**

- Always handle `JSONDecodeError` — corrupted files are common when multiple processes write at the same time.

**Extra Concept:**

- Using `return {}` for errors allows the application to **continue running**, instead of crashing.

---

##### Step 5: Save Locks

```python
def save_locks(self, locks: dict):
    try:
        with LockedFile(self.locks_file, 'w') as f:
            json.dump(locks, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save locks: {e}")
        raise
```

- Writes the updated lock dictionary back to file safely.
- `indent=2` → makes JSON human-readable.

**Gotchas:** Never write locks without a **file lock**, or simultaneous writes will corrupt the file.

---

##### Step 6: Check Lock State

```python
def is_locked(self, filename: str) -> bool:
    locks = self.load_locks()
    return filename in locks

def get_lock_info(self, filename: str) -> Optional[dict]:
    locks = self.load_locks()
    return locks.get(filename)
```

- `is_locked` → returns True if the file has a lock.
- `get_lock_info` → returns lock metadata (user, timestamp, message) or `None`.

**Python Tip:** `.get()` avoids `KeyError` for missing keys.

---

##### Step 7: Acquire and Release Locks

```python
def acquire_lock(self, filename: str, user: str, message: str):
    locks = self.load_locks()
    if filename in locks:
        existing = locks[filename]
        raise ValueError(f"File already locked by {existing['user']}")

    from datetime import datetime, timezone
    locks[filename] = {
        'user': user,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'message': message
    }
    self.save_locks(locks)
    logger.info(f"Lock acquired: {filename} by {user}")

def release_lock(self, filename: str, user: str):
    locks = self.load_locks()
    if filename not in locks:
        raise ValueError("File is not locked")
    if locks[filename]['user'] != user:
        raise ValueError(f"Lock owned by {locks[filename]['user']}, not {user}")
    del locks[filename]
    self.save_locks(locks)
    logger.info(f"Lock released: {filename} by {user}")
```

- `acquire_lock` → checks existing locks, stores user, timestamp, message.
- `release_lock` → ensures **only the owner** can release a lock.
- `datetime.now(timezone.utc)` → use UTC for consistency across time zones.

**Gotchas:**

- Always verify ownership before releasing a lock.
- Frequent `load_locks()` reads ensure latest state but may impact performance for large repositories.

---

#### SECTION II: File Repository

##### Step 1: Repository Class

```python
class FileRepository:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.repo_path.mkdir(parents=True, exist_ok=True)
```

- Ensures the repository folder exists.
- `mkdir(parents=True, exist_ok=True)` creates intermediate directories safely.

---

##### Step 2: List Files

```python
def list_files(self, extension: str = '.mcam') -> list[dict]:
    files = []
    for item in self.repo_path.iterdir():
        if not item.is_file():
            continue
        if not item.name.lower().endswith(extension):
            continue
        stat = item.stat()
        files.append({
            'name': item.name,
            'size_bytes': stat.st_size,
            'modified': stat.st_mtime,
        })
    return files
```

- Iterates through the directory.
- Filters **files only**, matches extension, gets metadata.
- `stat()` → fast access to file info.

---

##### Step 3: Helper Methods

```python
def file_exists(self, filename: str) -> bool:
    return (self.repo_path / filename).exists()

def get_file_path(self, filename: str) -> Path:
    return self.repo_path / filename

def read_file(self, filename: str) -> bytes:
    return self.get_file_path(filename).read_bytes()

def write_file(self, filename: str, content: bytes):
    self.get_file_path(filename).write_bytes(content)
```

- Encapsulates file operations.
- Using `Path` methods makes it **cross-platform**.

---

#### SECTION III: Combined File Service

##### Step 1: Service Constructor

```python
class FileService:
    def __init__(self, repo_path: Path, locks_file: Path):
        self.repository = FileRepository(repo_path)
        self.lock_manager = LockManager(locks_file)
```

- Orchestrates **repository + lock manager**.
- Keeps code modular.

---

##### Step 2: Files with Status

```python
def get_files_with_status(self) -> list[dict]:
    files = self.repository.list_files()
    locks = self.lock_manager.load_locks()
    result = []
    for file_info in files:
        filename = file_info['name']
        lock_info = locks.get(filename)
        result.append({
            'name': filename,
            'size_bytes': file_info['size_bytes'],
            'status': 'checked_out' if lock_info else 'available',
            'locked_by': lock_info['user'] if lock_info else None,
        })
    return result
```

- Combines **file metadata + lock state**.
- Ideal for APIs or UI display.

---

##### Step 3: Checkout / Checkin

```python
def checkout_file(self, filename: str, user: str, message: str):
    if not self.repository.file_exists(filename):
        raise ValueError(f"File not found: {filename}")
    self.lock_manager.acquire_lock(filename, user, message)

def checkin_file(self, filename: str, user: str):
    self.lock_manager.release_lock(filename, user)
```

- Simple, high-level methods to **manage file access safely**.
- Throws `ValueError` if file doesn’t exist or lock is invalid.

---

✅ **Next Steps / Practice**

- Add **unit tests** for LockManager to simulate multiple users trying to acquire/release locks.
- Try **checking files in/out** from multiple scripts to see the locks in action.
- Consider **FileLock library** as a cross-platform alternative if you run into weird locking behavior on Windows

### 3.3: File Service Layer

**File: `backend/app/services/file_service.py`**

```python
"""
File management business logic.

Handles:
- Reading files from filesystem
- Lock state management
- File metadata extraction
"""

from pathlib import Path
from typing import List, Dict, Optional
import json
import logging

from app.utils.file_locking import LockedFile

logger = logging.getLogger(__name__)

## ============================================================================
## SECTION 1: Lock Management
## ============================================================================

class LockManager:
    """
    Manages file lock state.

    Stores locks in JSON file with atomic read/write operations.
    """

    def __init__(self, locks_file: Path):
        self.locks_file = locks_file

        ## Ensure file exists
        if not self.locks_file.exists():
            self.locks_file.write_text('{}')

    def load_locks(self) -> Dict[str, dict]:
        """
        Load current lock state.

        Returns:
            Dict mapping filename to lock info
        """
        if not self.locks_file.exists():
            return {}

        try:
            with LockedFile(self.locks_file, 'r') as f:
                content = f.read()
                if not content.strip():
                    return {}
                return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse locks file: {e}")
            return {}
        except Exception as e:
            logger.error(f"Failed to load locks: {e}")
            return {}

    def save_locks(self, locks: dict):
        """
        Save lock state atomically.

        Args:
            locks: Dict mapping filename to lock info
        """
        try:
            with LockedFile(self.locks_file, 'w') as f:
                json.dump(locks, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save locks: {e}")
            raise

    def is_locked(self, filename: str) -> bool:
        """Check if file is locked."""
        locks = self.load_locks()
        return filename in locks

    def get_lock_info(self, filename: str) -> Optional[dict]:
        """Get lock information for a file."""
        locks = self.load_locks()
        return locks.get(filename)

    def acquire_lock(self, filename: str, user: str, message: str):
        """
        Acquire lock on a file.

        Raises:
            ValueError: If file is already locked
        """
        locks = self.load_locks()

        if filename in locks:
            existing = locks[filename]
            raise ValueError(
                f"File already locked by {existing['user']}"
            )

        ## Add lock
        from datetime import datetime, timezone
        locks[filename] = {
            'user': user,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'message': message
        }

        self.save_locks(locks)
        logger.info(f"Lock acquired: {filename} by {user}")

    def release_lock(self, filename: str, user: str):
        """
        Release lock on a file.

        Args:
            filename: File to unlock
            user: User releasing lock (must own lock)

        Raises:
            ValueError: If file not locked or wrong user
        """
        locks = self.load_locks()

        if filename not in locks:
            raise ValueError("File is not locked")

        if locks[filename]['user'] != user:
            raise ValueError(
                f"Lock owned by {locks[filename]['user']}, not {user}"
            )

        ## Remove lock
        del locks[filename]
        self.save_locks(locks)
        logger.info(f"Lock released: {filename} by {user}")

## ============================================================================
## SECTION 2: File Repository
## ============================================================================

class FileRepository:
    """
    Manages file operations on the repository directory.
    """

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path

        ## Ensure repo directory exists
        self.repo_path.mkdir(parents=True, exist_ok=True)

    def list_files(self, extension: str = '.mcam') -> List[Dict]:
        """
        List all files in repository with metadata.

        Args:
            extension: File extension filter

        Returns:
            List of file info dicts
        """
        files = []

        try:
            for item in self.repo_path.iterdir():
                ## Filter by type and extension
                if not item.is_file():
                    continue
                if not item.name.lower().endswith(extension):
                    continue

                ## Get file metadata (from inode - fast!)
                stat = item.stat()

                files.append({
                    'name': item.name,
                    'size_bytes': stat.st_size,
                    'modified': stat.st_mtime,
                })

        except Exception as e:
            logger.error(f"Error listing files: {e}")
            raise

        return files

    def file_exists(self, filename: str) -> bool:
        """Check if file exists in repository."""
        return (self.repo_path / filename).exists()

    def get_file_path(self, filename: str) -> Path:
        """Get full path to a file."""
        return self.repo_path / filename

    def read_file(self, filename: str) -> bytes:
        """Read file contents."""
        path = self.get_file_path(filename)
        return path.read_bytes()

    def write_file(self, filename: str, content: bytes):
        """Write file contents."""
        path = self.get_file_path(filename)
        path.write_bytes(content)

## ============================================================================
## SECTION 3: Combined Service
## ============================================================================

class FileService:
    """
    High-level file management service.

    Combines file operations with lock management.
    """

    def __init__(self, repo_path: Path, locks_file: Path):
        self.repository = FileRepository(repo_path)
        self.lock_manager = LockManager(locks_file)

    def get_files_with_status(self) -> List[Dict]:
        """
        Get all files with their lock status.

        Returns:
            List of dicts with file info and lock status
        """
        ## Get files from filesystem
        files = self.repository.list_files()

        ## Get lock state
        locks = self.lock_manager.load_locks()

        ## Combine information
        result = []
        for file_info in files:
            filename = file_info['name']
            lock_info = locks.get(filename)

            result.append({
                'name': filename,
                'size_bytes': file_info['size_bytes'],
                'status': 'checked_out' if lock_info else 'available',
                'locked_by': lock_info['user'] if lock_info else None,
            })

        return result

    def checkout_file(self, filename: str, user: str, message: str):
        """
        Check out a file for editing.

        Raises:
            ValueError: If file doesn't exist or is already locked
        """
        ## Verify file exists
        if not self.repository.file_exists(filename):
            raise ValueError(f"File not found: {filename}")

        ## Acquire lock
        self.lock_manager.acquire_lock(filename, user, message)

    def checkin_file(self, filename: str, user: str):
        """
        Check in a file after editing.

        Raises:
            ValueError: If not locked or wrong user
        """
        self.lock_manager.release_lock(filename, user)
```

---

### 3.4: Update API Endpoints

**Update `backend/app/api/files.py`:**

## Tutorial: File Management API Endpoints (FastAPI)

---

### SECTION 1: Router Setup

```python
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.files import (
    FileInfo,
    FileListResponse,
    FileCheckoutRequest,
    FileCheckinRequest
)
from app.services.file_service import FileService
from pathlib import Path
```

**Explanation:**

- `APIRouter` → lets you group endpoints into a clean, modular API.
- `HTTPException` → raise errors that FastAPI translates into proper HTTP responses.
- `status` → constants like `404_NOT_FOUND`, keeps your code readable.
- `Depends` → dependency injection system, lets FastAPI create services for each request.
- `schemas.files` → **Pydantic models** that define request/response shapes.
- `FileService` → our business logic layer from the previous section.
- `Path` → used for filesystem paths (we’ll configure repository paths later).

---

```python
router = APIRouter(
    prefix="/api/files",
    tags=["files"],
)
```

- `prefix="/api/files"` → all routes in this router will start with `/api/files`.
- `tags=["files"]` → shows up in Swagger/OpenAPI docs for grouping.

👉 This keeps your API organized, especially when you have multiple routers (e.g., `/api/users`, `/api/admin`).

---

### SECTION 2: Dependency Injection

```python
def get_file_service() -> FileService:
    """
    Dependency that provides FileService instance.

    In production, this would be a singleton.
    For now, we create it per-request (still fast).
    """
    from app.config import settings

    repo_path = settings.BASE_DIR / 'repo'
    locks_file = settings.BASE_DIR / 'locks.json'

    return FileService(repo_path, locks_file)
```

**Explanation:**

- FastAPI can **inject this function** into endpoints using `Depends()`.
- Reads `repo_path` and `locks_file` from config (you’d centralize paths in `settings`).
- Creates a **new `FileService` instance per request**.

**Gotcha:**
If you want **better performance**, you could make this a **singleton** instead of per-request, but per-request is easier and safe for now.

---

### SECTION 3: GET Endpoints

#### List Files

```python
@router.get("/", response_model=FileListResponse)
def get_files(
    file_service: FileService = Depends(get_file_service)
):
    """
    Get list of all files with their lock status.
    """
    try:
        files = file_service.get_files_with_status()

        return FileListResponse(
            files=files,
            total=len(files)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list files: {str(e)}"
        )
```

**Explanation:**

- `@router.get("/")` → endpoint at `GET /api/files/`.
- `response_model=FileListResponse` → FastAPI validates & documents the response.
- Injects `file_service` automatically.
- Returns files + total count.

**Error Handling:**

- Wraps everything in try/except.
- Returns **500 Internal Server Error** for unexpected problems.

---

#### Get File by Name

```python
@router.get("/{filename}", response_model=FileInfo)
def get_file(
    filename: str,
    file_service: FileService = Depends(get_file_service)
):
    """
    Get details for a specific file.
    """
    files = file_service.get_files_with_status()

    for file in files:
        if file['name'] == filename:
            return FileInfo(**file)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"File '{filename}' not found"
    )
```

**Explanation:**

- `@router.get("/{filename}")` → path parameter like `/api/files/test.mcam`.
- Loops through results of `get_files_with_status`.
- Returns **FileInfo** schema if found.
- Raises **404 Not Found** if missing.

👉 Notice how we don’t call `repository` directly — we stick to `FileService`, keeping layers clean.

---

### SECTION 4: POST Endpoints

#### Checkout File (Lock)

```python
@router.post("/checkout")
def checkout_file(
    request: FileCheckoutRequest,
    file_service: FileService = Depends(get_file_service)
):
    """
    Check out a file for editing.

    Acquires an exclusive lock on the file.
    """
    try:
        file_service.checkout_file(
            filename=request.filename,
            user=request.user,
            message=request.message
        )

        return {
            "success": True,
            "message": f"File '{request.filename}' checked out successfully"
        }

    except ValueError as e:
        ## Business logic error (file not found, already locked)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    except Exception as e:
        ## Unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to checkout file: {str(e)}"
        )
```

**Explanation:**

- `@router.post("/checkout")` → endpoint at `POST /api/files/checkout`.
- Takes a **request body** (`FileCheckoutRequest`) with filename, user, message.
- Calls `checkout_file` in service, which **writes a lock** to JSON.

**Error Mapping:**

- `ValueError` → business error → HTTP `409 Conflict`.
- Any other exception → `500 Internal Server Error`.

---

#### Checkin File (Unlock)

```python
@router.post("/checkin")
def checkin_file(
    request: FileCheckinRequest,
    file_service: FileService = Depends(get_file_service)
):
    """
    Check in a file after editing.

    Releases the lock on the file.
    """
    try:
        file_service.checkin_file(
            filename=request.filename,
            user=request.user
        )

        return {
            "success": True,
            "message": f"File '{request.filename}' checked in successfully"
        }

    except ValueError as e:
        ## Business logic error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to checkin file: {str(e)}"
        )
```

**Explanation:**

- `@router.post("/checkin")` → endpoint at `POST /api/files/checkin`.
- Takes `FileCheckinRequest` (filename + user).
- Calls service → releases lock if owned by user.

**Error Mapping:**

- `ValueError` → business error → `400 Bad Request`.
- Any other → `500 Internal Server Error`.

---

### Key Takeaways

1. **Separation of concerns**

   - File logic (`FileService`) is independent of API layer.
   - API just translates service calls into HTTP responses.

2. **Dependency injection with `Depends()`**

   - Makes it easy to swap implementations (e.g., mock service for tests).

3. **Pydantic models**

   - Keep request/response schemas consistent.
   - Auto-generate Swagger docs at `/docs`.

4. **Error Handling Strategy**

   - Business logic errors → `400` or `409`.
   - Unexpected errors → `500`.
   - Always map exceptions to proper HTTP codes.

```python
"""
File management API endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.files import (
    FileInfo,
    FileListResponse,
    FileCheckoutRequest,
    FileCheckinRequest
)
from app.services.file_service import FileService
from pathlib import Path

## ============================================================================
## SECTION 1: Router Setup
## ============================================================================

router = APIRouter(
    prefix="/api/files",
    tags=["files"],
)

## ============================================================================
## SECTION 2: Dependency Injection
## ============================================================================

def get_file_service() -> FileService:
    """
    Dependency that provides FileService instance.

    In production, this would be a singleton.
    For now, we create it per-request (still fast).
    """
    from app.config import settings

    repo_path = settings.BASE_DIR / 'repo'
    locks_file = settings.BASE_DIR / 'locks.json'

    return FileService(repo_path, locks_file)

## ============================================================================
## SECTION 3: GET Endpoints
## ============================================================================

@router.get("/", response_model=FileListResponse)
def get_files(
    file_service: FileService = Depends(get_file_service)
):
    """
    Get list of all files with their lock status.

    Now reads from real filesystem instead of mock data.
    """
    try:
        files = file_service.get_files_with_status()

        return FileListResponse(
            files=files,
            total=len(files)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list files: {str(e)}"
        )

@router.get("/{filename}", response_model=FileInfo)
def get_file(
    filename: str,
    file_service: FileService = Depends(get_file_service)
):
    """
    Get details for a specific file.
    """
    files = file_service.get_files_with_status()

    for file in files:
        if file['name'] == filename:
            return FileInfo(**file)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"File '{filename}' not found"
    )

## ============================================================================
## SECTION 4: POST Endpoints - Checkout/Checkin
## ============================================================================

@router.post("/checkout")
def checkout_file(
    request: FileCheckoutRequest,
    file_service: FileService = Depends(get_file_service)
):
    """
    Check out a file for editing.

    Acquires an exclusive lock on the file.
    """
    try:
        file_service.checkout_file(
            filename=request.filename,
            user=request.user,
            message=request.message
        )

        return {
            "success": True,
            "message": f"File '{request.filename}' checked out successfully"
        }

    except ValueError as e:
        ## Business logic error (file not found, already locked)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    except Exception as e:
        ## Unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to checkout file: {str(e)}"
        )

@router.post("/checkin")
def checkin_file(
    request: FileCheckinRequest,
    file_service: FileService = Depends(get_file_service)
):
    """
    Check in a file after editing.

    Releases the lock on the file.
    """
    try:
        file_service.checkin_file(
            filename=request.filename,
            user=request.user
        )

        return {
            "success": True,
            "message": f"File '{request.filename}' checked in successfully"
        }

    except ValueError as e:
        ## Business logic error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to checkin file: {str(e)}"
        )
```

---

### 3.5: Create Test Repository

**Create sample files:**

```bash
cd backend
mkdir -p repo

## Create sample .mcam files (simulating CAM files)
echo "G0 X0 Y0 Z10" > repo/PN1001_OP1.mcam
echo "G1 X10 Y10 F100" > repo/PN1002_OP1.mcam
echo "G2 X20 Y20 I5 J5" > repo/PN1003_OP1.mcam
```

---

### 3.6: Modal Manager for Frontend

**File: `backend/static/js/modules/modal-manager.js`**

## Step 1 – Declaring the Class

```js
/**
 * Modal Manager
 *
 * Handles modal dialogs with:
 * - Backdrop clicks
 * - Escape key
 * - Focus trapping
 */

export class ModalManager {
  constructor(modalId) {
    this.modal = document.getElementById(modalId);

    if (!this.modal) {
      console.error(`Modal not found: ${modalId}`);
      return;
    }

    this.setupEventListeners();
  }
}
```

### Explanation

- `export class ModalManager { ... }`

  - Declares a **class** in JavaScript. Using `export` lets us import it later from another file (`import { ModalManager } from './ModalManager.js'`).
  - Classes are used here to group modal logic into one reusable “blueprint.”

- `constructor(modalId)`

  - Runs **when the class is instantiated**:

    ```js
    const manager = new ModalManager("loginModal");
    ```

    - The `modalId` is a string matching the `<div id="loginModal">` in your HTML.

- `this.modal = document.getElementById(modalId);`

  - Grabs the modal DOM element by its ID. This `this.modal` reference is stored for use in all methods.

- The `if (!this.modal)` check

  - Prevents crashes if you pass a wrong or missing ID. Instead of throwing an error, it logs a helpful message.

- `this.setupEventListeners();`

  - Immediately attaches event listeners (defined later).
  - Important: We only run this if `this.modal` exists. Otherwise, it would error out.

⚠️ **Gotcha:**
If you use PyInstaller or a bundler like Webpack, sometimes imports inside classes/functions aren’t detected for tree-shaking. But here, `document.getElementById` is safe because it’s runtime, not an import. The “hidden import” issue happens with Python packaging, not here — but it’s good you’re noticing these differences.

---

## Step 2 – Adding Event Listeners

```js
  setupEventListeners() {
    // Close on backdrop click
    this.modal.addEventListener("click", (e) => {
      if (e.target === this.modal) {
        this.close();
      }
    });

    // Close on X button
    const closeBtn = this.modal.querySelector(".modal-close");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => this.close());
    }

    // Close on Escape key
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !this.modal.classList.contains("hidden")) {
        this.close();
      }
    });
  }
```

### Explanation

- **Backdrop click**

  - `this.modal.addEventListener("click", (e) => {...})`
  - If you click _outside_ the modal content but still inside the `<div>` backdrop, `e.target` equals `this.modal`. That triggers `this.close()`.
  - Otherwise, if you click inside (like on a form), it won’t close.

- **Close button**

  - `this.modal.querySelector(".modal-close")` searches _inside_ the modal for a button with `.modal-close`.
  - If found, we attach another click listener that calls `this.close()`.
  - Defensive coding: we check `if (closeBtn)` in case the button isn’t present in this modal.

- **Escape key**

  - `document.addEventListener("keydown", ...)` listens globally.
  - We check `e.key === "Escape"` and also `!this.modal.classList.contains("hidden")`.
  - That second condition ensures we only close **if the modal is actually open**.

⚠️ **Gotcha:**

- Listening on `document` can affect all modals. If you ever support multiple modals, you may need to track “active” modals and only close the top one.

---

## Step 3 – Opening the Modal

```js
  open() {
    this.modal.classList.remove("hidden");

    // Focus first input
    const firstInput = this.modal.querySelector("input, textarea");
    if (firstInput) {
      setTimeout(() => firstInput.focus(), 100);
    }

    // Prevent body scroll
    document.body.style.overflow = "hidden";
  }
```

### Explanation

- **Show modal**

  - Removes `"hidden"` class. Assumes your CSS has something like:

    ```css
    .hidden {
      display: none;
    }
    ```

  - By removing it, the modal becomes visible.

- **Focus first input**

  - Good accessibility practice: put keyboard focus on the first `input` or `textarea`.
  - Uses `setTimeout(..., 100)` because if you call `.focus()` immediately, the browser might not have rendered the modal yet. A short delay ensures it works consistently.

- **Prevent background scroll**

  - Sets `document.body.style.overflow = "hidden"`.
  - Locks the page behind the modal, so users don’t scroll content they can’t interact with.

---

## Step 4 – Closing the Modal

```js
  close() {
    this.modal.classList.add("hidden");

    // Restore body scroll
    document.body.style.overflow = "";

    // Clear forms
    const forms = this.modal.querySelectorAll("form");
    forms.forEach((form) => form.reset());
  }
}
```

### Explanation

- **Hide modal**

  - Adds the `"hidden"` class back. The CSS handles hiding it.

- **Restore scroll**

  - Resetting `document.body.style.overflow` re-enables scrolling.

- **Reset forms**

  - Finds all `<form>` elements inside the modal and calls `.reset()` on each.
  - This clears input fields so the next time you open the modal, it starts fresh.
  - Example: if it’s a login modal, the username/password fields will be cleared automatically.

⚠️ **Gotcha:**

- `.reset()` resets to the _default values in the HTML_, not always empty. If you have `value="default@example.com"` in HTML, it’ll reset to that, not blank.

---

## Wrap-up

Now you have a **step-by-step build**:

1. Write the class skeleton + constructor.
2. Add event listeners one at a time.
3. Add open logic.
4. Add close logic.

```javascript
/**
 * Modal Manager
 *
 * Handles modal dialogs with:
 * - Backdrop clicks
 * - Escape key
 * - Focus trapping
 */

export class ModalManager {
  constructor(modalId) {
    this.modal = document.getElementById(modalId);

    if (!this.modal) {
      console.error(`Modal not found: ${modalId}`);
      return;
    }

    this.setupEventListeners();
  }

  setupEventListeners() {
    // Close on backdrop click
    this.modal.addEventListener("click", (e) => {
      if (e.target === this.modal) {
        this.close();
      }
    });

    // Close on X button
    const closeBtn = this.modal.querySelector(".modal-close");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => this.close());
    }

    // Close on Escape key
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

    // Prevent body scroll
    document.body.style.overflow = "hidden";
  }

  close() {
    this.modal.classList.add("hidden");

    // Restore body scroll
    document.body.style.overflow = "";

    // Clear forms
    const forms = this.modal.querySelectorAll("form");
    forms.forEach((form) => form.reset());
  }
}
```

---

### 3.7: Add Modals to HTML

**Update `backend/static/index.html` - add before closing `</body>`:**

## Step 1 – Modal Wrapper (the overlay)

```html
<!-- Checkout Modal -->
<div id="checkout-modal" class="modal-overlay hidden"></div>
```

#### Explanation

- `id="checkout-modal"`

  - Unique identifier so our JavaScript (`ModalManager`) knows which modal to open.

- `class="modal-overlay hidden"`

  - `modal-overlay`: this is the _backdrop_ — usually a semi-transparent dark background that sits behind the modal content.
  - `hidden`: CSS class to keep it invisible until `ModalManager.open()` removes it.

This `div` is the **container for the entire modal**. Everything else goes inside it.

---

## Step 2 – Modal Content Box

```html
<div id="checkout-modal" class="modal-overlay hidden">
  <div class="modal-content"></div>
</div>
```

#### Explanation

- `modal-content`

  - This is the actual dialog box that sits on top of the overlay.
  - Typically styled with a white background, padding, and rounded corners.
  - Everything inside is what the user sees and interacts with.

So we now have:

- Overlay = “dark backdrop”
- Content = “white card on top”

---

## Step 3 – Modal Header

```html
<div class="modal-content">
  <div class="modal-header">
    <h3>Check Out File</h3>
    <button class="modal-close" type="button">&times;</button>
  </div>
</div>
```

#### Explanation

- `modal-header`

  - Groups the **title** and the **close button**.

- `<h3>`

  - Displays the modal title (“Check Out File”).

- `<button class="modal-close">`

  - The `&times;` (`×`) is a typographic “close” symbol.
  - Class name `.modal-close` is important — our `ModalManager` looks for this and wires up the click-to-close behavior.
  - `type="button"` prevents this button from accidentally submitting a form if it’s inside one.

---

## Step 4 – Modal Body with Text

```html
<div class="modal-body">
  <p>You are checking out: <strong id="checkout-filename"></strong></p>
</div>
```

#### Explanation

- `modal-body`

  - Holds the actual content.

- The `<p>` text explains what action is being performed.
- `<strong id="checkout-filename"></strong>`

  - Placeholder where JavaScript can dynamically insert the filename.
  - Example: `document.getElementById("checkout-filename").textContent = "readme.md";`

---

## Step 5 – Checkout Form

```html
<form id="checkout-form">
  <div class="form-group">
    <label for="checkout-user">Your Name</label>
    <input
      type="text"
      id="checkout-user"
      name="user"
      required
      minlength="3"
      placeholder="Enter your name"
    />
  </div>

  <div class="form-group">
    <label for="checkout-message">Reason for checkout</label>
    <textarea
      id="checkout-message"
      name="message"
      required
      minlength="5"
      placeholder="Why are you editing this file?"
      rows="3"
    ></textarea>
  </div>

  <div class="modal-actions">
    <button
      type="button"
      class="btn btn-secondary"
      onclick="checkoutModal.close()"
    >
      Cancel
    </button>
    <button type="submit" class="btn btn-primary">Confirm Checkout</button>
  </div>
</form>
```

#### Explanation

- **`form id="checkout-form"`**

  - Wraps the inputs and buttons. The `id` lets JavaScript target this form specifically.

- **User field**

  - `<label for="checkout-user">Your Name</label>` links the label to the input via `for` and `id`.
  - `<input type="text" ... required minlength="3">`

    - Forces at least 3 characters before submission.
    - `placeholder` is a visual hint.

- **Message field**

  - `<textarea ... required minlength="5">` ensures the user writes a meaningful reason.
  - `rows="3"` makes it display as 3 lines tall.

- **Actions (buttons)**

  - `Cancel` button: `type="button"` so it doesn’t submit the form.

    - Has `onclick="checkoutModal.close()"`, which calls the JS `ModalManager.close()` instance directly.

  - `Confirm Checkout` button: `type="submit"` so the form can be processed by JavaScript when submitted.

---

## Step 6 – Checkin Modal (Differences)

The checkin modal is almost identical, but let’s highlight the differences:

```html
<!-- Checkin Modal -->
<div id="checkin-modal" class="modal-overlay hidden">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Check In File</h3>
      <button class="modal-close" type="button">&times;</button>
    </div>

    <div class="modal-body">
      <p>You are checking in: <strong id="checkin-filename"></strong></p>

      <form id="checkin-form">
        <div class="form-group">
          <label for="checkin-user">Your Name (for confirmation)</label>
          <input
            type="text"
            id="checkin-user"
            name="user"
            required
            minlength="3"
            placeholder="Enter your name"
          />
        </div>

        <div class="modal-actions">
          <button
            type="button"
            class="btn btn-secondary"
            onclick="checkinModal.close()"
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-primary">
            Confirm Check-in
          </button>
        </div>
      </form>
    </div>
  </div>
</div>
```

#### Key differences

- Title is now **“Check In File”**.
- Placeholder filename goes in `<strong id="checkin-filename">`.
- Form `id="checkin-form"`.
- Input only asks for name (no message textarea).
- Buttons wired to `checkinModal.close()` instead of `checkoutModal.close()`.

---

## Deep Dives & Gotchas

1. **Why two nearly identical modals?**

   - Separation keeps logic clear — you can customize validation rules differently for checkout vs. checkin.
   - Alternative: make one modal and pass in different titles/fields via JavaScript.

2. **Why reset forms on close (from ModalManager)?**

   - Prevents stale values from showing up if a user reopens the modal.

3. **Accessibility notes:**

   - Always associate `<label>` with its input via `for`/`id`.
   - `aria-hidden` attributes could be added to `hidden` state for screen readers.

4. **CSS assumptions:**

   - You need styles for `.modal-overlay`, `.modal-content`, `.modal-header`, `.modal-actions`, `.hidden`.
   - Example:

     ```css
     .modal-overlay {
       position: fixed;
       inset: 0;
       background: rgba(0, 0, 0, 0.5);
       display: flex;
       justify-content: center;
       align-items: center;
     }
     .modal-content {
       background: white;
       padding: 1.5rem;
       border-radius: 0.5rem;
       width: 400px;
       max-width: 90%;
     }
     .hidden {
       display: none;
     }
     ```

---

✅ With this breakdown, you can add the **Checkout Modal** piece by piece, test it, then duplicate and tweak it for the **Checkin Modal**.

```html
<!-- ===================================================================
     MODALS
     =================================================================== -->

<!-- Checkout Modal -->
<div id="checkout-modal" class="modal-overlay hidden">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Check Out File</h3>
      <button class="modal-close" type="button">&times;</button>
    </div>

    <div class="modal-body">
      <p>You are checking out: <strong id="checkout-filename"></strong></p>

      <form id="checkout-form">
        <div class="form-group">
          <label for="checkout-user">Your Name</label>
          <input
            type="text"
            id="checkout-user"
            name="user"
            required
            minlength="3"
            placeholder="Enter your name"
          />
        </div>

        <div class="form-group">
          <label for="checkout-message">Reason for checkout</label>
          <textarea
            id="checkout-message"
            name="message"
            required
            minlength="5"
            placeholder="Why are you editing this file?"
            rows="3"
          ></textarea>
        </div>

        <div class="modal-actions">
          <button
            type="button"
            class="btn btn-secondary"
            onclick="checkoutModal.close()"
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-primary">
            Confirm Checkout
          </button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Checkin Modal -->
<div id="checkin-modal" class="modal-overlay hidden">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Check In File</h3>
      <button class="modal-close" type="button">&times;</button>
    </div>

    <div class="modal-body">
      <p>You are checking in: <strong id="checkin-filename"></strong></p>

      <form id="checkin-form">
        <div class="form-group">
          <label for="checkin-user">Your Name (for confirmation)</label>
          <input
            type="text"
            id="checkin-user"
            name="user"
            required
            minlength="3"
            placeholder="Enter your name"
          />
        </div>

        <div class="modal-actions">
          <button
            type="button"
            class="btn btn-secondary"
            onclick="checkinModal.close()"
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-primary">
            Confirm Check-in
          </button>
        </div>
      </form>
    </div>
  </div>
</div>
```

---

### 3.8: Update Frontend JavaScript

**Update `backend/static/js/app.js`:**

Got it 👍 — instead of dumping a big code block, I’ll restructure **Section 3.8 (Main Application)** into a **code-along tutorial**. We’ll move step by step, introducing _small code pieces_, explaining what they do, _how they work in JavaScript_, and why they matter in application development. Think of it like a guided workshop: type, read, understand, repeat.

---

## 📘 Section 3.8 — Main Application (Code-Along Tutorial)

This section brings everything together. We’ll manage app state, connect the modals, load data, render files, and handle events.

We’ll go in **small increments** so you’re learning JavaScript fundamentals and application patterns — not just copying code.

---

### 🔹 Step 1: Module Imports

```js
/**
 * Main Application
 */

import { themeManager } from "./modules/theme-manager.js";
import { apiClient } from "./modules/api-client.js";
import { ModalManager } from "./modules/modal-manager.js";
```

#### 🔍 Explanation

- `import { ... } from ...` is **ES6 module syntax**.
- Instead of one giant script, we split logic into modules:

  - **`themeManager`** → Handles light/dark mode.
  - **`apiClient`** → Wraps our backend HTTP calls.
  - **`ModalManager`** → Manages opening/closing modals.

➡️ **Why modules?**
They keep code organized, reusable, and prevent naming conflicts. In a real app, modular design makes scaling easier.

---

### 🔹 Step 2: Application State

```js
// ============================================================================
// SECTION 1: Application State
// ============================================================================

let allFiles = [];
let currentFilename = null;
```

#### 🔍 Explanation

- `let allFiles = []` → stores the list of files we fetch from the server.
- `let currentFilename = null` → keeps track of the file currently being checked out/in.

➡️ **Key JavaScript lesson**:

- `let` means the variable can be reassigned later (vs. `const` which locks reassignment).
- We use `null` as a placeholder value until something is selected.

---

### 🔹 Step 3: Modal Instances

```js
// ============================================================================
// SECTION 2: Modal Instances
// ============================================================================

const checkoutModal = new ModalManager("checkout-modal");
const checkinModal = new ModalManager("checkin-modal");
```

#### 🔍 Explanation

- `new ModalManager("checkout-modal")` → Creates a modal instance tied to the element with `id="checkout-modal"`.
- Same for `"checkin-modal"`.
- Each instance manages open/close behavior.

➡️ **Why use classes here?**
Instead of writing duplicated code for each modal, we encapsulate modal logic in the `ModalManager` class and reuse it.

---

### 🔹 Step 4: Data Loading Function

```js
// ============================================================================
// SECTION 3: Data Loading
// ============================================================================

async function loadFiles() {
  const loadingEl = document.getElementById("loading-indicator");
  const fileListEl = document.getElementById("file-list");

  loadingEl.classList.remove("hidden");
  fileListEl.innerHTML = "";

  try {
    const data = await apiClient.getFiles();
    allFiles = data.files;

    loadingEl.classList.add("hidden");
    displayFiles(allFiles);
  } catch (error) {
    loadingEl.classList.add("hidden");
    fileListEl.innerHTML = `
      <div style="text-align: center; padding: 2rem; color: var(--status-danger-text);">
        <p><strong>Error loading files:</strong></p>
        <p>${error.message}</p>
        <button class="btn btn-primary" onclick="location.reload()">
          Retry
        </button>
      </div>
    `;
  }
}
```

#### 🔍 Explanation

- `async function loadFiles()` → lets us use `await` for asynchronous calls.
- `loadingEl.classList.remove("hidden")` → shows a loading spinner/indicator.
- `fileListEl.innerHTML = ""` → clears out any previous files.
- `await apiClient.getFiles()` → fetches files from backend (returns a Promise).
- On success → `displayFiles(allFiles)`.
- On error → display a retry message.

➡️ **JavaScript deep dive**:

- `await` pauses execution until the Promise resolves, but doesn’t block the browser.
- Errors inside `await` must be caught with `try/catch`.

---

✅ So far we’ve:

- Imported modules.
- Created app state.
- Connected modals.
- Written a function to fetch and display files.

---

Perfect 👍 Let’s continue the **code-along tutorial for Section 3.8** — moving to **DOM Rendering**.

We’ll break this into **small chunks**: add some code, then pause to explain how it works and why it’s written this way.

---

## 📘 Section 3.8 — Main Application (Code-Along)

### 🔹 Step 5: Rendering Files (Wrapper Function)

```js
// ============================================================================
// SECTION 4: DOM Rendering
// ============================================================================

function displayFiles(files) {
  const container = document.getElementById("file-list");
  container.innerHTML = "";
```

#### 🔍 Explanation

- `function displayFiles(files)` → defines a **reusable function** that takes an array of file objects and renders them into the DOM.
- `document.getElementById("file-list")` → finds the `<div id="file-list">` element where our files will appear.
- `container.innerHTML = ""` → clears any previous content before rendering fresh data.

➡️ **Why clear first?**
If we don’t, the old file list will remain, and the new one will just append on top → duplicates.

---

### 🔹 Step 6: Empty State Handling

```js
if (!files || files.length === 0) {
  container.innerHTML = `
      <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
        <p>No .mcam files found in repository.</p>
        <p style="font-size: var(--font-size-sm);">Add files to backend/repo/</p>
      </div>
    `;
  return;
}
```

#### 🔍 Explanation

- `if (!files || files.length === 0)` → checks if the `files` array is empty or undefined.
- If true → replace the container’s content with a **friendly empty state message**.
- `return;` → exits the function early so we don’t try to loop over `files`.

➡️ **Key pattern**:
Always handle “nothing to show” cases in UI → improves user experience and prevents runtime errors.

---

### 🔹 Step 7: Looping Through Files

```js
  files.forEach((file) => {
    const fileElement = createFileElement(file);
    container.appendChild(fileElement);
  });
}
```

#### 🔍 Explanation

- `.forEach((file) => { ... })` → loops over every file object.
- `createFileElement(file)` → builds the HTML for a single file.
- `container.appendChild(fileElement)` → adds the file’s HTML to the container.

➡️ **Why separate into `createFileElement`?**
Keeps `displayFiles` clean. It handles **“when and where”** files are displayed, while `createFileElement` handles **“what each file looks like.”**

---

### 🔹 Step 8: Creating a File Element (Start)

```js
function createFileElement(file) {
  const div = document.createElement("div");
  div.className = "file-item";
```

#### 🔍 Explanation

- `document.createElement("div")` → dynamically creates a `<div>` in memory.
- `div.className = "file-item"` → applies a CSS class for styling.

➡️ **Why not `innerHTML` here?**
Using `createElement` is safer — avoids XSS injection risks and gives more flexibility for dynamic child nodes.

---

### 🔹 Step 9: File Info Section

```js
const infoDiv = document.createElement("div");
infoDiv.className = "file-info";

const nameSpan = document.createElement("span");
nameSpan.className = "file-name";
nameSpan.textContent = file.name;

const statusSpan = document.createElement("span");
statusSpan.className = `file-status status-${file.status}`;
statusSpan.textContent = file.status.replace("_", " ").toUpperCase();

infoDiv.appendChild(nameSpan);
infoDiv.appendChild(statusSpan);
```

#### 🔍 Explanation

- `infoDiv` → wraps the filename + status.
- `nameSpan.textContent = file.name` → sets the text to the actual filename.
- `statusSpan.className = status-${file.status}` → gives dynamic CSS class like `status-available` or `status-locked`.
- `file.status.replace("_", " ").toUpperCase()` → turns `checked_out` into `CHECKED OUT` (more readable).
- Finally → `appendChild` adds both spans into `infoDiv`.

➡️ **Lesson:** This shows how to **bind data to DOM elements** dynamically — a key skill in any frontend app.

---

✅ At this point, each file has:

- A wrapper `<div class="file-item">`.
- Inside it, a file info block with name + status.

---

Got it ✅ — I’ll keep the **teaching focus** front and center: not just what the code does, but why it’s structured this way, what JavaScript concepts it demonstrates, and how it relates to app development best practices.

We’re still in **Section 3.8 → DOM Rendering**, and now we’ll build out the **actions** part of each file row.

---

## 📘 Section 3.8 — DOM Rendering (Part 2)

### 🔹 Step 10: Actions Wrapper

```js
const actionsDiv = document.createElement("div");
actionsDiv.className = "file-actions";
```

#### 🔍 Explanation

- `createElement("div")` → creates a container for buttons and extra metadata (like “locked by”).
- `actionsDiv.className = "file-actions";` → CSS handles spacing & alignment.

➡️ **Teaching Point**:
When structuring UI, separate _information display_ (file name/status) from _actions_ (buttons). This separation of concerns makes code and layout cleaner.

---

### 🔹 Step 11: Conditional Rendering – Available File

```js
if (file.status === "available") {
  const checkoutBtn = document.createElement("button");
  checkoutBtn.className = "btn btn-primary btn-sm";
  checkoutBtn.textContent = "Checkout";
  checkoutBtn.onclick = () => handleCheckout(file.name);
  actionsDiv.appendChild(checkoutBtn);
}
```

#### 🔍 Explanation

- `if (file.status === "available")` → branching logic: only show “Checkout” if no one has the file locked.
- `checkoutBtn.textContent = "Checkout";` → sets button label.
- `checkoutBtn.onclick = () => handleCheckout(file.name);`

  - Here’s **event-driven programming** in action: the UI doesn’t _do_ anything until the user clicks.
  - The `() => handleCheckout(file.name)` uses an **arrow function** → keeps `file.name` bound to the correct file when the loop runs.

➡️ **Key JS Concept**: Closures in event handlers.
If we didn’t use arrow functions (or properly scoped functions), we could accidentally bind the wrong file to the click.

---

### 🔹 Step 12: Conditional Rendering – Checked Out File

```js
  else {
    const checkinBtn = document.createElement("button");
    checkinBtn.className = "btn btn-secondary btn-sm";
    checkinBtn.textContent = "Checkin";
    checkinBtn.onclick = () => handleCheckin(file.name);
    actionsDiv.appendChild(checkinBtn);
```

#### 🔍 Explanation

- If status is **not** `available`, assume it’s checked out.
- This creates a “Checkin” button with a different CSS class (secondary style).
- Again, attaches a click handler: `handleCheckin(file.name)`.

➡️ **Lesson**:
Here, the **UI adapts based on state**. This is a fundamental principle of app development:

- **State → UI.**
  Whenever state changes (like a file being locked), the UI should reflect that.

---

### 🔹 Step 13: Showing Who Locked It

```js
    if (file.locked_by) {
      const lockedBySpan = document.createElement("span");
      lockedBySpan.style.fontSize = "var(--font-size-sm)";
      lockedBySpan.style.color = "var(--text-secondary)";
      lockedBySpan.textContent = `Locked by: ${file.locked_by}`;
      actionsDiv.appendChild(lockedBySpan);
    }
  }
```

#### 🔍 Explanation

- `if (file.locked_by)` → only show this if backend returned a username.
- Instead of a button, we’re adding a `<span>` with inline styles for smaller, muted text.
- `lockedBySpan.textContent = ...` → shows “Locked by: Alice”.

➡️ **Teaching Point**:

- Here you see **progressive enrichment**: not every file has this info, but if it exists, we render it.
- Also demonstrates **inline styling vs CSS classes**:

  - Inline styles are fine for one-offs.
  - For consistency, production apps usually prefer CSS classes.

---

### 🔹 Step 14: Final Assembly of File Element

```js
  div.appendChild(infoDiv);
  div.appendChild(actionsDiv);

  return div;
}
```

#### 🔍 Explanation

- `appendChild(infoDiv)` → add the name & status block.
- `appendChild(actionsDiv)` → add the buttons block.
- Finally → `return div;` → now the full file row is ready to be inserted into the page.

➡️ **Lesson Recap**:

- **DOM creation**: `createElement`, `textContent`, `appendChild`.
- **Dynamic UI**: conditionally render based on `file.status`.
- **Events**: attach handlers directly in JS, not inline HTML.
- **Separation of concerns**:

  - `displayFiles` decides _which_ files to render.
  - `createFileElement` decides _how_ a file looks.

---

✅ At this point, you can run the app and you’ll see:

- Each file shows its name and status.
- Available → shows **Checkout** button.
- Locked → shows **Checkin** button and “Locked by …”.

---

Perfect 👍 let’s dive into **Section 5: Event Handlers**.
This is where our UI buttons (Checkout / Checkin) actually start doing things — turning clicks into app logic.
I’ll keep it **code-along style**: small code chunks + deep explanation.

---

## 📘 Section 3.8 — Event Handlers (Part 1)

### 🔹 Step 15: Checkout Handler

```js
function handleCheckout(filename) {
  currentFilename = filename;
  document.getElementById("checkout-filename").textContent = filename;
  checkoutModal.open();
}
```

#### 🔍 Explanation

- `function handleCheckout(filename)` → normal JS function, triggered when you click a “Checkout” button.
- `currentFilename = filename;`

  - We save the selected file’s name in a **global state variable** (defined earlier).
  - Why? Because when the user fills out the form and submits, we need to know which file they were acting on.

- `document.getElementById("checkout-filename").textContent = filename;`

  - Inside the modal, there’s a `<strong id="checkout-filename">` placeholder.
  - This line updates that placeholder with the actual filename → gives user visual confirmation.

- `checkoutModal.open();`

  - Calls our `ModalManager` class to actually display the modal.
  - This handles showing the popup, preventing scroll, and focusing on inputs.

➡️ **Teaching Point**:
This is the **UI flow pattern**:

1. Store app state (filename).
2. Update DOM to reflect the state.
3. Open modal for user interaction.

---

### 🔹 Step 16: Checkin Handler

```js
function handleCheckin(filename) {
  currentFilename = filename;
  document.getElementById("checkin-filename").textContent = filename;
  checkinModal.open();
}
```

#### 🔍 Explanation

- Identical logic, but for **checkin** instead of checkout.
- Updates `currentFilename`.
- Displays filename inside the checkin modal.
- Opens `checkinModal`.

➡️ **Key Idea**:
Both checkout and checkin follow the **same pattern**, but with different forms.
This repetition is intentional: it shows how you can reuse code structures with small variations — a common practice in app development.

---

✅ At this stage:

- Clicking “Checkout” opens the checkout modal with the correct file name filled in.
- Clicking “Checkin” opens the checkin modal with the correct file name.

So far, no API calls — just **state + UI updates**.

---

Perfect! Let’s move to **Step 17: submitCheckout()**, the first function that actually talks to the backend. We'll break it down **line by line**, and explain **how JavaScript handles forms, events, and async calls**.

---

## 📘 Section 3.8 — Event Handlers (Part 2)

### 🔹 Step 17: submitCheckout

```js
async function submitCheckout(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const data = {
    filename: currentFilename,
    user: formData.get("user"),
    message: formData.get("message"),
  };

  try {
    await apiClient.post("/api/files/checkout", data);

    showNotification("File checked out successfully!", "success");
    checkoutModal.close();
    loadFiles();
  } catch (error) {
    showNotification(`Checkout failed: ${error.message}`, "error");
  }
}
```

---

#### 🔍 Line-by-Line Breakdown

##### 1️⃣ `async function submitCheckout(event) {`

- Declares a function as **async**, which means we can use `await` inside.
- Why async? Because sending requests to the backend is **asynchronous** (non-blocking).
- `event` is the **form submission event** automatically passed by the browser.

---

##### 2️⃣ `event.preventDefault();`

- Forms usually **reload the page** on submit.
- `preventDefault()` **stops the browser’s default behavior** so we can handle it via JavaScript.
- Teaching Point: Forms in modern apps almost always use `preventDefault()` with JS submissions.

---

##### 3️⃣ `const formData = new FormData(event.target);`

- `FormData` is a built-in browser API.
- `event.target` is the `<form>` element that triggered the submit.
- `FormData` collects all input values from the form automatically.
- Example: `{ user: "Alice", message: "Fixing a bug" }`

---

##### 4️⃣ Construct the payload

```js
const data = {
  filename: currentFilename,
  user: formData.get("user"),
  message: formData.get("message"),
};
```

- Combines **UI state** (`currentFilename`) and **form data** (`user`, `message`) into a single object.
- Why not just send formData?

  - Because the backend expects **JSON** (`{ filename, user, message }`), not raw form data.

---

##### 5️⃣ `try { ... } catch (error) { ... }`

- JS **try/catch** block handles errors gracefully.
- `await apiClient.post(...)` may fail (network down, server error).
- If it throws, the `catch` block runs instead of crashing the app.

---

##### 6️⃣ `await apiClient.post("/api/files/checkout", data);`

- Sends a **POST request** to the backend API.
- `apiClient` is a wrapper around `fetch()` (or similar).
- Teaching Point: `await` pauses execution **only in this function**, not the entire page.
- This allows the browser to remain responsive while waiting for the server.

---

##### 7️⃣ Success Handling

```js
showNotification("File checked out successfully!", "success");
checkoutModal.close();
loadFiles();
```

- `showNotification()` → tells the user the operation succeeded.
- `checkoutModal.close()` → hides the modal, restores body scroll, clears the form.
- `loadFiles()` → reloads the file list from backend to reflect the new lock status.

---

##### 8️⃣ Error Handling

```js
catch (error) {
  showNotification(`Checkout failed: ${error.message}`, "error");
}
```

- If the POST fails, the user sees a clear message.
- This avoids silent failures, which are **common beginner mistakes**.

---

#### ✅ Key Teaching Points

1. **Async/Await**: Modern JS pattern for handling asynchronous tasks like network requests.
2. **FormData API**: Simplifies reading form inputs without manually querying `input.value`.
3. **State + DOM Integration**: Combines `currentFilename` (app state) with form values (UI input).
4. **Error Handling**: Always wrap `await` calls in `try/catch` to avoid unhandled rejections.
5. **UX Flow**: Success → notify user → close modal → refresh data.

---

Perfect! Let’s do **Step 18: submitCheckin()** the same way. We’ll go **line by line**, highlight similarities and subtle differences from `submitCheckout()`, and explain why those differences exist.

---

## 📘 Section 3.8 — Event Handlers (Part 3)

### 🔹 Step 18: submitCheckin

```js
async function submitCheckin(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const data = {
    filename: currentFilename,
    user: formData.get("user"),
  };

  try {
    await apiClient.post("/api/files/checkin", data);

    showNotification("File checked in successfully!", "success");
    checkinModal.close();
    loadFiles();
  } catch (error) {
    showNotification(`Checkin failed: ${error.message}`, "error");
  }
}
```

---

#### 🔍 Line-by-Line Breakdown

##### 1️⃣ `async function submitCheckin(event) {`

- Async function because **posting to the backend is asynchronous**.
- Receives the **form submit event** automatically.

---

##### 2️⃣ `event.preventDefault();`

- Prevents the form from **refreshing the page**, same as in `submitCheckout()`.
- Essential for **single-page app behavior**.

---

##### 3️⃣ `const formData = new FormData(event.target);`

- Reads all inputs from the check-in form.
- Teaching Point: `FormData` works with any form, so you don’t have to manually select inputs like `document.getElementById("checkin-user").value`.

---

##### 4️⃣ Construct the payload

```js
const data = {
  filename: currentFilename,
  user: formData.get("user"),
};
```

- **Difference from checkout**: no `message` field.
- Backend only needs **filename** and **user** to release the lock.
- Shows how **different API endpoints require different payloads**, even if the function structure is almost identical.

---

##### 5️⃣ `try { ... } catch (error) { ... }`

- Same pattern as `submitCheckout()`.
- Ensures the app **doesn’t crash** if the network request fails.

---

##### 6️⃣ `await apiClient.post("/api/files/checkin", data);`

- Posts the payload to the **check-in endpoint**.
- `await` pauses this function until the backend responds.
- Teaching Point: `await` only blocks this function, not the whole app.

---

##### 7️⃣ Success Handling

```js
showNotification("File checked in successfully!", "success");
checkinModal.close();
loadFiles();
```

- Shows a notification on success.
- Closes the **check-in modal** instead of checkout modal.
- Refreshes the file list to reflect the lock release.
- Teaching Point: You can **reuse the same patterns** for multiple operations by swapping out **modal instances** and **API endpoints**.

---

##### 8️⃣ Error Handling

```js
catch (error) {
  showNotification(`Checkin failed: ${error.message}`, "error");
}
```

- Same pattern as checkout: user sees a clear message if something goes wrong.

---

#### ✅ Key Teaching Points

1. **Repetition reinforces patterns**: `submitCheckout` and `submitCheckin` share almost the same structure.
2. **Payload differences**: Always check backend requirements; sending extra fields may be ignored or cause errors.
3. **Modularity**: By separating checkout vs checkin, the modal manager and apiClient can be reused.
4. **Event-driven design**: Forms submit → JS intercepts → backend call → UI update. This pattern is **core to modern web apps**.
5. **Error-first mindset**: Always anticipate failures and provide user feedback.

---

Perfect! Let’s tackle **Step 19: DOMContentLoaded initialization**. This is the final glue that ties all the previous pieces together, and it’s a great opportunity to teach **DOM events, event listeners, and app initialization patterns** in JavaScript.

We’ll break it **line by line**, explaining everything and showing why each piece matters.

---

## 📘 Section 3.8 — Initialization (Step 19)

```js
document.addEventListener("DOMContentLoaded", () => {
  console.log("PDM App initialized");

  // Theme toggle
  document
    .getElementById("theme-toggle")
    .addEventListener("click", () => themeManager.toggle());

  // Form submissions
  document
    .getElementById("checkout-form")
    .addEventListener("submit", submitCheckout);

  document
    .getElementById("checkin-form")
    .addEventListener("submit", submitCheckin);

  // Load initial data
  loadFiles();
});
```

---

#### 🔍 Line-by-Line Breakdown

##### 1️⃣ `document.addEventListener("DOMContentLoaded", () => {`

- This registers a **callback function** that runs **only after the HTML document has been fully loaded and parsed**.
- Teaching Point: Unlike `window.onload`, `DOMContentLoaded` fires **before images and other external assets are fully loaded**, so your app feels faster.
- Ensures **all `getElementById` calls succeed** because the elements exist in the DOM.

---

##### 2️⃣ `console.log("PDM App initialized");`

- Debugging / teaching tool. Shows that your initialization code ran.
- Helps beginners **verify event listeners are registered**.

---

##### 3️⃣ Theme toggle

```js
document
  .getElementById("theme-toggle")
  .addEventListener("click", () => themeManager.toggle());
```

- Selects the **theme toggle button** by its `id`.
- Registers a **click event listener** that calls `themeManager.toggle()`.
- Teaching Points:

  1. `getElementById` is the most direct way to select elements by ID.
  2. Event listeners allow **decoupling UI from logic**.
  3. Arrow functions are used here to maintain **lexical `this`** (though not critical here, it’s a good habit).

---

##### 4️⃣ Form submission handlers

```js
document
  .getElementById("checkout-form")
  .addEventListener("submit", submitCheckout);

document
  .getElementById("checkin-form")
  .addEventListener("submit", submitCheckin);
```

- Each form is selected and an event listener is attached to **intercept submission**.
- Teaching Points:

  1. This is where `submitCheckout` and `submitCheckin` are **connected to the UI**.
  2. `addEventListener("submit", ...)` is preferred over `onsubmit=` in HTML because it allows **multiple listeners** and keeps JS separate from HTML.
  3. The forms will **not refresh the page**, thanks to `event.preventDefault()` inside each handler.

---

##### 5️⃣ Load initial data

```js
loadFiles();
```

- Calls the function we discussed earlier to **fetch all files from the backend and render them**.

- Teaching Point: App initialization is a pattern:

  1. Wait for DOM → ensure elements exist.
  2. Register UI event listeners → enable user interaction.
  3. Fetch initial data → populate the UI.

- This pattern is **core to almost every JS single-page application (SPA)**.

---

#### ✅ Key Teaching Points

1. **DOMContentLoaded vs window.onload**: `DOMContentLoaded` fires earlier and is ideal for setting up **event listeners**.
2. **Separation of concerns**: JS initializes the app, attaches events, and then fetches data. HTML remains declarative.
3. **Reusability**: By using `submitCheckout`, `submitCheckin`, and `loadFiles` as separate functions, the initialization code is **short, readable, and maintainable**.
4. **Debugging habits**: Using `console.log` at init points helps verify app flow.

---

💡 **Teaching Tip:**
You can expand this pattern to any SPA: setup state → attach UI events → fetch data → render UI. Everything in this app follows this **modular and event-driven design**, which is a best practice.

---

```javascript
/**
 * Main Application
 */

import { themeManager } from "./modules/theme-manager.js";
import { apiClient } from "./modules/api-client.js";
import { ModalManager } from "./modules/modal-manager.js";

// ============================================================================
// SECTION 1: Application State
// ============================================================================

let allFiles = [];
let currentFilename = null;

// ============================================================================
// SECTION 2: Modal Instances
// ============================================================================

const checkoutModal = new ModalManager("checkout-modal");
const checkinModal = new ModalManager("checkin-modal");

// ============================================================================
// SECTION 3: Data Loading
// ============================================================================

async function loadFiles() {
  const loadingEl = document.getElementById("loading-indicator");
  const fileListEl = document.getElementById("file-list");

  loadingEl.classList.remove("hidden");
  fileListEl.innerHTML = "";

  try {
    const data = await apiClient.getFiles();
    allFiles = data.files;

    loadingEl.classList.add("hidden");
    displayFiles(allFiles);
  } catch (error) {
    loadingEl.classList.add("hidden");
    fileListEl.innerHTML = `
      <div style="text-align: center; padding: 2rem; color: var(--status-danger-text);">
        <p><strong>Error loading files:</strong></p>
        <p>${error.message}</p>
        <button class="btn btn-primary" onclick="location.reload()">
          Retry
        </button>
      </div>
    `;
  }
}

// ============================================================================
// SECTION 4: DOM Rendering
// ============================================================================

function displayFiles(files) {
  const container = document.getElementById("file-list");
  container.innerHTML = "";

  if (!files || files.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
        <p>No .mcam files found in repository.</p>
        <p style="font-size: var(--font-size-sm);">Add files to backend/repo/</p>
      </div>
    `;
    return;
  }

  files.forEach((file) => {
    const fileElement = createFileElement(file);
    container.appendChild(fileElement);
  });
}

function createFileElement(file) {
  const div = document.createElement("div");
  div.className = "file-item";

  const infoDiv = document.createElement("div");
  infoDiv.className = "file-info";

  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ").toUpperCase();

  infoDiv.appendChild(nameSpan);
  infoDiv.appendChild(statusSpan);

  const actionsDiv = document.createElement("div");
  actionsDiv.className = "file-actions";

  if (file.status === "available") {
    const checkoutBtn = document.createElement("button");
    checkoutBtn.className = "btn btn-primary btn-sm";
    checkoutBtn.textContent = "Checkout";
    checkoutBtn.onclick = () => handleCheckout(file.name);
    actionsDiv.appendChild(checkoutBtn);
  } else {
    const checkinBtn = document.createElement("button");
    checkinBtn.className = "btn btn-secondary btn-sm";
    checkinBtn.textContent = "Checkin";
    checkinBtn.onclick = () => handleCheckin(file.name);
    actionsDiv.appendChild(checkinBtn);

    if (file.locked_by) {
      const lockedBySpan = document.createElement("span");
      lockedBySpan.style.fontSize = "var(--font-size-sm)";
      lockedBySpan.style.color = "var(--text-secondary)";
      lockedBySpan.textContent = `Locked by: ${file.locked_by}`;
      actionsDiv.appendChild(lockedBySpan);
    }
  }

  div.appendChild(infoDiv);
  div.appendChild(actionsDiv);

  return div;
}

// ============================================================================
// SECTION 5: Event Handlers
// ============================================================================

function handleCheckout(filename) {
  currentFilename = filename;
  document.getElementById("checkout-filename").textContent = filename;
  checkoutModal.open();
}

function handleCheckin(filename) {
  currentFilename = filename;
  document.getElementById("checkin-filename").textContent = filename;
  checkinModal.open();
}

async function submitCheckout(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const data = {
    filename: currentFilename,
    user: formData.get("user"),
    message: formData.get("message"),
  };

  try {
    await apiClient.post("/api/files/checkout", data);

    showNotification("File checked out successfully!", "success");
    checkoutModal.close();
    loadFiles();
  } catch (error) {
    showNotification(`Checkout failed: ${error.message}`, "error");
  }
}

async function submitCheckin(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const data = {
    filename: currentFilename,
    user: formData.get("user"),
  };

  try {
    await apiClient.post("/api/files/checkin", data);

    showNotification("File checked in successfully!", "success");
    checkinModal.close();
    loadFiles();
  } catch (error) {
    showNotification(`Checkin failed: ${error.message}`, "error");
  }
}

function showNotification(message, type = "info") {
  // Simple notification - will enhance in Stage 4
  alert(message);
}

// ============================================================================
// SECTION 6: Initialization
// ============================================================================

document.addEventListener("DOMContentLoaded", () => {
  console.log("PDM App initialized");

  // Theme toggle
  document
    .getElementById("theme-toggle")
    .addEventListener("click", () => themeManager.toggle());

  // Form submissions
  document
    .getElementById("checkout-form")
    .addEventListener("submit", submitCheckout);

  document
    .getElementById("checkin-form")
    .addEventListener("submit", submitCheckin);

  // Load initial data
  loadFiles();
});
```

---

### Stage 3 Complete

**Test the full workflow:**

```bash
## Start server
uvicorn app.main:app --reload

## Visit
http://127.0.0.1:8000
```

**You should be able to:**

1. See real files from `backend/repo/`
2. Click "Checkout" on an available file
3. Fill out the modal form
4. Submit and see file status change to "checked_out"
5. Click "Checkin" to release the lock
6. See file return to "available"

**File structure now:**

```
backend/
├── app/
│   ├── services/
│   │   └── file_service.py      ## NEW
│   ├── utils/
│   │   └── file_locking.py      ## NEW
│   ├── learn_filesystem.py      ## NEW
│   └── (existing files)
├── static/
│   └── js/modules/
│       └── modal-manager.js     ## NEW
├── repo/                        ## NEW
│   ├── PN1001_OP1.mcam
│   ├── PN1002_OP1.mcam
│   └── PN1003_OP1.mcam
└── locks.json                   ## Auto-created
```

**What you learned:**

- File system operations and performance
- Race conditions and atomicity
- Cross-platform file locking
- Service layer architecture
- Dependency injection in FastAPI
- Modal dialogs and form handling
- Async form submission

Ready for Stage 4?

## Stage 4: Advanced Frontend - State Management & UX Polish

**Prerequisites**: Completed Stage 3

**Time**: 4-5 hours

**What you'll build**: Professional state management system, toast notifications, search/filter/sort functionality, and polished UX.

---

### 4.1: Deep Dive - State Management Patterns

**File: `backend/static/js/modules/learn_state_management.js`**

```javascript
/**
 * Understanding State Management in Frontend Applications
 *
 * State = Data that changes over time and affects what users see
 *
 * Examples of state:
 * - List of files
 * - Current search term
 * - Which file is selected
 * - Loading status
 * - User preferences
 */

// ============================================================================
// SECTION 1: The Problem - Scattered State
// ============================================================================

/**
 * BAD APPROACH: Global variables everywhere
 *
 * Problems:
 * - Hard to track what changed
 * - No single source of truth
 * - Bugs from stale data
 * - Can't time-travel debug
 */
let files = [];
let searchTerm = "";
let isLoading = false;
let selectedFile = null;

function badExample() {
  // Code in file1.js modifies files
  files.push({ name: "new.txt" });

  // Code in file2.js doesn't know files changed
  // UI is out of sync
}

// ============================================================================
// SECTION 2: The Solution - Centralized Store
// ============================================================================

/**
 * GOOD APPROACH: Single store with observers
 *
 * Benefits:
 * - Single source of truth
 * - Predictable updates
 * - Easy to debug (log all state changes)
 * - UI automatically syncs
 *
 * This is the Observer Pattern (aka Pub/Sub)
 */

class SimpleStore {
  constructor(initialState) {
    this.state = initialState;
    this.listeners = [];
  }

  /**
   * Subscribe to state changes
   * Listener is called whenever state updates
   */
  subscribe(listener) {
    this.listeners.push(listener);
    // Immediately call with current state
    listener(this.state);
  }

  /**
   * Update state and notify all listeners
   */
  setState(newState) {
    this.state = { ...this.state, ...newState };
    this.notify();
  }

  /**
   * Notify all subscribers of state change
   */
  notify() {
    this.listeners.forEach((listener) => {
      listener(this.state);
    });
  }
}

// Usage example
const store = new SimpleStore({ count: 0, name: "Alice" });

// Component 1 subscribes
store.subscribe((state) => {
  console.log("Component 1 sees:", state);
});

// Component 2 subscribes
store.subscribe((state) => {
  console.log("Component 2 sees:", state);
});

// Update state - both components are notified automatically
store.setState({ count: 1 });
// Logs:
// Component 1 sees: { count: 1, name: 'Alice' }
// Component 2 sees: { count: 1, name: 'Alice' }

// ============================================================================
// SECTION 3: Actions Pattern
// ============================================================================

/**
 * Actions = Named functions that update state
 *
 * Benefits:
 * - Self-documenting ("setFiles" vs setState({ files: [...] }))
 * - Can add logging/validation
 * - Can be asynchronous
 */

class StoreWithActions {
  constructor() {
    this.state = {
      files: [],
      isLoading: false,
      error: null,
    };
    this.listeners = [];
  }

  subscribe(listener) {
    this.listeners.push(listener);
    listener(this.state);
  }

  notify() {
    this.listeners.forEach((listener) => listener(this.state));
  }

  // Actions - named state updates

  setLoading() {
    console.log("ACTION: setLoading");
    this.state = { ...this.state, isLoading: true, error: null };
    this.notify();
  }

  setFiles(files) {
    console.log("ACTION: setFiles", files.length, "files");
    this.state = { ...this.state, files, isLoading: false };
    this.notify();
  }

  setError(error) {
    console.log("ACTION: setError", error);
    this.state = { ...this.state, error, isLoading: false };
    this.notify();
  }
}

// ============================================================================
// SECTION 4: Computed Properties (Derived State)
// ============================================================================

/**
 * Computed = State derived from other state
 *
 * Don't store filtered results - compute them on demand
 * Keeps state minimal and prevents bugs from stale data
 */

class StoreWithComputed {
  constructor() {
    this.state = {
      files: [
        { name: "file1.txt", status: "available" },
        { name: "file2.txt", status: "locked" },
      ],
      searchTerm: "",
      statusFilter: "all",
    };
  }

  // Computed property - not stored, calculated on demand
  getFilteredFiles() {
    let result = this.state.files;

    // Apply search
    if (this.state.searchTerm) {
      const term = this.state.searchTerm.toLowerCase();
      result = result.filter((f) => f.name.toLowerCase().includes(term));
    }

    // Apply status filter
    if (this.state.statusFilter !== "all") {
      result = result.filter((f) => f.status === this.state.statusFilter);
    }

    return result;
  }
}

// ============================================================================
// SECTION 5: Comparison to React/Vue/Svelte
// ============================================================================

/**
 * Our simple store vs. frameworks:
 *
 * Our Store:
 * - Manual subscribe/notify
 * - Manual DOM updates
 * - Simple, no build step
 *
 * React:
 * - useState/useReducer for local state
 * - Context API or Redux for global state
 * - Virtual DOM automatically updates UI
 *
 * Vue:
 * - Reactive data() for local state
 * - Vuex/Pinia for global state
 * - Reactive system automatically updates UI
 *
 * Svelte:
 * - $: reactive declarations
 * - Stores for global state
 * - Compiler generates efficient updates
 *
 * Our approach teaches the fundamentals they all use internally.
 */

export { SimpleStore, StoreWithActions, StoreWithComputed };
```

---

### 4.2: Production Store Implementation

**File: `backend/static/js/modules/store.js`**

```javascript
/**
 * Application State Store
 *
 * Centralized state management for the PDM application.
 * Implements Observer pattern with actions for predictable updates.
 */

// ============================================================================
// SECTION 1: Store Class
// ============================================================================

class Store {
  constructor(initialState = {}) {
    this.state = {
      // File data
      allFiles: [],

      // UI state
      isLoading: true,
      error: null,

      // Filters and search
      searchTerm: "",
      statusFilter: "all", // 'all' | 'available' | 'checked_out'
      sortBy: "name-asc", // 'name-asc' | 'name-desc' | 'size-asc' | 'size-desc'

      // Selection
      selectedFile: null,

      // Override with initial state
      ...initialState,
    };

    this.listeners = [];
  }

  // ==========================================================================
  // SECTION 2: Subscription Management
  // ==========================================================================

  /**
   * Subscribe to state changes
   * Returns unsubscribe function
   */
  subscribe(listener) {
    this.listeners.push(listener);

    // Immediately invoke with current state
    listener({ ...this.state });

    // Return unsubscribe function
    return () => {
      const index = this.listeners.indexOf(listener);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }

  /**
   * Notify all listeners of state change
   */
  _notify() {
    // Pass a copy to prevent accidental mutation
    const stateCopy = { ...this.state };
    this.listeners.forEach((listener) => {
      try {
        listener(stateCopy);
      } catch (error) {
        console.error("Error in state listener:", error);
      }
    });
  }

  // ==========================================================================
  // SECTION 3: Actions - File Data
  // ==========================================================================

  setLoading() {
    this.state.isLoading = true;
    this.state.error = null;
    this._notify();
  }

  setFiles(files) {
    this.state.allFiles = files;
    this.state.isLoading = false;
    this.state.error = null;
    this._notify();
  }

  setError(error) {
    this.state.error = error;
    this.state.isLoading = false;
    this._notify();
  }

  updateFile(filename, updates) {
    const index = this.state.allFiles.findIndex((f) => f.name === filename);
    if (index !== -1) {
      this.state.allFiles[index] = {
        ...this.state.allFiles[index],
        ...updates,
      };
      this._notify();
    }
  }

  // ==========================================================================
  // SECTION 4: Actions - Filters
  // ==========================================================================

  setSearchTerm(term) {
    this.state.searchTerm = term;
    this._notify();
  }

  setStatusFilter(filter) {
    this.state.statusFilter = filter;
    this._notify();
  }

  setSortBy(sortBy) {
    this.state.sortBy = sortBy;
    this._notify();
  }

  // ==========================================================================
  // SECTION 5: Actions - Selection
  // ==========================================================================

  setSelectedFile(file) {
    this.state.selectedFile = file;
    this._notify();
  }

  clearSelection() {
    this.state.selectedFile = null;
    this._notify();
  }

  // ==========================================================================
  // SECTION 6: Computed Properties
  // ==========================================================================

  /**
   * Get filtered files based on search and status filter
   */
  getFilteredFiles() {
    let result = [...this.state.allFiles];

    // Apply search filter
    if (this.state.searchTerm) {
      const term = this.state.searchTerm.toLowerCase();
      result = result.filter((file) => file.name.toLowerCase().includes(term));
    }

    // Apply status filter
    if (this.state.statusFilter !== "all") {
      result = result.filter((file) => file.status === this.state.statusFilter);
    }

    return result;
  }

  /**
   * Get sorted files
   */
  getSortedFiles(files) {
    const [field, direction] = this.state.sortBy.split("-");

    return [...files].sort((a, b) => {
      let aVal, bVal;

      switch (field) {
        case "name":
          aVal = a.name.toLowerCase();
          bVal = b.name.toLowerCase();
          break;
        case "size":
          aVal = a.size_bytes || 0;
          bVal = b.size_bytes || 0;
          break;
        case "status":
          aVal = a.status;
          bVal = b.status;
          break;
        default:
          return 0;
      }

      const comparison = aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
      return direction === "asc" ? comparison : -comparison;
    });
  }

  /**
   * Get files with all transformations applied
   */
  getDisplayFiles() {
    const filtered = this.getFilteredFiles();
    return this.getSortedFiles(filtered);
  }
}

// ============================================================================
// SECTION 7: Export Singleton Instance
// ============================================================================

export const store = new Store();
```

---

### 4.3: Toast Notification System

**File: `backend/static/js/modules/toast.js`**

```javascript
/**
 * Toast Notification System
 *
 * Non-blocking notifications that auto-dismiss.
 */

// ============================================================================
// SECTION 1: Toast Manager
// ============================================================================

class ToastManager {
  constructor() {
    this.container = null;
    this.toasts = [];
    this.nextId = 1;
    this.init();
  }

  init() {
    // Create container if it doesn't exist
    if (!document.getElementById("toast-container")) {
      this.container = document.createElement("div");
      this.container.id = "toast-container";
      this.container.className = "toast-container";
      document.body.appendChild(this.container);
    } else {
      this.container = document.getElementById("toast-container");
    }
  }

  /**
   * Show a toast notification
   *
   * @param {string} message - Message to display
   * @param {string} type - 'success' | 'error' | 'warning' | 'info'
   * @param {number} duration - Auto-dismiss time in ms (0 = no auto-dismiss)
   */
  show(message, type = "info", duration = 4000) {
    const id = this.nextId++;

    // Create toast element
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.dataset.toastId = id;

    // Icon based on type
    const icons = {
      success: "✓",
      error: "✕",
      warning: "⚠",
      info: "ℹ",
    };

    toast.innerHTML = `
      <div class="toast-icon">${icons[type]}</div>
      <div class="toast-message">${message}</div>
      <button class="toast-close" aria-label="Close">&times;</button>
    `;

    // Close button
    const closeBtn = toast.querySelector(".toast-close");
    closeBtn.addEventListener("click", () => this.dismiss(id));

    // Add to container
    this.container.appendChild(toast);

    // Trigger animation
    requestAnimationFrame(() => {
      toast.classList.add("toast-show");
    });

    // Store reference
    this.toasts.push({ id, element: toast, type });

    // Auto-dismiss
    if (duration > 0) {
      setTimeout(() => this.dismiss(id), duration);
    }

    return id;
  }

  /**
   * Dismiss a toast
   */
  dismiss(id) {
    const toast = this.toasts.find((t) => t.id === id);
    if (!toast) return;

    // Fade out animation
    toast.element.classList.remove("toast-show");
    toast.element.classList.add("toast-hide");

    // Remove after animation
    setTimeout(() => {
      if (toast.element.parentNode) {
        toast.element.parentNode.removeChild(toast.element);
      }
      this.toasts = this.toasts.filter((t) => t.id !== id);
    }, 300);
  }

  /**
   * Convenience methods
   */
  success(message, duration) {
    return this.show(message, "success", duration);
  }

  error(message, duration = 6000) {
    return this.show(message, "error", duration);
  }

  warning(message, duration) {
    return this.show(message, "warning", duration);
  }

  info(message, duration) {
    return this.show(message, "info", duration);
  }
}

// ============================================================================
// SECTION 2: Export Singleton
// ============================================================================

export const toast = new ToastManager();
```

**Add toast styles to `backend/static/css/components.css`:**

```css
/* =========================================================================
   TOAST NOTIFICATIONS
   ========================================================================= */

.toast-container {
  position: fixed;
  top: var(--spacing-6);
  right: var(--spacing-6);
  z-index: var(--z-tooltip);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-3);
  max-width: 400px;
}

.toast {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  padding: var(--spacing-4);
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);

  /* Animation */
  transform: translateX(120%);
  opacity: 0;
  transition: all var(--transition-base);
}

.toast-show {
  transform: translateX(0);
  opacity: 1;
}

.toast-hide {
  transform: translateX(120%);
  opacity: 0;
}

.toast-icon {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toast-message {
  flex: 1;
  font-size: var(--font-size-sm);
  color: var(--text-primary);
}

.toast-close {
  background: none;
  border: none;
  font-size: var(--font-size-xl);
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}

.toast-close:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

/* Toast variants */
.toast-success {
  border-left: 4px solid var(--status-success);
}

.toast-success .toast-icon {
  color: var(--status-success);
}

.toast-error {
  border-left: 4px solid var(--status-danger);
}

.toast-error .toast-icon {
  color: var(--status-danger);
}

.toast-warning {
  border-left: 4px solid var(--status-warning);
}

.toast-warning .toast-icon {
  color: var(--status-warning);
}

.toast-info {
  border-left: 4px solid var(--status-info);
}

.toast-info .toast-icon {
  color: var(--status-info);
}

/* Responsive */
@media (max-width: 768px) {
  .toast-container {
    right: var(--spacing-4);
    left: var(--spacing-4);
    max-width: none;
  }
}
```

---

### 4.4: Add Search, Filter, Sort UI

**Update `backend/static/index.html` - replace the file list section:**

```html
<!-- File List Section -->
<section>
  <h2>File Dashboard</h2>

  <!-- Controls -->
  <div class="file-controls">
    <!-- Search -->
    <div
      class="form-group"
      style="margin-bottom: 0; flex: 1; min-width: 200px;"
    >
      <input
        type="search"
        id="file-search"
        placeholder="Search files..."
        class="search-input"
      />
    </div>

    <!-- Status Filter -->
    <div class="form-group" style="margin-bottom: 0; min-width: 150px;">
      <select id="status-filter" class="filter-select">
        <option value="all">All Files</option>
        <option value="available">Available Only</option>
        <option value="checked_out">Locked Only</option>
      </select>
    </div>

    <!-- Sort -->
    <div class="form-group" style="margin-bottom: 0; min-width: 150px;">
      <select id="sort-select" class="filter-select">
        <option value="name-asc">Name (A→Z)</option>
        <option value="name-desc">Name (Z→A)</option>
        <option value="size-desc">Size (Largest)</option>
        <option value="size-asc">Size (Smallest)</option>
        <option value="status-asc">Status (A→Z)</option>
      </select>
    </div>
  </div>

  <!-- Results info -->
  <div id="results-info" class="results-info"></div>

  <!-- Loading state -->
  <div id="loading-indicator" class="loading">
    <p>Loading files...</p>
  </div>

  <!-- File list container -->
  <div id="file-list"></div>
</section>
```

**Add control styles to `backend/static/css/components.css`:**

```css
/* =========================================================================
   FILE CONTROLS
   ========================================================================= */

.file-controls {
  display: flex;
  gap: var(--spacing-4);
  margin-bottom: var(--spacing-6);
  flex-wrap: wrap;
}

.search-input {
  width: 100%;
}

.filter-select {
  width: 100%;
}

.results-info {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-4);
  padding: var(--spacing-2) 0;
}

/* Enhanced file item with selection state */
.file-item.selected {
  border-color: var(--interactive-primary);
  background: var(--interactive-primary-alpha);
  transform: translateX(5px);
}
```

---

### 4.5: Update Main Application

**Update `backend/static/js/app.js`:**

```javascript
/**
 * Main Application - Now with centralized state
 */

import { themeManager } from "./modules/theme-manager.js";
import { apiClient } from "./modules/api-client.js";
import { ModalManager } from "./modules/modal-manager.js";
import { store } from "./modules/store.js";
import { toast } from "./modules/toast.js";

// ============================================================================
// SECTION 1: Modal Instances
// ============================================================================

const checkoutModal = new ModalManager("checkout-modal");
const checkinModal = new ModalManager("checkin-modal");

let currentFilename = null;

// ============================================================================
// SECTION 2: Data Loading
// ============================================================================

async function loadFiles() {
  store.setLoading();

  try {
    const data = await apiClient.getFiles();
    store.setFiles(data.files);
  } catch (error) {
    store.setError(error.message);
    toast.error(`Failed to load files: ${error.message}`);
  }
}

// ============================================================================
// SECTION 3: Main Render Function
// ============================================================================

/**
 * Render the entire UI based on current state
 * Called automatically whenever state changes
 */
function render(state) {
  const loadingEl = document.getElementById("loading-indicator");
  const fileListEl = document.getElementById("file-list");
  const resultsInfo = document.getElementById("results-info");

  // Show/hide loading
  if (state.isLoading) {
    loadingEl.classList.remove("hidden");
    fileListEl.innerHTML = "";
    resultsInfo.textContent = "";
    return;
  }

  loadingEl.classList.add("hidden");

  // Handle error state
  if (state.error) {
    fileListEl.innerHTML = `
      <div style="text-align: center; padding: 2rem; color: var(--status-danger-text);">
        <p><strong>Error:</strong> ${state.error}</p>
        <button class="btn btn-primary" onclick="location.reload()">
          Retry
        </button>
      </div>
    `;
    return;
  }

  // Get filtered and sorted files
  const displayFiles = store.getDisplayFiles();

  // Update results info
  const totalFiles = state.allFiles.length;
  const filteredCount = displayFiles.length;

  if (state.searchTerm || state.statusFilter !== "all") {
    resultsInfo.textContent = `Showing ${filteredCount} of ${totalFiles} files`;
  } else {
    resultsInfo.textContent = `${totalFiles} file${
      totalFiles !== 1 ? "s" : ""
    }`;
  }

  // Render files
  renderFileList(displayFiles, state.selectedFile);
}

/**
 * Render file list
 */
function renderFileList(files, selectedFile) {
  const container = document.getElementById("file-list");
  container.innerHTML = "";

  if (files.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
        <p>No files match your search.</p>
      </div>
    `;
    return;
  }

  files.forEach((file) => {
    const element = createFileElement(file, selectedFile);
    container.appendChild(element);
  });
}

/**
 * Create file element
 */
function createFileElement(file, selectedFile) {
  const div = document.createElement("div");
  div.className = "file-item";

  // Add selected class
  if (selectedFile && selectedFile.name === file.name) {
    div.classList.add("selected");
  }

  // Click to select
  div.addEventListener("click", (e) => {
    // Don't select if clicking button
    if (e.target.tagName !== "BUTTON") {
      store.setSelectedFile(file);
    }
  });

  const infoDiv = document.createElement("div");
  infoDiv.className = "file-info";

  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ").toUpperCase();

  // Size display
  const sizeSpan = document.createElement("span");
  sizeSpan.style.fontSize = "var(--font-size-sm)";
  sizeSpan.style.color = "var(--text-secondary)";
  sizeSpan.textContent = formatBytes(file.size_bytes);

  infoDiv.appendChild(nameSpan);
  infoDiv.appendChild(statusSpan);
  infoDiv.appendChild(sizeSpan);

  const actionsDiv = document.createElement("div");
  actionsDiv.className = "file-actions";

  if (file.status === "available") {
    const checkoutBtn = document.createElement("button");
    checkoutBtn.className = "btn btn-primary btn-sm";
    checkoutBtn.textContent = "Checkout";
    checkoutBtn.onclick = (e) => {
      e.stopPropagation();
      handleCheckout(file.name);
    };
    actionsDiv.appendChild(checkoutBtn);
  } else {
    const checkinBtn = document.createElement("button");
    checkinBtn.className = "btn btn-secondary btn-sm";
    checkinBtn.textContent = "Checkin";
    checkinBtn.onclick = (e) => {
      e.stopPropagation();
      handleCheckin(file.name);
    };
    actionsDiv.appendChild(checkinBtn);

    if (file.locked_by) {
      const lockedBySpan = document.createElement("span");
      lockedBySpan.style.fontSize = "var(--font-size-sm)";
      lockedBySpan.style.color = "var(--text-secondary)";
      lockedBySpan.textContent = `Locked by: ${file.locked_by}`;
      actionsDiv.appendChild(lockedBySpan);
    }
  }

  div.appendChild(infoDiv);
  div.appendChild(actionsDiv);

  return div;
}

// ============================================================================
// SECTION 4: Event Handlers
// ============================================================================

function handleCheckout(filename) {
  currentFilename = filename;
  document.getElementById("checkout-filename").textContent = filename;
  checkoutModal.open();
}

function handleCheckin(filename) {
  currentFilename = filename;
  document.getElementById("checkin-filename").textContent = filename;
  checkinModal.open();
}

async function submitCheckout(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const data = {
    filename: currentFilename,
    user: formData.get("user"),
    message: formData.get("message"),
  };

  try {
    await apiClient.post("/api/files/checkout", data);

    toast.success(`Successfully checked out ${currentFilename}`);
    checkoutModal.close();
    loadFiles();
  } catch (error) {
    toast.error(error.message);
  }
}

async function submitCheckin(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const data = {
    filename: currentFilename,
    user: formData.get("user"),
  };

  try {
    await apiClient.post("/api/files/checkin", data);

    toast.success(`Successfully checked in ${currentFilename}`);
    checkinModal.close();
    loadFiles();
  } catch (error) {
    toast.error(error.message);
  }
}

// ============================================================================
// SECTION 5: Utility Functions
// ============================================================================

function formatBytes(bytes) {
  if (bytes === 0) return "0 Bytes";

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
}

// ============================================================================
// SECTION 6: Initialization
// ============================================================================

document.addEventListener("DOMContentLoaded", () => {
  console.log("PDM App initialized with centralized state");

  // Subscribe to store - render on every state change
  store.subscribe(render);

  // Theme toggle
  document
    .getElementById("theme-toggle")
    .addEventListener("click", () => themeManager.toggle());

  // Search input
  document.getElementById("file-search").addEventListener("input", (e) => {
    store.setSearchTerm(e.target.value);
  });

  // Status filter
  document.getElementById("status-filter").addEventListener("change", (e) => {
    store.setStatusFilter(e.target.value);
  });

  // Sort selector
  document.getElementById("sort-select").addEventListener("change", (e) => {
    store.setSortBy(e.target.value);
  });

  // Form submissions
  document
    .getElementById("checkout-form")
    .addEventListener("submit", submitCheckout);

  document
    .getElementById("checkin-form")
    .addEventListener("submit", submitCheckin);

  // Load initial data
  loadFiles();
});
```

---

### Stage 4 Complete

**Test all features:**

```bash
uvicorn app.main:app --reload
```

**You should now have:**

1. **Search**: Type in search box, files filter instantly
2. **Status filter**: Select "Available Only" or "Locked Only"
3. **Sort**: Sort by name or size, ascending/descending
4. **Toast notifications**: Success/error messages in top-right
5. **File selection**: Click file to highlight it
6. **Results info**: Shows "Showing X of Y files"
7. **Smooth animations**: All state changes animated
8. **No page refreshes**: Everything updates in real-time

**File structure:**

```
backend/
├── static/
│   └── js/
│       └── modules/
│           ├── store.js                    ## NEW
│           ├── toast.js                    ## NEW
│           └── learn_state_management.js   ## NEW
```

**What you learned:**

- State management patterns (Observer/Pub-Sub)
- Computed properties (derived state)
- Toast notification systems
- Search/filter/sort algorithms
- Reactive UI updates
- Performance optimization (no unnecessary renders)

**Verification:**

- [ ] Search works and filters files
- [ ] Status filter dropdown works
- [ ] Sort dropdown changes order
- [ ] Toast notifications appear on checkout/checkin
- [ ] File selection highlights
- [ ] All filters work together
- [ ] No console errors

Ready for Stage 5 (Authentication)?

## Stage 5: Authentication & Authorization

**Prerequisites**: Completed Stage 4

**Time**: 5-6 hours

**What you'll build**: Secure authentication system with JWT tokens, login/logout, password hashing, and protected API endpoints.

---

### 5.1: Deep Dive - Authentication vs Authorization

**File: `backend/app/learn_auth_concepts.py`**

```python
"""
Understanding Authentication and Authorization

These are two distinct security concepts that work together.
"""

## ============================================================================
## SECTION 1: Definitions
## ============================================================================

"""
AUTHENTICATION (AuthN): "Who are you?"
- Verifying identity
- Proving you are who you claim to be
- Examples: username/password, biometrics, 2FA

AUTHORIZATION (AuthZ): "What are you allowed to do?"
- Verifying permissions
- Checking if you have access to a resource
- Examples: admin role, file ownership, read/write permissions

Flow:
1. User provides credentials (username/password)
2. System authenticates (checks if credentials are valid)
3. System issues token/session (proof of authentication)
4. User requests protected resource
5. System authorizes (checks if user has permission)
6. Resource is granted or denied

You ALWAYS authenticate before you authorize.
You can be authenticated but not authorized.
"""

## ============================================================================
## SECTION 2: Password Storage - The Wrong Ways
## ============================================================================

"""
NEVER STORE PLAIN TEXT PASSWORDS

Bad Database:
| user_id | username | password  |
|---------|----------|-----------|
| 1       | alice    | secret123 |
| 2       | bob      | pass456   |

Problems:
1. Database breach = all passwords exposed
2. Admins can see passwords
3. Users reuse passwords across sites
"""

import hashlib

def bad_approach_1_plaintext():
    """Storing passwords in plain text - NEVER DO THIS"""
    password = "secret123"
    ## Stored directly in database
    return password  ## Anyone with DB access sees this

def bad_approach_2_simple_hash():
    """Using fast hash like MD5 or SHA256 - STILL BAD"""
    password = "secret123"
    hashed = hashlib.sha256(password.encode()).hexdigest()

    """
    Problems with fast hashes for passwords:

    1. TOO FAST
       - GPUs can compute billions of SHA256 hashes per second
       - Attacker can brute force common passwords quickly

    2. NO SALT
       - Same password = same hash
       - Rainbow tables (precomputed hashes) work
       - If two users have password "123456", hashes are identical

    3. DETERMINISTIC
       - Easy to verify if a password is common
       - Can build dictionary of common password hashes
    """
    return hashed

## ============================================================================
## SECTION 3: Password Storage - The Right Way
## ============================================================================

"""
CORRECT APPROACH: Key Derivation Functions (KDFs)

Requirements for password hashing:
1. SLOW - takes time to compute (defeats brute force)
2. SALTED - random salt added (defeats rainbow tables)
3. ADAPTIVE - can increase cost as computers get faster

Algorithms:
- bcrypt (good) - Our choice, battle-tested since 1999
- scrypt (better) - Memory-hard, resists GPU attacks
- Argon2 (best) - Winner of Password Hashing Competition 2015
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def correct_password_storage():
    """Using bcrypt with passlib"""
    password = "secret123"

    ## Hash password (automatically adds random salt)
    hashed = pwd_context.hash(password)
    print(f"Hashed: {hashed}")
    ## Output: $2b$12$randomsalt...actualhash
    ##         │  │  │
    ##         │  │  └─ Salt (random per password)
    ##         │  └──── Cost factor (12 = 2^12 iterations)
    ##         └─────── Algorithm identifier (bcrypt)

    ## Same password, different hash each time (different salt)
    hashed2 = pwd_context.hash(password)
    print(f"Same password, different hash: {hashed != hashed2}")

    ## Verify password
    is_correct = pwd_context.verify("secret123", hashed)
    print(f"Password correct: {is_correct}")

    is_wrong = pwd_context.verify("wrong", hashed)
    print(f"Wrong password: {is_wrong}")

    """
    Why bcrypt is secure:

    1. Cost Factor (12 = 2^12 = 4,096 iterations)
       - Deliberately slow: ~0.3 seconds per hash
       - This is GOOD for passwords
       - Attacker needs 0.3s per guess = 288 guesses/day

    2. Random Salt
       - Different users with same password get different hashes
       - Rainbow tables are useless
       - Must brute force each password individually

    3. Adaptive
       - Can increase cost factor as computers get faster
       - Currently 12 is good, in 2030 might use 15
    """

## ============================================================================
## SECTION 4: Session Management - Tokens vs Cookies
## ============================================================================

"""
Two approaches to "remember" authenticated users:

APPROACH 1: Server-Side Sessions (Traditional)
┌─────────┐                    ┌─────────┐
│ Browser │                    │ Server  │
└────┬────┘                    └────┬────┘
     │                              │
     │  1. Login (user/pass)        │
     ├──────────────────────────────>
     │                              │
     │  2. Create session in DB     │
     │     session_id = "abc123"    │
     │     user_id = 42             │
     │                              │
     │  3. Set cookie               │
     │<─────────────────────────────┤
     │  Set-Cookie: sid=abc123      │
     │                              │
     │  4. Request with cookie      │
     ├──────────────────────────────>
     │  Cookie: sid=abc123          │
     │                              │
     │  5. Lookup session in DB     │
     │     Find user_id = 42        │
     │                              │

Pros:
- Can revoke sessions immediately (delete from DB)
- Server has full control

Cons:
- Requires database lookup on every request
- Doesn't scale horizontally (session tied to one server)
- Complex with load balancers


APPROACH 2: JSON Web Tokens (JWT) - Stateless
┌─────────┐                    ┌─────────┐
│ Browser │                    │ Server  │
└────┬────┘                    └────┬────┘
     │                              │
     │  1. Login (user/pass)        │
     ├──────────────────────────────>
     │                              │
     │  2. Create JWT               │
     │     Sign with secret key     │
     │     {user_id: 42, role: user}│
     │                              │
     │  3. Return JWT               │
     │<─────────────────────────────┤
     │  {token: "eyJhbG..."}        │
     │                              │
     │  4. Request with JWT         │
     ├──────────────────────────────>
     │  Authorization: Bearer eyJ...│
     │                              │
     │  5. Verify signature         │
     │     No DB lookup needed      │
     │                              │

Pros:
- Stateless - no DB lookup on every request
- Scales horizontally (any server can verify)
- Works with microservices

Cons:
- Can't revoke immediately (must wait for expiration)
- Token contains data (larger than session ID)
- If secret key leaks, all tokens are compromised

We'll use JWT for scalability and simplicity.
"""

## ============================================================================
## SECTION 5: JWT Structure
## ============================================================================

"""
JWT = JSON Web Token

Structure: xxxxx.yyyyy.zzzzz
           │     │     │
           │     │     └─ SIGNATURE (proves authenticity)
           │     └─────── PAYLOAD (user data)
           └───────────── HEADER (metadata)

HEADER (Base64 encoded JSON):
{
  "alg": "HS256",     ## Algorithm
  "typ": "JWT"        ## Type
}

PAYLOAD (Base64 encoded JSON):
{
  "sub": "alice",     ## Subject (user identifier)
  "role": "admin",    ## Custom claims
  "exp": 1735689600   ## Expiration timestamp
}

SIGNATURE:
HMACSHA256(
  base64(header) + "." + base64(payload),
  secret_key
)

How verification works:
1. Server receives: header.payload.signature
2. Server recomputes: HMACSHA256(header.payload, secret_key)
3. Compare recomputed signature with received signature
4. If match: token is authentic, hasn't been tampered with
5. If no match: token is invalid, reject request

Key point: Signature proves token wasn't modified.
Anyone can READ a JWT (it's just base64, not encrypted).
But only server with secret key can CREATE valid signatures.
"""

import base64
import json

def decode_jwt_demo():
    """Demonstrate JWT structure"""
    ## Real JWT from our app
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZSIsInJvbGUiOiJ1c2VyIiwiZXhwIjoxNzM1Njg5NjAwfQ.signature"

    header, payload, signature = token.split('.')

    ## Decode header (add padding if needed)
    header_json = base64.urlsafe_b64decode(header + '==')
    print(f"Header: {header_json}")

    ## Decode payload
    payload_json = base64.urlsafe_b64decode(payload + '==')
    print(f"Payload: {payload_json}")

    print(f"Signature: {signature} (binary data, proves authenticity)")

    """
    Security note: JWTs are NOT encrypted, only signed.
    Don't put sensitive data in JWT payload.
    Anyone can decode and read it.
    """

if __name__ == "__main__":
    print("=== Password Hashing ===")
    correct_password_storage()

    print("\n=== JWT Demo ===")
    decode_jwt_demo()
```

Run it:

```bash
pip install passlib[bcrypt]
python -m app.learn_auth_concepts
```

---

### 5.2: Install Authentication Dependencies

```bash
pip install "passlib[bcrypt]" "python-jose[cryptography]" python-multipart
pip freeze > requirements.txt
```

**Why these packages:**

- `passlib[bcrypt]`: Password hashing
- `python-jose[cryptography]`: JWT creation/verification
- `python-multipart`: Required for OAuth2 password flow (form data)

---

### 5.3: Update Configuration

**Update `backend/app/config.py`:**

```python
"""
Application configuration.
"""

from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """Application settings."""

    ## ========================================================================
    ## Application Settings
    ## ========================================================================
    APP_NAME: str = "PDM Backend API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    ## ========================================================================
    ## Security Settings
    ## ========================================================================
    ## CRITICAL: Change this in production!
    ## Generate with: openssl rand -hex 32
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

    ## JWT Settings
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ## ========================================================================
    ## Path Configuration
    ## ========================================================================
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

**Create `.env` file for local overrides:**

```bash
## backend/.env
SECRET_KEY=your-super-secret-key-change-in-production
DEBUG=True
```

**Add to `.gitignore`:**

```
.env
```

---

### 5.4: Authentication Schemas

**File: `backend/app/schemas/auth.py`**

```python
"""
Pydantic schemas for authentication.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional

## ============================================================================
## SECTION 1: User Models
## ============================================================================

class User(BaseModel):
    """
    User model for API responses.
    Never includes password_hash.
    """
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str
    role: str = Field(..., description="User role: 'admin' or 'user'")

    class Config:
        schema_extra = {
            "example": {
                "username": "alice",
                "full_name": "Alice Smith",
                "role": "user"
            }
        }

class UserInDB(User):
    """
    User model as stored in database/file.
    Includes password_hash (never sent to client).
    """
    password_hash: str

class UserCreate(BaseModel):
    """Schema for creating new users."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: str
    role: str = "user"

    @validator('username')
    def username_alphanumeric(cls, v):
        """Username must be alphanumeric."""
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()

    @validator('password')
    def password_strength(cls, v):
        """Basic password strength validation."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if v.isdigit():
            raise ValueError('Password cannot be all numbers')
        if v.lower() == v:
            raise ValueError('Password must contain at least one uppercase letter')
        return v

## ============================================================================
## SECTION 2: Token Models
## ============================================================================

class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Data encoded in JWT token."""
    username: Optional[str] = None
    role: Optional[str] = None
```

**Update `backend/app/schemas/__init__.py`:**

```python
from app.schemas.files import (
    FileInfo,
    FileListResponse,
    FileCheckoutRequest,
    FileCheckinRequest
)
from app.schemas.auth import (
    User,
    UserInDB,
    UserCreate,
    Token,
    TokenData
)

__all__ = [
    ## Files
    "FileInfo",
    "FileListResponse",
    "FileCheckoutRequest",
    "FileCheckinRequest",
    ## Auth
    "User",
    "UserInDB",
    "UserCreate",
    "Token",
    "TokenData"
]
```

---

### 5.5: Authentication Service

**File: `backend/app/services/auth_service.py`**

```python
"""
Authentication service - handles password hashing and user management.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from pathlib import Path
import json

from passlib.context import CryptContext
from jose import JWTError, jwt

from app.config import settings
from app.schemas.auth import UserInDB, User
from app.utils.file_locking import LockedFile

## ============================================================================
## SECTION 1: Password Hashing
## ============================================================================

## Create password context for bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.

    Args:
        plain_password: Password to check
        hashed_password: Stored bcrypt hash

    Returns:
        True if password matches
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Bcrypt hash string
    """
    return pwd_context.hash(password)

## ============================================================================
## SECTION 2: JWT Token Management
## ============================================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary of claims to encode (e.g., {"sub": "username"})
        expires_delta: How long until token expires

    Returns:
        Encoded JWT string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    ## Add standard claims
    to_encode.update({"exp": expire})

    ## Encode and sign with secret key
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT token.

    Args:
        token: JWT string

    Returns:
        Decoded payload dict, or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None

## ============================================================================
## SECTION 3: User Management
## ============================================================================

class UserService:
    """Manages user data stored in JSON file."""

    def __init__(self, users_file: Path):
        self.users_file = users_file

        ## Ensure file exists
        if not self.users_file.exists():
            self.users_file.write_text('{}')

    def load_users(self) -> dict:
        """Load all users from file."""
        try:
            with LockedFile(self.users_file, 'r') as f:
                content = f.read()
                if not content.strip():
                    return {}
                return json.loads(content)
        except Exception:
            return {}

    def save_users(self, users: dict):
        """Save users to file."""
        with LockedFile(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)

    def get_user(self, username: str) -> Optional[UserInDB]:
        """
        Get user by username.

        Returns:
            UserInDB model or None if not found
        """
        users = self.load_users()
        user_data = users.get(username)

        if user_data:
            return UserInDB(**user_data)
        return None

    def create_user(self, username: str, password: str, full_name: str, role: str = "user"):
        """
        Create a new user.

        Raises:
            ValueError: If username already exists
        """
        users = self.load_users()

        if username in users:
            raise ValueError(f"Username '{username}' already exists")

        ## Hash password
        password_hash = get_password_hash(password)

        ## Add user
        users[username] = {
            "username": username,
            "password_hash": password_hash,
            "full_name": full_name,
            "role": role
        }

        self.save_users(users)

    def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        """
        Authenticate user with username and password.

        Returns:
            UserInDB if authentication successful, None otherwise
        """
        user = self.get_user(username)

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    def create_default_users(self):
        """Create default admin and test users."""
        users = self.load_users()

        ## Only create if no users exist
        if users:
            return

        ## Create admin user
        self.create_user(
            username="admin",
            password="Admin123!",
            full_name="Administrator",
            role="admin"
        )

        ## Create test user
        self.create_user(
            username="john",
            password="Password123!",
            full_name="John Doe",
            role="user"
        )
```

---

### 5.6: Authentication Dependencies

**File: `backend/app/api/deps.py`**

```python
"""
FastAPI dependencies for authentication and authorization.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from pathlib import Path

from app.schemas.auth import User, UserInDB
from app.services.auth_service import decode_access_token, UserService
from app.config import settings

## ============================================================================
## SECTION 1: OAuth2 Setup
## ============================================================================

## This tells FastAPI where to find the login endpoint
## and extracts the token from the "Authorization: Bearer <token>" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

## ============================================================================
## SECTION 2: Get Current User
## ============================================================================

def get_user_service() -> UserService:
    """Dependency that provides UserService instance."""
    users_file = settings.BASE_DIR / 'users.json'
    return UserService(users_file)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> User:
    """
    Dependency to get current authenticated user from JWT token.

    This is the main authentication dependency.
    Add it to any endpoint that requires authentication:

    @app.get("/protected")
    def protected_route(current_user: User = Depends(get_current_user)):
        return {"user": current_user.username}

    Raises:
        HTTPException 401: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    ## Decode token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    ## Extract username from token
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    ## Get user from storage
    user_in_db = user_service.get_user(username)
    if user_in_db is None:
        raise credentials_exception

    ## Return User model (without password_hash)
    return User(
        username=user_in_db.username,
        full_name=user_in_db.full_name,
        role=user_in_db.role
    )

## ============================================================================
## SECTION 3: Role-Based Authorization
## ============================================================================

def require_role(allowed_roles: list[str]):
    """
    Dependency factory for role-based authorization.

    Usage:
        require_admin = require_role(["admin"])

        @app.delete("/admin/files/{filename}")
        def delete_file(current_user: User = Depends(require_admin)):
            ...
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {allowed_roles}"
            )
        return current_user

    return role_checker

## Convenience aliases
require_admin = require_role(["admin"])
require_user = require_role(["admin", "user"])
```

---

### 5.7: Authentication API Routes

**File: `backend/app/api/auth.py`**

```python
"""
Authentication API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.schemas.auth import Token, User
from app.services.auth_service import UserService, create_access_token
from app.api.deps import get_user_service, get_current_user
from app.config import settings

## ============================================================================
## SECTION 1: Router Setup
## ============================================================================

router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"]
)

## ============================================================================
## SECTION 2: Login Endpoint
## ============================================================================

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    """
    OAuth2 compatible token login.

    Send form data (application/x-www-form-urlencoded):
    - username: your username
    - password: your password

    Returns JWT access token.
    """
    ## Authenticate user
    user = user_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    ## Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

## ============================================================================
## SECTION 3: User Info Endpoint
## ============================================================================

@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information.

    Requires authentication (Bearer token).
    """
    return current_user
```

**Update `backend/app/main.py` to include auth router:**

```python
## Add import
from app.api import files, auth

## In create_application(), after including files router:
app.include_router(auth.router)

## Add startup event to create default users
@app.on_event("startup")
async def startup_event():
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")

    ## Create default users
    from app.services.auth_service import UserService
    users_file = settings.BASE_DIR / 'users.json'
    user_service = UserService(users_file)
    user_service.create_default_users()
    print("Default users created (admin/Admin123!, john/Password123!)")
```

---

### 5.8: Protect API Endpoints

**Update `backend/app/api/files.py` to require authentication:**

```python
## Add import
from app.api.deps import get_current_user
from app.schemas.auth import User

## Update all endpoints to require authentication:

@router.get("/", response_model=FileListResponse)
def get_files(
    current_user: User = Depends(get_current_user),  ## ADD THIS
    file_service: FileService = Depends(get_file_service)
):
    """Get list of all files. Requires authentication."""
    ## ... rest of implementation

@router.post("/checkout")
def checkout_file(
    request: FileCheckoutRequest,
    current_user: User = Depends(get_current_user),  ## ADD THIS
    file_service: FileService = Depends(get_file_service)
):
    """Check out a file. Requires authentication."""
    ## Use current_user.username instead of request.user
    file_service.checkout_file(
        filename=request.filename,
        user=current_user.username,  ## FROM TOKEN
        message=request.message
    )
    ## ...

## Do the same for checkin_file and get_file
```

**Update checkout/checkin schemas to remove user field:**

**Update `backend/app/schemas/files.py`:**

```python
class FileCheckoutRequest(BaseModel):
    """Request body for checking out a file."""
    filename: str = Field(..., min_length=1)
    ## Remove user field - will come from JWT token
    message: str = Field(..., min_length=1, max_length=500)

class FileCheckinRequest(BaseModel):
    """Request body for checking in a file."""
    filename: str
    ## Remove user field - will come from JWT token
```

---

### 5.9: Frontend - Login Page

**File: `backend/static/login.html`:**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Login - PDM System</title>
    <link rel="stylesheet" href="/static/css/main.css" />

    <style>
      body {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background: linear-gradient(
          135deg,
          var(--color-primary-500),
          var(--color-primary-700)
        );
      }

      .login-card {
        background: var(--card-bg);
        padding: var(--spacing-8);
        border-radius: var(--card-border-radius);
        box-shadow: var(--shadow-xl);
        width: 90%;
        max-width: 400px;
        border: 1px solid var(--border-default);
      }

      .login-header {
        text-align: center;
        margin-bottom: var(--spacing-6);
      }

      .login-header h1 {
        color: var(--color-primary-500);
        margin-bottom: var(--spacing-2);
      }

      .error-message {
        background: var(--status-danger-bg);
        color: var(--status-danger-text);
        padding: var(--spacing-3);
        border-radius: var(--radius-base);
        margin-bottom: var(--spacing-4);
        font-size: var(--font-size-sm);
        display: none;
      }

      .error-message.show {
        display: block;
      }

      .demo-credentials {
        margin-top: var(--spacing-6);
        padding-top: var(--spacing-6);
        border-top: 1px solid var(--border-default);
        text-align: center;
        font-size: var(--font-size-sm);
        color: var(--text-secondary);
      }

      .demo-credentials code {
        font-size: var(--font-size-sm);
      }
    </style>
  </head>
  <body>
    <div class="login-card">
      <div class="login-header">
        <h1>PDM System</h1>
        <p>Parts Data Management</p>
      </div>

      <div id="error-message" class="error-message"></div>

      <form id="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            required
            autofocus
            autocomplete="username"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            required
            autocomplete="current-password"
          />
        </div>

        <button type="submit" class="btn btn-primary" style="width: 100%;">
          Login
        </button>
      </form>

      <div class="demo-credentials">
        <p><strong>Demo Credentials:</strong></p>
        <p>Admin: <code>admin</code> / <code>Admin123!</code></p>
        <p>User: <code>john</code> / <code>Password123!</code></p>
      </div>
    </div>

    <script type="module" src="/static/js/login.js"></script>
  </body>
</html>
```

**File: `backend/static/js/login.js`:**

```javascript
/**
 * Login Page Logic
 */

document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const errorDiv = document.getElementById("error-message");
  const submitBtn = e.target.querySelector('button[type="submit"]');

  // Clear previous error
  errorDiv.classList.remove("show");
  submitBtn.disabled = true;
  submitBtn.textContent = "Logging in...";

  try {
    // OAuth2 password flow requires form-encoded data
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

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Login failed");
    }

    // Store token
    localStorage.setItem("access_token", data.access_token);

    // Decode token to get user info (for UI purposes only)
    const payload = JSON.parse(atob(data.access_token.split(".")[1]));
    localStorage.setItem("username", payload.sub);
    localStorage.setItem("user_role", payload.role);

    // Redirect to main app
    window.location.href = "/";
  } catch (error) {
    errorDiv.textContent = error.message;
    errorDiv.classList.add("show");
    submitBtn.disabled = false;
    submitBtn.textContent = "Login";
  }
});
```

**Update `backend/app/main.py` to serve login page:**

```python
@app.get("/login", response_class=FileResponse)
async def serve_login():
    """Serve login page."""
    return FileResponse("static/login.html")
```

---

### 5.10: Frontend - Auth Guard

**Add auth guard to `backend/static/index.html` in `<head>`:**

```html
<script>
  // Auth guard - redirect to login if no token
  (function () {
    const token = localStorage.getItem("access_token");
    if (!token && window.location.pathname !== "/login") {
      window.location.href = "/login";
    }
  })();
</script>
```

---

### 5.11: Update API Client with Auth

**Update `backend/static/js/modules/api-client.js`:**

```javascript
/**
 * API Client with authentication support
 */

export class APIClient {
  constructor(baseURL = "") {
    this.baseURL = baseURL;
  }

  getToken() {
    return localStorage.getItem("access_token");
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;

    // Add auth header
    const token = this.getToken();
    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const config = {
      ...options,
      headers,
    };

    try {
      const response = await fetch(url, config);

      // Handle 401 - redirect to login
      if (response.status === 401) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("username");
        localStorage.removeItem("user_role");
        window.location.href = "/login";
        throw new Error("Session expired. Please login again.");
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `HTTP ${response.status}: ${response.statusText}`
        );
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  // ... rest of methods remain the same
}

export const apiClient = new APIClient();
```

**Update `backend/static/js/app.js` - add logout button:**

```javascript
// In DOMContentLoaded:

// Logout handler
const logoutBtn = document.createElement("button");
logoutBtn.className = "btn btn-secondary btn-sm";
logoutBtn.textContent = "Logout";
logoutBtn.onclick = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("username");
  localStorage.removeItem("user_role");
  window.location.href = "/login";
};

document.querySelector(".header-actions").appendChild(logoutBtn);

// Show username in header
const username = localStorage.getItem("username");
if (username) {
  const userSpan = document.createElement("span");
  userSpan.style.marginRight = "var(--spacing-3)";
  userSpan.style.color = "var(--text-inverse)";
  userSpan.textContent = `Logged in as: ${username}`;
  document.querySelector(".header-actions").prepend(userSpan);
}
```

**Update checkout form to not ask for username:**

**Update modals in `backend/static/index.html`:**

```html
<!-- Checkout Modal - remove user input -->
<div id="checkout-modal" class="modal-overlay hidden">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Check Out File</h3>
      <button class="modal-close" type="button">&times;</button>
    </div>

    <div class="modal-body">
      <p>You are checking out: <strong id="checkout-filename"></strong></p>

      <form id="checkout-form">
        <!-- Remove user input field -->

        <div class="form-group">
          <label for="checkout-message">Reason for checkout</label>
          <textarea
            id="checkout-message"
            name="message"
            required
            minlength="5"
            placeholder="Why are you editing this file?"
            rows="3"
          ></textarea>
        </div>

        <div class="modal-actions">
          <button
            type="button"
            class="btn btn-secondary"
            onclick="checkoutModal.close()"
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-primary">
            Confirm Checkout
          </button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Checkin Modal - remove user input -->
<div id="checkin-modal" class="modal-overlay hidden">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Check In File</h3>
      <button class="modal-close" type="button">&times;</button>
    </div>

    <div class="modal-body">
      <p>You are checking in: <strong id="checkin-filename"></strong></p>
      <p style="font-size: var(--font-size-sm); color: var(--text-secondary);">
        As: <strong id="checkin-username"></strong>
      </p>

      <form id="checkin-form">
        <div class="modal-actions">
          <button
            type="button"
            class="btn btn-secondary"
            onclick="checkinModal.close()"
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-primary">
            Confirm Check-in
          </button>
        </div>
      </form>
    </div>
  </div>
</div>
```

**Update app.js form handlers:**

```javascript
async function submitCheckout(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const data = {
    filename: currentFilename,
    message: formData.get("message"),
    // User comes from JWT token
  };

  try {
    await apiClient.post("/api/files/checkout", data);
    toast.success(`Successfully checked out ${currentFilename}`);
    checkoutModal.close();
    loadFiles();
  } catch (error) {
    toast.error(error.message);
  }
}

async function submitCheckin(event) {
  event.preventDefault();

  const data = {
    filename: currentFilename,
    // User comes from JWT token
  };

  try {
    await apiClient.post("/api/files/checkin", data);
    toast.success(`Successfully checked in ${currentFilename}`);
    checkinModal.close();
    loadFiles();
  } catch (error) {
    toast.error(error.message);
  }
}

function handleCheckin(filename) {
  currentFilename = filename;
  document.getElementById("checkin-filename").textContent = filename;
  document.getElementById("checkin-username").textContent =
    localStorage.getItem("username");
  checkinModal.open();
}
```

---

### Stage 5 Complete

**Test the complete auth flow:**

```bash
uvicorn app.main:app --reload
```

1. Visit http://127.0.0.1:8000
2. Should redirect to login page
3. Login with `admin` / `Admin123!`
4. Should redirect to main app
5. See username in header
6. Check out a file (no username prompt)
7. Check in file
8. Click logout
9. Should redirect back to login

**File structure:**

```
backend/
├── app/
│   ├── services/
│   │   └── auth_service.py          ## NEW
│   ├── schemas/
│   │   └── auth.py                  ## NEW
│   ├── api/
│   │   ├── deps.py                  ## NEW
│   │   └── auth.py                  ## NEW
│   └── learn_auth_concepts.py       ## NEW
├── static/
│   ├── login.html                   ## NEW
│   └── js/
│       └── login.js                 ## NEW
└── users.json                       ## Auto-created
```

**What you learned:**

- Password hashing with bcrypt
- JWT token creation and verification
- OAuth2 password flow
- Protected API endpoints
- Authentication vs Authorization
- Role-based access control foundations
- Session management with tokens
- Secure credential handling

Ready for Stage 6 (Advanced Authorization)?

## Stage 6: Advanced Authorization & Audit System

**Prerequisites**: Completed Stage 5

**Time**: 4-5 hours

**What you'll build**: Role-based access control, ownership validation, audit logging, and admin dashboard.

---

### 6.1: Deep Dive - Authorization Patterns

**File: `backend/app/learn_authorization.py`**

```python
"""
Understanding Authorization Patterns

Authorization answers: "What can this user do?"
After authentication proves identity, authorization grants/denies access.
"""

## ============================================================================
## SECTION 1: Authorization Models
## ============================================================================

"""
AUTHORIZATION MODEL 1: Role-Based Access Control (RBAC)

Users are assigned roles, roles have permissions.

Example:
┌──────────┐
│  User    │──has──> Role ──has──> Permissions
└──────────┘
   Alice           Admin        - Create users
   Bob             User         - Edit files
   Carol           Guest        - View files

Pros:
- Simple to understand and implement
- Easy to manage (change role = change permissions)
- Most common in business applications

Cons:
- Can become complex with many roles
- Doesn't handle exceptions well (Bob can edit ALL files?)
- Role explosion (Admin, SuperAdmin, Editor, Viewer, etc.)
"""

class RBACExample:
    """Simple RBAC implementation"""

    PERMISSIONS = {
        'admin': [
            'read_files',
            'write_files',
            'delete_files',
            'manage_users',
            'view_audit_logs'
        ],
        'user': [
            'read_files',
            'write_files'
        ],
        'guest': [
            'read_files'
        ]
    }

    def has_permission(self, user_role: str, permission: str) -> bool:
        """Check if role has permission"""
        return permission in self.PERMISSIONS.get(user_role, [])

"""
AUTHORIZATION MODEL 2: Attribute-Based Access Control (ABAC)

Access based on attributes of user, resource, and environment.

Example Rules:
- Users can edit files they created
- Users can view files in their department
- Users can approve during business hours if they're managers

Attributes:
- User attributes: role, department, location, clearance_level
- Resource attributes: owner, sensitivity, department
- Environment: time, location, IP address

Pros:
- Very flexible
- Fine-grained control
- Handles exceptions naturally

Cons:
- Complex to implement
- Harder to audit ("why can Alice access this?")
- Performance overhead evaluating rules
"""

class ABACExample:
    """Simple ABAC implementation"""

    def can_edit_file(self, user, file, environment):
        """
        Attribute-based decision
        """
        ## Rule 1: Owner can always edit
        if file.owner == user.id:
            return True

        ## Rule 2: Admin can edit everything
        if user.role == 'admin':
            return True

        ## Rule 3: Same department can edit during business hours
        if (user.department == file.department and
            environment.is_business_hours()):
            return True

        return False

"""
AUTHORIZATION MODEL 3: Resource-Based / Ownership

Simple model: Users can only modify resources they own.

Our PDM app uses this:
- Users can checkout any available file
- Users can ONLY checkin files THEY checked out

Pros:
- Simple and intuitive
- Natural for many applications
- Easy to audit

Cons:
- Needs RBAC for admin overrides
- Doesn't handle shared ownership well
"""

class OwnershipExample:
    """Resource ownership model"""

    def can_checkin_file(self, user, file_lock):
        """User can only checkin their own files"""
        if user.role == 'admin':
            return True  ## Admin override

        return file_lock.owner == user.username

"""
OUR APPROACH: Hybrid RBAC + Ownership

- RBAC for high-level permissions (admin vs user)
- Ownership for file operations (checkin your own files)
- Admin role can override ownership

Best of both worlds for our use case.
"""

## ============================================================================
## SECTION 2: Common Authorization Anti-Patterns
## ============================================================================

"""
ANTI-PATTERN 1: Client-Side Authorization

BAD:
    Frontend: if (user.role === 'admin') { showDeleteButton() }
    Backend: No checks

Problem: User can call API directly, bypass frontend.

CORRECT:
    Frontend: UI hints (show/hide buttons)
    Backend: ALWAYS validate permissions
"""

"""
ANTI-PATTERN 2: Insecure Direct Object Reference (IDOR)

BAD:
    DELETE /api/files/123
    ## No check if user owns file 123

Problem: User can delete any file by guessing IDs.

CORRECT:
    DELETE /api/files/123
    ## Check: current_user owns file 123 OR is admin
"""

"""
ANTI-PATTERN 3: Privilege Escalation via Parameter Tampering

BAD:
    POST /api/users
    { "username": "alice", "role": "admin" }
    ## No check on role parameter

Problem: Any user can make themselves admin.

CORRECT:
    POST /api/users
    ## Only admins can set role
    ## OR ignore role parameter from non-admins
"""

## ============================================================================
## SECTION 3: Defense in Depth
## ============================================================================

"""
Security Principle: Defense in Depth

Multiple layers of security:

Layer 1: Authentication
- Is user logged in? Valid token?

Layer 2: Authorization
- Does user have permission for this action?

Layer 3: Resource Validation
- Does resource exist?
- Does user own resource (if applicable)?

Layer 4: Input Validation
- Is data properly formatted?
- No injection attacks?

Layer 5: Audit Logging
- Log all sensitive operations
- Can investigate breaches

Example flow for checkin:
1. Authenticate: Valid JWT token? ✓
2. Authorize: User role allows checkin? ✓
3. Validate: File is locked? ✓
4. Ownership: User owns this lock? ✓
5. Log: Record checkin action ✓
6. Execute: Release lock ✓

If ANY layer fails, reject request.
"""

if __name__ == "__main__":
    print("Authorization patterns explained.")

    ## Demo RBAC
    rbac = RBACExample()
    print(f"\nCan admin delete? {rbac.has_permission('admin', 'delete_files')}")
    print(f"Can user delete? {rbac.has_permission('user', 'delete_files')}")
```

Run it:

```bash
python -m app.learn_authorization
```

---

### 6.2: Enhanced Lock Management with Ownership

**Update `backend/app/services/file_service.py` - add audit logging:**

```python
"""
File management with ownership validation and audit logging.
"""

from pathlib import Path
from typing import List, Dict, Optional
import json
import logging
from datetime import datetime, timezone

from app.utils.file_locking import LockedFile

logger = logging.getLogger(__name__)

## ============================================================================
## SECTION 1: Audit Logger
## ============================================================================

class AuditLogger:
    """
    Records all file operations for security and compliance.
    """

    def __init__(self, audit_file: Path):
        self.audit_file = audit_file

        ## Ensure file exists
        if not self.audit_file.exists():
            self.audit_file.write_text('[]')

    def log_action(
        self,
        action: str,
        filename: str,
        user: str,
        details: Optional[dict] = None,
        success: bool = True
    ):
        """
        Log an audit event.

        Args:
            action: Type of action (checkout, checkin, delete, etc.)
            filename: File affected
            user: User who performed action
            details: Additional context
            success: Whether action succeeded
        """
        try:
            ## Load existing logs
            with LockedFile(self.audit_file, 'r') as f:
                content = f.read()
                logs = json.loads(content) if content.strip() else []

            ## Create new log entry
            entry = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'action': action,
                'filename': filename,
                'user': user,
                'success': success,
                'details': details or {}
            }

            logs.append(entry)

            ## Save logs
            with LockedFile(self.audit_file, 'w') as f:
                json.dump(logs, f, indent=2)

            logger.info(f"AUDIT: {action} on {filename} by {user} - {'success' if success else 'failed'}")

        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")

    def get_logs(
        self,
        filename: Optional[str] = None,
        user: Optional[str] = None,
        action: Optional[str] = None,
        limit: int = 100
    ) -> List[dict]:
        """
        Query audit logs with filters.

        Args:
            filename: Filter by filename
            user: Filter by user
            action: Filter by action type
            limit: Maximum number of results

        Returns:
            List of matching audit entries
        """
        try:
            with LockedFile(self.audit_file, 'r') as f:
                content = f.read()
                logs = json.loads(content) if content.strip() else []

            ## Apply filters
            results = logs

            if filename:
                results = [log for log in results if log['filename'] == filename]

            if user:
                results = [log for log in results if log['user'] == user]

            if action:
                results = [log for log in results if log['action'] == action]

            ## Return most recent first, up to limit
            return list(reversed(results))[:limit]

        except Exception as e:
            logger.error(f"Failed to read audit logs: {e}")
            return []

## ============================================================================
## SECTION 2: Update LockManager with Ownership
## ============================================================================

class LockManager:
    """Manages file lock state with ownership validation."""

    def __init__(self, locks_file: Path):
        self.locks_file = locks_file

        if not self.locks_file.exists():
            self.locks_file.write_text('{}')

    def load_locks(self) -> Dict[str, dict]:
        """Load current lock state."""
        if not self.locks_file.exists():
            return {}

        try:
            with LockedFile(self.locks_file, 'r') as f:
                content = f.read()
                if not content.strip():
                    return {}
                return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse locks file: {e}")
            return {}
        except Exception as e:
            logger.error(f"Failed to load locks: {e}")
            return {}

    def save_locks(self, locks: dict):
        """Save lock state atomically."""
        try:
            with LockedFile(self.locks_file, 'w') as f:
                json.dump(locks, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save locks: {e}")
            raise

    def is_locked(self, filename: str) -> bool:
        """Check if file is locked."""
        locks = self.load_locks()
        return filename in locks

    def get_lock_info(self, filename: str) -> Optional[dict]:
        """Get lock information for a file."""
        locks = self.load_locks()
        return locks.get(filename)

    def is_locked_by_user(self, filename: str, user: str) -> bool:
        """
        Check if file is locked by specific user.

        Used for ownership validation.
        """
        lock_info = self.get_lock_info(filename)
        if not lock_info:
            return False
        return lock_info['user'] == user

    def acquire_lock(self, filename: str, user: str, message: str):
        """Acquire lock on a file."""
        locks = self.load_locks()

        if filename in locks:
            existing = locks[filename]
            raise ValueError(
                f"File already locked by {existing['user']}"
            )

        from datetime import datetime, timezone
        locks[filename] = {
            'user': user,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'message': message
        }

        self.save_locks(locks)
        logger.info(f"Lock acquired: {filename} by {user}")

    def release_lock(self, filename: str, user: str, is_admin: bool = False):
        """
        Release lock on a file.

        Args:
            filename: File to unlock
            user: User releasing lock
            is_admin: If True, bypass ownership check

        Raises:
            ValueError: If file not locked or wrong user
        """
        locks = self.load_locks()

        if filename not in locks:
            raise ValueError("File is not locked")

        ## Ownership check (unless admin override)
        if not is_admin and locks[filename]['user'] != user:
            raise ValueError(
                f"Lock owned by {locks[filename]['user']}, not {user}. "
                f"You can only checkin files you checked out."
            )

        del locks[filename]
        self.save_locks(locks)
        logger.info(f"Lock released: {filename} by {user}")

    def force_release(self, filename: str):
        """
        Force release a lock (admin only).

        Use case: User went on vacation and left file locked.
        """
        locks = self.load_locks()

        if filename not in locks:
            raise ValueError("File is not locked")

        del locks[filename]
        self.save_locks(locks)
        logger.warning(f"Lock force-released: {filename}")

## ============================================================================
## SECTION 3: Update FileRepository (no changes needed)
## ============================================================================

class FileRepository:
    """Manages file operations on the repository directory."""

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.repo_path.mkdir(parents=True, exist_ok=True)

    def list_files(self, extension: str = '.mcam') -> List[Dict]:
        """List all files in repository with metadata."""
        files = []

        try:
            for item in self.repo_path.iterdir():
                if not item.is_file():
                    continue
                if not item.name.lower().endswith(extension):
                    continue

                stat = item.stat()

                files.append({
                    'name': item.name,
                    'size_bytes': stat.st_size,
                    'modified': stat.st_mtime,
                })

        except Exception as e:
            logger.error(f"Error listing files: {e}")
            raise

        return files

    def file_exists(self, filename: str) -> bool:
        """Check if file exists in repository."""
        return (self.repo_path / filename).exists()

    def get_file_path(self, filename: str) -> Path:
        """Get full path to a file."""
        return self.repo_path / filename

    def read_file(self, filename: str) -> bytes:
        """Read file contents."""
        path = self.get_file_path(filename)
        return path.read_bytes()

    def write_file(self, filename: str, content: bytes):
        """Write file contents."""
        path = self.get_file_path(filename)
        path.write_bytes(content)

## ============================================================================
## SECTION 4: Update FileService with Audit Logging
## ============================================================================

class FileService:
    """High-level file management with audit logging."""

    def __init__(self, repo_path: Path, locks_file: Path, audit_file: Path):
        self.repository = FileRepository(repo_path)
        self.lock_manager = LockManager(locks_file)
        self.audit_logger = AuditLogger(audit_file)

    def get_files_with_status(self) -> List[Dict]:
        """Get all files with their lock status."""
        files = self.repository.list_files()
        locks = self.lock_manager.load_locks()

        result = []
        for file_info in files:
            filename = file_info['name']
            lock_info = locks.get(filename)

            result.append({
                'name': filename,
                'size_bytes': file_info['size_bytes'],
                'status': 'checked_out' if lock_info else 'available',
                'locked_by': lock_info['user'] if lock_info else None,
                'locked_at': lock_info.get('timestamp') if lock_info else None,
                'lock_message': lock_info.get('message') if lock_info else None,
            })

        return result

    def checkout_file(self, filename: str, user: str, message: str):
        """
        Check out a file for editing.

        Raises:
            ValueError: If file doesn't exist or is already locked
        """
        ## Verify file exists
        if not self.repository.file_exists(filename):
            self.audit_logger.log_action(
                'checkout', filename, user,
                details={'error': 'File not found'},
                success=False
            )
            raise ValueError(f"File not found: {filename}")

        try:
            ## Acquire lock
            self.lock_manager.acquire_lock(filename, user, message)

            ## Log success
            self.audit_logger.log_action(
                'checkout', filename, user,
                details={'message': message}
            )

        except ValueError as e:
            ## Log failure
            self.audit_logger.log_action(
                'checkout', filename, user,
                details={'error': str(e)},
                success=False
            )
            raise

    def checkin_file(self, filename: str, user: str, is_admin: bool = False):
        """
        Check in a file after editing.

        Args:
            filename: File to checkin
            user: User performing checkin
            is_admin: If True, bypass ownership check

        Raises:
            ValueError: If not locked or wrong user
        """
        try:
            ## Release lock (with ownership check)
            self.lock_manager.release_lock(filename, user, is_admin)

            ## Log success
            self.audit_logger.log_action(
                'checkin', filename, user,
                details={'admin_override': is_admin}
            )

        except ValueError as e:
            ## Log failure
            self.audit_logger.log_action(
                'checkin', filename, user,
                details={'error': str(e)},
                success=False
            )
            raise

    def force_checkin(self, filename: str, admin_user: str):
        """
        Force checkin a file (admin only).

        Use case: User is unavailable, need to release lock.
        """
        lock_info = self.lock_manager.get_lock_info(filename)
        if not lock_info:
            raise ValueError("File is not locked")

        original_user = lock_info['user']

        ## Force release
        self.lock_manager.force_release(filename)

        ## Log admin action
        self.audit_logger.log_action(
            'force_checkin', filename, admin_user,
            details={
                'original_user': original_user,
                'reason': 'Admin override'
            }
        )

    def get_audit_logs(
        self,
        filename: Optional[str] = None,
        user: Optional[str] = None,
        limit: int = 100
    ) -> List[dict]:
        """Get audit logs with optional filters."""
        return self.audit_logger.get_logs(filename, user, limit=limit)
```

---

### 6.3: Update Dependencies for Authorization

**Update `backend/app/api/deps.py`:**

```python
"""
FastAPI dependencies for authentication and authorization.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from pathlib import Path

from app.schemas.auth import User
from app.services.auth_service import decode_access_token, UserService
from app.services.file_service import FileService
from app.config import settings

## ============================================================================
## SECTION 1: OAuth2 Setup
## ============================================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

## ============================================================================
## SECTION 2: Service Dependencies
## ============================================================================

def get_user_service() -> UserService:
    """Dependency that provides UserService instance."""
    users_file = settings.BASE_DIR / 'users.json'
    return UserService(users_file)

def get_file_service() -> FileService:
    """Dependency that provides FileService instance."""
    repo_path = settings.BASE_DIR / 'repo'
    locks_file = settings.BASE_DIR / 'locks.json'
    audit_file = settings.BASE_DIR / 'audit.json'  ## NEW

    return FileService(repo_path, locks_file, audit_file)

## ============================================================================
## SECTION 3: Get Current User
## ============================================================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> User:
    """
    Dependency to get current authenticated user from JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user_in_db = user_service.get_user(username)
    if user_in_db is None:
        raise credentials_exception

    return User(
        username=user_in_db.username,
        full_name=user_in_db.full_name,
        role=user_in_db.role
    )

## ============================================================================
## SECTION 4: Role-Based Authorization
## ============================================================================

def require_role(allowed_roles: list[str]):
    """
    Dependency factory for role-based authorization.

    Usage:
        @app.delete("/admin/users/{username}")
        def delete_user(current_user: User = Depends(require_admin)):
            ...
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {allowed_roles}. You have: {current_user.role}"
            )
        return current_user

    return role_checker

## Convenience aliases
require_admin = require_role(["admin"])
require_user = require_role(["admin", "user"])

## ============================================================================
## SECTION 5: Resource Ownership Validation
## ============================================================================

def validate_file_ownership(
    filename: str,
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service)
) -> bool:
    """
    Validate that current user owns the lock on a file.

    Returns True if:
    - User owns the lock, OR
    - User is admin (can override)

    Raises 403 if user doesn't own lock and isn't admin.
    """
    lock_info = file_service.lock_manager.get_lock_info(filename)

    ## File not locked - no ownership issue
    if not lock_info:
        return True

    ## Admin can always proceed
    if current_user.role == 'admin':
        return True

    ## Check ownership
    if lock_info['user'] != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"File is locked by {lock_info['user']}. You can only checkin files you checked out."
        )

    return True
```

---

### 6.4: Update Files API with Authorization

**Update `backend/app/api/files.py`:**

```python
"""
File management API endpoints with authorization.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional

from app.schemas.files import (
    FileInfo,
    FileListResponse,
    FileCheckoutRequest,
    FileCheckinRequest
)
from app.schemas.auth import User
from app.services.file_service import FileService
from app.api.deps import (
    get_current_user,
    get_file_service,
    require_admin
)

## ============================================================================
## SECTION 1: Router Setup
## ============================================================================

router = APIRouter(
    prefix="/api/files",
    tags=["files"],
)

## ============================================================================
## SECTION 2: File Listing Endpoints
## ============================================================================

@router.get("/", response_model=FileListResponse)
def get_files(
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service)
):
    """
    Get list of all files with their lock status.

    Requires: Authentication (any role)
    """
    try:
        files = file_service.get_files_with_status()

        return FileListResponse(
            files=files,
            total=len(files)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list files: {str(e)}"
        )

@router.get("/{filename}", response_model=FileInfo)
def get_file(
    filename: str,
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service)
):
    """
    Get details for a specific file.

    Requires: Authentication (any role)
    """
    files = file_service.get_files_with_status()

    for file in files:
        if file['name'] == filename:
            return FileInfo(**file)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"File '{filename}' not found"
    )

## ============================================================================
## SECTION 3: Checkout/Checkin Endpoints
## ============================================================================

@router.post("/checkout")
def checkout_file(
    request: FileCheckoutRequest,
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service)
):
    """
    Check out a file for editing.

    Requires: Authentication (user or admin)
    Authorization: Any authenticated user can checkout available files
    """
    try:
        ## Use authenticated user's username
        file_service.checkout_file(
            filename=request.filename,
            user=current_user.username,
            message=request.message
        )

        return {
            "success": True,
            "message": f"File '{request.filename}' checked out successfully",
            "locked_by": current_user.username
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to checkout file: {str(e)}"
        )

@router.post("/checkin")
def checkin_file(
    request: FileCheckinRequest,
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service)
):
    """
    Check in a file after editing.

    Requires: Authentication
    Authorization: Can only checkin files YOU checked out (or admin override)
    """
    try:
        ## Checkin with ownership validation
        is_admin = current_user.role == 'admin'

        file_service.checkin_file(
            filename=request.filename,
            user=current_user.username,
            is_admin=is_admin
        )

        return {
            "success": True,
            "message": f"File '{request.filename}' checked in successfully"
        }

    except ValueError as e:
        ## Ownership error returns 403 Forbidden
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to checkin file: {str(e)}"
        )

## ============================================================================
## SECTION 4: Admin-Only Endpoints
## ============================================================================

@router.post("/admin/force-checkin/{filename}")
def force_checkin_file(
    filename: str,
    current_user: User = Depends(require_admin),
    file_service: FileService = Depends(get_file_service)
):
    """
    Force checkin a locked file (admin only).

    Requires: Admin role
    Use case: User unavailable, need to release lock
    """
    try:
        file_service.force_checkin(filename, current_user.username)

        return {
            "success": True,
            "message": f"File '{filename}' force-checked-in by admin"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to force checkin: {str(e)}"
        )

@router.get("/admin/audit-logs")
def get_audit_logs(
    filename: Optional[str] = None,
    user: Optional[str] = None,
    limit: int = 100,
    current_user: User = Depends(require_admin),
    file_service: FileService = Depends(get_file_service)
):
    """
    Get audit logs (admin only).

    Requires: Admin role

    Query parameters:
    - filename: Filter by filename
    - user: Filter by user
    - limit: Max results (default 100)
    """
    try:
        logs = file_service.get_audit_logs(filename, user, limit)

        return {
            "logs": logs,
            "count": len(logs)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch audit logs: {str(e)}"
        )
```

---

### 6.5: Admin Dashboard UI

**Add admin styles to `backend/static/css/components.css`:**

```css
/* =========================================================================
   ADMIN DASHBOARD
   ========================================================================= */

.admin-panel {
  background: var(--status-warning-bg);
  border: 2px solid var(--status-warning);
  border-radius: var(--radius-lg);
  padding: var(--spacing-6);
  margin-bottom: var(--spacing-6);
}

.admin-panel h3 {
  color: var(--status-warning-text);
  margin-bottom: var(--spacing-4);
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}

.admin-actions {
  display: flex;
  gap: var(--spacing-3);
  flex-wrap: wrap;
  margin-top: var(--spacing-4);
}

.audit-log-entry {
  padding: var(--spacing-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-3);
  background: var(--bg-secondary);
}

.audit-log-entry.failed {
  border-left: 4px solid var(--status-danger);
}

.audit-log-entry.success {
  border-left: 4px solid var(--status-success);
}

.audit-log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-2);
}

.audit-log-action {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.audit-log-time {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.audit-log-details {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.badge {
  display: inline-block;
  padding: var(--spacing-1) var(--spacing-2);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
}

.badge-admin {
  background: var(--status-danger-bg);
  color: var(--status-danger-text);
}

.badge-user {
  background: var(--status-info-bg);
  color: var(--status-info-text);
}
```

**Update `backend/static/index.html` - add admin panel:**

```html
<!-- After header, before main -->
<div id="admin-panel-container"></div>

<!-- Add before modals section -->

<!-- Audit Logs Modal -->
<div id="audit-modal" class="modal-overlay hidden">
  <div class="modal-content" style="max-width: 800px;">
    <div class="modal-header">
      <h3>Audit Logs</h3>
      <button class="modal-close" type="button">&times;</button>
    </div>

    <div class="modal-body">
      <div
        style="display: flex; gap: var(--spacing-3); margin-bottom: var(--spacing-4);"
      >
        <input
          type="text"
          id="audit-filename-filter"
          placeholder="Filter by filename"
          style="flex: 1;"
        />
        <input
          type="text"
          id="audit-user-filter"
          placeholder="Filter by user"
          style="flex: 1;"
        />
        <button class="btn btn-primary" id="audit-search-btn">Search</button>
      </div>

      <div
        id="audit-logs-container"
        style="max-height: 500px; overflow-y: auto;"
      >
        <!-- Audit logs will be inserted here -->
      </div>
    </div>
  </div>
</div>
```

---

### 6.6: Update Frontend for Admin Features

**Update `backend/static/js/modules/api-client.js` - add admin methods:**

```javascript
// Add these methods to APIClient class:

/**
 * Force checkin a file (admin only)
 */
async forceCheckin(filename) {
  return this.post(`/api/files/admin/force-checkin/${encodeURIComponent(filename)}`);
}

/**
 * Get audit logs (admin only)
 */
async getAuditLogs(params = {}) {
  const queryString = new URLSearchParams(params).toString();
  const endpoint = `/api/files/admin/audit-logs${queryString ? '?' + queryString : ''}`;
  return this.get(endpoint);
}
```

**Update `backend/static/js/app.js` - add admin features:**

```javascript
// Add after imports
import { ModalManager } from "./modules/modal-manager.js";

// Add modal instance
const auditModal = new ModalManager("audit-modal");

// ============================================================================
// SECTION: Admin Panel
// ============================================================================

function renderAdminPanel(userRole) {
  const container = document.getElementById("admin-panel-container");

  if (userRole !== "admin") {
    container.innerHTML = "";
    return;
  }

  container.innerHTML = `
    <div class="container" style="padding-top: var(--spacing-6);">
      <div class="admin-panel">
        <h3>
          ⚠️ Admin Panel
        </h3>
        <p style="margin-bottom: var(--spacing-4); color: var(--text-secondary);">
          You have administrative privileges. Use these powers responsibly.
        </p>
        <div class="admin-actions">
          <button class="btn btn-secondary btn-sm" id="view-audit-logs-btn">
            📋 View Audit Logs
          </button>
        </div>
      </div>
    </div>
  `;

  // Wire up button
  document
    .getElementById("view-audit-logs-btn")
    .addEventListener("click", showAuditLogs);
}

// ============================================================================
// SECTION: Audit Logs
// ============================================================================

async function showAuditLogs() {
  auditModal.open();
  loadAuditLogs();
}

async function loadAuditLogs(filename = null, user = null) {
  const container = document.getElementById("audit-logs-container");
  container.innerHTML =
    '<div class="loading"><p>Loading audit logs...</p></div>';

  try {
    const params = {};
    if (filename) params.filename = filename;
    if (user) params.user = user;
    params.limit = 50;

    const data = await apiClient.getAuditLogs(params);

    if (data.logs.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
          <p>No audit logs found.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = data.logs
      .map((log) => {
        const date = new Date(log.timestamp);
        const statusClass = log.success ? "success" : "failed";

        return `
        <div class="audit-log-entry ${statusClass}">
          <div class="audit-log-header">
            <div class="audit-log-action">
              ${log.action.toUpperCase()}: ${log.filename}
            </div>
            <div class="audit-log-time">
              ${date.toLocaleString()}
            </div>
          </div>
          <div class="audit-log-details">
            <strong>User:</strong> ${log.user} &nbsp;&nbsp;
            <strong>Status:</strong> ${log.success ? "✓ Success" : "✗ Failed"}
            ${
              log.details && Object.keys(log.details).length > 0
                ? `<br><strong>Details:</strong> ${JSON.stringify(log.details)}`
                : ""
            }
          </div>
        </div>
      `;
      })
      .join("");
  } catch (error) {
    container.innerHTML = `
      <div style="text-align: center; padding: 2rem; color: var(--status-danger-text);">
        <p><strong>Error loading audit logs:</strong></p>
        <p>${error.message}</p>
      </div>
    `;
  }
}

// ============================================================================
// SECTION: Enhanced File Actions with Admin Override
// ============================================================================

function createFileElement(file, selectedFile) {
  const div = document.createElement("div");
  div.className = "file-item";

  if (selectedFile && selectedFile.name === file.name) {
    div.classList.add("selected");
  }

  div.addEventListener("click", (e) => {
    if (e.target.tagName !== "BUTTON") {
      store.setSelectedFile(file);
    }
  });

  const infoDiv = document.createElement("div");
  infoDiv.className = "file-info";

  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ").toUpperCase();

  const sizeSpan = document.createElement("span");
  sizeSpan.style.fontSize = "var(--font-size-sm)";
  sizeSpan.style.color = "var(--text-secondary)";
  sizeSpan.textContent = formatBytes(file.size_bytes);

  infoDiv.appendChild(nameSpan);
  infoDiv.appendChild(statusSpan);
  infoDiv.appendChild(sizeSpan);

  const actionsDiv = document.createElement("div");
  actionsDiv.className = "file-actions";

  const userRole = localStorage.getItem("user_role");
  const username = localStorage.getItem("username");

  if (file.status === "available") {
    const checkoutBtn = document.createElement("button");
    checkoutBtn.className = "btn btn-primary btn-sm";
    checkoutBtn.textContent = "Checkout";
    checkoutBtn.onclick = (e) => {
      e.stopPropagation();
      handleCheckout(file.name);
    };
    actionsDiv.appendChild(checkoutBtn);
  } else {
    // Regular checkin button
    const checkinBtn = document.createElement("button");
    checkinBtn.className = "btn btn-secondary btn-sm";
    checkinBtn.textContent = "Checkin";
    checkinBtn.onclick = (e) => {
      e.stopPropagation();
      handleCheckin(file.name);
    };

    // Disable if not owner (unless admin)
    if (file.locked_by !== username && userRole !== "admin") {
      checkinBtn.disabled = true;
      checkinBtn.title = `Locked by ${file.locked_by}. Only they can checkin.`;
    }

    actionsDiv.appendChild(checkinBtn);

    // Admin force checkin
    if (userRole === "admin" && file.locked_by !== username) {
      const forceBtn = document.createElement("button");
      forceBtn.className = "btn btn-danger btn-sm";
      forceBtn.textContent = "🔓 Force Checkin";
      forceBtn.onclick = (e) => {
        e.stopPropagation();
        handleForceCheckin(file.name);
      };
      actionsDiv.appendChild(forceBtn);
    }

    if (file.locked_by) {
      const lockedBySpan = document.createElement("span");
      lockedBySpan.style.fontSize = "var(--font-size-sm)";
      lockedBySpan.style.color = "var(--text-secondary)";
      lockedBySpan.textContent = `Locked by: ${file.locked_by}`;
      actionsDiv.appendChild(lockedBySpan);
    }
  }

  div.appendChild(infoDiv);
  div.appendChild(actionsDiv);

  return div;
}

async function handleForceCheckin(filename) {
  if (
    !confirm(
      `⚠️ ADMIN ACTION\n\nForce checkin "${filename}"?\n\nThis will release the lock regardless of who owns it. This action will be logged.`
    )
  ) {
    return;
  }

  try {
    await apiClient.forceCheckin(filename);
    toast.success(`Admin force-checked-in ${filename}`);
    loadFiles();
  } catch (error) {
    toast.error(error.message);
  }
}

// ============================================================================
// SECTION: Update Initialization
// ============================================================================

document.addEventListener("DOMContentLoaded", () => {
  console.log("PDM App initialized with authorization");

  const userRole = localStorage.getItem("user_role");
  const username = localStorage.getItem("username");

  // Render admin panel if admin
  renderAdminPanel(userRole);

  // Subscribe to store
  store.subscribe(render);

  // Theme toggle
  document
    .getElementById("theme-toggle")
    .addEventListener("click", () => themeManager.toggle());

  // Show username and role badge in header
  if (username) {
    const userInfo = document.createElement("div");
    userInfo.style.display = "flex";
    userInfo.style.alignItems = "center";
    userInfo.style.gap = "var(--spacing-2)";
    userInfo.style.marginRight = "var(--spacing-3)";
    userInfo.style.color = "var(--text-inverse)";

    const badge = document.createElement("span");
    badge.className = `badge badge-${userRole}`;
    badge.textContent = userRole;

    userInfo.innerHTML = `<span>${username}</span>`;
    userInfo.appendChild(badge);

    document.querySelector(".header-actions").prepend(userInfo);
  }

  // Audit search button
  document.getElementById("audit-search-btn").addEventListener("click", () => {
    const filename = document.getElementById("audit-filename-filter").value;
    const user = document.getElementById("audit-user-filter").value;
    loadAuditLogs(filename || null, user || null);
  });

  // Logout button
  const logoutBtn = document.createElement("button");
  logoutBtn.className = "btn btn-secondary btn-sm";
  logoutBtn.textContent = "Logout";
  logoutBtn.onclick = () => {
    localStorage.clear();
    window.location.href = "/login";
  };
  document.querySelector(".header-actions").appendChild(logoutBtn);

  // Search, filters, sorts
  document
    .getElementById("file-search")
    .addEventListener("input", (e) => store.setSearchTerm(e.target.value));

  document
    .getElementById("status-filter")
    .addEventListener("change", (e) => store.setStatusFilter(e.target.value));

  document
    .getElementById("sort-select")
    .addEventListener("change", (e) => store.setSortBy(e.target.value));

  // Form submissions
  document
    .getElementById("checkout-form")
    .addEventListener("submit", submitCheckout);

  document
    .getElementById("checkin-form")
    .addEventListener("submit", submitCheckin);

  // Load initial data
  loadFiles();
});
```

---

### Stage 6 Complete

**Test all authorization features:**

```bash
uvicorn app.main:app --reload
```

**Test as regular user (john):**

1. Login as `john` / `Password123!`
2. Checkout a file
3. Try to checkin someone else's locked file → Should fail
4. Checkin your own file → Should succeed
5. No admin panel visible

**Test as admin:**

1. Login as `admin` / `Admin123!`
2. See admin panel at top
3. Checkout a file as admin
4. Login as john (different browser/incognito)
5. Try to checkin admin's file → Disabled button
6. Back to admin: Force checkin john's file → Should work
7. Click "View Audit Logs" → See all actions logged

**File structure:**

```
backend/
├── app/
│   ├── learn_authorization.py       ## NEW
│   ├── services/
│   │   └── file_service.py          ## UPDATED with audit
│   └── api/
│       ├── deps.py                  ## UPDATED
│       └── files.py                 ## UPDATED
├── static/
│   ├── css/
│   │   └── components.css           ## UPDATED admin styles
│   ├── js/
│   │   ├── modules/
│   │   │   └── api-client.js        ## UPDATED
│   │   └── app.js                   ## UPDATED
│   └── index.html                   ## UPDATED
└── audit.json                       ## Auto-created
```

**What you learned:**

- RBAC (Role-Based Access Control)
- Resource ownership validation
- Admin privilege escalation
- Audit logging for compliance
- Defense in depth security
- Authorization vs Authentication
- Admin override patterns
- Security best practices

**Verification:**

- [ ] Regular users can't checkin others' files
- [ ] Admin can force checkin any file
- [ ] Audit logs capture all actions
- [ ] Admin panel only visible to admins
- [ ] Authorization errors return 403 Forbidden
- [ ] All actions properly logged

Ready for Stage 7? (We could cover Git integration, WebSockets for real-time updates, or Docker deployment - let me know what you'd like next!)

## Stage 7: Version Control with Git Integration

**Prerequisites**: Completed Stage 6

**Time**: 5-6 hours

**What you'll build**: Full Git integration for version control, commit history, diff viewing, and rollback capabilities.

---

### 7.1: Deep Dive - Git Internals

**File: `backend/app/learn_git_internals.py`**

```python
"""
Understanding Git - How Version Control Actually Works

Git is NOT a file system - it's a content-addressable database
with a version control UI on top.
"""

import hashlib
import zlib

## ============================================================================
## SECTION 1: Git's Core Concept - Content Addressing
## ============================================================================

"""
Content Addressing = Using the content itself as the address/key

Traditional filesystem:
/path/to/file.txt → Read content

Git's approach:
hash(content) → Read content

Example:
Content: "Hello World"
SHA-1: 0x557db03de997c86a4a028e1ebd3a1ceb225be238
Store at: .git/objects/55/7db03de997c86a4a028e1ebd3a1ceb225be238

Why this is powerful:
1. Same content = same hash (automatic deduplication)
2. Any change = different hash (tamper detection)
3. Can reference content by hash forever
"""

def git_hash_object(content: bytes) -> str:
    """
    Compute Git's SHA-1 hash for content.

    Git's hash format: sha1("blob " + size + "\0" + content)
    """
    ## Git adds a header: "blob <size>\0"
    header = f"blob {len(content)}\0".encode()
    store = header + content

    ## Compute SHA-1
    sha1 = hashlib.sha1(store).hexdigest()
    return sha1

def demonstrate_content_addressing():
    """Show how Git hashes content"""

    ## Same content = same hash
    content1 = b"Hello World"
    content2 = b"Hello World"
    hash1 = git_hash_object(content1)
    hash2 = git_hash_object(content2)

    print(f"Content 1 hash: {hash1}")
    print(f"Content 2 hash: {hash2}")
    print(f"Hashes match: {hash1 == hash2}")

    ## Different content = different hash
    content3 = b"Hello World!"  ## Added exclamation
    hash3 = git_hash_object(content3)
    print(f"Content 3 hash: {hash3}")
    print(f"Changed content: {hash3 != hash1}")

## ============================================================================
## SECTION 2: Git Object Types
## ============================================================================

"""
Git stores 4 types of objects (all content-addressed):

1. BLOB (Binary Large Object)
   - Raw file content
   - No filename, no metadata
   - Just bytes

2. TREE
   - Directory listing
   - Maps filenames to blob/tree hashes
   - Like a directory snapshot

3. COMMIT
   - Points to a tree (project snapshot)
   - Points to parent commit(s)
   - Has author, message, timestamp

4. TAG (not covering today)
   - Named reference to a commit

Example structure:

commit a1b2c3
├─ tree d4e5f6
│  ├─ blob 123456 "file1.txt"
│  ├─ blob 789abc "file2.txt"
│  └─ tree def012
│     └─ blob 345678 "subdir/file3.txt"
├─ parent 987654
├─ author "Alice"
└─ message "Added file3"
"""

## ============================================================================
## SECTION 3: How Git Tracks Changes
## ============================================================================

"""
Git does NOT store deltas (differences between versions).
Git stores FULL SNAPSHOTS.

Version 1: "Hello World" (100 bytes)
Version 2: "Hello World!" (101 bytes)

Git stores BOTH complete files:
- blob abc123: "Hello World"
- blob def456: "Hello World!"

But Git compresses and packs objects, so actual disk usage is minimal.

Why snapshots vs deltas?

Snapshots (Git's approach):
✓ Fast checkout (just copy files)
✓ Simple branching (just copy references)
✓ Fast history traversal (each commit is complete)
✗ More storage (mitigated by compression)

Deltas (SVN's approach):
✓ Less storage
✗ Slow checkout (must replay all deltas)
✗ Complex branching
✗ Slow history (must compute deltas)
"""

## ============================================================================
## SECTION 4: How Commits Form a Chain
## ============================================================================

"""
Commits form a Directed Acyclic Graph (DAG):

A ← B ← C ← D (main)
     ↖ E ← F (feature-branch)

Each commit points to its parent(s):
- D.parent = C
- C.parent = B
- F.parent = E
- E.parent = B

HEAD is a pointer to current commit:
HEAD → main → D

When you commit:
1. Git creates new tree (snapshot of working directory)
2. Git creates new commit pointing to tree and parent
3. Git moves branch pointer forward

Before: HEAD → main → D
After:  HEAD → main → E (where E.parent = D)
"""

## ============================================================================
## SECTION 5: Working Directory, Staging Area, Repository
## ============================================================================

"""
Git has three "states" for files:

1. WORKING DIRECTORY (workspace)
   - Your actual files on disk
   - Can edit, modify, delete
   - Not tracked by Git until staged

2. STAGING AREA (index)
   - Prepared snapshot for next commit
   - "git add" moves files here
   - Acts as a draft commit

3. REPOSITORY (.git directory)
   - Committed history
   - Permanent (unless force-deleted)
   - "git commit" saves staging area here

Flow:
Working Dir → git add → Staging Area → git commit → Repository

Why staging area?

Allows partial commits:
- Edit 10 files
- Stage only 5 (git add file1 file2 ...)
- Commit those 5
- Continue working on other 5

This lets you create logical, focused commits.
"""

## ============================================================================
## SECTION 6: Branches Are Just Pointers
## ============================================================================

"""
A branch in Git is just a 41-byte file containing a commit hash.

.git/refs/heads/main:
  a1b2c3d4e5f6...

That's it. Creating a branch = creating a small file.
Switching branches = changing what file HEAD points to.

This is why Git branching is so fast - it's just pointer manipulation.

Traditional VCS (SVN):
  Branch = Copy entire codebase (expensive)

Git:
  Branch = Create 41-byte file (instant)
"""

## ============================================================================
## SECTION 7: What We'll Implement
## ============================================================================

"""
For our PDM system, we'll implement:

1. Repository initialization
   - Create .git structure
   - Initialize empty repo

2. File tracking
   - Add files to Git when checked out
   - Commit files when checked in

3. History viewing
   - List all commits
   - Show who changed what when

4. Diff viewing
   - Compare versions of files
   - Show what changed

5. Rollback
   - Revert to previous version
   - Safety mechanism for mistakes

We'll use GitPython library (wrapper around Git CLI).
"""

if __name__ == "__main__":
    print("=== Content Addressing Demo ===")
    demonstrate_content_addressing()

    print("\n=== Git Concepts Explained ===")
    print("Git is a content-addressable filesystem with version control UI.")
    print("Objects: blob (file), tree (directory), commit (snapshot + metadata)")
    print("Commits form a DAG, branches are pointers, HEAD is current position.")
```

Run it:

```bash
python -m app.learn_git_internals
```

---

### 7.2: Install Git Dependencies

```bash
pip install GitPython
pip freeze > requirements.txt

## Also ensure git is installed on system
## Windows: https://git-scm.com/download/win
## macOS: brew install git (usually pre-installed)
## Linux: sudo apt install git
```

**Verify Git installation:**

```bash
git --version
## Should output: git version 2.x.x
```

---

### 7.3: Update Configuration

**Update `backend/app/config.py`:**

```python
"""
Application configuration.
"""

from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """Application settings."""

    ## ========================================================================
    ## Application Settings
    ## ========================================================================
    APP_NAME: str = "PDM Backend API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    ## ========================================================================
    ## Security Settings
    ## ========================================================================
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ## ========================================================================
    ## Path Configuration
    ## ========================================================================
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    ## ========================================================================
    ## Git Settings
    ## ========================================================================
    GIT_REPO_PATH: Path = BASE_DIR / "git_repo"  ## NEW
    GIT_USER_NAME: str = "PDM System"            ## NEW
    GIT_USER_EMAIL: str = "pdm@example.com"      ## NEW

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

---

### 7.4: Git Service Layer

**File: `backend/app/services/git_service.py`**

```python
"""
Git integration service for version control.

Wraps GitPython to provide version control for PDM files.
"""

from pathlib import Path
from typing import List, Dict, Optional
import logging
from datetime import datetime, timezone

from git import Repo, Git, InvalidGitRepositoryError, GitCommandError
from git.exc import NoSuchPathError

from app.config import settings

logger = logging.getLogger(__name__)

## ============================================================================
## SECTION 1: Git Repository Manager
## ============================================================================

class GitService:
    """
    Manages Git repository for file versioning.

    Each file operation (checkout/checkin) creates a Git commit,
    providing complete audit trail and rollback capability.
    """

    def __init__(self, repo_path: Path):
        """
        Initialize Git service.

        Args:
            repo_path: Path to Git repository
        """
        self.repo_path = repo_path
        self.repo = None

        ## Ensure repository exists
        self._ensure_repo()

    def _ensure_repo(self):
        """
        Ensure Git repository exists, create if needed.
        """
        try:
            ## Try to open existing repo
            self.repo = Repo(self.repo_path)
            logger.info(f"Opened existing Git repository at {self.repo_path}")

        except (InvalidGitRepositoryError, NoSuchPathError):
            ## Create new repository
            logger.info(f"Creating new Git repository at {self.repo_path}")
            self.repo_path.mkdir(parents=True, exist_ok=True)
            self.repo = Repo.init(self.repo_path)

            ## Configure repo
            with self.repo.config_writer() as config:
                config.set_value("user", "name", settings.GIT_USER_NAME)
                config.set_value("user", "email", settings.GIT_USER_EMAIL)

            ## Create initial commit
            readme_path = self.repo_path / "README.md"
            readme_path.write_text("## PDM File Repository\n\nVersion controlled files.\n")

            self.repo.index.add(["README.md"])
            self.repo.index.commit(
                "Initial commit",
                author_date=datetime.now(timezone.utc).isoformat(),
                commit_date=datetime.now(timezone.utc).isoformat()
            )

            logger.info("Created initial commit")

    ## ========================================================================
    ## SECTION 2: File Operations
    ## ========================================================================

    def add_file(self, filename: str, content: bytes):
        """
        Add or update a file in the repository.

        Args:
            filename: Name of file
            content: File contents as bytes
        """
        file_path = self.repo_path / filename
        file_path.write_bytes(content)
        logger.info(f"Wrote file to repository: {filename}")

    def get_file_content(self, filename: str) -> bytes:
        """
        Get current content of a file.

        Args:
            filename: Name of file

        Returns:
            File contents as bytes

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        file_path = self.repo_path / filename

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {filename}")

        return file_path.read_bytes()

    def file_exists(self, filename: str) -> bool:
        """Check if file exists in repository."""
        return (self.repo_path / filename).exists()

    ## ========================================================================
    ## SECTION 3: Commit Operations
    ## ========================================================================

    def commit_file(
        self,
        filename: str,
        message: str,
        author_name: str,
        author_email: Optional[str] = None
    ) -> str:
        """
        Commit a file to version control.

        Args:
            filename: File to commit
            message: Commit message
            author_name: Name of person making commit
            author_email: Email (optional)

        Returns:
            Commit SHA hash

        Raises:
            ValueError: If file doesn't exist
        """
        if not self.file_exists(filename):
            raise ValueError(f"Cannot commit non-existent file: {filename}")

        try:
            ## Stage file
            self.repo.index.add([filename])

            ## Create commit
            author_email = author_email or f"{author_name}@pdm.local"

            commit = self.repo.index.commit(
                message,
                author=f"{author_name} <{author_email}>",
                author_date=datetime.now(timezone.utc).isoformat(),
                commit_date=datetime.now(timezone.utc).isoformat()
            )

            logger.info(f"Committed {filename}: {commit.hexsha[:8]}")
            return commit.hexsha

        except GitCommandError as e:
            logger.error(f"Git commit failed: {e}")
            raise ValueError(f"Failed to commit file: {e}")

    ## ========================================================================
    ## SECTION 4: History Queries
    ## ========================================================================

    def get_file_history(self, filename: str, limit: int = 50) -> List[Dict]:
        """
        Get commit history for a specific file.

        Args:
            filename: File to get history for
            limit: Maximum number of commits to return

        Returns:
            List of commit info dicts, newest first
        """
        try:
            commits = []

            ## Get commits that modified this file
            ## rev-list walks the commit graph
            for commit in self.repo.iter_commits(paths=filename, max_count=limit):
                commits.append({
                    'sha': commit.hexsha,
                    'short_sha': commit.hexsha[:8],
                    'message': commit.message.strip(),
                    'author': commit.author.name,
                    'author_email': commit.author.email,
                    'date': commit.committed_datetime.isoformat(),
                    'timestamp': commit.committed_date,
                })

            return commits

        except GitCommandError as e:
            logger.error(f"Failed to get file history: {e}")
            return []

    def get_all_commits(self, limit: int = 100) -> List[Dict]:
        """
        Get all commits in repository.

        Args:
            limit: Maximum number of commits

        Returns:
            List of commit info dicts, newest first
        """
        try:
            commits = []

            for commit in self.repo.iter_commits(max_count=limit):
                ## Get files changed in this commit
                changed_files = []
                if commit.parents:
                    ## Compare with parent to see what changed
                    parent = commit.parents[0]
                    diffs = parent.diff(commit)
                    changed_files = [d.a_path or d.b_path for d in diffs]
                else:
                    ## Initial commit - all files are new
                    changed_files = [item.path for item in commit.tree.traverse()]

                commits.append({
                    'sha': commit.hexsha,
                    'short_sha': commit.hexsha[:8],
                    'message': commit.message.strip(),
                    'author': commit.author.name,
                    'date': commit.committed_datetime.isoformat(),
                    'files': changed_files,
                    'stats': commit.stats.total,
                })

            return commits

        except Exception as e:
            logger.error(f"Failed to get commits: {e}")
            return []

    ## ========================================================================
    ## SECTION 5: Diff Operations
    ## ========================================================================

    def get_file_diff(self, filename: str, commit_sha: str) -> Dict:
        """
        Get diff for a file at a specific commit.

        Shows what changed in that commit.

        Args:
            filename: File to check
            commit_sha: Commit to examine

        Returns:
            Dict with diff information
        """
        try:
            commit = self.repo.commit(commit_sha)

            ## Get parent commit
            if not commit.parents:
                ## Initial commit - entire file is "new"
                return {
                    'type': 'added',
                    'content': self._get_file_at_commit(filename, commit_sha),
                    'diff': None
                }

            parent = commit.parents[0]

            ## Get diff between parent and this commit
            diffs = parent.diff(commit, paths=filename, create_patch=True)

            if not diffs:
                return {
                    'type': 'unchanged',
                    'diff': None
                }

            diff = diffs[0]

            return {
                'type': 'modified' if diff.a_path else 'added',
                'old_content': diff.a_blob.data_stream.read().decode('utf-8', errors='ignore') if diff.a_blob else None,
                'new_content': diff.b_blob.data_stream.read().decode('utf-8', errors='ignore') if diff.b_blob else None,
                'diff': diff.diff.decode('utf-8', errors='ignore'),
            }

        except Exception as e:
            logger.error(f"Failed to get diff: {e}")
            return {'type': 'error', 'error': str(e)}

    def _get_file_at_commit(self, filename: str, commit_sha: str) -> str:
        """Get file content at specific commit."""
        try:
            commit = self.repo.commit(commit_sha)
            blob = commit.tree / filename
            return blob.data_stream.read().decode('utf-8', errors='ignore')
        except:
            return ""

    ## ========================================================================
    ## SECTION 6: Rollback Operations
    ## ========================================================================

    def rollback_file(self, filename: str, commit_sha: str) -> str:
        """
        Rollback a file to a previous version.

        Creates a NEW commit with old content (doesn't rewrite history).

        Args:
            filename: File to rollback
            commit_sha: Commit to rollback to

        Returns:
            New commit SHA
        """
        try:
            ## Get file content at target commit
            commit = self.repo.commit(commit_sha)
            blob = commit.tree / filename
            old_content = blob.data_stream.read()

            ## Write old content to working directory
            file_path = self.repo_path / filename
            file_path.write_bytes(old_content)

            ## Commit the rollback
            self.repo.index.add([filename])
            rollback_commit = self.repo.index.commit(
                f"Rollback {filename} to {commit_sha[:8]}",
                author=f"{settings.GIT_USER_NAME} <{settings.GIT_USER_EMAIL}>",
                author_date=datetime.now(timezone.utc).isoformat()
            )

            logger.info(f"Rolled back {filename} to {commit_sha[:8]}")
            return rollback_commit.hexsha

        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            raise ValueError(f"Failed to rollback file: {e}")

    ## ========================================================================
    ## SECTION 7: Repository Statistics
    ## ========================================================================

    def get_repository_stats(self) -> Dict:
        """
        Get repository statistics.

        Returns:
            Dict with commit count, file count, etc.
        """
        try:
            ## Count total commits
            commit_count = sum(1 for _ in self.repo.iter_commits())

            ## Count files in latest commit
            head_commit = self.repo.head.commit
            file_count = sum(1 for _ in head_commit.tree.traverse() if _.type == 'blob')

            ## Get repo size
            repo_size = sum(
                f.stat().st_size
                for f in self.repo_path.rglob('*')
                if f.is_file()
            )

            return {
                'commit_count': commit_count,
                'file_count': file_count,
                'repo_size_bytes': repo_size,
                'latest_commit': head_commit.hexsha[:8],
                'latest_commit_date': head_commit.committed_datetime.isoformat(),
            }

        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {
                'commit_count': 0,
                'file_count': 0,
                'error': str(e)
            }
```

---

### 7.5: Integrate Git with File Service

**Update `backend/app/services/file_service.py`:**

```python
"""
File management with Git version control integration.
"""

from pathlib import Path
from typing import List, Dict, Optional
import json
import logging
import shutil
from datetime import datetime, timezone

from app.utils.file_locking import LockedFile
from app.services.git_service import GitService

logger = logging.getLogger(__name__)

## Keep AuditLogger, LockManager, FileRepository classes as-is...
## (Copy from Stage 6)

## ============================================================================
## SECTION 4: Update FileService with Git Integration
## ============================================================================

class FileService:
    """
    High-level file management with audit logging and Git version control.
    """

    def __init__(
        self,
        repo_path: Path,
        locks_file: Path,
        audit_file: Path,
        git_repo_path: Path
    ):
        self.repository = FileRepository(repo_path)
        self.lock_manager = LockManager(locks_file)
        self.audit_logger = AuditLogger(audit_file)
        self.git_service = GitService(git_repo_path)  ## NEW

    def get_files_with_status(self) -> List[Dict]:
        """Get all files with their lock status."""
        files = self.repository.list_files()
        locks = self.lock_manager.load_locks()

        result = []
        for file_info in files:
            filename = file_info['name']
            lock_info = locks.get(filename)

            result.append({
                'name': filename,
                'size_bytes': file_info['size_bytes'],
                'status': 'checked_out' if lock_info else 'available',
                'locked_by': lock_info['user'] if lock_info else None,
                'locked_at': lock_info.get('timestamp') if lock_info else None,
                'lock_message': lock_info.get('message') if lock_info else None,
            })

        return result

    def checkout_file(self, filename: str, user: str, message: str):
        """
        Check out a file for editing.

        NEW: Copies file to Git repository for version tracking.
        """
        if not self.repository.file_exists(filename):
            self.audit_logger.log_action(
                'checkout', filename, user,
                details={'error': 'File not found'},
                success=False
            )
            raise ValueError(f"File not found: {filename}")

        try:
            ## Acquire lock
            self.lock_manager.acquire_lock(filename, user, message)

            ## Copy file to Git repository (if not already there)
            if not self.git_service.file_exists(filename):
                content = self.repository.read_file(filename)
                self.git_service.add_file(filename, content)
                self.git_service.commit_file(
                    filename,
                    f"Initial version of {filename}",
                    user
                )

            ## Log success
            self.audit_logger.log_action(
                'checkout', filename, user,
                details={'message': message}
            )

        except ValueError as e:
            self.audit_logger.log_action(
                'checkout', filename, user,
                details={'error': str(e)},
                success=False
            )
            raise

    def checkin_file(self, filename: str, user: str, is_admin: bool = False):
        """
        Check in a file after editing.

        NEW: Creates Git commit with changes.
        """
        try:
            ## Release lock (with ownership check)
            self.lock_manager.release_lock(filename, user, is_admin)

            ## Copy current version to Git repo
            content = self.repository.read_file(filename)
            self.git_service.add_file(filename, content)

            ## Commit changes
            lock_info = self.lock_manager.get_lock_info(filename)
            commit_message = lock_info.get('message', 'File updated') if lock_info else 'File updated'

            commit_sha = self.git_service.commit_file(
                filename,
                f"Checkin: {commit_message}",
                user
            )

            ## Log success
            self.audit_logger.log_action(
                'checkin', filename, user,
                details={
                    'admin_override': is_admin,
                    'commit_sha': commit_sha
                }
            )

        except ValueError as e:
            self.audit_logger.log_action(
                'checkin', filename, user,
                details={'error': str(e)},
                success=False
            )
            raise

    def force_checkin(self, filename: str, admin_user: str):
        """Force checkin a file (admin only)."""
        lock_info = self.lock_manager.get_lock_info(filename)
        if not lock_info:
            raise ValueError("File is not locked")

        original_user = lock_info['user']

        ## Force release
        self.lock_manager.force_release(filename)

        ## Commit current state
        content = self.repository.read_file(filename)
        self.git_service.add_file(filename, content)
        commit_sha = self.git_service.commit_file(
            filename,
            f"Force checkin by admin (was locked by {original_user})",
            admin_user
        )

        ## Log admin action
        self.audit_logger.log_action(
            'force_checkin', filename, admin_user,
            details={
                'original_user': original_user,
                'commit_sha': commit_sha
            }
        )

    ## ========================================================================
    ## NEW: Git Operations
    ## ========================================================================

    def get_file_history(self, filename: str, limit: int = 50) -> List[Dict]:
        """Get version history for a file."""
        return self.git_service.get_file_history(filename, limit)

    def get_all_commits(self, limit: int = 100) -> List[Dict]:
        """Get all commits in repository."""
        return self.git_service.get_all_commits(limit)

    def get_file_diff(self, filename: str, commit_sha: str) -> Dict:
        """Get diff for a file at specific commit."""
        return self.git_service.get_file_diff(filename, commit_sha)

    def rollback_file(self, filename: str, commit_sha: str, user: str) -> str:
        """
        Rollback a file to previous version.

        Args:
            filename: File to rollback
            commit_sha: Target commit
            user: User performing rollback

        Returns:
            New commit SHA
        """
        ## Must have file locked to rollback
        if not self.lock_manager.is_locked_by_user(filename, user):
            if user != 'admin':  ## Allow admin override
                raise ValueError("You must checkout the file before rolling back")

        try:
            ## Perform rollback
            new_commit = self.git_service.rollback_file(filename, commit_sha)

            ## Copy rolled-back version to working directory
            content = self.git_service.get_file_content(filename)
            self.repository.write_file(filename, content)

            ## Log action
            self.audit_logger.log_action(
                'rollback', filename, user,
                details={
                    'target_commit': commit_sha,
                    'new_commit': new_commit
                }
            )

            return new_commit

        except Exception as e:
            self.audit_logger.log_action(
                'rollback', filename, user,
                details={'error': str(e)},
                success=False
            )
            raise ValueError(f"Rollback failed: {e}")

    def get_repository_stats(self) -> Dict:
        """Get Git repository statistics."""
        return self.git_service.get_repository_stats()

    def get_audit_logs(
        self,
        filename: Optional[str] = None,
        user: Optional[str] = None,
        limit: int = 100
    ) -> List[dict]:
        """Get audit logs with optional filters."""
        return self.audit_logger.get_logs(filename, user, limit=limit)
```

---

### 7.6: Update API Dependencies

**Update `backend/app/api/deps.py`:**

```python
## Update get_file_service:

def get_file_service() -> FileService:
    """Dependency that provides FileService instance."""
    repo_path = settings.BASE_DIR / 'repo'
    locks_file = settings.BASE_DIR / 'locks.json'
    audit_file = settings.BASE_DIR / 'audit.json'
    git_repo_path = settings.GIT_REPO_PATH  ## NEW

    return FileService(repo_path, locks_file, audit_file, git_repo_path)
```

---

### 7.7: Version Control API Endpoints

**File: `backend/app/api/version_control.py`:**

```python
"""
Version control API endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional

from app.schemas.auth import User
from app.services.file_service import FileService
from app.api.deps import get_current_user, get_file_service, require_admin

## ============================================================================
## SECTION 1: Router Setup
## ============================================================================

router = APIRouter(
    prefix="/api/version-control",
    tags=["version-control"],
)

## ============================================================================
## SECTION 2: History Endpoints
## ============================================================================

@router.get("/history/{filename}")
def get_file_history(
    filename: str,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service)
):
    """
    Get version history for a specific file.

    Shows all commits that modified this file.
    """
    try:
        history = file_service.get_file_history(filename, limit)

        return {
            "filename": filename,
            "commits": history,
            "count": len(history)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get file history: {str(e)}"
        )

@router.get("/commits")
def get_all_commits(
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service)
):
    """
    Get all commits in repository.

    Shows complete commit history across all files.
    """
    try:
        commits = file_service.get_all_commits(limit)

        return {
            "commits": commits,
            "count": len(commits)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get commits: {str(e)}"
        )

## ============================================================================
## SECTION 3: Diff Endpoints
## ============================================================================

@router.get("/diff/{filename}/{commit_sha}")
def get_file_diff(
    filename: str,
    commit_sha: str,
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service)
):
    """
    Get diff for a file at specific commit.

    Shows what changed in that commit.
    """
    try:
        diff = file_service.get_file_diff(filename, commit_sha)

        return {
            "filename": filename,
            "commit_sha": commit_sha,
            "diff": diff
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get diff: {str(e)}"
        )

## ============================================================================
## SECTION 4: Rollback Endpoints
## ============================================================================

@router.post("/rollback/{filename}/{commit_sha}")
def rollback_file(
    filename: str,
    commit_sha: str,
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service)
):
    """
    Rollback a file to a previous version.

    Requires: File must be checked out by you (or admin)
    Creates new commit with old content (doesn't rewrite history)
    """
    try:
        new_commit = file_service.rollback_file(
            filename,
            commit_sha,
            current_user.username
        )

        return {
            "success": True,
            "message": f"Rolled back {filename} to commit {commit_sha[:8]}",
            "new_commit": new_commit
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rollback failed: {str(e)}"
        )

## ============================================================================
## SECTION 5: Repository Stats
## ============================================================================

@router.get("/stats")
def get_repository_stats(
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service)
):
    """
    Get repository statistics.

    Total commits, file count, repo size, etc.
    """
    try:
        stats = file_service.get_repository_stats()

        return stats

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )
```

**Update `backend/app/main.py` to include version control router:**

```python
## Add import
from app.api import files, auth, version_control

## After including other routers:
app.include_router(version_control.router)
```

---

### 7.8: Frontend - Version History UI

**Add history styles to `backend/static/css/components.css`:**

```css
/* =========================================================================
   VERSION CONTROL UI
   ========================================================================= */

.version-history {
  margin-top: var(--spacing-4);
}

.commit-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-3);
}

.commit-item {
  padding: var(--spacing-4);
  border: 1px solid var(--border-default);
  border-left: 4px solid var(--interactive-primary);
  border-radius: var(--radius-md);
  background: var(--bg-secondary);
  transition: all var(--transition-fast);
}

.commit-item:hover {
  transform: translateX(5px);
  box-shadow: var(--shadow-sm);
}

.commit-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: var(--spacing-2);
}

.commit-message {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin-bottom: var(--spacing-1);
}

.commit-sha {
  font-family: var(--font-mono);
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  background: var(--bg-tertiary);
  padding: var(--spacing-1) var(--spacing-2);
  border-radius: var(--radius-sm);
}

.commit-meta {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  display: flex;
  gap: var(--spacing-4);
  flex-wrap: wrap;
}

.commit-actions {
  display: flex;
  gap: var(--spacing-2);
  margin-top: var(--spacing-3);
}

.diff-viewer {
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
  background: var(--bg-tertiary);
  padding: var(--spacing-4);
  border-radius: var(--radius-base);
  overflow-x: auto;
  white-space: pre;
  line-height: 1.5;
  max-height: 400px;
  overflow-y: auto;
}

.diff-line-added {
  background: rgba(16, 185, 129, 0.1);
  color: var(--status-success-text);
}

.diff-line-removed {
  background: rgba(239, 68, 68, 0.1);
  color: var(--status-danger-text);
}

.diff-line-context {
  color: var(--text-secondary);
}

.repo-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-4);
  margin-top: var(--spacing-4);
}

.stat-card {
  background: var(--bg-secondary);
  padding: var(--spacing-4);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-default);
}

.stat-value {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--interactive-primary);
  margin-bottom: var(--spacing-2);
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

**Update `backend/static/index.html` - add history modal:**

```html
<!-- Version History Modal -->
<div id="history-modal" class="modal-overlay hidden">
  <div class="modal-content" style="max-width: 900px;">
    <div class="modal-header">
      <h3>Version History: <span id="history-filename"></span></h3>
      <button class="modal-close" type="button">&times;</button>
    </div>

    <div class="modal-body">
      <div id="history-container"></div>
    </div>
  </div>
</div>

<!-- Diff Viewer Modal -->
<div id="diff-modal" class="modal-overlay hidden">
  <div class="modal-content" style="max-width: 1000px;">
    <div class="modal-header">
      <h3>Changes in Commit</h3>
      <button class="modal-close" type="button">&times;</button>
    </div>

    <div class="modal-body">
      <div id="diff-info" style="margin-bottom: var(--spacing-4);"></div>
      <div id="diff-container" class="diff-viewer"></div>
    </div>
  </div>
</div>
```

---

### 7.9: Update Frontend API Client

**Update `backend/static/js/modules/api-client.js`:**

```javascript
// Add version control methods:

/**
 * Get file history
 */
async getFileHistory(filename, limit = 50) {
  return this.get(`/api/version-control/history/${encodeURIComponent(filename)}?limit=${limit}`);
}

/**
 * Get all commits
 */
async getAllCommits(limit = 100) {
  return this.get(`/api/version-control/commits?limit=${limit}`);
}

/**
 * Get file diff at commit
 */
async getFileDiff(filename, commitSha) {
  return this.get(`/api/version-control/diff/${encodeURIComponent(filename)}/${commitSha}`);
}

/**
 * Rollback file to previous version
 */
async rollbackFile(filename, commitSha) {
  return this.post(`/api/version-control/rollback/${encodeURIComponent(filename)}/${commitSha}`);
}

/**
 * Get repository stats
 */
async getRepoStats() {
  return this.get('/api/version-control/stats');
}
```

---

### 7.10: Update Main Application

**Update `backend/static/js/app.js` - add version control features:**

```javascript
// Add modal instances after existing ones:
const historyModal = new ModalManager("history-modal");
const diffModal = new ModalManager("diff-modal");

let currentHistoryFile = null;

// ============================================================================
// SECTION: Enhanced File Item with History Button
// ============================================================================

function createFileElement(file, selectedFile) {
  const div = document.createElement("div");
  div.className = "file-item";

  if (selectedFile && selectedFile.name === file.name) {
    div.classList.add("selected");
  }

  div.addEventListener("click", (e) => {
    if (e.target.tagName !== "BUTTON") {
      store.setSelectedFile(file);
    }
  });

  const infoDiv = document.createElement("div");
  infoDiv.className = "file-info";

  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ").toUpperCase();

  const sizeSpan = document.createElement("span");
  sizeSpan.style.fontSize = "var(--font-size-sm)";
  sizeSpan.style.color = "var(--text-secondary)";
  sizeSpan.textContent = formatBytes(file.size_bytes);

  infoDiv.appendChild(nameSpan);
  infoDiv.appendChild(statusSpan);
  infoDiv.appendChild(sizeSpan);

  const actionsDiv = document.createElement("div");
  actionsDiv.className = "file-actions";

  const userRole = localStorage.getItem("user_role");
  const username = localStorage.getItem("username");

  // History button (always available)
  const historyBtn = document.createElement("button");
  historyBtn.className = "btn btn-secondary btn-sm";
  historyBtn.textContent = "📜 History";
  historyBtn.onclick = (e) => {
    e.stopPropagation();
    showFileHistory(file.name);
  };
  actionsDiv.appendChild(historyBtn);

  if (file.status === "available") {
    const checkoutBtn = document.createElement("button");
    checkoutBtn.className = "btn btn-primary btn-sm";
    checkoutBtn.textContent = "Checkout";
    checkoutBtn.onclick = (e) => {
      e.stopPropagation();
      handleCheckout(file.name);
    };
    actionsDiv.appendChild(checkoutBtn);
  } else {
    const checkinBtn = document.createElement("button");
    checkinBtn.className = "btn btn-secondary btn-sm";
    checkinBtn.textContent = "Checkin";
    checkinBtn.onclick = (e) => {
      e.stopPropagation();
      handleCheckin(file.name);
    };

    if (file.locked_by !== username && userRole !== "admin") {
      checkinBtn.disabled = true;
      checkinBtn.title = `Locked by ${file.locked_by}`;
    }

    actionsDiv.appendChild(checkinBtn);

    if (userRole === "admin" && file.locked_by !== username) {
      const forceBtn = document.createElement("button");
      forceBtn.className = "btn btn-danger btn-sm";
      forceBtn.textContent = "🔓 Force";
      forceBtn.onclick = (e) => {
        e.stopPropagation();
        handleForceCheckin(file.name);
      };
      actionsDiv.appendChild(forceBtn);
    }

    if (file.locked_by) {
      const lockedBySpan = document.createElement("span");
      lockedBySpan.style.fontSize = "var(--font-size-sm)";
      lockedBySpan.style.color = "var(--text-secondary)";
      lockedBySpan.textContent = `By: ${file.locked_by}`;
      actionsDiv.appendChild(lockedBySpan);
    }
  }

  div.appendChild(infoDiv);
  div.appendChild(actionsDiv);

  return div;
}

// ============================================================================
// SECTION: Version History
// ============================================================================

async function showFileHistory(filename) {
  currentHistoryFile = filename;
  document.getElementById("history-filename").textContent = filename;
  historyModal.open();

  const container = document.getElementById("history-container");
  container.innerHTML =
    '<div class="loading"><p>Loading version history...</p></div>';

  try {
    const data = await apiClient.getFileHistory(filename);

    if (data.commits.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
          <p>No version history available yet.</p>
          <p style="font-size: var(--font-size-sm);">History is created when you checkin files.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = `
      <div class="commit-list">
        ${data.commits
          .map((commit) => createCommitElement(commit, filename))
          .join("")}
      </div>
    `;

    // Wire up buttons
    data.commits.forEach((commit) => {
      const viewBtn = document.getElementById(`view-diff-${commit.sha}`);
      if (viewBtn) {
        viewBtn.onclick = () => showDiff(filename, commit.sha);
      }

      const rollbackBtn = document.getElementById(`rollback-${commit.sha}`);
      if (rollbackBtn) {
        rollbackBtn.onclick = () => handleRollback(filename, commit.sha);
      }
    });
  } catch (error) {
    container.innerHTML = `
      <div style="text-align: center; padding: 2rem; color: var(--status-danger-text);">
        <p><strong>Error:</strong> ${error.message}</p>
      </div>
    `;
  }
}

function createCommitElement(commit, filename) {
  const date = new Date(commit.date);
  const username = localStorage.getItem("username");
  const userRole = localStorage.getItem("user_role");

  // Check if user can rollback (must own lock or be admin)
  const canRollback = userRole === "admin"; // Simplified for now

  return `
    <div class="commit-item">
      <div class="commit-header">
        <div>
          <div class="commit-message">${escapeHtml(commit.message)}</div>
          <div class="commit-meta">
            <span>👤 ${escapeHtml(commit.author)}</span>
            <span>📅 ${date.toLocaleString()}</span>
            <span class="commit-sha">${commit.short_sha}</span>
          </div>
        </div>
      </div>
      <div class="commit-actions">
        <button class="btn btn-secondary btn-sm" id="view-diff-${commit.sha}">
          👁️ View Changes
        </button>
        ${
          canRollback
            ? `
          <button class="btn btn-warning btn-sm" id="rollback-${commit.sha}">
            ⏮️ Rollback to This Version
          </button>
        `
            : ""
        }
      </div>
    </div>
  `;
}

// ============================================================================
// SECTION: Diff Viewer
// ============================================================================

async function showDiff(filename, commitSha) {
  diffModal.open();

  const infoDiv = document.getElementById("diff-info");
  const container = document.getElementById("diff-container");

  infoDiv.innerHTML = `<p>Loading diff for <strong>${filename}</strong> at commit <code>${commitSha.substring(
    0,
    8
  )}</code>...</p>`;
  container.textContent = "";

  try {
    const data = await apiClient.getFileDiff(filename, commitSha);
    const diff = data.diff;

    infoDiv.innerHTML = `
      <p><strong>File:</strong> ${filename}</p>
      <p><strong>Commit:</strong> <code>${commitSha.substring(0, 8)}</code></p>
      <p><strong>Type:</strong> ${diff.type}</p>
    `;

    if (diff.type === "error") {
      container.innerHTML = `<div style="color: var(--status-danger-text);">Error: ${diff.error}</div>`;
      return;
    }

    if (diff.type === "unchanged") {
      container.innerHTML = `<div style="color: var(--text-secondary);">No changes in this commit.</div>`;
      return;
    }

    if (diff.diff) {
      // Format diff output
      container.innerHTML = formatDiff(diff.diff);
    } else if (diff.type === "added") {
      container.innerHTML = `<div class="diff-line-added">+++ New file created</div>`;
    }
  } catch (error) {
    container.innerHTML = `<div style="color: var(--status-danger-text);">Error loading diff: ${error.message}</div>`;
  }
}

function formatDiff(diffText) {
  const lines = diffText.split("\n");
  return lines
    .map((line) => {
      if (line.startsWith("+") && !line.startsWith("+++")) {
        return `<div class="diff-line-added">${escapeHtml(line)}</div>`;
      } else if (line.startsWith("-") && !line.startsWith("---")) {
        return `<div class="diff-line-removed">${escapeHtml(line)}</div>`;
      } else {
        return `<div class="diff-line-context">${escapeHtml(line)}</div>`;
      }
    })
    .join("");
}

// ============================================================================
// SECTION: Rollback
// ============================================================================

async function handleRollback(filename, commitSha) {
  if (
    !confirm(
      `⚠️ Rollback "${filename}" to commit ${commitSha.substring(
        0,
        8
      )}?\n\nThis will create a new commit with the old version. Current changes will be preserved in history.`
    )
  ) {
    return;
  }

  try {
    const result = await apiClient.rollbackFile(filename, commitSha);
    toast.success(`Rolled back ${filename} to ${commitSha.substring(0, 8)}`);
    historyModal.close();
    loadFiles();
  } catch (error) {
    toast.error(error.message);
  }
}

// ============================================================================
// SECTION: Utility Functions
// ============================================================================

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// ... rest of app.js remains the same
```

---

### Stage 7 Complete

**Test version control features:**

```bash
uvicorn app.main:app --reload
```

**Test workflow:**

1. Login as any user
2. Checkout a file
3. Checkin the file (creates Git commit)
4. Click "📜 History" button on the file
5. See commit history with your checkin
6. Click "👁️ View Changes" to see diff
7. Click "⏮️ Rollback" (if admin) to restore old version
8. Verify file is rolled back

**File structure:**

```
backend/
├── app/
│   ├── learn_git_internals.py      ## NEW
│   ├── services/
│   │   ├── git_service.py          ## NEW
│   │   └── file_service.py         ## UPDATED
│   └── api/
│       ├── version_control.py      ## NEW
│       └── deps.py                 ## UPDATED
├── static/
│   ├── css/
│   │   └── components.css          ## UPDATED
│   ├── js/
│   │   ├── modules/
│   │   │   └── api-client.js       ## UPDATED
│   │   └── app.js                  ## UPDATED
│   └── index.html                  ## UPDATED
├── git_repo/                       ## Auto-created Git repo
│   └── .git/
└── repo/                           ## Working files
```

**What you learned:**

- Git internals (content addressing, objects, commits)
- GitPython library usage
- Version control integration
- Commit history tracking
- Diff generation and viewing
- Rollback/revert operations
- Git repository management
- SHA-1 hashing and content addressing

**Verification:**

- [ ] Git repository auto-created on startup
- [ ] Checkins create Git commits
- [ ] History button shows commit log
- [ ] View Changes shows diffs
- [ ] Rollback restores old versions
- [ ] All operations logged in audit
- [ ] Commits have proper author/message

**What we've built so far:**

- ✅ Professional dev environment (Stage 0)
- ✅ FastAPI backend with routing (Stage 1)
- ✅ Professional frontend with theming (Stage 2)
- ✅ File locking system (Stage 3)
- ✅ State management & UX polish (Stage 4)
- ✅ Authentication with JWT (Stage 5)
- ✅ Authorization & audit logging (Stage 6)
- ✅ Git version control integration (Stage 7)

**Possible Stage 8 topics:**

- Real-time collaboration (WebSockets)
- Database integration (PostgreSQL/SQLite)
- Docker containerization
- File upload/download
- Advanced Git features (branching, merging)
- Email notifications
- REST API documentation improvements
- Performance optimization

Let me know what you'd like for Stage 8!

## Stage 8: Hybrid Architecture - GitLab Integration for Both Modes

**Prerequisites**: Completed Stage 7

**Time**: 7-8 hours

**What you'll build**: A hybrid system that works standalone (PyInstaller) OR as a central server, with GitLab as the single source of truth in both modes.

---

### 8.1: Deep Dive - Hybrid Architecture Patterns

**File: `backend/app/learn_hybrid_architecture.py`**

```python
"""
Understanding Hybrid Architecture: Standalone + Server Modes

Your PDM system needs to work in TWO deployment modes:

MODE 1: STANDALONE (PyInstaller Executable)
- Each user runs their own .exe file
- No central server
- Each exe clones GitLab repo locally
- GitLab is single source of truth
- Users authenticate with GitLab Personal Access Token

MODE 2: SERVER (What we built in Stages 1-7)
- Central FastAPI server
- Multiple browser clients
- Server clones GitLab repo
- Server periodically syncs with GitLab
- Users authenticate with username/password OR GitLab PAT

BOTH MODES share:
- GitLab repo contains: users.json, locks.json, messages.json, .mcam files
- All data operations: pull from GitLab → modify → commit → push to GitLab
- GitLab acts as coordination layer
"""

## ============================================================================
## SECTION 1: The Problem with Distributed Systems
## ============================================================================

"""
When multiple machines modify the same files, you get conflicts:

Timeline:
T1: Alice's machine pulls from GitLab
    locks.json: {}

T2: Bob's machine pulls from GitLab
    locks.json: {}

T3: Alice checks out PN1001.mcam
    Local locks.json: {"PN1001.mcam": {"user": "alice"}}

T4: Alice commits and pushes to GitLab
    GitLab locks.json: {"PN1001.mcam": {"user": "alice"}}

T5: Bob (still has old locks.json) checks out PN1001.mcam
    Local locks.json: {"PN1001.mcam": {"user": "bob"}}

T6: Bob tries to push → GIT CONFLICT!
    GitLab has Alice's lock, Bob has different version

SOLUTION: Always pull before modifying
- Pull from GitLab
- Check locks.json (Alice's lock exists)
- Reject Bob's checkout attempt
- Show error: "File already locked by Alice"

This is called "Optimistic Locking"
"""

## ============================================================================
## SECTION 2: GitLab Personal Access Token (PAT) Authentication
## ============================================================================

"""
GitLab Personal Access Token = API key for authentication

Traditional username/password:
- Username: alice
- Password: secret123
- Problem: Can't use for API calls

GitLab PAT:
- Token: glpat-xxxxxxxxxxxxxxxxxxxx
- Scopes: api, read_repository, write_repository
- Can be used for:
  1. Git operations (git clone, push, pull)
  2. GitLab API calls
  3. Authentication verification

Our authentication flow:

INITIAL SETUP (First time user):
1. User creates GitLab account
2. User generates Personal Access Token in GitLab
   - Settings → Access Tokens
   - Scopes: api, read_repository, write_repository
3. User enters PAT in our app
4. App validates PAT against GitLab API
5. App asks user to create app password
6. App stores in GitLab repo's users.json:
   {
     "username": "alice",
     "password_hash": "bcrypt_hash_of_app_password",
     "gitlab_token_hash": "bcrypt_hash_of_PAT",
     "full_name": "Alice Smith",
     "role": "user"
   }
7. Commit and push users.json to GitLab

SUBSEQUENT LOGINS (From any machine):
Option A: Login with GitLab PAT
  - User enters: username + PAT
  - App validates PAT against GitLab API
  - App pulls users.json from GitLab
  - App verifies username exists and PAT hash matches
  - Success → User is logged in

Option B: Login with app password
  - User enters: username + app password
  - App pulls users.json from GitLab
  - App verifies password hash
  - Success → User is logged in
  - App retrieves stored PAT hash to use for Git operations

Why hash the PAT?
- Security in depth
- Even if GitLab repo is compromised, attacker can't use PAT
- But wait... we NEED the PAT to do Git operations!

SOLUTION: Encrypt PAT with user's password
- Encrypt(PAT, user_password) → stored in users.json
- When user logs in with password → Decrypt PAT
- Use decrypted PAT for Git operations during session
- PAT never stored in plain text
"""

## ============================================================================
## SECTION 3: Configuration Modes
## ============================================================================

"""
Configuration file determines mode:

## config.yaml
mode: "standalone"  ## or "server"
gitlab:
  repo_url: "https://gitlab.com/your-org/pdm-files"
  branch: "main"
  lfs_enabled: true
local_storage:
  clone_path: "./pdm_repo_clone"
server:
  host: "0.0.0.0"
  port: 8000
  sync_interval: 60  ## seconds

STANDALONE MODE:
- App starts embedded FastAPI server on localhost:5000
- Opens browser automatically to localhost:5000
- User sees UI
- All operations go through localhost:5000
- Backend syncs with GitLab
- When user closes app, server shuts down

SERVER MODE:
- App starts FastAPI server on configured host/port
- Admin accesses from any browser
- Multiple users can connect
- Server runs continuously
- Periodic background sync with GitLab
"""

## ============================================================================
## SECTION 4: Git LFS (Large File Storage)
## ============================================================================

"""
Git LFS for Large Files (.mcam files might be large)

Normal Git:
- Stores full file content in repository
- Large files slow down clone/pull
- Repo size grows quickly

Git LFS:
- Stores pointer file in Git (small)
- Actual file stored on LFS server
- Git clone is fast
- Files downloaded on-demand

Setup:
1. Install Git LFS: brew install git-lfs / apt install git-lfs
2. Initialize: git lfs install
3. Track file types: git lfs track "*.mcam"
4. Commit .gitattributes
5. Normal git operations work (clone, push, pull)

In our app:
- Check if LFS is installed
- Warn user if not installed
- Provide installation instructions
"""

## ============================================================================
## SECTION 5: Sync Strategy
## ============================================================================

"""
STANDALONE MODE Sync Strategy:

BEFORE every operation:
1. git pull origin main
2. Check if conflicts
3. If conflicts → resolve or abort
4. Proceed with operation

AFTER every operation:
1. git add <files>
2. git commit -m "message"
3. git push origin main
4. If push fails (someone else pushed) → pull and retry

SERVER MODE Sync Strategy:

Background sync (every 60 seconds):
1. git pull origin main
2. Reload in-memory state (locks.json, users.json)
3. Notify connected clients of changes via WebSocket

User operations:
1. Modify local state
2. Commit to local Git
3. Push to GitLab
4. If push fails → pull, merge, retry
"""

## ============================================================================
## SECTION 6: Conflict Resolution
## ============================================================================

"""
What if two users modify locks.json simultaneously?

Scenario:
T1: Alice pulls (locks.json is empty)
T2: Bob pulls (locks.json is empty)
T3: Alice locks PN1001, pushes
T4: Bob locks PN1002, tries to push → CONFLICT

Git merge conflict in locks.json:
<<<<<<< HEAD (GitLab)
{
  "PN1001.mcam": {"user": "alice", ...}
}
=======
{
  "PN1002.mcam": {"user": "bob", ...}
}
>>>>>>> incoming (Bob)

RESOLUTION:
Merge both locks (they don't conflict):
{
  "PN1001.mcam": {"user": "alice", ...},
  "PN1002.mcam": {"user": "bob", ...}
}

Our strategy:
- Detect conflict
- Automatically merge locks.json (union of locks)
- If same file locked by two users → last push wins (error for one user)
- Retry push after merge
"""

if __name__ == "__main__":
    print("Hybrid architecture concepts explained.")
    print("Mode 1: Standalone - PyInstaller exe with embedded server")
    print("Mode 2: Server - Central server with browser clients")
    print("Both modes: GitLab is single source of truth")
```

Run it:

```bash
python -m app.learn_hybrid_architecture
```

---

### 8.2: Update Configuration for Hybrid Mode

**Update `backend/app/config.py`:**

```python
"""
Application configuration for hybrid deployment.
"""

from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Literal

class Settings(BaseSettings):
    """Application settings."""

    ## ========================================================================
    ## Application Settings
    ## ========================================================================
    APP_NAME: str = "PDM System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    ## ========================================================================
    ## Deployment Mode
    ## ========================================================================
    MODE: Literal["standalone", "server"] = "server"  ## NEW

    ## In standalone mode, server starts on localhost
    ## In server mode, server starts on configured host

    ## ========================================================================
    ## Security Settings
    ## ========================================================================
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ## Encryption key for storing GitLab PAT
    ## Generate with: from cryptography.fernet import Fernet; Fernet.generate_key()
    ENCRYPTION_KEY: str = "your-fernet-encryption-key-here"  ## NEW

    ## ========================================================================
    ## GitLab Configuration
    ## ========================================================================
    GITLAB_ENABLED: bool = True  ## NEW
    GITLAB_URL: str = "https://gitlab.com"  ## NEW
    GITLAB_REPO_URL: str = ""  ## NEW - e.g., "https://gitlab.com/username/pdm-repo.git"
    GITLAB_BRANCH: str = "main"  ## NEW
    GITLAB_LFS_ENABLED: bool = True  ## NEW

    ## ========================================================================
    ## Path Configuration
    ## ========================================================================
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    ## Local Git repository clone
    GITLAB_CLONE_PATH: Path = BASE_DIR / "gitlab_repo_clone"  ## NEW

    ## Legacy local paths (used when GitLab disabled)
    GIT_REPO_PATH: Path = BASE_DIR / "git_repo"

    ## ========================================================================
    ## Server Configuration
    ## ========================================================================
    HOST: str = "127.0.0.1"  ## NEW - localhost for standalone, 0.0.0.0 for server
    PORT: int = 8000  ## NEW

    ## Sync interval for server mode (seconds)
    GITLAB_SYNC_INTERVAL: int = 60  ## NEW

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

## Auto-adjust host based on mode
if settings.MODE == "standalone":
    settings.HOST = "127.0.0.1"
elif settings.MODE == "server":
    settings.HOST = "0.0.0.0"
```

**Create `.env` file with your GitLab details:**

```bash
## backend/.env

## Deployment mode
MODE=server

## GitLab Configuration
GITLAB_ENABLED=true
GITLAB_URL=https://gitlab.com
GITLAB_REPO_URL=https://gitlab.com/YOUR_USERNAME/pdm-files.git
GITLAB_BRANCH=main
GITLAB_LFS_ENABLED=true

## Security
SECRET_KEY=your-secret-key-change-this
ENCRYPTION_KEY=your-fernet-key-here

## Server settings
HOST=0.0.0.0
PORT=8000
```

---

### 8.3: GitLab API Service

**Install dependencies:**

```bash
pip install python-gitlab cryptography
pip freeze > requirements.txt
```

**File: `backend/app/services/gitlab_service.py`:**

```python
"""
GitLab integration service.

Handles GitLab API calls, authentication, and repository operations.
"""

import gitlab
from pathlib import Path
from typing import Optional, Dict
import logging

from app.config import settings

logger = logging.getLogger(__name__)

## ============================================================================
## SECTION 1: GitLab API Client
## ============================================================================

class GitLabService:
    """
    Manages GitLab API interactions.

    Used for:
    - Validating Personal Access Tokens
    - Checking user permissions
    - Querying repository information
    """

    def __init__(self):
        """Initialize GitLab service."""
        self.gitlab_url = settings.GITLAB_URL
        self.gl = None

    def validate_token(self, token: str) -> Optional[Dict]:
        """
        Validate a GitLab Personal Access Token.

        Args:
            token: GitLab PAT to validate

        Returns:
            User info dict if valid, None if invalid
            {
                'username': 'alice',
                'name': 'Alice Smith',
                'email': 'alice@example.com',
                'id': 12345
            }
        """
        try:
            ## Connect to GitLab with token
            gl = gitlab.Gitlab(self.gitlab_url, private_token=token)

            ## Authenticate (this validates the token)
            gl.auth()

            ## Get current user info
            current_user = gl.user

            return {
                'username': current_user.username,
                'name': current_user.name,
                'email': current_user.email,
                'id': current_user.id
            }

        except gitlab.exceptions.GitlabAuthenticationError:
            logger.warning("Invalid GitLab token provided")
            return None
        except Exception as e:
            logger.error(f"GitLab token validation failed: {e}")
            return None

    def check_repository_access(self, token: str, repo_url: str) -> bool:
        """
        Check if token has access to repository.

        Args:
            token: GitLab PAT
            repo_url: Repository URL

        Returns:
            True if has access, False otherwise
        """
        try:
            gl = gitlab.Gitlab(self.gitlab_url, private_token=token)
            gl.auth()

            ## Extract project path from URL
            ## https://gitlab.com/username/project → username/project
            if '//' in repo_url:
                path = repo_url.split('//')[-1]
                path = '/'.join(path.split('/')[1:])  ## Remove domain
                path = path.replace('.git', '')
            else:
                path = repo_url.replace('.git', '')

            ## Try to get project
            project = gl.projects.get(path)

            return True

        except gitlab.exceptions.GitlabGetError:
            logger.warning(f"No access to repository: {repo_url}")
            return False
        except Exception as e:
            logger.error(f"Repository access check failed: {e}")
            return False

    def get_project_info(self, token: str, repo_url: str) -> Optional[Dict]:
        """
        Get repository/project information.

        Args:
            token: GitLab PAT
            repo_url: Repository URL

        Returns:
            Project info dict or None
        """
        try:
            gl = gitlab.Gitlab(self.gitlab_url, private_token=token)
            gl.auth()

            ## Extract project path
            if '//' in repo_url:
                path = repo_url.split('//')[-1]
                path = '/'.join(path.split('/')[1:])
                path = path.replace('.git', '')
            else:
                path = repo_url.replace('.git', '')

            project = gl.projects.get(path)

            return {
                'id': project.id,
                'name': project.name,
                'path': project.path_with_namespace,
                'description': project.description,
                'http_url': project.http_url_to_repo,
                'ssh_url': project.ssh_url_to_repo,
                'lfs_enabled': project.lfs_enabled,
            }

        except Exception as e:
            logger.error(f"Failed to get project info: {e}")
            return None
```

---

### 8.4: GitLab Repository Sync Service

**File: `backend/app/services/gitlab_sync_service.py`:**

```python
"""
GitLab repository synchronization service.

Handles cloning, pulling, committing, and pushing to GitLab.
"""

from pathlib import Path
from typing import Optional
import logging
import subprocess
import json

from git import Repo, GitCommandError
from git.exc import InvalidGitRepositoryError

from app.config import settings
from app.utils.file_locking import LockedFile

logger = logging.getLogger(__name__)

## ============================================================================
## SECTION 1: GitLab Sync Manager
## ============================================================================

class GitLabSyncService:
    """
    Manages GitLab repository synchronization.

    This is the bridge between local operations and GitLab.
    """

    def __init__(self, clone_path: Path, repo_url: str, token: str):
        """
        Initialize GitLab sync service.

        Args:
            clone_path: Local path for Git clone
            repo_url: GitLab repository URL
            token: GitLab Personal Access Token
        """
        self.clone_path = clone_path
        self.repo_url = self._inject_token_to_url(repo_url, token)
        self.token = token
        self.repo = None

        ## Ensure repository is cloned and ready
        self._ensure_repository()

    def _inject_token_to_url(self, url: str, token: str) -> str:
        """
        Inject GitLab token into repository URL for authentication.

        https://gitlab.com/user/repo.git
        →
        https://oauth2:TOKEN@gitlab.com/user/repo.git
        """
        if '@' in url:
            ## Token already in URL
            return url

        if url.startswith('https://'):
            return url.replace('https://', f'https://oauth2:{token}@')
        elif url.startswith('http://'):
            return url.replace('http://', f'http://oauth2:{token}@')
        else:
            return url

    def _ensure_repository(self):
        """
        Ensure repository is cloned and accessible.
        """
        try:
            ## Try to open existing repo
            self.repo = Repo(self.clone_path)
            logger.info(f"Opened existing GitLab clone at {self.clone_path}")

            ## Ensure we're on correct branch
            if self.repo.active_branch.name != settings.GITLAB_BRANCH:
                self.repo.git.checkout(settings.GITLAB_BRANCH)

        except (InvalidGitRepositoryError, Exception):
            ## Clone repository
            logger.info(f"Cloning GitLab repository to {self.clone_path}")
            self.clone_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                self.repo = Repo.clone_from(
                    self.repo_url,
                    self.clone_path,
                    branch=settings.GITLAB_BRANCH
                )
                logger.info("Successfully cloned GitLab repository")

                ## Configure Git LFS if enabled
                if settings.GITLAB_LFS_ENABLED:
                    try:
                        self.repo.git.execute(['git', 'lfs', 'install'])
                        logger.info("Git LFS initialized")
                    except Exception as e:
                        logger.warning(f"Git LFS setup failed (is it installed?): {e}")

            except GitCommandError as e:
                logger.error(f"Failed to clone repository: {e}")
                raise ValueError(f"Cannot clone GitLab repository. Check token and URL.")

    ## ========================================================================
    ## SECTION 2: Sync Operations
    ## ========================================================================

    def pull(self) -> bool:
        """
        Pull latest changes from GitLab.

        Returns:
            True if successful, False otherwise
        """
        try:
            ## Fetch latest
            origin = self.repo.remote('origin')
            origin.pull(settings.GITLAB_BRANCH)

            logger.info("Successfully pulled from GitLab")
            return True

        except GitCommandError as e:
            logger.error(f"Failed to pull from GitLab: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during pull: {e}")
            return False

    def commit_and_push(
        self,
        files: list[str],
        message: str,
        author_name: str,
        author_email: str
    ) -> bool:
        """
        Commit changes and push to GitLab.

        Args:
            files: List of file paths to commit (relative to repo root)
            message: Commit message
            author_name: Author name
            author_email: Author email

        Returns:
            True if successful, False otherwise
        """
        try:
            ## Pull first to ensure we're up to date
            if not self.pull():
                logger.warning("Pull failed before commit, proceeding anyway")

            ## Stage files
            self.repo.index.add(files)

            ## Check if there are changes to commit
            if not self.repo.index.diff("HEAD"):
                logger.info("No changes to commit")
                return True

            ## Commit
            commit = self.repo.index.commit(
                message,
                author=f"{author_name} <{author_email}>"
            )
            logger.info(f"Created commit: {commit.hexsha[:8]}")

            ## Push
            origin = self.repo.remote('origin')
            origin.push(settings.GITLAB_BRANCH)

            logger.info("Successfully pushed to GitLab")
            return True

        except GitCommandError as e:
            logger.error(f"Git operation failed: {e}")

            ## If push failed due to conflict, try pull and retry once
            if 'rejected' in str(e).lower() or 'conflict' in str(e).lower():
                logger.info("Push rejected, pulling and retrying...")
                if self.pull():
                    ## Retry push
                    try:
                        origin = self.repo.remote('origin')
                        origin.push(settings.GITLAB_BRANCH)
                        logger.info("Retry push succeeded")
                        return True
                    except:
                        pass

            return False

        except Exception as e:
            logger.error(f"Unexpected error during commit/push: {e}")
            return False

    ## ========================================================================
    ## SECTION 3: File Operations
    ## ========================================================================

    def read_file(self, filename: str) -> Optional[bytes]:
        """
        Read file from repository.

        Args:
            filename: Relative path from repo root

        Returns:
            File contents as bytes, or None if not found
        """
        try:
            file_path = self.clone_path / filename
            if file_path.exists():
                return file_path.read_bytes()
            return None
        except Exception as e:
            logger.error(f"Failed to read file {filename}: {e}")
            return None

    def write_file(self, filename: str, content: bytes):
        """
        Write file to repository.

        Args:
            filename: Relative path from repo root
            content: File contents as bytes
        """
        try:
            file_path = self.clone_path / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_bytes(content)
        except Exception as e:
            logger.error(f"Failed to write file {filename}: {e}")
            raise

    def file_exists(self, filename: str) -> bool:
        """Check if file exists in repository."""
        return (self.clone_path / filename).exists()

    def list_files(self, pattern: str = "*.mcam") -> list[Path]:
        """
        List files matching pattern in repository.

        Args:
            pattern: Glob pattern

        Returns:
            List of file paths
        """
        try:
            return list(self.clone_path.glob(pattern))
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            return []

    ## ========================================================================
    ## SECTION 4: JSON State Files (users.json, locks.json, messages.json)
    ## ========================================================================

    def load_json_file(self, filename: str) -> dict:
        """
        Load and parse JSON file from repository.

        Args:
            filename: JSON filename (e.g., 'users.json')

        Returns:
            Parsed JSON as dict, or empty dict if not found
        """
        try:
            file_path = self.clone_path / filename

            if not file_path.exists():
                return {}

            with LockedFile(file_path, 'r') as f:
                content = f.read()
                if not content.strip():
                    return {}
                return json.loads(content)

        except Exception as e:
            logger.error(f"Failed to load {filename}: {e}")
            return {}

    def save_json_file(self, filename: str, data: dict):
        """
        Save dict as JSON file in repository.

        Args:
            filename: JSON filename
            data: Dictionary to save
        """
        try:
            file_path = self.clone_path / filename

            with LockedFile(file_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to save {filename}: {e}")
            raise

    ## ========================================================================
    ## SECTION 5: Repository Info
    ## ========================================================================

    def get_current_commit(self) -> str:
        """Get current commit SHA."""
        try:
            return self.repo.head.commit.hexsha
        except:
            return "unknown"

    def get_remote_url(self) -> str:
        """Get remote URL (without token)."""
        try:
            url = self.repo.remote('origin').url
            ## Remove token from URL
            if '@' in url and 'oauth2:' in url:
                parts = url.split('@')
                return 'https://' + parts[-1]
            return url
        except:
            return "unknown"
```

---

This is getting quite long. Should I continue with:

**Stage 8 - Part 2:**

- User authentication with GitLab PAT
- Encrypted token storage
- User registration flow
- Messaging system
- API updates for GitLab mode
- Frontend updates

Or would you prefer I provide a summary of what's next and you can request specific parts?

## Stage 8 - Part 2: GitLab Authentication & Messaging

---

### 8.5: Encrypted Token Storage

**File: `backend/app/utils/encryption.py`:**

```python
"""
Encryption utilities for secure token storage.

Uses Fernet symmetric encryption to encrypt GitLab PATs.
PAT is encrypted with user's password, stored encrypted in GitLab repo.
"""

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
import os
from typing import Optional

## ============================================================================
## SECTION 1: Key Derivation
## ============================================================================

def derive_key_from_password(password: str, salt: bytes) -> bytes:
    """
    Derive encryption key from password using PBKDF2.

    PBKDF2 = Password-Based Key Derivation Function 2
    - Takes password and random salt
    - Applies hash function many times (100,000 iterations)
    - Produces cryptographic key

    Why?
    - Prevents rainbow table attacks
    - Slows down brute force attacks
    - Each password+salt combination produces unique key

    Args:
        password: User's password
        salt: Random bytes (16 bytes recommended)

    Returns:
        32-byte encryption key
    """
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,  ## Deliberately slow
    )
    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key)

## ============================================================================
## SECTION 2: Token Encryption/Decryption
## ============================================================================

def encrypt_token(token: str, password: str) -> dict:
    """
    Encrypt GitLab PAT with user's password.

    Process:
    1. Generate random salt
    2. Derive encryption key from password + salt
    3. Encrypt token with key
    4. Return encrypted token + salt

    Args:
        token: GitLab Personal Access Token (plain text)
        password: User's app password

    Returns:
        {
            'encrypted_token': base64_string,
            'salt': base64_string
        }
    """
    ## Generate random salt
    salt = os.urandom(16)

    ## Derive key from password
    key = derive_key_from_password(password, salt)

    ## Create Fernet cipher
    cipher = Fernet(key)

    ## Encrypt token
    encrypted = cipher.encrypt(token.encode())

    return {
        'encrypted_token': base64.urlsafe_b64encode(encrypted).decode('utf-8'),
        'salt': base64.urlsafe_b64encode(salt).decode('utf-8')
    }

def decrypt_token(encrypted_token: str, salt: str, password: str) -> Optional[str]:
    """
    Decrypt GitLab PAT using user's password.

    Args:
        encrypted_token: Base64 encoded encrypted token
        salt: Base64 encoded salt
        password: User's app password

    Returns:
        Decrypted token string, or None if decryption fails
    """
    try:
        ## Decode from base64
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_token)
        salt_bytes = base64.urlsafe_b64decode(salt)

        ## Derive key from password
        key = derive_key_from_password(password, salt_bytes)

        ## Create cipher
        cipher = Fernet(key)

        ## Decrypt
        decrypted = cipher.decrypt(encrypted_bytes)

        return decrypted.decode('utf-8')

    except (InvalidToken, Exception) as e:
        ## Wrong password or corrupted data
        return None

## ============================================================================
## SECTION 3: Testing Encryption
## ============================================================================

if __name__ == "__main__":
    """Test encryption/decryption"""

    ## Simulate GitLab PAT
    original_token = "glpat-xxxxxxxxxxxxxxxxxxxx"
    user_password = "MySecurePassword123!"

    print("=== Token Encryption Test ===")
    print(f"Original token: {original_token}")
    print(f"User password: {user_password}")

    ## Encrypt
    encrypted_data = encrypt_token(original_token, user_password)
    print(f"\nEncrypted token: {encrypted_data['encrypted_token'][:50]}...")
    print(f"Salt: {encrypted_data['salt']}")

    ## Decrypt with correct password
    decrypted = decrypt_token(
        encrypted_data['encrypted_token'],
        encrypted_data['salt'],
        user_password
    )
    print(f"\nDecrypted token: {decrypted}")
    print(f"Match: {decrypted == original_token}")

    ## Try with wrong password
    wrong_decrypted = decrypt_token(
        encrypted_data['encrypted_token'],
        encrypted_data['salt'],
        "WrongPassword"
    )
    print(f"\nDecryption with wrong password: {wrong_decrypted}")
```

---

### 8.6: GitLab-Aware User Service

**Update `backend/app/services/auth_service.py`:**

```python
"""
Authentication service with GitLab integration.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from pathlib import Path
import json

from passlib.context import CryptContext
from jose import JWTError, jwt

from app.config import settings
from app.schemas.auth import UserInDB, User
from app.utils.file_locking import LockedFile
from app.services.gitlab_service import GitLabService
from app.services.gitlab_sync_service import GitLabSyncService
from app.utils.encryption import encrypt_token, decrypt_token

## Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password with bcrypt."""
    return pwd_context.hash(password)

## JWT token functions remain the same...
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decode JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None

## ============================================================================
## SECTION 3: GitLab-Aware User Service
## ============================================================================

class UserService:
    """
    User management with GitLab integration.

    Supports two authentication modes:
    1. GitLab PAT authentication
    2. Local password authentication
    """

    def __init__(
        self,
        users_file: Optional[Path] = None,
        gitlab_sync: Optional[GitLabSyncService] = None
    ):
        """
        Initialize user service.

        Args:
            users_file: Path to users.json (legacy mode)
            gitlab_sync: GitLab sync service (GitLab mode)
        """
        self.users_file = users_file
        self.gitlab_sync = gitlab_sync
        self.gitlab_service = GitLabService()

        ## Determine which storage to use
        self.use_gitlab = gitlab_sync is not None and settings.GITLAB_ENABLED

        if not self.use_gitlab and users_file:
            ## Legacy mode: local users.json
            if not self.users_file.exists():
                self.users_file.write_text('{}')

    def load_users(self) -> dict:
        """
        Load users from storage.

        Returns:
            Dict mapping username to user data
        """
        if self.use_gitlab:
            ## Pull latest from GitLab first
            self.gitlab_sync.pull()

            ## Load users.json from GitLab clone
            return self.gitlab_sync.load_json_file('users.json')
        else:
            ## Legacy: load from local file
            try:
                with LockedFile(self.users_file, 'r') as f:
                    content = f.read()
                    if not content.strip():
                        return {}
                    return json.loads(content)
            except Exception:
                return {}

    def save_users(self, users: dict):
        """
        Save users to storage.

        Args:
            users: Dict mapping username to user data
        """
        if self.use_gitlab:
            ## Save to GitLab clone
            self.gitlab_sync.save_json_file('users.json', users)

            ## Commit and push to GitLab
            self.gitlab_sync.commit_and_push(
                files=['users.json'],
                message="Update user database",
                author_name=settings.GIT_USER_NAME,
                author_email=settings.GIT_USER_EMAIL
            )
        else:
            ## Legacy: save to local file
            with LockedFile(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)

    def get_user(self, username: str) -> Optional[UserInDB]:
        """
        Get user by username.

        Returns:
            UserInDB model or None
        """
        users = self.load_users()
        user_data = users.get(username)

        if user_data:
            return UserInDB(**user_data)
        return None

    def create_user(
        self,
        username: str,
        password: str,
        full_name: str,
        role: str = "user",
        gitlab_token: Optional[str] = None
    ):
        """
        Create a new user.

        Args:
            username: Username
            password: App password (will be hashed)
            full_name: Full name
            role: User role ('admin' or 'user')
            gitlab_token: GitLab PAT (optional, will be encrypted)

        Raises:
            ValueError: If username exists or GitLab token invalid
        """
        users = self.load_users()

        if username in users:
            raise ValueError(f"Username '{username}' already exists")

        ## Validate GitLab token if provided
        if gitlab_token and self.use_gitlab:
            user_info = self.gitlab_service.validate_token(gitlab_token)
            if not user_info:
                raise ValueError("Invalid GitLab token")

            ## Check if token username matches requested username
            if user_info['username'] != username:
                raise ValueError(
                    f"GitLab username '{user_info['username']}' "
                    f"doesn't match requested username '{username}'"
                )

        ## Hash password
        password_hash = get_password_hash(password)

        ## Prepare user data
        user_data = {
            "username": username,
            "password_hash": password_hash,
            "full_name": full_name,
            "role": role
        }

        ## Encrypt and store GitLab token if provided
        if gitlab_token:
            encrypted_data = encrypt_token(gitlab_token, password)
            user_data['encrypted_gitlab_token'] = encrypted_data['encrypted_token']
            user_data['token_salt'] = encrypted_data['salt']

        ## Save user
        users[username] = user_data
        self.save_users(users)

    def authenticate_user(
        self,
        username: str,
        password: str
    ) -> Optional[UserInDB]:
        """
        Authenticate user with username and password.

        Returns:
            UserInDB if successful, None otherwise
        """
        user = self.get_user(username)

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    def authenticate_with_gitlab_token(
        self,
        username: str,
        gitlab_token: str
    ) -> Optional[UserInDB]:
        """
        Authenticate user with GitLab Personal Access Token.

        Args:
            username: Username
            gitlab_token: GitLab PAT

        Returns:
            UserInDB if successful, None otherwise
        """
        ## Validate token with GitLab API
        user_info = self.gitlab_service.validate_token(gitlab_token)
        if not user_info:
            return None

        ## Check if username matches
        if user_info['username'] != username:
            return None

        ## Get or create user
        user = self.get_user(username)

        if not user:
            ## Auto-register user from GitLab
            ## Generate random password (user won't use it)
            import secrets
            temp_password = secrets.token_urlsafe(32)

            self.create_user(
                username=username,
                password=temp_password,
                full_name=user_info['name'],
                role='user',
                gitlab_token=gitlab_token
            )

            user = self.get_user(username)

        return user

    def get_gitlab_token(self, username: str, password: str) -> Optional[str]:
        """
        Retrieve decrypted GitLab token for a user.

        Args:
            username: Username
            password: User's app password

        Returns:
            Decrypted GitLab PAT, or None if not available
        """
        user = self.get_user(username)
        if not user:
            return None

        ## Check if user has encrypted token stored
        users = self.load_users()
        user_data = users.get(username, {})

        encrypted_token = user_data.get('encrypted_gitlab_token')
        salt = user_data.get('token_salt')

        if not encrypted_token or not salt:
            return None

        ## Decrypt token
        return decrypt_token(encrypted_token, salt, password)

    def create_default_users(self):
        """Create default admin user."""
        users = self.load_users()

        if users:
            return  ## Users already exist

        ## Create admin
        self.create_user(
            username="admin",
            password="Admin123!",
            full_name="Administrator",
            role="admin"
        )
```

---

### 8.7: Messaging System

**File: `backend/app/services/message_service.py`:**

```python
"""
Messaging system for user communication.

Messages are stored in GitLab repo as messages.json.
"""

from pathlib import Path
from typing import List, Dict, Optional
import json
from datetime import datetime, timezone
import logging

from app.services.gitlab_sync_service import GitLabSyncService
from app.utils.file_locking import LockedFile

logger = logging.getLogger(__name__)

## ============================================================================
## SECTION 1: Message Service
## ============================================================================

class MessageService:
    """
    Manages user messages stored in GitLab.

    Message structure:
    {
        "id": "uuid",
        "from_user": "alice",
        "to_user": "bob",  ## or "all" for broadcast
        "subject": "About PN1001",
        "body": "Message content...",
        "timestamp": "2025-01-01T12:00:00Z",
        "read": false,
        "related_file": "PN1001.mcam"  ## optional
    }
    """

    def __init__(
        self,
        messages_file: Optional[Path] = None,
        gitlab_sync: Optional[GitLabSyncService] = None
    ):
        """
        Initialize message service.

        Args:
            messages_file: Path to messages.json (legacy)
            gitlab_sync: GitLab sync service (preferred)
        """
        self.messages_file = messages_file
        self.gitlab_sync = gitlab_sync
        self.use_gitlab = gitlab_sync is not None

        if not self.use_gitlab and messages_file:
            if not messages_file.exists():
                messages_file.write_text('[]')

    def load_messages(self) -> List[Dict]:
        """
        Load all messages.

        Returns:
            List of message dicts
        """
        if self.use_gitlab:
            ## Pull latest from GitLab
            self.gitlab_sync.pull()

            ## Load messages.json
            messages = self.gitlab_sync.load_json_file('messages.json')

            ## Handle both dict and list formats
            if isinstance(messages, dict):
                return messages.get('messages', [])
            return messages if isinstance(messages, list) else []
        else:
            ## Legacy: local file
            try:
                with LockedFile(self.messages_file, 'r') as f:
                    content = f.read()
                    if not content.strip():
                        return []
                    return json.loads(content)
            except Exception:
                return []

    def save_messages(self, messages: List[Dict]):
        """
        Save messages.

        Args:
            messages: List of message dicts
        """
        if self.use_gitlab:
            ## Save to GitLab clone
            self.gitlab_sync.save_json_file('messages.json', messages)

            ## Commit and push
            self.gitlab_sync.commit_and_push(
                files=['messages.json'],
                message="Update messages",
                author_name="PDM System",
                author_email="pdm@system.local"
            )
        else:
            ## Legacy: local file
            with LockedFile(self.messages_file, 'w') as f:
                json.dump(messages, f, indent=2)

    def send_message(
        self,
        from_user: str,
        to_user: str,
        subject: str,
        body: str,
        related_file: Optional[str] = None
    ) -> str:
        """
        Send a message.

        Args:
            from_user: Sender username
            to_user: Recipient username (or "all" for broadcast)
            subject: Message subject
            body: Message body
            related_file: Optional related filename

        Returns:
            Message ID (UUID)
        """
        import uuid

        messages = self.load_messages()

        message = {
            'id': str(uuid.uuid4()),
            'from_user': from_user,
            'to_user': to_user,
            'subject': subject,
            'body': body,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'read': False,
            'related_file': related_file
        }

        messages.append(message)
        self.save_messages(messages)

        logger.info(f"Message sent from {from_user} to {to_user}: {subject}")

        return message['id']

    def get_messages_for_user(self, username: str) -> List[Dict]:
        """
        Get all messages for a specific user.

        Returns messages where:
        - to_user == username
        - OR to_user == "all" (broadcasts)

        Args:
            username: Username

        Returns:
            List of messages, newest first
        """
        messages = self.load_messages()

        user_messages = [
            msg for msg in messages
            if msg['to_user'] == username or msg['to_user'] == 'all'
        ]

        ## Sort by timestamp, newest first
        user_messages.sort(key=lambda m: m['timestamp'], reverse=True)

        return user_messages

    def get_unread_count(self, username: str) -> int:
        """
        Get count of unread messages for user.

        Args:
            username: Username

        Returns:
            Number of unread messages
        """
        messages = self.get_messages_for_user(username)
        return sum(1 for msg in messages if not msg.get('read', False))

    def mark_as_read(self, message_id: str, username: str):
        """
        Mark message as read.

        Args:
            message_id: Message ID
            username: User marking as read (must be recipient)
        """
        messages = self.load_messages()

        for msg in messages:
            if msg['id'] == message_id:
                ## Verify user is recipient
                if msg['to_user'] == username or msg['to_user'] == 'all':
                    msg['read'] = True
                    self.save_messages(messages)
                    break

    def delete_message(self, message_id: str, username: str):
        """
        Delete a message.

        Args:
            message_id: Message ID
            username: User deleting (must be sender or recipient)
        """
        messages = self.load_messages()

        messages = [
            msg for msg in messages
            if not (
                msg['id'] == message_id and
                (msg['from_user'] == username or msg['to_user'] == username)
            )
        ]

        self.save_messages(messages)

    def get_messages_for_file(self, filename: str) -> List[Dict]:
        """
        Get all messages related to a specific file.

        Args:
            filename: Filename

        Returns:
            List of messages related to file
        """
        messages = self.load_messages()

        return [
            msg for msg in messages
            if msg.get('related_file') == filename
        ]
```

---

### 8.8: Update API Authentication

**Update `backend/app/api/auth.py`:**

```python
"""
Authentication API with GitLab support.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Optional

from app.schemas.auth import Token, User, UserCreate
from app.services.auth_service import UserService, create_access_token
from app.services.gitlab_service import GitLabService
from app.api.deps import get_user_service, get_current_user
from app.config import settings

## ============================================================================
## SECTION 1: Router Setup
## ============================================================================

router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"]
)

## ============================================================================
## SECTION 2: Login Endpoints
## ============================================================================

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    """
    Login with username and password.

    Supports:
    - Local password authentication
    - GitLab PAT authentication
    """
    ## Try local password authentication first
    user = user_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    ## Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login-gitlab", response_model=Token)
def login_with_gitlab(
    username: str = Form(...),
    gitlab_token: str = Form(...),
    user_service: UserService = Depends(get_user_service)
):
    """
    Login with GitLab Personal Access Token.

    If user doesn't exist, auto-registers from GitLab.
    """
    if not settings.GITLAB_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GitLab authentication is disabled"
        )

    ## Authenticate with GitLab
    user = user_service.authenticate_with_gitlab_token(username, gitlab_token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid GitLab token or username",
            headers={"WWW-Authenticate": "Bearer"},
        )

    ## Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

## ============================================================================
## SECTION 3: Registration
## ============================================================================

@router.post("/register", response_model=User)
def register(
    user_data: UserCreate,
    gitlab_token: Optional[str] = None,
    user_service: UserService = Depends(get_user_service)
):
    """
    Register a new user.

    Optionally provide GitLab token for validation.
    """
    try:
        user_service.create_user(
            username=user_data.username,
            password=user_data.password,
            full_name=user_data.full_name,
            role=user_data.role,
            gitlab_token=gitlab_token
        )

        ## Return created user (without password)
        user = user_service.get_user(user_data.username)
        return User(
            username=user.username,
            full_name=user.full_name,
            role=user.role
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

## ============================================================================
## SECTION 4: User Info
## ============================================================================

@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information."""
    return current_user

@router.get("/validate-gitlab-token")
def validate_gitlab_token(
    token: str,
    gitlab_service: GitLabService = Depends()
):
    """
    Validate a GitLab Personal Access Token.

    Returns user info if valid.
    """
    user_info = gitlab_service.validate_token(token)

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid GitLab token"
        )

    return user_info
```

---

### 8.9: Messaging API

**File: `backend/app/api/messages.py`:**

```python
"""
Messaging API endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from pydantic import BaseModel, Field

from app.schemas.auth import User
from app.services.message_service import MessageService
from app.api.deps import get_current_user

## ============================================================================
## SECTION 1: Schemas
## ============================================================================

class MessageCreate(BaseModel):
    """Schema for creating a message."""
    to_user: str = Field(..., description="Recipient username or 'all' for broadcast")
    subject: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1, max_length=5000)
    related_file: str | None = Field(None, description="Related filename")

class Message(BaseModel):
    """Message response schema."""
    id: str
    from_user: str
    to_user: str
    subject: str
    body: str
    timestamp: str
    read: bool
    related_file: str | None = None

## ============================================================================
## SECTION 2: Router Setup
## ============================================================================

router = APIRouter(
    prefix="/api/messages",
    tags=["messages"],
)

## ============================================================================
## SECTION 3: Dependency Injection
## ============================================================================

def get_message_service() -> MessageService:
    """Get message service instance."""
    from app.config import settings

    if settings.GITLAB_ENABLED:
        ## Use GitLab sync
        from app.services.gitlab_sync_service import GitLabSyncService

        ## Get GitLab token from current request context
        ## For now, use a system token
        ## TODO: Get user's token from session
        gitlab_sync = GitLabSyncService(
            clone_path=settings.GITLAB_CLONE_PATH,
            repo_url=settings.GITLAB_REPO_URL,
            token="system-token"  ## TODO: Use user token
        )

        return MessageService(gitlab_sync=gitlab_sync)
    else:
        ## Legacy mode
        messages_file = settings.BASE_DIR / 'messages.json'
        return MessageService(messages_file=messages_file)

## ============================================================================
## SECTION 4: Message Endpoints
## ============================================================================

@router.get("/", response_model=List[Message])
def get_my_messages(
    current_user: User = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
):
    """
    Get all messages for current user.

    Returns messages where user is recipient, newest first.
    """
    try:
        messages = message_service.get_messages_for_user(current_user.username)
        return messages

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load messages: {str(e)}"
        )

@router.get("/unread-count")
def get_unread_count(
    current_user: User = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
):
    """Get count of unread messages."""
    try:
        count = message_service.get_unread_count(current_user.username)
        return {"unread_count": count}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to count messages: {str(e)}"
        )

@router.post("/send")
def send_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
):
    """Send a message to another user or broadcast to all."""
    try:
        message_id = message_service.send_message(
            from_user=current_user.username,
            to_user=message.to_user,
            subject=message.subject,
            body=message.body,
            related_file=message.related_file
        )

        return {
            "success": True,
            "message_id": message_id,
            "message": "Message sent successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {str(e)}"
        )

@router.post("/{message_id}/mark-read")
def mark_message_read(
    message_id: str,
    current_user: User = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
):
    """Mark a message as read."""
    try:
        message_service.mark_as_read(message_id, current_user.username)
        return {"success": True}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark as read: {str(e)}"
        )

@router.delete("/{message_id}")
def delete_message(
    message_id: str,
    current_user: User = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
):
    """Delete a message."""
    try:
        message_service.delete_message(message_id, current_user.username)
        return {"success": True, "message": "Message deleted"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete message: {str(e)}"
        )

@router.get("/file/{filename}")
def get_file_messages(
    filename: str,
    current_user: User = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
):
    """Get all messages related to a specific file."""
    try:
        messages = message_service.get_messages_for_file(filename)
        return {"filename": filename, "messages": messages}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load file messages: {str(e)}"
        )
```

**Update `backend/app/main.py` to include messages router:**

```python
## Add import
from app.api import files, auth, version_control, messages

## Include router
app.include_router(messages.router)
```

---

### 8.10: Update Dependencies for GitLab Mode

**Update `backend/app/api/deps.py`:**

```python
"""
Dependencies with GitLab support.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pathlib import Path

from app.schemas.auth import User
from app.services.auth_service import decode_access_token, UserService
from app.services.file_service import FileService
from app.services.gitlab_sync_service import GitLabSyncService
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

## ============================================================================
## SECTION 1: GitLab Sync Dependency
## ============================================================================

def get_gitlab_sync(token: str = Depends(oauth2_scheme)) -> GitLabSyncService:
    """
    Get GitLab sync service with user's token.

    In production, this would use the user's stored GitLab token.
    For now, we'll implement a simplified version.
    """
    if not settings.GITLAB_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GitLab integration is disabled"
        )

    ## TODO: Retrieve user's encrypted GitLab token from storage
    ## For now, use a placeholder
    gitlab_sync = GitLabSyncService(
        clone_path=settings.GITLAB_CLONE_PATH,
        repo_url=settings.GITLAB_REPO_URL,
        token="placeholder-token"  ## TODO: Get from user
    )

    return gitlab_sync

## ============================================================================
## SECTION 2: Service Dependencies
## ============================================================================

def get_user_service() -> UserService:
    """Get user service instance."""
    if settings.GITLAB_ENABLED:
        ## Use GitLab sync
        try:
            gitlab_sync = get_gitlab_sync()
            return UserService(gitlab_sync=gitlab_sync)
        except:
            ## Fallback to local if GitLab fails
            pass

    ## Legacy mode
    users_file = settings.BASE_DIR / 'users.json'
    return UserService(users_file=users_file)

def get_file_service() -> FileService:
    """Get file service instance."""
    repo_path = settings.BASE_DIR / 'repo'
    locks_file = settings.BASE_DIR / 'locks.json'
    audit_file = settings.BASE_DIR / 'audit.json'
    git_repo_path = settings.GIT_REPO_PATH

    return FileService(repo_path, locks_file, audit_file, git_repo_path)

## ============================================================================
## SECTION 3: Authentication
## ============================================================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user_in_db = user_service.get_user(username)
    if user_in_db is None:
        raise credentials_exception

    return User(
        username=user_in_db.username,
        full_name=user_in_db.full_name,
        role=user_in_db.role
    )

## Keep existing role-based dependencies...
def require_role(allowed_roles: list[str]):
    """Role-based authorization."""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires role: {allowed_roles}"
            )
        return current_user
    return role_checker

require_admin = require_role(["admin"])
require_user = require_role(["admin", "user"])
```

---

### Stage 8 Part 2 Complete

**What we've built:**

- ✅ Encrypted token storage (Fernet encryption)
- ✅ GitLab PAT authentication
- ✅ User registration with GitLab validation
- ✅ Messaging system stored in GitLab
- ✅ GitLab-aware user service
- ✅ Messaging API endpoints
- ✅ Hybrid mode support (local vs GitLab)

**File structure:**

```
backend/
├── app/
│   ├── utils/
│   │   └── encryption.py           ## NEW
│   ├── services/
│   │   ├── gitlab_service.py       ## NEW
│   │   ├── gitlab_sync_service.py  ## NEW
│   │   ├── message_service.py      ## NEW
│   │   └── auth_service.py         ## UPDATED
│   ├── api/
│   │   ├── messages.py             ## NEW
│   │   ├── auth.py                 ## UPDATED
│   │   └── deps.py                 ## UPDATED
│   └── config.py                   ## UPDATED
```

**Next: Stage 8 Part 3 will cover:**

- Frontend updates for GitLab login
- Message UI
- Configuration management
- PyInstaller packaging
- Testing both standalone and server modes

Ready for Part 3?

## Stage 8 - Part 3: Frontend Integration & Deployment

---

### 8.11: Frontend - GitLab Login UI

**Update `backend/static/login.html`:**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Login - PDM System</title>
    <link rel="stylesheet" href="/static/css/main.css" />

    <style>
      body {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background: linear-gradient(
          135deg,
          var(--color-primary-500),
          var(--color-primary-700)
        );
      }

      .login-card {
        background: var(--card-bg);
        padding: var(--spacing-8);
        border-radius: var(--card-border-radius);
        box-shadow: var(--shadow-xl);
        width: 90%;
        max-width: 450px;
        border: 1px solid var(--border-default);
      }

      .login-header {
        text-align: center;
        margin-bottom: var(--spacing-6);
      }

      .login-header h1 {
        color: var(--color-primary-500);
        margin-bottom: var(--spacing-2);
      }

      .error-message {
        background: var(--status-danger-bg);
        color: var(--status-danger-text);
        padding: var(--spacing-3);
        border-radius: var(--radius-base);
        margin-bottom: var(--spacing-4);
        font-size: var(--font-size-sm);
        display: none;
      }

      .error-message.show {
        display: block;
      }

      .login-tabs {
        display: flex;
        gap: var(--spacing-2);
        margin-bottom: var(--spacing-6);
        border-bottom: 2px solid var(--border-default);
      }

      .tab-button {
        flex: 1;
        padding: var(--spacing-3);
        background: none;
        border: none;
        border-bottom: 3px solid transparent;
        color: var(--text-secondary);
        font-weight: var(--font-weight-medium);
        cursor: pointer;
        transition: all var(--transition-fast);
        margin-bottom: -2px;
      }

      .tab-button.active {
        color: var(--interactive-primary);
        border-bottom-color: var(--interactive-primary);
      }

      .tab-button:hover {
        color: var(--interactive-primary-hover);
      }

      .tab-content {
        display: none;
      }

      .tab-content.active {
        display: block;
      }

      .demo-credentials {
        margin-top: var(--spacing-6);
        padding-top: var(--spacing-6);
        border-top: 1px solid var(--border-default);
        text-align: center;
        font-size: var(--font-size-sm);
        color: var(--text-secondary);
      }

      .demo-credentials code {
        font-size: var(--font-size-sm);
      }

      .info-box {
        background: var(--status-info-bg);
        color: var(--status-info-text);
        padding: var(--spacing-3);
        border-radius: var(--radius-base);
        margin-bottom: var(--spacing-4);
        font-size: var(--font-size-sm);
      }

      .info-box a {
        color: var(--status-info-text);
        text-decoration: underline;
        font-weight: var(--font-weight-semibold);
      }
    </style>
  </head>
  <body>
    <div class="login-card">
      <div class="login-header">
        <h1>PDM System</h1>
        <p>Parts Data Management</p>
      </div>

      <div class="login-tabs">
        <button class="tab-button active" data-tab="password">Password</button>
        <button class="tab-button" data-tab="gitlab">GitLab Token</button>
      </div>

      <div id="error-message" class="error-message"></div>

      <!-- Password Login Tab -->
      <div id="password-tab" class="tab-content active">
        <form id="password-login-form">
          <div class="form-group">
            <label for="password-username">Username</label>
            <input
              type="text"
              id="password-username"
              name="username"
              required
              autofocus
              autocomplete="username"
            />
          </div>

          <div class="form-group">
            <label for="password-password">Password</label>
            <input
              type="password"
              id="password-password"
              name="password"
              required
              autocomplete="current-password"
            />
          </div>

          <button type="submit" class="btn btn-primary" style="width: 100%;">
            Login
          </button>
        </form>
      </div>

      <!-- GitLab Token Login Tab -->
      <div id="gitlab-tab" class="tab-content">
        <div class="info-box">
          Login with your GitLab Personal Access Token (PAT).
          <br />
          <a
            href="https://gitlab.com/-/profile/personal_access_tokens"
            target="_blank"
          >
            Generate token →
          </a>
        </div>

        <form id="gitlab-login-form">
          <div class="form-group">
            <label for="gitlab-username">GitLab Username</label>
            <input
              type="text"
              id="gitlab-username"
              name="username"
              required
              autocomplete="username"
              placeholder="your-gitlab-username"
            />
          </div>

          <div class="form-group">
            <label for="gitlab-token">Personal Access Token</label>
            <input
              type="password"
              id="gitlab-token"
              name="token"
              required
              placeholder="glpat-xxxxxxxxxxxxxxxxxxxx"
            />
            <small
              style="color: var(--text-secondary); font-size: var(--font-size-xs);"
            >
              Required scopes: api, read_repository, write_repository
            </small>
          </div>

          <button type="submit" class="btn btn-primary" style="width: 100%;">
            Login with GitLab
          </button>
        </form>
      </div>

      <div class="demo-credentials">
        <p><strong>Demo Credentials:</strong></p>
        <p>Admin: <code>admin</code> / <code>Admin123!</code></p>
        <p>User: <code>john</code> / <code>Password123!</code></p>
      </div>
    </div>

    <script type="module" src="/static/js/login.js"></script>
  </body>
</html>
```

**Update `backend/static/js/login.js`:**

```javascript
/**
 * Login Page with GitLab Support
 */

// ============================================================================
// SECTION 1: Tab Switching
// ============================================================================

document.querySelectorAll(".tab-button").forEach((button) => {
  button.addEventListener("click", () => {
    const tabName = button.dataset.tab;

    // Update buttons
    document.querySelectorAll(".tab-button").forEach((b) => {
      b.classList.remove("active");
    });
    button.classList.add("active");

    // Update content
    document.querySelectorAll(".tab-content").forEach((content) => {
      content.classList.remove("active");
    });
    document.getElementById(`${tabName}-tab`).classList.add("active");

    // Clear error
    document.getElementById("error-message").classList.remove("show");
  });
});

// ============================================================================
// SECTION 2: Password Login
// ============================================================================

document
  .getElementById("password-login-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("password-username").value;
    const password = document.getElementById("password-password").value;
    const errorDiv = document.getElementById("error-message");
    const submitBtn = e.target.querySelector('button[type="submit"]');

    errorDiv.classList.remove("show");
    submitBtn.disabled = true;
    submitBtn.textContent = "Logging in...";

    try {
      // OAuth2 password flow
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

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Login failed");
      }

      // Store token and user info
      localStorage.setItem("access_token", data.access_token);

      // Decode token to get user info
      const payload = JSON.parse(atob(data.access_token.split(".")[1]));
      localStorage.setItem("username", payload.sub);
      localStorage.setItem("user_role", payload.role);
      localStorage.setItem("auth_method", "password");

      // Redirect to main app
      window.location.href = "/";
    } catch (error) {
      errorDiv.textContent = error.message;
      errorDiv.classList.add("show");
      submitBtn.disabled = false;
      submitBtn.textContent = "Login";
    }
  });

// ============================================================================
// SECTION 3: GitLab Token Login
// ============================================================================

document
  .getElementById("gitlab-login-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("gitlab-username").value;
    const token = document.getElementById("gitlab-token").value;
    const errorDiv = document.getElementById("error-message");
    const submitBtn = e.target.querySelector('button[type="submit"]');

    errorDiv.classList.remove("show");
    submitBtn.disabled = true;
    submitBtn.textContent = "Authenticating with GitLab...";

    try {
      // GitLab authentication
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("gitlab_token", token);

      const response = await fetch("/api/auth/login-gitlab", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "GitLab authentication failed");
      }

      // Store token and user info
      localStorage.setItem("access_token", data.access_token);

      // Decode token
      const payload = JSON.parse(atob(data.access_token.split(".")[1]));
      localStorage.setItem("username", payload.sub);
      localStorage.setItem("user_role", payload.role);
      localStorage.setItem("auth_method", "gitlab");

      // Store GitLab token for this session (encrypted in backend)
      sessionStorage.setItem("gitlab_token", token);

      // Redirect
      window.location.href = "/";
    } catch (error) {
      errorDiv.textContent = error.message;
      errorDiv.classList.add("show");
      submitBtn.disabled = false;
      submitBtn.textContent = "Login with GitLab";
    }
  });
```

---

### 8.12: Frontend - Messaging UI

**Add message styles to `backend/static/css/components.css`:**

```css
/* =========================================================================
   MESSAGING UI
   ========================================================================= */

.messages-panel {
  position: fixed;
  top: 0;
  right: -400px;
  width: 400px;
  height: 100vh;
  background: var(--bg-primary);
  box-shadow: var(--shadow-xl);
  border-left: 1px solid var(--border-default);
  z-index: var(--z-modal);
  transition: right var(--transition-base);
  display: flex;
  flex-direction: column;
}

.messages-panel.open {
  right: 0;
}

.messages-header {
  padding: var(--spacing-4);
  border-bottom: 1px solid var(--border-default);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-secondary);
}

.messages-header h3 {
  margin: 0;
  color: var(--text-primary);
}

.messages-body {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-4);
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-3);
}

.message-item {
  padding: var(--spacing-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.message-item:hover {
  transform: translateX(-5px);
  box-shadow: var(--shadow-sm);
}

.message-item.unread {
  border-left: 4px solid var(--interactive-primary);
  background: var(--interactive-primary-alpha);
}

.message-from {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin-bottom: var(--spacing-1);
}

.message-subject {
  font-size: var(--font-size-base);
  color: var(--text-primary);
  margin-bottom: var(--spacing-2);
}

.message-preview {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.message-time {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  margin-top: var(--spacing-2);
}

.message-badge {
  background: var(--status-danger);
  color: var(--text-inverse);
  border-radius: var(--radius-full);
  padding: 0.125rem 0.5rem;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  min-width: 20px;
  text-align: center;
  display: inline-block;
}

.new-message-button {
  margin: var(--spacing-4);
  width: calc(100% - var(--spacing-8));
}

/* Message compose form */
.compose-form {
  padding: var(--spacing-4);
}

.compose-form .form-group {
  margin-bottom: var(--spacing-4);
}

/* Empty state */
.messages-empty {
  text-align: center;
  padding: var(--spacing-8);
  color: var(--text-secondary);
}

/* Mobile responsive */
@media (max-width: 768px) {
  .messages-panel {
    width: 100%;
    right: -100%;
  }
}
```

**Update `backend/static/index.html` - add messages panel and button:**

```html
<!-- In header-actions, add messages button -->
<button id="messages-toggle" class="btn btn-secondary btn-sm" title="Messages">
  📨
  <span id="message-badge" class="message-badge" style="display: none;">0</span>
</button>

<!-- Before closing body tag, add messages panel -->

<!-- Messages Panel -->
<div id="messages-panel" class="messages-panel">
  <div class="messages-header">
    <h3>Messages</h3>
    <button class="modal-close" id="close-messages">&times;</button>
  </div>

  <button class="btn btn-primary new-message-button" id="new-message-btn">
    ✉️ New Message
  </button>

  <div class="messages-body">
    <div id="messages-list"></div>
  </div>
</div>

<!-- New Message Modal -->
<div id="new-message-modal" class="modal-overlay hidden">
  <div class="modal-content">
    <div class="modal-header">
      <h3>New Message</h3>
      <button class="modal-close" type="button">&times;</button>
    </div>

    <div class="modal-body">
      <form id="new-message-form" class="compose-form">
        <div class="form-group">
          <label for="message-to">To</label>
          <input
            type="text"
            id="message-to"
            name="to_user"
            required
            placeholder="username or 'all' for broadcast"
          />
        </div>

        <div class="form-group">
          <label for="message-subject">Subject</label>
          <input
            type="text"
            id="message-subject"
            name="subject"
            required
            maxlength="200"
          />
        </div>

        <div class="form-group">
          <label for="message-body">Message</label>
          <textarea
            id="message-body"
            name="body"
            required
            rows="6"
            maxlength="5000"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="message-file">Related File (Optional)</label>
          <input
            type="text"
            id="message-file"
            name="related_file"
            placeholder="e.g., PN1001.mcam"
          />
        </div>

        <div class="modal-actions">
          <button
            type="button"
            class="btn btn-secondary"
            onclick="newMessageModal.close()"
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-primary">Send Message</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- View Message Modal -->
<div id="view-message-modal" class="modal-overlay hidden">
  <div class="modal-content">
    <div class="modal-header">
      <h3 id="view-message-subject"></h3>
      <button class="modal-close" type="button">&times;</button>
    </div>

    <div class="modal-body">
      <div style="margin-bottom: var(--spacing-4);">
        <strong>From:</strong> <span id="view-message-from"></span><br />
        <strong>Date:</strong> <span id="view-message-date"></span><br />
        <span id="view-message-file-info"></span>
      </div>

      <div id="view-message-body" style="white-space: pre-wrap;"></div>

      <div class="modal-actions" style="margin-top: var(--spacing-6);">
        <button class="btn btn-danger" id="delete-message-btn">Delete</button>
        <button class="btn btn-secondary" onclick="viewMessageModal.close()">
          Close
        </button>
      </div>
    </div>
  </div>
</div>
```

---

### 8.13: Frontend - Messaging JavaScript

**Update `backend/static/js/modules/api-client.js` - add message methods:**

```javascript
// Add these methods to APIClient class:

/**
 * Get messages for current user
 */
async getMessages() {
  return this.get('/api/messages/');
}

/**
 * Get unread message count
 */
async getUnreadCount() {
  return this.get('/api/messages/unread-count');
}

/**
 * Send a message
 */
async sendMessage(data) {
  return this.post('/api/messages/send', data);
}

/**
 * Mark message as read
 */
async markMessageRead(messageId) {
  return this.post(`/api/messages/${messageId}/mark-read`);
}

/**
 * Delete message
 */
async deleteMessage(messageId) {
  return this.delete(`/api/messages/${messageId}`);
}

/**
 * Get messages for a file
 */
async getFileMessages(filename) {
  return this.get(`/api/messages/file/${encodeURIComponent(filename)}`);
}
```

**Update `backend/static/js/app.js` - add messaging functionality:**

```javascript
// Add after modal instances
const newMessageModal = new ModalManager("new-message-modal");
const viewMessageModal = new ModalManager("view-message-modal");

let currentViewMessage = null;

// ============================================================================
// SECTION: Messages Panel
// ============================================================================

function toggleMessagesPanel() {
  const panel = document.getElementById("messages-panel");
  panel.classList.toggle("open");

  if (panel.classList.contains("open")) {
    loadMessages();
  }
}

async function loadMessages() {
  const container = document.getElementById("messages-list");
  container.innerHTML = '<div class="loading"><p>Loading messages...</p></div>';

  try {
    const data = await apiClient.getMessages();

    if (data.length === 0) {
      container.innerHTML = `
        <div class="messages-empty">
          <p>No messages yet.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = `
      <div class="message-list">
        ${data.map((msg) => createMessageElement(msg)).join("")}
      </div>
    `;

    // Wire up click handlers
    data.forEach((msg) => {
      const el = document.getElementById(`message-${msg.id}`);
      if (el) {
        el.onclick = () => viewMessage(msg);
      }
    });
  } catch (error) {
    container.innerHTML = `
      <div class="messages-empty" style="color: var(--status-danger-text);">
        <p>Error loading messages: ${error.message}</p>
      </div>
    `;
  }
}

function createMessageElement(message) {
  const date = new Date(message.timestamp);
  const isUnread = !message.read;

  return `
    <div class="message-item ${isUnread ? "unread" : ""}" id="message-${
    message.id
  }">
      <div class="message-from">
        ${
          message.from_user === "all"
            ? "📢 Broadcast"
            : "👤 " + message.from_user
        }
      </div>
      <div class="message-subject">${escapeHtml(message.subject)}</div>
      <div class="message-preview">${escapeHtml(
        message.body.substring(0, 100)
      )}...</div>
      <div class="message-time">${date.toLocaleString()}</div>
    </div>
  `;
}

async function viewMessage(message) {
  currentViewMessage = message;

  document.getElementById("view-message-subject").textContent = message.subject;
  document.getElementById("view-message-from").textContent = message.from_user;
  document.getElementById("view-message-date").textContent = new Date(
    message.timestamp
  ).toLocaleString();
  document.getElementById("view-message-body").textContent = message.body;

  const fileInfo = document.getElementById("view-message-file-info");
  if (message.related_file) {
    fileInfo.innerHTML = `<strong>Related File:</strong> ${message.related_file}<br>`;
  } else {
    fileInfo.innerHTML = "";
  }

  viewMessageModal.open();

  // Mark as read
  if (!message.read) {
    try {
      await apiClient.markMessageRead(message.id);
      loadMessages();
      updateUnreadCount();
    } catch (error) {
      console.error("Failed to mark as read:", error);
    }
  }
}

async function sendNewMessage(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const data = {
    to_user: formData.get("to_user"),
    subject: formData.get("subject"),
    body: formData.get("body"),
    related_file: formData.get("related_file") || null,
  };

  try {
    await apiClient.sendMessage(data);
    toast.success("Message sent successfully!");
    newMessageModal.close();
    loadMessages();
  } catch (error) {
    toast.error(error.message);
  }
}

async function deleteCurrentMessage() {
  if (!currentViewMessage) return;

  if (!confirm("Delete this message?")) return;

  try {
    await apiClient.deleteMessage(currentViewMessage.id);
    toast.success("Message deleted");
    viewMessageModal.close();
    loadMessages();
    updateUnreadCount();
  } catch (error) {
    toast.error(error.message);
  }
}

async function updateUnreadCount() {
  try {
    const data = await apiClient.getUnreadCount();
    const badge = document.getElementById("message-badge");

    if (data.unread_count > 0) {
      badge.textContent = data.unread_count;
      badge.style.display = "inline-block";
    } else {
      badge.style.display = "none";
    }
  } catch (error) {
    console.error("Failed to update unread count:", error);
  }
}

// ============================================================================
// SECTION: Update Initialization
// ============================================================================

document.addEventListener("DOMContentLoaded", () => {
  console.log("PDM App initialized with messaging");

  const userRole = localStorage.getItem("user_role");
  const username = localStorage.getItem("username");

  // ... existing initialization ...

  // Messages panel toggle
  document
    .getElementById("messages-toggle")
    .addEventListener("click", toggleMessagesPanel);
  document
    .getElementById("close-messages")
    .addEventListener("click", toggleMessagesPanel);

  // New message button
  document.getElementById("new-message-btn").addEventListener("click", () => {
    newMessageModal.open();
  });

  // New message form
  document
    .getElementById("new-message-form")
    .addEventListener("submit", sendNewMessage);

  // Delete message button
  document
    .getElementById("delete-message-btn")
    .addEventListener("click", deleteCurrentMessage);

  // Update unread count
  updateUnreadCount();
  setInterval(updateUnreadCount, 30000); // Check every 30 seconds

  // ... rest of initialization ...
});
```

---

### 8.14: Configuration Manager

**File: `backend/app/config_manager.py`:**

```python
"""
Configuration management for hybrid deployment.

Handles loading config from file and environment variables.
"""

import yaml
from pathlib import Path
from typing import Optional, Dict
import os

## ============================================================================
## SECTION 1: Configuration Schema
## ============================================================================

DEFAULT_CONFIG = {
    'mode': 'server',  ## 'standalone' or 'server'
    'gitlab': {
        'enabled': True,
        'url': 'https://gitlab.com',
        'repo_url': '',
        'branch': 'main',
        'lfs_enabled': True,
    },
    'server': {
        'host': '0.0.0.0',
        'port': 8000,
        'sync_interval': 60,
    },
    'security': {
        'secret_key': '',
        'encryption_key': '',
    },
    'paths': {
        'clone_path': './gitlab_repo_clone',
    }
}

## ============================================================================
## SECTION 2: Config Manager
## ============================================================================

class ConfigManager:
    """
    Manages application configuration.

    Priority (highest to lowest):
    1. Environment variables
    2. config.yaml file
    3. Default values
    """

    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize config manager.

        Args:
            config_file: Path to config.yaml (optional)
        """
        self.config_file = config_file or Path('config.yaml')
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load configuration from all sources."""
        ## Start with defaults
        config = DEFAULT_CONFIG.copy()

        ## Load from file if exists
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                file_config = yaml.safe_load(f) or {}
                self._merge_config(config, file_config)

        ## Override with environment variables
        self._load_from_env(config)

        return config

    def _merge_config(self, base: Dict, override: Dict):
        """Recursively merge configuration dictionaries."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def _load_from_env(self, config: Dict):
        """Load configuration from environment variables."""
        ## Mode
        if os.getenv('MODE'):
            config['mode'] = os.getenv('MODE')

        ## GitLab
        if os.getenv('GITLAB_ENABLED'):
            config['gitlab']['enabled'] = os.getenv('GITLAB_ENABLED').lower() == 'true'
        if os.getenv('GITLAB_URL'):
            config['gitlab']['url'] = os.getenv('GITLAB_URL')
        if os.getenv('GITLAB_REPO_URL'):
            config['gitlab']['repo_url'] = os.getenv('GITLAB_REPO_URL')
        if os.getenv('GITLAB_BRANCH'):
            config['gitlab']['branch'] = os.getenv('GITLAB_BRANCH')

        ## Server
        if os.getenv('HOST'):
            config['server']['host'] = os.getenv('HOST')
        if os.getenv('PORT'):
            config['server']['port'] = int(os.getenv('PORT'))

        ## Security
        if os.getenv('SECRET_KEY'):
            config['security']['secret_key'] = os.getenv('SECRET_KEY')
        if os.getenv('ENCRYPTION_KEY'):
            config['security']['encryption_key'] = os.getenv('ENCRYPTION_KEY')

    def save_config(self):
        """Save current configuration to file."""
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def get(self, key_path: str, default=None):
        """
        Get configuration value by dot-notation path.

        Example:
            config.get('gitlab.repo_url')
            config.get('server.port')
        """
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path: str, value):
        """
        Set configuration value by dot-notation path.

        Example:
            config.set('gitlab.repo_url', 'https://...')
        """
        keys = key_path.split('.')
        target = self.config

        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]

        target[keys[-1]] = value

    def is_standalone_mode(self) -> bool:
        """Check if running in standalone mode."""
        return self.config['mode'] == 'standalone'

    def is_gitlab_enabled(self) -> bool:
        """Check if GitLab integration is enabled."""
        return self.config['gitlab']['enabled']

## ============================================================================
## SECTION 3: Singleton Instance
## ============================================================================

## Global config instance
config_manager = ConfigManager()
```

**Create example `config.yaml`:**

```yaml
## PDM System Configuration

## Deployment mode: 'standalone' or 'server'
mode: server

## GitLab Integration
gitlab:
  enabled: true
  url: https://gitlab.com
  repo_url: https://gitlab.com/your-username/pdm-files.git
  branch: main
  lfs_enabled: true

## Server Configuration
server:
  host: 0.0.0.0
  port: 8000
  sync_interval: 60 ## seconds

## Security (leave empty, use environment variables)
security:
  secret_key: ""
  encryption_key: ""

## Paths
paths:
  clone_path: ./gitlab_repo_clone
```

---

### 8.15: PyInstaller Packaging

**File: `backend/pdm_app.py` - Standalone app entry point:**

```python
"""
PDM System - Standalone Application Entry Point

This script is used for PyInstaller packaging.
It starts an embedded FastAPI server and opens the browser.
"""

import sys
import webbrowser
import threading
import time
from pathlib import Path

## Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.main import app
from app.config import settings
import uvicorn

## ============================================================================
## SECTION 1: Standalone Mode
## ============================================================================

def run_server():
    """Run FastAPI server."""
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level="info"
    )

def open_browser():
    """Open browser after server starts."""
    time.sleep(2)  ## Wait for server to start
    webbrowser.open(f'http://127.0.0.1:{settings.PORT}')

def main():
    """Main entry point for standalone app."""
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║                PDM System - Standalone Mode              ║
    ║                                                          ║
    ║  Server starting on http://127.0.0.1:{settings.PORT}              ║
    ║  Browser will open automatically...                      ║
    ║                                                          ║
    ║  Press Ctrl+C to stop the server                         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    ## Start browser opener in background
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    ## Run server (blocking)
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nShutting down PDM System...")
        sys.exit(0)

if __name__ == '__main__':
    main()
```

**Create PyInstaller spec file: `backend/pdm.spec`:**

```python
## -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['pdm_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('static', 'static'),
        ('app', 'app'),
        ('config.yaml', '.'),
    ],
    hiddenimports=[
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'passlib.handlers.bcrypt',
        'git',
        'gitlab',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDM_System',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  ## Optional: add your icon
)
```

**Create build script: `backend/build_standalone.py`:**

```python
"""
Build script for creating standalone executable.
"""

import subprocess
import sys
from pathlib import Path

def build():
    """Build standalone executable with PyInstaller."""

    print("Building PDM System standalone executable...")
    print("=" * 60)

    ## Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    ## Run PyInstaller
    spec_file = Path(__file__).parent / "pdm.spec"

    cmd = [
        "pyinstaller",
        str(spec_file),
        "--clean",
        "--noconfirm"
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("Build successful!")
        print("Executable location: dist/PDM_System.exe")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("Build failed!")
        print("=" * 60)
        sys.exit(1)

if __name__ == '__main__':
    build()
```

**Build the executable:**

```bash
cd backend
pip install pyinstaller
python build_standalone.py
```

---

### 8.16: Testing Guide

**File: `TESTING.md`:**

```markdown
## PDM System Testing Guide

### Mode 1: Server Mode (Development)

#### Setup

1. Create GitLab repository
2. Configure `.env`:
```

MODE=server
GITLAB_ENABLED=true
GITLAB_REPO_URL=https://gitlab.com/YOUR_USERNAME/pdm-files.git

````
3. Generate GitLab Personal Access Token
4. Run server:
```bash
uvicorn app.main:app --reload
````

#### Test Cases

##### 1. Authentication

- [ ] Login with local password
- [ ] Login with GitLab PAT
- [ ] Auto-registration with GitLab PAT
- [ ] Invalid credentials rejected

##### 2. File Operations

- [ ] List files
- [ ] Checkout available file
- [ ] Cannot checkout locked file
- [ ] Checkin own file
- [ ] Cannot checkin other's file (unless admin)
- [ ] View version history
- [ ] Rollback to previous version

##### 3. Messaging

- [ ] Send message to user
- [ ] Send broadcast message (all)
- [ ] Receive messages
- [ ] Mark as read
- [ ] Delete message
- [ ] View unread count badge

##### 4. GitLab Sync

- [ ] Changes committed to GitLab
- [ ] Pull updates from GitLab
- [ ] users.json synced
- [ ] locks.json synced
- [ ] messages.json synced

##### 5. Admin Features

- [ ] View audit logs
- [ ] Force checkin
- [ ] Admin panel visible
- [ ] Regular users cannot access admin endpoints

---

### Mode 2: Standalone Mode (PyInstaller)

#### Setup

1. Build executable:
   ```bash
   cd backend
   python build_standalone.py
   ```
2. Copy `config.yaml` to same folder as `PDM_System.exe`
3. Configure `config.yaml`:
   ```yaml
   mode: standalone
   gitlab:
     enabled: true
     repo_url: https://gitlab.com/YOUR_USERNAME/pdm-files.git
   server:
     host: 127.0.0.1
     port: 5000
   ```

#### Test Cases

##### 1. Startup

- [ ] Double-click executable
- [ ] Server starts on localhost:5000
- [ ] Browser opens automatically
- [ ] Login page loads

##### 2. GitLab Integration

- [ ] First run clones GitLab repo
- [ ] Subsequent runs use existing clone
- [ ] Changes sync to GitLab
- [ ] Pull on startup

##### 3. Multi-User Scenario

- [ ] User A runs executable on Machine 1
- [ ] User A checks out file
- [ ] User B runs executable on Machine 2
- [ ] User B sees file locked by User A
- [ ] User B cannot checkout locked file

##### 4. Messaging Between Machines

- [ ] User A sends message on Machine 1
- [ ] Message commits to GitLab
- [ ] User B receives message on Machine 2 (after sync)

---

### Performance Testing

#### Metrics to Monitor

- [ ] GitLab clone time (first run)
- [ ] GitLab pull time (subsequent runs)
- [ ] File list load time
- [ ] Commit/push time
- [ ] Message load time

#### Expected Performance

- Local operations: < 100ms
- GitLab operations: 1-5 seconds
- Large file operations (with LFS): 5-30 seconds

---

### Security Testing

#### Authentication

- [ ] JWT tokens expire correctly
- [ ] Invalid tokens rejected
- [ ] Encrypted GitLab PAT not readable in users.json
- [ ] Password hashes secure (bcrypt)

#### Authorization

- [ ] Users cannot access admin endpoints
- [ ] Users cannot checkin others' files
- [ ] Audit logs cannot be tampered

#### GitLab Security

- [ ] PAT not exposed in logs
- [ ] PAT not in Git history
- [ ] Repository access validated

---

### Troubleshooting

#### GitLab Clone Fails

- Check PAT has correct scopes
- Check repository URL
- Check network connectivity
- Check Git is installed

#### LFS Issues

- Install Git LFS: `git lfs install`
- Verify: `git lfs version`

#### Build Issues

- Update PyInstaller: `pip install --upgrade pyinstaller`
- Clear build cache: `rm -rf build/ dist/`
- Check hidden imports in spec file

#### Sync Conflicts

- Check GitLab repo for conflicts
- Force pull if needed
- Reset local changes: `git reset --hard origin/main`

```

---

### Stage 8 Complete! 🎉

**What we've built:**

✅ **Hybrid Architecture**
- Works as central server OR standalone app
- GitLab integration for distributed teams
- Config-driven deployment

✅ **GitLab Integration**
- Personal Access Token authentication
- Automatic sync (pull/commit/push)
- Encrypted token storage
- LFS support for large files

✅ **Messaging System**
- User-to-user messages
- Broadcast messages
- Message history in GitLab
- Unread count badges

✅ **PyInstaller Packaging**
- Standalone executable
- Embedded web server
- Auto-open browser
- Portable deployment

**Complete file structure:**
```

pdm-tutorial/
├── backend/
│ ├── app/
│ │ ├── services/
│ │ │ ├── gitlab_service.py
│ │ │ ├── gitlab_sync_service.py
│ │ │ ├── message_service.py
│ │ │ ├── auth_service.py (updated)
│ │ │ ├── file_service.py
│ │ │ └── git_service.py
│ │ ├── api/
│ │ │ ├── messages.py (new)
│ │ │ ├── auth.py (updated)
│ │ │ ├── files.py
│ │ │ ├── version_control.py
│ │ │ └── deps.py (updated)
│ │ ├── utils/
│ │ │ ├── encryption.py (new)
│ │ │ └── file_locking.py
│ │ ├── config.py (updated)
│ │ ├── config_manager.py (new)
│ │ └── main.py
│ ├── static/
│ │ ├── css/
│ │ ├── js/
│ │ ├── login.html (updated)
│ │ └── index.html (updated)
│ ├── pdm_app.py (new)
│ ├── pdm.spec (new)
│ ├── build_standalone.py (new)
│ ├── config.yaml (new)
│ └── .env
├── TESTING.md (new)
└── README.md

````

**To use your app:**

**Option 1: Server Mode (Team deployment)**
```bash
## Configure .env with GitLab repo
uvicorn app.main:app --host 0.0.0.0 --port 8000

## Access from any browser
http://your-server:8000
````

**Option 2: Standalone Mode (Individual users)**

```bash
## Build once
python build_standalone.py

## Distribute PDM_System.exe to users
## Each user double-clicks executable
## Browser opens automatically
```

**Does this match your original app now?**

- ✅ GitLab as single source of truth
- ✅ Distributed users each running their own instance
- ✅ Shared users.json, locks.json in GitLab
- ✅ Hashed passwords
- ✅ GitLab token authentication
- ✅ Messaging system
- ✅ History tracking
- ✅ PyInstaller packaging ready

Ready to test or need any adjustments?
