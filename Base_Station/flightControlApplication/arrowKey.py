# 1 - Import library
import pygame
import time
from pygame.locals import *

from devices import baseStation

#           [UP, LEFT, DOWN, RIGHT]
arrowKeys = [False, False, False, False]
#           [W, A, S, D]
wasdKeys = [False, False, False, False]


def controlDronesManually(baseStationXbee, droneToControl=None):
    def detectKeyPress():
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                arrowKeys[0] = True
            elif event.key == K_LEFT:
                arrowKeys[1] = True
            elif event.key == K_DOWN:
                arrowKeys[2] = True
            elif event.key == K_RIGHT:
                arrowKeys[3] = True
            elif event.key == K_w:
                wasdKeys[0] = True
            elif event.key == K_a:
                wasdKeys[1] = True
            elif event.key == K_s:
                wasdKeys[2] = True
            elif event.key == K_d:
                wasdKeys[3] = True

        if event.type == pygame.KEYUP:
            if event.key == K_UP:
                arrowKeys[0] = False
            elif event.key == K_LEFT:
                arrowKeys[1] = False
            elif event.key == K_DOWN:
                arrowKeys[2] = False
            elif event.key == K_RIGHT:
                arrowKeys[3] = False
            elif event.key == K_w:
                wasdKeys[0] = False
            elif event.key == K_a:
                wasdKeys[1] = False
            elif event.key == K_s:
                wasdKeys[2] = False
            elif event.key == K_d:
                wasdKeys[3] = False

    def sendCorrectXbeeMessage():
        if arrowKeys[0]:
            baseStationXbee.sendMessage("forward", droneToControl)
        # If the down key is pressed
        elif arrowKeys[2]:
            baseStationXbee.sendMessage("backward", droneToControl)
        # If the left key is pressed
        if arrowKeys[1]:
            baseStationXbee.sendMessage("left", droneToControl)
        # If the right key is pressed
        elif arrowKeys[3]:
            baseStationXbee.sendMessage("right", droneToControl)
        if wasdKeys[0]:
            baseStationXbee.sendMessage("up", droneToControl)
        elif wasdKeys[2]:
            baseStationXbee.sendMessage("down", droneToControl)
        if wasdKeys[1]:
            baseStationXbee.sendMessage("left rotate", droneToControl)
        elif wasdKeys[3]:
            baseStationXbee.sendMessage("right rotate", droneToControl)

    # 2 - Initialize the game
    pygame.init()

    myfont = pygame.font.SysFont("Comic Sans MS", 30)

    width, height = 64 * 10, 64 * 8
    screen = pygame.display.set_mode((width, height))
    #      [UP, LEFT, DOWN, RIGHT]

    # 4 - keep looping through
    while True:
        screen.fill((255, 255, 255))
        textsurface = myfont.render("NOTHING", True, (200, 0, 0))
        # 8 - loop through the events
        for event in pygame.event.get():
            # check if a key has been pressed
            detectKeyPress()
        sendCorrectXbeeMessage()

        screen.blit(textsurface, (200, 200))
        time.sleep(0.05)


if __name__ == "__main__":
    baseStationXbeeDevice = baseStation()
    controlDronesManually(baseStationXbeeDevice)