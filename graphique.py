# Module relatif à l'interface graphique
import sys
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *
from couleurs import *

app = QApplication(sys.argv)

class Fenetre(QWidget):
    def __init__(self, titre, size=[600, 500]):
        super().__init__()
        self.setWindowTitle(titre)
        self.resize(size[0], size[1])

        self.layout = QHBoxLayout()

        self.edit = QTextEdit()
        self.layout.addWidget(self.edit)

        self.button = QPushButton("Valider")
        self.layout.addWidget(self.button)

        self.nav = QWebView()
        self.nav.load("http://www.google.fr")
        self.layout.addWidget(self.nav)

        self.setLayout(self.layout)

        self.show()

        editor = QTextEdit()
        self.highlighter = HTMLHighLighter(self.edit.document())


fenetre = Fenetre("IDE de la mort qui tue (Bleu Royal)", [400, 400])
sys.exit(app.exec_())
