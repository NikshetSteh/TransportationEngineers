# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_menu.ui'
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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 600)
        MainWindow.setStyleSheet(u"background-color: white;")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(208, 265, 200, 70))
        font = QFont()
        font.setFamilies([u"Rubik"])
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(u"background: #d9d9d9;\n"
"border-radius: 5px;")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(608, 265, 200, 70))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(u"background: #d9d9d9;\n"
"border-radius: 5px;")
        self.welcomeLabel = QLabel(self.centralwidget)
        self.welcomeLabel.setObjectName(u"welcomeLabel")
        self.welcomeLabel.setGeometry(QRect(0, 0, 1024, 265))
        font1 = QFont()
        font1.setFamilies([u"Rubik"])
        font1.setPointSize(20)
        self.welcomeLabel.setFont(font1)
        self.welcomeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(410, 400, 200, 70))
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet(u"background: #d9d9d9;\n"
"border-radius: 5px;")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u0433\u0430\u0437\u0438\u043d\u044b", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f", None))
        self.welcomeLabel.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0434\u0440\u0430\u0432\u0441\u0442\u0432\u0443\u0439\u0442\u0435, {0}!", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0445\u043e\u0434", None))
    # retranslateUi

