import pygame
import sys
import threading
from pygame.locals import *
from Board import Board
from Piece import Piece
from client import Network

def main(screen, player_id):
    clock = pygame.time.Clock()
    board = Board(n, player_id, screen, 50)
    board.initializePieces()
    pygame.display.flip()
    
    running = True
    while running:
        screen.fill((255, 255, 255))
        board.drawBoard()
        board.drawPieces()
        board.drawHints()
        pygame.display.update()
        
        for events in pygame.event.get():
            if events.type == QUIT:
                running = False
            elif events.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                board.getClicked(pos)
            elif events.type == pygame.KEYDOWN:
                if events.key == pygame.K_ESCAPE:
                    board.deselect()
                elif events.key == pygame.K_p:
                    board.setFromTo((0, 0), (0, 1))
                elif events.key == pygame.K_o:
                    board.setFromTo((0, 1), (0, 0))
        
        clock.tick(60)  # Limit the frame rate to 60 FPS

def wait_for_player(network_client):
    global playerType, ready
    try:
        playerType = int(network_client.receiveID())
        print("Player type ID is", playerType)
        ready = True
    except Exception as e:
        print("Error waiting for player:", e)

def update_board_data(network_client, board):
    while True:
        try:
            data = network_client.receive()
            board.loadBoardData(data)
        except Exception as e:
            print("Error receiving data from server:", e)
            break

pygame.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Chinese Chess Game")

font = pygame.font.SysFont("hiraginosansgbttc", 30)
text_wait = font.render("Wait for other to join", True, (255, 0, 0))
text_click = font.render("Click to join", True, (255, 0, 0))
text_pos = text_wait.get_rect(center=(screen.get_rect().centerx, 100))

clicked = False
ready = False
playerType = -1

while True:
    screen.fill((255, 255, 255))
    if ready:
        n = Network()  # Assuming 'n' should be the network client instance
        threading.Thread(target=update_board_data, args=(n, Board), daemon=True).start()
        main(screen, playerType)
        break
    elif clicked:
        screen.blit(text_wait, text_pos)
    else:
        screen.blit(text_click, text_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN and not clicked:
            n = Network()
            threading.Thread(target=wait_for_player, args=(n,), daemon=True).start()
            clicked = True

    pygame.display.flip()
