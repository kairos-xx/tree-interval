"""GitHub Actions workflow configuration and environment setup.

This module handles the setup and configuration of GitHub Actions workflows,
environment variables, and project dependencies. It includes utilities for
checking and installing required packages, setting up GitHub repositories,
and managing project configurations.
"""

from difflib import get_close_matches
from importlib import import_module
from os import environ, getenv, mkdir
from os.path import exists
from subprocess import CalledProcessError, run
from textwrap import dedent
from typing import List, Optional, Tuple

from replit import db, info
from requests import get, post
from toml import dump as toml_dump


def check_packages(
        required_packages: Optional[List[str]] = None) -> Tuple[str, ...]:
    """Check which required packages are missing from the environment.

    Args:
        required_packages: List of package names to check

    Returns:
        Tuple of missing package names
    """
    missing_packages = ()
    for package in required_packages or []:
        try:
            import_module(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is not installed")
            missing_packages += (package, )
    return missing_packages


def install_missing_packages(
        packages: Optional[Tuple[str, ...]] = None) -> None:
    """Install packages that are missing from the environment.

    Args:
        packages: Tuple of package names to install

    Raises:
        CalledProcessError: If package installation fails
    """
    for package in packages or []:
        try:
            run(["pip", "install", package], check=True)
            print(f"Successfully installed {package}")
        except CalledProcessError as e:
            print(f"Failed to install {package}: {e}")


def setup_github_repo(
    github_token: str,
    project_name: str,
    user_name: str,
    user_email: str,
    name: str,
) -> None:
    """Create and configure a GitHub repository for the project.

    Args:
        github_token: GitHub authentication token
        project_name: Name of the project/repository
        user_name: GitHub username
        user_email: User's email address
        name: Full name of the user

    Raises:
        Exception: If repository initialization or configuration fails
    """
    try:
        if not exists(".git"):
            run(["git", "init"], check=True)
        run(["git", "config", "--global", "user.name", user_name], check=True)
        run(
            ["git", "config", "--global", "user.email", user_email],
            check=True,
        )
        print(f"\nGit repository initialized as '{project_name}'")
    except Exception as e:
        print(f"Error initializing repository: {str(e)}")
        return

    try:
        response = post(
            "https://api.github.com/user/repos",
            headers={
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json",
            },
            json={
                "name": name,
                "private": False,
                "auto_init": False,
            },
        )

        if response.status_code != 201:
            print(f"Error creating repository: {response.json()}")
            return

        response_json = response.json()
        db["GITHUB_TOKEN"] = environ["GITHUB_TOKEN"] = github_token
        db["GIT_NAME"] = user_name
        db["GIT_EMAIL"] = user_email
        repo_url = db["GIT_URL"] = response_json["clone_url"].replace(
            "https://",
            f"https://{github_token}@",
        )

        run(["git", "remote", "add", "origin", repo_url], check=True)
        run(["git", "add", "."], check=True)
        run(["git", "commit", "-m", "Initial commit"], check=True)
        run(["git", "push", "-u", "origin", "main"], check=True)

        print(
            f"\nRepository created and configured: {response_json['html_url']}"
        )
    except Exception as e:
        print(f"Error setting up repository: {str(e)}")


def run_all() -> None:
    """Execute all environment setup tasks.

    This function orchestrates the entire setup process including:
    - Loading project configuration
    - Installing required packages
    - Setting up GitHub repository
    - Configuring project files
    """
    project_info = {
        "templates": {
            "pyproject": {
                "build-system": {
                    "requires": [
                        "setuptools>=45",
                        "wheel",
                    ],
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
                    "authors": [
                        {
                            "name": "",
                            "email": "",
                        },
                    ],
                    "license": {
                        "file": "LICENSE",
                    },
                    "requires-python":
                    ">=3.11",
                    "classifiers": [
                        "Intended Audience :: Developers",
                        "Intended Audience :: Science/Research",
                        "License :: OSI Approved :: MIT License",
                        "Programming Language :: Python :: 3",
                        "Programming Language :: Python :: 3.11",
                        "Operating System :: OS Independent",
                        "Natural Language :: English",
                        "Typing :: Typed",
                    ],
                    "urls": {
                        "Homepage": "",
                        "Repository": "",
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
                            "ignore": [
                                "W291",
                                "W292",
                                "W293",
                                "E203",
                                "E701",
                            ],
                        }
                    },
                    "flake8": {
                        "max-line-length": 79,
                        "ignore": [
                            "E203",
                            "E701",
                            "W503",
                        ],
                    },
                },
            },
            "replit": {
                "run": [
                    "python",
                    "",
                ],
                "entrypoint": "",
                "modules": [
                    "python-3.11:v30-20240222-aba8eb6",
                ],
                "hidden": [
                    ".pythonlibs",
                ],
                "disableGuessImports": True,
                "disableInstallBeforeRun": True,
                "nix": {
                    "channel": "stable-23_11",
                },
                "unitTest": {
                    "language": "python3",
                },
                "deployment": {
                    "run": [
                        "python3",
                        "",
                    ],
                    "deploymentTarget": "cloudrun",
                },
                "env": {
                    "PYTHONPATH":
                    ("$PYTHONPATH:$REPL_HOME/.pythonlibs/lib/python3.11/"
                     "site-packages")
                },
                "workflows": {
                    "workflow": [
                        {
                            "name":
                            "[Package] pypi upload",
                            "mode":
                            "sequential",
                            "author":
                            0,
                            "tasks": [
                                {
                                    "task":
                                    "shell.exec",
                                    "args":
                                    ("python @@pypi_upload@@ | "
                                     "tee @@logs@@/pypi_upload.log 2>&1"),
                                },
                            ],
                        },
                        {
                            "name": "————————————————",
                            "mode": "sequential",
                            "author": 0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": ""
                                },
                            ],
                        },
                        {
                            "name":
                            "[Util] create zip",
                            "mode":
                            "sequential",
                            "author":
                            0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": "python @@create_zip@@",
                                },
                            ],
                        },
                        {
                            "name":
                            "[Util] build",
                            "mode":
                            "sequential",
                            "author":
                            0,
                            "tasks": [
                                {
                                    "task":
                                    "shell.exec",
                                    "args":
                                    ("rm -rf dist build *.egg-info && "
                                     "python setup.py sdist bdist_wheel"),
                                },
                            ],
                        },
                        {
                            "name": "————————————————",
                            "mode": "sequential",
                            "author": 0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": ""
                                },
                            ],
                        },
                        {
                            "name":
                            "[Format] ruff",
                            "mode":
                            "sequential",
                            "author":
                            0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": "ruff . format --line-length 79",
                                },
                            ],
                        },
                        {
                            "name":
                            "[Format] black",
                            "mode":
                            "sequential",
                            "author":
                            0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": "black . --line-length 79",
                                },
                            ],
                        },
                        {
                            "name":
                            "[Format] isort",
                            "mode":
                            "sequential",
                            "author":
                            0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": "isort . -l 79 -m 1",
                                },
                            ],
                        },
                        {
                            "name": "————————————————",
                            "mode": "sequential",
                            "author": 0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": ""
                                },
                            ],
                        },
                        {
                            "name":
                            "[Report] pyright",
                            "mode":
                            "sequential",
                            "author":
                            0,
                            "tasks": [
                                {
                                    "task":
                                    "shell.exec",
                                    "args": ("pyright --warnings | "
                                             "tee @@logs@@/pyright.log 2>&1"),
                                },
                            ],
                        },
                        {
                            "name":
                            "[Report] flake8",
                            "mode":
                            "sequential",
                            "author":
                            0,
                            "tasks": [
                                {
                                    "task":
                                    "shell.exec",
                                    "args":
                                    ("pflake8 --exclude */. --exclude __* | "
                                     "tee @@logs@@/flake8.log 2>&1"),
                                },
                            ],
                        },
                        {
                            "name":
                            "[Report] ruff",
                            "mode":
                            "sequential",
                            "author":
                            0,
                            "tasks": [
                                {
                                    "task":
                                    "shell.exec",
                                    "args": ("ruff check . --line-length 79 | "
                                             "tee @@logs@@/ruff.log 2>&1"),
                                },
                            ],
                        },
                        {
                            "name":
                            "[Report] black",
                            "mode":
                            "sequential",
                            "author":
                            0,
                            "tasks": [
                                {
                                    "task":
                                    "shell.exec",
                                    "args":
                                    ("black . --check --line-length 79 | "
                                     "tee @@logs@@/ruff.log 2>&1"),
                                },
                            ],
                        },
                        {
                            "name":
                            "[Report] pytest",
                            "mode":
                            "sequential",
                            "author":
                            0,
                            "tasks": [
                                {
                                    "task":
                                    "shell.exec",
                                    "args":
                                    ("pytest --cov=src --cov-report "
                                     "term-missing | tee @@logs@@/pytest.log "
                                     "2>&1"),
                                },
                            ],
                        },
                        {
                            "name":
                            "[Report] All",
                            "mode":
                            "sequential",
                            "author":
                            0,
                            "tasks": [
                                {
                                    "task":
                                    "shell.exec",
                                    "args": ("pyright --warnings | "
                                             "tee @@logs@@/pyright.log 2>&1"),
                                },
                                {
                                    "task":
                                    "shell.exec",
                                    "args":
                                    ("pflake8 --exclude */. --exclude __* | "
                                     "tee @@logs@@/flake8.log 2>&1"),
                                },
                                {
                                    "task":
                                    "shell.exec",
                                    "args": ("ruff check . --line-length 79 | "
                                             "tee @@logs@@/ruff.log 2>&1"),
                                },
                                {
                                    "task":
                                    "shell.exec",
                                    "args":
                                    ("black . --check --line-length 79 | "
                                     "tee @@logs@@/black.log 2>&1"),
                                },
                            ],
                        },
                    ]
                },
            },
            "nix":
            """
            {pkgs}: {
              deps = [
              @@@
              ];
            }
            """,
            "pypi_upload":
            '''
            """
            PyPI package upload script.
            Handles building and uploading package to PyPI with proper
            versioning and logging.
            Contains utilities for version management and package deployment.
            """

            from datetime import datetime
            from os import getenv
            from pathlib import Path
            from subprocess import CalledProcessError, run
            from sys import exit
            from textwrap import dedent
            from typing import Optional

            from replit import info
            from requests import get


            def get_latest_version(project_name) -> str:
                """Fetch the latest version from PyPI.

                Returns:
                    str: Latest version number in format 'x.y.z' or
                         '0.0.0' if not found
                """
                try:
                    return get(f"https://pypi.org/pypi/{project_name}/json"
                    ).json()["info"]["version"]
                except Exception:
                    return "0.0.0"


            def increment_version(version: str) -> str:
                """Increment the patch version number.

                Args:
                    version: Current version in format 'x.y.z'

                Returns:
                    str: Incremented version number
                """
                major, minor, patch = map(int, version.split("."))
                return f"{major}.{minor}.{patch + 1}"


            def update_version_in_files(
                new_version: str,
                pyproject_path: str,
                project_name: str,
            ) -> None:
                """Update version strings in project configuration files.

                Args:
                    new_version: Version string to set
                """
                # Update pyproject.toml
                with open(pyproject_path, "r") as f:
                    content = f.read()
                with open(pyproject_path, "w") as f:
                    f.write(content.replace(
                        f'version = "{get_latest_version(project_name)}"',
                        f'version = "{new_version}"',
                    ))

                # Update setup.py
                with open("setup.py", "r") as f:
                    content = f.read()
                with open("setup.py", "w") as f:
                    f.write(content.replace(
                        f'version="{get_latest_version(project_name)}"',
                        f'version="{new_version}"',
                    ))

            def check_token() -> str:
                """Verify PyPI token exists in environment.

                Returns:
                    str: PyPI token

                Raises:
                    SystemExit: If token is not set
                """
                token = getenv("PYPI_TOKEN")
                if not token:
                    print("Error: PYPI_TOKEN environment variable not set")
                    print(
                        "Please set it in the Secrets tab (Env Variables)"
                    )
                    exit(1)
                return token


            def create_pypirc(token: str) -> None:
                """Create PyPI configuration file with authentication.

                Args:
                    token: PyPI authentication token
                """
                pypirc_content = f"""
                [distutils]
                index-servers = pypi

                [pypi]
                username = __token__
                password = {token}
                """
                with open(str(Path.home() / ".pypirc"), "w") as f:
                    f.write(dedent(pypirc_content))


            def build_and_upload(project_dir: Optional[str] = None) -> None:
                """Build and upload package to PyPI.

                Args:
                    project_dir: Optional directory containing the project

                Raises:
                    SystemExit: If build or upload fails
                """
                working_dir = project_dir if project_dir else "."
                try:
                    print(f"Building and uploading {working_dir}...")

                    # Clean previous builds
                    run(
                        "rm -rf dist build *.egg-info",
                        shell=True,
                        cwd=working_dir,
                        check=True,
                    )

                    # Build the package
                    run(
                        ["python", "setup.py", "sdist", "bdist_wheel"],
                        cwd=working_dir,
                        check=True,
                    )

                    # Upload to PyPI
                    run(
                        ["python", "-m", "twine", "upload", "dist/*"],
                        cwd=working_dir,
                        check=True,
                    )

                    print(f"Successfully uploaded {working_dir} to PyPI!")

                except CalledProcessError as e:
                    print(f"Error during build/upload for {working_dir}: {e}")
                    exit(1)


            def main() -> None:
                """Main execution function for PyPI package upload."""
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                project_name = get(str(info.replit_id_url)).url.split("/")[-1]
                pyproject_path = "@@@"

                # Install required packages
                run(["pip", "install", "wheel", "twine", "build"], check=True)

                # Get current version and increment it
                current_version = get_latest_version(project_name)
                new_version = increment_version(current_version)
                print(
                    f"Incrementing version from {current_version} to "
                    f"{new_version}"
                )

                # Update version in files
                update_version_in_files(
                    new_version,
                    pyproject_path,
                    project_name,
                )

                # Check and setup PyPI token
                create_pypirc(check_token())

                # Build and upload directly
                build_and_upload(
                    f'{Path.home()}/{(info.replit_url or "").split("/")[-1]}'
                )
                print("Package built and uploaded successfully!")


            if __name__ == "__main__":
                main()
            ''',
            "create_zip":
            '''
            """Create a ZIP archive of the project.

            This script creates a timestamped ZIP archive of the project files,
            excluding specified directories and files.
            """

            from datetime import datetime
            from os import makedirs, path, walk
            from typing import List
            from zipfile import ZipFile


            def get_exclude_dirs() -> List[str]:
                """Get list of directories to exclude from ZIP.

                Returns:
                    List[str]: Directories to exclude
                """
                return ["build", "dist", "zip", "venv", "logs"]


            def create_zip() -> None:
                """Create ZIP archive of project files.

                Creates a timestamped ZIP file in the zip directory,
                excluding specified directories and files.
                """
                # Get current timestamp for filename
                project_name = "@@@"
                zip_path = "###"

                # Ensure zip directory exists
                if not path.exists(zip_path):
                    makedirs(zip_path)

                # Create ZIP with filtered contents
                filename = (
                    f"{zip_path}/{project_name}_"
                    f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
                )
                with ZipFile(filename, "w") as zip_file:
                    for root, dirs, files in walk("."):
                        dirs[:] = [
                            d for d in dirs
                            if d not in get_exclude_dirs()
                            and not d.startswith(".")
                            and not d.startswith("__")
                        ]
                        for file in files:
                            zip_file.write(path.join(root, file))


            if __name__ == "__main__":
                create_zip()
            ''',
            "license":
            """
            MIT License

            Copyright (c) 2024 @@@

            Permission is hereby granted, free of charge, to any person
            obtaining
            a copy of this software and associated documentation files (the
            "Software"), to deal in the Software without restriction, including
            without limitation the rights to use, copy, modify, merge, publish,
            distribute, sublicense, and/or sell copies of the Software, and to
            permit persons to whom the Software is furnished to do so,
            subject to
            the following conditions:

            The above copyright notice and this permission notice shall be
            included in all copies or substantial portions of the Software.

            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
            EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
            MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
            NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
            BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
            ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
            CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
            SOFTWARE.
            """,
        },
        "classifiers": {
            "development_status": {
                1: "Development Status :: 1 - Planning",
                2: "Development Status :: 2 - Pre-Alpha",
                3: "Development Status :: 3 - Alpha",
                4: "Development Status :: 4 - Beta",
                5: "Development Status :: 5 - Production/Stable",
                6: "Development Status :: 6 - Mature",
                7: "Development Status :: 7 - Inactive",
            },
            "topics": [
                "Topic :: Scientific/Engineering :: Artificial Intelligence",
                "Topic :: Software Development :: Libraries :: Python Modules",
                "Topic :: Text Processing :: Linguistic",
            ],
        },
        "setup": {
            "paths": {
                "pyproject": "pyproject.toml",
                "requirements": "requirements.txt",
                "replit": ".replit",
                "nix": "replit.nix",
                "readme": "README.md",
                "license": "LICENSE",
                "pypi_upload": "scripts/pypi_upload.py",
                "create_zip": "scripts/create_zip.py",
                "create_zip_folder": "zip",
                "logs_folder": "logs",
                "entrypoint": "main.py",
            },
            "classifiers": {
                "development_status": 1,
                "topics": [
                    "Python Modules",
                    "Code Generators",
                    "Debuggers",
                ],
            },
            "version":
            "0.1.1",
            "description":
            "",
            "user_config": {
                "user_name": "kairos-xx",
                "user_email": "joaoslopes@gmail.com",
                "name": "Joao Lopes",
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
                "zipfile",
            ],
            "nix_packages": [
                "pkgs.libyaml",
                "pkgs.nano",
                "pkgs.python312Full",
            ],
            "required_packages": [
                "replit",
                "requests",
                "toml",
            ],
        },
    }

    setup = project_info["setup"]
    missing_packages = check_packages(setup["required_packages"])
    print(f"Installing missing packages... {','.join(missing_packages)}")
    if missing_packages:
        install_missing_packages(missing_packages)
    print("\nAll required packages are installed!")

    user_config = setup["user_config"]
    paths = setup["paths"]
    project_info_urls = setup["urls"]
    setup_classifiers = setup["classifiers"]
    user_name = user_config["user_name"]
    user_email = user_config["user_email"]
    name = user_config["name"]
    pypi_upload_path = paths["pypi_upload"]
    pyproject_path = paths["pyproject"]
    create_zip_path = paths["create_zip"]
    create_zip_folder_path = paths["create_zip_folder"]
    logs_folder_path = paths["logs_folder"]
    license_path = paths["license"]
    entrypoint_path = paths["entrypoint"]
    templates = project_info["templates"]
    replit_dict = templates["replit"]
    pyproject_dict = templates["pyproject"]
    pyproject_dict_project = pyproject_dict["project"]
    pyproject_dict_project_classifiers = pyproject_dict_project["classifiers"]
    classifiers = project_info["classifiers"]
    topics = classifiers["topics"]
    development_status = classifiers["development_status"]
    project_name = get(
        str(info.replit_id_url),
        allow_redirects=True,
        timeout=5,
    ).url.split("/")[-1]
    replit_owner_id = getenv("REPL_OWNER_ID", "299513")
    token_base = "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"
    github_token = getenv(
        "GITHUB_TOKEN",
        f"{token_base}{token_base}",
    )

    project_info_urls["Homepage"] += f"{user_name}/{project_name}"
    project_info_urls["Repository"] += f"{user_name}/{project_name}.git"
    pyproject_dict_project["name"] = project_name
    pyproject_dict_project["readme"] = paths["readme"]
    pyproject_dict_project["license"]["file"] = license_path
    pyproject_dict_project["authors"][0]["name"] = name
    pyproject_dict_project["authors"][0]["email"] = user_email
    pyproject_dict_project["version"] = setup["version"]
    pyproject_dict_project["description"] = setup["description"]
    pyproject_dict_project["urls"] = setup["urls"]
    pyproject_dict_project_classifiers.insert(
        0,
        development_status[setup_classifiers["development_status"]],
    )
    for v in setup_classifiers["topics"]:
        topic = next(
            iter(get_close_matches(v, topics, len(topics), 0)),
            None,
        )
        if topic:
            pyproject_dict_project_classifiers.append(topic)
    for v1 in replit_dict["workflows"]["workflow"]:
        v1["author"] = int(replit_owner_id)
        for v2 in v1["tasks"]:
            v2["args"] = (v2["args"].replace(
                "@@pypi_upload@@",
                pypi_upload_path,
            ).replace(
                "@@create_zip@@",
                create_zip_path,
            ).replace("@@logs@@", logs_folder_path))

    replit_dict["run"][1] += entrypoint_path
    replit_dict["deployment"]["run"][1] += entrypoint_path
    replit_dict["entrypoint"] += entrypoint_path

    def create() -> None:
        """Create and configure project files."""
        with open(pyproject_path, "w") as f:
            toml_dump(pyproject_dict, f)
        with open(paths["replit"], "w") as f:
            toml_dump(replit_dict, f)
        with open(paths["requirements"], "w") as f:
            f.write("\n".join(setup["requirements"]))
        with open(paths["nix"], "w") as f:
            f.write(
                dedent(templates["nix"].replace(
                    "@@@",
                    "\n".join(setup["nix_packages"]),
                )))
        mkdir("/".join(pypi_upload_path.split("/")[:-1]))
        with open(pypi_upload_path, "w") as f:
            f.write(
                dedent(templates["pypi_upload"].replace(
                    "@@@",
                    pyproject_path,
                )))
        mkdir("/".join(create_zip_path.split("/")[:-1]))
        with open(create_zip_path, "w") as f:
            f.write(
                dedent(templates["create_zip"].replace(
                    "@@@",
                    project_name,
                ).replace(
                    "###",
                    create_zip_folder_path,
                )))
        with open(license_path, "w") as f:
            f.write(dedent(templates["license"].replace("@@@", name)))

        mkdir(logs_folder_path)
        open(paths["readme"], "a+").close()
        setup_github_repo(
            github_token,
            project_name,
            user_name,
            user_email,
            name,
        )


if __name__ == "__main__":
    run_all()
