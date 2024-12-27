
import os
import subprocess

def run_publish_workflow():
    """Run the publish workflow programmatically"""
    try:
        # Build package
        subprocess.run(["python", "-m", "build"], check=True)
        
        # Build wheel
        subprocess.run(["python", "setup.py", "sdist", "bdist_wheel"], check=True)
        
        print("Package built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running workflow: {e}")
        return False
