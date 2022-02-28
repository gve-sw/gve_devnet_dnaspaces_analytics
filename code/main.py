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




from polygon_def import *
from dwell_time_calculator import *


FILE = 'User_Location_Data_SAPLE.csv'

if __name__ == '__main__' :


    #To do with X-Y data visualization from the report and clustering
    result = read_points(FILE)
    point_collection = result[1]
    report_dict_list = result[0]

    print([point.x for point in point_collection])

    shapes = plot_quadrants(point_collection)


    plt.scatter([point.x for point in point_collection], [point.y for point in point_collection])

    X = np.array([ [point.x, point.y] for point in point_collection])

    cluster_collection = k_means_handler(X)




    for cluster in cluster_collection :
        points_in_cluster = cluster_collection[cluster]
        for point in points_in_cluster:
            get_row_from_point(point_with_index= point, report_dict_list= report_dict_list) 


    #Outputs average dwell time per visit

    dwelltimes = dwell_time_calculator(shapes, report_dict_list)
  



