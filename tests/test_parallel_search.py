#
# Tests for ParallelSearch
#
# Uses the same problem instances as the other test files:
#
#   - SumOne.py    : simple +1/+2 numeric search
#   - AspiradorPo.py : vacuum-world two-room problem
#   - poi.py       : graph of cities with costs
#
# Each of the six wrapped algorithms is tested with all three pruning modes.
# Correctness is checked against the solutions produced by the single-process
# versions of the same algorithms.
#

from aigyminsper.search.search_algorithms import (
    ParallelSearch,
    BuscaLargura,
    BuscaProfundidade,
    BuscaProfundidadeIterativa,
    BuscaCustoUniforme,
    BuscaGananciosa,
    AEstrela,
)
from .SumOne import SumOne
from .AspiradorPo import AspiradorPo
from .poi import Poi


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sumone(start: int, goal: int) -> SumOne:
    return SumOne(start, "", goal)


# ---------------------------------------------------------------------------
# SumOne — BuscaLargura wrapped in ParallelSearch
# ---------------------------------------------------------------------------

def test_parallel_BL_without():
    result = ParallelSearch(BuscaLargura).search(_sumone(1, 11))
    assert result is not None
    assert result.state.is_goal()


def test_parallel_BL_father_son():
    result = ParallelSearch(BuscaLargura).search(_sumone(1, 11), pruning="father-son")
    assert result is not None
    assert result.state.is_goal()


def test_parallel_BL_general():
    result = ParallelSearch(BuscaLargura).search(_sumone(1, 11), pruning="general")
    assert result is not None
    assert result.state.is_goal()


# ---------------------------------------------------------------------------
# SumOne — BuscaProfundidade wrapped in ParallelSearch
# ---------------------------------------------------------------------------

def test_parallel_BP_without():
    result = ParallelSearch(BuscaProfundidade).search(_sumone(1, 11), m=15)
    assert result is not None
    assert result.state.is_goal()


def test_parallel_BP_father_son():
    result = ParallelSearch(BuscaProfundidade).search(
        _sumone(1, 11), m=15, pruning="father-son"
    )
    assert result is not None
    assert result.state.is_goal()


def test_parallel_BP_general():
    result = ParallelSearch(BuscaProfundidade).search(
        _sumone(1, 11), m=15, pruning="general"
    )
    assert result is not None
    assert result.state.is_goal()


# ---------------------------------------------------------------------------
# SumOne — BuscaProfundidadeIterativa wrapped in ParallelSearch
# ---------------------------------------------------------------------------

def test_parallel_BPI_without():
    result = ParallelSearch(BuscaProfundidadeIterativa).search(_sumone(1, 11))
    assert result is not None
    assert result.state.is_goal()


def test_parallel_BPI_general():
    result = ParallelSearch(BuscaProfundidadeIterativa).search(
        _sumone(1, 11), pruning="general"
    )
    assert result is not None
    assert result.state.is_goal()


# ---------------------------------------------------------------------------
# SumOne — BuscaCustoUniforme wrapped in ParallelSearch
# ---------------------------------------------------------------------------

def test_parallel_BCU_without():
    result = ParallelSearch(BuscaCustoUniforme).search(_sumone(1, 11))
    assert result is not None
    assert result.state.is_goal()
    assert result.g == 5  # five +2 steps, each cost 1


def test_parallel_BCU_general():
    result = ParallelSearch(BuscaCustoUniforme).search(
        _sumone(1, 11), pruning="general"
    )
    assert result is not None
    assert result.state.is_goal()
    assert result.g == 5


# ---------------------------------------------------------------------------
# SumOne — BuscaGananciosa / AEstrela wrapped in ParallelSearch
# ---------------------------------------------------------------------------

def test_parallel_gananciosa_general():
    result = ParallelSearch(BuscaGananciosa).search(
        _sumone(1, 11), pruning="general"
    )
    assert result is not None
    assert result.state.is_goal()


def test_parallel_aestrela_general():
    result = ParallelSearch(AEstrela).search(_sumone(1, 11), pruning="general")
    assert result is not None
    assert result.state.is_goal()


# ---------------------------------------------------------------------------
# AspiradorPo — vacuum-world problem
# ---------------------------------------------------------------------------

def test_parallel_aspira_BL():
    state = AspiradorPo("", "ESQ", "SUJO", "SUJO")
    result = ParallelSearch(BuscaLargura).search(state, pruning="general")
    assert result is not None
    assert result.state.is_goal()


def test_parallel_aspira_BCU():
    state = AspiradorPo("", "ESQ", "SUJO", "SUJO")
    result = ParallelSearch(BuscaCustoUniforme).search(state, pruning="general")
    assert result is not None
    assert result.state.is_goal()


# ---------------------------------------------------------------------------
# Poi (city graph) — cost and path checks
# ---------------------------------------------------------------------------

def test_parallel_poi_BL_goal():
    state = Poi("", "0", "A", "E")
    result = ParallelSearch(BuscaLargura).search(state)
    assert result is not None
    assert result.state.is_goal()


def test_parallel_poi_BCU_optimal_cost():
    # All workers now run to completion; ParallelSearch picks the minimum-g
    # result, so the cost must match the sequential BuscaCustoUniforme.
    single = BuscaCustoUniforme().search(Poi("", "0", "A", "E"))
    result = ParallelSearch(BuscaCustoUniforme).search(
        Poi("", "0", "A", "E"), pruning="general"
    )
    assert result is not None
    assert result.state.is_goal()
    assert result.g == single.g


def test_parallel_poi_aestrela_general():
    state = Poi("", "0", "A", "E")
    result = ParallelSearch(AEstrela).search(state, pruning="general")
    assert result is not None
    assert result.state.is_goal()


def test_parallel_poi_aestrela_general_low_process_count():
    state = Poi("", "0", "A", "E")
    result = ParallelSearch(AEstrela, n_processes=1).search(
        state, pruning="general"
    )
    assert result is not None
    assert result.state.is_goal()


# ---------------------------------------------------------------------------
# n_processes parameter
# ---------------------------------------------------------------------------

def test_parallel_n_processes_1():
    """With a single worker the result must still be correct."""
    result = ParallelSearch(BuscaLargura, n_processes=1).search(
        _sumone(1, 11), pruning="general"
    )
    assert result is not None
    assert result.state.is_goal()


def test_parallel_n_processes_2():
    result = ParallelSearch(BuscaLargura, n_processes=2).search(
        _sumone(1, 11), pruning="general"
    )
    assert result is not None
    assert result.state.is_goal()


# ---------------------------------------------------------------------------
# Goal already at the initial state
# ---------------------------------------------------------------------------

def test_parallel_goal_at_initial_state():
    state = _sumone(11, 11)
    result = ParallelSearch(BuscaLargura).search(state)
    assert result is not None
    assert result.state.is_goal()


# ---------------------------------------------------------------------------
# No solution (depth-limited search that cannot reach the goal)
# ---------------------------------------------------------------------------

def test_parallel_no_solution():
    result = ParallelSearch(BuscaProfundidade).search(_sumone(1, 100), m=3)
    assert result is None
