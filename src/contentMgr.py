import os
import json

from pymongo import MongoClient

class contentMgr():
    with open(os.path.join('/etc/telegram', 'settings.json'), 'r') as f:
        db_settings = json.load(f)
        mongo_host = db_settings['db']['MONGO_HOST']
        mongo_port = db_settings['db']['MONGO_PORT']
        mongo_database = db_settings['db']['MONGO_DATABASE']
        collection_name = db_settings['db']['collection_name']
        daily_limit = db_settings['daily_limit']
        
    client = MongoClient(host=mongo_host, port=mongo_port)
    database = client[mongo_database]
    collection = database[collection_name]

    def readDaily():
        