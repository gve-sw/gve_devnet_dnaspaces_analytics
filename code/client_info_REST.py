"""
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Ozair Saiyad <osaiyad@cisco.com>"
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"





from env_vars import *
import logging
import json
import requests
import asyncio
import math
import pprint
import csv 
import datetime
import pymongo
import certifi
import pprint


logging.basicConfig(filename='ble.log', level=logging.DEBUG,
format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
datefmt='%H:%M:%S')


base_url = 'https://dnaspaces.io/api/location/v1'

dnaspaces_url_history = f'{base_url}/history'
dnaspaces_url_history_records = f'{base_url}/history/records'
dnaspaces_url_history_count= f'{base_url}/history/records/count'
dnaspaces_url_active_clients = f'{base_url}/clients'
dnaspaces_url_map = f'{base_url}/map/hierarchy'

headers = {
    'Authorization' : 'Bearer {}'.format(REST_API_KEY),
    'Content-Type': 'application/json'
}



client_records = requests.request('GET', url= dnaspaces_url_history, headers= headers )
with open('User_Location_Data.csv', 'w+') as outputfile:
    outputfile.write(client_records.text)



# TRIED CLIENT HISTORY ENDPOINT
# client_history_records = requests.request('GET', url= dnaspaces_url_history_records, headers= headers )
# print(client_history_records.text)
# with open('User_Location_Data_Records.csv', 'w+') as outputfile:
#     outputfile.write(client_history_records.text)


client_count = requests.request('GET',url= dnaspaces_url_history_count, headers= headers )
pprint.pprint(client_count.text)


# map = requests.request('GET',url= dnaspaces_url_map, headers= headers )
# pprint.pprint(map.json())

# active_clients = requests.request('GET',url= dnaspaces_url_active_clients, headers= headers )
# pprint.pprint(active_clients.headers)
# pprint.pprint(active_clients.text)



            



          