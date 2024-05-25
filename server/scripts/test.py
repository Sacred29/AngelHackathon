import json
import requests

# Your existing code
url = "https://data.busrouter.sg/v1/stops.min.json"
response = requests.get(url)
data = response.json()
formattedData = json.loads(json.dumps(data))
print(formattedData)

def get_bus_stop_number(latitude, longitude):
    for stop_number, details in formattedData.items():
        if details[1] == latitude and details[0] == longitude:
            return stop_number
    return None

# latitude = 1.28706
# longitude = 103.83963

# bus_stop_number = get_bus_stop_number(latitude, longitude)
# if bus_stop_number:
#     print(f"Bus Stop Number: {bus_stop_number}")
# else:
#     print("Bus stop not found.")


# url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
# params = {
#     "location": "1.3703045,103.7519296",
#     "radius": 1500,
#     "types": "bus_station",
#     "sensor": "true",
#     "key": ""
# }

# response = requests.get(url, params=params)
# data = response.json()
# print(json.dumps(data, indent=4))