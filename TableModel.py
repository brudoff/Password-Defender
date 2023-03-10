# This Python file uses the following encoding: utf-8
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QFont
from PyQt5 import QtCore


class TableModel(QAbstractTableModel):
    # Custom signal which emit after changing data
    cellChanged = QtCore.pyqtSignal(int, str, str)

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self.__data = data
        print(len(self.__data))
        self.__rowCount = len(self.__data)
        self.__horizontal_data = []

    def rowCount(self, index = QModelIndex()):
        return self.__rowCount

    def columnCount(self, index = QModelIndex()):
        if self.rowCount() > 0:
            return len(self.__data[0])
        else:
            return 0

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        else:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def setData(self, index, value, role = Qt.EditRole):
        if role == Qt.EditRole and value and index.column() != 0:
            self.__data[index.row()][index.column()] = value
            id = self.__data[index.row()][0]
            fieldName = self.__horizontal_data[index.column()]
            self.cellChanged.emit(id, value, fieldName)
            return True
        return False

    def data(self, index, role = Qt.DisplayRole):
        if role == Qt.DisplayRole and index.isValid():
            if index.column() == 3:
                return str('*' * 15)
            else:
                return self.__data[index.row()][index.column()]
        # If role equal -1 data should return password for clipboard
        if role == -1 and index.column() == 3:
            return self.__data[index.row()][3]


    def setHeaderData(self, section, value):
        self.__horizontal_data.insert(section, value)

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return str(self.__horizontal_data[section])
            if role == Qt.FontRole:
                header_font = QFont("Aller", 12, QFont.Bold)
                return header_font

    def insert(self, row):
        if isinstance(row, list):
            self.__data.append(row)
            self.__rowCount += 1
            self.layoutChanged.emit()
            return True
        return False

    def remove(self, id):
        for i, row in enumerate(self.__data):
            if row[0] == id:
                self.__data.remove(row)
                self.__rowCount -= 1
                self.layoutChanged.emit()
                return True
        return False


