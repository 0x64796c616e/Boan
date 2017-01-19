import sys
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread

from http.server import HTTPServer, BaseHTTPRequestHandler



   
class A(QObject):

	sayhi = pyqtSignal()

	def __init__(self):
		QObject.__init__(self)
		self.sayhi.connect(self.bfunc)

	def afunc(self):
		self.sayhi.emit()  
        
	def bfunc(self):
		print ("Hello World!")



if __name__=="__main__":
    app=QCoreApplication(sys.argv)
    a=A()
    a.afunc()    
    sys.exit(app.exec_())


