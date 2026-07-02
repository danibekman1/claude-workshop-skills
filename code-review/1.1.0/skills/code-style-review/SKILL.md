---
name: code-style-review
description: Review code style using 18 mechanical patterns plus 4 judgment-guided design principles (KISS/YAGNI/DRY/SOLID) - catches default values, nullability issues, misplaced fields, abstraction violations, and naming problems before PR review
---

# Code Style Review

Automated code review applying 18 mechanical patterns plus 4 judgment-guided design principles (KISS/YAGNI/DRY/SOLID) to code changes. Catches issues that generic reviewers miss: API default values, unjustified nullability, misplaced fields, class coherence problems, and stale comments. The design principles flag suspects for the developer to judge; they never auto-fix and never block the verdict.

It also carries a small set of language-agnostic principles extracted from python-dev (magic numbers, guard clauses, secret handling, and typing the public boundary; labelled `[LA: ...]` in the reviewer template), so those standards apply across every language rather than living only in the Python pack. Language-specific syntax and idiom stay in the per-language packs (`strict-review:language-pack-review`).

## When to Use

- After completing a logical unit of implementation work
- Before requesting human PR review
- As part of strict-review orchestrator (dispatched automatically)
- Dispatched in parallel with superpowers:code-reviewer (see ~/.claude/CLAUDE.md Code Review Workflow)

## How to Use

Dispatch as a subagent using the Task tool with the code-style-reviewer.md template.

```
Task tool (general-purpose):
  description: "Code style review: [description]"
  prompt: [contents of code-style-reviewer.md with placeholders filled]
```

Fill in `{WORK_DIR}` (git working directory), `{DESCRIPTION}`, and `{DECISION_LOG_PATH}`.

Reviews TWO layers of changes:
1. **Branch diff vs the base branch** (`git diff {BASE_BRANCH}...HEAD`) - all committed work on the branch, pushed or not
2. **Local worktree** (`git diff HEAD`) - staged + unstaged changes not yet committed

This gives complete coverage: the branch diff catches everything since diverging from the base branch (including unpushed commits), and the local diff catches work in progress.
Each finding is tagged `[BRANCH]`, `[LOCAL]`, or `[BOTH]` so you know what's committed vs uncommitted.

## Decision Log

When iterating on a PR, the reviewer will re-flag the same items every run unless you tell it what was already decided. The **decision log** solves this.

**Path convention:**
- With PR number: `tasks/strict-review-decisions-PR-{PR_NUMBER}.md`
- Pre-PR (branch only): `tasks/strict-review-decisions-{BRANCH_NAME}.md`

These are local files - never committed. Add `tasks/` to `.gitignore`.

**File format:**

```markdown
# Strict Review Decision Log - PR #13662

| ID | Pattern | Skill | File:Line | Finding Summary | Decision | Date |
|----|---------|-------|-----------|-----------------|----------|------|
| 1 | Pattern 9: Nullability | style | OrderServiceApi.kt:39 | "why nullable?" | Keep - business requirement | 2026-02-25 |
| 2 | Pattern 7: Field Placement | style | Parameters.kt:22 | "belongs elsewhere?" | Moved to TestHeader - done in abc123 | 2026-02-25 |
```

**Caller workflow after each review:**

1. Reviewer returns output with a "Pending Decisions" table
2. Present flagged items to the human for decision
3. Copy the pending rows into the decision log, replacing `PENDING` with the actual decision
4. On the next review run, the reviewer reads the log and skips decided items

**Re-flagging:** If code near a decided item changes significantly between runs, the reviewer will re-flag it with a warning. This prevents stale decisions from hiding new issues.

**Migration:** Existing `tasks/gilad-decisions-*` files continue to work. Rows without a Skill column are treated as `style`.

## Authority Levels

- **Auto-fix:** Clear violations - apply fix directly, report what changed
  - Default values in API/interface params
  - Missing trailing commas
  - Unnecessary `this.` prefix
  - Non-exhaustive `when` with `else`
  - Non-idiomatic Kotlin syntax
  - Missing `.use` for Closeable resources

- **Flag for human:** Subjective design calls - present as question, wait for decision
  - Field placement ("does this belong here?")
  - Abstraction layer mixing
  - Nullability without business justification
  - Related fields that should be grouped
  - Eager vs lazy evaluation
  - Code placement / responsibility
  - Unnecessary wrappers
  - Config vs parameter ambiguity

- **Report only:** Awareness items - note in output, no action
  - Missing E2E tests
  - Missing validation / invariant checks
  - Names that will age poorly
  - Sealed type exhaustiveness

- **Judgment-guided (design principles):** Suspects for the developer to decide - never auto-fix, never block the verdict
  - KISS: a convoluted solution to a simple problem
  - YAGNI: speculative generality with no current caller
  - DRY: non-trivial logic duplicated three or more times
  - SOLID: mixed responsibilities (SRP) or a type-switch that should be polymorphism (OCP)
