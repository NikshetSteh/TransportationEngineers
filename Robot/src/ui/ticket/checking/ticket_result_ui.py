# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'result.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QSizePolicy,
    QWidget)
import ui.ticket.checking.ticket_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.IconLabel = QLabel(self.centralwidget)
        self.IconLabel.setObjectName(u"IconLabel")
        self.IconLabel.setGeometry(QRect(384, 32, 256, 256))
        self.IconLabel.setPixmap(QPixmap(u":/icons/media/check.png"))
        self.TextLabel = QLabel(self.centralwidget)
        self.TextLabel.setObjectName(u"TextLabel")
        self.TextLabel.setGeometry(QRect(384, 300, 256, 271))
        self.TextLabel.setTextFormat(Qt.TextFormat.MarkdownText)
        self.TextLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.IconLabel.setText("")
        self.TextLabel.setText(QCoreApplication.translate("MainWindow", u"Test ticket\n"
"\n"
"Place: 1\n"
"\n"
"Wagon: 1\n"
"\n"
"", None))
    # retranslateUi

