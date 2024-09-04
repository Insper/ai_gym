from aigyminsper.search.CSPAlgorithms import SubidaMontanha, SubidaMontanhaEstocastico
from .Equacao import Equacao
import pytest

"""
Testes com subida da montanha
"""

DELTA = 0.1


@pytest.mark.parametrize(
    "n, expected",
    [(0, 2.18), (2, 2.18), (4, 2.18), (7, 8.07), (10, 8.07), (11, 14.26), (15, 14.26)],
)
def test_equacao_subida_montanha(n, expected):
    state = Equacao("", n)
    algorithm = SubidaMontanha()
    result = algorithm.search(state)
    assert result.number == pytest.approx(expected, DELTA)


"""
Testes com subida da montanha estocástico
"""


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 14.26),
        (2, 14.26),
        (4, 14.26),
        (7, 14.26),
        (10, 14.26),
        (11, 14.26),
        (15, 14.26),
    ],
)
def test_equacao_subida_montanha_estocastico(n, expected):
    state = Equacao("", n)
    algorithm = SubidaMontanhaEstocastico()
    result = algorithm.search(state)
    assert result.number == pytest.approx(expected, DELTA)
