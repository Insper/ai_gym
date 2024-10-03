"""
Exposes the main classes of the search module:

- State: the class that represents a state of the search.
- SearchAlgorithm: the class that represents a search algorithm.
- BuscaLargura: the class that implements the Breadth-first search algorithm.
- BuscaProfundidade: the class that implements the Depth-first search algorithm.
- BuscaProfundidadeIterativa: the class that implements the Iterative Depth-first search algorithm.
- BuscaCustoUniforme: the class that implements the Uniform cost search algorithm.
- BuscaGananciosa: the class that implements the Greedy search algorithm.
- AEstrela: the class that implements the A* search algorithm.
- SubidaMontanha: the class that implements the Hill Climbing search algorithm.
- SubidaMontanhaEstocastico: the class that implements the
  Stochastic Hill Climbing search algorithm.
"""

from .graph import State
from .search_algorithms import (
    SearchAlgorithm,
    BuscaLargura,
    BuscaProfundidade,
    BuscaProfundidadeIterativa,
    BuscaCustoUniforme,
    BuscaGananciosa,
    AEstrela,
)
from .csp_algorithms import SubidaMontanha, SubidaMontanhaEstocastico

__all__ = [
    "State",
    "SearchAlgorithm",
    "BuscaLargura",
    "BuscaProfundidade",
    "BuscaProfundidadeIterativa",
    "BuscaCustoUniforme",
    "BuscaGananciosa",
    "AEstrela",
    "SubidaMontanha",
    "SubidaMontanhaEstocastico",
]
