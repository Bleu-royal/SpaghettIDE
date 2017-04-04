import sys

from PySide.QtGui import *
from PySide.QtCore import *

from language.language import get_text
sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class Loading(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setWindowTitle(get_text("charging"))

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
