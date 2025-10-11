Perfect! Let's continue with smaller, incremental steps where you code along as we go.

---

# Section 1 Continued: Logical Equivalence Checker

## 1.15 Checking Logical Equivalence

### Introduction

Two logical expressions are **equivalent** if they have identical truth tables.

For example:

- $p \rightarrow q$ and $\neg p \vee q$ are equivalent
- $\neg(p \wedge q)$ and $\neg p \vee \neg q$ are equivalent (De Morgan's Law)

We can **prove** these equivalences by comparing truth tables.

---

## Step 1: Create the File

First, create a new file for equivalence checking:

**Create**: `foundations/logic/equivalence.py`

Just create an empty file for now. We'll build it piece by piece.

---

## Step 2: Add the Module Docstring

**In `equivalence.py`, type:**

```python
"""
Logical equivalence checking.

Two logical expressions are equivalent if they produce identical
truth tables for all possible input combinations.

Mathematical notation: p ≡ q means "p is equivalent to q"
"""
```

**Stop. Let me explain:**

**What's a module docstring?**

- First thing in a Python file
- Explains what the entire file does
- Shows up when you `import equivalence` and run `help(equivalence)`

**Triple quotes** allow multiple lines of documentation.

**Type this out, save the file.**

Ready? Let me know when you've typed it!

---

## Step 3: Add Imports

**Below the docstring, add:**

```python

from typing import List, Dict, Callable
from foundations.logic.truth_tables import generate_truth_table
```

**Stop. Explanation:**

**Line 1** - Blank line after docstring (PEP 8 style)

**Line 2** - Import type hints

- `List`, `Dict`, `Callable` for type annotations
- These let us specify complex types

**Line 3** - Import our truth table generator

- We'll use this to compare tables
- Notice the path: `from foundations.logic.truth_tables`

**Type these imports. Save.**

Ready for the next piece?

---

## Step 4: Start the Function Definition

**Add after the imports:**

```python


def are_equivalent(
    variables: List[str],
    expression1: Callable[[Dict[str, bool]], bool],
    expression2: Callable[[Dict[str, bool]], bool]
) -> bool:
```

**Stop. Let's understand this:**

**Two blank lines** before function (PEP 8 style - separates from imports)

**Function name**: `are_equivalent`

- Descriptive name
- Returns boolean (True if equivalent, False if not)
- Follows Python convention: functions that return bool often start with `is_` or `are_`

**Parameters breakdown:**

1. `variables: List[str]`
   - List of variable names like `['p', 'q']`
2. `expression1: Callable[[Dict[str, bool]], bool]`
   - First expression to compare
   - It's a function that takes `{'p': True, 'q': False}` and returns `bool`
3. `expression2: Callable[[Dict[str, bool]], bool]`
   - Second expression to compare
   - Same type as expression1

**Return type**: `-> bool`

- Returns `True` if equivalent
- Returns `False` if different

**Type this function signature. Save.**

Does this make sense so far?

---

## Step 5: Add the Docstring

**Inside the function, add:**

```python
    """
    Check if two logical expressions are equivalent.

    Two expressions are equivalent if they produce identical
    results for all possible combinations of input values.

    Args:
        variables: List of variable names used in both expressions
        expression1: First logical expression
        expression2: Second logical expression

    Returns:
        True if expressions are equivalent, False otherwise
    """
```

**Stop. Explanation:**

**Indentation**: 4 spaces (inside the function)

**Docstring structure**:

- Brief description (first line)
- Longer explanation (after blank line)
- Args section (what inputs mean)
- Returns section (what comes out)

This follows **Google Python Style Guide**.

**Type this docstring, maintaining the indentation. Save.**

Ready to implement the logic?

---

## Step 6: Generate Both Truth Tables

**After the docstring, add:**

```python
    # Generate truth tables for both expressions
    table1 = generate_truth_table(variables, expression1)
    table2 = generate_truth_table(variables, expression2)
```

**Stop. Let's understand:**

**Comment** explains what the next code does

- Good practice: explain the "why" not just the "what"

**Line 2**: Call `generate_truth_table` for first expression

- `variables` is the list of variable names
- `expression1` is the first function
- Returns a list of tuples: `[((True, True), True), ...]`
- Store in `table1`

**Line 3**: Same for second expression

- Store in `table2`

**What we have now:**

```python
table1 = [((True, True), True), ((True, False), False), ...]
table2 = [((True, True), True), ((True, False), False), ...]
```

**Type these two lines. Save.**

Got it?

---

## Step 7: Compare the Tables

**Add next:**

```python

    # Compare every row
    for row1, row2 in zip(table1, table2):
```

**Stop. Explanation:**

**Blank line** before new logical section

**`zip(table1, table2)`** pairs up rows from both tables:

```python
table1 = [row_a, row_b, row_c]
table2 = [row_x, row_y, row_z]

zip pairs:
(row_a, row_x)
(row_b, row_y)
(row_c, row_z)
```

**The loop** iterates through paired rows:

- First iteration: `row1 = row_a`, `row2 = row_x`
- Second iteration: `row1 = row_b`, `row2 = row_y`
- etc.

**Type this line. Save.**

Make sense?

---

## Step 8: Extract the Results

**Inside the loop, add:**

```python
        # Each row is ((inputs), result)
        inputs1, result1 = row1
        inputs2, result2 = row2
```

**Stop. Explanation:**

**Indentation**: 8 spaces (inside the for loop)

**Comment** explains the structure

**Tuple unpacking**:

```python
row1 = ((True, False), True)
#         ↓            ↓
#      inputs1      result1
```

Unpacking splits the tuple:

- `inputs1 = (True, False)`
- `result1 = True`

**Same for row2**

**Type these three lines. Save.**

Clear?

---

## Step 9: Check If Results Differ

**Add next:**

```python

        # If any results differ, expressions are not equivalent
        if result1 != result2:
            return False
```

**Stop. Explanation:**

**Blank line** for readability

**Comment** explains the logic

**The check**: `if result1 != result2:`

- If the results are different for this input combination
- The expressions are NOT equivalent
- We can immediately return `False`

**Early return** is efficient:

- Don't need to check remaining rows
- Found a difference = proven not equivalent

**Example:**

```python
# Expression 1 gives True for (True, False)
# Expression 2 gives False for (True, False)
# They're different! Return False immediately.
```

**Type these three lines. Save.**

Understand why we return False here?

---

## Step 10: Return True If No Differences Found

**Outside the loop (same indentation as the `for`), add:**

```python

    # If we checked all rows without finding differences, they're equivalent
    return True
```

**Stop. Explanation:**

**Indentation**: Back to 4 spaces (inside function, but outside loop)

**Logic**:

- If the loop completes without returning False
- That means every row matched
- Therefore, the expressions are equivalent!

**Think about it:**

```
Check row 1: results match ✓
Check row 2: results match ✓
Check row 3: results match ✓
Check row 4: results match ✓
All rows checked, no differences → equivalent!
```

**Type these two lines. Save.**

---

## Step 11: Review the Complete Function

**Your complete `equivalence.py` should look like:**

```python
"""
Logical equivalence checking.

Two logical expressions are equivalent if they produce identical
truth tables for all possible input combinations.

Mathematical notation: p ≡ q means "p is equivalent to q"
"""

from typing import List, Dict, Callable
from foundations.logic.truth_tables import generate_truth_table


def are_equivalent(
    variables: List[str],
    expression1: Callable[[Dict[str, bool]], bool],
    expression2: Callable[[Dict[str, bool]], bool]
) -> bool:
    """
    Check if two logical expressions are equivalent.

    Two expressions are equivalent if they produce identical
    results for all possible combinations of input values.

    Args:
        variables: List of variable names used in both expressions
        expression1: First logical expression
        expression2: Second logical expression

    Returns:
        True if expressions are equivalent, False otherwise
    """
    # Generate truth tables for both expressions
    table1 = generate_truth_table(variables, expression1)
    table2 = generate_truth_table(variables, expression2)

    # Compare every row
    for row1, row2 in zip(table1, table2):
        # Each row is ((inputs), result)
        inputs1, result1 = row1
        inputs2, result2 = row2

        # If any results differ, expressions are not equivalent
        if result1 != result2:
            return False

    # If we checked all rows without finding differences, they're equivalent
    return True
```

**Save the file.**

Does your file match? Any questions before we test it?

---

## Step 12: Create Test File

Now let's test our function!

**Create**: `foundations/logic/test_equivalence.py`

Just create the empty file for now.

---

## Step 13: Add Test File Docstring and Imports

**In `test_equivalence.py`, type:**

```python
"""
Tests for logical equivalence checking.

We verify that equivalent expressions are correctly identified
and non-equivalent expressions are distinguished.
"""

from foundations.logic.equivalence import are_equivalent
from foundations.logic.operators import NOT, AND, OR, IMPLIES
```

**Stop. Explanation:**

**Docstring** explains what these tests do

**Import our new function**: `are_equivalent`

**Import operators** we'll use in tests: `NOT, AND, OR, IMPLIES`

**Type this. Save.**

Ready for the first test?

---

## Step 14: Write First Test - IMPLIES Equivalence

**Add:**

```python


def test_implies_equivalence():
    """
    Test that (p → q) is equivalent to (¬p ∨ q).

    This is a fundamental equivalence in logic.
    """
```

**Stop. Explanation:**

**Two blank lines** before test function (PEP 8)

**Test function name**: `test_implies_equivalence`

- MUST start with `test_` for pytest to find it
- Descriptive name

**Docstring** explains what mathematical fact we're testing

**Type this. Save.**

Now let's add the test body. Ready?

---

## Step 15: Set Up Variables for Test

**Inside the test function, add:**

```python
    # Set up
    variables = ['p', 'q']
```

**Stop. Explanation:**

**Comment**: "Set up" - this is the **Arrange** phase

**Variables list**: `['p', 'q']`

- Both expressions will use variables named 'p' and 'q'
- Must be the same for both

**Type this line. Save.**

---

## Step 16: Define First Expression

**Add:**

```python

    # First expression: p → q (using IMPLIES)
    expression1 = lambda v: IMPLIES(v['p'], v['q'])
```

**Stop. Explanation:**

**Blank line** for readability

**Comment** explains what this expression is

**Lambda function**:

- `lambda v:` - anonymous function taking parameter `v`
- `v` will be a dictionary like `{'p': True, 'q': False}`
- `IMPLIES(v['p'], v['q'])` - calls our IMPLIES operator
- Looks up 'p' and 'q' values from the dictionary

**Type these lines. Save.**

Understand the lambda?

---

## Step 17: Define Second Expression

**Add:**

```python

    # Second expression: ¬p ∨ q (NOT p OR q)
    expression2 = lambda v: OR(NOT(v['p']), v['q'])
```

**Stop. Explanation:**

**This is the equivalent form** of IMPLIES

**Lambda function**:

- `NOT(v['p'])` - negates p
- `OR(..., v['q'])` - OR with q
- Together: "NOT p OR q"

**These should be equivalent!**

**Type these lines. Save.**

---

## Step 18: Call the Function and Assert

**Add:**

```python

    # Act: Check if they're equivalent
    result = are_equivalent(variables, expression1, expression2)

    # Assert: They should be equivalent
    assert result == True, "p → q should be equivalent to ¬p ∨ q"
```

**Stop. Explanation:**

**Act phase**: Call our function

- Pass the variables list
- Pass both expressions
- Store result (True or False)

**Assert phase**: Verify result

- `assert result == True` - check it returned True
- The message explains what should be true
- If assertion fails, this message is shown

**Type these lines. Save.**

Ready to run the test?

---

## Step 19: Run Your First Equivalence Test

**Run:**

```bash
pytest foundations/logic/test_equivalence.py::test_implies_equivalence -v
```

**Did it pass? ✅**

If yes, great! If no, let me know what error you got.

---

## Step 20: Add Second Test - De Morgan's Law

Let's test another famous equivalence.

**In `test_equivalence.py`, add:**

```python


def test_de_morgans_law_and():
    """
    Test De Morgan's Law: ¬(p ∧ q) ≡ ¬p ∨ ¬q

    "NOT (p AND q)" is equivalent to "(NOT p) OR (NOT q)"
    """
    variables = ['p', 'q']

    # First expression: ¬(p ∧ q)
    expression1 = lambda v: NOT(AND(v['p'], v['q']))

    # Second expression: ¬p ∨ ¬q
    expression2 = lambda v: OR(NOT(v['p']), NOT(v['q']))

    result = are_equivalent(variables, expression1, expression2)

    assert result == True, "De Morgan's Law should hold"
```

**Stop. What's different here?**

**De Morgan's Law** is a famous equivalence:

- "NOT (A AND B)" = "(NOT A) OR (NOT B)"

**Expression 1**: `NOT(AND(v['p'], v['q']))`

- First AND them: `p ∧ q`
- Then NOT the result: `¬(p ∧ q)`

**Expression 2**: `OR(NOT(v['p']), NOT(v['q']))`

- NOT each one: `¬p`, `¬q`
- Then OR them: `¬p ∨ ¬q`

**These should be equivalent!**

**Type this test. Save.**

---

## Step 21: Test a Non-Equivalence

Let's test that our function correctly identifies when expressions are NOT equivalent.

**Add:**

```python


def test_not_equivalent():
    """
    Test that non-equivalent expressions are correctly identified.

    p → q is NOT equivalent to q → p (implication is not symmetric)
    """
    variables = ['p', 'q']

    # These are NOT equivalent
    expression1 = lambda v: IMPLIES(v['p'], v['q'])  # p → q
    expression2 = lambda v: IMPLIES(v['q'], v['p'])  # q → p

    result = are_equivalent(variables, expression1, expression2)

    assert result == False, "p → q should NOT be equivalent to q → p"
```

**Stop. Explanation:**

**This tests the negative case**: They should NOT be equivalent

**Why aren't they equivalent?**

Consider: "If it rains, the ground is wet"

- This is true
- Reverse: "If the ground is wet, it rained"
- This is false! (could be sprinkler)

**Implication is NOT symmetric!**

**We assert `result == False`** because they're different.

**Type this test. Save.**

---

## Step 22: Run All Equivalence Tests

**Run:**

```bash
pytest foundations/logic/test_equivalence.py -v
```

**You should see 3 passing tests:**

- test_implies_equivalence ✅
- test_de_morgans_law_and ✅
- test_not_equivalent ✅

**Did all three pass?**

If yes, excellent! If no, what error did you get?

---

## Step 23: Run ALL Tests

Let's verify everything still works together:

```bash
pytest foundations/logic/ -v
```

**You should see:**

- 29 passing tests total
- All green ✅

**How many do you have?**

---

## Step 24: Add a Comparison Function

Let's add one more function to make comparisons easier to visualize.

**In `equivalence.py`, add after the `are_equivalent` function:**

```python


def compare_expressions(
    variables: List[str],
    expression1: Callable[[Dict[str, bool]], bool],
    expression1_name: str,
    expression2: Callable[[Dict[str, bool]], bool],
    expression2_name: str
) -> None:
```

**Stop. Explanation:**

**New function**: `compare_expressions`

- Will show tables side-by-side
- Visual comparison

**Parameters:**

- Same variables and expressions
- Plus **names** for each expression (for display)
- Example names: "p → q", "¬p ∨ q"

**Return type**: `-> None`

- Doesn't return anything
- Just prints to console

**Type this function signature. Save.**

Ready for the docstring?

---

## Step 25: Add Docstring

**Add:**

```python
    """
    Compare two expressions by showing their truth tables side by side.

    This helps visualize whether expressions are equivalent.
    Shows each combination and both results.

    Args:
        variables: Variable names
        expression1: First expression
        expression1_name: Display name for first expression
        expression2: Second expression
        expression2_name: Display name for second expression

    Returns:
        None (prints comparison to console)
    """
```

**Type this docstring. Save.**

Ready for implementation?

---

## Step 26: Generate Tables and Print Header

**Add:**

```python
    # Generate both truth tables
    table1 = generate_truth_table(variables, expression1)
    table2 = generate_truth_table(variables, expression2)

    # Print header
    print(f"\nComparing: {expression1_name} vs {expression2_name}")
    print("=" * 70)
```

**Stop. Explanation:**

**First two lines**: Generate both tables (we've done this before)

**Print header**:

- Shows which expressions we're comparing
- `"=" * 70` creates a line of 70 equals signs (separator)

**Type these lines. Save.**

---

## Step 27: Print Column Headers

**Add:**

```python

    # Create column headers
    header_parts = [f"{var:^6}" for var in variables]
    header_parts.append(f"{expression1_name:^20}")
    header_parts.append(f"{expression2_name:^20}")
    header_parts.append("Same?")

    header = " | ".join(header_parts)
    print(header)
    print("-" * 70)
```

**Stop. Explanation:**

**List comprehension**: `[f"{var:^6}" for var in variables]`

- Creates centered variable names
- Example: `["  p   ", "  q   "]`

**Append expression names**: 20 characters wide each

**Append "Same?" column**: Shows if results match

**Join with " | "**: Creates table structure

**Separator line**: `"-" * 70`

**Type these lines. Save.**

Understand the formatting?

---

## Step 28: Print Each Row

**Add:**

```python

    # Print each row
    for (inputs1, result1), (inputs2, result2) in zip(table1, table2):
        # Format input values
        row_parts = [f"{'T' if val else 'F':^6}" for val in inputs1]

        # Format results
        row_parts.append(f"{'T' if result1 else 'F':^20}")
        row_parts.append(f"{'T' if result2 else 'F':^20}")

        # Check if same
        same = "✓" if result1 == result2 else "✗"
        row_parts.append(same)

        row = " | ".join(row_parts)
        print(row)
```

**Stop. Let me explain each part:**

**Line 1**: Loop through both tables simultaneously

- `zip(table1, table2)` pairs up rows
- Unpacking extracts inputs and results from both

**Line 2-3**: Format input values (True/False → T/F)

**Line 5-6**: Format results for both expressions

**Line 8-10**: Check if results match

- `"✓"` if same (equivalent for this row)
- `"✗"` if different

**Line 12-13**: Join and print the row

**Type these lines. Save.**

---

## Step 29: Print Summary

**Add:**

```python

    # Print summary
    equivalent = are_equivalent(variables, expression1, expression2)
    print("=" * 70)
    if equivalent:
        print("✓ EQUIVALENT - These expressions always give the same result")
    else:
        print("✗ NOT EQUIVALENT - These expressions differ")
```

**Stop. Explanation:**

**Call `are_equivalent`**: Get the final verdict

**Print appropriate message**:

- If equivalent: celebration message ✓
- If not: explanation ✗

**Type these lines. Save.**

---

## Step 30: Test the Comparison Function

Let's create a demo to see it in action!

**Create**: `foundations/logic/demo_equivalence.py`

**Add:**

```python
"""
Demonstration of logical equivalence checking.

Shows how to compare logical expressions and verify equivalences.
"""

from foundations.logic.equivalence import compare_expressions
from foundations.logic.operators import NOT, AND, OR, IMPLIES


if __name__ == "__main__":
    print("\n" + "="*70)
    print("LOGICAL EQUIVALENCE DEMONSTRATIONS")
    print("="*70)

    # Demo 1: IMPLIES equivalence
    compare_expressions(
        variables=['p', 'q'],
        expression1=lambda v: IMPLIES(v['p'], v['q']),
        expression1_name="p → q",
        expression2=lambda v: OR(NOT(v['p']), v['q']),
        expression2_name="¬p ∨ q"
    )
```

**Type this. Save.**

**Run it:**

```bash
python foundations/logic/demo_equivalence.py
```

**Do you see a nice side-by-side comparison?**

---

## Step 31: Add More Demos

**In `demo_equivalence.py`, add at the end (before the closing of `if __name__`):**

```python

    # Demo 2: De Morgan's Law
    compare_expressions(
        variables=['p', 'q'],
        expression1=lambda v: NOT(AND(v['p'], v['q'])),
        expression1_name="¬(p ∧ q)",
        expression2=lambda v: OR(NOT(v['p']), NOT(v['q'])),
        expression2_name="¬p ∨ ¬q"
    )

    # Demo 3: Non-equivalent (implication is not symmetric)
    compare_expressions(
        variables=['p', 'q'],
        expression1=lambda v: IMPLIES(v['p'], v['q']),
        expression1_name="p → q",
        expression2=lambda v: IMPLIES(v['q'], v['p']),
        expression2_name="q → p"
    )
```

**Type these. Save.**

**Run again:**

```bash
python foundations/logic/demo_equivalence.py
```

**You should see three comparisons!**

Do they all look good? Which one shows ✗ (not equivalent)?

---

## Step 32: Commit Your Work

Time to save progress!

```bash
git status
```

**What files changed?**

```bash
git add foundations/logic/equivalence.py
git add foundations/logic/test_equivalence.py
git add foundations/logic/demo_equivalence.py
```

**Commit:**

```bash
git commit -m "Add logical equivalence checking

- Implement are_equivalent function
  - Compares truth tables row by row
  - Returns True if identical, False if different
  - Early return for efficiency

- Implement compare_expressions function
  - Visual side-by-side comparison
  - Shows which rows match/differ
  - Clear equivalent/not equivalent verdict

- Add comprehensive tests
  - Test IMPLIES equivalence
  - Test De Morgan's Law
  - Test non-equivalent expressions

- Add demonstration script
  - Shows famous equivalences
  - Demonstrates visual comparison"
```

**Did it commit successfully?**

---

## Progress Check

**Run all tests:**

```bash
pytest foundations/logic/ -v
```

**How many tests pass?**

You should have: 29 tests total

**Check coverage:**

```bash
pytest foundations/logic/ --cov=foundations.logic --cov-report=term-missing
```

**What's your coverage percentage?**

Should be 100%!

---

## What We've Built

In this section, you learned to:

**Build incrementally**:

- Type small pieces
- Understand each part
- Test as you go

**New functions**:

- ✅ `are_equivalent` - check if expressions match
- ✅ `compare_expressions` - visual comparison

**New concepts**:

- ✅ Comparing data structures
- ✅ Early returns for efficiency
- ✅ Side-by-side display formatting
- ✅ Unicode symbols (✓, ✗)

---

## What's Next?

We now have a complete logic foundation:

- ✅ All five operators
- ✅ Truth table generation
- ✅ Equivalence checking
- ✅ Visual comparison

**Next up**: Building our first **visualization** - interactive truth tables in HTML/JavaScript!

This will teach you:

- HTML structure
- CSS styling
- JavaScript logic
- How math concepts translate to interactive web pages

**Ready to start building the web visualization?** This is where things get visual and interactive!
