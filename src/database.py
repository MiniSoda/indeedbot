import os
import json
from datetime import datetime

from pymongo import MongoClient

class database_manager():
    def __init__(self, database_settings):
        self.database_settings = database_settings
        self.is_connected = False
        """
        self.client
        self.database
        self.job_collection
        self.search_collection
        self.bot_settings_collection
        """
        self.__connect__()
        

    def __connect__(self):
        if not self.is_connected:
            self.is_connected = True
            self.client = MongoClient(host=self.database_settings['MONGO_HOST'], port=self.database_settings['MONGO_PORT'])
            self.database = self.client['indeed_spider']
            self.job_collection = self.database['job']
            self.search_collection = self.database['search_criteria']
            self.bot_settings_collection = self.database['telegram_bot_setting']
        else:
            pass

    
    def get_job_count_today(self):
        job_daily_list = []
        days_adjust = 1
        start = datetime.today() - timedelta(days=days_adjust)
        end = datetime.today()
        job_daily_list = get_jobs_between(start, end)
        return len(job_daily_list)


    def get_job_count_all(self):
        return len(self.job_collection.find({}))


    def get_jobs_today(self):
        days_adjust = 1
        start = datetime.today() - timedelta(days=days_adjust)
        end = datetime.today()
        job_daily_list = get_jobs_between(start, end)
        return job_daily_list


    def get_jobs_between(self, start, end):
        #check start, end validity
        job_list = []
        for job in self.jobs_collection.find({'real_pub_date': {'$lt': end, '$gte': start}}):
            job_list.append(job)
        return job_list


    def get_scrawler_schedule(self):
        cursor = self.bot_settings_collection.find({'name':'scrawler_schedule'})
        return cursor[0]['schedule']


    def get_publish_schedule(self):
        cursor = self.bot_settings_collection.find({'name':'publish_schedule'})
        return cursor[0]['schedule']


    def get_scrawler_urls(self):
        url_list = []
        for url in self.search_collection.find({}):
            if url['inuse']:
                url_list.append(url)
        return url_list


    def set_scrawler_urls(self):
        cursor = self.bot_settings_collection.find_and_update({'name':'scrawler_schedule'})


    #schedule : '0300' string stands for a timepoint 03:00
    def set_scrawler_schedule(self, schedule):
        self.bot_settings_collection.find_one_and_update( {'name':'scrawler_schedule'}, {'$set': {'schedule': schedule}} )


    #schedule : '0930' string stands for a timepoint 09:30
    def set_publish_schedule(self, schedule):
        self.bot_settings_collection.find_one_and_update( {'name':'publish_schedule'}, {'$set': {'schedule': schedule}})