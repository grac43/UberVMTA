# #Travel Times Function using Google API
# import googlemaps
# import geocoder 
# from datetime import datetime
# from datetime import timedelta
# from pytimeparse.timeparse import timeparse

# gmaps = googlemaps.Client(key='AIzaSyD1zTwme37sTYJy2y5gBzOg9TluuK2xgcc')


def get_travel_time():
    now = datetime.now() #gets current time
    current = str(input("Where are you now? ")) + ', NY'
    destination = str(input("Where do you want to go? ")) + ', NY'

    #create a dictionary to store values of different travel tmies
    travel_times_int = {'driving' : 0,
                    'transit' : 0,
                    'bicycling' : 0,
                    'walking': 0,
                    }

    #Run for loop to cycle through google API to get travel time for different modes of transport
    for mode in ['transit', 'driving', 'walking', 'bicycling']:
        directions_result = gmaps.directions(current,
                                         destination,
                                         mode,
                                         departure_time=now)
        travel_times_int[mode] = directions_result[0]['legs'][0]['duration']['value']

    return travel_times_int




# ### DGraca coding for citi bike integration

# #import the citi bike api: http://appservices.citibikenyc.com/v1/station/list
# #use current address and find closest citi bike station with >1 citi bike available in the dock by using lat and long of both current and all citi bike stations
# use destination to find closest citi bike dock with greater than 1 dock


# first we need to pull the citi bike data from the internet. the file is a json file and a http link.

# import urllib.request
# import json
# req = urllib.Request("https://feeds.citibikenyc.com/stations/stations.json")
# opener = urllib2.build_opener()
# f = opener.open(req)
# json = json.loads(f.read())
# print (json)
    
# Array example

import json
import urllib.request
import requests
url = "https://feeds.citibikenyc.com/stations/stations.json"

r = requests.get(url)

info = r.json()

r.



# json_citibike = urllib.request.urlopen("https://feeds.citibikenyc.com/stations/stations.json").read()



# # print (json_citibike)

# loaded_json = json.loads(json_citibike)

# print(loaded_json)


# #do you want to take a citi bike?

# yes: the closest citi bike from you is on X and Y, there are x bikes available. Drop off your citi bike at x and y. there are x docks available





