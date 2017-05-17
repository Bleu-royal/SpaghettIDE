import sys
import os
import stat
from PySide.QtGui import *
from PySide.QtCore import *
from systeme import workplace
from systeme import execute
from themes import themes
from language.language import get_text, get_tmenu
import shutil
import kernel.variables as var

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]

class RenameDialog(QDialog):

    def __init__(self, name):
        super().__init__()

        self.setWindowTitle(get_text("rename_btn"))

        self.valid = False

        layout = QVBoxLayout()

        self.line_name = QLineEdit(text=name)
        layout.addWidget(self.line_name)

        btn_valider = QPushButton(text=get_text("rename_btn"))
        btn_valider.clicked.connect(self.validate)
        layout.addWidget(btn_valider)

        self.setLayout(layout)

    def validate(self):
        if self.line_name.text() != "":
            self.valid = True
            self.done(0)
        else:
            QMessageBox.critical(self, get_text("invalid_name"), get_text("invalid_name"))

class TreeView(QTreeView):
    function_declarations = Signal(tuple)

    def __init__(self, fenetre):
        """
        Hérite de QTreeView.
        Permet d'afficher le navigateur de fichiers, permettant d'ouvrir et de visualiser les documents
        d'un ou de plusieurs projets.

        :param fenetre: Fenêtre où est placée le navigateur de fichier (ici : Parent)
        :type fenetre: Fenetre
        :rtype: None
        """

        super().__init__()
        # self.img1 = QPixmap("Dragon.jpg")  # Image de lancement
        # self.ouvrir.setIcon(QIcon(self.img1))  # Image sur le bouton
        # self.ouvrir.setIconSize(QSize(self.code.width()*1.5, self.code.height()*1.5))  # Taille de l'image

        self.fenetre = fenetre

        # self.setStyleSheet("background-color: rgb(50, 50, 50); color: white")

        self.model = QFileSystemModel()        

        self.file = QFile()
        self.model.setRootPath(self.fenetre.workplace_path)
        self.setModel(self.model)

        for i in range(1, 4):
             self.hideColumn(i)
        # irmodel = QDirModel()
        # dirmodel.setHeaderData(1,Qt.Horizontal,"Folders");

        self.setHeaderHidden(True)

        self.setAnimated(True)  # Animations

        # self.filters = []
        # extentions = var.extension_by_language[self.fenetre.project_type] + var.ext_neutres
        # for ext in extentions:
        #     self.filters.append(ext)

        # self.model.setNameFilters(self.filters)

        # self.model.setNameFilterDisables(False)
        self.model.setReadOnly(False)
        self.setRootIndex(self.model.index(self.fenetre.workplace_path))

        self.customContextMenuRequested.connect(self.create_menu)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.maj_style()  # Load theme using stylesheets

        self.cacher_pas_projet()

        self.function_declarations.connect(self.load_project)

    def create_menu(self, point):
        """
        Créé le menu clic droit du navigateur de projets.
        """
        menu = QMenu(self.fenetre)

        path = self.model.filePath(self.currentIndex())
        
        project_name = path.replace(self.fenetre.workplace_path, "")
        project_name = project_name.split("/")

        if os.path.isfile(path):
            act_remove_file = QAction(get_tmenu("delete_file"), menu)
            act_remove_file.triggered.connect(self.act_remove_file_func)
            menu.addAction(act_remove_file)

            act_rename_file = QAction(get_tmenu("rename_file"), menu)
            act_rename_file.triggered.connect(self.act_rename_file_func)
            menu.addAction(act_rename_file)

        elif len(project_name)<=1:

            if not os.path.exists(path + "/" + project_name[0] + ".xml"):

                act_import = QAction(get_tmenu("import_project"), menu)
                act_import.triggered.connect(self.act_import_func)
                menu.addAction(act_import)

            else:

                act_delete = QAction(get_tmenu("delete_project"), menu)
                act_delete.triggered.connect(self.act_delete_func)
                menu.addAction(act_delete)

                act_infos = QAction(get_tmenu("info_project"), menu)
                act_infos.triggered.connect(self.act_infos_func)
                menu.addAction(act_infos)

        elif os.path.isdir(path):

            act_rm_folder = QAction(get_tmenu("rm_folder"), menu)
            act_rm_folder.triggered.connect(self.act_rm_folder_func)
            menu.addAction(act_rm_folder)

            act_rename_folder = QAction(get_tmenu("rename_folder"), menu)
            act_rename_folder.triggered.connect(self.act_rename_folder)
            menu.addAction(act_rename_folder)

        menu.popup(self.fenetre.mapToGlobal(point))

    def act_rename_file_func(self):
        name = self.model.fileName(self.currentIndex())
        path = self.model.filePath(self.currentIndex())

        rename_file_dialog = RenameDialog(name)
        rename_file_dialog.exec()

        if rename_file_dialog.valid:
            new_name = rename_file_dialog.line_name.text()
            new_path = path.replace(name, new_name)
            os.rename(path, new_path)

    def act_rename_folder(self):
        name = self.model.fileName(self.currentIndex())
        path = self.model.filePath(self.currentIndex())

        rename_folder_dialog = RenameDialog(name)
        rename_folder_dialog.exec()

        if rename_folder_dialog.valid:
            new_name = rename_folder_dialog.line_name.text()
            new_path = path.replace(name, new_name)
            os.rename(path, new_path)

    def act_rm_folder_func(self):
        path = self.model.filePath(self.currentIndex())
        shutil.rmtree(path)
    
    def act_remove_file_func(self):
        path = self.model.filePath(self.currentIndex())

        docs = self.fenetre.docs
        doc_idx = False
        for i,doc in enumerate(docs):
            if doc.chemin_enregistrement == path:
                doc_idx = i
                break

        self.fenetre.close_tab_idx(doc_idx)

        os.remove(path)

    def act_import_func(self):
        chemin = self.fenetre.workplace_path + self.model.fileName(self.currentIndex())
        if os.path.exists(chemin):
            workplace.importproject(self.fenetre, chemin)

    def act_delete_func(self):
        chemin = self.fenetre.workplace_path + self.model.fileName(self.currentIndex())
        if os.path.exists(chemin):
            workplace.deleteproject(self.fenetre, chemin)

    def act_infos_func(self):
        chemin = self.fenetre.workplace_path + self.model.fileName(self.currentIndex())
        if os.path.exists(chemin):
            workplace.infoproject(self.fenetre, chemin)

    def change_worplace(self, workplace_path):
        self.model.setRootPath(workplace_path)
        self.setRootIndex(self.model.index(workplace_path))

    def maj_style(self):
        colors = themes.get_color_from_theme("treeview")
        self.setStyleSheet("QTreeView{background: " + themes.get_rgb(colors["BACKGROUND"]) +
                           ";}""QTreeView::item{color: " + themes.get_rgb(colors["ITEMS"]) +
                           ";}""QTreeView::item:hover{color: " + themes.get_rgb(colors["ITEMSHOVER"]) + ";}")

    def cacher_pas_projet(self):
        pass

    def mouseDoubleClickEvent(self, event):
        """ Lorsque l'on double-clique sur le navigateur, on ouvre soit un projet, soit un document dans un projet.
        :param event: Contient les positions x et y de l'endroit où on a cliqué. NON UTILISÉ ICI.
        :rtype: None
        """
        workplace.open_project(self)

    def keyPressEvent(self, event):
        """
        Bind de la touche entrée.
        Lorsque l'on sélectionne un document et que l'on appuie sur entrée, on ouvre le document
        ou le projet sélectionné.

        Contient les positions x et y de l'endroit où on a cliqué. NON UTILISÉ ICI.
        :rtype: None
        """
        if event.key() == 16777220:  # Référence de la touche "entrée"
            workplace.open_project(self)
        else:
            QTreeView.keyPressEvent(self, event)

    def load_project(self, declarators):
        """
        Calls open_project() in workplace module using a thread.

        :return:
        """
        if declarators != (None, None, None):
            self.fenetre.def_functions, self.fenetre.def_structs, self.fenetre.def_vars = declarators
            self.fenetre.status_message(get_text("project_opened"))
            self.fenetre.hide_progress_bar()

    def open(self):
        """
        Ouvre un document si son extension est valide.
        Appelle la fonction parent pour ouvrir un fichier.

        :rtype: None
        """
        path = self.model.filePath(self.currentIndex())
        name = self.model.fileName(self.currentIndex())
        ext = name.split(".")[-1]

        dir_ = stat.filemode(os.stat(path).st_mode)[0] == "d"
        executable = "x" in stat.filemode(os.stat(path).st_mode)[:4]

        if ext in [i[1:] for i in var.extension_by_language[self.fenetre.project_type]] + [i[1:] for i in var.txt_extentions]:
            self.fenetre.open(path)
        elif ext in [i[1:] for i in var.imgs_extentions]:
            self.fenetre.open_img(path)
        elif ext in [i[1:] for i in var.gif_extentions]:
            self.fenetre.open_gif(path)
        elif dir_:
            pass#temp
        elif executable:
            execute.exec_(path)
        else:
            QMessageBox.critical(self.fenetre, get_text("opening_fail"), get_text("opening_fail_text"))
