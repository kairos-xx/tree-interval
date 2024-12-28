
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

def create_zip():
    """Create a zip file with all non-ignored files."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f'tree_interval_{timestamp}.zip'
    files = get_files_to_process()

    try:
        with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                zipf.write(file)
        print(f"✅ Zip file created: {output_filename}")
    except Exception as e:
        print(f"❌ Error creating zip: {e}")

def get_latest_version():
    try:
        with urllib.request.urlopen("https://pypi.org/pypi/tree-interval/json") as response:
            return json.loads(response.read())["info"]["version"]
    except Exception:
        return "0.0.0"

def upload_to_pypi():
    """Build and upload package to PyPI."""
    try:
        token = os.getenv("PYPI_TOKEN")
        if not token:
            print("❌ Error: PYPI_TOKEN not set")
            return

        # Create .pypirc
        pypirc_content = f"""[distutils]
index-servers = pypi

[pypi]
username = __token__
password = {token}
"""
        with open(str(Path.home() / ".pypirc"), "w") as f:
            f.write(pypirc_content)

        # Build and upload
        subprocess.run(["pip", "install", "wheel", "twine", "build"], check=True)
        subprocess.run("rm -rf dist build *.egg-info", shell=True, check=True)
        subprocess.run(["python", "setup.py", "sdist", "bdist_wheel"], check=True)
        subprocess.run(["python", "-m", "twine", "upload", "dist/*"], check=True)
        print("✅ Package uploaded to PyPI")
    except Exception as e:
        print(f"❌ Error uploading to PyPI: {e}")

def commit_changes():
    """Commit and push changes to git."""
    try:
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'config', 'user.email', "noreply@replit.com"], check=True)
            subprocess.run(['git', 'config', 'user.name', "Replit"], check=True)

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
    
    print("\n1. Creating ZIP archive...")
    create_zip()
    
    print("\n2. Uploading to PyPI...")
    upload_to_pypi()
    
    print("\n3. Committing changes...")
    commit_changes()
    
    print("\n✨ All operations completed!")

if __name__ == "__main__":
    main()
