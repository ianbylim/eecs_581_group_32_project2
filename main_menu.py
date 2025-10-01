'''
Module: main_menu.py
Description: A main menu for Minesweeper using Pygame. Allows player to select the number of mines (10-20) and start the game.
Inputs: Player chosen number of mines.
Outputs: Running the actual game with the grid. The number of mines will be sent to it.
Sources:
    Used Copilot to help spacing out the buttons.
    Pygame event handling documentation used in main_menu(): https://www.pygame.org/docs/ref/event.html
Author: Atharva Patil, 
Creation Date: 9/2/2025
'''

import pygame
import sys
import config

class MainMenu:
    def __init__(self, gameStateManager):
        pygame.init()
        self.gameStateManager = gameStateManager

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (100, 100, 100)
        self.BLUE = (50, 100, 200)
        self.GREEN = (0, 150, 0)
        self.YELLOW = (200, 150, 0)
        self.RED = (200, 0, 0)

        # Screen setup
        self.WIDTH, self.HEIGHT = 400, 300

        # Fonts
        self.FONT = pygame.font.SysFont(None, 36)
        self.SMALL_FONT = pygame.font.SysFont(None, 28)
       
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Minesweeper - Main Menu")

        # Default menu state
        self.mine_count = 10

        # Buttons
        self.start_button = pygame.Rect(self.WIDTH//2 - 60, self.HEIGHT - 50, 120, 40)
        self.minus_button = pygame.Rect(self.WIDTH//2 - 70, self.HEIGHT//2 + 45, 40, 40)
        self.plus_button = pygame.Rect(self.WIDTH//2 + 30, self.HEIGHT//2 + 45, 40, 40)

        # Difficulty buttons
        self.easy_button = pygame.Rect(self.WIDTH//2 - 150, self.HEIGHT//2 - 30, 100, 40)
        self.medium_button = pygame.Rect(self.WIDTH//2 - 50, self.HEIGHT//2 - 30, 100, 40)
        self.hard_button = pygame.Rect(self.WIDTH//2 + 50, self.HEIGHT//2 - 30, 100, 40)

    # Draw the menu
    def draw_menu(self):
        self.screen.fill(self.WHITE)

        # Title
        large_font = pygame.font.SysFont("Calibri", 64, True)
        title_text = large_font.render("Minesweeper", True, self.BLACK)
        self.screen.blit(title_text, (self.WIDTH//2 - title_text.get_width()//2, 30))

        # Mine count label
        label_text = self.SMALL_FONT.render("Select Mine Count:", True, self.BLACK)
        self.screen.blit(label_text, (self.WIDTH//2 - label_text.get_width()//2, self.HEIGHT//2 + 20))

        # Mine count display
        count_text = self.FONT.render(str(self.mine_count), True, self.BLUE)
        self.screen.blit(count_text, (self.WIDTH//2 - count_text.get_width()//2, self.HEIGHT//2 + 55))

        # Minus button
        pygame.draw.rect(self.screen, self.GRAY, self.minus_button)
        minus_text = self.FONT.render("-", True, self.BLACK)
        self.screen.blit(minus_text, (self.minus_button.centerx - minus_text.get_width()//2, self.minus_button.centery - minus_text.get_height()//2))

        # Plus button
        pygame.draw.rect(self.screen, self.GRAY, self.plus_button)
        plus_text = self.FONT.render("+", True, self.BLACK)
        self.screen.blit(plus_text, (self.plus_button.centerx - plus_text.get_width()//2, self.plus_button.centery - plus_text.get_height()//2))

        # AI Difficulty Label
        AI_text = self.SMALL_FONT.render("Select AI Difficulty:", True, self.BLACK)
        self.screen.blit(AI_text, (self.WIDTH//2 - label_text.get_width()//2, self.HEIGHT//2 - 55))

        # Easy button
        pygame.draw.rect(self.screen, self.GREEN, self.easy_button)
        easy_text = self.SMALL_FONT.render("Easy", True, self.WHITE)
        self.screen.blit(easy_text, (self.easy_button.centerx - easy_text.get_width()//2, self.easy_button.centery - easy_text.get_height()//2))
        
        # Medium button
        pygame.draw.rect(self.screen, self.YELLOW, self.medium_button)
        medium_text = self.SMALL_FONT.render("Medium", True, self.WHITE)
        self.screen.blit(medium_text, (self.medium_button.centerx - medium_text.get_width()//2, self.medium_button.centery - medium_text.get_height()//2))

        # Hard button
        pygame.draw.rect(self.screen, self.RED, self.hard_button)
        hard_text = self.SMALL_FONT.render("Hard", True, self.WHITE)
        self.screen.blit(hard_text, (self.hard_button.centerx - hard_text.get_width()//2, self.hard_button.centery - hard_text.get_height()//2))

        # Start button
        pygame.draw.rect(self.screen, self.DARK_GRAY, self.start_button)
        start_text = self.SMALL_FONT.render("Start Game", True, self.WHITE)
        self.screen.blit(start_text, (self.start_button.centerx - start_text.get_width()//2, self.start_button.centery - start_text.get_height()//2))
        
        pygame.display.flip()


    # Main loop for the menu
    def run(self): 
        clock = pygame.time.Clock()

        while True:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # When a button is clicked, check which one
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.minus_button.collidepoint(event.pos):
                        if self.mine_count > 10:
                            self.mine_count -= 1

                    elif self.plus_button.collidepoint(event.pos):
                        if self.mine_count < 20:
                            self.mine_count += 1

                    elif self.easy_button.collidepoint(event.pos):
                        pass
                    
                    elif self.medium_button.collidepoint(event.pos):
                        pass

                    elif self.hard_button.collidepoint(event.pos):
                        pass
                    
                    elif self.start_button.collidepoint(event.pos):
                        # Run MineSweeper.py and pass mine_count so it can be used there
                        self.gameStateManager.setState('mine_sweeper', {"numMine": self.mine_count})
                        # Return to loop in Game class
                        return
                    
            clock.tick(30)
