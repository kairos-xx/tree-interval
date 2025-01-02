"""GitHub Actions workflow update script.

Updates GitHub Actions workflow files with new configurations.
"""

from json import dumps as json_dumps
from json import loads as json_loads
from typing import Any, Dict

from toml import dump as toml_dump
from toml import dumps as toml_dumps
from toml import load as toml_load
from yaml import load as yaml_load
from yaml import safe_load


def load_workflow_config() -> Dict[str, Any]:
    """Load workflow configuration from YAML.

    Returns:
        Dict[str, Any]: Workflow configuration
    """
    config = {
        "name": "Python Package",
        "on": ["push", "pull_request"],
        "jobs": {
            "build": {
                "runs-on":
                "ubuntu-latest",
                "steps": [
                    {
                        "uses": "actions/checkout@v2"
                    },
                    {
                        "name": "Set up Python",
                        "uses": "actions/setup-python@v2",
                        "with": {
                            "python-version": "3.x"
                        },
                    },
                    {
                        "name": "Install dependencies",
                        "run": "pip install -r requirements.txt",
                    },
                    {
                        "name": "Run tests",
                        "run": "pytest"
                    },
                ],
            }
        },
    }
    return config


def update_workflows() -> None:

    # run pip install toml, yaml
    project_info = {
        "paths": {
            "pyproject": "pyproject.toml",
            "requirements": "requirements.txt"
        },
        "templates": {
            "pyproject": {
                "build-system": {
                    "requires": ["setuptools>=45", "wheel"],
                    "build-backend": "setuptools.build_meta"
                },
                "project": {
                    "name":
                    "tree-",
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
                        "Topic :: Software Development :: Libraries :: Python Modules",
                        "Topic :: Software Development :: Code Generators",
                        "Topic :: Software Development :: Debuggers",
                        "Operating System :: OS Independent",
                        "Natural Language :: English", "Typing :: Typed"
                    ],
                    "urls": {
                        "Homepage":
                        "https://github.com/kairos-xx/tree-interval",
                        "Repository":
                        "https://github.com/kairos-xx/tree-interval.git"
                    }
                },
                "tool": {
                    "ruff": {
                        "lint": {
                            "select":
                            ["E", "W", "F", "I", "B", "C4", "ARG", "SIM"],
                            "ignore": ["W291", "W292", "W293", "E203", "E701"]
                        }
                    },
                    "flake8": {
                        "max-line-length": 79,
                        "ignore": ["E203", "E701", "W503"]
                    }
                }
            }
        },
        "name":
        "tree-interval",
        "version":
        "0.1.22",
        "description":
        "A Python package for managing and visualizing interval tree structures",
        "urls": {
            "Homepage": "https://github.com/kairos-xx/tree-interval",
            "Repository": "https://github.com/kairos-xx/tree-interval.git"
        },
        "requirements": [
            "pytest>=7.0.0", "pytest", "replit==4.1.0", "black", "flake8",
            "build", "requests", "toml", "pyyaml", "isort"
        ]
    }

    pyproject_dict = project_info["templates"]["pyproject"]
    pyproject_dict["project"]["name"] = project_info["name"]
    pyproject_dict["project"]["version"] = project_info["version"]
    pyproject_dict["project"]["description"] = project_info["description"]
    pyproject_dict["project"]["urls"] = project_info["urls"]
    requirements_text = "\n".join(project_info["requirements"])
    with open(project_info["paths"]["pyproject"], "w") as f:
        toml_dump(pyproject_dict, f)
    with open(project_info["paths"]["requirements"], "w") as f:
        f.write(requirements_text)


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
