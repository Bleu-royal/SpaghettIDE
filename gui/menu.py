import sys
from PySide.QtGui import *
from PySide.QtCore import *
from systeme.workplace import *
from themes.themes import *
from language.language import *

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class MyAction(QAction):
    def __init__(self, parent, name, statut, fonction, shortcut_command=None):
        """
        Hérite de QAction.
        Crée ce qui est nécessaire pour faire un nouvel onglet dans la barre de menu, avec le nom,
        un raccourci, une fonction à exécuter.

        :param parent:  Classe qui appelle MyAction (ici Fenetre)
        :type parent: object
        :param name:  Nom à donner à l'action
        :type name: str
        :param statut:  Truc
        :type statut: str
        :param shortcut_command:  Commande de raccourci (facultative)
        :type shortcut_command: str
        :param fonction:  Fonction à exécuter
        :rtype: None
        """

        QAction.__init__(self, name, parent)  # Initialisation de l'action
        self.setMenuRole(QAction.NoRole)  # Pour que ca fonctionne sur toutes les plateformes
        self.setStatusTip(statut)
        self.setShortcut(shortcut_command)
        self.triggered.connect(fonction)


class MenuBar(QMenuBar):
    def __init__(self, parent):
        """
        Hérite de QMenuBar.
        C'est ici que la barre de menu est créée.
        On appelle la classe MyAction pour chaque élément du menu que l'on souhaite créer, puis on ajoute
        ces éléments au menu principal.

        :param parent: Parent de la classe ( qui appelle )
        :type parent: object
        :rtype: None
        """
        super().__init__(parent)
        self.master = parent

        # Nouveau Projet
        new_project_action = MyAction(parent, "&Nouveau Projet", "Nouveau projet", parent.new_project, "Ctrl+M")
        open_project_action = MyAction(parent, "&Ouvrir Projet", "Ouvrir un projet", parent.open_project, "Ctrl+L")
        exit_project_action = MyAction(parent, "&Fermer Projet", "Fermer le projet", parent.close_project, "Ctrl+K")

        # Nouveau Fichier
        new_fic_action = MyAction(parent, "&Nouveau", "Nouveau fichier", parent.new, "Ctrl+N")
        open_fic_action = MyAction(parent, "&Ouvrir", "Ouvrir un fichier", parent.open, "Ctrl+O")
        sauv_fic_action = MyAction(parent, "&Sauvegarder", "Sauvegarder le fichier courant", parent.save, "Ctrl+S")
        exit_ide_action = MyAction(parent, "&Fermer", "Fermer l'application", parent.quit_func, "Esc")

        # Menu divers
        apropos_ide_action = MyAction(parent, "&À Propos", "À propos de SpaghettIDE", parent.a_propos)
        help_ide_action = MyAction(parent, "&Aide", "Aide sur l'IDE", parent.help_func)

        # # # Menu Fichier et ses sous-menus # # #
        fichier_menu = self.addMenu("&Fichier")
        self.set_actions(fichier_menu, new_fic_action, open_fic_action, sauv_fic_action, "sep", exit_ide_action)

        # # # Menu Projet et ses sous-menus # # #
        projet_menu = self.addMenu("&Projet")
        self.set_actions(projet_menu, new_project_action, open_project_action, exit_project_action)

        # # # Menu Apparence # # #
        apparence_menu = self.addMenu("&Apparence")

        # Thèmes
        groupe_theme = QActionGroup(parent)
        theme_basic = MyAction(parent, "&Thème Basique", "Thème Basique", self.to_basic)
        theme_pimp = MyAction(parent, "&Thème Pimp", "Thème Pimp", self.to_pimp)
        theme_forest = MyAction(parent, "&Thème Forêt", "Thème Forêt", self.to_forest)
        theme_ocean = MyAction(parent, "&Thème Océan", "Thème Océan", self.to_ocean)
        theme_galaxy = MyAction(parent, "&Thème Galaxie", "Thème Galaxie", self.to_galaxy)
        theme_blackwhite = MyAction(parent, "&Thème Black & White", "Thème Black & White", self.to_blackwhite)
        # autre_theme = MyAction(parent, "&nom theme", "nom theme", self.fonction_a_relier)

        self.set_group(theme_basic, groupe_theme, apparence_menu, "basic")
        self.set_group(theme_pimp, groupe_theme, apparence_menu, "pimp")
        self.set_group(theme_forest, groupe_theme, apparence_menu, "forest")
        self.set_group(theme_ocean, groupe_theme, apparence_menu, "ocean")
        self.set_group(theme_galaxy, groupe_theme, apparence_menu, "galaxy")
        self.set_group(theme_blackwhite, groupe_theme, apparence_menu, "black_white")
        # self.set_group(autre_theme, groupe_theme, apparence_menu, "nom theme")

        apparence_menu.addSeparator()

        # Langues
        groupe_langue = QActionGroup(parent)
        fr = MyAction(parent, "&Français", "Français", self.to_fr)
        en = MyAction(parent, "&English", "English", self.to_en)

        self.set_group(fr, groupe_langue, apparence_menu, "fr")
        self.set_group(en, groupe_langue, apparence_menu, "en")

        # # # Menu SpaghettIDE # # #
        spaghettide_menu = self.addMenu("&SpaghettIDE")
        self.set_actions(spaghettide_menu, apropos_ide_action, help_ide_action)

    def set_actions(self, menu, *args):
        """
        Sets all actions to a menu

        :param menu: Menu where actions will be added (QMenuBar)
        :type menu: object
        :param args: List of actions you wanna add
        :type args: list
        :rtype: None
        """
        for a in args:
            if a == "sep":
                menu.addSeparator()
            else:
                menu.addAction(a)

    def set_group(self, action, groupe, menu, name):
        """
        Create a groupe of action (especially for themes)

        :param action: Action to add in a group
        :param groupe: Group
        :param menu: Menu where is the groupe
        :param name: Name of the theme
        """
        action.setCheckable(True)
        if name in (get_current_theme(), get_current_language()):
            action.setChecked(True)
        groupe.addAction(action)
        menu.addAction(action)

    # Themes
    def __change_theme_to(self, theme):
        if get_current_theme() != theme:
            change_theme(theme)
            self.message_redemarrer()
            self.master.maj_style()

    def to_basic(self):
        self.__change_theme_to("basic")

    def to_pimp(self):
        self.__change_theme_to("pimp")

    def to_forest(self):
        self.__change_theme_to("forest")

    def to_ocean(self):
        self.__change_theme_to("ocean")

    def to_galaxy(self):
        self.__change_theme_to("galaxy")

    def to_blackwhite(self):
        self.__change_theme_to("black_white")

    # Languages
    def to_fr(self):
        if get_current_language() != "fr":
            self.master.statusbar.showMessage("Changement en langue Française à venir.", 2000)

    def to_en(self):
        if get_current_language() != "en":
            self.master.statusbar.showMessage("English language comming soon !", 2000)

    def message_redemarrer(self):
        QMessageBox.critical(self.master, "Redémarrer", "Veuillez relancer l'application pour que le thème "
                                                        "soit actualisé.")