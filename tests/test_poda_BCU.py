#
# Considerando as implementações: 
#
# - AspiradorPo.py
# - SumOne.py
# - poi.py
#
# Testar o algoritmo: 
#
# 4) Uniform cost search (CustoUniforme)
#
# Com as seguintes configurações de poda: 
#
# - without pruning
# - father-son pruning
# - general pruning
#
#

from aigyminsper.search.SearchAlgorithms import BuscaCustoUniforme
from .SumOne import SumOne
from .poi import Poi
from .AspiradorPo import AspiradorPo

def test_bcu_sumone_without_pruning():
    state = SumOne(1, '', 23)
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state)
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2 "
    assert result.g == 11

def test_bcu_sumone_father_son_pruning():
    state = SumOne(1, '', 23)
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state, pruning='father-son')
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2 "
    assert result.g == 11

def test_bcu_sumone_general_pruning():
    state = SumOne(1, '', 23)
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state, pruning='general')
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2 "
    assert result.g == 11

def test_bcu_aspirador_without_pruning():
    state = AspiradorPo('','ESQ','SUJO','SUJO')
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state)
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; dir ; limpar ; esq ; limpar"
    assert result.g == 4

def test_bcu_aspirador_father_son_pruning():
    state = AspiradorPo('','ESQ','SUJO','SUJO')
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state, pruning='father-son')
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; dir ; limpar ; esq ; limpar"
    assert result.g == 4

def test_bcu_aspirador_general_pruning():
    state = AspiradorPo('','ESQ','SUJO','SUJO')
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state, pruning='general')
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; limpar ; dir ; limpar ; esq"
    assert result.g == 4

def test_bcu_poi_without_pruning():
    state = Poi('',"A","A","G")
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state)
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; ir p/ b ; ir p/ d ; ir p/ e ; ir p/ f ; ir p/ g"
    assert result.g == 7

def test_bcu_poi_father_son_pruning():
    state = Poi('',"A","A","G")
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state, pruning='father-son')
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; ir p/ b ; ir p/ d ; ir p/ e ; ir p/ f ; ir p/ g"
    assert result.g == 7

def test_bcu_poi_general_pruning():
    state = Poi('',"A","A","G")
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state, pruning='general')
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; ir p/ b ; ir p/ d ; ir p/ e ; ir p/ f ; ir p/ g"
    assert result.g == 7