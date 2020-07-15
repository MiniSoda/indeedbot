from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient

client = MongoClient(host="beiaurum01", port=27017)
database = client["indeed_spider"]
collection = database["search_criteria"]

#collection.update({}, {"$set": {"inuse": True}}, multi= True)
"""
start_urls = []
for criteria in collection.find({}):
        if criteria['inuse']:
            start_urls.append(criteria['url'])
            base_url = get_base_url(criteria['url'])
            region = criteria['region']
            url2region_dict[base_url] = region

print(url2region_dict)

days_adjust = 1
start = datetime.today() - timedelta(days=days_adjust)
end = datetime.today()
job_collection = database["jobs"]

for job in job_collection.find( {'real_pub_date': {'$lt': end, '$gte': start}}):
    print(job)

"""
clock = datetime.now()
time = clock.strftime("%H:%M:%S")
print("time:", time)
message = "Hi MiniSoda, it's " + time