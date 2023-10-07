import pytest
from main import KnightBoard

@pytest.fixture
def setup_board():
    return KnightBoard()

def test_default_start(setup_board):
    board = setup_board
    board.board[0][0] = 0
    result = board.solve_knight_tour(0, 0, 1)
    assert result == True

def test_known_result_start_0_0(setup_board):
    board = setup_board
    board.board[0][0] = 0
    result = board.solve_knight_tour(0, 0, 1)
    
    expected_board = [
        [0, 33, 2, 17, 48, 31, 12, 15],
        [3, 18, 55, 32, 13, 16, 49, 30],
        [56, 1, 34, 47, 54, 51, 14, 11],
        [19, 4, 59, 52, 35, 46, 29, 50],
        [40, 57, 36, 45, 60, 53, 10, 25],
        [5, 20, 41, 58, 37, 26, 63, 28],
        [42, 39, 22, 7, 44, 61, 24, 9],
        [21, 6, 43, 38, 23, 8, 27, 62]
    ]
    
    assert result == True
    assert board.board == expected_board


def test_known_result_start_0_1(setup_board):
    board = setup_board
    board.board[0][1] = 0
    result = board.solve_knight_tour(0, 1, 1)

    expected_board = [
        [13, 0, 43, 28, 15, 10, 19, 22],
        [44, 29, 14, 11, 42, 21, 16, 9],
        [1, 12, 39, 46, 27, 18, 23, 20],
        [30, 45, 56, 63, 38, 41, 8, 17],
        [59, 2, 47, 40, 55, 26, 37, 24],
        [48, 31, 60, 57, 62, 35, 52, 7],
        [3, 58, 33, 50, 5, 54, 25, 36],
        [32, 49, 4, 61, 34, 51, 6, 53]
    ]

    assert result == True
    assert board.board == expected_board

def test_invalid_start(setup_board):
    board = setup_board
    result = board.solve_knight_tour(10, 10, 1)  # 10,10 is out of bounds for an 8x8 board
    assert result == False

