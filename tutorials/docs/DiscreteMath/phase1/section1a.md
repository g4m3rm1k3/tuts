# Section 1 Continued: Advanced Logical Operators

## 1.6 The IMPLIES Operator - Where Logic Gets Interesting

### Introduction: The Most Misunderstood Operator

The IMPLIES operator (also called **implication** or **conditional**) is the **most confusing** operator in logic. Even experienced programmers struggle with it.

**Why does it matter?**

- Every `if` statement is related to implication
- Critical for proofs and reasoning
- Understanding this deeply separates beginners from experts

Let's build understanding from the ground up.

---

### The Real-World Intuition

Think of implication as a **promise** or **guarantee**.

**Example promise**: "If it rains today, I'll bring an umbrella."

Let's analyze when this promise is **kept** vs **broken**:

**Scenario 1**: It rains, and I bring an umbrella

- ✅ **Promise kept** (I did what I said)

**Scenario 2**: It rains, and I DON'T bring an umbrella

- ❌ **Promise broken** (I failed to do what I said)

**Scenario 3**: It doesn't rain, and I bring an umbrella

- ✅ **Promise kept** (I can bring an umbrella anytime!)

**Scenario 4**: It doesn't rain, and I DON'T bring an umbrella

- ✅ **Promise kept** (I only promised to bring it IF it rains)

**Key insight**: The promise can only be **broken** when the condition is true but the consequence doesn't follow.

---

### Mathematical Foundation

**Notation**: $p \rightarrow q$ (read as "p implies q" or "if p then q")

**Definition**: $p \rightarrow q$ is FALSE only when $p$ is TRUE and $q$ is FALSE

**Truth table**:

| $p$ | $q$ | $p \rightarrow q$       |
| --- | --- | ----------------------- |
| T   | T   | T                       |
| T   | F   | **F** ← only false case |
| F   | T   | T                       |
| F   | F   | T                       |

**The shocking part**: When $p$ is false, the implication is **always true**!

This is called **vacuous truth** (true by default when the premise doesn't hold).

---

### Why IMPLIES = (NOT p) OR q

There's a mathematical equivalence that's crucial to understand:

$$p \rightarrow q \equiv (\neg p) \vee q$$

"If p then q" is the same as "NOT p OR q"

**Let's verify with our truth table**:

| $p$ | $q$ | $\neg p$ | $(\neg p) \vee q$ | $p \rightarrow q$ | Same? |
| --- | --- | -------- | ----------------- | ----------------- | ----- |
| T   | T   | F        | T                 | T                 | ✓     |
| T   | F   | F        | F                 | F                 | ✓     |
| F   | T   | T        | T                 | T                 | ✓     |
| F   | F   | T        | T                 | T                 | ✓     |

**They're identical!** This is why we can implement IMPLIES as `(not p) or q`.

---

### Code Along: Implement IMPLIES

Add to `foundations/logic/operators.py`:

```python


def IMPLIES(p: bool, q: bool) -> bool:
    """
    Logical IMPLIES operator (implication, conditional).

    Returns False ONLY when the premise (p) is True but the conclusion (q) is False.
    This is the only case where an implication is violated.

    Mathematical notation: p → q (read as "p implies q" or "if p then q")

    Important: This is NOT the same as "if p: q" in code!
    - In logic: p → q is a statement that evaluates to True or False
    - In code: if p: q is a control flow statement that executes q when p is True

    Args:
        p: The premise (hypothesis, the "if" part)
        q: The conclusion (consequent, the "then" part)

    Returns:
        True in all cases except when p is True and q is False

    Truth table:
        p    | q    | p → q
        -----|------|-------
        T    | T    | T
        T    | F    | F     ← only False case!
        F    | T    | T
        F    | F    | T

    Mathematical equivalence:
        p → q ≡ ¬p ∨ q
        "if p then q" is equivalent to "not p or q"

    Examples:
        >>> IMPLIES(True, True)
        True
        >>> IMPLIES(True, False)
        False
        >>> IMPLIES(False, True)
        True
        >>> IMPLIES(False, False)
        True

    Real-world examples:
        1. Warranty: "If product is defective, we'll refund you"
           - Defective AND refunded: promise kept (True)
           - Defective AND NOT refunded: promise broken (False)
           - NOT defective: promise kept regardless (True)

        2. Access control: "If user is NOT premium, then rate limit applies"
           - Not premium AND rate limited: correct (True)
           - Not premium AND NOT rate limited: violation (False)
           - Premium user: no obligation, always True

    Common confusion:
        Students often think p → q means "p causes q" or "q only when p"
        But it actually means "whenever p is true, q must also be true"
        When p is false, q can be anything - the implication is vacuously true.
    """
    return (not p) or q
```

**Save the file.**

---

### Explanation: The Implementation

```python
    return (not p) or q
```

**Why this works:**

Let's trace through each case:

**Case 1: p=True, q=True**

```python
(not True) or True
False or True
True ✓
```

**Case 2: p=True, q=False**

```python
(not True) or False
False or False
False ✓ (this is the only False case!)
```

**Case 3: p=False, q=True**

```python
(not False) or True
True or True
True ✓
```

**Case 4: p=False, q=False**

```python
(not False) or False
True or False
True ✓
```

**It works for all cases!**

---

### Understanding: Parentheses Matter

```python
return (not p) or q
```

**Why the parentheses around `not p`?**

**Operator precedence** in Python:

1. `not` (highest)
2. `and`
3. `or` (lowest)

**Without parentheses**, it still works:

```python
return not p or q  # Same as (not p) or q
```

**But parentheses make it clearer:**

- Shows we're negating `p` first
- Then OR-ing with `q`
- Easier to read

**If we wrote:**

```python
return not (p or q)  # WRONG! This is different
```

This would be De Morgan's Law: $\neg(p \vee q) = (\neg p) \wedge (\neg q)$

Not what we want!

---

### Code Along: Test IMPLIES

Create **File**: `foundations/logic/test_implies.py`

```python
"""
Tests for the IMPLIES operator.

IMPLIES is tricky! Only False when premise is True and conclusion is False.
We test all four cases to ensure correctness.

Think of it as a promise:
- T → T: Promise kept (True)
- T → F: Promise broken (False)
- F → T: No obligation, promise kept (True)
- F → F: No obligation, promise kept (True)
"""

from foundations.logic.operators import IMPLIES


def test_implies_true_true():
    """
    Test IMPLIES(True, True) = True

    Premise is true, conclusion is true.
    Promise kept!

    Example: "If it rains (True), I'll bring umbrella (True)" ✓
    """
    # Arrange
    p = True
    q = True

    # Act
    result = IMPLIES(p, q)

    # Assert
    assert result == True, "When both are True, implication should be True"


def test_implies_true_false():
    """
    Test IMPLIES(True, False) = False

    THIS IS THE ONLY FALSE CASE!
    Premise is true, but conclusion is false.
    Promise broken!

    Example: "If it rains (True), I'll bring umbrella (False)" ✗
    """
    p = True
    q = False
    result = IMPLIES(p, q)
    assert result == False, "This is the only case where implication is False"


def test_implies_false_true():
    """
    Test IMPLIES(False, True) = True

    Premise is false, conclusion is true.
    Promise kept (vacuously true).

    Example: "If it rains (False), I'll bring umbrella (True)" ✓
    I brought an umbrella even though it didn't rain. Promise not broken!
    """
    p = False
    q = True
    result = IMPLIES(p, q)
    assert result == True, "When premise is False, implication is vacuously True"


def test_implies_false_false():
    """
    Test IMPLIES(False, False) = True

    Premise is false, conclusion is false.
    Promise kept (vacuously true).

    Example: "If it rains (False), I'll bring umbrella (False)" ✓
    It didn't rain, I didn't bring umbrella. I only promised IF it rained!
    """
    p = False
    q = False
    result = IMPLIES(p, q)
    assert result == True, "When premise is False, implication is vacuously True"


def test_implies_equivalence_to_not_or():
    """
    Test that IMPLIES(p, q) is equivalent to (NOT p) OR q

    This is a mathematical equivalence:
    p → q ≡ ¬p ∨ q

    We verify it works for all cases.
    """
    from foundations.logic.operators import NOT, OR

    # Test all four combinations
    test_cases = [
        (True, True),
        (True, False),
        (False, True),
        (False, False)
    ]

    for p, q in test_cases:
        implies_result = IMPLIES(p, q)
        equivalent_result = OR(NOT(p), q)

        assert implies_result == equivalent_result, \
            f"For p={p}, q={q}: IMPLIES should equal (NOT p) OR q"
```

**Save and run:**

```bash
pytest foundations/logic/test_implies.py -v
```

**You should see 5 passing tests!**

---

### Explanation: Assert Messages

```python
assert result == True, "When both are True, implication should be True"
```

**The comma adds a custom message:**

- Shown only if the assertion **fails**
- Explains what went wrong
- Makes debugging easier

**Without message:**

```
AssertionError
```

Not helpful!

**With message:**

```
AssertionError: When both are True, implication should be True
```

Much clearer!

**Good practice**: Add messages to complex assertions.

---

### Explanation: Testing Equivalence

```python
def test_implies_equivalence_to_not_or():
```

This test verifies a **mathematical theorem**:

$$p \rightarrow q \equiv (\neg p) \vee q$$

**Why test this?**

- Proves our implementation is correct
- Demonstrates the mathematical relationship
- Documents the equivalence for future readers

```python
    test_cases = [
        (True, True),
        (True, False),
        (False, True),
        (False, False)
    ]
```

**List of tuples:**

- Each tuple is a test case: `(p_value, q_value)`
- We'll loop through and test each one

```python
    for p, q in test_cases:
        implies_result = IMPLIES(p, q)
        equivalent_result = OR(NOT(p), q)

        assert implies_result == equivalent_result
```

**For each test case:**

1. Calculate `IMPLIES(p, q)`
2. Calculate `OR(NOT(p), q)`
3. Assert they're equal

If they're equal for **all** cases, the equivalence holds!

---

### Deep Dive: Why IMPLIES Works This Way

**Question**: Why is "False implies anything" true?

**Answer**: It's about logical consistency. Let's explore:

**Consider this statement**: "If 2+2=5, then I'm the King of France"

Is this true or false?

- The premise (2+2=5) is **false**
- The conclusion (I'm the King of France) is **false**
- The implication is... **TRUE**!

**Why?** Because the premise is false, I can never be proven wrong. The statement makes no actual claim about reality when the premise doesn't hold.

**Real-world programming example**:

```python
# API rate limiting rule:
# "If user is NOT premium, then rate limit applies"

def should_rate_limit(is_premium, rate_limit_applies):
    return IMPLIES(not is_premium, rate_limit_applies)

# Test cases:
# NOT premium (True), rate limit applies (True) → True ✓
# NOT premium (True), NO rate limit (False) → False ✗ (violation!)
# Premium (False), rate limit applies (True) → True ✓
# Premium (False), NO rate limit (False) → True ✓

# When user IS premium (premise False), the rule doesn't apply!
# They can make unlimited requests - the implication is satisfied.
```

**Further reading:**

- [Material Conditional (Wikipedia)](https://en.wikipedia.org/wiki/Material_conditional)
- [Vacuous Truth (Stanford Encyclopedia)](https://plato.stanford.edu/entries/truth-values/)

---

## 1.7 The IFF Operator - Bidirectional Implication

### Introduction: Both Directions Matter

**IFF** stands for "**If and Only If**" (also called **biconditional**).

**The difference**:

**IMPLIES** ($\rightarrow$): One direction

- "If it rains, then the ground is wet"
- Rain → Wet
- But the ground can be wet for other reasons (sprinkler)

**IFF** ($\leftrightarrow$): Both directions

- "The alarm sounds if and only if motion is detected"
- Motion → Alarm **AND** Alarm → Motion
- No other reason for alarm to sound

---

### Mathematical Foundation

**Notation**: $p \leftrightarrow q$ (read as "p if and only if q" or "p iff q")

**Definition**: $p \leftrightarrow q$ is TRUE when $p$ and $q$ have the **same truth value**

**Truth table**:

| $p$ | $q$ | $p \leftrightarrow q$ |
| --- | --- | --------------------- |
| T   | T   | T ← same values       |
| T   | F   | F ← different values  |
| F   | T   | F ← different values  |
| F   | F   | T ← same values       |

**Mathematical equivalence**:

$$p \leftrightarrow q \equiv (p \rightarrow q) \wedge (q \rightarrow p)$$

"p iff q" means "if p then q" **AND** "if q then p"

Both directions must hold!

---

### The Simple Implementation

For boolean values, IFF is just **equality**:

$$p \leftrightarrow q \equiv (p = q)$$

When do $p$ and $q$ have the same truth value? When they're **equal**!

---

### Code Along: Implement IFF

Add to `foundations/logic/operators.py`:

```python


def IFF(p: bool, q: bool) -> bool:
    """
    Logical IFF operator (biconditional, if and only if).

    Returns True when both inputs have the SAME truth value.
    Returns False when inputs have DIFFERENT truth values.

    Mathematical notation: p ↔ q (read as "p if and only if q" or "p iff q")

    This is bidirectional implication:
    p ↔ q means both (p → q) AND (q → p)

    Args:
        p: First boolean value
        q: Second boolean value

    Returns:
        True if p and q have the same truth value, False otherwise

    Truth table:
        p    | q    | p ↔ q
        -----|------|-------
        T    | T    | T     ← same
        T    | F    | F     ← different
        F    | T    | F     ← different
        F    | F    | T     ← same

    Mathematical equivalences:
        1. p ↔ q ≡ (p → q) ∧ (q → p)
           "p iff q" means "p implies q" AND "q implies p"

        2. p ↔ q ≡ (p ∧ q) ∨ (¬p ∧ ¬q)
           "both true" OR "both false"

        3. For booleans: p ↔ q ≡ (p = q)
           Simply checking equality!

    Examples:
        >>> IFF(True, True)
        True
        >>> IFF(True, False)
        False
        >>> IFF(False, True)
        False
        >>> IFF(False, False)
        True

    Real-world examples:
        1. File sync: "File is synced ↔ timestamps match"
           - Synced AND matching timestamps: True
           - Synced AND different timestamps: False (impossible!)
           - Not synced AND matching timestamps: False (impossible!)
           - Not synced AND different timestamps: True

        2. Data integrity: "Data is valid ↔ checksum matches"
           Either both conditions hold or neither does.

        3. Authentication: "User logged in ↔ valid session token exists"
           These must always be in sync.

    Difference from IMPLIES:
        IMPLIES is one-directional:
            "If it rains → ground is wet"
            But ground can be wet without rain (sprinkler)

        IFF is bidirectional:
            "Alarm sounds ↔ motion detected"
            No other cause for alarm
            If alarm sounds, there WAS motion
            If motion, alarm WILL sound
    """
    return p == q
```

**Save the file.**

---

### Explanation: The Implementation

```python
    return p == q
```

**Why this simple implementation works:**

For boolean values, "same truth value" is just **equality**!

| $p$ | $q$ | $p = q$ |
| --- | --- | ------- |
| T   | T   | T       |
| T   | F   | F       |
| F   | T   | F       |
| F   | F   | T       |

Perfect match with the IFF truth table!

---

### Understanding: IFF vs IMPLIES

**IMPLIES** ($p \rightarrow q$):

```python
"If user is admin, then has full access"
```

**One direction only:**

- Admin → Full Access (True)
- Full Access → Admin (False! Could be superuser)

**IFF** ($p \leftrightarrow q$):

```python
"User has badge access iff badge is activated"
```

**Both directions:**

- Badge access → Activated (True)
- Activated → Badge access (True)
- These are **completely synchronized**

---

### Code Along: Test IFF

Create **File**: `foundations/logic/test_iff.py`

```python
"""
Tests for the IFF operator.

IFF returns True when both inputs have the same truth value.
It's bidirectional - both directions of implication must hold.

Think of it as "logical equality" - returns True when p and q match.
"""

from foundations.logic.operators import IFF, IMPLIES, AND


def test_iff_true_true():
    """
    Test IFF(True, True) = True

    Both have same truth value (both True).
    Example: "File synced (T) ↔ Timestamps match (T)" ✓
    """
    assert IFF(True, True) == True


def test_iff_true_false():
    """
    Test IFF(True, False) = False

    Different truth values.
    Example: "File synced (T) ↔ Timestamps match (F)" ✗
    Impossible state!
    """
    assert IFF(True, False) == False


def test_iff_false_true():
    """
    Test IFF(False, True) = False

    Different truth values.
    Example: "File synced (F) ↔ Timestamps match (T)" ✗
    Impossible state!
    """
    assert IFF(False, True) == False


def test_iff_false_false():
    """
    Test IFF(False, False) = True

    Both have same truth value (both False).
    Example: "File synced (F) ↔ Timestamps match (F)" ✓
    """
    assert IFF(False, False) == True


def test_iff_is_equality():
    """
    Test that IFF(p, q) is the same as (p == q) for booleans.

    Mathematical fact: For boolean values, ↔ is just equality.
    """
    test_cases = [
        (True, True),
        (True, False),
        (False, True),
        (False, False)
    ]

    for p, q in test_cases:
        iff_result = IFF(p, q)
        equality_result = (p == q)

        assert iff_result == equality_result, \
            f"IFF({p}, {q}) should equal ({p} == {q})"


def test_iff_is_bidirectional_implies():
    """
    Test that IFF(p, q) equals (p → q) ∧ (q → p)

    Mathematical equivalence:
    p ↔ q ≡ (p → q) ∧ (q → p)

    IFF means both directions of implication hold.
    """
    test_cases = [
        (True, True),
        (True, False),
        (False, True),
        (False, False)
    ]

    for p, q in test_cases:
        iff_result = IFF(p, q)

        # (p → q) ∧ (q → p)
        bidirectional = AND(IMPLIES(p, q), IMPLIES(q, p))

        assert iff_result == bidirectional, \
            f"IFF({p}, {q}) should equal (IMPLIES({p}, {q}) AND IMPLIES({q}, {p}))"


def test_iff_symmetry():
    """
    Test that IFF is symmetric: IFF(p, q) = IFF(q, p)

    Order doesn't matter for biconditional.
    p ↔ q is the same as q ↔ p
    """
    test_cases = [
        (True, True),
        (True, False),
        (False, True),
        (False, False)
    ]

    for p, q in test_cases:
        forward = IFF(p, q)
        backward = IFF(q, p)

        assert forward == backward, \
            f"IFF should be symmetric: IFF({p}, {q}) should equal IFF({q}, {p})"
```

**Save and run:**

```bash
pytest foundations/logic/test_iff.py -v
```

**You should see 7 passing tests!**

---

### Explanation: Testing Symmetry

```python
def test_iff_symmetry():
```

**Symmetry** means order doesn't matter:

$$p \leftrightarrow q = q \leftrightarrow p$$

**For IFF, this should be true:**

- IFF(True, False) = IFF(False, True)
- Both return False

**Why test this?**

- Verifies mathematical property
- Catches implementation bugs
- Documents expected behavior

**Contrast with IMPLIES:**

```python
IMPLIES(True, False)  # False
IMPLIES(False, True)  # True
# NOT symmetric!
```

IMPLIES is **not** symmetric because it's directional.

---

## 1.8 Running All Tests

Let's run all our tests together:

```bash
pytest foundations/logic/ -v
```

**You should see:**

```
======================== test session starts ========================
collected 22 items

foundations/logic/test_and.py::test_and_true_true PASSED      [  4%]
foundations/logic/test_and.py::test_and_true_false PASSED     [  9%]
foundations/logic/test_and.py::test_and_false_true PASSED     [ 13%]
foundations/logic/test_and.py::test_and_false_false PASSED    [ 18%]
foundations/logic/test_iff.py::test_iff_true_true PASSED      [ 22%]
foundations/logic/test_iff.py::test_iff_true_false PASSED     [ 27%]
foundations/logic/test_iff.py::test_iff_false_true PASSED     [ 31%]
foundations/logic/test_iff.py::test_iff_false_false PASSED    [ 36%]
foundations/logic/test_iff.py::test_iff_is_equality PASSED    [ 40%]
foundations/logic/test_iff.py::test_iff_is_bidirectional_implies PASSED [ 45%]
foundations/logic/test_iff.py::test_iff_symmetry PASSED       [ 50%]
foundations/logic/test_implies.py::test_implies_true_true PASSED [ 54%]
foundations/logic/test_implies.py::test_implies_true_false PASSED [ 59%]
foundations/logic/test_implies.py::test_implies_false_true PASSED [ 63%]
foundations/logic/test_implies.py::test_implies_false_false PASSED [ 68%]
foundations/logic/test_implies.py::test_implies_equivalence_to_not_or PASSED [ 72%]
foundations/logic/test_not.py::test_not_true PASSED           [ 77%]
foundations/logic/test_not.py::test_not_false PASSED          [ 81%]
foundations/logic/test_or.py::test_or_true_true PASSED        [ 86%]
foundations/logic/test_or.py::test_or_true_false PASSED       [ 90%]
foundations/logic/test_or.py::test_or_false_true PASSED       [ 95%]
foundations/logic/test_or.py::test_or_false_false PASSED      [100%]

========================= 22 passed in 0.08s =========================
```

**22 passing tests! �**

---

### Understanding: Test Coverage

Let's check what percentage of our code is tested:

```bash
pytest foundations/logic/ --cov=foundations.logic --cov-report=term-missing
```

**You should see:**

```
---------- coverage: platform ..., python ... -----------
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
foundations/logic/__init__.py           0      0   100%
foundations/logic/operators.py          5      0   100%
-----------------------------------------------------------------
TOTAL                                   5      0   100%
```

**100% coverage!** Every line of code is tested.

---

### Explanation: Code Coverage

**What is code coverage?**

- Percentage of code executed by tests
- Shows untested code
- Helps find gaps

**Reading the report:**

- **Stmts**: Number of statements (lines of code)
- **Miss**: Statements not executed by tests
- **Cover**: Percentage covered

**100% coverage means:**

- Every function was called
- Every line was executed
- High confidence in correctness

**Why it matters:**

```python
def divide(a, b):
    if b == 0:
        return None  # This line not tested!
    return a / b
```

Without coverage, you might not realize you never tested the `b == 0` case!

**Further reading:**

- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Code Coverage Best Practices](https://martinfowler.com/bliki/TestCoverage.html)

---

## 1.9 Commit Your Progress

Time to save our work!

```bash
# Check status
git status

# Add new files
git add foundations/logic/

# Commit
git commit -m "Add IMPLIES and IFF logical operators

- Implement IMPLIES operator (p → q)
  - Include detailed explanation of vacuous truth
  - Document equivalence to (¬p ∨ q)
  - Add real-world examples (warranties, rate limiting)

- Implement IFF operator (p ↔ q)
  - Document bidirectional nature
  - Show equivalence to (p → q) ∧ (q → p)
  - Demonstrate symmetry property

- Add comprehensive test suites
  - Test all truth table cases
  - Verify mathematical equivalences
  - Test symmetry and other properties
  - 22 tests total, 100% code coverage

All operators now complete: NOT, AND, OR, IMPLIES, IFF"

# View history
git log --oneline
```

---

## Progress Check & Summary

### What We've Built

**Five core logical operators:**

- ✅ NOT ($\neg$) - Negation
- ✅ AND ($\wedge$) - Conjunction
- ✅ OR ($\vee$) - Disjunction
- ✅ IMPLIES ($\rightarrow$) - Implication
- ✅ IFF ($\leftrightarrow$) - Biconditional

**Complete test suite:**

- ✅ 22 tests covering all operators
- ✅ 100% code coverage
- ✅ Mathematical equivalences verified
- ✅ Properties tested (symmetry, etc.)

**Professional practices:**

- ✅ Type hints on all functions
- ✅ Comprehensive docstrings
- ✅ Real-world examples
- ✅ Version control with meaningful commits

---

### What You've Learned

**Discrete Math Concepts:**

1. Propositions and truth values
2. Five logical operators and their truth tables
3. Logical equivalences (IMPLIES ≡ (NOT p) OR q)
4. Vacuous truth
5. Symmetry and other properties

**Programming Concepts:**

1. Functions with parameters and return values
2. Type hints (`bool`, `-> bool`)
3. Docstrings (comprehensive documentation)
4. Test-driven development
5. pytest framework
6. Code coverage analysis
7. Git workflow and commits

**Skills Developed:**

1. Reading mathematical notation
2. Implementing mathematical concepts in code
3. Writing thorough tests
4. Documenting code professionally
5. Using version control effectively

---

## What's Next?

We have the **operators**. Now we need tools to analyze them!

**Coming up:**

1. **Truth Table Generator** - Systematically test all combinations
2. **Logical Equivalence Checker** - Prove expressions are the same
3. **First Visualization** - Interactive truth tables in HTML/JS
4. **Mini-Project** - Boolean Expression Analyzer

These will use everything we've built so far and teach:

- Working with `itertools.product` (combinations)
- Dictionaries for variable assignments
- Classes and objects
- HTML/CSS/JavaScript basics
- Building complete applications

**Ready to continue with truth table generation?** This is where things get really powerful!
