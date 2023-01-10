# This Python file uses the following encoding: utf-8
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QFont

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self.__data = data
        self.__rowCount = len(self.__data)
        self.__horizontal_data = []

    def rowCount(self, index = QModelIndex()) -> int:
        return self.__rowCount

    def columnCount(self, index = QModelIndex()):
        if self.__rowCount > 0:
            return len(self.__data[0])

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setData(self, index, value, role = Qt.EditRole):
        if role == Qt.EditRole and value:
            self.__data[index.row()][index.column()] = value
            return True
        return False

    def data(self, index, role = Qt.DisplayRole):
        if role == Qt.DisplayRole and index.isValid():
            if index.column() == 3:
                return str('*' * 15)
            else:
                return self.__data[index.row()][index.column()]

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


