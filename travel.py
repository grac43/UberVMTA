import googlemaps
import geocoder 
from datetime import datetime
from datetime import timedelta
import citibike

#from pytimeparse.timeparse import timeparse - I don't think I need this. Will delete. 

#import all of our own functions from another file
from travel_functions import get_travel_time, find_transit_mode, are_you_late, print_time, send_excuse
#ADD THE IMPORTS FOR THE CITIBIKE FUNCTIONS FROM THEIR FILES

now = datetime.now() #gets current time

current = str(input("Where are you now? ")) + ', NY'
destination = str(input("Where do you want to go? ")) + ', NY'

current_lat = geocoder.google(current).lat
current_lng = geocoder.google(current).lng
dest_lat = geocoder.google(destination).lat
dest_lng = geocoder.google(destination).lng

print("Ok, I will find out how long it will take you to get there!")

travel_times = get_travel_time(now, current, destination) #run this function to get the users travel times

for i in travel_times:
    arrival_time = now + timedelta(seconds = travel_times[i])
    print(f"{i} you will arrive at {arrival_time.strftime('%H:%M')}")

min = min(travel_times.items(),key=lambda x: x[1]) 
print(f"{min[0]} is fastest.")

user_mode = find_transit_mode() #run function to find out what travel method user is using
arrival_time = now + timedelta(seconds = travel_times[user_mode])

####ADD SOME CITIBIKE CODE HERE TO SHOW THE CITBIKE INFO AT YOUR CURRENT & DESTINATION####


# dan's code current latlng
closest_origin = citibike.get_closest_station((current_lat, current_lng))
# dan's code destination latlng
closest_dest   = citibike.get_closest_station((dest_lat, dest_lng))

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
