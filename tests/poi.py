from aigyminsper.search.Graph import State
from aigyminsper.search.SearchAlgorithms import BuscaLargura, BuscaProfundidadeIterativa
from aigyminsper.search.SearchAlgorithms import BuscaProfundidade,BuscaCustoUniforme

class Poi(State):

    def __init__(self, op, origem, poi, goal):
        self.operator = op
        self.origem = origem
        self.poi = poi
        self.goal = goal

    def successors(self):
        successors = []
        if self.poi == 'A':
            successors.append(Poi('ir p/ b',self.poi,'B',self.goal))
            successors.append(Poi('ir p/ c',self.poi,'C',self.goal))
        if self.poi == 'B':
            successors.append(Poi('ir p/ c',self.poi,'C',self.goal))
            successors.append(Poi('ir p/ d',self.poi,'D',self.goal))
            successors.append(Poi('ir p/ a',self.poi,'A',self.goal))
        if self.poi == 'C':
            successors.append(Poi('ir p/ e',self.poi,'E',self.goal))
            successors.append(Poi('ir p/ a',self.poi,'A',self.goal))
            successors.append(Poi('ir p/ b',self.poi,'B',self.goal))
        if self.poi == 'D':
            successors.append(Poi('ir p/ b',self.poi,'B',self.goal))
            successors.append(Poi('ir p/ e',self.poi,'E',self.goal))
        if self.poi == 'E':
            successors.append(Poi('ir p/ c',self.poi,'C',self.goal))
            successors.append(Poi('ir p/ d',self.poi,'D',self.goal))
            successors.append(Poi('ir p/ f',self.poi,'F',self.goal))
            successors.append(Poi('ir p/ g',self.poi,'G',self.goal))
        if self.poi == 'F':
            successors.append(Poi('ir p/ e',self.poi,'E',self.goal))
            successors.append(Poi('ir p/ g',self.poi,'G',self.goal))
        if self.poi == 'G':
            successors.append(Poi('ir p/ e',self.poi,'E',self.goal))
            successors.append(Poi('ir p/ f',self.poi,'F',self.goal))
        return successors
    
    def cost(self):
        if (self.origem == 'C' and self.poi == 'E') or (self.origem == 'E' and self.poi == 'C'):
            return 5
        elif (self.origem == 'A' and self.poi == 'C') or (self.origem == 'C' and self.poi == 'A'):
            return 10
        elif (self.origem == 'D' and self.poi == 'E') or (self.origem == 'E' and self.poi == 'D'):
            return 3
        elif (self.origem == 'E' and self.poi == 'G') or (self.origem == 'G' and self.poi == 'E'):
            return 2
        else:
            return 1
    
    def is_goal(self):
        return self.poi == self.goal
    
    def env(self):
        return f'pai: {self.origem} - atual: {self.poi}'
    
    def description(self):
        return "Encontrar o menor caminho entre dois pontos de interesse (PÒI)"
    
def main():
    origem = input('Digite o seu local de origem ')
    destino = input('Digite o seu local de destino ')
    state = Poi('',origem,origem,destino)
    #algorithm = BuscaLargura()
    #algorithm = BuscaProfundidade()
    #result = algorithm.search(state, m=3)
    #algorithm = BuscaProfundidadeIterativa()

    #algorithm = BuscaCustoUniforme()
    result = algorithm.search(state, trace=True)

    if result != None:
        print(f'O caminho é {result.show_path()}')
        print(f'O custo do caminho é {result.g}')
    else:
        print('Não achou caminho')

if __name__ == '__main__':
    main()    