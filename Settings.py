# This Python file uses the following encoding: utf-8
# Setting
import json
import os


class Settings:
    def __init__(self):
        self.settings_file = "settings.json"
        self.db_info = dict()
        self.load()

    def getDbList(self):
        if len(self.db_info) > 0:
            return self.db_info.values()
        return list()

    def getMKFilename(self, db_name):
        if len(self.db_info) > 0:
            for key, value in self.db_info.items():
                if value == db_name:
                    return key
        return None

    def appendNewDB(self, db_name, mk_filename):
        self.json_data['databases'].append({'mk' : mk_filename, 'path' : db_name})
        with open(os.path.join(os.getcwd(), self.settings_file), 'r+') as jfile:
            jfile.seek(0)
            json.dump(self.json_data, jfile)

    def __read_settings(self):
        with open(os.path.join(os.getcwd(), self.settings_file)) as jfile:
            self.json_data = json.load(jfile)
            used_db = self.json_data['databases']
            for pair in used_db:
                key = pair['mk']
                value = pair['path']
                self.db_info[key] = value

    def __create_settings_file(self):
        with open(os.path.join(os.getcwd(), self.settings_file), 'w') as jfile:
            json_data = {
                "databases" :[
                {
                    "mk" : "master_key.key",
                    "path" : "D:\\Python\\Qt\\PasswordDefender\\data.db"
                }]
            }
            json.dump(json_data, jfile)

    def load(self):
        if os.path.isfile(self.settings_file):
            self.__read_settings()
        else:
            self.__create_settings_file()
            self.__read_settings()
