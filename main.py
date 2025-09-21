'''
Module: main.py
Description: The main entry point for the Minesweeper game. It initializes the game, manages
    the game states (main menu and gameplay), and handles transitions between these states.
    The GameStateManager is used to track the current state of the game, allowing for smooth
    transitions between the main menu and the Minesweeper game itself. The main loop waits
    for events and updates the display accordingly.
Inputs: None
Outputs: None
External Sources: Pygame library
Authors: Wesley McDougal, Abdulaziz Ali

'''

import pygame
import sys
from gamestate_manager import GameStateManager
from main_menu import MainMenu
from Minesweeper import MineSweeper

WIDTH, HEIGHT = 400, 300

# Start point of the game
class Game:
    def __init__(self):
        '''
        Initialize a screen for the gameStateManager to use 
        and set all state possibilites
        '''

        pygame.init()

        # Set screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # Initialize gamestate manager to start at main_menu
        self.gameStateManager = GameStateManager("main_menu")

        # Initialize main menu
        self.mainMenu = MainMenu(self.gameStateManager)

        # Store all possible states
        self.states = {"main_menu": self.mainMenu}

        # Start with menu’s dimensions
        self.screen = pygame.display.set_mode(
            (self.mainMenu.WIDTH, self.mainMenu.HEIGHT)
        )

    def run(self):
        '''
        Gets the current state for GameStateManager and
        switches state of the current game to the state
        that is recieved (ie. switching from main menu to the game)
        '''

        while True:

            # If users quits 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Run the current state
            state = self.gameStateManager.getState()

            # Resize window if needed
            if state == "main_menu":
                current = self.states["main_menu"]
                if self.screen.get_size() != (current.WIDTH, current.HEIGHT):
                    self.screen = pygame.display.set_mode(
                        (current.WIDTH, current.HEIGHT)
                    )
                current.run()

            elif state == "mine_sweeper":
                MineSweeper(self.gameStateManager).run()  # Create new instance each time
            else:
                self.states[self.gameStateManager.getState()].run()

            pygame.display.update()
            self.clock.tick(30) 

if __name__ == "__main__":
    game = Game()
    game.run()
