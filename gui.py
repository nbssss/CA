import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.colors import ListedColormap
from PyQt6.QtWidgets import QFileDialog, QVBoxLayout, QPushButton, QWidget, QMainWindow
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas      # umieszczenie matplotlib w oknie PyQt6

from simulation import evolution, GRID_SIZE, TREE, FIRE
from utils import load_image_as_grid

class GUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fire Simulation")
        self.setGeometry(100,100,600,600)
        self.file_path = None
        self.initGUI()

    def load_image(self):
        # otwiera się okno do wyboru przez użytkownika pliku z komputera
        # _ oznacz że druga zwracana wartość nie jest potrzbna - ignorujemy ją
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose an image", "", "Obrazy (*.png *.jpg *.jpeg);;All files (*)")         # ustalam, że do wyboru sa tylko pliki graficzne
        if file_path:
            self.file_path = file_path
            self.grid = load_image_as_grid(file_path, GRID_SIZE)
            self._refresh_display()

    def _refresh_display(self):
        cmap = ListedColormap(["saddlebrown", "green", "red", "blue"])
        display_grid = np.where(np.isnan(self.grid), -1, self.grid)
        self.img = self.ax.imshow(self.grid, cmap=cmap, vmin=0, vmax=3)
        self.canvas.draw()

    def initGUI(self):
        self.startBtn = QPushButton("Start Fire")
        self.startBtn.clicked.connect(self.start_simulation)

        self.restartBtn = QPushButton("Restart")
        self.restartBtn.clicked.connect(self.reset_grid)

        self.loadBtn = QPushButton("Load an image")
        self.loadBtn.clicked.connect(self.load_image)

        layout = QVBoxLayout()

        self.fig, self.ax = plt.subplots()
        plt.xticks([])
        plt.yticks([])

        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        layout.addWidget(self.startBtn)
        layout.addWidget(self.restartBtn)
        layout.addWidget(self.loadBtn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.grid = np.full((GRID_SIZE,GRID_SIZE), np.nan)
        self._refresh_display()

    def start_simulation(self):
        tree_positions = np.argwhere(self.grid == TREE)     # znajduje wszystkie pozycje drzew

        if len(tree_positions) > 0:     # jeżeli w obrazie występuja drzewa
            random_index = np.random.choice(len(tree_positions))
            y, x = tree_positions[random_index]
            self.grid[y,x] = FIRE

        self.ani = animation.FuncAnimation(self.fig, evolution, fargs=(self.img, self.grid), frames=10, interval=150)
        self.canvas.draw()

    def reset_grid(self):
        self.grid = load_image_as_grid(self.file_path,GRID_SIZE)
        self._refresh_display()
