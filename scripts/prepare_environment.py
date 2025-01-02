"""GitHub Actions workflow update script.
Updates GitHub Actions workflow files with new configurations.
"""

from difflib import get_close_matches
from importlib import import_module
from json import dumps as json_dumps
from os import environ, getenv, mkdir
from os.path import exists
from pathlib import Path
from subprocess import CalledProcessError, run
from textwrap import dedent
from typing import List, Tuple

from replit import db, info
from requests import get, post
from toml import dump as toml_dump


def check_packages(required_packages: List) -> Tuple:
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


def setup_github_repo(github_token, project_name, user_name, user_email,
                      name) -> None:
    """Create and configure GitHub repository."""
    try:
        if not exists(".git"):
            run(
                [
                    "git",
                    "init",
                ],
                check=True,
            )
        run(
            [
                "git",
                "config",
                "--global",
                "user.name",
                user_name,
            ],
            check=True,
        )
        run(
            [
                "git",
                "config",
                "--global",
                "user.email",
                user_email,
            ],
            check=True,
        )
        print(f"\nGit repository initialized as '{project_name}'")
    except Exception as e:
        print(f"Error initializing repository: {str(e)}")
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
            "https://", f"https://{github_token}@")

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


def run_all() -> None:

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
                            0,
                            "tasks": [
                                {
                                    "task":
                                    "shell.exec",
                                    "args":
                                    "python @@pypi_upload@@ | " +
                                    "tee @@logs@@/pypi_upload.log 2>&1",
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
                                    "rm -rf dist build *.egg-info && " +
                                    "python setup.py sdist bdist_wheel",
                                },
                            ],
                        },
                        {
                            "name": "————————————————",
                            "mode": "sequential",
                            "author": 299513,
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
                                    "args":
                                    "ruff . " + "format --line-length 79",
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
                            "author": 299513,
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
                                    "args":
                                    "pyright --warnings | " +
                                    "tee @@logs@@/pyright.log 2>&1",
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
                                    "pflake8 --exclude */. " +
                                    "--exclude __*  | " +
                                    "tee @@logs@@/flake8.log 2>&1",
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
                                    "args":
                                    "ruff check . " + "--line-length 79 | " +
                                    "tee @@logs@@/ruff.log 2>&1",
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
                                    "black . --check " +
                                    "--line-length 79 | " +
                                    "tee @@logs@@/ruff.log 2>&1",
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
                                    "pytest --cov=src --cov-report term-missing | "
                                    + "tee @@logs@@/pytest.log 2>&1",
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
                                    "args":
                                    "pyright --warnings | " +
                                    "tee @@logs@@/pyright.log 2>&1"
                                },
                                {
                                    "task":
                                    "shell.exec",
                                    "args":
                                    "pflake8 --exclude */. " +
                                    "--exclude __* | " +
                                    "tee @@logs@@/flake8.log 2>&1"
                                },
                                {
                                    "task":
                                    "shell.exec",
                                    "args":
                                    "ruff check . " + "--line-length 79 | " +
                                    "tee @@logs@@/ruff.log 2>&1",
                                },
                                {
                                    "task":
                                    "shell.exec",
                                    "args":
                                    "black . --check " +
                                    "--line-length 79 | " +
                                    "tee @@logs@@/black.log 2>&1",
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
            """PyPI package upload script.   
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
                    return get(f"https://pypi.org/pypi/{project_name}/json").json(
                    )["info"]["version"]
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


            def update_version_in_files(new_version: str, pyproject_path: str,
                                        project_name: str) -> None:
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
                        ))

                # Update setup.py
                with open("setup.py", "r") as f:
                    content = f.read()
                with open("setup.py", "w") as f:
                    f.write(
                        content.replace(f'version="{get_latest_version(project_name)}"',
                                        f'version="{new_version}"'))

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
                    print("Please set it in the Secrets tab (Environment Variables)")
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
                print(f"Incrementing version from {current_version} to {new_version}")

                # Update version in files
                update_version_in_files(new_version, pyproject_path, project_name)

                # Check and setup PyPI token
                create_pypirc(check_token())

                # Build and upload directly
                build_and_upload(f'{Path.home()}/{(info.replit_url or "").split("/")[-1]}')
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
                with ZipFile(
                        f"{zip_path}/" + f"{project_name}_" +
                        f'{datetime.now().strftime("%Y%m%d_%H%M%S")}' + ".zip",
                        "w",
                ) as zip_file:
                    for root, dirs, files in walk("."):
                        dirs[:] = [
                            d for d in dirs if d not in get_exclude_dirs()
                            and not d.startswith(".") and not d.startswith("__")
                        ]
                        for file in files:
                            zip_file.write(path.join(root, file))


            if __name__ == "__main__":
                create_zip()
            '''
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
                "Topic :: Communications :: Email :: Mail Transport Agents",
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
                "Topic :: Desktop Environment :: K Desktop Environment (KDE)",
                "Topic :: Desktop Environment :: K Desktop Environment (KDE) :: Themes",
                "Topic :: Desktop Environment :: PicoGUI",
                "Topic :: Desktop Environment :: PicoGUI :: Applications",
                "Topic :: Desktop Environment :: PicoGUI :: Themes",
                "Topic :: Desktop Environment :: Screen Savers",
                "Topic :: Desktop Environment :: Window Managers",
                "Topic :: Desktop Environment :: Window Managers :: Afterstep",
                "Topic :: Desktop Environment :: Window Managers :: Afterstep :: Themes",
                "Topic :: Desktop Environment :: Window Managers :: Applets",
                "Topic :: Desktop Environment :: Window Managers :: Blackbox",
                "Topic :: Desktop Environment :: Window Managers :: Blackbox :: Themes",
                "Topic :: Desktop Environment :: Window Managers :: CTWM",
                "Topic :: Desktop Environment :: Window Managers :: CTWM :: Themes",
                "Topic :: Desktop Environment :: Window Managers :: Enlightenment",
                "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Epplets",
                "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR15",
                "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR16",
                "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR17",
                "Topic :: Desktop Environment :: Window Managers :: Fluxbox",
                "Topic :: Desktop Environment :: Window Managers :: Fluxbox :: Themes",
                "Topic :: Desktop Environment :: Window Managers :: FVWM",
                "Topic :: Desktop Environment :: Window Managers :: FVWM :: Themes",
                "Topic :: Desktop Environment :: Window Managers :: IceWM",
                "Topic :: Desktop Environment :: Window Managers :: IceWM :: Themes",
                "Topic :: Desktop Environment :: Window Managers :: MetaCity",
                "Topic :: Desktop Environment :: Window Managers :: MetaCity :: Themes",
                "Topic :: Desktop Environment :: Window Managers :: Oroborus",
                "Topic :: Desktop Environment :: Window Managers :: Oroborus :: Themes",
                "Topic :: Desktop Environment :: Window Managers :: Sawfish",
                "Topic :: Desktop Environment :: Window Managers :: Sawfish :: Themes 0.30",
                "Topic :: Desktop Environment :: Window Managers :: Sawfish :: Themes pre-0.30",
                "Topic :: Desktop Environment :: Window Managers :: Waimea",
                "Topic :: Desktop Environment :: Window Managers :: Waimea :: Themes",
                "Topic :: Desktop Environment :: Window Managers :: Window Maker",
                "Topic :: Desktop Environment :: Window Managers :: Window Maker :: Applets",
                "Topic :: Desktop Environment :: Window Managers :: Window Maker :: Themes",
                "Topic :: Desktop Environment :: Window Managers :: XFCE",
                "Topic :: Desktop Environment :: Window Managers :: XFCE :: Themes",
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
                "Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)",
                "Topic :: Games/Entertainment :: Puzzle Games",
                "Topic :: Games/Entertainment :: Real Time Strategy",
                "Topic :: Games/Entertainment :: Role-Playing",
                "Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games",
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
                "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
                "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards",
                "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
                "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Page Counters",
                "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
                "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
                "Topic :: Internet :: WWW/HTTP :: Session",
                "Topic :: Internet :: WWW/HTTP :: Site Management",
                "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
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
                "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera",
                "Topic :: Multimedia :: Graphics :: Capture :: Scanners",
                "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
                "Topic :: Multimedia :: Graphics :: Editors",
                "Topic :: Multimedia :: Graphics :: Editors :: Raster-Based",
                "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
                "Topic :: Multimedia :: Graphics :: Graphics Conversion",
                "Topic :: Multimedia :: Graphics :: Presentation",
                "Topic :: Multimedia :: Graphics :: Viewers",
                "Topic :: Multimedia :: Sound/Audio",
                "Topic :: Multimedia :: Sound/Audio :: Analysis",
                "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
                "Topic :: Multimedia :: Sound/Audio :: CD Audio",
                "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Playing",
                "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Ripping",
                "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Writing",
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
                "Topic :: Scientific/Engineering :: Artificial Intelligence",
                "Topic :: Scientific/Engineering :: Artificial Life",
                "Topic :: Scientific/Engineering :: Astronomy",
                "Topic :: Scientific/Engineering :: Atmospheric Science",
                "Topic :: Scientific/Engineering :: Bio-Informatics",
                "Topic :: Scientific/Engineering :: Chemistry",
                "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
                "Topic :: Scientific/Engineering :: GIS",
                "Topic :: Scientific/Engineering :: Human Machine Interfaces",
                "Topic :: Scientific/Engineering :: Image Recognition",
                "Topic :: Scientific/Engineering :: Information Analysis",
                "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
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
                "Topic :: Software Development :: Libraries :: Application Frameworks",
                "Topic :: Software Development :: Libraries :: Java Libraries",
                "Topic :: Software Development :: Libraries :: Perl Modules",
                "Topic :: Software Development :: Libraries :: PHP Classes",
                "Topic :: Software Development :: Libraries :: Pike Modules",
                "Topic :: Software Development :: Libraries :: pygame",
                "Topic :: Software Development :: Libraries :: Python Modules",
                "Topic :: Software Development :: Libraries :: Ruby Modules",
                "Topic :: Software Development :: Libraries :: Tcl Extensions",
                "Topic :: Software Development :: Localization",
                "Topic :: Software Development :: Object Brokering",
                "Topic :: Software Development :: Object Brokering :: CORBA",
                "Topic :: Software Development :: Pre-processors",
                "Topic :: Software Development :: Quality Assurance",
                "Topic :: Software Development :: Testing",
                "Topic :: Software Development :: Testing :: Traffic Generation",
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
                "Topic :: System :: Hardware :: Symmetric Multi-processing",
                "Topic :: System :: Installation/Setup",
                "Topic :: System :: Logging",
                "Topic :: System :: Monitoring",
                "Topic :: System :: Networking",
                "Topic :: System :: Networking :: Firewalls",
                "Topic :: System :: Networking :: Monitoring",
                "Topic :: System :: Networking :: Monitoring :: Hardware Watchdog",
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
                "Topic :: System :: Systems Administration :: Authentication/Directory",
                "Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP",
                "Topic :: System :: Systems Administration :: Authentication/Directory :: NIS",
                "Topic :: System :: System Shells",
                "Topic :: Terminals",
                "Topic :: Terminals :: Serial",
                "Topic :: Terminals :: Telnet",
                "Topic :: Terminals :: Terminal Emulators/X Terminals",
                "Topic :: Text Editors",
                "Topic :: Text Editors :: Documentation",
                "Topic :: Text Editors :: Emacs",
                "Topic :: Text Editors :: Integrated Development Environments (IDE)",
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
                "Topic :: Utilities",
            ],
        },
        "setup": {
            "paths": {
                "pyproject": "pyproject.toml",
                "requirements": "requirements.txt",
                "replit": ".replit",
                "nix": "replit.nix",
                "readme": "README.md",
                "pypi_upload": "scripts/pypi_upload.py",
                "create_zip": "scripts/create_zip.py",
                "create_zip_folder": "zip",
                "logs_folder": "logs",
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
            "descriptors": [
                "",
            ],
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
                "pytest>=7.0.0", "pytest", "replit==4.1.0", "black", "flake8",
                "build", "requests", "toml", "pyyaml", "isort", "zipfile"
            ],
            "entrypoint":
            "main.py",
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

    a=get(str(info.replit_id_url),allow_redirects=True)
    

    
   
    project_name = a.url.split("/")[-1]
    replit_owner_id = getenv("REPL_OWNER_ID", "299513")
    github_token = getenv(
        "GITHUB_TOKEN",
        "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ghp" +
        "_jMChfQ9izNyKLdJd9M46VTTOfZDTGV2r2CfY",
    )
    
    
    print(project_name)
    homedir = Path.home()
    homedir = str(homedir).replace("\\", "/")

    try:
        __sid__ = open(f"{homedir}/repl-cli/connect.sid", "r").read().strip()
    except:
        __sid__ = None
        
    print(__sid__,get(f"https://replit.com/data/repls/@kairos").content,homedir)

    setup = project_info["setup"]
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
    templates = project_info["templates"]
    replit_dict = templates["replit"]
    pyproject_dict = templates["pyproject"]
    pyproject_dict_project = pyproject_dict["project"]
    pyproject_dict_project_classifiers = pyproject_dict_project["classifiers"]
    classifiers = project_info["classifiers"]
    topics = classifiers["topics"]
    development_status = classifiers["development_status"]

    project_info_urls["Homepage"] += f"{user_name}/{project_name}"
    project_info_urls["Repository"] += f"{user_name}/{project_name}.git"
    pyproject_dict["name"] = project_name
    pyproject_dict_project["authors"][0]["name"] = name
    pyproject_dict_project["authors"][0]["email"] = user_email
    pyproject_dict_project["version"] = setup["version"]
    pyproject_dict_project["description"] = setup["description"]
    pyproject_dict_project["urls"] = setup["urls"]
    pyproject_dict_project_classifiers.insert(
        0, development_status[setup_classifiers["development_status"]])

    for v in setup_classifiers["topics"]:
        topic = next(iter(get_close_matches(v, topics, len(topics), 0)), None)
        if topic:
            pyproject_dict_project_classifiers.append(topic)
    for v1 in replit_dict["workflows"]["workflow"]:
        v1["author"] = int(replit_owner_id)
        for v2 in v1["tasks"]:
            v2["args"] = v2["args"].replace(
                "@@pypi_upload@@", pypi_upload_path).replace(
                    "@@create_zip@@",
                    create_zip_path).replace("@@logs@@", logs_folder_path)
    entry_point = setup["entrypoint"]
    replit_dict["run"][1] += entry_point
    replit_dict["deployment"]["run"][1] += entry_point
    replit_dict["entrypoint"] += entry_point


    def create():
        missing_packages = check_packages(setup["required_packages"])
        print(f"Installing missing packages... {','.join(missing_packages)}")
        if missing_packages:
            install_missing_packages(missing_packages)
        print("\nAll required packages are installed!")

        with open(pyproject_path, "w") as f:
            toml_dump(pyproject_dict, f)
        with open(paths["replit"], "w") as f:
            toml_dump(replit_dict, f)
        with open(paths["requirements"], "w") as f:
            f.write("\n".join(setup["requirements"]))
        with open(paths["nix"], "w") as f:
            f.write(
                dedent(templates["nix"].replace(
                    "@@@", "\n".join(setup["nix_packages"]))))
        mkdir("/".join(pypi_upload_path.split("/")[:-1]))
        with open(pypi_upload_path, "w") as f:
            f.write(
                dedent(templates["pypi_upload"].replace("@@@",
                                                        pyproject_path)))
        mkdir("/".join(create_zip_path.split("/")[:-1]))
        with open(create_zip_path, "w") as f:
            f.write(
                dedent(templates["create_zip"].replace(
                    "@@@", project_name).replace("###",
                                                 create_zip_folder_path)))

        mkdir(logs_folder_path)
        open(paths["readme"], "a+").close()
        setup_github_repo(github_token, project_name, user_name, user_email,
                          name)


if __name__ == "__main__":
    #print(open("scripts/pypi_upload.py").read())
    run_all()
