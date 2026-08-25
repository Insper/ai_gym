# User Guide

## Choosing a State class

The state class defines how a problem is represented and what information is available to the search algorithm. A state typically represents one configuration of the problem, while successors() defines the configurations that can be reached from it.

Aigyminsper provides different state classes for different kinds of search problems

| State class      | Purpose                                                                             | Typical algorithms                                 |
| ---------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------- |
| `State`          | Basic state-space representation                                                    | BFS, DFS, iterative deepening, uniform-cost search |
| `HeuristicState` | State with heuristic information about the distance or quality relative to the goal | Greedy search, A*, hill climbing                   |
| `CspState`       | State representation for constraint-satisfaction problems                           | CSP-oriented search algorithms                     |


In order to create a basic agent you can implement the `State` interface as shown below (relative to the choosen state class):

```python
from aigyminsper.search.graph import State

class MyAgent(State):

    def __init__(self, op):
        super().__init__(op)
        # You must define how to represent the state

    def successors(self):
        successors = []
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
        pass
```

For heuristics algorithms using the HeuristicState you must implement all of the above methods in adition to the method `h()` bellow

```python
from aigyminsper.search.graph import HeuristicState

class MyAgent(HeuristicState):

    def __init__(self, op):
        super().__init__(op)
        # You must define how to represent the state

    def successors(self): ...

    def is_goal(self): ...

    def description(self): ...

    def cost(self): ...

    def env(self): ...

    def h(self):
        """
        Return the heuristic of the current state
        """
        
```

And for Constraint Satisfaction Problem (CSP) you must use as well the method `random_state()` (if needed)

```python
from aigyminsper.search.graph import HeuristicState

class MyAgent(HeuristicState):

    def __init__(self, op):
        super().__init__(op)
        # You must define how to represent the state

    def successors(self): ...

    def is_goal(self): ...

    def description(self): ...

    def cost(self): ...

    def env(self): ...

    def h(self):
        """
        Return the heuristic of the current state
        """

    def random_state(self):
        """
        Return random possible state
        """
        
```

> Obs: You can use just the `State` class and implement the needed method if you want to

You, as a developer, must implement the methods `successors`, `is_goal`, `description`, `cost`, and `env`, and describe how the world must be represented.

## Choosing the Search Algorithm

The next step is define the best algorithm to solve the problem.

```python
from aigyminsper.search.search_algorithms import BuscaLargura


def main():
    print('Using Breath First search')
    state = MyAgent('', ...)
    algorithm = BuscaLargura()
    result = algorithm.search(state)
    if result != None:
        print('Found!')
        print(result.show_path())
    else:
        print('No solution')


if __name__ == '__main__':
    main()
```

The available algorithms and their corresponding characteristics:

| Algorithm                | Class                        | State type                   |                   Uses cost | Uses heuristic | Important constraint                        |
| ------------------------ | ---------------------------- | ---------------------------- | --------------------------: | -------------: | ------------------------------------------- |
| Breadth-first            | `BuscaLargura`               | `State`                      |                          No |             No | Memory-intensive                            |
| Depth-first              | `BuscaProfundidade`          | `State`                      |                          No |             No | Requires/configures a depth limit           |
| Iterative deepening      | `BuscaProfundidadeIterativa` | `State`                      |                          No |             No | Repeats depth-limited searches              |
| Uniform cost             | `BuscaCustoUniforme`         | `State`                      |                         Yes |             No | Appropriate for varying action costs        |
| Greedy                   | `BuscaGananciosa`            | `HeuristicState`             | No/implementation-dependent |            Yes | Not generally optimal                       |
| A*                       | `AEstrela`                   | `HeuristicState`             |                         Yes |            Yes | Optimality depends on heuristic assumptions |
| Hill climbing            | `SubidaMontanha`             | `HeuristicState`             |                           — |            Yes | Local search; can get stuck                 |
| Stochastic hill climbing | `SubidaMontanhaEstocastico`  | `CspState`             |                           — |            Yes | Local/stochastic search                     |
| Parallel                 | `ParallelSearch`             | Depends on wrapped algorithm |                     Depends |        Depends | Global optimality may be lost               |


All algorithms except `SubidaMontanha` and `SubidaMontanhaEstocastico` accept a `pruning` argument:

```python
result = algorithm.search(state, pruning='general')  # 'without', 'father-son', or 'general'
```

> For examples on real usages of the flow above see [Examples](./examples.md) page.

## Pruning strategies

**without** — no repeated-state pruning. The algorithm may revisit states it has already explored.

**father-son** — prevents immediate backtracking between a state and its parent, if that matches your implementation.

**general** — tracks previously visited environments and prevents/reduces repeated exploration, presumably based on env().

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
