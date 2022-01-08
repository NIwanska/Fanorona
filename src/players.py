import pygame
import sys
from random import choice


class Player():
    """
    A class to represent a player. Parent class of HumanPlayer and Computer classes.

    ...

    Attributes
    ----------
    stone : int
        1 - white
        2 - black
    opponent_stone: int
        1 - white
        2 - black

    Methods
    -------
    __init__(stone):
        creates player
    stone():
        returns player's stone
    opponent_stone():
        returns opponent's stone
    paika_move(board, move):
        makes move without capturing
    capturing_move(board, move):
        makes move and captures opponent's stones
    choose_which_to_capture(board, captured_stones):
        captures chosen stones
    is_next_turn(self, board, r, c, forbidden_moves):
        returns True if there is possible next turn
    make_turn(board):
        makes turns until there are no capturing moves
    """

    def __init__(self, stone):
        """
        Constructs all the necessary attributes for the player object.

        Parameters
        ----------
        stone : int
            1 or 2
        """
        self._stone = stone
        self._opponent_stone = 1 if self._stone == 2 else 2

    def stone(self):
        """
        returns player's stone

        Returns
        -------
        player's stone
        """
        return self._stone

    def opponent_stone(self):
        """
        returns opponents's stone

        Returns
        -------
        opponent's stone
        """
        return self._opponent_stone

    def paika_move(self, board, move):
        """
        changes place from stone goes to 0 and plece where stone goes to 1 or 2
        depending on stone. Draws board.

        Parameters
        ----------
        board : Board
        stone : 1 or 2
        move : (r, c, r1, c1)

        Returns
        -------
        None
        """
        r1, c1, r, c = move
        chosen_stone = (r1, c1)
        board.matrix[chosen_stone[0]][chosen_stone[1]] = 0
        board.matrix[r][c] = self.stone()
        return

    def capturing_move(self, board, move):
        """
        changes place from stone goes to 0 and plece where stone goes to 1 or 2
        depending on stone. If capturing move is only approaching or only
        withdrawal it changes captured stone to 0 and draws board.
        if the capture is withdrawal and approaching it asks player to choose
        which stones to capture

        Parameters
        ----------
        board : Board
        move : (r1, c1, r, c)

        Returns
        -------
        move : (r, c, r1, r2)

        """
        stone = self.stone()
        opponent_stone = self.opponent_stone()
        r1, c1, r, c = move
        chosen_stone = (r1, c1)
        board.matrix[chosen_stone[0]][chosen_stone[1]] = 0
        board.matrix[r][c] = stone
        captured_stones = board.captured_stones(
            opponent_stone, move)
        if len(captured_stones[0]) != 0 and len(captured_stones[1]) != 0:
            self.choose_which_to_capture(board, captured_stones)
            return (r, c, r1, c1)

        elif len(captured_stones[0]) != 0:
            for captured_stone in captured_stones[0]:
                board.matrix[captured_stone[0]
                             ][captured_stone[1]] = 0
            return (r, c, r1, c1)
        elif len(captured_stones[1]) != 0:
            for captured_stone in captured_stones[1]:
                board.matrix[captured_stone[0]
                             ][captured_stone[1]] = 0
            return (r, c, r1, c1)

    def choose_which_to_capture(self, board, captured_stones):
        """
        if player is not computer it asks player to choose witch capture they want to do:
        approching or withdrawal. If player is computer with easy level it draw which stones to capture
        if its level is hard it takes option with more captured stones.
        It changes captured stones to 0 and draw a board

        Parameters
        ----------
        board : Board
        captured_stones : list
            tuple with lists of approaching and withdrawal captured stones

        Returns
        -------
        None

        """
        while True:
            if type(self) == HumanPlayer:
                board.draw_board()
                board.light_up_stones_to_capture(captured_stones[0])
                board.light_up_stones_to_capture(captured_stones[1])
                r, c = self.choose_stone(board)
            elif self.level() == 'Easy':
                (r, c) = choice(captured_stones[0] + captured_stones[1])
            else:
                index = 0 if len(captured_stones[0]) > len(
                    captured_stones[1]) else 1
                (r, c) = choice(captured_stones[index])
            if (r, c) in captured_stones[0]:
                for captured_stone in captured_stones[0]:
                    board.matrix[captured_stone[0]
                                 ][captured_stone[1]] = 0
                return
            elif (r, c) in captured_stones[1]:
                for captured_stone in captured_stones[1]:
                    board.matrix[captured_stone[0]
                                 ][captured_stone[1]] = 0
                return

    def is_next_turn(self, board, r, c, forbidden_moves):
        """
        returns True if from given place there is capturing move

        Parameters
        ----------
        board : Board
        r : int
            stone's row
        c : int
            stone's column
        forbidden_moves : list
            list of places where stone cannot go
        Returns
        -------
        bool

        """

        captured_stones = []
        for move in board.capturing_moves(self.stone(), self.opponent_stone()):
            is_move_available = True
            for forbidden_move in forbidden_moves:
                if move[2] == forbidden_move[0] and move[3] == forbidden_move[1]:
                    is_move_available = False
            if is_move_available and move[0] == r and move[1] == c:
                captured_stones = captured_stones + board.captured_stones(self.opponent_stone(), move)[0]\
                    + board.captured_stones(self.opponent_stone(), move)[1]
        return captured_stones

    def make_turn(self, board):
        """
        makes first move, adds forbidden moves to list and checks if next move is possible,
        it makes next turns until it is impossible

        Parameters
        ----------
        board : Board

        Returns
        -------
        None
        """

        next_turn_moves = self.first_move(board)

        forbidden_moves = []
        board.draw_board()
        while True:
            if next_turn_moves:
                r = next_turn_moves[0]
                c = next_turn_moves[1]
                forbidden_moves.append(
                    (next_turn_moves[2], next_turn_moves[3]))
                diff_r = r - next_turn_moves[2]
                diff_c = c - next_turn_moves[3]
                forbidden_moves.append((r + diff_r, c + diff_c))
                captured_stones = self.is_next_turn(
                    board, r, c, forbidden_moves)
                if bool(len(captured_stones)):
                    board.light_up_chosen_stone([(r, c)])
                    board.light_up_stones_to_capture(captured_stones)
                    next_turn_moves = self.next_turn(
                        board, (r, c), forbidden_moves)
                    forbidden_moves.pop()
                    board.draw_board()
                else:
                    return
            else:
                return


class HumanPlayer(Player):
    """
    A class to represent human player. Child class of Player class.

    Methods
    -------
    __init__(stone):
        creates player
    choose_stone(board):
        returns position of the stone if clicked on it
    first_move(board):
        start of turn, makes paika move or capturing move dependent of the next click
    next_turn( board, chosen_stone, forbidden_moves):
        it checks if chosen move is capturing and
        not forbidden and makes capturing move
    """

    def __init__(self, stone):
        """
        Creates human player.

        Parameters
        ----------
        stone : int
            1 or 2
        """
        super().__init__(stone)

    def choose_stone(self, board):
        """
        returns position of the stone if clicked on it

        Parameters
        ----------
        board : Board

        Returns
        -------
        r, c : int
            row and column of clicked stone
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not board.chosen_position(event.pos[0], event.pos[1]):
                        break
                    r, c = board.chosen_position(event.pos[0], event.pos[1])
                    return r, c

    def first_move(self, board):
        """
        start of turn, lights stones that can move,
        when stone was chosen by clicking stones that can be capture changes color to red
        makes paika move or capturing move dependent of the next click

        Parameters
        ----------
        board : Board

        Returns
        -------
        move : (r, c, r1, r2)
        """
        stone = self.stone()
        opponent_stone = self.opponent_stone()
        chosen_stone = None
        board.light_up_possible_stones(stone, opponent_stone)
        while True:
            r, c = self.choose_stone(board)
            if board.matrix[r][c] == stone:
                captured_stones = []
                board.light_up_chosen_stone([(r, c)])
                chosen_stone = (r, c)
                for move in board.possible_moves(stone):
                    if move[0] == r and move[1] == c:
                        captured_stones = captured_stones + \
                            board.captured_stones(opponent_stone, move)[0] + \
                            board.captured_stones(opponent_stone, move)[1]
                board.light_up_stones_to_capture(captured_stones)
            elif (chosen_stone
                  and (chosen_stone[0], chosen_stone[1], r, c) in board.capturing_moves(stone, opponent_stone)):
                return self.capturing_move(board, (chosen_stone[0], chosen_stone[1], r, c))

            elif (chosen_stone and (chosen_stone[0], chosen_stone[1], r, c) in board.possible_moves(stone)
                  and len(board.capturing_moves(stone, opponent_stone)) == 0):
                self.paika_move(
                    board, (chosen_stone[0], chosen_stone[1], r, c))
                return

    def next_turn(self, board, chosen_stone, forbidden_moves):
        """
        if there is possible next turn it checks if chosen move is capturing and
        not forbidden and makes capturing move
        Parameters
        ----------
        board : Board
        chosen stone : (r, c)
        forbidden_moves : list
            a list of places that where stone cannot move

        Returns
        -------
        move : (r, c, r1, r2)

        """
        while True:
            r, c = self.choose_stone(board)
            if (chosen_stone and (r, c) not in forbidden_moves
                    and (chosen_stone[0], chosen_stone[1], r, c) in
                    board.capturing_moves(self.stone(), self.opponent_stone())):
                return self.capturing_move(board, (chosen_stone[0], chosen_stone[1], r, c))


class Computer(Player):
    """
    A class to represent a Computer. Child class of Player class.
    ...

    Attributes
    ----------
    level : str
        "Easy" or "Hard"

    Methods
    -------
    __init__(stone, level):
        creates player
    level():
        returns computer's level
    next_turn(board, chosen_stone, forbidden_moves):
        draws or choose the best move and makes capturing move
    first_move(board):
        draws or choose the best move and makes possible move
    best_drawing(board):
        returns best move
    best_next_drawing(board, r, c):
        returns best move for given stone

    """

    def __init__(self, stone, level):
        """
        Creates computer player with its level

        Parameters
        ----------
        stone : int
            1 or 2
        level : str
            "Easy" or "Hard"
        """
        super().__init__(stone)
        self._level = level

    def level(self):
        """
        returns computer's level

        Returns
        -------
        computer's level
        """
        return self._level

    def next_turn(self, board, chosen_stone, forbidden_moves):
        """
        it waits two sec.
        if there is possible next turn it draws capturing move - if computer's level is easy
        and choose the best move - if computer's level is hard.
        It checkes if move is not forbidden and makes capturing move
        Parameters
        ----------
        board : Board
        chosen stone : (r, c)
        forbidden_moves : list
            a list of places that where stone cannot move

        Returns
        -------
        move : (r, c, r1, r2)

        """
        pygame.time.delay(1800)
        stone = self.stone()
        opponent_stone = self.opponent_stone()
        while True:
            if self.level() == 'Easy':
                drawing_move = choice(
                    board.capturing_moves(stone, opponent_stone))
            else:
                drawing_move = self.best_next_drawing(
                    board, chosen_stone[0], chosen_stone[1])
            r = drawing_move[2]
            c = drawing_move[3]
            if (r, c) not in forbidden_moves and chosen_stone[0] == drawing_move[0] and chosen_stone[1] == drawing_move[1]:
                return self.capturing_move(board, (chosen_stone[0], chosen_stone[1], r, c))

    def first_move(self, board):
        """
        if there is no capturing moves it draws any possible move and make it.
        else if computer's level is easy it draws capturing move
        else it takes best capturing move
        makes capturing move
        Parameters
        ----------
        board : Board

        Returns
        -------
        move : (r, c, r1, r2)
        None
            if it was paika move

        """
        pygame.time.delay(1000)
        stone = self.stone()
        opponent_stone = self.opponent_stone()
        if len(board.capturing_moves(stone, opponent_stone)) == 0:
            drawing_move = choice(board.possible_moves(stone))
            self.paika_move(board, drawing_move)
        else:
            while True:
                if self.level() == 'Easy':
                    drawing_move = choice(
                        board.capturing_moves(stone, opponent_stone))
                else:
                    drawing_move = self.best_drawing(board)
                return self.capturing_move(board, drawing_move)

    def best_drawing(self, board):
        """
        from capturing moves it returns move that lead to next move
        if it is impossible it returns move that captures the most stones

        Parameters
        ----------
        board : Board

        Returns
        -------
        move
        """
        stone = self.stone()
        opponent_stone = self.opponent_stone()
        capturing_moves = board.capturing_moves(stone, opponent_stone)
        next_moves = []
        best_capture = []
        for move in capturing_moves:
            best_capture.append(
                len(board.captured_stones(opponent_stone, move)[0]))
            best_capture.append(
                len(board.captured_stones(opponent_stone, move)[1]))
            for empty in board.empty_places(move[2], move[3]):
                empty_r = empty[0]
                empty_c = empty[1]
                future_move = (move[2], move[3], empty_r, empty_c)
                if len(board.captured_stones(opponent_stone, future_move)[0]) != 0 or\
                        len(board.captured_stones(opponent_stone, future_move)[1]) != 0:
                    next_moves.append(move)
        if len(next_moves) > 0:
            return choice(next_moves)
        best_value = max(best_capture)
        indices = [i for i, x in enumerate(best_capture) if x == best_value]
        index = choice(indices)
        return capturing_moves[index//2]

    def best_next_drawing(self, board, r, c):
        """
        from capturing moves it returns move that lead to next move
        if it is impossible it returns move that captures the most stones

        Parameters
        ----------
        board : Board
        r : int,
        c : int,
            position of last moven stone

        Returns
        -------
        move
        """
        stone = self.stone()
        opponent_stone = self.opponent_stone()
        next_moves = []
        best_capture = []
        capturing_moves_for_stone = []
        for move in board.capturing_moves(stone, opponent_stone):
            if move[0] == r and move[1] == c:
                best_capture.append(
                    len(board.captured_stones(opponent_stone, move)[0]))
                best_capture.append(
                    len(board.captured_stones(opponent_stone, move)[1]))
                for empty in board.empty_places(move[2], move[3]):
                    empty_r = empty[0]
                    empty_c = empty[1]
                    future_move = (move[2], move[3], empty_r, empty_c)
                    if len(board.captured_stones(opponent_stone, future_move)[0]) != 0 or\
                            len(board.captured_stones(opponent_stone, future_move)[1]) != 0:
                        next_moves.append(move)
                capturing_moves_for_stone.append(move)
        if len(next_moves) > 0:
            return choice(next_moves)
        best_value = max(best_capture)
        indices = [i for i, x in enumerate(best_capture) if x == best_value]
        index = choice(indices)
        return capturing_moves_for_stone[index//2]
