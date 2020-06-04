from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import MainAppGUI
from ProcStat import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

import numpy
class TaskManager(QtWidgets.QMainWindow, MainAppGUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(TaskManager, self).__init__(parent)
        self.setupUi(self)

        self.pushButton_shutdown.clicked.connect(self.__poweroff)
        self.pushButton_reboot.clicked.connect(self.__reboot)
        self.pushButton_kill.clicked.connect(self.__kill)

        # paletteColor = self.label_CPU_Total.palette()
        # paletteColor.setColor(QPalette.WindowText, QColor(CpuPlot.colors[0]))
        # self.label_CPU_Total.setPalette(paletteColor)

        # self.label_CPU_Cores.setText("")
        # self.label_CPU_list = {}

        # keys = self.qwtPlot_CPU.data.keys()
        # for x in xrange(0, len(keys)):
        #     key = keys[x]
        #     if str(key).find("cpu") == 0:
        #         paletteColor = self.label_CPU_Total.palette()
        #         paletteColor.setColor(QPalette.WindowText,
        #             QColor(CpuPlot.colors[int(str(key).strip("cpu")) + 1]))
        #         label_CPU = QtGui.QLabel(self.tab_mem)
        #         label_CPU.setGeometry(QtCore.QRect(20 + 100 * (x - 1), 235, 321, 31))
        #         label_CPU.setText(str(key).upper())
        #         label_CPU.setPalette(paletteColor)
        #         self.label_CPU_list.update({str(key):label_CPU})

        # paletteColor = self.label_CPU_Total.palette()
        # paletteColor.setColor(QPalette.WindowText, QColor(CpuPlot.colors[0]))
        # self.label_mem_usage.setPalette(paletteColor)

        # paletteColor = self.label_CPU_Total.palette()
        # paletteColor.setColor(QPalette.WindowText, QColor(CpuPlot.colors[1]))
        # self.label_swap_usage.setPalette(paletteColor)

        self.tableWidget_process.verticalHeader().setVisible(False)
        self.tableWidget_process.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_process.setHorizontalHeaderLabels(
            ["PID".center(10), "PPID".center(10), "Name".center(38), "St.", "Pri.".center(7), "Memory(KB)".center(15)])
        self.tableWidget_process.resizeColumnsToContents()
        self.tableWidget_process.setSortingEnabled(True)

        self.tableWidget_module.verticalHeader().setVisible(False)
        self.tableWidget_module.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_module.setHorizontalHeaderLabels(["Name".center(50), "Memory(KB)".center(15), "Usage"])
        self.tableWidget_module.resizeColumnsToContents()
        self.tableWidget_module.setSortingEnabled(True)

        self.procStat = ProcStat()
        self.statInfo = {}

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1000)

    def __displayInfo(self):
        self.label_CPU_name.setText(self.statInfo["CPUInfo"]["name"])
        self.label_CPU_type.setText(self.statInfo["CPUInfo"]["type"])
        self.label_CPU_freq.setText(self.statInfo["CPUInfo"]["frequency"] + " MHz")
        self.label_OS_type.setText(self.statInfo["OSInfo"]["type"])
        self.label_OS_version.setText(self.statInfo["OSInfo"]["version"])
        self.label_GCC_version.setText(self.statInfo["OSInfo"]["GCCversion"])

    def __poweroff(self):
        pass
    def __reboot(self):
        pass

    def __displayCPU(self):
        # try:
        #     x = numpy.arange(0, 60, 1)
        #     y = x * 0
        #     curve = QwtPlotCurve()
        #     curve.setData(x, y)
        #     curve.attach(self.qwtPlot_CPU)
        # except:
        #     print("Exception: TaskMgr.__displaySources()")
        #     print(sys.exc_info())

        self.progressBar.setProperty("value",float(self.statInfo["CPUUsage"][0]["usage"])*100)
        self.progressBar_2.setProperty("value",float(self.statInfo["CPUUsage"][1]["usage"])*100)
        self.progressBar_3.setProperty("value",float(self.statInfo["CPUUsage"][2]["usage"])*100)
        self.progressBar_4.setProperty("value",float(self.statInfo["CPUUsage"][3]["usage"])*100)

    def __displayProcs(self):
        try:
            row = len(self.statInfo["ProcInfos"])
            self.tableWidget_process.setRowCount(row)
            for x in range(0, row):
                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, int(self.statInfo["ProcInfos"][x]["pid"]))
                self.tableWidget_process.setItem(x, 0, item)

                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, self.statInfo["ProcInfos"][x]["name"])
                self.tableWidget_process.setItem(x, 2, item)

                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, int(self.statInfo["ProcInfos"][x]["ppid"]))
                self.tableWidget_process.setItem(x, 1, item)

                item = QTableWidgetItem(self.statInfo["ProcInfos"][x]["status"])
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget_process.setItem(x, 3, item)
                self.tableWidget_process.setItem(x, 4, QTableWidgetItem(self.statInfo["ProcInfos"][x]["priority"]))

                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, int(self.statInfo["ProcInfos"][x]["memory"]) / 1024)
                self.tableWidget_process.setItem(x, 5, item)

                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, int(self.statInfo["ProcInfos"][x]["res"]) / 1024)
                self.tableWidget_process.setItem(x, 6, item)

                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, int(self.statInfo["ProcInfos"][x]["shr"]) / 1024)
                self.tableWidget_process.setItem(x, 7, item)
        except:
            print("Exception: TaskMgr.__displayProcs()")
            print(sys.exc_info())
        self.label_total.setText(str(self.statInfo["ProcCount"]["Total"]))
        self.label_runable.setText(str(self.statInfo["ProcCount"]["Runnable"]))
        self.label_sleep.setText(str(self.statInfo["ProcCount"]["Sleeping"]))
        self.label_defunct.setText(str(self.statInfo["ProcCount"]["Defunct"]))


    def __displayModules(self):
        try:
            rows = len(self.statInfo["ModuleInfos"])
            self.tableWidget_module.setRowCount(rows)

            for x in range(0, rows):
                self.tableWidget_module.setItem(x, 0, QTableWidgetItem(self.statInfo["ModuleInfos"][x]["name"]))

                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, int(self.statInfo["ModuleInfos"][x]["memory"]))
                self.tableWidget_module.setItem(x, 1, QTableWidgetItem(item))

                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, int(self.statInfo["ModuleInfos"][x]["usage"]))
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget_module.setItem(x, 2, item)
        except:
            print("Exception: TaskMgr.__displayModules()")
            print(sys.exc_info())

    def __displayMem(self):
        pass
        # series = QPieSeries()
        # series.append("Python", 80)
        # series.append("C++", 70)
        # series.append("Java", 50)
        # series.append("C#", 40)
        # series.append("PHP", 30)

        # slice = QPieSlice()
        # slice = series.slices()[2]
        # slice.setExploded(True)
        # slice.setLabelVisible(True)
        # slice.setPen(QPen(Qt.darkGreen, 2))
        # slice.setBrush(Qt.green)

        # slice = QPieSlice()
        # slice = series.slices()[2]
        # slice.setExploded(True)
        # slice.setLabelVisible(True)
        # slice.setPen(QPen(Qt.darkGreen, 2))
        # slice.setBrush(Qt.green)
        # slice = series.slices()[2]

        # chart = QChart()
        # chart.legend().hide()
        # chart.addSeries(series)
        # chart.createDefaultAxes()
        # chart.setAnimationOptions(QChart.SeriesAnimations)
        # chart.setTitle("Pie Chart Example")

        # chart.legend().setVisible(True)
        # chart.legend().setAlignment(Qt.AlignBottom)
        # chart.createDefaultAxes()

        # chart.setAnimationOptions(QChart.SeriesAnimations)
        # chart.setTitle("Pie Chart Example")

        # chartview = QChartView(chart)

        # self.setCentralWidget(chartview)
        # try:
        #     x = numpy.arange(0, 60, 1)
        #     y = x * 0
        #     curve = QwtPlotCurve()
        #     curve.setData(x, y)
        #     curve.attach(self.qwtPlot_memory)
        # except:
        #     print("Exception: TaskMgr.__displaySources()")
        #     print(sys.exc_info())


    def __kill(self):
        rowIndex = self.tableWidget_process.currentRow()
        os.system("kill " + str(self.tableWidget_process.item(rowIndex, 0).data(0)))

    def refresh(self):
        try:
            self.procStat.refresh()
            self.statInfo = {}
            self.statInfo.update({"CPUInfo":self.procStat.getCPUInfo()})
            self.statInfo.update({"MemoryInfo":self.procStat.getMemInfo()})
            self.statInfo.update({"OSInfo":self.procStat.getOSInfo()})
            self.statInfo.update({"CPUUsage":self.procStat.getCPUStat()})
            procInfo_stat = self.procStat.getProcInfos()
            self.statInfo.update({"ProcInfos":procInfo_stat[0]})
            self.statInfo.update({"ProcCount":procInfo_stat[1]})
            self.modInfo_stat = self.procStat.getModuleInfos()
            self.statInfo.update({"ModuleInfos":self.modInfo_stat[0]})
            self.__displayInfo()
            self.__displayCPU()
            self.__displayProcs()
            self.__displayModules()
            self.__displayMem()
        except:
            print("Exception: TaskManager.refresh()")
            print(sys.exc_info())
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = TaskManager()
    form.show()
    app.exec_()
