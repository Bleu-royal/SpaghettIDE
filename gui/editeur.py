import sys
import os
from PySide.QtGui import *
from PySide.QtCore import *

from lexer import *
from themes.themes import *
import gui.style.style as style
sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class Editeur(QTextEdit):

	tabPress = Signal()

	def __init__(self, police, taille_texte, def_functions, keywords, parent, snippets):
		"""
		Hérite de QTextEdit.
		C'est une zone de texte dans laquelle on peut écrire, que l'on utilise ici pour écrire du code.

		Ici, on modifie ses paramètres en fonction du thème souhaité.
		:param police: Police d'écriture
		:type police: str
		:param couleur_fond: Couleur d'arrière plan de l'éditeur (background)
		:type couleur_fond: str
		:param couleur_texte: Couleur du texte de base
		:type couleur_texte: str
		:param taille_texte: Taille de la police (en points)
		:type taille_texte: int
		:rtype: None
		"""
		super().__init__()

		self.parent = parent
		self.police = police
		self.taille_texte = taille_texte
		self.def_functions = def_functions
		self.keywords = keywords
		self.snippets = snippets

		self.setTabStopWidth(20)

		self.yacc_errors = []
		self.last_yacc_errors = []

		self.maj_style()
		self.setFocus()

		# self.append("int main ( int argc, char** argv ){\n\n\treturn 0;\n\n}")
		
	def analyse(self):
	
		self.parent.defaut_info_message()  # Actualisation des infos de base dès que l'on tape sur une touche
		
		# process_yacc = Yaccer(self)  # Module parallele --> Sur un Thread
		# process_yacc.start()
		
		self.last_yacc_errors = self.yacc_errors
		self.yacc_errors = yaccing(self.toPlainText())
		
		if self.last_yacc_errors != self.yacc_errors:
			idx = self.parent.get_idx()
			self.parent.highlighters[idx].rehighlight()

	def keyPressEvent(self, event):

		self.parent.defaut_info_message()  # Actualisation des infos de base dès que l'on tape sur une touche
		"""
		if event.key() == 16777220:  # enter key

			# process_yacc = Yaccer(self)  # Module parallele --> Sur un Thread
			# process_yacc.start()

			self.last_yacc_errors = self.yacc_errors
			self.yacc_errors = yaccing(self.toPlainText())

			if self.last_yacc_errors != self.yacc_errors:
				idx = self.parent.get_idx()
				self.parent.highlighters[idx].rehighlight()
		"""

		if event.key() == 16777217:  # tab key

			if self.use_snippets(): return True

		if ("darwin" in sys.platform and event.nativeModifiers() == 4096) or \
				(not "darwin" in sys.platform and event.key() == 32 and event.nativeModifiers() == 514):
			self.tabPress.emit()
			return False

		super().keyPressEvent(event)

	def use_snippets(self):

		textCursor = self.textCursor()
		textCursor.select(QTextCursor.WordUnderCursor)
		word = textCursor.selectedText()
		if word in self.snippets:
			infos = self.snippets[word]
			textCursor.removeSelectedText()
			textCursor.insertText(infos[0])

			self.parent.indent()

			for i in range(infos[1]):
				self.moveCursor(QTextCursor.Up)

			for i in range(infos[2]):
				self.moveCursor(QTextCursor.Right)

			textCursor = self.textCursor()
			textCursor.select(QTextCursor.WordUnderCursor)
			self.setTextCursor(textCursor)

			return True

	def maj_style(self):
		c = get_color_from_theme("textedit")

		self.setStyleSheet("QTextEdit { background-color:" + get_rgb(c["text-back-color"]) + ";"
						   + "font-family:" + self.police + ";"
						   + "color:" + get_rgb(c["text-color"]) + ";"
						   + "font-size:" + str(self.taille_texte) + "pt; }")

	def show_nb_prop(self, nb_prop):
		if nb_prop == 0:
			self.parent.info_message("empty")
		else:
			self.parent.info_message(str(nb_prop) + " proposition%s" % ("s" * (nb_prop != 1)))

	def select_current_line(self):
		textCursor = self.textCursor()
		textCursor.select(QTextCursor.LineUnderCursor)

		self.setTextCursor(textCursor)

	def select_current_word(self):
		textCursor = self.textCursor()
		textCursor.select(QTextCursor.WordUnderCursor)

		self.setTextCursor(textCursor)

	def duplicate(self):
		textCursor = self.textCursor()
		return_ = ""

		if textCursor.selectedText() == "":
			textCursor.select(QTextCursor.LineUnderCursor)
			return_ = "\n"

		textCursor.insertText(textCursor.selectedText() + return_ + textCursor.selectedText())

	def comment_selection(self):
		textCursor = self.textCursor()

		if textCursor.selectedText() == "":
			textCursor.select(QTextCursor.LineUnderCursor)

		text = textCursor.selectedText()
		textCursor.removeSelectedText()

		lines = text.split("\u2029") # \u2029 -> \n

		is_commented = self.check_comment(lines)

		for i in range(len(lines)):
			if lines[i].strip() != "":
				if is_commented:
					lines[i] = lines[i][2:]
				else:
					lines[i] = "//" + lines[i]

		textCursor.insertText("\n".join(lines))

	def check_comment(self, lines):
		for line in lines:
			if line[:2] != "//" and line.strip() != "":
				return False
		return True
