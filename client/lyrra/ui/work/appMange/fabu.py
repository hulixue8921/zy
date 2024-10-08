from lyrra.ui.work.appMange.fabuWidget import Ui_fabuWidget
from lyrra.share.mySocket import MySocket
from PyQt5.Qt import *
from threading import Thread


class MySignal(QObject):
    t = pyqtSignal(str)
    d= pyqtSignal()


class Fabu(Ui_fabuWidget):
    def __init__(self, main, widget, projectName, appName, fabuId, envName):
        super().__init__()
        self.main = main
        self.widget = widget
        self.projectName = projectName
        self.appName = appName
        self.fabuId = fabuId
        self.envName = envName
        self.branch = None
        self.tag = None
        self.git = None
        self.gitProjectInfo = None
        self.mySignal = MySignal()
        self.setupUi(self.widget)
        self.mySignal.t.connect(self.info)
        self.mySignal.d.connect(self.d)
        self.comboBox.currentTextChanged.connect(self.initData)
        self.gitCombox.currentTextChanged.connect(self.gitBoxChangeFun)
        self.cacelButton.clicked.connect(self.cacelFun)
        self.sureButton.clicked.connect(self.sureFun)
        self.widget.setWindowTitle(appName + ":" + envName + ":" + "发布")

    def initData(self):
        self.initLineFun()
        self.initComboxFun()
        selectGit = self.comboBox.currentText()
        if selectGit == "git分支":
            sentData = {'model': 'gitlab', 'api': 'listBranch'}
            sentData['gitProject'] = self.projectName
            try:
                server = MySocket()
                result = server.send(sentData)
                self.gitProjectInfo = result
            except Exception as e:
                QMessageBox.information(self.widget, "提示信息", "网络中断")

            else:
                for i in result['project']:
                    self.gitCombox.addItem(i['name'])
                    self.git = i['git']

        elif selectGit == "gitTag":
            sentData = {'model': 'gitlab', 'api': 'listTag'}
            sentData['gitProject'] = self.projectName
            try:
                server = MySocket()
                result = server.send(sentData)
                self.gitProjectInfo = result
            except Exception:
                QMessageBox.information(self.widget, "提示信息", "网络中断")
            else:
                for i in result['project']:
                    self.gitCombox.addItem(i['name'])
                    self.git = i['git']

    def initComboxFun(self):
        self.gitCombox.clear()

    def initLineFun(self):
        self.gitLine.clear()

    def cacelFun(self):
        self.widget.deleteLater()

    def sureFun(self):
        gitAddress = self.git
        gitInfo = self.gitCombox.currentText()
        sentData = {'model': 'app', "api": "fabu"}
        sentData['token'] = self.main.token
        sentData['fabuId'] = self.fabuId
        sentData['gitAddress'] = gitAddress
        sentData['gitCommit'] = gitInfo

        def fun():
            try:
                self.mySignal.d.emit()
                server = MySocket()
                result = server.send(sentData)
            except Exception:
                QMessageBox.information(self.widget, "提示信息", "网络中断")
            else:
                self.mySignal.t.emit(result['message'])


        t1 = Thread(target=fun)
        t1.start()

    def gitBoxChangeFun(self):
        name = self.gitCombox.currentText()
        for i in self.gitProjectInfo['project']:
            if name == i['name']:
                self.gitLine.setText(i['message'])

    def info(self, message):
        QMessageBox.information(self.main.workWidget, "提示信息", message)
        if message == "token问题或过期":
            self.main.tokenTimeout()

    def d(self):
        self.widget.deleteLater()
