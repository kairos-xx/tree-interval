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
required_workflows = []

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
