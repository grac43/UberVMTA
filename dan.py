import requests
import googlemaps
from operator import itemgetter, attrgetter


cur_latlng = (40.753460, -73.980737) #Parijat--need your help connecting this to your program
url = "https://feeds.citibikenyc.com/stations/stations.json"
r = requests.get(url)
info = r.json()

#pull from json file a list of all the lat and longs for each citibike station
stations = info['stationBeanList']
latlngs = []
for station in stations:
  latlngs.append(
      (station["latitude"] ,station["longitude"])
  )

gmaps = googlemaps.Client(key='AIzaSyD1zTwme37sTYJy2y5gBzOg9TluuK2xgcc') #Parijat this is your private key
results = [] #empty list that will be appended as we run the code

#for each dest in lat longs, the program will run an iteration to figure out the total walking time in seconds.
for dest in latlngs:
  result = gmaps.distance_matrix(origins = cur_latlng, destinations = dest, mode = "walking")
  results.append(result)

length = len(results) #the total length of our citibike list 

durations = [] #empty list that will be appended as we run the code

for index in range(length): 
  # get result
  result =  results[index] 
  # get station
  station = stations[index]
  # make a tuple with (value, station name, index)
  # save index to be used later for retrieving more info about station
  info = (result['rows'][0]['elements'][0]['duration']['value'],
          station['stationName'], index)
  # append info to a list
  durations.append(info)

sorted_durations = sorted(durations, key=itemgetter(0)) #sorts smallest to larget based on the "first collumn" which is the duration in seconds

closest = stations[sorted_durations[0][2]] #pulls out the closest citbike station.

print ('The nearest CitiBike Station is on', closest['stAddress1'], '\nTotal Available Bike(s):', closest['availableBikes'],)

