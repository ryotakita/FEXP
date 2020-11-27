# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import os


class QListDir(QListView):
    rightClicked = Signal(QModelIndex)
    doubleClicked = Signal(QModelIndex)
    leftClicked = Signal(QModelIndex)
    def mouseDoubleClickEvent(self, e):
        self.doubleClicked.emit(self.indexAt(e.pos()))
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.RightButton:
            self.rightClicked.emit(self.indexAt(e.pos()))
        elif e.button() == Qt.LeftButton:
            self.leftClicked.emit(self.indexAt(e.pos()))
        else:
            super(QListView, self).mouseReleaseEvent(e)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.title = QLabel(self.centralwidget)
        self.title.setText("PDFMerger")
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(20,490,300,70))
        self.title.setStyleSheet("font-family: Source Han Code JP; \
                                  font-size: 50px; \
                                  font-weight: bold; \
                                  color: rgb(255,255,255,30); \
                                  ")

        self.listView = QListDir(self.centralwidget)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(30, 10, 700, 192))

        self.listTarget = QListView(self.centralwidget)
        self.listTarget.setObjectName(u"listTarget")
        self.listTarget.setGeometry(QRect(430, 220, 300, 192))

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(40, 220, 75, 23))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(120, 220, 75, 23))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        model = QFileSystemModel()
        path = 'C://'
        model.setRootPath(path)
        self.listView.setModel(model)
        self.listView.setRootIndex(model.index(path))

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
    # retranslateUi

