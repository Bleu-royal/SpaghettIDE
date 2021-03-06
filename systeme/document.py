# Module relatif au traitement des documents (noms, extension, sauvegarde, chargement...)

from PySide.QtGui import *
from PySide.QtCore import *
import sys
import threading
import json
import kernel.variables as var

from systeme import workplace
from language.language import get_text
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
        self.prev_button = QPushButton(text=get_text("prev"))
        self.next_button = QPushButton(text=get_text("suiv"))

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

        """
        Cette fonction envoie l'évènement de recherche
        :type prev: bool
        :param prev:Permet de savoir si l'on recherche dans le sens inverse
        """
        text = self.line_edit.text()
        if text.strip() != "":
            self.searchEvent.emit(self.parent, text, prev, self.case_sensitive_checkbox.isChecked())
            self.parent.show_nb_found(text)

    def research_next(self):
        """
        Appelle la fonction research
        """
        self.research()

    def research_prev(self):
        """
        Appelle la fonction research
        """
        self.research(True)

    def keyPressEvent(self, event):

        """
        Cette fonction gère les pressions sur les touches
        :type event: Event
        :param event: l'évènement
        """
        if event.key() == 16777216:  # if esc key pressed then quit
            self.done(0)
            self.parent.defaut_info_message()
        elif ("darwin" in sys.platform and event.nativeModifiers() == 512) or (not "darwin" in sys.platform and event.key() == 16777220 and event.nativeModifiers() == 514):  # if shift+enter pressed then search result backward
            self.research_prev()

        elif event.key() == 16777220:  # if enter is pressed then search result
            self.research_next()


class Document:
    def __init__(self, parent, text_edit, chemin_enregistrement, ouverture=False):  # Sauvegarde des variables dans la classe

        """

        :type parent: QWidget
        :param parent: Le parent
        :type text_edit: QTextEdit
        :param text_edit: L'editeur
        :type chemin_enregistrement: str
        :param chemin_enregistrement: Le chemin d'enregistrement du fichier
        :type ouverture: bool
        :param ouverture: True si le document doit être ouvert
        """
        self.parent = parent
        self.text_edit = text_edit  # Objet QTextEdit
        self.chemin_enregistrement = chemin_enregistrement
        self.nom = self.chemin_enregistrement.split("/")[-1]  # Recupération du nom du fichier
        self.extension = self.nom.split(".")[-1]  # Recupération de l'extension du fichier

        if ouverture:
            self.ouverture_document()

        self.set_snippets()

    def get_nb_lignes(self):
        # Obtention du nombre de lignes presentes dans le QTextEdit
        """
        retourne le nombre de lignes
        :return: le nombre de lignes
        :rtype: int
        """
        return self.text_edit.document().lineCount()

    def ouverture_document(self):
        """
        ouvre le document
        """
        fichier = open(self.chemin_enregistrement, "r")
        code = fichier.read()  # lecture du fichier
        fichier.close()
        self.text_edit.setPlainText(code)
        # ICI

    def sauvegarde_document(self, path=False):
        """
        Sauvegarde le document
        :type path: bool
        :param path: False si l'on veut prendre le chemin d'enregistrement comme path
        """
        if not path:
            fichier = open(self.chemin_enregistrement, "w")
        else:
            fichier = open(path, "w")
        fichier.write(self.text_edit.toPlainText())  # Ecriture du fichier.
        fichier.close()

    def set_chemin_enregistrement(self, value):
        """

        :type value: str
        :param value: le chemin d'enregistrement
        """
        self.chemin_enregistrement = value
        self.nom = self.chemin_enregistrement.split("/")[-1]
        self.extension = self.nom.split(".")[-1]

    def is_saved(self):

        """
        Retourne vrai si le document est sauvegardé
        :return: True si le document est sauvegardé
        :rtype: bool
        """
        if self.chemin_enregistrement == "":
            return False

        doc = open(self.chemin_enregistrement, "r")
        val = doc.read()
        doc.close()

        return val == self.text_edit.toPlainText()

    def set_snippets(self):
        """
        Ajoute les snippets
        """
        idx = self.parent.get_idx()
        code = self.parent.codes[idx]
        
        try:
            fichier = open("snippets/%s.json"%self.extension, "r")
            snippets = json.loads(fichier.read())
            fichier.close()
        except BaseException as e:
            snippets = []

        code.snippets = snippets

    def maj_ext(self):
        """
        Met à jour l'extension du document
        """
        self.extension = self.chemin_enregistrement.split(".")[-1]
        self.set_snippets()

def new_document(parent):
    """
    Créé un nouveau document
    :type parent: QWidget
    :param parent: Le parent
    """
    new = get_text("nom_new_fic") + str(len(parent.docs) + 1)
    parent.status_message((get_text("new_file") + new), 2000)
    parent.defaut_info_message()
    parent.add_code(new, True, current_ext="")
    parent.docs += [Document(parent, parent.codes[-1], "")]
    parent.tab_widget.setCurrentIndex(len(parent.codes) - 1)


def save_document(parent):
    if parent.project_path != "":
        idx = parent.tab_widget.currentIndex()
        if idx != -1:
            if parent.docs[idx].chemin_enregistrement == "":
                chemin = \
                    QFileDialog.getSaveFileName(parent, get_text("save_file"), parent.project_path, var.file_by_language[parent.project_type] + ";;" + var.txt_extentions_filedialog)[0]
                if chemin != "" and parent.project_path in chemin:
                    parent.docs[idx].set_chemin_enregistrement(chemin)
                    parent.docs[idx].sauvegarde_document(chemin)
                    parent.docs[idx].maj_ext()
                    parent.tab_widget.setTabText(idx, parent.docs[idx].nom)

                    parent.status_message(parent.docs[idx].nom+get_text("save_complete"), 2000)
                    # Message de statut


                elif parent.project_path in chemin:
                    QMessageBox.critical(parent, get_text("save_failed"), get_text("save_fail_text"))
            else:
                parent.docs[idx].sauvegarde_document()
                parent.status_message(parent.docs[idx].nom+get_text("save_complete"), 2000)

    else:
        QMessageBox.critical(parent, get_text("no_project_on"), get_text("text_please_open_project"))


def document_deja_ouvert(parent, chemin):

    for doc in parent.docs:
        if doc.chemin_enregistrement == chemin:
            return True

    return False

def open_document(parent, chemin, secu=False):
    if parent.project_path != "":
        if not chemin:
            chemin = QFileDialog.getOpenFileName(parent, get_text("ouverture_2"), parent.project_path, var.file_by_language[parent.project_type] + ";;" + var.txt_extentions_filedialog)[0]
        if chemin != "" and parent.project_path in chemin:
            if not parent.deja_ouvert(chemin):
                title = chemin.split("/")[-1]
                parent.add_code(title, current_ext=chemin.split(".")[-1])
                parent.status_message(get_text("ouverture_de")+title, 2000)  # Message de status
                parent.docs += [Document(parent, parent.codes[-1], chemin, True)]
                
                parent.highlighters[-1].first_launch = False
                parent.highlighters[-1].cache_name = parent.docs[-1].chemin_enregistrement.replace("/", "_")
                parent.codes[-1].highlight_by_block()

                parent.tab_widget.setCurrentIndex(len(parent.codes) - 1)
                parent.defaut_info_message()
            else:
                for i in range(len(parent.docs)):
                    if parent.docs[i].chemin_enregistrement == chemin:
                        parent.tab_widget.setCurrentIndex(i)
                        break
        elif chemin != "":
            if not secu:
                open_project_and_document(parent, chemin)
    else:
        if not secu  and chemin:
            open_project_and_document(parent, chemin)

def open_project_and_document(parent, chemin):
    parent.docs = []
    parent.highlighters = []
    parent.codes = []
    parent.tab_widget.clear()

    path = chemin.replace(parent.workplace_path, "").split("/")[0]
    workplace.open_project(parent.treeview, path)
    open_document(parent, chemin)

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
