
"""Script to get Git author information.

Retrieves the Git author name and email from local Git config
or environment variables. Used for package metadata.
"""

import os
from typing import Tuple


def get_git_author() -> Tuple[str, str]:
    """Get Git author name and email.
    
    Returns:
        Tuple[str, str]: Author name and email
    """
    # Try environment variables first
    name = os.environ.get('GIT_AUTHOR_NAME', '')
    email = os.environ.get('GIT_AUTHOR_EMAIL', '')
    
    if not name or not email:
        # Fallback to git config
        try:
            import subprocess
            name = subprocess.check_output(
                ['git', 'config', 'user.name']
            ).decode().strip()
            email = subprocess.check_output(
                ['git', 'config', 'user.email']
            ).decode().strip()
        except Exception:
            name = 'Unknown'
            email = 'unknown@example.com'
    
    return name, email


if __name__ == '__main__':
    author_name, author_email = get_git_author()
    print(f'Author: {author_name} <{author_email}>')
