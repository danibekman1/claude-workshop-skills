---
name: review-walkthrough
description: Walk through strict-review findings one at a time with code context, recommendations, and user decisions via AskUserQuestion. Invoked by the main agent after strict-review returns.
---

# Review Walkthrough

Interactive walkthrough of strict-review findings. Presents each finding one at a time with code snippets, explanations, and type-aware decision options.

## When to Use

- Automatically after strict-review returns its unified report
- Referenced from CLAUDE.md's "After both return" instructions
- Runs in the main agent context (needs AskUserQuestion access)

## How It Works

The main agent invokes this skill after receiving the strict-review report. The skill instructs the agent to iterate through ALL findings (auto-fixes, flagged, report items) one at a time, showing code context and collecting decisions.

## Input

The strict-review report is already in conversation context. No parameters needed.

## Walkthrough Order

1. Auto-fixes (confirm/revert)
2. Flagged-for-decision (fix/skip/modify)
3. Report items (noted/fix anyway)
4. Cross-component insights (pursue/skip)

## Decision Options by Type

| Finding Type | Options |
|-------------|---------|
| Auto-fix | Confirm / Revert / Modify |
| Flagged | Fix (recommended) / Skip / Modify |
| Report | Noted / Want to fix anyway |
| SC-1 (missing) | Implement now / Defer / Already covered |
| SC-2 (wrong approach) | Fix to match design / Update design / Discuss |
| SC-3 (unspecified) | Keep / Remove / Discuss |
| SC-4 (ambiguous) | Interpret as... / Clarify with author / Flag on design doc |
| Cross-component | Pursue / Skip |
