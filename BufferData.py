# This Python file uses the following encoding: utf-8
from PyQt5 import QtSql
# Custom packages
from Crypter import Crypter
from TableModel import TableModel


class BufferData:
    """ Buffer class between View and Database,
        This class control reading, writing and encrypting data
    """

    SUCCESS = 0
    DB_OPEN_FAILED = 1
    QUERY_EXEC_FAILED = 2
    REMOVE_ROW_FAILED = 3
    INSERT_ROW_FAILED = 4

    def __init__(self, crypter: Crypter, path: str):
        self.__crypter = crypter
        self.__db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.__db.setDatabaseName(path)
        self.readData()
        if self.model:
           print("Read data : DONE")
        else:
            print("DB wasn`t open")

    def readData(self):
        if self.__db.open():
            query = QtSql.QSqlQuery("SELECT * FROM user_data")
            data = []
            while query.next():
                print("Query exec")
                row = []
                id = query.value(0)
                domain = self.__crypter.decrypt(query.value(1).encode())
                username = self.__crypter.decrypt(query.value(2).encode())
                password = self.__crypter.decrypt(query.value(3).encode())
                description = self.__crypter.decrypt(query.value(4).encode())

                row.append(id)
                row.append(domain.decode())
                row.append(username.decode())
                row.append(password.decode())
                row.append(description.decode())
                data.append(row)

            self.model = TableModel(data)
            self.model.setHeaderData(0, "ID")
            self.model.setHeaderData(1, "Domain")
            self.model.setHeaderData(2, "Username")
            self.model.setHeaderData(3, "Password")
            self.model.setHeaderData(4, "Description")
        self.__db.close()

    def removeRow(self, id: int) -> int:
        if self.__db.open():
            query = QtSql.QSqlQuery()
            query.prepare(f"DELETE FROM user_data WHERE id = '{id}'")
            if query.exec_():
                if self.model.remove(id):
                    self.__db.close()
                    return self.SUCCESS
                else:
                    self.__db.close()
                    return self.REMOVE_ROW_FAILED
            else:
                self.__db.close()
                return self.QUERY_EXEC_FAILED
        else:
            return self.DB_OPEN_FAILED


    def editRow(self, row: int) -> int:
        ...

    def addRow(self, list_data: list) -> int:
        if self.__db.open():
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO user_data VALUES(?,?,?,?,?)")
            list_data.insert(0, self.model.rowCount() + 1)
            for i, value in enumerate(list_data):
                if i == 0:
                    query.bindValue(i, value)
                else:
                    query.bindValue(i, self.__crypter.encrypt(value).decode())
            if query.exec_():
                if self.model.insert(list_data):
                    self.__db.close()
                    return self.SUCCESS
                else:
                    self.__db.close()
                    return self.INSERT_ROW_FAILED
            else:
                self.__db.close()
                return self.QUERY_EXEC_FAILED
        else:
            return self.DB_OPEN_FAILED

