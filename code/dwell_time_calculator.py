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
__copyright__ = "Copyright (c) 2021 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"





from asyncore import read
from glob import glob
import logging
import json
from operator import contains
from pydoc import cli
from turtle import st
import requests
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import asyncio
import math
import csv
import pprint
from io import StringIO
import datetime




location_visit_map = dict()
previous_location = ''


def get_locationvisitmap() :
    return location_visit_map


#Determine which shape a point falls under, where a shape represents an object
def determine_location(point, shapes) :

    for shape_dict in shapes:
        if list(shape_dict.values())[0].contains(point) :
            return list(shape_dict.keys())[0] #we just want to return the name of the shape



#If the client is seen at a new location in one session, we can increment the visit counter for the corresponding locations
def update_visits_per_client(location) :
    global previous_location
    if previous_location != location :
        if location in list(location_visit_map.keys()) :
            location_visit_map[location] +=1 
        else :
            location_visit_map[location] = 1

        previous_location = location




#main function to calculate dwell time
def dwell_time_calculator(shapes, report) :

    print("ENTERING DWELL TIME CALCULATION")




    overall_dwell_times = dict()
  



    mac_address_set = set()


    #Get the set of appropriate MAC Addresses to consider (ignoring Meraki) 
    for row in report :
            if row['campusid'] == '<Enter relevant Campus ID>': # COMMENT THIS LINE OUT IF YOU DO NOT HAVE MERAKI NETWORKS TO IGNORE
                    mac_address_set.add(row['macaddress'])
    print(f"MAC ADDRESSES CONSIDERED: {mac_address_set}")





    for client in mac_address_set :
        #Going to analyze visits per client
        client_records = [x for x in report if x['macaddress'] ==  client]


        
        trip_startpoints = set()

        #Getting all the the visit start-times per client, the 'firstactiveat' field in the report can be used to distinguish different visits
        for row in client_records:

            if 'firstactiveat' in list(row.keys()):
                trip_startpoints.add(int(row['firstactiveat']))



        client_records.sort(key=lambda x : x['sourcetimestamp'])
  

        for start in trip_startpoints :
            latest_timestamp = 0

            for row in client_records:

                if int(row['firstactiveat']) == start:
                    print(int(row['sourcetimestamp']), start, 'latest_timestamp:', latest_timestamp)
                    location = determine_location( Point( float(row['coordinatex']), float(row['coordinatey']) ), shapes )#get the current location
                    update_visits_per_client(location) 
                         
                         
                    #for every sample after the first one, look at the difference in timestamps to get delta and add to the appropriate counter in the dictionary
                    if int(row['sourcetimestamp']) > latest_timestamp:
                        if latest_timestamp > 0:

                            if location in list(overall_dwell_times.keys() ):
                                overall_dwell_times[location] += int(row['sourcetimestamp']) - latest_timestamp

                            else:
                                overall_dwell_times[location] = int(row['sourcetimestamp']) - latest_timestamp


                    #for first time, we see the difference betweeen time of polling and time when the visit first became star  
                        else:

                            if location in list( overall_dwell_times.keys() ):
                                overall_dwell_times[location] += int(row['sourcetimestamp']) - start
                            else:
                                overall_dwell_times[location] = int(row['sourcetimestamp']) - start
                            
                           
                        latest_timestamp = int(row['sourcetimestamp'])
                        

      

    location_visit_map = get_locationvisitmap()



    #Printing some stats to STDOUT

    print('----------------------------')
    print('Dwell time statistics')
    print('\nVisits per location:')
    pprint.pprint(location_visit_map)
    print('\nHours spent on average per visit:')

  
    for location, times in overall_dwell_times.items() :
        
        overall_dwell_times[location] = (times/3600000 )/ location_visit_map[location]
    pprint.pprint(overall_dwell_times)


    print('----------------------------')




    return overall_dwell_times

