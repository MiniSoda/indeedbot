import os
import json

from pymongo import MongoClient
from abstract_db import abstract_database

class database_manager(abstract_database):
    def __init__(self, database_settings):
        super(abstract_database, self).__init__(database_settings)

    def get_job_count(self, date_range):
        pass

    def get_job_brief(self, count):
        pass

    def set_scrapper_runtime(self, runtime):
        pass

    def get_scrapper_runtime(self, runtime):
        pass

    def get_scrapper_runcmd(self, cmd):
        pass

    