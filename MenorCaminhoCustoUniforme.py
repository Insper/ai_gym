from aigyminsper.search.SearchAlgorithms import BuscaCustoUniforme
from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from aigyminsper.search.Graph import State
import pandas as pd

class MenorCaminho(State):

    def __init__(self, op, pos, dest):
        # You must use this name for the operator!
        self.operator = op
        self.pos = pos 
        self.dest = dest
    
    def successors(self):
        successors = []

        if self.pos == 'A':
            successors.append(MenorCaminho("de A ir p/ b", "B", self.dest))
            successors.append(MenorCaminho("de A ir p/ c", "C", self.dest))

        if self.pos == 'B':
            successors.append(MenorCaminho("de B ir p/ a", "A", self.dest))
            successors.append(MenorCaminho("de B ir p/ c", "C", self.dest))
            successors.append(MenorCaminho("de B ir p/ d", "D", self.dest))

        if self.pos == 'C':
            successors.append(MenorCaminho("de C ir p/ a", "A", self.dest))
            successors.append(MenorCaminho("de C ir p/ b", "B", self.dest))
            successors.append(MenorCaminho("de C ir p/ e", "E", self.dest))

        if self.pos == 'D':
            successors.append(MenorCaminho("de D ir p/ b", "B", self.dest))
            successors.append(MenorCaminho("de D ir p/ e", "E", self.dest))

        if self.pos == 'E':
            successors.append(MenorCaminho("de E ir p/ c", "C", self.dest))
            successors.append(MenorCaminho("de E ir p/ d", "D", self.dest))
            successors.append(MenorCaminho("de E ir p/ f", "F", self.dest))
            successors.append(MenorCaminho("de E ir p/ g", "G", self.dest))

        if self.pos == 'F':
            successors.append(MenorCaminho("de F ir p/ g", "G", self.dest))
            successors.append(MenorCaminho("de F ir p/ e", "E", self.dest))

        if self.pos == 'G':
            successors.append(MenorCaminho("de G ir p/ e", "E", self.dest))
            successors.append(MenorCaminho("de G ir p/ f", "F", self.dest))
        
        return successors
    
    def is_goal(self):
        return self.pos == self.dest
    
    def description(self):
        return "Encontrar menor caminho"

    def cost(self):
        if self.operator == "de A ir p/ b":
            return 1
        if self.operator == "de A ir p/ c":
            return 10
        if self.operator == "de B ir p/ a":
            return 1
        if self.operator == "de B ir p/ c":
            return 1
        if self.operator == "de B ir p/ d":
            return 1
        if self.operator == "de C ir p/ a":
            return 10
        if self.operator == "de C ir p/ b":
            return 1
        if self.operator == "de C ir p/ e":
            return 5
        if self.operator == "de D ir p/ b":
            return 1
        if self.operator == "de D ir p/ e":
            return 3
        if self.operator == "de E ir p/ d":
            return 3
        if self.operator == "de E ir p/ c":
            return 5
        if self.operator == "de E ir p/ f":
            return 1
        if self.operator == "de E ir p/ g":
            return 2
        if self.operator == "de F ir p/ g":
            return 1
        if self.operator == "de F ir p/ e":
            return 1
        if self.operator == "de G ir p/ e":
            return 2
        if self.operator == "de G ir p/ f":
            return 1

    def env(self):
        return (f"Posição atual:{self.pos}, Destino:{self.dest}")

def main():
    print('Busca em profundidade iterativa')
    origem = input('Digite a origem: ')
    destino = input('Digite o destino: ')
    state = MenorCaminho("", origem, destino)
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state, trace=True)
    if result is not None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Não achou solucao')

if __name__ == '__main__':
    main()
