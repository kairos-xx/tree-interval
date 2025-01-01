
"""Get git author information.

Retrieves the git author name and email from git config.
"""

from typing import Tuple
import subprocess

def get_git_author() -> Tuple[str, str]:
    """Get git author name and email.
    
    Returns:
        Tuple[str, str]: Author name and email
    
    Raises:
        subprocess.CalledProcessError: If git command fails
    """
    # Get author name
    name = subprocess.check_output(
        ["git", "config", "user.name"]
    ).decode().strip()
    
    # Get author email
    email = subprocess.check_output(
        ["git", "config", "user.email"]
    ).decode().strip()
    
    return name, email

if __name__ == "__main__":
    author_name, author_email = get_git_author()
    print(f"Author: {author_name} <{author_email}>")
