import pygame
import sys
from players import HumanPlayer, Computer
from board import Board
import board as brd
from config import (
    SQUARESIZE,
    width,
    height,
    BROWN,
    BLACK,
    YELLOW,
)


class Game():
    """
    A class to represent game.

    ...

    Attributes
    ----------
    myfont, myfont2, myfont_title : font
    stone, opponent_stone : 1 or 2
    player1 player2 : Player
    board : Board
    stone_turn : 1 or 2

    Methods
    -------
    __init__(stone):
        creates game
    print_question(question, options):
        draws on screen questions and buttons
    ask_for_size_of_board():
        returns size o chosen board
    print_text(text):
        draws on screen big text
    ask_for_opponent(stone):
        creates opponent
    ask_for_stone():
        returns players' stones
    print_result(player1, winning_stone):
        draws on screen result of game
    show_turn(player, f_player_stone):
        shows which turn is now
    play():
        make turns till there is no winner
    """

    def __init__(self):
        """
        creates player, board and constructs all the necessary attributes for the game object.

        Parameters
        ----------
        question : str

        options : list of strings:

        Returns
        -------
        None
        """
        self.myfont = pygame.font.SysFont('Comic Sans MS', 60)
        self.myfont2 = pygame.font.SysFont('Comic Sans MS', 30)
        self.myfont_title = pygame.font.SysFont('Comic Sans MS', 120)
        self.print_text("FANORONA")
        size_of_board = self.ask_for_size_of_board()
        self.stone, self.opponent_stone = self.ask_for_stone()
        self.player2 = self.ask_for_opponent(self.opponent_stone)
        self.player1 = HumanPlayer(self.stone)
        self.board = Board(size_of_board[0], size_of_board[1])
        self.board.draw_board()
        self.stone_turn = 1

    def print_question(self, question, options):
        """
        draws on screen questions and buttons

        Parameters
        ----------
        question : str

        options : list of strings:

        Returns
        -------
        None
        """
        question = self.myfont.render(question, True, YELLOW)
        question_rect = question.get_rect(center=(width/2, height/5))
        screen.blit(question, question_rect)
        for enum, option in enumerate(options):
            x = enum*SQUARESIZE
            button = self.myfont.render(option, True, YELLOW, BROWN)
            button_rect = button.get_rect(center=(width/2, height/3+x))
            screen.blit(button, button_rect)
        pygame.display.update()

    def ask_for_size_of_board(self):
        """
        asks about size of board and takes answer

        Returns
        -------
        size :
        (3, 3) if first option
        (5, 5) if second option
        (5, 9) if last option
        """
        options = ['3 x 3', '5 x 5', '5 x 9']
        size_of_button = pygame.font.Font.size(self.myfont, max(options))
        self.print_question('CHOOSE SIZE OF THE BOARD', options)
        size = None
        while not size:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    posy = event.pos[1]
                    if posx >= (width - size_of_button[0])/2 and posx <= (width + size_of_button[0])/2 \
                            and posy >= height/3 - size_of_button[1]/2 and posy <= height/3 + size_of_button[1]/2:
                        size = (3, 3)
                    elif posx >= (width - size_of_button[0])/2 and posx <= (width + size_of_button[0])/2 \
                            and posy >= height/3 - size_of_button[1]/2 + SQUARESIZE \
                            and posy <= height/3 + size_of_button[1]/2 + SQUARESIZE:
                        size = (5, 5)
                    elif posx >= (width - size_of_button[0])/2 and posx <= (width + size_of_button[0])/2 \
                            and posy >= height/3 - size_of_button[1]/2 + 2*SQUARESIZE \
                            and posy <= height/3 + size_of_button[1]/2 + 2*SQUARESIZE:
                        size = (5, 9)
        screen.fill(BLACK)
        pygame.display.update()
        return size

    def print_text(self, text):
        """
        draws on screen big text

        Parameters
        ----------
        text : str

        Returns
        -------
        None
        """
        question = self.myfont_title.render(text, True, BROWN)
        question_rect = question.get_rect(center=(width/2, height/2))
        screen.blit(question, question_rect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    screen.fill(BLACK)
                    pygame.display.update()
                    return
                if event.type == pygame.QUIT:
                    sys.exit()

    def ask_for_opponent(self, stone):
        """
        asks about kind of opponent

        Parameters
        ----------
        stone : 1 or 2
            opponent_stone

        Returns
        -------
        opponent :
        Player if first option
        Computer(Easy) if second option
        Computer(Hard) if last option
        """
        options = ['Another Player', 'Computer - Easy', 'Computer - Hard']
        size_of_button = pygame.font.Font.size(self.myfont, max(options))
        self.print_question('CHOOSE YOUR OPPONENT', options)
        opponent = None
        pygame.display.update()
        while not opponent:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    posy = event.pos[1]
                    if posx >= (width - size_of_button[0])/2 and posx <= (width + size_of_button[0])/2 \
                            and posy >= height/3 - size_of_button[1]/2 and posy <= height/3 + size_of_button[1]/2:
                        opponent = HumanPlayer(stone)
                    elif posx >= (width - size_of_button[0])/2 and posx <= (width + size_of_button[0])/2 \
                            and posy >= height/3 - size_of_button[1]/2 + SQUARESIZE\
                            and posy <= height/3 + size_of_button[1]/2 + SQUARESIZE:
                        opponent = Computer(stone, 'Easy')
                    elif posx >= (width - size_of_button[0])/2 and posx <= (width + size_of_button[0])/2 \
                            and posy >= height/3 - size_of_button[1]/2 + 2*SQUARESIZE\
                            and posy <= height/3 + size_of_button[1]/2 + 2*SQUARESIZE:
                        opponent = Computer(stone, 'Hard')
        screen.fill(BLACK)
        pygame.display.update()
        return opponent

    def ask_for_stone(self):
        """
        asks about stone

        Returns
        -------
        stone, opponent_stone :
        1, 2 if first option
        2, 1 if second option
        """
        options = ['WHITE', 'BLACK']
        size_of_button = pygame.font.Font.size(self.myfont, max(options))
        self.print_question('CHOOSE YOUR STONE', options)
        stone = None
        while not stone:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    posy = event.pos[1]
                    if posx >= (width - size_of_button[0])/2 and posx <= (width + size_of_button[0])/2 \
                            and posy >= height/3 - size_of_button[1]/2 and posy <= height/3 + size_of_button[1]/2:
                        stone = 1
                        opponent_stone = 2

                    elif posx >= (width - size_of_button[0])/2 and posx <= (width + size_of_button[0])/2 \
                            and posy >= height/3 - size_of_button[1]/2 + SQUARESIZE \
                            and posy <= height/3 + size_of_button[1]/2 + SQUARESIZE:
                        stone = 2
                        opponent_stone = 1
        screen.fill(BLACK)
        pygame.display.update()
        return stone, opponent_stone

    def print_result(self, player1, winning_stone):
        """
        draws on screen result of game
        'YOU WON!!!' OR 'YOU LOSE'

        Parameters
        ----------
        player1 : Player

        winning_stone : 1 or 2

        Returns
        -------
        None
        """
        screen.fill(BLACK)
        pygame.display.update()
        if winning_stone == player1.stone():
            self.print_text("YOU WON!!!")
        else:
            self.print_text("YOU LOSE...")
        return

    def show_turn(self, player, f_player_stone):
        """
        draws on screen which turn is now and what color of stone is playing now

        Parameters
        ----------
        player : Player
            current player

        f_player_stone : 1 or 2
            first player's stone

        Returns
        -------
        None
        """
        stone = 'WHITE' if player.stone() == 1 else 'BLACK'
        text = 'Your Turn' if player.stone() == f_player_stone else "Opponent's turn"
        text += f', stone : {stone}'
        turn = self.myfont2.render(text, True, YELLOW)
        rect = turn.get_rect(center=(width/2, height - SQUARESIZE/4))
        pygame.draw.rect(screen, BLACK, (0, height -
                         SQUARESIZE/2, width, SQUARESIZE))
        screen.blit(turn, rect)
        pygame.display.update()

    def play(self):
        """
        while there is no winner makes turns, print result of game

        Returns
        -------
        None
        """
        while not self.board.is_winner():
            current_player = self.player1 if self.player1.stone(
            ) == self.stone_turn else self.player2
            self.show_turn(current_player, self.stone)
            current_player.make_turn(self.board)
            self.stone_turn = 1 if self.stone_turn == 2 else 2
        pygame.time.delay(1000)
        self.print_result(self.player1, self.board.is_winner())


def main():
    """
    makes window and starts game

    Returns
    -------
    None
    """
    global screen
    pygame.init()
    size = (width, height)
    screen = pygame.display.set_mode(size)
    brd.screen = screen
    game = Game()
    game.play()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
            sys.exit()


if __name__ == "__main__":
    main()
