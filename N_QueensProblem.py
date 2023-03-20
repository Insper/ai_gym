#
# Implements a solution for N-queens problem, where N could 
# be any number between 4 and 10.
#

from aigyminsper.search.CSPAlgorithms import SubidaMontanha
from aigyminsper.search.CSPAlgorithms import SubidaMontanhaEstocastico
from aigyminsper.search.Graph import State
import numpy as np
import random
import time

class N_QueensProblem(State):

    def __init__(self, size, board):
        self.size = size
        self.board = board

    def env(self):
        return self.board
    
    def sucessors(self):
        sucessores = []
        for i in range(0,self.size):
            for j in range(0,self.size):
                if(self.board[i][j] == 1):
                    #move up
                    if((i - 1) >=0 and self.board[i-1][j] == 0):
                        temp = self.board.copy()
                        temp[i][j] = 0
                        temp[i-1][j] = 1
                        sucessores.append(N_QueensProblem(self.size, temp))
                    #move down
                    if((i + 1) < self.size and self.board[i+1][j] == 0):
                        temp = self.board.copy()
                        temp[i][j] = 0
                        temp[i+1][j] = 1
                        sucessores.append(N_QueensProblem(self.size, temp))
                    #move left
                    #if((j - 1) >=0 and self.board[i][j-1] == 0):
                    #    temp = self.board.copy()
                    #    temp[i][j] = 0
                    #    temp[i][j-1] = 1
                    #    sucessores.append(N_QueensProblem(self.size, temp))
                    #move right
                    #if((j + 1) < self.size and self.board[i][j+1] == 0):
                    #    temp = self.board.copy()
                    #    temp[i][j] = 0
                    #    temp[i][j+1] = 1
                    #    sucessores.append(N_QueensProblem(self.size, temp))
        return sucessores
                      
    def is_goal(self):
        if self.h() == 0:
            return True
        return False
    
    def description(self):
        return "Queens Problem"
    
    def cost(self):
        return 1
    
    def h(self):
        h = 0

        for i in range(0,self.size):
            for j in range(0,self.size):
                
                if self.board[i][j] == 1:

                    # linha
                    for k in range(0,self.size):
                        if self.board[i][k] == 1 and k != j:
                            h += 1

                    # coluna
                    for k in range(0,self.size):
                        if self.board[k][j] == 1 and k != i:
                            h += 1

                    # diagonal
                    for k in range(0,self.size):
                        for l in range(0,self.size):
                            if self.board[k][l] == 1 and (k != i or l != j):
                                if abs(k-i) == abs(l-j):
                                    h += 1
        return h

    def randomState(self):
        self.board = self.generateBoard()
        while not self.validBoard():
            self.board = self.generateBoard()

    def generateBoard(self):
        board = np.zeros( (self.size,self.size) )
        for i in range(0,self.size):
            line = random.randrange(0, self.size)
            #column = random.randrange(0, self.size)
            board[line,i] = 1
        return board

    def validBoard(self):
        if np.sum(self.board) != self.size:
            return False
        return True

def main():
    N = int(input("Digite o tamanho do tabuleiro (4-10): "))
    state = N_QueensProblem(size = N, board = None)
    state.randomState()
    algorithm = SubidaMontanhaEstocastico()
    print("Initial state with h = "+str(state.h()))
    start = time.time()
    result = algorithm.search(state)
    end = time.time()
    if result != None:
        print(result.env())
        print('Final state with h = '+str(result.h()))
        print('Duration in seconds = '+str(end-start))
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()