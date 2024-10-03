from unittest import result
from aicode.search.SearchAlgorithms import AEstrela
from aicode.search.Graph import State
import math

class Puzzle8(State):

    objetivo = [[1,2,3],[8,0,4],[7,6,5]]

    def __init__(self, tabuleiro, op):
        self.operator = op
        self.tabuleiro = tabuleiro
    
    def onde_esta_N(tabuleiro, n):
        for i in range(0,3):
            for j in range(0,3):
                if tabuleiro[i][j] == n:
                    return i, j

    def copia_tabuleiro(self):
        resultado = [[0,0,0],[0,0,0],[0,0,0]]
        for i in range(0,3):
            for j in range(0,3):
                resultado[i][j] = self.tabuleiro[i][j]
        return resultado

    def sucessors(self):
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
        for i in range(0,3):
            for j in range(0,3):
                if self.tabuleiro[i][j] != self.objetivo[i][j]:
                    return False
        return True
    
    def description(self):
        return "8 Puzzle"
    
    def cost(self):
        return 1

    def print(self):
        return str(self.operator)
    
    def env(self):
        return str(self.tabuleiro)

    def h(self):
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