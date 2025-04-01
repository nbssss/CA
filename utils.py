import os

import numpy as np
from PIL import Image
from simulation import TREE, WATER, ASH, FIRE

def load_image_as_grid(image_path, grid_size):
    img = Image.open(image_path).convert("RGB")     # upewniam się, że obraz jest w formacie RGB
    img = img.resize((grid_size, grid_size), Image.Resampling.NEAREST)        # skaluje obraz do rozmiaru siatki symulacji
    img_arr = np.array(img)     # przekształcam obraz w tablicę numpy, aby operować na pikselach

    grid = np.zeros((grid_size,grid_size))

    for i in range(grid_size):
        for j in range(grid_size):
            r, g, b = img_arr[i,j]         # pobieram wartości RGB dla każdego piksela

            if r < 100 and g > 100 and b < 100:     # dużo zielonego = TREE
                grid[i,j] = TREE
            elif r < 100 and g < 100 and b > 150:       # dużo niebieskiego = WATER
                grid[i,j] = WATER
            elif r > 150 and g < 100 and b < 100:
                grid[i,j] = FIRE
            else:
                grid[i,j] = ASH

    return grid

def clear_window():
    os.system('cls' if os.name == 'nt' else 'clear')
