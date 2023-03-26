from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from aigyminsper.search.SearchAlgorithms import BuscaCustoUniforme
from aigyminsper.search.SearchAlgorithms import BuscaGananciosa
from aigyminsper.search.SearchAlgorithms import BuscaLargura
from aigyminsper.search.Graph import State
import time
import networkx as nx
import csv

class Map(State):

    def __init__(self, city, cost, op, goal):
        self.city = city
        self.cost_value = cost
        self.operator = op
        self.goal = goal
    
    def sucessors(self):
        sucessors = []
        neighbors = Map.area[self.city]
        for next_city in neighbors:
            sucessors.append(Map(next_city[1], next_city[0], next_city[1], self.goal))
        return sucessors
    
    def is_goal(self):
        return (self.city == self.goal)
    
    def description(self):
        return "Um mapa para procurar"
    
    def cost(self):
        return self.cost_value
    
    def print(self):
        return str(self.operator)
    
    def env(self):
        return self.city
    
    def h(self):
        return int(Map.g.edges[self.city,self.goal]['distance'])
        #return random.randint(1,10)
        #return 1

    @staticmethod
    def createArea():
        Map.area = {
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
        
    @staticmethod
    def createHeuristics():
        Map.g = nx.Graph()
        f = csv.reader(open("MapHeuristics.csv","r"))
        for row in f: 
            Map.g.add_edge(row[0],row[1], distance = row[2])

def main():

    Map.createArea()
    Map.createHeuristics()

    #state = Map('i', 0, 'i', 'o')
    state = Map('b', 0, 'b', 'o')
    #state = Map('i', 0, 'i', 'x')
    #algorithm = BuscaLargura()
    #algorithm = BuscaCustoUniforme()
    algorithm = BuscaGananciosa()
    ts = time.time()
    result = algorithm.search(state, trace=True)
    tf = time.time()
    if result != None:
        print(result.show_path())
    else:
        print('Nao achou solucao')
    print('Tempo de processamento em segundos: ' + str(tf-ts))
    print('O custo da solucao eh: '+str(result.g))

if __name__ == '__main__':
    main()
