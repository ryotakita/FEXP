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
        if not model_new.isDir(item) : return

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

        dockWidget = QDockWidget("Dock Window", self)
        dockWrapper = QWidget()
        dockWidget.setWidget(dockWrapper)
        dockLayout = QVBoxLayout()
        dockWrapper.setLayout(dockLayout)
        dockLabel_file = QLabel("ファイル名:")
        dockDescription_file = QLabel(str_file)
        dockLabel = QLabel("ページ指定:")
        dockDescription = QLineEdit()
        dockAlert = QLabel("※ページ指定はPDF作成時には考慮されません。")
        dockLayout.addWidget(dockLabel_file)
        dockLayout.addWidget(dockDescription_file)
        dockLayout.addWidget(dockLabel)
        dockLayout.addWidget(dockDescription)
        dockLayout.addWidget(dockAlert)
        dockButton = QPushButton("OK")
        dockLayout.addWidget(dockButton)
        dockLayout.addStretch()
        dockWidget.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.__list_path_of_target.append([model_file.filePath(item), model_file.isDir(item) 
                                         , len(str_list), dockWidget])
        print(self.__list_path_of_target)

    def createPDF(self):
        #Logの初期化
        self.ui.log.setText("")
        for file_or_dir, isDir, _ in self.__list_path_of_target:
            if isDir:
                files = os.listdir(file_or_dir)
                for file in files:
                    pass
                    #os.system('powershell -File powershell.ps1 ' + file + " " + )
            else:
                print(file_or_dir)
                file = file_or_dir.rsplit("/",1)[1]
                print(file)
                os.system('powershell -File powershell.ps1 ' + file + " " + file_or_dir)
                log_message = self.ui.log.toPlainText()
                log_message = log_message + (file  + "をPDFに変換しました。\n")
                print(log_message)
                self.ui.log.setText(log_message)
        self.clearTarget()
        
    def mergePDF(self):
        self.ui.log.setText("")
        dialog = QInputDialog()
        file_name = dialog.getText(self, 'MergedFileName', 'マージしたファイルの名前を指定してください。')[0]
        if not file_name : file_name = "merged_file"
        pdf_writer = PdfFileWriter()
        for file in self.__list_path_of_target:
                if( 'doc' in file ) : continue
                print(file)
                pdf_reader = PdfFileReader(file[0])
                for page in range(pdf_reader.getNumPages()):
                    # Add each page to the writer object
                    pdf_writer.addPage(pdf_reader.getPage(page))

        # Write out the merged PDF
        with open(self.__list_path_of_target[0][0].rsplit('/',1)[0] + '/' + file_name + '.pdf', 'wb') as out:
            pdf_writer.write(out)
        log_message = self.ui.log.toPlainText()
        log_message = log_message + ("結合しました。 ファイル名:" + file_name) 
        self.ui.log.setText(log_message)
        self.clearTarget()
        
    def clearTarget(self):
        self.__list_path_of_target.clear()
        model_empty = QtCore.QStringListModel()
        self.ui.listTarget.setModel(model_empty)
    
    def showDock(self,item):
        #表示されている全てのdockをhiddenする
        for _, _, _, dock in self.__list_path_of_target:
            dock.hide()
        dock_this = self.__list_path_of_target[item.row()][3] 
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock_this)
        dock_this.show()




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
        self.ui.listTarget.clicked.connect(self.showDock)

    


#実行処理
if __name__=="__main__":
    #アプリケーション作成
    app = QApplication(sys.argv)
    #オブジェクト作成
    window = MainWindow()
    # ウィンドウ消し
    window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    window.setStyleSheet("background-color:rgb(100,100,100,150);")
    window.ui.listView.setStyleSheet("color: #c0c0c0")
    #MainWindowの表示
    window.show()

    sys.exit(app.exec_())