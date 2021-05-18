# Cloud Helper  
Library of helper tools to interact with cloud resources.

## Installation
To install the most recent version of the package in another projects, run
```
$ pip install -e git://github.com/jina-ai/cloud-helper.git#egg=jinacld_tools
```
If you want to use a specific version tag, run
```
$ pip install -e git://github.com/jina-ai/cloud-helper.git@0.0.1#egg=jinacld_tools 
```

## Developer Quickstart Guide

## Developer Installation
To install the project in editable mode run:
```
$ pip install -e .
```
To get the development requirements run:
```
$ pip install -e .[test]
```

### Pre-Commit Hooks
This project uses [black](https://black.readthedocs.io/en/stable/) and [isort](https://pycqa.github.io/isort/) for consistent
code formatting. [pre-commit](https://pre-commit.com/) configuration files are available in the repository to run these
tools as a Git pre-commit hook - simply run the following command after cloning the repo to set it up:

```
$ pip install pre-commit
$ pre-commit install --install-hooks
```

### Bump Version

This library uses bump version to manage version updates on releases.
Depending on the release type (patch, minor, major), run:
```
$ bump2version patch --commit --tag
```
to update the version, commit the changes and tag create a new version tag.
