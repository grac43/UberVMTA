import geocoder 
from datetime import datetime
from datetime import timedelta
from geopy.geocoders import Nominatim

#import all of our own functions from  the file with functions
from t_func import get_travel_time, find_transit_mode, are_you_late, print_time, send_excuse, get_closest_station

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


print("Ok, I will find out how long it will take you to get there!")

travel_times = get_travel_time(now, current, destination) #run this function to get the users travel times

for i in travel_times:
    arrival_time = now + timedelta(seconds = travel_times[i])
    print(f"{i} you will arrive at {arrival_time.strftime('%H:%M')}")

min = min(travel_times.items(),key=lambda x: x[1]) 
print(f"\n{min[0]} is fastest.\n")

print("Let me check Citibikes, give a few seconds.")
try:
    closest_origin = get_closest_station((current_lat, current_lng))
    print (f"\nThe nearest CitiBike Station based on your current location is on {closest_origin['stAddress1']} \nTotal Available Bike(s): {closest_origin['availableBikes']}\n")
except:
    print("Sorry, I couldn't find a station near you now")
    pass

try:
    closest_dest   = get_closest_station((dest_lat, dest_lng))
    print (f"\nThe nearest CitiBike Station based on your destination is on {closest_dest['stAddress1']} \nTotal Open Docks(s):{closest_dest['availableDocks']}")
except:
    print("Sorry, I couldn't find a station near your destination")
    pass

user_mode = find_transit_mode() #run function to find out what travel method user is using
arrival_time = now + timedelta(seconds = travel_times[user_mode])

try:
    correct_arrival_time = datetime.strptime(input("When were you supposed to arrive? Example 1:30pm "), '%I:%M%p')
except:
    print("Incorrect format! Format should 10:15am")
    correct_arrival_time = datetime.strptime(input("When were you supposed to arrive? "), '%I:%M%p')

correct_arrival_time = correct_arrival_time.replace(year=now.year, month = now.month, day = now.day)

late_time = are_you_late(arrival_time, correct_arrival_time) #run function to determine whether user is late

if arrival_time > correct_arrival_time: 
#if clause to determine what to do if the user is late

    if input("Do you want to send an excuse text? yes / no").lower() =="yes":
            
        #if user is late, ask if they want you to text their friend, run another function to do so
      
        phone_number = input("What is your friend' phone number? \n Please enter as +12128675309").lower() 
            
        if (user_mode == 'bike'): 
            #A citibike specific excuse
            excuse = "I'm so sorry I could not get a Citibike, I will be " + print_time(late_time)
        
        else:
            excuse = "I'm so sorry, I will be "
        #WARNING: The texting function in the other file uses Parijat's Twilio information.
        #To test, please update the from number in the function and use the to number associated with your Twilio account
        try:
            excuse = excuse + print_time(late_time)
            send_excuse(phone_number, excuse)
        except: 
            print("I'm sorry, there was an error and I could not send your message. \n Hurry hurry!")
    else:
        print("Ok, well hurry up!")
else:
    print("Being timely is a virtue, good job!")