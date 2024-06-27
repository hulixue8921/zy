import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QToolBox, QToolButton,
                             QGroupBox, QVBoxLayout, QHBoxLayout)
from test import Ui_Form
import random
import numpy as np
import pyqtgraph as pg
import time
from datetime import datetime
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph


class MyStringAxis(pg.AxisItem):
    def __init__(self, xdict, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)
        self.x_values = np.asarray(xdict.keys())
        self.x_strings = xdict.values()

    def tickStrings(self, values, scale, spacing):
        strings = []
        for v in values:
            # vs is the original tick value
            vs = v * scale
            # if we have vs in our values, show the string
            # otherwise show nothing
            if vs in self.x_values:
                # Find the string with x_values closest to vs
                vstr = self.x_strings[np.abs(self.x_values - vs).argmin()]
            else:
                vstr = ""
            strings.append(vstr)
        print(strings)
        #return ["a" , "b", "c","d", "e","f"]
        return strings


x = ['a', 'b', 'c', 'd', 'e', 'f']
y = [1, 2, 3, 4, 5, 6]
xdict = dict(enumerate(x))



app = QApplication(sys.argv)
w = QWidget()
win = Ui_Form()
win.setupUi(w)
w.show()

stringaxis = MyStringAxis(xdict, orientation='bottom')
plot=win.p1.addPlot(axisItems={'bottom': stringaxis})
plot.plot(list(xdict.keys()),y)

sys.exit(app.exec())