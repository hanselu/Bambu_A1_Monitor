# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mqtt_mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QProgressBar,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(250, 196)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_task = QLabel(self.centralwidget)
        self.label_task.setObjectName(u"label_task")

        self.verticalLayout.addWidget(self.label_task)

        self.label_layer = QLabel(self.centralwidget)
        self.label_layer.setObjectName(u"label_layer")

        self.verticalLayout.addWidget(self.label_layer)

        self.label_time = QLabel(self.centralwidget)
        self.label_time.setObjectName(u"label_time")

        self.verticalLayout.addWidget(self.label_time)

        self.label_nozzle = QLabel(self.centralwidget)
        self.label_nozzle.setObjectName(u"label_nozzle")

        self.verticalLayout.addWidget(self.label_nozzle)

        self.label_hotbed = QLabel(self.centralwidget)
        self.label_hotbed.setObjectName(u"label_hotbed")

        self.verticalLayout.addWidget(self.label_hotbed)

        self.label_stage = QLabel(self.centralwidget)
        self.label_stage.setObjectName(u"label_stage")

        self.verticalLayout.addWidget(self.label_stage)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)

        self.btn_pull_all = QPushButton(self.centralwidget)
        self.btn_pull_all.setObjectName(u"btn_pull_all")

        self.verticalLayout.addWidget(self.btn_pull_all)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_task.setText(QCoreApplication.translate("MainWindow", u"\u4efb\u52a1", None))
        self.label_layer.setText(QCoreApplication.translate("MainWindow", u"\u5c42\u6570", None))
        self.label_time.setText(QCoreApplication.translate("MainWindow", u"\u65f6\u95f4", None))
        self.label_nozzle.setText(QCoreApplication.translate("MainWindow", u"\u55b7\u5634\u6e29\u5ea6", None))
        self.label_hotbed.setText(QCoreApplication.translate("MainWindow", u"\u70ed\u5e8a\u6e29\u5ea6", None))
        self.label_stage.setText(QCoreApplication.translate("MainWindow", u"\u72b6\u6001", None))
        self.btn_pull_all.setText(QCoreApplication.translate("MainWindow", u"\u5237\u65b0\u5168\u90e8\u4fe1\u606f", None))
    # retranslateUi

