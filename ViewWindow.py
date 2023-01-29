# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
# Custom packages
from NewEntryWindow import NewEntryWindow
from Crypter import Crypter
from BufferData import BufferData
import pyperclip as pc


class ViewWindow(QWidget):
    def __init__(self, db_name: str, crypter: Crypter, db=None):
        QWidget.__init__(self)
        uic.loadUi("Form/ViewForm.ui", self)
        if not db:
            self.buffer = BufferData(crypter, db_name)
        else:
            self.buffer = BufferData(crypter, "", db)
        # Connect all slots with signals
        self.newEntryBtn.clicked.connect(self.showEntryForm)
        self.deleteBtn.clicked.connect(self.on_delete_clicked)
        self.clipboardBtn.clicked.connect(self.on_clipboard_clicked)

    def initForm(self):
        self.setLayout(self.mainFormLayout)
        self.viewData.setModel(self.buffer.model)
        self.viewData.setColumnWidth(0, 15)
        self.viewData.setColumnWidth(1, 120)
        self.viewData.setColumnWidth(2, 150)
        self.viewData.setColumnWidth(3, 150)
        self.viewData.setColumnWidth(4, 260)

    def showEntryForm(self):
        self.new_entry = NewEntryWindow()
        self.new_entry.show()
        self.new_entry.submitClick.connect(self.on_add_entry)

    def on_add_entry(self, insert_data):
        self.buffer.addRow(insert_data)

    def on_delete_clicked(self):
        index = self.viewData.currentIndex()
        id = index.siblingAtColumn(0).data()
        self.buffer.removeRow(id)

    def on_clipboard_clicked(self):
        index = self.viewData.currentIndex()
        password = self.buffer.model.data(index.siblingAtColumn(3), -1)
        pc.copy(password)


