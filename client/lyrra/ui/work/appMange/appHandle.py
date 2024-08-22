from lyrra.share.mySocket import MySocket
from lyrra.ui.work.appMange.appHandleWidget import Ui_appHandleWidget
from lyrra.ui.work.appMange.appHandleButtons import Ui_appHandleButtons
from lyrra.ui.work.appMange.fabu import Fabu
from PyQt5.Qt import *


class AppHandle(Ui_appHandleWidget):
    def __init__(self, main, widget):
        super().__init__()
        self.main = main
        self.widget = widget
        self.setupUi(self.widget)
        self.fabus = None
        self.tmpWidget = None
        self.tmp = None
        self.appNameComboBox.currentTextChanged.connect(self.appChange)
        self.envNameComboBox.currentTextChanged.connect(self.envChange)

    def initData(self):
        self.appNameComboBox.clear()
        self.envNameComboBox.clear()
        self.initTable()
        self.appNameComboBox.currentTextChanged.disconnect()
        self.envNameComboBox.currentTextChanged.disconnect()
        sentData = {"model": "app", 'api': "listMyFabu"}
        sentData['token'] = self.main.token
        try:
            server = MySocket()
            result = server.send(sentData)
        except Exception:
            pass
        else:
            self.fabus = result
            self.appNameComboBox.currentTextChanged.connect(self.appChange)
            self.envNameComboBox.currentTextChanged.connect(self.envChange)
            self.setAppBox()
            self.setEnvBox()

    def setAppBox(self):
        data = []
        for fabu in self.fabus['fabu']:
            data.append(fabu['appName'])
        data = set(data)
        for i in data:
            self.appNameComboBox.addItem(i)

    def setEnvBox(self):
        data = []
        for fabu in self.fabus['fabu']:
            data.append(fabu['envName'])
        data = set(data)
        for i in data:
            self.envNameComboBox.addItem(i)

    def setTable(self):
        appName = self.appNameComboBox.currentText()
        envName = self.envNameComboBox.currentText()
        for i, data in enumerate(self.fabus['fabu']):
            if appName == data['appName'] and envName == data['envName']:
                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)
                self.tableWidget.setItem(row, 0, QTableWidgetItem(str(data['appName'])))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(data['envName']))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(data['commit']))
                widget = QWidget()
                handle = Ui_appHandleButtons()
                handle.setupUi(widget)
                self.tableWidget.setCellWidget(row, 3, widget)
                handle.startButton.clicked.connect(self.start)
                handle.stopButton.clicked.connect(self.stop)
                handle.fabuButton.clicked.connect(self.fabu)
                handle.restartButton.clicked.connect(self.restart)

        self.tableWidget.setSortingEnabled(True)

    def initTable(self):
        self.tableWidget.clearContents()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setRowCount(0)

    def appChange(self):
        self.initTable()
        self.setTable()

    def envChange(self):
        self.initTable()
        self.setTable()

    def start(self):
        button = self.widget.sender()
        row = self.tableWidget.indexAt(button.parent().pos()).row()
        appName = self.tableWidget.item(row, 0).text()
        envName = self.tableWidget.item(row, 1).text()
        fabuId = self.getFabuId(appName, envName)
        sentData = {'model': 'app', 'api': 'appAction'}
        sentData['token'] = self.main.token
        sentData['fabuId'] = fabuId
        sentData['type'] = "start"
        try:
            server = MySocket()
            result = server.send(sentData)
        except Exception:
            pass
        else:
            if result['code'] == 200:
                QMessageBox.information(self.widget, "提示信息", result['message'])
            elif result['code'] == 402:
                QMessageBox.information(self.widget, "提示信息", "token已过期， 请重新登陆")
                self.main.tokenTimeout()
            else:
                QMessageBox.information(self.widget, "提示信息", result['message'])


    def stop(self):
        button = self.widget.sender()
        row = self.tableWidget.indexAt(button.parent().pos()).row()
        appName = self.tableWidget.item(row, 0).text()
        envName = self.tableWidget.item(row, 1).text()
        fabuId = self.getFabuId(appName, envName)
        sentData = {'model': 'app', 'api': 'appAction'}
        sentData['token'] = self.main.token
        sentData['fabuId'] = fabuId
        sentData['type'] = "stop"
        try:
            server = MySocket()
            result = server.send(sentData)
        except Exception:
            pass
        else:
            if result['code'] == 200:
                QMessageBox.information(self.widget, "提示信息", result['message'])
            elif result['code'] == 402:
                QMessageBox.information(self.widget, "提示信息", "token已过期， 请重新登陆")
                self.main.tokenTimeout()
            else:
                QMessageBox.information(self.widget, "提示信息", result['message'])

    def fabu(self):
        button = self.widget.sender()
        row = self.tableWidget.indexAt(button.parent().pos()).row()
        appName = self.tableWidget.item(row, 0).text()
        envName = self.tableWidget.item(row, 1).text()
        fabuId = self.getFabuId(appName, envName)
        projectName = self.getProjectName(appName, envName)
        self.tmpWidget = QWidget()
        self.tmp = Fabu(self.main, self.tmpWidget, projectName, appName, fabuId,envName)
        self.tmp.initData()
        self.tmpWidget.show()

    def restart(self):
        button = self.widget.sender()
        row = self.tableWidget.indexAt(button.parent().pos()).row()
        appName = self.tableWidget.item(row, 0).text()
        envName = self.tableWidget.item(row, 1).text()
        fabuId = self.getFabuId(appName, envName)
        sentData = {'model': 'app', 'api': 'appAction'}
        sentData['token'] = self.main.token
        sentData['fabuId'] = fabuId
        sentData['type'] = "restart"
        try:
            server = MySocket()
            result = server.send(sentData)
        except Exception:
            pass
        else:
            if result['code'] == 200:
                QMessageBox.information(self.widget, "提示信息", result['message'])
            elif result['code'] == 402:
                QMessageBox.information(self.widget, "提示信息", "token已过期， 请重新登陆")
                self.main.tokenTimeout()
            else:
                QMessageBox.information(self.widget, "提示信息", result['message'])


    def getFabuId(self, appName, envName):
        for fabu in self.fabus['fabu']:
            if appName == fabu['appName'] and envName == fabu['envName']:
                return fabu['fabuId']

    def getProjectName(self, appName, envName):
        for fabu in self.fabus['fabu']:
            if appName == fabu['appName'] and envName == fabu['envName']:
                return fabu['projectName']
