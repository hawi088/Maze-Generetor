# commit 2: "Add DFS maze generation - Mouse eats through walls"
import pygame
import random
import sys
from collections import deque

# Constants
CELL_SIZE = 20
WALL_THICKNESS = 2
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)
MOUSE_COLOR = (255, 0, 0)
DEAD_END_COLOR = (0, 0, 255)
PATH_COLOR = (255, 200, 0)
VISITED_COLOR = (200, 200, 200)
WALL_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)

class Maze:
    def __init__(self, rows, cols, screen):
        self.rows = rows
        self.cols = cols
        self.screen = screen
        self.northWall = [[True for _ in range(cols)] for _ in range(rows)]
        self.eastWall = [[True for _ in range(cols)] for _ in range(rows)]
        self.bottomBoundary = [True for _ in range(cols)]
        self.leftBoundary = [True for _ in range(rows)]
        self.visited = [[False for _ in range(cols)] for _ in range(rows)]
        self.random = random.Random()
        self.start_pos = None
        self.end_pos = None
        self.solution_path = []
        self.dead_ends = []
        
    def draw_cell(self, row, col, color=None):
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        
        if color:
            pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
        else:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
        
        if self.northWall[row][col]:
            pygame.draw.line(self.screen, WALL_COLOR, 
                           (x, y), (x + CELL_SIZE, y), WALL_THICKNESS)
        
        if self.eastWall[row][col]:
            pygame.draw.line(self.screen, WALL_COLOR,
                           (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), WALL_THICKNESS)
        
        if row == self.rows - 1:
            if self.bottomBoundary[col]:
                pygame.draw.line(self.screen, WALL_COLOR,
                               (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), WALL_THICKNESS)
        else:
            if self.northWall[row + 1][col]:
                pygame.draw.line(self.screen, WALL_COLOR,
                               (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), WALL_THICKNESS)
        
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
        if self.start_pos:
            self.draw_cell(self.start_pos[0], self.start_pos[1], START_COLOR)
        if self.end_pos:
            self.draw_cell(self.end_pos[0], self.end_pos[1], END_COLOR)
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
        # Reset
        self.northWall = [[True for _ in range(self.cols)] for _ in range(self.rows)]
        self.eastWall = [[True for _ in range(self.cols)] for _ in range(self.rows)]
        self.bottomBoundary = [True for _ in range(self.cols)]
        self.leftBoundary = [True for _ in range(self.rows)]
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        
        start_row = self.random.randint(0, self.rows - 1)
        start_col = self.random.randint(0, self.cols - 1)
        stack = [(start_row, start_col)]
        self.visited[start_row][start_col] = True
        
        print("mouse is creating the maze...")
        
        while stack:
            r, c = stack[-1]
            self.draw_cell(r, c, (255, 255, 0))
            pygame.display.flip()
            if delay > 0:
                pygame.time.wait(int(delay * 1000))
            
            neighbors = self.get_neighbors(r, c)
            if neighbors:
                nr, nc, direction = self.random.choice(neighbors)
                self.eat_wall((r, c), (nr, nc), direction)
                self.visited[nr][nc] = True
                stack.append((nr, nc))
                self.draw_cell(r, c)
                self.draw_cell(nr, nc)
                pygame.display.flip()
            else:
                stack.pop()
                self.draw_cell(r, c, VISITED_COLOR)
                pygame.display.flip()
                if delay > 0:
                    pygame.time.wait(int(delay * 1000))
        
        # Set start and end on opposite edges
        edge_choice = self.random.choice(['left_right', 'top_bottom'])
        if edge_choice == 'left_right':
            self.start_pos = (self.random.randint(0, self.rows - 1), 0)
            self.end_pos = (self.random.randint(0, self.rows - 1), self.cols - 1)
            self.leftBoundary[self.start_pos[0]] = False
            self.eastWall[self.end_pos[0]][self.cols - 1] = False
        else:
            self.start_pos = (0, self.random.randint(0, self.cols - 1))
            self.end_pos = (self.rows - 1, self.random.randint(0, self.cols - 1))
            self.northWall[0][self.start_pos[1]] = False
            self.bottomBoundary[self.end_pos[1]] = False
        
        print(f"Start: {self.start_pos} (GREEN)")
        print(f"End: {self.end_pos} (RED)")
        self.draw_maze()

def main():
    pygame.init()
    ROWS, COLS = 15, 20
    WINDOW_WIDTH = COLS * CELL_SIZE + 2
    WINDOW_HEIGHT = ROWS * CELL_SIZE + 2
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Maze Generator")
    
    maze = Maze(ROWS, COLS, screen)
    maze.generate_maze(delay=0.03)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()