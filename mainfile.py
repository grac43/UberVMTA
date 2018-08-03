Final project psedocode

-   Connect to Google Direction’s API
-   Connect to Uber’s API

-   current_location = Ask user for their current location

-   def get_travel_time(current_location, arguments) #Write function to take user’s location & whatever other information is needed and returns: 
o   subway_time = Subway travel time to destination
o   driving_time = Driving travel time to destination
 
-   def get_uber(current_location, arguments) #Writes function to request an uber
o   Returns a message that somehow confirms you got an uber
 
-   if subway_time > driving_time: #Compare subway travel time and driving travel time. 
o   If true:
   Ask the user: do you want an uber (y/n)?:
•   If y:
o   get_uber() #run the get uber function to call you an uber
•   If n: print(“You’re going to be late to school!”)
o   Else: print(f“Take the subway and save some money. Your expected arrival time at school is {arrival_time}”)
 
