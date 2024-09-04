"""
This module implements the following search algorithms:

- hill-climing search algorithm
- stochastic hill-climbing search algorithm
- simulated annealing search (algoritmo da têmpera simulada) TODO
- local beam search (busca em feixe local) TODO

"""

from aigyminsper.search.SearchAlgorithms import SearchAlgorithm

def sortFunction(val):
    """
    Function to sort the list by g(), h() or f()  
    """
    return val[1]


class SubidaMontanha (SearchAlgorithm):
    """
    This class implements the hill-climbing search algorithm.
    """

    def best(self, successors):
        best_state = successors[0]
        for i in successors:
            if i.h() < best_state.h():
                best_state = i
        return best_state

    def search (self, initialState, trace= False):
        atual = initialState
        while True:
            if trace: print(f'Estado = {atual.env()}') 
            prox = self.best(atual.successors())
            if prox.h() >= atual.h():
                return atual
            atual = prox


class SubidaMontanhaEstocastico (SearchAlgorithm):
    """
    This class implements the stochastic hill-climbing search algorithm.
    """

    def best(self, successors):
        best_state = successors[0]
        for i in successors:
            if i.h() < best_state.h():
                best_state = i
        return best_state

    def search (self, initialState, trace= False):
        atual = initialState
        while True:
            if trace: print(f'Estado = {atual.env()}') 
            prox = self.best(atual.successors())
            if prox.h() >= atual.h():
                if atual.is_goal():
                    return atual
                else: 
                    atual.randomState()
            else:
                atual = prox


