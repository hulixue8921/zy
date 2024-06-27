from PyQt5.Qt import *
from lyrra.ui.work.workWidget import Ui_workWidget
from lyrra.ui.work.sysMange.roleMange.roleMange import RoleMangle
from lyrra.ui.work.sysMange.userMange.user import User
from lyrra.ui.work.appMange.listApp import ListApp
from lyrra.ui.work.appMange.appHandle import AppHandle


class Work(Ui_workWidget):
    def __init__(self, main, mem):
        super().__init__()
        self.main = main
        self.setupUi(self.main.workWidget)
        self.createTree(mem)
        self.createUserMangePage()

        def initListUser():
            self.workStackUser.clearAll()
            self.workStackUser.getData()

        def initRole():
            self.workStackRoleMange.clearAll()
            self.workStackRoleMange.getData()

        def initListApp():
            self.workStackListApp.clearAll()
            self.workStackListApp.getData()

        def initAppHandle():
            self.workStackAppHandle.initData()

        self.pageIndex = {
            "用户管理": {'index': 1, 'fun': initListUser},
            "角色管理": {'index': 2, 'fun': initRole},
            "app列表": {'index': 3, 'fun': initListApp},
            "app操作": {'index': 4, 'fun': initAppHandle}
        }

        self.workWidgeTree.clicked.connect(self.treeClickFun)

    def createTree(self, memData):
        # 管理栏tree
        self.workWidgeTree.clear()
        treeRoot = QTreeWidgetItem(self.workWidgeTree)
        treeRoot.setText(0, "管理中心")
        self.treeMem(memData, treeRoot)
        self.workWidgeTree.setColumnWidth(0, 150)

    def treeMem(self, mem, root):
        if mem:
            for i in mem.keys():
                item = QTreeWidgetItem(root)
                item.setText(0, i)
                self.treeMem(mem[i], item)
        else:
            pass

    def treeClickFun(self):
        item = self.workWidgeTree.currentItem()
        mem = item.text(0)
        if mem in self.pageIndex.keys():
            self.workWidgetStack.setCurrentIndex(self.pageIndex[mem]['index'])
            self.pageIndex[mem]['fun']()
        else:
            self.workWidgetStack.setCurrentIndex(0)

    def createUserMangePage(self):
        # 用户管理页面
        self.workStackUser = User(self.main, self.workStackUsersMangeWidget)
        self.workStackUser.setupUi()
        self.workStackUser.listUserWidgeUserTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # 角色管理页面
        self.workStackRoleMange = RoleMangle(self.main, self.workStackRolesMangeWidge)
        self.workStackRoleMange.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # app列表 页面
        self.workStackListApp = ListApp(self.main, self.workStackListAppWidge)
        self.workStackListApp.appTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # app操作 页面
        self.workStackAppHandle= AppHandle(self.main, self.workStackHandleAppWidget)
        self.workStackAppHandle.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


