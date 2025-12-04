import os
import requests
import yaml

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = os.environ.get('REPO_OWNER')
REPO_NAME = os.environ.get('REPO_NAME')

PROTECTED_BRANCHES_FILE = 'protected_branches.yaml'
GITHUB_API = 'https://api.github.com'

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json',
}

def load_protected_branches():
    with open(PROTECTED_BRANCHES_FILE, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('protected', [])

def update_branch_protection(branch):
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/branches/{branch}/protection"
    # Example: Require status checks and prevent deletion
    payload = {
        "required_status_checks": None,
        "enforce_admins": True,
        "required_pull_request_reviews": None,
        "restrictions": None,
        "allow_deletions": False,
        "allow_force_pushes": False
    }
    resp = requests.put(url, headers=headers, json=payload)
    if resp.status_code in (200, 201):
        print(f"Protection updated for branch: {branch}")
    else:
        print(f"Failed to update protection for {branch}: {resp.status_code} {resp.text}")

def main():
    branches = load_protected_branches()
    for branch in branches:
        # Only apply to exact branch names, not patterns
        if '*' not in branch:
            update_branch_protection(branch)
        else:
            print(f"Skipping pattern: {branch} (manual protection required)")

if __name__ == "__main__":
    main()
