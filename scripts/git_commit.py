"""Automated git commit script.

Handles git add, commit, and push operations with logging.
"""

from datetime import datetime
from os import makedirs, path
from subprocess import CalledProcessError, run
from typing import Optional


def git_commit(message: Optional[str] = None) -> None:
    """Perform git commit and push operations.

    Args:
        message: Optional commit message. Uses timestamp if not provided.

    Raises:
        subprocess.CalledProcessError: If git commands fail
    """
    # Use timestamp as default commit message
    if not message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Auto commit: {timestamp}"

    # Ensure logs directory exists
    if not path.exists("logs"):
        makedirs("logs")

    # Log git operations
    with open("logs/git_commit.log", "a") as log:
        try:
            # Add all changes
            run(["git", "add", "."], check=True)
            log.write(f"\nGit add completed at {datetime.now()}\n")

            # Commit changes
            run(["git", "commit", "-m", message], check=True)
            log.write(f"Git commit completed at {datetime.now()}\n")

            # Push changes
            run(["git", "push"], check=True)
            log.write(f"Git push completed at {datetime.now()}\n")

        except CalledProcessError as e:
            log.write(f"Error during git operations: {str(e)}\n")
            raise


if __name__ == "__main__":
    git_commit()
