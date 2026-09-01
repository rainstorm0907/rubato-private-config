---
name: pr-wrap
description: Manage pull-request creation and updates from the current git worktree. Use when asked to create a PR, update an existing PR, or update PR documentation. This skill owns staging, committing, pushing, and GitHub PR operations; document-only requests use their dedicated document skills.
---

# PR Wrap

Execute a deterministic PR-doc workflow based on whether the current branch already has an open PR.

## Preconditions

- Work from the current repository/worktree.
- Ensure `gh` is installed and authenticated.
- Assume `wrapping-sessions` and `update-docs` skills are available.

## Branch And PR Detection

1. Detect current branch:
   - `git rev-parse --abbrev-ref HEAD`
2. Detect whether a PR exists for that branch:
   - `gh pr view --json number,url,title,headRefName,baseRefName`
3. Branch by result:
   - Success: follow **Existing PR Path**
   - Error "no pull requests found": follow **No PR Path**
4. If branch/PR mapping is ambiguous, pause and ask for PR number.

## No PR Path (Create)

1. Run the `wrapping-sessions` workflow:
   - Create a new wrap document under `cycles/YYYY-MM/wkN/MM-DD/HHMM-topic-wrap.md`.
   - Document full journey from checkpoint replay (early → middle → latest), not only latest session.
2. Keep the created wrap path for common finalization.

## Existing PR Path (Update)

1. Find wrap doc already included in PR:
   - `gh pr view --json files --jq '.files[].path' | rg '(^|/)cycles/.+-wrap\\.md$'`
2. Select the matching wrap file for current task context.
3. Run the `update-docs` workflow:
   - Append an update section with current time.
   - Reconfirm full checkpoint replay and record how this update fits the whole journey.
4. Keep the updated wrap path for common finalization.

## Common Git Finalization

After either document workflow returns:

1. Stage the topic-scoped code and documentation changes plus the wrap document.
2. Create one conventional commit containing the whole topic change.
3. Include the required trailer:
   - `Co-Authored-By: Codex <noreply@openai.com>`
4. Push:
   - No PR path: `git push -u origin HEAD`
   - Existing PR path: `git push`

## GitHub Finalization

- No PR path:
  1. Create the PR with `gh pr create --fill`.
  2. Ensure the PR text references the wrap document path.
- Existing PR path:
  1. Optionally add a comment summarizing the update and wrap path.
- Return the PR URL, commit hash, and wrap file path.

## Fallback Rules

- If no wrap file exists in the existing PR, create one using `wrapping-sessions`, then continue to common finalization.
- If `gh` is not authenticated, request `gh auth login` and pause.
- Do not rewrite or remove previous wrap sections; append only.
- Avoid touching unrelated files.
- `wrapping-sessions` and `update-docs` only write documents; never delegate Git operations to them.

## Completion Checklist

- Wrap document created or updated correctly.
- Commit created and pushed.
- PR created or updated on current branch.
- Final report includes:
  - PR URL
  - Commit hash
  - Wrap file path
