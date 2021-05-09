#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

CURRENT_CITY_CODE = "LON"

tomorrow = datetime.today() + timedelta(days=1)
# print(tomorrow.strftime("%d/%m/%Y"))
six_months = datetime.today() + timedelta(days=(6*30))
# print(six_months.strftime("%d/%m/%Y"))

data_manager = DataManager()
sheet_data = DataManager().get_data()
flight_search = FlightSearch()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.sheet_data = sheet_data
    # data_manager.update_data()
print(sheet_data)

for destination in sheet_data:
    flight = flight_search.search_flight(
        CURRENT_CITY_CODE,
        destination["iataCode"],
        tomorrow,
        six_months
    )

    if flight.price < destination['lowestPrice']:
        NotificationManager(text=f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}.")
