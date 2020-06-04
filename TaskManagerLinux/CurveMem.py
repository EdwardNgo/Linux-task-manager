import os
import sys
import numpy as np

from qwt.qt.QtGui import (QApplication, QColor, QBrush, QWidget, QVBoxLayout,
                          QLabel,QPen)
from qwt.qt.QtCore import QRect, QTime
from qwt.qt.QtCore import Qt
from qwt import (QwtPlot, QwtPlotMarker, QwtScaleDraw, QwtLegend, QwtPlotCurve,
                 QwtPlotItem, QwtLegendData, QwtText, QwtPlotGrid )


class MemStat:
    @staticmethod
    def statistic():
        values = {}
        for line in open("/proc/meminfo"):
            words = line.split(":")
            if words[0].find("MemTotal") != -1:
                memTotal = float(words[1].strip().split()[0])
                values.update({"MemTotal":memTotal})
                continue
            if words[0].find("MemFree") != -1:
                memFree = float(words[1].strip().split()[0])
                values.update({"MemFree":memFree})
                continue
            if words[0].find("SwapTotal") != -1:
                swapTotal = float(words[1].strip().split()[0])
                values.update({"SwapTotal":swapTotal})
                continue
            if words[0].find("SwapFree") != -1:
                swapFree = float(words[1].strip().split()[0])
                values.update({"SwapFree":swapFree})
                continue
        values.update({"MemUsage":str(100 * (memTotal - memFree) / memTotal)})
        values.update({"SwapUsage":str(100 * (swapTotal - swapFree) / swapTotal)})
        return values


# class CpuPieMarker(QwtPlotMarker):
#     def __init__(self, *args):
#         QwtPlotMarker.__init__(self, *args)
#         self.setZ(1000.0)
#         self.setRenderHint(QwtPlotItem.RenderAntialiased, True)

#     def rtti(self):
#         return QwtPlotItem.Rtti_PlotUserItem

#     def draw(self, painter, xMap, yMap, rect):
#         margin = 5
#         pieRect = QRect()
#         pieRect.setX(rect.x() + margin)
#         pieRect.setY(rect.y() + margin)
#         pieRect.setHeight(yMap.transform(80.0))
#         pieRect.setWidth(pieRect.height())

#         angle = 3*5760/4
#         for key in ["User", "System", "Idle"]:
#             curve = self.plot().cpuPlotCurve(key)
#             if curve.dataSize():
#                 value = int(5760*curve.sample(0).y()/100.0)
#                 painter.save()
#                 painter.setBrush(QBrush(curve.pen().color(),
#                                               Qt.SolidPattern))
#                 painter.drawPie(pieRect, -angle, -value)
#                 painter.restore()
#                 angle += value


# class TimeScaleDraw(QwtScaleDraw):
#     def __init__(self, baseTime, *args):
#         QwtScaleDraw.__init__(self, *args)
#         self.baseTime = baseTime

#     def label(self, value):
#         upTime = self.baseTime.addSecs(int(value))
#         return QwtText(upTime.toString())


# class Background(QwtPlotItem):
#     def __init__(self):
#         QwtPlotItem.__init__(self)
#         self.setZ(0.0)

#     def rtti(self):
#         return QwtPlotItem.Rtti_PlotUserItem

#     def draw(self, painter, xMap, yMap, rect):
#         c = QColor(Qt.white)
#         r = QRect(rect)

#         for i in range(100, 0, -10):
#             r.setBottom(yMap.transform(i - 10))
#             r.setTop(yMap.transform(i))
#             painter.fillRect(r, c)
#             c = c.darker(110)


class MemoryCurve(QwtPlotCurve):

    def __init__(self, *args):
        QwtPlotCurve.__init__(self, *args)
        self.setRenderHint(QwtPlotItem.RenderAntialiased)

    # __init__()

    def setColor(self, color):
        c = QColor(color)
        self.setPen(c)


HISTORY = 60

class MemPlot(QwtPlot):
    colors  = [Qt.red, Qt.blue, Qt.darkGreen,
               Qt.darkYellow, Qt.darkRed, Qt.darkGray,
               Qt.green, Qt.darkMagenta, Qt.darkCyan,
               Qt.darkBlue, Qt.gray, Qt.cyan,
               Qt.lightGray, Qt.magenta, Qt.black,
               Qt.white, Qt.yellow, Qt.transparent]
    def __init__(self, *args):
        QwtPlot.__init__(self, *args)

        self.curves = {}
        self.data = {}
        self.timeData = 1.0 * np.arange(0, HISTORY, 1)
        self.MemStat = MemStat()

        self.setAutoReplot(False)

        self.plotLayout().setAlignCanvasToScales(True)
        self.setAxisScale(QwtPlot.xBottom, HISTORY, 0)
        self.setAxisScale(QwtPlot.yLeft, 0, 100)
        self.setAxisLabelAlignment(
            QwtPlot.xBottom, Qt.AlignLeft | Qt.AlignBottom)

        grid = QwtPlotGrid()
        grid.enableXMin(True)
        grid.enableYMin(True)
        grid.setMajPen(QPen(Qt.black, 0, Qt.DotLine));
        grid.setMinPen(QPen(Qt.gray, 0 , Qt.DotLine));

        grid.attach(self)

        stat = MemStat.statistic()

        self.data["MemTotal"] = np.zeros(HISTORY, float)
        self.data["MemFree"] = np.zeros(HISTORY, float)
        self.data["SwapTotal"] = np.zeros(HISTORY, float)
        self.data["SwapFree"] = np.zeros(HISTORY, float)

        curve = MemoryCurve("Memory")
        curve.setColor(self.colors[0])
        curve.attach(self)
        self.curves["Memory"] = curve
        self.data["Memory"] = np.zeros(HISTORY, float)

        curve = MemoryCurve("Swap")
        curve.setColor(self.colors[1])
        curve.attach(self)
        self.curves["Swap"] = curve
        self.data["Swap"] = np.zeros(HISTORY, float)

        self.startTimer(1000)
        self.replot()

    def timerEvent(self, e):
        for data in self.data.values():
            data[1:] = data[0:-1]

        stat = MemStat.statistic()
        self.data["MemTotal"][0] = stat["MemTotal"]
        self.data["MemFree"][0] = stat["MemFree"]
        self.data["SwapTotal"][0] = stat["SwapTotal"]
        self.data["SwapFree"][0] = stat["SwapFree"]

        self.data["Memory"][0] = stat["MemUsage"]
        self.curves["Memory"].setData(self.timeData, self.data["Memory"])

        self.data["Swap"][0] = stat["SwapUsage"]
        self.curves["Swap"].setData(self.timeData, self.data["Swap"])

        self.replot()

    def showCurve(self, item, on, index=None):
        item.setVisible(on)
        self.legend().legendWidget(item).setChecked(on)
        self.replot()

    def memoryPlotCurve(self, key):
        return self.curves[key]


def make():
    demo = QWidget()
    demo.setWindowTitle('Cpu Plot')

    plot = MemPlot(demo)
    plot.setTitle("History")

    label = QLabel("Press the legend to en/disable a curve", demo)

    layout = QVBoxLayout(demo)
    layout.addWidget(plot)
    layout.addWidget(label)

    demo.resize(600, 400)
    demo.show()
    return demo


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = make()
    sys.exit(app.exec_())
