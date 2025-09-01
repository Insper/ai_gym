"""
This module implements various search algorithms, including
Breadth-first search, Depth-first search, Iterative Deepening
Depth-first search, Uniform Cost search, Greedy search, and
A* search algorithms. Each algorithm is implemented as a subclass
of the SearchAlgorithm class.
"""

import json
from collections import deque
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D
from networkx.drawing.nx_pydot import graphviz_layout

from aigyminsper.search.graph import Node


def sort_function(val):
    """
    Function to sort the list by g(), h() or f()  
    """
    return val[1]

class SearchAlgorithm:
    """
    This class implements an interface for search algorithms.
    This class should not be instantiated.

    This class is used by the following implementations:
        - Breadth-first search (BuscaLargura)
        - Depth-first search (BuscaProfundidade)
        - Iterative deepening search (BPI)
        - Uniform cost search (CustoUniforme)
        - Greddy search algorithm (BuscaGananciosa)
        - A* search algorithm (AEstrela)
    """

    trace_graph: nx.DiGraph = nx.DiGraph()
    trace_edge_labels: dict[tuple,str] = {}

    def search(self, initial_state, m=None, pruning='without', trace=False):
        """
        This method implements a search algorithm.

        Parameters:
            initial_state: the initial state of the search.
            m: the maximum depth for depth-limited search.
            pruning: a string that defines the pruning option.
            The pruning options are: without, father-son and general.
            trace: a boolean that defines if the trace is printed or not.
        """

    def print_trace(self, node) -> None:
        """
        This method prints the trace of the search.

        Parameters:
            node: the node that is the solution of the search.
        """
        print(f"Path (State {node.state.env()}): {node.show_path()} -- Cost: {node.g}")

    def graph_trace(self, node: Node, node_successors: list[Node], open_list: deque[Node]) -> None:
        """
        This method displays a graphical view of the search nodes

        Parameters:
            node: the current node in the search
            node_successors: list of the successors of the current node
            state_is_goal: boolean if the current node is goal state
        """

        trace_fullscreen: bool = True
        trace_rotate_labels: bool = True
        trace_display_as_states: bool = False
        trace_display_at_depth: int = 0
        trace_hidden_labels: list[str] = ["operator", "mapa"]

        def hide_text(text: str) -> str:
            if trace_display_as_states:
                return ""
            return text + (" " * 1000) + "\n\n"
        def make_label(n: Node) -> str:
            node_state: dict[str, Any] = n.state.__dict__
            node_state_label: str = (
                hide_text(n.identifier)
                + json.dumps(
                {x: node_state[x] for x in node_state if x not in trace_hidden_labels},
                )
                .replace("\"",'').replace(':',' ')[1:-1]
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
        highlighted_edges: list[tuple[str,str]] = []
        highlighted_edges_labels = {}
        if not state_is_goal:
            for node_sucessor_index, node_sucessor_label in enumerate(node_sucessor_labels):
                nx.add_path(
                self.trace_graph,
                [node_state_label, node_sucessor_label]
                )

                node_sucessor = node_successors[node_sucessor_index]
                label: str = make_edge_label(node_sucessor)
                self.trace_edge_labels[(node_state_label, node_sucessor_label)] = label
        else:
            outlining_path: bool = True
            current_node: Node = node
            parent_node: Node = current_node.father_node
            while outlining_path:
                if parent_node is None:
                    outlining_path = False
                else:
                    highlighted_edge = (make_label(parent_node), make_label(current_node))
                    highlighted_edges.append(highlighted_edge)
                    label: str = make_edge_label(current_node)
                    highlighted_edges_labels[highlighted_edge] = label
                    current_node = parent_node
                    parent_node: Node = current_node.father_node

        # Categorize graph nodes
        color_map = []
        in_memory_nodes_label = [make_label(open_list_node) for open_list_node in open_list]
        for index, graph_node in enumerate(self.trace_graph):
            if graph_node == node_state_label:
                color_map.append("purple")
            elif (index == 0) or (state_is_goal and graph_node==node_state_label):
                color_map.append("green")
            elif graph_node in node_sucessor_labels and graph_node in in_memory_nodes_label:
                color_map.append("red")
            elif graph_node in node_sucessor_labels:
                color_map.append("yellow")
            elif graph_node in in_memory_nodes_label:
                color_map.append("blue")
            else:
                color_map.append("gray")

        # Categorize node edges
        edge_color_map = [
        "red" if edge in highlighted_edges else "black" for edge in self.trace_graph.edges()
        ]
        edge_width_map = [
        6 if edge in highlighted_edges else 2 for edge in self.trace_graph.edges()
        ]

        # Explain search action
        if state_is_goal:
            graph_title: str = "Evaluated state is goal"
        else:
            graph_title: str = "Evaluated state is not goal, generating successors"
        plt.title(graph_title)

        # Draw graph as tree
        if node.depth >= trace_display_at_depth:
            if trace_display_as_states:
                pos = nx.planar_layout(self.trace_graph)
            else:
                pos = graphviz_layout(self.trace_graph, prog="dot")
            nx.draw(
            self.trace_graph,
            pos, with_labels=True,
            node_color=color_map,
            edge_color=edge_color_map,
            width=edge_width_map
            )
            nx.draw_networkx_edge_labels(
            self.trace_graph,
            pos,
            self.trace_edge_labels,
            rotate=trace_rotate_labels
            )
            nx.draw_networkx_edge_labels(
            self.trace_graph,
            pos,
            highlighted_edges_labels,
            rotate=trace_rotate_labels,
            font_color='r'
            )
            plt.legend(handles=[
                Line2D([0], [0], marker='o', color='w', label='Initial node',
                markerfacecolor='g', markersize=15),
                Line2D([0], [0], marker='o', color='w', label='Currently evaluating node',
                markerfacecolor='purple', markersize=15),
                Line2D([0], [0], marker='o', color='w', label='Sucessor (added)',
                markerfacecolor='r', markersize=15),
                Line2D([0], [0], marker='o', color='w', label='Sucessor (discarded by pruning)',
                markerfacecolor='yellow', markersize=15),
                Line2D([0], [0], marker='o', color='w', label='Node (in memory)',
                markerfacecolor='b', markersize=15),
                Line2D([0], [0], marker='o', color='w', label='Node (used)',
                markerfacecolor='gray', markersize=15),
                ])
            if trace_fullscreen:
                plt.get_current_fig_manager().full_screen_toggle()
            plt.show()


class BuscaLargura (SearchAlgorithm):
    """
    This class implements the Breadth-first search algorithm.    
    """

    def search(self, initial_state, m=None, pruning='without', trace=False):
        # Define valid pruning options
        valid_pruning_options = ['without', 'father-son', 'general']
        if pruning not in valid_pruning_options:
            raise ValueError(
                f"Invalid pruning option: {pruning}. Valid options are {valid_pruning_options}"
            )

        # Set to keep track of the visited nodes
        states = set()
        #Creating a Queue
        open_list = deque()
        open_list.append(Node(initial_state, None))
        while len(open_list) > 0:
            n = open_list.popleft()
            if trace:
                self.print_trace(n)

            if n.state.is_goal():
                if trace:
                    self.graph_trace(n,[],open_list)
                return n
            for i in n.state.successors():
                new_n = Node(i,n)
                # without pruning
                if pruning == "without":
                    open_list.append(new_n)
                # father-son pruning
                elif pruning == "father-son" and (new_n.state.env() != n.state.env()):
                    open_list.append(new_n)
                # general pruning
                elif pruning == "general" and (new_n.state.env() not in states):
                    open_list.append(new_n)
                    states.add(new_n.state.env())
                if trace:
                    self.graph_trace(n,[new_n],open_list)
        return None


class BuscaProfundidade (SearchAlgorithm):
    """
    This class implements the Depth-first search (limited)    
    """

    def search (self, initial_state, m=None, pruning='without', trace=False):
        # Define valid pruning options
        valid_pruning_options = ['without', 'father-son', 'general']
        if pruning not in valid_pruning_options:
            raise ValueError(
                f"Invalid pruning option: {pruning}. Valid options are {valid_pruning_options}"
            )

        # Set to keep track of the visited nodes
        states = set()
        #Using list as stack
        open_list = []
        open_list.append(Node(initial_state, None))
        while len(open_list) > 0:
            n = open_list.pop()
            if trace:
                self.print_trace(n)

            if n.state.is_goal():
                if trace:
                    self.graph_trace(n,[],open_list)
                return n
            if n.depth < m:
                for i in n.state.successors():
                    new_n = Node(i,n)
                    # without pruning
                    if pruning == "without":
                        open_list.append(new_n)
                    # father-son pruning
                    elif pruning == "father-son" and (new_n.state.env() != n.state.env()):
                        open_list.append(new_n)
                    # general pruning
                    elif pruning == "general" and (new_n.state.env() not in states):
                        open_list.append(new_n)
                        states.add(new_n.state.env())
                    if trace:
                        self.graph_trace(n,[new_n],open_list)
        return None

class BuscaProfundidadeIterativa (SearchAlgorithm):
    """
    This class implements Iterative Deepening Depth-first search
    """

    def search(self, initial_state, m=None, pruning='without', trace=False):
        n = 1
        algorithm = BuscaProfundidade()
        while True:
            result = algorithm.search(initial_state, n, pruning, trace)
            if result is not None:
                return result
            n = n+1


class BuscaCustoUniforme (SearchAlgorithm):
    """
    This class implements a Uniform cost search algorithm
    """

    def search (self, initial_state, m=None, pruning='without', trace=False):
        # Define valid pruning options
        valid_pruning_options = ['without', 'father-son', 'general']
        if pruning not in valid_pruning_options:
            raise ValueError(
                f"Invalid pruning option: {pruning}. Valid options are {valid_pruning_options}"
            )

        # Set to keep track of the visited nodes
        states = set()
        open_list = []
        new_n = Node(initial_state, None)
        open_list.append((new_n, new_n.g))
        while len(open_list) > 0:
            #list sorted by g()
            open_list.sort(key = sort_function, reverse = True)
            n = open_list.pop()[0]
            if trace:
                self.print_trace(n)

            if n.state.is_goal():
                if trace:
                    self.graph_trace(n,[],open_list)
                return n
            for i in n.state.successors():
                new_n = Node(i,n)
                # without pruning
                if pruning == "without":
                    open_list.append((new_n, new_n.g))
                # father-son pruning
                elif pruning == "father-son" and (new_n.state.env() != n.state.env()):
                    open_list.append((new_n, new_n.g))
                # general pruning
                elif pruning == "general" and (new_n.state.env() not in states):
                    open_list.append((new_n, new_n.g))
                    states.add(new_n.state.env())
                if trace:
                    self.graph_trace(n,[new_n],open_list)
        return None


class BuscaGananciosa (SearchAlgorithm):
    """
    This class implements a Greddy search algorithm
    """

    def search (self, initial_state, m=None, pruning='without', trace=False):
        # Define valid pruning options
        valid_pruning_options = ['without', 'father-son', 'general']
        if pruning not in valid_pruning_options:
            raise ValueError(
                f"Invalid pruning option: {pruning}. Valid options are {valid_pruning_options}"
            )

        # Set to keep track of the visited nodes
        states = set()
        open_list = []
        new_n = Node(initial_state, None)
        open_list.append((new_n, new_n.h()))
        while len(open_list) > 0:
            #list sorted by h()
            open_list.sort(key = sort_function, reverse = True)
            n = open_list.pop()[0]
            if trace:
                self.print_trace(n)

            if n.state.is_goal():
                if trace:
                    self.graph_trace(n,[],open_list)
                return n
            for i in n.state.successors():
                new_n = Node(i,n)
                # without pruning
                if pruning == "without":
                    open_list.append((new_n, new_n.h()))
                # father-son pruning
                elif pruning == "father-son" and (new_n.state.env() != n.state.env()):
                    open_list.append((new_n, new_n.h()))
                # general pruning
                elif pruning == "general" and (new_n.state.env() not in states):
                    open_list.append((new_n, new_n.h()))
                    states.add(new_n.state.env())
                if trace:
                    self.graph_trace(n,[new_n],open_list)
        return None


class AEstrela (SearchAlgorithm):
    """
    This class implements a A* search algorithm
    """

    def search (self, initial_state, m=None, pruning='without', trace=False):
        # Define valid pruning options
        valid_pruning_options = ['without', 'father-son', 'general']
        if pruning not in valid_pruning_options:
            raise ValueError(
                f"Invalid pruning option: {pruning}. Valid options are {valid_pruning_options}"
            )

        # Set to keep track of the visited nodes
        states = set()
        open_list = []
        new_n = Node(initial_state, None)
        open_list.append((new_n, new_n.f()))

        while len(open_list) > 0:
            #list sorted by f()
            open_list.sort(key = sort_function, reverse = True)
            n = open_list.pop()[0]
            if trace:
                self.print_trace(n)

            if n.state.is_goal():
                if trace:
                    self.graph_trace(n,[],open_list)
                return n

            # iterate trought all successors
            for i in n.state.successors():

                new_n = Node(i,n)
                # without pruning
                if pruning == "without":
                    open_list.append((new_n,new_n.f()))
                # father-son pruning
                elif pruning == "father-son" and (new_n.state.env() != n.state.env()):
                    open_list.append((new_n,new_n.f()))
                # general pruning
                elif pruning == "general" and (new_n.state.env() not in states):
                    open_list.append((new_n,new_n.f()))
                    # nao eh adiciona o estado ao vetor.
                    # eh adicionado o conteudo
                    states.add(new_n.state.env())
                if trace:
                    self.graph_trace(n,[new_n],open_list)
        return None
