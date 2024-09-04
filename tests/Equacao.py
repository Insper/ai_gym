from aigyminsper.search.CSPAlgorithms import SubidaMontanha, SubidaMontanhaEstocastico
from aigyminsper.search.Graph import State
import numpy as np

class Equacao(State):

    def __init__(self, op, number):
        self.number = number
        self.operator = op

    def successors(self):
        successors = []
        successors.append(Equacao('+', self.number + 0.001))
        successors.append(Equacao('-', self.number - 0.001))
        return successors
    
    def is_goal(self):
        return self._equation(self.number) >= 29.4
    
    def description(self):
        return "Esta implementação deve encontrar o valor de x que maximiza a equação: f(x) = sin(x) + x + x*sin(x), onde x é um valor entre 0 e 15"
    
    def cost(self):
        return 1
    
    def env(self):
        return str(self.number)
    
    def _equation(self, x):
        return np.sin(x) + x + x * np.sin(x)

    def h(self):
        return 30 - self._equation(self.number)
    
    def randomState(self):
        self.number = np.random.uniform(0, 15)

def main():
    n = int(input('Digite o valor de n: '))
    state = Equacao('', n)
    algorithm = SubidaMontanhaEstocastico()
    result = algorithm.search(state, trace=True)
    if result != None:
        print(f'O valor de x que maximiza a função é {result.env()}')
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()