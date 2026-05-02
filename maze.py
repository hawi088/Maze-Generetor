import pygame
import random
import sys

# Constants
CELL_SIZE = 20
WALL_THICKNESS = 2
VISITED_COLOR = (200, 200, 200)
WALL_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)

class Maze:
    def __init__(self, rows, cols, screen):
        self.rows = rows
        self.cols = cols
        self.screen = screen
        
        # Wall representation
        self.northWall = [[True for _ in range(cols)] for _ in range(rows)]
        self.eastWall = [[True for _ in range(cols)] for _ in range(rows)]
        self.bottomBoundary = [True for _ in range(cols)]
        self.leftBoundary = [True for _ in range(rows)]
        
        # Visited tracking for generation
        self.visited = [[False for _ in range(cols)] for _ in range(rows)]
        
        # Random number generator
        self.random = random.Random()
        
    def draw_cell(self, row, col, color=None):
        
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        
        if color:
            pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
        else:
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
        
        self.screen.fill(BACKGROUND_COLOR)
        for r in range(self.rows):
            for c in range(self.cols):
                self.draw_cell(r, c)
        pygame.display.flip()
    
    def get_neighbors(self, row, col):
       
        neighbors = []
        
        if row > 0 and not self.visited[row - 1][col]:
            neighbors.append((row - 1, col, 'north'))
        if row < self.rows - 1 and not self.visited[row + 1][col]:
            neighbors.append((row + 1, col, 'south'))
        if col > 0 and not self.visited[row][col - 1]:
            neighbors.append((row, col - 1, 'west'))
        if col < self.cols - 1 and not self.visited[row][col + 1]:
            neighbors.append((row, col + 1, 'east'))
        
        return neighbors
    
    def eat_wall(self, from_cell, to_cell, direction):
        
        r1, c1 = from_cell
        r2, c2 = to_cell
        
        if direction == 'north':
            self.northWall[r1][c1] = False
        elif direction == 'south':
            self.northWall[r2][c2] = False
        elif direction == 'west':
            self.eastWall[r1][c1 - 1] = False
        elif direction == 'east':
            self.eastWall[r1][c1] = False
    
    def generate_maze(self, delay=0.03):
       
        # Reset everything
        self.northWall = [[True for _ in range(self.cols)] for _ in range(self.rows)]
        self.eastWall = [[True for _ in range(self.cols)] for _ in range(self.rows)]
        self.bottomBoundary = [True for _ in range(self.cols)]
        self.leftBoundary = [True for _ in range(self.rows)]
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Start at random cell
        start_row = self.random.randint(0, self.rows - 1)
        start_col = self.random.randint(0, self.cols - 1)
        
        stack = [(start_row, start_col)]
        self.visited[start_row][start_col] = True
        
        print("mouse creating maze...")
        
        while stack:
            r, c = stack[-1]
            
            # Draw current cell as YELLOW (mouse position)
            self.draw_cell(r, c, (255, 255, 0))
            pygame.display.flip()
            
            if delay > 0:
                pygame.time.wait(int(delay * 1000))
            
            neighbors = self.get_neighbors(r, c)
            
            if neighbors:
                # Choose random unvisited neighbor
                nr, nc, direction = self.random.choice(neighbors)
                
                # Eat the wall
                self.eat_wall((r, c), (nr, nc), direction)
                
                # Mark as visited and push to stack
                self.visited[nr][nc] = True
                stack.append((nr, nc))
                
                # Redraw cells
                self.draw_cell(r, c)
                self.draw_cell(nr, nc)
                pygame.display.flip()
            else:
                # Dead end - backtrack
                stack.pop()
                self.draw_cell(r, c, VISITED_COLOR)
                pygame.display.flip()
                if delay > 0:
                    pygame.time.wait(int(delay * 1000))
        
        self.draw_maze()
        print("Done")

def main():
    pygame.init()
    
    ROWS = 15
    COLS = 20
    
    WINDOW_WIDTH = COLS * CELL_SIZE + 2
    WINDOW_HEIGHT = ROWS * CELL_SIZE + 2
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Maze Generator - Mouse Eating Walls")
    
    maze = Maze(ROWS, COLS, screen)
    maze.generate_maze(delay=0.03)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    maze.generate_maze(delay=0.03)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()