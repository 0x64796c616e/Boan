#!/usr/bin/env python3

import sys
import os
from time import sleep
### Proxy ###
import proxy
from urllib.parse import urlparse
### GUI ###
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import *

qtCreatorFile = "g.ui" #Qt XML ui file.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

waitCondition = QWaitCondition()
mutex = QMutex()

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.px = ProxyThread() # Proxy Qthread
        self.connect()

    def connect(self):
        self.pushButton_forward.clicked.connect(self.handleButton_forward)
        self.pushButton_power.clicked[bool].connect(self.handleButton_power)
        self.px.statusbarsignal.connect(self.update_statusbar)
        self.px.reqsignal.connect(self.handle_reqsignal)

    def handleButton_forward(self):
        self.pushButton_forward.setEnabled(False)
        #self.px.req.path = self.box_body.toPlainText()
        self.box_body.clear()
        self.wakeup()
        return

    def handleButton_power(self,isPressed):
        if isPressed:
            self.px['port'] = self.spinBox_port.value()
            self.px.start()
            self.spinBox_port.setEnabled(False)
            self.pushButton_power.setText("Running...")
        else:
            self.px.stop()
            self.pushButton_power.setText("Run")
            self.spinBox_port.setEnabled(True)
            self.pushButton_forward.setEnabled(False)

    def update_statusbar(self,msg,msec):
        self.statusbar.clearMessage()
        self.statusbar.showMessage(msg,msec)

    def handle_reqsignal(self):
        self.pushButton_forward.setEnabled(True)
        #self.box_body.appendPlainText(self.px.req.path);
        self.box_body.appendPlainText(self.px.req.command+" "+self.px.req.path+" "+self.px.req.protocol_version);
        for h in self.px.req.headers:
            self.box_body.appendPlainText(h+": "+self.px.req.headers[h])
        self.box_body.appendPlainText("") # newline
        if self.px.req_body:
            self.box_body.appendPlainText(self.px.req_body.decode("utf-8"))

    def wakeup(self):
        waitCondition.wakeAll()

class PX(proxy.ProxyRequestHandler):

    def request_handler(self, req, req_body):
        self.reqsignal.emit()
        self.pt.req = req
        self.pt.req_body = req_body
        mutex.lock()
        waitCondition.wait(mutex)
        mutex.unlock()
        #req = self.pt.req
        #req_body = self.pt.req_body
        pass

    def wakey(self):
        self.wakeup()

    def sayhi(msg="hey there"):
        print(msg)

class ProxyThread(QThread):
    port = 8080
    statusbarsignal = pyqtSignal(str,int)
    reqsignal = pyqtSignal()
    updsignal = pyqtSignal(str)
    req = None
    req_body = None

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def run(self):
        HandlerClass=PX
        ServerClass=proxy.ThreadingHTTPServer

        protocol="HTTP/1.1"
        server_address = ('', self.port)
        HandlerClass.protocol_version = protocol

        HandlerClass.pt = self
        HandlerClass.statusbarsignal = self.statusbarsignal
        HandlerClass.reqsignal = self.reqsignal

        self.httpd = ServerClass(server_address, HandlerClass)

        sa = self.httpd.socket.getsockname()

        self.statusbarsignal.emit("Listening on "+sa[0]+" port "+str(sa[1])+"...",0)
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.server_close()
        self.terminate()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())