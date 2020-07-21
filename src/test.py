from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient
from content import content_manager

client = MongoClient(host="nas.imangoo.site", port=27017)
database = client["indeed_spider"]
collection = database["jobs"]

#ci test script
#TODO: test should be used as a CI script, however testing a DB within intranet is tricky