from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from aigyminsper.search.SearchAlgorithms import BuscaCustoUniforme
from aigyminsper.search.SearchAlgorithms import BuscaGananciosa
from aigyminsper.search.SearchAlgorithms import BuscaLargura
from aigyminsper.search.Graph import State
import time
import networkx as nx
import csv

class Map(State):

    @staticmethod
    def createArea():
        #
        # TODO mover a definicao do mapa de uma forma hard-coded para para leitura
        # a partir de um arquivo, similar ao que é feito no metodo createHeuristics()
        # 
        Mapa = {
            'a':[(3,'b'),(6,'c')],
            'b':[(3,'a'),(3,'h'),(3,'k')],
            'c':[(6,'a'),(2,'g'),(3,'d'),(2,'o'),(2,'p')],
            'd':[(3,'c'),(1,'f'),(1,'e')],
            'e':[(2,'i'),(1,'f'),(1,'d'),(14,'m')],
            'f':[(1,'g'),(1,'e'),(1,'d')],
            'g':[(2,'c'),(1,'f'),(2,'h')],
            'h':[(2,'i'),(2,'g'),(3,'b'),(4,'k')],
            'i':[(2,'e'),(2,'h')],
            'l':[(1,'k')],
            'k':[(1,'l'),(3,'n'),(4,'h'),(3,'b')],
            'm':[(2,'n'),(1,'x'),(14,'e')],
            'n':[(2,'m'),(3,'k')],
            'o':[(2,'c')],
            'p':[(2,'c')],
            'x':[(1,'m')]
            }

    def __init__(self, op, custo, lugar, goal):
        self.operator = op
        self.lugar_atual = lugar
        self.custo = custo
        self.goal = goal

    def successors(self):
        sucessors = []
        m = Map.createArea()
        for i in m[self.lugar_atual]:
            sucessors.append(Map(f'ir p/ {i[1]}', i[0], i[1], self.goal))
        return sucessors
    
    def is_goal(self):
        return (self.lugar_atual == self.goal)

    def description(self):
        return "Um mapa para procurar"

    def cost(self):
        return self.custo

    def print(self):
        return str(self.operator)

    def env(self):
        return (f'Atual: {self.lugar_atual} Custo: {self.custo} Destino: {self.goal} Operador: {self.operator}')

def main():

    inicial = input("Digite o ponto inicial: ")
    final = input("Digite o ponto final: ")

    state = Map('', 0, inicial, final)
    algorithm = BuscaLargura()
    ts = time.time()
    result = algorithm.search(state, trace=True)
    tf = time.time()
    if result != None:
        print('O caminho é:' + str(result.show_path()))
        print('O custo é:' + str(result.g()))
    else:
        print('Nao achou solucao')
    print('Tempo de processamento em segundos: ' + str(tf-ts))
    print('O custo da solucao eh: '+str(result.g))

if __name__ == '__main__':
    main()