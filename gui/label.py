import sys
from PySide.QtGui import *
from PySide.QtCore import *
import gui.style.style as style
sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class Label(QLabel):

    def __init__(self, parent, enter_message=None):
        QLabel.__init__(self)

        self.parent = parent

        self.message = enter_message

    def enterEvent(self, event):
        if self.message is not None:
            self.parent.status_message(self.message, 500)
            self.parent.setCursor(Qt.ForbiddenCursor)

    def leaveEvent(self, event):
        if self.message is not None:
            self.parent.setCursor(Qt.ArrowCursor)
