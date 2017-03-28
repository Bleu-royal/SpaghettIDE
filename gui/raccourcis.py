import sys
from PySide.QtCore import *
from PySide.QtGui import *
from language.language import get_tmenu


class Raccourcis(QDialog):
	def __init__(self, parent, titre):
		QDialog.__init__(self)
		
		self.setWindowTitle(titre)
		self.setGeometry(20, 50, 500, 500)
		
		self.tab_widget = QTabWidget()
		self.tab_widget.addTab(MenuFichier(parent), "Fichier")
		
		# self.tab_widget.addTab(MenuEdition(), "Edition")
		# self.tab_widget.addTab(MenuProjet(), "Projet")
		
		self.bouton_valider = QPushButton("Valider")
		self.bouton_valider.clicked.connect(self.valider)
		
		self.layout = QVBoxLayout()
		self.layout.addWidget(self.tab_widget)
		
		self.setLayout(self.layout)
	
	def recup_valeur(self, clef_raccourci):
		"""Renvoie la valeur correspondant à la clef du raccourci voulu"""
		pass
	
	def valider(self):
		"""Fonction correspondant au bouton valider pour enregistrer tous les
		changements."""
		val_menu_fic = self.tab_widget.widget(0)  # Retourne MenuFichier
		
		for element in val_menu_fic.liste_fonctions:
			val = element.raccourci.text()  # Nouveau raccourci
			if val != "":
				clef = element.label.text()  # Ecrire json


class MenuFichier(QWidget):
	def __init__(self, parent):
		QWidget.__init__(self)
		
		new_fichier = MenuFonction("Nouveau Fichier", "Ctrl+N")  # lire json
		new_projet = MenuFonction("Nouveau Projet", "Ctrl+M")
		
		self.liste_fonctions = [new_projet, new_fichier]
		
		self.fic_layout = QVBoxLayout()
		
		for widget in self.liste_fonctions:
			self.fic_layout.addWidget(widget)
		
		self.setLayout(self.fic_layout)


class MenuFonction(QWidget):
	def __init__(self, nom_label, valeur_defaut):
		QWidget.__init__(self)
		
		self.label = QLabel(nom_label)
		self.raccourci = QLineEdit()
		self.raccourci.setPlaceholderText(valeur_defaut)
		
		self.fonction_layout = QHBoxLayout()
		
		self.fonction_layout.addWidget(self.label)
		self.fonction_layout.addWidget(self.raccourci)
		
		self.setLayout(self.fonction_layout)
