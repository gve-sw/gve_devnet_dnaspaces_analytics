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





from asyncio.base_futures import _future_repr_info
from cProfile import label
import imp
from mimetypes import init
from pprint import pp, pprint
from env_vars import *

import requests
import json
import pprint
from dwell_time_calculator import dwell_time_calculator
from kneed import KneeLocator
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import csv
from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score
import numpy as np
import seaborn as sns



# dimensions = tuple()
floor_collection = dict()

cluster_collection = dict()
point_index_map = list()
shapes = list()
units = 'FEET'

base_url = 'https://dnaspaces.io/api/location/v1'

dnaspaces_url_map = f'{base_url}/map/hierarchy'

headers = {
    'Authorization' : 'Bearer {}'.format(REST_API_KEY),
    'Content-Type': 'application/json'
}




#Get info about the floor plan such as units, length/width, and floors in a building
map_heirarchy = requests.request(method='GET', url=dnaspaces_url_map, headers= headers).json()


for site in map_heirarchy['map'] :
    # print(site)
        item_ref = site
        buildings = item_ref['relationshipData']['children']
        for building in buildings :
            floors = building['relationshipData']['children']
            for floor in floors:
                floor_length = floor['details']['length']
                floor_width = floor['details']['width']
                floor_name = floor['name']
                units = floor['details']['units']
                floor_id = floor['id']
                print(units)

                floor_collection[floor_id] = (floor_name,floor_length,floor_width )

print(floor_collection)
floor_id = list(floor_collection.keys())[0]
length = floor_collection[floor_id][1]
width = floor_collection[floor_id][2]



#Method for getting number of clusters based on 'smooth surfaces' in scatter plot
def mean_shift_handler(X) :
    bandwidth = estimate_bandwidth(X, 
                               quantile=0.3, 
                               n_jobs=-1)
    ms = MeanShift(bandwidth=bandwidth, 
                bin_seeding=False, 
                n_jobs=-1, 
                max_iter=500)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)
    print(f"Number of estimated clusters : {n_clusters_}")


    P = ms.predict(X)


    return n_clusters_



#Method for finding optimal K value based on finding an 'elbow' in a weighted metric 
def elbow_method(X) :
    # A list holds the SSE values for each k
    sse = []
    for k in range(1, 11): #Trying between 1 and 11 ---> for larger floors change this range, otherwise it will max at 11 for k !!!
        kmeans =KMeans(
              init="random",
              n_clusters = k,
              n_init=10,
              max_iter=500,
              random_state=42
               )
        kmeans.fit(X)
        sse.append(kmeans.inertia_)
        
    kl = KneeLocator(
        range(1, 11), sse, curve="convex", direction="decreasing"
   )
   
    return kl.elbow


#Method for finding optimal K value based on finding the highest point in a  metric (silhouette score) 
def silhouette_method(X) :

    silhouette_coefficients = []

   # Notice you start at 2 clusters for silhouette coefficient
    for k in range(2, 11):
        kmeans = KMeans(
              init="random",
              n_clusters = k,
              n_init=10,
              max_iter=500,
              random_state=42
               )

        kmeans.fit(X)

        kmeans.inertia_


        score = silhouette_score(X, kmeans.labels_)
        silhouette_coefficients.append(score)
    
    print(silhouette_coefficients)

    silhouette_coefficients = list(silhouette_coefficients)

    return silhouette_coefficients.index( max(silhouette_coefficients) )+2 


# Does the K means clustering, provided feautres -X- as input
def k_means_handler(X) :


    k = elbow_method(X)

    #color pallette for the clusters
    sns.color_palette("husl", 9)
    color = plt.cm.rainbow(np.linspace(0, 1, k))
    print(color)






    kmeans = KMeans(
              init="random",
              n_clusters = k,
              n_init=10,
              max_iter=500,
              random_state=42
               )

    kmeans.fit(X)



    #assigning colour to each cluster
    P = kmeans.labels_
    colors = tuple(map(lambda x: color[x] , P))
    print(X)
    labels = map( lambda x : f'Cluster {x}', range(1, k+1) )
    kmeans_plot = plt.scatter(X[:,0], X[:,1],  c=colors, marker="o", picker=True)
    plt.title(f'Estimated number of clusters = {k}')

 



    print(kmeans.cluster_centers_)
    print(X)
    print(kmeans.labels_, type(kmeans.labels_))

    #centroids
    plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1], color='black' )

    plt.xlabel(f'X Values- {units} ')
    plt.ylabel(f'Y Values- {units} ')

    plt.show()

    #Using data structures to hold the points and index in each cluster
    zip_label_point = zip(P, X)

    for i in range(1, k+1) :
        cluster_collection['Cluster_{0}'.format(i)] = list()

    for index, value in enumerate(zip_label_point) :
        label = value[0]
        point = value[1]
        cluster_collection['Cluster_{0}'.format(label+1)].append((point, point_index_map[index] ) )

    pprint.pprint(cluster_collection)

    return cluster_collection



#Returns 'row' that contains a point by comapring the index values (note only giving timestamp, macaddress, ssid, username and coordinate to keep it concise for now)
def get_row_from_point(point_with_index, report_dict_list) :

    for item in report_dict_list :
        if item['index'] == point_with_index[1] :
            print(item['index'], item['sourcetimestamp'], item['macaddress'], item['ssid'], item['username'],  ( item['coordinatex'], item['coordinatey'] ) )

            return item


#Reads the CSV file report to output a list of points, and the rows of the report in a python dictionary datastructure
def read_points(filename) :
    point_collection = list()
    report_dict_list = list()
    with open(filename) as input: 

        reader = csv.DictReader(input)
        print("ROWS:", reader.__sizeof__())

    
        for index, row in enumerate(reader) :


            
            # print(row['floorhierarchy'])
            if row['floorhierarchy'] == 'Test-Location->Home->Building1->Floor 1' :


                index_dict = {'index' : index}

                point_collection.append(Point( [ float(row['coordinatex']), float(row['coordinatey']) ]) )
                row.update(index_dict)

                report_dict_list.append(row)
                point_index_map.append(index)


    
    report_dict_list.sort(key=  lambda x : x['index'])
    return report_dict_list, point_collection

        


#Plots quadrants based on the exteremas of the points collection
def plot_quadrants(point_collection) :

    # giving a padding to the boxes
    max_x = max( [point.x for point in point_collection] ) + 1
    max_y = max( [point.y for point in point_collection] ) + 1

    min_x = min( [point.x for point in point_collection] )-1
    min_y = min( [point.y for point in point_collection] )-1


    print('MAXES:{}, {}'.format(max_x, max_y))
    print('MINS:{}, {}'.format(min_x, min_y))

    centre_x = min_x + (max_x-min_x)/2
    centre_y = min_y + (max_y-min_y)/2

    print('CENTERS:{}, {}'.format(centre_x, centre_y))

    #defining the shape based on vertices
    q1 = make_rectangle(Point(min_x, min_y), (max_x-min_x)/2, (max_y-min_y)/2  )
    q2 = make_rectangle(Point(centre_x, min_y), (max_x-min_x)/2, (max_y-min_y)/2  )
    q3 = make_rectangle(Point(min_x, centre_y), (max_x-min_x)/2, (max_y-min_y)/2  )
    q4 = make_rectangle(Point(centre_x, centre_y), (max_x-min_x)/2, (max_y-min_y)/2  )

    global shapes
    shapes= [ {'q1' : q1}, {'q2': q2}, {'q3': q3}, {'q4':q4}]


    #x-y values that can be plotted
    (x1, y1) = q1.exterior.xy
    (x2,y2) = q2.exterior.xy 
    (x3,y3) = q3.exterior.xy
    (x4,y4) = q4.exterior.xy


    #plotting them on the graph
    plt.figure()
    plt.plot(x1,y1, label='q1')
    plt.plot(x2,y2, label='q2')
    plt.plot(x3,y3, label = 'q3')
    plt.plot(x4,y4, label='q4')

    plt.legend()

    return shapes




#returns a rectangle object based on shapely polygons, provided the parameters
def make_rectangle(origin, width, length) :
    ox = origin.x
    oy = origin.y

    rect = Polygon( [(ox,oy), (ox+width, oy), (ox+width, oy+length), (ox, oy+length ) ])

    return rect

#plots the rectangle using the function above
def plot_rectangle():
    rect = make_rectangle(Point(0,10), 50, 100)
    (x,y) = rect.exterior.xy
    plt.plot(x,y)

        
