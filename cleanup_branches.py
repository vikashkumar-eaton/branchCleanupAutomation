import subprocess
from branch_protection import is_protected_branch

# List all remote branches (example for origin)
def get_remote_branches():
    result = subprocess.run(["git", "branch", "-r"], capture_output=True, text=True)
    branches = [line.strip().replace('origin/', '') for line in result.stdout.splitlines() if '->' not in line]
    return branches

# Attempt to delete a branch if not protected
def cleanup_stale_branches():
    branches = get_remote_branches()
    for branch in branches:
        if is_protected_branch(branch):
            print(f"Skipping protected branch: {branch}")
            continue
        # Example: print or delete (uncomment next line to actually delete)
        print(f"Would delete branch: {branch}")
        # subprocess.run(["git", "push", "origin", "--delete", branch])

if __name__ == "__main__":
    cleanup_stale_branches()
