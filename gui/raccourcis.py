import sys
import json
from PySide.QtCore import *
from PySide.QtGui import *
from language.language import get_tmenu
from gui import bouton


class Raccourcis(QDialog):
	""" Fenêtre des raccourcis. Logistique interface. """
	
	def __init__(self, parent, titre):
		QDialog.__init__(self)
		
		self.setWindowTitle(titre)
		self.setGeometry(20, 50, 500, 500)
		
		self.tab_widget = QTabWidget()
		
		self.tab_widget.addTab(MenuFichier(parent), "Fichier")
		
		self.tab_widget.addTab(MenuEdition(parent), "Edition")
		self.tab_widget.addTab(MenuProjet(parent), "Projet")
		
		self.bouton_valider = bouton.Bouton("Valider", self.valider)
		
		self.layout = QVBoxLayout()
		
		self.layout.addWidget(self.tab_widget)
		self.layout.addWidget(self.bouton_valider)
	
		self.setLayout(self.layout)
	
	def valider(self):
		""" Fonction correspondant au bouton valider pour enregistrer tous les
		changements. """
		
		val_menu_fic = self.tab_widget.widget(0)  # Retourne MenuFichier
		val_menu_edit = self.tab_widget.widget(1)  # Retourne MenuEdition
		val_menu_proj = self.tab_widget.widget(2)  # Retourne MenuProjet
		
		dictio = dico_utilisateur()
		
		for element in val_menu_fic.liste_fonctions:
			val = element.raccourci.text()  # Nouveau raccourci
			if val != "":  # Si il a été modifié, on doit enregistrer la nouvelle valeur dans le dico utilisateur.
				clef = element.label.text()  # Ecrire json
				
				dictio["Fichier"][clef] = val
		
		for element in val_menu_edit.liste_fonctions:
			val = element.raccourci.text()  # Nouveau raccourci
			if val != "":  # Si il a été modifié, on doit enregistrer la nouvelle valeur dans le dico utilisateur.
				clef = element.label.text()  # Ecrire json
				
				dictio["Edition"][clef] = val
		
		for element in val_menu_proj.liste_fonctions:
			val = element.raccourci.text()  # Nouveau raccourci
			if val != "":  # Si il a été modifié, on doit enregistrer la nouvelle valeur dans le dico utilisateur.
				clef = element.label.text()  # Ecrire json
				
				dictio["Projet"][clef] = val
		
		save = json.dumps(dictio, indent=2)
		
		wfi = open("gui/racc_utilisateur.json", "w")
		wfi.write(save)
		wfi.close()


class MenuFichier(QWidget):
	
	def __init__(self, parent):
		QWidget.__init__(self)
		
		self.menu = "Fichier"
		
		new_fichier = MenuFonction("Nouveau Fichier",
		                           donne_valeur_utilisateur(self.menu, "Nouveau Fichier"))
		new_projet = MenuFonction("Nouveau Projet",
		                          donne_valeur_utilisateur(self.menu, "Nouveau Projet"))
		ouvrir = MenuFonction("Ouvrir",
		                      donne_valeur_utilisateur(self.menu, "Ouvrir"))
		sauver = MenuFonction("Sauvegarder",
		                      donne_valeur_utilisateur(self.menu, "Sauvegarder"))
		fermer_onglet = MenuFonction("Fermer Onglet",
		                             donne_valeur_utilisateur(self.menu, "Fermer Onglet"))
		compiler = MenuFonction("Compiler",
		                        donne_valeur_utilisateur(self.menu, "Compiler"))
		configuration = MenuFonction("Configuration",
		                             donne_valeur_utilisateur(self.menu, "Configuration"))
		cheminee = MenuFonction("Cheminee",
		                        donne_valeur_utilisateur(self.menu, "Cheminee"))
		ecran_chargement = MenuFonction("Ecran Chargement",
		                                donne_valeur_utilisateur(self.menu, "Ecran Chargement"))
		num_lignes = MenuFonction("Num Lignes",
		                          donne_valeur_utilisateur(self.menu, "Num Lignes"))
		assistance_vocale = MenuFonction("Assistance Vocale",
		                                 donne_valeur_utilisateur(self.menu, "Assistance vocale"))
		plein_ecran = MenuFonction("Plein Ecran",
		                           donne_valeur_utilisateur(self.menu, "Plein Ecran"))
		quitter = MenuFonction("Quitter",
		                       donne_valeur_utilisateur(self.menu, "Quitter"))
		
		self.liste_fonctions = [new_projet, new_fichier, ouvrir, sauver, fermer_onglet, compiler,
		                        configuration, cheminee, ecran_chargement, num_lignes, assistance_vocale,
		                        plein_ecran, quitter]
		
		self.fic_layout = QHBoxLayout()
		
		self.layout_1 = QVBoxLayout()
		self.layout_2 = QVBoxLayout()
		
		for widget in self.liste_fonctions[:7]:
			self.layout_1.addWidget(widget)
			
		for widget in self.liste_fonctions[7:]:
			self.layout_2.addWidget(widget)
		
		self.fic_layout.addLayout(self.layout_1)
		self.fic_layout.addLayout(self.layout_2)
		
		self.setLayout(self.fic_layout)
		
		
class MenuEdition(QWidget):
	
	def __init__(self, parent):
		QWidget.__init__(self)
		
		self.menu = "Edition"
		
		ligne_courante = MenuFonction("Ligne Courante",
		                              donne_valeur_utilisateur(self.menu, "Ligne Courante"))
		mot_courant = MenuFonction("Mot Courant",
		                           donne_valeur_utilisateur(self.menu, "Mot Courant"))
		dupliquer = MenuFonction("Dupliquer",
		                         donne_valeur_utilisateur(self.menu, "Dupliquer"))
		mode_insertion = MenuFonction("Mode Insertion",
		                              donne_valeur_utilisateur(self.menu, "Mode Insertion"))
		rechercher = MenuFonction("Rechercher",
		                          donne_valeur_utilisateur(self.menu, "Rechercher"))
		indenter = MenuFonction("Indenter",
		                        donne_valeur_utilisateur(self.menu, "Indenter"))
		
		self.liste_fonctions = [ligne_courante, mot_courant, dupliquer, mode_insertion, rechercher, indenter]
		
		self.fic_layout = QVBoxLayout()
		
		for widget in self.liste_fonctions:
			self.fic_layout.addWidget(widget)
		
		self.setLayout(self.fic_layout)
		
class MenuProjet(QWidget):
	
	def __init__(self, parent):
		QWidget.__init__(self)
		
		self.menu = "Projet"
		
		importer = MenuFonction("Importer Projet",
		                        donne_valeur_utilisateur(self.menu, "Importer Projet"))
		supprimer = MenuFonction("Supprimer Projet",
		                         donne_valeur_utilisateur(self.menu, "Supprimer Projet"))
		informations = MenuFonction("Informations Projet",
		                            donne_valeur_utilisateur(self.menu, "Informations Projet"))
		cache_projet = MenuFonction("Vider Cache Projet",
		                            donne_valeur_utilisateur(self.menu, "Vider Cache Projet"))
		tous_cache = MenuFonction("Vider Tout Le Cache",
		                          donne_valeur_utilisateur(self.menu, "Vider Tous Caches"))
		
		self.liste_fonctions = [importer, supprimer, informations, cache_projet, tous_cache]
		
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
		

def dico_defaut():
	""" Fonction qui enregistre dans une variable le contenu du json de base."""
	
	dictio = open("gui/racc_defaut.json", "r")
	dico = json.load(dictio)
	dictio.close()
	
	return dico

def dico_utilisateur():
	""" Fonction qui enregistre dans une variable le contenu du json de l'utilisateur. """
	
	dictio = open("gui/racc_utilisateur.json", "r")
	dico = json.load(dictio)
	dictio.close()
	
	return dico

def donne_valeur_defaut(clef_menu, clef_voulue):
	""" Fonction qui donne la valeur de la clef voulue, qui est contenue dans le dico correspondant
	à la valeur de la clef_menu, qui est contenue dans le dico des raccourcis de base. """
	
	dico = dico_defaut()
	
	if clef_menu in dico.keys():
		if clef_voulue in dico[clef_menu].keys():
			return dico[clef_menu][clef_voulue]
	
	return ""

def donne_valeur_utilisateur(clef_menu, clef_voulue):
	""" Fonction qui donne la valeur de la clef voulue, qui est contenue dans le dico correspondant
		à la valeur de la clef_menu, qui est contenue dans le dico des raccourcis d'utilisateur. """
	
	dico = dico_utilisateur()
	
	if clef_menu in dico.keys():
		if clef_voulue in dico[clef_menu].keys():
			return dico[clef_menu][clef_voulue]
		else:
			print("Clef voulue pas valide")
	else:
		print("Clef menu pas valide")
	return ""
