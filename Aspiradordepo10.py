from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from aigyminsper.search.Graph import State
import copy

casa = [["Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo"],
        ["Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo"],
        ["Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo"],
        ["Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo"],
        ["Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo"],
        ["Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo"],
        ["Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo"],
        ["Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo"],
        ["Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo"],
        ["Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo", "Sujo"],]


class Aspiradordepo10(State):

    def __init__(self, op, pos_x, pos_y, casa):
        # You must use this name for the operator!
        self.operator = op
        self.pos_x = pos_x 
        self.pos_y = pos_y
        self.casa = casa
    
    def successors(self):
        successors = []
        
        # limpar
        if self.casa[self.pos_x][self.pos_y] == "Sujo":
            temp = copy.deepcopy(self.casa)
            temp[self.pos_x][self.pos_y] = "Limpo"
            successors.append(Aspiradordepo10("LIMPAR", self.pos_x, self.pos_y, temp))

        # baixo
        if self.pos_x < 9:
            successors.append(Aspiradordepo10("BAIXO", self.pos_x + 1, self.pos_y, self.casa))

        # cima
        if self.pos_x > 0:
            successors.append(Aspiradordepo10("CIMA", self.pos_x - 1, self.pos_y, self.casa))

        # direita
        if self.pos_y < 9:
            successors.append(Aspiradordepo10("DIREITA", self.pos_x, self.pos_y + 1, self.casa))

        # esquerda
        if self.pos_y > 0:
            successors.append(Aspiradordepo10("ESQUERDA", self.pos_x, self.pos_y - 1, self.casa))

        return successors
    
    def is_goal(self):
        if (self.casa == [["Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo"],
        ["Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo"],
        ["Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo"],
        ["Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo"],
        ["Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo"],
        ["Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo"],
        ["Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo"],
        ["Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo"],
        ["Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo"],
        ["Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo", "Limpo"]]) and (self.pos_x == 0 and self.pos_y == 0):
            return True
        else:
            return False
    
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
        return (f"Posição robÔ:{self.pos_x}  {self.pos_y}, Casa:{self.casa}")


def main():
    print('Busca em profundidade iterativa')
    state = Aspiradordepo10("", 0, 0, casa)
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state, trace=False)
    #trace apresenta a arvore inteira de possibilidades
    if result != None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()