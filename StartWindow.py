# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
# Custom packages
from Settings import Settings


class StartWindow(QWidget):
    def __init__(self, settings: Settings):
        QWidget.__init__(self)
        uic.loadUi("Form/StartForm.ui", self)
        self.setLayout(self.mainLayout)

        self.databaseLw.addItems(settings.getDbList())
