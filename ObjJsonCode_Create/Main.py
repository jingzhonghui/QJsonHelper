from PyQt5.QtWidgets import QApplication
import sys
from MainWindow import MainWinwdow

if __name__ == "__main__":
    a = QApplication(sys.argv)
    win = MainWinwdow()
    win.setWindowTitle('JsonHelper代码生成器')
    win.show()
    sys.exit(a.exec_())
