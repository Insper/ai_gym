from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from .SumOne import SumOne
from .poi import Poi
from .AspiradorPo import AspiradorPo

def test_sumone_without_pruning():
    state = SumOne(3, '', 6)
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state)
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +1 "

def test_sumone_father_son_pruning():
    state = SumOne(3, '', 6)
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state, pruning='father-son')
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +1 "

def test_sumone_general_pruning():
    state = SumOne(3, '', 6)
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state, pruning='general')
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +1 "

def test_poi_without_pruning():
    state = Poi('','A','A','D')
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state)
    assert result.show_path() == " ; ir p/ b ; ir p/ d"

def test_poi_father_son_pruning():
    state = Poi('','A','A','D')
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state, pruning='father-son')
    assert result.show_path() == " ; ir p/ b ; ir p/ d"

def test_poi_general_pruning():
    state = Poi('','A','A','D')
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state, pruning='general')
    assert result.show_path() == " ; ir p/ b ; ir p/ d"

def test_aspiradorpo_without_pruning():
    state = AspiradorPo('','ESQ','LIMPO','SUJO')
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state)
    assert result.show_path() == " ; dir ; limpar ; esq"

def test_aspiradorpo_father_son_pruning():
    state = AspiradorPo('','ESQ','LIMPO','SUJO')
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state, pruning='father-son')
    assert result.show_path() == " ; dir ; limpar ; esq"
    
def test_aspiradorpo_general_pruning():
    state = AspiradorPo('','ESQ','LIMPO','SUJO')
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state, pruning='general')
    assert result.show_path() == " ; dir ; limpar ; esq"
