---
description: Render-and-critique loop for an existing pandoc/beamer deck. Builds the PDF, renders every slide to PNG, runs mechanical (em-dash, balance, escaping), visual (overflow, floating labels, color drift), and editorial (acronyms, note length, narrative arc, superlatives) inspections, then iterates one finding at a time.
argument-hint: "[path/to/deck/dir]"
allowed-tools: Read, Edit, Bash, AskUserQuestion
---

# /slide-deck:review

Iterate on an existing pandoc/beamer deck. Load and follow the skill at:

```
${CLAUDE_PLUGIN_ROOT}/skills/review/SKILL.md
```

If `$ARGUMENTS` is non-empty, treat it as the deck directory path (cd there before Phase A). Otherwise assume cwd is the deck directory and let Phase A verify.

Plugin-relative paths the skill references:

- Rules checklist: `${CLAUDE_PLUGIN_ROOT}/rules/checklist.md`
