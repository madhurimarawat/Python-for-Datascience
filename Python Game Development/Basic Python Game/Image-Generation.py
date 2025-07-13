# Example of Simple Window Generation and Image Display using Pygame

# Importing all functions from pygame
from pygame import *

# Importing pygame library
import pygame

# Class for Game
class Game:

    # Constructor for class
    def __init__(self):
        self._running = True

    # Initialization Function
    def on_init(self):

        # Initialization
        pygame.init()

        # Set the Window- its height and width in pixels
        # HWSURFACE is for hardware acceleration
        self._display_surf = pygame.display.set_mode((640, 480), pygame.HWSURFACE)

        # Window title
        pygame.display.set_caption("Pygame Image Loading")

        # Setting Cat Image
        self._cat_image = pygame.image.load("Cat Image.jpg").convert()

    # Function for rendering screen
    def on_render(self):

        # Clears the Screen
        self._display_surf.fill((0, 0, 0))

        # Setting Dimensions of image(height and width)
        self._display_surf.blit(self. _cat_image, (40,50))

        # Updates the screen
        pygame.display.flip()

    # Function to end game
    # Quit function is used
    def on_cleanup(self):
        pygame.quit()

    # Main loop
    def on_execute(self):

        # Not initialized
        if self.on_init() == False:
            self._running = False

        while self._running:

            # Calling for events or user input
            for event in pygame.event.get():

                # Checking condition if we need to end the game
                if event.type == pygame.QUIT:
                    self._running = False

            # Update Screen
            self.on_render()

        # To Clean Screen
        self.on_cleanup()

# Main Function
if __name__ == "__main__":

    # To initialize object
    game = Game()

    # Calling execute function
    game.on_execute()