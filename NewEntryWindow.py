# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QShortcut
from PyQt5.QtSql import QSqlRecord
from PyQt5 import uic
from string import ascii_letters, digits, punctuation
import secrets


class NewEntryWindow(QWidget):
    """ Class which represent New Entry Form """
    # Create custom signal which emit
    # When user click submit Button
    submitClick = QtCore.pyqtSignal(list)
    characters = ascii_letters + digits + punctuation

    def __init__(self):
        # Init form
        QWidget.__init__(self)
        uic.loadUi("Form/NewEntryForm.ui", self)
        self.setLayout(self.mainLayout)
        self.passwordLengthChanged()
        # Connect slots/signals
        self.submitBtn.clicked.connect(self.submitEntry)
        self.lengthPasswordSlider.valueChanged.connect(self.passwordLengthChanged)
        self.generateBtn.clicked.connect(self.generatePassword)
        # Fast fill
        self.fillShortcut = QShortcut(QtGui.QKeySequence('Ctrl+Q'), self)
        self.fillShortcut.activated.connect(self.fillFields)

        print(self.characters)

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
        self.domainLe.setText("test.com")
        self.usernameLe.setText("test@gmail.com")
        self.passwordLe.setText("Test_Password1")
        self.descriptionLe.setText("Example description1")

    def passwordLengthChanged(self):
        lbText = f"Password length : {self.lengthPasswordSlider.value()}"
        self.lengthPasswordLb.setText(lbText)

    def generatePassword(self):
        pswd = ""
        for i in range(0, self.lengthPasswordSlider.value()):
            pswd += secrets.choice(self.characters)
        self.passwordLe.setText(pswd)

