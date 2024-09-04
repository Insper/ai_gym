from aigyminsper.search.SearchAlgorithms import BuscaLargura
from aigyminsper.search.SearchAlgorithms import BuscaProfundidade
from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from .SumOne import SumOne

def test_largura():
    state = SumOne(1, '', 11)
    algorithm = BuscaLargura()
    result = algorithm.search(state)
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +2  ; +2  ; +2  ; +2 "

def test_largura2():
    state = SumOne(1, '', 23)
    algorithm = BuscaLargura()
    result = algorithm.search(state)
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2  ; +2 "

def test_largura3():
    state = SumOne(1, '', 5)
    algorithm = BuscaLargura()
    result = algorithm.search(state)
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +2 "

def test_profundidade():
    state = SumOne(1, '', 10)
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, 10)
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +2  ; +2  ; +2  ; +1 "

def test_BPI():
    state = SumOne(1, '', 10)
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state)
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +2  ; +2  ; +2  ; +1 "
