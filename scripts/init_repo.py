"""Initialize a new Git repository for the Replit project.

This script creates a new Git repository and configures it with the
current project directory.
"""

import os
from subprocess import run


def init_git_repo() -> None:
    """Initialize a new Git repository for the current project."""
    try:
        # Get Replit project name from environment
        repl_slug = os.getenv("REPL_SLUG", "")
        if not repl_slug:
            print("Error: Could not determine Repl name")
            return

        # Initialize git repository
        run(["git", "init"], check=True)

        # Configure git user if not already set
        try:
            run(["git", "config", "user.name"], check=True)
        except:
            name = input("Enter your name for Git: ")
            run(["git", "config", "user.name", name], check=True)

        try:
            run(["git", "config", "user.email"], check=True)
        except:
            email = input("Enter your email for Git: ")
            run(["git", "config", "user.email", email], check=True)

        # Add all files
        run(["git", "add", "."], check=True)

        # Initial commit
        run(["git", "commit", "-m", "Initial commit"], check=True)

        print(f"\nGit repository initialized as '{repl_slug}'")
        print("\nNext steps:")
        print("1. Create a new repository on your Git provider (e.g. GitHub)")
        print("2. Add your repository URL as a remote:")
        print("   git remote add origin <repository-url>")
        print("3. Push your code:")
        print("   git push -u origin main")

    except Exception as e:
        print(f"Error initializing repository: {str(e)}")


if __name__ == "__main__":
    init_git_repo()
