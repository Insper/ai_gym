# arquivo com a solução para o problema do Mapa.

from aigyminsper.search.SearchAlgorithms import BuscaProfundidade
from aigyminsper.search.Graph import State
import time

class Map(State):

    def __init__(self, city, cost, op, goal):
        self.city = city
        self.cost_value = cost
        self.operator = op
        self.goal = goal

    def successors(self):
        successors = []
        neighbors = Map.area[self.city]
        for next_city in neighbors:
            successors.append(Map(next_city[1], next_city[0], next_city[1], self.goal))
        return successors

    def is_goal(self):
        return (self.city == self.goal)

    def description(self):
        return "Implementação do problema: caminho entre cidades"

    def cost(self):
        return self.cost_value

    def print(self):
        return str(self.operator)

    def env(self):
        return self.city

    def h(self):
        return int(Map.g.edges[self.city,self.goal]['distance'])

    @staticmethod
    def createArea():
        Map.area = {
            'São Paulo':[(59,'Jundiaí'), (72,'Santos'), (104,'Sorocaba'), (131,'Taubaté')],
            'Sorocaba':[(89,'Campinas'),(93,'Jundiaí'), (104,'São Paulo')],
            'Campinas': [(39,'Jundiaí'), (59,'Limeira'), (89,'Sorocaba')],
            'Limeira': [(59,'Campinas')],
            'Jundiaí': [(39,'Campinas'), (59,'São Paulo'), (93,'Sorocaba')],
            'Santos': [(72,'São Paulo'), (238,'Ubatuba')],
            'Ubatuba': [(238,'Santos'), (97,'Taubaté')],
            'Taubaté': [(131,'São Paulo'), (97,'Ubatuba')]
            }
        
        

def main():

    Map.createArea()
    state = Map('São Paulo', 0, '', 'Taubaté')
    algorithm = BuscaProfundidade()
    ts = time.time()
    result = algorithm.search(state, trace=True, m=50)
    tf = time.time()
    if result != None:
        print(result.show_path())
    else:
        print('Nao achou solucao')
    print('Tempo de processamento em milisegundos: ' + str(tf-ts))
    print('O custo da solucao eh: '+str(result.g))

if __name__ == '__main__':
    main()