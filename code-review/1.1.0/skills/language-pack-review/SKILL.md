---
name: language-pack-review
description: Language-specific syntax and idiom review, one pack per language, dispatched only when matching files are in the diff. Ships a Python pack (mutable default arguments, eval/exec, exception chaining, PEP-8, frozen dataclasses, docstrings, typing) and a contrived empty TypeScript skeleton. Use as part of strict-review.
---

# Language Pack Review

The language-specific half of strict-review. Code-style holds the language-agnostic patterns (naming, error handling, magic numbers, guard clauses, secret-handling); a language pack holds the syntax and idiom rules that only make sense for one language. A pack runs only when the diff touches files of its language, so a Kotlin-only change never gets Python findings and a Python change gets the Python pack.

One shared reviewer template serves every pack. The per-language rules live in a manifest under `packs/`, and a single registry table decides which pack runs on which files. Adding a language is a one-file-plus-one-row change, not a new skill.

## When to Use

- After completing a feature that touches code in a language with a pack
- As part of the strict-review orchestrator, which dispatches a pack automatically when the diff contains matching files
- Directly, to review one language's syntax and idioms in isolation

## How to Use

Dispatch as a subagent using the Task tool with the `language-pack-reviewer.md` template, once per pack whose files are in the diff.

```
Task tool (general-purpose):
  description: "Language pack review (python): [description]"
  prompt: [contents of language-pack-reviewer.md with placeholders filled]
```

Fill in `{WORK_DIR}`, `{DESCRIPTION}`, `{DECISION_LOG_PATH}`, `{PACK_NAME}`, `{LANGUAGE}`, and `{MANIFEST_PATH}` (the absolute path to the pack's manifest, for example `${CLAUDE_PLUGIN_ROOT}/skills/language-pack-review/packs/python.md`; a relative path will not resolve after the subagent runs `cd {WORK_DIR}`). The orchestrator also passes `{DIFF_CONTENT}` and `{DECIDED_ITEMS}`; when you invoke the reviewer directly without them, it gathers the diff and reads the decision log itself.

## Packs

This table is the single source of truth for which files trigger which pack. The orchestrator reads it to decide dispatch; a manifest never repeats its own globs.

| Pack | Language | Globs | Manifest | Status |
|------|----------|-------|----------|--------|
| python | Python | `*.py` | `packs/python.md` | active |
| ts | TypeScript | `*.ts`, `*.tsx` | `packs/ts.md` | skeleton |

A pack with status `active` ships real rules. A pack with status `skeleton` declares no rules yet; it dispatches on its globs and returns a single "skeleton pack, no rules defined yet" note, so the add-a-pack mechanism stays testable. At runtime the reviewer decides skeleton-versus-active by reading the manifest and finding no rules; the `Status` column is descriptive documentation of that state, not a separate switch, so keep it in sync with the manifest.

## Authority Levels

Pack findings carry the same authority code-style uses for the same class of issue. There is no auto-fix; auto-fix stays a code-style-only authority.

- **Flag:** genuine safety or correctness issues whose silent failure is expensive. In the Python pack: `[PY: MUTABLE-DEFAULT]`, `[PY: EVAL-EXEC]`, `[PY: RAISE-FROM]`.
- **Report:** idiom and style. In the Python pack: `[PY: IMPORTS-TOP]`, `[PY: VALUE-DATACLASS]`, `[PY: DOCSTRING]`, `[PY: TYPING]`.

## Adding a Language Pack

1. Copy `packs/ts.md` to `packs/<lang>.md` and write the rules, following the pattern shape in `packs/python.md` (a `[<LANG>: NAME]` prefix, a trigger, detection markers, a "do not flag" guard, a terse voice line, and a severity per rule).
2. Add one row to the Packs table above with the language's globs and the manifest path. Set status to `active`.
3. Done. The orchestrator discovers the row, gates on the globs, and dispatches the shared `language-pack-reviewer.md` template against the new manifest. No orchestrator edit is needed.

To stub a language before its rules exist, add the row with status `skeleton` and an empty manifest (see `packs/ts.md`). The pack then dispatches as a no-op until you fill it in.

## Verdict Guidelines

- **Approve:** no findings, or a skeleton pack with no rules.
- **Comment:** one or more report-level findings and no standing flag finding.
- **Request Changes:** at least one flag-level finding stands. This matches code-style, so the orchestrator's most-severe-sub-verdict rule needs no special case.
