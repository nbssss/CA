import numpy as np
from utils import load_image_as_grid
from const import GRID_SIZE, TREE, FIRE, ASH, WATER

class Simulation:
    def __init__(self):
        self.grid = np.full((GRID_SIZE, GRID_SIZE), np.nan)

    def load_grid_from_image(self, image_path):
        self.grid = load_image_as_grid(image_path, GRID_SIZE)

    def start_fire(self):
        tree_positions = np.argwhere(self.grid == TREE)     # znajduje wszystkie pozycje drzew

        if len(tree_positions) > 0:     # jeżeli w obrazie występuja drzewa
            random_index = np.random.choice(len(tree_positions))
            y, x = tree_positions[random_index]
            self.grid[y,x] = FIRE

    def evolve(self, frameNum, img):
        how_many_neighbours = np.zeros((GRID_SIZE, GRID_SIZE))

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                how_many_neighbours[i, j] = self._count_neighbours_on_fire(i, j)

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i, j] == FIRE:
                    self.grid[i, j] = ASH
                elif self.grid[i, j] == TREE and how_many_neighbours[i, j] >= 1:
                    self.grid[i, j] = FIRE

        img.set_data(self.grid)
        return img

    def _count_neighbours_on_fire(self, y, x):
        how_many = 0

        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE and self.grid[i,j] == FIRE:
                    how_many += 1

        if self.grid[y,x] == FIRE:
            how_many -= 1

        return how_many

    def reset(self):
        self.grid = np.full((GRID_SIZE, GRID_SIZE), np.nan)

