
import numpy as np
import random
import time
import os

GRID_SIZE = 10

# cell states
ALIVE = True
DEAD = False

# clear terminal window
def clear_window():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_grid():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            temp = random.randint(0,4)

            if temp == 0:
                grid[i, j] = ALIVE
            else:
                grid[i, j] = DEAD

    return grid

# [y,x] - grid position
def count_alive_neighbours(y, x, grid):
    how_many = 0

    for i in range(y-1, y+2):
        for j in range(x-1, x+2):
            if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE and grid[i,j] == ALIVE:
                how_many += 1

    # if [y,x] cell is alive decreasing how_much to exclude it from neighbours
    if grid[y,x] == ALIVE:
        how_many -= 1

    return how_many



# 3 neighbours = alive
# more than 3 neighbours = dead
# 2 or less neighbours = dead
def evolution(grid):
    how_many_neighbours = np.zeros((GRID_SIZE, GRID_SIZE))

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            how_many_neighbours[i,j] = count_alive_neighbours(i,j,grid)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i,j] == DEAD:
                if how_many_neighbours[i,j] == 3:
                    grid[i,j] = ALIVE
            elif grid[i,j] == ALIVE:
                if how_many_neighbours[i,j] < 2 or how_many_neighbours[i,j] > 3:
                    grid[i,j] = DEAD

def show_grid(grid):
    clear_window()

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i,j] == ALIVE:
                print(u'\u25a0', end='')    # full block
            else:
                print(u'\u25a1', end='')    # empty block

        print('\n', end='')
    print('\n', end='')

def main():
    grid = create_grid()

    while True:
        show_grid(grid)
        evolution(grid)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
