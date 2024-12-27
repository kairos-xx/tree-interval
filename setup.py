from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    readme = fh.read()
setup(
    name="tree-interval",
    version="0.1.7",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description="A Python package for managing and visualizing "
    + "interval tree structures",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Joao Lopes",
    author_email="joaoslopes@gmail.com",
    url="https://github.com/kairos-xx/tree-interval",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=["rich>=10.0.0"],
)
