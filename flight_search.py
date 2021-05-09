import json

import requests
import os
import pprint
from flight_data import FlightData

kiwi_api_key = os.environ["KIWI_API_KEY"]
kiwi_endpoint = "https://tequila-api.kiwi.com"

headers = {
    "apikey": kiwi_api_key,
}

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city):
        quary = {
            "term": city,
        }
        response = requests.get(url=f"{kiwi_endpoint}/locations/query", params=quary, headers=headers)
        iata_code = response.json()["locations"][0]["code"]
        return iata_code

    def search_flight(self, current_city_code, destination_city_code, date_from, date_to, ):
        quary = {
            "fly_from": current_city_code,
            "fly_to": destination_city_code,
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(url=f"{kiwi_endpoint}/v2/search", params=quary, headers=headers)
        try:
            data = response.json()['data'][0]
            # formatted_data = json.dumps(response.json())
            # print(formatted_data)
            # print(f"{data['cityTo']}: £{data['price']}")
        except IndexError:
            print(f"No flights found for {destination_city_code}")
            return None

        flight_data = FlightData(
            price=data['price'],
            origin_city=data['cityFrom'],
            origin_airport=data['flyFrom'],
            destination_city=data['cityTo'],
            destination_airport=data['flyTo'],
            out_date=data['route'][0]['local_departure'].split('T')[0],
            return_date=data['route'][1]['local_departure'].split('T')[0]
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data
