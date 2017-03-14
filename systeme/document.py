# Module relatif au traitement des documents (noms, extension, sauvegarde, chargement...)

from PySide.QtGui import *
from PySide.QtCore import *
import sys
import threading
import json
import kernel.variables as var

from systeme.workplace import *

import gui.style.style as style

class SearchDialog(QDialog):

    searchEvent = Signal(QWidget, str, bool, bool)

    def __init__(self, parent):
        """
        Creates a small window with a line to enter a word or an expression that you want to find if it exists in your
        code tab.
        It uses a signal "searchEvent" that is connected to a function not related with this class which will do the
        searching operation.

        :param parent: Object parent which is calling the function (Fenetre)
        :type parent: Fenetre
        :rtype: None
        """
        super().__init__(parent)

        self.parent = parent

        self.layout = QVBoxLayout()

        self.line_edit = QLineEdit()
        self.case_sensitive_checkbox = QCheckBox(text="Case sensitive")
        self.case_sensitive_checkbox.setChecked(True)
        self.prev_button = QPushButton(text="Précédent")
        self.next_button = QPushButton(text="Suivant")

        self.setStyleSheet(style.get("buttons", "window", "check_box", "line_edit"))

        self.prev_button.clicked.connect(self.research_prev)
        self.next_button.clicked.connect(self.research_next)

        self.button_layout = QHBoxLayout()

        self.button_layout.addWidget(self.prev_button)
        self.button_layout.addWidget(self.next_button)

        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.case_sensitive_checkbox)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    def research(self, prev=False):

        text = self.line_edit.text()
        if text.strip() != "":
            self.searchEvent.emit(self.parent, text, prev, self.case_sensitive_checkbox.isChecked())
            self.parent.show_nb_found(text)

    def research_next(self):
        self.research()

    def research_prev(self):
        self.research(True)

    def keyPressEvent(self, event):

        if event.key() == 16777216:  # if esc key pressed then quit
            self.done(0)
            self.parent.defaut_info_message()
        elif ("darwin" in sys.platform and event.nativeModifiers() == 512) or (not "darwin" in sys.platform and event.key() == 16777220 and event.nativeModifiers() == 514):  # if shift+enter pressed then search result backward
            self.research_prev()

        elif event.key() == 16777220:  # if enter is pressed then search result
            self.research_next()


class Document:
    def __init__(self, parent, text_edit, chemin_enregistrement, ouverture=False):  # Sauvegarde des variables dans la classe

        self.parent = parent
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
        # ICI

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

        line_number = self.text_edit.textCursor().blockNumber()  # Obtention du numero de la ligne

        text = self.text_edit.toPlainText()
        lines = text.split("\n")

        indent_level = 0

        for i, line in enumerate(lines):
            indent_level -= "}" in line  # Si il y'a un accolade fermante on retire un niveau d'indentation
            if lines[i].strip() != "": lines[i] = "\t" * indent_level + self.remove_tabs(line)  # On ajoute indent_level
            # fois un '\t' au debut de la ligne
            indent_level += "{" in line  # Si il y'a un accolade ouvrante on ajoute un niveau d'indentation

        self.text_edit.setPlainText("\n".join(lines))

        for i in range(line_number):  # On remet le cursor au bon endroit
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
    parent.defaut_info_message()
    parent.add_code(new, True)
    parent.docs += [Document(parent, parent.codes[-1], "")]
    parent.tab_widget.setCurrentIndex(len(parent.codes) - 1)


def save_document(parent):
    if parent.project_path != "":
        idx = parent.tab_widget.currentIndex()
        if idx != -1:
            if parent.docs[idx].chemin_enregistrement == "":
                chemin = \
                    QFileDialog.getSaveFileName(parent, 'Sauvegarder un fichier', parent.project_path, var.file_by_language[parent.project_type])[0]
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

def open_document(parent, chemin, secu=False):

    if parent.project_path != "":
        if not chemin:
            chemin = QFileDialog.getOpenFileName(parent, 'Ouvrir un fichier', parent.project_path, var.file_by_language[parent.project_type])[0]
        if chemin != "" and parent.project_path in chemin:
            if not parent.deja_ouvert(chemin):
                title = chemin.split("/")[-1]
                parent.add_code(title)
                parent.status_message("Ouverture de "+title, 2000)  # Message de status
                parent.docs += [Document(parent, parent.codes[-1], chemin, True)]
                
                parent.highlighters[-1].first_launch = False
                parent.highlighters[-1].cache_name = parent.docs[-1].chemin_enregistrement.replace("/", "_")
                parent.codes[-1].highlight_by_block()

                parent.tab_widget.setCurrentIndex(len(parent.codes) - 1)
                parent.defaut_info_message()
            else:
                idx = 0
                for i in range(len(parent.docs)):
                    if parent.docs[i].chemin_enregistrement == chemin:
                        idx = i
                        break
                parent.tab_widget.setCurrentIndex(idx)
        else:
            # parent.status_message("Impossible d'ouvrir ce document car il ne fait pas partie du projet courant.", 2000)
            if not secu:
                open_project_and_document(parent, chemin)
    else:
        if not secu  and chemin:
            open_project_and_document(parent, chemin)
        # parent.status_message("Aucun projet ouvert, veuillez ouvrir ou créer un projet.", 2000)

def open_project_and_document(parent, chemin):
        parent.docs = []
        parent.highlighters = []
        parent.codes = []
        parent.tab_widget.clear()

        path = chemin.replace(parent.workplace_path, "").split("/")[0]
        open_project(parent.treeview, path)
        # open_document(parent, chemin)
        parent.sig_progress_termine.connect(lambda e: open_doc_from_sig(e, parent, chemin))


def open_doc_from_sig(e, parent, chemin):
    if e:
        print("-----", chemin)
        open_document(parent, chemin, True)


def closedocument(parent):
    pass


def deletedocument(parent):
    pass


def find_dialog(parent):
    """
    Run a little window to enter text that you want to find in your code

    :param parent: Object parent which is calling the function (Fenetre)
    :rtype: None
    """
    idx = parent.tab_widget.currentIndex()
    if idx != -1:
        dial = SearchDialog(parent)
        dial.searchEvent.connect(find)
        dial.exec()


def find(parent, text, back, case, already_go_to_top=False):
    """
    Finds if it exists a word or an expression in a tab which contains code.

    :param parent: Object parent which is calling the function (Fenetre)
    :type parent: Fenetre
    :param text: text you wanna find
    :type text: str
    :param back: Find backwards or forwards
    :type back: bool
    :param case:  Case sensitive
    :type case: bool
    :return:
    """

    idx = parent.tab_widget.currentIndex()

    flags = False
    if back:
        flags = QTextDocument.FindBackward
    if case:
        if flags:
            flags |= QTextDocument.FindCaseSensitively
        else:
            flags = QTextDocument.FindCaseSensitively

    res = parent.codes[idx].find(text, flags)
    if not res and back and not already_go_to_top:
        parent.codes[idx].moveCursor(QTextCursor.End)
        find(parent, text, back, case, already_go_to_top=True)
    elif not res and not back and not already_go_to_top:
        parent.codes[idx].moveCursor(QTextCursor.Start)
        find(parent, text, back, case, already_go_to_top=True)
