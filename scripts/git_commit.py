"""Script to automate Git commits.

Handles staged changes in Git repository by creating commits
with standardized messages and optional push to remote.
"""

import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional


def run_git_command(command: list[str], log_file: Path) -> Optional[str]:
    """Run a Git command and log output.
    
    Args:
        command: Git command as list of strings
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
    """Main entry point for Git commit automation."""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'git_commit.log'
    
    # Generate commit message with timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f'Auto commit: {timestamp}'
    
    # Run git commands
    if (run_git_command(['git', 'add', '.'], log_file) and 
          run_git_command(['git', 'commit', '-m', message], log_file)):
          run_git_command(['git', 'push'], log_file)


if __name__ == '__main__':
    main()