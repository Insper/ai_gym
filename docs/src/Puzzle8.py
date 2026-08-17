from unittest import result
from aigyminsper.search.search_algorithms import AEstrela
from aigyminsper.search.graph import State
import math

class Puzzle8(State):

    objetivo = [[1,2,3],[8,0,4],[7,6,5]]

    def __init__(self, tabuleiro, op):
        """
        In the init method, we set the initial variables:
        tabuleiro: A square NumPy array representing where each of the numbers is on the tabuleiro
            ex: [[2, 1, 3],
                 [0, 8, 4]
                 [6, 5, 7]]
            note: It is not a list of lists, but rather a NumPy array!! and 0 represents no number
        op: the operation that led to the current state
            ex: If the state has just started, op = ' '; if the blank space moved right, op='direita', if left, op='esquerda' and so on
        """
        super().__init__(op)
        self.tabuleiro = tabuleiro
    
    def onde_esta_N(tabuleiro, n):
        """
        This helper function searches where a number is on the tabuleiro
        """
        for i in range(0,3):
            for j in range(0,3):
                if tabuleiro[i][j] == n:
                    return i, j

    def copia_tabuleiro(self):
        """
        This helper function create a copy of the tabuleiro
        """
        resultado = [[0,0,0],[0,0,0],[0,0,0]]
        for i in range(0,3):
            for j in range(0,3):
                resultado[i][j] = self.tabuleiro[i][j]
        return resultado

    def successors(self):
        """
        When generating the successors, we follow the flow below:
        1 - We create an empty list of successors `sucessors = []`
        2 - We list the possible actions and ask: what conditions must be met to execute an action?
        3 - We create conditional statements for each action
        4 - When a condition is satisfied, we create a new state with the new characteristics resulting from the action and add it to the successors
        5 - We return the successors

        In Puzzle8, the flow would be
        1 - `sucessors = []`
        2 - possible action: move the empty space (left, right, up, down)
        3 - to move up the empty space can't be on the first line
            to move down the empty space can't be on the last line
            to move left the empty space can't be on the first column
            to move right the empty space can't be on the last column
        4 - when the empty space move, we copy the map and swap the empty space location with the number on the direction it moved
            then we append the State with this new tabuleiro, and the operation used in the condition
                ex: append Puzzle8(new_tabuleiro, 'esquerda')
        5 - `return sucessors`
        """
        sucessors = []
        lin, col = Puzzle8.onde_esta_N(self.tabuleiro, 0)
        # zero para cima
        if lin > 0 and self.operator != 'baixo':
            novo = self.copia_tabuleiro()
            temp = self.tabuleiro[lin-1][col]
            novo[lin][col] = temp
            novo[lin-1][col] = 0
            sucessors.append(Puzzle8(novo,'cima'))
        # zero para baixo
        if lin < 2 and self.operator != 'cima':
            novo = self.copia_tabuleiro()
            temp = self.tabuleiro[lin+1][col]
            novo[lin][col] = temp
            novo[lin+1][col] = 0
            sucessors.append(Puzzle8(novo,"baixo"))
        # zero para esquerda
        if col > 0 and self.operator != 'direita':
            novo = self.copia_tabuleiro()
            temp = self.tabuleiro[lin][col-1]
            novo[lin][col] = temp
            novo[lin][col-1] = 0
            sucessors.append(Puzzle8(novo,"esquerda"))
        # zero para direita
        if col < 2 and self.operator != 'esquerda':
            novo = self.copia_tabuleiro()
            temp = self.tabuleiro[lin][col+1]
            novo[lin][col] = temp
            novo[lin][col+1] = 0
            sucessors.append(Puzzle8(novo,"direita"))
        return sucessors
    
    def is_goal(self):
        """
        Is goal method checks if a State is the goal state,
        so it returns True if it is the goal state and False otherwise

        In the Puzzle8, the goal state is the configuration where the tabuleiro must be exactly as below
        tabuleiro = [[1,2,3],
                     [8,0,4],
                     [7,6,5]]

        This is, the variable objective set on the beginning of the class
        """
        for i in range(0,3):
            for j in range(0,3):
                if self.tabuleiro[i][j] != self.objetivo[i][j]:
                    return False
        return True
    
    def description(self):
        """
        Descriptions helps undestand the enviroment the State are basing from,

        In the 8 Puzzle the game is well know and self descripted
        """
        return "8 Puzzle"
    
    def cost(self):
        """
        The cost() function is the function that dictitate how much resources the agent will use
        to reach this State given an specific action

        In the Puzzle8, moving the empty space to any direction cost the same (1)
        """
        
        return 1
    
    def env(self):
        """
        env stands for Enviroment, it is a function that describes the actual
        state using it's variables.

        The description the State can be sumerized by its tabuleiro
        """
        return str(self.tabuleiro)

    def h(self):
        """
        h() function is called Heuristic,
        Heuristics are an estimate cost mapped from the current state
        to the goal state

        It helps the search algorithm to reach the goal state "easier"
        than testing all possibilities at random

        The rule is, the lower the heuristics, the nearer from the goal!
        
        In the Puzzle8, the h1() and h2() are diferent aproachs
        h1() says that the less cells in the wrong place, the nearer from the goal
        h2() says that the nearer each cell is from it's desired location, the nearer from the goal

        These two heuristics represents diferent visualizations of the problem,
        as many others can also exist
        """
        return self.h1()
        #return self.h2()

    #
    # quantidade de pecas fora do lugar
    #
    def h1(self):
        count = 0
        if self.tabuleiro[0][0] != 1:
            count = count + 1
        if self.tabuleiro[0][1] != 2:
            count = count + 1
        if self.tabuleiro[0][2] != 3:
            count = count + 1
        if self.tabuleiro[1][0] != 8:
            count = count + 1
        if self.tabuleiro[1][1] != 0:
            count = count + 1
        if self.tabuleiro[1][2] != 4:
            count = count + 1
        if self.tabuleiro[2][0] != 7:
            count = count + 1
        if self.tabuleiro[2][1] != 6:
            count = count + 1
        if self.tabuleiro[2][2] != 5:
            count = count + 1
        return count
    
    #
    # distancia euclidiana
    #
    def h2(self):
        count = 0
        for num in range(0,8):
            lin_ideal, col_ideal = Puzzle8.onde_esta_N(self.objetivo, num)
            lin_real, col_real = Puzzle8.onde_esta_N(self.tabuleiro, num)
            count = count + math.sqrt((lin_ideal - lin_real)**2 + (col_ideal - col_real)**2)
        return count

    #
    # Deve-se calcular a quantidade de inversões necessárias para ordenar 
    # certa sequência numérica, determinado por Possível a quantidade de 
    # inversões pares e Impossível a quantidade de inversões ímpares.
    # 
    # referência: https://pt.stackoverflow.com/questions/333702/como-verificar-se-o-sliding-puzzle-%C3%A9-solucion%C3%A1vel 
    #
    def tem_solucao(tabuleiro):
        """
        Helper function to check if the given initial state has a solution,
        as in this problem, some initial states are unsolvables
        """
        count = 0
        lista = []
        for lin in range(0,3):
            for col in range(0,3):
                if tabuleiro[lin][col] != 0:
                    lista.append(tabuleiro[lin][col])
        for i in range(0,8):
            for j in range(i+1,8):
                if lista[i] > lista[j]:
                    count = count + 1
        if count % 2:
            return True
        else:
            return False
        
    def show_path(self):
        """
        Helper function to use the search algorithm AEstrela
        """
        algorithm = AEstrela()
        if not Puzzle8.tem_solucao(self.tabuleiro):
            return 'Nao tem solucao' 
        result = algorithm.search(self)
        if result != None:
            return result.show_path()
        else:
            return 'Nao achou solucao'


def main():
    tabuleiro_trivial = [[1,2,3],[8,4,0],[7,6,5]]
    tabuleiro_facil = [[8,1,3],[0,7,2],[6,5,4]]
    tabuleiro_facil2 = [[8,1,3],[7,0,2],[6,5,4]]
    tabuleiro_facil3 = [[0,1,3],[8,7,2],[6,5,4]]
    tabuleiro_dificil1 = [[7,8,6],[2,3,5],[1,4,0]]
    tabuleiro_dificil2 = [[7,8,6],[2,3,5],[0,1,4]]
    tabuleiro_dificil3 = [[8,3,6],[7,5,4],[2,1,0]]
    tabuleiro_dificil4 = [[3,1,2],[5,4,8],[0,6,7]]
    tabuleiro_impossivel1 = [[3,4,8],[1,2,5],[7,0,6]]
    tabuleiro_impossivel2 = [[5,4,0],[6,1,8],[7,3,2]]
    tabuleiro_impossivel3 = [[1,7,2],[3,9,5],[6,4,8]]
    
    state = Puzzle8(tabuleiro_facil3,'')
    print(state.show_path())

if __name__ == '__main__':
    main()