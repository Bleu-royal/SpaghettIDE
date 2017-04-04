import sys
import os

from PySide.QtGui import *
from PySide.QtCore import *

from themes import themes
import gui.style.style as style

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class StatusBar(QStatusBar):
    def __init__(self, width=None):
        QStatusBar.__init__(self)
        if width is not None:
            self.setFixedWidth(width)

        self.setFixedHeight(30)
        self.setSizeGripEnabled(False)

        self.maj_style()

    def maj_style(self):
        status_color = themes.get_color_from_theme("statusbar")
        self.setStyleSheet("QStatusBar {background: " + themes.get_rgb(status_color["BACKGROUND"]) + ";""color: " +
                           themes.get_rgb(status_color["TEXT"]) + ";}")
