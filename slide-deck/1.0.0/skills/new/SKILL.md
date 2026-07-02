---
name: new
description: Use when the user wants to create a new LaTeX/beamer presentation from scratch. Bootstraps a pandoc/xelatex/metropolis deck with a configurable brand palette and drafts slides section-by-section, applying the 12 baked-in lessons (no overflow, no em-dashes, jargon glossary, brand-correct plots, speaker notes that actually help). Trigger phrases - "create a presentation", "new slide deck", "/slide-deck:new", "presentation about X".
---

# slide-deck:new

Bootstrap a brand-new LaTeX/beamer presentation in a consistent style. Produces a directory with Makefile, theme (configurable brand palette), plot scaffold, and a first-draft `slides.md` that already obeys all 12 rules from `${CLAUDE_PLUGIN_ROOT}/rules/checklist.md`.

## When to use

- User says "create a presentation", "I need slides for X", "new deck", or types `/slide-deck:new`.
- If a slide-deck-shaped directory already exists in cwd, redirect them to `/slide-deck:review`.

## Process

Follow these phases in order. Do not skip Phase A even if the user seems impatient - the questions prevent the most common rewrites.

### Phase A - clarifying Q&A

Ask one question at a time using `AskUserQuestion` (multiple choice when possible):

1. **Topic + audience.** One sentence. Audience drives jargon level - R&D engineers tolerate more, squad leads and PMs need plain English with glossary.
2. **Time budget.** 5 / 10 / 20 / 30 minutes. Target ~75 sec per slide -> roughly 4 / 8 / 16 / 24 slides.
3. **One-sentence takeaway.** What the audience leaves remembering. If the user can't state it, push back - the deck has no spine yet.
4. **Story arc.** Default - *Problem -> Solution -> Mechanics -> Validation -> Plan -> Q&A*. Alternatives - *Compare A vs B -> Recommendation*, *Status update*, *Custom*.
5. **Source material (optional).** Paths to notes, docs, papers, or a dataset. Read them before drafting.

### Phase B - scaffold

1. Ask for the output dir (default - `~/<topic-slug>/` where slug is kebab-case of the topic).
2. Create the dir. Copy `${CLAUDE_PLUGIN_ROOT}/templates/` into it - `cp -r ${CLAUDE_PLUGIN_ROOT}/templates/* <dir>/` then `mv <dir>/slides.md.template <dir>/slides.md`.
3. Substitute YAML header in `slides.md`:
   - `title`, `subtitle` from Phase A question 1 (topic).
   - `author`: ask the user, or read from `git config user.name`.
   - `date`: today via `date '+%B %d, %Y'`.
   - `audience`: from Phase A question 1 (e.g. "R&D engineers", "PMs", "mixed").
   - `time_budget`: bare integer in minutes from Phase A question 2 (e.g. `20`).
   - `takeaway`: one-sentence string from Phase A question 3.
4. Run `cd <dir> && make` once. Must produce non-empty `slides.pdf`. If it fails, stop and debug pandoc/xelatex before drafting any content.

### Phase C - first draft

1. **Outline first.** Write only the `#` section headers (one per arc beat) and a one-line description of each as a comment. Show the user. Get approval before expanding.
2. **Expand section-by-section.** For each section, write all its slides, then build, then render the new slides to PNG with `pdftoppm -f N -l M -png -r 100 slides.pdf /tmp/sd-new-$$/p`, then Read each PNG and check for overflow. Only after that's clean, show the user.
3. **Apply the 12 rules at write-time** (load `${CLAUDE_PLUGIN_ROOT}/rules/checklist.md`):
   - Max ~5 bullets per slide, or title + figure, or title + 4-row table.
   - No em-dashes in source - never `—`, never ` --- `. Use ` - ` (hyphen with spaces).
   - First acronym mention spelled out inline.
   - Speaker notes - `"<one-liner of what to say>" - <why-it-matters>`. <=7 bullets, <=80 words.
   - Inline commands/identifiers in backticks - `` `mvn install` ``, never raw `mvn install`.
   - No code on slides unless <=6 lines with no `\` continuations.
   - No "background" or "context restated" slides.
   - No superlatives ("powerful", "robust", "seamlessly"). Numbers and verbs only.
4. **Plots.** If a slide needs a figure, write a `plots/<name>.py` that uses `from _common import setup, save, parse_output, BRAND, ROLE` and the `box/arrow/band` helpers. Save target = `figs/<name>.png` via the Makefile rule. After writing the script, run `cd plots && python3 <name>.py -o ../figs/<name>.png`, then Read the PNG and check for floating labels, label-arrow misalignment, panel clipping. Fix before showing user.

### Phase D - handoff

Print to the user:

```
Deck ready at <dir>/.

  cd <dir>
  make                    # build slides.pdf
  make notes.pdf          # build notes.pdf (one slide + notes per page)
  make present            # presenter view via pdfpc - press `s` at runtime to swap screens

Run /slide-deck:review from inside the dir to iterate.
```

## Invariants

- Never claim a draft is done without rendering each new slide to PNG and Reading it.
- Never commit `<dir>/` to a git repo unless the user asks - presentations are personal artifacts.
- If the user asks to skip Phase A questions, push back once. They prevent the rewrites.
- If pandoc/xelatex fails, stop and fix. Don't paper over with `2>/dev/null`.
