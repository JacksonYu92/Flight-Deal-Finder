import os
import requests
from pprint import pprint

token = os.environ["SHEETY_TOKEN"]
endpoint = os.environ["SHEETY_ENDPOINTS"]

headers = {
    "Authorization": token,
}

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheet_data = {}

    def get_data(self):
        response = requests.get(url=endpoint, headers=headers)
        data = response.json()
        self.sheet_data = data["prices"]
        return self.sheet_data

    def update_data(self):
        for city in self.sheet_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"],
                }
            }
            response = requests.put(url=f"{endpoint}/{city['id']}", json=new_data, headers=headers)
            print(response.text)


