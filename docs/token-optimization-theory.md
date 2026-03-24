# Token Optimization Theory

Principles and techniques to maximize efficiency in Claude Pro.

## 🎯 Why It Matters

### Claude Pro Limits

Claude Pro has daily usage limits:
- **Messages per day:** Limited
- **Tokens per message:** Counted
- **Cumulative context:** Accumulates in long conversations

**Every token counts toward these limits.**

### The Inefficient Prompt Problem

```markdown
❌ BAD (verbose, 150 tokens):
"Hi, I would really appreciate it if you could please help me understand
in great detail and completeness, with all possible details, exactly
what this code does and how each line works step by step,
because I need to understand it well for my project..."

✅ GOOD (concise, 25 tokens):
"Explain this code line by line"
```

**Savings:** 83% fewer tokens, same result.

## 🧠 Optimization Principles

### 1. Eliminate Redundancy

**Before:**
```
Could you please help me to...
```

**After:**
```
Help me...
```

**Rule:** Get to the point. Claude understands implicit context.

### 2. Be Specific, Not Verbose

**Before:**
```
Create a function that takes two integer parameters and
returns the sum of both numbers
```

**After:**
```
Function: sum of two integers
```

**Rule:** Specificity ≠ Verbosity

### 3. Use Built-in Commands

**Before:**
```
Please read this file and tell me what it contains
```

**After:**
```
/view file.py
```

**Rule:** Use native tools when they exist.

### 4. Batch Operations

**Before (3 messages):**
```
1. "Create sum function"
2. "Now subtract function"
3. "Now multiply function"
```

**After (1 message):**
```
Create functions: sum, subtract, multiply
```

**Rule:** Group related requests.

### 5. Context Management

**Before:**
```
[Full 50-message history loaded]
```

**After:**
```
/compact  # Compacts context automatically
```

**Rule:** Use `/compact` when context is >50% full.

## 🛠️ Advanced Techniques

### A. Global Configuration

`~/.claude/global.md`:

```markdown
## Token Efficiency
- Use `/btw` for questions that don't need context
- Read files only when explicitly needed
- Batch related edits in single operation
```

**Effect:** Claude applies these rules automatically.

### B. Custom Ignorefile

Optimized `.claudeignore`:

```
# Block noise
node_modules/
*.log
__pycache__/

# Allow when needed
# dist/  ← NOT blocked by default
```

**Effect:** Claude doesn't read 10,000 files from node_modules.

### C. Smart-Init

Auto-generate configs:

```
/init
```

**Effect:** Perfect setup in seconds, no manual config.

### D. Explicit File Reading

**Before:**
```
"Read all the project files"
```

**After:**
```
/view src/main.py
/view tests/test_main.py
```

**Rule:** Specify what to read, not "everything".

## 📊 Strategies by Use Case

### Debugging

```markdown
❌ "The code doesn't work, help me"
✅ "Error on line 42: NameError 'x' not defined"
```

### Code Review

```markdown
❌ "Review this entire file"
✅ "Review function `process_data()` (lines 30-45)"
```

### Refactoring

```markdown
❌ "Improve the code"
✅ "Refactor: extract validation logic into a separate function"
```

### Documentation

```markdown
❌ "Document this entire project"
✅ "Document function `calculate_metrics()`"
```

## 🎯 Optimal Workflow

### Initial Setup (once)

1. Install configs from this repo
2. Configure `.claudeignore` for your stack
3. Run `/init` in projects

### Daily Use

```
1. Specific, concise message
2. Use /btw for quick questions
3. Batch related operations
4. /compact when context is high
5. Check limits in settings
```

### Long Conversations

```
- Every 10-15 messages → /compact
- If hitting limits → New conversation
- Export important info before compacting
```

## 📈 Success Metrics

### Before Optimizing

- Prompts: ~200 tokens average
- Useful messages/day: ~30
- Hit limit: frequently

### After Optimizing

- Prompts: ~50 tokens average
- Useful messages/day: ~80
- Hit limit: rarely

**Result:** 2.5x more conversations with the same plan.

## 🔍 Anti-Patterns

### ❌ Over-optimization

```
"fnc sum(a,b)ret a+b"  # Unreadable
```

**Balance:** Clarity > extreme token savings

### ❌ Omitting Critical Context

```
"Fix the bug"  # Which bug?
```

**Balance:** Specific ≠ Minimal

### ❌ Overusing /compact

```
/compact after every message
```

**Balance:** Compact every 10-15 messages

## 💡 Advanced Tips

### 1. Use Markdown Efficiently

```markdown
Before: "The function must do X, Y, and Z"

After:
Function must:
- X
- Y
- Z
```

### 2. Partial Code Snippets

```markdown
Before: [Paste 500 lines of code]

After: "See src/main.py lines 100-120"
```

### 3. Mental Aliases

```markdown
Before: "The data processing system"

After (first mention):
"The data processing system (DPS)"

After (rest):
"DPS should..."
```

## 📚 References

- [Setup Guide](setup-guide.md) - How to install
- [Creating Skills](creating-skills.md) - Advanced automation
- [Workflow Demo](../examples/workflow-demo.md) - Real examples

## 🎓 Exercise

**Optimize this prompt:**

```
"Hi Claude, hope you're doing well. I'd really appreciate it if you could
please help me with something. I have a Python project and I need you to
help me create a function that takes two integer parameters and returns
the sum of those two numbers. Could you please help me with that? Thanks!"
```

**Solution:**

```
"Python function: sum two integers"
```

**Reduction:** ~90% fewer tokens, clarity maintained.

---

**Remember:** Efficiency ≠ Sacrificing clarity. The goal is clear communication with minimum waste. 🎯
