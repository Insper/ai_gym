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

## How to test the project

To run the tests, please type in the root directory: 

```bash
export PYTHONPATH=.
pytest tests
```

## How to publish the package using PyPi

Change the version attribute in `setup.py` and then type: 

```bash
python setup.py sdist
twine upload dist/*
```

## How to upgrade the package

If you need to upgrade the package, please follow these steps: 

* change what you need in the code;
* test it :smile: ;
* change the `setup.py` file. In special, the `version` attribute;
* type 

```bash
python setup.py sdist
twine upload dist/*
```

## How to install the package

```bash
pip install aigyminsper
```

## Change log

The change log of this library is in the [Changelog.md](./Changelog.md) file. 