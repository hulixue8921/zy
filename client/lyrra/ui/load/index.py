from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from lyrra.share.mySocket import MySocket
from lyrra.ui.load.indexWidget import Ui_indexWidget


class Index(Ui_indexWidget):
    username = None
    passwd = None

    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setupUi(self.main.indexWidget)
        self.indexWidgeUserLine.setPlaceholderText("请输入用户名")
        self.indexWidgePasswdLine.setPlaceholderText("请输入密码")

        if Index.username and Index.passwd:
            self.indexWidgeUserLine.setText(Index.username)
            self.indexWidgePasswdLine.setText(Index.passwd)
        self.signal()

    def signal(self):
        self.indexWidgeLoadButton.clicked.connect(self.load)
        self.indexWidgeRegButton.clicked.connect(self.reg)
        self.indexWidgePasswdEcho.clicked.connect(self.passwdCheckFun)

    def load(self):
        user = self.indexWidgeUserLine.text()
        passwd = self.indexWidgePasswdLine.text()
        data = {"model": "user", 'api': "load"}
        data['username'] = user
        data['passwd'] = passwd

        if len(user) == 0:
            self.indexWidgeUserLine.setFocus(True)
            QMessageBox.information(self.main.indexWidget, '提示信息', "请输入用户名密码")
            return
        elif len(passwd) == 0:
            QMessageBox.information(self.main.indexWidget, '提示信息', "请输入用户名密码")
            self.indexWidgePasswdLine.setFocus(True)
            return
        try:
            server = MySocket()
            result = server.send(data)
        except Exception:
            QMessageBox.information(self.main.indexWidget, '提示信息', "网络不可达")
        else:
            if result['code'] == 200:
                Index.username = user
                Index.passwd = passwd
                self.main.indexWidget.deleteLater()
                self.main.memTree = result['mem']
                self.main.token = result['token']
                self.main.createWork()
            else:
                QMessageBox.information(self.main.indexWidget, '提示信息', result['message'])

    def reg(self):
        user = self.indexWidgeUserLine.text()
        passwd = self.indexWidgePasswdLine.text()
        data = {"model": "user", 'api': "reg"}
        data['username'] = user
        data['passwd'] = passwd
        if len(user) == 0:
            self.indexWidgeUserLine.setFocus(True)
            QMessageBox.information(self.main.indexWidget, '提示信息', "请输入用户名密码")
            return
        elif len(passwd) == 0:
            QMessageBox.information(self.main.indexWidget, '提示信息', "请输入用户密码")
            self.indexWidgePasswdLine.setFocus(True)
            return
        try:
            server = MySocket()
            result = server.send(data)
        except Exception:
            QMessageBox.information(self.main.indexWidget, '提示信息', "网络不可达")
        else:
            if result['code'] == 200:
                Index.username = user
                Index.passwd = passwd
                self.main.indexWidget.deleteLater()
                self.main.createWork()
            else:
                QMessageBox.information(self.main.indexWidget, '提示信息', result['message'])

    def passwdCheckFun(self):
        if self.indexWidgePasswdEcho.isChecked() is True:
            self.indexWidgePasswdLine.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.indexWidgePasswdLine.setEchoMode(QtWidgets.QLineEdit.Password)
