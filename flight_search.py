import os
from typing import Any

import requests
import datetime as dt
from flight_data import FlightData
from time import sleep

ORIGIN_CITY = "MIA"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        # load_dotenv()
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_token = os.getenv("AMADEUS_API_SECRET")
        # get the auth token
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type" : "client_credentials",
            "client_id" : self.api_key,
            "client_secret" :  self.api_token
        }
        response = requests.post(url=url, headers=header, data=data)
        response.raise_for_status()
        bearer = response.json()
        self.bearer_token = bearer["access_token"]
        self.header = {
            "Authorization": f"Bearer {self.bearer_token}"
        }

    def get_city_code(self, city_name: str):
        url= "https://test.api.amadeus.com/v1/reference-data/locations"

        query_string = {
            "subType" : ["CITY","AIRPORT"],
            "keyword" : city_name,
            "view" : "LIGHT"
        }
        response = requests.get(url=url, headers=self.header, params=query_string)
        # response.raise_for_status()
        print(query_string)
        city_list = response.json()
        print(city_list)
        if len(city_list["data"]) > 0 :
            return city_list["data"][0]["iataCode"]
        else:
            return ""

    def get_cheap_flight(self, city_code):
        flights: list[FlightData] = []
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        dates = self.get_dates_to_fly()
        for date in dates:
            query_string = {
                "originLocationCode" : ORIGIN_CITY,
                "destinationLocationCode" : city_code,
                "departureDate" : date,
                "adults" : 1,
                "max":1
            }
            response = requests.get(url=url, headers=self.header, params=query_string)
            response.raise_for_status()
            json_data = response.json()
            if "data" in json_data:
                if len(json_data["data"]) > 0:
                    flights.append(FlightData(flight_data = json_data["data"][0]))
                    print(f"Found flight for {query_string['destinationLocationCode']} on {query_string['departureDate']}")
            #don't go too fast, or they will stop you.
            sleep(2)
        cheap_flight = flights[0]
        for flight in flights:
            if float(cheap_flight.price) > flight.price:
                cheap_flight = flight

        return cheap_flight


    @staticmethod
    def get_dates_to_fly():
        #get a list of dates to check for flights 2 weeks, 1month, 2months, 3months, 4months, 5months
        dates = [(dt.datetime.now() + dt.timedelta(weeks = i * 4)).strftime("%Y-%m-%d") for i in range(1,7)]
        return [(dt.datetime.now() + dt.timedelta(weeks = 2)).strftime("%Y-%m-%d")] + dates

# from dotenv import load_dotenv
# load_dotenv()
# fs = FlightSearch()
# # print(fs.get_dates_to_fly())
#
# print(fs.get_cheap_flight("PAR").flight_data)
# # print(fs.get_city_code("lauderdale"))