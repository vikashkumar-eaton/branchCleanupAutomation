import requests
import subprocess
import yaml
import fnmatch
from datetime import datetime, timezone, timedelta

# Load protected branches
def load_protected_patterns():
    with open('protected_branches.yaml', 'r') as f:
        config = yaml.safe_load(f)
        return config.get('protected', [])

def is_protected_branch(branch_name, protected_patterns):
    for pattern in protected_patterns:
        if fnmatch.fnmatch(branch_name, pattern):
            return True
    return False

def get_merged_pr_branches(github_token, owner, repo, days_old=2):
    headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}
    prs_url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&per_page=100"
    merged_branches = []
    now = datetime.now(timezone.utc)
    page = 1
    while True:
        url = f"{prs_url}&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch PRs: {response.text}")
            break
        data = response.json()
        if not data or isinstance(data, dict):
            break
        for pr in data:
            if pr.get('merged_at'):
                merged_at = datetime.strptime(pr['merged_at'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                if (now - merged_at).days >= days_old:
                    branch = pr['head']['ref']
                    merged_branches.append(branch)
        page += 1
    return merged_branches

def delete_remote_branch(branch):
    print(f"Deleting remote branch: {branch}")
    subprocess.run(["git", "push", "origin", "--delete", branch])

if __name__ == "__main__":
    github_token = input("Enter your GitHub token: ").strip()
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    days_old = 2
    protected_patterns = load_protected_patterns()
    merged_branches = get_merged_pr_branches(github_token, owner, repo, days_old)
    for branch in merged_branches:
        if is_protected_branch(branch, protected_patterns):
            print(f"Skipping protected branch: {branch}")
            continue
        delete_remote_branch(branch)