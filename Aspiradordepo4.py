from aigyminsper.search.SearchAlgorithms import BuscaLargura
from aigyminsper.search.Graph import State
import time

class Aspiradordepo4(State):

    def __init__(self, op, pos, esq_sup, dir_sup, esq_inf, dir_inf):
        # You must use this name for the operator!
        self.operator = op
        self.pos = pos 
        self.esq_sup = esq_sup
        self.dir_sup = dir_sup
        self.esq_inf = esq_inf
        self.dir_inf = dir_inf

    
    def successors(self):
        successors = []

        if self.pos == "ESQ SUP":
            successors.append(Aspiradordepo4("BAIXO", "ESQ INF", self.esq_sup, self.dir_sup, self.esq_inf, self.dir_inf))
            successors.append(Aspiradordepo4("DIREITA", "DIR SUP", self.esq_sup, self.dir_sup, self.esq_inf, self.dir_inf))
            successors.append(Aspiradordepo4("LIMPAR", self.pos, "LIMPO", self.dir_sup, self.esq_inf, self.dir_inf))

        if self.pos == "DIR SUP":
            successors.append(Aspiradordepo4("BAIXO", "DIR INF", self.esq_sup, self.dir_sup, self.esq_inf, self.dir_inf))
            successors.append(Aspiradordepo4("ESQUERDA", "ESQ SUP", self.esq_sup, self.dir_sup, self.esq_inf, self.dir_inf))
            successors.append(Aspiradordepo4("LIMPAR", self.pos, self.esq_sup, "LIMPO", self.esq_inf, self.dir_inf))

        if self.pos == "ESQ INF":
            successors.append(Aspiradordepo4("CIMA", "ESQ SUP", self.esq_sup, self.dir_sup, self.esq_inf, self.dir_inf))
            successors.append(Aspiradordepo4("DIREITA", "DIR INF", self.esq_sup, self.dir_sup, self.esq_inf, self.dir_inf))
            successors.append(Aspiradordepo4("LIMPAR", self.pos, self.esq_sup, self.dir_sup, "LIMPO", self.dir_inf))

        if self.pos == "DIR INF":
            successors.append(Aspiradordepo4("CIMA", "DIR SUP", self.esq_sup, self.dir_sup, self.esq_inf, self.dir_inf))
            successors.append(Aspiradordepo4("ESQUERDA", "ESQ INF", self.esq_sup, self.dir_sup, self.esq_inf, self.dir_inf))
            successors.append(Aspiradordepo4("LIMPAR", self.pos, self.esq_sup, self.dir_sup, self.esq_inf, "LIMPO"))
    

        return successors
    
    def is_goal(self):
        if (self.dir_sup == "LIMPO") and (self.esq_sup == "LIMPO") and (self.dir_inf == "LIMPO") and (self.esq_inf == "LIMPO") and (self.pos == "ESQ SUP"):
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
        return (f"Posição robô:{self.pos}, Quarto esquerdo superior:{self.esq_sup}, Quarto direito superior:{self.dir_sup}, Quarto esquerdo inferior:{self.esq_inf}, Quarto direito inferior:{self.dir_inf}")



def main():
    print('Busca em profundidade iterativa')
    state = Aspiradordepo4("", "ESQ SUP", "SUJO", "SUJO", "SUJO", "SUJO")
    algorithm = BuscaLargura()
    inicial = time.time()
    result = algorithm.search(state, trace=False)
    final = time.time()
    #trace apresenta a arvore inteira de possibilidades
    if result != None:
        print('Achou!')
        print(result.show_path())
        print(final-inicial)
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()