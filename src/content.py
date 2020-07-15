import os
import json
from datetime import datetime
import urllib.parse

import config
from pymongo import MongoClient
from database import database_manager
from collections import OrderedDict

from telegram.utils import helpers as helpers

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
        
        escaped_title = helpers.escape_markdown(self.trim_title(job['title']),2)
        escaped_comanpy = helpers.escape_markdown(job['company'],2)
        escaped_location = helpers.escape_markdown(job['location'],2)
        escaped_region = helpers.escape_markdown(job['region'],2)
        escaped_summary = helpers.escape_markdown(job['summary'],2)

        view_content = '*{title}*\n{company}\n{location}, {region}\n{summary}\n[More Detail]({url})'.format( 
                title = escaped_title, 
                company = escaped_comanpy, 
                location = escaped_location, 
                region = escaped_region, 
                summary = escaped_summary, 
                url = self.format_url(job['url'])
            )
        return view_content

    def format_url(self, url):
        return url_template.format(job_url = urllib.parse.quote(url))

    def publish_content(self):
        job_dict = self.read_daily()
        return job_dict

    def trim_title(self, title):
        if title.endswith('new'):
            title = title[:-4]
            return title