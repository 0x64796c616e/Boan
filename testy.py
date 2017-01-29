import sys
import os
from time import sleep
### GUI ###
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import *


qtCreatorFile = "test.ui" #Qt XML ui file.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QMainWindow, Ui_MainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.connect()

	def connect(self):
		self.pushButton.clicked.connect(self.handleButton)
	def handleButton(self):
		print("clicked")
		sleep(3)
		self.raise_()
		#self.show()
		#self.activateWindow()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())