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

## How to implement the trace function

First install the needed application

Graph visualizer application
```cmd
# Windows
winget install graphviz

# Debian / Ubuntu / Linux Mint
sudo apt update
sudo apt install graphviz
```
> Check your distro relatice

Then test it

```cmd
# Windows
where.exe dot

# Linux
which dot

# Inside the venv
dot -V
```


Then finaly test if matplotlib has an interative backend

Check
```
python -c "import matplotlib; print(matplotlib.get_backend())"
```

if you get an "Agg" you may not have an graphc display associated

We recomend the QtAgg backend, follow the instructions below to install it

```
# Install in the virtual enviroment
python -m pip install PyQt6

# Verify
python -m pip install PyQt6

# You should get a "PyQt6 OK"

# then export it's backend

# Windows
$env:MPLBACKEND="QtAgg"

# Linux
export MPLBACKEND=QtAgg
```

Then test it
```
# On root folder
python tests/AspiradorPo.py
```

## How to test the project

Execute:

```bash
pytest 
```
You can also run the tests using the VSCode. Just open the `tests` folder and click on the `Run All Tests` button.

Besides, there are some features that must be tested manually, like the trace of the execution of the algorithms. To do that, you can run the following script:

```bash
export PYTHONPATH=.:$PYTHONPATH
cd tests/
python SumOne.py
python AspiradorPo.py
```

or: 

```bash
python tests/SumOne.py
python tests/AspiradorPo.py
```

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

### On Linux

```bash
pip install aigyminsper*
```

### On Windows or MacOS

Before execute the command `pip install aigyminsper`, please install the **graphviz** software in your machine.

To install the graphviz software, please follow the instructions in the [graphviz](https://graphviz.org/download/) website.

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
