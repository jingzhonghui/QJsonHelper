from PyQt5.QtCore import QFile
from PyQt5.QtGui import QFont,QColor
from PyQt5.Qsci import  QsciScintilla,QsciLexerCPP,QsciAPIs

class TextEdit(QsciScintilla):
    def __init__(self,parent = None):
        super().__init__(parent)
        # 初始化字体
        self.setFont(QFont("Consolas",16))
        #初始化语法器
        self.lexer = QsciLexerCPP(self)
        self.setLexer(self.lexer)
        # 默认使用utf-8编码
        self.setUtf8(True)
        # 设置tab宽度
        self.setTabWidth(4)
        # 设置自动缩进
        self.setAutoIndent(True)
        #设置当前行的颜色
        self.setCaretLineBackgroundColor(QColor("#1fff0000"))
        self.setCaretLineVisible(True)
        # 显示行号
        # 先设置哪个位置显示行号
        self.setMarginType(0,QsciScintilla.MarginType.NumberMargin)
        # 启用行号显示
        self.setMarginLineNumbers(0,True)
        # 设置宽度
        self.setMarginWidth(0,"9999")
        # 语法提示
        self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
        self._apis = QsciAPIs(self.lexer)
        self._apis.prepare()
        self.autoCompleteFromAll() #显示自动完成列表
        self.setAutoCompletionThreshold(1)  #输入一个字符就开始显示提示，必须设置才会显示
        # 函数参数提示
        self.setCallTipsVisible(0)
        self.setCallTipsPosition(QsciScintilla.CallTipsPosition.CallTipsBelowText)
        # 样式
        self.setCallTipsBackgroundColor(QColor(255,255,255))
        self.setCallTipsForegroundColor(QColor("#9cdcfe"))


    def slot_openFile(self,_path:str):
        self.clear()
        try:
            f = QFile(_path)
            f.open(QFile.OpenModeFlag.ReadOnly)
            _data = f.readAll()
            f.close()
            self.setText(_data.data().decode('utf-8'))
        except Exception as e:
            print(e)