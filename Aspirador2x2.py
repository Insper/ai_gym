from aigyminsper.search.SearchAlgorithms import BuscaLargura
from aigyminsper.search.graph import State

class AspiradorPo(State):

    def __init__(self, op, posicao, s_esq_cima, s_dir_cima, s_esq_baixo, s_dir_baixo):
        self.operator = op
        # DIR; ESQ
        self.posicao_robo = posicao
        # LIMPO; SUJO
        self.situacao_esq_cima = s_esq_cima
        # LIMPO; SUJO
        self.situacao_dir_cima = s_dir_cima
        # LIMPO; SUJO
        self.situacao_esq_baixo = s_esq_baixo
        # LIMPO; SUJO
        self.situacao_dir_baixo = s_dir_baixo
        

    def sucessors(self):
        sucessors = []

        # esq_cima
        if self.posicao_robo == 'DIR_CIMA':
            # fazer ele se movimentar apenas para a esquerda cima ou direita baixo
            sucessors.append(AspiradorPo("esq","ESQ_CIMA",self.situacao_esq_cima,self.situacao_dir_cima,self.situacao_esq_baixo,self.situacao_dir_baixo))
            sucessors.append(AspiradorPo("baixo","DIR_BAIXO",self.situacao_esq_cima,self.situacao_dir_cima,self.situacao_esq_baixo,self.situacao_dir_baixo))
            # limpar
            sucessors.append(AspiradorPo("limpar",self.posicao_robo,self.situacao_esq_cima,'LIMPO',self.situacao_esq_baixo,self.situacao_dir_baixo))

        elif self.posicao_robo == 'ESQ_CIMA':
            # fazer ele se movimentar apenas para a direita cima ou esquerda baixo
            sucessors.append(AspiradorPo("dir","DIR_CIMA",self.situacao_esq_cima,self.situacao_dir_cima,self.situacao_esq_baixo,self.situacao_dir_baixo))
            sucessors.append(AspiradorPo("baixo","ESQ_BAIXO",self.situacao_esq_cima,self.situacao_dir_cima,self.situacao_esq_baixo,self.situacao_dir_baixo))
            # limpar
            sucessors.append(AspiradorPo("limpar",self.posicao_robo,'LIMPO',self.situacao_dir_cima,self.situacao_esq_baixo,self.situacao_dir_baixo))

        elif self.posicao_robo == 'DIR_BAIXO':
            # fazer ele se movimentar apenas para a esquerda baixo ou direita cima
            sucessors.append(AspiradorPo("esq","ESQ_BAIXO",self.situacao_esq_cima,self.situacao_dir_cima,self.situacao_esq_baixo,self.situacao_dir_baixo))
            sucessors.append(AspiradorPo("cima","DIR_CIMA",self.situacao_esq_cima,self.situacao_dir_cima,self.situacao_esq_baixo,self.situacao_dir_baixo))
            # limpar
            sucessors.append(AspiradorPo("limpar",self.posicao_robo,self.situacao_esq_cima,self.situacao_dir_cima,self.situacao_esq_baixo,'LIMPO'))

        elif self.posicao_robo == 'ESQ_BAIXO':
            # fazer ele se movimentar apenas para a direita baixo ou esquerda cima
            sucessors.append(AspiradorPo("dir","DIR_BAIXO",self.situacao_esq_cima,self.situacao_dir_cima,self.situacao_esq_baixo,self.situacao_dir_baixo))
            sucessors.append(AspiradorPo("cima","ESQ_CIMA",self.situacao_esq_cima,self.situacao_dir_cima,self.situacao_esq_baixo,self.situacao_dir_baixo))
            # limpar
            sucessors.append(AspiradorPo("limpar",self.posicao_robo,self.situacao_esq_cima,self.situacao_dir_cima,'LIMPO',self.situacao_dir_baixo))

        return sucessors

    def is_goal(self):
        return self.situacao_esq_cima == 'LIMPO' and self.situacao_dir_cima == 'LIMPO' and self.situacao_esq_baixo == 'LIMPO' and self.situacao_dir_baixo == 'LIMPO' and self.posicao_robo == 'DIR_CIMA'

    def cost(self):
        return 1

    def description(self):
        return "Implementa um aspirador de po para 4 quartos"

    def env(self):
        return self.operator


def main():
    state = AspiradorPo("","ESQ_CIMA","SUJO","SUJO","SUJO","SUJO")
    algorithm = BuscaLargura()
    result = algorithm.search(state)
    if result != None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()