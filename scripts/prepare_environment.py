"""GitHub Actions workflow update script.

Updates GitHub Actions workflow files with new configurations.
"""

from importlib import import_module
from json import dumps as json_dumps
from json import loads as json_loads
from subprocess import CalledProcessError, run
from typing import Any, Dict, List, Tuple

from toml import dump as toml_dump
from toml import dumps as toml_dumps
from toml import load as toml_load
from yaml import load as yaml_load
from yaml import safe_load


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


def update_workflows() -> None:
    required_packages = ("toml", "yaml")
    project_info = {
        "paths": {
            "pyproject": "pyproject.toml",
            "requirements": "requirements.txt",
            "replit": "replit.txt",
        },
        "templates": {
            "pyproject": {
                "build-system": {
                    "requires": ["setuptools>=45", "wheel"],
                    "build-backend": "setuptools.build_meta",
                },
                "project": {
                    "name": "tree-",
                    "version": "",
                    "description": "",
                    "readme": "README.md",
                    "authors": [{
                        "name": "Joao Lopes",
                        "email": "joaoslopes@gmail.com"
                    }],
                    "license": {"file": "LICENSE"},
                    "requires-python": ">=3.11",
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
                        "Homepage": (
                            "https://github.com/kairos-xx/tree-interval"
                        ),
                        "Repository": (
                            "https://github.com/kairos-xx/tree-interval.git"
                        ),
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
                "run": ["python", "main.py"],
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
                    "run": ["python3", "main.py"],
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
                                "python scripts/pypi_upload.py | tee logs/pypi_upload.log 2>&1",
                            }],
                        },
                        {
                            "name":
                            "\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014",
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
                                "rm -rf dist build *.egg-info && python  setup.py sdist bdist_wheel",
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
                                "pytest ./tests | tee logs/tests.log 2>&1",
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
                                "python scripts/update_workflows.py | tee logs/update_worflows.log 2>&1",
                            }],
                        },
                        {
                            "name":
                            "\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014",
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
                            "name":
                            "\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014",
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
                                "pyright --warnings | tee logs/pyright.log 2>&1",
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
                                "pflake8 --exclude */. --exclude ./build  | tee logs/flake8.log 2>&1",
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
                                "ruff check ./dev ./src ./examples ./tests ./scripts  | tee logs/ruff.log 2>&1",
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
                                "pytest --cov=src --cov-report term-missing | tee logs/pytest.log 2>&1",
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
                                "pyright --warnings | tee logs/pyright.log 2>&1 && pflake8 --exclude */. --exclude ./build | tee logs/flake8.log 2>&1 && ruff check ./dev ./src ./examples ./tests ./scripts | tee logs/ruff.log 2>&1",
                            }],
                        },
                    ]
                },
            },
        },
        "name":
        "tree-interval",
        "version":
        "0.1.1",
        "description":
        "A Python package for managing and visualizing interval tree structures",
        "urls": {
            "Homepage": "https://github.com/kairos-xx/tree-interval",
            "Repository": "https://github.com/kairos-xx/tree-interval.git",
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
        "main.py"
    }

    pyproject_dict = project_info["templates"]["pyproject"]
    pyproject_dict["project"]["name"] = project_info["name"]
    pyproject_dict["project"]["version"] = project_info["version"]
    pyproject_dict["project"]["description"] = project_info["description"]
    pyproject_dict["project"]["urls"] = project_info["urls"]
    # requirements_text = "\n".join(project_info["requirements"])
    # with open(project_info["paths"]["pyproject"], "w") as f:
    #     toml_dump(pyproject_dict, f)
    # with open(project_info["paths"]["requirements"], "w") as f:
    #     f.write(requirements_text)

    # missing_packages = check_packages(required_packages)
    # if missing_packages:
    #     print("\nInstalling missing packages...")
    #     install_missing_packages(missing_packages)
    # else:
    #     print("\nAll required packages are installed!")

    # replit_dict = project_info["templates"]["replit"]
    # replit_dict["run"][1] = replit_dict["deployment"][1] = replit_dict[
    #     "entrypoint"] = project_info["entrypoint"]

    # with open(".replit", "r") as f:
    #     replit_config = toml_load(f)
    #     print(json_dumps(replit_config, indent=4))
    from replit import info
    print(dir(info),info.co_url,info.id_co_url)


# with open(pyproject_path, "rb") as f:

# pyproject_path = "pyproject.toml"
# requirements_path = "requirements.txt"

# # Write updated workflow file
# with open(pyproject_path, "rb") as f:
#     p = toml_load(f)
# print(json_dumps(p, indent=3))

# # Log update
# with open("logs/update_worflows.log", "a") as log:
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     log.write(f"\nWorkflow updated at {timestamp}\n")

if __name__ == "__main__":
    update_workflows()
