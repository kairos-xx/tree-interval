<<<<<<< HEAD
=======

>>>>>>> 151f403bd09e889cfadedf4c57cd8af99003b1b7
from setuptools import find_packages, setup

setup(
    name="tree-interval",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description="A Python package for managing and visualizing interval tree structures",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Joao Lopes",
<<<<<<< HEAD
    author_email="joaoslopes@gmail.com",
=======
    author_email="joaslopes@gmail.com",
>>>>>>> 151f403bd09e889cfadedf4c57cd8af99003b1b7
    url="https://github.com/kairos-xx/tree-interval",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
<<<<<<< HEAD
    install_requires=["rich>=10.0.0"],
=======
    install_requires=[
        "rich>=10.0.0"
    ],
>>>>>>> 151f403bd09e889cfadedf4c57cd8af99003b1b7
)
