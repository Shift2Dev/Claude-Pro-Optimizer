# Workflow Demo

Real examples of how to use Claude Pro Optimizer in your day-to-day work.

## 🚀 Case 1: New Project Setup

### Situation

You're starting a new FastAPI project.

### Without Optimization (15 minutes)

```
1. "Hi Claude, I'm going to create a new project with FastAPI..."
2. Manually create structure
3. "Now I need pytest configuration..."
4. "What commands should I use for...?"
5. "How do I configure linting..."
6. [15 more setup messages]
```

**Time:** ~15 minutes
**Messages used:** ~20

### With Optimization (30 seconds)

```
# In your empty project
/init
```

**Output:**
```
✅ Generated .claude/CLAUDE.md

Detected:
- Stack: Python 3.13 + FastAPI
- Tests: pytest setup detected
- Commands: 5 scripts extracted from pyproject.toml
- Linting: ruff configured

Ready to use!
```

**Time:** 30 seconds
**Messages used:** 1

---

## 💻 Case 2: Debugging

### Situation

You have an error in your code.

### ❌ Inefficient (5 messages)

```
1. "Hi Claude, I have a problem in my code"
2. [Claude asks what code]
3. [You paste 500 lines]
4. [Claude asks what error]
5. "Oh right, it's a NameError on line 42"
```

**Tokens spent:** ~3,000

### ✅ Efficient (1 message)

```
Error in src/main.py line 42:
NameError: name 'process_data' is not defined

Context: inside function `run_pipeline()`
```

**Tokens spent:** ~100

**Savings:** 96%

---

## 🔧 Case 3: Refactoring

### Situation

You need to refactor legacy code.

### ❌ Inefficient

```
1. "Please review this entire file"
   [Paste 1000 lines]

2. "Now improve it"
   [Claude asks what to improve]

3. "Everything, make it better"
   [Generic result]
```

### ✅ Efficient

```
Refactor src/legacy.py:
- Extract validation into a separate function (lines 50-80)
- Convert DataProcessor class to pure functions
- Add type hints

Focus: maintainability, not performance
```

**Result:** Specific, useful refactor.

---

## 📝 Case 4: Documentation

### Situation

Documenting a complex function.

### ❌ Verbose

```
"Hi Claude, I need you to help me document this function.
It's very important that the documentation is clear and complete,
with all parameters explained, the return value, usage examples,
and also edge cases. The function is called calculate_metrics
and it's in the analytics.py file..."
```

**Tokens:** ~150

### ✅ Concise

```
Document `calculate_metrics()` in analytics.py:
- Docstring with params, return, examples
- Type hints
```

**Tokens:** ~30

**Savings:** 80%

---

## 🎯 Case 5: Code Review

### Situation

Reviewing a PR before merge.

### Without .claudeignore (BAD)

```
/view .  # Reads the ENTIRE project
```

**Files read:** 5,000+
**Context:** Immediately full
**Result:** "Context limit exceeded"

### With .claudeignore (GOOD)

```
/view src/
/view tests/
```

**Files read:** 50
**Context:** 30%
**Result:** Useful review

---

## 🔄 Case 6: Long Conversation

### Situation

A 30-message debugging session.

### Without Management

```
Message 25: "Context almost full"
Message 26: [Error, cannot process]
```

**Solution:** New conversation, lose context.

### With /compact

```
Message 10: /compact
# Continue...

Message 20: /compact
# Continue...

Message 30: Debugging completed with context intact
```

**Result:** Smooth conversation without limits.

---

## 💡 Case 7: Quick Questions

### Situation

A quick question with no context needed.

### ❌ Normal

```
"How do you write a loop in Python?"
# Uses the full context of the current conversation
```

### ✅ With /btw

```
/btw How do you write a loop in Python?
# Does NOT use context, fast response
```

**Savings:** Doesn't pollute the current conversation.

---

## 🎨 Case 8: Batch Operations

### Situation

Creating multiple related functions.

### ❌ Sequential (3 messages)

```
1. "Create sum function"
2. "Now subtract function"
3. "Now multiply function"
```

**Tokens:** ~300
**Time:** 3x latency

### ✅ Batched (1 message)

```
Create module math_ops.py:
- sum(a, b)
- subtract(a, b)
- multiply(a, b)

Type hints, docstrings, tests
```

**Tokens:** ~100
**Time:** 1x latency

---

## 📊 Typical Day Comparison

### Before Optimizing

```
09:00 - Project setup (20 messages)
10:30 - Debugging (15 messages)
12:00 - Code review (25 messages)
14:00 - Hit daily limit ❌
```

**Total:** 60 messages, limit reached

### After Optimizing

```
09:00 - /init (1 message)
09:30 - Efficient debugging (5 messages)
10:00 - Code review with .claudeignore (8 messages)
11:00 - New features (20 messages)
14:00 - Refactoring (15 messages)
16:00 - Documentation (10 messages)
17:00 - Still with headroom ✅
```

**Total:** ~60 messages, much more productive

---

## 🎯 Efficient Message Template

```markdown
[Specific action] [Precise location]:
- [Requirement 1]
- [Requirement 2]

[Important constraint if any]
```

**Examples:**

```
Fix bug src/api.py line 89:
- IndexError in loop
- Handle empty list

Maintain backward compatibility
```

```
Refactor components/Header.tsx:
- Extract logic to hooks
- Memoize expensive renders

Performance is critical
```

```
Test calculator.py:
- Edge cases (division by zero, overflow)
- Property-based testing

Pytest + hypothesis
```

---

## ✅ Daily Checklist

**At the start:**
- [ ] Check available limits
- [ ] Configure .claudeignore if new project
- [ ] Run /init if needed

**During work:**
- [ ] Specific, concise messages
- [ ] Use /btw for quick questions
- [ ] Batch related operations
- [ ] /compact every 10-15 messages

**At the end:**
- [ ] /compact if conversation was long
- [ ] Export important decisions
- [ ] Review daily usage

---

## 📚 Resources

- [Token Optimization Theory](../docs/token-optimization-theory.md)
- [Setup Guide](../docs/setup-guide.md)
- [Creating Skills](../docs/creating-skills.md)

---

**Pro tip:** Save this workflow demo as a reference. Efficiency is built with practice. 🚀
