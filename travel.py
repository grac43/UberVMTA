import googlemaps
import geocoder 
from datetime import datetime
from datetime import timedelta
import citibike
from geopy.geocoders import Nominatim




#from pytimeparse.timeparse import timeparse - I don't think I need this. Will delete. 

#import all of our own functions from another file
from travel_functions import get_travel_time, find_transit_mode, are_you_late, print_time, send_excuse
#ADD THE IMPORTS FOR THE CITIBIKE FUNCTIONS FROM THEIR FILES

now = datetime.now() #gets current time

current = str(input("Where are you now?\nFormat Example: 293 central park west, ny, ny, 100024\n")) + ''
destination = str(input("Where do you want to go?\nFormat Example: 293 central park west, ny, ny, 100024\n")) + ''
geolocator = Nominatim(user_agent="find me")
geocode_current = geolocator.geocode(current)
geocode_destination = geolocator.geocode(destination)


current_lat = geocode_current.latitude
current_lng = geocode_current.longitude
dest_lat = geocode_destination.latitude
dest_lng = geocode_destination.longitude


print("Ok, I will find out how long it will take you to get there!\n")

travel_times = get_travel_time(now, current, destination) #run this function to get the users travel times

for i in travel_times:
    arrival_time = now + timedelta(seconds = travel_times[i])
    print(f"{i} you will arrive at {arrival_time.strftime('%H:%M')}")

min = min(travel_times.items(),key=lambda x: x[1]) 
print(f"\n{min[0]} is fastest.\n")

# dan's code current latlng
closest_origin = citibike.get_closest_station((current_lat, current_lng))
closest = closest_origin
print (f"\nThe nearest CitiBike Station based on your current location is on {closest['stAddress1']} \nTotal Open Docks(s):{closest['availableDocks']} \nTotal Available Bike(s): {closest['availableBikes']}\n")

# dan's code destination latlng
closest_dest   = citibike.get_closest_station((dest_lat, dest_lng))
closest = closest_dest
print (f"\nThe nearest CitiBike Station based on your destination is on {closest['stAddress1']} \nTotal Open Docks(s):{closest['availableDocks']} \nTotal Available Bike(s): {closest['availableBikes']}")

user_mode = find_transit_mode() #run function to find out what travel method user is using
arrival_time = now + timedelta(seconds = travel_times[user_mode])


# print(f"({current_lat}, {current_lng}), ({dest_lat}, {dest_lng})")

correct_arrival_time = datetime.strptime(input("\nWhen were you supposed to arrive? Enter the military time, with no spaces: "), '%H:%M')
correct_arrival_time = correct_arrival_time.replace(year=now.year, month = now.month, day = now.day)

late_time = are_you_late(arrival_time, correct_arrival_time) #run function to determine whether user is late

if arrival_time > correct_arrival_time: 
#if clause to determine what to do if the user is late

    if input("Do you want to send an excuse text? (input: yes/no):").lower() =="yes":
            
        #if user is late, ask if they want you to text their friend, run another function to do so
      
            phone_number = input("What is your friend' phone number? ").lower() 
            if (user_mode == 'bike'): 
#A citibike specific excuse
                excuse = "I'm so sorry I could not get a Citibike, I will be " + print_time(late_time)
        
            else:
                excuse = "I'm so sorry, I will be "

excuse = excuse + print_time(late_time)
send_excuse(phone_number, excuse)
#     else:
# print("Being timely is a virtue, good job!")
