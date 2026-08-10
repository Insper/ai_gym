# AIGYM

The goal of this library is to provide a set of tools to help you to learn the basics of Artificial Intelligence. In other words, the goal of this library is to help you to learn how to build agents that solve problems by searching.

This library implements the following algorithms:

1. Breadth-first search 
1. Depth-first search 
1. Iterative deepening search 
1. Uniform cost search 
1. Greedy search algorithm
1. A* search algorithm 
1. Hill climbing search algorithm
1. Stochastic hill climbing search algorithm
1. Parallel search (distributes work across all CPU cores)

This library also has a common interface for agents, allowing you to easily create and deploy agents that solve problems by searching.

## How to install the library

```bash
pip install aigyminsper
```

# Trace Feature

## What it is

The trace feature is a graphical interface where you can see the algorithm searching and building the search tree, it is useful if you want a more descriptive visualization

## How to install

The trace feature uses an application called Graphviz, which helps create graphs.
To use it, it is needed to install its executable 

To install it, run:
```
# On Windows
# Windows
winget install graphviz

# Debian / Ubuntu / Linux Mint
sudo apt update
sudo apt install graphviz
```

Check if the installation was successuful 
```
# Windows
where.exe dot

# Linux
which dot
```

And finally, with the library installed, check if you have a proper display for Matplotlib

run:
```
python -c "import matplotlib; print(matplotlib.get_backend())"
```

If you get anything other than "Agg" you're fine, if not we recommend you to install QtAgg backend

To install it run inside the venv:
```
python -m pip install PyQt6
```

Then verify
```
python -c "from PyQt6 import QtWidgets; print('PyQt6 OK')"
```
You should get a "PyQt6 OK"

Then export it to the environment

```
# On Windows
$env:MPLBACKEND="QtAgg"

# On Linux
export MPLBACKEND=QtAgg
```

## How to use it

When running the search function, add `trace=True` in its call.
```
# Example
algorithm = BuscaLargura()
result = algorithm.search(state, trace=True)
```

If you want full screen add `trace_fullscreen=True` as well
