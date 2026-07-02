---
name: test-validation-review
description: Review test quality - catches mock-only testing, deleted tests not replaced, presence-only assertions, untested intentional absence, and boundary value gaps. Use after completing work or as part of strict-review.
---

# Test Validation Review

Reviews test quality and coverage completeness in code changes. Catches issues where tests exist but don't actually verify correctness - the bugs that hurt most are where data flows through the pipeline but comes out wrong, and the tests don't catch it.

## When to Use

- After completing a feature that changes test files
- When refactoring moves behavior between components
- As part of strict-review orchestrator (dispatched automatically)

## How to Use

Dispatch as a subagent using the Task tool with the test-validation-reviewer.md template.

```
Task tool (general-purpose):
  description: "Test validation review: [description]"
  prompt: [contents of test-validation-reviewer.md with placeholders filled]
```

Fill in `{WORK_DIR}`, `{DESCRIPTION}`, and `{DECISION_LOG_PATH}`.

## Authority Levels

- **Flag for human:** Issues that need human judgment - mock-only testing, deleted tests, weak assertions
  - TV-1: Mock-Only Testing
  - TV-2: Deleted Tests Not Replaced
  - TV-3: Presence-Only Assertions

- **Report only:** Awareness items - intentional absence, boundary gaps
  - TV-4: Intentional Absence Untested
  - TV-5: Boundary Value Gaps

- **Flag for human (continued):**
  - TV-6: Lenient Assertions

No auto-fix patterns - test quality issues require human judgment to resolve correctly.

## Relationship to test-minimizer

This reviewer and test-minimizer-review are deliberate opposites and run in parallel. Where this reviewer catches under-testing (missing coverage, weak assertions), test-minimizer argues for removing tests that add no signal. When the two collide on the same test (this reviewer says "strengthen it", test-minimizer says "remove it"), the orchestrator surfaces the contradiction for the developer to resolve - strengthen the test or delete it, not both.

## Verdict Guidelines

- **Approve:** 0 flags, report items are informational only
- **Comment:** 1-2 flags worth discussing, not blocking
- **Request Changes:** Any of:
  - TV-1 (mock-only) on a function that handles validation, security, or data integrity
  - TV-2 (deleted tests) with no replacement for critical behavior
  - TV-3 (presence-only) on tests that are the only coverage for a code path
