# The 13 baked-in lessons

Both `/slide-deck:new` and `/slide-deck:review` load this file. Each rule has:
- `id` - stable handle, used in findings
- `class` - mechanical (greppable), visual (PNG inspection), editorial (judgment)
- `detect` - how to surface it
- `fix` - one-line corrective action

Add a 13th lesson by appending an entry here. No skill code change needed.

---

## 1. Slide overflow

- **class:** visual
- **detect:** Render every touched slide to PNG via `pdftoppm -r 100 -png` and Read it. Look for content cut at the bottom edge, page-number footer eaten, or PNG count < `^## ` heading count in slides.md.
- **fix:** Trim bullets, demote half to `::: notes`, shrink table to `\footnotesize`, or split the slide. Never claim done without re-rendering.
- **evidence:** "slide 11 cropped from the bottom", "slide 17 onwards became blank" (was actually overflow tail).

## 2. Brand palette drift in matplotlib

- **class:** mechanical + visual
- **detect:** `grep -nE '#1f77b4|#d62728|#2ca02c' plots/*.py` (Tableau defaults) or visual check shows non-brand colors.
- **fix:** Import from `_common.py` only: `from _common import BRAND, ROLE`. Never hard-code hex in plot scripts.
- **evidence:** "I think the colours are not human readible."

## 3. Floating diagram labels

- **class:** visual
- **detect:** Arrow labels in matplotlib `FancyArrowPatch` figures appear next to but not on the arrow, or text overlaps arrow line with no white background.
- **fix:** Every arrow label needs `bbox=dict(facecolor='white', edgecolor='none', pad=2.5, alpha=0.95)` and `label_xy` on the arrow midpoint. The `_common.arrow()` helper does this by default.
- **evidence:** "'HTTP/WS' and 'kubectl apply' and 'ECR pull' seems floating?"

## 4. Speaker note quality

- **class:** editorial
- **detect:** For each `::: notes ... :::` block: count bullets and words. Flag > 7 bullets or > 80 words, or empty.
- **fix:** Each bullet is `"<what to say>" - <why it matters>`. Plain-English unpacking of any on-slide jargon as the first bullet.
- **evidence:** "keep whats most imporant so it won't be too crowded", "I need a brief reminder on what to say for each step and why it matters."

## 5. Unexpanded acronyms

- **class:** editorial
- **detect:** For each `\b[A-Z]{2,}\b` token, find first occurrence in slides.md. If the next 30 chars don't contain `(...)`, flag.
- **fix:** First mention spells out: `SVD (Singular Value Decomposition)`. Subsequent uses can abbreviate. Glossary for the deck lives in the appendix notes.
- **evidence:** "Procrustes?", "SVD?", "k3d - how to pronounce?", "max cardinality? no clue."

## 6. Code on slides

- **class:** editorial
- **detect:** Fenced code block inside a `## ` slide. Check line count, presence of `\` continuations, undefined identifiers.
- **fix:** Prefer pseudocode or math notation. If code is mandatory: ≤ 6 lines, no `\` continuations, every identifier self-evident or defined 2 lines above.
- **evidence:** "the code is broken", "no need to show code if its not working."

## 7. Narrative arc gaps

- **class:** editorial
- **detect:** Scan top-level `# ` headers. Expected beats: problem, solution, mechanics/how, validation/numbers (optional), plan/next steps, Q&A.
- **fix:** Add missing beat or restructure. If a slide's only content is "background" or restates the prior slide, delete it.
- **evidence:** "it should tell a story", "drop slide 16 + slides 12-15 are very wordsie and boring."

## 8. pdfpc usability

- **class:** mechanical
- **detect:** Makefile missing `present` target, or HANDOFF.md missing pdfpc keybindings, or anyone trying `pdfpc --windowed <path>` (wrong - `-w` takes value).
- **fix:** Makefile ships `present: slides-pdfpc.pdf; pdfpc -n right slides-pdfpc.pdf`. Tell user `s` swaps screens at runtime, `-S` swaps at launch.
- **evidence:** "isnt there a split screen view?", "Unknown windowed mode '...slides-pdfpc.pdf'" (wrong CLI use).

## 9. Em-dashes

- **class:** mechanical
- **detect:** `grep -nP '—|\s---\s' slides.md` must be empty. Both U+2014 and ` --- ` (pandoc converts the latter to em-dash) are forbidden.
- **fix:** Replace with ` - ` (hyphen with spaces) or rewrite the sentence.
- **evidence:** Many user style guides forbid em-dashes. Pandoc smart-punctuation silently converts ` --- ` to U+2014, so a hyphen-only source can still produce em-dashes in the PDF.

## 10. Special-char escaping

- **class:** mechanical
- **detect:** `grep -nE '(^|[^\\`])[&%#]' slides.md` - flag for review. Bare `_` outside backticks/math: `grep -nE '(^|[^`$\\])_[a-zA-Z]' slides.md`.
- **fix:** Wrap inline commands/identifiers in backticks (pandoc → `\texttt`). For raw LaTeX `\texttt{...}`, escape `_` `&` `%` `$` `#` manually.
- **evidence:** Underscore-related pandoc/LaTeX errors in build logs.

## 11. Frozen Makefile pattern

- **class:** mechanical
- **detect:** Diff against templates/Makefile. Flag added/removed targets or changed PANDOC_FLAGS.
- **fix:** Don't customize the Makefile unless adding a new target. PANDOC_FLAGS, the three PDF targets, and the `figs/%.png: plots/%.py plots/_common.py` rule are frozen.
- **evidence:** Convergence across all three reference decks - same Makefile, same flags.

## 12. Bulk-edit overreach

- **class:** process
- **detect:** Skill behavior, not source-level. A turn that edits 5+ slides without intermediate user confirmation.
- **fix:** One slide (or one section) per turn unless user explicitly says "fix all of them." Render and Read each before claiming done.
- **evidence:** "lets start here with a draft to make it better", "got it. slide 3 - drop X. slide 4 - remove Y. slide 7 - what does Z mean..."

## 13. notes-on-second-screen + `\begin{center}` empty-slide bug

- **class:** mechanical + visual
- **detect:**
  - **Mechanical:** if `pdfpc-preamble.tex` contains `show notes on second screen`, AND `slides.md` contains any `\begin{center}` block OR any markdown table preceded by a `\small`/`\footnotesize`/`\large` switch + blank line, the deck is at risk.
    ```bash
    grep -l "show notes on second screen" pdfpc-preamble.tex && \
      grep -nE '\\begin\{center\}' slides.md
    ```
  - **Visual:** render BOTH `slides.pdf` and `slides-pdfpc.pdf`. Compare same-numbered pages. If the slides-pdfpc page has empty content where slides.pdf has full content, the bug has fired. The notes-panel thumbnail on the right of slides-pdfpc may still show the content (red herring).
- **fix (preferred):** remove `\setbeameroption{show notes on second screen=right}` from `pdfpc-preamble.tex`. **Also** remove `-n right` from the `present` and `present-windowed` targets in `Makefile` - the flag tells pdfpc to slice each page in half looking for notes on the right, which crops slides when the PDF is single-width. The two changes are coupled: do both or neither. Trade-off: pdfpc presenter view loses inline side-by-side notes; speaker uses `notes.pdf` on a separate window/device.
- **fix (alternative):** rewrite every `\begin{center}` block as a markdown blockquote or other construct, and move any "table at top after font-switch + blank line" pattern to use raw LaTeX `tabular` or move the table below other content. Brittle - any new `\begin{center}` reintroduces the bug.
- **evidence:** Empty projector-half slides observed when the notes-on-second-screen option fires together with `\begin{center}` blocks; the speaker's notes-thumbnail still shows full content (red herring).
