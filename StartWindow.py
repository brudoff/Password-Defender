# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5 import uic
# Custom packages
from Settings import Settings
# Import handle of window classes
from AddExistWindow import AddExistWindow


class StartWindow(QWidget):
    """ Class which represent Start Form """

    def __init__(self, settings: Settings):
        QWidget.__init__(self)
        self.settings = settings
        uic.loadUi("Form/StartForm.ui", self)
        self.setLayout(self.mainLayout)
        # Init latest open db list
        self.databaseLw.addItems(settings.getDbList())
        self.add_exist_window = AddExistWindow()
        # Connect slot and signal for showing window for btn click
        self.btnAdd.clicked.connect(self.add_existing_db)

    def add_existing_db(self):
        self.add_exist_window.show()
        self.add_exist_window.added_database.connect(self.on_add_exist_pair)

    def on_add_exist_pair(self, db_path, mk_path):
        # Write new db path and mk path to settings file
        self.settings.appendNewDB(db_path, mk_path)
        # Add this file to list
        self.databaseLw.insertItem(0, db_path)

