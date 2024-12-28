
import os
import subprocess
from datetime import datetime
import zipfile
import urllib.request
import json
from pathlib import Path
import sys
from typing import List

# Custom list of patterns to ignore
CUSTOM_IGNORE = [
    'build', '__pycache__', 'dist', 'attached_assets',
    '.pytest_cache', '.ruff_cache', 'tree_interval.egg-info',
    '.coverage', ".gitignore", 'poetry.lock', 'flake.txt',
    ".replit", "replit.nix", "generated-icon.png"
]

def clean_merge_conflicts(file_path: str) -> None:
    """Remove merge conflict markers from a file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Skip if no conflict markers
        if '<<<<<<< HEAD' not in content:
            return

        # Keep the HEAD version (local changes)
        lines = content.split('\n')
        cleaned_lines = []
        skip_mode = False
        
        for line in lines:
            if line.startswith('<<<<<<< HEAD'):
                skip_mode = False
                continue
            elif line.startswith('======='):
                skip_mode = True
                continue
            elif line.startswith('>>>>>>> origin/main'):
                skip_mode = False
                continue
            
            if not skip_mode:
                cleaned_lines.append(line)
        
        # Write back cleaned content
        with open(file_path, 'w') as f:
            f.write('\n'.join(cleaned_lines))
            
    except Exception as e:
        print(f"Error cleaning merge conflicts in {file_path}: {e}")

def get_files_to_process() -> List[str]:
    """Get list of files to process, excluding ignored patterns."""
    files = []
    for root, dirs, filenames in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in CUSTOM_IGNORE]
        for filename in filenames:
            filepath = os.path.join(root, filename)
            if not any(ignore in filepath for ignore in CUSTOM_IGNORE) and filename not in CUSTOM_IGNORE:
                files.append(filepath)
    return files

def commit_changes():
    """Commit and push changes to git."""
    try:
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'config', 'user.email', "noreply@replit.com"], check=True)
            subprocess.run(['git', 'config', 'user.name', "Replit"], check=True)
        
        # Clean merge conflicts in all files
        files = get_files_to_process()
        for file in files:
            clean_merge_conflicts(file)
        
        subprocess.run(['git', 'add', '.'], check=True)
        message = f"Auto commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', message], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print("✅ Changes committed and pushed")
    except Exception as e:
        print(f"❌ Error in git operations: {e}")

def main():
    """Run all operations."""
    print("🚀 Starting automated operations...")
    print("\nCommitting changes...")
    commit_changes()
    print("\n✨ All operations completed!")

if __name__ == "__main__":
    main()
