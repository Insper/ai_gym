from aigyminsper.search.SearchAlgorithms import AEstrela
from aigyminsper.search.Graph import State
import math
import copy
class Knuth(State):
    def __init__(self, operator, numero, objetivo):
        self.operator = operator
        self.numero = numero
        self.objetivo = objetivo


    def sucessors(self):
        sucessors = []
        # fact
        if not self.numero > self.objetivo * 100:
            if type(self.numero) == int :
                sucessors.append(Knuth("fact",math.factorial(self.numero),self.objetivo))
        # sqrt
        if not self.numero < self.objetivo / 100:
            sucessors.append(Knuth("sqrt",math.sqrt(self.numero),self.objetivo))
        # floor
        if not type(self.numero) == int :
            sucessors.append(Knuth("floor",math.floor(self.numero),self.objetivo))
        return sucessors
    
    def h(self):
        node = self.numero
        goal = self.objetivo
        diff = abs(node - goal)
        if node > goal:
            return diff
        elif node < goal:
            return abs(goal - math.sqrt(node))
        else:
            return diff

    
    def is_goal(self):
        if self.numero == self.objetivo:
            return True
        else:
            return False
    
    def description(self):
        return "Knuth's problem"
    
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
        return str(self.numero) + self.operator

def main(operator, numero, objetivo):
    state = Knuth(operator, numero, objetivo)
    algorithm = AEstrela()
    result = algorithm.search(state,trace=True,pruning=False)

    if result != None:
        print(result.show_path())
        return result.show_path()
    else:
        print("Não foi possível encontrar uma solução.")

if __name__ == "__main__":
    main("",4,5)