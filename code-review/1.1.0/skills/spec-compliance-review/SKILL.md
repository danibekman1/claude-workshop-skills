---
name: spec-compliance-review
description: Review code changes against a Confluence design doc for completeness gaps, faithfulness issues, scope creep, and ambiguous design areas. Optional sub-skill of strict-review, activated with --spec flag.
---

# Spec Compliance Review

Reviews branch changes against a Confluence design document. Catches requirements that weren't implemented, approaches that deviate from the design, unspecified additions, and areas where the design is ambiguous.

## When to Use

- As part of strict-review orchestrator when `--spec <confluence-url>` is provided
- Only activated when a spec URL is available (from `--spec` arg or decision log header)
- Skipped entirely when no spec URL is configured

## How to Use

Dispatch as a subagent using the Task tool with the spec-compliance-reviewer.md template.

```
Task tool (general-purpose):
  description: "Spec compliance review: [description]"
  prompt: [contents of spec-compliance-reviewer.md with placeholders filled]
```

Fill in `{WORK_DIR}`, `{DESCRIPTION}`, `{DECISION_LOG_PATH}`, `{SPEC_CONTENT}`, and optionally `{DIFF_CONTENT}` and `{DECIDED_ITEMS}`.

## Review Tiers

**Design-level (reviewed for compliance):**
- Architecture and component structure
- Data flow and public interfaces
- Key invariants and constraints
- Error handling strategy

**Implementation details (within implementer's discretion - NOT reviewed):**
- Variable names, internal helpers
- Lock choice, internal method structure
- Import organization, formatting

## The 4 Patterns

All findings are **flagged for human decision**.

| ID | Pattern | Description |
|----|---------|-------------|
| SC-1 | Missing Requirement | Design specifies something, no code implements it |
| SC-2 | Wrong Approach | Code contradicts the design's specified approach |
| SC-3 | Unspecified Addition | Code adds something the design doesn't mention |
| SC-4 | Ambiguous Design | Design is unclear on a design-level concern, needs clarification |

## Decision Log

Uses the same unified decision log as other sub-skills. Findings use `Skill = spec-compliance`.

**Matching rule:** A finding matches a decided item when the **Pattern** and **Finding Summary** match (spec findings often lack a file reference).

**Re-flagging:** If the spec URL changes (user passes a different `--spec`), all previous spec-compliance decisions are invalidated and re-reviewed.

## Verdict Guidelines

- **Approve:** 0 findings, or only SC-3 (minor unspecified additions)
- **Comment:** SC-4 (ambiguous design) items that need discussion
- **Request Changes:** Any SC-1 (missing requirement) or SC-2 (wrong approach)
