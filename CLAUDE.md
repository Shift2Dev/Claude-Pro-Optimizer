# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About

Claude Pro Optimizer is a configuration toolkit for Claude Desktop/Pro users. It provides a global config, a `.claudeignore` template, and a `smart-init` skill to auto-generate optimized `CLAUDE.md` files for any project.

## Stack

- **Language**: Python 3.8+ (optional tools only)
- **Dependencies**: `matplotlib>=3.7.0`, `numpy>=1.24.0` (only needed for chart generation)
- **Platform**: Claude Desktop / Claude.ai

## Running the Tools

```bash
# Terminal visual comparison (no dependencies needed)
python tools/visual_comparison.py

# Generate PNG charts (requires matplotlib)
pip install matplotlib numpy
python tools/generate_charts.py
```

Charts are saved to the working directory: `comparison_chart.png`, `daily_impact.png`, `monthly_projection.png`.

## Project Structure

- `configs/global.md` - Global Claude preferences (copy to `~/.claude/global.md`)
- `configs/.claudeignore` - Ignore patterns (copy to `~/.claude/.claudeignore`)
- `configs/skills/smart-init/SKILL.md` - The smart-init skill definition (copy to `~/.claude/skills/smart-init/`)
- `tools/` - Standalone Python scripts for visualization; no shared modules between them
- `docs/` - Guides for setup, token optimization theory, and skill creation
- `examples/` - Workflow demos

## Architecture

This is a configuration distribution project, not a runnable application. The core deliverable is the `configs/` directory — files users copy into their `~/.claude/` directory.

The `smart-init` skill (`configs/skills/smart-init/SKILL.md`) is invoked via `/init` in Claude Desktop. It analyzes a target project's `package.json`/`pyproject.toml`/etc. and generates a complete `.claude/CLAUDE.md` with zero placeholders. The skill template uses smart defaults per stack (Python, JS/TS, Java) when auto-detection is insufficient.

The `configs/.claudeignore` intentionally does NOT block `dist/`, `build/`, or `target/` — these may be needed for analysis. Users should add those manually if desired.

## Code Conventions

- Pure functions, no side effects, explicit parameters, strict typing
- Commits: Conventional Commits (`feat/fix/docs/...`)
- Communication: Spanish for messages, English for code/comments/commits
