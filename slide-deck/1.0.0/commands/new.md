---
description: Bootstrap a new LaTeX/beamer presentation via pandoc. Asks topic/audience/time/takeaway/arc, scaffolds Makefile + theme + plot helpers from templates, drafts slides section-by-section applying 12 baked-in rules (no overflow, no em-dashes, jargon glossary, brand-correct plots, speaker notes).
argument-hint: "[one-line topic]"
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

# /slide-deck:new

Bootstrap a brand-new pandoc/beamer presentation. Load and follow the skill at:

```
${CLAUDE_PLUGIN_ROOT}/skills/new/SKILL.md
```

If the user passed a one-line topic as an argument (`$ARGUMENTS`), use it as the seed for Phase A question 1; otherwise begin Phase A from scratch.

Plugin-relative paths the skill references:

- Templates: `${CLAUDE_PLUGIN_ROOT}/templates/`
- Rules checklist: `${CLAUDE_PLUGIN_ROOT}/rules/checklist.md`
