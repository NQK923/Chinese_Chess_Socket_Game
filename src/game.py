import os
import pygame
import sys
from pygame.locals import *
from Board import Board
from client import Network
import threading

stop_threads = False

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
            if not game_over:
                if events.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    board.getClicked(pos)
                    if board.isCheckmate():
                        game_over = True
                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_ESCAPE:
                        board.deselect()
                    if events.key == pygame.K_p:
                        board.setFromTo((0, 0), (0, 1))
                    if events.key == pygame.K_o:
                        board.setFromTo((0, 1), (0, 0))
            else:
                if events.type == pygame.KEYDOWN and events.key == pygame.K_r:
                    return

def update(client, boardChess):
    global stop_threads
    while not stop_threads:
        print("Receiving the data from server")
        data = client.receive()
        if data:
            print(data)
            boardChess.loadBoardData(data)

RED = 0
BLACK = 1
playerType = -1

pygame.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Chinese Chess Game")
run = True
ready = False
clicked = False
font = pygame.font.SysFont("hiraginosansgbttc", 30)
textWait = font.render("Wait for other to join", True, (255, 0, 0))
textclick = font.render("Click to join", True, (255, 0, 0))

textPos = textWait.get_rect()
textPos.center = (screen.get_rect().centerx, 100)

script_dir = os.path.dirname(os.path.realpath(__file__))
background_path = os.path.join(script_dir,"imgs", "background.png")

background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (500, 600))

def wait(client):
    global playerType, ready
    playerType = int(client.receiveID())
    print("playerType ID is ", playerType)
    ready = True

def draw_button(screen, text, position, size=(240, 70)):
    font = pygame.font.SysFont("arial", 36)
    button_surf = pygame.Surface(size)
    button_rect = button_surf.get_rect(center=position)
    button_surf.fill((227, 211, 51))
    pygame.draw.rect(button_surf, (0, 0, 0), button_rect, 2,border_radius=15)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(size[0] // 2, size[1] // 2))
    button_surf.blit(text_surf, text_rect)
    screen.blit(button_surf, button_rect.topleft)
    return button_rect

i = 1
menu = True
start_button_rect = None
quit_button_rect = None

while run:
    screen.blit(background, (0, 0))
    if menu:
        start_button_rect = draw_button(screen, "Start", (screen.get_width() // 2, 200))
        quit_button_rect = draw_button(screen, "Quit", (screen.get_width() // 2, 300))
    elif ready:
        main(screen, playerType)
        menu = True
        ready = False
        clicked = False
    elif clicked:
        i += 5
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
