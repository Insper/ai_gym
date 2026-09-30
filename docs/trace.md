# Graphical tracing

The trace feature displays the search tree while an algorithm evaluates and
expands states. It requires the Graphviz executable and a graphical Matplotlib
backend.

## Install Graphviz

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

## Configure the graphical backend

Check the current Matplotlib backend:

```bash
python -c "import matplotlib; print(matplotlib.get_backend())"
```

If the command reports `Agg`, install PyQt6 inside the virtual environment and
select the Qt backend:

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

## Enable tracing

Pass `trace=True` when calling an algorithm's `search` method:

```python
algorithm = BuscaLargura()
result = algorithm.search(state, trace=True)
```

The most useful options are:

| Option | Description |
| --- | --- |
| `trace_live=True` | Updates the graph while the search runs instead of replaying it afterward. |
| `trace_fullscreen=True` | Opens the visualization in full-screen mode. |
| `trace_hold_graph=False` | Closes the visualization when the trace finishes. |
| `trace_delay=0.02` | Sets the delay, in seconds, between replayed frames. |
| `trace_max_depth=2` | Limits the displayed tree depth for algorithms such as MinMax. |

For example, the following call replays a bounded trace and closes it when the
replay ends:

```python
result = algorithm.search(
    state,
    trace=True,
    trace_live=False,
    trace_hold_graph=False,
    trace_delay=0.02,
    trace_max_depth=2,
)
```
