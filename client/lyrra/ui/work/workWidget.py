# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'workWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_workWidget(object):
    def setupUi(self, workWidget):
        workWidget.setObjectName("workWidget")
        workWidget.resize(1108, 596)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(workWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.workLay = QtWidgets.QHBoxLayout()
        self.workLay.setSpacing(6)
        self.workLay.setObjectName("workLay")
        self.workWidgeTree = QtWidgets.QTreeWidget(workWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.workWidgeTree.sizePolicy().hasHeightForWidth())
        self.workWidgeTree.setSizePolicy(sizePolicy)
        self.workWidgeTree.setObjectName("workWidgeTree")
        self.workWidgeTree.headerItem().setText(0, "1")
        self.workWidgeTree.header().setVisible(False)
        self.workLay.addWidget(self.workWidgeTree)
        self.workWidgetStack = QtWidgets.QStackedWidget(workWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.workWidgetStack.sizePolicy().hasHeightForWidth())
        self.workWidgetStack.setSizePolicy(sizePolicy)
        self.workWidgetStack.setObjectName("workWidgetStack")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.workWidgetStack.addWidget(self.page)
        self.workStackUsersMangeWidget = QtWidgets.QWidget()
        self.workStackUsersMangeWidget.setObjectName("workStackUsersMangeWidget")
        self.workWidgetStack.addWidget(self.workStackUsersMangeWidget)
        self.workStackRolesMangeWidge = QtWidgets.QWidget()
        self.workStackRolesMangeWidge.setObjectName("workStackRolesMangeWidge")
        self.workWidgetStack.addWidget(self.workStackRolesMangeWidge)
        self.workStackListAppWidge = QtWidgets.QWidget()
        self.workStackListAppWidge.setObjectName("workStackListAppWidge")
        self.workWidgetStack.addWidget(self.workStackListAppWidge)
        self.workStackHandleAppWidget = QtWidgets.QWidget()
        self.workStackHandleAppWidget.setObjectName("workStackHandleAppWidget")
        self.workWidgetStack.addWidget(self.workStackHandleAppWidget)
        self.p3 = QtWidgets.QWidget()
        self.p3.setObjectName("p3")
        self.workWidgetStack.addWidget(self.p3)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.workWidgetStack.addWidget(self.page_3)
        self.workLay.addWidget(self.workWidgetStack)
        self.workLay.setStretch(0, 2)
        self.workLay.setStretch(1, 8)
        self.verticalLayout.addLayout(self.workLay)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(workWidget)
        QtCore.QMetaObject.connectSlotsByName(workWidget)

    def retranslateUi(self, workWidget):
        _translate = QtCore.QCoreApplication.translate
        workWidget.setWindowTitle(_translate("workWidget", "运维工作台"))
