# This Python file uses the following encoding: utf-8
# Standart Packages
import sys
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QStackedWidget
from PyQt5.QtWidgets import QVBoxLayout
# Own classes
from StartWindow import StartWindow
from ViewWindow import ViewWindow
from AuthWindow import AuthWindow
from CreateDatabaseWindow import CreateDatabaseWindow as CreateDBWindow
from Crypter import Crypter
from Settings import Settings


class Main(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.crypter = Crypter()
        self.settings = Settings()
        self.__attempt = 3
        self.__initUi()

    def on_new_db_created(self, crypter, db):
        self.createDB_window.close()
        self.view_window = ViewWindow("", crypter, db)
        self.stack.addWidget(self.view_window)
        self.view_window.initForm()
        # Change Main widget and show data
        self.stack.setCurrentIndex(1)

    def on_new_clicked(self):
        self.createDB_window = CreateDBWindow(self.crypter, self.settings)
        self.createDB_window.setWindowModality(QtCore.Qt.ApplicationModal)
        self.createDB_window.create_new_db.connect(self.on_new_db_created)
        self.createDB_window.show()

    def on_open_clicked(self):
        self.choosed_db = self.start_window.databaseLw.currentItem().text()
        self.crypter.load_master_key(self.settings.getMKFilename(self.choosed_db))
        self.auth.setWindowModality(QtCore.Qt.ApplicationModal)
        self.auth.show()

    def on_confirm_clicked(self):
        # User have 3 attempt to write Master Key
        if self.__attempt > 1:
            master_key = self.auth.leMasterKey.text()
            # Check storage hash of master key with MK which get from user
            if(self.crypter.check_master_key(master_key)):
                # If MK which user input is good read data from DB
                self.view_window = ViewWindow(self.choosed_db, self.crypter)
                self.stack.addWidget(self.view_window)
                self.view_window.initForm()
                # Change Main widget and show data
                self.stack.setCurrentIndex(1)
                # Close auth form
                self.auth.close()
            else:
                # If MK is wrong clear Line Edit
                # Attempt decrease
                self.__attempt -= 1
                self.auth.lbInfo.setText(f"Enter Master Key\nYou have {self.__attempt} attempt")
                self.auth.leMasterKey.setText("")
        else:
            # If attempt was expend app will be close
            self.auth.close()
            self.close()
            sys.exit()

    def __initUi(self):
        self.setWindowTitle("Password Defender")
        # Init all forms
        self.stack = QStackedWidget(self)
        self.start_window = StartWindow(self.settings)
        self.auth = AuthWindow()
        # Add all forms to Stack for changing state
        self.stack.addWidget(self.start_window)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.stack)
        self.setLayout(mainLayout)
        # Connect all handler event function
        self.start_window.btnOpen.clicked.connect(self.on_open_clicked)
        self.auth.btnConfirm.clicked.connect(self.on_confirm_clicked)
        self.start_window.newBtn.clicked.connect(self.on_new_clicked)


def main():
    app = QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
