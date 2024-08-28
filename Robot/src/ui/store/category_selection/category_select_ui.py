# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'category_select.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QWidget)

import ui.store.category_selection.category_select_rc


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
        self.label.setPixmap(QPixmap(u":/media/window.png"))
        self.recommendations = QPushButton(self.centralwidget)
        self.recommendations.setObjectName(u"recommendations")
        self.recommendations.setGeometry(QRect(132, 268, 150, 150))
        self.recommendations.setStyleSheet(u"background: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.city_souvenirs = QPushButton(self.centralwidget)
        self.city_souvenirs.setObjectName(u"city_souvenirs")
        self.city_souvenirs.setGeometry(QRect(335, 265, 150, 150))
        self.city_souvenirs.setStyleSheet(u"background: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.train_souvenirs = QPushButton(self.centralwidget)
        self.train_souvenirs.setObjectName(u"train_souvenirs")
        self.train_souvenirs.setGeometry(QRect(538, 265, 150, 150))
        self.train_souvenirs.setStyleSheet(u"background: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.food = QPushButton(self.centralwidget)
        self.food.setObjectName(u"food")
        self.food.setGeometry(QRect(741, 265, 150, 150))
        self.food.setStyleSheet(u"background: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(799, 21, 204, 39))
        self.pushButton.setStyleSheet(u"background: rgba(255, 255, 255, 0);\n"
"border: none;")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0431\u0438\u043b\u0435\u0442\u0430", None))
        self.label.setText("")
        self.recommendations.setText("")
        self.city_souvenirs.setText("")
        self.train_souvenirs.setText("")
        self.food.setText("")
        self.pushButton.setText("")
    # retranslateUi

