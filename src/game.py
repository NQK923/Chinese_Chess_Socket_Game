import os
import pygame
import sys
from pygame.locals import *
from Board import Board
from client import Network
import threading

stop_threads = False
playerType = -1
ready_event = threading.Event()

def main(screen, ID):
    global stop_threads
    font = pygame.font.SysFont("arial", 24)
    pygame.display.flip()
    board = Board(n, ID, screen, 50)
    board.initializePieces()
    pygame.display.flip()
    thread2 = threading.Thread(target=update, args=(n, board))
    thread2.start()

    game_over = False

    while True:
        screen.fill((255, 255, 255))
        board.drawBoard()
        board.drawPieces()
        board.drawHints()
        if game_over:
            winner = "Black" if board.currentPlayer == 1 else "Red"
            textWin = font.render(f"{winner} wins by checkmate!", True, (128, 0, 0))
            textRect = textWin.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2-20))
            screen.blit(textWin, textRect)
            replayText = font.render("Press R to replay", True, (128, 0, 0))
            replayRect = replayText.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 20))
            screen.blit(replayText, replayRect)

        pygame.display.update()

        for events in pygame.event.get():
            if events.type == QUIT:
                print("quit")
                stop_threads = True
                pygame.quit()
                sys.exit(0)
            if board.isCheckmate():
                game_over = True
            if not game_over:
                if events.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    board.getClicked(pos)
                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_ESCAPE:
                        board.deselect()
            else:
                if events.type == pygame.KEYDOWN and events.key == pygame.K_r:
                    return

def update(client, boardChess):
    global stop_threads
    while not stop_threads:
        print("Receiving the data from server")
        data = client.receive()
        if data:
            boardChess.loadBoardData(data)

pygame.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Chinese Chess Game")
run = True
menu = True
clicked = False
font = pygame.font.SysFont("hiraginosansgbttc", 30)
textWait = font.render("Wait for other to join", True, (255, 0, 0))
textclick = font.render("Click to join", True, (255, 0, 0))

textPos = textWait.get_rect()
textPos.center = (screen.get_rect().centerx, 100)

script_dir = os.path.dirname(os.path.realpath(__file__))
background_path = os.path.join(script_dir, "imgs", "background.png")

background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (500, 600))

def wait(client):
    global playerType, ready_event
    playerType = int(client.receiveID())
    print("playerType ID is ", playerType)
    ready_event.set()

def draw_text_with_border(screen, text, font, position, text_color, border_color):
    text_surface = font.render(text, True, text_color)
    border_surface = font.render(text, True, border_color)
    border_positions = [(position[0] - 1, position[1]), (position[0] + 1, position[1]),
                        (position[0], position[1] - 1), (position[0], position[1] + 1)]
    for bp in border_positions:
        screen.blit(border_surface, bp)
    screen.blit(text_surface, position)

def draw_button(screen, text, position, size=(240, 70)):
    font = pygame.font.SysFont("arial", 40)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=position)
    draw_text_with_border(screen, text, font, text_rect.topleft, (255, 255, 255), (0, 0, 0))
    return text_rect

start_button_rect = None
quit_button_rect = None

while run:
    screen.blit(background, (0, 0))
    if menu:
        title_font = pygame.font.SysFont("arial", 54)
        draw_text_with_border(screen, "Chinese Chess", title_font, (screen.get_width() // 2 - 145, 100), (255, 255, 255), (0, 0, 0))
        start_button_rect = draw_button(screen, "Start", (screen.get_width() // 2, 230))
        quit_button_rect = draw_button(screen, "Quit", (screen.get_width() // 2, 330))
    elif ready_event.is_set():
        main(screen, playerType)
        menu = True
        ready_event.clear()
        clicked = False
    elif clicked:
        screen.blit(textWait, textPos)
    else:
        screen.blit(textclick, textPos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            stop_threads = True
            pygame.quit()
            sys.exit(0)
        if event.type == MOUSEBUTTONDOWN:
            if menu:
                if start_button_rect.collidepoint(event.pos):
                    n = Network()
                    thread = threading.Thread(target=wait, args=(n,))
                    thread.start()
                    clicked = True
                    menu = False
                elif quit_button_rect.collidepoint(event.pos):
                    run = False
                    stop_threads = True
                    pygame.quit()
                    sys.exit(0)
            elif not clicked:
                n = Network()
                thread = threading.Thread(target=wait, args=(n,))
                thread.start()
                clicked = True

    pygame.display.flip()

stop_threads = True
pygame.quit()
sys.exit()
