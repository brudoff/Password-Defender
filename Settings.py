# This Python file uses the following encoding: utf-8
# Setting
import json
import os


class Settings:
    def __init__(self):
        self.settings_file = "settings.json"
        self._data = dict()
        self.load()

    def getDbList(self):
        if len(self._data) > 0:
            return self._data.values()

    def load(self):
        try:
            with open(os.path.join(os.getcwd(), self.settings_file), 'r') as jfile:
                data = json.loads(json.load(jfile))
                db_key_pairs = data['databases']
                for pair in db_key_pairs:
                    key = pair['mk']
                    value = pair['path']
                    self._data[key] = value

        except FileNotFoundError:
            with open(os.path.join(os.getcwd(), "settings.json"), 'w') as jfile:
                json_data = """
                {
                    "databases" :[
                    {
                        "mk" : "master_key.key",
                        "path" : "D:/Python/Qt/PasswordDefender/data.db"
                    }]
                }"""
                json.dump(json_data, jfile)
