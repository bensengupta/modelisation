# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

with open("LICENSE", "r") as f:
    license = f.read()

setup(
    name="modelisation",
    version="0.1.0",
    description="Simplifie la construction de graphiques",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Benjamin Sengupta",
    author_email="benjamin.sengupta@gmail.com",
    license=license,
    packages=find_packages(exclude=("tests")),
    # url="https://github.com/kennethreitz/samplemod",
)
