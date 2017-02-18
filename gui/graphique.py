# Module relatif à l'interface graphique

import sys
import os
from PySide.QtGui import *
from PySide.QtCore import *
# from time import time

from lexer import *
import lexerAR as AR
from themes.themes import *
import gui.style.style as style
from language.language import *

from systeme.workplace import *
# Importation du module relatif à la coloration lexicale et de la gestion des documents
from systeme.couleurs import *
from systeme.document import *
from systeme.parallele import *

# Importation des modules du menu, des onglets, du navigateur de fichiers, de l'éditeur
# de la barre de statut, des boutons et de l'inspecteur
from gui.menu import *
from gui.navigateur import *
from gui.onglet import *
from gui.editeur import *
from gui.statusbar import *
from gui.bouton import Bouton
from gui.label import Label
from gui.inspecteur import *

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


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
        self.setGeometry(20, 50, self.ecran.screenGeometry().width() - 100,
                         self.ecran.screenGeometry().height() - 100)
        # Taille de la fenêtre

        self.workplace_path = workplace_path

        self.project_path = ""
        self.def_functions = ""
        self.snippets = self.get_snippets()

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

        self.cheminee = Label(self, "Aie ! Ça brule !!")
        self.cheminee.setFixedHeight(1)

        self.inspecteur = Inspecteur(self)

        # Les boutons
        self.bouton_analyse = Bouton("Analyse", self.pre_analyse)
        self.bouton_change = Bouton("Navigateur", self.change_affichage)

        self.boutons = QSplitter()
        self.boutons.addWidget(self.bouton_change)
        self.boutons.addWidget(self.bouton_analyse)
        self.boutons.setOrientation(Qt.Horizontal)
        self.boutons.setChildrenCollapsible(False)
        self.boutons.setHandleWidth(1)
        self.boutons.setFixedWidth(100)

        # Le QSplitter contenant le QTreeView et le QPushButton
        self.split_gauche = QSplitter()
        self.split_gauche.addWidget(self.cheminee)
        self.split_gauche.addWidget(self.inspecteur)
        self.split_gauche.addWidget(self.treeview)
        self.split_gauche.addWidget(self.boutons)
        self.split_gauche.setOrientation(Qt.Vertical)
        self.split_gauche.setChildrenCollapsible(False)
        self.split_gauche.setHandleWidth(1)

        # Le QSplitter contenant le QTabWidget et le QSplitter (cf. ci-dessus)
        self.splitter = QSplitter()
        self.splitter.addWidget(self.split_gauche)
        self.splitter.addWidget(self.tab_widget)
        self.splitter.setSizes([100, 400])
        self.splitter.setMinimumSize(self.width(), self.height() - 50)

        # Les barres de statut
        self.statusbar = StatusBar()
        self.infobar = StatusBar(200)

        # La barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet(style.get("progress_bar"))

        name = ""
        if "darwin" in sys.platform:
            name = os.environ["USER"]

        self.status_message("Bienvenue %s!" % name)

        # self.statusbar.addWidget(MyReadWriteIndication)
        self.menuBar = MenuBar(self)

        # Positionnement des Layouts

        y = 0

        if "win" in sys.platform.lower():
            self.gridLayout.addWidget(self.menuBar, y, 0)
            y += 1

        self.gridLayout.addWidget(self.splitter, y+1, 0, 1, 2)
        self.gridLayout.addWidget(self.statusbar, y+2, 0)
        self.gridLayout.addWidget(self.infobar, y+2, 1)
        self.setLayout(self.gridLayout)

        # if sys.platform == "linux":
        #     self.show()

        self.show()

        self.maj_style()

    def change_affichage(self):
        """
        Change the widget displayed at the left

        0: Treeview
        1: Inspector of elements
        """
        if self.get_idx() == -1:
            self.status_message("Veuillez ouvrir un document.")
        else:
            widgets = ["Navigateur", "Inspecteur"]
            actual = self.bouton_change.text()
            self.bouton_change.setText(widgets[(widgets.index(actual) + 1) % len(widgets)])
            self.status_message(self.bouton_change.text() + " est maintenant affiché à la place de " + actual)

            if actual == widgets[0]:
                self.inspecteur.setMaximumHeight(self.ecran.screenGeometry().height())
                self.inspecteur.load()
                self.treeview.setMaximumHeight(1)
            elif actual == widgets[1]:
                self.treeview.setMaximumHeight(self.ecran.screenGeometry().height())
                self.inspecteur.setMaximumHeight(1)

    def comment_selection(self):
        idx = self.tab_widget.currentIndex()
        if idx != -1: self.codes[idx].comment_selection()

    def find(self):
        find_dialog(self)

    def get_snippets(self):

        try:
            fichier = open("snippets.json", "r")
            res = json.loads(fichier.read())
            fichier.close()
        except:
            res = []

        return res

    def get_idx(self):
        return self.tab_widget.currentIndex()

    def duplicate(self):
        if self.get_idx() != -1: self.codes[self.get_idx()].duplicate()

    def select_current_word(self):
        if self.get_idx() != -1: self.codes[self.get_idx()].select_current_word()

    def select_current_line(self):
        if self.get_idx() != -1: self.codes[self.get_idx()].select_current_line()

    def indent(self):
        if self.get_idx() != -1: self.docs[self.get_idx()].indent()

    def show_progress_bar(self):
        self.infobar.clearMessage()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.infobar.addWidget(self.progress_bar)
        self.progress_bar.show()

    def hide_progress_bar(self):
        self.progress_bar.setValue(100)
        self.infobar.removeWidget(self.progress_bar)

    # Messages in status bars
    def info_message(self, message, time=-1):
        self.infobar.clearMessage()
        if message == "empty":
            self.defaut_info_message()
        elif time == -1:
            self.infobar.showMessage(message)
        else:
            self.infobar.showMessage(message, time)

    def defaut_info_message(self):

        idx = self.tab_widget.currentIndex()
        if idx in range(len(self.docs)) and len(self.docs) > 0:
            nblignes = self.docs[idx].get_nb_lignes()
            self.infobar.showMessage(str(nblignes) + " ligne%s" % ("s" * (nblignes != 1)))
        else:
            self.infobar.clearMessage()

    def show_nb_found(self, text):
        n = self.codes[self.get_idx()].toPlainText().count(text)
        self.info_message(str(n) + " occurrence%s de '%s'" % ("s" * (n != 1), text))

    def status_message(self, message, time=2000, say=True):
        """
        Shows a message in the status bar

        :param message: Message to show
        :type message: str
        :param time: Time of printed message
        :type time: int
        :rtype: None
        """
        self.statusbar.clearMessage()
        if say and time != -1:
            if "darwin" in sys.platform:
                configuration = open_xml()
                if configuration['assistance_vocale'] == 'True':
                    self.blabla = SayMessage(message)
                    self.blabla.start()
            self.statusbar.showMessage(message, time)
        elif time != -1:
            self.statusbar.showMessage(message, time)
        else:
            self.statusbar.showMessage(message)

    def assist_voc(self):
        if "darwin" in sys.platform:
            configuration = open_xml()
            if configuration['assistance_vocale'] == 'True':
                self.status_message("Assistance vocale désactivée.")
                write_xml("assistance_vocale", "False")
            else:
                write_xml("assistance_vocale", "True")
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
        # debut = time()
        open_document(self, chemin)
        # fin = time()
        # self.info_message(str(round((fin-debut), 3)), 1000)

    def add_code(self, title):
        """
        Fonction qui se charge d'ajouter à la liste des codes ouverts une nouvelle instance de la classe
        Editeur et de créer un nouvel onglet

        :param title: Nom du document
        :type title: str
        :rtype: None
        """
        self.codes += [Editeur("ABeeZee", 14, self.def_functions, list(keywords.keys()) +
                               know_functions, self, self.snippets)]
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

    # def open_project(self):
    # 	"""
    # 	Ouvre un projet
    # 	:rtype: None
    # 	"""

    # 	open_projects(self)

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

    def contact(self):

        if "darwin" in sys.platform:
            os.system("open mailto:contact@spaghettide.com")

        if "linux" in sys.platform:
            os.system("xdg-open mailto:contact@spaghettide.com")

        if "win32" in sys.platform:
            os.system("start mailto:contact@spaghettide.com")

    # Bouton analyse
    def pre_analyse(self):
        index = self.get_idx()
        if index == -1:
            self.status_message("Veuillez ouvrir un document.")
        else:
            self.codes[index].analyse()
            self.status_message("Le fichier courant a bien été analysé.")

    # Thèmes
    def maj_style(self):

        self.setStyleSheet("QObject::pane{background: " + get_rgb(get_color_from_theme("textedit")
                                                                  ["text-back-color"]) + ";}")
        self.inspecteur.setStyleSheet("background: " + get_rgb(get_color_from_theme("treeview")
                                                                  ["BACKGROUND"]) + ";")

        for onglets_ouverts in self.codes:
            onglets_ouverts.maj_style()

    def help_func(self):

        if "darwin" in sys.platform:
            os.system("open https://doc.qt.io/")

        if "linux" in sys.platform:
            os.system("xdg-open https://doc.qt.io/")

        if "win32" in sys.platform:
            os.system("start https://doc.qt.io/")

    def site(self):

        if "darwin" in sys.platform:
            os.system("open https://www.spaghettide.com")

        if "linux" in sys.platform:
            os.system("xdg-open https://www.spaghettide.com")

        if "win32" in sys.platform:
            os.system("start https://www.spaghettide.com")

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

    def show_cheminee(self):
        """
        Shows or hides the cheminey
        :return:
        """
        if self.cheminee.height() == 1:
            self.fire = QMovie("content/fireplace.gif")
            self.cheminee.setMovie(self.fire)
            self.cheminee.setFixedHeight(260)
            self.fire.start()
            self.status_message("C'est un bon feu. Vous pouvez vous réchauffer les mains !")
        else:
            self.cheminee.setFixedHeight(1)
            self.fire.stop()
            self.cheminee.clear()
            self.status_message("Vous allez attraper froid sans la cheminée !")

    def token_recoloration(self):
        for highlighter in self.highlighters:  # For each Editor instance, we change the text to recolorate it
            highlighter.rehighlight()

    def fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def quit_func(self):
        """
        Fonction de fermeture de l'IDE.
        On affiche une petite boîte pour demander si l'on souhaite vraiment fermer l'IDE.
        Les touches "return" et "escape" sont respectivement reliées à "Fermer" et "Annuler".

        :rtype: None
        """
        self.status_message("Fermeture...", -1, False)  # Message de statut
        box = QMessageBox()
        box.setText("Voulez-vous vraiment fermer l'IDE ?")
        box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Close)
        box.setDefaultButton(QMessageBox.Close)
        box.setEscapeButton(QMessageBox.Cancel)
        box.setStyleSheet(style.get("buttons", "window"))
        val = box.exec_()

        if val == QMessageBox.Close:
            self.restart = False
            self.close()
        else:
            self.status_message("... ou pas !!", 1000, False)  # Message de statut
