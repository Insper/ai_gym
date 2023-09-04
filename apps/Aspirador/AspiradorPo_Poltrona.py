from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from aigyminsper.search.Graph import State

class AspiradorPo(State):

    # armchairs = {'ESQ': [True, 'desvirado'], 'DIR': [True,['desvirado']], 'CIMA': [True,['desvirado']], 'BAIXO': [True,['desvirado']]}
    def __init__(self, op, posicao, s_esq, s_dir, s_cima, s_baixo, armchairs: dict):
        self.operator = op
        self.posicao_robo = posicao
        self.situacao_esq = s_esq
        self.situacao_dir = s_dir
        self.situacao_cima = s_cima
        self.situacao_baixo = s_baixo
        self.armchairs = armchairs
        self.preconditions = {
            "ESQ": ["CIMA","BAIXO","DIR"],
            "DIR": ["CIMA","BAIXO","ESQ"],
            "CIMA": ["ESQ","DIR"],
            "BAIXO": ["ESQ","DIR"],
        }
                              
    def successors(self):
        successors = []
        # movimentar
        for direction in self.preconditions[self.posicao_robo]:
            successors.append(AspiradorPo(direction.lower(), direction, self.situacao_esq, self.situacao_dir, self.situacao_cima, self.situacao_baixo, self.armchairs))
        
        # # virar a poltrona
        # if self.armchairs['ESQ'][0] and self.situacao_esq == 'SUJO' and self.posicao_robo == 'ESQ' and self.armchairs['ESQ'][1] == 'desvirado':
        #     novo = copy.deepcopy(self.armchairs)
        #     novo['ESQ'][1] = 'virado'
        #     successors.append(AspiradorPo("virar poltrona",self.posicao_robo,self.situacao_esq,self.situacao_dir,self.situacao_cima, self.situacao_baixo, novo))

        # if self.armchairs['DIR'][0] and self.situacao_dir == 'SUJO' and self.posicao_robo == 'DIR' and self.armchairs['DIR'][1] == 'desvirado':
        #     novo = copy.deepcopy(self.armchairs)
        #     novo['DIR'][1] = 'virado'
        #     successors.append(AspiradorPo("virar poltrona",self.posicao_robo,self.situacao_esq,self.situacao_dir,self.situacao_cima, self.situacao_baixo, novo))

        # if self.armchairs['CIMA'][0] and self.situacao_cima == 'SUJO' and self.posicao_robo == 'CIMA' and self.armchairs['CIMA'][1] == 'desvirado':
        #     novo = copy.deepcopy(self.armchairs)
        #     novo['CIMA'][1] = 'virado'
        #     successors.append(AspiradorPo("virar poltrona",self.posicao_robo,self.situacao_esq,self.situacao_dir,self.situacao_cima, self.situacao_baixo, novo))

        # if self.armchairs['BAIXO'][0] and self.situacao_baixo == 'SUJO' and self.posicao_robo == 'BAIXO' and self.armchairs['BAIXO'][1] == 'desvirado':
        #     novo = copy.deepcopy(self.armchairs)
        #     novo['BAIXO'][1] = 'virado'
        #     successors.append(AspiradorPo("virar poltrona",self.posicao_robo,self.situacao_esq,self.situacao_dir,self.situacao_cima, self.situacao_baixo, novo))


        # #limpar, se tiver poltrona
        # if self.armchairs['ESQ'][0] and self.armchairs['ESQ'][1] == 'virado' and self.situacao_esq == 'SUJO' and self.posicao_robo == 'ESQ':
        #     successors.append(AspiradorPo("limpar",self.posicao_robo,'LIMPO',self.situacao_dir,self.situacao_cima, self.situacao_baixo, self.armchairs))
            
        # if self.armchairs['DIR'][0] and self.armchairs['DIR'][1] == 'virado' and self.situacao_dir == 'SUJO' and self.posicao_robo == 'DIR':
        #     successors.append(AspiradorPo("limpar",self.posicao_robo,self.situacao_esq,'LIMPO',self.situacao_cima, self.situacao_baixo, self.armchairs))

        # if self.armchairs['CIMA'][0] and self.armchairs['CIMA'][1] == 'virado' and self.situacao_cima == 'SUJO' and self.posicao_robo == 'CIMA':
        #     successors.append(AspiradorPo("limpar",self.posicao_robo,self.situacao_esq,self.situacao_dir,'LIMPO', self.situacao_baixo, self.armchairs))


        # if self.armchairs['BAIXO'][0] and self.armchairs['BAIXO'][1] == 'virado' and self.situacao_baixo == 'SUJO' and self.posicao_robo == 'BAIXO':
        #     successors.append(AspiradorPo("limpar",self.posicao_robo,self.situacao_esq,self.situacao_dir,self.situacao_cima, 'LIMPO', self.armchairs))



        # #desvirar poltrona
        # if self.armchairs['ESQ'][0] and self.armchairs['ESQ'][1] == 'virado' and self.situacao_esq == 'LIMPO' and self.posicao_robo == 'ESQ':
        #     novo = copy.deepcopy(self.armchairs)
        #     novo['ESQ'][1] = 'desvirado'
        #     successors.append(AspiradorPo("desvirar poltrona",self.posicao_robo,self.situacao_esq,self.situacao_dir,self.situacao_cima, self.situacao_baixo, novo))
        # if self.armchairs['DIR'][0] and self.armchairs['DIR'][1] == 'virado' and self.situacao_dir == 'LIMPO' and self.posicao_robo == 'DIR':
        #     novo = copy.deepcopy(self.armchairs)
        #     novo['DIR'][1] = 'desvirado'
        #     successors.append(AspiradorPo("desvirar poltrona",self.posicao_robo,self.situacao_esq,self.situacao_dir,self.situacao_cima, self.situacao_baixo, novo))
        # if self.armchairs['CIMA'][0] and self.armchairs['CIMA'][1] == 'virado' and self.situacao_cima == 'LIMPO' and self.posicao_robo == 'CIMA':
        #     novo = copy.deepcopy(self.armchairs)
        #     novo['CIMA'][1] = 'desvirado'
        #     successors.append(AspiradorPo("desvirar poltrona",self.posicao_robo,self.situacao_esq,self.situacao_dir,self.situacao_cima, self.situacao_baixo, novo))
        # if self.armchairs['BAIXO'][0] and self.armchairs['BAIXO'][1] == 'virado' and self.situacao_baixo == 'LIMPO' and self.posicao_robo == 'BAIXO':
        #     novo = copy.deepcopy(self.armchairs)
        #     novo['BAIXO'][1] = 'desvirado'
        #     successors.append(AspiradorPo("desvirar poltrona",self.posicao_robo,self.situacao_esq,self.situacao_dir,self.situacao_cima, self.situacao_baixo, novo))
        # if self.armchairs['ESQ'][0] and self.situacao_esq == 'SUJO' and self.posicao_robo == 'ESQ':
        #     self.armchairs['ESQ'][1] = 'virado'
        #     successors.append(AspiradorPo("virar poltrona",self.posicao_robo,'POLTRONA VIRADA',self.situacao_dir,self.situacao_cima, self.situacao_baixo, self.armchairs))
        # if self.armchairs['DIR'][0] and self.situacao_dir == 'SUJO' and self.posicao_robo == 'DIR':
        #     self.armchairs['DIR'][1] = 'virado'
        #     successors.append(AspiradorPo("virar poltrona",self.posicao_robo,self.situacao_esq,'POLTRONA VIRADA',self.situacao_cima, self.situacao_baixo, self.armchairs))
        # if self.armchairs['CIMA'][0] and self.situacao_cima == 'SUJO' and self.posicao_robo == 'CIMA':
        #     self.armchairs['CIMA'][1] = 'virado'
        #     successors.append(AspiradorPo("virar poltrona",self.posicao_robo,self.situacao_esq,self.situacao_dir,'POLTRONA VIRADA', self.situacao_baixo, self.armchairs))
        # if self.armchairs['BAIXO'][0] and    self.situacao_baixo == 'SUJO' and self.posicao_robo == 'BAIXO':
        #     self.armchairs['BAIXO'][1] = 'virado'
        #     successors.append(AspiradorPo("virar poltrona",self.posicao_robo,self.situacao_esq,self.situacao_dir,self.situacao_cima, 'POLTRONA VIRADA', self.armchairs))


        # #limpar poltrona
        # if self.armchairs['ESQ'][1] == 'virado' and self.situacao_esq == 'SUJO' and self.posicao_robo == 'ESQ':
        #     successors.append(AspiradorPo("limpar",self.posicao_robo,'LIMPO',self.situacao_dir,self.situacao_cima, self.situacao_baixo, self.armchairs))
        #     self.armchairs['ESQ'][1] = 'desvirado'
        # if self.armchairs['DIR'][1] == 'virado' and self.situacao_dir == 'SUJO' and self.posicao_robo == 'DIR':
        #     successors.append(AspiradorPo("limpar",self.posicao_robo,self.situacao_esq,'LIMPO',self.situacao_cima, self.situacao_baixo, self.armchairs))
        #     self.armchairs['DIR'][1] = 'desvirado'
        # if self.armchairs['CIMA'][1] == 'virado' and self.situacao_cima == 'SUJO' and self.posicao_robo == 'CIMA':
        #     successors.append(AspiradorPo("limpar",self.posicao_robo,self.situacao_esq,self.situacao_dir,'LIMPO', self.situacao_baixo, self.armchairs))
        #     self.armchairs['CIMA'][1] = 'desvirado'
        # if self.armchairs['BAIXO'][1] == 'virado' and self.situacao_baixo == 'SUJO' and self.posicao_robo == 'BAIXO':
        #     successors.append(AspiradorPo("limpar",self.posicao_robo,self.situacao_esq,self.situacao_dir,self.situacao_cima, 'LIMPO', self.armchairs))
        #     self.armchairs['BAIXO'][1] = 'desvirado'


        # #desvirar poltrona
        # if self.armchairs['ESQ'][1] == 'desvirado' and self.situacao_esq == 'LIMPO' and self.posicao_robo == 'ESQ':
        #     successors.append(AspiradorPo("desvirar poltrona",self.posicao_robo,'POLTRONA DESVIRADA',self.situacao_dir,self.situacao_cima, self.situacao_baixo, self.armchairs))
        # if self.armchairs['DIR'][1] == 'desvirado' and self.situacao_dir == 'LIMPO' and self.posicao_robo == 'DIR':
        #     successors.append(AspiradorPo("desvirar poltrona",self.posicao_robo,self.situacao_esq,'POLTRONA DESVIRADA',self.situacao_cima, self.situacao_baixo, self.armchairs))
        # if self.armchairs['CIMA'][1] == 'desvirado' and self.situacao_cima == 'LIMPO' and self.posicao_robo == 'CIMA':
        #     successors.append(AspiradorPo("desvirar poltrona",self.posicao_robo,self.situacao_esq,self.situacao_dir,'POLTRONA DESVIRADA', self.situacao_baixo, self.armchairs))
        # if self.armchairs['BAIXO'][1] == 'desvirado' and self.situacao_baixo == 'LIMPO' and self.posicao_robo == 'BAIXO':
        #     successors.append(AspiradorPo("desvirar poltrona",self.posicao_robo,self.situacao_esq,self.situacao_dir,self.situacao_cima, 'POLTRONA DESVIRADA', self.armchairs))
            
        return successors

        
    
    def is_goal(self):
        if all(status == 'LIMPO' for status in [self.situacao_dir, self.situacao_esq, self.situacao_cima, self.situacao_baixo]) and (self.armchairs['ESQ'][1] == 'desvirado' and self.armchairs['DIR'][1] == 'desvirado' and self.armchairs['CIMA'][1] == 'desvirado' and self.armchairs['BAIXO'][1] == 'desvirado') and self.posicao_robo == 'ESQ':
            return True
        return False 

    def cost(self):
        return 1

    def description(self):
        return "Implementa um aspirador de po para 4 quartos com poltronas"

    def env(self):
        return self.operator + ' ' + self.posicao_robo + ' ' + self.situacao_esq + ' ' + str(self.armchairs)


# def main():
#     armchairs = {'ESQ': [True, 'desvirado'], 'DIR': [True,'desvirado'], 'CIMA': [True,'desvirado'], 'BAIXO': [True,'desvirado']}
#     state = AspiradorPo('', 'ESQ', 'SUJO', 'LIMPO', 'LIMPO', 'LIMPO', armchairs)
#     algorithm = BuscaProfundidadeIterativa()
#     result = algorithm.search(state, True)
#         return self.operator


def main():
    armchairs = {'ESQ': [True, 'desvirado'], 'DIR': [True,['desvirado']], 'CIMA': [True,['desvirado']], 'BAIXO': [True,['desvirado']]}
    state = AspiradorPo('', 'ESQ', 'SUJO', 'LIMPO', 'LIMPO', 'LIMPO', armchairs)
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state, False)
    if result is not None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()
