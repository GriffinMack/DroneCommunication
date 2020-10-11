# Import library
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
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

    def addImagesToScreen():
        # Import the drone images
        leftStick = pygame.image.load(
            "flightControlApplication/images/leftStick.png"
        ).convert()
        leftStick = pygame.transform.scale(leftStick, (600, 650))
        rightStick = pygame.image.load(
            "flightControlApplication/images/rightStick.png"
        ).convert()
        rightStick = pygame.transform.scale(rightStick, (600, 650))

        # # Define coordinates for the drone images
        leftStick_x = 0
        leftStick_y = 25
        rightStick_x = 680
        rightStick_y = 25

        # # Reposition the drone images
        leftStick_rect = leftStick.get_rect()
        leftStick_rect = leftStick_rect.move((leftStick_x, leftStick_y))
        rightStick_rect = rightStick.get_rect()
        rightStick_rect = rightStick_rect.move((rightStick_x, rightStick_y))

        # # Paint the drone images to the screen
        screen.blit(leftStick, leftStick_rect)
        screen.blit(rightStick, rightStick_rect)

        pygame.display.flip()  # paint screen one time

    # Initialize the game
    pygame.init()

    myfont = pygame.font.SysFont("Comic Sans MS", 30)

    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))

    # Give the application a name
    pygame.display.set_caption("Manual Control")

    # Paint the screen
    addImagesToScreen()

    while True:
        screen.fill((255, 255, 255))
        # loop through the events
        for event in pygame.event.get():
            # check if a key has been pressed
            detectKeyPress()
        # send a message to the drone if a key was pressed
        sendCorrectXbeeMessage()
        time.sleep(0.05)
