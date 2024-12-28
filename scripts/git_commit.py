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
    "replit.nix"
]


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


def commit_changes(message: Optional[str] = None) -> None:
    """Commit changes to git repository."""
    if not message:
        message = f"Auto commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    files = get_files_to_commit()

    try:
        # Add files
        for file in files:
            subprocess.run(['git', 'add', file], check=True)

        # Commit
        subprocess.run(['git', 'commit', '-m', message], check=True)
        print("Changes committed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e}")


if __name__ == "__main__":
    commit_message = input(
        "Enter commit message (press Enter for auto-message): ").strip()
    commit_changes(commit_message if commit_message else None)
