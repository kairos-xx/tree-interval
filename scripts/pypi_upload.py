import os
import subprocess
import sys
from pathlib import Path


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
            "rm -rf dist build *.egg-info", shell=True, cwd=working_dir, check=True
        )

        # Build the package
        subprocess.run(
            ["python", "setup.py", "sdist", "bdist_wheel"], cwd=working_dir, check=True
        )

        # Upload to PyPI
        subprocess.run(
            ["python", "-m", "twine", "upload", "dist/*"], cwd=working_dir, check=True
        )

        print(f"Successfully uploaded {working_dir} to PyPI!")

    except subprocess.CalledProcessError as e:
        print(f"Error during build/upload for {working_dir}: {e}")
        sys.exit(1)


def main():
    # Install required packages
    subprocess.run(["pip", "install", "wheel", "twine", "build"], check=True)

    # Check and setup PyPI token
    token = check_token()
    create_pypirc(token)

    # Build and upload directly
    build_and_upload()
    print("Tree Interval package built and uploaded successfully!")


if __name__ == "__main__":
    main()
