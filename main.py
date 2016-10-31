import sys
from gui.graphique import *
from kernel.bind import bind

app = QApplication(sys.argv)
fenetre = Fenetre("IDE de la mort qui tue (Bleu Royal)")  # Creation of the main window

bind(fenetre)  # Connection between buttons and functions

sys.exit(app.exec_())
