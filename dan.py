import googlemaps
import requests
from operator import itemgetter, attrgetter




def get_closest_station_idx(origin, destinations, bucket_sz = 100):
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

  #for buckket of lat longs, the program will run an iteration to figure out the total walking time in seconds from current location to citibike terminal
  for idx in range(0, len(destinations), bucket_sz):
    latlng_bucket = latlngs[idx: idx + bucket_sz];
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


if __name__ == "__main__":

  # set inputs
  cur_latlng = (40.753460, -73.980737) #Parijat--need your help connecting this to your program
  url = "https://feeds.citibikenyc.com/stations/stations.json"

  # api
  gmaps = googlemaps.Client(key='AIzaSyD1zTwme37sTYJy2y5gBzOg9TluuK2xgcc') #Parijat this is your private key

  # get info from URL
  r = requests.get(url)
  stations = r.json()['stationBeanList']
  latlngs = []
  #pull from json file a list of all the lat and longs for each citibike station
  for station in stations:
    latlngs.append(
        (station["latitude"] ,station["longitude"])
    )

  # get the closest station to origin

  closest_station_idx = get_closest_station_idx(cur_latlng, latlngs)
  closest = stations[closest_station_idx]
  print (f"The nearest CitiBike Station is on {closest['stAddress1']} \nTotal Open Docks(s):{closest['availableDocks']} \nTotal Available Bike(s): {closest['availableBikes']}")


  dest_latlng = (40.815041, -73.959868)
  dest_station_idx = get_closest_station_idx(dest_latlng, latlngs)
  closest_dest = stations[dest_station_idx]
  print (f"The nearest CitiBike Station to destination is on {closest_dest['stAddress1']} \nTotal Open Docks(s):{closest_dest['availableDocks']} \nTotal Available Bike(s): {closest_dest['availableBikes']}")
