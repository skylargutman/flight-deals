#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import os
from time import sleep
from dotenv import load_dotenv
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

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
            print(f"Saving City Code: {city_code}")
    sleep(2)


#TODO search for cheap price for each city
alerts = []
for dest in dm.destinations:
    if dest["iataCode"] != "":
        flight = fs.get_cheap_flight(city_code= dest["iataCode"])
        if flight.price != "":
            if float(dest["lowestPrice"]) > float(flight.price):
                #save the new flight info to the alerts list to be sent
                alerts.append(flight)


#todo send text message for low fares
nm = NotificationManager()
for flight in alerts:
    nm.send_flight_info(flight)
    sleep(2)

