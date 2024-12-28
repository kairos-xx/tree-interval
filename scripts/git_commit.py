import os
import subprocess
from datetime import datetime
from typing import List, Optional

# Custom list of patterns to ignore (directories and files)
CUSTOM_IGNORE = [
    # Directories
    'build',
    '__pycache__',
    'dist',
    'attached_assets',
    '.pytest_cache',
    '.ruff_cache',
    'tree_interval.egg-info',
    # Individual files
    '.coverage',
    ".gitignore",
    'poetry.lock',
    'flake.txt',
    "poetry.lock",
    ".replit",
    "replit.nix",
    "generated-icon.png"
]


def init_git_repo():
    """Initialize git repository if not already initialized."""
    if not os.path.exists('.git'):
        try:
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(
                ['git', 'config', 'user.email', "noreply@replit.com"],
                check=True)
            subprocess.run(['git', 'config', 'user.name', "Replit"],
                           check=True)
            print("Git repository initialized")
        except subprocess.CalledProcessError as e:
            print(f"Error initializing git repository: {e}")
            return False
    return True


def get_files_to_commit() -> List[str]:
    """Get list of files to commit, excluding ignored patterns."""
    files = []
    for root, dirs, filenames in os.walk('.'):
        # Skip directories that start with '.' or are in CUSTOM_IGNORE
        dirs[:] = [
            d for d in dirs if not d.startswith('.') and d not in CUSTOM_IGNORE
        ]

        # Filter filenames
        for filename in filenames:
            filepath = os.path.join(root, filename)
            # Skip if the file matches any ignore pattern
            if (not any(ignore in filepath for ignore in CUSTOM_IGNORE)
                    and filename not in CUSTOM_IGNORE):
                files.append(filepath)

    return files


def commit_changes() -> None:
    """Commit changes to git repository."""
    if not init_git_repo():
        return

    message = f"Auto commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    try:
        # Fetch and merge remote changes
        subprocess.run(['git', 'fetch', 'origin', 'main'], check=True)
        subprocess.run(
            ['git', 'merge', 'origin/main', '--allow-unrelated-histories'],
            check=True)

        # Add all files
        subprocess.run(['git', 'add', '.'], check=True)

        # Commit
        subprocess.run(['git', 'commit', '-m', message], check=True)

        # Push changes
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print("Changes committed and pushed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e}")
        print("Try resolving any merge conflicts manually")


if __name__ == "__main__":
    commit_changes()
