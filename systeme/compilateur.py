import os
from PySide.QtGui import *

configuration=""#Variable temporaire à mettre dans le XML
type_projet="c"#Variable temporaire à mettre dans le XML

class GroupBoxOptions(QGroupBox):

	def __init__(self):
		super().__init__("Options de compilation")

		layout = QGridLayout()

		pipe_option = QCheckBox("-pipe option")
		layout.addWidget(pipe_option, 0, 0)

		pas_lien_option = QCheckBox("-c option")
		layout.addWidget(pas_lien_option, 0, 1)

		supp_avert_option = QCheckBox("-w option")
		layout.addWidget(supp_avert_option, 0, 2)

		supp_avert_option = QCheckBox("-W option")
		layout.addWidget(supp_avert_option, 0, 3)

		supp_avert_option = QCheckBox("-Wall option")
		layout.addWidget(supp_avert_option, 1, 0)

		supp_avert_option = QCheckBox("-Werror option")
		layout.addWidget(supp_avert_option, 1, 1)

		supp_avert_option = QCheckBox("-v option")
		layout.addWidget(supp_avert_option, 1, 2)

		self.setLayout(layout)


class ConfigCompilC(QDialog):

	def __init__(self):
		super().__init__()

		self.est_valide = False

		self.setWindowTitle("Configurateur de la compilation")

		layout = QGridLayout()

		lbl_titre = QLabel("Configurateur de la compilation")
		layout.addWidget(lbl_titre, 0, 0, 1, 2)

		#Gestion des fichiers à compiler
		lbl_fichiers_compiler = QLabel("Fichiers à compiler (séparés par des espaces) : ")
		layout.addWidget(lbl_fichiers_compiler, 1, 0)

		self.lineEdit_fichiers_compiler = QLineEdit()
		layout.addWidget(self.lineEdit_fichiers_compiler, 1, 1)

		#Gestion de l'emplacement des headers
		lbl_fichier_header = QLabel("Emplacement des fichiers headers : ")
		layout.addWidget(lbl_fichier_header, 2, 0)

		self.lineEdit_fichier_header = QLineEdit()
		layout.addWidget(self.lineEdit_fichier_header, 2, 1)

		#Gestion du nom du fichier de sortie
		lbl_fichier_sortie = QLabel("Nom du fichier de sortie : ")
		layout.addWidget(lbl_fichier_sortie, 3, 0)

		self.lineEdit_fichier_sortie = QLineEdit()
		layout.addWidget(self.lineEdit_fichier_sortie, 3, 1)

		#Gestion des options de compilation
		group_options = GroupBoxOptions()
		layout.addWidget(group_options, 4, 0, 1, 2)

		btn_valider = QPushButton("Valider")
		btn_valider.clicked.connect(self.valider)
		layout.addWidget(btn_valider, 5, 0, 1, 2)

		self.setLayout(layout)

	def valider(self):

		if self.est_configuration_valide():
			self.est_valide = True
			self.done(0)
		else:
			QMessageBox.critical(self, "La configuration n'est pas valide", "Veuillez entrer une configuration valide")


	def est_configuration_valide(self):
		return self.lineEdit_fichiers_compiler.text().strip() != "" and len(self.lineEdit_fichier_sortie.text().split()) <= 1 and len(self.lineEdit_fichier_header.text().split()) <= 1

	def get_configuration_string(self):
		
		fichiers_compiler = self.lineEdit_fichiers_compiler.text()

		fichier_header = ""
		le_fichier_header = self.lineEdit_fichier_header.text()
		if le_fichier_header.strip() != "":
			fichier_header = "-I %s"%le_fichier_header


		fichier_sortie = ""
		le_fichier_sortie = self.lineEdit_fichier_sortie.text()
		if le_fichier_sortie.strip() != "":
			fichier_sortie = "-o %s"%le_fichier_sortie
 
		return "gcc %s %s %s"%(fichiers_compiler, fichier_header, fichier_sortie)

class LineEditPath(QLineEdit):

	def __init__(self, parent):
		super().__init__()
		self.parent = parent

	def mousePressEvent(self, event):
		self.open_selection_window()

	def keyPressEvent(self, event):
		return False

	def open_selection_window(self):
		nom_fichier, filtre = QFileDialog.getOpenFileName(self, "Ouvrir", self.parent.project_path)
		self.setText(nom_fichier)


class ConfigInterpPython(QDialog):

	def __init__(self, parent):
		super().__init__()

		self.parent = parent

		self.est_valide = False

		self.setWindowTitle("Configurateur de l'interpreteur python")

		layout = QGridLayout()

		lbl_titre = QLabel("Configurateur de l'interpreteur python")
		layout.addWidget(lbl_titre, 0, 0, 1, 2)

		lbl_emplacement_interpreteur = QLabel("Emplacement de l'interpreteur python : ")
		layout.addWidget(lbl_emplacement_interpreteur, 1, 0)

		self.lineEdit_emplacement_interpreteur = LineEditPath(self.parent)
		layout.addWidget(self.lineEdit_emplacement_interpreteur, 1, 1)

		lbl_emplacement_depart = QLabel("Fichier de depart : ")
		layout.addWidget(lbl_emplacement_depart, 2, 0)

		self.lineEdit_fichier_depart = LineEditPath(self.parent)
		layout.addWidget(self.lineEdit_fichier_depart, 2, 1)

		btn_valider = QPushButton("Valider")
		btn_valider.clicked.connect(self.valider)
		layout.addWidget(btn_valider, 3, 0, 1, 2)

		self.setLayout(layout)
	def valider(self):

		if self.est_configuration_valide():
			self.est_valide = True
			self.done(0)
		else:
			QMessageBox.critical(self, "La configuration n'est pas valide", "Veuillez entrer une configuration valide")


	def est_configuration_valide(self):
		return self.lineEdit_emplacement_interpreteur.text().strip() != "" and self.lineEdit_fichier_depart.text().strip() != "" and self.parent.project_path in self.lineEdit_fichier_depart.text()

	def get_configuration_string(self):

		return "%s %s"%(self.lineEdit_emplacement_interpreteur.text(), self.lineEdit_fichier_depart.text())



def compiler(parent):
	if configuration == "":
		configuration_compilation(parent)
	print("compilation en cours avec la commande : %s"%configuration)
	# os.system(configuration)

def configuration_compilation(parent):

	global configuration # Configuration -> XML

	if type_projet == "c":
		config = ConfigCompilC()
	else:
		config = ConfigInterpPython(parent)

	config.exec()

	if config.est_valide:
		configuration = config.get_configuration_string()
