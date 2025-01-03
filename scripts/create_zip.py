"""Create a ZIP archive of the project.

This script creates a timestamped ZIP archive of the project files,
excluding specified directories and files.
"""

from datetime import datetime
from os import makedirs, path, walk
from typing import List
from zipfile import ZipFile


def get_exclude_dirs() -> List[str]:
    """Get list of directories to exclude from ZIP.

    Returns:
        List[str]: Directories to exclude
    """
    return ["build", "dist", "zip", "venv", "logs"]


def create_zip() -> None:
    """Create ZIP archive of project files.

    Creates a timestamped ZIP file in the zip directory,
    excluding specified directories and files.
    """
    # Get current timestamp for filename
    zip_path = "zip"
    project_name = "tree_interval"

    # Ensure zip directory exists
    if not path.exists(zip_path):
        makedirs(zip_path)

    # Create ZIP with filtered contents
    with ZipFile(
        f"{zip_path}/"
        + f"{project_name}_"
        + f'{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        + ".zip",
        "w",
    ) as zip_file:
        for root, dirs, files in walk("."):
            dirs[:] = [
                d
                for d in dirs
                if d not in get_exclude_dirs()
                and not d.startswith(".")
                and not d.startswith("__")
            ]
            for file in files:
                zip_file.write(path.join(root, file))


if __name__ == "__main__":
    create_zip()
