from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from aigyminsper.search.Graph import State

class Grafo(State):

    def __init__(self, op, anterior, posicao, final, grafo):
        self.operator = op
        self.anterior = anterior
        self.posicao_robo = posicao
        self.grafo = grafo
        self.final = final

    def successors(self):
        successors = []

        for i in self.grafo[self.posicao_robo]:
            successors.append(Grafo(f'{self.posicao_robo} -> {i}', self.posicao_robo, i, self.final, self.grafo))


        return successors
    
 

    def cost(self):
        costs = {
            'A -> B': 1, 
            'A -> C': 10,
            'B -> A': 1,  
            'B -> C': 1,
            'B -> D': 1,
            'C -> A': 10,
            'C -> B': 1,
            'C -> E': 5,
            'D -> B': 1,
            'D -> E': 3,
            'E -> C': 5,
            'E -> D': 3,
            'E -> F': 1,
            'E -> G': 2,
            'F -> E': 1,
            'F -> G': 1,
            'G -> E': 2,
            'G -> F': 1, 
        }
        
        transition_key = f'{self.anterior} -> {self.posicao_robo}'
        cost = costs.get(transition_key, 1)
        print(f'Custo de {transition_key} é {cost}')

        return cost

    def is_goal(self):
        if self.posicao_robo == self.final:
            return True
        return False

    def description(self):
        return "Encontrar o menor caminho entre dois pontos de interesse (POI)"

    def env(self):
        return self.operator+"  "+self.posicao_robo


def main():
    state = Grafo('', '', 'A', 'E', {'A': ['B', 'C'], 'B': ['A', 'C', 'D'], 'C': ['A', 'B', 'E'], 'D': ['B', 'E'], 'E': ['F','G','C','D'], 'F': ['G','E'], 'G': ['E','F']})
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state, trace=True)
    if result != None:
        print('Achou!')
        print(result.g)
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()