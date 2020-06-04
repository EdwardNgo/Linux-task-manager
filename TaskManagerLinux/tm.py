from PyQt5 import QtCore, QtGui, QtWidgets
import psutil, sys, time
from PyQt5.QtWidgets import QTreeWidgetItem

process = []
cpuPer = [0,1,2,3,4,5,6,7]
memPer = 0.1
pIDs = []
a = 1
class Ui_linuxTaskManager(object):

    def veriler(a):
        pIDs = psutil.pids()
        pMet = []
        cpuTemp = psutil.cpu_percent(percpu=True)
        for k in range(4):
            cpuPer[k] = float(cpuTemp[k])
        print(cpuTemp)
        print(cpuPer)
        memTemp = psutil.virtual_memory()
        memPer = float(memTemp[2])
        for i in pIDs:
            p = psutil.Process(i)
            pMet.append((p.name()))
            pMet.append(str(i))
            pMet.append(str(p.cpu_percent()))
            pMet.append(str(p.memory_percent()))
            process.append(QTreeWidgetItem(pMet))
            pMet = []
        return cpuPer,memPer,pIDs,process

    def pidSort(self):

        gelen = self.veriler()

        print(gelen[2])
        listSort = sorted(gelen[2])
        print(listSort)
        for j in process:
            self.treeWidget.addTopLevelItem(j)

    def pNSort(self):

        gelenName = self.veriler()

        nameSort = sorted(gelenName[3])
        print(nameSort)

    def update(self):
        self.veriler()
        upVal = self.veriler()
        self.ramBar.setProperty("value",int(upVal[1]))
        self.cpuBar0.setProperty("value",int(upVal[0][0]))
        self.cpuBar1.setProperty("value",int(upVal[0][1]))
        self.cpuBar2.setProperty("value",int(upVal[0][2]))
        self.cpuBar3.setProperty("value",int(upVal[0][3]))
        self.cpuBar4.setProperty("value",int(upVal[0][4]))
        self.cpuBar5.setProperty("value",int(upVal[0][5]))
        self.cpuBar6.setProperty("value",int(upVal[0][6]))
        self.cpuBar7.setProperty("value",int(upVal[0][7]))


    def setupUi(self, linuxTaskManager):

        reVal = self.veriler()

        linuxTaskManager.setObjectName("linuxTaskManager")
        linuxTaskManager.resize(851, 602)
        self.centralwidget = QtWidgets.QWidget(linuxTaskManager)
        self.centralwidget.setObjectName("centralwidget")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(10, 10, 481, 561))
        self.treeWidget.setObjectName("treeWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(520, 40, 58, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(520, 150, 58, 15))
        self.label_2.setObjectName("label_2")
        self.reFresh = QtWidgets.QPushButton(self.centralwidget)
        self.reFresh.setGeometry(QtCore.QRect(740, 540, 89, 27))
        self.reFresh.setObjectName("reFresh")
        self.pNameSort = QtWidgets.QPushButton(self.centralwidget)
        self.pNameSort.setGeometry(QtCore.QRect(10, 10, 101, 27))
        self.pNameSort.setObjectName("pNameSort")
        self.PIDSort = QtWidgets.QPushButton(self.centralwidget)
        self.PIDSort.setGeometry(QtCore.QRect(110, 10, 101, 27))
        self.PIDSort.setObjectName("PIDSort")
        self.CPUSort = QtWidgets.QPushButton(self.centralwidget)
        self.CPUSort.setGeometry(QtCore.QRect(210, 10, 101, 27))
        self.CPUSort.setObjectName("CPUSort")
        self.RAMSort = QtWidgets.QPushButton(self.centralwidget)
        self.RAMSort.setGeometry(QtCore.QRect(310, 10, 181, 27))
        self.RAMSort.setObjectName("RAMSort")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(520, 190, 41, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(520, 230, 41, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(520, 270, 41, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(520, 310, 41, 16))
        self.label_6.setObjectName("label_6")
        self.ramBar = QtWidgets.QProgressBar(self.centralwidget)
        self.ramBar.setGeometry(QtCore.QRect(520, 60, 321, 51))
        self.ramBar.setProperty("value", int(reVal[1]))
        self.ramBar.setObjectName("ramBar")
        self.cpuBar0 = QtWidgets.QProgressBar(self.centralwidget)
        self.cpuBar0.setGeometry(QtCore.QRect(570, 140, 271, 31))
        self.cpuBar0.setProperty("value", int(reVal[0][0]))
        self.cpuBar0.setObjectName("cpuBar0")
        self.cpuBar1 = QtWidgets.QProgressBar(self.centralwidget)
        self.cpuBar1.setGeometry(QtCore.QRect(570, 180, 271, 31))
        self.cpuBar1.setProperty("value", int(reVal[0][1]))
        self.cpuBar1.setObjectName("cpuBar1")
        self.cpuBar2 = QtWidgets.QProgressBar(self.centralwidget)
        self.cpuBar2.setGeometry(QtCore.QRect(570, 220, 271, 31))
        self.cpuBar2.setProperty("value", int(reVal[0][2]))
        self.cpuBar2.setObjectName("cpuBar2")
        self.cpuBar3 = QtWidgets.QProgressBar(self.centralwidget)
        self.cpuBar3.setGeometry(QtCore.QRect(570, 260, 271, 31))
        self.cpuBar3.setProperty("value", int(reVal[0][3]))
        self.cpuBar3.setObjectName("cpuBar3")
        self.cpuBar4 = QtWidgets.QProgressBar(self.centralwidget)
        self.cpuBar4.setGeometry(QtCore.QRect(570, 300, 271, 31))
        self.cpuBar4.setProperty("value", int(reVal[0][4]))
        self.cpuBar4.setObjectName("cpuBar4")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(520, 350, 58, 15))
        self.label_7.setObjectName("label_7")
        self.cpuBar5 = QtWidgets.QProgressBar(self.centralwidget)
        self.cpuBar5.setGeometry(QtCore.QRect(570, 340, 271, 31))
        self.cpuBar5.setProperty("value", int(reVal[0][5]))
        self.cpuBar5.setObjectName("cpuBar5")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(520, 390, 58, 15))
        self.label_8.setObjectName("label_8")
        self.cpuBar6 = QtWidgets.QProgressBar(self.centralwidget)
        self.cpuBar6.setGeometry(QtCore.QRect(570, 380, 271, 31))
        self.cpuBar6.setProperty("value", int(reVal[0][6]))
        self.cpuBar6.setObjectName("cpuBar6")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(520, 430, 58, 15))
        self.label_9.setObjectName("label_9")
        self.cpuBar7 = QtWidgets.QProgressBar(self.centralwidget)
        self.cpuBar7.setGeometry(QtCore.QRect(570, 420, 271, 31))
        self.cpuBar7.setProperty("value", int(reVal[0][7]))
        self.cpuBar7.setObjectName("cpuBar7")
        linuxTaskManager.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(linuxTaskManager)
        self.statusbar.setObjectName("statusbar")
        linuxTaskManager.setStatusBar(self.statusbar)

        self.retranslateUi(linuxTaskManager)
        QtCore.QMetaObject.connectSlotsByName(linuxTaskManager)

        self.PIDSort.clicked.connect(self.pidSort)
        self.pNameSort.clicked.connect(self.pNSort)
        self.reFresh.clicked.connect(self.update)


        for j in process:
            self.treeWidget.addTopLevelItem(j)

    def retranslateUi(self, linuxTaskManager):
        _translate = QtCore.QCoreApplication.translate
        linuxTaskManager.setWindowTitle(_translate("linuxTaskManager", "MainWindow"))
        self.treeWidget.headerItem().setText(0, _translate("linuxTaskManager", "Process Name"))
        self.treeWidget.headerItem().setText(1, _translate("linuxTaskManager", "PID"))
        self.treeWidget.headerItem().setText(2, _translate("linuxTaskManager", "CPU"))
        self.treeWidget.headerItem().setText(3, _translate("linuxTaskManager", "RAM"))
        self.label.setText(_translate("linuxTaskManager", "RAM"))
        self.label_2.setText(_translate("linuxTaskManager", "CPU 0"))
        self.reFresh.setText(_translate("linuxTaskManager", "Refresh"))
        self.pNameSort.setText(_translate("linuxTaskManager", "Process Name"))
        self.PIDSort.setText(_translate("linuxTaskManager", "PID"))
        self.CPUSort.setText(_translate("linuxTaskManager", "CPU"))
        self.RAMSort.setText(_translate("linuxTaskManager", "RAM"))
        self.label_3.setText(_translate("linuxTaskManager", "CPU 1"))
        self.label_4.setText(_translate("linuxTaskManager", "CPU 2"))
        self.label_5.setText(_translate("linuxTaskManager", "CPU 3"))
        self.label_6.setText(_translate("linuxTaskManager", "CPU 4"))
        self.label_7.setText(_translate("linuxTaskManager", "CPU 5"))
        self.label_8.setText(_translate("linuxTaskManager", "CPU 6"))
        self.label_9.setText(_translate("linuxTaskManager", "CPU 7"))

class sFunc():
    def showFunc(a):
        app =QtWidgets.QApplication(sys.argv)
        columnApp = QtWidgets.QMainWindow()
        ui = Ui_linuxTaskManager()
        ui.setupUi(columnApp)
        columnApp.show()
        sys.exit(app.exec_())


class mFunc():
    def main():
        Ui_linuxTaskManager.veriler(a)
        sFunc.showFunc(a)
        #Ui_linuxTaskManager.killProc.clicked.connect(mFunc.main)

    main()
