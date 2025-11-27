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

1. Update `protected_branches.yaml` as needed.
2. Run `cleanup_branches.py` to see which branches would be deleted or skipped.
3. Only unprotected branches will be considered for deletion.

## Maintainers
- Please review and update the protection list regularly.
- All changes to protected branches are tracked in version control for transparency.
