from typing import Iterable

from aigyminsper.search.search_algorithms import MinMax
from aigyminsper.search.graph import State


# Noughts&Crosses specs
ROWS = 3
COLUMNS = 3
WIN_SEQUENCE = 3
MAX_PLAYER = 1
MIN_PLAYER = -1
EMPTY = 0

if (WIN_SEQUENCE > ROWS or WIN_SEQUENCE > COLUMNS):
    raise RuntimeError("Cannot create a board for Noughts&Crosses with these specs")

class NoughtsNCrosses(State):
    def __init__(self, board: tuple[tuple[int, ...]] | None = None, player: int = MAX_PLAYER, op: str = ""):
        super().__init__(op)
        self.board = board or tuple(tuple(EMPTY for _ in range(COLUMNS)) for _ in range(ROWS))
        self.player = player

    def successors(self) -> list["NoughtsNCrosses"]:
        """Return every legal position after the current player's move."""
        if self.is_goal():
            return []

        states = []
        for column in range(COLUMNS):
            for row in range(ROWS):
                if self.board[row][column] == EMPTY:
                    new_board = [list(line) for line in self.board]
                    new_board[row][column] = self.player
                    states.append(
                        NoughtsNCrosses(
                            tuple(tuple(line) for line in new_board),
                            -self.player,
                            f"column {column + 1}, row {row + 1}",
                        )
                    )
        return states

    def is_goal(self) -> bool:
        """
            A terminal state is a victory for either player or a draw.
        """
        return self.winner() != EMPTY or all(
            (
                all(self.board[row][column] != EMPTY for column in range(COLUMNS)) for row in range(ROWS)
            )
        )

    def cost(self) -> int:
        """Return terminal utility or a heuristic for a depth cutoff."""
        winner = self.winner()
        if winner == MAX_PLAYER:
            return 1_000_000
        if winner == MIN_PLAYER:
            return -1_000_000

        score = 0
        # Owning the central column / row creates more potential lines.
        score += 6 * self.board[ROWS//2][COLUMNS // 2]
        for window in self._windows():
            score += self._window_score(window)
        return score

    def description(self) -> str:
        return (
            "Noughts&Crosses: X maximizes the score and O minimizes it. "
            "In the standard form, 3 equal pieces in any direction win the game."
        )

    def env(self) -> str:
        """Uniquely identify the board and the player whose turn it is."""
        cells = "".join(str(cell + 1) for row in self.board for cell in row)
        return f"{cells}#{self.player}"

    def winner(self) -> int:
        """Return 1 for X, -1 for O, or 0 when nobody has won."""
        for window in self._windows():
            total = sum(window)
            
            if total == WIN_SEQUENCE:
                return MAX_PLAYER
            if total == -WIN_SEQUENCE:
                return MIN_PLAYER
        return EMPTY

    def __str__(self):
        symbols = {EMPTY: ".", MAX_PLAYER: "X", MIN_PLAYER: "O"}
        space = ROWS // 10 + 1
        lines = [str(n + 1) + (space - (n + 1)//10) * " | " for n in range(ROWS)]
        final_lines = []
        for i, line in enumerate(lines):
            new_line = line + " ".join(symbols[cell] + " |" for cell in self.board[i])
            final_lines.append(new_line[:-2])
            final_lines.append((space + 1) * " " + "|" + "-" * 4 * COLUMNS)
        final_lines.pop()
        final_lines.append((space + 1) * "-" + "-" + "-" * 4 * COLUMNS)
        final_lines.append((space + 1) * " " + "|" + "".join(" {a}  ".format(a=n) for n in range(1, COLUMNS + 1)))
        return "\n".join(final_lines)

    def _windows(self) -> Iterable[tuple[tuple[int, ...]]]:
        """
            Generator to check each column, row and diagonal in the bord.
        """
        # Horizontal windows.
        for row in range(ROWS):
            for column in range(COLUMNS - WIN_SEQUENCE + 1):
                yield tuple(self.board[row][column + offset] for offset in range(WIN_SEQUENCE))

        # Vertical windows.
        for row in range(ROWS - WIN_SEQUENCE + 1):
            for column in range(COLUMNS):
                yield tuple(self.board[row + offset][column] for offset in range(WIN_SEQUENCE))

        # Down-right diagonals.
        for row in range(ROWS - WIN_SEQUENCE + 1):
            for column in range(COLUMNS - WIN_SEQUENCE + 1):
                yield tuple(
                    self.board[row + offset][column + offset] for offset in range(WIN_SEQUENCE)
                )

        # Up-right diagonals.
        for row in range(WIN_SEQUENCE - 1, ROWS):
            for column in range(COLUMNS - WIN_SEQUENCE + 1):
                yield tuple(
                    self.board[row - offset][column + offset] for offset in range(WIN_SEQUENCE)
                )

    @staticmethod
    def _window_score(window: tuple[int, ...]) -> int:
        max_count = window.count(MAX_PLAYER)
        min_count = window.count(MIN_PLAYER)
        empty_count = window.count(EMPTY)

        if max_count and min_count:
            return 0

        if max_count == WIN_SEQUENCE - 1 and empty_count == 1:
            return 10 * max_count + 20
        if min_count == WIN_SEQUENCE - 1 and empty_count == 1:
            return -12 * min_count - 20
        
        for i in range(WIN_SEQUENCE-2, WIN_SEQUENCE//2, -1):    
            if min_count == i and empty_count == (WIN_SEQUENCE - i):
                return min_count * -10
            if max_count == 1 and empty_count == (WIN_SEQUENCE - i):
                return max_count * 10
        return 0


def main() -> None:
    play(40, m=4, opponent_m=4, trace=True)
    


def play(n=10, m=4, opponent_m=4, trace=False):
    state = NoughtsNCrosses()
    print("Initial board:")
    print(state)

    algorithm = MinMax()

    for i in range(n):
        result = algorithm.search(
            state,
            start=0 if state.player == 1 else 1,
            m=m if state.player == 1 else opponent_m,
            trace=trace,
            trace_hold_graph=False,
            trace_delay=0.02,
        )
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
