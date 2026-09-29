#
# Considerando as implementações: 
#
# - AspiradorPo.py
# - SumOne.py
# - poi.py
#
# Testar o algoritmo: 
#
# 6) A* search algorithm (AEstrela)
#
# Com as seguintes configurações de poda: 
#
# - without pruning
# - father-son pruning
# - general pruning
#

import pytest

from aigyminsper.search.search_algorithms import AEstrela

from .AspiradorPo import AspiradorPo
from .SumOne import SumOne
from .poi import Poi


PRUNING_OPTIONS = ("without", "father-son", "general")


@pytest.mark.parametrize("pruning", PRUNING_OPTIONS)
def test_a_estrela_sumone_returns_shortest_path(pruning):
    state = SumOne(1, "", 7)

    result = AEstrela().search(state, pruning=pruning)

    assert result is not None
    assert result.state.is_goal()
    assert result.show_path() == " ; +2  ; +2  ; +2 "
    assert result.g == 3


@pytest.mark.parametrize("pruning", PRUNING_OPTIONS)
def test_a_estrela_poi_returns_lowest_cost_route(pruning):
    state = Poi("", "A", "A", "E")

    result = AEstrela().search(state, pruning=pruning)

    assert result is not None
    assert result.state.is_goal()
    assert result.show_path() == " ; ir p/ b ; ir p/ d ; ir p/ e"
    assert result.g == 5


@pytest.mark.parametrize(
    ("pruning", "expected_path"),
    [
        ("without", " ; dir ; limpar ; esq ; limpar"),
        ("father-son", " ; dir ; limpar ; esq ; limpar"),
        ("general", " ; limpar ; dir ; limpar ; esq"),
    ],
)
def test_a_estrela_aspirador_returns_clean_world(pruning, expected_path):
    state = AspiradorPo("", "ESQ", "SUJO", "SUJO")

    result = AEstrela().search(state, pruning=pruning)

    assert result is not None
    assert result.state.is_goal()
    assert result.show_path() == expected_path
    assert result.g == 4
#
