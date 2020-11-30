# -*- coding: utf-8 -*-
import sys
from main_ui import Ui_MainWindow
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import *
from PyPDF2 import PdfFileReader, PdfFileWriter
import os

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

    def nextDir(self, item):
        model_old = item.model()
        model_new = QFileSystemModel()
        path_new = model_old.filePath(item)
        model_new.setRootPath(path_new)
        self.ui.listView.setModel(model_new)
        self.ui.listView.setRootIndex(model_new.index(path_new))
    
    def returnDir(self, item):
        model_old = self.ui.listView.model()
        model_new = QFileSystemModel()
        dir_new = model_old.rootDirectory()
        #path_new = dir_new.absolutePath
        path_new = dir_new.absolutePath()
        path_root = path_new.rsplit('/',1)[0]
        print(item)
        model_new.setRootPath(path_root)
        self.ui.listView.setModel(model_new)
        self.ui.listView.setRootIndex(model_new.index(path_root))
    
    def addTarget(self,item):
        model_file = self.ui.listView.model()
        str_file = model_file.fileName(item)
        str_list = self.ui.listTarget.model().stringList()
        str_list.append(str_file)
        self.ui.listTarget.model().setStringList(str_list)
        self.__list_path_of_target.append([model_file.filePath(item), model_file.isDir(item), len(str_list)])
        print(self.__list_path_of_target)
    
    def createPDF(self):
        for file_or_dir, isDir, _ in self.__list_path_of_target:
            if isDir:
                files = os.listdir(file_or_dir)
                print(files)
                for file in files:
                    pass
                    print (file)
                    #os.system('powershell -File powershell.ps1 ' + file + " " + )
            else:
                print(file_or_dir)
                file = file_or_dir.rsplit("/",1)[1]
                print(file)
                os.system('powershell -File powershell.ps1 ' + file + " " + file_or_dir)
        
    def mergePDF(self):
        pdf_writer = PdfFileWriter()
        for file in self.__list_path_of_target:
                if( 'doc' in file ) : continue
                print(file)
                pdf_reader = PdfFileReader(file[0])
                for page in range(pdf_reader.getNumPages()):
                    # Add each page to the writer object
                    pdf_writer.addPage(pdf_reader.getPage(page))

        # Write out the merged PDF
        with open(self.__list_path_of_target[0][0].rsplit('/',1)[0] + '/' + 'merged' + '.pdf', 'wb') as out:
            pdf_writer.write(out)



    def __init__(self, parent = None):
        self.__isDrag = False
        self.__startPos = QtCore.QPoint(0,0)

        #listTargetの内部データ保持リスト
        self.__list_path_of_target = []

        #UI初期化処理
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.menubar.addMenu('File')

        #ディレクトリ関連の処理
        self.ui.listView.leftClicked.connect(self.nextDir)
        self.ui.listView.rightClicked.connect(self.addTarget)
        self.ui.listView.backClicked.connect(self.returnDir)
        self.ui.pushButton.clicked.connect(self.createPDF)
        self.ui.pushButton_2.clicked.connect(self.mergePDF)

    


#実行処理
if __name__=="__main__":
    #アプリケーション作成
    app = QApplication(sys.argv)
    #オブジェクト作成
    window = MainWindow()
    # ウィンドウ消し
    window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    window.setStyleSheet("background-color:rgb(50,50,100,150);")
    window.ui.listView.setStyleSheet("color: #c0c0c0")
    #MainWindowの表示
    window.show()

    sys.exit(app.exec_())