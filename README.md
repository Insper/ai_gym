# AIGYM

This is a package with basic AI algorithms. This package is used in some subjects at Insper. 

## How to setup the environment

To avoid any configuration problems, we recommend creating a virtual environment with python:

```bash
python3 -m virtualenv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

To quit the virtual environment, type `deactivate`. If you already have the virtual environment configured then type `source venv/bin/activate`.

## How to publish the package using PyPi

Change the version attribute in `setup.py` and then type: 

```bash
python setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

if you need to upload a new version, please type:

```bash
twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*
```

## How to install the package

```bash
pip install --index-url https://test.pypi.org/simple/ aigyminsper
```