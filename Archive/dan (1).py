mport json
import urllib.request
import requests


url = "https://feeds.citibikenyc.com/stations/stations.json"

r = requests.get(url)

r.json()

type(info)

citibike_data = r.json()

type(citibike_data)

info = []

for station in citibike_data['stationBeanList']:
  
  info.append({
      "communication_time": station["lastCommunicationTime"],
      "station_name" : station["stationName"],
      "available_bikes": station["availableBikes"],
      "available_docks" : station["availableDocks"],
            "latitude": station["latitude"],
      "longitude": station["longitude"]

  })

info[0]

