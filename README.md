# DNA Spaces Location Analytics
This sample code highlights the DNA Spaces REST API, and how to visualize and derive insights from it such as clustering user movements and calculating dwell time statistics.

client_info_REST.py: Generates the report from the rest api, default is over a 24 hours period  
client_info.py: Sample code to try out Firehose if applicable.  
polygon_def.py: Allows you to create polygon shapes to represent spaces in your floor, and visualize co-ordinates over your report time period.  
dwell_time_calculator.py: Calculates an average dwell_time for each region (per visit) from the report.  
main.py: Main file. 

## Contacts
* Ozair Saiyad (osaiyad@cisco.com)


## Solution Components
* DNA Spaces Location REST API
* Shapely library: For shape definitions in vector space
* Scikit: For Kmeans and methods to optimize the guess for K
  

#### Set up a Python venv
First make sure that you have Python 3 installed on your machine. We will then be using venv to create
an isolated environment with only the necessary packages.

##### Install virtualenv via pip
```
$ pip install virtualenv
```
##### Create a new venv
```
Change to your project folder
$ cd DNASpaces_Template
Create the venv
$ python3 -m venv venv
Activate your venv
$ source venv/bin/activate
```
#### Install dependencies
In the target folder: 
```
$ pip install -r requirements.txt
```

#### API Secrets
Create a [env_vars.py](code/env_vars.py) file where you will fill in your API Keys/Secrets and other sensitive variables

## Setup:

Import the env_vars file in client_info_REST.py, put it in the authorization section. Edit the name of the output file, which will be the report, to your liking.

Please read the shapely polygon documentation before defining shapes as there are rules about shape interactions (valid vs invalid) : https://shapely.readthedocs.io/en/stable/manual.html 

For K-Means, refer to scikit: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html 

polygon_def.py contains code related to shape definition and plotting, also for visualizing the X-Y coordinates and running the K-means clustering.


## Running:

Enter the following command to run the script:

```
$ cd code

$ python3 client_info_REST.py

$ python3 main.py
```


The first command generates the report summarizing the data over 24 hrs by default, the second command runs the main script to orchestrats the various function to produce clustering and dwell time statistics

## Output :

The K means handler will produce the output related to clustering and visualizing the X-Y coordinates with the floor plan as set. (By default, floor plan is just 4 quadrants)

The dwell time statistics will be displayed once the pyplot is closed on the terminal (stdout). The dwell time statistics assume the following:
*  For a sampling duration t, if theres a change in location during 2 samples, time t will be attributed to the new location ie location at the new sample location
*  Different 'firstactiveat' values in the report indicate different visits
*  Epoch time used in the report is in miliseconds. (final shown result is in hours by converting)
*  The locations are defined properly in accordance with Shapely library rules, ie same point should not be in 2 shapes at the same time. This can lead to inconsistency
   if not followed correctly. 
   
## Screenshots:
   
### K-Means output (polygon_def.py): 
![K means clustering, X-Y visualization, quadrant representing floor](/IMAGES/KMeans_Output.png)

### Dwell-time statistics output (dwell_time_calculator.py) :
![Dwell time statistics](/IMAGES/DwellTime_Output.png)

## Additional info:

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](License.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](Code_of_Conduct.md)

### CONTRIBUTING

See our contributing guidelines [here](Contributing.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
