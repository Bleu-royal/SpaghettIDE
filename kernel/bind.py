def bind(fenetre):  # binding

	fenetre.bouton_sauvegarde.clicked.connect(fenetre.save)
	fenetre.bouton_nouveau.clicked.connect(fenetre.new)
	fenetre.ouvrir.clicked.connect(fenetre.open)
