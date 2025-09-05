"""Module providing classes Node and State."""

from abc import abstractmethod
from uuid import uuid4

class Node:
    """
    It is the most basic data structures necessary to implement search algorithms.
    """

    def __init__(self,state,father_node):
        """
        - state: the state represented by the node
        - father_node: the father node of the current node
        - identifier: unique identifier generated when node is instantiated, used internally
        """
        self.identifier: str = f"{uuid4()}"

        self.state = state
        self.father_node = father_node
        if self.father_node is None:
            self.depth = 0
            self.g = 0
        else:
            self.depth = father_node.depth + 1
            self.g = state.cost() + self.father_node.g

    def show_path(self):
        """
        Return the path from the root node to the current node
        """
        if self.father_node is not None:
            return self.father_node.show_path()  + " ; " + self.state.operator
        return self.state.operator

    def h(self):
        """
        Return the heuristic value of the current node
        """
        return self.state.h()

    def f(self):
        """
        Return the evaluation function value of the current node: f(n) = g(n) + h(n)
        """
        return self.g + self.h()


class State:
    """
    This class represents a state in a search problem.
    This is an abstract class. This class defines the following abstract methods:
    - successors: returns a list of successors of the current state
    - is_goal: returns True if the current state is a goal state
    - description: returns a string with a brief description of the problem
    - cost: returns the cost of the current state
    - env: returns the description of the environment of the current state

    This class also defines the following non-abstract methods:
    - print: returns a string with the operator that generated the current state
    """

    def __init__(self,operator):
        """
        - operator: the operator that generated the current state
        """
        self.operator = operator

    @abstractmethod
    def successors(self):
        """
        Return a list of successors of the current state
        """

    @abstractmethod
    def is_goal(self):
        """
        It returns True if the current state is a goal state
        """

    @abstractmethod
    def description(self):
        """
        Return a string with a brief description of the problem
        """

    @abstractmethod
    def cost(self):
        """
        Return the cost of the current state
        """

    def print(self):
        """
        Return a string with the operator that generated the current state
        """
        return str(self.operator)

    @abstractmethod
    def env(self):
        """
        Return the description of the environment of the current state
        """
