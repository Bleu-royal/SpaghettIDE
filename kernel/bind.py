def bind(fenetre):  # binding

	fenetre.bouton_sauvegarde.clicked.connect(fenetre.save)
	fenetre.ouvrir.clicked.connect(fenetre.open)
