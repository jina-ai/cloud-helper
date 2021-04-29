# Cloud Helper  
Library of helper tools to interact with cloud resources.



## Developer Quickstart Guide

## Installation
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
Depending on the release type (build, patch, minor, major), run:
```
$ bump2version build --commit
```
to update the version and commit.
