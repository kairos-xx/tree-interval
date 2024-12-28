import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

from replit import info


def get_latest_version():
    try:
        url = "https://pypi.org/pypi/tree-interval/json"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            return data["info"]["version"]
    except Exception:
        return "0.0.0"


def increment_version(version):
    major, minor, patch = map(int, version.split("."))
    return f"{major}.{minor}.{patch + 1}"


def update_version_in_files(new_version):
    # Update pyproject.toml
    with open("pyproject.toml", "r") as f:
        content = f.read()
    with open("pyproject.toml", "w") as f:
        f.write(
            content.replace(
<<<<<<< HEAD
                f'version = "{get_latest_version()}"',
                f'version = "{new_version}"',
=======
                f'version = "{get_latest_version()}"', f'version = "{new_version}"'
>>>>>>> origin/main
            )
        )

    # Update setup.py
    with open("setup.py", "r") as f:
        content = f.read()
    with open("setup.py", "w") as f:
        f.write(
            content.replace(
                f'version="{get_latest_version()}"', f'version="{new_version}"'
            )
        )


def check_token():
    token = os.getenv("PYPI_TOKEN")
    if not token:
        print("Error: PYPI_TOKEN environment variable not set")
        print("Please set it in the Secrets tab (Environment Variables)")
        sys.exit(1)
    return token


def create_pypirc(token):
    pypirc_content = f"""[distutils]
index-servers = pypi

[pypi]
username = __token__
password = {token}
"""
    with open(str(Path.home() / ".pypirc"), "w") as f:
        f.write(pypirc_content)


def build_and_upload(project_dir=None):
    working_dir = project_dir if project_dir else "."
    try:
        print(f"Building and uploading {working_dir}...")

        # Clean previous builds
        subprocess.run(
<<<<<<< HEAD
            "rm -rf dist build *.egg-info",
            shell=True,
            cwd=working_dir,
            check=True,
=======
            "rm -rf dist build *.egg-info", shell=True, cwd=working_dir, check=True
>>>>>>> origin/main
        )

        # Build the package
        subprocess.run(
<<<<<<< HEAD
            ["python", "setup.py", "sdist", "bdist_wheel"],
            cwd=working_dir,
            check=True,
=======
            ["python", "setup.py", "sdist", "bdist_wheel"], cwd=working_dir, check=True
>>>>>>> origin/main
        )

        # Upload to PyPI
        subprocess.run(
<<<<<<< HEAD
            ["python", "-m", "twine", "upload", "dist/*"],
            cwd=working_dir,
            check=True,
=======
            ["python", "-m", "twine", "upload", "dist/*"], cwd=working_dir, check=True
>>>>>>> origin/main
        )

        print(f"Successfully uploaded {working_dir} to PyPI!")

    except subprocess.CalledProcessError as e:
        print(f"Error during build/upload for {working_dir}: {e}")
        sys.exit(1)


def main():
    # Install required packages
    subprocess.run(["pip", "install", "wheel", "twine", "build"], check=True)

    # Get current version and increment it
    current_version = get_latest_version()
    new_version = increment_version(current_version)
    print(f"Incrementing version from {current_version} to {new_version}")

    # Update version in files
    update_version_in_files(new_version)

    # Check and setup PyPI token
    token = check_token()
    create_pypirc(token)

    # Build and upload directly
    build_and_upload(f'{Path.home()}/{(info.replit_url or "").split("/")[-1]}')
    print("Tree Interval package built and uploaded successfully!")


if __name__ == "__main__":
    main()
