from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from aigyminsper.search.Graph import State

class AspiradorPo(State):

    def __init__(self, op, posicao, s_esq, s_dir, s_cima, s_baixo):
        # You must use this name for the operator!
        self.operator = op
        # DIR; ESQ; CIMA; BAIXO
        self.posicao_robo = posicao
        # LIMPO; SUJO
        self.situacao_esq = s_esq
        # LIMPO; SUJO
        self.situacao_dir = s_dir
        # LIMPO; SUJO
        self.situacao_cima = s_cima
        # LIMPO; SUJO
        self.situacao_baixo = s_baixo

    
    def successors(self):
        successors = []
        # esq
        successors.append(AspiradorPo("esq","ESQ",self.situacao_esq,self.situacao_dir,self.situacao_cima, self.situacao_baixo))

        # dir
        successors.append(AspiradorPo("dir","DIR",self.situacao_esq,self.situacao_dir,self.situacao_cima, self.situacao_baixo))

        # cima
        successors.append(AspiradorPo("cima","CIMA",self.situacao_esq,self.situacao_dir,self.situacao_cima, self.situacao_baixo))
       
        # baixo
        successors.append(AspiradorPo("baixo","BAIXO",self.situacao_esq,self.situacao_dir,self.situacao_cima, self.situacao_baixo))
        
        # limpar
        if self.posicao_robo == 'ESQ':
            successors.append(AspiradorPo("limpar",self.posicao_robo,'LIMPO',self.situacao_dir,self.situacao_cima, self.situacao_baixo))
        elif self.posicao_robo == 'DIR':
            successors.append(AspiradorPo('limpar',self.posicao_robo,self.situacao_esq,'LIMPO',self.situacao_cima, self.situacao_baixo))
        elif self.posicao_robo == 'CIMA':
            successors.append(AspiradorPo('limpar',self.posicao_robo,self.situacao_esq, self.situacao_dir,'LIMPO', self.situacao_baixo))
        else:
            successors.append(AspiradorPo('limpar',self.posicao_robo,self.situacao_esq,self.situacao_dir,self.situacao_cima,'LIMPO'))

        
        return successors
    
    def is_goal(self):
        if (self.situacao_dir == 'LIMPO') and (self.situacao_esq == 'LIMPO') and (self.situacao_cima == 'LIMPO') and (self.situacao_baixo == 'LIMPO') and (self.posicao_robo == "ESQ"):
            return True
        return False 

    def cost(self):
        return 1

    def description(self):
        return "Implementa um aspirador de po para 4 quartos"

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
        return self.operator


def main():
    state = AspiradorPo('','ESQ','SUJO','SUJO','SUJO','SUJO')
    #state = AspiradorPo('','ESQ','LIMPO','LIMPO')
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state)
    if result != None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()