import os
import json

from pymongo import MongoClient
from database import database_manager

class content_manager():
    def __init__(self):
        with open(os.path.join('/etc/teledeed', 'settings.json'), 'r') as f:
            settings = json.load(f)

        self.settings = settings
        self.database = database_manager(settings['db'])
            
    def readDaily():
        