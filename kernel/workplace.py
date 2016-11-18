from PySide.QtCore import *

def create_workplace():
	path=QDir.homePath()

	if not QDir(path + '/workplace/').exists():
		QDir(path).mkpath("workplace")
