"""
This module implements the following search algorithms:

- hill-climing search algorithm
- stochastic hill-climbing search algorithm
- simulated annealing search (algoritmo da têmpera simulada) TODO
- local beam search (busca em feixe local) TODO

"""

from aigyminsper.search.search_algorithms import SearchAlgorithm

def sort_function(val):
    """
    Function to sort the list by g(), h() or f()  
    """
    return val[1]


class SubidaMontanha (SearchAlgorithm):
    """
    This class implements the hill-climbing search algorithm.
    """

    def best(self, successors):
        """
        This method finds and returns the best successor based on the heuristic value.
        Parameters:
            successors (list): A list of successor states to evaluate.
        Returns:
            Node: The successor with the lowest heuristic value.
        """
        best_state = successors[0]
        for i in successors:
            if i.h() < best_state.h():
                best_state = i
        return best_state

    def search(self, initial_state, m=None, pruning='without', trace=False):
        atual = initial_state
        while True:
            if trace:
                print(f'Estado = {atual.env()}')
            prox = self.best(atual.successors())
            if prox.h() >= atual.h():
                return atual
            atual = prox


class SubidaMontanhaEstocastico (SearchAlgorithm):
    """
    This class implements the stochastic hill-climbing search algorithm.
    """

    def best(self, successors):
        """
        Determine the best state from the list of successors based on the heuristic value.
        Parameters:
            successors: A list of successor states to evaluate.
        Returns:
            The best state with the lowest heuristic value.
        """

        best_state = successors[0]
        for i in successors:
            if i.h() < best_state.h():
                best_state = i
        return best_state

    def search(self, initial_state, m=None, pruning='without', trace=False):
        atual = initial_state
        while True:
            if trace:
                print(f'Estado = {atual.env()}')
            prox = self.best(atual.successors())
            if prox.h() >= atual.h():
                if atual.is_goal():
                    return atual
                atual.randomState()
            else:
                atual = prox
