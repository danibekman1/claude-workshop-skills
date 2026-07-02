# Presentation quality rubric (6 dimensions, 32 sub-checks, 64 points)

`/slide-deck:critique` loads this file. Each dimension has 3-4 sub-checks; each sub-check scores 0 (fail), 1 (partial), or 2 (pass).

Dimension score = sum of its sub-check scores. Overall score = sum / 64 → percentage. Grade: A ≥ 90%, B ≥ 75%, C ≥ 60%, D < 60%.

Equal raw weighting; no multipliers. Craft has 13 sub-checks (one per rule in `checklist.md`) so it contributes more in absolute terms than Stickiness (3 sub-checks); this is intentional - craft mistakes are easy to count, while stickiness is judgment-heavy and we keep it small to avoid rewarding gimmicks.

Sub-checks that overlap with `checklist.md` rules are noted by `xref:` and contribute to the relevant dimension's score; they are not double-counted in Craft. Dimension 6 (Craft) uses a single collapsed entry that expands to 13 sub-checks at runtime - see its section for details.

Add a 33rd sub-check or a 7th dimension by appending here - no skill code change needed.

---

## Dimension 1: Structure (from Minto)

Logical organization. Lead with the answer; support with grouped, non-overlapping arguments.

### 1.1 Takeaway stated early

- **class:** editorial
- **detect:** Read YAML `takeaway:` field. Search slide 1 and slide 2 prose (excluding `::: notes`) for the takeaway's content words. Pass if at least 60% of the takeaway's content words appear in slide 1-2 body. Partial if takeaway appears only in title. Fail if takeaway is absent and slide 1 opens with "Agenda", "Background", "Who I am".
- **fix:** Add a prose statement of the takeaway to slide 1 or slide 2.
- **evidence:** Decks that opened with "Why I built this" instead of "We can cut iteration time by 4x."

### 1.2 Body sections MECE

- **class:** editorial
- **detect:** Extract top-level `^# ` headers from `slides.md`. For each pair, check semantic overlap (e.g. both mention "architecture", "approach", "how"). Flag pairs with > 50% word overlap or synonymic overlap.
- **fix:** Merge overlapping sections, or rename one to a distinct beat.
- **evidence:** "Architecture" + "How it works" as two sections covering the same content.

### 1.3 Closing reinforces takeaway

- **class:** editorial
- **detect:** Read the last `## ` slide before any Q&A slide. Search its body for the takeaway's content words. Pass if ≥ 40% overlap. Fail if last content slide is a fresh topic with no callback.
- **fix:** Add a closing slide or expand the final slide to restate the takeaway.
- **evidence:** Deck ends on "Future work" with no return to the opener.

### 1.4 Agenda slide justified

- **class:** mechanical
- **detect:** Count `^## ` slides. If total ≤ 10 AND slide 2 title matches `^(Agenda|Outline|Today|What I.ll cover)`, flag.
- **fix:** Delete the agenda slide. For short decks the structure is self-evident.
- **evidence:** 8-slide decks with an "Outline" on slide 2 listing 4 sections.

## Dimension 2: Story arc (from Duarte)

Narrative shape. Problem → change → resolution. Distinct from Dimension 1 - structure is logical; story is emotional.

### 2.1 Problem-before-solution

- **class:** editorial
- **detect:** Find first `^# ` section header matching `problem|today|pain|gap|risk|why|broken`. Find first `^# ` section header matching `solution|approach|proposal|how|design|architecture`. Pass if problem precedes solution. Partial if problem section exists but is shorter than 1 slide. Fail if no problem section exists.
- **fix:** Add a 1-2 slide "what hurts today" section before the solution.
- **evidence:** Decks opening with the architecture diagram on slide 3 with no setup.

### 2.2 Contrast moment

- **class:** editorial
- **detect:** Search `slides.md` for slides with `before|after|vs|with X / without X|expected|actual` in headers or first bullet. Pass if ≥ 1 such slide exists. Fail if zero.
- **fix:** Add a before/after slide near the solution introduction.
- **evidence:** One-sided decks that only describe the proposed state.

### 2.3 Resolution / call-to-action

- **class:** editorial
- **detect:** Read last `## ` slide before Q&A. Search for imperative verbs (`approve|adopt|pilot|fund|merge|review|decide|sign off|commit`) or "next steps" with a date. Pass if found. Partial if a generic "thanks" with no ask. Fail if deck ends abruptly.
- **fix:** Replace closing "Thanks - questions?" with a specific ask: "I'm asking the squad to pilot this on the next sprint."
- **evidence:** Decks ending on "Q&A" with no decision request.

### 2.4 No flat-list sections

- **class:** editorial
- **detect:** For each `^# ` section, check if every `^## ` slide in the section is an independent topic (Feature A, Feature B, Feature C). Flag if no glue slide ties them together.
- **fix:** Add a "why these together" slide at the section start, or restructure as one slide.
- **evidence:** A "Features" section that reads like a product brochure with no narrative.

## Dimension 3: Density (from Reynolds)

One idea per slide. Bullet/word counts. Signal vs noise.

### 3.1 Bullet count ≤ 5

- **class:** mechanical
- **detect:** For each `^## ` slide, count top-level bullets (`^- `, `^\* `, `^[0-9]+\.`) outside `::: notes` blocks. Pass if ≤ 5. Partial if 6. Fail if ≥ 7.
- **fix:** Trim, demote half to `::: notes`, or split the slide.
- **evidence:** 9-bullet "Architecture" slides.

### 3.2 Word count

- **class:** mechanical
- **detect:** For each slide body (excluding `::: notes`, YAML, code blocks): word-count. Pass if ≤ 50 words. Partial if 51-70. Fail if > 70. Separately: count title words (after `## `); flag titles > 15 words.
- **fix:** Cut paragraphs-disguised-as-bullets. Speaker notes carry the long sentences.
- **evidence:** Bullets that are 30-word sentences.

### 3.3 One idea per slide

- **class:** mechanical + editorial
- **detect:** For each `^## ` header: search for ` and |&| plus |, ` joining what look like two distinct topics. Pass if no such joiner. Partial if joiner present but joining list items ("apples and oranges"). Fail if joining two ideas ("architecture and migration").
- **fix:** Split into two slides.
- **evidence:** "Design tradeoffs and migration plan" as a single slide.

### 3.4 Figures earn their space

- **class:** visual + editorial
- **detect:** For each `\includegraphics` or `![...](figs/...)` reference: read the surrounding slide. Pass if a one-line takeaway bullet or in-figure annotation is present. Fail if figure stands alone with only a title.
- **fix:** Add a "what this shows" caption or annotate the figure directly via the `_common.arrow/box` helpers.
- **evidence:** Bar charts titled "Throughput" with no annotation telling the audience what to notice.

## Dimension 4: Audience fit (from beautiful.ai, sharpened)

Right content for the right audience and time slot.

### 4.1 Jargon level matches audience

- **class:** editorial
- **detect:** Read YAML `audience:` field. Count `\b[A-Z]{2,}\b` tokens + domain-specific jargon per slide.
  - Audience "R&D engineers": pass if avg ≤ 4 jargon tokens/slide.
  - Audience "squad leads" / "mixed": pass if avg ≤ 2.
  - Audience "PMs" / "customers" / "exec": pass if avg ≤ 1.
- **fix:** Replace jargon with plain English in slide body; keep technical terms in `::: notes`.
- **evidence:** PM-audience decks with `SVD`, `MECE`, `k3d`, `gRPC` in the first three slides.

### 4.2 Acronyms defined on first mention

- **class:** editorial
- **xref:** `checklist.md` rule 5
- **detect:** Re-run the same detect logic as `checklist.md` rule 5 (scan `\b[A-Z]{2,}\b` tokens, check first occurrence has expansion in parentheses within ~30 chars). Score under Audience fit; the Craft sub-check 6.5 also runs this and scores it, but the report annotates it as "scored under Audience fit" to avoid double-counting in the user's mental model.
- **fix:** First mention spells out: `SVD (Singular Value Decomposition)`.
- **evidence:** "Procrustes?", "SVD?", "k3d - how to pronounce?", "max cardinality? no clue."

### 4.3 Slide count matches time budget

- **class:** mechanical
- **detect:** Read YAML `time_budget:` (minutes). Count `^## ` slides (excluding Q&A). Target rate: ~75 sec/slide. Pass if slide_count is within [budget/2, budget]. Partial if within [budget/3, budget × 1.5] (and not already in the pass band). Fail if outside.
- **fix:** Cut slides or extend time budget.
- **evidence:** 24-slide decks for 10-min slots.

### 4.4 Audience-relevant framing

- **class:** editorial
- **detect:** Read slides 1-3. Pass if they reference the audience's stake (their problems, their decisions, their context). Fail if they are presenter-centric ("My work this quarter", "What I built").
- **fix:** Reframe the opener around the audience's stake, not the presenter's output.
- **evidence:** Slide 1 reading "My Q2 work" instead of "The bottleneck the squad is hitting."

## Dimension 5: Stickiness (from Heath, lightweight)

What survives the audience's next 24 hours. Three sub-checks only (judgment-heavy; keep small).

### 5.1 Concrete numbers in claims

- **class:** mechanical + editorial
- **detect:** Grep slide body (not notes) for vague adjectives: `\b(fast|slow|scalable|robust|efficient|significant|several|many|various|seamless|powerful|best-in-class|cutting-edge)\b`. Each vague adjective costs a point. Count numeric quantifiers: `\d+\s*(ms|s|x|%|hr|hrs|GB|MB|rps|qps|users|devs|tickets)`. Each numeric quantifier earns a point. Net = quantifiers - adjectives, summed across the deck. Pass if net ≥ 0. Partial if -3 ≤ net < 0. Fail if net < -3.
- **fix:** Replace "fast" with "p99 200 ms at 10k rps". Replace "saves time" with "saves 8 hr/wk per dev."
- **evidence:** "powerful, robust, seamless" trio from older decks.

### 5.2 At least one concrete example

- **class:** editorial
- **detect:** Search the deck for named entities: proper nouns from the domain, ticket IDs (`[A-Z]+-\d+`), timestamps, real customer/team names, screenshots from real systems. Pass if ≥ 1 named entity or screenshot. Fail if 100% abstract.
- **fix:** Add a "real example" slide with an actual scenario, ticket, or log snippet.
- **evidence:** Decks that are 100% boxes-and-arrows with no anchor to lived reality.

### 5.3 Unexpected / contrast moment

- **class:** editorial
- **detect:** Search for counterintuitive framing: `you'd think|surprisingly|actually|turns out|but in fact|despite|even though`. Or a sharp before/after numeric contrast (e.g. "before: 40min, after: 90sec"). Pass if ≥ 1 such moment. Fail if deck is uniformly expected.
- **fix:** Find one number or framing that subverts the audience's prior. If there isn't one, the deck may not have a real insight to land.
- **evidence:** Decks that are a uniform monotone of expected results.

## Dimension 6: Craft (delegated to existing 13 rules)

Production quality. Overflow, em-dashes, palette drift, escape errors. The critique skill imports findings from `/slide-deck:review`'s checks - it does not reinvent them.

### 6.x Craft (collapsed: one sub-check per rule in `checklist.md`)

This is the only sub-check in the file that doesn't follow the `^### \d+\.\d+ ` pattern. Dimension 6 represents 13 sub-checks (6.1 through 6.13), one per rule in `checklist.md`, but they share a single specification block:

- **class:** matches the source rule's class (mechanical / visual / editorial / process).
- **detect:** Run the same `detect` block as the corresponding rule in `checklist.md`.
- **fix:** Same as the corresponding rule's `fix`.
- **scoring:** Each rule contributes 0/1/2 points. Default mapping: rule passes → 2; rule has 1 finding → 1; rule has ≥ 2 findings → 0.

A skill iterating sub-checks should treat this entry as expanding to 13 sub-checks named `6.1` through `6.13`, each delegating to the matching rule in `checklist.md`.

When a craft rule is xref'd by another dimension's sub-check (rule 5 currently), the finding is reported under the higher dimension; the craft sub-check still scores it but the report annotates "scored under Audience fit".
