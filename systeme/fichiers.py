# Module relatif à la gestion des fichiers

import sys
sys.path[:0] = ["../"]
from gui.graphique import *
sys.path[:0] = ["systeme"]

def new(self):
    """
    Fonction de création de nouveau fichier reliée au sous-menu "Nouveau".
    On ajoute ici un nouvel onglet à nos codes déjà ouverts ( ou on créée un premier onglet ) qui s'appelle par défaut "Sans nom" + le numéro courant dans la liste des onglets.
    On appelle la fonction self.addCode()

    :rtype: None
    """

    Fenetre.__init__()

    new = "Sans nom"+str(len(self.docs)+1)
    self.statusbar.showMessage(("Nouveau fichier " + new), 2000)
    self.addCode(new)
    self.docs += [Document(self.codes[-1], "")]
    self.tab_widget.setCurrentIndex(len(self.codes) - 1)

def save(self):
    """
    Fonction de sauvegarde reliée au sous-menu "Sauvergarder".
    On sauvegarde un fichier en l'enregistrant dans un projet (ou non).
    On ouvre une QFileDialog qui affiche le navigateur du système habituel pour enregistrer des documents.

    :return:
    """

    Fenetre.__init__()

    if self.project_path != "":
        idx = self.tab_widget.currentIndex()
        if idx != -1:
            if self.docs[idx].chemin_enregistrement == "":
                chemin = \
                    QFileDialog.getSaveFileName(self, 'Sauvegarder un fichier', self.project_path, "Fichier C (*.c) ;; Fichier H (*.h)")[0]
                if chemin != "" and self.project_path in chemin:
                    self.docs[idx].set_chemin_enregistrement(chemin)
                    self.docs[idx].sauvegarde_document(chemin)
                    self.tab_widget.setTabText(idx, self.docs[idx].nom)

                    self.statusbar.showMessage(self.docs[idx].nom+" a bien été sauvegardé.", 2000)  # Message de status
                else:
                    QMessageBox.critical(self, "Impossible de sauvegarder ce document", "Ce document ne fais pas partie du projet courant")
            else:
                self.docs[idx].sauvegarde_document()
    else:
        QMessageBox.critical(self, "Aucun projet ouvert", "Veuillez ouvrir ou créer un projet")

def deja_ouvert(self, chemin):

    Fenetre.__init__()

    for doc in self.docs:
        if doc.chemin_enregistrement == chemin:
            return True

    return False

def open_file(self, chemin=False):
    """
    Fonction d'ouverture d'un fichier reliée au sous-menu "Ouvrir un fichier"
    On utilise une QFileDialog qui affiche le navigateur du système habituel pour ouvrir des documents.

    :param chemin: N'existe pas si on appelle via le menu ou le raccourcis clavier. Il est spécifié si il appartient au projet courant et que l'on souhaite l'ouvrir sans passer par la fenetre de dialogue.
    :type chemin: str
    :rtype: None
    """

    Fenetre.__init__()

    if self.project_path != "":
        if not chemin:
            chemin = QFileDialog.getOpenFileName(self, 'Ouvrir un fichier', self.project_path, "Fichier C (*.c) ;; Fichier H (*.h)")[0]
        if self.project_path in chemin:
            # print("ici")
            pass
        if chemin != "" and self.project_path in chemin:
            if not self.deja_ouvert(chemin):
                title = chemin.split("/")[-1]
                self.addCode(title)
                self.statusbar.showMessage("Ouverture de "+title, 2000)  # Message de status
                self.docs += [Document(self.codes[-1], chemin, True)]
                self.tab_widget.setCurrentIndex(len(self.codes) - 1)
            else:
                self.statusbar.showMessage("Impossible d'ouvrir ce document car il est déjà ouvert.", 2000)
        else:
            self.statusbar.showMessage("Impossible d'ouvrir ce document car il ne fait pas partit du projet courrant.", 2000)
    else:
        self.statusbar.showMessage("Aucun projet ouvert, veuillez ouvrir ou créer un projet.", 2000)

def close(self):

    Fenetre.__init__()

    pass

def delete(self):

    Fenetre.__init__()
    
    pass