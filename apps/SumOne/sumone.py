from aigyminsper.search.SearchAlgorithms import BuscaLargura
from aigyminsper.search.SearchAlgorithms import BuscaProfundidade
from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from aigyminsper.search.Graph import State
from datetime import datetime

class SumOne(State):

    def __init__(self, n, op, g):
        self.operator = op
        self.number = n
        self.goal = g

    def successors(self):
        successors = []
        if self.number < self.goal:
            successors.append(SumOne(self.number+1, "+1 ", self.goal))
            successors.append(SumOne(self.number+2, "+2 ", self.goal))
        return successors

    def is_goal(self):
        if self.goal == self.number:
            return True
        return False

    def description(self):
        return "Este é um agente simples que sabe somar 1 e 2"

    def cost(self):
        return 1

    def env(self):
        return self.number

def main():
    objetivo = int(input('Digite o valor objetivo: '))
    state = SumOne(1, '', objetivo)
    # algorithm = BuscaLargura()
    #algorithm = BuscaProfundidade()
    algorithm = BuscaProfundidadeIterativa()
    start_time = datetime.now()
    result = algorithm.search(state)
    end_time = datetime.now()
    print(f'Tempo de processamento = {end_time - start_time}')
    if result != None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()