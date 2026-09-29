"""Connect Four state for the search algorithms in ``aigyminsper``.

Player 1 (X) is the maximizing player and player -1 (O) is the minimizing
player.  A move consists of selecting a column; the piece falls to the lowest
empty row in that column.
"""

from __future__ import annotations

from typing import Iterable

from aigyminsper.search.graph import State
from aigyminsper.search.search_algorithms import MinMax
from aigyminsper.search.graph import Node


# ConnectFour specs
ROWS = 6
COLUMNS = 7
EMPTY = 0
MAX_PLAYER = 1
MIN_PLAYER = -1


class ConnectFour(State):
    """Immutable Connect Four position compatible with ``State``."""

    def __init__(
        self,
        board: tuple[tuple[int, ...], ...] | None = None,
        player: int = MAX_PLAYER,
        op: str = "",
    ) -> None:
        """
        This method implements the initialization of a ConnectFour state,
        generating a 6x7 `board`, setting the actual `player` turn and defining the `operation` done
        
        """
        super().__init__(op)
        self.board = board or tuple(
            tuple(EMPTY for _ in range(COLUMNS)) for _ in range(ROWS)
        )
        self.player = player

        # Checking connect four specs
        if len(self.board) != ROWS or any(
            len(row) != COLUMNS for row in self.board
        ):
            raise ValueError("The board must have 6 rows and 7 columns.")
        if self.player not in (MAX_PLAYER, MIN_PLAYER):
            raise ValueError("player must be 1 (X) or -1 (O).")

    def successors(self) -> list["ConnectFour"]:
        """Return every legal position after the current player's move."""
        if self.is_goal():
            return []

        states = []
        for column in range(COLUMNS):
            # See if column has an empty space, if None then continue.
            row = self._available_row(column)
            if row is None:
                continue

            new_board = [list(line) for line in self.board]
            new_board[row][column] = self.player
            states.append(
                ConnectFour(
                    tuple(tuple(line) for line in new_board),
                    -self.player,
                    f"column {column + 1}",
                )
            )
        return states

    def is_goal(self) -> bool:
        """
            A terminal state is a victory for either player or a draw.
        """
        return self.winner() != EMPTY or all(
            self.board[0][column] != EMPTY for column in range(COLUMNS)
        )

    def winner(self) -> int:
        """Return 1 for X, -1 for O, or 0 when nobody has won."""
        for window in self._windows():
            total = sum(window)
            if total == 4:
                return MAX_PLAYER
            if total == -4:
                return MIN_PLAYER
        return EMPTY

    def description(self) -> str:
        return (
            "Connect Four: X maximizes the score and O minimizes it. "
            "Four equal pieces in any direction win the game."
        )

    def cost(self) -> int:
        """Return terminal utility or a heuristic for a depth cutoff."""
        winner = self.winner()
        if winner == MAX_PLAYER:
            return 1_000_000
        if winner == MIN_PLAYER:
            return -1_000_000

        score = 0
        # Owning the central column creates more potential lines.
        score += 6 * sum(self.board[row][COLUMNS // 2] for row in range(ROWS))
        for window in self._windows():
            score += self._window_score(window)
        return score

    def h(self) -> int:
        return self.cost()

    def env(self) -> str:
        """Uniquely identify the board and the player whose turn it is."""
        cells = "".join(str(cell + 1) for row in self.board for cell in row)
        return f"{cells}#{self.player}"

    def __str__(self) -> str:
        symbols = {EMPTY: ".", MAX_PLAYER: "X", MIN_PLAYER: "O"}
        lines = [" ".join(symbols[cell] for cell in row) for row in self.board]
        lines.append("1 2 3 4 5 6 7")
        return "\n".join(lines)

    def _available_row(self, column: int) -> int | None:
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][column] == EMPTY:
                return row
        return None

    def _windows(self) -> Iterable[tuple[int, int, int, int]]:
        """
            Generator to check each column, row and diagonal in the bord.
        """
        # Horizontal windows.
        for row in range(ROWS):
            for column in range(COLUMNS - 3):
                yield tuple(self.board[row][column + offset] for offset in range(4))

        # Vertical windows.
        for row in range(ROWS - 3):
            for column in range(COLUMNS):
                yield tuple(self.board[row + offset][column] for offset in range(4))

        # Down-right diagonals.
        for row in range(ROWS - 3):
            for column in range(COLUMNS - 3):
                yield tuple(
                    self.board[row + offset][column + offset] for offset in range(4)
                )

        # Up-right diagonals.
        for row in range(3, ROWS):
            for column in range(COLUMNS - 3):
                yield tuple(
                    self.board[row - offset][column + offset] for offset in range(4)
                )

    @staticmethod
    def _window_score(window: tuple[int, int, int, int]) -> int:
        max_count = window.count(MAX_PLAYER)
        min_count = window.count(MIN_PLAYER)
        empty_count = window.count(EMPTY)

        if max_count and min_count:
            return 0
        if max_count == 3 and empty_count == 1:
            return 100
        if max_count == 2 and empty_count == 2:
            return 10
        if min_count == 3 and empty_count == 1:
            return -120  # Blocking an immediate loss is slightly more urgent.
        if min_count == 2 and empty_count == 2:
            return -10
        return 0

def main() -> None:
    play(40, m=4, opponent_m=4)
    


def play(n=10, m=4, opponent_m=5):
    state = ConnectFour()
    print("Initial board:")
    print(state)

    algorithm = MinMax()

    for i in range(n):
        result = algorithm.search(state, start=0 if state.player == 1 else -1, m=m if state.player == 1 else opponent_m)
        print(f"State {i+1}: ")
        child = result
        parent = result.father_node if result.father_node else result
        while (p:=parent.father_node) is not None:
            child = parent
            parent = p
        state = child.get_state()
        if state.is_goal():
            break
        print(state)

    if (state.is_goal()):
        print("Win state")
        print(state)
        print(f"Winner player: {"You" if state.winner() == 1 else "Opponent" if state.winner() == -1 else "Draw"}")
    else:
        print("Final state")
        print(state)



if __name__ == "__main__":
    main()
