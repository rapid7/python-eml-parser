#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="python_eml_parser",
    version="1.0.0",
    description="Rapid7 InsightConnect email parser for email plugins",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rapid7 Integrations Alliance",
    author_email="integrationalliance@rapid7.com",
    url="https://github.com/rapid7/python-eml-parser",
    packages=find_packages(),
    install_requires=[],
    entry_points={"console_scripts": ["eml-parser=eml_parser.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
    license="MIT",
)
