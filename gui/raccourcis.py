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
		
		self.tab_widget.addTab(MenuEdition(parent), "Edition")
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
		ouvrir = MenuFonction("Ouvrir", "Ctrl+O")
		sauver = MenuFonction("Sauvegarder", "Ctrl+S")
		fermer_onglet = MenuFonction("Fermer Onglet", "Ctrl+W")
		compiler = MenuFonction("Compiler", "F5")
		configuration = MenuFonction("Configuration", "Maj+F5")
		cheminee = MenuFonction("Cheminee", "F6")
		ecran_chargement = MenuFonction("Ecran Chargement", "F4")
		num_lignes = MenuFonction("Num Lignes", "F2")
		assistance_vocale = MenuFonction("Assistance Vocale", "F12")
		plein_ecran = MenuFonction("Plein Ecran", "F7")
		quitter = MenuFonction("Quitter", "Echap")
		
		self.liste_fonctions = [new_projet, new_fichier, ouvrir, sauver, fermer_onglet, compiler,
		                        configuration, cheminee, ecran_chargement, num_lignes, assistance_vocale,
		                        plein_ecran, quitter]
		
		self.fic_layout = QVBoxLayout()
		
		for widget in self.liste_fonctions:
			self.fic_layout.addWidget(widget)
		
		self.setLayout(self.fic_layout)
		
		
class MenuEdition(QWidget):
	
	def __init__(self, parent):
		QWidget.__init__(self)
		
		ligne_courante = MenuFonction("Ligne Courante", "Ctrl+L")
		mot_courant = MenuFonction("Mot Courant", "Ctrl+D")
		dupliquer = MenuFonction("Dupliquer", "Maj+Ctrl+D")
		mode_insertion = MenuFonction("Mode Insertion", "Ctrl+I")
		rechercher = MenuFonction("Rechercher", "Ctrl+F")
		indenter = MenuFonction("Indenter", "Ctrl+Alt+L")
		
		self.liste_fonctions = [ligne_courante, mot_courant, dupliquer, mode_insertion, rechercher, indenter]
		
		self.fic_layout = QVBoxLayout()
		
		for widget in self.liste_fonctions:
			self.fic_layout.addWidget(widget)
		
		self.setLayout(self.fic_layout)
		
class MenuProjet(QWidget):
	
	def __init__(self, parent):
		QWidget.__init__(self)
		
		importer = MenuFonction("Importer Projet", "Maj+Ctrl+I")
		supprimer = MenuFonction("Supprimer Projet", "Ctrl+Alt+S")
		informations = MenuFonction("Informations Projet", "Ctrl+Alt+I")
		
		self.liste_fonctions = [importer, supprimer, informations]
		
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
