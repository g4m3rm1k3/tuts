# Section 1: Logic & Proofs - The Foundation of Reasoning

## Introduction: Why Logic Matters

**Question**: Why study logic if you want to build software?

**Answer**: Every line of code you write is logic:

```python
if user.is_authenticated and user.has_permission:
    allow_access()
```

This is **formal logic**. Understanding it deeply means:

- Writing correct conditionals the first time
- Simplifying complex boolean expressions
- Proving your code handles all cases
- Designing systems that can't fail in unexpected ways
- Building compilers, databases, security systems

**In manufacturing**: Logic controls safety systems, quality checks, and automated decisions. A bug in logic can mean injuries or millions in losses.

**In this section**, you'll learn the mathematical foundation of all computation and build tools to analyze logical expressions.

---

## Learning Path for Section 1

We'll build in this order:

1. **Basic operators** (NOT, AND, OR) - The atoms of logic
2. **Tests** - Verify they work correctly
3. **Complex operators** (IMPLIES, IFF) - How conditionals really work
4. **Truth tables** - Exhaustive case analysis
5. **Equivalence checker** - Prove expressions are the same
6. **Visualization** - See it visually in HTML/JS
7. **Mini-project** - Boolean analyzer tool

Each piece builds on the previous one.

---

## 1.1 Propositional Logic - The Building Blocks

### What is a Proposition?

A **proposition** is a statement that is either **true** or **false** (not both, not neither).

**Examples:**

✅ **Propositions** (have a definite truth value):

- "The server is running" (either true or false)
- "5 is greater than 3" (true)
- "Python is a color" (false)

❌ **Not propositions**:

- "What time is it?" (question, not a statement)
- "Close the door!" (command, not a statement)
- "x > 5" (depends on x - not yet a proposition)

### Mathematical Notation

In math, we use variables to represent propositions:

$$p = \text{"User is authenticated"}$$
$$q = \text{"User has admin role"}$$
$$r = \text{"Database is available"}$$

In code:

```python
p = True   # User is authenticated
q = False  # User does not have admin role
r = True   # Database is available
```

---

### Code Along: Understanding Boolean Type

Let's start at the absolute beginning. Create your first file:

**File**: `foundations/logic/basics.py`

```python
"""
Basic propositions and boolean values.

This file demonstrates the fundamental concept of propositions
in discrete mathematics and how they map to Python's boolean type.
"""

# A proposition is represented as a boolean in Python
# There are only two possible values: True and False

# These are propositions with truth values
server_is_running = True
user_is_authenticated = False
database_is_available = True

# Print them to see
print("Proposition values:")
print(f"Server is running: {server_is_running}")
print(f"User is authenticated: {user_is_authenticated}")
print(f"Database is available: {database_is_available}")
```

**Save this file and run it:**

```bash
python foundations/logic/basics.py
```

**You should see:**

```
Proposition values:
Server is running: True
User is authenticated: False
Database is available: True
```

---

### Explanation: Breaking Down This Code

Let's understand every part:

```python
"""
Basic propositions and boolean values.
...
"""
```

**What is this?**

- This is a **docstring** (documentation string)
- Triple quotes (`"""`) let you write multiple lines
- Always at the top of a file or function
- Explains what the code does

**Why use docstrings?**

- Document your code's purpose
- Professional practice
- Python tools can extract these for documentation

---

```python
server_is_running = True
```

**Breaking this down:**

**`server_is_running`** = variable name

- Variables are names for values
- Use lowercase with underscores (Python convention)
- Names should describe what they represent

**`=`** = assignment operator

- NOT "equals" in the math sense!
- Means: "store this value in this variable"
- Read as: "server_is_running **gets** True"

**`True`** = boolean literal

- One of only two boolean values: `True` or `False`
- **Must be capitalized** in Python
- Represents a true proposition

**What happens in memory:**

```
Memory:
┌─────────────────────┬────────┐
│ server_is_running   │  True  │
└─────────────────────┴────────┘
```

Python creates a box labeled "server_is_running" and puts `True` in it.

---

```python
print(f"Server is running: {server_is_running}")
```

**Breaking this down:**

**`print()`** = built-in function

- Outputs text to the terminal
- Everything inside the parentheses is printed

**`f"..."`** = f-string (formatted string)

- The `f` before the quote makes this special
- Lets you insert variable values

**`{server_is_running}`** = placeholder

- Curly braces insert the variable's value
- Python replaces `{server_is_running}` with `True`

**Result:**

```
Server is running: True
```

**Without the `f`:**

```python
print("Server is running: {server_is_running}")
# Prints literally: Server is running: {server_is_running}
# Wrong!
```

The `f` is crucial!

---

### Understanding: Python's Boolean Type

Python has a special type for truth values: **`bool`**

```python
type(True)   # <class 'bool'>
type(False)  # <class 'bool'>
```

**Let's verify this.**

Add this to `basics.py`:

```python
# Check the type
print("\nTypes:")
print(f"Type of True: {type(True)}")
print(f"Type of False: {type(False)}")
print(f"Type of server_is_running: {type(server_is_running)}")
```

**Run it again:**

```bash
python foundations/logic/basics.py
```

**You'll see:**

```
Types:
Type of True: <class 'bool'>
Type of False: <class 'bool'>
Type of server_is_running: <class 'bool'>
```

**Explanation:**

- `type()` tells you what kind of value something is
- `<class 'bool'>` means "boolean type"
- All three are booleans

---

### Code Along: Boolean Values in Expressions

Add this to `basics.py`:

```python
# Boolean values can come from expressions
x = 5
y = 10

is_x_less_than_y = x < y
is_x_equal_to_y = x == y
is_x_greater_than_y = x > y

print("\nComparisons create boolean values:")
print(f"x = {x}, y = {y}")
print(f"x < y: {is_x_less_than_y}")
print(f"x == y: {is_x_equal_to_y}")
print(f"x > y: {is_x_greater_than_y}")
```

**Run it:**

```bash
python foundations/logic/basics.py
```

---

### Explanation: Comparison Operators

```python
is_x_less_than_y = x < y
```

**The `<` operator:**

- Compares two values
- Returns a **boolean**: `True` or `False`
- Doesn't modify either value

**Python's comparison operators:**

| Operator | Meaning               | Example   | Result  |
| -------- | --------------------- | --------- | ------- |
| `<`      | Less than             | `5 < 10`  | `True`  |
| `>`      | Greater than          | `5 > 10`  | `False` |
| `==`     | Equal to              | `5 == 5`  | `True`  |
| `!=`     | Not equal to          | `5 != 10` | `True`  |
| `<=`     | Less than or equal    | `5 <= 5`  | `True`  |
| `>=`     | Greater than or equal | `10 >= 5` | `True`  |

**Critical: `=` vs `==`**

```python
x = 5      # ASSIGNMENT: store 5 in x
x == 5     # COMPARISON: is x equal to 5?
```

**Common beginner mistake:**

```python
if x = 5:      # WRONG! Syntax error
if x == 5:     # CORRECT! Comparison
```

---

### Exercise: Practice Propositions

Before moving on, try this yourself:

**Add to `basics.py`:**

```python
# Your turn: Create some propositions
temperature = 72
is_too_hot = temperature > 80
is_too_cold = temperature < 60
is_comfortable = not is_too_hot and not is_too_cold

print("\nTemperature check:")
print(f"Temperature: {temperature}°F")
print(f"Too hot? {is_too_hot}")
print(f"Too cold? {is_too_cold}")
print(f"Comfortable? {is_comfortable}")
```

**Before running it, predict the output!**

Then run it and check:

```bash
python foundations/logic/basics.py
```

**Did you predict correctly?**

---

## 1.2 Logical Operators - Combining Propositions

Now that we understand individual propositions, let's combine them.

### The Three Basic Operators

In discrete math and programming, there are three fundamental logical operators:

| Math Symbol | Name | Python | Meaning              |
| ----------- | ---- | ------ | -------------------- |
| $\neg$      | NOT  | `not`  | Negation (opposite)  |
| $\wedge$    | AND  | `and`  | Conjunction (both)   |
| $\vee$      | OR   | `or`   | Disjunction (either) |

Let's implement each one carefully.

---

### Code Along: The NOT Operator

Create a new file:

**File**: `foundations/logic/operators.py`

```python
"""
Logical operators implementation.

This module implements the fundamental logical operators from discrete math.
Each operator is implemented as a function with clear documentation and examples.

Mathematical notation:
    ¬p (NOT p)
    p ∧ q (p AND q)
    p ∨ q (p OR q)
"""


def NOT(p: bool) -> bool:
    """
    Logical NOT operator (negation).

    The NOT operator returns the opposite truth value.

    Mathematical notation: ¬p

    Args:
        p: A boolean value

    Returns:
        The negation of p (True becomes False, False becomes True)

    Truth table:
        p    | ¬p
        -----|-----
        T    | F
        F    | T

    Examples:
        >>> NOT(True)
        False
        >>> NOT(False)
        True

    Real-world example:
        If p = "machine is safe", then ¬p = "machine is NOT safe"
    """
    return not p
```

**Save this file.**

---

### Explanation: Function Definition

Let's break down this function completely:

```python
def NOT(p: bool) -> bool:
```

**`def`** = keyword to define a function

- Short for "define"
- Tells Python: "a function starts here"

**`NOT`** = function name

- We choose this (could be anything)
- Using caps to match mathematical notation
- In Python, function names are usually lowercase, but we're being mathematical here

**`(p: bool)`** = parameter with type hint

- `p` is the parameter name (input variable)
- `: bool` is a **type hint** saying "p should be a boolean"
- Type hints are optional but professional

**`-> bool`** = return type hint

- The `->` means "returns"
- `bool` says this function returns a boolean
- Documents what the function gives back

**`:`** = starts the function body

- Everything indented after this is part of the function

---

### Understanding: Type Hints

```python
def NOT(p: bool) -> bool:
```

**What are type hints?**

- Annotations that document expected types
- Added in Python 3.5+
- **Optional** (Python doesn't enforce them automatically)
- But tools like `mypy` can check them

**Without type hints:**

```python
def NOT(p):
    return not p
```

Works, but you don't know what `p` should be!

**With type hints:**

```python
def NOT(p: bool) -> bool:
    return not p
```

Clear: takes a boolean, returns a boolean.

**Why use them?**

- **Documentation**: Others (and future you) know what to pass
- **Error catching**: `mypy` can find bugs before running
- **IDE support**: Better autocomplete and warnings
- **Professional**: Industry standard

**Further reading:**

- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [mypy Documentation](https://mypy.readthedocs.io/)

---

### Understanding: Docstrings

```python
"""
Logical NOT operator (negation).
...
"""
```

**What is a docstring?**

- Documentation for a function/class/module
- First thing after the function definition
- Triple quotes allow multiple lines
- Accessible via `help(NOT)`

**Good docstring includes:**

1. **Brief description**: What does it do?
2. **Args**: What parameters and what do they mean?
3. **Returns**: What does it return?
4. **Examples**: How to use it
5. **Notes**: Anything important to know

**Try it:**

```python
help(NOT)
```

Shows your docstring!

**Docstring conventions (Google style):**

```python
def function_name(param1, param2):
    """
    Brief description.

    Longer explanation if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ExceptionType: When does this exception occur

    Examples:
        >>> function_name(1, 2)
        3
    """
```

**Further reading:**

- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

---

### Understanding: The Function Body

```python
    return not p
```

**Indentation (4 spaces):**

- Shows this line is **inside** the function
- Python uses indentation instead of braces `{}`
- Mixing tabs and spaces causes errors
- **Standard**: 4 spaces per level

**`return`** = keyword to return a value

- Sends a value back to whoever called the function
- Exits the function immediately
- Everything after `return` is ignored

**`not p`** = the expression being returned

- `not` is Python's boolean negation operator
- If `p` is `True`, `not p` is `False`
- If `p` is `False`, `not p` is `True`

---

### Code Along: Testing NOT Operator

Let's test our function. Create:

**File**: `foundations/logic/test_not.py`

```python
"""
Tests for the NOT operator.

This file contains tests to verify the NOT operator works correctly.
We test every possible input (True and False).
"""

# We need to import the function we're testing
from foundations.logic.operators import NOT


def test_not_true():
    """
    Test that NOT(True) returns False.
    """
    # Arrange: set up the input
    input_value = True

    # Act: call the function
    result = NOT(input_value)

    # Assert: check the result is correct
    assert result == False


def test_not_false():
    """
    Test that NOT(False) returns True.
    """
    input_value = False
    result = NOT(input_value)
    assert result == True
```

**Save this file.**

---

### Explanation: Test Structure

```python
from foundations.logic.operators import NOT
```

**`from ... import ...`** = import statement

- `from foundations.logic.operators` - the file path
- `import NOT` - the specific function we want
- Now we can use `NOT()` in this file

**Why the path?**

```
foundations/
├── __init__.py       ← Makes it a package
├── logic/
│   ├── __init__.py   ← Makes logic a package
│   └── operators.py  ← Contains NOT function
```

The `__init__.py` files let us import like this.

---

```python
def test_not_true():
```

**Test function naming:**

- **Must** start with `test_` (pytest requirement)
- Descriptive name: `test_not_true` says what it tests
- No parameters needed for simple tests

---

```python
    # Arrange: set up the input
    input_value = True

    # Act: call the function
    result = NOT(input_value)

    # Assert: check the result is correct
    assert result == False
```

**This is the "Arrange-Act-Assert" pattern:**

**1. Arrange** - Set up the test data

```python
input_value = True
```

Prepare what you need for the test.

**2. Act** - Execute the code being tested

```python
result = NOT(input_value)
```

Call the function and store the result.

**3. Assert** - Verify the result is correct

```python
assert result == False
```

Check that you got the expected outcome.

**Why use this pattern?**

- **Clear structure**: Anyone can read the test
- **Organized**: Separate setup from verification
- **Professional**: Industry standard

---

### Understanding: The assert Statement

```python
assert result == False
```

**`assert`** = keyword that checks a condition

- If the condition is `True`: nothing happens, test passes
- If the condition is `False`: raises an `AssertionError`, test fails

**Examples:**

```python
assert True        # Passes silently
assert False       # Fails with AssertionError
assert 2 + 2 == 4  # Passes (condition is True)
assert 2 + 2 == 5  # Fails (condition is False)
```

**In testing:**

```python
result = NOT(True)
assert result == False  # Check: is result False?
```

If `NOT(True)` doesn't return `False`, the test fails!

---

### Code Along: Run Your First Test

```bash
pytest foundations/logic/test_not.py -v
```

**You should see:**

```
======================== test session starts ========================
collected 2 items

foundations/logic/test_not.py::test_not_true PASSED          [ 50%]
foundations/logic/test_not.py::test_not_false PASSED         [100%]

========================= 2 passed in 0.01s =========================
```

**� Both tests pass!**

---

### Explanation: pytest Commands

```bash
pytest foundations/logic/test_not.py -v
```

**`pytest`** = run the pytest test runner

- Automatically finds test files (starting with `test_`)
- Runs all test functions (starting with `test_`)
- Reports results

**`foundations/logic/test_not.py`** = specific file to test

- Can also use directories: `pytest foundations/`
- Or omit to test everything: `pytest`

**`-v`** = verbose flag

- Shows each test individually
- More detailed output
- Helpful for debugging

**Other useful flags:**

```bash
pytest -v              # Verbose
pytest -x              # Stop on first failure
pytest -k "not_true"   # Only run tests matching "not_true"
pytest --lf            # Run last failed tests
pytest --cov           # Show code coverage
```

**Further reading:**

- [pytest Documentation](https://docs.pytest.org/)
- [pytest Usage Guide](https://docs.pytest.org/en/stable/how-to/usage.html)

---

### Understanding: Why Test?

**Question**: Why write tests? The function is simple!

**Answer**:

**1. Verification**

- Proves the function works correctly
- Tests every possible case (for NOT: True and False)

**2. Confidence**

- Can refactor/change code knowing tests will catch breaks
- Professional safety net

**3. Documentation**

- Tests show HOW to use the function
- Living examples that can't get outdated

**4. Regression Prevention**

- If you break it later, tests fail immediately
- Catches bugs before they reach production

**Real-world example:**

You write `NOT` operator. Works great. Six months later, you "optimize" it:

```python
def NOT(p: bool) -> bool:
    return p  # BUG! Forgot the 'not'
```

**Without tests**: Bug goes into production, breaks everything  
**With tests**: `pytest` immediately shows failure, you fix it

**In manufacturing**: Testing is like quality control. You don't ship without checking!

---

## 1.3 The AND Operator

### Mathematical Foundation

The AND operator (conjunction) returns `True` only if **both** inputs are `True`.

**Mathematical notation**: $p \wedge q$

**Truth table**:

| $p$ | $q$ | $p \wedge q$ |
| --- | --- | ------------ |
| T   | T   | T            |
| T   | F   | F            |
| F   | T   | F            |
| F   | F   | F            |

**Real-world**: Think of a manufacturing safety system:

- Machine can start IF safety check passed AND operator present
- Need BOTH conditions

---

### Code Along: Implement AND

Add this to `foundations/logic/operators.py`:

```python


def AND(p: bool, q: bool) -> bool:
    """
    Logical AND operator (conjunction).

    The AND operator returns True only if both inputs are True.

    Mathematical notation: p ∧ q

    Args:
        p: First boolean value
        q: Second boolean value

    Returns:
        True if both p and q are True, False otherwise

    Truth table:
        p    | q    | p ∧ q
        -----|------|-------
        T    | T    | T
        T    | F    | F
        F    | T    | F
        F    | F    | F

    Examples:
        >>> AND(True, True)
        True
        >>> AND(True, False)
        False
        >>> AND(False, True)
        False
        >>> AND(False, False)
        False

    Real-world example:
        can_start_machine = AND(safety_check_passed, operator_present)
        Both conditions must be true to start the machine.
    """
    return p and q
```

**Save the file.**

---

### Explanation: Multiple Parameters

```python
def AND(p: bool, q: bool) -> bool:
```

**This function takes TWO parameters:**

- `p: bool` - first boolean
- `q: bool` - second boolean
- Separated by comma

**Calling it:**

```python
result = AND(True, False)
# p gets True
# q gets False
# result gets False
```

**Parameter order matters:**

```python
AND(True, False)   # p=True, q=False
AND(False, True)   # p=False, q=True (different!)
```

Though for AND, the result is the same either way (we'll prove this later!).

---

```python
    return p and q
```

**Python's `and` operator:**

- Built-in boolean operator
- Returns first value if it's falsy, otherwise returns second value
- For booleans: returns `True` only if both are `True`

**How it works:**

```python
True and True    # True
True and False   # False
False and True   # False
False and False  # False
```

---

### Code Along: Test AND Operator

Create **File**: `foundations/logic/test_and.py`

```python
"""
Tests for the AND operator.

We need to test ALL possible combinations:
- True AND True = True
- True AND False = False
- False AND True = False
- False AND False = False

This gives us complete coverage of the truth table.
"""

from foundations.logic.operators import AND


def test_and_true_true():
    """
    Test that AND(True, True) returns True.
    This is the only case where AND returns True.
    """
    # Arrange
    p = True
    q = True

    # Act
    result = AND(p, q)

    # Assert
    assert result == True


def test_and_true_false():
    """
    Test that AND(True, False) returns False.
    """
    p = True
    q = False
    result = AND(p, q)
    assert result == False


def test_and_false_true():
    """
    Test that AND(False, True) returns False.
    """
    p = False
    q = True
    result = AND(p, q)
    assert result == False


def test_and_false_false():
    """
    Test that AND(False, False) returns False.
    """
    p = False
    q = False
    result = AND(p, q)
    assert result == False
```

**Save and run:**

```bash
pytest foundations/logic/test_and.py -v
```

**You should see 4 passing tests!**

---

### Explanation: Complete Test Coverage

```python
def test_and_true_true():
def test_and_true_false():
def test_and_false_true():
def test_and_false_false():
```

**Why four tests?**

For two boolean inputs, there are $2^2 = 4$ possible combinations:

- (True, True)
- (True, False)
- (False, True)
- (False, False)

**We test ALL of them** to ensure complete correctness!

**This is called exhaustive testing:**

- Test every possible input combination
- For boolean functions, this is feasible
- For other types (integers, strings), it's impossible (infinite combinations)

---

## 1.4 The OR Operator

### Mathematical Foundation

The OR operator (disjunction) returns `True` if **at least one** input is `True`.

**Mathematical notation**: $p \vee q$

**Truth table**:

| $p$ | $q$ | $p \vee q$ |
| --- | --- | ---------- |
| T   | T   | T          |
| T   | F   | T          |
| F   | T   | T          |
| F   | F   | F          |

**Real-world**: Payment processing:

- Can pay IF has_credit_card OR has_debit_card
- Either one works!

---

### Code Along: Implement OR

Add to `foundations/logic/operators.py`:

```python


def OR(p: bool, q: bool) -> bool:
    """
    Logical OR operator (disjunction).

    The OR operator returns True if at least one input is True.

    Mathematical notation: p ∨ q

    Args:
        p: First boolean value
        q: Second boolean value

    Returns:
        True if p or q (or both) are True, False only if both are False

    Truth table:
        p    | q    | p ∨ q
        -----|------|-------
        T    | T    | T
        T    | F    | T
        F    | T    | T
        F    | F    | F

    Examples:
        >>> OR(True, True)
        True
        >>> OR(True, False)
        True
        >>> OR(False, True)
        True
        >>> OR(False, False)
        False

    Real-world example:
        can_pay = OR(has_credit_card, has_debit_card)
        User can pay if they have either payment method.
    """
    return p or q
```

---

### Code Along: Test OR Operator

**File**: `foundations/logic/test_or.py`

```python
"""
Tests for the OR operator.

OR returns True if at least one input is True.
Only returns False when both inputs are False.
"""

from foundations.logic.operators import OR


def test_or_true_true():
    """Test OR(True, True) = True"""
    assert OR(True, True) == True


def test_or_true_false():
    """Test OR(True, False) = True"""
    assert OR(True, False) == True


def test_or_false_true():
    """Test OR(False, True) = True"""
    assert OR(False, True) == True


def test_or_false_false():
    """Test OR(False, False) = False - the only False case"""
    assert OR(False, False) == False
```

**Run all logic tests:**

```bash
pytest foundations/logic/ -v
```

**You should see 10 passing tests total!**

- 2 for NOT
- 4 for AND
- 4 for OR

---

## 1.5 First Commit - Save Progress

We've built something substantial! Let's commit it.

```bash
# Check status
git status

# Add all new files
git add foundations/logic/

# Commit
git commit -m "Implement basic logical operators (NOT, AND, OR)

- Add operators.py with NOT, AND, OR functions
- Include comprehensive docstrings with truth tables
- Add type hints for all functions
- Create complete test suite with exhaustive coverage
- All tests passing (10/10)"

# View your history
git log --oneline
```

---

### Explanation: Good Git Commits

**When to commit?**

- Completed a logical unit of work
- All tests passing
- Code is in a working state

**What we just completed:**

- ✅ Implemented 3 operators
- ✅ Wrote comprehensive tests
- ✅ All tests pass
- ✅ Code is documented

Perfect time to commit!

**Commit message structure:**

```
Short summary (50 chars)

Detailed explanation:
- What was added
- What was changed
- What was fixed
- Why it matters
```

---

## Progress Check

Before continuing, let's verify everything is working.

**Your file structure should look like:**

```
discrete-math-masterclass/
├── foundations/
│   ├── __init__.py
│   └── logic/
│       ├── __init__.py
│       ├── basics.py
│       ├── operators.py
│       ├── test_not.py
│       ├── test_and.py
│       └── test_or.py
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

**Run all tests:**

```bash
pytest foundations/logic/ -v
```

**Expected output:**

```
collected 10 items

foundations/logic/test_and.py::test_and_true_true PASSED
foundations/logic/test_and.py::test_and_true_false PASSED
foundations/logic/test_and.py::test_and_false_true PASSED
foundations/logic/test_and.py::test_and_false_false PASSED
foundations/logic/test_not.py::test_not_true PASSED
foundations/logic/test_not.py::test_not_false PASSED
foundations/logic/test_or.py::test_or_true_true PASSED
foundations/logic/test_or.py::test_or_true_false PASSED
foundations/logic/test_or.py::test_or_false_true PASSED
foundations/logic/test_or.py::test_or_false_false PASSED

========================= 10 passed in 0.05s =========================
```

**All green?** ✅ Perfect! Ready to continue!

**Any errors?** Let me know what you see and I'll help you fix it.

---

## What's Next?

We've laid a solid foundation:

- ✅ Implemented NOT, AND, OR
- ✅ Written comprehensive tests
- ✅ Learned functions, type hints, docstrings
- ✅ Practiced testing methodology
- ✅ Committed our work

**Coming up:**

1. IMPLIES operator (the tricky one!)
2. IFF operator (bidirectional)
3. Truth table generator
4. Logical equivalence checker
5. First visualization!

Should I continue with the IMPLIES operator? This is where logic gets really interesting!
