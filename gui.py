import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from PyQt6.QtWidgets import QFileDialog, QVBoxLayout, QPushButton, QWidget, QMainWindow
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from simulation import Simulation

from const import GRID_SIZE

class GUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.simulation = Simulation()
        self.setWindowTitle("Fire Simulation")
        self.setGeometry(100,100,600,600)
        self.file_path = None
        self.initGUI()

    def initGUI(self):
        self._setup_buttons()
        self._setup_canvas()
        self._setup_layout()

    def _setup_buttons(self):
        self.startBtn = QPushButton("Start Fire")
        self.startBtn.clicked.connect(self.start_simulation)

        self.restartBtn = QPushButton("Restart")
        self.restartBtn.clicked.connect(self.reset_simulation)

        self.loadBtn = QPushButton("Load an image")
        self.loadBtn.clicked.connect(self.load_image)

    def _setup_canvas(self):
        self.fig, self.ax = plt.subplots()
        plt.xticks([])
        plt.yticks([])
        self.canvas = FigureCanvas(self.fig)
        self.grid = np.full((GRID_SIZE, GRID_SIZE), np.nan)

    def _setup_layout(self):
        layout = QVBoxLayout()

        layout.addWidget(self.canvas)

        layout.addWidget(self.startBtn)
        layout.addWidget(self.restartBtn)
        layout.addWidget(self.loadBtn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose an image", "", "Obrazy (*.png *.jpg *.jpeg);;All files (*)")         # ustalam, że do wyboru sa tylko pliki graficzne
        if file_path:
            self.simulation.load_grid_from_image(file_path)
            self._refresh_display()

    def _refresh_display(self):
        cmap = ListedColormap(["saddlebrown", "green", "red", "blue"])
        display_grid = np.where(np.isnan(self.simulation.grid), -1, self.simulation.grid)
        self.img = self.ax.imshow(display_grid, cmap=cmap, vmin=0, vmax=3)
        self.canvas.draw()

    def start_simulation(self):
        self.simulation.start_fire()
        self.ani = animation.FuncAnimation(self.fig, self.simulation.evolve, fargs=(self.img, ), frames=10, interval=150)
        self.canvas.draw()

    def reset_simulation(self):
        self.simulation.reset()
        self._refresh_display()
