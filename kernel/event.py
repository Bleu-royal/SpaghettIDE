# Module relatif à la gestion des évènements, tels que clics de souris et pression de touches

import sys
sys.path[:0] = ["../"]
from gui.graphique import *
sys.path[:0] = ["kernel"]


def keyPressEvent(self, event):

        Editeur.__init__()

        QTextEdit.keyPressEvent(self, event)

        if event.key() == 16777220:
            yaccing(self.toPlainText())

def mousePressEvent(self, event):
    """
    On créée un nouvel onglet de code lorsqu'on double-clique sur la page vide (si on a pas d'onglet déjà ouvert).

    :param event: Contient les positions x et y de l'endroit où on a cliqué. NON UTILISÉ ICI.
    :rtype: None
    """

    TabWidget.__init__()

    if len(self.parent.docs) == 0:
        self.parent.new()


def mouseDoubleClickEvent(self, event):
    """
    Lorsque l'on double-clique sur le navigateur, on ouvre soit un projet, soit un document dans un projet.

    :param event: Contient les positions x et y de l'endroit où on a cliqué. NON UTILISÉ ICI.
    :rtype: None
    """

    TreeView.__init__()

    name = self.model.fileName(self.currentIndex())
    check_file = QFileInfo(self.fenetre.workplace_path + name + "/.conf")
    if QDir(self.fenetre.workplace_path + name).exists() and check_file.exists() and check_file.isFile():
        self.fenetre.project_path = self.fenetre.workplace_path + name
        self.fenetre.statusbar.showMessage("Le projet " + name + " a bien été ouvert.", 2000)
    else:
        self.open()


def keyPressEvent(self, event):
    """
    Bind de la touche entrée.
    Lorsque l'on sélectionne un document et que l'on appuie sur entrée, on ouvre le document ou le projet sélectionné.

    Contient les positions x et y de l'endroit où on a cliqué. NON UTILISÉ ICI.
    :rtype: None
    """

    TreeView.__init__()

    if event.key() == 16777220:  # Référence de la touche "entrée"
        name = self.model.fileName(self.currentIndex())
        if QDir(self.fenetre.workplace_path + name).exists():
            self.fenetre.project_path = self.fenetre.workplace_path + name
            self.fenetre.statusbar.showMessage("Le projet " + name + " a bien été ouvert.", 2000)
        else:
            self.open()
    else:
        QTreeView.keyPressEvent(self, event)