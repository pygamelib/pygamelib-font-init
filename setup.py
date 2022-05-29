import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

DIR = os.path.dirname(os.path.abspath(__file__))
INSTALL_PACKAGES = open(os.path.join(DIR, "requirements.txt")).read().splitlines()

print(INSTALL_PACKAGES)

setuptools.setup(
    name="pygamelib-font-init",
    version="0.1.0",
    author="Arnaud Dupuis",
    author_email="8bitscoding@gmail.com",
    description="A script to easily initialize a new font for the pygamelib.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=INSTALL_PACKAGES,
    url="https://www.pygamelib.org",
    packages=setuptools.find_packages(),
    scripts=["pygamelib-font-init.py"],
    keywords=["development", "console", "terminal", "font"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Environment :: Console",
        "Topic :: Terminals",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Documentation": "https://github.com/pygamelib/pygamelib-font-init",
        "Source": "https://github.com/pygamelib/pygamelib-font-init",
        "Tracker": "https://github.com/pygamelib/pygamelib-font-init/issues",
    },
    python_requires=">=3.6",
)
