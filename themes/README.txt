—— English ——

Here are the different themes of the application.
themes.py is the module where are methods to get the current theme, change it, and get the colors depending of the theme.


— Create a new theme —
You can create a new theme using the create_theme.py file. Just run it in a console and add a name (don’t forget to go in the themes repertory before). For exemple typing « python3 create_theme.py myExempleTheme » will create a repertory named ’myExempleTheme’ (which is the name of your new theme) and will contain files with .json extension. Those files contains the colors (everything is black by default), and you’ll need to specify all of them.


—> statusbar.json :
‘BACKGROUND’ : background color of the status bar
‘TEXT’ : color of the text

—> token.json :
‘IDENTIFIER’ : basic writing color in the code area
‘KEYWORD’ : keywords colors (return, break…) 
‘STRING_LITERAL’ : strings colors (“hello world“)
‘COMMENT’ : comments colors (//this is a comment line)
‘TYPE’ : types colors (int, char, bool…)
‘OP’ : operands colors (+, -, =, …)

—> textedit.json :
‘text-back-color’ : background color of the code area
‘text-color’ : text basic and cursor color
‘tab-color’ : tabs text color
‘tab-back-color’ : tabs background color
‘tab-hover-back-color’ : tabs background color when hovered or selected
‘tab-hover-color’ : tabs text color when hovered or selected
‘tab-hover-bord-bot-color’ : bottom border tabs hovered color (optional, you can leave it to black)

—> treeview.json :
‘BACKGROUND’ : background color of the treeview
‘ITEMS’ : items text color
‘ITEMSHOVER’ : items text color when hovered



Finally, you want to add it in the menu bar. To do so, you need to add it manually in the graphique.py module.

First, create an Action :
new_theme = MyAction(parent, "&theme name", "theme name", self.fonction_to_bind)

Then, add it to the theme group :
self.set_group(new_theme, groupe_theme, apparence_menu, "theme name")

And don’t forget to make the bind function :
def to_newTheme(self):
    self.__change_theme_to("theme name")


==================================


—— Français ——
Ce répertoire contient tout ce qui est relatif aux thèmes.
Le module themes.py regroupe les méthodes pour récupérer le thème actuel, le changer ainsi que de récupérer les couleurs des éléments en fonction du thème sélectionné.


— Créer un nouveau thème —
Vous pouvez créer votre propre thème. Pour cela, lancez le fichier « create_theme.py » dans le répertoire themes via une console de terminal et spécifiez le nom du thème. Si vous tapez par exemple « python3 create_theme.py monNouveauTheme » vous créez un thème appelé ‘monNouveauTheme’ qui est représenté par un répertoire, ainsi que des fichiers en .json à l’intérieur. Ces fichiers contiennent les couleurs de votre nouveau thème. Par défaut elles seront toutes en noir, il vous faudra donc les changer.

—> statusbar.json :
‘BACKGROUND’ : couleur de fond de la barre de statut
‘TEXT’ : couleur du texte

—> token.json :
‘IDENTIFIER’ : couleur de base de l’écriture dans la zone de code
‘KEYWORD’ : couleur des mots clefs (return, break…) 
‘STRING_LITERAL’ : couleur des chaînes de caratères (“hello world“)
‘COMMENT’ : couleur des commentaires (//this is a comment line)
‘TYPE’ : couleur des déclarations de type (int, char, bool…)
‘OP’ : couleur des opérandes (+, -, =, …)

—> textedit.json :
‘text-back-color’ : couleur de fond de la zone de code
‘text-color’ : couleur basique du texte et du curseur
‘tab-color’ : couleur du texte des onglets
‘tab-back-color’ : couleur de fond des onglets
‘tab-hover-back-color’ : couleur de fond des onglets quand ils sont survolés ou sélectionnés
‘tab-hover-color’ : couleur du texte des onglets quand ils sont survolés ou sélectionnés
‘tab-hover-bord-bot-color’ : couleur de la bordure du bas de l’onglet survolé ou sélectionné (c’est facultatif, vous pouvez le laisser en noir)

—> treeview.json :
‘BACKGROUND’ : couleur de fond du navigateur de fichiers
‘ITEMS’ : couleur des éléments (texte) du navigateur de fichiers
‘ITEMSHOVER’ : couleur des éléments lorsqu’ils sont survolés.



Enfin, pour afficher votre nouveau thème dans la barre de menu, vous devez aller dans le module graphique, et l’ajouter manuellement.

Pour cela créez une action pour ce thème :
autre_theme = MyAction(parent, "&nom theme", "nom theme", self.fonction_a_relier)

Ajoutez l’action au groupe des thèmes : 
self.set_group(autre_theme, groupe_theme, apparence_menu, "nom theme")

Et n’oubliez pas de définir la fonction qui va relier le thème, par exemple :
def to_autreTheme(self):
    self.__change_theme_to("nom theme")
