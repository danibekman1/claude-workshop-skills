# Review Walkthrough

Walk through strict-review findings one at a time. The strict-review report is already in the conversation context from the orchestrator's return.

## Instructions

Parse the strict-review report and walk through every finding interactively. Do NOT dump the full report. Present findings one at a time.

### Step 1: Parse the Report

Extract all findings into an ordered list from these report sections:
1. **Auto-Fixes Applied** - type: `auto-fix`
2. **Flagged for Decision** (Style, Test Validation, Refactoring Safety, Spec Compliance) - type: `flagged`
3. **Report (Awareness)** - type: `report`
4. **Cross-Component Insights** - type: `cross-component`

Count the total: `TOTAL = auto-fixes + flagged + report + cross-component`

If TOTAL is 0 and the verdict is Approve, say: "Strict review passed with no findings. Nothing to walk through." and stop.

### Step 2: Show Progress and Summary

Before starting the walkthrough, show a brief summary:

```
Strict review returned N findings:
- A auto-fixes applied
- F items flagged for decision
- R items for awareness
- C cross-component insights

Walking through each one now. [1/N]
```

### Step 3: For Each Finding

Present findings in the order listed above (auto-fixes first, then flagged, then report, then cross-component).

For EACH finding:

**3a. Show header with progress:**
```
[N/TOTAL] {TYPE_LABEL}: [{ID}: {Pattern Name}]
File: {file:line} [{BRANCH/LOCAL/BOTH}]
```

Where TYPE_LABEL is one of: "Auto-Fix", "Flagged", "Report", "Cross-Component"

**3b. Show the code:**
Use the Read tool to read the file at the specified line (5 lines before, 10 lines after the finding location). Show the relevant snippet.

If the file doesn't exist or the line reference is unclear, show what's available from the report's finding description instead.

**3c. Explain the finding:**
- What the reviewer found (1-2 sentences)
- Why it matters (1 sentence)
- Your recommendation with brief reasoning (1 sentence)

Keep it concise. The user should be able to decide in seconds.

**3d. Ask for decision using AskUserQuestion:**

Use type-aware options:

**For auto-fix findings:**
```
AskUserQuestion:
  question: "[N/TOTAL] {ID}: {summary} - this was auto-fixed. What do you want to do?"
  header: "Auto-fix"
  options:
    - label: "Confirm"
      description: "Keep the auto-fix as applied."
    - label: "Revert"
      description: "Undo this auto-fix, keep original code."
    - label: "Modify"
      description: "I want a different fix - I'll explain."
```

**For flagged findings:**
```
AskUserQuestion:
  question: "[N/TOTAL] {ID}: {summary} - what do you want to do?"
  header: "{ID}"
  options:
    - label: "Fix (Recommended)"
      description: "{brief description of what the fix would be}"
    - label: "Skip"
      description: "Acknowledge but don't change anything."
    - label: "Modify"
      description: "I want a different approach - I'll explain."
```

**For spec-compliance findings (SC-1: Missing Requirement):**
```
AskUserQuestion:
  question: "[N/TOTAL] SC-1: {summary} - this requirement is missing from the implementation. What do you want to do?"
  header: "SC-1"
  options:
    - label: "Implement now"
      description: "Add this to the implementation task list."
    - label: "Defer"
      description: "Create a follow-up ticket for this requirement."
    - label: "Already covered"
      description: "This is implemented elsewhere - I'll explain where."
```

**For spec-compliance findings (SC-2: Wrong Approach):**
```
AskUserQuestion:
  question: "[N/TOTAL] SC-2: {summary} - the implementation deviates from the design. What do you want to do?"
  header: "SC-2"
  options:
    - label: "Fix to match design"
      description: "Change the code to match the design's approach."
    - label: "Update design"
      description: "The implementation approach is better - update the design doc."
    - label: "Discuss"
      description: "Need to discuss this with the design author."
```

**For spec-compliance findings (SC-3: Unspecified Addition):**
```
AskUserQuestion:
  question: "[N/TOTAL] SC-3: {summary} - this code isn't covered by the design. What do you want to do?"
  header: "SC-3"
  options:
    - label: "Keep"
      description: "Keep the code and update the design to reflect it."
    - label: "Remove"
      description: "Remove this code - it's out of scope."
    - label: "Discuss"
      description: "Need to discuss whether this belongs."
```

**For spec-compliance findings (SC-4: Ambiguous Design):**
```
AskUserQuestion:
  question: "[N/TOTAL] SC-4: {summary} - the design is ambiguous here. What do you want to do?"
  header: "SC-4"
  options:
    - label: "Interpret as..."
      description: "I'll state my interpretation of the design intent."
    - label: "Clarify with author"
      description: "Need the design author to clarify this area."
    - label: "Flag on design doc"
      description: "Add a comment on the Confluence page requesting clarification."
```

**For report findings:**
```
AskUserQuestion:
  question: "[N/TOTAL] {ID}: {summary} - this is for awareness. Any action?"
  header: "Report"
  options:
    - label: "Noted"
      description: "Acknowledged, no action needed."
    - label: "Want to fix"
      description: "Actually, I'd like to address this."
```

**For cross-component insights:**
```
AskUserQuestion:
  question: "[N/TOTAL] Cross-component: {summary} - pursue this?"
  header: "Cross-comp"
  options:
    - label: "Pursue"
      description: "Add this to the fix list."
    - label: "Skip"
      description: "Not worth the complexity right now."
```

**3e. Record the decision:**
After the user answers, record: `{ID} -> {decision}`. If the user chose "Modify" or "Other", ask a follow-up to understand what they want, then record it.

Move to the next finding.

### Step 4: Summary and Next Steps

After all findings are walked through, present a summary:

```
## Walkthrough Complete

### Decisions Summary
| # | Finding | Decision |
|---|---------|----------|
| 1 | {ID}: {summary} | {decision} |
| ... | ... | ... |

### Action Items
- {list of items that need fixing, from "Fix", "Revert", "Want to fix", "Pursue", or "Modify" decisions}

### No Action Needed
- {list of "Confirm", "Skip", "Noted" items}
```

Then:
1. **Create tasks** for each action item using TaskCreate
2. **Update the decision log** - copy Pending Decisions rows from the report, replacing `PENDING` with the actual decision text and today's date
3. **Proceed to implement** the action items (fix tasks)

## Key Principles

- **One finding at a time** - never batch multiple findings in one question
- **Always show code** - the user needs visual context to decide
- **Recommend, don't dictate** - give your recommendation but respect the user's choice
- **Progress indicator** - always show [N/TOTAL] so the user knows how far along they are
- **Record everything** - decisions feed into the decision log and task list
