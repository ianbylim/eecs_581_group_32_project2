'''
Module: Minesweeper Game
Description: Implements the main game loop for Minesweeper, handling user input, game state updates, and rendering the game board and HUD. Implements AI if neccessary.
Inputs: User mouse clicks
Outputs: Graphical display of the game board and HUD, game state changes (win/loss)
External Sources: Pygame library for graphics and event handling
    How to install pygames - https://www.geeksforgeeks.org/installation-guide/how-to-install-pygame-in-windows/
    Pygames documentation - https://www.pygame.org/docs/
    Pygames Tutorial - https://coderslegacy.com/python/python-pygame-tutorial/
Authors: Wesley McDougal, Abdulaziz Ali, Matthew Nash, Malek Kchaou, Jace Keagy, K Li, Ian Lim, Jenna Luong, Kit Magar, Bryce Martin.
Creation Date: 9/4/2025
'''

# Imports
import pygame
import sys
import BoardGenerator
from grid import Grid
import random

# RGB variables
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

# App window sizing configuration (in pixels)
grid_width = 10
grid_height = 10
grid_size = 32
border = 30
top_border = 90
grid_offset_x = 5
grid_offset_y = 10
app_width = grid_size * grid_width + border * 2
app_height = grid_size * grid_height + border + top_border

# Coloring for the grid and background
bg_color = (192, 192, 192)
grid_color = (128, 128, 128)

class MineSweeper:
    def __init__(self, gameStateManager):
        '''
        Takes in a gameStateManagers object and inializes the window that the board
        which the board will be drawn on
        '''
        
        pygame.init()
        
        # Creates main pygame window
        self.gameDisplay = pygame.display.set_mode((app_width, app_height))
        
        # Control FPS
        self.clock = pygame.time.Clock()  
        
        # Set game state manager
        self.gameStateManager = gameStateManager

        
        pygame.display.set_caption("Minesweeper")  # Set window title to "Minesweeper"
        
        # Track if grid has been generated
        self.initialized = False

        # Flag to track first click 
        self.first_click = True

        # Track the difficulty
        self.difficulty = None

        # HUD Assets
        self.flag_icon = pygame.image.load("sprites/flag.png")
        self.retry_icon = pygame.image.load("sprites/retry.png")
        self.quit_icon = pygame.image.load("sprites/quit.png")

        # Icons on HUD
        icon_size = 48
        self.flag_icon = pygame.transform.scale(self.flag_icon, (icon_size, icon_size))
        self.retry_icon = pygame.transform.scale(self.retry_icon, (icon_size, icon_size))
        self.quit_icon = pygame.transform.scale(self.quit_icon, (icon_size, icon_size))

        # Rects for interaction
        self.flag_rect = self.flag_icon.get_rect(topleft=(border, border-20))
        self.retry_rect = self.retry_icon.get_rect(topleft=(border + 120, border-20))
        self.quit_rect = self.quit_icon.get_rect(topleft=(border + 180, border-20))

        # Track game state text
        self.game_status = "Playing"

        # SFX: load 
        self._s_click = self._try_load_sfx("audio/click.wav", 0.7)
        self._s_flag  = self._try_load_sfx("audio/flag.wav",  0.7)
        self._s_unflg = self._try_load_sfx("audio/unflag.wav", 0.7)  
        self._s_win   = self._try_load_sfx("audio/win.wav",   0.8)
        self._s_lose  = self._try_load_sfx("audio/lose.wav",  0.8)
        

    # SFX helpers
    def _try_load_sfx(self, path, vol=0.7):
        try:
            s = pygame.mixer.Sound(path)
            s.set_volume(vol)
            return s
        except Exception:
            return None

    def _play(self, sfx):
        if sfx:
            try: sfx.play()
            except Exception: pass
    

    def draw_hud(self, surface):
        '''
        Draws the hud elements flags left, retry, back to menu, 
        and game status to the top of the provided surface
        '''
        
        # Draw flag icon + remaining flag count
        surface.blit(self.flag_icon, self.flag_rect.topleft)

        # Count how many flags are currently placed on the board
        flags_placed = sum(cell.flag for row in self.grid for cell in row)

        # Calculate remaining flags available to place
        remaining_flags = len(self.mines) - flags_placed

        # Draw remaining flag count
        font = pygame.font.SysFont("Calibri", 24, True)
        text = font.render(str(remaining_flags), True, black)
        surface.blit(text, (self.flag_rect.right + 15, self.flag_rect.y + 15))

        # Draw retry + quit buttons
        surface.blit(self.retry_icon, self.retry_rect.topleft)
        surface.blit(self.quit_icon, self.quit_rect.topleft)
        
        # Determine text color based on game status
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        if self.game_status == "Playing":
            status_color = BLUE
        elif self.game_status == "Win":
            status_color = GREEN
        elif self.game_status == "Loss":
            status_color = RED

        # Draw game state (Playing, Win, Loss)
        status_text = font.render(self.game_status, True, status_color)
        surface.blit(status_text, (app_width - status_text.get_width() - border, border - 10))

    # Utility function
    def drawText(self, txt, s, yOff=0):
        """
        Draws text centered on the game screen.
        txt  = text string
        s    = font size
        yOff = vertical offset for placement
        """
        
        # Creates a font surface Object
        screen_text = pygame.font.SysFont("Calibri", s, True).render(txt, True, blue)  
        # Get rectangle boundary of text
        rect = screen_text.get_rect()  
        # Center text in the grid area with vertical offset
        rect.center = (grid_width * grid_size / 2 + border, 
                    grid_height * grid_size / 2 + top_border + yOff)
        self.gameDisplay.blit(screen_text, rect)  # Draws text to screen

    def draw_labels(self, surface):
        '''
        Draws column letters (A-J) and row numbers (1-10) around the grid
        '''
        
        font = pygame.font.SysFont("Calibri", 20, True)
        padding = 25
        # Create text for column labels
        for col in range(grid_width):
            # Increment the column letter decimal value by 1 
            label = chr(ord('A') + col) 
            text = font.render(label, True, black)

            x = border + grid_offset_x + col * grid_size + grid_size // 2 - text.get_width() // 2
            # Position on top of the grid
            y = top_border + grid_offset_y - 30
            surface.blit(text, (x, y)) # Draw to screen

        # Create the text for row labels
        for row in range(grid_height):
            label = str(row + 1)
            text = font.render(label, True, black)
            # Position to the left
            x = border + grid_offset_x - padding
            y = top_border + grid_offset_y + row * grid_size + grid_size // 2 - text.get_height() // 2
            surface.blit(text, (x, y))# Draw to screen
    
    def initialize_minesweeper(self, safe_row=None, safe_col=None):
        '''
        Takes in safe_row and safe_col (both optional) that should be garanted to be empty
        and generated a grid will the specified amount of bombs. It then numbers the approximate
        mine count and converts the grid into sprite objects.
        '''
        
        # Get number of mines from state manager
        params = self.gameStateManager.getParams()
        # Set to 10 if param set to num
        numMine = params.get("numMine", 10)
        self.difficulty = params.get("difficulty")

        # Program entry point
        #print(f"gameloop start... \nNumber of Mines = {numMine}")  # Debug print to console

        # 1. Create bomb grid (10x10 with bombs randomly placed)
        raw_grid = BoardGenerator.generate_bombs(numMine, safe_row, safe_col)
        # 2. Create numbering for adjacent mines
        raw_grid = BoardGenerator.generate_numbering(raw_grid)

        # #-> Prints raw_grid
        # print("Heres raw_grid:")
        # BoardGenerator.print_grid(raw_grid)
    
        # 3. Convert raw grid into Grid objects
        self.grid = [[Grid(x, y, "b" if raw_grid[y][x] == 'b' else int(raw_grid[y][x]), self.gameDisplay, border+grid_offset_x, top_border+grid_offset_y, grid_size) for x in range(grid_width)] for y in range(grid_height)]
        self.mines = [(x, y) for y in range(grid_height) for x in range(grid_width) if raw_grid[y][x] == 'b']

        # Game state tracking
        self.game_win = False
        self.game_over = False
        
        self.initialized = True
    
    def check_state(self, result, cell):

        if result == "mine":
            # Game over: player clicked on a mine
            self.game_over = True
            self.game_win = False
            self.game_status = "Loss"
            self._play(self._s_lose)  # SFX (added)
            # Reveal all mines
            for mx, my in self.mines:
                self.grid[my][mx].clicked = True
                    
        # If the cell is empty, recursively reveal neighbors
        if result == "empty":
            self.reveal_neighbors(cell.xGrid, cell.yGrid)

        # Check for win
        if self.check_win():
            self.game_over = True
            self.game_win = True
            self.game_status = "Win"
            self._play(self._s_win)  # SFX (added)

    # Main game loop
    def run(self):
            '''
            Initializes the board and handls player input (clicks, flags, quits), 
            updats the grid, checks win/loss conditions, and redraws the screen each frame
            '''
        
            if not self.initialized:
                self.initialize_minesweeper()

            while not self.game_over:
                # Handle events
                for event in pygame.event.get():

                    # For debug purposes
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:  # Press 'W' to trigger a win
                            self.game_over = True
                            self.game_win = True
                            self.game_status = "Win"
                            # Optionally reveal all cells
                            for row in self.grid:
                                for cell in row:
                                    cell.clicked = True

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()

                        # HUD interactions first
                        if self.retry_rect.collidepoint(mouse_pos):
                            self.initialized = False  # Reset
                            self.first_click = True
                            self.run()  # Restart game
                            return
                        elif self.quit_rect.collidepoint(mouse_pos):
                            self.gameStateManager.setState("main_menu")
                            return
                            
                        for row in self.grid:
                            for cell in row:
                                if cell.rect.collidepoint(mouse_pos): # If mouse click is within cell
                                    if event.button == 1:  # Left click
                                        if self.first_click:
                                            self.first_click = False
                                            # Regenerate board guaranteeing this cell is safe
                                            self.initialize_minesweeper(cell.yGrid, cell.xGrid)

                                            # Now reveal the chosen cell safely
                                            result = self.grid[cell.yGrid][cell.xGrid].reveal()
                                            self._play(self._s_click)

                                            if result == "empty":
                                                self.reveal_neighbors(cell.xGrid, cell.yGrid)

                                            self.check_state(result, self.grid[cell.yGrid][cell.xGrid])

                                        else:
                                            result = cell.reveal()
                                            self._play(self._s_click)  # SFX (added)

                                            self.check_state(result,cell)
                                            
                                            if self.difficulty == "easy" or self.difficulty == "medium" or self.difficulty == "hard":
                                                if result == "number":       
                                                    result, cell = self.ai_uncover() # AI takes a turn and uncovers a cell

                                            self.check_state(result,cell)
                                            
                                    # Right click to toggle flag
                                    elif event.button == 3:  
                                        prev = cell.flag                     # (added) capture prior state
                                        cell.toggleFlag()
                                        if cell.flag and not prev:
                                            self._play(self._s_flag)         # SFX (added)
                                        elif (not cell.flag) and prev:
                                            self._play(self._s_unflg or self._s_flag)  # SFX (added, fallback)

                # Draw grid and create off-screen frame buffer
                frame_surface = pygame.Surface((app_width, app_height))
                frame_surface.fill((192, 192, 192))  # Background
                for row in self.grid:
                    for cell in row:
                        cell.drawGrid(frame_surface)

                # Draw labels and HUD
                self.draw_labels(frame_surface)                
                self.draw_hud(frame_surface)
                
                # Blit buffer to main display
                self.gameDisplay.blit(frame_surface, (0,0))
                pygame.display.flip()  # Flip once per frame
                self.clock.tick(30)

            # Wait for user input to restart or quit to menu
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.retry_rect.collidepoint(mouse_pos):
                            self.initialized = False  # Reset
                            self.first_click = True
                            self.game_status = "Playing"
                            self.run()  # Restart game
                            waiting = False
                        elif self.quit_rect.collidepoint(mouse_pos):
                            self.gameStateManager.setState("main_menu")
                            waiting = False
    
    def reveal_neighbors(self, x, y):
        '''
        Goes through the board and reveals empty
        spaces attached to a clicked empty space
        '''
        
        queue = [(x, y)]
        visited = set()
        
        while queue:

            # Process current cell
            cx, cy = queue.pop(0)  
            
            # Skip if already processed
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            
            # Check all 8 neighbors
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    # Skip the center cell (current cell)
                    if dx == 0 and dy == 0:
                        continue
                        
                    nx, ny = cx + dx, cy + dy
                    
                    # Check bounds and if already visited
                    if (0 <= nx < grid_width and 0 <= ny < grid_height and 
                        (nx, ny) not in visited):
                        
                        neighbor = self.grid[ny][nx]
                        
                        # Only reveal unclicked, unflagged cells
                        if not neighbor.clicked and not neighbor.flag:
                            result = neighbor.reveal()
                            
                            # If empty, add to queue for further processing
                            if result == "empty":
                                queue.append((nx, ny))

    def check_win(self):
        '''
        Iterate through the grid and checks if a 
        cell is not a bomb and has not been clicked.
        '''
        
        for row in self.grid:
            for cell in row:
                if cell.val != "b" and not cell.clicked:
                    return False
        return True
    
    def check_lose(self):
        '''
        Iterate through the grid and checks if a 
        cell is a bomb and has been clicked.
        '''
        
        for row in self.grid:
            for cell in row:
                if cell.val == "b" and cell.clicked:
                    return True
        return False
    
    # iterate over all clicked cells to find neighboring cells that can be flagged
    def flag_cells(self,clicked_cells,unclicked_cells):
        for x,y in clicked_cells:
                hidden_neighbor = []
                flagged_neighbor = []
                # check all neighbors
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        #skip the cell itself
                        if di == 0 and dj == 0:
                            continue 
                        # Calculate adjacent cell coordinates
                        ni, nj = x + di, y + dj
                        # Check if coordinates are within grid bounds
                        if 0 <= ni < len(self.grid) and 0 <= nj < len(self.grid[0]):
                            # Check if the neighboring cell is not clicked and is not flagged and add to array
                            if (ni,nj) in unclicked_cells and not self.grid[nj][ni].flag:
                                hidden_neighbor.append((ni,nj))
                            # Check if the neighboring cell is a valid flag and add to array
                            if self.grid[nj][ni].flag and self.grid[nj][ni].val == 'b':
                                flagged_neighbor.append((ni,nj))
                # If the number of hidden neighbors matches the value of the cell, flag all hidden neighbors and update
                if  self.grid[y][x].val == (len(hidden_neighbor)+len(flagged_neighbor)):
                    for i,j in hidden_neighbor:
                        if not self.grid[j][i].flag:
                            self.grid[j][i].toggleFlag()
                            hidden_neighbor.remove((i,j))
                            flagged_neighbor.append((i,j))

    # Find cells with matching value and number of flagged neighbors to reveal safe cell
    def reveal_hidden_neighbor(self,clicked_cells,unclicked_cells):
        
            for x,y in clicked_cells:
                flagged_neighbor = []
                hidden_neighbor = []
                # Check all neighbors
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        #skip the cell itself
                        if di == 0 and dj == 0:
                            continue 
                        # Calculate adjacent cell coordinates
                        ni, nj = x + di, y + dj
                        # Check if coordinates are within grid bounds
                        if 0 <= ni < len(self.grid) and 0 <= nj < len(self.grid[0]):
                            # Check if the neighboring cell is not clicked and is not flagged and add to array
                            if (ni,nj) in unclicked_cells and not self.grid[nj][ni].flag:
                                hidden_neighbor.append((ni,nj))
                            # Check if the neighboring cell is a valid flag and add to array
                            if self.grid[nj][ni].flag and self.grid[nj][ni].val == 'b':
                                flagged_neighbor.append((ni,nj))
                # If the value of the cell matches the number of flagged neighbors and there are hidden neighbors, reveal hidden neighbor                
                if self.grid[y][x].val == len(flagged_neighbor) and len(hidden_neighbor)!=0:
                    i,j = hidden_neighbor[0]
                    return self.grid[j][i].reveal(), self.grid[j][i]


    def ai_uncover(self):
        if self.difficulty == "easy":
            # Find all unclicked, non-flagged cells
            unclicked_cells = [(x, y) for y in range(grid_height) for x in range(grid_width) 
                if not self.grid[y][x].clicked and not self.grid[y][x].flag]
            
            if not unclicked_cells:
                return None, None
            
            # Randomly choose one cell
            x, y = random.choice(unclicked_cells)
            return self.grid[y][x].reveal(), self.grid[y][x]  # Uncover the chosen cell

        elif self.difficulty == "medium":
            # Find all unclicked, non-flagged cells
            unclicked_cells = [(x, y) for y in range(grid_height) for x in range(grid_width) 
                if not self.grid[y][x].clicked and not self.grid[y][x].flag]
            # Find all clicked, non-flagged cells that neighbor mines
            clicked_cells = [(x, y) for y in range(grid_height) for x in range(grid_width) 
                if self.grid[y][x].clicked and not self.grid[y][x].flag and self.grid[y][x].val != 0]
            
            # iterate over all clicked cells to find neighboring cells that can be flagged
            self.flag_cells(clicked_cells,unclicked_cells)

            # Find cells with matching value and number of flagged neighbors to reveal safe cell
            self.reveal_hidden_neighbor(clicked_cells,unclicked_cells)

            # If the game is not already won, choose a random unclicked cell to reveal
            if self.game_status != 'win':
                if not unclicked_cells:
                    return None, None
                x, y = random.choice(unclicked_cells)
                return self.grid[y][x].reveal(), self.grid[y][x]
        
        elif self.difficulty == "hard":
           # Find all unclicked, non-flagged cells
            unclicked_cells = [(x, y) for y in range(grid_height) for x in range(grid_width) 
                if not self.grid[y][x].clicked and not self.grid[y][x].flag]
            # Find all clicked, non-flagged cells that neighbor mines
            clicked_cells = [(x, y) for y in range(grid_height) for x in range(grid_width) 
                if self.grid[y][x].clicked and not self.grid[y][x].flag and self.grid[y][x].val != 0]
            
            # iterate over all clicked cells to find neighboring cells that can be flagged
            self.flag_cells(clicked_cells,unclicked_cells)
            
            # Find cells with matching value and number of flagged neighbors to reveal safe cell
            self.reveal_hidden_neighbor(clicked_cells,unclicked_cells)
            # 3) Hard extra: 1-2-1 pattern (horizontal & vertical)
            #    Action priority: flag outer hidden first; if outers settled, reveal middle if hidden.
            # --- horizontal 1-2-1 (numbers at y, x..x+2), act on row below or above ---
            for y in range(grid_height):
                for x in range(grid_width - 2):
                    c1 = self.grid[y][x]
                    c2 = self.grid[y][x+1]
                    c3 = self.grid[y][x+2]
                    if c1.clicked and c2.clicked and c3.clicked and c1.val == 1 and c2.val == 2 and c3.val == 1:
                        # try row below
                        if y + 1 < grid_height:
                            b0 = self.grid[y+1][x]
                            b1 = self.grid[y+1][x+1]
                            b2 = self.grid[y+1][x+2]
                            # prefer flagging outer unknowns
                            if not b0.clicked and not b0.flag:
                                b0.toggleFlag()
                                return None, None
                            if not b2.clicked and not b2.flag:
                                b2.toggleFlag()
                                return None, None
                            # then reveal middle if still hidden & not flagged
                            if not b1.clicked and not b1.flag:
                                return b1.reveal(), b1
                        # try row above
                        if y - 1 >= 0:
                            a0 = self.grid[y-1][x]
                            a1 = self.grid[y-1][x+1]
                            a2 = self.grid[y-1][x+2]
                            if not a0.clicked and not a0.flag:
                                a0.toggleFlag()
                                return None, None
                            if not a2.clicked and not a2.flag:
                                a2.toggleFlag()
                                return None, None
                            if not a1.clicked and not a1.flag:
                                return a1.reveal(), a1

            # --- vertical 1-2-1 (numbers at x, y..y+2), act on column right or left ---
            for x in range(grid_width):
                for y in range(grid_height - 2):
                    c1 = self.grid[y][x]
                    c2 = self.grid[y+1][x]
                    c3 = self.grid[y+2][x]
                    if c1.clicked and c2.clicked and c3.clicked and c1.val == 1 and c2.val == 2 and c3.val == 1:
                        # try column right
                        if x + 1 < grid_width:
                            r0 = self.grid[y][x+1]
                            r1 = self.grid[y+1][x+1]
                            r2 = self.grid[y+2][x+1]
                            if not r0.clicked and not r0.flag:
                                r0.toggleFlag()
                                return None, None
                            if not r2.clicked and not r2.flag:
                                r2.toggleFlag()
                                return None, None
                            if not r1.clicked and not r1.flag:
                                return r1.reveal(), r1
                        # try column left
                        if x - 1 >= 0:
                            l0 = self.grid[y][x-1]
                            l1 = self.grid[y+1][x-1]
                            l2 = self.grid[y+2][x-1]
                            if not l0.clicked and not l0.flag:
                                l0.toggleFlag()
                                return None, None
                            if not l2.clicked and not l2.flag:
                                l2.toggleFlag()
                                return None, None
                            if not l1.clicked and not l1.flag:
                                return l1.reveal(), l1

            
                
            # If the game is not already won, choose a random unclicked cell to reveal
            if self.game_status != 'win':
                if not unclicked_cells:
                    return None, None
                x, y = random.choice(unclicked_cells)
                return self.grid[y][x].reveal(), self.grid[y][x]
        