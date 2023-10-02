# arquivo com a solução para o problema das Rotas.# arquivo com a solução para o problema do Mapa.

from aigyminsper.search.SearchAlgorithms import BuscaCustoUniforme
from aigyminsper.search.Graph import State
import time

class Map(State):

    def __init__(self, city, cost, op, goal, terminal_carga, cidade_estrategica, visited=None):
        self.city = city
        self.cost_value = cost
        self.operator = op
        self.goal = goal
        self.terminal_carga = terminal_carga
        self.cidade_estrategica = cidade_estrategica

        if visited is None:
            self.visited = []
        else:
            self.visited = visited

    def successors(self):
        successors = []
        neighbors = Map.area[self.city]

        for next_city in neighbors:
            if next_city[1] not in self.visited:
                new_visited = self.visited + [self.city]
                successors.append(Map(next_city[1], next_city[0], next_city[1], self.goal, self.terminal_carga, self.cidade_estrategica, new_visited))
        
        return successors
    

    def is_goal(self):
        goal_reached = self.city == self.goal
        if self.terminal_carga:
            goal_reached = goal_reached and (('Limeira' in self.visited) or ('Sorocaba' in self.visited))
        if self.cidade_estrategica:
            goal_reached = goal_reached and (('Ubatuba' in self.visited) or ('São Carlos' in self.visited))
        
        return goal_reached


    def description(self):
        return "Implementação do problema: caminho entre cidades"

    def cost(self):
        return self.cost_value  * 0.5

    def print(self):
        return str(self.operator)

    def env(self):
        return self.city

    def h(self):
        return int(Map.g.edges[self.city,self.goal]['distance'])
    
    @staticmethod
    def createArea():
        Map.area = {
            'São Paulo':[(59,'Jundiaí'),(72,'Santos'), (92,'São José dos Campos'), (104,'Sorocaba')],
            'Sorocaba':[(89,'Campinas'),(93,'Jundiaí'), (104,'São Paulo')],
            'Campinas': [(39,'Jundiaí') ,(59,'Limeira'), (70,'Piracicaba'), (142,'São Carlos'), (89,'Sorocaba')],
            'Limeira': [(59,'Campinas'), (28,'Rio Claro')],
            'Jundiaí': [(39,'Campinas'), (59,'São Paulo'), (93,'Sorocaba')],
            'Santos': [(72,'São Paulo'), (238,'Ubatuba')],
            'Ubatuba': [(238,'Santos'), (139,'São José dos Campos'), (97,'Taubaté')],
            'Taubaté': [(43,'São José dos Campos'), (97,'Ubatuba')],
            'Rio Claro': [(186,'Bauru'), (28,'Limeira'), (62,'São Carlos')],
            'Bauru': [(194,'Piracicaba'),(186,'Rio Claro'), (152,'São Carlos')],
            'Piracicaba': [(194,'Bauru'), (70,'Campinas')],
            'São Carlos': [(152,'Bauru'), (142,'Campinas'), (62,'Rio Claro')],
            'São José dos Campos': [(92,'São Paulo'), (43,'Taubaté'), (139,'Ubatuba')]
            }
        

def main():

    Map.createArea()
    state = Map('Rio Claro', 0, 'Rio Claro', 'Piracicaba', True, False)
    algorithm = BuscaCustoUniforme()
    ts = time.time()
    result = algorithm.search(state, trace=True)
    tf = time.time()
    if result != None:
        print(result.show_path())
    else:
        print('Nao achou solucao')
    print('Tempo de processamento em milisegundos: ' + str(tf-ts))
    print('O custo da solucao eh: '+str(result.g))

if __name__ == '__main__':
    main()