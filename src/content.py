import os
import json
from datetime import datetime
import urllib.parse

import config
from pymongo import MongoClient
from database import database_manager
from collections import OrderedDict

#url should be filled with encoded url
url_template = r'https://t.me/iv?url={job_url}&rhash=0a7f50a497a51b'

class content_manager():
    def __init__(self, database_manager):
        self.database = database_manager
        #{ job_id : job_formatted_info }
        self.job_list = OrderedDict{}
            
    def get_jobs_count():
        count = self.database_manager.get_jobs_count();
        return count

    def get_jobs_count_all():
        return count

    def read_daily():
        jobs_collection = self.jobs_collection
        days_adjust = 1
        start = datetime.today() - timedelta(days=days_adjust)
        end = datetime.today()
        self.job_list = self.database_manager.get_jobs_between(start,end)
        return self.job_list


    def format_job_info(job):
        view_content = '###{title}\n{company}\{location}, {region}\n{summary}\n(More Detain)[{url}]'.format( title = job.title, 
                company = job.company, 
                location = job.location, 
                region = job.region, 
                summary = job.summary, 
                url = format_url(job.url))

    def format_url(url):
        return url_template.format(job_url = urllib.parse.quote(url))
