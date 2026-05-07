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
CYCLE_WALL_COLOR = (255, 0, 255)  

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
        self.dead_ends = []
        self.cycle_walls = [] 
        
    def draw_cell(self, row, col, color=None):
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        
        if color:
            pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
        else:
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
        
        if self.northWall[row][col]: 
            if ('north', row, col) in self.cycle_walls:
                pygame.draw.line(self.screen, CYCLE_WALL_COLOR, 
                               (x, y), (x + CELL_SIZE, y), WALL_THICKNESS)
            else:
                pygame.draw.line(self.screen, WALL_COLOR, 
                               (x, y), (x + CELL_SIZE, y), WALL_THICKNESS)
        if self.eastWall[row][col]:
            # MODIFIED for BONUS: Check if this is a cycle wall to draw in magenta
            if ('east', row, col) in self.cycle_walls:
                pygame.draw.line(self.screen, CYCLE_WALL_COLOR,
                               (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), WALL_THICKNESS)
            else:
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
    
    def can_move(self, row, col, direction):
        if direction == 'up':
            if row > 0 and not self.northWall[row][col]:
                return True
        elif direction == 'down':
            if row < self.rows - 1 and not self.northWall[row + 1][col]:
                return True
        elif direction == 'left':
            if col > 0 and not self.eastWall[row][col - 1]:
                return True
        elif direction == 'right':
            if col < self.cols - 1 and not self.eastWall[row][col]:
                return True
        return False
    
    def get_possible_moves(self, row, col):
        moves = []
        if self.can_move(row, col, 'up'):
            moves.append(('up', row - 1, col))
        if self.can_move(row, col, 'down'):
            moves.append(('down', row + 1, col))
        if self.can_move(row, col, 'left'):
            moves.append(('left', row, col - 1))
        if self.can_move(row, col, 'right'):
            moves.append(('right', row, col + 1))
        return moves
    
   
    def is_connected(self):
        """Check if start and end are connected using BFS"""
        if not self.start_pos or not self.end_pos:
            return False
        
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        queue = deque([self.start_pos])
        visited[self.start_pos[0]][self.start_pos[1]] = True
        
        while queue:
            r, c = queue.popleft()
            
            if (r, c) == self.end_pos:
                return True
            
           
            if r > 0 and not self.northWall[r][c] and not visited[r-1][c]:
                visited[r-1][c] = True
                queue.append((r-1, c))
            if r < self.rows-1 and not self.northWall[r+1][c] and not visited[r+1][c]:
                visited[r+1][c] = True
                queue.append((r+1, c))
            if c > 0 and not self.eastWall[r][c-1] and not visited[r][c-1]:
                visited[r][c-1] = True
                queue.append((r, c-1))
            if c < self.cols-1 and not self.eastWall[r][c] and not visited[r][c+1]:
                visited[r][c+1] = True
                queue.append((r, c+1))
        
        return False
    
    def solve_maze_with_backtracking(self, delay=0.03):
        if not self.start_pos or not self.end_pos:
            print("Maze not generated yet!")
            return False
        
        solver_visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.dead_ends = []
        stack = [(self.start_pos[0], self.start_pos[1])]
        solver_visited[self.start_pos[0]][self.start_pos[1]] = True
        
        print("\nsolving by backtracking....")
        
        while stack:
            r, c = stack[-1]
            self.draw_cell(r, c, MOUSE_COLOR)
            pygame.display.flip()
            
            if delay > 0:
                pygame.time.wait(int(delay * 1000))
            
            if (r, c) == self.end_pos:
                print(f" PATH FOUND! Length: {len(stack)}")
                for pos in stack:
                    self.draw_cell(pos[0], pos[1], PATH_COLOR)
                self.draw_cell(self.end_pos[0], self.end_pos[1], END_COLOR)
                pygame.display.flip()
                pygame.time.wait(2000)
                return True
            
            moves = self.get_possible_moves(r, c)
            unvisited_moves = [(dir, nr, nc) for dir, nr, nc in moves 
                              if not solver_visited[nr][nc]]
            
            if unvisited_moves:
                direction, nr, nc = unvisited_moves[0]
                solver_visited[nr][nc] = True
                stack.append((nr, nc))
            else:
                dead_end = stack.pop()
                self.dead_ends.append(dead_end)
                self.draw_cell(dead_end[0], dead_end[1], DEAD_END_COLOR)
                pygame.display.flip()
                if delay > 0:
                    pygame.time.wait(int(delay * 1000))
        
        print("No path found!")
        return False
    
    # MODIFIED for BONUS: Added cycle detection message
    def left_hand_rule_demo(self, delay=0.03):
        """Demonstrate left-hand rule (shoulder-to-the-wall)"""
        if not self.start_pos or not self.end_pos:
            return False
        
        self.draw_maze()
        r, c = self.start_pos
        facing = 0  # 0: up, 1: right, 2: down, 3: left
        visited_with_facing = set()
        steps = 0
        max_steps = self.rows * self.cols * 5
        
        print("\nleft hand rule..")
        # ADDED for BONUS: Warning about cycles
        if self.cycle_walls:
            print("This maze has CYCLES! Left-hand rule may fail!")
        
        while steps < max_steps:
            steps += 1
            self.draw_cell(r, c, MOUSE_COLOR)
            pygame.display.flip()
            
            if delay > 0:
                pygame.time.wait(int(delay * 1000))
            
            if (r, c) == self.end_pos:
                print(f" Left-hand rule found exit in {steps} steps!")
                pygame.time.wait(2000)
                return True
            
            found_move = False
            for turn in [-1, 0, 1, 2]:
                new_facing = (facing + turn) % 4
                nr, nc = r, c
                
                if new_facing == 0:
                    nr, nc = r - 1, c
                elif new_facing == 1:
                    nr, nc = r, c + 1
                elif new_facing == 2:
                    nr, nc = r + 1, c
                else:
                    nr, nc = r, c - 1
                
                valid = True
                if nr < 0 or nr >= self.rows or nc < 0 or nc >= self.cols:
                    valid = False
                else:
                    if new_facing == 0 and self.northWall[r][c]:
                        valid = False
                    elif new_facing == 1 and self.eastWall[r][c]:
                        valid = False
                    elif new_facing == 2 and self.northWall[nr][nc]:
                        valid = False
                    elif new_facing == 3 and self.eastWall[r][nc]:
                        valid = False
                
                if valid:
                    if (r, c) != self.start_pos:
                        self.draw_cell(r, c, VISITED_COLOR)
                    r, c = nr, nc
                    facing = new_facing
                    found_move = True
                    
                    state = (r, c, facing)
                    if state in visited_with_facing:
                        print(f"\n loop found at ({r},{c}) after {steps} steps!")
                        print("stuck in cycle")
                        # ADDED for BONUS: Better explanation
                        print("\n💡 The left-hand rule failed because cycles in the maze")
                        print("   created a loop that the mouse cannot escape!")
                        pygame.time.wait(3000)
                        return False
                    visited_with_facing.add(state)
                    break
            
            if not found_move:
                print("\nNo valid moves left")
                return False
        
        print("\n exceeded maximum steps")
        return False
    
   
    def generate_maze(self, delay=0.03):
        self.northWall = [[True for _ in range(self.cols)] for _ in range(self.rows)]
        self.eastWall = [[True for _ in range(self.cols)] for _ in range(self.rows)]
        self.bottomBoundary = [True for _ in range(self.cols)]
        self.leftBoundary = [True for _ in range(self.rows)]
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.cycle_walls = [] 
        
        start_row = self.random.randint(0, self.rows - 1)
        start_col = self.random.randint(0, self.cols - 1)
        stack = [(start_row, start_col)]
        self.visited[start_row][start_col] = True
        
        print("mouse generating maze...")
        
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
        
        print(f" Start: {self.start_pos}  End: {self.end_pos}")
        
        
        print("\nAdding extra walls with 1/20 chance to create CYCLES...")
        extra_wall_count = 0
        

        candidate_walls = []
        for r in range(self.rows):
            for c in range(self.cols):
                # North wall candidate (if it doesn't exist)
                if not self.northWall[r][c] and r > 0:
                    candidate_walls.append(('north', r, c))
                # East wall candidate (if it doesn't exist)
                if not self.eastWall[r][c]:
                    candidate_walls.append(('east', r, c))
        
        # Randomly add walls with 1 in 20 chance
        random.shuffle(candidate_walls)
        for wall_type, r, c in candidate_walls:
            if self.random.randint(1, 20) == 1:  # 1 in 20 chance
                # Try adding the wall
                old_state = None
                if wall_type == 'north':
                    old_state = self.northWall[r][c]
                    self.northWall[r][c] = True
                else:  # east
                    old_state = self.eastWall[r][c]
                    self.eastWall[r][c] = True
                
                # Check if start and end are still connected
                if self.is_connected():
                    extra_wall_count += 1
                    self.cycle_walls.append((wall_type, r, c))
                    print(f"  ✓ Added wall at ({r},{c}) - Created a CYCLE!")
                    # Draw the new wall in magenta briefly to highlight
                    self.draw_cell(r, c)
                    if wall_type == 'north' and r > 0:
                        self.draw_cell(r-1, c)
                    elif wall_type == 'east' and c < self.cols-1:
                        self.draw_cell(r, c+1)
                    pygame.display.flip()
                    pygame.time.wait(300)
                else:
                    # Revert the wall - it would disconnect the maze
                    if wall_type == 'north':
                        self.northWall[r][c] = old_state
                    else:
                        self.eastWall[r][c] = old_state
        
        if extra_wall_count > 0:
            print(f"\nAdded {extra_wall_count} extra walls creating CYCLES!")
            pygame.time.wait(2000)
        else:
            print("\n No cycles created.Press R to try again!")
       
        self.draw_maze()

def main():
    pygame.init()
    ROWS, COLS = 15, 20
    screen = pygame.display.set_mode((COLS * CELL_SIZE + 2, ROWS * CELL_SIZE + 2))
    pygame.display.set_caption("Maze generator") 
    maze = Maze(ROWS, COLS, screen)
    maze.generate_maze(delay=0.03)
    
    print("\n" + "="*50)  
    print("SPACE - Backtracking (RED dot, BLUE dead ends) - ALWAYS works")
    print("L     - Left-hand rule demo - WILL FAIL with cycles")
    print("R     - New maze | ESC - Exit")
    running = True
    solving = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    maze.generate_maze(delay=0.03)
                elif event.key == pygame.K_SPACE and not solving:
                    solving = True
                    maze.solve_maze_with_backtracking(delay=0.03)
                    solving = False
                elif event.key == pygame.K_l and not solving:
                    solving = True
                    maze.left_hand_rule_demo(delay=0.03)
                    solving = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()