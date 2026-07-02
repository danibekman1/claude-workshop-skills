---
description: Run strict code review on current branch using 34+ review patterns (18 style + 6 test + 5 test-minimization + 5 refactoring + optional spec compliance + per-language packs gated on the diff + skill review gated on the diff) plus 4 judgment-guided design principles (KISS/YAGNI/DRY/SOLID)
argument-hint: [description of changes] [--spec <confluence-url>] [--no-spec]
---

# Strict Review

Run a strict code review on the current branch's changes vs the base branch. Dispatches the four base reviewers in parallel (code-style, test-validation, test-minimizer, refactoring-safety), plus spec-compliance when a spec is provided, one language pack per language whose files appear in the diff, and skill-review when the diff touches skill files, performs cross-component analysis, and produces a unified report.

## Setup

1. **Detect working directory and base branch:**
   - Use the current working directory as `{WORK_DIR}`
   - Detect the base branch to diff against (defaults to the remote's default branch, else `main`):
     ```bash
     BASE_BRANCH="$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo main)"
     ```
     Use this value as `{BASE_BRANCH}` throughout.

2. **Detect description:**
   - If the user provided arguments, use them as `{DESCRIPTION}`: `$ARGUMENTS`
   - Otherwise, auto-detect from the branch:
     ```bash
     git log "${BASE_BRANCH}"...HEAD --oneline --no-decorate
     ```
     Summarize the commit messages into a short description.

3. **Detect decision log path:**
   - Check if there's a PR for the current branch:
     ```bash
     gh pr view --json number --jq '.number' 2>/dev/null
     ```
   - If a PR exists: `{DECISION_LOG_PATH}` = `{WORK_DIR}/tasks/strict-review-decisions-PR-{NUMBER}.md`
   - If no PR: Use the branch name:
     ```bash
     git branch --show-current
     ```
     `{DECISION_LOG_PATH}` = `{WORK_DIR}/tasks/strict-review-decisions-{BRANCH}.md`

4. **Detect spec URL (optional):**
    - Check if user provided `--spec <url>` in arguments: parse `$ARGUMENTS` for `--spec` followed by a URL
    - Check if user provided `--no-spec`: if so, skip spec compliance entirely
    - If no `--spec` in arguments, check the decision log header for a stored spec URL:
      - Read `{DECISION_LOG_PATH}` and look for a line starting with `spec: `
      - If found, use that URL as `{SPEC_URL}`
    - If a `--spec <url>` was provided:
      - Store/update it in the decision log header (create the file if needed):
        ```markdown
        # Strict Review Decision Log - PR #{NUMBER} (or branch name)
        spec: {URL}
        ```
      - Set `{SPEC_URL}` to the provided URL
    - If no spec URL found anywhere, set `{SPEC_URL}` to empty. Spec compliance will be skipped.
    - If `{SPEC_URL}` is set, fetch the design doc content:
      - Extract the page ID from the URL (standard Confluence URL format)
      - Fetch via REST API:
        ```bash
        source ~/.bashrc
        PAGE_ID=$(echo "{SPEC_URL}" | grep -oP 'pages/\K[0-9]+')
        curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
          "${JIRA_URL}wiki/rest/api/content/${PAGE_ID}?expand=body.storage,version" \
          | python3 -c "
        import sys, json, re
        d = json.load(sys.stdin)
        title = d.get('title', 'Unknown')
        version = d.get('version', {}).get('when', 'Unknown')
        body = d.get('body', {}).get('storage', {}).get('value', '')
        clean = re.sub(r'<[^>]+>', ' ', body)
        clean = re.sub(r'\s+', ' ', clean).strip()
        print(f'# {title}')
        print(f'Last modified: {version}')
        print()
        print(clean)
        "
        ```
      - Save the output as `{SPEC_CONTENT}`

5. **Load and execute the orchestrator:**
    - Read the orchestrator template at `${CLAUDE_PLUGIN_ROOT}/skills/strict-review/strict-review-orchestrator.md`
    - Substitute `{WORK_DIR}`, `{DESCRIPTION}`, `{DECISION_LOG_PATH}`, `{BASE_BRANCH}`, `{SPEC_URL}`, and `{SPEC_CONTENT}` with the detected values
    - If `{SPEC_URL}` is empty, pass empty strings for both spec placeholders
    - Dispatch the orchestrator as a subagent via Task tool (general-purpose)
    - The orchestrator will dispatch the base reviewers plus any conditional ones (spec compliance, language packs, skill review) in parallel and return a unified report

## After Review

- Present the unified review output to the user
- Invoke the review-walkthrough skill (`${CLAUDE_PLUGIN_ROOT}/skills/review-walkthrough/review-walkthrough.md`) to walk through findings one at a time
- The walkthrough collects user decisions, creates action items, and updates the decision log
