# 1 - Import library
import pygame
import time
from pygame.locals import *


def controlDronesManually(baseStationXbee, droneToControl=None):
    # 2 - Initialize the game
    pygame.init()
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    width, height = 64 * 10, 64 * 8
    screen = pygame.display.set_mode((width, height))
    #      [UP, LEFT, DOWN, RIGHT]
    arrowKeys = [False, False, False, False]
    wasdKeys = [False, False, False, False]
    # 4 - keep looping through
    while True:
        screen.fill((255, 255, 255))
        textsurface = myfont.render('NOTHING', True, (200, 0, 0))
        # 8 - loop through the events
        for event in pygame.event.get():
            # check if the event is the X button
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
                if event.key == pygame.K_UP:
                    arrowKeys[0] = False
                elif event.key == pygame.K_LEFT:
                    arrowKeys[1] = False
                elif event.key == pygame.K_DOWN:
                    arrowKeys[2] = False
                elif event.key == pygame.K_RIGHT:
                    arrowKeys[3] = False
                elif event.key == K_w:
                    wasdKeys[0] = False
                elif event.key == K_a:
                    wasdKeys[1] = False
                elif event.key == K_s:
                    wasdKeys[2] = False
                elif event.key == K_d:
                    wasdKeys[3] = False
        # If the up button is pressed
        if arrowKeys[0]:
            textsurface = myfont.render('forward', False, (200, 000, 000))
            baseStationXbee.sendMessage("forward", droneToControl)

        # If the down key is pressed
        elif arrowKeys[2]:
            textsurface = myfont.render('backward', False, (200, 000, 000))
            baseStationXbee.sendMessage("backward", droneToControl)

        # If the left key is pressed
        if arrowKeys[1]:
            textsurface = myfont.render('left', False, (200, 000, 000))
            baseStationXbee.sendMessage("left", droneToControl)

        # If the right key is pressed
        elif arrowKeys[3]:
            textsurface = myfont.render('right', False, (200, 000, 000))
            baseStationXbee.sendMessage("right", droneToControl)

        if wasdKeys[0]:
            textsurface = myfont.render('up', False,(200, 000, 000))
            baseStationXbee.sendMessage("up", droneToControl)

        elif wasdKeys[2]:
            textsurface = myfont.render('down', False, (200, 000, 000))
            baseStationXbee.sendMessage("down", droneToControl)

        if wasdKeys[1]:
            textsurface = myfont.render('left rotate', False, (200, 000, 000))
            baseStationXbee.sendMessage("left rotate", droneToControl)

        elif wasdKeys[3]:
            textsurface = myfont.render('right rotate', False, (200, 000, 000))
            baseStationXbee.sendMessage("right rotate", droneToControl)
        
        screen.blit(textsurface,(200,200))
        time.sleep(0.01)