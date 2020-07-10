import os
import json
from datetime import datetime

import config
from pymongo import MongoClient
from database import database_manager

class content_manager():
    def __init__(self):
        with open(os.path.join('/etc/teledeed', 'settings.json'), 'r') as f:
            settings = json.load(f)

        self.settings = settings
        self.database = database_manager(settings['db'])
        self.jobs_collection = database[config.job_collection]
            
    def get_daily_jobs_count():
        days_adjust = 1
        start = datetime.today() - timedelta(days=days_adjust)
        end = datetime.today()

        count = len(self.jobs_collection.find( {'real_pub_date': {'$lt': end, '$gte': start}}))
        return count

    def read_daily():
        jobs_collection = self.jobs_collection
        days_adjust = 1
        start = datetime.today() - timedelta(days=days_adjust)
        end = datetime.today()

        for job in job_collection.find( {'real_pub_date': {'$lt': end, '$gte': start}}):
            continue
    
    def format_jobs():
        pass