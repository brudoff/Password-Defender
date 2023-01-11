# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QShortcut
from PyQt5.QtSql import QSqlRecord
from PyQt5 import uic


class NewEntryWindow(QWidget):
    """ Class which represent New Entry Form """
    # Create custom signal which emit
    # When user click submit Button
    submitClick = QtCore.pyqtSignal(list)

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("Form/NewEntryForm.ui", self)
        self.setLayout(self.mainLayout)
        self.submitBtn.clicked.connect(self.submitEntry)

        # Fast fill
        self.fillShortcut = QShortcut(QtGui.QKeySequence('Ctrl+Q'), self)
        self.fillShortcut.activated.connect(self.fillFields)

    def submitEntry(self):
        # Check all fileds if data was inputed
        # If filed must have some value, but not generate MessageBox
        _domain = self.domainLe.text()
        _username = self.usernameLe.text()
        _password = self.passwordLe.text()
        _description = self.descriptionLe.text()
        # After click on submit button emit signal which send inserted data
        self.submitClick.emit([_domain, _username, _password, _description])
        self.close()

    def fillFields(self):
        self.domainLe.setText("facebook.com")
        self.usernameLe.setText("facebook@gmail.com")
        self.passwordLe.setText("Test_Password2")
        self.descriptionLe.setText("Example description2")

