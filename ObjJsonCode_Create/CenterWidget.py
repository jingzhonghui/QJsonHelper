from PyQt5.QtWidgets import QWidget,QSplitter,QHBoxLayout,QVBoxLayout,QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
from TextEditWidget import TextEdit
from CreateCode import CreateCode

class CenterWidget(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.__initUI()
        self.__connectAll()
    
    '''
    初始化界面
    '''
    def __initUI(self):
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(3,3,3,3)
        
        self._layout1 = QHBoxLayout(self)
        self._layout1.setContentsMargins(3,3,3,3)
        self._layout.addLayout(self._layout1)
        # 打开文件按钮
        self.importBtn = QPushButton("从文件导入",self)
        self._layout1.addWidget(self.importBtn)

        #生成按钮
        self.createBtn = QPushButton("生成代码",self)
        self._layout1.addWidget(self.createBtn)
        self._layout1.addStretch()

        #分裂器
        self.splitter = QSplitter(Qt.Orientation.Horizontal,self)
        self.splitter.setLineWidth(2)
        self._layout.addWidget(self.splitter)

        # 左边编辑器
        self.ledit = TextEdit(self)
        self.ledit.setText("//这边填写需要转换的结构体")
        self.splitter.addWidget(self.ledit)
        #编辑器
        self.redit = TextEdit(self)
        self.redit.setText("//这边将显示转换后的代码")
        self.splitter.addWidget(self.redit)

    def __connectAll(self):
        self.importBtn.clicked.connect(self._openFile)
        self.createBtn.clicked.connect(self._createCode)

    def _openFile(self):
        _temp = QFileDialog.getOpenFileName(self,"选择文件",'.','txt(*.txt)')
        _path = _temp[0]
        if not _path:
            return
        with open(_path) as f:
            self.ledit.setText(f.read())
    
    def _createCode(self):
        _source = self.ledit.text()
        _code = CreateCode(_source).run()
        self.redit.setText(_code)
        
    def setSplitterSize(self,size:list):
        self.splitter.setSizes(size)