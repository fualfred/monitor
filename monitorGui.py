# -*- coding: utf-8 -*-

# MainWindow implementation generated from reading ui file 'monitor.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from mUtils import get_ssh_client,sshClose,getCpu,getMem
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdate
import matplotlib
from matplotlib import pyplot as plt
#matplotlib.use("Qt5Agg")
class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self,sshClient,plotCanvas):
        super(Ui_MainWindow, self).__init__()
        self.sshClient = sshClient
        self.plotCanvas = plotCanvas
        self.setCentralWidget(self.plotCanvas)
        self.timer = QTimer()
        self.setupUi(self)
        self.retranslateUi(self)
        self.show()
        self.max_cpu_used = []
        self.max_mem_used = []
        self.xr=[]
        self.yc=[]
        self.ym=[]
        self.timer.timeout.connect(self.append_data)
        self.ani = FuncAnimation(self.plotCanvas.figure, self.update_line, interval=10)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 630)
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setGeometry(QtCore.QRect(10, 10, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit.setGeometry(QtCore.QRect(80, 10, 101, 20))
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(MainWindow)
        self.label_2.setGeometry(QtCore.QRect(210, 10, 31, 16))
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit_2.setGeometry(QtCore.QRect(250, 10, 41, 20))
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(MainWindow)
        self.label_3.setGeometry(QtCore.QRect(210, 50, 71, 16))
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit_3.setGeometry(QtCore.QRect(270, 50, 113, 20))
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton = QtWidgets.QPushButton(MainWindow)
        self.pushButton.setGeometry(QtCore.QRect(310, 10, 75, 23))
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(MainWindow)
        self.label_4.setGeometry(QtCore.QRect(10, 50, 60, 10))
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit_4.setGeometry(QtCore.QRect(80, 50, 113, 20))
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_5 = QtWidgets.QLabel(MainWindow)
        self.label_5.setGeometry(QtCore.QRect(400, 20, 91, 16))
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(MainWindow)
        self.label_6.setGeometry(QtCore.QRect(400, 50, 91, 16))
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lineEdit_5 = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit_5.setGeometry(QtCore.QRect(500, 20, 71, 20))
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_5.setEnabled(False)
        self.lineEdit_6 = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit_6.setGeometry(QtCore.QRect(500, 50, 71, 20))
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_6.setEnabled(False)
        self.pushButton.clicked.connect(self.login)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Monitor"))
        MainWindow.setWindowIcon(QtGui.QIcon("monitor.jpg"))
        self.label.setText(_translate("MainWindow", "HostName"))
        self.lineEdit.setText(_translate("MainWindow", "192.168.34.171"))
        self.label_2.setText(_translate("MainWindow", "Port"))
        self.lineEdit_2.setText(_translate("MainWindow", "22"))
        self.lineEdit_4.setText(_translate("MainWindow", "root"))
        self.lineEdit_3.setText(_translate("MainWindow", "NSD123dev"))
        self.label_3.setText(_translate("MainWindow", "Password"))
        self.pushButton.setText(_translate("MainWindow", "connect"))
        self.label_4.setText(_translate("MainWindow", "User"))
        self.label_5.setText(_translate("MainWindow", "Max_CpuUsed"))
        self.label_6.setText(_translate("MainWindow", "Max_MemUsed"))
    def beforeLogin(self):
        self.hostName = self.lineEdit.text()
        self.port = self.lineEdit_2.text()
        self.userName = self.lineEdit_4.text()
        self.password = self.lineEdit_3.text()
        print("获取******成功")
    def login(self):
        if self.sshClient != None:
           sshClose(self.sshClient)
           self.beforeLogin()
           self.timer.stop()
           self.timer.start(5000)
        else:
           self.beforeLogin()
           self.timer.stop()
           self.timer.start(5000)
    def getData(self):
        time = datetime.now()
        #print(time.strftime("%Y-%m-%d %H:%M:%S"))
        self.sshClient=get_ssh_client(self.hostName,self.port,self.userName,self.password)
        cpuUsePercent =getCpu(self.sshClient)[0]
        cpuValue = cpuUsePercent.rstrip("%")
        cpuUse = round(float(cpuValue) / 100, 3)
        mem_values = getMem(self.sshClient)
        self.sshClient.close()
        mem_use = round((float(int(mem_values[0]) - int(mem_values[1]))) / int(mem_values[0]), 3)
        self.setCpuMaxUsedValue(self.max_cpu_used,cpuUse)
        self.setMemMaxUsedValue(self.max_mem_used,mem_use)
        cpuRecordFile = open("cpuRecord.csv", "a+")
        memRecordFile = open("memRecord.csv", "a+")
        cpuRecordFile.write(time.strftime("%Y-%m-%d %H:%M:%S")+","+cpuUsePercent+"\n")
        memRecordFile.write(time.strftime( "%Y-%m-%d %H:%M:%S") + "," + str(mem_values[0]) +","+str(mem_values[1])+ "\n")
        cpuRecordFile.close()
        memRecordFile.close()
        return (time,cpuUse,mem_use)
    def getConnectStaus(self):
        if self.sshClient ==None:
            return False
        else:
            return True
    def handlerData(self):
        if self.getConnectStaus():
            return self.getData()
        else:
            self.sshClient =get_ssh_client(self.hostName, self.port, self.userName, self.password)
    def append_data(self):
        timeDisplay,cpuUse,mem_use =self.getData()
        timeDisplay =timeDisplay.strftime("%H:%M:%S")
        self.xr.append(timeDisplay)
        self.yc.append(cpuUse)
        self.ym.append(mem_use)
        if len(self.xr) > 200:
            del self.xr[0]
        if len(self.yc)>200:
            del self.yc[0]
        if len(self.ym)>200:
            del self.ym[0]
    def update_line(self,i):
        self.plotCanvas.axes.clear()
        self.plotCanvas.axes.plot(self.xr,self.yc)
        self.plotCanvas.axes.plot(self.xr, self.ym)
        #self.plotCanvas.axes.legend()
    def setCpuMaxUsedValue(self,list,cpuValue):
        if len(list)==0:
            list.append(cpuValue)
            self.lineEdit_5.setText(str(cpuValue))
        else:
            if cpuValue >list[0]:
                self.lineEdit_5.setText(str(cpuValue))
                list[0] = cpuValue
    def setMemMaxUsedValue(self,list,memValue):
        if len(list)==0:
            list.append(memValue)
            self.lineEdit_6.setText(str(memValue))
        else:
            if memValue >list[0]:
                self.lineEdit_6.setText(str(memValue))
                list[0] = memValue
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        #self.axes.xaxis_date()
        #self.axes.xaxis.set_major_locator(mdate.MinuteLocator())
        #self.axes.xaxis.set_minor_locator(mdate.SecondLocator([10, 20, 30, 40, 50]))
        self.fig.autofmt_xdate(rotation=90)
        #self.axes.xaxis.set_major_formatter(mdate.DateFormatter("%H:%M:%S"))
        self.axes.set_xlabel("Time")
        self.axes.set_ylabel("Used-Percent")
        #self.axex.set_xticks([])
        self.axes.set_ylim(0, 1)
        super(PlotCanvas, self).__init__(self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
class Myanimation(object):
    def __init__(self):
        super(Myanimation, self).__init__()
if __name__  ==  "__main__":
    sshClient = None
    plotCanvas = PlotCanvas()
    app = QtWidgets.QApplication(sys.argv)
    ui_MainWindow = Ui_MainWindow(sshClient,plotCanvas)
    sys.exit(app.exec())