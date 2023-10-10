from aigyminsper.search.SearchAlgorithms import BuscaLargura
from aigyminsper.search.Graph import State

class Aspiradordepoltrona(State):

    def __init__(self, op, pos, cima, esq, dir, baixo):
        self.operator = op
        self.pos = pos #cima, esq, dir, baixo
        self.cima = cima #sujo, limpo, sujo_sofa, limpo_sofa, sujo_sofa_virado, limpo_sofa_virado
        self.esq = esq
        self.dir = dir
        self.baixo = baixo

    def successors(self):
        successors = []
        # ir para cima, baixo, dir, esq
        if self.pos == 'cima':
            successors.append(Aspiradordepoltrona('ir esq', 'esq', self.cima, self.esq, self.dir, self.baixo))
            successors.append(Aspiradordepoltrona('ir dir', 'dir', self.cima, self.esq, self.dir, self.baixo))
        if self.pos == 'baixo': 
            successors.append(Aspiradordepoltrona('ir esq', 'esq', self.cima, self.esq, self.dir, self.baixo))
            successors.append(Aspiradordepoltrona('ir dir', 'dir', self.cima, self.esq, self.dir, self.baixo))
        if self.pos == 'dir':
            successors.append(Aspiradordepoltrona('ir cima', 'cima', self.cima, self.esq, self.dir, self.baixo))
            successors.append(Aspiradordepoltrona('ir baixo', 'baixo', self.cima, self.esq, self.dir, self.baixo))
            successors.append(Aspiradordepoltrona('ir esq', 'esq', self.cima, self.esq, self.dir, self.baixo))
        if self.pos == 'esq':
            successors.append(Aspiradordepoltrona('ir cima', 'cima', self.cima, self.esq, self.dir, self.baixo))
            successors.append(Aspiradordepoltrona('ir baixo', 'baixo', self.cima, self.esq, self.dir, self.baixo))
            successors.append(Aspiradordepoltrona('ir dir', 'dir', self.cima, self.esq, self.dir, self.baixo))

        # limpar
        if self.cima == 'sujo' and self.pos == 'cima':
            successors.append(Aspiradordepoltrona('limpar', self.pos, 'limpo', self.esq, self.dir, self.baixo))
        if self.esq == 'sujo' and self.pos == 'esq':
            successors.append(Aspiradordepoltrona('limpar', self.pos, self.cima, 'limpo', self.dir, self.baixo))
        if self.dir == 'sujo' and self.pos == 'dir':
            successors.append(Aspiradordepoltrona('limpar', self.pos, self.cima, self.esq, 'limpo', self.baixo))
        if self.baixo == 'sujo' and self.pos == 'baixo':
            successors.append(Aspiradordepoltrona('limpar', self.pos, self.cima, self.esq, self.dir, 'limpo'))
        
        if self.cima == 'sujo_sofa_virado' and self.pos == 'cima':
            successors.append(Aspiradordepoltrona('limpar', self.pos, 'limpo_sofa_virado', self.esq, self.dir, self.baixo))
        if self.esq == 'sujo_sofa_virado' and self.pos == 'esq':
            successors.append(Aspiradordepoltrona('limpar', self.pos, self.cima, 'limpo_sofa_virado', self.dir, self.baixo))
        if self.dir == 'sujo_sofa_virado' and self.pos == 'dir':
            successors.append(Aspiradordepoltrona('limpar', self.pos, self.cima, self.esq, 'limpo_sofa_virado', self.baixo))
        if self.baixo == 'sujo_sofa_virado' and self.pos == 'baixo':
            successors.append(Aspiradordepoltrona('limpar', self.pos, self.cima, self.esq, self.dir, 'limpo_sofa_virado'))
        
        # virar sofa
        if self.cima == 'sujo_sofa' and self.pos == 'cima':
            successors.append(Aspiradordepoltrona('virar sofa', self.pos, 'sujo_sofa_virado', self.esq, self.dir, self.baixo))
        if self.esq == 'sujo_sofa' and self.pos == 'esq':
            successors.append(Aspiradordepoltrona('virar sofa', self.pos, self.cima, 'sujo_sofa_virado', self.dir, self.baixo))
        if self.dir == 'sujo_sofa' and self.pos == 'dir':
            successors.append(Aspiradordepoltrona('virar sofa', self.pos, self.cima, self.esq, 'sujo_sofa_virado', self.baixo))
        if self.baixo == 'sujo_sofa' and self.pos == 'baixo':
            successors.append(Aspiradordepoltrona('virar sofa', self.pos, self.cima, self.esq, self.dir, 'sujo_sofa_virado'))

        # desvirar sofa
        if self.cima == 'limpo_sofa_virado' and self.pos == 'cima':
            successors.append(Aspiradordepoltrona('desvirar sofa', self.pos, 'limpo_sofa', self.esq, self.dir, self.baixo))
        if self.esq == 'limpo_sofa_virado' and self.pos == 'esq':
            successors.append(Aspiradordepoltrona('desvirar sofa', self.pos, self.cima, 'limpo_sofa', self.dir, self.baixo))
        if self.dir == 'limpo_sofa_virado' and self.pos == 'dir': 
            successors.append(Aspiradordepoltrona('desvirar sofa', self.pos, self.cima, self.esq, 'limpo_sofa', self.baixo))
        if self.baixo == 'limpo_sofa_virado' and self.pos == 'baixo':
            successors.append(Aspiradordepoltrona('desvirar sofa', self.pos, self.cima, self.esq, self.dir, 'limpo_sofa'))

        return successors

    def is_goal(self):  
        return (self.cima == 'limpo' or self.cima == 'limpo_sofa') and (self.esq == 'limpo' or self.esq == 'limpo_sofa') and (self.dir == 'limpo' or self.dir == 'limpo_sofa') and (self.baixo == 'limpo' or self.baixo == 'limpo_sofa') and self.pos == 'cima'

    def description(self):
        return ""

    def cost(self):
        return 1

    def env(self):
        return ""       

def main():
    state = Aspiradordepoltrona("", "cima", "limpo_sofa", "sujo_sofa", "sujo", "sujo_sofa")
    algorithm = BuscaLargura()
    result = algorithm.search(state)
    if result != None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()