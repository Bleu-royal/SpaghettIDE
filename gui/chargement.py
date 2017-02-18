import sys
from time import sleep

from PySide.QtGui import *
from PySide.QtCore import *

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class Loading(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setWindowTitle("Chargement...")

        file_gif = "content/intro_tpa.gif"

        size = QImage(file_gif).size()

        self.anim = QLabel()
        self.gif = QMovie(file_gif)
        self.anim.setMovie(self.gif)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.anim)
        self.resize(size)
        self.setLayout(self.layout)

        self.gif.start()
