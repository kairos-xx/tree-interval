
from setuptools import setup, find_packages

setup(
    name="tree-visualizer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description="A Python package for building and visualizing tree structures",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Replit User",
    author_email="user@example.com",
    url="https://github.com/user/tree-visualizer",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[],
)
