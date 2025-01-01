
"""Script to build and upload package to PyPI.

Handles the process of building Python package distributions
and uploading them to PyPI using twine.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional


def run_command(command: list[str], log_file: Path) -> Optional[str]:
    """Run a shell command and log output.
    
    Args:
        command: Command as list of strings
        log_file: Path to log file
        
    Returns:
        str: Command output if successful, None otherwise
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        log_file.write_text(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        log_file.write_text(f'Error: {e.stderr}')
        return None


def main() -> None:
    """Main entry point for PyPI upload process."""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'pypi_upload.log'
    
    # Build distributions
    if run_command(['python', '-m', 'build'], log_file):
        # Upload to PyPI
        username = os.environ.get('PYPI_USERNAME')
        password = os.environ.get('PYPI_PASSWORD')
        
        if username and password:
            run_command([
                'twine', 'upload',
                'dist/*',
                '-u', username,
                '-p', password
            ], log_file)


if __name__ == '__main__':
    main()
