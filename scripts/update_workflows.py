"""Update workflows configuration."""

import subprocess

try:
    author_id = int(
        subprocess.check_output(["python", "scripts/get_author.py"]).strip())
except Exception:
    author_id = 299513

workflows = [
    {
        "name":
        "[Package] pypi upload",
        "mode":
        "sequential",
        "author":
        author_id,
        "tasks": [{
            "task":
            "shell.exec",
            "args":
            "python scripts/pypi_upload.py | tee logs/pypi_upload.log 2>&1"
        }],
    },
    {
        "name":
        "[Package] git commit",
        "mode":
        "sequential",
        "author":
        author_id,
        "tasks": [{
            "task":
            "shell.exec",
            "args":
            "python scripts/git_commit.py | tee logs/git_commit.log 2>&1"
        }],
    },
    {
        "name": "————————————————",
        "mode": "sequential",
        "author": author_id,
        "tasks": [{
            "task": "shell.exec",
            "args": ""
        }],
    },
    {
        "name": "[Util] create zip",
        "mode": "sequential",
        "author": author_id,
        "tasks": [{
            "task": "shell.exec",
            "args": "python scripts/create_zip.py"
        }],
    },
    {
        "name":
        "[Util] build",
        "mode":
        "sequential",
        "author":
        author_id,
        "tasks": [{
            "task":
            "shell.exec",
            "args":
            "rm -rf dist build *.egg-info && python setup.py sdist bdist_wheel"
        }],
    },
    {
        "name":
        "[Util] tests",
        "mode":
        "sequential",
        "author":
        author_id,
        "tasks": [{
            "task": "shell.exec",
            "args": "pytest ./tests | tee logs/tests.log 2>&1"
        }],
    },
    {
        "name":
        "[Util] demo",
        "mode":
        "sequential",
        "author":
        author_id,
        "tasks": [{
            "task": "shell.exec",
            "args": "python -m examples | tee logs/demo.log 2>&1"
        }],
    },
    {
        "name":
        "[Util] update workflows",
        "mode":
        "sequential",
        "author":
        author_id,
        "tasks": [{
            "task":
            "shell.exec",
            "args": ("python scripts/update_workflows.py | tee " +
                     "logs/update_worflows.log 2>&1")
        }],
    },
    {
        "name": "————————————————",
        "mode": "sequential",
        "author": author_id,
        "tasks": [{
            "task": "shell.exec",
            "args": ""
        }],
    },
    {
        "name": "[Format] ruff",
        "mode": "sequential",
        "author": author_id,
        "tasks": [{
            "task": "shell.exec",
            "args": "ruff format"
        }],
    },
    {
        "name": "————————————————",
        "mode": "sequential",
        "author": author_id,
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
        author_id,
        "tasks": [{
            "task": "shell.exec",
            "args": "pyright --warnings | tee logs/pyright.log 2>&1"
        }],
    },
    {
        "name":
        "[Report] flake8",
        "mode":
        "sequential",
        "author":
        author_id,
        "tasks": [{
            "task":
            "shell.exec",
            "args":
            "flake8 --exclude */. --exclude ./build | tee logs/flake8.log 2>&1"
        }],
    },
    {
        "name":
        "[Report] ruff",
        "mode":
        "sequential",
        "author":
        author_id,
        "tasks": [{
            "task":
            "shell.exec",
            "args": ("ruff check ./dev ./src ./examples ./tests ./scripts | " +
                     "tee logs/ruff.log 2>&1")
        }],
    },
    {
        "name":
        "[Report] pytest",
        "mode":
        "sequential",
        "author":
        author_id,
        "tasks": [{
            "task": "shell.exec",
            "args": "pytest --cov=src | tee logs/pytest.log 2>&1"
        }],
    },
    {
        "name":
        "[Report] All",
        "mode":
        "sequential",
        "author":
        author_id,
        "tasks": [{
            "task":
            "shell.exec",
            "args": ("pyright --warnings | tee logs/pyright.log 2>&1 && " +
                     "flake8 --exclude */. --exclude ./build | " +
                     "tee logs/flake8.log 2>&1 && " +
                     "ruff check ./dev ./src ./examples ./tests ./scripts | " +
                     "tee logs/ruff.log 2>&1")
        }],
    },
]
