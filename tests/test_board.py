from src.board import Board


def test_init_board():
    board = Board(5, 5)
    assert ([2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 1, 0, 2, 1],
            [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]) in board.matrix
    assert board.rows == 5
    assert board.columns == 5
    assert board.board_position_x == 200
    assert board.board_position_y == 0


def test_is_winner_1():
    board = Board(5, 5)
    board.matrix = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0]]
    assert board.is_winner() == 1


def test_is_winner_2():
    board = Board(5, 5)
    board.matrix = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0],
        [0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0]]
    assert board.is_winner() == 2


def test_is_winner_none():
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 0, 0, 2, 0],
        [0, 1, 2, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0]]
    assert board.is_winner() is None


def test_chosen_position():
    board = Board(5, 9)
    assert board.chosen_position(150, 150) == (1, 1)


def test_diagonal_moves():
    board = Board(3, 3)
    assert (0, 0) in board.diagonal_moves()
    assert (2, 2) in board.diagonal_moves()
    assert (1, 1) in board.diagonal_moves()
    assert (0, 2) in board.diagonal_moves()
    assert (2, 0) in board.diagonal_moves()
    assert len(board.diagonal_moves()) == 5


def test_possible_moves():
    board = Board(3, 3)
    board.matrix = [
        [0, 0, 0],
        [1, 2, 2],
        [2, 1, 1]]
    assert (1, 1, 0, 0) in board.possible_moves(2)
    assert (1, 1, 0, 1) in board.possible_moves(2)
    assert (1, 1, 0, 2) in board.possible_moves(2)
    assert (1, 2, 0, 2) in board.possible_moves(2)
    assert len(board.possible_moves(2)) == 4


def test_capturing_moves():
    board = Board(3, 3)
    board.matrix = [
        [0, 0, 0],
        [1, 2, 2],
        [2, 1, 1]]
    assert (1, 1, 0, 0) in board.capturing_moves(2, 1)
    assert (1, 1, 0, 1) in board.capturing_moves(2, 1)
    assert (1, 2, 0, 2) in board.capturing_moves(2, 1)
    assert len(board.capturing_moves(2, 1)) == 3


def test_captured_stone():
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 0, 0, 2, 0],
        [0, 1, 2, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0]]
    assert (2, 4) in board.captured_stones(1, (2, 2, 2, 3))[0]
    assert (2, 1) in board.captured_stones(1, (2, 2, 2, 3))[1]


def test_empty_places():
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 0, 0, 2, 0],
        [0, 1, 2, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0]]
    assert (1, 4) in board.empty_places(2, 4)
    assert (3, 4) in board.empty_places(2, 4)
    assert (2, 3) in board.empty_places(2, 4)
    assert len(board.empty_places(2, 4)) == 3
