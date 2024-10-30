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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
                               QWidget)


class Ui_ItemUI(object):
    def setupUi(self, ItemUI):
        if not ItemUI.objectName():
            ItemUI.setObjectName(u"ItemUI")
        ItemUI.resize(450, 155)
        ItemUI.setStyleSheet(u"border:1px solid rgb(0, 0, 0);")
        self.label = QLabel(ItemUI)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 130, 155))
        self.label.setStyleSheet(u"border-radius: 5px;\n"
"border: 2px solid rgb(0, 0, 0);")
        self.name = QLabel(ItemUI)
        self.name.setObjectName(u"name")
        self.name.setGeometry(QRect(146, 0, 304, 41))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(25)
        self.name.setFont(font)
        self.name.setStyleSheet(u"color: #E72410;\n"
"border: none;")
        self.price = QLabel(ItemUI)
        self.price.setObjectName(u"price")
        self.price.setGeometry(QRect(146, 52, 251, 41))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(20)
        font1.setBold(True)
        self.price.setFont(font1)
        self.price.setStyleSheet(u"border: none;")
        self.button = QPushButton(ItemUI)
        self.button.setObjectName(u"button")
        self.button.setGeometry(QRect(0, 0, 450, 155))
        self.button.setStyleSheet(u"background: rgbs(255, 255, 255, 1);\n"
"border: none;")

        self.retranslateUi(ItemUI)

        QMetaObject.connectSlotsByName(ItemUI)
    # setupUi

    def retranslateUi(self, ItemUI):
        ItemUI.setWindowTitle(QCoreApplication.translate("ItemUI", u"Form", None))
        self.label.setText("")
        self.name.setText(QCoreApplication.translate("ItemUI", u"name", None))
        self.price.setText(QCoreApplication.translate("ItemUI", u"\u0426\u0435\u043d\u0430: 100 \u0440\u0443\u0431.", None))
        self.button.setText("")
    # retranslateUi

