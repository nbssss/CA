import numpy as np
import random

GRID_SIZE = 100

# cell states
TREE = 1    # healthy tree - could be fired
FIRE = 2    # tree in fire
ASH = 0     # burned tree
WATER = 3

'''
def create_grid():
    grid = np.zeros((GRID_SIZE, GRID_SIZE))

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            temp = random.random()

            if temp < 0.5:
                grid[i, j] = TREE
            elif temp < 0.6:
                grid[i,j] = WATER
            else:
                grid[i, j] = ASH

    while True:
        y, x = np.random.randint(0, GRID_SIZE, size=2)

        if grid[y,x] == TREE:
            grid[y,x] = FIRE
            break

    return grid
'''


# [y,x] - grid position
def count_neighbours_on_fire(y, x, grid):
    how_many = 0

    for i in range(y-1, y+2):
        for j in range(x-1, x+2):
            if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE and grid[i,j] == FIRE:
                how_many += 1

    # if [y,x] cell is on fire decreasing how_many to exclude it from neighbours
    if grid[y,x] == FIRE:
        how_many -= 1

    return how_many


def evolution(frameNum, img, grid):
    how_many_neighbours = np.zeros((GRID_SIZE, GRID_SIZE))

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            how_many_neighbours[i,j] = count_neighbours_on_fire(i,j,grid)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i,j] == FIRE:
                grid[i,j] = ASH
            elif grid[i,j] == TREE and how_many_neighbours[i,j] >= 1:
                grid[i,j] = FIRE

    img.set_data(grid)
    return img
