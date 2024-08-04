# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'auth.ui'
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
        self.label_t = QLabel(self.centralwidget)
        self.label_t.setObjectName(u"label_t")
        self.label_t.setGeometry(QRect(180, 400, 712, 200))
        font = QFont()
        font.setPointSize(31)
        self.label_t.setFont(font)
        self.label_t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label = QLabel(self.centralwidget)
        self.video_label.setObjectName(u"video_label")
        self.video_label.setGeometry(QRect(180, 0, 712, 400))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0431\u0438\u043b\u0435\u0442\u0430", None))
        self.label_t.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044f...", None))
        self.video_label.setText(QCoreApplication.translate("MainWindow", u"\u042d\u0442\u043e \u0432\u0438\u0434\u0435\u043e \u0432\u0438\u0434\u0436\u0435\u0442, \u043d\u0435 \u0442\u0435\u043a\u0441\u0442. ", None))
    # retranslateUi

