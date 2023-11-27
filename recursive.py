import random

# Constants for direction and movement
N, S, E, W = 1, 2, 4, 8
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE = {E: W, W: E, N: S, S: N}

def generate_maze(grid, cx, cy):
    directions = [N, S, E, W]
    random.shuffle(directions)

    for direction in directions:
        nx, ny = cx + DX[direction], cy + DY[direction]

        if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) and grid[ny][nx] == 0:
            grid[cy][cx] |= direction
            grid[ny][nx] |= OPPOSITE[direction]
            generate_maze(grid, nx, ny)

# Size of the maze grid
width = 10
height = 10

# Create a grid filled with zeros
maze_grid = [[0] * width for _ in range(height)]

# Generate the maze starting from cell (0, 0)
generate_maze(maze_grid, 0, 0)

# Printing the maze structure as ASCII art
print(" " + "_" * (width * 2 - 1))
for y in range(height):
    print("|", end="")
    for x in range(width):
        print((" " if maze_grid[y][x] & S != 0 else "_") + (" " if maze_grid[y][x] & E != 0 else "|"), end="")
    print()