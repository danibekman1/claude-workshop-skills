---
name: skill-review
description: Reviews Claude Code skill definitions (a SKILL.md plus its supporting files) for frontmatter validity, broken file references, description and triggering quality, content voice, and progressive disclosure. Dispatched only when the diff touches skill files. Use as part of strict-review.
---

# Skill Review

Reviews the skill definitions a diff changes. A skill is a `SKILL.md` (YAML frontmatter plus a Markdown body) and the supporting files it points to. This reviewer checks that the frontmatter is valid, the file references resolve, the description triggers reliably, the body reads as instructions, and detail sits behind pointers rather than crammed into the entry file.

The rubric is adapted from the plugin-dev `skill-reviewer` agent (the `claude-plugins-official` marketplace). It is embedded here, not invoked, so strict-review carries no runtime dependency on plugin-dev being installed. The adaptation also corrects one generic assumption that is wrong for this plugin: see "Progressive disclosure in this plugin" below.

## When to Use

- After adding or changing a skill (a `SKILL.md` or any file under a `skills/` directory)
- As part of the strict-review orchestrator, which dispatches this reviewer automatically when the diff touches skill files
- Directly, to review a skill's structure and triggering in isolation

## How to Use

Dispatch as a subagent using the Task tool with the `skill-reviewer.md` template.

```
Task tool (general-purpose):
  description: "Skill review: [description]"
  prompt: [contents of skill-reviewer.md with placeholders filled]
```

Fill in `{WORK_DIR}`, `{DESCRIPTION}`, and `{DECISION_LOG_PATH}`. The orchestrator also passes `{DIFF_CONTENT}` and `{DECIDED_ITEMS}`; when you invoke the reviewer directly without them, it gathers the diff and reads the decision log itself.

## Patterns and Authority Levels

Two patterns may flag because they are objective, verifiable breakage; the other three are advisory and never block, like the design principles and test-minimizer. There is no auto-fix.

- **Flag** (genuine structural breakage that makes the skill malfunction):
  - `SK-1` Frontmatter validity - a required field (`name` or `description`) is missing, or the YAML frontmatter is malformed or absent.
  - `SK-2` Broken file reference - the `SKILL.md` (or a changed supporting file) points to a path that does not exist on disk.
- **Report** (advisory, Comment at most):
  - `SK-3` Description and triggering quality - the description should be third person, name concrete trigger phrases, and sit roughly in the 50-500 character range.
  - `SK-4` Content quality and voice - the body should use imperative or infinitive instructions ("To do X, do Y"), not second-person narration, and give concrete guidance over vague advice.
  - `SK-5` Progressive disclosure - detail that belongs in a referenced file is inlined into the `SKILL.md`, or referenced detail lacks a pointer from the entry file.

## Progressive Disclosure in This Plugin

The generic skill-reviewer rubric targets a 1,000-3,000 word `SKILL.md` and treats a short one as a defect. That is wrong here. In this plugin the split between a lean `SKILL.md` and a detailed `*-reviewer.md` (or `references/`) sibling IS the progressive disclosure: the `SKILL.md` is the intended entry point, and the depth lives one pointer away. So `SK-5` judges whether the `SKILL.md` is a clear entry point that points to its detail, not whether it crosses a word count. A short `SKILL.md` that points to a detailed template is correct, not "too short", and must not be flagged for length.

## Verdict Guidelines

- **Approve:** no findings.
- **Comment:** one or more report-level findings (`SK-3`, `SK-4`, `SK-5`) and no standing flag finding.
- **Request Changes:** at least one `SK-1` or `SK-2` finding stands. This matches code-style, so the orchestrator's most-severe-sub-verdict rule needs no special case.
