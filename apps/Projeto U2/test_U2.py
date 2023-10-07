import Solver

#Para bono, edge, adam, larry e lanterna FALSE significa lado esquerdo do rio
#TRUE significa lado direito do rio
#Tem que passar do lado esquerdo pro direito

def test_menor_caminho():
    assert Solver.main(False, False, False, False, False) == 'Achou uma solucao que satisfaz o enunciado'

def test_custo_elevado():
    "Teste em que a pessoa que possui o maior custo começa com a lanterna fazendo com que a banda chegue atrasada ao concerto"
    assert Solver.main(False, False, False, True, True) == 'Achou uma solucao que NAO satisfaz a restricao de custo'

def test_resolvido():
    "Teste em que o problema ja começa resolvido, ou seja, todos já estão do lado certo da ponte então o custo é 0"
    assert Solver.main(True, True, True, True, True) == 'Achou uma solucao que satisfaz o enunciado'

def test_sem_solucao():
    "Teste em que ninguem consegue atravessar a ponte pois a lanterna está do outro lado"
    assert Solver.main(False, False, False, False, True) == 'Nao achou solucao'

def test_sem_solucao_01():
    assert Solver.main(True, True, True, True, False) == 'Nao achou solucao'

def test_custo_excedente():
    '''
        Este teste leva em consideração que o integrante mais lento da banda é o unico que se
        encontra do lado da ponte em que esta a lampada, tornando então o tempo de resolução do
        problema maior do que o tempo em que os mesmos tem para chegar ao show.
    '''
    assert  Solver.main(False, False, False, True, True) == 'Achou uma solucao que NAO satisfaz a restricao de custo'

