import toml
from get_author import get_repl_author

# Read existing .replit file
try:
    with open('.replit', 'r') as f:
        config = toml.load(f)
except Exception:
    config = {}

# Initialize workflows if not exists
if 'workflows' not in config:
    config['workflows'] = {'workflow': []}

# Get author ID dynamically
author_id = get_repl_author() or 299513  # Fallback to existing ID if API fails



# Define workflows to check
required_workflows = [
    {
        'name': '————————————————',
        'mode': 'sequential',
        'author': author_id,
        'tasks': [{'task': 'shell.exec', 'args': ''}]
    },
    {
        'name': '[Util] create zip',
        'mode': 'sequential',
        'author': author_id,
        'tasks': [{'task': 'shell.exec', 'args': 'python scripts/create_zip.py'}]
    },
    {
        'name': '[Util] build',
        'mode': 'sequential',
        'author': author_id,
        'tasks': [{'task': 'shell.exec', 'args': 'rm -rf dist build *.egg-info && python  setup.py sdist bdist_wheel'}]
    },
    {
        'name': '[Util] tests',
        'mode': 'sequential',
        'author': author_id,
        'tasks': [{'task': 'shell.exec', 'args': 'pytest ./tests | tee logs/tests.log 2>&1'}]
    },
    {
        'name': '[Util] update workflows',
        'mode': 'sequential',
        'author': author_id,
        'tasks': [{'task': 'shell.exec', 'args': 'python scripts/update_workflows.py | tee logs/update_worflows.log 2>&1'}]
    },
    {
        'name': '————————————————',
        'mode': 'sequential',
        'author': author_id,
        'tasks': [{'task': 'shell.exec', 'args': ''}]
    },
    {
        'name': '[Format] ruff',
        'mode': 'sequential',
        'author': author_id,
        'tasks': [{'task': 'shell.exec', 'args': 'ruff format'}]
    },
    {
        'name': '————————————————',
        'mode': 'sequential',
        'author': author_id,
        'tasks': [{'task': 'shell.exec', 'args': ''}]
    },
    {
        'name': '[Report] pyright',
        'mode': 'sequential',
        'author': author_id,
        'tasks': [{'task': 'shell.exec', 'args': 'pyright --warnings | tee logs/pyright.log 2>&1'}]
    },
    {
        'name': '[Report] flake8',
        'mode': 'sequential',
        'author': author_id,
        'tasks': [{'task': 'shell.exec', 'args': 'flake8 --exclude */. --exclude ./build  | tee logs/flake8.log 2>&1'}]
    },
    {
        'name': '[Report] ruff',
        'mode': 'sequential',
        'author': author_id,
        'tasks': [{'task': 'shell.exec', 'args': 'ruff check ./src  | tee logs/ruff.log 2>&1'}]
    }
}, {
    'name':
    '[Util] create zip',
    'mode':
    'sequential',
    'author':
    author_id,
    'tasks': [{
        'task': 'shell.exec',
        'args': 'python scripts/create_zip.py'
    }]
}, {
    'name':
    '[Util] build',
    'mode':
    'sequential',
    'author':
    author_id,
    'tasks': [{
        'task':
        'shell.exec',
        'args':
        'rm -rf dist build *.egg-info && python  setup.py sdist bdist_wheel'
    }]
}, {
    'name':
    '[Run] tests',
    'mode':
    'sequential',
    'author':
    author_id,
    'tasks': [{
        'task': 'shell.exec',
        'args': 'pytest ./tests | tee logs/tests.log 2>&1'
    }]
}, {
    'name':
    '[Report] pyright',
    'mode':
    'sequential',
    'author':
    author_id,
    'tasks': [{
        'task': 'shell.exec',
        'args': 'pyright --warnings | tee logs/pyright.log 2>&1'
    }]
}, {
    'name':
    '[Report] flake8',
    'mode':
    'sequential',
    'author':
    author_id,
    'tasks': [{
        'task':
        'shell.exec',
        'args':
        'flake8 --exclude */. --exclude ./build  | tee logs/flake8.log 2>&1'
    }]
}, {
    'name':
    '[Report] ruff',
    'mode':
    'sequential',
    'author':
    author_id,
    'tasks': [{
        'task': 'shell.exec',
        'args': 'ruff check ./src  | tee logs/ruff.log 2>&1'
    }]
}]

# Add missing workflows
existing_names = {w['name'] for w in config['workflows'].get('workflow', [])}
for workflow in required_workflows:
    if workflow['name'] not in existing_names:
        if 'workflow' not in config['workflows']:
            config['workflows']['workflow'] = []
        config['workflows']['workflow'].append(workflow)
        print(f"Added workflow: {workflow['name']}")

# Write updated config
with open('.replit', 'w') as f:
    toml.dump(config, f)
print("Workflows updated successfully!")
