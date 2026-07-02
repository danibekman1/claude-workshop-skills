---
name: review
description: Use when the user wants to iterate on an existing LaTeX/beamer deck - finds slide overflow, floating labels, em-dashes, unexpanded acronyms, narrative gaps, and other issues from the 12-rule checklist. Renders every touched slide to PNG and inspects visually. Trigger phrases - "review my slides", "check the deck", "/slide-deck:review", "slide N is cropped/blank/broken".
---

# slide-deck:review

Render-and-critique loop for an existing pandoc/beamer deck. Catches the 12 recurring issues from `${CLAUDE_PLUGIN_ROOT}/rules/checklist.md` and iterates with the user, one slide at a time.

## When to use

- User says "review the deck", "the slides look weird", "/slide-deck:review", "slide N is cropped".
- If cwd doesn't look like a deck dir (no `slides.md` or `Makefile`), ask where the deck is - don't guess.

## Process

### Phase A - sanity & build

1. Verify cwd has `slides.md`, `Makefile`, `theme-overrides.tex`. If not, ask the user for the path.
2. Run `make` and capture stderr. If pandoc/xelatex errors, fix those first - rendering is meaningless until build is clean.
3. Render every slide to PNG - `mkdir -p /tmp/sd-review-$$ && pdftoppm -r 100 -png slides.pdf /tmp/sd-review-$$/p`.
4. Count PNGs vs `^##` headers in `slides.md`. A mismatch (PNGs < headers) means an earlier slide's content overflowed and pushed a frame off the page. Flag this as a high-severity finding.

### Phase B - three-class inspection

Load `${CLAUDE_PLUGIN_ROOT}/rules/checklist.md`. Run all three classes.

#### Mechanical (text-level grep, fast)

```bash
# Em-dash lint - pandoc converts both to U+2014
grep -nP '—|\s---\s' slides.md         # must be empty

# Font-size pumping (common overflow cause)
grep -nE '\\(Large|huge|HUGE)\{' slides.md

# Unbalanced ::: notes blocks
awk '/^::: notes/{n++} /^:::$/{n--} END{exit (n!=0)}' slides.md

# Bare underscores outside backticks/math (LaTeX errors)
grep -nE '(^|[^`$\\])_[a-zA-Z]' slides.md

# Unescaped & % # in non-verbatim
grep -nE '(^|[^\\`])[&%#]' slides.md   # report, may be intentional
```

#### Visual (per-PNG inspection)

For each PNG (or just the touched ones if iterating), use Read to view it. Look for:

- **Overflow** - content cut at bottom edge, footer page-number eaten, bullets running off frame.
- **Floating labels** in matplotlib diagrams - arrow labels with no white bbox underneath, labels not sitting on the arrow line.
- **Misaligned diagrams** - arrow endpoints not aligned to box edges/centers; label positions inconsistent across the figure.
- **Code bleed** - monospace blocks wider than the frame.
- **Color drift** - plot uses Tableau defaults (#1f77b4 blue, #d62728 red) instead of the brand palette -> indicates the plot didn't import BRAND/ROLE from `_common.py`.

#### Editorial (whole-deck pass at end)

- **Acronyms unexpanded on first mention.** Build a list - scan `slides.md` for tokens matching `\b[A-Z]{2,}\b`; for each, find first occurrence and check whether expansion follows in parentheses.
- **Speaker notes too long.** For each `::: notes :::` block, count bullets and words. Flag >7 bullets or >80 words.
- **Speaker notes empty.** Flag any `## Slide` without a notes block.
- **Narrative arc gaps.** Check section headers for Problem / Solution / Mechanics / Plan equivalents. Flag if any beat is missing.
- **Superlatives.** Grep for "powerful", "robust", "seamlessly", "leverage", "best-in-class". Suggest rewrites with numbers/verbs.
- **Background slides.** Flag any slide whose first bullet is "context", "background", or restates the previous slide.

### Phase C - report and iterate

Group findings by severity:

1. **Build-breaking** (pandoc errors, unbalanced `:::`).
2. **Overflow** (visual cut-off, PNG count mismatch).
3. **Diagram layout** (floating labels, misalignment, color drift).
4. **Editorial** (notes, acronyms, narrative, superlatives).

Present findings to the user one slide at a time (or grouped by class if many slides are clean). For each finding, use `AskUserQuestion` with options: *apply suggested fix*, *skip*, *discuss*.

When applying fixes:

- Edit `slides.md` (and `plots/*.py` for diagram fixes).
- Rebuild with `make`.
- **Re-render only the touched slides** - `pdftoppm -f N -l N -png -r 100 slides.pdf /tmp/sd-review-$$/sN`.
- Read the new PNG. Confirm the fix landed. Loop if not.

Stop when the user says stop, or when all findings are resolved (or explicitly skipped).

## Invariants

- **Never claim a fix is done without re-rendering the affected slide and Reading the PNG.** This is the single most load-bearing rule - it would have saved most of the "slide N is still cropped" turns in prior sessions.
- When the user says "slide N is blank", check N-1 first - it's almost always an overflow tail from the previous slide, not a real blank frame.
- Don't bulk-edit multiple slides per turn unless the user explicitly says "fix all of them". One-at-a-time iteration is the established preference.
- Visual inspection beats heuristic text scans. If the PNG looks fine, trust it over the grep.
