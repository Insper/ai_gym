"""
This module implements various search algorithms, including
Breadth-first search, Depth-first search, Iterative Deepening
Depth-first search, Uniform Cost search, Greedy search, and
A* search algorithms. Each algorithm is implemented as a subclass
of the SearchAlgorithm class.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from collections import deque
from platform import system
from typing import ClassVar, Literal, TypedDict

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D
from networkx.drawing.nx_pydot import graphviz_layout

from aigyminsper.search.graph import Node, State


def sort_function(val: tuple[Node, int]) -> int:
    """
    Function to sort the list by g(), h() or f()
    """
    return val[1]


class TraceOptions(TypedDict, total=False):
    """Trace options for the search algorithms."""

    trace_fullscreen: bool
    trace_rotate_labels: bool
    trace_display_as_states: bool
    trace_display_at_depth: int
    trace_hidden_labels: list[str] | None


PruningOptions: PruningOptions = Literal[
    "without",
    "father-son",
    "general",
]


class SearchAlgorithm(ABC):
    """
    This class implements an interface for search algorithms.
    This class should not be instantiated.

    This class is used by the following implementations:
        - Breadth-first search (BuscaLargura)
        - Depth-first search (BuscaProfundidade)
        - Iterative deepening search (BPI)
        - Uniform cost search (CustoUniforme)
        - Greedy search algorithm (BuscaGananciosa)
        - A* search algorithm (AEstrela)
    """

    trace_graph: nx.DiGraph = nx.DiGraph()
    trace_edge_labels: ClassVar[dict[tuple, str]] = {}

    @abstractmethod
    def search(
        self,
        initial_state: State,
        /,
        m: int | None = None,
        pruning: Literal["without", "father-son", "general"] = "without",
        *,
        trace: bool = False,
        **kwargs: TraceOptions,
    ) -> State:
        """
        This method implements a search algorithm.

        Parameters:
            initialState: the initial state of the search.
            pruning: a string that defines the pruning option. 
              The pruning options are: without, father-son and general.
            trace: a boolean that defines if the trace if printed or not.
            initial_state: the initial state of the search.
            m: the maximum depth for depth-limited search.
            pruning: a string that defines the pruning option.
            The pruning options are: without, father-son and general.
            trace: a boolean that defines if the trace is printed or not.
            trace_fullscreen: if graph tracing view should open in fullscreen.
            trace_rotate_labels: if graph tracing edge labels be rotated.
            trace_display_as_states: if graph tracing should show the states
            instead of node tree.
            trace_display_at_depth: search depth that graph display will start.
            trace_hidden_labels: list of labels in node state to hide in graph.
        """

    def get_trace_options(self, kwargs: dict) -> TraceOptions:
        """
        Get the trace options from the keyword arguments.

        Args:
            kwargs (dict): The keyword arguments from the search method.

        Returns:
            TraceOptions: The trace options for the search algorithm.
        """

        trace_options: TraceOptions = {
            "trace_fullscreen": kwargs.get("trace_fullscreen", False),
            "trace_rotate_labels": kwargs.get("trace_rotate_labels", True),
            "trace_display_as_states": kwargs.get(
                "trace_display_as_states",
                False,
            ),
            "trace_display_at_depth": kwargs.get("trace_display_at_depth", 0),
            "trace_hidden_labels": kwargs.get("trace_hidden_labels"),
        }
        return trace_options

    def validate_pruning_option(self, pruning: str) -> None:
        """Validates the pruning option.

        Args:
            pruning (str): The pruning option to validate.

        Raises:
            ValueError: If the pruning option is invalid.
        """

        # Define valid pruning options
        valid_pruning_options = ["without", "father-son", "general"]
        if pruning not in valid_pruning_options:
            invalid_prune_error = (
                f"Invalid pruning option: {pruning}.\n",
                "Valid options are {valid_pruning_options}",
            )
            raise ValueError(invalid_prune_error)

    def print_trace(self, node: Node) -> None:
        """
        This method prints the trace of the search.

        Parameters:
            node: the node that is the solution of the search.
        """
        print(
            f"Path (State {node.state.env()}): {node.show_path()} -- Cost: {node.g}",
        )

    def graph_trace(
        self,
        node: Node,
        node_successors: list[Node],
        open_list: deque[Node] | list[Node],
        trace_fullscreen: bool = True,
        trace_rotate_labels: bool = True,
        trace_display_as_states: bool = False,
        trace_display_at_depth: int = 0,
        trace_hidden_labels: list[str] | None = None,
    ) -> None:
        """
        This method displays a graphical view of the search nodes.

        Parameters:
            node: the current node in the search.
            node_successors: list of the successors of the current node.
            open_list: list or queue of open nodes.
            trace_fullscreen: if graph tracing view should open in fullscreen.
            trace_rotate_labels: if graph tracing edge labels be rotated.
            trace_display_as_states: if graph tracing should show the states instead of node tree.
            trace_display_at_depth: search depth that graph display will start.
            trace_hidden_labels: list of labels in node state to hide in graph.
        """

        default_trace_hidden_labels: list[str] = [
            "operator",
            "operador",
            "cost",
            "custo",
            "goal",
            "objetivo",
            "map",
            "mapa",
        ]
        if trace_hidden_labels is None:
            trace_hidden_labels = default_trace_hidden_labels.copy()
        else:
            trace_hidden_labels = (
                trace_hidden_labels + default_trace_hidden_labels
            )
        if not isinstance(trace_hidden_labels, list):
            hidden_labels_error = "trace_hidden_labels must be a list."
            raise TypeError(hidden_labels_error)

        # Hide text outside view to uniquely identify nodes
        hide_text_offset = (
            int((1920 * 4) / 14) + 100
        )  #  Minimum chars to add in 4k screen to hide

        def hide_text(text: str) -> str:
            if trace_display_as_states:
                return ""
            return text + (" " * hide_text_offset) + "\n\n"

        def format_state(state: dict[str, object]) -> str:
            return (
                json.dumps(state)
                .replace('"', "")
                .replace(":", " =")[1:-1]
                .replace(",", "\n")
            )

        def make_label(n: Node) -> str:
            node_state: dict[str, str] = n.state.__dict__
            filtered_state = {
                x: node_state[x]
                for x in node_state
                if trace_hidden_labels is not None
                and x.lower() not in trace_hidden_labels
            }
            node_state_label: str = hide_text(n.identifier) + format_state(
                filtered_state,
            )
            return node_state_label

        def make_edge_label(n: Node) -> str:
            return f"{n.state.operator} - cost {n.state.cost()}"

        # Get node states
        state_is_goal = node.state.is_goal()
        node_state_label: str = make_label(node)
        node_sucessor_labels: list[str] = [
            make_label(node_sucessor) for node_sucessor in node_successors
        ]

        # Add nodes to graph
        highlighted_edges: list[tuple[str, str]] = []
        highlighted_edges_labels = {}
        if not state_is_goal:
            for node_sucessor_index, node_sucessor_label in enumerate(
                node_sucessor_labels,
            ):
                nx.add_path(
                    self.trace_graph,
                    [node_state_label, node_sucessor_label],
                )

                node_sucessor = node_successors[node_sucessor_index]
                label: str = make_edge_label(node_sucessor)
                self.trace_edge_labels[
                    (node_state_label, node_sucessor_label)
                ] = label
        else:
            outlining_path: bool = True
            current_node: Node = node
            parent_node: Node | None = current_node.father_node
            while outlining_path:
                if parent_node is None:
                    outlining_path = False
                else:
                    highlighted_edge = (
                        make_label(parent_node),
                        make_label(current_node),
                    )
                    highlighted_edges.append(highlighted_edge)
                    label: str = make_edge_label(current_node)
                    highlighted_edges_labels[highlighted_edge] = label
                    current_node = parent_node
                    parent_node: Node | None = current_node.father_node

        # Categorize graph nodes
        color_map = []
        in_memory_nodes_label = [
            make_label(open_list_node) for open_list_node in open_list
        ]
        for index, graph_node in enumerate(self.trace_graph):
            if graph_node == node_state_label:
                color_map.append("purple")
            elif (index == 0) or (
                state_is_goal and graph_node == node_state_label
            ):
                color_map.append("green")
            elif (
                graph_node in node_sucessor_labels
                and graph_node in in_memory_nodes_label
            ):
                color_map.append("red")
            elif graph_node in node_sucessor_labels:
                color_map.append("yellow")
            elif graph_node in in_memory_nodes_label:
                color_map.append("blue")
            else:
                color_map.append("gray")

        # Categorize node edges
        edge_color_map = [
            "red" if edge in highlighted_edges else "black"
            for edge in self.trace_graph.edges()
        ]
        edge_width_map = [
            6 if edge in highlighted_edges else 2
            for edge in self.trace_graph.edges()
        ]

        # Explain search action
        if state_is_goal:
            graph_title: str = "Evaluated state is goal"
        else:
            graph_title: str = (
                "Evaluated state is not goal, generating successors"
            )
        plt.title(graph_title)

        # Draw graph as tree
        if node.depth >= trace_display_at_depth:
            if trace_display_as_states:
                pos = nx.planar_layout(self.trace_graph)
            else:
                pos = graphviz_layout(self.trace_graph, prog="dot")
            nx.draw(
                self.trace_graph,
                pos,
                with_labels=True,
                node_color=color_map,
                edge_color=edge_color_map,
                width=edge_width_map,
            )
            nx.draw_networkx_edge_labels(
                self.trace_graph,
                pos,
                self.trace_edge_labels,
                rotate=trace_rotate_labels,
            )
            nx.draw_networkx_edge_labels(
                self.trace_graph,
                pos,
                highlighted_edges_labels,
                rotate=trace_rotate_labels,
                font_color="r",
            )
            plt.legend(
                handles=[
                    Line2D(
                        [0],
                        [0],
                        marker="o",
                        color="w",
                        label="Initial node",
                        markerfacecolor="g",
                        markersize=15,
                    ),
                    Line2D(
                        [0],
                        [0],
                        marker="o",
                        color="w",
                        label="Currently evaluating node",
                        markerfacecolor="purple",
                        markersize=15,
                    ),
                    Line2D(
                        [0],
                        [0],
                        marker="o",
                        color="w",
                        label="Successor (added)",
                        markerfacecolor="r",
                        markersize=15,
                    ),
                    Line2D(
                        [0],
                        [0],
                        marker="o",
                        color="w",
                        label="Successor (discarded by pruning)",
                        markerfacecolor="yellow",
                        markersize=15,
                    ),
                    Line2D(
                        [0],
                        [0],
                        marker="o",
                        color="w",
                        label="Node (in memory)",
                        markerfacecolor="b",
                        markersize=15,
                    ),
                    Line2D(
                        [0],
                        [0],
                        marker="o",
                        color="w",
                        label="Node (used)",
                        markerfacecolor="gray",
                        markersize=15,
                    ),
                ],
            )
            if trace_fullscreen:
                backend = plt.get_backend()
                cfm = plt.get_current_fig_manager()
                if cfm:
                    if backend.lower() == "wxagg":
                        cfm.frame.Maximize(True)
                    elif backend.lower() == "tkagg":
                        if system().lower() == "windows":
                            cfm.window.state("zoomed")
                        else:
                            cfm.resize(*cfm.window.maxsize())
                    elif backend.lower() == "qt4agg":
                        cfm.window.showMaximized()
            plt.show()


class BuscaLargura(SearchAlgorithm):
    """
    This class implements the Breadth-first search algorithm.
    """

    def search(
        self,
        initial_state: State,
        /,
        _m: None = None,
        pruning: PruningOptions = "without",
        *,
        trace: bool = False,
        **kwargs: TraceOptions,
    ) -> Node | None:
        trace_options: TraceOptions = super().get_trace_options(kwargs)
        super().validate_pruning_option(pruning)

        # Set to keep track of the visited nodes
        states: set[State] = set()
        # Creating a Queue
        open_list: deque[Node] = deque()
        open_list.append(Node(initial_state, None))
        while len(open_list) > 0:
            n: Node = open_list.popleft()
            if trace:
                self.print_trace(n)

            if n.state.is_goal():
                if trace:
                    self.graph_trace(
                        n,
                        [],
                        open_list,
                        **trace_options,
                    )
                return n
            for i in n.state.successors():
                new_n: Node = Node(i, n)
                # without pruning
                if pruning == "without":
                    open_list.append(new_n)
                # father-son pruning
                elif pruning == "father-son" and (
                    new_n.state.env() != n.state.env()
                ):
                    open_list.append(new_n)
                # general pruning
                elif pruning == "general" and (
                    new_n.state.env() not in states
                ):
                    open_list.append(new_n)
                    states.add(new_n.state.env())
                if trace:
                    self.graph_trace(
                        n,
                        [new_n],
                        open_list,
                        **trace_options,
                    )
        return None


class BuscaProfundidade(SearchAlgorithm):
    """
    This class implements the Depth-first search (limited)
    """

    def search(
        self,
        initial_state: State,
        /,
        m: int | None = None,
        pruning: Literal["without", "father-son", "general"] = "without",
        *,
        trace: bool = False,
        **kwargs: TraceOptions,
    ) -> Node | None:
        trace_options: TraceOptions = super().get_trace_options(kwargs)
        super().validate_pruning_option(pruning)
        if m is None:
            msg = "Depth limit 'm' must be provided for depth-limited search."
            raise ValueError(msg)

        # Set to keep track of the visited nodes
        states: set[State] = set()
        # Using list as stack
        open_list: list[Node] = []
        open_list.append(Node(initial_state, None))
        while len(open_list) > 0:
            n: Node = open_list.pop()
            if trace:
                self.print_trace(n)

            if n.state.is_goal():
                if trace:
                    self.graph_trace(
                        n,
                        [],
                        open_list,
                        **trace_options,
                    )
                return n
            if n.depth < m:
                for i in n.state.successors():
                    new_n: Node = Node(i, n)
                    # without pruning
                    if pruning == "without":  # noqa: SIM114
                        open_list.append(new_n)
                    # father-son pruning
                    elif pruning == "father-son" and (
                        new_n.state.env() != n.state.env()
                    ):
                        open_list.append(new_n)
                    # general pruning
                    elif pruning == "general" and (
                        new_n.state.env() not in states
                    ):
                        open_list.append(new_n)
                        states.add(new_n.state.env())
                    if trace:
                        self.graph_trace(
                            n,
                            [new_n],
                            open_list,
                            **trace_options,
                        )
        return None


class BuscaProfundidadeIterativa(SearchAlgorithm):
    """
    This class implements Iterative Deepening Depth-first search
    """

    def search(
        self,
        initial_state: State,
        /,
        _m: None = None,
        pruning: Literal["without", "father-son", "general"] = "without",
        *,
        trace: bool = False,
        **kwargs: TraceOptions,
    ) -> Node | None:
        trace_options: TraceOptions = super().get_trace_options(kwargs)
        super().validate_pruning_option(pruning)

        n: int = 1
        algorithm: BuscaProfundidade = BuscaProfundidade()
        while True:
            result = algorithm.search(
                initial_state,
                m=n,
                pruning=pruning,
                trace=trace,
                **trace_options,
            )
            if result is not None:
                return result
            n: int = n + 1


class BuscaCustoUniforme(SearchAlgorithm):
    """
    This class implements a Uniform cost search algorithm
    """

    def search(
        self,
        initial_state: State,
        /,
        _m: None = None,
        pruning: Literal["without", "father-son", "general"] = "without",
        *,
        trace: bool = False,
        **kwargs: TraceOptions,
    ) -> Node | None:
        trace_options: TraceOptions = super().get_trace_options(kwargs)
        super().validate_pruning_option(pruning)

        # Set to keep track of the visited nodes
        states = set()
        open_list: list[tuple[Node, int]] = []
        new_n = Node(initial_state, None)
        open_list.append((new_n, new_n.g))
        while len(open_list) > 0:
            # list sorted by g()
            open_list.sort(key=sort_function, reverse=True)
            n = open_list.pop()[0]
            if trace:
                self.print_trace(n)

            if n.state.is_goal():
                if trace:
                    self.graph_trace(
                        n,
                        [],
                        open_list,
                        **trace_options,
                    )
                return n
            for i in n.state.successors():
                new_n = Node(i, n)
                # without pruning
                if pruning == "without":
                    open_list.append((new_n, new_n.g))
                # father-son pruning
                elif pruning == "father-son" and (
                    new_n.state.env() != n.state.env()
                ):
                    open_list.append((new_n, new_n.g))
                # general pruning
                elif pruning == "general" and (
                    new_n.state.env() not in states
                ):
                    open_list.append((new_n, new_n.g))
                    states.add(new_n.state.env())
                if trace:
                    self.graph_trace(
                        n,
                        [new_n],
                        [open_list_item[0] for open_list_item in open_list],
                        **trace_options,
                    )
        return None


class BuscaGananciosa(SearchAlgorithm):
    """
    This class implements a Greedy search algorithm
    """

    def search(
        self,
        initial_state: State,
        /,
        _m: None = None,
        pruning: Literal["without", "father-son", "general"] = "without",
        *,
        trace: bool = False,
        **kwargs: TraceOptions,
    ) -> Node | None:
        trace_options: TraceOptions = super().get_trace_options(kwargs)
        super().validate_pruning_option(pruning)

        # Set to keep track of the visited nodes
        states = set()
        open_list = []
        new_n = Node(initial_state, None)
        open_list.append((new_n, new_n.h()))
        while len(open_list) > 0:
            # list sorted by h()
            open_list.sort(key=sort_function, reverse=True)
            n = open_list.pop()[0]
            if trace:
                self.print_trace(n)

            if n.state.is_goal():
                if trace:
                    self.graph_trace(
                        n,
                        [],
                        open_list,
                        **trace_options,
                    )
                return n
            for i in n.state.successors():
                new_n = Node(i, n)
                # without pruning
                if pruning == "without":
                    open_list.append((new_n, new_n.h()))
                # father-son pruning
                elif pruning == "father-son" and (
                    new_n.state.env() != n.state.env()
                ):
                    open_list.append((new_n, new_n.h()))
                # general pruning
                elif pruning == "general" and (
                    new_n.state.env() not in states
                ):
                    open_list.append((new_n, new_n.h()))
                    states.add(new_n.state.env())
                if trace:
                    self.graph_trace(
                        n,
                        [new_n],
                        [open_list_item[0] for open_list_item in open_list],
                        **trace_options,
                    )
        return None


class AEstrela(SearchAlgorithm):
    """
    This class implements a A* search algorithm
    """

    def search(
        self,
        initial_state: State,
        /,
        _m: None = None,
        pruning: Literal["without", "father-son", "general"] = "without",
        *,
        trace: bool = False,
        **kwargs: TraceOptions,
    ) -> Node | None:
        trace_options: TraceOptions = super().get_trace_options(kwargs)
        super().validate_pruning_option(pruning)

        # Set to keep track of the visited nodes
        states = set()
        open_list = []
        new_n = Node(initial_state, None)
        open_list.append((new_n, new_n.f()))

        while len(open_list) > 0:
            # list sorted by f()
            open_list.sort(key=sort_function, reverse=True)
            n = open_list.pop()[0]
            if trace:
                self.print_trace(n)

            if n.state.is_goal():
                if trace:
                    self.graph_trace(
                        n,
                        [],
                        open_list,
                        **trace_options,
                    )
                return n

            # iterate through all successors
            for i in n.state.successors():
                new_n = Node(i, n)
                # without pruning
                if pruning == "without":
                    open_list.append((new_n, new_n.f()))
                # father-son pruning
                elif pruning == "father-son" and (
                    new_n.state.env() != n.state.env()
                ):
                    open_list.append((new_n, new_n.f()))
                # general pruning
                elif pruning == "general" and (
                    new_n.state.env() not in states
                ):
                    open_list.append((new_n, new_n.f()))
                    # nao eh adiciona o estado ao vetor.
                    # eh adicionado o conteúdo
                    states.add(new_n.state.env())
                if trace:
                    self.graph_trace(
                        n,
                        [new_n],
                        [open_list_item[0] for open_list_item in open_list],
                        **trace_options,
                    )
        return None
