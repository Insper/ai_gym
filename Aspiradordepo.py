from aigyminsper.search.SearchAlgorithms import BuscaLargura
from aigyminsper.search.Graph import State

class Aspiradordepo(State):

    def __init__(self, op, pos, sit_esq, sit_dir):
        # You must use this name for the operator!
        self.operator = op
        self.pos = pos 
        self.sit_esq = sit_esq
        self.sit_dir = sit_dir
    
    def successors(self):
        successors = []

        successors.append(Aspiradordepo("esq", "ESQ", self.sit_esq, self.sit_dir))
        successors.append(Aspiradordepo("dir", "DIR", self.sit_esq, self.sit_dir))

        if self.pos == "ESQ":
            successors.append(Aspiradordepo("limpar", self.pos, "LIMPO", self.sit_dir))

        else:
            successors.append(Aspiradordepo("limpar", self.pos, self.sit_esq, "LIMPO")) 

        return successors
    
    def is_goal(self):
        if (self.sit_dir == "LIMPO") and (self.sit_esq == "LIMPO") and (self.pos == "ESQ"):
            return True
    
    def description(self):
        return "Descrição do problema"
    
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
        return (f"Posição robÔ:{self.pos}, Quarto esquerdo:{self.sit_esq}, Quarto direito:{self.sit_dir}")



def main():
    print('Busca em profundidade iterativa')
    state = Aspiradordepo("", "DIR", "SUJO", "SUJO")
    algorithm = BuscaLargura()
    result = algorithm.search(state, trace=True)
    if result != None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()