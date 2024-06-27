from PyQt5.Qt import *
from qt_material import apply_stylesheet
from lyrra.ui.load.index import Index
from lyrra.ui.work.work import Work


class Main:
    def __init__(self):
        self.memTree = {}
        self.token = None
        self.app = QApplication([])
        self.createIndex()
        apply_stylesheet(self.app, theme='dark_teal.xml')
        #apply_stylesheet(self.app,theme='light_cyan_500.xml')
        self.app.exec_()

    # 界面 登录页
    def createIndex(self):
        self.indexWidget = QWidget()
        self.index = Index(self)
        self.indexWidget.show()

    # 界面 管理页
    def createWork(self):
        self.workWidget = QWidget()
        self.work = Work(self, self.memTree)
        self.workWidget.show()

    def tokenTimeout(self):
        self.workWidget.deleteLater()
        self.createIndex()

    def createDialog(self):
        pass


if __name__ == '__main__':
    main = Main()
