
import googlemaps
import geocoder 
from datetime import datetime
from datetime import timedelta
from pytimeparse.timeparse import timeparse
from urllib.request import urlopen
import json
import time
import requests
from operator import itemgetter, attrgetter


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
    user_input_mode = input("\nHow are you getting there? Options: subway, car, walking, or bike\n")

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

#FUNCTION 3:
def print_time(time): 
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
#WARNING: This texting function uses Parijat's Twilio information.
#To test, please update the from number in the function and use the to number associated with your Twilio account
def send_excuse(phone_number, excuse): #function that uses Twilio to send a text if you're running late
    from twilio.rest import Client

    account = "ACce880bdf137e2d193b3deaeadc5ef68f"
    token = "f2adc22dae86e6b8a173f2e63c7289ef"
    client = Client(account, token)
   #WARNING: CHANGE THIS FROM NUMBER TO WHATEVER IS ASSOCIATED WITH YOUR TWILLIO ACCOUNT TO TEST
    message = client.messages.create(to=phone_number, from_="+12015145987",
                                     body=excuse) 

    print("Your excuse was sent! Now hurry!")

#FUNCTION 6
def get_closest_station(origin, destinations, bucket_sz = 100): #Function that finds the closest citibike to you
  """
  :param origin
  Origin is a single tuple (latitude, longitude)
  :param destinations
  Destinations is a list of (latitude, longitude)
  :param bucket_sz
  Bucket size when retreiving result. Max should be 100
  """
  results = []
  bucket_sz = 100
  # api
  gmaps = googlemaps.Client(key='AIzaSyD1zTwme37sTYJy2y5gBzOg9TluuK2xgcc') #our private key

  #for bucket of lat longs, the program will run an iteration to figure out the total walking time in seconds from current location to citibike terminal
  for idx in range(0, len(destinations), bucket_sz):
    latlng_bucket = destinations[idx: idx + bucket_sz];
    results_bucket = gmaps.distance_matrix(origins = origin, destinations = latlng_bucket, mode = "walking")
    results.extend(results_bucket['rows'][0]['elements'])


  length = len(results) #the total length of our citibike list
  durations = [] #empty list that will be appended as we run the code

  for index in range(length):
    # get result
    result =  results[index]

    # make a tuple with (value, station name, index)
    # save index to be used later for retrieving more info about station
    info = (result['duration']['value'], index)
    # append info to a list
    durations.append(info)

    sorted_durations = sorted(durations, key=itemgetter(0)) #sorts smallest to larget based on the "first collumn" which is the duration in seconds
  return sorted_durations[0][1] #pulls out the closest citbike station index
