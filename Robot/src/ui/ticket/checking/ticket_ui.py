# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ticket.ui'
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

import ui.ticket.checking.ticket_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 600)
        MainWindow.setMinimumSize(QSize(1024, 600))
        MainWindow.setMaximumSize(QSize(1024, 600))
        MainWindow.setBaseSize(QSize(1024, 600))
        icon = QIcon()
        icon.addFile(u":/icons/Media/ticket.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"background-color: rgb(255, 255, 255)")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.video_label = QLabel(self.centralwidget)
        self.video_label.setObjectName(u"video_label")
        self.video_label.setGeometry(QRect(523, 57, 476, 486))
        self.video_label.setMinimumSize(QSize(476, 486))
        self.video_label.setMaximumSize(QSize(476, 486))
        self.video_label.setStyleSheet(u"border-radius: 50px;")
        self.video_label.setPixmap(QPixmap(u":/images/media/VideoZaglushka.png"))
        self.video_label.setScaledContents(True)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 1024, 600))
        self.label.setMinimumSize(QSize(1024, 600))
        self.label.setMaximumSize(QSize(1024, 600))
        self.label.setBaseSize(QSize(1024, 600))
        self.label.setPixmap(QPixmap(u":/images/media/Background_TC.png"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.label.raise_()
        self.video_label.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0431\u0438\u043b\u0435\u0442\u0430", None))
        self.video_label.setText("")
        self.label.setText("")
    # retranslateUi

