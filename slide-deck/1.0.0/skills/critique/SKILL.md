---
name: slide-deck:critique
description: Use when the user wants a quality score for an existing pandoc/beamer deck - evaluates against a 6-dimension rubric (Structure, Story arc, Density, Audience fit, Stickiness, Craft) and produces an inline summary + a written `critique-report.md`. Trigger phrases: "critique my deck", "score my presentation", "/slide-deck:critique", "how good is this deck", "rate my slides".
---

# /slide-deck:critique

Rubric-based quality evaluation for an existing pandoc/beamer deck. Loads `${CLAUDE_PLUGIN_ROOT}/rules/rubric.md` and `${CLAUDE_PLUGIN_ROOT}/rules/checklist.md`, runs all 6 dimensions, prints a scored summary, and writes a full report to `critique-report.md`.

## When to use

- User says "critique the deck", "score this presentation", "/slide-deck:critique", "how good is this?".
- If cwd doesn't look like a deck dir (no `slides.md` or `Makefile`), ask where the deck is - don't guess.
- If the build is broken (`make` fails), redirect the user to `/slide-deck:review` first - scoring a broken build is meaningless.
- Distinct from `/slide-deck:review`, which catches *craft mistakes*. `:critique` evaluates *presentation quality*. The two skills are complementary; run `:review` to fix obvious issues first, then `:critique` to measure overall quality.

## Process

### Phase A - sanity

1. Verify cwd has `slides.md`, `Makefile`, and `theme-overrides.tex`. If any is missing, ask the user where the deck is - don't guess.
2. Run `make` and capture stderr. If pandoc/xelatex errors, stop and tell the user to run `/slide-deck:review` first. Also stop if `slides.pdf` is missing after `make`, or if `pdfinfo slides.pdf` reports 0 pages - this is the silent-xelatex-bail failure mode and a critique on a 0-page PDF is meaningless.
3. Render every slide to PNG: `mkdir -p /tmp/sd-critique-$$ && pdftoppm -r 200 -png slides.pdf /tmp/sd-critique-$$/p`. Same DPI floor as `:review`.

### Phase B - metadata

1. Parse the YAML header of `slides.md`. Extract `audience`, `time_budget`, `takeaway`.
2. If any of the three is missing or empty, prompt the user via `AskUserQuestion`:
   - **Audience:** "R&D engineers", "Squad leads / mixed technical", "PMs / customers / exec", or "Other".
   - **Time budget:** "5 / 10 / 20 / 30 minutes" or "Other (custom)".
   - **Takeaway:** open-ended one-sentence.
3. After collecting answers, ask the user if they want the values written back into the YAML so the next run is silent. Default yes. If yes, edit `slides.md`'s YAML block to add the three fields.

### Phase C - scoring

Load `${CLAUDE_PLUGIN_ROOT}/rules/rubric.md` and `${CLAUDE_PLUGIN_ROOT}/rules/checklist.md`.

For each dimension in order (1 through 6), run every sub-check. Record:
- Score (0/1/2).
- Evidence (slide number + offending text or PNG observation).
- Fix suggestion.

For Dimension 6 (Craft), iterate the 13 rules in `${CLAUDE_PLUGIN_ROOT}/rules/checklist.md`. For each rule, run its `detect:` block verbatim (the same bash greps for mechanical rules; the same per-PNG visual inspection for visual rules; the same regex scans for editorial rules). Map each rule's finding count to a 0/1/2 score per the rubric's Dimension 6 mapping (rule passes → 2; rule has 1 finding → 1; rule has ≥ 2 findings → 0). This re-uses `checklist.md` as the source of truth without invoking `/slide-deck:review` as a sub-skill.

For sub-checks that xref a craft rule (currently only 4.2 acronyms): run the same detect block as the referenced rule and score it under the higher dimension. The Craft sub-check still runs and scores, but the report annotates the finding as "scored under Audience fit" to avoid double-counting in the user's mental model.

Compute per-dimension subtotals and the overall score (sum / 64 → percentage → letter grade A ≥ 90%, B ≥ 75%, C ≥ 60%, D < 60%).

### Phase D - report and iterate

#### Inline summary (print to chat)

Format:

```
Critique: slides.md (N slides, M-min slot, <audience>)
Score: X/64 (P%) - <grade>

  Structure         A/8   <symbol>
  Story arc         B/8   <symbol>
  Density           C/8   <symbol>
  Audience fit      D/8   <symbol>
  Stickiness        E/6   <symbol>
  Craft             F/26  <symbol>

Top fixes (ordered by impact: Structure > Story arc > Audience fit > Density > Craft > Stickiness):
  1. <one-line fix> (<dimension>, slide N)
  2. ...
  5. ...

Walk through these one at a time? [yes / no / show full report]
```

Symbol legend: ✓ = full marks, ◐ = any partial and no fails, ✗ = ≥ 1 fail.

Top-fixes ordering: dimension priority is Structure > Story arc > Audience fit > Density > Craft > Stickiness. Within a dimension, lowest sub-check score first; ties broken by slide number ascending.

#### Written report (`critique-report.md` in cwd)

Each dimension as its own H2 section. Each sub-check listed with: pass/partial/fail, evidence (slide ref + quote or PNG note), fix suggestion. Append a "Methodology" section at the bottom referencing `rubric.md`. Overwrite on re-runs.

#### Iteration

Offer the one-at-a-time walkthrough using `AskUserQuestion` per finding (*apply suggested fix*, *skip*, *discuss*). Same pattern as `/slide-deck:review`.

When applying fixes:
- Edit `slides.md` (and `plots/*.py` for Dimension 3.4 figure fixes).
- Rebuild with `make`.
- Re-run only the affected sub-check(s).
- Update the in-memory score table and the `critique-report.md` file.
- Confirm to the user that the fix landed before moving on.

Stop when the user says stop, or when all findings are resolved or skipped.

## Invariants

- **Never claim a fix is done without re-running the affected sub-check.** Same load-bearing rule as `/slide-deck:review`.
- **Never duplicate `/slide-deck:review`'s craft-check logic.** Run the same detects; share the source of truth in `${CLAUDE_PLUGIN_ROOT}/rules/checklist.md`.
- **One fix per turn** unless the user explicitly says "fix all of them."
- **Overwrite `critique-report.md`** on each full run. User can `git diff` against a prior commit for history if they versioned the deck.
- **Don't score a broken build.** Redirect to `/slide-deck:review` if `make` fails.
- **PDFs and non-pandoc decks are out of scope.** If cwd lacks `slides.md`, ask the user for the source dir; don't try to OCR the PDF.
