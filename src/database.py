import os
import json
from datetime import datetime

from pymongo import MongoClient
from abstract_db import abstract_database

class database_manager(abstract_database):
    def __init__(self, database_settings):
        super(abstract_database, self).__init__(database_settings)
        self.job_list = []

    def get_job_count(self, date_range):
        if len(self.job_list) == 0:
            days_adjust = 1
            start = datetime.today() - timedelta(days=days_adjust)
            end = datetime.today()
            self.get_jobs_between(start, end)
        return len(self.job_list)

    def get_job_count_all(self):
        return len(self.job_collection.find({}))

    def get_jobs_between(self, start, end):
        #check start, end validity
        if len(self.job_list) == 0 :
            for job in self.jobs_collection.find({'real_pub_date': {'$lt': end, '$gte': start}}):
                self.job_list.append(job)
        return self.job_list

    def get_scrawler_schedule():
        cursor = self.bot_settings_collection.find({'name':'scrawler_schedule'})
        return cursor[0]['schedule']

    def set_scrawler_schedule(string schedule):
        pass

    def get_scrawler_urls():
        pass

    def set_scrawler_urls():
        pass

    #should reset before shedule
    def clear_memory():
        self.job_list = []
