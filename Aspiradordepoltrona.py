from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from aigyminsper.search.Graph import State

class Aspiradordepoltrona(State):

    def __init__(self, op, pos, cima, esq, dir, baixo, poltronas):
        # You must use this name for the operator!
        self.operator = op
        self.pos = pos 
        self.cima = cima
        self.esq = esq
        self.dir = dir
        self.baixo = baixo
        self.poltronas = poltronas

    
    def successors(self):
        successors = []

        if self.pos == "CIMA":
            successors.append(Aspiradordepoltrona("esquerda", "ESQ", self.cima, self.esq, self.dir, self.baixo, self.poltronas))
            successors.append(Aspiradordepoltrona("direita", "DIR", self.cima, self.esq, self.dir, self.baixo, self.poltronas))
            if self.cima == "SUJO":
                if "CIMA" in self.poltronas:
                    successors.append(Aspiradordepoltrona("VIRAR", self.pos, self.cima, self.esq, self.dir, self.baixo, self.poltronas))
                    #successors.append(Aspiradordepoltrona("LIMPAR", self.pos, "LIMPO", self.esq, self.dir, self.baixo, self.poltronas))
                    #successors.append(Aspiradordepoltrona("DESVIRAR", self.pos, self.cima, self.esq, self.dir, self.baixo, self.poltronas))

                    self.poltronas.remove("CIMA")
                else:
                    successors.append(Aspiradordepoltrona("LIMPAR", self.pos, "LIMPO", self.esq, self.dir, self.baixo, self.poltronas))
        


        if self.pos == "ESQ":
            successors.append(Aspiradordepoltrona("cima", "CIMA", self.cima, self.esq, self.dir, self.baixo, self.poltronas))
            successors.append(Aspiradordepoltrona("direita", "DIR", self.cima, self.esq, self.dir, self.baixo, self.poltronas))
            successors.append(Aspiradordepoltrona("baixo", "BAIXO", self.cima, self.esq, self.dir, self.baixo, self.poltronas))

            if self.esq == "SUJO":
                if "ESQ" in self.poltronas:
                    successors.append(Aspiradordepoltrona("VIRAR", self.pos, self.cima, self.esq, self.dir, self.baixo, self.poltronas))
                    successors.append(Aspiradordepoltrona("LIMPAR", self.pos, self.cima, "LIMPO", self.dir, self.baixo, self.poltronas))
                    successors.append(Aspiradordepoltrona("DESVIRAR", self.pos, self.cima, self.esq, self.dir, self.baixo, self.poltronas))

                    self.poltronas.remove("ESQ")
                
                else:
                    successors.append(Aspiradordepoltrona("LIMPAR", self.pos, self.cima, "LIMPO", self.dir, self.baixo, self.poltronas))
        

        if self.pos == "DIR":
            successors.append(Aspiradordepoltrona("baixo", "BAIXO", self.cima, self.esq, self.dir, self.baixo, self.poltronas))
            successors.append(Aspiradordepoltrona("esquerda", "ESQ", self.cima, self.esq, self.dir, self.baixo, self.poltronas))
            successors.append(Aspiradordepoltrona("cima", "CIMA", self.cima, self.esq, self.dir, self.baixo, self.poltronas))

            if self.dir == "SUJO":
                if "DIR" in self.poltronas:
                    successors.append(Aspiradordepoltrona("VIRAR", self.pos, self.cima, self.esq, self.dir, self.baixo, self.poltronas))
                    successors.append(Aspiradordepoltrona("LIMPAR", self.pos, self.cima, self.esq, "LIMPO", self.baixo, self.poltronas))
                    successors.append(Aspiradordepoltrona("DESVIRAR", self.pos, self.cima, self.esq, self.dir, self.baixo, self.poltronas))

                    self.poltronas.remove("DIR")
                
                else:
                    successors.append(Aspiradordepoltrona("LIMPAR", self.pos, self.cima, self.esq, "LIMPO", self.baixo, self.poltronas))
        

        if self.pos == "BAIXO":
            successors.append(Aspiradordepoltrona("esquerda", "ESQ", self.cima, self.esq, self.dir, self.baixo, self.poltronas))
            successors.append(Aspiradordepoltrona("direita", "DIR", self.cima, self.esq, self.dir, self.baixo, self.poltronas))
            if self.baixo == "SUJO":
                if "BAIXO" in self.poltronas:
                    successors.append(Aspiradordepoltrona("VIRAR", self.pos, self.cima, self.esq, self.dir, self.baixo, self.poltronas))
                    successors.append(Aspiradordepoltrona("LIMPAR", self.pos, self.cima, self.esq, self.dir, "LIMPO", self.poltronas))
                    successors.append(Aspiradordepoltrona("DESVIRAR", self.pos, self.cima, self.esq, self.dir, self.baixo, self.poltronas))

                    self.poltronas.remove("BAIXO")
                
                else:
                    successors.append(Aspiradordepoltrona("LIMPAR", self.pos, self.cima, self.esq, self.dir, "LIMPO", self.poltronas))
                
        return successors
    
    def is_goal(self):

        #preciso add sofa no lugar
        if (self.dir == self.esq == self.baixo == self.cima == "LIMPO") and (len(self.poltronas) == 0) and (self.pos == "ESQ"):
            return True
    
    def description(self):
        return "Limpa casa com poltronas"
    
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
        return (f"Posição robÔ:{self.pos}, Quarto de cima:{self.cima}, Quarto direito:{self.dir}, Quarto esquerdo:{self.esq}, Quarto de baixo:{self.baixo}, Poltronas:{self.poltronas}")

    #busca largura
    #adicionar trace = true no search 


def main():
    print('Busca em profundidade iterativa')
    poltronas = ["CIMA", "ESQ"]
    state = Aspiradordepoltrona("", "ESQ", "SUJO", "SUJO", "SUJO", "SUJO", poltronas)
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state)
    if result != None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()