from lyrra.share.mySocket import MySocket
from PyQt5.Qt import *
from lyrra.ui.work.sysMange.userMange.userWidget import Ui_userWidget
from lyrra.ui.work.sysMange.userMange.handleUser import Ui_handleUserWidget
from lyrra.ui.work.sysMange.userMange.updateUserWidget import Ui_updateUserWidget
from lyrra.ui.work.sysMange.userMange.changeWidget import Ui_changePasswdWidget


class User(Ui_userWidget):
    def __init__(self, main, widget):
        super().__init__()
        self.main = main
        self.widget = widget
        self.tempWidget = None
        self.temp =None
        self.selectRow=None

    def setupUi(self):
        super().setupUi(self.widget)

    def clearAll(self):
        # 修护bug ,取消排序，再清除表单数据，bug: 排序后，不能更新table ?
        self.listUserWidgeUserTable.setSortingEnabled(False)
        self.listUserWidgeUserTable.clearContents()
        self.listUserWidgeUserTable.setRowCount(0)

    def getData(self):
        sentData = {"model": "user", "api": "listUsers"}
        sentData['token'] = self.main.token
        try:
            server = MySocket()
            result = server.send(sentData)
        except Exception:
            QMessageBox.information(self.widget, '提示信息', "网络不可达")
        else:
            if result['code'] == 200:
                for i, data in enumerate(result['users']):
                    row = self.listUserWidgeUserTable.rowCount()
                    self.listUserWidgeUserTable.insertRow(row)
                    self.listUserWidgeUserTable.setItem(row, 0, QTableWidgetItem(str(data['id'])))
                    self.listUserWidgeUserTable.setItem(row, 1, QTableWidgetItem(data['username']))
                    self.listUserWidgeUserTable.setItem(row, 2, QTableWidgetItem(str(data['roleId'])))
                    self.listUserWidgeUserTable.setItem(row, 3, QTableWidgetItem(data['roleName']))

                    widget = QWidget()
                    handleUser = Ui_handleUserWidget()
                    handleUser.setupUi(widget)
                    self.listUserWidgeUserTable.setCellWidget(row, 4, widget)
                    handleUser.delUserButton.clicked.connect(self.delUser)
                    handleUser.updateUserButton.clicked.connect(self.updateUser)
                    handleUser.changePasswdButton.clicked.connect(self.changePasswd)
                self.listUserWidgeUserTable.setSortingEnabled(True)
            elif result['code'] == 402:
                QMessageBox.information(self.widget, "提示信息", "token已过期， 请重新登陆")
                self.widget.deleteLater()
                self.main.tokenTimeout()
            else:
                QMessageBox.information(self.widget, '提示信息', result['message'])

    def delUser(self):
        button = self.widget.sender()
        if button:
            # 确定位置的时候这里是关键
            row = self.listUserWidgeUserTable.indexAt(button.parent().pos()).row()
            sentData = {"model": "user", "api": "delUser"}
            sentData["userId"] = self.listUserWidgeUserTable.item(row, 0).text()
            sentData['token'] = self.main.token
            server = MySocket()
            result = server.send(sentData)
            if result['code'] == 200:
                self.listUserWidgeUserTable.removeRow(row)
            elif result['code'] == 402:
                QMessageBox.information(self.widget, "提示信息", "token已过期， 请重新登陆")
                self.widget.deleteLater()
                self.main.tokenTimeout()

    def updateUser(self):
        self.Roles=None
        def getRole():
            sentData = {"model": "user", "api": "listRoles"}
            sentData['token'] = self.main.token
            try:
                server = MySocket()
                result = server.send(sentData)
            except Exception:
                QMessageBox.information(self.widget, "提示信息", "网络不可达")
            else:
                if result['code'] == 200:
                    self.Roles=result
                    return result
                elif result['code'] == 402:
                    QMessageBox.information(self.widget, "提示信息", "token已过期， 请重新登陆")
                    self.widget.deleteLater()
                    self.main.tokenTimeout()

        def cacleFun():
            self.tempWidget.deleteLater()

        def sureFun():
            sentData = {"model": "user", "api": "updateUser"}
            sentData['token'] = self.main.token
            sentData["userId"] = self.listUserWidgeUserTable.item(self.selectRow, 0).text()
            sentData["username"] = self.temp.userLine.text()
            for item in self.Roles['roles']:
                if item["roleName"] == self.temp.roleComboBox.currentText():
                    sentData["roleId"] = item["roleId"]
            try:
                server = MySocket()
                result = server.send(sentData)
            except Exception:
                QMessageBox.information(self.widget, "提示信息", "网络不可达")
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

        button = self.widget.sender()
        if button:
            self.selectRow = self.listUserWidgeUserTable.indexAt(button.parent().pos()).row()
            # 生成修改用户页面
            self.tempWidget = QWidget()
            self.temp=Ui_updateUserWidget()
            self.temp.setupUi(self.tempWidget)
            self.tempWidget.show()
            self.temp.userLine.setText(self.listUserWidgeUserTable.item(self.selectRow, 1).text())
            roles=getRole()
            for i in roles['roles']:
                self.temp.roleComboBox.addItem(i['roleName'])
            self.temp.cacleButton.clicked.connect(cacleFun)
            self.temp.sureButton.clicked.connect(sureFun)

    def changePasswd(self):
        def cacleFun():
            self.tempWidget.deleteLater()

        def sureFun():
            try:
                sentData = {"model": "user", "api": "changePasswd"}
                sentData['token'] = self.main.token
                sentData['passwd'] = self.temp.passwdLine.text()
                sentData['userId'] = self.listUserWidgeUserTable.item(self.selectRow, 0).text()
                server = MySocket()
                result = server.send(sentData)
            except Exception:
                QMessageBox.information(self.widget, "提示信息", "网络不可达")
            else:
                if result['code'] == 200:
                    self.tempWidget.deleteLater()
                elif result['code'] == 402:
                    QMessageBox.information(self.widget, "提示信息", "token已过期， 请重新登陆")
                    self.tempWidget.deleteLater()
                    self.widget.deleteLater()
                    self.main.tokenTimeout()

        button = self.widget.sender()
        if button:
            self.selectRow = self.listUserWidgeUserTable.indexAt(button.parent().pos()).row()
            self.tempWidget=QWidget()
            self.temp=Ui_changePasswdWidget()
            self.temp.setupUi(self.tempWidget)
            self.tempWidget.show()
            self.temp.cacelButton.clicked.connect(cacleFun)
            self.temp.sureButton.clicked.connect(sureFun)

