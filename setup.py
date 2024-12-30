from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="tree-interval",
    version="0.1.12",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description="""A Python package for managing and
    visualizing interval tree structures""",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Joao Lopes",
    author_email="joaoslopes@gmail.com",
    url="https://github.com/kairos-xx/tree-interval",
    classifiers=[
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
        "Natural Language :: English",
        "Typing :: Typed",
        "Framework :: IPython",
        "Environment :: Console",
    ],
    python_requires=">=3.11",
    install_requires=["rich>=10.0.0"],
    keywords="tree interval visualization ast analysis debugging",
    project_urls={
        "Homepage": "https://github.com/kairos-xx/tree-interval",
        "Bug Tracker": "https://github.com/kairos-xx/tree-interval/issues",
        "Documentation": "https://github.com/kairos-xx/tree-interval/wiki",
        "Source Code": "https://github.com/kairos-xx/tree-interval",
    },
)
