from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from aigyminsper.search.Graph import State

class ProblemSpecification(State):

    def __init__(self, op):
        # You must use this name for the operator!
        self.operator = op
        #TODO
    
    def sucessors(self):
        sucessors = []
        #TODO
        return sucessors
    
    def is_goal(self):
        pass
    
    def description(self):
        return "Descrição do problema"
    
    def cost(self):
        return 1

    def print(self):
        #
        # Usado para imprimir a solução encontrada. 
        # O PATH do estado inicial até o final.
        return str(self.operator)
    
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
        None


def main():
    print('Busca em profundidade iterativa')
    state = ProblemSpecification('')
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state)
    if result != None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()