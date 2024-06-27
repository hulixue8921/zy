from lyrra.ui.work.sysMange.roleMange.roleMangleWidget import Ui_roleMangeWidget
from lyrra.ui.work.sysMange.roleMange.handleWidget import Ui_handleWidget
from lyrra.ui.work.sysMange.roleMange.addRoleWidget import Ui_addRoleWidget
from lyrra.ui.work.sysMange.roleMange.updateMem import UpdateMem
from lyrra.ui.work.appMange.fabuRight import FabuRight
from lyrra.share.mySocket import MySocket
from PyQt5.Qt import *


class RoleMangle(Ui_roleMangeWidget):
    def __init__(self, main, widget):
        super().__init__()
        self.main = main
        self.widget = widget
        self.setupUi(self.widget)
        self.addRoleButton.clicked.connect(self.addRoleFun)
        self.tempWidget = None
        self.temp = None
        self.selectRow = None

    def clearAll(self):
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

    def getData(self):
        sentData = {"model": "user", "api": "listRoles"}
        sentData['token'] = self.main.token
        try:
            server = MySocket()
            result = server.send(sentData)
        except Exception:
            QMessageBox.information(self.widget, '提示信息', "网络不可达")
        else:
            if result['code'] == 200:
                for i, data in enumerate(result['roles']):
                    row = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row)
                    self.tableWidget.setItem(row, 0, QTableWidgetItem(str(data['roleId'])))
                    self.tableWidget.setItem(row, 1, QTableWidgetItem(data['roleName']))

                    widget = QWidget()
                    handleRole = Ui_handleWidget()
                    handleRole.setupUi(widget)
                    self.tableWidget.setCellWidget(row, 2, widget)

                    handleRole.updateMemButton.clicked.connect(self.updateMemFun)
                    handleRole.delRoleButton.clicked.connect(self.delRoleFun)
                    handleRole.updateFabuButton.clicked.connect(self.updateFabuFun)

                self.tableWidget.setSortingEnabled(True)
            elif result['code'] == 402:
                QMessageBox.information(self.widget, "提示信息", "token已过期， 请重新登陆")
                self.widget.deleteLater()
                self.main.tokenTimeout()
            else:
                QMessageBox.information(self.widget, '提示信息', result['message'])

    def updateFabuFun(self):
        button = self.widget.sender()
        row = self.tableWidget.indexAt(button.parent().pos()).row()
        roleId = self.tableWidget.item(row, 0).text()
        roleName = self.tableWidget.item(row, 1).text()
        self.tempWidget = QWidget()
        self.temp = FabuRight(self.main, self.tempWidget, roleId, roleName)
        self.tempWidget.show()

    def updateMemFun(self):
        button = self.widget.sender()
        row = self.tableWidget.indexAt(button.parent().pos()).row()
        roleId = self.tableWidget.item(row, 0).text()
        roleName = self.tableWidget.item(row, 1).text()
        self.tempWidget = QWidget()
        self.temp = UpdateMem(self.main, self.tempWidget, roleId, roleName)
        self.tempWidget.show()

    def delRoleFun(self):
        button = self.widget.sender()
        if button:
            self.row = self.tableWidget.indexAt(button.parent().pos()).row()
            sentData = {"model": "user", "api": "delRole"}
            sentData["roleId"] = self.tableWidget.item(self.row, 0).text()
            sentData['token'] = self.main.token
            server = MySocket()
            result = server.send(sentData)
            print(result)
            if result['code'] == 200:
                self.tableWidget.removeRow(self.row)
            elif result['code'] == 402:
                QMessageBox.information(self.widget, "提示信息", "token已过期， 请重新登陆")
                self.widget.deleteLater()
                self.main.tokenTimeout()

    def addRoleFun(self):
        def cacleFun():
            self.tempWidget.deleteLater()

        def sureFun():
            sentData = {"model": "user", "api": "addRole"}
            sentData['token'] = self.main.token
            sentData['roleName'] = self.temp.addRoleLine.text()
            try:
                server = MySocket()
                result = server.send(sentData)
            except Exception:
                QMessageBox.information(self.widget, '提示信息', "网络不可达")
            else:
                if result['code'] == 200:
                    self.tempWidget.deleteLater()
                    self.clearAll()
                    self.getData()
                elif result['code'] == 402:
                    QMessageBox.information(self.widget, "提示信息", "token已过期， 请重新登陆")
                    self.tempWidget.deleteLater()
                    self.widget.deleteLater()
                    self.main.tokenTimeout()

        self.tempWidget = QWidget()
        self.temp = Ui_addRoleWidget()
        self.temp.setupUi(self.tempWidget)
        self.tempWidget.show()
        self.temp.cacelButton.clicked.connect(cacleFun)
        self.temp.sureButton.clicked.connect(sureFun)
