## Enforcing Branch Naming Conventions

This repository enforces branch naming conventions using a GitHub Actions workflow (`.github/workflows/branch-naming.yml`).

- **Allowed branch name patterns:**
  - main
  - develop
  - release/*
  - hotfix/*
  - feature/*
  - bugfix/*
- When a pull request is created or updated, the workflow checks the source branch name.
- If the branch name does not match the allowed patterns, the workflow fails and provides clear feedback in the PR “Checks” tab.
- Contributors must use compliant branch names for their PRs to pass CI and be merged.

# Branch Protection and Cleanup Guide

This repository supports branch protection to prevent accidental deletion of important branches.

## How to Mark a Branch as Protected

- Edit the `protected_branches.yaml` file in the repository root.
- Add branch names or wildcard patterns under the `protected` key. Example:

```yaml
protected:
  - main
  - develop
  - release/*
  - hotfix/*
  - feature/*
  - bugfix/*
```

Branches matching these names or patterns will be protected from deletion by cleanup scripts.

## How Protection Works

- The `branch_protection.py` script loads the protected patterns and provides an `is_protected_branch(branch_name)` function.
- The `cleanup_branches.py` script uses this function to skip protected branches during cleanup.
- Actual deletion is commented out for safety; review and uncomment if you wish to enable deletion.


## Usage

### Manual Cleanup
1. Update `protected_branches.yaml` as needed.
2. Run `cleanup_branches.py` to see which branches would be deleted or skipped (no branches are deleted unless you uncomment the deletion line).
3. Only unprotected branches will be considered for deletion.

### Automated/Scheduled Cleanup
1. The repository includes a scheduled GitHub Actions workflow (`.github/workflows/scheduled-branch-cleanup.yml`) that runs `delete_merged_branches.py` automatically (e.g., daily).
2. This script deletes remote branches whose pull requests have been merged and are older than 2 days, except for protected branches.
3. The workflow uses a GitHub token stored as a repository secret for authentication.
4. You can also trigger the workflow manually from the GitHub Actions tab.

## Enforcing PR Naming Convention

Pull request titles must start with `YUK-` followed by one or more digits, then a colon, and then any description. For example:

```
YUK-123: Add new feature for user login
YUK-4567: Fix bug in payment processing
```

This is enforced by a GitHub Actions workflow. PRs that do not follow this pattern will fail the check and must be renamed.

**How to update the PR title:**
- Go to the Pull Request page on GitHub.
- Click the PR title at the top (it becomes editable).
- Edit the title to match the required format (e.g., `YUK-123: Add new feature`).
- Save or press Enter. The check will re-run automatically.

> **Note:** Actual deletion in both scripts is protected by the patterns in `protected_branches.yaml`. Review and uncomment the deletion line in scripts if you wish to enable real branch deletion.

## Maintainers
- Please review and update the protection list regularly.
- All changes to protected branches are tracked in version control for transparency.
