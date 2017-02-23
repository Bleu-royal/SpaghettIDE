import sys
from PySide.QtGui import *
from PySide.QtCore import *

import gui.style.style as style
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

        #### Projet
        new_project_action = MyAction(parent, "&Nouveau Projet", "Nouveau projet", parent.new_project, "Ctrl+M")
        # open_project_action = MyAction(parent, "&Ouvrir Projet", "Ouvrir un projet", parent.open_project, "Ctrl+P")
        exit_project_action = MyAction(parent, "&Fermer Projet", "Fermer le projet", parent.close_project, "Ctrl+K")

        #### Fichier
        new_fic_action = MyAction(parent, "&Nouveau", "Nouveau fichier", parent.new, "Ctrl+N")
        open_fic_action = MyAction(parent, "&Ouvrir", "Ouvrir un fichier", parent.open, "Ctrl+O")
        sauv_fic_action = MyAction(parent, "&Sauvegarder", "Sauvegarder le fichier courant", parent.save, "Ctrl+S")
        close_fic_action = MyAction(parent, "&Fermer", "Fermer le fichier courant", parent.close_current_tab, "Ctrl+W")
        fullscreen_action = MyAction(parent, "&Mode plein écran", "Plein Écran", parent.fullscreen, "F7")
        fullscreen_action.setCheckable(True)
        exit_ide_action = MyAction(parent, "&Fermer", "Fermer l'application", parent.quit_func, "Esc")
       
        #### Edition
        indent_action = MyAction(parent, "&Indenter le fichier", "Indentation automatique du fichier",
                                 parent.indent, "Ctrl+Alt+L")
        
        select_current_line_action = MyAction(parent, "&Sélectionner la ligne courante",
                                              "Sélectionner la ligne courante", parent.select_current_line, "Ctrl+L")
        
        select_current_word_action = MyAction(parent, "&Sélectionner le mot courant", "Sélectionner le mot courant",
                                              parent.select_current_word, "Ctrl+D")
        duplicate_action = MyAction(parent, "&Dupliquer", "Dupliquer", parent.duplicate, "Ctrl+Shift+D")
        
        find_action = MyAction(parent, "&Rechercher", "Rechercher", parent.find, "Ctrl+F")
        
        comment_selection_action = MyAction(parent, "&Commenter la selection", "Commenter", parent.comment_selection,
                                            "Ctrl+Shift+:")

        #### Menu divers
        apropos_ide_action = MyAction(parent, "&À Propos", "À propos de SpaghettIDE", parent.a_propos)
        contact_ide_action = MyAction(parent, "&Contact", "", parent.contact)
        site_ide_action = MyAction(parent, "&Notre site", "Site", parent.site)
        help_ide_action = MyAction(parent, "&Aide", "Aide sur l'IDE", parent.help_func)

        # Assistance vocale
        assist_voc_action = MyAction(parent, "&Assistance Vocale", "Assistance vocale", parent.assist_voc, "F12")
        assist_voc_action.setCheckable(True)
        
        configuration = open_xml()
        if configuration['assistance_vocale'] == 'False':
            assist_voc_action.setChecked(False)
        else:
            assist_voc_action.setChecked(True)

        if "darwin" not in sys.platform:
            assist_voc_action.setDisabled(True)

        # # # Menu Fichier et ses sous-menus # # #
        fichier_menu = self.addMenu("&Fichier")
        self.set_actions(fichier_menu, new_fic_action, open_fic_action, sauv_fic_action, close_fic_action, "sep",
                         assist_voc_action, "sep", fullscreen_action, exit_ide_action)

        # # # Menu Edition et ses sous-menus # # #

        edition_menu = self.addMenu("&Edition")
        self.set_actions(edition_menu, select_current_line_action, select_current_word_action, duplicate_action, "sep",
                         find_action, "sep", indent_action, comment_selection_action)

        # # # Menu Projet et ses sous-menus # # #
        projet_menu = self.addMenu("&Projet")
        self.set_actions(projet_menu, new_project_action, exit_project_action)#, open_project_action, )

        # # # Menu Apparence # # #
        apparence_menu = self.addMenu("&Apparence")

        clair = apparence_menu.addMenu("&Thème clair")
        fonce = apparence_menu.addMenu("&Thème foncé")

        # Thèmes
        groupe_theme = QActionGroup(parent)
        theme_basic = MyAction(parent, "&Thème Basique", "Thème Basique", lambda: self.__change_theme_to("basic"))
        theme_pimp = MyAction(parent, "&Thème Pimp", "Thème Pimp", lambda: self.__change_theme_to("pimp"))
        theme_forest = MyAction(parent, "&Thème Forêt", "Thème Forêt", lambda: self.__change_theme_to("forest"))
        theme_ocean = MyAction(parent, "&Thème Océan", "Thème Océan", lambda: self.__change_theme_to("ocean"))
        theme_galaxy = MyAction(parent, "&Thème Galaxie", "Thème Galaxie", lambda: self.__change_theme_to("galaxy"))
        theme_blackwhite = MyAction(parent, "&Thème Black n White", "Thème Black n White",
                                    lambda: self.__change_theme_to("black_white"))
        theme_pastel = MyAction(parent, "&Thème Pastel", "Thème Pastel", lambda: self.__change_theme_to("pastel"))
        # nomTheme = MyAction(parent, "&monNouveauTheme", "monNouveauTheme", lambda: self.__change_theme_to("monNouveauTheme"))

        self.set_group(theme_basic, groupe_theme, fonce, "basic")
        self.set_group(theme_pimp, groupe_theme, clair, "pimp")
        self.set_group(theme_forest, groupe_theme, fonce, "forest")
        self.set_group(theme_ocean, groupe_theme, clair, "ocean")
        self.set_group(theme_galaxy, groupe_theme, fonce, "galaxy")
        self.set_group(theme_blackwhite, groupe_theme, fonce, "black_white")
        self.set_group(theme_pastel, groupe_theme, clair, "pastel")
        # self.set_group(nomTheme, groupe_theme, apparence_menu, "monNouveauTheme")

        fire_action = MyAction(parent, "&Afficher la cheminée", "Afficher la cheminée", parent.show_cheminee, "F6")
        fire_action.setCheckable(True)

        line_action = MyAction(parent, "&Numérotation des lignes", "Numérotation des lignes", parent.show_line_column, "F2")
        line_action.setCheckable(True)
        if parent.is_show_line:
            line_action.setChecked(True)

        self.set_actions(apparence_menu, "sep", fire_action, line_action, "sep")

        # Langues
        langues = apparence_menu.addMenu("&Langues")
        groupe_langue = QActionGroup(parent)
        fr = MyAction(parent, "&Français", "Français", self.to_fr)
        en = MyAction(parent, "&English", "English", self.to_en)

        self.set_group(fr, groupe_langue, langues, "fr")
        self.set_group(en, groupe_langue, langues, "en")

        # # # Menu SpaghettIDE # # #
        spaghettide_menu = self.addMenu("&SpaghettIDE")
        self.set_actions(spaghettide_menu, apropos_ide_action, contact_ide_action, site_ide_action, help_ide_action)

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

    def set_group(self, action, groupe, sous_groupe, name):
        """
        Create a groupe of action (especially for themes)

        :param action: Action to add in a group
        :param groupe: Group
        :param sous_groupe: Secondary menu where will be aded the action
        :param name: Name of the theme
        """
        action.setCheckable(True)
        if name in (get_current_theme(), get_current_language()):
            action.setChecked(True)
        groupe.addAction(action)
        sous_groupe.addAction(action)

    # Themes
    def __change_theme_to(self, theme):
        """
        Change le thème actuel
        :param theme: nouveau thème
        """
        if get_current_theme() != theme:
            change_theme(theme)
            self.master.full_maj_style()

            self.master.status_message("Thème actuel : " + theme + ". La coloration lexicale sera actualisée lorsque "
                                       "vous écrirez un caractère.", 4000)

    # Languages
    def to_fr(self):
        if get_current_language() != "fr":
            self.master.status_message("Changement en langue Française à venir.")

    def to_en(self):
        if get_current_language() != "en":
            self.master.status_message("English language comming soon !")
