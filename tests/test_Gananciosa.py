#
# Considerando as implementações: 
#
# - AspiradorPo.py
# - SumOne.py
# - poi.py
#
# Testar o algoritmo: 
#
# 5) Greddy search algorithm (BuscaGananciosa)
#
# Com as seguintes configurações de poda: 
#
# - without pruning
# - father-son pruning
# - general pruning
#

import pytest

from aigyminsper.search.search_algorithms import BuscaGananciosa

from .AspiradorPo import AspiradorPo
from .SumOne import SumOne
from .poi import Poi


PRUNING_OPTIONS = ("without", "father-son", "general")


@pytest.mark.parametrize(
    ("pruning", "expected_path", "expected_cost"),
    [
        ("without", " ; +2  ; +1  ; +2  ; +1 ", 4),
        ("father-son", " ; +2  ; +1  ; +2  ; +1 ", 4),
        ("general", " ; +2  ; +2  ; +2 ", 3),
    ],
)
def test_busca_gananciosa_sumone_reaches_goal(
    pruning,
    expected_path,
    expected_cost,
):
    state = SumOne(1, "", 7)

    result = BuscaGananciosa().search(state, pruning=pruning)

    assert result is not None
    assert result.state.is_goal()
    assert result.show_path() == expected_path
    assert result.g == expected_cost


@pytest.mark.parametrize("pruning", PRUNING_OPTIONS)
def test_busca_gananciosa_poi_reaches_goal(pruning):
    # C is an immediate successor, keeping this heuristic-free cyclic example
    # finite even when pruning is disabled.
    state = Poi("", "A", "A", "C")

    result = BuscaGananciosa().search(state, pruning=pruning)

    assert result is not None
    assert result.state.is_goal()
    assert result.show_path() == " ; ir p/ c"
    assert result.g == 10


@pytest.mark.parametrize("pruning", PRUNING_OPTIONS)
def test_busca_gananciosa_aspirador_reaches_goal(pruning):
    # Cleaning the left room produces the goal as the next selected state.
    state = AspiradorPo("", "ESQ", "SUJO", "LIMPO")

    result = BuscaGananciosa().search(state, pruning=pruning)

    assert result is not None
    assert result.state.is_goal()
    assert result.show_path() == " ; limpar"
    assert result.g == 1
#
