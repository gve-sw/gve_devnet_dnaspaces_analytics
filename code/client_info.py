import logging
import json
import requests
import asyncio
import math
import pprint
import datetime
import pymongo
import certifi


logging.basicConfig(filename='ble.log', level=logging.DEBUG,
format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
datefmt='%H:%M:%S')

dnaspaces_url = 'https://partners.dnaspaces.io/api/partners/v1/firehose/events'

headers = {
    'X-API-Key' : '<Enter API Key>'
}



with requests.request('GET', url=dnaspaces_url, headers=headers, data={}, stream=True) as response:
    for line in response.iter_lines() :
        if line:
            resp_string = line.decode('utf8')
            # print(resp_string)
            resp_dict = json.loads(resp_string)
            pprint.pprint(resp_dict)
            



          
