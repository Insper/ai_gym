"""
This module implements the following search algorithms:

- hill-climbing search algorithm
- stochastic hill-climbing search algorithm
- simulated annealing search (algoritmo da têmpera simulada) TODO
- local beam search (busca em feixe local) TODO

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from aigyminsper.search.search_algorithms import (
    PruningOptions,
    SearchAlgorithm,
    TraceOptions,
)

if TYPE_CHECKING:
    from aigyminsper.search.graph import CspState, Node


def sort_function(val: tuple[Node, int]) -> int:
    """
    Function to sort the list by g(), h() or f()
    """
    return val[1]


class SubidaMontanha(SearchAlgorithm):
    """
    This class implements the hill-climbing search algorithm.
    """

    def best(self, successors: list[CspState]) -> CspState:
        """
        This method finds and returns the best successor based on the heuristic value.
        Parameters:
            successors (list): A list of successor states to evaluate.
        Returns:
            Node: The successor with the lowest heuristic value.
        """
        best_state = successors[0]
        for i in successors:
            if i.h() < best_state.h():
                best_state = i
        return best_state

    def search(
        self,
        initial_state: CspState,
        /,
        _m: int | None = None,
        _pruning: PruningOptions = "without",
        *,
        trace: bool = False,
        **kwargs: TraceOptions,
    ) -> CspState:
        _trace_options: TraceOptions = super().get_trace_options(kwargs)
        super().validate_pruning_option(_pruning)

        atual = initial_state
        while True:
            if trace:
                print(f"Estado = {atual.env()}")
            prox = self.best(atual.successors())
            if prox.h() >= atual.h():
                return atual
            atual = prox


class SubidaMontanhaEstocastico(SearchAlgorithm):
    """
    This class implements the stochastic hill-climbing search algorithm.
    """

    def best(self, successors: list[CspState]) -> CspState:
        """
        Determine the best state from the list of successors based on the heuristic value.
        Parameters:
            successors: A list of successor states to evaluate.
        Returns:
            The best state with the lowest heuristic value.
        """

        best_state = successors[0]
        for i in successors:
            if i.h() < best_state.h():
                best_state = i
        return best_state

    def search(
        self,
        initial_state: CspState,
        /,
        _m: int | None = None,
        _pruning: PruningOptions = "without",
        *,
        trace: bool = False,
        **kwargs: TraceOptions,
    ) -> CspState:
        _trace_options: TraceOptions = super().get_trace_options(kwargs)
        super().validate_pruning_option(_pruning)

        atual = initial_state
        while True:
            if trace:
                print(f"Estado = {atual.env()}")
            prox = self.best(atual.successors())
            if prox.h() >= atual.h():
                if atual.is_goal():
                    return atual
                atual.random_state()
            else:
                atual = prox
