#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import os
from dotenv import load_dotenv
from data_manager import DataManager
from flight_search import FlightSearch

#todo Get rows from sheet to determine if they have a city code.  if not update the code
load_dotenv()
current_pricing=[]

dm = DataManager()
dm.get_destinations()


fs = FlightSearch()
for dest in dm.destinations:
    if dest["iataCode"] == '':
        #get the code for that city
        city_code = fs.get_city_code(dest["city"])
        if len(city_code) > 0:
            #save the city code to the spreadsheet
            dm.save_city_code(dest_id = dest["id"], code = city_code)


#TODO search for cheap price for each city
for dest in dm.destinations:
    if dest["iataCode"] != "":
        cp_data = fs.get_cheap_flights(city_code= dest["iataCode"])
        print(cp_data)
        #loop through flights for the cheapest one
        # for flight in cp_data:

        # current_pricing.append(
        #     {
        #         "id": dest['id'],
        #
        #     }
        # )

#todo compare the flight price to the low price in the spreadsheet


#todo send text message for low fares