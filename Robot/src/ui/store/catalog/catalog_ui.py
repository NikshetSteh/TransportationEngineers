# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'catalog.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
                               QPushButton, QScrollArea, QSizePolicy, QWidget)

import ui.store.catalog.catalog_rc


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
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 1024, 600))
        self.label.setPixmap(QPixmap(u":/media/window_catalog.png"))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(799, 21, 204, 39))
        self.pushButton.setStyleSheet(u"background: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.search = QLineEdit(self.centralwidget)
        self.search.setObjectName(u"search")
        self.search.setGeometry(QRect(60, 120, 341, 40))
        self.search.setStyleSheet(u"background: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(20, 170, 984, 431))
        self.scrollArea.setStyleSheet(u"background: rgba(255, 255, 255, 1);\n"
"border: none;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 984, 431))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0431\u0438\u043b\u0435\u0442\u0430", None))
        self.label.setText("")
        self.pushButton.setText("")
        self.search.setText("")
    # retranslateUi

