import pygame
import sys
from players import Player, HumanPlayer, Computer
from board import (
    Board,
    width,
    height,
    screen,
    SQUARESIZE,
    BLACK,
    BROWN,
    YELLOW
)
myfont = pygame.font.SysFont('Comic Sans MS', 60)
myfont_title = pygame.font.SysFont('Comic Sans MS', 120)


def print_question(question, options):
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
    question = myfont.render(question, True, YELLOW)
    question_rect = question.get_rect(center=(width/2, height/5))
    screen.blit(question, question_rect)
    for enum, option in enumerate(options):
        x = enum*SQUARESIZE
        button = myfont.render(option, True, YELLOW, BROWN)
        button_rect = button.get_rect(center=(width/2, height/3+x))
        screen.blit(button, button_rect)
    pygame.display.update()


def ask_for_size_of_board():
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
    size_of_button = pygame.font.Font.size(myfont, max(options))
    print_question('CHOOSE SIZE OF THE BOARD', options)
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


def print_text(text):
    """
    draws on screen big text

    Parameters
    ----------
    text : str

    Returns
    -------
    None
    """
    question = myfont_title.render(text, True, BROWN)
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


def ask_for_opponent(stone):
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
    size_of_button = pygame.font.Font.size(myfont, max(options))
    print_question('CHOOSE YOUR OPPONENT', options)
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


def ask_for_stone():
    """
    asks about stone

    Returns
    -------
    stone, opponent_stone :
    1, 2 if first option
    2, 1 if second option
    """
    options = ['WHITE', 'BLACK']
    size_of_button = pygame.font.Font.size(myfont, max(options))
    print_question('CHOOSE YOUR STONE', options)
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


def print_result(player1, winning_stone):
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
        print_text("YOU WON!!!")
    else:
        print_text("YOU LOSE...")
    return


def main():
    """
    starts game, prints questions and plays turns till there is no winner
    prints result of game

    Returns
    -------
    None
    """
    print_text("FANORONA")
    size_of_board = ask_for_size_of_board()
    stone, opponent_stone = ask_for_stone()
    player2 = ask_for_opponent(opponent_stone)
    player1 = HumanPlayer(stone)
    board = Board(size_of_board[0], size_of_board[1])
    board.draw_board()
    stone_turn = 1
    while not board.is_winner():
        current_player = player1 if player1.stone() == stone_turn else player2
        current_player.make_turn(board)
        stone_turn = 1 if stone_turn == 2 else 2
    pygame.time.delay(1000)
    print_result(player1, board.is_winner())
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                sys.exit()


if __name__ == "__main__":
    main()
