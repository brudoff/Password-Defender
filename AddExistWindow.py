# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5 import uic
from PyQt5 import QtCore


class AddExistWindow(QWidget):
    # Custom signal which emit when user click to submit button
    # This signal send pathes of pair database/master key
    added_database = QtCore.pyqtSignal(str, str)

    def __init__(self):
        self.__db_path = None
        self.__mk_path = None

        QWidget.__init__(self)
        uic.loadUi("Form/AddExistDbForm.ui", self)
        self.setLayout(self.mainLayout)
        # Connect signals with slots
        self.openDbBtn.clicked.connect(self.on_openDb_clicked)
        self.openMkBtn.clicked.connect(self.on_openMk_clicked)
        self.submitBtn.clicked.connect(self.on_submit_clicked)

    def on_openDb_clicked(self):
        db_dialog = QFileDialog.getOpenFileName(self,
                                "Choose Database", "C:\\", "Database (*.db)")
        self.__db_path = db_dialog[0]
        self.pathDbLe.setText(self.__db_path)


    def on_openMk_clicked(self):
        mk_dialog = QFileDialog.getOpenFileName(self,
                                "Choose Database", "C:\\", "Database (*.key)")
        self.__mk_path = mk_dialog[0]
        self.pathMkLe.setText(self.__mk_path)

    def on_submit_clicked(self):
        self.added_database.emit(self.__db_path, self.__mk_path)
        self.close()
