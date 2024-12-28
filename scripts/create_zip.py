
import os
import zipfile
from datetime import datetime
from typing import List
from git_commit import CUSTOM_IGNORE

def get_files_to_zip() -> List[str]:
    """Get list of files to zip, excluding ignored patterns."""
    files = []
    for root, dirs, filenames in os.walk('.'):
        # Skip directories that start with '.' or are in CUSTOM_IGNORE
        dirs[:] = [
            d for d in dirs if not d.startswith('.') and d not in CUSTOM_IGNORE
        ]
        
        # Filter filenames
        for filename in filenames:
            filepath = os.path.join(root, filename)
            # Skip if the file matches any ignore pattern
            if (not any(ignore in filepath for ignore in CUSTOM_IGNORE)
                    and filename not in CUSTOM_IGNORE):
                files.append(filepath)
    
    return files

def create_zip(output_filename: str = None) -> None:
    """Create a zip file with all non-ignored files."""
    if not output_filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'tree_interval_{timestamp}.zip'
    
    files = get_files_to_zip()
    
    try:
        with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                zipf.write(file)
        print(f"Zip file created successfully: {output_filename}")
        print(f"Total files included: {len(files)}")
        
    except Exception as e:
        print(f"Error creating zip file: {e}")

if __name__ == "__main__":
    custom_filename = input("Enter zip filename (press Enter for auto-name): ").strip()
    create_zip(custom_filename if custom_filename else None)
