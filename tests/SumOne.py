from aigyminsper.search.SearchAlgorithms import BuscaLargura
from aigyminsper.search.Graph import State

class SumOne(State):

    def __init__(self, n, op, g):
        # You must use this name for the operator!
        self.operator = op
        self.number = n
        self.goal = g
    
    def sucessors(self):
        sucessors = []
        sucessors.append(SumOne(self.number+1, "+1 ", self.goal))
        sucessors.append(SumOne(self.number+2, "+2 ", self.goal))
        return sucessors
    
    def is_goal(self):
        if self.goal == self.number:
            return True
        return False
    
    def description(self):
        return "This is a very simple agent that is able to sum 1 or 2 to reach a specific number."
    
    def cost(self):
        return 1


    def env(self):
        #
        # IMPORTANTE: este método não deve apenas retornar uma descrição do environment, mas 
        # deve também retornar um valor que descreva aquele nodo em específico. Pois 
        # esta representação é utilizada para verificar se um nodo deve ou ser adicionado 
        # na lista de abertos.
        #
        # Exemplos de especificações adequadas: 
        # - para o problema do soma 1 e 2: return str(self.number)+"#"+str(self.cost)
        # - para o problema das cidades: return self.city+"#"+str(self.cost())
        #
        # Exemplos de especificações NÃO adequadas: 
        # - para o problema do soma 1 e 2: return str(self.number)
        # - para o problema das cidades: return self.city
        #
        return self.number


def main():
    state = SumOne(1, '', 23)
    algorithm = BuscaLargura()
    result = algorithm.search(state, trace=True)
    if result != None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()