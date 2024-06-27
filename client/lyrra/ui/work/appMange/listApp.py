from lyrra.ui.work.appMange.listAppWidget import Ui_listApp
from lyrra.ui.work.appMange.delAppWidget import Ui_delAppWidget
from lyrra.ui.work.appMange.addAppWidget import Ui_addAppWidget
from lyrra.share.mySocket import MySocket
from PyQt5.Qt import *
from threading import Thread


class MySignals(QObject):
    project = pyqtSignal(dict)
    info = pyqtSignal(str)
    tokenTimeout= pyqtSignal(str)


class ListApp(Ui_listApp):
    def __init__(self, main, widget):
        super().__init__()
        self.main = main
        self.widget = widget
        self.tempWidget = None
        self.temp = None
        self.setupUi(self.widget)
        self.Signal=MySignals()
        self.addAppButton.clicked.connect(self.listProject)
        self.Signal.project.connect(self.addAppWidge)
        self.Signal.info.connect(self.info)
        self.Signal.tokenTimeout.connect(self.tokenTimeout)
        self.projectData=None

    def clearAll(self):
        self.appTable.setSortingEnabled(False)
        self.appTable.clearContents()
        self.appTable.setRowCount(0)

    def getData(self):
        sentData = {"model": "app", "api": "listApp"}
        sentData['token'] = self.main.token
        try:
            server = MySocket()
            result = server.send(sentData)
        except Exception:
            QMessageBox.information(self.widget, '提示信息', "网络不可达")
        else:
            if result['code'] == 200:
                for i, data in enumerate(result['app']):
                    row = self.appTable.rowCount()
                    self.appTable.insertRow(row)
                    self.appTable.setItem(row, 0, QTableWidgetItem(str(data['appId'])))
                    self.appTable.setItem(row, 1, QTableWidgetItem(str(data['appName'])))
                    self.appTable.setItem(row, 2, QTableWidgetItem(str(data['projectName'])))
                    widget = QWidget()
                    delApp = Ui_delAppWidget()
                    delApp.setupUi(widget)
                    self.appTable.setCellWidget(row, 3, widget)
                    delApp.delAppButton.clicked.connect(self.delAppFun)
                self.appTable.setSortingEnabled(True)
            elif result['code'] == 402:
                self.Signal.tokenTimeout.emit("token 过期，请重新登陆")
            else:
                QMessageBox.information(self.widget, '提示信息', result['message'])

    def delAppFun(self):
        button = self.widget.sender()
        if button:
            row = self.appTable.indexAt(button.parent().pos()).row()
            sentData = {"model": "app", "api": "delApp"}
            sentData['token'] = self.main.token
            sentData['appId'] = self.appTable.item(row, 0).text()
            try:
                server = MySocket()
                result = server.send(sentData)
            except Exception:
                QMessageBox.information(self.widget, '提示信息', "网络不可达")
            else:
                if result['code'] == 200:
                    self.appTable.removeRow(row)
                elif result['code'] == 402:
                    self.Signal.tokenTimeout.emit("token 过期，请重新登陆")

    def addAppWidge(self, data):
        self.projectData =data
        self.tempWidget = QWidget()
        self.temp = Ui_addAppWidget()
        self.temp.setupUi(self.tempWidget)
        self.tempWidget.show()
        self.temp.cacelButton.clicked.connect(self.addAppCacelFun)
        self.temp.sureButton.clicked.connect(self.addAppSureFun)
        for p in data['project']:
            self.temp.projectNameCombox.addItem(p['projectName'])

    def addAppCacelFun(self):
        self.tempWidget.deleteLater()

    def addAppSureFun(self):
        project=self.temp.projectNameCombox.currentText()
        for p in self.projectData['project']:
            if p['projectName'] == project:
                git=p['git']
                sentData={'model':'app', 'api':'addApp'}
                sentData['token']=self.main.token
                sentData['git']=git
                sentData['project']=project
                sentData['name']=self.temp.appLine.text()
                try:
                    server = MySocket()
                    result = server.send(sentData)
                except Exception:
                    QMessageBox.information(self.widget, '提示信息', "网络不可达")
                else:
                    if result['code'] == 200:
                        QMessageBox.information(self.widget, '提示信息', "添加app 成功 ")
                        self.clearAll()
                        self.getData()
                        #self.tempWidget.deleteLater()
                    elif result['code'] == 402:
                        self.Signal.tokenTimeout.emit("token 过期，请重新登陆")
                    else:
                        QMessageBox.information(self.widget, '提示信息', result['message'])

                break

    def info(self, message):
        QMessageBox.information(self.widget, '提示信息', message)

    def tokenTimeout(self, message):
        self.info(message)
        self.widget.deleteLater()
        self.main.tokenTimeout()


    def listProject(self):
        def fun():
            sentData = {"model": "gitlab", "api": "listProject"}
            sentData['token'] = self.main.token
            try:
                server = MySocket()
                result = server.send(sentData)
            except Exception:
                self.Signal.info.emit("网络不可达")
            else:
                if result['code'] == 200:
                    self.Signal.project.emit(result)
                elif result['code'] == 402:
                    self.Signal.tokenTimeout.emit("token 过期，请重新登陆")
                else:
                    self.Signal.info.emit(result['message'])

        t1=Thread(target=fun)
        t1.start()
