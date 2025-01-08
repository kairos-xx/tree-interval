"""
Prepare a new Replit Environment
"""

from contextlib import suppress
from difflib import get_close_matches
from importlib import import_module
from os import environ, getenv
from os.path import abspath, exists
from pathlib import Path
from subprocess import CalledProcessError, run
from textwrap import dedent, indent
from typing import List, Optional, Tuple


def check_packages(
    required_packages: Optional[List[str]] = None,
) -> Tuple[str, ...]:
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
            missing_packages += (package,)
    return missing_packages


def install_missing_packages(
    packages: Optional[Tuple[str, ...]] = None,
) -> None:
    """Install packages that are missing from the environment.

    Args:
        packages: Tuple of package names to install

    Raises:
        CalledProcessError: If package installation fails
    """
    for package in packages or []:
        try:
            run(["pip", "install", package])
            print(f"Successfully installed {package}")
        except CalledProcessError as e:
            print(f"Failed to install {package}: {e}")


def setup_github_repo(
    github_token: str,
    project_name: str,
    user_name: str,
    user_email: str,
) -> None:
    """Create and configure a GitHub repository for the project.

    Args:
        github_token: GitHub authentication token
        project_name: Name of the project/repository
        user_name: GitHub username
        user_email: User's email address

    Raises:
        Exception: If repository initialization or configuration fails
    """
    try:
        # Initialize git if needed
        if not exists(".git"):
            run(["git", "init"], check=True)

        # Configure git user
        run(["git", "config", "--global", "user.name", user_name], check=True)
        run(
            ["git", "config", "--global", "user.email", user_email], check=True
        )

        # Remove existing remote if present
        try:
            run(["git", "remote", "remove", "origin"])
        except Exception as e:
            print(f"Error initializing repository: {str(e)}")

        print(f"\nGit repository initialized as '{project_name}'")
    except Exception as e:
        print(f"Error initializing repository: {str(e)}")

    try:
        from replit import db
        from requests import post

        response = post(
            "https://api.github.com/user/repos",
            headers={
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json",
            },
            json={
                "name": project_name,
                "private": False,
                "auto_init": False,
            },
        )
        if response.status_code != 201:
            print(f"Error creating repository: {response.json()}")
            repo_url_cleaned = db["GIT_URL_CLEANED"]
        else:
            response_json = response.json()
            db["GITHUB_TOKEN"] = github_token
            db["GIT_NAME"] = user_name
            db["GIT_EMAIL"] = user_email
            repo_url_cleaned = db["GIT_URL_CLEANED"] = response_json[
                "html_url"
            ]

        with suppress(Exception):
            run(["git", "stash"])
        with suppress(Exception):
            run(["git", "remote", "add", "origin", repo_url_cleaned])
        with suppress(Exception):
            run(["git", "pull", "origin", "main", "--rebase"])
        with suppress(Exception):
            run(["git", "stash", "pop"])
        with suppress(Exception):
            run(["git", "add", "origin", repo_url_cleaned])
        with suppress(Exception):
            run(["git", "add", "."])
        with suppress(Exception):
            run(["git", "commit", "-m", "Initial commit"])
        with suppress(Exception):
            run(["git", "push", "-u", "origin", "main"])
        print(f"\nRepository created and configured: {repo_url_cleaned}")
    except Exception as e:
        print(f"Error setting up repository: {str(e)}")


def get_latest_version(name: str) -> str:
    """Fetch the latest version from PyPI.
    
    Returns:
        str: Latest version number or empty string if not found
    """
    try:
        return get(f"https://pypi.org/pypi/{name}/json").json()["info"]["version"]
    except Exception:
        return ""

def run_all() -> None:
    """Execute all environment setup tasks.

    This function orchestrates the entire setup process including:
    - Loading project configuration
    - Installing required packages
    - Setting up GitHub repository
    - Configuring project files
    """
    home = "."
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
                    "name": "",
                    "version": "",
                    "description": "",
                    "readme": "README.md",
                    "authors": [
                        {
                            "name": "",
                            "email": "",
                        },
                    ],
                    "license": {
                        "file": "LICENSE",
                    },
                    "requires-python": ">=3.11",
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
                    "PYTHONPATH": (
                        "$PYTHONPATH:"
                        "$REPL_HOME/.pythonlibs/lib/python3.11/site-packages"
                    )
                },
                "workflows": {
                    "workflow": [
                        {
                            "name": "[Package] pypi upload",
                            "mode": "sequential",
                            "author": 0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": (
                                        "python @@pypi_upload@@ | "
                                        "tee @@logs@@/pypi_upload.log 2>&1"
                                    ),
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
                                    "args": "",
                                },
                            ],
                        },
                        {
                            "name": "[Util] create zip",
                            "mode": "sequential",
                            "author": 0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": "python @@create_zip@@",
                                },
                            ],
                        },
                        {
                            "name": "[Util] build",
                            "mode": "sequential",
                            "author": 0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": (
                                        "rm -rf dist build *.egg-info && "
                                        "python setup.py sdist bdist_wheel"
                                    ),
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
                                    "args": "",
                                },
                            ],
                        },
                        {
                            "name": "[Format] ruff",
                            "mode": "sequential",
                            "author": 0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": (
                                        "ruff . " "format --line-length 79"
                                    ),
                                },
                            ],
                        },
                        {
                            "name": "[Format] black",
                            "mode": "sequential",
                            "author": 0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": (
                                        "black . --exclude "
                                        "'/\\.[^/]+|/__[^/]+__$' "
                                        "--line-length 79"
                                    ),
                                },
                            ],
                        },
                        {
                            "name": "[Format] isort",
                            "mode": "sequential",
                            "author": 0,
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
                                    "args": "",
                                },
                            ],
                        },
                        {
                            "name": "[Report] pyright",
                            "mode": "sequential",
                            "author": 0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": (
                                        "pyright --warnings --project "
                                        '<(echo \'{"exclude": '
                                        '["**/.*", "**/__*__"]}\')'
                                        " | tee @@logs@@/pyright.log 2>&1"
                                    ),
                                },
                            ],
                        },
                        {
                            "name": "[Report] flake8",
                            "mode": "sequential",
                            "author": 0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": (
                                        "pflake8 --exclude '.*,__*__' | "
                                        "tee @@logs@@/flake8.log 2>&1"
                                    ),
                                },
                            ],
                        },
                        {
                            "name": "[Report] ruff",
                            "mode": "sequential",
                            "author": 0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": (
                                        "ruff check . --exclude "
                                        '"**/.*,**/__*__" --line-length 79 | '
                                        "tee @@logs@@/ruff.log 2>&1"
                                    ),
                                },
                            ],
                        },
                        {
                            "name": "[Report] black",
                            "mode": "sequential",
                            "author": 0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": (
                                        "black . --exclude "
                                        "'/\\.[^/]+|/__[^/]+__$' "
                                        "--check --line-length 79 | "
                                        "tee @@logs@@/black.log 2>&1"
                                    ),
                                },
                            ],
                        },
                        {
                            "name": "[Report] pytest",
                            "mode": "sequential",
                            "author": 0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": (
                                        "pytest --cov=@@src@@ --cov-report "
                                        "term-missing | "
                                        "tee @@logs@@/pytest.log 2>&1"
                                    ),
                                },
                            ],
                        },
                        {
                            "name": "[Report] All",
                            "mode": "sequential",
                            "author": 0,
                            "tasks": [
                                {
                                    "task": "shell.exec",
                                    "args": (
                                        "pyright --warnings --project "
                                        '<(echo \'{"exclude": ["**/.*", '
                                        '"**/__*__"]}\') | '
                                        "tee @@logs@@/pyright.log 2>&1 && "
                                        "pflake8 --exclude '.*,__*__' | "
                                        "tee @@logs@@/flake8.log 2>&1 && "
                                        "ruff check . --exclude "
                                        '"**/.*,**/__*__" '
                                        "--line-length 79 | "
                                        "tee @@logs@@/ruff.log 2>&1 && "
                                        "black . --exclude '/\\.[^/]+|"
                                        "/__[^/]+__$' "
                                        "--check --line-length 79 | "
                                        "tee @@logs@@/black.log 2>&1"
                                    ),
                                }
                            ],
                        },
                    ]
                },
            },
            "nix": """
            {pkgs}: {
              deps = [
              @@nix_packages@@
              ];
            }
            """,
            "pypi_upload": '''
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


            def get_latest_version(name) -> str:
                """Fetch the latest version from PyPI.

                Returns:
                    str: Latest version number in format 'x.y.z' or '0.0.0'
                         if not found
                """
                try:
                    return get(f"https://pypi.org/pypi/{name}/json").json()[
                        "info"
                    ]["version"]
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
                    f.write(
                        content.replace(
                            f'version = "{get_latest_version(project_name)}"',
                            f'version = "{new_version}"',
                        )
                    )

                # Update setup.py
                with open("setup.py", "r") as f:
                    content = f.read()
                with open("setup.py", "w") as f:
                    f.write(
                        content.replace(
                            f'version="{get_latest_version(project_name)}"',
                            f'version="{new_version}"',
                        )
                    )


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
                    print("Please set it in the Secrets tab (Env Variables)")
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
                project_name = "@@project_name@@"
                pyproject_path = "@@pyproject@@"

                # Install required packages
                run(["pip", "install", "wheel", "twine", "build"], check=True)

                # Get current version and increment it
                current_version = get_latest_version(project_name)
                new_version = increment_version(current_version)
                print(
                    f"Incrementing version from {current_version} to "
                    f"{new_version}"
                )

                update_version_in_files(
                    # Update version in files
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
            "create_zip": '''
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
                project_name = "@@project_name@@"
                zip_path = "@@zip_folder@@"

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
                            d
                            for d in dirs
                            if d not in get_exclude_dirs()
                            and not d.startswith(".")
                            and not d.startswith("__")
                        ]
                        for file in files:
                            zip_file.write(path.join(root, file))


            if __name__ == "__main__":
                create_zip()
            ''',
            "license": """
            MIT License

            Copyright (c) 2024 @@name@@

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
            "setup": """
            from pathlib import Path

            from setuptools import find_packages, setup

            setup(
                name="@@project_name@@",
                version="@@version@@",
                packages=find_packages(),
                install_requires=[
            @@requirements@@
                ],
                author="@@name@@s",
                author_email="@@email@@",
                description="@@description@@",
                long_description=Path('@@readme@@').read_text(),
                long_description_content_type="text/markdown",
                url="@@url@@",
                classifiers=[
            @@classifiers@@
                ],
                python_requires=">=3.11",
            )
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
                "Development Status :: 1 - Planning",
                "Development Status :: 2 - Pre-Alpha",
                "Development Status :: 3 - Alpha",
                "Development Status :: 4 - Beta",
                "Development Status :: 5 - Production/Stable",
                "Development Status :: 6 - Mature",
                "Development Status :: 7 - Inactive",
                "Environment :: Console",
                "Environment :: Console :: Curses",
                "Environment :: Console :: Framebuffer",
                "Environment :: Console :: Newt",
                "Environment :: Console :: svgalib",
                "Environment :: Handhelds/PDA's",
                "Environment :: MacOS X",
                "Environment :: MacOS X :: Aqua",
                "Environment :: MacOS X :: Carbon",
                "Environment :: MacOS X :: Cocoa",
                "Environment :: No Input/Output (Daemon)",
                "Environment :: OpenStack",
                "Environment :: Other Environment",
                "Environment :: Plugins",
                "Environment :: Web Environment",
                "Environment :: Web Environment :: Buffet",
                "Environment :: Web Environment :: Mozilla",
                "Environment :: Web Environment :: ToscaWidgets",
                "Environment :: Win32 (MS Windows)",
                "Environment :: X11 Applications",
                "Environment :: X11 Applications :: Gnome",
                "Environment :: X11 Applications :: GTK",
                "Environment :: X11 Applications :: KDE",
                "Environment :: X11 Applications :: Qt",
                "Framework :: BFG",
                "Framework :: Bob",
                "Framework :: Bottle",
                "Framework :: Buildout",
                "Framework :: Buildout :: Extension",
                "Framework :: Buildout :: Recipe",
                "Framework :: Chandler",
                "Framework :: CherryPy",
                "Framework :: CubicWeb",
                "Framework :: Django",
                "Framework :: Django :: 1.4",
                "Framework :: Django :: 1.5",
                "Framework :: Django :: 1.6",
                "Framework :: Django :: 1.7",
                "Framework :: Django :: 1.8",
                "Framework :: Django :: 1.9",
                "Framework :: Flask",
                "Framework :: IDLE",
                "Framework :: IPython",
                "Framework :: Opps",
                "Framework :: Paste",
                "Framework :: Plone",
                "Framework :: Plone :: 3.2",
                "Framework :: Plone :: 3.3",
                "Framework :: Plone :: 4.0",
                "Framework :: Plone :: 4.1",
                "Framework :: Plone :: 4.2",
                "Framework :: Plone :: 4.3",
                "Framework :: Plone :: 5.0",
                "Framework :: Pylons",
                "Framework :: Pyramid",
                "Framework :: Pytest",
                "Framework :: Review Board",
                "Framework :: Robot Framework",
                "Framework :: Scrapy",
                "Framework :: Setuptools Plugin",
                "Framework :: Sphinx",
                "Framework :: Sphinx :: Extension",
                "Framework :: Sphinx :: Theme",
                "Framework :: Trac",
                "Framework :: Tryton",
                "Framework :: TurboGears",
                "Framework :: TurboGears :: Applications",
                "Framework :: TurboGears :: Widgets",
                "Framework :: Twisted",
                "Framework :: ZODB",
                "Framework :: Zope2",
                "Framework :: Zope3",
                "Intended Audience :: Customer Service",
                "Intended Audience :: Developers",
                "Intended Audience :: Education",
                "Intended Audience :: End Users/Desktop",
                "Intended Audience :: Financial and Insurance Industry",
                "Intended Audience :: Healthcare Industry",
                "Intended Audience :: Information Technology",
                "Intended Audience :: Legal Industry",
                "Intended Audience :: Manufacturing",
                "Intended Audience :: Other Audience",
                "Intended Audience :: Religion",
                "Intended Audience :: Science/Research",
                "Intended Audience :: System Administrators",
                "Intended Audience :: Telecommunications Industry",
                "License :: Aladdin Free Public License (AFPL)",
                (
                    "License :: CC0 1.0 Universal (CC0 1.0) Public Domain"
                    + "Dedication"
                ),
                "License :: DFSG approved",
                "License :: Eiffel Forum License (EFL)",
                "License :: Free For Educational Use",
                "License :: Free For Home Use",
                "License :: Free for non-commercial use",
                "License :: Freely Distributable",
                "License :: Free To Use But Restricted",
                "License :: Freeware",
                "License :: Netscape Public License (NPL)",
                "License :: Nokia Open Source License (NOKOS)",
                "License :: OSI Approved",
                "License :: OSI Approved :: Academic Free License (AFL)",
                "License :: OSI Approved :: Apache Software License",
                "License :: OSI Approved :: Apple Public Source License",
                "License :: OSI Approved :: Artistic License",
                "License :: OSI Approved :: Attribution Assurance License",
                "License :: OSI Approved :: BSD License",
                (
                    "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre"
                    + "License, version 2.1 (CeCILL-2.1)"
                ),
                "License :: OSI Approved :: Common Public License",
                "License :: OSI Approved :: Eiffel Forum License",
                (
                    "License :: OSI Approved :: European Union Public Licence"
                    + "1.0 (EUPL 1.0)"
                ),
                (
                    "License :: OSI Approved :: European Union Public Licence"
                    + "1.1 (EUPL 1.1)"
                ),
                (
                    "License :: OSI Approved :: GNU Affero General Public"
                    + "License v3"
                ),
                (
                    "License :: OSI Approved :: GNU Affero General Public"
                    + "License v3 or later (AGPLv3+)"
                ),
                (
                    "License :: OSI Approved :: GNU Free Documentation"
                    + "License (FDL)"
                ),
                (
                    "License :: OSI Approved :: GNU General Public License"
                    + "(GPL)"
                ),
                (
                    "License :: OSI Approved :: GNU General Public License v2"
                    + "(GPLv2)"
                ),
                (
                    "License :: OSI Approved :: GNU General Public License v2"
                    + "or later (GPLv2+)"
                ),
                (
                    "License :: OSI Approved :: GNU General Public License v3"
                    + "(GPLv3)"
                ),
                (
                    "License :: OSI Approved :: GNU General Public License v3"
                    + "or later (GPLv3+)"
                ),
                (
                    "License :: OSI Approved :: GNU Lesser General Public"
                    + "License v2 (LGPLv2)"
                ),
                (
                    "License :: OSI Approved :: GNU Lesser General Public"
                    + "License v2 or later (LGPLv2+)"
                ),
                (
                    "License :: OSI Approved :: GNU Lesser General Public"
                    + "License v3 (LGPLv3)"
                ),
                (
                    "License :: OSI Approved :: GNU Lesser General Public"
                    + "License v3 or later (LGPLv3+)"
                ),
                (
                    "License :: OSI Approved :: GNU Library or Lesser General"
                    + "Public License (LGPL)"
                ),
                "License :: OSI Approved :: IBM Public License",
                "License :: OSI Approved :: Intel Open Source License",
                "License :: OSI Approved :: ISC License (ISCL)",
                "License :: OSI Approved :: Jabber Open Source License",
                "License :: OSI Approved :: MIT License",
                (
                    "License :: OSI Approved :: MITRE Collaborative Virtual"
                    + "Workspace License (CVW)"
                ),
                "License :: OSI Approved :: Motosoto License",
                (
                    "License :: OSI Approved :: Mozilla Public License 1.0"
                    + "(MPL)"
                ),
                (
                    "License :: OSI Approved :: Mozilla Public License 1.1"
                    + "(MPL 1.1)"
                ),
                (
                    "License :: OSI Approved :: Mozilla Public License 2.0"
                    + "(MPL 2.0)"
                ),
                (
                    "License :: OSI Approved :: Nethack General Public"
                    + "License"
                ),
                "License :: OSI Approved :: Nokia Open Source License",
                "License :: OSI Approved :: Open Group Test Suite License",
                (
                    "License :: OSI Approved :: Python License (CNRI Python"
                    + "License)"
                ),
                (
                    "License :: OSI Approved :: Python Software Foundation"
                    + "License"
                ),
                "License :: OSI Approved :: Qt Public License (QPL)",
                (
                    "License :: OSI Approved :: Ricoh Source Code Public"
                    + "License"
                ),
                "License :: OSI Approved :: Sleepycat License",
                (
                    "License :: OSI Approved :: Sun Industry Standards Source"
                    + "License (SISSL)"
                ),
                "License :: OSI Approved :: Sun Public License",
                (
                    "License :: OSI Approved :: University of Illinois/NCSA"
                    + "Open Source License"
                ),
                "License :: OSI Approved :: Vovida Software License 1.0",
                "License :: OSI Approved :: W3C License",
                "License :: OSI Approved :: X.Net License",
                "License :: OSI Approved :: zlib/libpng License",
                "License :: OSI Approved :: Zope Public License",
                "License :: Other/Proprietary License",
                "License :: Public Domain",
                "License :: Repoze Public License",
                "Natural Language :: Afrikaans",
                "Natural Language :: Arabic",
                "Natural Language :: Bengali",
                "Natural Language :: Bosnian",
                "Natural Language :: Bulgarian",
                "Natural Language :: Cantonese",
                "Natural Language :: Catalan",
                "Natural Language :: Chinese (Simplified)",
                "Natural Language :: Chinese (Traditional)",
                "Natural Language :: Croatian",
                "Natural Language :: Czech",
                "Natural Language :: Danish",
                "Natural Language :: Dutch",
                "Natural Language :: English",
                "Natural Language :: Esperanto",
                "Natural Language :: Finnish",
                "Natural Language :: French",
                "Natural Language :: Galician",
                "Natural Language :: German",
                "Natural Language :: Greek",
                "Natural Language :: Hebrew",
                "Natural Language :: Hindi",
                "Natural Language :: Hungarian",
                "Natural Language :: Icelandic",
                "Natural Language :: Indonesian",
                "Natural Language :: Italian",
                "Natural Language :: Japanese",
                "Natural Language :: Javanese",
                "Natural Language :: Korean",
                "Natural Language :: Latin",
                "Natural Language :: Latvian",
                "Natural Language :: Macedonian",
                "Natural Language :: Malay",
                "Natural Language :: Marathi",
                "Natural Language :: Norwegian",
                "Natural Language :: Panjabi",
                "Natural Language :: Persian",
                "Natural Language :: Polish",
                "Natural Language :: Portuguese",
                "Natural Language :: Portuguese (Brazilian)",
                "Natural Language :: Romanian",
                "Natural Language :: Russian",
                "Natural Language :: Serbian",
                "Natural Language :: Slovak",
                "Natural Language :: Slovenian",
                "Natural Language :: Spanish",
                "Natural Language :: Swedish",
                "Natural Language :: Tamil",
                "Natural Language :: Telugu",
                "Natural Language :: Thai",
                "Natural Language :: Turkish",
                "Natural Language :: Ukranian",
                "Natural Language :: Urdu",
                "Natural Language :: Vietnamese",
                "Operating System :: Android",
                "Operating System :: BeOS",
                "Operating System :: iOS",
                "Operating System :: MacOS",
                "Operating System :: MacOS :: MacOS 9",
                "Operating System :: MacOS :: MacOS X",
                "Operating System :: Microsoft",
                "Operating System :: Microsoft :: MS-DOS",
                "Operating System :: Microsoft :: Windows",
                (
                    "Operating System :: Microsoft :: Windows :: Windows 3.1"
                    + "or Earlier"
                ),
                "Operating System :: Microsoft :: Windows :: Windows 7",
                (
                    "Operating System :: Microsoft :: Windows :: Windows"
                    + "95/98/2000"
                ),
                "Operating System :: Microsoft :: Windows :: Windows CE",
                (
                    "Operating System :: Microsoft :: Windows :: Windows"
                    + "NT/2000"
                ),
                (
                    "Operating System :: Microsoft :: Windows :: Windows"
                    + "Server 2003"
                ),
                (
                    "Operating System :: Microsoft :: Windows :: Windows"
                    + "Server 2008"
                ),
                (
                    "Operating System :: Microsoft :: Windows :: Windows"
                    + "Vista"
                ),
                "Operating System :: Microsoft :: Windows :: Windows XP",
                "Operating System :: OS/2",
                "Operating System :: OS Independent",
                "Operating System :: Other OS",
                "Operating System :: PalmOS",
                "Operating System :: PDA Systems",
                "Operating System :: POSIX",
                "Operating System :: POSIX :: AIX",
                "Operating System :: POSIX :: BSD",
                "Operating System :: POSIX :: BSD :: BSD/OS",
                "Operating System :: POSIX :: BSD :: FreeBSD",
                "Operating System :: POSIX :: BSD :: NetBSD",
                "Operating System :: POSIX :: BSD :: OpenBSD",
                "Operating System :: POSIX :: GNU Hurd",
                "Operating System :: POSIX :: HP-UX",
                "Operating System :: POSIX :: IRIX",
                "Operating System :: POSIX :: Linux",
                "Operating System :: POSIX :: Other",
                "Operating System :: POSIX :: SCO",
                "Operating System :: POSIX :: SunOS/Solaris",
                "Operating System :: Unix",
                "Programming Language :: Ada",
                "Programming Language :: APL",
                "Programming Language :: ASP",
                "Programming Language :: Assembly",
                "Programming Language :: Awk",
                "Programming Language :: Basic",
                "Programming Language :: C",
                "Programming Language :: C#",
                "Programming Language :: C++",
                "Programming Language :: Cold Fusion",
                "Programming Language :: Cython",
                "Programming Language :: Delphi/Kylix",
                "Programming Language :: Dylan",
                "Programming Language :: Eiffel",
                "Programming Language :: Emacs-Lisp",
                "Programming Language :: Erlang",
                "Programming Language :: Euler",
                "Programming Language :: Euphoria",
                "Programming Language :: Forth",
                "Programming Language :: Fortran",
                "Programming Language :: Haskell",
                "Programming Language :: Java",
                "Programming Language :: JavaScript",
                "Programming Language :: Lisp",
                "Programming Language :: Logo",
                "Programming Language :: ML",
                "Programming Language :: Modula",
                "Programming Language :: Objective C",
                "Programming Language :: Object Pascal",
                "Programming Language :: OCaml",
                "Programming Language :: Other",
                "Programming Language :: Other Scripting Engines",
                "Programming Language :: Pascal",
                "Programming Language :: Perl",
                "Programming Language :: PHP",
                "Programming Language :: Pike",
                "Programming Language :: Pliant",
                "Programming Language :: PL/SQL",
                "Programming Language :: PROGRESS",
                "Programming Language :: Prolog",
                "Programming Language :: Python",
                "Programming Language :: Python :: 2",
                "Programming Language :: Python :: 2.3",
                "Programming Language :: Python :: 2.4",
                "Programming Language :: Python :: 2.5",
                "Programming Language :: Python :: 2.6",
                "Programming Language :: Python :: 2.7",
                "Programming Language :: Python :: 2 :: Only",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.0",
                "Programming Language :: Python :: 3.1",
                "Programming Language :: Python :: 3.2",
                "Programming Language :: Python :: 3.3",
                "Programming Language :: Python :: 3.4",
                "Programming Language :: Python :: 3.5",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3 :: Only",
                "Programming Language :: Python :: Implementation",
                (
                    "Programming Language :: Python :: Implementation ::"
                    + "CPython"
                ),
                (
                    "Programming Language :: Python :: Implementation ::"
                    + "IronPython"
                ),
                (
                    "Programming Language :: Python :: Implementation ::"
                    + "Jython"
                ),
                "Programming Language :: Python :: Implementation :: PyPy",
                (
                    "Programming Language :: Python :: Implementation ::"
                    + "Stackless"
                ),
                "Programming Language :: REBOL",
                "Programming Language :: Rexx",
                "Programming Language :: Ruby",
                "Programming Language :: Scheme",
                "Programming Language :: Simula",
                "Programming Language :: Smalltalk",
                "Programming Language :: SQL",
                "Programming Language :: Tcl",
                "Programming Language :: Unix Shell",
                "Programming Language :: Visual Basic",
                "Programming Language :: XBasic",
                "Programming Language :: YACC",
                "Programming Language :: Zope",
                "Topic :: Adaptive Technologies",
                "Topic :: Artistic Software",
                "Topic :: Communications",
                "Topic :: Communications :: BBS",
                "Topic :: Communications :: Chat",
                "Topic :: Communications :: Chat :: AOL Instant Messenger",
                "Topic :: Communications :: Chat :: ICQ",
                "Topic :: Communications :: Chat :: Internet Relay Chat",
                "Topic :: Communications :: Chat :: Unix Talk",
                "Topic :: Communications :: Conferencing",
                "Topic :: Communications :: Email",
                "Topic :: Communications :: Email :: Address Book",
                "Topic :: Communications :: Email :: Email Clients (MUA)",
                "Topic :: Communications :: Email :: Filters",
                "Topic :: Communications :: Email :: Mailing List Servers",
                (
                    "Topic :: Communications :: Email :: Mail Transport"
                    + "Agents"
                ),
                "Topic :: Communications :: Email :: Post-Office",
                "Topic :: Communications :: Email :: Post-Office :: IMAP",
                "Topic :: Communications :: Email :: Post-Office :: POP3",
                "Topic :: Communications :: Fax",
                "Topic :: Communications :: FIDO",
                "Topic :: Communications :: File Sharing",
                "Topic :: Communications :: File Sharing :: Gnutella",
                "Topic :: Communications :: File Sharing :: Napster",
                "Topic :: Communications :: Ham Radio",
                "Topic :: Communications :: Internet Phone",
                "Topic :: Communications :: Telephony",
                "Topic :: Communications :: Usenet News",
                "Topic :: Database",
                "Topic :: Database :: Database Engines/Servers",
                "Topic :: Database :: Front-Ends",
                "Topic :: Desktop Environment",
                "Topic :: Desktop Environment :: File Managers",
                "Topic :: Desktop Environment :: Gnome",
                "Topic :: Desktop Environment :: GNUstep",
                (
                    "Topic :: Desktop Environment :: K Desktop Environment"
                    + "(KDE)"
                ),
                (
                    "Topic :: Desktop Environment :: K Desktop Environment"
                    + "(KDE) :: Themes"
                ),
                "Topic :: Desktop Environment :: PicoGUI",
                "Topic :: Desktop Environment :: PicoGUI :: Applications",
                "Topic :: Desktop Environment :: PicoGUI :: Themes",
                "Topic :: Desktop Environment :: Screen Savers",
                "Topic :: Desktop Environment :: Window Managers",
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Afterstep"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Afterstep :: Themes"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Applets"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Blackbox"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Blackbox :: Themes"
                ),
                "Topic :: Desktop Environment :: Window Managers :: CTWM",
                (
                    "Topic :: Desktop Environment :: Window Managers :: CTWM"
                    + ":: Themes"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Enlightenment"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Enlightenment :: Epplets"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Enlightenment :: Themes DR15"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Enlightenment :: Themes DR16"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Enlightenment :: Themes DR17"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Fluxbox"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Fluxbox :: Themes"
                ),
                "Topic :: Desktop Environment :: Window Managers :: FVWM",
                (
                    "Topic :: Desktop Environment :: Window Managers :: FVWM"
                    + ":: Themes"
                ),
                "Topic :: Desktop Environment :: Window Managers :: IceWM",
                (
                    "Topic :: Desktop Environment :: Window Managers :: IceWM"
                    + ":: Themes"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "MetaCity"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "MetaCity :: Themes"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Oroborus"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Oroborus :: Themes"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Sawfish"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Sawfish :: Themes 0.30"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Sawfish :: Themes pre-0.30"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Waimea"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Waimea :: Themes"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Window Maker"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Window Maker :: Applets"
                ),
                (
                    "Topic :: Desktop Environment :: Window Managers ::"
                    + "Window Maker :: Themes"
                ),
                "Topic :: Desktop Environment :: Window Managers :: XFCE",
                (
                    "Topic :: Desktop Environment :: Window Managers :: XFCE"
                    + ":: Themes"
                ),
                "Topic :: Documentation",
                "Topic :: Documentation :: Sphinx",
                "Topic :: Education",
                "Topic :: Education :: Computer Aided Instruction (CAI)",
                "Topic :: Education :: Testing",
                "Topic :: Games/Entertainment",
                "Topic :: Games/Entertainment :: Arcade",
                "Topic :: Games/Entertainment :: Board Games",
                "Topic :: Games/Entertainment :: First Person Shooters",
                "Topic :: Games/Entertainment :: Fortune Cookies",
                (
                    "Topic :: Games/Entertainment :: Multi-User Dungeons"
                    + "(MUD)"
                ),
                "Topic :: Games/Entertainment :: Puzzle Games",
                "Topic :: Games/Entertainment :: Real Time Strategy",
                "Topic :: Games/Entertainment :: Role-Playing",
                (
                    "Topic :: Games/Entertainment :: Side-Scrolling/Arcade"
                    + "Games"
                ),
                "Topic :: Games/Entertainment :: Simulation",
                "Topic :: Games/Entertainment :: Turn Based Strategy",
                "Topic :: Home Automation",
                "Topic :: Internet",
                "Topic :: Internet :: File Transfer Protocol (FTP)",
                "Topic :: Internet :: Finger",
                "Topic :: Internet :: Log Analysis",
                "Topic :: Internet :: Name Service (DNS)",
                "Topic :: Internet :: Proxy Servers",
                "Topic :: Internet :: WAP",
                "Topic :: Internet :: WWW/HTTP",
                "Topic :: Internet :: WWW/HTTP :: Browsers",
                "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
                (
                    "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI"
                    + "Tools/Libraries"
                ),
                (
                    "Topic :: Internet :: WWW/HTTP :: Dynamic Content ::"
                    + "Message Boards"
                ),
                (
                    "Topic :: Internet :: WWW/HTTP :: Dynamic Content ::"
                    + "News/Diary"
                ),
                (
                    "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Page"
                    + "Counters"
                ),
                "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
                "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
                "Topic :: Internet :: WWW/HTTP :: Session",
                "Topic :: Internet :: WWW/HTTP :: Site Management",
                (
                    "Topic :: Internet :: WWW/HTTP :: Site Management :: Link"
                    + "Checking"
                ),
                "Topic :: Internet :: WWW/HTTP :: WSGI",
                "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
                "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
                "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
                "Topic :: Internet :: Z39.50",
                "Topic :: Multimedia",
                "Topic :: Multimedia :: Graphics",
                "Topic :: Multimedia :: Graphics :: 3D Modeling",
                "Topic :: Multimedia :: Graphics :: 3D Rendering",
                "Topic :: Multimedia :: Graphics :: Capture",
                (
                    "Topic :: Multimedia :: Graphics :: Capture :: Digital"
                    + "Camera"
                ),
                "Topic :: Multimedia :: Graphics :: Capture :: Scanners",
                (
                    "Topic :: Multimedia :: Graphics :: Capture :: Screen"
                    + "Capture"
                ),
                "Topic :: Multimedia :: Graphics :: Editors",
                (
                    "Topic :: Multimedia :: Graphics :: Editors :: Raster-"
                    + "Based"
                ),
                (
                    "Topic :: Multimedia :: Graphics :: Editors :: Vector-"
                    + "Based"
                ),
                "Topic :: Multimedia :: Graphics :: Graphics Conversion",
                "Topic :: Multimedia :: Graphics :: Presentation",
                "Topic :: Multimedia :: Graphics :: Viewers",
                "Topic :: Multimedia :: Sound/Audio",
                "Topic :: Multimedia :: Sound/Audio :: Analysis",
                "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
                "Topic :: Multimedia :: Sound/Audio :: CD Audio",
                (
                    "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD"
                    + "Playing"
                ),
                (
                    "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD"
                    + "Ripping"
                ),
                (
                    "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD"
                    + "Writing"
                ),
                "Topic :: Multimedia :: Sound/Audio :: Conversion",
                "Topic :: Multimedia :: Sound/Audio :: Editors",
                "Topic :: Multimedia :: Sound/Audio :: MIDI",
                "Topic :: Multimedia :: Sound/Audio :: Mixers",
                "Topic :: Multimedia :: Sound/Audio :: Players",
                "Topic :: Multimedia :: Sound/Audio :: Players :: MP3",
                "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
                "Topic :: Multimedia :: Sound/Audio :: Speech",
                "Topic :: Multimedia :: Video",
                "Topic :: Multimedia :: Video :: Capture",
                "Topic :: Multimedia :: Video :: Conversion",
                "Topic :: Multimedia :: Video :: Display",
                "Topic :: Multimedia :: Video :: Non-Linear Editor",
                "Topic :: Office/Business",
                "Topic :: Office/Business :: Financial",
                "Topic :: Office/Business :: Financial :: Accounting",
                "Topic :: Office/Business :: Financial :: Investment",
                "Topic :: Office/Business :: Financial :: Point-Of-Sale",
                "Topic :: Office/Business :: Financial :: Spreadsheet",
                "Topic :: Office/Business :: Groupware",
                "Topic :: Office/Business :: News/Diary",
                "Topic :: Office/Business :: Office Suites",
                "Topic :: Office/Business :: Scheduling",
                "Topic :: Other/Nonlisted Topic",
                "Topic :: Printing",
                "Topic :: Religion",
                "Topic :: Scientific/Engineering",
                (
                    "Topic :: Scientific/Engineering :: Artificial"
                    + "Intelligence"
                ),
                "Topic :: Scientific/Engineering :: Artificial Life",
                "Topic :: Scientific/Engineering :: Astronomy",
                "Topic :: Scientific/Engineering :: Atmospheric Science",
                "Topic :: Scientific/Engineering :: Bio-Informatics",
                "Topic :: Scientific/Engineering :: Chemistry",
                (
                    "Topic :: Scientific/Engineering :: Electronic Design"
                    + "Automation (EDA)"
                ),
                "Topic :: Scientific/Engineering :: GIS",
                (
                    "Topic :: Scientific/Engineering :: Human Machine"
                    + "Interfaces"
                ),
                "Topic :: Scientific/Engineering :: Image Recognition",
                "Topic :: Scientific/Engineering :: Information Analysis",
                (
                    "Topic :: Scientific/Engineering :: Interface"
                    + "Engine/Protocol Translator"
                ),
                "Topic :: Scientific/Engineering :: Mathematics",
                "Topic :: Scientific/Engineering :: Medical Science Apps.",
                "Topic :: Scientific/Engineering :: Physics",
                "Topic :: Scientific/Engineering :: Visualization",
                "Topic :: Security",
                "Topic :: Security :: Cryptography",
                "Topic :: Sociology",
                "Topic :: Sociology :: Genealogy",
                "Topic :: Sociology :: History",
                "Topic :: Software Development",
                "Topic :: Software Development :: Assemblers",
                "Topic :: Software Development :: Bug Tracking",
                "Topic :: Software Development :: Build Tools",
                "Topic :: Software Development :: Code Generators",
                "Topic :: Software Development :: Compilers",
                "Topic :: Software Development :: Debuggers",
                "Topic :: Software Development :: Disassemblers",
                "Topic :: Software Development :: Documentation",
                "Topic :: Software Development :: Embedded Systems",
                "Topic :: Software Development :: Internationalization",
                "Topic :: Software Development :: Interpreters",
                "Topic :: Software Development :: Libraries",
                (
                    "Topic :: Software Development :: Libraries ::"
                    + "Application Frameworks"
                ),
                (
                    "Topic :: Software Development :: Libraries :: Java"
                    + "Libraries"
                ),
                (
                    "Topic :: Software Development :: Libraries :: Perl"
                    + "Modules"
                ),
                (
                    "Topic :: Software Development :: Libraries :: PHP"
                    + "Classes"
                ),
                (
                    "Topic :: Software Development :: Libraries :: Pike"
                    + "Modules"
                ),
                "Topic :: Software Development :: Libraries :: pygame",
                (
                    "Topic :: Software Development :: Libraries :: Python"
                    + "Modules"
                ),
                (
                    "Topic :: Software Development :: Libraries :: Ruby"
                    + "Modules"
                ),
                (
                    "Topic :: Software Development :: Libraries :: Tcl"
                    + "Extensions"
                ),
                "Topic :: Software Development :: Localization",
                "Topic :: Software Development :: Object Brokering",
                (
                    "Topic :: Software Development :: Object Brokering ::"
                    + "CORBA"
                ),
                "Topic :: Software Development :: Pre-processors",
                "Topic :: Software Development :: Quality Assurance",
                "Topic :: Software Development :: Testing",
                (
                    "Topic :: Software Development :: Testing :: Traffic"
                    + "Generation"
                ),
                "Topic :: Software Development :: User Interfaces",
                "Topic :: Software Development :: Version Control",
                "Topic :: Software Development :: Version Control :: CVS",
                "Topic :: Software Development :: Version Control :: RCS",
                "Topic :: Software Development :: Version Control :: SCCS",
                "Topic :: Software Development :: Widget Sets",
                "Topic :: System",
                "Topic :: System :: Archiving",
                "Topic :: System :: Archiving :: Backup",
                "Topic :: System :: Archiving :: Compression",
                "Topic :: System :: Archiving :: Mirroring",
                "Topic :: System :: Archiving :: Packaging",
                "Topic :: System :: Benchmark",
                "Topic :: System :: Boot",
                "Topic :: System :: Boot :: Init",
                "Topic :: System :: Clustering",
                "Topic :: System :: Console Fonts",
                "Topic :: System :: Distributed Computing",
                "Topic :: System :: Emulators",
                "Topic :: System :: Filesystems",
                "Topic :: System :: Hardware",
                "Topic :: System :: Hardware :: Hardware Drivers",
                "Topic :: System :: Hardware :: Mainframes",
                (
                    "Topic :: System :: Hardware :: Symmetric Multi-"
                    + "processing"
                ),
                "Topic :: System :: Installation/Setup",
                "Topic :: System :: Logging",
                "Topic :: System :: Monitoring",
                "Topic :: System :: Networking",
                "Topic :: System :: Networking :: Firewalls",
                "Topic :: System :: Networking :: Monitoring",
                (
                    "Topic :: System :: Networking :: Monitoring :: Hardware"
                    + "Watchdog"
                ),
                "Topic :: System :: Networking :: Time Synchronization",
                "Topic :: System :: Operating System",
                "Topic :: System :: Operating System Kernels",
                "Topic :: System :: Operating System Kernels :: BSD",
                "Topic :: System :: Operating System Kernels :: GNU Hurd",
                "Topic :: System :: Operating System Kernels :: Linux",
                "Topic :: System :: Power (UPS)",
                "Topic :: System :: Recovery Tools",
                "Topic :: System :: Shells",
                "Topic :: System :: Software Distribution",
                "Topic :: System :: Systems Administration",
                (
                    "Topic :: System :: Systems Administration ::"
                    + "Authentication/Directory"
                ),
                (
                    "Topic :: System :: Systems Administration ::"
                    + "Authentication/Directory :: LDAP"
                ),
                (
                    "Topic :: System :: Systems Administration ::"
                    + "Authentication/Directory :: NIS"
                ),
                "Topic :: System :: System Shells",
                "Topic :: Terminals",
                "Topic :: Terminals :: Serial",
                "Topic :: Terminals :: Telnet",
                "Topic :: Terminals :: Terminal Emulators/X Terminals",
                "Topic :: Text Editors",
                "Topic :: Text Editors :: Documentation",
                "Topic :: Text Editors :: Emacs",
                (
                    "Topic :: Text Editors :: Integrated Development"
                    + "Environments (IDE)"
                ),
                "Topic :: Text Editors :: Text Processing",
                "Topic :: Text Editors :: Word Processors",
                "Topic :: Text Processing",
                "Topic :: Text Processing :: Filters",
                "Topic :: Text Processing :: Fonts",
                "Topic :: Text Processing :: General",
                "Topic :: Text Processing :: Indexing",
                "Topic :: Text Processing :: Linguistic",
                "Topic :: Text Processing :: Markup",
                "Topic :: Text Processing :: Markup :: HTML",
                "Topic :: Text Processing :: Markup :: LaTeX",
                "Topic :: Text Processing :: Markup :: SGML",
                "Topic :: Text Processing :: Markup :: VRML",
                "Topic :: Text Processing :: Markup :: XML",
            ],
        },
        # Setup configuration for project initialization and management
        "setup": {
            # File path configurations for project structure
            "paths": {
                "pyproject": "pyproject.toml",  # Python project configuration
                "requirements": "requirements.txt",  # Python dependencies
                "replit": ".replit",  # Replit IDE configuration
                "nix": "replit.nix",  # Nix environment setup
                "readme": "README.md",  # Project documentation
                "license": "LICENSE",  # Project license
                "current_script": "scripts/prepare_environment.py",
                # This script
                "pypi_upload": "scripts/pypi_upload.py",  # PyPI upload utility
                "create_zip": "scripts/create_zip.py",  # Archive creator
                "create_zip_folder": "zip",  # Archive storage
                "logs_folder": "logs",  # Log file storage
                "entrypoint": "main.py",  # Project entry point
                "source_folder": "src",  # Source code directory
                "setup": "setup.py",  # Package setup file
                "replit_id_url": (  # Replit project ID API
                    "https://replit-info.replit.app/" + "get?title&replit_id="
                ),
            },
            # PyPI project classifiers configuration
            "classifiers": {
                "development_status": 1,  # Planning stage
                "topics": [  # Project categories
                    "Python Modules",
                    "Code Generators",
                    "Debuggers",
                ],
            },
            "version": get_latest_version(project_name) or "0.1.1",  # Project version
            "description": "",  # Project description
            # User and maintainer information
            "user_config": {
                "user_name": "username",  # GitHub username
                "user_email": "email@email.com",  # Contact email
                "name": "Author name",  # Full name
            },
            # Project repository URLs
            "urls": {
                "Homepage": "https://github.com/",  # Project homepage
                "Repository": "https://github.com/",  # Source repository
            },
            # Python package dependencies
            "requirements": [
                "pytest>=7.0.0",  # Testing framework
                "pytest",
                "replit==4.1.0",  # Replit integration
                "black",  # Code formatter
                "flake8",  # Code linter
                "build",  # Package builder
                "requests",  # HTTP client
                "pyright",  # Type checker
                "toml",  # TOML parser
                "pyyaml",  # YAML parser
                "isort",  # Import sorter
                "pyproject-flake8",  # Modern flake8
                "zipfile38==0.0.3",  # Archive handling
            ],
            # Nix environment package requirements
            "nix_packages": [
                "pkgs.libyaml",  # YAML library
                "pkgs.ruff",  # Fast Python linter
                "pkgs.nano",  # Text editor
                "pkgs.python312Full",  # Python runtime
            ],
            # Essential setup packages
            "required_packages": [
                "replit",  # Replit integration
                "requests",  # HTTP client
                "toml",  # TOML parser
            ],
        },
    }

    setup = project_info["setup"]
    missing_packages = check_packages(setup["required_packages"])
    print(f"Installing missing packages... {','.join(missing_packages)}")
    if missing_packages:
        install_missing_packages(missing_packages)
    print("\nAll required packages are installed!")

    from replit import info
    from requests import get
    from toml import dump

    user_config = setup["user_config"]
    paths = setup["paths"]
    project_info_urls = setup["urls"]
    setup_classifiers = setup["classifiers"]
    description = setup["description"]
    requirements = setup["requirements"]
    version = setup["version"]
    user_name = user_config["user_name"]
    user_email = user_config["user_email"]
    name = user_config["name"]
    pypi_upload_path = paths["pypi_upload"]
    pyproject_path = paths["pyproject"]
    create_zip_path = paths["create_zip"]
    create_zip_folder_path = paths["create_zip_folder"]
    logs_folder_path = paths["logs_folder"]
    current_script_path = paths["current_script"]
    license_path = paths["license"]
    entrypoint_path = paths["entrypoint"]
    source_folder_path = paths["source_folder"]
    requirements_path = paths["requirements"]
    readme_path = paths["readme"]
    replit_id_url = paths["replit_id_url"]
    templates = project_info["templates"]
    replit_dict = templates["replit"]
    pyproject_dict = templates["pyproject"]
    pyproject_dict_project = pyproject_dict["project"]
    pyproject_dict_project_classifiers = pyproject_dict_project["classifiers"]
    classifiers = project_info["classifiers"]
    topics = classifiers["topics"]
    development_status = classifiers["development_status"]

    response = get(replit_id_url + info.id)
    project_name = response.text.replace('"', "").replace("\n", "")
    replit_owner_id = getenv("REPL_OWNER_ID", "")
    if "GITHUB_TOKEN" not in environ:
        raise ValueError(
            "GITHUB_TOKEN environment variable is not set."
            + "Please set it to your GitHub personal access token."
        )
    if "REPLIT_TOKEN" not in environ:
        raise ValueError(
            "REPLIT_TOKEN environment variable is not set."
            + "Please set it to your Replit token."
        )
    github_token = getenv("GITHUB_TOKEN", "")
    homepage = project_info_urls["Homepage"]
    homepage += f"{user_name}/{project_name}"
    project_info_urls["Homepage"] += f"{user_name}/{project_name}.git"
    project_info_urls["Repository"] += f"{user_name}/{project_name}.git"
    pyproject_dict_project["name"] = project_name
    pyproject_dict_project["readme"] = readme_path
    pyproject_dict_project["license"]["file"] = license_path
    pyproject_dict_project["authors"][0]["name"] = name
    pyproject_dict_project["authors"][0]["email"] = user_email
    pyproject_dict_project["version"] = version
    pyproject_dict_project["description"] = description
    pyproject_dict_project["urls"] = setup["urls"]
    pyproject_dict_project_classifiers.insert(
        0, development_status[setup_classifiers["development_status"]]
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
            v2["args"] = (
                v2["args"]
                .replace("@@pypi_upload@@", pypi_upload_path)
                .replace("@@create_zip@@", create_zip_path)
                .replace("@@logs@@", logs_folder_path)
                .replace("@@src@@", source_folder_path)
            )

    replit_dict["run"][1] += entrypoint_path
    replit_dict["deployment"]["run"][1] += entrypoint_path
    replit_dict["entrypoint"] += entrypoint_path

    def create() -> None:
        """Create and configure project files."""
        with open(f"{home}/{pyproject_path}", "w") as f:
            dump(pyproject_dict, f)
        with open(f'{home}/{paths["replit"]}', "w") as f:
            dump(replit_dict, f)
        with open(f"{home}/{requirements_path}", "w") as f:
            f.write("\n".join(requirements))
        missing_packages = check_packages(requirements)
        print(f"Installing missing packages... {','.join(missing_packages)}")
        if missing_packages:
            install_missing_packages(missing_packages)
        print("\nAll required packages are installed!")

        with open(f'{home}/{paths["nix"]}', "w") as f:
            nix_data = dedent(templates["nix"]).replace(
                "@@nix_packages@@", "\n  ".join(setup["nix_packages"])
            )
            f.write(nix_data)
        with open(f'{home}/{paths["setup"]}', "w") as f:
            setup_content = (
                dedent(templates["setup"])
                .replace(
                    "@@requirements@@",
                    indent(
                        ",\n".join(f"'{v}'" for v in requirements),
                        "        ",
                    ),
                )
                .replace("@@project_name@@", project_name)
                .replace("@@name@@", name)
                .replace("@@version@@", version)
                .replace("@@email@@", user_email)
                .replace("@@description@@", description)
                .replace("@@readme@@", readme_path)
                .replace("@@url@@", homepage)
                .replace(
                    "@@classifiers@@",
                    indent(
                        ",\n".join(
                            f"'{v}'"
                            for v in pyproject_dict_project_classifiers
                        ),
                        "        ",
                    ),
                )
            )
            f.write(setup_content)
        Path(f"{home}/{pypi_upload_path}").parent.mkdir(
            parents=True, exist_ok=True
        )
        with open(f"{home}/{pypi_upload_path}", "w") as f:
            f.write(
                dedent(
                    templates["pypi_upload"]
                    .replace("@@project_name@@", project_name)
                    .replace("@@pyproject@@", pyproject_path)
                )
            )
        Path(f"{home}/{create_zip_path}").parent.mkdir(
            parents=True, exist_ok=True
        )
        with open(f"{home}/{create_zip_path}", "w") as f:
            f.write(
                dedent(
                    templates["create_zip"]
                    .replace("@@project_name@@", project_name)
                    .replace("@@zip_folder@@", create_zip_folder_path)
                )
            )
        with open(f"{home}/{license_path}", "w") as f:
            f.write(dedent(templates["license"].replace("@@name@@", name)))
        Path(f"{home}/{logs_folder_path}").mkdir(parents=True, exist_ok=True)
        Path(f"{home}/{source_folder_path}").mkdir(parents=True, exist_ok=True)
        open(f"{home}/{readme_path}", "a+").close()

    create()
    setup_github_repo(
        github_token,
        project_name,
        user_name,
        user_email,
    )
    with suppress(Exception):
        Path(abspath(__file__)).rename(f"{home}/{current_script_path}")


if __name__ == "__main__":
    run_all()
