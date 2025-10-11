# Section 1 Continued: Truth Table Generation

## 1.10 Truth Tables - Systematic Case Analysis

### Introduction: Why Truth Tables Matter

Imagine you're building a security system with this logic:

```python
if (user.is_authenticated and user.has_permission) or user.is_admin:
    grant_access()
```

**Question**: Does this work correctly for all cases?

**Without truth tables**: You might test a few cases, miss edge cases, ship bugs.

**With truth tables**: You systematically check **every possible combination**. No surprises.

**Truth tables are:**

- Exhaustive verification of logical expressions
- How you **prove** code is correct
- Essential for security, safety-critical systems, compilers

---

### The Challenge

For 3 boolean variables, there are $2^3 = 8$ possible combinations:

```
(True, True, True)
(True, True, False)
(True, False, True)
(True, False, False)
(False, True, True)
(False, True, False)
(False, False, True)
(False, False, False)
```

Writing nested loops for each variable count is tedious. We need a **general solution**.

---

## 1.11 Understanding itertools.product

Before building our truth table generator, we need to understand a powerful tool: `itertools.product`.

### What is itertools?

**itertools** is a built-in Python library for efficient iteration.

Think of it as: "Advanced loop tools that are faster and cleaner than writing nested loops yourself."

**Where it comes from:**

- Built into Python (no pip install needed)
- Implemented in C (very fast)
- Used by professionals everywhere

---

### Code Along: Exploring itertools.product

Let's learn by doing. Create a new file:

**File**: `foundations/logic/learn_itertools.py`

```python
"""
Learning itertools.product

This file demonstrates how itertools.product generates
all combinations - the foundation of truth table generation.
"""

# Import the product function from itertools
from itertools import product


print("="*60)
print("UNDERSTANDING itertools.product")
print("="*60)

# Example 1: Simple combination of two lists
print("\nExample 1: Combining two lists")
print("-"*60)

colors = ['red', 'blue']
sizes = ['small', 'large']

print(f"Colors: {colors}")
print(f"Sizes: {sizes}")
print("\nAll combinations:")

for color, size in product(colors, sizes):
    print(f"  {color} {size}")
```

**Save and run:**

```bash
python foundations/logic/learn_itertools.py
```

**Output:**

```
============================================================
UNDERSTANDING itertools.product
============================================================

Example 1: Combining two lists
------------------------------------------------------------
Colors: ['red', 'blue']
Sizes: ['small', 'large']

All combinations:
  red small
  red large
  blue small
  blue large
```

---

### Explanation: What Just Happened?

```python
from itertools import product
```

**Import statement breakdown:**

- `from itertools` - from the itertools module
- `import product` - import just the product function
- Now we can use `product()` directly

---

```python
for color, size in product(colors, sizes):
```

**What `product()` does:**

Generates the **Cartesian product** - all possible pairs:

```
colors = ['red', 'blue']        (2 items)
sizes = ['small', 'large']      (2 items)
                                ↓
product generates:              (2 × 2 = 4 combinations)
('red', 'small')
('red', 'large')
('blue', 'small')
('blue', 'large')
```

**Manual equivalent (nested loops):**

```python
for color in colors:
    for size in sizes:
        print(f"  {color} {size}")
```

**With product:**

```python
for color, size in product(colors, sizes):
    print(f"  {color} {size}")
```

Cleaner!

---

### Understanding: Tuple Unpacking

```python
for color, size in product(colors, sizes):
```

**`product()` yields tuples:** `('red', 'small')`

**Tuple unpacking** assigns parts to variables:

```python
# Without unpacking
for item in product(colors, sizes):
    color = item[0]
    size = item[1]
    print(color, size)

# With unpacking (better!)
for color, size in product(colors, sizes):
    print(color, size)
```

**The second way is more readable and Pythonic.**

---

### Code Along: The `repeat` Parameter

Add this to `learn_itertools.py`:

```python
# Example 2: Using the repeat parameter
print("\n\nExample 2: Boolean combinations with repeat")
print("-"*60)

print("All 2-variable boolean combinations:")
for combo in product([True, False], repeat=2):
    print(f"  {combo}")

print("\nAll 3-variable boolean combinations:")
for combo in product([True, False], repeat=3):
    print(f"  {combo}")
```

**Run it again:**

```bash
python foundations/logic/learn_itertools.py
```

---

### Explanation: The `repeat` Parameter

```python
product([True, False], repeat=2)
```

**What this means:**

- Take the list `[True, False]`
- Repeat it 2 times
- Generate all combinations

**Equivalent to:**

```python
product([True, False], [True, False])
```

**Why it's useful:**

```python
# Without repeat (manual):
product([True, False], [True, False])

# With repeat (clean):
product([True, False], repeat=2)
```

**For 3 variables:**

```python
# Manual (tedious):
product([True, False], [True, False], [True, False])

# With repeat (elegant):
product([True, False], repeat=3)
```

**This is how we'll generate truth tables for any number of variables!**

---

### Code Along: Counting Combinations

Add to `learn_itertools.py`:

```python
# Example 3: Understanding exponential growth
print("\n\nExample 3: Exponential growth of combinations")
print("-"*60)

for n in range(1, 6):
    # Generate combinations for n variables
    combinations = list(product([True, False], repeat=n))
    count = len(combinations)

    print(f"{n} variables: 2^{n} = {count} combinations")

    # Show combinations for small n
    if n <= 2:
        for combo in combinations:
            print(f"  {combo}")
        print()
```

**Run it:**

```bash
python foundations/logic/learn_itertools.py
```

---

### Explanation: Exponential Growth

```python
combinations = list(product([True, False], repeat=n))
```

**Converting to list:**

- `product()` returns an iterator (generates values on-demand)
- `list()` converts it to an actual list
- Now we can count them with `len()`

**Why we need to understand this:**

| Variables | Combinations | Formula  |
| --------- | ------------ | -------- |
| 1         | 2            | $2^1$    |
| 2         | 4            | $2^2$    |
| 3         | 8            | $2^3$    |
| 4         | 16           | $2^4$    |
| 5         | 32           | $2^5$    |
| 10        | 1,024        | $2^{10}$ |
| 20        | 1,048,576    | $2^{20}$ |

**This is why exhaustive testing becomes impractical for many variables!**

But for logic with 2-4 variables, it's perfect.

---

### Code Along: Indexing Variables

Add to `learn_itertools.py`:

```python
# Example 4: Mapping combinations to variable names
print("\n\nExample 4: Mapping to variable names")
print("-"*60)

variables = ['p', 'q', 'r']
print(f"Variables: {variables}\n")

for combination in product([True, False], repeat=len(variables)):
    # The zip function pairs variables with values
    mapping = dict(zip(variables, combination))
    print(f"{combination} → {mapping}")
```

**Run it:**

```bash
python foundations/logic/learn_itertools.py
```

**Output:**

```
Variables: ['p', 'q', 'r']

(True, True, True) → {'p': True, 'q': True, 'r': True}
(True, True, False) → {'p': True, 'q': True, 'r': False}
...
```

---

### Explanation: zip() and dict()

```python
mapping = dict(zip(variables, combination))
```

**This is a powerful pattern. Let's break it down:**

**Step 1: zip() pairs up elements**

```python
variables = ['p', 'q', 'r']
combination = (True, False, True)

zipped = zip(variables, combination)
# Result: [('p', True), ('q', False), ('r', True)]
```

**`zip()` creates pairs from two iterables:**

- First from each: `('p', True)`
- Second from each: `('q', False)`
- Third from each: `('r', True)`

**Step 2: dict() creates a dictionary**

```python
pairs = [('p', True), ('q', False), ('r', True)]
mapping = dict(pairs)
# Result: {'p': True, 'q': False, 'r': True}
```

**The full pipeline:**

```python
variables:  ['p', 'q', 'r']
combination: (True, False, True)
              ↓ zip()
pairs:      [('p', True), ('q', False), ('r', True)]
              ↓ dict()
mapping:    {'p': True, 'q': False, 'r': True}
```

**Why this matters:**

Now we can evaluate expressions like:

```python
expression = lambda v: v['p'] and v['q']
result = expression(mapping)  # Uses the dictionary!
```

---

### Understanding: Why Dictionaries for Variables?

**Without dictionaries:**

```python
def evaluate(p, q, r):
    return p and (q or r)

# Must remember order:
evaluate(True, False, True)
```

**With dictionaries:**

```python
def evaluate(variables):
    return variables['p'] and (variables['q'] or variables['r'])

# Names are clear:
evaluate({'p': True, 'q': False, 'r': True})
```

**Benefits:**

1. **Self-documenting**: Clear which value is which
2. **Flexible**: Add variables without changing function signature
3. **Error-resistant**: Can't mix up order
4. **Generalizable**: Works for any number of variables

---

## 1.12 Building the Truth Table Generator

Now we have all the pieces! Let's build our truth table generator.

### Code Along: Basic Truth Table Function

Create a new file:

**File**: `foundations/logic/truth_tables.py`

```python
"""
Truth table generation.

This module provides functions to generate and display truth tables
for logical expressions. Truth tables systematically show the output
of an expression for every possible input combination.

Mathematical foundation:
For n boolean variables, there are 2^n possible combinations.
A truth table lists all combinations and their results.
"""

from itertools import product
from typing import List, Dict, Callable


def generate_truth_table(
    variables: List[str],
    expression: Callable[[Dict[str, bool]], bool]
) -> List[tuple]:
    """
    Generate a truth table for a logical expression.

    This function creates all possible combinations of True/False
    for the given variables, evaluates the expression for each,
    and returns the complete truth table.

    Args:
        variables: List of variable names (e.g., ['p', 'q', 'r'])
        expression: Function that takes a dict of variable values
                   and returns a boolean result
                   Example: lambda v: v['p'] and v['q']

    Returns:
        List of tuples, where each tuple is:
        (input_combination, result)

        Example:
        [
            ((True, True), True),
            ((True, False), False),
            ((False, True), False),
            ((False, False), False)
        ]

    Example usage:
        >>> variables = ['p', 'q']
        >>> expression = lambda v: v['p'] and v['q']
        >>> table = generate_truth_table(variables, expression)
        >>> len(table)
        4
        >>> table[0]
        ((True, True), True)

    Mathematical note:
        For n variables, this generates 2^n rows.
        The combinations are generated in lexicographic order
        (True comes before False).
    """
    # Store all rows of the truth table
    truth_table = []

    # Generate all possible True/False combinations
    # repeat=len(variables) means: one True/False choice per variable
    for combination in product([True, False], repeat=len(variables)):
        # Create a dictionary mapping variable names to their values
        # zip pairs up: ['p', 'q'] with (True, False) → [('p', True), ('q', False)]
        # dict converts pairs to dictionary: {'p': True, 'q': False}
        variable_values = dict(zip(variables, combination))

        # Evaluate the expression with these variable values
        result = expression(variable_values)

        # Store the input combination and its result
        truth_table.append((combination, result))

    return truth_table
```

**Save this file.**

---

### Explanation: Type Hints for Complex Types

```python
from typing import List, Dict, Callable
```

**Why import from `typing`?**

For complex type hints:

- `List[str]` - a list of strings
- `Dict[str, bool]` - a dictionary with string keys and boolean values
- `Callable` - a function type

**Without typing imports:**

```python
def generate_truth_table(variables, expression):
```

No type information!

**With typing imports:**

```python
def generate_truth_table(
    variables: List[str],
    expression: Callable[[Dict[str, bool]], bool]
) -> List[tuple]:
```

Complete type information!

---

```python
variables: List[str]
```

**What this means:**

- `variables` should be a **list**
- The list should contain **strings**
- Example: `['p', 'q', 'r']`

**Type checker can catch errors:**

```python
# Wrong:
generate_truth_table([1, 2, 3], ...)  # mypy error: expected List[str]

# Right:
generate_truth_table(['p', 'q'], ...)  # ✓
```

---

```python
expression: Callable[[Dict[str, bool]], bool]
```

**This is complex! Let's break it down:**

**`Callable`** = a function type

**`[[Dict[str, bool]], bool]`** = function signature:

- `[Dict[str, bool]]` - takes one parameter: a dictionary with string keys and boolean values
- `, bool` - returns a boolean

**Example of a valid expression:**

```python
def my_expression(v: Dict[str, bool]) -> bool:
    return v['p'] and v['q']

# Or as lambda:
lambda v: v['p'] and v['q']
```

**Further reading:**

- [Python Typing Module](https://docs.python.org/3/library/typing.html)
- [Type Hints Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

---

```python
) -> List[tuple]:
```

**Return type annotation:**

- Function returns a **list**
- List contains **tuples**
- Each tuple is: `(input_combination, result)`

Example return value:

```python
[
    ((True, True), True),
    ((True, False), False),
    ...
]
```

---

### Explanation: The Function Body

Let's walk through the function step by step:

```python
    truth_table = []
```

**Create an empty list** to store results.

---

```python
    for combination in product([True, False], repeat=len(variables)):
```

**Generate all combinations:**

- `len(variables)` counts how many variables we have
- If `variables = ['p', 'q']`, then `len(variables) = 2`
- `product([True, False], repeat=2)` generates 4 combinations
- Works for any number of variables!

---

```python
        variable_values = dict(zip(variables, combination))
```

**Create the variable-to-value mapping:**

Example with `variables = ['p', 'q']` and `combination = (True, False)`:

```python
# Step 1: zip
zip(['p', 'q'], (True, False))
# → [('p', True), ('q', False)]

# Step 2: dict
dict([('p', True), ('q', False)])
# → {'p': True, 'q': False}
```

---

```python
        result = expression(variable_values)
```

**Evaluate the expression:**

If `expression = lambda v: v['p'] and v['q']` and `variable_values = {'p': True, 'q': False}`:

```python
result = expression({'p': True, 'q': False})
# → True and False
# → False
```

---

```python
        truth_table.append((combination, result))
```

**Store this row:**

```python
(combination, result)
# Example: ((True, False), False)
```

Added to `truth_table` list.

---

```python
    return truth_table
```

**Return the complete list** of all rows.

---

### Code Along: Test the Generator

Create **File**: `foundations/logic/test_truth_tables.py`

```python
"""
Tests for truth table generation.

We verify that generate_truth_table correctly generates
all combinations and evaluates expressions properly.
"""

from foundations.logic.truth_tables import generate_truth_table


def test_truth_table_two_variables():
    """
    Test truth table generation for 2 variables.
    Should generate 2^2 = 4 rows.
    """
    variables = ['p', 'q']
    expression = lambda v: v['p'] and v['q']

    # Generate the truth table
    table = generate_truth_table(variables, expression)

    # Check we got 4 rows (2^2)
    assert len(table) == 4, "Should have 4 rows for 2 variables"

    # Verify each row has the correct structure
    for row in table:
        assert len(row) == 2, "Each row should have (inputs, result)"
        inputs, result = row
        assert len(inputs) == 2, "Should have 2 input values"
        assert isinstance(result, bool), "Result should be boolean"


def test_truth_table_and_operator():
    """
    Test that truth table correctly evaluates AND operator.
    """
    variables = ['p', 'q']
    expression = lambda v: v['p'] and v['q']

    table = generate_truth_table(variables, expression)

    # Expected results for AND:
    # T, T → T
    # T, F → F
    # F, T → F
    # F, F → F
    expected = [
        ((True, True), True),
        ((True, False), False),
        ((False, True), False),
        ((False, False), False)
    ]

    assert table == expected, "AND truth table should match expected values"


def test_truth_table_three_variables():
    """
    Test truth table generation for 3 variables.
    Should generate 2^3 = 8 rows.
    """
    variables = ['p', 'q', 'r']
    expression = lambda v: v['p'] and (v['q'] or v['r'])

    table = generate_truth_table(variables, expression)

    # Check we got 8 rows (2^3)
    assert len(table) == 8, "Should have 8 rows for 3 variables"

    # Each row should have 3 input values
    for row in table:
        inputs, result = row
        assert len(inputs) == 3, "Should have 3 input values"


def test_truth_table_complex_expression():
    """
    Test a complex expression: (p → q) ↔ (¬p ∨ q)
    This should always be True (they're equivalent).
    """
    from foundations.logic.operators import IMPLIES, OR, NOT

    variables = ['p', 'q']

    # The equivalence: (p → q) ↔ (¬p ∨ q)
    expression = lambda v: IMPLIES(v['p'], v['q']) == (OR(NOT(v['p']), v['q']))

    table = generate_truth_table(variables, expression)

    # Every row should be True (equivalence always holds)
    for inputs, result in table:
        assert result == True, f"Equivalence should hold for {inputs}"
```

**Save and run:**

```bash
pytest foundations/logic/test_truth_tables.py -v
```

**You should see 4 passing tests!**

---

### Explanation: Testing Strategy

```python
def test_truth_table_two_variables():
```

**Tests the basic functionality:**

- Correct number of rows (2^2 = 4)
- Correct structure of each row
- Correct types

```python
def test_truth_table_and_operator():
```

**Tests correctness of evaluation:**

- Compares against known AND truth table
- Verifies exact values

```python
def test_truth_table_three_variables():
```

**Tests scalability:**

- Works with 3 variables (8 rows)
- Shows it generalizes

```python
def test_truth_table_complex_expression():
```

**Tests real usage:**

- Uses our operators
- Verifies mathematical theorem
- Shows practical application

---

## 1.13 Displaying Truth Tables

We can generate truth tables, but we need to **display** them nicely!

### Code Along: Pretty Printing Function

Add to `foundations/logic/truth_tables.py`:

```python


def print_truth_table(
    variables: List[str],
    expression: Callable[[Dict[str, bool]], bool],
    expression_name: str
) -> None:
    """
    Generate and print a nicely formatted truth table.

    This function creates a truth table and displays it in a
    readable format with headers, separators, and aligned columns.

    Args:
        variables: List of variable names
        expression: Function to evaluate
        expression_name: Human-readable name of the expression
                        (e.g., "p ∧ q" or "p AND q")

    Returns:
        None (prints to console)

    Example output:
        Truth Table: p ∧ q
        ════════════════════════
        p     | q     | p ∧ q
        ------+-------+--------
        T     | T     | T
        T     | F     | F
        F     | T     | F
        F     | F     | F

    Example usage:
        >>> print_truth_table(
        ...     ['p', 'q'],
        ...     lambda v: v['p'] and v['q'],
        ...     "p ∧ q"
        ... )
    """
    # Generate the truth table
    table = generate_truth_table(variables, expression)

    # Print title
    print(f"\nTruth Table: {expression_name}")
    print("=" * 60)

    # Create and print header
    header_parts = [f"{var:^6}" for var in variables]
    header_parts.append(f"{expression_name:^15}")
    header = " | ".join(header_parts)
    print(header)

    # Print separator line
    separator_parts = ["-" * 6 for _ in variables]
    separator_parts.append("-" * 15)
    separator = "-+-".join(separator_parts)
    print(separator)

    # Print each row
    for combination, result in table:
        # Convert booleans to T/F for readability
        row_parts = [f"{'T' if value else 'F':^6}" for value in combination]
        row_parts.append(f"{'T' if result else 'F':^15}")
        row = " | ".join(row_parts)
        print(row)

    print()  # Blank line at end
```

---

### Explanation: String Formatting

```python
header_parts = [f"{var:^6}" for var in variables]
```

**List comprehension with formatting:**

**Without list comprehension:**

```python
header_parts = []
for var in variables:
    formatted = f"{var:^6}"
    header_parts.append(formatted)
```

**With list comprehension (more Pythonic):**

```python
header_parts = [f"{var:^6}" for var in variables]
```

**The format `{var:^6}`:**

- `^` = center align
- `6` = field width of 6 characters
- Example: `"p"` becomes `"  p   "` (centered in 6 spaces)

---

```python
header = " | ".join(header_parts)
```

**join() method:**

Combines list elements with a separator:

```python
parts = ["  p   ", "  q   ", "   p ∧ q    "]
result = " | ".join(parts)
# →  "  p    |   q    |    p ∧ q    "
```

**Why use join()?**

**Bad way (inefficient):**

```python
result = ""
for part in parts:
    result += part + " | "
```

Creates new string each time (slow for many items)!

**Good way (efficient):**

```python
result = " | ".join(parts)
```

Single operation, much faster!

---

```python
row_parts = [f"{'T' if value else 'F':^6}" for value in combination]
```

**Nested formatting:**

- `'T' if value else 'F'` - convert boolean to 'T' or 'F'
- `:^6` - center in 6 characters
- Result: `" T "` or `" F  "` (centered)

**Breaking it down:**

```python
value = True
text = 'T' if value else 'F'  # → 'T'
formatted = f"{text:^6}"       # → "  T   "
```

All in one line:

```python
formatted = f"{'T' if value else 'F':^6}"
```

---

### Code Along: Test the Display

Create a simple test script:

**File**: `foundations/logic/demo_truth_tables.py`

```python
"""
Demonstration of truth table generation and display.

Run this file to see truth tables for various logical expressions.
"""

from foundations.logic.truth_tables import print_truth_table
from foundations.logic.operators import NOT, AND, OR, IMPLIES, IFF


if __name__ == "__main__":
    print("\n" + "="*60)
    print("TRUTH TABLE DEMONSTRATIONS")
    print("="*60)

    # Example 1: AND operator
    print_truth_table(
        variables=['p', 'q'],
        expression=lambda v: AND(v['p'], v['q']),
        expression_name="p ∧ q"
    )

    # Example 2: OR operator
    print_truth_table(
        variables=['p', 'q'],
        expression=lambda v: OR(v['p'], v['q']),
        expression_name="p ∨ q"
    )

    # Example 3: IMPLIES operator
    print_truth_table(
        variables=['p', 'q'],
        expression=lambda v: IMPLIES(v['p'], v['q']),
        expression_name="p → q"
    )

    # Example 4: IFF operator
    print_truth_table(
        variables=['p', 'q'],
        expression=lambda v: IFF(v['p'], v['q']),
        expression_name="p ↔ q"
    )

    # Example 5: Complex expression
    print_truth_table(
        variables=['p', 'q', 'r'],
        expression=lambda v: v['p'] and (v['q'] or v['r']),
        expression_name="p ∧ (q ∨ r)"
    )

    # Example 6: De Morgan's Law
    print_truth_table(
        variables=['p', 'q'],
        expression=lambda v: NOT(AND(v['p'], v['q'])),
        expression_name="¬(p ∧ q)"
    )

    print_truth_table(
        variables=['p', 'q'],
        expression=lambda v: OR(NOT(v['p']), NOT(v['q'])),
        expression_name="¬p ∨ ¬q"
    )

    print("Notice: The last two tables are identical!")
    print("This proves De Morgan's Law: ¬(p ∧ q) ≡ ¬p ∨ ¬q")
```

**Run it:**

```bash
python foundations/logic/demo_truth_tables.py
```

**You should see beautiful formatted truth tables!**

---

### Understanding: The `if __name__ == "__main__":` Pattern

```python
if __name__ == "__main__":
    # Code here
```

**What is `__name__`?**

A special variable Python sets automatically:

- When you **run** a file: `__name__` is `"__main__"`
- When you **import** a file: `__name__` is the module name

**Example:**

**File: mymodule.py**

```python
print(f"__name__ is: {__name__}")

if __name__ == "__main__":
    print("Running as main!")
else:
    print("Being imported!")
```

**Run it directly:**

```bash
python mymodule.py
```

Output:

```
__name__ is: __main__
Running as main!
```

**Import it:**

```python
import mymodule
```

Output:

```
__name__ is: mymodule
Being imported!
```

**Why use this pattern?**

Makes files dual-purpose:

1. **Library**: Can be imported
2. **Script**: Can be run directly with demo/test code

**Professional practice everywhere!**

---

## 1.14 Commit Your Progress

Great work! Time to commit:

```bash
# Check status
git status

# Add new files
git add foundations/logic/

# Commit
git commit -m "Add truth table generation and display

- Implement generate_truth_table function
  - Uses itertools.product for combinations
  - Works for any number of variables
  - Returns structured data (tuples)

- Implement print_truth_table function
  - Pretty-prints truth tables with formatting
  - Aligned columns and separators
  - Converts booleans to T/F for readability

- Add comprehensive tests
  - Test 2 and 3 variable cases
  - Verify correctness against known tables
  - Test complex expressions

- Add demonstration script
  - Shows all basic operators
  - Demonstrates De Morgan's Law
  - Proves mathematical equivalences

- Create learning material for itertools
  - Comprehensive examples of product()
  - Explains repeat parameter
  - Shows zip() and dict() patterns"

# View log
git log --oneline
```

---

## Progress Check

**Run all tests:**

```bash
pytest foundations/logic/ -v --cov=foundations.logic
```

**You should have:**

- ✅ 26 passing tests (22 operators + 4 truth tables)
- ✅ 100% code coverage
- ✅ All operators working
- ✅ Truth table generation working
- ✅ Pretty printing working

**Verify truth tables work:**

```bash
python foundations/logic/demo_truth_tables.py
```

Should show beautifully formatted tables!

---

## What's Next?

We can now:

- ✅ Evaluate any logical expression
- ✅ Generate complete truth tables
- ✅ Display them nicely

**Coming up:**

1. **Logical Equivalence Checker**
