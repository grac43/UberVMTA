#File containing all the functions our program uses
import googlemaps
import geocoder 
from datetime import datetime
from datetime import timedelta
from pytimeparse.timeparse import timeparse
from urllib.request import urlopen
import json
import time
from math import cos, asin, sqrt

gmaps = googlemaps.Client(key='AIzaSyD1zTwme37sTYJy2y5gBzOg9TluuK2xgcc')

#FUNCTION 1
def get_travel_time(now, current, destination): #function to get the travel time between destinations
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

    return travel_times_int #function's output is the dictionary with travel time's as datetime 

#FUNCTION 2
def find_transit_mode(): #function that asks user for their mode of transport
    user_input_mode = input("How are you getting there? subway, car, walking, or bike? ")

    if user_input_mode == "subway" or user_input_mode == 'train': 
        mode = "transit"
    elif user_input_mode == "bike" or user_input_mode == 'cycle' or user_input_mode == 'biking':
        mode = 'bicycling'
    elif user_input_mode == "car" or user_input_mode == 'uber' or user_input_mode == 'taxi':
        mode = 'driving'
    elif user_input_mode == "walking":
        mode = user_input_mode
    else:
        print("That is not an accepted transit type. Please re-run program")
        exit() #breaks if you type something other than what the program can accept
    return mode

#FUNCTION 3
def print_time(time): #function to show a time in a readable way 
    time = str(time) #converts datetime class to string
    time = time.split(':') #splits the string by colon character

    #if clauses for different formatting options:
    if time[0] == '0':
        time = time[1] + " minutes"
    
    elif time[0] == '1':
        time = time[0] + " hr and " + time[1]  + " minutes"

    else:
        time = time[0] + " hrs and " + time[1]  + " minutes"
    return time

#FUNCTION 4
def are_you_late(arrival_time, correct_arrival_time): #function to say whether you will be on-time
    if arrival_time <= correct_arrival_time: #output for if you're on-time
        print("You will be on-time!")
        print(f"You will arrive at: {arrival_time.time().replace(microsecond=0)}")
        late_time = 0

    else: #function for if you're late. Calls the print_time function
        late_time = arrival_time - correct_arrival_time
        print(f"You will be {print_time(late_time)} late!")
    return late_time

#FUNCTION 5
def send_excuse(phone_number, excuse): #function that uses Twilio to send a text if you're running late
    from twilio.rest import Client

    account = "ACce880bdf137e2d193b3deaeadc5ef68f"
    token = "f2adc22dae86e6b8a173f2e63c7289ef"
    client = Client(account, token)
    #from number hard coded to my Twilio
    message = client.messages.create(to=phone_number, from_="+12015145987",
                                     body=excuse) 

    print("Your excuse was sent! Now hurry!")

#FUNCTION 6
def get_coord_dist(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

#FUNCTION 7
def find_closest_station(current_lat,current_lng):
    citibikenycJson = json.loads(urlopen('http://www.citibikenyc.com/stations/json').read())
    stations_dict_list = citibikenycJson['stationBeanList']

    for station in stations_dict_list:
        lat = station['latitude']
        lng = station['longitude']
        dist_to_station = get_coord_dist(current_lat, current_lng, lat, lng)
        station.update({'dist_to_me' : dist_to_station})
        #print(dist_to_station)

    closest_station = min(stations_dict_list, key=lambda x:x['dist_to_me'])
    return closest_station
    print(closest_station)
