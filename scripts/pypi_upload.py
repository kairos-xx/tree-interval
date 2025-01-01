"""PyPI package upload script.

Handles building and uploading package to PyPI with logging.
"""

import os
import subprocess
from datetime import datetime
from typing import List


def run_command(command: List[str], log_file: str) -> None:
    """Run shell command and log output.

    Args:
        command: Command and arguments to execute
        log_file: Path to log file

    Raises:
        subprocess.CalledProcessError: If command fails
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as log:
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT)
            log.write(f"\n=== Command executed at {timestamp} ===\n")
            log.write(f"Command: {' '.join(command)}\n")
            log.write(f"Output:\n{output.decode()}\n")
        except subprocess.CalledProcessError as e:
            log.write(f"\n=== Error at {timestamp} ===\n")
            log.write(f"Command: {' '.join(command)}\n")
            log.write(f"Error:\n{e.output.decode()}\n")
            raise


def upload_to_pypi() -> None:
    """Build and upload package to PyPI.

    Builds distribution files and uploads to PyPI using twine.
    Logs all operations to pypi_upload.log.
    """
    # Ensure logs directory exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_file = "logs/pypi_upload.log"

    # Build distribution files
    run_command(["python", "-m", "build"], log_file)

    # Upload to PyPI
    run_command(["python", "-m", "twine", "upload", "dist/*"], log_file)


if __name__ == "__main__":
    upload_to_pypi()
