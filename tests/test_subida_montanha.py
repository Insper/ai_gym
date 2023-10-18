from aigyminsper.search.CSPAlgorithms import SubidaMontanha, SubidaMontanhaEstocastico
from Equacao import Equacao
import pytest

'''
Testes com subida da montanha
'''

def test_equacao_subida_montanha_2(n=0):
    state = Equacao('', n)
    algorithm = SubidaMontanha()
    result = algorithm.search(state)
    assert result.number == pytest.approx(2.18, 0.1)

def test_equacao_subida_montanha_2(n=2):
    state = Equacao('', n)
    algorithm = SubidaMontanha()
    result = algorithm.search(state)
    assert result.number == pytest.approx(2.18, 0.1)

def test_equacao_subida_montanha_4(n=4):
    state = Equacao('', n)
    algorithm = SubidaMontanha()
    result = algorithm.search(state)
    assert result.number == pytest.approx(2.18, 0.1)

def test_equacao_subida_montanha_7(n=7):
    state = Equacao('', n)
    algorithm = SubidaMontanha()
    result = algorithm.search(state)
    assert result.number == pytest.approx(8.07, 0.1)

def test_equacao_subida_montanha_10(n=10):
    state = Equacao('', n)
    algorithm = SubidaMontanha()
    result = algorithm.search(state)
    assert result.number == pytest.approx(8.07, 0.1)

def test_equacao_subida_montanha_11(n=11):
    state = Equacao('', n)
    algorithm = SubidaMontanha()
    result = algorithm.search(state)
    assert result.number == pytest.approx(14.26, 0.1)

def test_equacao_subida_montanha_15(n=15):
    state = Equacao('', n)
    algorithm = SubidaMontanha()
    result = algorithm.search(state)
    assert result.number == pytest.approx(14.26, 0.1)

'''
Testes com subida da montanha estocástico
'''

def test_equacao_subida_montanha_estocastico_2(n=0):
    state = Equacao('', n)
    algorithm = SubidaMontanhaEstocastico()
    result = algorithm.search(state)
    assert result.number == pytest.approx(14.26, 0.1)

def test_equacao_subida_montanha_estocastico_2(n=2):
    state = Equacao('', n)
    algorithm = SubidaMontanhaEstocastico()
    result = algorithm.search(state)
    assert result.number == pytest.approx(14.26, 0.1)

def test_equacao_subida_montanha_estocastico_4(n=4):
    state = Equacao('', n)
    algorithm = SubidaMontanhaEstocastico()
    result = algorithm.search(state)
    assert result.number == pytest.approx(14.26, 0.1)

def test_equacao_subida_montanha_estocastico_7(n=7):
    state = Equacao('', n)
    algorithm = SubidaMontanhaEstocastico()
    result = algorithm.search(state)
    assert result.number == pytest.approx(14.26, 0.1)

def test_equacao_subida_montanha_estocastico_10(n=10):
    state = Equacao('', n)
    algorithm = SubidaMontanhaEstocastico()
    result = algorithm.search(state)
    assert result.number == pytest.approx(14.26, 0.1)

def test_equacao_subida_montanha_estocastico_11(n=11):
    state = Equacao('', n)
    algorithm = SubidaMontanhaEstocastico()
    result = algorithm.search(state)
    assert result.number == pytest.approx(14.26, 0.1)

def test_equacao_subida_montanha_estocastico_15(n=15):
    state = Equacao('', n)
    algorithm = SubidaMontanhaEstocastico()
    result = algorithm.search(state)
    assert result.number == pytest.approx(14.26, 0.1)