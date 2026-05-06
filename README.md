# Maze Generator and Solver

## Overview
This program generates a random proper maze using a stack-based DFS algorithm (the "mouse eating walls" technique), then solves it using backtracking. The project demonstrates the difference between DFS maze generation and BFS, as well as comparing backtracking vs left-hand rule solving.

## How It Works

### Maze Representation
- `northWall[r][c]`: Boolean array indicating if cell (r,c) has a north wall
- `eastWall[r][c]`: Boolean array indicating if cell (r,c) has an east wall
- Boundaries handled with `bottomBoundary` and `leftBoundary` arrays


**Why stack?** Creates depth-first maze with long corridors and unique paths - perfect for proper mazes.

### Solver (Backtracking)
- RED dot shows current mouse position
- BLUE dots mark explored dead ends
- Uses stack to remember path
- Backtracks when dead end reached
- Gold path shows final solution

### Bonus Challenge: Cycles
- Adds extra walls with 1/20 chance
- Magenta walls indicate cycles (loops)
- Demonstrates why left-hand rule fails with cycles
- Backtracking still works because it remembers visited cells

## Controls
| Key | Action |
|-----|--------|
| SPACE | Solve with backtracking (RED dot, BLUE dead ends) |
| L | Left-hand rule demo (fails with cycles) |
| R | Generate new random maze |
| ESC | Exit |

## Question: Stack vs Queue for Generation
**Stack (used)** = Depth-First Search → Creates long corridors, unique paths, tortuous mazes
**Queue** = Breadth-First Search → Creates many branches, shorter segments, grid-like mazes

Stack is better for challenging "proper" mazes.


## Running the Program
```bash
python maze.py
```
