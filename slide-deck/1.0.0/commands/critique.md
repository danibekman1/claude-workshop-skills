---
description: Rubric-based quality score for an existing pandoc/beamer deck. Evaluates against a 6-dimension rubric (Structure, Story arc, Density, Audience fit, Stickiness, Craft) with 32 sub-checks and 64 max points. Produces an inline summary with letter grade plus a written critique-report.md, then offers a one-at-a-time fix walkthrough.
argument-hint: "[path/to/deck/dir]"
allowed-tools: Read, Edit, Bash, AskUserQuestion
---

# /slide-deck:critique

Score an existing pandoc/beamer deck against a presentation-quality rubric. Load and follow the skill at:

```
${CLAUDE_PLUGIN_ROOT}/skills/critique/SKILL.md
```

If `$ARGUMENTS` is non-empty, treat it as the deck directory path (cd there before Phase A). Otherwise assume cwd is the deck directory and let Phase A verify.

Plugin-relative paths the skill references:

- Rubric: `${CLAUDE_PLUGIN_ROOT}/rules/rubric.md`
- Rules checklist (for Dimension 6 Craft): `${CLAUDE_PLUGIN_ROOT}/rules/checklist.md`
