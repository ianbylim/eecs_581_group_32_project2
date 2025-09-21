'''
Module: Grid class

Description: Represents a single cell in the Minesweeper grid, handling its state (clicked,
flagged, mine status) and rendering the appropriate sprite based on its state.

Inputs: xGrid (int), yGrid (int), type (str or int), gameDisplay (pygame.Surface), 
border (int), top_border (int), grid_size (int)

Outputs: None (but modifies the game display)
External Sources: Pygame library
Authors: Wesley McDougal, Abdulaziz Ali, Matthew Nash, Malek Kchaou
Creation Date: 9/7/2025
'''

import pygame

# Loads sprite images for game
sprite_emptyGrid = pygame.image.load("Sprites/Grid_ClickedOn.png")  # Revealed empty grid
sprite_flag = pygame.image.load("Sprites/flag.png")                 # Flag marker
sprite_grid = pygame.image.load("Sprites/Grid.png")                 # Hidden grid square
sprite_grid1 = pygame.image.load("Sprites/gridnum1.png")            # Grid with number 1
sprite_grid2 = pygame.image.load("Sprites/gridnum2.png")            # Grid with number 2
sprite_grid3 = pygame.image.load("Sprites/gridnum3.png")            # Grid with number 3
sprite_grid4 = pygame.image.load("Sprites/gridnum4.png")            # Grid with number 4
sprite_grid5 = pygame.image.load("Sprites/gridnum5.png")            # Grid with number 5
sprite_grid6 = pygame.image.load("Sprites/gridnum6.png")            # Grid with number 6
sprite_grid7 = pygame.image.load("Sprites/gridnum7.png")            # Grid with number 7
sprite_grid8 = pygame.image.load("Sprites/gridnum8.png")            # Grid with number 8
sprite_mine = pygame.image.load("Sprites/mineNeutral.png")          # Untriggered mine
sprite_mineClicked = pygame.image.load("Sprites/mineClickedOn.png") # Mine that was clicked
sprite_mineFalse = pygame.image.load("Sprites/mineFalse.png")       # Wrongly flagged mine

class Grid:
    def __init__(self, xGrid, yGrid, type, gameDisplay, border, top_border, grid_size,):
        '''
        Initialize the grid with provided parameters
        '''

        self.xGrid = xGrid
        self.yGrid = yGrid
        self.clicked = False
        self.mineClicked = False
        self.mineFalse = False
        self.flag = False
        # Rect(left, top, width, height) -> Rect
        self.rect = pygame.Rect(border + self.xGrid * grid_size,
                                top_border + self.yGrid * grid_size,
                                grid_size, grid_size)
        self.val = type
        self.gameDisplay = gameDisplay

    # Draws the sprites onto grid after every click/interaction update
    def drawGrid(self, surface):
        '''
        Assignes each value in the grid to its appropriate sprite
        and draws them on the provided surface.
        '''

        if self.mineFalse:
            surface.blit(sprite_mineFalse, self.rect)
        else:
            if self.clicked:
                if self.val == "b":
                    if self.mineClicked:
                        surface.blit(sprite_mineClicked, self.rect)
                    else:
                        surface.blit(sprite_mine, self.rect)
                else:
                    if self.val == 0:
                        surface.blit(sprite_emptyGrid, self.rect)
                    elif self.val == 1:
                        surface.blit(sprite_grid1, self.rect)
                    elif self.val == 2:
                        surface.blit(sprite_grid2, self.rect)
                    elif self.val == 3:
                        surface.blit(sprite_grid3, self.rect)
                    elif self.val == 4:
                        surface.blit(sprite_grid4, self.rect)
                    elif self.val == 5:
                        surface.blit(sprite_grid5, self.rect)
                    elif self.val == 6:
                        surface.blit(sprite_grid6, self.rect)
                    elif self.val == 7:
                        surface.blit(sprite_grid7, self.rect)
                    elif self.val == 8:
                        surface.blit(sprite_grid8, self.rect)
            else:
                if self.flag:
                    surface.blit(sprite_flag, self.rect)
                else:
                    surface.blit(sprite_grid, self.rect)

    # Add flag toggle method           
    def toggleFlag(self): 
       if not self.clicked:
           self.flag = not self.flag

    def reveal(self):
        '''
        Reveal this tile and return its type.
        '''

        if self.clicked or self.flag:
            return None  # Do nothing if already clicked or flagged

        self.clicked = True

        if self.val == "b":
            self.mineClicked = True
            return "mine"
        elif self.val == 0:
            return "empty"
        else:
            return "number"
