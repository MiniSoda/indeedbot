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
  
    def get_jobs_count(self):
        count = self.database.get_jobs_count()
        return count

    def get_jobs_count_all(self):
        return self.database.get_jobs_count_all()

    def read_daily(self):
        job_list = self.database.get_jobs_today()
        job_dict = OrderedDict()
        for job in job_list:
            job_dict.update({job['_id'] : self.format_job_info(job)})
        return job_dict

    def format_job_info(self, job):
        view_content = r'###{title}\n{company}\{location}, {region}\n{summary}\n(More Detain)[{url}]'.format( title = job['title'], 
                company = job['company'], 
                location = job['location'], 
                region = job['region'], 
                summary = job['summary'], 
                url = self.format_url(job['url']))
        return view_content

    def format_url(self, url):
        return url_template.format(job_url = urllib.parse.quote(url))

    def publish_content(self):
        job_dict = self.read_daily()
        return job_dict

