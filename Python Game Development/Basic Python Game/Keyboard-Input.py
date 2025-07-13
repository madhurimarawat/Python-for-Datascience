# Load Modules
from pygame.locals import *
import pygame

# Define Class
class Player:
    x = 0
    y = 0


# Game Class
class Game:

    # Initializer
    def __init__(self):

        self._running = True

        # Create Player Object
        self.Player = Player()

    # Init Function/ Start Function
    def 