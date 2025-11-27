import yaml
import fnmatch

# Load protected branches from YAML config
with open('protected_branches.yaml', 'r') as f:
    config = yaml.safe_load(f)
    protected_patterns = config.get('protected', [])

def is_protected_branch(branch_name):
    """
    Returns True if the branch matches any protected pattern.
    Supports wildcards (e.g., release/*).
    """
    for pattern in protected_patterns:
        if fnmatch.fnmatch(branch_name, pattern):
            return True
    return False

# Example usage:
if __name__ == "__main__":
    test_branches = ["main", "feature/important-feature", "release/v1.2.3", "bugfix/123"]
    for b in test_branches:
        print(f"{b}: {'PROTECTED' if is_protected_branch(b) else 'not protected'}")
