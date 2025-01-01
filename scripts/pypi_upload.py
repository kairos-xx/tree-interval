"""PyPI package upload script.

Handles building and uploading package to PyPI with proper
versioning and logging.
Contains utilities for version management and package deployment.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional
import json
import os
import subprocess
import sys
import urllib.request

from replit import info


def get_latest_version() -> str:
    """Fetch the latest version from PyPI.

    Returns:
        str: Latest version number in format 'x.y.z' or
             '0.0.0' if not found
    """
    try:
        url = "https://pypi.org/pypi/tree-interval/json"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            return data["info"]["version"]
    except Exception:
        return "0.0.0"


def increment_version(version: str) -> str:
    """Increment the patch version number.

    Args:
        version: Current version in format 'x.y.z'

    Returns:
        str: Incremented version number
    """
    major, minor, patch = map(int, version.split("."))
    return f"{major}.{minor}.{patch + 1}"


def update_version_in_files(new_version: str) -> None:
    """Update version strings in project configuration files.

    Args:
        new_version: Version string to set
    """
    # Update pyproject.toml
    with open("pyproject.toml", "r") as f:
        content = f.read()
    with open("pyproject.toml", "w") as f:
        f.write(
            content.replace(
                f'version = "{get_latest_version()}"',
                f'version = "{new_version}"',
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

    # Update __init__.py
    with open("src/tree_interval/__init__.py", "r") as f:
        content = f.read()
    with open("src/tree_interval/__init__.py", "w") as f:
        match_string = "__version__ = "
        f.write(
            "\n".join(
                (
                    line.split(match_string, 1)[0]
                    + match_string
                    + f'"{new_version}"\n'
                    if match_string in line
                    else line
                )
                for line in content.splitlines()
            )
        )


def check_token() -> str:
    """Verify PyPI token exists in environment.

    Returns:
        str: PyPI token

    Raises:
        SystemExit: If token is not set
    """
    token = os.getenv("PYPI_TOKEN")
    if not token:
        print("Error: PYPI_TOKEN environment variable not set")
        print("Please set it in the Secrets tab (Environment Variables)")
        sys.exit(1)
    return token


def create_pypirc(token: str) -> None:
    """Create PyPI configuration file with authentication.

    Args:
        token: PyPI authentication token
    """
    pypirc_content = f"""[distutils]
index-servers = pypi

[pypi]
username = __token__
password = {token}
"""
    with open(str(Path.home() / ".pypirc"), "w") as f:
        f.write(pypirc_content)


def build_and_upload(project_dir: Optional[str] = None) -> None:
    """Build and upload package to PyPI.

    Args:
        project_dir: Optional directory containing the project

    Raises:
        SystemExit: If build or upload fails
    """
    working_dir = project_dir if project_dir else "."
    try:
        print(f"Building and uploading {working_dir}...")

        # Clean previous builds
        subprocess.run(
            "rm -rf dist build *.egg-info",
            shell=True,
            cwd=working_dir,
            check=True,
        )

        # Build the package
        subprocess.run(
            ["python", "setup.py", "sdist", "bdist_wheel"],
            cwd=working_dir,
            check=True,
        )

        # Upload to PyPI
        subprocess.run(
            ["python", "-m", "twine", "upload", "dist/*"],
            cwd=working_dir,
            check=True,
        )

        print(f"Successfully uploaded {working_dir} to PyPI!")

    except subprocess.CalledProcessError as e:
        print(f"Error during build/upload for {working_dir}: {e}")
        sys.exit(1)


def main() -> None:
    """Main execution function for PyPI package upload."""
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
