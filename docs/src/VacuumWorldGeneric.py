from aigyminsper.search.search_algorithms import BuscaProfundidadeIterativa, AEstrela
from aigyminsper.search.graph import State
import numpy
import sys
# Importação das bibliotecas necessárias
# Utilizaremos a Busca em Profundidade Iterativa neste exemplo, e a classe base State

class VacuumWorldGeneric(State):

    def __init__(self, mapa, lin, col, op):
        """
        In the init method, we set the initial variables:
        mapa: A square binary NumPy array representing the map
            ex: [[0, 1, 1, 1],
                 [0, 0, 1, 1]
                 [1, 1, 1, 1]]
            note: It is not a list of lists, but rather a NumPy array!!
        lin: the agent's horizontal position (row)
        col: the agent's vertical position (column)
        op: the operation that led to the current state
            ex: If the agent has just started, op = ' '; if the agent moved to the left, op = 'esq', and so on...
        """

        super().__init__(op)
        self.mapa = mapa
        self.lin_max = self.mapa.shape[0]-1 # A linha máxima que o agente pode chegar
        self.col_max = self.mapa.shape[1]-1 # A coluna máxima que o agento pode chegar
        self.lin = lin
        self.col = col
    
    def successors(self):
        """
        When generating the successors, we follow the flow below:
        1 - We create an empty list of successors `sucessors = []`
        2 - We list the possible actions and ask: what conditions must be met to execute an action?
        3 - We create conditional statements for each action
        4 - When a condition is satisfied, we create a new state with the new characteristics resulting from the action and add it to the successors
        5 - We return the successors

        In the Vacuum World, the flow would be
        1 - `sucessors = []`
        2 - possible actions: move (left, right, up, down); clean; I can only move if there's a tile to move to, I can only clean if I'm on a dirt tile
        3 - for movement, verify next position available, if it is add to sucessors. verify if the floor is dirt, if it is, add to sucessors
        4 - if moving, set the lin or col to the next, and copy the map, then append VacuumWorldGeneric(new_map, next_lin, next_col, "left") to the sucessors
            if cleaning, copy the map, and the lin and col to the new State, change the copy map tile to clean (state 0) and append VacuumWorldGeneric(new_map, lin, col, "clean") to the sucessors
        5 - `return sucessors`
        """

        sucessors = []

        # ir para a esquerda
        if self.col - 1 >= 0:
            new = self.mapa.copy()
            sucessors.append(VacuumWorldGeneric(new, self.lin, self.col-1, 'esq'))

        # ir para a direita
        if self.col + 1 <= self.col_max:
            new = self.mapa.copy()
            sucessors.append(VacuumWorldGeneric(new, self.lin, self.col+1, 'dir'))

        # ir para cima
        if self.lin - 1 >=0:
            new = self.mapa.copy()
            sucessors.append(VacuumWorldGeneric(new, self.lin-1, self.col, 'cima'))

        # ir para baixo
        if self.lin + 1 <= self.lin_max:
            new = self.mapa.copy()
            sucessors.append(VacuumWorldGeneric(new, self.lin+1, self.col, 'baixo'))

        # limpar
        if self.mapa[self.lin][self.col] == 1:
            new = self.mapa.copy()
            new[self.lin][self.col] = 0 
            sucessors.append(VacuumWorldGeneric(new, self.lin, self.col, 'limpar'))

        return sucessors
    
    def is_goal(self):
        """
        Is goal method checks if a State is the goal state,
        so it returns True if it is the goal state and False otherwise

        In the VacuumWorldGeneric, the goal is achieve if all tiles 
        in the `mapa` variable is clean, that is, if all tiles is equal to zero
        otherwise it is false

        obs: sometimes is easier and faster to check if something is false,
        then to check if it is true 
        """
        for y in self.mapa:
            for x in y:
                if x != 0:
                    return False
        return True

    def h(self):
        """
        h() function is called Heuristic,
        Heuristics are an estimate cost mapped from the current state
        to the goal state

        It helps the search algorithm to reach the goal state "easier"
        than testing all possibilities at random

        The rule is, the lower the heuristics, the nearer from the goal!
        
        In the VacuumWorldGeneric a great heuristic is the number of cells
        that are not clean in the state.

        The less cells dirt, the nearer from the goal state.
        """
        count = 0
        for y in self.mapa:
            for x in y:
                if x != 0:
                    count = count + 1
        return count
    
    def description(self):
        """
        Descriptions helps undestand the enviroment the State are basing from,
        In the Vacuum World Generic, the agent is trying to maitain clean all times
        from the world
        """
        return "Agente genérico para o problema do aspirador de pó"
    
    def cost(self):
        """
        The cost() function is the function that dictitate how much resources the agent will use
        to reach this State given an specific action

        In the vaccum world generic, moving left, right, up, down or cleaning all costs `1`
        """
        return 1
    
    def env(self):
        """
        env stands for Enviroment, it is a function that describes the actual
        state using it's variables.

        In the Vacuum World Generic the enviroment is a combination of it's
        map, the agent's position in the line and the agent's position in the column
        """
        return str(self.mapa)+" "+str(self.lin)+" "+str(self.col)


def convert_file_to_map(file_map_path):
    """
    Simple function that translate .txt file to a numpy array 
    """
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