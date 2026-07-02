---
name: strict-review
description: Comprehensive code review orchestrator - dispatches code-style, test validation, test minimization, refactoring safety, optionally spec compliance, per-language packs (Python in v0.1), and skill review (when the diff touches skill files) in parallel, then performs cross-component analysis. Use after completing a logical unit of work, before requesting human PR review.
---

# Strict Review

Extensible code review orchestrator that dispatches specialized sub-skills in parallel and produces a unified report. Catches style issues, test quality gaps, redundant tests, refactoring safety problems, language-specific syntax and idiom issues (via language packs gated on the diff), skill-definition quality (via skill-review gated on the diff), and optionally checks implementation against a Confluence design doc.

## When to Use

- After completing a logical unit of work (feature, bugfix, refactor)
- Before requesting human PR review
- Dispatched in parallel with superpowers:code-reviewer (see ~/.claude/CLAUDE.md)

## How to Use

Dispatch as a subagent using the Task tool with the strict-review-orchestrator.md template.

```
Task tool (general-purpose):
  description: "Strict review: [description]"
  prompt: [contents of strict-review-orchestrator.md with placeholders filled]
```

Fill in `{WORK_DIR}`, `{DESCRIPTION}`, and `{DECISION_LOG_PATH}`.

## Sub-Skills

| Skill | Path | Authority Levels | Focus |
|-------|------|-----------------|-------|
| code-style-review | skills/code-style-review/SKILL.md | auto-fix, flag, report, judgment | API design, Kotlin idioms, naming (18 patterns) + design principles (KISS/YAGNI/DRY/SOLID) |
| test-validation-review | skills/test-validation-review/SKILL.md | flag, report | Test quality, assertion depth, coverage gaps (6 patterns) |
| test-minimizer-review | skills/test-minimizer-review/SKILL.md | suggest (Comment max) | Devil's-advocate counterweight: redundant, framework-only, tautological, brittle, and trivial-accessor tests (5 patterns) |
| refactoring-safety-review | skills/refactoring-safety-review/SKILL.md | flag, report | Caller completeness, behavior preservation (5 patterns) |
| spec-compliance-review | skills/spec-compliance-review/SKILL.md | flag | Design compliance: completeness, faithfulness, scope, ambiguity (4 patterns) |
| language-pack-review | skills/language-pack-review/SKILL.md | flag, report | Language-specific syntax and idiom, one pack per language, dispatched only when matching files are in the diff (Python pack: 7 patterns; TS skeleton) |
| skill-review | skills/skill-review/SKILL.md | flag, report | Skill-definition quality: frontmatter validity, file references, description and triggering, content voice, progressive disclosure; dispatched only when the diff touches skill files (5 patterns) |
| review-walkthrough | skills/review-walkthrough/SKILL.md | n/a | Interactive one-by-one walkthrough of all findings with code context |

code-style-review, test-validation-review, test-minimizer-review, refactoring-safety-review, spec-compliance-review, language-pack-review, and skill-review are independently invocable - users can run them directly for focused reviews. review-walkthrough is invoked by the main agent after the orchestrator returns (not independently).

## Orchestrator Responsibilities

0. **Fetch spec (optional)** - If `--spec` URL provided, fetches Confluence design doc
1. **Gather diff** - Runs git diff once, passes to all sub-skills
2. **Read decision log** - Single log, passes relevant items to each sub-skill
3. **Dispatch sub-skills in parallel** - Four base subagents, plus spec compliance if a spec is provided, plus one per language pack whose files are in the diff, plus skill review if the diff touches skill files, via Task tool
4. **Cross-component pass** - Correlates findings across skills
5. **Consolidate** - Unified report with single pending-decisions table
6. **Walkthrough** - After the orchestrator returns, the main agent invokes `review-walkthrough` to present findings one at a time with code context and collect user decisions

## Decision Log

Single unified log with skill column:

**Path convention:**
- With PR: `tasks/strict-review-decisions-PR-{PR_NUMBER}.md`
- Pre-PR: `tasks/strict-review-decisions-{BRANCH}.md`

**Migration:** Existing `tasks/gilad-decisions-*` files continue to work. Rows without a Skill column are treated as `style` (code-style-review).

## Adding New Sub-Skills

To add a new review sub-skill:
1. Create a directory under `skills/{skill-name}/`
2. Add `SKILL.md` (skill definition) and `{skill-name}-reviewer.md` (subagent template)
3. Add the skill to the registry table in this file
4. Update `strict-review-orchestrator.md` to dispatch the new skill

To add a new **language** (not a new sub-skill), do not follow the steps above. Add a pack to language-pack-review instead: drop a manifest under `skills/language-pack-review/packs/` and add one row to that skill's Packs table. The orchestrator dispatches it automatically; no orchestrator edit is needed. See `skills/language-pack-review/SKILL.md`.
