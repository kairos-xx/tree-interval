
"""Script to create a ZIP archive of the project.

This script creates a timestamped ZIP archive of the project files,
excluding specified directories and files. The archive is saved
in the 'zip' directory.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Set
from zipfile import ZipFile


def get_excluded_paths() -> Set[str]:
    """Get set of paths to exclude from ZIP archive.
    
    Returns:
        Set[str]: Set of directory/file paths to exclude
    """
    return {
        '.git', '__pycache__', '.pytest_cache', '.ruff_cache',
        'build', 'dist', '.coverage', '.venv'
    }


def create_zip(source_dir: str, zip_name: str) -> None:
    """Create a ZIP archive of the source directory.
    
    Args:
        source_dir: Path to directory to archive
        zip_name: Name of output ZIP file
    """
    excluded = get_excluded_paths()
    
    # Create zip directory if it doesn't exist
    zip_dir = Path('zip')
    zip_dir.mkdir(exist_ok=True)
    
    # Create the ZIP archive
    with ZipFile(zip_dir / zip_name, 'w') as zf:
        for root, dirs, files in os.walk(source_dir):
            # Remove excluded dirs
            dirs[:] = [d for d in dirs if d not in excluded]
            
            for file in files:
                file_path = Path(root) / file
                if not any(ex in str(file_path) for ex in excluded):
                    zf.write(file_path)


def main() -> None:
    """Main entry point for ZIP creation."""
    # Generate ZIP filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_name = f'tree_interval_{timestamp}.zip'
    
    try:
        create_zip('.', zip_name)
        print(f'Created {zip_name}')
    except Exception as e:
        print(f'Error creating ZIP: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
