from setuptools import find_packages, setup

setup(
    name="tree-interval",
    version="0.1.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description="A Python package for managing and visualizing "
    + "interval tree structures",
    long_description=open("README.md").read(),
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
