# -*- coding: utf-8 -*-
import sys
from main_ui import Ui_MainWindow
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import *

class MainWindow(QMainWindow):
    #Ui_MainWindow生成のための初期化処理
    def mousePressEvent(self, event):
        self.__isDrag = True
        self.__startPos = event.pos()
        super(MainWindow, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.__isDrag = False
        super(MainWindow, self).mouseReleaseEvent(event)
          
    def mouseMoveEvent(self, event):
        if self.__isDrag:
            self.move(self.mapToParent(event.pos() - self.__startPos))
        super(MainWindow, self).mouseMoveEvent(event)

    def __init__(self, parent = None):
        self.__isDrag = False
        self.__startPos = QtCore.QPoint(0,0)

        #UI初期化処理
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.menubar.addMenu('File')

#実行処理
if __name__=="__main__":
    #アプリケーション作成
    app = QApplication(sys.argv)
    #オブジェクト作成
    window = MainWindow()
    # ウィンドウ消し
    window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    window.setStyleSheet("background-color:rgb(50,50,100,150);")
    #MainWindowの表示
    window.show()

    sys.exit(app.exec_())