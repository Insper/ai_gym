from aigyminsper.search.SearchAlgorithms import SearchAlgorithm

# function used to sort a list
def sortFunction(val):
    return val[1]

#
# Implements search algorithms:
# 1) hill-climing search algorithms
# 2) Simulated annealing search (algoritmo da têmpera simulada) TODO
# 3) Local Beam Search (busca em feixe local) TODO
#

class SubidaMontanha (SearchAlgorithm):

    def best(self, successors):
        best_state = successors[0]
        for i in successors:
            if i.h() < best_state.h():
                best_state = i
        return best_state

    def search (self, initialState):
        atual = initialState
        while True:
            prox = self.best(atual.successors())
            if prox.h() >= atual.h():
                return atual
            atual = prox


class SubidaMontanhaEstocastico (SearchAlgorithm):

    def best(self, successors):
        best_state = successors[0]
        for i in successors:
            if i.h() < best_state.h():
                best_state = i
        return best_state

    def search (self, initialState):
        atual = initialState
        while True:
            prox = self.best(atual.successors())
            if prox.h() >= atual.h():
                if atual.is_goal():
                    return atual
                else: 
                    atual.randomState()
            else:
                atual = prox


