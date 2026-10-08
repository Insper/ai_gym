from aigyminsper.search.search_algorithms import BuscaProfundidadeIterativa, AEstrela
from aigyminsper.search.graph import State
import numpy
import sys
# Importa as bibliotecas necessárias.
# Este exemplo utiliza a classe base State e algoritmos de busca compatíveis.

class VacuumWorldGeneric(State):

    def __init__(self, mapa, lin, col, op):
        """Inicializa o estado do mundo do aspirador.

        mapa: uma matriz binária NumPy retangular que representa o mapa
            ex: [[0, 1, 1, 1],
                 [0, 0, 1, 1]
                 [1, 1, 1, 1]]
            observação: é uma matriz NumPy, não uma lista de listas.
        lin: posição horizontal do agente (linha)
        col: posição vertical do agente (coluna)
        op: operação que levou ao estado atual
            ex.: se o agente moveu para a esquerda, op = 'esq'.
        """

        super().__init__(op)
        self.mapa = mapa
        self.lin_max = self.mapa.shape[0]-1 # Linha máxima que o agente pode alcançar
        self.col_max = self.mapa.shape[1]-1 # Coluna máxima que o agente pode alcançar
        self.lin = lin
        self.col = col
    
    def successors(self):
        """Retorna os estados produzidos por cada movimento ou limpeza válida."""

        sucessors = []

        # Move para a esquerda
        if self.col - 1 >= 0:
            new = self.mapa.copy()
            sucessors.append(VacuumWorldGeneric(new, self.lin, self.col-1, 'esq'))

        # Move para a direita
        if self.col + 1 <= self.col_max:
            new = self.mapa.copy()
            sucessors.append(VacuumWorldGeneric(new, self.lin, self.col+1, 'dir'))

        # Move para cima
        if self.lin - 1 >=0:
            new = self.mapa.copy()
            sucessors.append(VacuumWorldGeneric(new, self.lin-1, self.col, 'cima'))

        # Move para baixo
        if self.lin + 1 <= self.lin_max:
            new = self.mapa.copy()
            sucessors.append(VacuumWorldGeneric(new, self.lin+1, self.col, 'baixo'))

        # Limpa o cômodo atual
        if self.mapa[self.lin][self.col] == 1:
            new = self.mapa.copy()
            new[self.lin][self.col] = 0 
            sucessors.append(VacuumWorldGeneric(new, self.lin, self.col, 'limpar'))

        return sucessors
    
    def is_goal(self):
        """Retorna se todos os cômodos do mapa estão limpos."""
        for y in self.mapa:
            for x in y:
                if x != 0:
                    return False
        return True

    def h(self):
        """Estima o trabalho restante contando os cômodos sujos."""
        count = 0
        for y in self.mapa:
            for x in y:
                if x != 0:
                    count = count + 1
        return count
    
    def description(self):
        """Descreve o problema representado por este estado."""
        return "Agente genérico para o problema do aspirador de pó"
    
    def cost(self):
        """Atribui custo unitário às ações de movimento e limpeza."""
        return 1
    
    def env(self):
        """Identifica o estado pelo mapa e pela posição do agente."""
        return str(self.mapa)+" "+str(self.lin)+" "+str(self.col)


def convert_file_to_map(file_map_path):
    """Converte um arquivo separado por ponto e vírgula em uma matriz NumPy."""
    return numpy.loadtxt(open(file_map_path, "rb"), delimiter=";")

def main(file_map_path, lin, col):
    mapa = convert_file_to_map(file_map_path)
    print(mapa)

    # Cria o estado inicial
    state = VacuumWorldGeneric(mapa, lin, col, '')

    #print('Busca em AEstrela')
    algorithm = AEstrela()
    
    print('Busca Profundidade Iterativa')
    # Cria o objeto do algoritmo de busca
    # algorithm = BuscaProfundidadeIterativa()

    # Executa a busca
    result = algorithm.search(state, trace=True)
    if result != None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
