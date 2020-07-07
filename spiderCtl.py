import requests

URL = 'http://{0}/schedule.json'

def spider_run(url):
    url = URL.format(url)
    data = {
    'project': 'indeed',
    'spider': 'indeed_jobs'
    }
    response = requests.post(url, data=data)
    return response.status_code, response.content