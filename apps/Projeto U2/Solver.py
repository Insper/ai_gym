from aigyminsper.search.SearchAlgorithms import BuscaCustoUniforme
from U2 import U2


def main(bono, adam, larry, edge, lanterna):
    state = U2(bono, adam, larry, edge, lanterna, '')
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state)
    if result != None:
        if result.g > 17:
            print('Achou uma solucao que NAO satisfaz a restricao de custo')
            print(result.show_path())
            print(result.g)
            return 'Achou uma solucao que NAO satisfaz a restricao de custo'
  
        return 'Achou uma solucao que satisfaz o enunciado'
    
    else:
        print('Nao achou solucao')
        return 'Nao achou solucao'

if __name__ == '__main__':
    main(False, False, False, False, False)

