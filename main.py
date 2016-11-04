import sys
from gui.graphique import *
from kernel.bind import bind

app = QApplication(sys.argv)
"""
opts = Options("Cthulhu (Bleu Royal)")

def creer_fenetre():
    folder_path = QFileDialog.getExistingDirectory(opts, 'Ouverture du projet')
    if folder_path:
        fenetre = Fenetre("Cthulhu (Bleu Royal)", folder_path)  # Creation of the main window
        bind(fenetre)  # Connection between buttons and functions
        opts.close()

opts.button.clicked.connect(creer_fenetre)"""

fenetre = Fenetre("Cthulhu (Bleu Royal)")  # Creation of the main window
bind(fenetre)  # Connection between buttons and functions

sys.exit(app.exec_())
