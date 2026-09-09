"""
This module implements various search algorithms, including
Breadth-first search, Depth-first search, Iterative Deepening
Depth-first search, Uniform Cost search, Greedy search, and
A* search algorithms. Each algorithm is implemented as a subclass
of the SearchAlgorithm class.
"""

from __future__ import annotations

import json
import multiprocessing as mp
from abc import ABC, abstractmethod
from collections import deque
from platform import system
from typing import ClassVar, Literal, TypedDict

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D
from matplotlib.colors import to_rgba
from networkx.drawing.nx_pydot import graphviz_layout

from PyQt6.QtCore import QLineF, QRectF, Qt, QTimer, QPoint
from PyQt6.QtGui import QBrush, QColor, QFont, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView,
    QLabel,
    QGraphicsItemGroup,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QGraphicsItem,
)


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
    trace_hold_graph: bool = True
    trace_live: bool = False
    trace_delay: float = 0.001


PruningOptions: PruningOptions = Literal[
    "without",
    "father-son",
    "general",
]

class ZoomableGraphicsView(QGraphicsView):
    def wheelEvent(self, event) -> None:
        zoom_factor = 1.15

        if event.angleDelta().y() < 0:
            zoom_factor = 1 / zoom_factor

        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse,
        )

        self.scale(zoom_factor, zoom_factor)


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
    trace_fig = None
    trace_ax = None
    trace_frames: list[dict] = []


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
            trace_hold_graph: set if graph will be holded in the end or auto close
            trace_live: set if graph will be displayed in parallel (live) or in the end of the search
            trace_delay: set the delay on oppening each node in the `trace_live = false` mode.
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
            "trace_hold_graph": kwargs.get("trace_hold_graph", True),
            "trace_live": kwargs.get("trace_live", False),
            "trace_delay": kwargs.get("trace_delay", 0.1)
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
        trace_hold_graph: bool = True,
        trace_live: bool = False,
        trace_delay: float = 0.001
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
            trace_hold_graph: set if graph auto-close on show the results in the end
            trace_live: set if graph will show as the search goes, or just in the end
            trace_delay: set the dalay of expanding nodes
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
            if (isinstance(tuple, n)):
                n = n[0]
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

        self.trace_frames.append(
            {
                "current": node_state_label,
                "successors": node_sucessor_labels.copy(),
                "open": set(in_memory_nodes_label),
                "goal": state_is_goal,
                "highlighted_edges": highlighted_edges.copy(),
            }
        )

        if not trace_live:
            return

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
        

        # Draw graph as tree
        if node.depth >= trace_display_at_depth:
            if (
                self.trace_fig is None
                or not plt.fignum_exists(self.trace_fig.number)
            ):
                plt.ion()
                self.trace_fig, self.trace_ax = plt.subplots()

                if trace_fullscreen:
                    manager = self.trace_fig.canvas.manager
                    if manager is not None:
                        backend = plt.get_backend().lower()

                        if backend == "wxagg":
                            manager.frame.Maximize(True)
                        elif backend == "tkagg":
                            if system().lower() == "windows":
                                manager.window.state("zoomed")
                            else:
                                manager.resize(*manager.window.maxsize())
                        elif backend in ("qtagg", "qt5agg", "qt4agg"):
                            manager.window.showMaximized()

                plt.show(block=False)

            self.trace_ax.clear()
            self.trace_ax.set_title(graph_title)
            
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
                ax=self.trace_ax
            )
            nx.draw_networkx_edge_labels(
                self.trace_graph,
                pos,
                self.trace_edge_labels,
                rotate=trace_rotate_labels,
                ax=self.trace_ax
            )
            nx.draw_networkx_edge_labels(
                self.trace_graph,
                pos,
                highlighted_edges_labels,
                rotate=trace_rotate_labels,
                font_color="r",
                ax=self.trace_ax
            )
            self.trace_ax.legend(
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
            # if trace_fullscreen:
            #     backend = plt.get_backend()
            #     cfm = plt.get_current_fig_manager()
            #     if cfm:
            #         if backend.lower() == "wxagg":
            #             cfm.frame.Maximize(True)
            #         elif backend.lower() == "tkagg":
            #             if system().lower() == "windows":
            #                 cfm.window.state("zoomed")
            #             else:
            #                 cfm.resize(*cfm.window.maxsize())
            #         elif backend.lower() == "qt4agg":
            #             cfm.window.showMaximized()
            self.trace_fig.canvas.draw_idle()
            self.trace_fig.canvas.flush_events()
            plt.pause(0.01)

            if state_is_goal and trace_hold_graph:
                plt.ioff()
                plt.show()

    def replay_trace(
        self,
        *,
        trace_rotate_labels: bool = True,
        trace_delay: float = 0.1,
    ) -> None:
        """Replay the recorded search using an incremental Qt graphics scene."""

        if not self.trace_frames:
            return

        app = QApplication.instance()

        if app is None:
            app = QApplication([])

        scene = QGraphicsScene()
        view = ZoomableGraphicsView(scene)
        background_color = view.palette().color(view.backgroundRole())
        QBrush(background_color)

        view.setWindowTitle("AI Gym — Search Trace")
        view.resize(1400, 900)

        view.setRenderHint(
            view.renderHints().Antialiasing,
            False,
        )

        view.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate,
        )

        view.setOptimizationFlag(
            QGraphicsView.OptimizationFlag.DontSavePainterState,
            True,
        )

        view.setDragMode(
            QGraphicsView.DragMode.ScrollHandDrag,
        )

        # Do not pass the large textual labels directly to Graphviz.
        # Integer labels make layout generation substantially faster.
        layout_graph = nx.convert_node_labels_to_integers(
            self.trace_graph,
            label_attribute="trace_key",
        )
        layout_graph.graph["graph"] = {
            "ranksep": "4",
            "nodesep": "0.1",
        }

        layout_graph.graph["node"] = {
            "width": "1.2",
            "height": "0.7",
            "fixedsize": "true",
        }

        indexed_positions = graphviz_layout(
            layout_graph,
            prog="dot",
        )

        

        pos = {
            data["trace_key"]: indexed_positions[index]
            for index, data in layout_graph.nodes(data=True)
        }

        node_diameter = 56.0
        node_radius = node_diameter / 2

        node_items = {}
        node_text_items = {}
        node_colors = {}

        edge_items = {}
        edge_text_items = {}
        edge_label_groups = {}

        visible_nodes = set()
        visible_edges = set()
        previously_active_edges = set()

        colors = {
            "initial": QColor("#2ca02c"),
            "current": QColor("#9467bd"),
            "successor_added": QColor("#d62728"),
            "successor_discarded": QColor("#f1c40f"),
            "open": QColor("#1f77b4"),
            "used": QColor("#9e9e9e"),
            "goal_path": QColor("#d62728"),
            "edge": QColor("#242424"),
            "text": QColor("#111111"),
        }
        

        legend_widget = QFrame()
        legend_widget.setObjectName("traceLegend")

        legend_widget.setStyleSheet(
            """
            QFrame#traceLegend {
                background-color: rgba(255, 255, 255, 235);
                border: 1px solid #777777;
                border-radius: 6px;
            }

            QLabel {
                color: #111111;
                background-color: transparent;
                border: none;
            }
            """
        )

        legend_layout = QVBoxLayout(legend_widget)
        legend_layout.setContentsMargins(10, 8, 10, 8)
        legend_layout.setSpacing(4)

        legend_entries = [
            ("Initial node", colors["initial"]),
            ("Currently evaluating node", colors["current"]),
            ("Successor (added)", colors["successor_added"]),
            (
                "Successor (discarded by pruning)",
                colors["successor_discarded"],
            ),
            ("Node (in memory)", colors["open"]),
            ("Node (used)", colors["used"]),
        ]

        for description, color in legend_entries:
            row_widget = QWidget()

            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(8)

            marker = QLabel("●")
            marker.setFixedWidth(20)
            marker.setStyleSheet(
                f"""
                QLabel {{
                    color: {color.name()};
                    font-size: 20px;
                }}
                """
            )

            text_label = QLabel(description)

            row_layout.addWidget(marker)
            row_layout.addWidget(text_label)
            row_layout.addStretch()

            legend_layout.addWidget(row_widget)

        legend_widget.adjustSize()

        legend_proxy = scene.addWidget(legend_widget)

        legend_proxy.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations,
            True,
        )

        legend_proxy.setZValue(1000)
        legend_proxy.show()

        label_font = QFont()
        label_font.setPointSize(8)

        edge_font = QFont()
        edge_font.setPointSize(7)


        def position_legend() -> None:
            """Position the legend in the viewport's upper-right corner."""

            margin = 12

            viewport_x = (
                view.viewport().width()
                - legend_widget.width()
                - margin
            )

            viewport_point = QPoint(
                viewport_x,
                margin,
            )

            scene_point = view.mapToScene(viewport_point)
            legend_proxy.setPos(scene_point)
            legend_proxy.show()
        

        def display_label(label: str) -> str:
            """Remove the whitespace identifier used by the Matplotlib trace."""

            if "\n\n" in label:
                label = label.split("\n\n", maxsplit=1)[1]

            label = label.strip()

            if not label:
                return "State"

            return label

        def set_node_color(node_key: str, color: QColor) -> None:
            """Change a node only when its color actually changed."""

            color_name = color.name()

            if node_colors.get(node_key) == color_name:
                return

            node_items[node_key].setBrush(QBrush(color))
            node_colors[node_key] = color_name

        def create_node(node_key: str) -> None:
            """Add one persistent node to the scene."""

            if node_key in node_items:
                return

            x, graphviz_y = pos[node_key]

            # Graphviz uses an upward-positive Y axis; Qt uses downward-positive.
            y = -graphviz_y

            node_item = scene.addEllipse(
                x - node_radius,
                y - node_radius,
                node_diameter,
                node_diameter,
                QPen(QColor("#333333"), 1.5),
                QBrush(colors["used"]),
            )

            node_item.setZValue(2)

            text_item = QGraphicsSimpleTextItem(
                display_label(node_key),
            )

            text_item.setFont(label_font)
            text_item.setBrush(QBrush(colors["text"]))
            text_item.setZValue(3)

            text_bounds = text_item.boundingRect()

            text_item.setPos(
                x - text_bounds.width() / 2,
                y + node_radius + 3,
            )

            scene.addItem(text_item)

            node_items[node_key] = node_item
            node_text_items[node_key] = text_item
            node_colors[node_key] = colors["used"].name()

        def create_edge(edge: tuple[str, str]) -> None:
            """Add one persistent edge and its label to the scene."""

            if edge in edge_items:
                return

            source, target = edge

            source_x, source_graphviz_y = pos[source]
            target_x, target_graphviz_y = pos[target]

            source_y = -source_graphviz_y
            target_y = -target_graphviz_y

            line = QLineF(
                source_x,
                source_y,
                target_x,
                target_y,
            )

            edge_item = scene.addLine(
                line,
                QPen(colors["edge"], 2),
            )

            edge_item.setZValue(0)

            edge_label = self.trace_edge_labels.get(edge, "")

            text_item = QGraphicsSimpleTextItem(edge_label)
            text_item.setFont(edge_font)
            text_item.setBrush(QBrush(colors["text"]))

            text_bounds = text_item.boundingRect()
            padding = 4.0

            background_item = scene.addRect(
                text_bounds.adjusted(
                    -padding,
                    -padding,
                    padding,
                    padding,
                ),
                QPen(Qt.PenStyle.NoPen),
                QBrush(QColor("#ffffff")),
            )

            # Position both items locally inside a movable group.
            text_item.setPos(0, 0)
            background_item.setPos(0, 0)

            scene.addItem(text_item)

            label_group = QGraphicsItemGroup()
            scene.addItem(label_group)

            label_group.addToGroup(background_item)
            label_group.addToGroup(text_item)

            midpoint_x = (source_x + target_x) / 2
            midpoint_y = (source_y + target_y) / 2

            group_bounds = label_group.boundingRect()

            label_group.setPos(
                midpoint_x - group_bounds.width() / 2,
                midpoint_y - group_bounds.height() / 2,
            )

            if trace_rotate_labels:
                angle = -line.angle()

                if angle > 90:
                    angle -= 180
                elif angle < -90:
                    angle += 180

                label_group.setTransformOriginPoint(
                    group_bounds.center(),
                )
                label_group.setRotation(angle)

            # Edge is at Z=0; the white background and text stay above it.
            label_group.setZValue(5)
            label_group.setVisible(False)

            edge_items[edge] = edge_item
            edge_text_items[edge] = text_item
            edge_label_groups[edge] = label_group

        # Establish a fixed scene rectangle from the final layout. This prevents
        # zooming and scrolling from changing while nodes are added.
        # x_values = [position[0] for position in pos.values()]
        # y_values = [-position[1] for position in pos.values()]

        # margin = 100.0

        # scene.setSceneRect(
        #     QRectF(
        #         min(x_values) - margin,
        #         min(y_values) - margin,
        #         max(x_values) - min(x_values) + (2 * margin),
        #         max(y_values) - min(y_values) + (2 * margin),
        #     ),
        # )

        camera_initialized = False

        def update_camera() -> None:
            """Centralize e expanda a câmera conforme o grafo visível cresce."""

            nonlocal camera_initialized

            if not visible_nodes:
                return

            visible_items = []

            for node_key in visible_nodes:
                visible_items.append(node_items[node_key])
                visible_items.append(node_text_items[node_key])

            for edge in visible_edges:
                edge_item = edge_items.get(edge)

                if edge_item is not None:
                    visible_items.append(edge_item)

                label_group = edge_label_groups.get(edge)

                if label_group is not None and label_group.isVisible():
                    visible_items.append(label_group)

            bounds = visible_items[0].sceneBoundingRect()

            for item in visible_items[1:]:
                bounds = bounds.united(item.sceneBoundingRect())

            margin = 80.0
            bounds = bounds.adjusted(
                -margin,
                -margin,
                margin,
                margin,
            )

            scene.setSceneRect(bounds)

            if not camera_initialized:
                # Mostra o primeiro nó em uma escala confortável.
                view.resetTransform()
                view.centerOn(node_items[self.trace_frames[0]["current"]])
                camera_initialized = True
            else:
                # Reduz o zoom para manter todo o grafo visível.
                view.fitInView(
                    bounds,
                    Qt.AspectRatioMode.KeepAspectRatio,
                )
            position_legend()

        frame_index = 0

        def render_next_frame() -> None:
            nonlocal frame_index
            nonlocal previously_active_edges

            if frame_index >= len(self.trace_frames):
                timer.stop()

                # Keep every solution action visible at the end.
                for edge in previously_active_edges:
                    label_item = edge_text_items.get(edge)

                    if label_item is not None:
                        label_group = edge_label_groups.get(edge)

                        if label_group is not None:
                            label_group.setVisible(True)

                return

            frame = self.trace_frames[frame_index]

            current = frame["current"]
            successors = frame["successors"]
            open_nodes = frame["open"]
            highlighted_edges = set(frame["highlighted_edges"])
            state_is_goal = frame["goal"]

            create_node(current)
            visible_nodes.add(current)

            for successor in successors:
                create_node(successor)
                visible_nodes.add(successor)

                edge = (current, successor)
                create_edge(edge)
                visible_edges.add(edge)

            # Determine colors for the current frame.
            for node_key in visible_nodes:
                if node_key == current:
                    color = (
                        colors["initial"]
                        if state_is_goal
                        else colors["current"]
                    )
                elif node_key in successors:
                    color = (
                        colors["successor_added"]
                        if node_key in open_nodes
                        else colors["successor_discarded"]
                    )
                elif node_key in open_nodes:
                    color = colors["open"]
                else:
                    color = colors["used"]

                set_node_color(node_key, color)

            # Restore edges that were highlighted by the previous frame.
            for edge in previously_active_edges:
                if edge in edge_items:
                    edge_items[edge].setPen(
                        QPen(colors["edge"], 2),
                    )

                label_item = edge_text_items.get(edge)

                if label_item is not None:
                    label_item.setVisible(False)
                    label_item.setBrush(QBrush(colors["text"]))

                    font = label_item.font()
                    font.setBold(False)
                    label_item.setFont(font)

            active_edges = {
                edge
                for edge in visible_edges
                if edge[0] == current
            }

            active_edges.update(highlighted_edges)

            for edge in active_edges:
                if edge not in edge_items:
                    continue

                is_solution_action = edge in highlighted_edges

                edge_items[edge].setPen(
                    QPen(
                        (
                            colors["goal_path"]
                            if is_solution_action
                            else colors["edge"]
                        ),
                        5 if is_solution_action else 2,
                    ),
                )

                label_item = edge_text_items.get(edge)

                if label_item is not None:
                    label_item.setVisible(True)

                    if is_solution_action:
                        # Keep the action associated with the red solution edge visible.
                        label_item.setBrush(
                            QBrush(colors["goal_path"]),
                        )

                        font = label_item.font()
                        font.setBold(True)
                        font.setPointSize(9)
                        label_item.setFont(font)

                        # Ensure labels appear above nodes and edges.
                        label_item.setZValue(10)
                    else:
                        label_item.setBrush(
                            QBrush(colors["text"]),
                        )

                        font = label_item.font()
                        font.setBold(False)
                        font.setPointSize(7)
                        label_item.setFont(font)

                        label_item.setZValue(1)

            previously_active_edges = active_edges
            update_camera()
            frame_index += 1

        interval_ms = max(0, round(trace_delay * 1000))

        timer = QTimer()
        timer.setTimerType(Qt.TimerType.PreciseTimer)
        timer.setInterval(interval_ms)
        timer.timeout.connect(render_next_frame)

        view.show()

        view.resetTransform()


        # Display the initial frame immediately.
        render_next_frame()
        timer.start()

        app.exec()


    def hold_trace(self) -> None:
        """Keep the final trace window open until it is closed."""
        plt.ioff()
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

                    if not trace_options["trace_live"]:
                        self.replay_trace(
                            trace_rotate_labels=trace_options["trace_rotate_labels"],
                            trace_delay=trace_options["trace_delay"]
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

                    if not trace_options["trace_live"]:
                        self.replay_trace(
                            trace_rotate_labels=trace_options["trace_rotate_labels"],
                            trace_delay=trace_options["trace_delay"]
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

                    if not trace_options["trace_live"]:
                        self.replay_trace(
                            trace_rotate_labels=trace_options["trace_rotate_labels"],
                            trace_delay=trace_options["trace_delay"]
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

                    if not trace_options["trace_live"]:
                        self.replay_trace(
                            trace_rotate_labels=trace_options["trace_rotate_labels"],
                            trace_delay=trace_options["trace_delay"]
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
                        [n[0] for n in open_list],
                        **trace_options,
                    )

                    if not trace_options["trace_live"]:
                        self.replay_trace(
                            trace_rotate_labels=trace_options["trace_rotate_labels"],
                            trace_delay=trace_options["trace_delay"]
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



class BuscaBidirecional(SearchAlgorithm):
    """
    This class implements the Two-way strategy with Busca em Largura.
    """
    def search(
            self,
            initial_state: State,
            final_state: State,
            /,
            _m: None = None,
            pruning: Literal["without", "father-son", "general"] = "without",
            *,
            trace: bool = False,
            **kwargs: TraceOptions,
        ) -> Node | None:
        trace_options: TraceOptions = super().get_trace_options(kwargs)
        super().validate_pruning_option(pruning)

        def reverse_hierarchy(n: Node):
            l: list[Node] = [n]
            while (father:=n.father_node) is not None:
                l.append(father)

            new_n = n
            i = 1
            while i < len(l):
                new_n. 
            

        # Set to keep track of the visited nodes
        states: set[State] = set()
        # Creating a Queue
        open_list_start: deque[Node] = deque()
        open_list_end: deque[Node] = deque()
        open_list_start.append(Node(initial_state, None))
        open_list_end.append(Node(final_state), None)
        goal: set[State] = set()
        while len(open_list_end) > 0 and len(open_list_start) > 0:
            n_start: Node = open_list_start.popleft()
            n_end: Node = open_list_end.popleft()

            if n_start in goal:
                pass
                
            for i in n_start.state.successors():
                new_n: Node = Node(i, n_start)
                # without pruning
                if pruning == "without":
                    open_list_start.append(new_n)
                # father-son pruning
                elif pruning == "father-son" and (
                    new_n.state.env() != n_start.state.env()
                ):
                    open_list_start.append(new_n)
                # general pruning
                elif pruning == "general" and (
                    new_n.state.env() not in states
                ):
                    open_list_start.append(new_n)
                    states.add(new_n.state.env())

            for i in n_end.state.successors():
                new_n: Node = Node(i, n_end)
                # without pruning
                if pruning == "without":
                    open_list_end.append(new_n)
                # father-son pruning
                elif pruning == "father-son" and (
                    new_n.state.env() != n_end.state.env()
                ):
                    open_list_end.append(new_n)
                # general pruning
                elif pruning == "general" and (
                    new_n.state.env() not in states
                ):
                    open_list_end.append(new_n)
                    states.add(new_n.state.env())

            
