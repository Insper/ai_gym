"""Exemplo de Jogo da Velha usando MinMax."""

from __future__ import annotations

from collections.abc import Iterable

from aigyminsper.search.graph import State
from aigyminsper.search.search_algorithms import MinMax


ROWS = 3
COLUMNS = 3
WIN_SEQUENCE = 3
# O MinMax maximiza valores positivos para X e minimiza valores para O.
MAX_PLAYER = 1
MIN_PLAYER = -1
EMPTY = 0


class NoughtsNCrosses(State):
    """Posição imutável em que X maximiza e O minimiza a utilidade."""

    def __init__(
        self,
        board: tuple[tuple[int, ...], ...] | None = None,
        player: int = MAX_PLAYER,
        op: str = "",
    ) -> None:
        """Cria uma posição e identifica qual jogador fará a próxima jogada.

        ``board`` usa ``1`` para X, ``-1`` para O e ``0`` para uma casa
        vazia. ``op`` descreve a jogada que produziu este estado.
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
        """Retorna um novo estado para cada jogada válida do jogador atual.

        Uma posição terminal não possui filhos. Caso contrário, cada casa
        vazia cria uma cópia do tabuleiro com a marca do jogador atual. O novo
        estado troca o jogador para que o MinMax alterne entre X e O.
        """
        # Um jogo encerrado não deve gerar outras posições.
        if self.is_goal():
            return []

        states = []
        # Cada casa vazia representa uma jogada possível nesta posição.
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.board[row][column] != EMPTY:
                    continue

                # Copia o tabuleiro imutável, faz a jogada e o congela novamente.
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
        """Retorna se a posição representa vitória ou empate.

        Um vencedor encerra o jogo imediatamente. Sem vencedor, um tabuleiro
        cheio representa empate e também é um estado terminal.
        """
        return self.winner() != EMPTY or all(
            cell != EMPTY for row in self.board for cell in row
        )

    def cost(self) -> int:
        """Retorna a utilidade terminal ou uma heurística no limite de profundidade.

        Estados vencedores recebem valores que dominam qualquer pontuação
        heurística. Em jogos inacabados, ocupar o centro é vantajoso e cada
        linha, coluna ou diagonal é avaliada pela proximidade de uma vitória.
        """
        winner = self.winner()
        if winner == MAX_PLAYER:
            return 1_000_000
        if winner == MIN_PLAYER:
            return -1_000_000

        # Prefere o centro, que pertence a quatro possíveis linhas vencedoras.
        score = 6 * self.board[ROWS // 2][COLUMNS // 2]
        return score + sum(
            self._window_score(window) for window in self._windows()
        )

    def description(self) -> str:
        """Descreve o problema adversarial representado por este estado."""
        return (
            "Noughts & Crosses: X maximizes utility and O minimizes it. "
            "Three equal pieces in a row, column, or diagonal win."
        )

    def env(self) -> str:
        """Identifica unicamente o tabuleiro e o próximo jogador.

        Incluir o jogador impede que tabuleiros iguais com turnos diferentes
        sejam tratados como o mesmo estado de busca.
        """
        cells = "".join(str(cell + 1) for row in self.board for cell in row)
        return f"{cells}#{self.player}"

    def winner(self) -> int:
        """Retorna 1 para X, -1 para O ou 0 quando ninguém venceu.

        Como X vale 1 e O vale -1, somar uma linha detecta três símbolos iguais
        sem verificações separadas para cada direção do tabuleiro.
        """
        for window in self._windows():
            total = sum(window)
            if total == WIN_SEQUENCE:
                return MAX_PLAYER
            if total == -WIN_SEQUENCE:
                return MIN_PLAYER
        return EMPTY

    def __str__(self) -> str:
        """Exibe o tabuleiro numérico com símbolos X, O e casas vazias."""
        symbols = {EMPTY: ".", MAX_PLAYER: "X", MIN_PLAYER: "O"}
        rows = [
            " | ".join(symbols[cell] for cell in row) for row in self.board
        ]
        return "\n---------\n".join(rows)

    def _windows(self) -> Iterable[tuple[int, ...]]:
        """Produz todas as linhas, colunas e diagonais que podem conter vitória."""
        # As linhas já estão armazenadas como tuplas no tabuleiro.
        yield from self.board
        # Monta cada coluna selecionando o mesmo índice de todas as linhas.
        for column in range(COLUMNS):
            yield tuple(self.board[row][column] for row in range(ROWS))
        # Finaliza com a diagonal principal e a diagonal oposta.
        yield tuple(self.board[index][index] for index in range(ROWS))
        yield tuple(
            self.board[index][COLUMNS - index - 1] for index in range(ROWS)
        )

    @staticmethod
    def _window_score(window: tuple[int, ...]) -> int:
        """Estima uma linha sem premiar linhas bloqueadas pelos dois jogadores.

        Duas marcas e uma casa vazia são mais urgentes do que uma marca e duas
        casas vazias. A ameaça imediata de O recebe peso um pouco maior para X
        bloqueá-la em vez de escolher uma linha de ataque igualmente atraente.
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
    """Retorna o estado logo abaixo da raiz do caminho resultante do MinMax.

    O MinMax retorna a folha avaliada. Percorrer os nós pais para cima revela
    a primeira jogada escolhida a partir do tabuleiro atual.
    """
    child = result
    while (
        child.father_node is not None
        and child.father_node.father_node is not None
    ):
        child = child.father_node
    return child.get_state()


def play(maximum_turns: int = 9, depth: int = 4, trace: bool = False) -> None:
    """Joga com X e O via MinMax até vitória, empate ou limite de turnos.

    ``start=0`` seleciona o turno maximizador de X e ``start=1`` seleciona o
    turno minimizador de O. ``depth`` limita a profundidade de cada decisão,
    enquanto ``trace`` ativa a visualização da árvore de busca.
    """
    state = NoughtsNCrosses()
    algorithm = MinMax()

    print("Initial board:")
    print(state)

    for turn in range(1, maximum_turns + 1):
        # Solicita ao MinMax o melhor caminho para o próximo jogador.
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

        # Joga apenas o primeiro movimento antes de executar uma nova busca.
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
