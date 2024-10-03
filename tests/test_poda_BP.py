#
# Considerando as implementações: 
#
# - AspiradorPo.py
# - SumOne.py
# - poi.py
#
# Testar o algoritmo: 
#
# 2) Depth-first search (BuscaProfundidade)
#
# Com as seguintes configurações de poda: 
#
# - without pruning
# - father-son pruning
# - general pruning
#
#

from aigyminsper.search.SearchAlgorithms import BuscaProfundidade
from .SumOne import SumOne
from .poi import Poi
from .AspiradorPo import AspiradorPo

# ---------------------------------- SumOne ---------------------------------- #

def test_bp_sumone_without_pruning():
    state = SumOne(1, '', 20)
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, 20, pruning='without')
    assert result.show_path() == ' ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +1 '
    assert result.g == 10

def test_bp_sumone_father_son_pruning():
    state = SumOne(1, '', 20)
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, 20, pruning='father-son')
    assert result.show_path() == ' ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +1 '
    assert result.g == 10

def test_bp_sumone_general_pruning():
    state = SumOne(1, '', 20)
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, 20, pruning='general')
    assert result.show_path() == ' ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +1 '
    assert result.g == 10


# ---------------------------------- POI ---------------------------------- #

def test_bp_poi_without_pruning():
    state = Poi('', 'A', 'A', 'E')
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, 5, pruning='without')
    assert result.show_path() == ' ; ir p/ c ; ir p/ b ; ir p/ a ; ir p/ c ; ir p/ e'
    assert result.g == 27

def test_bp_poi_father_son_pruning():
    state = Poi('', 'A', 'A', 'E')
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, 5, pruning='father-son')
    assert result.show_path() == ' ; ir p/ c ; ir p/ b ; ir p/ a ; ir p/ c ; ir p/ e'
    assert result.g == 27

def test_bp_poi_general_pruning():
    state = Poi('', 'A', 'A', 'E')
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, 5, pruning='general')
    assert result.show_path() == ' ; ir p/ c ; ir p/ b ; ir p/ d ; ir p/ e'
    assert result.g == 15


# ---------------------------------- Aspirador de Pó ---------------------------------- #

def test_bp_aspiradorpo_without_pruning():
    state = AspiradorPo('','ESQ','SUJO','SUJO')
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, 5, pruning='without')
    assert result.show_path() == ' ; limpar ; limpar ; dir ; limpar ; esq'
    assert result.g == 5

def test_bp_aspiradorpo_father_son_pruning():
    state = AspiradorPo('','ESQ','SUJO','SUJO')
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, 10, pruning='father-son')
    assert result.show_path() == ' ; limpar ; dir ; limpar ; esq'
    assert result.g == 4

def test_bp_aspiradorpo_general_pruning():
    state = AspiradorPo('', 'ESQ', 'SUJO', 'SUJO')
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, 5, pruning='general')
    assert result.show_path() == ' ; limpar ; dir ; limpar ; esq'

def test_bp_aspiradorpo_without_pruning_10():
    state = AspiradorPo('', 'ESQ', 'SUJO', 'SUJO')
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, 10, pruning='without')
    assert result.show_path() == ' ; limpar ; limpar ; limpar ; limpar ; limpar ; limpar ; limpar ; dir ; limpar ; esq'