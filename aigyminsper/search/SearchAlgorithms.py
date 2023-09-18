from collections import deque
from aigyminsper.search.Graph import Node

# function used to sort a list
def sortFunction(val):
    return val[1]

#
# Implements search algorithms:
# 1) Breadth-first search (BuscaLargura)
# 2) Depth-first search (BuscaProfundidade)
# 3) Iterative deepening search (BPI)
# 4) Uniform cost search (CustoUniforme)
# 5) Greddy search algorithm (BuscaGananciosa)
# 6) A* search algorithm (AEstrela)
#

class SearchAlgorithm:
    def search(self, pruning='without', trace=False):
        pass

#
# This class implements the Breadth-first search
#
class BuscaLargura (SearchAlgorithm):

    def search (self, initialState, pruning='without', trace=False): 
        # List to keep track of the visited nodes
        states = []
        #Creating a Queue
        open = deque()
        open.append(Node(initialState, None))
        while (len(open) > 0):
            n = open.popleft()
            if trace: print(f'Estado = {n.state.env()} com custo = {n.g}') 
            if (n.state.is_goal()):
                return n
            for i in n.state.successors():
                new_n = Node(i,n)
                # without pruning
                if pruning == "without":
                    open.append(new_n)
                # father-son pruning
                elif pruning == "father-son" and (new_n.state.env() != n.state.env()):
                    open.append(new_n)
                # general pruning
                elif pruning == "general" and (new_n.state.env() not in states):
                    open.append(new_n)
                    states.append(new_n.state.env())
        return None

#
# This class implements the Depth-first search (limited)
#
class BuscaProfundidade (SearchAlgorithm):

    def search (self, initialState, m, pruning='without', trace=False): 
        # List to keep track of the visited nodes
        states = []
        #Using list as stack
        open = []
        open.append(Node(initialState, None))
        while (len(open) > 0):
            n = open.pop()
            if trace: print(f'Estado = {n.state.env()} com custo = {n.g}') 
            if (n.state.is_goal()):
                return n
            if (n.depth < m):
                for i in n.state.successors():
                    new_n = Node(i,n)
                    # without pruning
                    if pruning == "without":
                        open.append(new_n)
                    # father-son pruning
                    elif pruning == "father-son" and (new_n.state.env() != n.state.env()):
                        open.append(new_n)
                    # general pruning
                    elif pruning == "general" and (new_n.state.env() not in states):
                        open.append(new_n)
                        states.append(new_n.state.env())
        return None

#
# This class implements Iterative Deepening Depth-first search
#
class BuscaProfundidadeIterativa (SearchAlgorithm):

    def search (self, initialState, pruning='without', trace=False): 
        n = 1
        algorithm = BuscaProfundidade()
        while True:
            result = algorithm.search(initialState, n, pruning, trace)
            if (result != None):
                return result
            n = n+1

#
# This class implements a Uniform cost search algorithm
#
class BuscaCustoUniforme (SearchAlgorithm):

    def search (self, initialState, pruning='without', trace=False):
        # List to keep track of the visited nodes
        states = []
        open = []
        new_n = Node(initialState, None)
        open.append((new_n, new_n.g))
        while (len(open) > 0):
            #list sorted by g()
            open.sort(key = sortFunction, reverse = True)
            n = open.pop()[0]
            if trace: print(f'Estado = {n.state.env()} com custo = {n.g}') 
            if (n.state.is_goal()):
                return n
            for i in n.state.successors():
                new_n = Node(i,n)
                # without pruning
                if pruning == "without":
                    open.append(new_n,new_n.g)
                # father-son pruning
                elif pruning == "father-son" and (new_n.state.env() != n.state.env()):
                    open.append(new_n,new_n.g)
                # general pruning
                elif pruning == "general" and (new_n.state.env() not in states):
                    open.append(new_n,new_n.g)
                    states.append(new_n.state.env())
        return None
    
#
# This class implements a Greddy search algorithm
#
class BuscaGananciosa (SearchAlgorithm):

    def search (self, initialState, pruning='without', trace=False):
        # List to keep track of the visited nodes
        states = []
        open = []
        new_n = Node(initialState, None)
        open.append((new_n, new_n.h()))
        while (len(open) > 0):
            #list sorted by h()
            open.sort(key = sortFunction, reverse = True)
            n = open.pop()[0]
            if trace: print(f'Estado = {n.state.env()} com custo = {n.g}') 
            if (n.state.is_goal()):
                return n
            for i in n.state.successors():
                new_n = Node(i,n)
                # without pruning
                if pruning == "without":
                    open.append(new_n,new_n.h())
                # father-son pruning
                elif pruning == "father-son" and (new_n.state.env() != n.state.env()):
                    open.append(new_n,new_n.h())
                # general pruning
                elif pruning == "general" and (new_n.state.env() not in states):
                    open.append(new_n,new_n.h())
                    states.append(new_n.state.env())
        return None

#
# This class implements a A* search algorithm

# Pruning options: 

# "without"
# "father-son"
# "ancestral-son"
# "general"

class AEstrela (SearchAlgorithm):

    def search (self, initialState, pruning='without', trace=False):
        # List to keep track of the visited nodes
        states = []
        open = []
        new_n = Node(initialState, None)
        open.append((new_n, new_n.f()))
        while (len(open) > 0):
            #list sorted by f()
            open.sort(key = sortFunction, reverse = True)
            n = open.pop()[0]
            if trace: print(f'Estado = {n.state.env()} com custo = {n.g}') 
            if (n.state.is_goal()):
                return n
            # iterate trought all successors
            for i in n.state.sucessors():

                new_n = Node(i,n)
                # without pruning
                if pruning == "without":
                    open.append((new_n,new_n.f()))
                # father-son pruning
                elif pruning == "father-son" and (new_n.state.env() != n.state.env()):
                    open.append((new_n,new_n.f()))
                # general pruning
                elif pruning == "general" and (new_n.state.env() not in states):
                    open.append((new_n,new_n.f()))
                    # nao eh adiciona o estado ao vetor.
                    # eh adicionado o conteudo
                    states.append(new_n.state.env())
        return None
