#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""


# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
import io
from os import path

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


requirements = [
    "Click==7.0",
    "NBT==1.5.0",
    "progressbar2==3.39.3",
    "pyyaml>=4.2b1",
    "terminaltables==3.1.0",
    "console-menu==0.5.1",
    "anyconfig==0.9.5",
    "pyfiglet==0.7",
]

setup_requirements = []

test_requirements = ["pytest==4.4.0"]

setup(
    author="nolte",
    author_email="nolte07@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: German",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Command line utility for handle multiply git projects",
    entry_points={"console_scripts": ["mcworldmanager=mcworldmanager.cli:main"]},
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="minecraft",
    name="mcworldmanager",
    packages=find_packages(include=["mcworldmanager", "mcworldmanager.core", "mcworldmanager.report"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/nolte/minecraft-world-manager",
    version="0.1.0",
    zip_safe=False,
    include_package_data=True,
)
