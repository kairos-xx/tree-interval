"""Set up GitHub repository and environment variables for the Replit project."""

import os
import subprocess
from subprocess import run

import requests
from replit import db


def setup_github_repo() -> None:
    """Create and configure GitHub repository and environment."""
    try:
        # Get Replit project name and GitHub token
        repl_slug = os.getenv("REPL_SLUG", "")
        github_token = os.getenv("GITHUB_TOKEN", "")

        if not repl_slug or not github_token:
            github_token = input("Enter your GitHub token: ")
            os.environ["GITHUB_TOKEN"] = github_token
            db["GITHUB_TOKEN"] = github_token

        # Configure git identity if not set
        try:
            name = run(
                ["git", "config", "user.name"], capture_output=True, text=True
            ).stdout.strip()
            email = run(
                ["git", "config", "user.email"], capture_output=True, text=True
            ).stdout.strip()

            if not name or not email:
                name = input("Enter your Git name: ")
                email = input("Enter your Git email: ")
                run(
                    ["git", "config", "--global", "user.name", name],
                    check=True,
                )
                run(
                    ["git", "config", "--global", "user.email", email],
                    check=True,
                )
                db["GIT_NAME"] = name
                db["GIT_EMAIL"] = email

        except subprocess.CalledProcessError:
            name = input("Enter your Git name: ")
            email = input("Enter your Git email: ")
            run(["git", "config", "--global", "user.name", name], check=True)
            run(["git", "config", "--global", "user.email", email], check=True)
            db["GIT_NAME"] = name
            db["GIT_EMAIL"] = email

        # Create GitHub repository
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        data = {"name": repl_slug, "private": False, "auto_init": False}

        response = requests.post(
            "https://api.github.com/user/repos", headers=headers, json=data
        )

        if response.status_code != 201:
            print(f"Error creating repository: {response.json()}")
            return

        repo_url = response.json()["clone_url"]
        repo_url = repo_url.replace("https://", f"https://{github_token}@")
        db["GIT_URL"] = repo_url

        # Initialize local repository if needed
        if not os.path.exists(".git"):
            run(["git", "init"], check=True)

        # Add remote and push
        run(["git", "remote", "add", "origin", repo_url], check=True)
        run(["git", "add", "."], check=True)
        run(["git", "commit", "-m", "Initial commit"], check=True)
        run(["git", "push", "-u", "origin", "main"], check=True)

        print(
            f"\nRepository created and configured: {response.json()['html_url']}"
        )
        print("\nGit environment variables have been set in Replit DB")

    except Exception as e:
        print(f"Error setting up repository: {str(e)}")


if __name__ == "__main__":
    setup_github_repo()
