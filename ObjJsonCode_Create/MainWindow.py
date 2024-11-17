from PyQt5.QtWidgets import QMainWindow
from CenterWidget import CenterWidget

class MainWinwdow(QMainWindow):
    def __init__(self, parent = None):
        super(QMainWindow,self).__init__(parent)
        self.__initUI()

    def __initUI(self):
        #设置布局
        #添加文件列表
        self.centerWidget = CenterWidget(self)
        self.setCentralWidget(self.centerWidget)
        self.resize(1400,800)
        # self.centerWidget.setSplitterSize({700,700})
