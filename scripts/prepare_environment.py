"""GitHub Actions workflow update script.
Updates GitHub Actions workflow files with new configurations.
"""
from importlib import import_module
from inspect import getmembers_static
from json import dumps as json_dumps
from os import environ, getenv
from os.path import exists
from subprocess import CalledProcessError, run
from textwrap import dedent
from typing import Tuple
from replit import info
from requests import get, post
from toml import dump as toml_dump
from toml import load as toml_load


def check_packages(required_packages: Tuple) -> Tuple:
    """Check if packages are installed and return missing ones.
    Args:
        required_packages: List of package names to check
    Returns:
        List of missing package names
    """
    missing_packages = ()
    for package in required_packages:
        try:
            import_module(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is not installed")
            missing_packages += (package, )
    return missing_packages


def install_missing_packages(packages: Tuple[str]) -> None:
    """Install missing packages using pip.
    Args:
        packages: List of packages to install
    """
    for package in packages:
        try:
            run(["pip", "install", package], check=True)
            print(f"Successfully installed {package}")
        except CalledProcessError as e:
            print(f"Failed to install {package}: {e}")


def init_git_repo(project_name, user_name, user_email) -> None:
    """Initialize a new Git repository for the current project."""
    try:
        # Initialize git repository
        run(["git", "init"], check=True)
        # Configure git user if not already set
        run(["git", "config", "user.name", user_name], check=True)
        run(["git", "config", "user.email", user_email], check=True)
        # Add all files
        run(["git", "add", "."], check=True)
        # Initial commit
        run(["git", "commit", "-m", "Initial commit"], check=True)
        print(f"\nGit repository initialized as '{project_name}'")
    except Exception as e:
        print(f"Error initializing repository: {str(e)}")


def setup_github_repo(github_token, author_name) -> None:
    """Create and configure GitHub repository."""
    try:
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {"name": author_name, "private": False, "auto_init": False}
        response = post("https://api.github.com/user/repos",
                        headers=headers,
                        json=data)
        if response.status_code != 201:
            print(f"Error creating repository: {response.json()}")
            return
        response_json = response.json()
        repo_url = response_json["clone_url"].replace(
            "https://", f"https://{github_token}@")
        if not exists(".git"):
            run(["git", "init"], check=True)
        # Add remote and push
        run(["git", "remote", "add", "origin", repo_url], check=True)
        run(["git", "add", "."], check=True)
        run(["git", "commit", "-m", "Initial commit"], check=True)
        run(["git", "push", "-u", "origin", "main"], check=True)
        print(
            f"\nRepository created and configured: {response_json['html_url']}"
        )
    except Exception as e:
        print(f"Error setting up repository: {str(e)}")


def update_workflows() -> None:
    required_packages = (
        "toml",
        "replit",
        "requests",
    )
    project_info = {
        "paths": {
            "pyproject": "pyproject.toml",
            "requirements": "requirements.txt",
            "replit": ".replit",
            "nix": "replit.nix",
            "readme": "README.md",
        },
        "templates": {
            "pyproject": {
                "build-system": {
                    "requires": ["setuptools>=45", "wheel"],
                    "build-backend": "setuptools.build_meta",
                },
                "project": {
                    "name":
                    "",
                    "version":
                    "",
                    "description":
                    "",
                    "readme":
                    "README.md",
                    "authors": [{
                        "name": "Joao Lopes",
                        "email": "joaoslopes@gmail.com"
                    }],
                    "license": {
                        "file": "LICENSE"
                    },
                    "requires-python":
                    ">=3.11",
                    "classifiers": [
                        "Development Status :: 5 - Production/Stable",
                        "Intended Audience :: Developers",
                        "Intended Audience :: Science/Research",
                        "License :: OSI Approved :: MIT License",
                        "Programming Language :: Python :: 3",
                        "Programming Language :: Python :: 3.11",
                        "Topic :: Software Development :: Libraries :: "
                        "Python Modules",
                        "Topic :: Software Development :: Code Generators",
                        "Topic :: Software Development :: Debuggers",
                        "Operating System :: OS Independent",
                        "Natural Language :: English",
                        "Typing :: Typed",
                    ],
                    "urls": {
                        "Homepage":
                        ("https://github.com/kairos-xx/tree-interval"),
                        "Repository":
                        ("https://github.com/kairos-xx/tree-interval.git"),
                    },
                },
                "tool": {
                    "ruff": {
                        "lint": {
                            "select": [
                                "E",
                                "W",
                                "F",
                                "I",
                                "B",
                                "C4",
                                "ARG",
                                "SIM",
                            ],
                            "ignore": ["W291", "W292", "W293", "E203", "E701"],
                        }
                    },
                    "flake8": {
                        "max-line-length": 79,
                        "ignore": ["E203", "E701", "W503"],
                    },
                },
            },
            "replit": {
                "run": ["python", ""],
                "entrypoint": "README.md",
                "modules": ["python-3.11:v30-20240222-aba8eb6"],
                "hidden": [".pythonlibs"],
                "disableGuessImports": True,
                "disableInstallBeforeRun": True,
                "nix": {
                    "channel": "stable-23_11"
                },
                "unitTest": {
                    "language": "python3"
                },
                "deployment": {
                    "run": ["python3", ""],
                    "deploymentTarget": "cloudrun",
                },
                "env": {
                    "PYTHONPATH":
                    "$PYTHONPATH:$REPL_HOME/.pythonlibs/lib/python3.11/site-packages"
                },
                "workflows": {
                    "workflow": [
                        {
                            "name":
                            "[Package] pypi upload",
                            "mode":
                            "sequential",
                            "author":
                            299513,
                            "tasks": [{
                                "task":
                                "shell.exec",
                                "args":
                                "python scripts/pypi_upload.py | " +
                                "tee logs/pypi_upload.log 2>&1",
                            }],
                        },
                        {
                            "name": "————————————————",
                            "mode": "sequential",
                            "author": 299513,
                            "tasks": [{
                                "task": "shell.exec",
                                "args": ""
                            }],
                        },
                        {
                            "name":
                            "[Util] create zip",
                            "mode":
                            "sequential",
                            "author":
                            299513,
                            "tasks": [{
                                "task": "shell.exec",
                                "args": "python scripts/create_zip.py",
                            }],
                        },
                        {
                            "name":
                            "[Util] build",
                            "mode":
                            "sequential",
                            "author":
                            299513,
                            "tasks": [{
                                "task":
                                "shell.exec",
                                "args":
                                "rm -rf dist build *.egg-info && " +
                                "python setup.py sdist bdist_wheel",
                            }],
                        },
                        {
                            "name":
                            "[Util] tests",
                            "mode":
                            "sequential",
                            "author":
                            299513,
                            "tasks": [{
                                "task":
                                "shell.exec",
                                "args":
                                "pytest ./tests | " +
                                "tee logs/tests.log 2>&1",
                            }],
                        },
                        {
                            "name":
                            "[Util] update workflows",
                            "mode":
                            "sequential",
                            "author":
                            299513,
                            "tasks": [{
                                "task":
                                "shell.exec",
                                "args":
                                "python scripts/update_workflows.py | " +
                                "tee logs/update_worflows.log 2>&1",
                            }],
                        },
                        {
                            "name": "————————————————",
                            "mode": "sequential",
                            "author": 299513,
                            "tasks": [{
                                "task": "shell.exec",
                                "args": ""
                            }],
                        },
                        {
                            "name":
                            "[Format] ruff",
                            "mode":
                            "sequential",
                            "author":
                            299513,
                            "tasks": [{
                                "task": "shell.exec",
                                "args": "ruff format --line-length 79"
                            }],
                        },
                        {
                            "name":
                            "[Format] black",
                            "mode":
                            "sequential",
                            "author":
                            299513,
                            "tasks": [{
                                "task": "shell.exec",
                                "args": "black . --line-length 79",
                            }],
                        },
                        {
                            "name":
                            "[Format] isort",
                            "mode":
                            "sequential",
                            "author":
                            299513,
                            "tasks": [{
                                "task": "shell.exec",
                                "args": "isort . -l 79 -m 1",
                            }],
                        },
                        {
                            "name": "————————————————",
                            "mode": "sequential",
                            "author": 299513,
                            "tasks": [{
                                "task": "shell.exec",
                                "args": ""
                            }],
                        },
                        {
                            "name":
                            "[Report] pyright",
                            "mode":
                            "sequential",
                            "author":
                            299513,
                            "tasks": [{
                                "task":
                                "shell.exec",
                                "args":
                                "pyright --warnings | " +
                                "tee logs/pyright.log 2>&1",
                            }],
                        },
                        {
                            "name":
                            "[Report] flake8",
                            "mode":
                            "sequential",
                            "author":
                            299513,
                            "tasks": [{
                                "task":
                                "shell.exec",
                                "args":
                                "pflake8 --exclude */. --exclude ./build  | " +
                                "tee logs/flake8.log 2>&1",
                            }],
                        },
                        {
                            "name":
                            "[Report] ruff",
                            "mode":
                            "sequential",
                            "author":
                            299513,
                            "tasks": [{
                                "task":
                                "shell.exec",
                                "args":
                                "ruff check " +
                                "./dev ./src ./examples ./tests ./scripts  " +
                                "--line-length 79 | " +
                                "tee logs/ruff.log 2>&1",
                            }],
                        },
                        {
                            "name":
                            "[Report] pytest",
                            "mode":
                            "sequential",
                            "author":
                            299513,
                            "tasks": [{
                                "task":
                                "shell.exec",
                                "args":
                                "pytest --cov=src --cov-report term-missing | "
                                + "tee logs/pytest.log 2>&1",
                            }],
                        },
                        {
                            "name":
                            "[Report] All",
                            "mode":
                            "sequential",
                            "author":
                            299513,
                            "tasks": [{
                                "task":
                                "shell.exec",
                                "args":
                                "pyright --warnings | " +
                                "tee logs/pyright.log 2>&1 && " +
                                "pflake8 --exclude */. --exclude ./build | " +
                                "tee logs/flake8.log 2>&1 && " +
                                "ruff check ./dev ./src ./examples ./tests ./scripts | "
                                + "tee logs/ruff.log 2>&1",
                            }],
                        },
                    ]
                },
            },
            "nix":
            '''
            {pkgs}: {
              deps = [
              @@@
              ];
            }
            ''',
        },
        "name":
        "",
        "version":
        "0.1.1",
        "description":
        "",
        "author_name":
        "Joao Lopes",
        "git_config": {
            "user_name": "kairos-xx",
            "user_email": "joaoslopes@gmail.com"
        },
        "urls": {
            "Homepage": "https://github.com/",
            "Repository": "https://github.com/",
        },
        "requirements": [
            "pytest>=7.0.0",
            "pytest",
            "replit==4.1.0",
            "black",
            "flake8",
            "build",
            "requests",
            "toml",
            "pyyaml",
            "isort",
        ],
        "entrypoint":
        "main.py",
        "nix_packages": ["pkgs.libyaml", "pkgs.nano", "pkgs.python312Full"]
    }
    project_name = get(str(info.replit_id_url)).url.split("/")[-1]
    user_name = project_info["git_config"]["user_name"]
    user_email = project_info["git_config"]["user_email"]
    author_name = project_info["author_name"]
    author = getenv("REPL_OWNER_ID", "299513")
    github_token = getenv("GITHUB_TOKEN", "")
    if not github_token:
        github_token = environ[
            "GITHUB_TOKEN"] = "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"
    project_info["urls"]["Homepage"] += f"{user_name}/{project_name}"
    project_info["urls"]["Repository"] += f"{user_name}/{project_name}.git"
    project_info["name"] = project_info["templates"]["pyproject"][
        "name"] = project_name
    pyproject_dict = project_info["templates"]["pyproject"]
    pyproject_dict["project"]["authors"][0]["name"] = author_name
    pyproject_dict["project"]["authors"][0]["email"] = user_email
    pyproject_dict["project"]["version"] = project_info["version"]
    pyproject_dict["project"]["description"] = project_info["description"]
    pyproject_dict["project"]["urls"] = project_info["urls"]
    requirements_text = "\n".join(project_info["requirements"])
    nix_text = project_info["templates"]["nix"].replace(
        "@@@", "\n".join(project_info["nix_packages"]))
    replit_dict = project_info["templates"]["replit"]
    for v in replit_dict["workflows"]["workflow"]:
        v["author"] = int(author)
    replit_dict["run"][1] = replit_dict["deployment"][1] = replit_dict[
        "entrypoint"] = project_info["entrypoint"]

    def create():
        missing_packages = check_packages(required_packages)
        if missing_packages:
            print("\nInstalling missing packages...")
            install_missing_packages(missing_packages)
        else:
            print("\nAll required packages are installed!")
        with open(project_info["paths"]["pyproject"], "w") as f:
            toml_dump(pyproject_dict, f)
        with open(project_info["paths"]["requirements"], "w") as f:
            f.write(requirements_text)
        with open(project_info["paths"]["nix"], "w") as f:
            f.write(dedent(nix_text))
        open(project_info["paths"]["readme"], 'a+').close()
        init_git_repo(project_name, user_name, user_email)
        setup_github_repo(github_token, author_name)


if __name__ == "__main__":
    update_workflows()
