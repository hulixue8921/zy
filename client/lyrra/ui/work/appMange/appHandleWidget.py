# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'appHandleWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_appHandleWidget(object):
    def setupUi(self, appHandleWidget):
        appHandleWidget.setObjectName("appHandleWidget")
        appHandleWidget.resize(678, 348)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(appHandleWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 100, -1)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(appHandleWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.appNameComboBox = QtWidgets.QComboBox(appHandleWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.appNameComboBox.sizePolicy().hasHeightForWidth())
        self.appNameComboBox.setSizePolicy(sizePolicy)
        self.appNameComboBox.setObjectName("appNameComboBox")
        self.horizontalLayout.addWidget(self.appNameComboBox)
        self.label_2 = QtWidgets.QLabel(appHandleWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.envNameComboBox = QtWidgets.QComboBox(appHandleWidget)
        self.envNameComboBox.setObjectName("envNameComboBox")
        self.horizontalLayout.addWidget(self.envNameComboBox)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(appHandleWidget)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.verticalHeader().setDefaultSectionSize(60)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(appHandleWidget)
        QtCore.QMetaObject.connectSlotsByName(appHandleWidget)

    def retranslateUi(self, appHandleWidget):
        _translate = QtCore.QCoreApplication.translate
        appHandleWidget.setWindowTitle(_translate("appHandleWidget", "app操作"))
        self.label.setText(_translate("appHandleWidget", "appName:"))
        self.label_2.setText(_translate("appHandleWidget", "envName:"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("appHandleWidget", "应用名称"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("appHandleWidget", "环境名称"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("appHandleWidget", "git版本号"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("appHandleWidget", "操作"))
