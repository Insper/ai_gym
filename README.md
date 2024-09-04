# AIGYM

The goal of this libray is provide a set of tools to help you to learn Artificial Intelligence.

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

Execute:

```bash
pytest 
```

You can also run the tests using the VSCode. Just open the `tests` folder and click on the `Run All Tests` button.

## How to upgrade the package

If you need to upgrade the package, please follow these steps: 

* change what you need in the code;
* test it :smile: ;
* describe what you did in the [Changelog.md](./Changelog.md) file;
* change the `setup.py` file. In special, the `version` attribute;
* commit and push the changes on `main` branch;
* then do the same on the `stable` branch;

We have two workflows in the GitHub Actions:

* to publish the package in the PyPI when you push something in the `stable` branch. This workflow does the same as: 

```bash
python setup.py sdist
twine upload dist/*
```

* to publish the website (documentation) in the GitHub Pages.


## How to install the package

```bash
pip install aigyminsper
```

## Change log

The change log of this library is in the [Changelog.md](./Changelog.md) file. 

## Documentation

The documentation of this library is in the [docs](./docs) folder. 
We are using [MkDocs](https://www.mkdocs.org/) to generate the documentation.

To see the documentation in your local machine, please type: 

```bash 
mkdocs serve
```

To deploy a new version of the documentation, please merge the content in the stable branch: 

```bash
git checkout stable
git merge main
git push
```

There is a GitHub Action that will deploy the documentation in the GitHub Pages.

## Contributing

* Fork the Project
* Create your Feature Branch (git checkout -b feature/AmazingFeature)
* Commit your Changes (git commit -m 'Add some AmazingFeature)
* Push to the Branch (git push origin feature/AmazingFeature)
* Open a Pull Request


