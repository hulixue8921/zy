# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addRoleWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addRoleWidget(object):
    def setupUi(self, addRoleWidget):
        addRoleWidget.setObjectName("addRoleWidget")
        addRoleWidget.resize(502, 335)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(addRoleWidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(addRoleWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.addRoleLine = QtWidgets.QLineEdit(addRoleWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addRoleLine.sizePolicy().hasHeightForWidth())
        self.addRoleLine.setSizePolicy(sizePolicy)
        self.addRoleLine.setObjectName("addRoleLine")
        self.horizontalLayout.addWidget(self.addRoleLine)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cacelButton = QtWidgets.QPushButton(addRoleWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cacelButton.sizePolicy().hasHeightForWidth())
        self.cacelButton.setSizePolicy(sizePolicy)
        self.cacelButton.setObjectName("cacelButton")
        self.horizontalLayout_2.addWidget(self.cacelButton)
        self.sureButton = QtWidgets.QPushButton(addRoleWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sureButton.sizePolicy().hasHeightForWidth())
        self.sureButton.setSizePolicy(sizePolicy)
        self.sureButton.setObjectName("sureButton")
        self.horizontalLayout_2.addWidget(self.sureButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(addRoleWidget)
        QtCore.QMetaObject.connectSlotsByName(addRoleWidget)

    def retranslateUi(self, addRoleWidget):
        _translate = QtCore.QCoreApplication.translate
        addRoleWidget.setWindowTitle(_translate("addRoleWidget", "新增角色"))
        self.label.setText(_translate("addRoleWidget", "角色名"))
        self.cacelButton.setText(_translate("addRoleWidget", "取消"))
        self.sureButton.setText(_translate("addRoleWidget", "确定"))
