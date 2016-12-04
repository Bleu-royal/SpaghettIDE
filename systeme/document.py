# Module relatif au traitement des documents (noms, extension, sauvegarde, chargement...)

import sys
sys.path[:0] = ["../"]
from gui.graphique import *
sys.path[:0] = ["systeme"]

class Document:
    def __init__(self, textEdit, chemin_enregistrement, ouverture=False):  # Sauvegarde des variables dans la classe

        self.textEdit = textEdit
        self.chemin_enregistrement = chemin_enregistrement
        self.nom = self.chemin_enregistrement.split("/")[-1]  # Recupération du nom du fichier
        self.extension = self.nom.split(".")[-1]  # Recupération de l'extension du fichier
        self.nombre_lignes = self.textEdit.document().lineCount()
        # Obtention du nombre de lignes presentes dans le QTextEdit

        if ouverture:
            self.ouverture_document()

    def ouverture_document(self):
        fichier = open(self.chemin_enregistrement, "r")
        code = fichier.read()  # lecture du fichier
        fichier.close()
        self.textEdit.setPlainText(code)

    def sauvegarde_document(self, path=False):
        if not path:
            fichier = open(self.chemin_enregistrement, "w")
        else:
            fichier = open(path, "w")
        fichier.write(self.textEdit.toPlainText())  # Ecriture du fichier.
        fichier.close()

    def set_chemin_enregistrement(self, value):
        self.chemin_enregistrement = value
        self.nom = self.chemin_enregistrement.split("/")[-1]
        self.extension = self.nom.split(".")[-1]

def close_current_tab(self):
    """
    Fonction pour fermer l'onglet courant.

    :rtype: None
    """

    TabWidget.__init__()

    if len(self.parent.codes) != 0:  # On vérifie que la liste d'onglet n'est pas vide.
        idx = self.currentIndex()

        self.removeTab(idx)

        doc = self.parent.docs[idx]
        code = self.parent.codes[idx]

        self.parent.docs.remove(doc)
        self.parent.codes.remove(code)

        self.parent.statusbar.showMessage("Fermeture de l'onglet courant.", 2000)

def open_document(self):
    """
    Ouvre un document si son extension est valide.
    Appelle la fonction parent pour ouvrir un fichier.

    :rtype: None
    """

    TreeView.__init__()
    
    path = self.model.filePath(self.currentIndex())
    name = self.model.fileName(self.currentIndex())
    ext = name.split(".")[-1]
    if ext in ("c", "h") and self.fenetre.project_path in path and self.fenetre.project_path != "":
        self.fenetre.open(path)
