import sys
from PySide.QtGui import *
from PySide.QtCore import *

from xml import *
from themes import themes
from language import language
from language.language import get_tmenu, get_text

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]

configuration = open_xml("conf.xml")

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

        # # # # Projet
        new_project_action = MyAction(parent, get_tmenu("new_proj"), "Nouveau projet", parent.new_project, "Ctrl+M")
        import_project_action = MyAction(parent, get_tmenu("import_proj"), "Importer un projet", parent.import_project, "Ctrl+Shift+I")
        del_project_action = MyAction(parent, get_tmenu("supr_proj"), "Supprimer le projet", parent.delete_project, "Ctrl+Alt+S")
        info_project_action = MyAction(parent, get_tmenu("info_proj"), "Informations d'un projet", parent.infos_project, "Ctrl+Alt+I")
        # open_project_action = MyAction(parent, "&Ouvrir Projet", "Ouvrir un projet", parent.open_project, "Ctrl+P")
        # exit_project_action = MyAction(parent, "&Fermer Projet", "Fermer le projet", parent.close_project, "Ctrl+K")

        # # # # Fichier
        new_fic_action = MyAction(parent, get_tmenu("new_file"), "Nouveau fichier", parent.new, "Ctrl+N")
        open_fic_action = MyAction(parent, get_tmenu("open_file"), "Ouvrir un fichier", parent.open, "Ctrl+O")
        sauv_fic_action = MyAction(parent, get_tmenu("save_file"), "Sauvegarder le fichier courant", parent.save, "Ctrl+S")
        close_fic_action = MyAction(parent, get_tmenu("close_file"), "Fermer le fichier courant", parent.close_current_tab, "Ctrl+W")
        fullscreen_action = MyAction(parent, get_tmenu("full_screen"), "Plein Écran", parent.fullscreen, "F7")
        fullscreen_action.setCheckable(True)
        exit_ide_action = MyAction(parent, get_tmenu("exit"), "Fermer l'application", parent.quit_func, "Esc")

        # # # # Edition
        indent_action = MyAction(parent, get_tmenu("indent"), "Indentation automatique du fichier",
                                 parent.indent, "Ctrl+Alt+L")
        select_current_line_action = MyAction(parent, get_tmenu("select_line"),
                                              "Sélectionner la ligne courante", parent.select_current_line, "Ctrl+L")
        select_current_word_action = MyAction(parent, get_tmenu("select_word"), "Sélectionner le mot courant",
                                              parent.select_current_word, "Ctrl+D")
        duplicate_action = MyAction(parent, get_tmenu("duplicate"), "Dupliquer", parent.duplicate, "Ctrl+Shift+D")
        find_action = MyAction(parent, get_tmenu("find"), "Rechercher", parent.find, "Ctrl+F")
        comment_selection_action = MyAction(parent, get_tmenu("comment"), "Commenter", parent.comment_selection,
                                            "Ctrl+Shift+:")
        insert_action = MyAction(parent, get_tmenu("insert"), "insertion", parent.insert_mode, "Ctrl+I")
        insert_action.setCheckable(True)

        # # # # Menu compilation
        compiler_action = MyAction(parent, get_tmenu("comp"), "Compiler le projet", parent.compiler, "F5")
        configurer_compilation_action = MyAction(parent, get_tmenu("conf_comp"), "Configurer la compilation", parent.configuration_compilation, "Shift+F5")

        # # # # Menu divers
        apropos_ide_action = MyAction(parent, get_tmenu("about"), "À propos de SpaghettIDE", parent.a_propos)
        contact_ide_action = MyAction(parent, get_tmenu("contact"), "", parent.contact)
        site_ide_action = MyAction(parent, get_tmenu("site"), "Site", parent.site)
        help_ide_action = MyAction(parent, get_tmenu("help"), "Aide sur l'IDE", parent.help_func)
        raccourcis_action = MyAction(parent, get_tmenu("raccourcis"), "Raccourcis", parent.menu_raccourcis)

        # # # # Assistance vocale
        assist_voc_action = MyAction(parent, get_tmenu("voice"), "Assistance vocale", parent.assist_voc, "F12")
        assist_voc_action.setCheckable(True)
        if configuration['assistance_vocale'] == 'False':
            assist_voc_action.setChecked(False)
        else:
            assist_voc_action.setChecked(True)

        if "darwin" not in sys.platform:
            assist_voc_action.setDisabled(True)

        # # # # Menu Fichier et ses sous-menus # # # #
        fichier_menu = self.addMenu(get_tmenu("fichier"))
        menu_new = fichier_menu.addMenu(get_tmenu("new"))
        self.set_actions(menu_new, new_fic_action, new_project_action)
        self.set_actions(fichier_menu, open_fic_action, sauv_fic_action, close_fic_action, "sep")

        # Compilation

        compilation_menu = fichier_menu.addMenu(get_tmenu("compil"))
        self.set_actions(compilation_menu, compiler_action, configurer_compilation_action)

        # sous-menu Apparence #
        apparence_menu = fichier_menu.addMenu(get_tmenu("settings"))

        clair = apparence_menu.addMenu(get_tmenu("theme_clair"))
        fonce = apparence_menu.addMenu(get_tmenu("theme_sombre"))

        # # # # Thèmes
        groupe_theme = QActionGroup(parent)
        theme_basic = MyAction(parent, "&Basika", "Thème Basique", lambda: self.__change_theme_to("basic"))
        theme_pimp = MyAction(parent, "&Pimp", "Thème Pimp", lambda: self.__change_theme_to("pimp"))
        theme_forest = MyAction(parent, "&Forêt", "Thème Forêt", lambda: self.__change_theme_to("forest"))
        theme_ocean = MyAction(parent, "&Océan", "Thème Océan", lambda: self.__change_theme_to("ocean"))
        theme_galaxy = MyAction(parent, "&Galexio", "Thème Galaxie", lambda: self.__change_theme_to("galaxy"))
        theme_blackwhite = MyAction(parent, "&Black n White", "Thème Black n White", lambda: self.__change_theme_to("black_white"))
        theme_pastel = MyAction(parent, "&Pastel", "Thème Pastel", lambda: self.__change_theme_to("pastel"))
        theme_awesome = MyAction(parent, "&Awesome", "Thème Awesome", lambda: self.__change_theme_to("awesome"))
        # nomTheme = MyAction(parent, "&monNouveauTheme", "monNouveauTheme", lambda: self.__change_theme_to("monNouveauTheme"))

        self.set_group(theme_basic, groupe_theme, fonce, "basic")
        self.set_group(theme_pimp, groupe_theme, clair, "pimp")
        self.set_group(theme_forest, groupe_theme, fonce, "forest")
        self.set_group(theme_ocean, groupe_theme, clair, "ocean")
        self.set_group(theme_galaxy, groupe_theme, fonce, "galaxy")
        self.set_group(theme_blackwhite, groupe_theme, fonce, "black_white")
        self.set_group(theme_pastel, groupe_theme, clair, "pastel")
        self.set_group(theme_awesome, groupe_theme, fonce, "awesome")
        # self.set_group(nomTheme, groupe_theme, apparence_menu, "monNouveauTheme")

        fire_action = MyAction(parent, get_tmenu("cheminee"), "Afficher la cheminée", parent.show_cheminee, "F6")
        fire_action.setCheckable(True)

        load_action = MyAction(parent, get_tmenu("chargement"), "Afficher l'écran de chargement au démarrage", parent.show_loading, "F4")
        load_action.setCheckable(True)

        if configuration['loading'] == 'False':
            load_action.setChecked(False)
        else:
            load_action.setChecked(True)

        line_action = MyAction(parent, get_tmenu("lines"), "Numérotation des lignes", parent.show_line_column, "F2")
        line_action.setCheckable(True)
        if parent.is_show_line:
            if configuration['numerote_lines'] == 'False':
                line_action.setChecked(False)
            else:
                line_action.setChecked(True)

        self.set_actions(apparence_menu, "sep", fire_action, load_action, line_action, assist_voc_action,"sep")

        # # # #Langues
        langues = apparence_menu.addMenu(get_tmenu("lang"))
        groupe_langue = QActionGroup(parent)
        fr = MyAction(parent, "&Français", "Français", lambda: self.__change_language_to("fr"))
        en = MyAction(parent, "&English", "English", lambda: self.__change_language_to("en"))

        self.set_group(fr, groupe_langue, langues, "fr")
        self.set_group(en, groupe_langue, langues, "en")

        self.set_actions(fichier_menu, "sep", fullscreen_action, exit_ide_action)

        # # # # Menu Edition et ses sous-menus # # # #
        edition_menu = self.addMenu(get_tmenu("edit"))
        self.set_actions(edition_menu, select_current_line_action, select_current_word_action, duplicate_action,
                         insert_action, "sep", find_action, "sep", indent_action, comment_selection_action)

        # # # # Menu Projet et ses sous-menus # # # #
        projet_menu = self.addMenu(get_tmenu("proj"))
        self.set_actions(projet_menu, import_project_action, del_project_action, info_project_action)

        # # # # Menu SpaghettIDE # # # #
        spaghettide_menu = self.addMenu("&SpaghettIDE")
        self.set_actions(spaghettide_menu, apropos_ide_action, contact_ide_action, site_ide_action,
                         help_ide_action, raccourcis_action)

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
        if name in (themes.get_current_theme(), language.get_current_language()):
            action.setChecked(True)
        groupe.addAction(action)
        sous_groupe.addAction(action)

    # # # # Themes
    def __change_theme_to(self, theme):
        """
        Change le thème actuel
        :param theme: nouveau thème
        """
        if themes.get_current_theme() != theme:
            themes.change_theme(theme)
            self.master.full_maj_style()

    # # # # Languages
    def __change_language_to(self, l):
        """
        Change la langue actuelle
        :param l: nouvelle langue
        """
        if language.get_current_language() != l:
            write_xml("conf.xml", "language", l)
            self.master.status_message(get_text("chang_lang"))

