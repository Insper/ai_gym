import time

class KnightBoard:

    MOVES = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

    def __init__(self, board_size=8):
        self.board_size = board_size
        self.board = [[-1 for _ in range(board_size)] for _ in range(board_size)]

    def is_valid_move(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[x][y] == -1

    def successor_count(self, x, y):
        count = 0
        for move in KnightBoard.MOVES:
            new_x, new_y = x + move[0], y + move[1]
            if self.is_valid_move(new_x, new_y):
                count += 1
        return count

    def solve_knight_tour(self, x, y, move_count):
        if move_count == self.board_size ** 2:
            return True
        neighbors = [(x + move[0], y + move[1]) for move in KnightBoard.MOVES if self.is_valid_move(x + move[0], y + move[1])]
        neighbors.sort(key=lambda pos: self.successor_count(*pos))  # Warnsdorff's Rule

        for new_x, new_y in neighbors:
            self.board[new_x][new_y] = move_count
            if self.solve_knight_tour(new_x, new_y, move_count + 1):
                return True
            self.board[new_x][new_y] = -1  # Backtrack

        return False

def main(start_x=0, start_y=0):
    ts = time.time()
    board = KnightBoard()
    if not board.is_valid_move(start_x, start_y):
        print("Invalid starting position!")
        return
    board.board[start_x][start_y] = 0
    if board.solve_knight_tour(start_x, start_y, 1):
        for row in board.board:
            print(row)
    else:
        print("No solution found!")
    tf = time.time()
    print('Processing time in seconds:', tf-ts)

if __name__ == '__main__':
    x = int(input("Enter the starting x position (0 to 7): "))
    y = int(input("Enter the starting y position (0 to 7): "))
    main(x, y)
