# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowFaYAzI.mqtt_mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import (QFont, QIcon)
from PySide6.QtWidgets import (QLabel, QProgressBar,
                               QVBoxLayout, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(250, 200)
        icon = QIcon()
        icon.addFile(u":/icon/logo.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_task = QLabel(self.centralwidget)
        self.label_task.setObjectName(u"label_task")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_task.setFont(font)
        self.label_task.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_task)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)

        self.label_requirement = QLabel(self.centralwidget)
        self.label_requirement.setObjectName(u"label_requirement")

        self.verticalLayout.addWidget(self.label_requirement)

        self.label_layer = QLabel(self.centralwidget)
        self.label_layer.setObjectName(u"label_layer")

        self.verticalLayout.addWidget(self.label_layer)

        self.label_time = QLabel(self.centralwidget)
        self.label_time.setObjectName(u"label_time")

        self.verticalLayout.addWidget(self.label_time)

        self.label_hotend = QLabel(self.centralwidget)
        self.label_hotend.setObjectName(u"label_hotend")

        self.verticalLayout.addWidget(self.label_hotend)

        self.label_hotbed = QLabel(self.centralwidget)
        self.label_hotbed.setObjectName(u"label_hotbed")

        self.verticalLayout.addWidget(self.label_hotbed)

        self.label_box = QLabel(self.centralwidget)
        self.label_box.setObjectName(u"label_box")

        self.verticalLayout.addWidget(self.label_box)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_task.setText("")
        self.label_requirement.setText(QCoreApplication.translate("MainWindow", u"\u9700\u8981\uff1a", None))
        self.label_layer.setText(QCoreApplication.translate("MainWindow", u"\u5c42\u6570\uff1a", None))
        self.label_time.setText(QCoreApplication.translate("MainWindow", u"\u7528\u65f6\uff1a", None))
        self.label_hotend.setText(QCoreApplication.translate("MainWindow", u"\u55b7\u5934\uff1a", None))
        self.label_hotbed.setText(QCoreApplication.translate("MainWindow", u"\u70ed\u5e8a\uff1a", None))
        self.label_box.setText(QCoreApplication.translate("MainWindow", u"\u8154\u4f53\uff1a", None))
    # retranslateUi

