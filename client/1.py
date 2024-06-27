import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QToolBox, QToolButton,
                             QGroupBox, QVBoxLayout, QHBoxLayout)

from test import Ui_Form
import random
import numpy as np
import pyqtgraph as pg

pg.setConfigOptions(antialias=True)
pg.setConfigOptions(leftButtonPan=False, antialias=True)

app = QApplication(sys.argv)
w = QWidget()
win = Ui_Form()
win.setupUi(w)

label = pg.LabelItem(justify='right')
win.p1.addPlot(title="Basic array plotting", y=np.random.normal(size=100))
p2 = win.p1.addPlot(title="Multiple curves")
p2.plot(np.random.normal(size=100), pen=(255, 0, 0), name="Red curve")
p2.plot(np.random.normal(size=110) + 5, pen=(0, 255, 0), name="Green curve")
x=p2.plot(np.random.normal(size=120) + 10, pen=(0, 0, 255), name="Blue curve")
x.setData(np.random.normal(size=120) + 20)
p2.setLabel("left", "xxxx")

win.p1.nextRow()
p3 = win.p1.addPlot(title="Drawing with points")
p3.plot(y=[1, 2, 3, 5, 8, 1, 2], pen='r')
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
p3.addItem(vLine, ignoreBounds=True)
p3.addItem(hLine, ignoreBounds=True)
win.p1.addItem(label)

vb = p3.vb

def mouseMoved(evt):
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    if p3.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        index = int(mousePoint.x())
        label.setText(
            "<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (
            mousePoint.x(), 2, 1))
        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())



proxy = pg.SignalProxy(p3.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

w.show()
sys.exit(app.exec())
