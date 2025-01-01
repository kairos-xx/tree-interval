
"""Create a ZIP archive of the project.

This script creates a timestamped ZIP archive of the project files,
excluding specified directories and files.
"""

import os
from datetime import datetime
from typing import List
from zipfile import ZipFile

def get_exclude_dirs() -> List[str]:
    """Get list of directories to exclude from ZIP.
    
    Returns:
        List[str]: Directories to exclude
    """
    return [
        "__pycache__",
        ".git",
        ".pytest_cache",
        ".ruff_cache",
        "build",
        "dist",
        "venv",
        "logs",
    ]

def create_zip() -> None:
    """Create ZIP archive of project files.
    
    Creates a timestamped ZIP file in the zip directory,
    excluding specified directories and files.
    """
    # Get current timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"tree_interval_{timestamp}.zip"
    
    # Ensure zip directory exists
    if not os.path.exists("zip"):
        os.makedirs("zip")
        
    exclude_dirs = get_exclude_dirs()
    
    # Create ZIP with filtered contents
    with ZipFile(f"zip/{zip_name}", "w") as zip_file:
        for root, dirs, files in os.walk("."):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                # Skip ZIP files
                if file.endswith(".zip"):
                    continue
                    
                file_path = os.path.join(root, file)
                zip_file.write(file_path)

if __name__ == "__main__":
    create_zip()
