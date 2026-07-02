---
name: test-minimizer-review
description: Devil's-advocate test review - argues for removing tests that add no signal: redundant coverage, tests of framework or language behavior, tautological mock-echo tests, tests pinned to incidental details, and trivial accessor tests. Suggestion-only, never blocks. Use as part of strict-review.
---

# Test Minimizer Review

The counterweight to test-validation. Where test-validation catches under-testing, this reviewer catches over-testing: tests that add no signal and cost build time, maintenance, and refactor friction. It argues for removing them. It only ever suggests - it never deletes a test, and its findings never block a PR.

## When to Use

- After completing a feature that adds or changes tests
- When a diff adds a large batch of tests and you want to find the ones that do not earn their place
- As part of strict-review orchestrator (dispatched automatically, in parallel with test-validation)

## How to Use

Dispatch as a subagent using the Task tool with the test-minimizer-reviewer.md template.

```
Task tool (general-purpose):
  description: "Test minimizer review: [description]"
  prompt: [contents of test-minimizer-reviewer.md with placeholders filled]
```

Fill in `{WORK_DIR}`, `{DESCRIPTION}`, and `{DECISION_LOG_PATH}`.

## Authority Levels

- **Suggest (Comment at most):** every pattern. A removal candidate is a proposal about test value; the developer decides whether to act. Nothing here blocks a PR.
  - TM: DUPLICATE - Redundant coverage
  - TM: FRAMEWORK - Testing the framework or language
  - TM: TAUTOLOGY - Tautological / mock-echo
  - TM: INCIDENTAL - Pinned to incidental implementation details
  - TM: ACCESSOR - Trivial accessor tests

No auto-fix and no auto-delete - removing a test is always the developer's call.

## Guards

Never suggest removing the only test of a critical / security / data-integrity path, a regression test tied to a specific bug fix, or the only test of a public-API contract. These guards run before the patterns, so a protected test is never a candidate.

## Relationship to test-validation

This reviewer and test-validation-review are deliberate opposites and run in parallel. When they reach opposite conclusions on the same test (test-validation says "strengthen it", test-minimizer says "remove it"), the orchestrator surfaces the contradiction for the developer to resolve - strengthen the test or delete it, not both.

## Verdict Guidelines

- **Approve:** no removal candidates.
- **Comment:** one or more removal candidates worth discussing.
- **Never Request Changes.** A removal candidate is a suggestion about test value, never a blocker, so a test-minimizer finding never gates the orchestrator's overall verdict.
