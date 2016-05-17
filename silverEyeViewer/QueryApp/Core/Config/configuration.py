import json
import os

from pymongo import MongoClient

file_config_name = "config_production.json"


class Configuration:

    def __init__(self):
        self.client = None
        self.database_name = None
        self.database_ip = None
        self.database_port = None

    def load_config_file(self):
        with open(os.path.dirname(os.path.dirname(__file__))+"/Config/"+file_config_name, 'r') as f:
            config = json.load(f)
            self.database_name = config['database_name']
            self.database_ip = config['database_ip']
            self.database_port = config['database_port']

    def get_client(self):

        if self.client is None:
            self.load_config_file()
            self.client = MongoClient(self.database_ip, self.database_port, connect=True)
            return self.client
        else:
            return self.client


    def get_database_name(self):
        if self.database_name is None:
            self.load_config_file()
            return self.database_name
        else:
            return self.database_name


if __name__ == '__main__':
    configuration = Configuration()
    print configuration.get_client()
    print configuration.get_database_name()
    print configuration.database_ip
    print configuration.database_port
