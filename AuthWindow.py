# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class AuthWindow(QWidget):
    """ Class which represent Authentification Form """

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("Form/AuthForm.ui", self)
        self.setLayout(self.mainLayout)
