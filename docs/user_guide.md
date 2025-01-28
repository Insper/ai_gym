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
