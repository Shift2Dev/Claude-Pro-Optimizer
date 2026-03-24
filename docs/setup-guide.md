# Setup Guide

Step-by-step guide to install and configure Claude Pro Optimizer.

## 📋 Requirements

- Claude Desktop installed
- Claude Pro plan (recommended)
- Terminal (PowerShell on Windows, bash on Mac/Linux)

## 🚀 Installation

### Windows (PowerShell)

```powershell
# 1. Navigate to your .claude directory
cd ~\.claude

# 2. Create skills folder if it doesn't exist
New-Item -ItemType Directory -Force -Path skills

# 3. Copy configurations
# Download the repo and run:
Copy-Item -Path C:\path\to\repo\configs\global.md -Destination . -Force
Copy-Item -Path C:\path\to\repo\configs\.claudeignore -Destination . -Force
Copy-Item -Path C:\path\to\repo\configs\skills\smart-init -Destination skills\ -Recurse -Force

# 4. Verify
ls
```

### Mac/Linux (bash)

```bash
# 1. Navigate to your .claude directory
cd ~/.claude

# 2. Create skills folder if it doesn't exist
mkdir -p skills

# 3. Copy configurations
cp /path/to/repo/configs/global.md .
cp /path/to/repo/configs/.claudeignore .
cp -r /path/to/repo/configs/skills/smart-init skills/

# 4. Verify
ls -la
```

## ✅ Verification

After installing, your `~/.claude` directory should look like this:

```
.claude/
├── global.md
├── .claudeignore
└── skills/
    └── smart-init/
        └── SKILL.md
```

## 🎯 First Use

### 1. Open a project

Open any project in Claude Desktop.

### 2. Run smart-init

In the chat, type:

```
/init
```

### 3. View the result

Claude will analyze your project and automatically generate `.claude/CLAUDE.md`.

```powershell
# View the generated file
cat .claude/CLAUDE.md
```

### 4. Edit if needed

The file is ready to use, but you can customize it:

```powershell
code .claude/CLAUDE.md
```

## 🔧 Customization

### Modify global.md

Edit `~/.claude/global.md` to adjust:

```markdown
## Tools
- OS: [Your operating system]
- Terminal: [Your preferred terminal]
- Editor: [Your editor]

## Code Style
- [Your code preferences]
```

### Modify .claudeignore

Add patterns specific to your stack:

```
# Example: Ignore Next.js files
.next/
out/

# Example: Ignore Rust files
target/debug/
target/release/
```

### Create Your Own Skills

1. Create a folder at `~/.claude/skills/your-skill/`
2. Create `SKILL.md` with this structure:

```markdown
---
name: your-skill
description: What your skill does
---

# Your Skill

Your skill instructions...
```

See [Creating Skills](creating-skills.md) for more details.

## 🐛 Troubleshooting

### Skill not working

**Problem:** `/init` does nothing

**Solution:**
1. Verify the file is at `~/.claude/skills/smart-init/SKILL.md`
2. Restart Claude Desktop
3. Try again

### Configuration not applied

**Problem:** Claude isn't using my global.md

**Solution:**
1. Verify path: `~/.claude/global.md`
2. Check for valid Markdown formatting
3. Restart Claude Desktop

### Smart-init generates the file incorrectly

**Problem:** CLAUDE.md has placeholders

**Solution:**
1. Verify your project has `package.json` or `pyproject.toml`
2. Make sure there are source files in `src/` or similar
3. Report an issue with a project example

## 💡 Tips

### Token Efficiency

- Use `/btw` for quick questions that don't need context
- Use `/compact` when context fills up
- Periodically review `.claudeignore` and add new noise patterns

### Optimal Workflow

1. **New project:** run `/init` immediately
2. **Existing project:** add `.claudeignore` first
3. **Teams:** share your `.claude/` configs in the repo

### Best Practices

- Commit `.claude/CLAUDE.md` to your repo
- Do NOT commit `global.md` (it's personal)
- Adjust smart-init defaults to your preferred stack

## 📚 Next Steps

- Read [Token Optimization Theory](token-optimization-theory.md)
- See examples in [Workflow Demo](../examples/workflow-demo.md)
- Learn to create skills in [Creating Skills](creating-skills.md)

## 🆘 Support

Having issues? Open an [issue](../../issues) with:
- Your OS and Claude Desktop version
- Contents of the config that's failing
- Steps to reproduce the problem

---

**Happy optimizing! 🚀**
