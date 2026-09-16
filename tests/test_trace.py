from aigyminsper.search.search_algorithms import (
    BuscaProfundidade,
    BuscaLargura,
    BuscaGananciosa,
    AEstrela,
    BuscaProfundidadeIterativa,
    BuscaCustoUniforme
)
from PyQt6.QtWidgets import QApplication
from .SumOne import SumOne

def test_buscaLarguraLive():
    state = SumOne(1, '', 7)
    algorithm = BuscaLargura()
    result = algorithm.search(state, trace=True, trace_live=True, trace_hold_graph=False)
    assert result.show_path() == ' ; +2  ; +2  ; +2 '

def test_buscaLarguraReplay():
    state = SumOne(1, '', 7)
    algorithm = BuscaLargura()
    result = algorithm.search(state, trace=True, trace_live=False, trace_hold_graph=False, trace_delay=0)
    assert result.show_path() == ' ; +2  ; +2  ; +2 '

def test_buscaProfundidadeLive():
    state = SumOne(1, '', 7)
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, m=3, trace=True, trace_live=True, trace_hold_graph=False)
    assert result.show_path() == ' ; +2  ; +2  ; +2 '

def test_buscaProfundidadeReplay():
    state = SumOne(1, '', 7)
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, m=3, trace=True, trace_live=False, trace_hold_graph=False, trace_delay=0)
    assert result.show_path() == ' ; +2  ; +2  ; +2 '
    

def test_buscaProfundidadeIterativaLive():
    state = SumOne(1, '', 7)
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state, trace=True, trace_live=True, trace_hold_graph=False)
    assert result.show_path() == ' ; +2  ; +2  ; +2 '

def test_buscaProfundidadeIterativaReplay():
    state = SumOne(1, '', 7)
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state, trace=True, trace_live=False, trace_hold_graph=False, trace_delay=0)
    assert result.show_path() == ' ; +2  ; +2  ; +2 '

def test_buscaGananciosaLive():
    state = SumOne(1, '', 7)
    algorithm = BuscaGananciosa()
    result = algorithm.search(state, trace=True, trace_live=True, trace_hold_graph=False)
    assert result.show_path() == ' ; +2  ; +1  ; +2  ; +1 '

def test_buscaGananciosaReplay():
    state = SumOne(1, '', 7)
    algorithm = BuscaGananciosa()
    result = algorithm.search(state, trace=True, trace_live=False, trace_hold_graph=False, trace_delay=0)
    assert result.show_path() == ' ; +2  ; +1  ; +2  ; +1 '

def test_buscaCustoUniformeLive():
    state = SumOne(1, '', 7)
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state, trace=True, trace_live=True, trace_hold_graph=False)
    assert result.show_path() == ' ; +2  ; +2  ; +2 '

def test_buscaCustoUniformeReplay():
    state = SumOne(1, '', 7)
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state, trace=True, trace_live=False, trace_hold_graph=False, trace_delay=0)
    assert result.show_path() == ' ; +2  ; +2  ; +2 '

def test_AEstrelaLive():
    state = SumOne(1, '', 7)
    algorithm = AEstrela()
    result = algorithm.search(state, trace=True, trace_live=True, trace_hold_graph=False)
    assert result.show_path() == ' ; +2  ; +2  ; +2 '

def test_AEstrelaReplay():
    state = SumOne(1, '', 7)
    algorithm = AEstrela()
    result = algorithm.search(state, trace=True, trace_live=False, trace_hold_graph=False, trace_delay=0)
    assert result.show_path() == ' ; +2  ; +2  ; +2 '