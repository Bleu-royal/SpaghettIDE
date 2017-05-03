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
		
		# La fenêtre
		self.setWindowTitle(titre)
		self.setGeometry(20, 50, 500, 500)
		
		self.tab_widget = QTabWidget()
		
		self.tab_widget.addTab(MenuFichier(parent), "Fichier")
		self.tab_widget.addTab(MenuEdition(parent), "Edition")
		self.tab_widget.addTab(MenuProjet(parent), "Projet")
		
		# Les boutons
		self.bouton_valider = bouton.Bouton("Valider", self.valider)
		self.bouton_raz = bouton.Bouton("Remise à zéro", self.raz)
		
		self.layout = QVBoxLayout()
		self.layout_bouton = QHBoxLayout()
		
		self.layout.addWidget(self.tab_widget)
		self.layout_bouton.addWidget(self.bouton_valider)
		self.layout_bouton.addWidget(self.bouton_raz)
		
		self.layout.addLayout(self.layout_bouton)
		self.setLayout(self.layout)
	
	def valider(self):
		""" Fonction correspondant au bouton valider pour enregistrer tous les
		changements. """
		
		val_menu_fic = self.tab_widget.widget(0)  # Retourne MenuFichier
		val_menu_edit = self.tab_widget.widget(1)  # Retourne MenuEdition
		val_menu_proj = self.tab_widget.widget(2)  # Retourne MenuProjet
		
		dictio = dico_utilisateur()
		
		# On repète la même opération pour chacun des menus
		
		for element in val_menu_fic.liste_fonctions:
			val = self.valider_raccourci(element.raccourci.text())  # Nouveau raccourci
			if val != "":  # Si il a été modifié, on doit enregistrer la nouvelle valeur dans le dico utilisateur.
				clef = element.label.text()  # Ecrire json
				
				dictio["Fichier"][clef] = val
		
		for element in val_menu_edit.liste_fonctions:
			val = self.valider_raccourci(element.raccourci.text())  # Nouveau raccourci
			if val != "":  # Si il a été modifié, on doit enregistrer la nouvelle valeur dans le dico utilisateur.
				clef = element.label.text()  # Ecrire json
				
				dictio["Edition"][clef] = val
		
		for element in val_menu_proj.liste_fonctions:
			val = self.valider_raccourci(element.raccourci.text())  # Nouveau raccourci
			if val != "":  # Si il a été modifié, on doit enregistrer la nouvelle valeur dans le dico utilisateur.
				clef = element.label.text()  # Ecrire json
				
				dictio["Projet"][clef] = val
		
		save = json.dumps(dictio, indent=2)
		
		wfi = open("gui/raccourcis/racc_utilisateur.json", "w")
		wfi.write(save)
		wfi.close()
		
		self.done(0)
		
	def valider_raccourci(self, val):
		""" La fonction qui vérifie que les raccourcis sont corrects. """
		
		ligne = val.split("+")
		res = ""
		if "Ctrl" in ligne:
			res += "Ctrl+"
		if "Alt" in ligne:
			res += "Alt+"
		if "AltGr" in ligne:
			res += "AltGr+"
		if "Shift" in ligne:
			res += "Shift+"
		
		if "Esc" in ligne:
			return res + "Esc"
		for i in range(1, 13):
			if "F" + str(i) in ligne:
				return res + "F" + str(i)
			
		for trucs in ligne:
			if trucs not in res:
				return res + trucs[0]
	
		return ""
		
	def raz(self):
		""" Fonction de remise à zéro des raccourcis, càd que les raccourcis personnalisés seront
		transformés en raccourcis de base. """
		
		val_menu_fic = self.tab_widget.widget(0)  # Retourne MenuFichier
		val_menu_edit = self.tab_widget.widget(1)  # Retourne MenuEdition
		val_menu_proj = self.tab_widget.widget(2)  # Retourne MenuProjet
		
		dictio_util = dico_utilisateur()
		dico_def = dico_defaut()
		
		for element in val_menu_fic.liste_fonctions:
			clef = element.label.text()
			dictio_util["Fichier"][clef] = dico_def["Fichier"][clef]
		
		for element in val_menu_edit.liste_fonctions:
				clef = element.label.text()
				dictio_util["Edition"][clef] = dico_def["Edition"][clef]
		
		for element in val_menu_proj.liste_fonctions:
				clef = element.label.text()
				dictio_util["Projet"][clef] = dico_def["Projet"][clef]
		
		save = json.dumps(dictio_util, indent=2)
		
		wfi = open("gui/raccourcis/racc_utilisateur.json", "w")
		wfi.write(save)
		wfi.close()
		
		self.done(0)
		

class MenuFichier(QWidget):
	
	def __init__(self, parent):
		""" La classe pour le menu Fichier. """
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
		workplace = MenuFonction("Emplacement Workplace",
		                         donne_valeur_utilisateur(self.menu, "Emplacement Workplace"))
		cheminee = MenuFonction("Cheminee",
		                        donne_valeur_utilisateur(self.menu, "Cheminee"))
		ecran_chargement = MenuFonction("Ecran Chargement",
		                                donne_valeur_utilisateur(self.menu, "Ecran Chargement"))
		num_lignes = MenuFonction("Numerotation Des Lignes",
		                          donne_valeur_utilisateur(self.menu, "Numerotation Des Lignes"))
		assistance_vocale = MenuFonction("Assistance Vocale",
		                                 donne_valeur_utilisateur(self.menu, "Assistance Vocale"))
		plein_ecran = MenuFonction("Plein Ecran",
		                           donne_valeur_utilisateur(self.menu, "Plein Ecran"))
		quitter = MenuFonction("Quitter",
		                       donne_valeur_utilisateur(self.menu, "Quitter"))
		
		self.liste_fonctions = [new_projet, new_fichier, ouvrir, sauver, fermer_onglet, compiler,
		                        configuration, workplace, cheminee, ecran_chargement, num_lignes, assistance_vocale,
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
		""" La classe pour le menu Edition. """
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
		commenter = MenuFonction("Commenter",
		                         donne_valeur_utilisateur(self.menu, "Commenter"))
		
		self.liste_fonctions = [ligne_courante, mot_courant, dupliquer, mode_insertion, rechercher, indenter, commenter]
		
		self.fic_layout = QVBoxLayout()
		
		for widget in self.liste_fonctions:
			self.fic_layout.addWidget(widget)
		
		self.setLayout(self.fic_layout)
		
class MenuProjet(QWidget):
	
	def __init__(self, parent):
		""" La classe pour le menu Projet. """
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
		                          donne_valeur_utilisateur(self.menu, "Vider Tout Le Cache"))
		
		self.liste_fonctions = [importer, supprimer, informations, cache_projet, tous_cache]
		
		self.fic_layout = QVBoxLayout()
		
		for widget in self.liste_fonctions:
			self.fic_layout.addWidget(widget)
		
		self.setLayout(self.fic_layout)
		

class MenuFonction(QWidget):
	
	def __init__(self, nom_label, valeur_defaut):
		""" La classe qui permet de réaliser les lignes de saisies et d'indiquer ce à quoi elles correspondent. """
		QWidget.__init__(self)
		
		self.label = QLabel(nom_label)
		self.raccourci = QLineEdit()
		self.raccourci.setPlaceholderText(valeur_defaut)
		
		self.fonction_layout = QHBoxLayout()
		
		self.fonction_layout.addWidget(self.label)
		self.fonction_layout.addWidget(self.raccourci)
		
		self.setLayout(self.fonction_layout)
	
	def keyPressEvent(self, event):
		""" Le fonction qui permet d'écrire "Ctrl" quand on tape sur la touche Ctrl (et autres). """
		
		if event.key() == 16777249:  # Ctrl
			self.raccourci.insert("Ctrl+")
		elif event.key() == 16777248:  # Shift/Maj
			self.raccourci.insert("Shift+")
		elif event.key() == 16777251:  # Alt
			self.raccourci.insert("Alt+")
		elif event.key() == 16781571:  # Alt Gr
			self.raccourci.insert("AltGr+")
		elif event.key() == 16777216:  # Echap
			self.raccourci.insert("Esc")
			
		if "darwin" in sys.platform:
			if event.key() == 16777250:  # Ctrl des Macs
				self.raccourci.insert("^")
		
		for touche in range(64, 76):
			if event.key() == 16777200 + touche:
				self.raccourci.insert("F%s" % (touche-63))
		
def dico_defaut():
	""" Fonction qui enregistre dans une variable le contenu du json de base."""
	
	dictio = open("gui/raccourcis/racc_defaut.json", "r")
	dico = json.load(dictio)
	dictio.close()
	
	return dico

def dico_utilisateur():
	""" Fonction qui enregistre dans une variable le contenu du json de l'utilisateur. """
	
	dictio = open("gui/raccourcis/racc_utilisateur.json", "r")
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
			print("Clef voulue pas valide", clef_voulue)
	else:
		print("Clef menu pas valide", clef_menu)
	return ""
