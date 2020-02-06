# very basic terminal emulator in pyqt
# https://pythonbasics.org/pyqt/

from PyQt5 import QtWidgets, uic, QtCore, Qt, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMessageBox, QDialog, QFileDialog
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow
import sys
import time
import subprocess
import pyxinput


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('gui.txt', self)
        #Handles Configuration:
        config = open('config.txt', "r+")
        self.lineEdit.returnPressed.connect(self.handleCommands)
        # self.pushButtonInstall.clicked.connect(self.onClick)
        config = config.readlines()
        titleBarHidden = config[0]
        titleBarHidden = [int(i) for i in titleBarHidden.split() if i.isdigit()][0]
        screenSizeX = config[1]
        screenSizeX = [int(i) for i in screenSizeX.split() if i.isdigit()][0]
        screenSizeY = config[2]
        screenSizeY = [int(i) for i in screenSizeY.split() if i.isdigit()][0]

        print("Title: " + str(titleBarHidden))
        #Handles Title and low level window control (gui)
        self.titleBar = titleBarHidden
        if(self.titleBar == 0):
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        else:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.setWindowTitle("Universal DollyCam")
        self.working_dir = "."
        self.setFixedSize(screenSizeX, screenSizeY)
        self.hideVal = 0
        self.move(0,0)
        self.textBrowser.setText("Universal Dollycam by c4syner" + "\n")
        #Handles virtual controller and modes for the dollycam
        self.controller = pyxinput.vController()
        self.init_mode = 0 #Init mode 1 is left joystick constant velocity
        self.mode = 0 #Mode 1 is left joystick velocity only

        #Constants:
        self.camLeftX = 0



    def keyPressEvent(self, event):
        if event.key() == 16777216:
            self.close()
        elif event.key() == 16777264:
            if(self.hideVal == 1):
                self.move(0, 0)
                self.hideVal = 0
            else:
                self.move(-1000, -1000)
                self.hideVal = 1

    def setController(self):
        self.controller.set_value("AxisLx", self.camLeftX)
    def stopController(self):
        self.controller.set_value("AxisLx", 0)
    def handleCommands(self):
        cmd = self.lineEdit.text()
        if(self.init_mode == 1):
            self.init_mode = 0
            self.mode = 1
            try:
                self.camLeftX = float(cmd)
                self.textBrowser.setText(self.textBrowser.toPlainText() + "$ " + "Value of camera x set to: " + str(self.camLeftX)+ "\n")
            except:
                self.textBrowser.setText(self.textBrowser.toPlainText() + "$ " + "Invalid value..."+ "\n")

        else:

            if cmd == "exec dollycam x_constant":
                output = "Dollycam left joystick activated... \nawaiting rate assignment"
                self.init_mode = 1
            elif(cmd == "help"):
                output = "Options:\nexec dollycam x_constant : \ninitalizes dollycam for left joystick x value (next value entered will be rate at which camera moves(-1,1))\n "
            elif((self.mode == 1) and (cmd == "start")): #Move along x axis until explicitly told to stop
                self.setController()
                output = "Camera velocity moving at " + str(self.camLeftX)
            elif(cmd == "stop"):
                self.stopController()
                output = "Camera Velocity set to 0"
            else:
                output = "Unknown command..."

            self.textBrowser.setText(self.textBrowser.toPlainText() + "$ "+ output + "\n")
        self.lineEdit.setText("")
        self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())


app = QtWidgets.QApplication([])
dark(app)


win = Main()
win.show()
sys.exit(app.exec())
