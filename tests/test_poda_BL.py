#
# Considerando as implementações: 
#
# - AspiradorPo.py
# - SumOne.py
# - poi.py
#
# Testar o algoritmo: 
#
# 1) Breadth-first search (BuscaLargura)
#
# Com as seguintes configurações de poda: 
#
# - without pruning
# - father-son pruning
# - general pruning
#
#

from aigyminsper.search.SearchAlgorithms import BuscaLargura
from .SumOne import SumOne
from .poi import Poi

def test_sumone_without_pruning():
    state = SumOne(1, '', 11)
    algorithm = BuscaLargura()
    result = algorithm.search(state)
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +2  ; +2  ; +2  ; +2 "

def test_sumone_father_pruning():
    state = SumOne(1, '', 11)
    algorithm = BuscaLargura()
    result = algorithm.search(state, pruning='father-son')
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +2  ; +2  ; +2  ; +2 "

def test_sumone_general():
    state = SumOne(1, '', 11)
    algorithm = BuscaLargura()
    result = algorithm.search(state, pruning='general')
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +2  ; +2  ; +2  ; +2 "

def test_poi_BL():
    state = Poi('','0','A','E')
    alg = BuscaLargura()
    result = alg.search(state)
    assert result.show_path() == ' ; ir p/ c ; ir p/ e'

def test_poi_BL_custo():
    state = Poi('','0','A','E')
    alg = BuscaLargura()
    result = alg.search(state)
    assert result.g == 15

def test_poi_BL_custo_0():
    state = Poi('','0','A','A')
    alg = BuscaLargura()
    result = alg.search(state)
    assert result.g == 0
