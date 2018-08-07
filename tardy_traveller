import googlemaps
import geocoder 
from datetime import datetime
from datetime import timedelta

#from pytimeparse.timeparse import timeparse - I don't think I need this. Will delete. 

#import all of our own functions from another file
from get_travel_times import get_travel_time, find_transit_mode, are_you_late, print_time, send_excuse, get_coord_dist, find_closest_station, check_if_bad_weather

gmaps = googlemaps.Client(key='AIzaSyD1zTwme37sTYJy2y5gBzOg9TluuK2xgcc')
now = datetime.now() #gets current time

current = str(input("Where are you now? ")) + ', NY'
destination = str(input("Where do you want to go? ")) + ', NY'

travel_times = get_travel_time(now, current, destination) #run this function to get the users travel times

user_mode = find_transit_mode().lower #run function to find out what travel method user is using
arrival_time = now + timedelta(seconds = travel_times[user_mode])

if (user_mode == 'bicycling'):
    #Block that checks if there are citibikes for you
    current = geocoder.google(current)
    current_lat = current.lat
    current_lng = current.lng
    try:
        citibike_station = find_closest_station(current_lat, current_lng)
    except TypeError:
        print("Sorry, I cannot find you a Citibike station")
        exit()
    else:
        print("Sorry, I cannot find you a Citibike station")
        exit()
    print(f"The {citibike_station['stationName']} Citibike station has {citibike_station['availableBikes']} bikes")

    if citibike_station['availableBikes'] > 0:
        destination = geocoder.google(destination)
        dest_lat = destination.lat
        dest_lng = destination.lng
        try: 
            citibike_station = find_closest_station(dest_lat, dest_lng)
        except TypeError:
            print("Sorry, I cannot find you a Citibike station")
            exit()  
        else:
            print("Sorry, I cannot find you a Citibike station")
            exit()
        print(f"The {citibike_station['stationName']} Citibike station has {citibike_station['availableDocks']} docks")


correct_arrival_time = datetime.strptime(input("When were you supposed to arrive? Enter hh:mm am/pm "), '%I:%M%p')
correct_arrival_time = correct_arrival_time.replace(year=now.year, month = now.month, day = now.day)

late_time = are_you_late(arrival_time, correct_arrival_time) #run function to determine whether user is late

if arrival_time > correct_arrival_time: 
#if clause to determine what to do if the user is late

    if input("Do you want to send an excuse text? ").lower == "yes":
    #if user is late, ask if they want you to text their friend, run another function to do so

        phone_number = input("What is your friend' phone number? ")
        if (user_mode == 'bicycling'): #A citibike specific excuse
            excuse = "I'm so sorry I could not get a Citibike, I will be " + print_time(late_time)
        
        else:
            excuse = "I'm so sorry, I will be "

        excuse = excuse + print_time(late_time)
        send_excuse(phone_number, excuse)
else:
    print("Being timely is a virtue, good job!")
    exit()   
    #end function if user is on-time
