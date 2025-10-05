"""
Deep dive into Python's typing module.
Type hints don't enforce types at runtime - they're for:
1. IDE autocomplete and error detection
2. Static analysis tools (mypy)
3. Documentation
4. Runtime validation (with Pydantic)
"""

from typing import Literal
from typing import (
    List, Dict, Tuple, Set,  # Generic types
    Optional, Union,          # Type combinations
    Any, TypeVar,            # Special types
    Callable,                # Function types
    Literal,                 # Exact values
    Protocol                 # Structural subtyping
)
from pathlib import Path
from datetime import datetime

# ============================================================================
# SECTION 1: Basic Type Hints
# ============================================================================


def greet(name: str) -> str:
    """
    Simple type hints: parameter 'name' must be str, returns str.
    """
    return f"Hello, {name}!"

# ============================================================================
# SECTION 2: Collection Types
# ============================================================================


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
    return (40.7128, -74.0060)  # NYC coordinates

# ============================================================================
# SECTION 3: Optional and Union
# ============================================================================


def find_user(user_id: int) -> Optional[Dict[str, str]]:
    """
    Optional[X] is shorthand for Union[X, None]
    This function might return a dict or None.
    """
    if user_id == 1:
        return {"name": "Alice", "role": "admin"}
    return None  # Not found


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

# ============================================================================
# SECTION 4: Callable (Function Types)
# ============================================================================


def execute_twice(func: Callable[[int], int], value: int) -> int:
    """
    Callable[[int], int] means:
    - Takes a function that accepts one int parameter
    - That function returns an int
    """
    return func(func(value))


def double(x: int) -> int:
    return x * 2

# Usage: execute_twice(double, 5)  # Returns 20

# ============================================================================
# SECTION 5: TypeVar (Generic Functions)
# ============================================================================


T = TypeVar('T')  # Define a type variable


def get_first(items: List[T]) -> Optional[T]:
    """
    Generic function: works with any type.
    If you pass List[str], it returns Optional[str]
    If you pass List[int], it returns Optional[int]
    """
    return items[0] if items else None

# ============================================================================
# SECTION 6: Literal (Exact Values)
# ============================================================================


UserRole = Literal["admin", "user", "guest"]


def check_permission(role: UserRole) -> bool:
    """
    role can ONLY be "admin", "user", or "guest"
    IDE will autocomplete these exact values
    """
    return role == "admin"

# ============================================================================
# SECTION 7: Protocol (Structural Typing)
# ============================================================================


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

# Works with files, StringIO, custom classes, etc.

# ============================================================================
# SECTION 8: Real-World Example - Our PDM App
# ============================================================================


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

# ============================================================================
# TESTING YOUR UNDERSTANDING
# ============================================================================


if __name__ == "__main__":
    # Test basic types
    print(greet("World"))

    # Test collections
    files = ["file1.txt", "file2.txt"]
    print(process_files(files))

    # Test Optional
    user = find_user(1)
    print(f"Found user: {user}")

    # Test Union
    print(process_data(42))
    print(process_data("hello"))
    print(process_data([1, 2, 3]))

    # Test Callable
    result = execute_twice(double, 5)
    print(f"Double twice: {result}")

    # Test generic
    first_str = get_first(["a", "b", "c"])
    first_int = get_first([1, 2, 3])
    print(f"First string: {first_str}, First int: {first_int}")
