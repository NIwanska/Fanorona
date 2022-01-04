from src.players import (
    Player,
    Computer,
    paika_move,
    capturing_move,
    choose_which_to_capture,
    is_next_turn)
from src.board import Board


def test_paika_move():
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 0, 0, 2, 0],
        [0, 1, 2, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0]]
    move = (3, 3, 3, 2)
    paika_move(board, 1, move)
    assert board.matrix[3][3] == 0
    assert board.matrix[3][2] == 1


def test_capturing_move_approching():
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 0, 0, 2, 0],
        [0, 1, 2, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0]]
    player = Player(2)
    move = (1, 3, 2, 3)
    assert capturing_move(board, move, player) == (2, 3, 1, 3)
    assert board.matrix[1][3] == 0
    assert board.matrix[2][3] == 2
    assert board.matrix[3][3] == 0
    assert board.matrix[4][3] == 0
    new_board = [[0, 2, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 1, 2, 2, 0],
                 [0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0]]
    for row in new_board:
        assert row in board.matrix


def test_capturing_move_withdrawal():
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 0, 0, 2, 0],
        [0, 1, 2, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0]]
    player = Player(2)
    move = (2, 2, 2, 3)
    assert capturing_move(board, move, player) == (2, 3, 2, 2)
    assert board.matrix[2][2] == 0
    assert board.matrix[2][3] == 2
    assert board.matrix[2][1] == 0
    new_board = [[0, 2, 0, 0, 0], [0, 0, 0, 2, 0], [0, 0, 0, 2, 0],
                 [0, 0, 0, 1, 0], [0, 1, 0, 1, 0]]
    for row in new_board:
        assert row in board.matrix


def test_capturing_move_choosing(monkeypatch):
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 2, 0, 2, 0],
        [0, 1, 2, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 2, 0, 1, 0]]
    player = Player(1)
    move = (2, 1, 3, 1)

    def return_choice(f, t):
        return 4, 1
    monkeypatch.setattr(Player, "choose_stone", return_choice)
    assert capturing_move(board, move, player) == (3, 1, 2, 1)
    assert board.matrix[0][1] == 2
    assert board.matrix[1][1] == 2
    assert board.matrix[2][1] == 0
    assert board.matrix[3][1] == 1
    assert board.matrix[4][1] == 0
    new_board = [[0, 2, 0, 0, 0],
                 [0, 2, 0, 2, 0],
                 [0, 0, 2, 0, 0],
                 [0, 1, 0, 1, 0],
                 [0, 0, 0, 1, 0]]
    for row in new_board:
        assert row in board.matrix


def test_choose_which_to_capture_player(monkeypatch):
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 2, 0, 2, 0],
        [0, 1, 2, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 2, 0, 1, 0]]
    player = Player(1)

    def return_choice(f, t):
        return 1, 1
    monkeypatch.setattr(Player, "choose_stone", return_choice)
    captured_stones = ([(0, 1), (1, 1)], [(4, 1)])
    choose_which_to_capture(board, captured_stones, player)
    assert board.matrix[0][1] == 0
    assert board.matrix[1][1] == 0
    assert board.matrix[2][1] == 1
    assert board.matrix[3][1] == 0
    assert board.matrix[4][1] == 2
    new_board = [[0, 0, 0, 0, 0],
                 [0, 0, 0, 2, 0],
                 [0, 1, 2, 0, 0],
                 [0, 0, 0, 1, 0],
                 [0, 2, 0, 1, 0]]
    for row in new_board:
        assert row in board.matrix


def test_choose_which_to_capture_computer_easy(monkeypatch):
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 2, 0, 2, 0],
        [0, 1, 2, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 2, 0, 1, 0]]
    player = Computer(1, 'Easy')

    def return_choice(f):
        return 1, 1
    monkeypatch.setattr("src.players.choice", return_choice)
    captured_stones = ([(0, 1), (1, 1)], [(4, 1)])
    choose_which_to_capture(board, captured_stones, player)
    assert board.matrix[0][1] == 0
    assert board.matrix[1][1] == 0
    assert board.matrix[2][1] == 1
    assert board.matrix[3][1] == 0
    assert board.matrix[4][1] == 2
    new_board = [[0, 0, 0, 0, 0],
                 [0, 0, 0, 2, 0],
                 [0, 1, 2, 0, 0],
                 [0, 0, 0, 1, 0],
                 [0, 2, 0, 1, 0]]
    for row in new_board:
        assert row in board.matrix


def test_choose_which_to_capture_computer_hard(monkeypatch):
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 2, 0, 2, 0],
        [0, 1, 2, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 2, 0, 1, 0]]
    player = Computer(1, 'Hard')

    def return_choice(f):
        return 4, 1
    monkeypatch.setattr("src.players.choice", return_choice)
    captured_stones = ([(0, 1), (1, 1)], [(4, 1)])
    choose_which_to_capture(board, captured_stones, player)
    assert board.matrix[0][1] == 2
    assert board.matrix[1][1] == 2
    assert board.matrix[2][1] == 1
    assert board.matrix[3][1] == 0
    assert board.matrix[4][1] == 0
    new_board = [[0, 2, 0, 0, 0],
                 [0, 2, 0, 2, 0],
                 [0, 1, 2, 0, 0],
                 [0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0]]
    for row in new_board:
        assert row in board.matrix


def test_is_next_turn_false():
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 2, 0, 2, 0],
        [0, 1, 2, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 2, 0, 1, 0]]
    assert is_next_turn(board, 2, 1, 1, 3, [(2, 3)]) is False


def test_is_next_turn_True():
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 2, 0, 2, 0],
        [0, 0, 2, 0, 0],
        [0, 2, 1, 1, 0],
        [0, 0, 0, 1, 0]]
    assert is_next_turn(board, 2, 1, 3, 1, [(4, 1)]) is True


def test_init_player():
    player = Player(1)
    assert player.stone() == 1
    assert player.opponent_stone() == 2


def test_next_turn(monkeypatch):
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 2, 0, 2, 0],
        [0, 1, 2, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 2, 0, 1, 0]]
    player = Player(2)
    chosen_stone = (2, 2)
    forbidden_moves = [(3, 2)]

    def return_choice(f, t):
        return 2, 3
    monkeypatch.setattr(Player, "choose_stone", return_choice)
    assert player.next_turn(board, chosen_stone,
                            forbidden_moves) == (2, 3, 2, 2)
    assert board.matrix[2][2] == 0
    assert board.matrix[2][3] == 2
    assert board.matrix[2][1] == 0
    new_board = [[0, 2, 0, 0, 0],
                 [0, 2, 0, 2, 0],
                 [0, 0, 0, 2, 0],
                 [0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0]]
    for row in new_board:
        assert row in board.matrix


def test_init_computer():
    player = Computer(2, 'Hard')
    assert player.stone() == 2
    assert player.opponent_stone() == 1
    assert player.level() == 'Hard'


def test_next_computer_turn_easy(monkeypatch):
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 2, 0, 2, 0],
        [0, 1, 2, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 2, 0, 1, 0]]
    player = Computer(2, "Easy")
    chosen_stone = (2, 2)
    forbidden_moves = [(3, 2)]

    def return_choice(f):
        return (2, 2, 2, 3)
    monkeypatch.setattr('src.players.choice', return_choice)
    assert player.next_computer_turn(
        board, chosen_stone, forbidden_moves) == (2, 3, 2, 2)
    assert board.matrix[2][2] == 0
    assert board.matrix[2][3] == 2
    assert board.matrix[2][1] == 0
    new_board = [[0, 2, 0, 0, 0],
                 [0, 2, 0, 2, 0],
                 [0, 0, 0, 2, 0],
                 [0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0]]
    for row in new_board:
        assert row in board.matrix


def test_next_computer_turn_hard(monkeypatch):
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 2, 0, 2, 0],
        [0, 1, 2, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 2, 0, 1, 0]]
    player = Computer(2, "Hard")
    chosen_stone = (2, 2)
    forbidden_moves = [(3, 2)]

    def return_choice(f, t, y, u):
        return (2, 2, 2, 3)
    monkeypatch.setattr(Computer, 'best_drawing', return_choice)
    assert player.next_computer_turn(
        board, chosen_stone, forbidden_moves) == (2, 3, 2, 2)
    assert board.matrix[2][2] == 0
    assert board.matrix[2][3] == 2
    assert board.matrix[2][1] == 0
    new_board = [[0, 2, 0, 0, 0],
                 [0, 2, 0, 2, 0],
                 [0, 0, 0, 2, 0],
                 [0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0]]
    for row in new_board:
        assert row in board.matrix


def test_draw_move_paika(monkeypatch):
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 2, 0, 0, 0],
        [0, 1, 2, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0]]
    player = Computer(2, "Easy")

    def return_choice(f):
        return (2, 2, 3, 2)
    monkeypatch.setattr('src.players.choice', return_choice)
    assert player.draw_move(board) is None
    assert board.matrix[2][2] == 0
    assert board.matrix[3][2] == 2
    new_board = [
        [0, 2, 0, 0, 0],
        [0, 2, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 2, 1, 0],
        [0, 1, 0, 1, 0]]
    for row in new_board:
        assert row in board.matrix


def test_draw_move_capture(monkeypatch):
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 2, 0, 0, 0],
        [0, 1, 2, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0]]
    player = Computer(1, "Easy")

    def return_choice(f):
        return (2, 1, 2, 0)
    monkeypatch.setattr('src.players.choice', return_choice)
    assert player.draw_move(board) == (2, 0, 2, 1)
    assert board.matrix[2][1] == 0
    assert board.matrix[2][0] == 1
    assert board.matrix[2][2] == 0
    new_board = [
        [0, 2, 0, 0, 0],
        [0, 2, 0, 0, 0],
        [1, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0]]
    for row in new_board:
        assert row in board.matrix


def test_best_drawing_next_turn():
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 0, 0],
        [0, 2, 0, 0, 0],
        [0, 1, 2, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0]]
    player = Computer(1, "Hard")
    assert player.best_drawing(board) == (2, 1, 3, 1)


def test_best_drawing_the_most_stones():
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 2, 0],
        [0, 2, 0, 0, 0],
        [0, 1, 2, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0]]
    player = Computer(2, "Hard")
    assert player.best_drawing(board) == (0, 3, 1, 3)


def test_best_drawing_next_move_given_stone():
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 2, 0],
        [0, 2, 0, 0, 0],
        [0, 1, 2, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0]]
    player = Computer(1, "Hard")
    assert player.best_drawing(board, 2, 3) == (2, 3, 1, 3)


def test_best_drawing_the_most_stones_given_stone():
    board = Board(5, 5)
    board.matrix = [
        [0, 2, 0, 2, 0],
        [0, 2, 0, 1, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0]]
    player = Computer(2, "Hard")
    assert player.best_drawing(board, 1, 1) == (1, 1, 1, 2)


def test_best_drawing():
    board = Board(5, 5)
    board.matrix = [
        [0, 0, 1, 2, 0],
        [0, 0, 2, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0]]

    player = Computer(1, 'Hard')
    assert player.best_drawing(board, 0, 2) == (0, 2, 0, 1)
    player.next_computer_turn(board, (0, 2), [(1, 1)])
    new_board = [[0, 1, 0, 0, 0],
                 [0, 0, 2, 1, 0],
                 [0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0],
                 [0, 1, 1, 1, 0]]
    for row in new_board:
        assert row in board.matrix
