import pygame
import sys

# Constants
CELL_SIZE = 20
WALL_THICKNESS = 2
WALL_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)

class Maze:
    def __init__(self, rows, cols, screen):
        self.rows = rows
        self.cols = cols
        self.screen = screen
        
        # Initialize all walls as solid
        self.northWall = [[True for _ in range(cols)] for _ in range(rows)]
        self.eastWall = [[True for _ in range(cols)] for _ in range(rows)]
        self.bottomBoundary = [True for _ in range(cols)]
        self.leftBoundary = [True for _ in range(rows)]
        
    def draw_cell(self, row, col):
        """Draw a single cell with its walls"""
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        
        # Fill cell background
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
        
        # Draw north wall
        if self.northWall[row][col]:
            pygame.draw.line(self.screen, WALL_COLOR, 
                           (x, y), (x + CELL_SIZE, y), WALL_THICKNESS)
        
        # Draw east wall
        if self.eastWall[row][col]:
            pygame.draw.line(self.screen, WALL_COLOR,
                           (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), WALL_THICKNESS)
        
        # Draw south wall
        if row == self.rows - 1:
            if self.bottomBoundary[col]:
                pygame.draw.line(self.screen, WALL_COLOR,
                               (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), WALL_THICKNESS)
        else:
            if self.northWall[row + 1][col]:
                pygame.draw.line(self.screen, WALL_COLOR,
                               (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), WALL_THICKNESS)
        
        # Draw west wall
        if col == 0:
            if self.leftBoundary[row]:
                pygame.draw.line(self.screen, WALL_COLOR,
                               (x, y), (x, y + CELL_SIZE), WALL_THICKNESS)
        else:
            if self.eastWall[row][col - 1]:
                pygame.draw.line(self.screen, WALL_COLOR,
                               (x, y), (x, y + CELL_SIZE), WALL_THICKNESS)
    
    def draw_maze(self):
        """Draw the complete maze"""
        self.screen.fill(BACKGROUND_COLOR)
        for r in range(self.rows):
            for c in range(self.cols):
                self.draw_cell(r, c)
        pygame.display.flip()

def main():
    pygame.init()
    
    ROWS = 15
    COLS = 20
    
    WINDOW_WIDTH = COLS * CELL_SIZE + 2
    WINDOW_HEIGHT = ROWS * CELL_SIZE + 2
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Maze Generator")
    
    maze = Maze(ROWS, COLS, screen)
    maze.draw_maze()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()