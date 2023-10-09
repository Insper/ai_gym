from abc import ABC, abstractmethod

class Node:
    """
    It is the most basic data structures necessary to implement search algorithms.
    """

    def __init__(self,state,father_node):
        """
        - state: the state represented by the node
        - father_node: the father node of the current node
        """

        self.state = state
        self.father_node = father_node
        if self.father_node == None:
            self.depth = 0
            self.g = 0
        else:
            self.depth = father_node.depth + 1
            self.g = state.cost() + self.father_node.g

    def show_path(self):
        """
        Return the path from the root node to the current node
        """
        if self.father_node != None:
            return self.father_node.show_path()  + " ; " + self.state.operator 
        else:
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
     
    
class State(ABC):
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

    @abstractmethod
    def successors(self):
        """
        Return a list of successors of the current state
        """
        pass
    
    @abstractmethod
    def is_goal(self):
        """
        It returns True if the current state is a goal state
        """
        pass
    
    @abstractmethod
    def description(self):
        """
        Return a string with a brief description of the problem
        """
        pass
    
    @abstractmethod
    def cost(self):
        """
        Return the cost of the current state
        """
        pass

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
        pass