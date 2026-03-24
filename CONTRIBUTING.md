# Contributing to Claude Pro Optimizer

Thank you for your interest in contributing! 🎉

## 🤝 How to Contribute

### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/your-username/claude-pro-optimizer.git
cd claude-pro-optimizer
```

### 2. Create a Branch

```bash
git checkout -b feat/amazing-feature
# or
git checkout -b fix/bug-description
# or
git checkout -b docs/improvement
```

### 3. Make Changes

- Keep the existing style
- Configs go in `configs/`
- Docs go in `docs/`
- Examples go in `examples/`

### 4. Commit

We use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git commit -m "feat: add new optimization skill"
git commit -m "fix: correct smart-init detection"
git commit -m "docs: improve setup guide"
```

**Prefixes:**
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `refactor:` refactoring without functional changes
- `chore:` maintenance tasks

### 5. Push and PR

```bash
git push origin feat/amazing-feature
```

Then open a Pull Request on GitHub.

## 💡 Contribution Ideas

### Useful Skills

Got a custom skill that others would find useful? Share it:

```
configs/skills/your-skill/
└── SKILL.md
```

### .claudeignore Improvements

Does your stack need specific patterns? Add them with comments:

```gitignore
# Framework X specific
.framework-cache/
*.framework-temp
```

### Real-World Examples

Used the optimizer in an interesting way? Document it:

```
examples/use-case-X.md
```

### New Optimizations

Found a new efficiency technique? Add it to:

```
docs/token-optimization-theory.md
```

## 📋 Guidelines

### Configs

- Comment non-obvious decisions
- Keep consistent formatting
- Test before committing

### Documentation

- English for all docs
- Concrete examples over abstract theory
- Markdown lint-free

### Skills

- Short, descriptive name
- Clear description of purpose
- Smart defaults, no placeholders
- Specific instructions

## 🐛 Reporting Bugs

Use [GitHub Issues](../../issues) with:

**Template:**

```markdown
## Description
[What isn't working]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Error appears]

## Expected Behavior
[What should happen]

## Environment
- OS: [Windows 11 / macOS 14 / Ubuntu 22.04]
- Claude Desktop: [version]
- Config: [which configs you have installed]
```

## 💭 Suggesting Features

**Template:**

```markdown
## Problem
[What problem this solves]

## Proposed Solution
[Your idea]

## Alternatives
[Other options considered]

## Benefit
[Why it's valuable]
```

## ✅ PR Checklist

Before opening a PR, verify:

- [ ] Code/configs work locally
- [ ] Docs updated if necessary
- [ ] Commits follow Conventional Commits
- [ ] Branch is up to date with main
- [ ] Clear description of the change

## 🎯 Code of Conduct

- Be respectful and constructive
- Accept feedback openly
- Focus on the code/configs, not the person
- Help create a learning environment
- Assume good intent from other contributors

## 🌟 Recognition

Contributors will be mentioned in:
- README.md (Contributors section)
- CHANGELOG.md
- Commit history

## 🆘 Need Help?

- Ask in [Discussions](../../discussions)
- Open an [Issue](../../issues) with your question
- Tag with `question` label

## 📚 Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Claude Documentation](https://docs.anthropic.com/claude/docs)

---

**Every contribution, big or small, is valuable!** 🚀

Questions? Open an issue. Ideas? Start a discussion. Code ready? Open a PR.

**Thanks for helping improve Claude Pro Optimizer.** 🎉
