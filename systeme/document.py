# Module relatif au traitement des documents (noms, extension, sauvegarde, chargement...)

from PySide.QtGui import *
from PySide.QtCore import *

class SearchDialog(QDialog):

    searchEvent = Signal(QWidget, str, bool, bool)

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.layout = QVBoxLayout()

        self.line_edit = QLineEdit()
        self.case_sensitive_checkbox = QCheckBox(text="Case sensitive")
        self.prev_button = QPushButton(text="Précédent")
        self.next_button = QPushButton(text="Suivant")

        self.prev_button.clicked.connect(self.research_prev)
        self.next_button.clicked.connect(self.research_next)

        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.case_sensitive_checkbox)

        self.layout.addWidget(self.prev_button)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)

    def research(self, prev=False):

        text = self.line_edit.text()

        if text.strip() != "":
            self.searchEvent.emit(self.parent, text, prev, self.case_sensitive_checkbox.isChecked())

    def research_next(self):
        self.research()

    def research_prev(self):
        self.research(True)



class Document:
    def __init__(self, text_edit, chemin_enregistrement, ouverture=False):  # Sauvegarde des variables dans la classe

        self.text_edit = text_edit  # Objet QTextEdit
        self.chemin_enregistrement = chemin_enregistrement
        self.nom = self.chemin_enregistrement.split("/")[-1]  # Recupération du nom du fichier
        self.extension = self.nom.split(".")[-1]  # Recupération de l'extension du fichier

        if ouverture:
            self.ouverture_document()

    def get_nb_lignes(self):
        # Obtention du nombre de lignes presentes dans le QTextEdit
        return self.text_edit.document().lineCount()

    def ouverture_document(self):
        fichier = open(self.chemin_enregistrement, "r")
        code = fichier.read()  # lecture du fichier
        fichier.close()
        self.text_edit.setPlainText(code)

    def sauvegarde_document(self, path=False):
        if not path:
            fichier = open(self.chemin_enregistrement, "w")
        else:
            fichier = open(path, "w")
        fichier.write(self.text_edit.toPlainText())  # Ecriture du fichier.
        fichier.close()

    def set_chemin_enregistrement(self, value):
        self.chemin_enregistrement = value
        self.nom = self.chemin_enregistrement.split("/")[-1]
        self.extension = self.nom.split(".")[-1]

    def indent(self):

        line_number = self.text_edit.textCursor().blockNumber() #Obtention du numero de la ligne

        text = self.text_edit.toPlainText()
        lines = text.split("\n")

        indent_level = 0

        for i,line in enumerate(lines): 
            indent_level -= "}" in line #Si il y'a un accolade fermante on retire un niveau d'indentation
            if lines[i].strip() != "" : lines[i] = "\t" * indent_level + self.remove_tabs(line) # On ajout indent_level fois un '\t' au debut de la ligne 
            indent_level += "{" in line #Si il y'a un accolade ouvrante on ajoute un niveau d'indentation

        self.text_edit.setPlainText("\n".join(lines))

        for i in range(line_number):    #On remet le cursor au bon endroit
            self.text_edit.moveCursor(QTextCursor.Down)
            self.text_edit.moveCursor(QTextCursor.EndOfLine)

    def remove_tabs(self, text):
        idx = 0
        while text[idx] == "\t" and idx in range(len(text)):
            idx += 1
        return text[idx:]

def new_document(parent):
    new = "Sans nom " + str(len(parent.docs) + 1)
    parent.status_message(("Nouveau fichier " + new), 2000)
    parent.add_code(new)
    parent.docs += [Document(parent.codes[-1], "")]
    parent.tab_widget.setCurrentIndex(len(parent.codes) - 1)


def save_document(parent):
    if parent.project_path != "":
        idx = parent.tab_widget.currentIndex()
        if idx != -1:
            if parent.docs[idx].chemin_enregistrement == "":
                chemin = \
                    QFileDialog.getSaveFileName(parent, 'Sauvegarder un fichier', parent.project_path,
                                                "Fichier C (*.c) ;; Fichier H (*.h)")[0]
                if chemin != "" and parent.project_path in chemin:
                    parent.docs[idx].set_chemin_enregistrement(chemin)
                    parent.docs[idx].sauvegarde_document(chemin)
                    parent.tab_widget.setTabText(idx, parent.docs[idx].nom)

                    parent.status_message(parent.docs[idx].nom+" a bien été sauvegardé.", 2000)
                    # Message de statut
                elif parent.project_path in chemin:
                    QMessageBox.critical(parent, "Impossible de sauvegarder ce document",
                                         "Ce document ne fait pas partie du projet courant")
            else:
                parent.docs[idx].sauvegarde_document()
                parent.status_message(parent.docs[idx].nom+" a bien été sauvegardé.", 2000)

    else:
        QMessageBox.critical(parent, "Aucun projet ouvert", "Veuillez ouvrir ou créer un projet")


def document_deja_ouvert(parent, chemin):

    for doc in parent.docs:
        if doc.chemin_enregistrement == chemin:
            return True

    return False


def open_document(parent, chemin):

    if parent.project_path != "":
        if not chemin:
            chemin = QFileDialog.getOpenFileName(parent, 'Ouvrir un fichier', parent.project_path,
                                                 "Fichier C (*.c) ;; Fichier H (*.h)")[0]
        if parent.project_path in chemin:
            # print("ici")
            pass
        if chemin != "" and parent.project_path in chemin:
            if not parent.deja_ouvert(chemin):
                title = chemin.split("/")[-1]
                parent.add_code(title)
                parent.status_message("Ouverture de "+title, 2000)  # Message de status
                parent.docs += [Document(parent.codes[-1], chemin, True)]
                parent.tab_widget.setCurrentIndex(len(parent.codes) - 1)
            else:
                parent.status_message("Impossible d'ouvrir ce document car il est déjà ouvert.", 2000)
        else:
            parent.status_message("Impossible d'ouvrir ce document car il ne fait pas partie "
                                         "du projet courant.", 2000)
    else:
        parent.status_message("Aucun projet ouvert, veuillez ouvrir ou créer un projet.", 2000)


def closedocument(parent):
    pass


def deletedocument(parent):
    pass

def find_dialog(parent):
    idx = parent.tab_widget.currentIndex()
    if idx != -1:
        dial = SearchDialog(parent)
        dial.searchEvent.connect(find)
        dial.exec()

def find(parent, text, back, case):

    idx = parent.tab_widget.currentIndex()

    flags = False
    if back:
        flags = QTextDocument.FindBackward
    if case:
        if flags:
            flags |= QTextDocument.FindCaseSensitively
        else:
            flags = QTextDocument.FindCaseSensitively

    parent.codes[idx].find(text, flags)


