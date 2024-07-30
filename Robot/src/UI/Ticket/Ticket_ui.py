# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ticket.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
import Ticket_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 600)
        MainWindow.setMinimumSize(QSize(1024, 600))
        MainWindow.setMaximumSize(QSize(1024, 600))
        MainWindow.setBaseSize(QSize(1024, 600))
        icon = QIcon()
        icon.addFile(u":/icons/Media/ticket.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_t = QLabel(self.centralwidget)
        self.label_t.setObjectName(u"label_t")
        self.label_t.setGeometry(QRect(110, 110, 261, 221))
        font = QFont()
        font.setPointSize(31)
        self.label_t.setFont(font)
        self.video_label = QLabel(self.centralwidget)
        self.video_label.setObjectName(u"video_label")
        self.video_label.setGeometry(QRect(460, 40, 511, 351))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0431\u0438\u043b\u0435\u0442\u0430", None))
        self.label_t.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430,\n"
" \u0443\u043b\u044b\u0431\u043e\u0447\u043a\u0443!", None))
        self.video_label.setText(QCoreApplication.translate("MainWindow", u"\u042d\u0442\u043e \u0432\u0438\u0434\u0435\u043e \u0432\u0438\u0434\u0436\u0435\u0442, \u043d\u0435 \u0442\u0435\u043a\u0441\u0442. ", None))
    # retranslateUi

