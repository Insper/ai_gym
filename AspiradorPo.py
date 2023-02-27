from aigyminsper.search.SearchAlgorithms import BuscaLargura
from aigyminsper.search.Graph import State

class AspiradorPo(State):

    def __init__(self, op, posicao, s_esq, s_dir):
        self.operator = op
        # DIR; ESQ
        self.posicao_robo = posicao
        # LIMPO; SUJO
        self.situacao_esq = s_esq
        # LIMPO; SUJO
        self.situacao_dir = s_dir

    def sucessors(self):
        sucessors = []
        # esq
        sucessors.append(AspiradorPo("esq","ESQ",self.situacao_esq,self.situacao_dir))
        # dir
        sucessors.append(AspiradorPo("dir","DIR",self.situacao_esq,self.situacao_dir))
        # limpar
        if self.posicao_robo == 'ESQ':
            sucessors.append(AspiradorPo("limpar",self.posicao_robo,'LIMPO',self.situacao_dir))
        else:
            sucessors.append(AspiradorPo('limpar',self.posicao_robo,self.situacao_esq,'LIMPO'))

        return sucessors

    def is_goal(self):
        if (self.situacao_dir == 'LIMPO') and (self.situacao_esq == 'LIMPO') and (self.posicao_robo == "ESQ"):
            return True
        return False 

    def cost(self):
        return 1

    def description(self):
        return "Implementa um aspirador de po para 2 quartos"

    def env(self):
        return self.operator


def main():
    state = AspiradorPo('','ESQ','LIMPO','SUJO')
    algorithm = BuscaLargura()
    result = algorithm.search(state)
    if result != None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()