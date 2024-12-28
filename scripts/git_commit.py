import os
import subprocess
from datetime import datetime
from typing import List, Optional

# Custom list of folders/files to ignore
CUSTOM_IGNORE = [
    'build', '__pycache__', 'dist', 'attached_assets', '.pytest_cache',
    '.ruff_cache', 'tree_interval.egg-info'
]


def get_files_to_commit() -> List[str]:
    """Get list of files to commit, excluding ignored patterns."""
    files = []
    for root, dirs, filenames in os.walk('.'):
        # Skip directories that start with '.' or are in CUSTOM_IGNORE
        dirs[:] = [
            d for d in dirs if not d.startswith('.') and d not in CUSTOM_IGNORE
        ]

        for filename in filenames:
            if not any(ignore in os.path.join(root, filename)
                       for ignore in CUSTOM_IGNORE):
                files.append(os.path.join(root, filename))

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
