# User Guide

## Choosing a state class

A state represents one configuration of a problem. Its `successors()` method
describes the configurations that can be reached from it.

| State class | Purpose | Typical algorithms |
| --- | --- | --- |
| `State` | Basic state-space or game representation | BFS, DFS, iterative deepening, uniform cost, MinMax |
| `HeuristicState` | State with an estimate of distance or quality | Greedy, A*, hill climbing |
| `CspState` | State for constraint-satisfaction and stochastic problems | Stochastic hill climbing |

### Basic state

Implement the `State` interface for ordinary search problems:

```python
from aigyminsper.search.graph import State


class MyAgent(State):
    def __init__(self, operator, value):
        super().__init__(operator)
        self.value = value

    def successors(self):
        return []  # Return reachable MyAgent states.

    def is_goal(self):
        return False

    def description(self):
        return "Problem description"

    def cost(self):
        return 1

    def env(self):
        # This value must uniquely represent the relevant state.
        return str(self.value)
```

`env()` is used by pruning strategies. Two states that should be treated as
equivalent must return the same value.

### Heuristic state

Heuristic algorithms additionally use `h()`:

```python
from aigyminsper.search.graph import HeuristicState


class MyHeuristicAgent(HeuristicState):
    # Implement successors(), is_goal(), description(), cost(), and env().

    def h(self):
        return 0  # Estimate the remaining distance or state quality.
```

`CspState` extends this interface with `random_state()` when a local stochastic
algorithm needs to generate another candidate.

## Choosing a search algorithm

```python
from aigyminsper.search.search_algorithms import BuscaLargura


state = MyAgent("", initial_value)
result = BuscaLargura().search(state)

if result is not None:
    print(result.show_path())
else:
    print("No solution")
```

| Algorithm | Class | State type | Cost | Heuristic | Main consideration |
| --- | --- | --- | ---: | ---: | --- |
| Breadth-first | `BuscaLargura` | `State` | No | No | Can require substantial memory |
| Depth-first | `BuscaProfundidade` | `State` | No | No | Requires a depth limit |
| Iterative deepening | `BuscaProfundidadeIterativa` | `State` | No | No | Repeats depth-limited searches |
| Uniform cost | `BuscaCustoUniforme` | `State` | Yes | No | Handles varying action costs |
| Greedy | `BuscaGananciosa` | `HeuristicState` | No | Yes | Is not generally optimal |
| A* | `AEstrela` | `HeuristicState` | Yes | Yes | Optimality depends on the heuristic |
| MinMax | `MinMax` | `State` | Utility | Optional | Alternates maximizing and minimizing turns |
| Hill climbing | `SubidaMontanha` | `HeuristicState` | — | Yes | Can stop at a local optimum |
| Stochastic hill climbing | `SubidaMontanhaEstocastico` | `CspState` | — | Yes | Uses randomized local search |

## Pruning strategies

Graph-search algorithms accept a `pruning` argument:

```python
result = algorithm.search(state, pruning="general")
```

- `without`: does not prevent repeated states.
- `father-son`: prevents an immediate return to the parent state.
- `general`: tracks environments that have already been generated.

The available behavior depends on `env()` uniquely representing the state.

## MinMax

MinMax uses `start=0` for the maximizing player and `start=1` for the
minimizing player. The optional `m` argument limits the explored depth.

```python
from aigyminsper.search.search_algorithms import MinMax


result = MinMax().search(state, start=0, m=4)
```

For a complete implementation, see the [Noughts & Crosses example](examples.md#noughts-crosses).
