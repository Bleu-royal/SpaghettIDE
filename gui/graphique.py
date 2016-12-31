# Module relatif à l'interface graphique

import sys
import os
from PySide.QtGui import *
from PySide.QtCore import *

from lexer import *
from themes.themes import *
from language.language import *

# Importation du module relatif à la coloration lexicale et de la gestion des documents
from systeme.couleurs import *
from systeme.document import *
from systeme.parallele import *
from systeme.workplace import *

# Importation des modules du menu, des onglets et du navigateur de fichiers
from gui.menu import *
from gui.navigateur import *
from gui.onglet import *

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]

class Editeur(QTextEdit):

    tabPress = Signal()

    def __init__(self, police, taille_texte, def_functions, keywords, parent):
        """
        Hérite de QTextEdit.
        C'est une zone de texte dans laquelle on peut écrire, que l'on utilise ici pour écrire du code.

        Ici, on modifie ses paramètres en fonction du thème souhaité.
        :param police: Police d'écriture
        :type police: str
        :param couleur_fond: Couleur d'arrière plan de l'éditeur (background)
        :type couleur_fond: str
        :param couleur_texte: Couleur du texte de base
        :type couleur_texte: str
        :param taille_texte: Taille de la police (en points)
        :type taille_texte: int
        :rtype: None
        """
        super().__init__()
        self.parent = parent

        self.police = police
        self.taille_texte = taille_texte
        self.def_functions = def_functions
        self.keywords = keywords

        self.yacc_erreurs = []

        self.maj_style()

        self.append("int main ( int argc, char** argv ){\n\n\treturn 0;\n\n}")

    def keyPressEvent(self, event, complete=False):

        self.parent.defaut_info_message()  # Actualisation des infos de base dès que l'on tape sur une touche

        if event.key() == 16777220:
            print("yaccing")
            # self.yacc_erreurs = yaccing(self.toPlainText())

        if ("darwin" in sys.platform and event.nativeModifiers() == 4096) or (not "darwin" in sys.platform and event.key() == 32 and event.nativeModifiers() == 514):
            self.tabPress.emit()
            return False

        super().keyPressEvent(event)

    def maj_style(self):
        c = get_color_from_theme("textedit")

        self.setStyleSheet("QTextEdit { background-color:" + get_rgb(c["text-back-color"]) + ";"
                           + "font-family:" + self.police + ";"
                           + "color:" + get_rgb(c["text-color"]) + ";"
                           + "font-size:" + str(self.taille_texte) + "pt; }")

    def show_nb_prop(self, nb_prop):
        if nb_prop == 0:
            self.parent.info_message("empty")
        else:
            self.parent.info_message(str(nb_prop) + " proposition" + "s" * (nb_prop != 1))


class StatusBar(QStatusBar):
    def __init__(self, width=None):
        QStatusBar.__init__(self)
        if width is not None:
            self.setFixedWidth(width)
        self.setFixedHeight(30)
        self.setSizeGripEnabled(False)

        self.maj_style()

    def maj_style(self):
        status_color = get_color_from_theme("statusbar")
        self.setStyleSheet("QStatusBar {background: " + get_rgb(status_color["BACKGROUND"]) + ";""color: " +
                                     get_rgb(status_color["TEXT"]) + ";}")

class Fenetre(QWidget):
    def __init__(self, titre, workplace_path=QDir.homePath() + "/workplace/"):
        """
        Hérite de QWidget
        Class principale, dans laquelle tout est rassemblé. On appelle tout ce qui est nécessaire à la création
        de la fenêtre et au fonctionnement du programme.

        :param titre: Nom de la fenêtre
        :type titre: str
        :param workplace_path: Chemin absolu vers l'emplacement où sont placés les projets créés.
        :rtype: None
        """
        super().__init__()

        self.ecran = QDesktopWidget()
        self.setWindowTitle(titre)
        self.setGeometry(20, 50, self.ecran.screenGeometry().width() - 100, self.ecran.screenGeometry().height() - 100)
        # Taille de la fenêtre

        self.workplace_path = workplace_path

        self.project_path = ""
        self.def_functions = ""

        if "darwin" in sys.platform:
            ###########################################################################################################
            ###########################################################################################################
            self.assistance_vocale = False  # Faire en fonction d'un fichier de configuration
            ###########################################################################################################
            ###########################################################################################################

        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)  # No spacing around widgets

        # Ajout du logo pieuvre
        # self.label_img = QLabel()
        # self.pixmap_img = QPixmap("images/pieuvre.jpg")
        # self.label_img.setPixmap(self.pixmap_img)

        self.treeview = TreeView(self)

        self.codes = []
        self.highlighters = []
        self.docs = []

        self.tab_widget = TabWidget(self)

        self.splitter = QSplitter()
        self.splitter.addWidget(self.treeview)
        self.splitter.addWidget(self.tab_widget)
        self.splitter.setSizes([100, 400])
        self.splitter.setMinimumSize(self.width(), self.height() - 50)

        self.statusbar = StatusBar()
        self.infobar = StatusBar(200)

        name = ""
        if "darwin" in sys.platform:
            name = self.workplace_path.split("/")[-3]

        self.status_message("Bienvenue %s!"%name)

        # self.statusbar.addWidget(MyReadWriteIndication)
        self.menuBar = MenuBar(self)

        # Positionnement des Layouts
        if "win" in sys.platform.lower():
            self.gridLayout.addWidget(self.menuBar)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.statusbar, 1, 0)
        self.gridLayout.addWidget(self.infobar, 1, 1)
        self.setLayout(self.gridLayout)

        # if sys.platform == "linux":
        #     self.show()

        self.show()

        self.maj_style()

    def indent(self):
        idx = self.tab_widget.currentIndex()
        self.docs[idx].indent()

    def info_message(self, message, time=-1):
        if message == "empty":
            self.defaut_info_message()
        elif time == -1:
            self.infobar.showMessage(message)
        else:
            self.infobar.showMessage(message, time)

    def defaut_info_message(self):
        info = DefautInfo(self)
        info.start()

    def status_message(self, message, time=2000, say=True):
        """
        Shows a message in the status bar
        :param message: Message to show
        :type message: str
        :param time: Time of printed message
        :type time: int
        :rtype: None
        """

        if say and time != -1:
            if "darwin" in sys.platform:
                if self.assistance_vocale:
                    self.blabla = SayMessage(message)
                    self.blabla.start()

            self.statusbar.showMessage(message, time)
        elif time != -1:
            self.statusbar.showMessage(message, time)
        else:
            self.statusbar.showMessage(message)

    def assist_voc(self):
        if "darwin" in sys.platform:
            if self.assistance_vocale:
                self.status_message("Assistance vocale désactivée.")
                self.assistance_vocale = False
            else:
                self.assistance_vocale = True
                self.status_message("Assistance vocale activée.")

    def new(self):
        """
        Fonction de création de nouveau fichier reliée au sous-menu "Nouveau".
        On ajoute ici un nouvel onglet à nos codes déjà ouverts ( ou on créée un premier onglet )
        qui s'appelle par défaut "Sans nom" + le numéro courant dans la liste des onglets.
        On appelle la fonction self.addCode()

        :rtype: None
        """
        if self.project_path != "":
            new_document(self)
        else:
            self.status_message("Veuillez ouvrir un projet.", 1000)

    def save(self):
        """
        Fonction de sauvegarde reliée au sous-menu "Sauvergarder".
        On sauvegarde un fichier en l'enregistrant dans un projet (ou non).
        On ouvre une QFileDialog qui affiche le navigateur du système habituel pour enregistrer des documents.

        :return:
        """

        save_document(self)

    def close_current_tab(self):
        self.tab_widget.close_current_tab()

    def deja_ouvert(self, chemin):

        return document_deja_ouvert(self, chemin)

    def open(self, chemin=False):
        """
        Fonction d'ouverture d'un fichier reliée au sous-menu "Ouvrir un fichier"
        On utilise une QFileDialog qui affiche le navigateur du système habituel pour ouvrir des documents.

        :param chemin: N'existe pas si on appelle via le menu ou le raccourcis clavier. Il est
        spécifié si il appartient au projet courant et que l'on souhaite l'ouvrir sans passer par
        la fenetre de dialogue.
        :type chemin: str
        :rtype: None
        """

        open_document(self, chemin)

    def add_code(self, title):
        """
        Fonction qui se charge d'ajouter à la liste des codes ouverts une nouvelle instance de la classe
        Editeur et de créer un nouvel onglet

        :param title: Nom du document
        :type title: str
        :rtype: None
        """
        self.codes += [Editeur("ABeeZee", 14, self.def_functions, keywords, self)]
        self.highlighters += [CodeHighLighter(self.codes[-1], self.codes[-1].document())]
        self.codes[-1].tabPress.connect(self.highlighters[-1].test)
        self.tab_widget.addTab(self.codes[-1], title)
        self.tab_widget.setCurrentIndex(len(self.codes) - 1)

    def new_project(self):
        """
        Créée un nouveau projet
        Le projet créé doit avoir un nom différent d'un projet déjà existant,
        et ne doit pas comporter de "/" dans son nom.

        :rtype: None
        """

        newproject(self)

    def open_project(self):
        """
        Ouvre un projet
        :rtype: None
        """

        open_projects(self)

    def close_project(self):
        """
        Ferme un projet
        :rtype: None
        """

        closeproject(self)

    def delete_project(self):

        deleteproject(self)

    def close_document(self):

        closedocument(self)

    def delete_document(self):

        deletedocument(self)

    def a_propos(self):
        """
        Donne des informations sur l'IDE
        :rtype: None
        """

        apropos = open("content/apropos.txt", "r").readlines()

        QMessageBox.about(self, "À propos de SpaghettIDE ", "".join(apropos))

    def help_func(self):

        self.status_message("AIDEZ MOIIIIIIII", 1000)

    # Thèmes
    def maj_style(self):

        self.setStyleSheet("QObject::pane{background: " + get_rgb(get_color_from_theme("textedit")
                                                                  ["text-back-color"]) + ";}")

        for onglets_ouverts in self.codes:
            onglets_ouverts.maj_style()

    def full_maj_style(self):
        """
        updating style --> theme
        :return:
        """
        l_objects = (self.treeview, self, self.tab_widget, self.statusbar, self.infobar)
        for o in l_objects:
            o.maj_style()

        update_token_color()
        self.token_recoloration()

    def token_recoloration(self):
        for code in self.codes:  # For each Editor instance, we change the text to recolorate it
            code.setPlainText(code.toPlainText())

    def quit_func(self):
        """
        Fonction de fermeture de l'IDE.
        On affiche une petite boîte pour demander si l'on souhaite vraiment fermer l'IDE.
        Les touches "return" et "escape" sont respectivement reliées à "Fermer" et "Annuler".

        :rtype: None
        """
        self.status_message("Fermeture...", -1, False)  # Message de status
        box = QMessageBox()
        box.setText("Voulez-vous vraiment fermer l'IDE ?")
        box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Close)
        box.setDefaultButton(QMessageBox.Close)
        box.setEscapeButton(QMessageBox.Cancel)
        val = box.exec_()

        if val == QMessageBox.Close:
            self.restart = False
            self.close()
        else:
            self.status_message("... ou pas !!", 1000, False)  # Message de status
