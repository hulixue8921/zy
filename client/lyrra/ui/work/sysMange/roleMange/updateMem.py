from lyrra.ui.work.sysMange.roleMange.updateMemWidget import Ui_updateMemWidget
from lyrra.share.mySocket import MySocket
from PyQt5.Qt import *


class UpdateMem(Ui_updateMemWidget):
    def __init__(self, main, widget, roleId,roleName):
        super().__init__()
        self.main = main
        self.widget = widget
        self.roleId = roleId
        self.roleName=roleName
        self.allMems = None
        self.ownMems = None
        self.setupUi(self.widget)
        self.initData()
        self.roleNameLabel.setText(self.roleName)
        self.addToolButton.setArrowType(Qt.RightArrow)
        self.delToolButton.setArrowType(Qt.LeftArrow)
        self.addToolButton.clicked.connect(self.addFun)
        self.delToolButton.clicked.connect(self.delFun)
        self.cacelButton.clicked.connect(self.cacelFun)
        self.sureButton.clicked.connect(self.sureFun)

    def initData(self):
        sentData = {"model": "user", "api": "listMems"}
        sentData['token'] = self.main.token
        try:
            server = MySocket()
            self.allMems = server.send(sentData)
        except:
            QMessageBox.information(self.widget, '提示信息', "网络不可达")


        sentData = {"model": "user", "api": "roleOwnMem"}
        sentData['token'] = self.main.token
        sentData['roleId'] = self.roleId
        try:
            server = MySocket()
            self.ownMems = server.send(sentData)
        except:
            QMessageBox.information(self.widget, '提示信息', "网络不可达")

        data = []
        data1 = []
        for i in self.ownMems['mems']:
            data1.append(i['value'])

        for i in self.allMems['mems']:
            if i['memValue'] in data1:
                pass
            else:
                data.append(i['memValue'])

        for i in data:
            self.allMemList.addItem(i)

        for i in self.ownMems['mems']:
            self.ownMemList.addItem(i['value'])

    def addFun(self):
        data1 = []
        for i in range(self.allMemList.count()):
            data1.append(self.allMemList.item(i).text())

        try:
            x = self.allMemList.currentItem().text()
        except Exception:
            QMessageBox.information(self.widget, '提示信息', '在"未有的菜单栏"请选择')
        else:
            data1.remove(x)
            self.allMemList.clear()
            self.ownMemList.addItem(x)
            for i in data1:
                self.allMemList.addItem(i)

    def delFun(self):
        data2 = []
        for i in range(self.ownMemList.count()):
            data2.append(self.ownMemList.item(i).text())
        try:
            x = self.ownMemList.currentItem().text()
        except Exception:
            QMessageBox.information(self.widget, '提示信息', '在"拥有的菜单栏"请选择')
        else:
            self.allMemList.addItem(x)
            data2.remove(x)
            self.ownMemList.clear()
            for i in data2:
                self.ownMemList.addItem(i)


    def cacelFun(self):
        self.widget.deleteLater()

    def sureFun(self):
        data = []
        sentData = {"model": "user", "api": "roleMem"}
        sentData['token'] = self.main.token
        sentData['memIds'] = data
        sentData['roleId'] = self.roleId
        for i in range(self.ownMemList.count()):
            x = self.ownMemList.item(i).text()
            for I in self.allMems['mems']:
                if x == I['memValue']:
                    data.append(I['memId'])
        try:
            server = MySocket()
            result = server.send(sentData)
        except:
            QMessageBox.information(self.widget, '提示信息', "网络不可达")
        else:
            self.widget.deleteLater()
