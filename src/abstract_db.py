from pymongo import MongoClient

class abstract_database():
    def __init__(self, connection_settings):
        self.connection_settings
        self.is_connected = False
        self.client
        self.database
        self.job_collection

    def connect():
        if not is_connected:
            self.is_connected = True
            self.client = MongoClient(host=self.connection_settings['MONGO_HOST'], port=self.connection_settings['MONGO_PORT'])
            self.database = client['MONGO_DATABASE']
            self.job_collection = self.database['job_collection']
        else:
            pass

    def close():
        pass

    def create():
        pass

    def read():
        pass

    def update():
        pass

    def delete():
        pass