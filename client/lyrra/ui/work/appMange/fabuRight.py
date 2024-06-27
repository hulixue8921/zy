from lyrra.ui.work.appMange.fabuRightWidget import Ui_fabuRightWidget
from lyrra.share.mySocket import MySocket
from PyQt5.Qt import *


class FabuRight(Ui_fabuRightWidget):
    def __init__(self, main, widget,roleId,roleName):
        super().__init__()
        self.main = main
        self.widget = widget
        self.roleId=roleId
        self.roleName=roleName
        self.ownFabu=None
        self.allApp=None
        self.setupUi(self.widget)

        self.addToolButton.setArrowType(Qt.RightArrow)
        self.delToolButton.setArrowType(Qt.LeftArrow)
        self.addToolButton.clicked.connect(self.addFun)
        self.delToolButton.clicked.connect(self.delFun)
        #self.addButton.clicked.connect(self.addFun)
        #self.delButton.clicked.connect(self.delFun)
        self.getInitData()
        self.appComboBox.currentIndexChanged.connect(self.comboxChangeFun)
        self.set()
        self.roleNameLabel.setText(self.roleName)
        self.cacelButton.clicked.connect(self.cacelFun)
        self.sureButton.clicked.connect(self.sureFun)


    def getInitData(self):
        sentData = {'model': 'app', 'api': 'listApp'}
        sentData['token'] = self.main.token
        try:
            server=MySocket()
            result=server.send(sentData)
            self.allApp=result
        except Exception:
            QMessageBox.information(self.widget, '提示信息', "网络不可达")

        sentData={'model':'app', 'api':'listFabu'}
        sentData['roleId']=self.roleId
        try:
            server = MySocket()
            self.ownFabu = server.send(sentData)
        except Exception:
            QMessageBox.information(self.widget, '提示信息', "网络不可达")

    def set(self):
        for app in self.allApp['app']:
            self.appComboBox.addItem(app['appName'])

        for fabu in self.ownFabu['fabu']:
            self.ownList.addItem(fabu['appName'] + ":" + fabu['envName'] + "-" + str(fabu['fabuId']))



    def cacelFun(self):
        self.widget.deleteLater()

    def sureFun(self):
        sentData={'model':'app', "api":"roleFabu"}
        sentData['roleId']=self.roleId
        sentData['fabuIds']=[]
        for i in range(self.ownList.count()):
            x=self.ownList.item(i).text()
            y=x.split("-")
            sentData['fabuIds'].append(y[1])

        try:
            server=MySocket()
            result=server.send(sentData)
        except Exception:
            QMessageBox.information(self.widget, '提示信息', "网络不可达")
        else:
            if result['code'] == 200:
                QMessageBox.information(self.widget, '提示信息', "修改发布成功")
                self.widget.deleteLater()
            else:
                QMessageBox.information(self.widget, '提示信息', "修改发布失败")



    def addFun(self):
        data1 = []
        for i in range(self.allList.count()):
            data1.append(self.allList.item(i).text())

        try:
            x = self.allList.currentItem().text()
        except Exception:
            QMessageBox.information(self.widget, '提示信息', '在"左边list中"请选择')
        else:
            data1.remove(x)
            self.allList.clear()
            self.ownList.addItem(x)
            for i in data1:
                self.allList.addItem(i)

    def delFun(self):
        data2 = []
        for i in range(self.ownList.count()):
            data2.append(self.ownList.item(i).text())
        try:
            x = self.ownList.currentItem().text()
        except Exception:
            QMessageBox.information(self.widget, '提示信息', '在"右边list中"请选择')
        else:
            self.allList.addItem(x)
            data2.remove(x)
            self.ownList.clear()
            for i in data2:
                self.ownList.addItem(i)

    def comboxChangeFun(self):
        self.noOwnFabuLabel.setText("你暂未拥有app:"+self.appComboBox.currentText()+"的发布")
        self.allList.clear()

        sentData = {'model': 'app', 'api': 'listAppFabu'}
        sentData['token'] = self.main.token
        for app in self.allApp['app']:
            if self.appComboBox.currentText() == app['appName']:
                sentData['appId']=app['appId']
        try:
            server = MySocket()
            result = server.send(sentData)
            tmpdata=[]
            for i in self.ownFabu['fabu']:
                tmpdata.append(i['fabuId'])
            for i in result['appFabu']:
                if i['fabuId'] not in tmpdata:
                    self.allList.addItem(i['appName']+":"+i['envName']+"-"+ str(i['fabuId']))
        except Exception:
            QMessageBox.information(self.widget, '提示信息', "网络不可达")


