import os

from PySide.QtCore import *
from threading import *

class Execution(QObject, Thread):

	resultat = Signal(str)

	def __init__(self, cmd):

		QObject.__init__(self)
		Thread.__init__(self)

		self.cmd = cmd

	def run(self):

		res = os.system(self.cmd)
		self.resultat.emit(res)

def exec_(cmd, ret=False):
	ex = Execution(cmd)
	if ret:
		ex.resultat.connect(test)
	ex.start()

def test(e):
	print(e)
