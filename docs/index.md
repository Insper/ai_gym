# AI Gym

AI Gym is a teaching library for learning the foundations of Artificial
Intelligence through search problems and agents.

## Available algorithms

1. Breadth-first search
2. Depth-first search
3. Iterative deepening search
4. Uniform-cost search
5. Greedy search
6. A* search
7. MinMax adversarial search
8. Hill climbing
9. Stochastic hill climbing

All search algorithms share a common state interface, making it possible to
reuse the same problem representation with compatible strategies.

## Installation

```bash
pip install aigyminsper
```

## Graphical tracing

The trace feature displays the search tree as an algorithm evaluates states.
It requires the Graphviz executable and a graphical Matplotlib backend.

### Install Graphviz

=== "Windows"

    ```powershell
    winget install graphviz
    where.exe dot
    ```

=== "Debian / Ubuntu / Linux Mint"

    ```bash
    sudo apt update
    sudo apt install graphviz
    which dot
    ```

### Configure the graphical backend

Check the current Matplotlib backend:

```bash
python -c "import matplotlib; print(matplotlib.get_backend())"
```

If it reports `Agg`, install PyQt6 and select the Qt backend:

```bash
python -m pip install PyQt6
python -c "from PyQt6 import QtWidgets; print('PyQt6 OK')"
```

=== "Windows PowerShell"

    ```powershell
    $env:MPLBACKEND="QtAgg"
    ```

=== "Linux"

    ```bash
    export MPLBACKEND=QtAgg
    ```

### Enable tracing

```python
algorithm = BuscaLargura()
result = algorithm.search(state, trace=True)
```

Useful options include `trace_live=True`, `trace_fullscreen=True`,
`trace_hold_graph=False`, and `trace_delay=0.02`. MinMax also accepts
`trace_max_depth` to keep large game trees readable.
