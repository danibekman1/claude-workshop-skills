---
name: refactoring-safety-review
description: Review refactoring completeness - catches missed caller updates, behavior changes during moves, new code paths missing from callers, deleted unreplaced code, and interface contract mismatches. Use after refactoring or as part of strict-review.
---

# Refactoring Safety Review

Reviews refactoring completeness and behavior preservation. Catches the class of bugs where code moves or changes but not all consumers are updated - the kind of issue that compiles fine but silently breaks at runtime.

## When to Use

- After any refactoring that moves, renames, or restructures code
- When changing function signatures, return types, or behavioral contracts
- As part of strict-review orchestrator (dispatched automatically)

## How to Use

Dispatch as a subagent using the Task tool with the refactoring-safety-reviewer.md template.

```
Task tool (general-purpose):
  description: "Refactoring safety review: [description]"
  prompt: [contents of refactoring-safety-reviewer.md with placeholders filled]
```

Fill in `{WORK_DIR}`, `{DESCRIPTION}`, and `{DECISION_LOG_PATH}`.

## Authority Levels

- **Flag for human:** Issues that likely indicate a bug or missed update
  - RS-1: Missed Caller Update
  - RS-2: Moved Behavior Changed
  - RS-3: New Code Path Missing From Existing Callers

- **Report only:** Awareness items that may or may not be issues
  - RS-4: Deleted Code Not Replaced
  - RS-5: Interface Contract Change Without Adapter Update

No auto-fix patterns - refactoring safety issues require understanding intent.

## Verdict Guidelines

- **Approve:** 0 flags, report items are informational
- **Comment:** 1-2 flags worth discussing, possible false positives
- **Request Changes:** Any of:
  - RS-1 (missed caller) - almost always a real bug
  - RS-2 (moved behavior changed) on a function that handles validation or data transformation
  - RS-3 (missing caller) for a new safety/validation function
