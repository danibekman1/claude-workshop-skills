# Claude Workshop Skills

Two Claude Code plugins we use in the Hebrew University research workshop:

- **`slide-deck`** - turn an idea into a real presentation. It asks a few questions, scaffolds a deck, drafts it slide by slide, then renders and critiques its own work. These workshop slides were built with it.
- **`code-review`** - a strict, multi-angle review of whatever you just changed. It reads your git diff and dispatches several specialized reviewers at once, then reports back on style, tests, and risky edits.

## Install

You need [Claude Code](https://docs.claude.com/en/docs/claude-code) already set up. Then, inside Claude Code, run:

```
/plugin marketplace add danielb-ship-it/claude-workshop-skills
/plugin install slide-deck@claude-workshop-skills
/plugin install code-review@claude-workshop-skills
```

Type `/` afterwards - you should see `/slide-deck:new`, `/slide-deck:review`, `/slide-deck:critique`, and `/strict-review` in the list.

## Using them

**slide-deck**

```
/slide-deck:new
```

It interviews you (topic, audience, time budget, the one thing they should remember), then builds the deck. `/slide-deck:review` renders each slide to an image and checks it against a 13-point checklist; `/slide-deck:critique` scores the whole deck against a 6-dimension rubric and gives it a letter grade.

Rendering slides needs a LaTeX toolchain on your machine - `pandoc`, `xelatex`, and the `metropolis` beamer theme. If that isn't installed, Claude will still draft the slide content; it just can't produce the PDF until the tools are there. We can sort this out together at the workshop.

**code-review**

From inside any git repository, after you've made some changes:

```
/strict-review
```

It compares your branch against its base and reports what it finds. It works with zero arguments - just review my changes. (There's an optional `--spec <url>` flag for teams that keep design docs in a wiki; you can ignore it.)

## Notes

These are working copies of internal tooling, lightly adapted for the workshop. Use them, fork them, take them apart to see how a skill is built - that's part of the point.
