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
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

mainwindow_ui_file = "g.ui" #Qt XML ui file.
Ui_MainWindow, QtBaseClass = uic.loadUiType(mainwindow_ui_file)

waitCondition = QWaitCondition()
mutex = QMutex()

class SettingsWindow(QDialog):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        uic.loadUi('settings.ui', self)
        self.settings = QSettings("Boan", "Boan")
        self.loadSettings()
        self.show()

    def loadSettings(self):
        self.spinBox_port.setValue(int(self.settings.value("port", 8080)))

    def accept(self):
        self.settings.setValue("port",self.spinBox_port.value())
        self.close()

class AboutWindow(QDialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        uic.loadUi('about.ui', self)
        self.show()

    def accept(self):
        self.close()

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.px = ProxyThread() # Proxy Qthread
        self.settings = QSettings("Boan", "Boan")
        self.connect()
        self.centerOnScreen()

    def connect(self):
        #Shortcuts
        self.shortcut_quit = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.shortcut_quit.activated.connect(self.on_quit)
        self.shortcut_settings = QShortcut(QKeySequence("Ctrl+Shift+S"), self)
        self.shortcut_settings.activated.connect(self.do_settings)

        #Menu
        self.actionSettings.triggered.connect(self.do_settings)
        self.actionAbout.triggered.connect(self.do_about)
        self.actionQuit.triggered.connect(self.on_quit)

        #Buttons
        self.pushButton_forward.clicked.connect(self.handleButton_forward)
        self.pushButton_power.clicked[bool].connect(self.handleButton_power)
        self.px.statusbarsignal.connect(self.update_statusbar)
        self.px.reqsignal.connect(self.handle_reqsignal)

    def centerOnScreen (self):
        '''centerOnScreen() Centers the window on the screen.'''
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),(resolution.height() / 2) - (self.frameSize().height() / 2))
    
    def do_settings(self):
        dlg = SettingsWindow()
        dlg.exec_()

    def do_about(self):
        dlg = AboutWindow()
        dlg.exec_()

    def on_quit(self):
        self.close()

    def handleButton_forward(self):
        self.pushButton_forward.setEnabled(False)
        self.px.raw_req = self.box_body.toPlainText() 
        self.box_body.clear()
        self.wakeup()
        return

    def handleButton_power(self,isPressed):
        if isPressed:
            self.px['port'] = int(self.settings.value("port", 8080))
            self.px.start()
            self.pushButton_power.setText("Running...")
        else:
            self.px.stop()
            self.pushButton_power.setText("Run")
            self.pushButton_forward.setEnabled(False)

    def update_statusbar(self,msg,msec):
        self.statusbar.clearMessage()
        self.statusbar.showMessage(msg,msec)

    def handle_reqsignal(self):
        self.raise_()
        self.show()
        self.activateWindow()

        self.box_body.append(self.px.req.command+" "+self.px.req.path+" "+self.px.req.protocol_version);
        for h in self.px.req.headers:
            self.box_body.append(h+": "+self.px.req.headers[h])
        self.box_body.append("") # newline
        if self.px.req_body:
            self.box_body.append(self.px.req_body.decode("utf-8"))
        self.pushButton_forward.setEnabled(True)

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
        
        # Parse the raw request and map onto the httpreq object
        raw = self.pt.raw_req.split('\n')
        req.raw_req = self.pt.raw_req
        try:  
            req.command, req.path, req.protocol_version = raw[0].split()
        except Exception as e:
            self.send_error(400)
        
        for c in range(1,len(raw)):
            #print(c,raw[c])
            if raw[c] == '': # the newline
                break
            try:  
                h,v = raw[c].split(': ')
            except Exception as e:
                self.send_error(400)

            del req.headers[h]
            req.headers[h] = v

        req_body = bytes('\n'.join(raw[c+1:]),"utf-8")

        return req_body

    def wakey(self):
        self.wakeup()

class ProxyThread(QThread):
    port = 8080
    statusbarsignal = pyqtSignal(str,int)
    reqsignal = pyqtSignal()
    updsignal = pyqtSignal(str)
    req = None
    req_body = None
    raw_req = None

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