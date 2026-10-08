from aigyminsper.search.search_algorithms import BuscaProfundidadeIterativa, AEstrela
from aigyminsper.search.graph import State
import numpy
import sys
# Import the required libraries.
# This example uses the base State class and compatible search algorithms.

class VacuumWorldGeneric(State):

    def __init__(self, mapa, lin, col, op):
        """Initialize the vacuum-world state.

        mapa: A rectangular binary NumPy array representing the map
            ex: [[0, 1, 1, 1],
                 [0, 0, 1, 1]
                 [1, 1, 1, 1]]
            note: This is a NumPy array rather than a list of lists.
        lin: the agent's horizontal position (row)
        col: the agent's vertical position (column)
        op: the operation that led to the current state
            ex: If the agent moved left, op = 'esq'.
        """

        super().__init__(op)
        self.mapa = mapa
        self.lin_max = self.mapa.shape[0]-1 # Maximum row the agent can reach
        self.col_max = self.mapa.shape[1]-1 # Maximum column the agent can reach
        self.lin = lin
        self.col = col
    
    def successors(self):
        """Return states produced by every valid movement or cleaning action."""

        sucessors = []

        # Move left
        if self.col - 1 >= 0:
            new = self.mapa.copy()
            sucessors.append(VacuumWorldGeneric(new, self.lin, self.col-1, 'esq'))

        # Move right
        if self.col + 1 <= self.col_max:
            new = self.mapa.copy()
            sucessors.append(VacuumWorldGeneric(new, self.lin, self.col+1, 'dir'))

        # Move up
        if self.lin - 1 >=0:
            new = self.mapa.copy()
            sucessors.append(VacuumWorldGeneric(new, self.lin-1, self.col, 'cima'))

        # Move down
        if self.lin + 1 <= self.lin_max:
            new = self.mapa.copy()
            sucessors.append(VacuumWorldGeneric(new, self.lin+1, self.col, 'baixo'))

        # Clean the current room
        if self.mapa[self.lin][self.col] == 1:
            new = self.mapa.copy()
            new[self.lin][self.col] = 0 
            sucessors.append(VacuumWorldGeneric(new, self.lin, self.col, 'limpar'))

        return sucessors
    
    def is_goal(self):
        """Return whether every room in the map is clean."""
        for y in self.mapa:
            for x in y:
                if x != 0:
                    return False
        return True

    def h(self):
        """Estimate the remaining work by counting dirty rooms."""
        count = 0
        for y in self.mapa:
            for x in y:
                if x != 0:
                    count = count + 1
        return count
    
    def description(self):
        """Describe the problem represented by this state."""
        return "Agente genérico para o problema do aspirador de pó"
    
    def cost(self):
        """Assign unit cost to movement and cleaning actions."""
        return 1
    
    def env(self):
        """Identify a state from its map and the agent's position."""
        return str(self.mapa)+" "+str(self.lin)+" "+str(self.col)


def convert_file_to_map(file_map_path):
    """Convert a semicolon-separated text file into a NumPy array."""
    return numpy.loadtxt(open(file_map_path, "rb"), delimiter=";")

def main(file_map_path, lin, col):
    mapa = convert_file_to_map(file_map_path)
    print(mapa)

    # Creates initial State
    state = VacuumWorldGeneric(mapa, lin, col, '')

    #print('Busca em AEstrela')
    algorithm = AEstrela()
    
    print('Busca Profundidade Iterativa')
    # Create search algorithm object
    # algorithm = BuscaProfundidadeIterativa()

    # Executes the search
    result = algorithm.search(state, trace=True)
    if result != None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
