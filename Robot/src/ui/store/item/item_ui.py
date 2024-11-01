# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'item.ui'
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

import ui.store.item.item_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 600)
        MainWindow.setMinimumSize(QSize(1024, 600))
        MainWindow.setMaximumSize(QSize(1024, 600))
        MainWindow.setBaseSize(QSize(1024, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 1024, 600))
        self.label.setPixmap(QPixmap(u":/media/window_item.png"))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(740, 510, 204, 39))
        self.pushButton.setStyleSheet(u"background: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.icon = QLabel(self.centralwidget)
        self.icon.setObjectName(u"icon")
        self.icon.setGeometry(QRect(54, 230, 300, 300))
        self.icon.setStyleSheet(u"border:2px solid rgb(0, 0, 0);\n"
"border-radius: 5px;")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(657, 419, 287, 76))
        self.pushButton_2.setStyleSheet(u"background: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.name = QLabel(self.centralwidget)
        self.name.setObjectName(u"name")
        self.name.setGeometry(QRect(0, 94, 1024, 121))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(60)
        font.setBold(True)
        self.name.setFont(font)
        self.name.setStyleSheet(u"color: rgba(231, 36, 16, 1);")
        self.name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description = QLabel(self.centralwidget)
        self.description.setObjectName(u"description")
        self.description.setGeometry(QRect(377, 230, 480, 88))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.description.setFont(font1)
        self.description.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.description.setWordWrap(True)
        self.count = QLabel(self.centralwidget)
        self.count.setObjectName(u"count")
        self.count.setGeometry(QRect(520, 337, 151, 28))
        self.count.setFont(font1)
        self.price = QLabel(self.centralwidget)
        self.price.setObjectName(u"price")
        self.price.setGeometry(QRect(450, 375, 241, 28))
        self.price.setFont(font1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0431\u0438\u043b\u0435\u0442\u0430", None))
        self.label.setText("")
        self.pushButton.setText("")
        self.icon.setText("")
        self.pushButton_2.setText("")
        self.name.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u0433\u0430\u0437\u0438\u043d", None))
        self.description.setText(QCoreApplication.translate("MainWindow", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430. \u0422\u043e\u0432\u0430\u0440 \u0440\u0430 \u0433\u044b\u0444\u0440\u0432 \u0430\u044b\u0440\u0440\u0430 \u0444\u044b\u0432\u0438\u0430\u043e\u0444\u044b\u0438\u0430 \u0444\u044b\u0432 \u0430\u043e\u043b\u0444\u044b\u0438\u0432\u0430\u0434\u043b \u044b\u043c\u043b\u0440\u0430\u0444\u044b\u0432 \u0438\u0430\u0448\u044b\u0444 \u0438\u0430\u0440 \u044b\u043b\u0448\u0430 \u044b\u0440\u0432 \u0438\u0430\u0434 \u0440\u0444\u044b\u0438\u0432 \u0430", None))
        self.count.setText(QCoreApplication.translate("MainWindow", u"25 \u0448\u0442.", None))
        self.price.setText(QCoreApplication.translate("MainWindow", u"1200 \u0440\u0443\u0431.", None))
    # retranslateUi

