from aigyminsper.search.search_algorithms import BuscaCustoUniforme
from aigyminsper.search.graph import State

class U2(State):

    def __init__(self, bono, edge, adam, larry, lanterna, op):
        """Inicializa o lado de cada pessoa, a lanterna e o último movimento.

        False representa o lado esquerdo da ponte e True representa o lado
        direito. ``op`` identifica quem atravessou para produzir este estado.
        """
        super().__init__(op)
        #
        # False significa o lado esquerdo e True significa o lado direito.
        #
        self.bono = bono
        self.edge = edge
        self.adam = adam
        self.larry = larry
        self.lanterna = lanterna

    def successors(self):
        """Retorna cada travessia válida de uma ou duas pessoas."""
        sucessors = []
        if self.bono == self.lanterna:
            sucessors.append(U2(not self.bono, self.edge, self.adam, self.larry, not self.lanterna, 'bono'))
            if self.edge == self.lanterna:
                sucessors.append(U2(not self.bono, not self.edge, self.adam, self.larry, not self.lanterna, 'bono;edge'))
            if self.adam == self.lanterna:
                sucessors.append(U2(not self.bono, self.edge, not self.adam, self.larry, not self.lanterna, 'bono;adam'))
            if self.larry == self.lanterna:
                sucessors.append(U2(not self.bono, self.edge, self.adam, not self.larry, not self.lanterna, 'bono;larry'))
        if self.edge == self.lanterna:
            sucessors.append(U2(self.bono, not self.edge, self.adam, self.larry, not self.lanterna, 'edge'))
            if self.adam == self.lanterna:
                sucessors.append(U2(self.bono, not self.edge, not self.adam, self.larry, not self.lanterna, 'edge;adam'))
            if self.larry == self.lanterna:
                sucessors.append(U2(self.bono, not self.edge, self.adam, not self.larry, not self.lanterna, 'edge;larry'))
        if self.adam == self.lanterna:
            sucessors.append(U2(self.bono, self.edge, not self.adam, self.larry, not self.lanterna, 'adam'))
            if self.larry == self.lanterna:
                sucessors.append(U2(self.bono, self.edge, not self.adam, not self.larry, not self.lanterna, 'adam;larry'))
        if self.larry == self.lanterna:
            sucessors.append(U2(self.bono, self.edge, self.adam, not self.larry, not self.lanterna, 'larry'))
        return sucessors
    
    def is_goal(self):
        """Retorna se todos e a lanterna chegaram ao lado direito."""
        return self.bono & self.edge & self.adam & self.larry & self.lanterna
    
    def description(self):
        """Descreve o problema de travessia da ponte com custo mínimo."""
        return "Problema de custo minimo usando os integrantes da banda U2"
    
    def cost(self):
        """Retorna o tempo de travessia da pessoa mais lenta no movimento."""
        if self.operator == 'bono':
            return 1
        elif self.operator == 'edge':
            return 2
        elif self.operator == 'adam':
            return 5
        elif self.operator == 'larry':
            return 10
        elif self.operator == 'bono;edge':
            return 2
        elif self.operator == 'bono;adam':
            return 5
        elif self.operator == 'bono;larry':
            return 10
        elif self.operator == 'edge;adam':
            return 5
        elif self.operator == 'edge;larry':
            return 10
        elif self.operator == 'adam;larry':
            return 10
    
    def env(self):
        """Identifica o estado pelo lado da ponte em que cada pessoa está."""
        return str(self.bono)+";"+str(self.edge)+";"+str(self.adam)+";"+str(self.larry)+str(self.cost)

def main():
    print('Busca de Custo Uniforme')
    state = U2(False, False, False, False, False, ' ')
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state)
    if result != None:
        if result.g <= 17:
            print('Achou uma solucao que satisfaz o enunciado')
            print(result.show_path())
            print(result.g)
        else:
            print('Achou uma solucao que NAO satisfaz a restricao de custo')
            print(result.show_path())
            print(result.g)
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()
