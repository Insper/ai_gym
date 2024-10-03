from aigyminsper.search.search_algorithms import AEstrela, BuscaGananciosa, BuscaLargura, BuscaProfundidade, BuscaProfundidadeIterativa
from aigyminsper.search.graph import State
import numpy
import sys

class VacuumWorldGeneric(State):

    def __init__(self, mapa, lin, col, op):
        self.mapa = mapa
        self.lin_max = self.mapa.shape[0]-1
        self.col_max = self.mapa.shape[1]-1
        self.lin = lin
        self.col = col
        self.operator = op
    
    def successors(self):
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
        for y in self.mapa:
            for x in y:
                if x != 0:
                    return False
        return True

    def h(self):
        count = 0
        for y in self.mapa:
            for x in y:
                if x != 0:
                    count = count + 1
        return count
    
    def description(self):
        return "Agente genérico para o problema do aspirador de pó"
    
    def cost(self):
        return 1
    
    def env(self):
        return str(self.mapa)+" "+str(self.lin)+" "+str(self.col)


def convert_file_to_map(file_map_path):
    return numpy.loadtxt(open(file_map_path, "rb"), delimiter=";")

def main(file_map_path, lin, col):
    mapa = convert_file_to_map(file_map_path)
    print(mapa)
    state = VacuumWorldGeneric(mapa, lin, col, '')

    #print('Busca em AEstrela')
    #algorithm = AEstrela()
    
    print('Busca Profundidade Iterativa')
    algorithm = BuscaProfundidadeIterativa()
    
    result = algorithm.search(state)
    if result != None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))