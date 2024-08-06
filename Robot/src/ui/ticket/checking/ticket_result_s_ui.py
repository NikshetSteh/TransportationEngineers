# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'result_s.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect, QSize, Qt,
                            QTime, QUrl)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QGradient, QIcon, QImage,
                           QKeySequence, QLinearGradient, QPainter, QPalette,
                           QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QSizePolicy,
                               QWidget)

import ui.ticket.checking.result_s_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 600)
        MainWindow.setMinimumSize(QSize(1024, 600))
        MainWindow.setMaximumSize(QSize(1024, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 1031, 601))
        self.label.setPixmap(QPixmap(u":/images/media/Background_TS.png"))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 245, 399, 131))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(41)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"color: rgb(231, 36, 16);")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 420, 531, 51))
        font1 = QFont()
        font1.setPointSize(45)
        self.label_3.setFont(font1)
        self.label_3.setStyleSheet(u"color: rgb(231, 36, 16);")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ResultS", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0425\u043e\u0440\u043e\u0448\u0435\u0433\u043e \u043f\u0443\u0442\u0438,\n"
"{0}!", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0430\u0448\u0435 \u043c\u0435\u0441\u0442\u043e: {0}", None))
    # retranslateUi

