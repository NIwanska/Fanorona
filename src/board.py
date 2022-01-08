import numpy as np
import pygame
from config import (
    SQUARESIZE,
    width,
    height,
    BROWN,
    BLACK,
    RED,
    WHITE,
    DARK_BROWN,
    YELLOW,
)


screen = None


class Board:
    """
    A class to represent a board.
    ...

    Attributes
    ----------
    rows : int
        number of rows of board
    columns : int
        number of columns of board
    board_position_x : int
        coordinate x of board at screen
    board_position_y : int
        coordinate y of board at screen
    matrix : list
        a list of lists represents places on board
    Methods
    -------
    __init__(rows, columns):
        creates a board

    is_winner():
        return winning stone if exists or None

    draw_board():
        draws board with stones on screen

    chosen_position(posx, posy):
        for coordinates of mouse click returns coordinates of a stone or None

    light_up_stones_to_capture(captured_stones):
        changes stone's color from captured_stones list to red

    light_up_chosen_stone(stones):
        draws yellow rims of stones from list stones

    diagonal_moves():
        returns places from which diagonal moves are possible

    possible_moves(stone):
        returns a list of (capturing and noncapturing) moves(places from and where the stone will move)
        for every player's stone

    capturing_moves(stone, opponent_stone):
        returns a list of capturing moves for every player's stone

    captured_stones(opponent_stone, move):
        returns two list with places of approach captured stones and withdrawal captured stones

    empty_places(r, c):
        returns list of empty places around place from argument

    light_up_possible_stones(stone, opponent_stone):
        draws yellow rims of stones that can move
    """

    def __init__(self, rows, columns):
        """
        Constructs all the necessary attributes for the board object.

        fills board's matrix with starting stones (1 - white, 2 - black)

        Parameters
        ----------
        rows : int
            number of rows, it has to be odd number and smaller than 10
        columns : int
            number of columns, it has to be odd number and smaller than 10
        """
        self.rows = rows
        self.columns = columns
        self.board_position_x = (width - self.columns*SQUARESIZE)//2
        self.board_position_y = (height - self.rows*SQUARESIZE)//2
        board = np.zeros((rows, columns), dtype=np.int8)
        for r in range(rows):
            if r < rows/2 - 1:
                for c in range(columns):
                    board[r][c] = 2
            elif r > rows/2:
                for c in range(columns):
                    board[r][c] = 1
            else:
                for c in range(columns):
                    if (c < columns/2 - 1 and c % 2 == 0) or (c > columns/2 and c % 2 == 1):
                        board[r][c] = 2
                    else:
                        board[r][c] = 1
                    if c == columns//2:
                        board[r][c] = 0
        self.matrix = board

    def is_winner(self):
        """
        returns winner's stone

        Returns
        -------
        1 - if there are no black stone on board
        2 - if there are no white stone
        None - if there are black and white stones on board
        """

        white = 0
        black = 0
        for verse in self.matrix:
            if 2 in verse:
                black += 1
            if 1 in verse:
                white += 1
        if white == 0:
            return 2
        if black == 0:
            return 1
        return None

    def draw_board(self):
        """
        draws current state of board

        Returns
        -------
        None
        """
        rows = self.rows
        columns = self.columns
        pygame.draw.rect(screen, BROWN, (self.board_position_x,
                                         self.board_position_y, columns*SQUARESIZE, rows*SQUARESIZE))
        for r in range(rows):
            for c in range(columns):
                circle_pos_x = self.board_position_x + (c+0.5)*SQUARESIZE
                circle_pos_y = self.board_position_y + (r+0.5)*SQUARESIZE
                if c % 2 == 0 and r % 2 == 0 and r < rows-1:
                    if c > 0:
                        pygame.draw.line(screen, DARK_BROWN, (circle_pos_x, circle_pos_y), (
                            circle_pos_x - 2*SQUARESIZE, circle_pos_y+2*SQUARESIZE), 5)
                    if c < columns-1:
                        pygame.draw.line(screen, DARK_BROWN, (circle_pos_x, circle_pos_y), (
                            circle_pos_x + 2*SQUARESIZE, circle_pos_y+2*SQUARESIZE), 5)
                if c == 0:
                    pygame.draw.line(screen, DARK_BROWN, (circle_pos_x, circle_pos_y),
                                     (circle_pos_x + (columns-1)*SQUARESIZE, circle_pos_y), 5)
                if r == 0:
                    pygame.draw.line(screen, DARK_BROWN, (circle_pos_x, circle_pos_y),
                                     (circle_pos_x, circle_pos_y + (rows-1)*SQUARESIZE), 5)
                if self.matrix[r][c] == 2:
                    pygame.draw.circle(
                        screen, BLACK, (circle_pos_x, circle_pos_y), SQUARESIZE/3)
                elif self.matrix[r][c] == 1:
                    pygame.draw.circle(
                        screen, WHITE, (circle_pos_x, circle_pos_y), SQUARESIZE/3)
        pygame.display.update()

    def chosen_position(self, posx, posy):
        """
        for coordinates of mouse click returns coordinates of a stone or None

        Parameters
        ----------
        posx : int
            coordinate x of moue click
        posy : int
            coordinate y of moue click

        Returns
        -------
        None - if not clicked on stone
        r, c : int
            row and column of clicked stone
        """
        for r in range(self.rows):
            for c in range(self.columns):
                circle_pos_x = self.board_position_x + (c+0.5)*SQUARESIZE
                circle_pos_y = self.board_position_y + (r+0.5)*SQUARESIZE
                if posx > circle_pos_x - SQUARESIZE/3 and posx < circle_pos_x + SQUARESIZE/3 \
                        and posy > circle_pos_y - SQUARESIZE/3 and posy < circle_pos_y + SQUARESIZE/3:
                    return r, c

    def light_up_stones_to_capture(self, captured_stones):
        """
        changes stone's color from captured_stones list to red

        Parameters
        ----------
        captured_stones - list with positions of stones that can be captured

        Returns
        -------
        None
        """
        for captured_stone in captured_stones:
            r = captured_stone[0]
            c = captured_stone[1]
            circle_pos_x = self.board_position_x + (c+0.5)*SQUARESIZE
            circle_pos_y = self.board_position_y + (r+0.5)*SQUARESIZE
            pygame.draw.circle(
                screen, RED, (circle_pos_x, circle_pos_y), SQUARESIZE/3)
            pygame.display.update()

    def light_up_chosen_stone(self, stones):
        """
        draws yellow rims of stones from list stones

        Parameters
        ----------
        stones - list with positions of stones

        Returns
        -------
        None
        """
        self.draw_board()
        for stone in stones:
            r = stone[0]
            c = stone[1]
            circle_pos_x = self.board_position_x + (c+0.5)*SQUARESIZE
            circle_pos_y = self.board_position_y + (r+0.5)*SQUARESIZE
            pygame.draw.circle(
                screen, YELLOW, (circle_pos_x, circle_pos_y), SQUARESIZE*5/13, SQUARESIZE//12)
        pygame.display.update()

    def diagonal_moves(self):
        """
        returns places from which diagonal moves are possible

        Returns
        -------
        list of places
        """
        list_of_diagonal_moves = []
        for c in range(self.columns):
            for r in range(self.rows):
                if (r % 2 == 0 and c % 2 == 0) or (r % 2 == 1 and c % 2 == 1):
                    list_of_diagonal_moves.append((r, c))
        return list_of_diagonal_moves

    def possible_moves(self, stone):
        """
        returns a list of (capturing and noncapturing) moves(places
        from and where the stone will move) for every player's stone

        Parameters
        ----------
        stone : (1 or 2)
            player's stone

        Returns
        -------
        list of moves
        """
        possible_moves = []
        diagonal_moves = self.diagonal_moves()
        for r in range(self.rows):
            for c in range(self.columns):
                if self.matrix[r][c] == stone:
                    if c > 0:
                        if self.matrix[r][c-1] == 0:
                            possible_moves.append((r, c, r, c-1))
                    if c < self.columns-1:
                        if self.matrix[r][c+1] == 0:
                            possible_moves.append((r, c, r, c+1))
                    if r > 0:
                        if self.matrix[r-1][c] == 0:
                            possible_moves.append((r, c, r-1, c))
                    if r < self.rows-1:
                        if self.matrix[r+1][c] == 0:
                            possible_moves.append((r, c, r+1, c))
                    if (r, c) in diagonal_moves:
                        if r > 0 and c > 0:
                            if self.matrix[r-1][c-1] == 0:
                                possible_moves.append((r, c, r-1, c-1))
                        if r < self.rows-1 and c > 0:
                            if self.matrix[r+1][c-1] == 0:
                                possible_moves.append((r, c, r+1, c-1))
                        if r < self.rows-1 and c < self.columns-1:
                            if self.matrix[r+1][c+1] == 0:
                                possible_moves.append((r, c, r+1, c+1))
                        if r > 0 and c < self.columns-1:
                            if self.matrix[r-1][c+1] == 0:
                                possible_moves.append((r, c, r-1, c+1))
        return possible_moves

    def capturing_moves(self, stone, opponent_stone):
        """
        returns a list of capturing moves for every player's stone

        Parameters
        ----------
        stone : (1 or 2)
            player's stone
        opponent_stone : (1 or 2)
            opponent's stone

        Returns
        -------
        list of capturing moves
        """
        capturing_moves = []
        for move in self.possible_moves(stone):
            captured_stones = self.captured_stones(opponent_stone, move)
            if len(captured_stones[0]) > 0 or len(captured_stones[1]) > 0:
                capturing_moves.append(move)
        return capturing_moves

    def captured_stones(self, opponent_stone, move):
        """
        returns two list with places of approach
        captured stones and withdrawal captured stones

        Parameters
        ----------
        opponent_stone : (1 or 2)
            opponent's stone
        move : (r1, c1, r2, c2)
            tuple with place from and where stone will go

        Returns
        -------
        tuple with two lists, first with approach
        captured stones and second with withdrawal captured stones
        """
        r1, c1, r2, c2 = move
        r_direction = r1 - r2
        c_direction = c1 - c2
        approach_capture = []
        withdrawal_capture = []
        if (r1, c1) not in self.diagonal_moves():
            if r_direction != 0 and c_direction != 0:
                return ([], [])
        while r2 >= 0 and r2 <= self.rows-1 and c2 >= 0 and c2 <= self.columns-1:
            r2 -= r_direction
            c2 -= c_direction
            if r2 >= 0 and r2 <= self.rows-1 and c2 >= 0 and c2 <= self.columns-1:
                if self.matrix[r2][c2] == opponent_stone:
                    approach_capture.append((r2, c2))
                else:
                    break
        while r1 >= 0 and r1 <= self.rows-1 and c1 >= 0 and c1 <= self.columns-1:
            r1 += r_direction
            c1 += c_direction
            if r1 >= 0 and r1 <= self.rows-1 and c1 >= 0 and c1 <= self.columns-1:
                if self.matrix[r1][c1] == opponent_stone:
                    withdrawal_capture.append((r1, c1))
                else:
                    break
        return (approach_capture, withdrawal_capture)

    def empty_places(self, r, c):
        """
        returns list of empty places around place from argument

        Parameters
        ----------
        r : int
            board's row
        c : int
            board's column

        Returns
        -------
        list of empty places around place from argument
        """
        arr = []
        for x in range(r-1, r+2):
            for y in range(c-1, c+2):
                if x >= 0 and x < self.rows and y >= 0 and y < self.columns:
                    if self.matrix[x][y] == 0 and not(x == r and y == c):
                        arr.append((x, y))
        return arr

    def light_up_possible_stones(self, stone, opponent_stone):
        """
        draws yellow rims of stones that can move

        Parameters
        ----------
        stone : (1 or 2)
            player's stone
        opponent_stone : (1 or 2)
            opponent's stone

        Returns
        -------
        None
        """
        stones = []
        if len(self.capturing_moves(stone, opponent_stone)) == 0:
            for move in self.possible_moves(stone):
                stones.append((move[0], move[1]))
        else:
            for move in self.capturing_moves(stone, opponent_stone):
                stones.append((move[0], move[1]))
        self.light_up_chosen_stone(stones)
