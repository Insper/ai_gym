"""Tests for the MinMax search algorithm with the game state examples."""

import pytest

from aigyminsper.search.search_algorithms import MinMax

from .ConnectFour import ConnectFour
from .NoughtsNCrosses import NoughtsNCrosses


@pytest.mark.parametrize(
    ("state", "expected_operator"),
    [
        (
            NoughtsNCrosses(
                board=(
                    (1, 1, 0),
                    (-1, -1, 0),
                    (0, 0, 0),
                ),
                player=1,
            ),
            "column 3, row 1",
        ),
        (
            ConnectFour(
                board=(
                    (0, 0, 0, 0, 0, 0, 0),
                    (0, 0, 0, 0, 0, 0, 0),
                    (0, 0, 0, 0, 0, 0, 0),
                    (0, 0, 0, 0, 0, 0, 0),
                    (0, 0, 0, 0, 0, 0, 0),
                    (1, 1, 1, 0, -1, -1, 0),
                ),
                player=1,
            ),
            "column 4",
        ),
    ],
    ids=("noughts-and-crosses", "connect-four"),
)
def test_max_player_selects_an_immediate_win(state, expected_operator):
    result = MinMax().search(state, start=0, m=1)

    assert result.state.operator == expected_operator
    assert result.state.winner() == 1
    assert result.state.cost() == 1_000_000


@pytest.mark.parametrize(
    ("state", "expected_operator"),
    [
        (
            NoughtsNCrosses(
                board=(
                    (-1, -1, 0),
                    (1, 1, 0),
                    (0, 0, 0),
                ),
                player=-1,
            ),
            "column 3, row 1",
        ),
        (
            ConnectFour(
                board=(
                    (0, 0, 0, 0, 0, 0, 0),
                    (0, 0, 0, 0, 0, 0, 0),
                    (0, 0, 0, 0, 0, 0, 0),
                    (0, 0, 0, 0, 0, 0, 0),
                    (0, 0, 0, 0, 0, 0, 0),
                    (-1, -1, -1, 0, 1, 1, 0),
                ),
                player=-1,
            ),
            "column 4",
        ),
    ],
    ids=("noughts-and-crosses", "connect-four"),
)
def test_min_player_selects_an_immediate_win(state, expected_operator):
    result = MinMax().search(state, start=1, m=1)

    assert result.state.operator == expected_operator
    assert result.state.winner() == -1
    assert result.state.cost() == -1_000_000


@pytest.mark.parametrize(
    "state",
    [
        NoughtsNCrosses(
            board=(
                (1, 1, 1),
                (-1, -1, 0),
                (0, 0, 0),
            ),
            player=-1,
        ),
        ConnectFour(
            board=(
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0),
                (1, 1, 1, 1, -1, -1, 0),
            ),
            player=-1,
        ),
    ],
    ids=("noughts-and-crosses", "connect-four"),
)
def test_terminal_state_returns_the_initial_node(state):
    result = MinMax().search(state, start=1, m=2)

    assert result.state is state
    assert result.father_node is None
    assert result.g == 0


def test_trace_records_tree_and_replays_selected_path(monkeypatch, capsys):
    state = NoughtsNCrosses(
        board=(
            (1, 1, 0),
            (-1, -1, 0),
            (0, 0, 0),
        ),
        player=1,
    )
    algorithm = MinMax()
    replay_options = []
    monkeypatch.setattr(
        algorithm,
        "replay_trace",
        lambda **options: replay_options.append(options),
    )

    result = algorithm.search(
        state,
        start=0,
        m=1,
        trace=True,
        trace_live=False,
        trace_hold_graph=False,
        trace_delay=0,
    )

    assert result.state.winner() == 1
    assert algorithm.trace_graph.number_of_nodes() == 6
    assert algorithm.trace_graph.number_of_edges() == 5

    evaluation_frames = algorithm.trace_frames[:-1]
    final_frame = algorithm.trace_frames[-1]
    assert any(frame["terminal"] for frame in evaluation_frames)
    assert not any(frame["goal"] for frame in evaluation_frames)
    assert final_frame["terminal"] is True
    assert final_frame["goal"] is True
    assert len(final_frame["highlighted_edges"]) == result.depth
    assert replay_options == [
        {
            "trace_rotate_labels": True,
            "trace_delay": 0,
            "trace_hold_graph": False,
        }
    ]
    assert capsys.readouterr().out == ""


def test_live_trace_does_not_start_replay(monkeypatch):
    state = NoughtsNCrosses(
        board=(
            (1, 1, 0),
            (-1, -1, 0),
            (0, 0, 0),
        ),
        player=1,
    )
    algorithm = MinMax()
    graph_calls = []
    monkeypatch.setattr(
        algorithm,
        "graph_trace",
        lambda *args, **options: graph_calls.append((args, options)),
    )
    monkeypatch.setattr(
        algorithm,
        "replay_trace",
        lambda **options: pytest.fail("live trace must not start replay"),
    )

    result = algorithm.search(
        state,
        start=0,
        m=1,
        trace=True,
        trace_live=True,
        trace_hold_graph=False,
    )

    assert result.state.winner() == 1
    assert graph_calls
    assert graph_calls[-1][1]["trace_terminal"] is True
    assert graph_calls[-1][1]["trace_highlight_path"] is True


def test_reused_algorithm_starts_a_new_trace(monkeypatch):
    state = NoughtsNCrosses(
        board=(
            (1, 1, 0),
            (-1, -1, 0),
            (0, 0, 0),
        ),
        player=1,
    )
    algorithm = MinMax()
    monkeypatch.setattr(algorithm, "replay_trace", lambda **options: None)

    algorithm.search(state, start=0, m=1, trace=True)
    first_frame_count = len(algorithm.trace_frames)
    first_node_count = algorithm.trace_graph.number_of_nodes()

    algorithm.search(state, start=0, m=1, trace=True)

    assert len(algorithm.trace_frames) == first_frame_count
    assert algorithm.trace_graph.number_of_nodes() == first_node_count


def test_deep_search_uses_bounded_trace_with_complete_selected_path(
    monkeypatch,
):
    algorithm = MinMax()
    monkeypatch.setattr(algorithm, "replay_trace", lambda **options: None)

    result = algorithm.search(
        NoughtsNCrosses(),
        start=0,
        m=4,
        trace=True,
    )

    final_frame = algorithm.trace_frames[-1]
    assert result.depth == 4
    assert len(algorithm.trace_frames) < 100
    assert len(final_frame["highlighted_edges"]) == result.depth
    assert all(
        algorithm.trace_graph.has_edge(*edge)
        for edge in final_frame["highlighted_edges"]
    )
