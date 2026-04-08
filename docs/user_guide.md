# User Guide

In order to create an agent you must implement the `State` interface as shown below:

```python
from aigyminsper.search.graph import State

class MyAgent(State):

    def __init__(self, op):
        super().__init__(op)
        # You must define how to represent the state
        #TODO

    def successors(self):
        successors = []
        #TODO
        # you must define how to generate the successors for each operator (action)
        return successors

    def is_goal(self):
        # You must define the goal state
        pass

    def description(self):
        return "Problem description"

    def cost(self):
        # Return the cost of each operator (action)
        return 1

    def env(self):
        #
        # This methos is used to return a description of the state (environment).
        # This method is used to print the state of the environment. This representation is used in the pruning method of the search algorithms.
        #
        None
```

You, as a developer, must implement the methods `successors`, `is_goal`, `description`, `cost`, and `env`, and describe how the world must be represented.

The next step is define the best algorithm to solve the problem.

```python
from aigyminsper.search.search_algorithms import BuscaLargura


def main():
    print('Busca em profundidade iterativa')
    state = AgentSpecification('')
    algorithm = BuscaLargura()
    result = algorithm.search(state)
    if result != None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')


if __name__ == '__main__':
    main()
```

The available algorithms and their corresponding class names are:

| Algorithm | Class |
|---|---|
| Breadth-first search | `BuscaLargura` |
| Depth-first search (depth-limited) | `BuscaProfundidade` |
| Iterative deepening depth-first search | `BuscaProfundidadeIterativa` |
| Uniform cost search | `BuscaCustoUniforme` |
| Greedy search | `BuscaGananciosa` |
| A\* search | `AEstrela` |
| Hill climbing | `SubidaMontanha` |
| Stochastic hill climbing | `SubidaMontanhaEstocastico` |
| Parallel search | `ParallelSearch` |

All algorithms except `SubidaMontanha` and `SubidaMontanhaEstocastico` accept a `pruning` argument:

```python
result = algorithm.search(state, pruning='general')  # 'without', 'father-son', or 'general'
```

## Parallel Search

`ParallelSearch` is a wrapper that runs any other search algorithm in parallel,
distributing work across all logical CPUs of the machine.

It works in two phases:

1. **Seeding** – a short BFS explores the initial state and collects one
   frontier node per available CPU.
2. **Parallel race** – each frontier node is handed to an independent worker
   process running the wrapped algorithm.  The first worker to find a solution
   wins; all other workers are stopped immediately.

The returned node has the full path from the initial state to the goal, and
`show_path()` / `g` work exactly like on any other result node.

```python
from aigyminsper.search.search_algorithms import ParallelSearch, AEstrela

def main():
    state = AgentSpecification('')
    # Wrap any algorithm — defaults to BuscaLargura when omitted
    algorithm = ParallelSearch(AEstrela)
    result = algorithm.search(state, pruning='general')
    if result is not None:
        print('Found!')
        print(result.show_path())
        print('Total cost:', result.g)
    else:
        print('No solution found')

if __name__ == '__main__':
    main()
```

You can also control the number of worker processes explicitly:

```python
algorithm = ParallelSearch(AEstrela, n_processes=4)
```

> **Note:** `ParallelSearch` splits the search space across seeds and does not
> guarantee a globally optimal solution when wrapping cost-optimal algorithms
> such as `BuscaCustoUniforme` or `AEstrela`.  For optimal guarantees use the
> single-process versions of those algorithms.
