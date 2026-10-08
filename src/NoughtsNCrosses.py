"""Noughts & Crosses (tic-tac-toe) example using MinMax."""

from __future__ import annotations

from collections.abc import Iterable

from aigyminsper.search.graph import State
from aigyminsper.search.search_algorithms import MinMax


ROWS = 3
COLUMNS = 3
WIN_SEQUENCE = 3
# MinMax maximizes positive values for X and minimizes them for O.
MAX_PLAYER = 1
MIN_PLAYER = -1
EMPTY = 0


class NoughtsNCrosses(State):
    """Immutable game position where X maximizes and O minimizes utility."""

    def __init__(
        self,
        board: tuple[tuple[int, ...], ...] | None = None,
        player: int = MAX_PLAYER,
        op: str = "",
    ) -> None:
        """Create a position and identify which player moves next.

        ``board`` uses ``1`` for X, ``-1`` for O, and ``0`` for an empty
        square. ``op`` describes the move that produced this state.
        """
        super().__init__(op)
        self.board = board or tuple(
            tuple(EMPTY for _ in range(COLUMNS)) for _ in range(ROWS)
        )
        self.player = player

        if len(self.board) != ROWS or any(
            len(row) != COLUMNS for row in self.board
        ):
            raise ValueError("The board must have 3 rows and 3 columns.")
        if self.player not in (MAX_PLAYER, MIN_PLAYER):
            raise ValueError("player must be 1 (X) or -1 (O).")

    def successors(self) -> list[NoughtsNCrosses]:
        """Return one new state for every legal move by the current player.

        A terminal position has no children. Otherwise, each empty square
        creates a copied board containing the current player's mark. The next
        state changes the player so MinMax alternates between X and O.
        """
        # A finished game must not expand into additional positions.
        if self.is_goal():
            return []

        states = []
        # Each empty square represents one possible move from this position.
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.board[row][column] != EMPTY:
                    continue

                # Copy the immutable board, make the move, and freeze it again.
                new_board = [list(line) for line in self.board]
                new_board[row][column] = self.player
                states.append(
                    NoughtsNCrosses(
                        tuple(tuple(line) for line in new_board),
                        -self.player,
                        f"row {row + 1}, column {column + 1}",
                    )
                )
        return states

    def is_goal(self) -> bool:
        """Return whether the position is a win or a draw.

        A winner ends the game immediately. With no winner, a full board is a
        draw and is also terminal.
        """
        return self.winner() != EMPTY or all(
            cell != EMPTY for row in self.board for cell in row
        )

    def cost(self) -> int:
        """Return terminal utility or a heuristic at a depth cutoff.

        Winning states receive values that dominate every heuristic score.
        For unfinished games, occupying the center is useful and each row,
        column, or diagonal is scored by how close it is to becoming a win.
        """
        winner = self.winner()
        if winner == MAX_PLAYER:
            return 1_000_000
        if winner == MIN_PLAYER:
            return -1_000_000

        # Prefer the center, which belongs to four possible winning lines.
        score = 6 * self.board[ROWS // 2][COLUMNS // 2]
        return score + sum(
            self._window_score(window) for window in self._windows()
        )

    def description(self) -> str:
        """Describe the adversarial problem represented by this state."""
        return (
            "Noughts & Crosses: X maximizes utility and O minimizes it. "
            "Three equal pieces in a row, column, or diagonal win."
        )

    def env(self) -> str:
        """Uniquely identify both the board and the next player.

        Including the player prevents equal boards with different turns from
        being treated as the same search state.
        """
        cells = "".join(str(cell + 1) for row in self.board for cell in row)
        return f"{cells}#{self.player}"

    def winner(self) -> int:
        """Return 1 for X, -1 for O, or 0 when nobody has won.

        Because X is 1 and O is -1, summing a line detects three identical
        marks without separate checks for every board direction.
        """
        for window in self._windows():
            total = sum(window)
            if total == WIN_SEQUENCE:
                return MAX_PLAYER
            if total == -WIN_SEQUENCE:
                return MIN_PLAYER
        return EMPTY

    def __str__(self) -> str:
        """Render the numeric board as X, O, and empty-square symbols."""
        symbols = {EMPTY: ".", MAX_PLAYER: "X", MIN_PLAYER: "O"}
        rows = [
            " | ".join(symbols[cell] for cell in row) for row in self.board
        ]
        return "\n---------\n".join(rows)

    def _windows(self) -> Iterable[tuple[int, ...]]:
        """Yield all rows, columns, and diagonals that can contain a win."""
        # Rows are already stored as tuples in the board.
        yield from self.board
        # Build each column by selecting the same index from every row.
        for column in range(COLUMNS):
            yield tuple(self.board[row][column] for row in range(ROWS))
        # Finish with the main diagonal and the opposite diagonal.
        yield tuple(self.board[index][index] for index in range(ROWS))
        yield tuple(
            self.board[index][COLUMNS - index - 1] for index in range(ROWS)
        )

    @staticmethod
    def _window_score(window: tuple[int, ...]) -> int:
        """Estimate a line without rewarding lines blocked by both players.

        Two marks and one empty square are more urgent than one mark and two
        empty squares. O's immediate threat is slightly stronger so X blocks
        it instead of choosing an equally attractive attacking line.
        """
        max_count = window.count(MAX_PLAYER)
        min_count = window.count(MIN_PLAYER)
        empty_count = window.count(EMPTY)

        if max_count and min_count:
            return 0
        if max_count == 2 and empty_count == 1:
            return 40
        if min_count == 2 and empty_count == 1:
            return -44
        if max_count == 1 and empty_count == 2:
            return 10
        if min_count == 1 and empty_count == 2:
            return -10
        return 0


def first_move(result):
    """Return the state immediately below the root of a MinMax result path.

    MinMax returns the evaluated leaf. Following parent nodes upward reveals
    the first move selected from the current board.
    """
    child = result
    while (
        child.father_node is not None
        and child.father_node.father_node is not None
    ):
        child = child.father_node
    return child.get_state()


def play(maximum_turns: int = 9, depth: int = 4, trace: bool = False) -> None:
    """Play X and O with MinMax until a win, draw, or turn limit.

    ``start=0`` selects the maximizing turn for X and ``start=1`` selects the
    minimizing turn for O. ``depth`` limits how far each decision looks ahead,
    while ``trace`` enables the search-tree visualization.
    """
    state = NoughtsNCrosses()
    algorithm = MinMax()

    print("Initial board:")
    print(state)

    for turn in range(1, maximum_turns + 1):
        # Ask MinMax for the best path for whichever player moves next.
        result = algorithm.search(
            state,
            start=0 if state.player == MAX_PLAYER else 1,
            m=depth,
            trace=trace,
            trace_hold_graph=False,
            trace_delay=0.02,
        )
        if result is None:
            break

        # Only the first move in the chosen path is played before searching again.
        state = first_move(result)
        print(f"\nTurn {turn}: {state.operator}")
        print(state)
        if state.is_goal():
            break

    outcome = {
        MAX_PLAYER: "X wins",
        MIN_PLAYER: "O wins",
        EMPTY: "Draw" if state.is_goal() else "Turn limit reached",
    }
    print(f"\nResult: {outcome[state.winner()]}")


if __name__ == "__main__":
    play()
