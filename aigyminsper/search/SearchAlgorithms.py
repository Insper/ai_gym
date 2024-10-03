from collections import deque
from aigyminsper.search.Graph import Node

def sortFunction(val):
    """
    Function to sort the list by g(), h() or f()  
    """
    return val[1]

class SearchAlgorithm:
    """
    This class implements an interface for search algorithms.
    This class should not be instantiated.

    This class is used by the following implementations:
        - Breadth-first search (BuscaLargura)
        - Depth-first search (BuscaProfundidade)
        - Iterative deepening search (BPI)
        - Uniform cost search (CustoUniforme)
        - Greddy search algorithm (BuscaGananciosa)
        - A* search algorithm (AEstrela)
    """

    def search(self, initialState, pruning='without', trace=False):
        """
        This method implements a search algorithm.

        Parameters:
            initialState: the initial state of the search.
            pruning: a string that defines the pruning option. The pruning options are: without, father-son and general.
            trace: a boolean that defines if the trace if printed or not.
        """
        pass

    def print_trace(self, node) -> None:
        """
        This method prints the trace of the search.

        Parameters:
            node: the node that is the solution of the search.
        """
        print(f"Path (State {node.state.env()}): {node.show_path()} -- Cost: {node.g}")


class BuscaLargura (SearchAlgorithm):
    """
    This class implements the Breadth-first search algorithm.    
    """

    def search (self, initialState, pruning='without', trace=False): 
        # Define valid pruning options
        valid_pruning_options = ['without', 'father-son', 'general']
        if pruning not in valid_pruning_options:
            raise ValueError(f"Invalid pruning option: {pruning}. Valid options are {valid_pruning_options}")

        # Set to keep track of the visited nodes
        states = set()
        #Creating a Queue
        open = deque()
        open.append(Node(initialState, None))
        while (len(open) > 0):
            n = open.popleft()
            if trace: self.print_trace(n)

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
                    states.add(new_n.state.env())
        return None


class BuscaProfundidade (SearchAlgorithm):
    """
    This class implements the Depth-first search (limited)    
    """

    def search (self, initialState, m, pruning='without', trace=False): 
        # Define valid pruning options
        valid_pruning_options = ['without', 'father-son', 'general']
        if pruning not in valid_pruning_options:
            raise ValueError(f"Invalid pruning option: {pruning}. Valid options are {valid_pruning_options}")

        # Set to keep track of the visited nodes
        states = set()
        #Using list as stack
        open = []
        open.append(Node(initialState, None))
        while (len(open) > 0):
            n = open.pop()
            if trace: self.print_trace(n)

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
                        states.add(new_n.state.env())
        return None

class BuscaProfundidadeIterativa (SearchAlgorithm):
    """
    This class implements Iterative Deepening Depth-first search
    """

    def search (self, initialState, pruning='without', trace=False): 
        n = 1
        algorithm = BuscaProfundidade()
        while True:
            result = algorithm.search(initialState, n, pruning, trace)
            if (result != None):
                return result
            n = n+1


class BuscaCustoUniforme (SearchAlgorithm):
    """
    This class implements a Uniform cost search algorithm
    """

    def search (self, initialState, pruning='without', trace=False):
        # Define valid pruning options
        valid_pruning_options = ['without', 'father-son', 'general']
        if pruning not in valid_pruning_options:
            raise ValueError(f"Invalid pruning option: {pruning}. Valid options are {valid_pruning_options}")

        # Set to keep track of the visited nodes
        states = set()
        open = []
        new_n = Node(initialState, None)
        open.append((new_n, new_n.g))
        while (len(open) > 0):
            #list sorted by g()
            open.sort(key = sortFunction, reverse = True)
            n = open.pop()[0]
            if trace: self.print_trace(n)

            if (n.state.is_goal()):
                return n
            for i in n.state.successors():
                new_n = Node(i,n)
                # without pruning
                if pruning == "without":
                    open.append((new_n, new_n.g))
                # father-son pruning
                elif pruning == "father-son" and (new_n.state.env() != n.state.env()):
                    open.append((new_n, new_n.g))
                # general pruning
                elif pruning == "general" and (new_n.state.env() not in states):
                    open.append((new_n, new_n.g))
                    states.add(new_n.state.env())
        return None
    

class BuscaGananciosa (SearchAlgorithm):
    """
    This class implements a Greddy search algorithm
    """

    def search (self, initialState, pruning='without', trace=False):
        # Define valid pruning options
        valid_pruning_options = ['without', 'father-son', 'general']
        if pruning not in valid_pruning_options:
            raise ValueError(f"Invalid pruning option: {pruning}. Valid options are {valid_pruning_options}")

        # Set to keep track of the visited nodes
        states = set()
        open = []
        new_n = Node(initialState, None)
        open.append((new_n, new_n.h()))
        while (len(open) > 0):
            #list sorted by h()
            open.sort(key = sortFunction, reverse = True)
            n = open.pop()[0]
            if trace: self.print_trace(n)

            if (n.state.is_goal()):
                return n
            for i in n.state.successors():
                new_n = Node(i,n)
                # without pruning
                if pruning == "without":
                    open.append((new_n, new_n.h()))
                # father-son pruning
                elif pruning == "father-son" and (new_n.state.env() != n.state.env()):
                    open.append((new_n, new_n.h()))
                # general pruning
                elif pruning == "general" and (new_n.state.env() not in states):
                    open.append((new_n, new_n.h()))
                    states.add(new_n.state.env())
        return None


class AEstrela (SearchAlgorithm):
    """
    This class implements a A* search algorithm
    """

    def search (self, initialState, pruning='without', trace=False):
        # Define valid pruning options
        valid_pruning_options = ['without', 'father-son', 'general']
        if pruning not in valid_pruning_options:
            raise ValueError(f"Invalid pruning option: {pruning}. Valid options are {valid_pruning_options}")

        # Set to keep track of the visited nodes
        states = set()
        open = []
        new_n = Node(initialState, None)
        open.append((new_n, new_n.f()))
        while (len(open) > 0):
            #list sorted by f()
            open.sort(key = sortFunction, reverse = True)
            n = open.pop()[0]
            if trace: self.print_trace(n)
            
            if (n.state.is_goal()):
                return n
            # iterate trought all successors
            for i in n.state.successors():

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
                    states.add(new_n.state.env())
        return None
