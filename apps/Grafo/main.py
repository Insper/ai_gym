from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from aigyminsper.search.Graph import State

class Grafo(State):

    def __init__(self, op,posicao, final, grafo):
        self.operator = op
        self.posicao_robo = posicao
        self.grafo = grafo
        self.final = final

    def successors(self):
        successors = []
        for i in self.grafo[self.posicao_robo]:
            successors.append(Grafo(f'{self.posicao_robo} -> {i}', i, self.final, self.grafo))
        return successors
    
    def is_goal(self):
        if self.posicao_robo == self.final:
            return True
        return False

    def cost(self):
        return 1

    def description(self):
        return "Encontrar o menor caminho entre dois pontos de interesse (POI)"

    def env(self):
        return self.operator


def main():
    state = Grafo('', 'B', 'E', {'A': ['B', 'C'], 'B': ['A', 'C', 'D'], 'C': ['A', 'B', 'E'], 'D': ['B', 'E'], 'E': ['F','G','C','D'], 'F': ['G','E'], 'G': ['E','F']})
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state)
    if result != None:
        print('Achou!')
        print(result.show_path())
        print(result.g) #Mostra o custo do caminho
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()