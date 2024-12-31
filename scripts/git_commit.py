import os
import subprocess
from datetime import datetime
from typing import List

# Custom list of patterns to ignore
CUSTOM_IGNORE = [
    "build",
    "__pycache__",
    "dist",
    "attached_assets",
    ".pytest_cache",
    ".ruff_cache",
    "tree_interval.egg-info",
    ".coverage",
    ".gitignore",
    "zip",
    "logs",
    "dev",
    "poetry.lock",
    "flake.txt",
    ".replit",
    "replit.nix",
    "generated-icon.png",
]


def clean_merge_conflicts(file_path: str) -> None:
    """Remove merge conflict markers from a file."""
    try:
        # Skip binary files and non-text files
        if os.path.splitext(file_path)[1] in [".png", ".jpg", ".zip", ".pyc"]:
            return

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Skip if no conflict markers
        if "<<<<<<< HEAD" not in content:
            return

        # Keep the HEAD version (local changes)
        lines = content.split("\n")
        cleaned_lines = []
        skip_mode = False

        for line in lines:
            if line.strip().startswith("<<<<<<< HEAD"):
                skip_mode = False
                continue
            elif line.strip().startswith("======="):
                skip_mode = True
                continue
            elif line.strip().startswith(">>>>>>> origin/replit"):
                skip_mode = False
                continue

            if not skip_mode:
                cleaned_lines.append(line)

        # Write back cleaned content
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(cleaned_lines))
        print(f"✅ Cleaned merge conflicts in {file_path}")

    except Exception as e:
        print(f"❌ Error cleaning merge conflicts in {file_path}: {e}")


def get_all_files(directory: str = ".") -> List[str]:
    """Get list of all files recursively."""
    files = []
    for root, dirs, filenames in os.walk(directory):
        dirs[:] = [
            d for d in dirs if not d.startswith(".") and d not in CUSTOM_IGNORE
        ]
        for filename in filenames:
            filepath = os.path.join(root, filename)
            if not any(ignore in filepath for ignore in CUSTOM_IGNORE):
                files.append(filepath)
    return files


def clean_all_files() -> None:
    """Clean merge conflicts in all files."""
    files = get_all_files()
    for file in files:
        clean_merge_conflicts(file)


def commit_changes():
    """Commit and push changes to git."""
    try:
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(
                ["git", "config", "user.email", "noreply@replit.com"],
                check=True)
            subprocess.run(["git", "config", "user.name", "Replit"],
                           check=True)

        # Clean merge conflicts in all files first
        clean_all_files()

        subprocess.run(["git", "add", "."], check=True)
        message = ("Auto commit:" +
                   f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push", "origin", "replit"], check=True)
        print("✅ Changes committed and pushed")
    except Exception as e:
        print(f"❌ Error in git operations: {e}")


def main():
    """Run all operations."""
    print("🚀 Starting automated operations...")
    print("\nCleaning merge conflicts and committing changes...")
    commit_changes()
    print("\n✨ All operations completed!")


if __name__ == "__main__":
    main()
