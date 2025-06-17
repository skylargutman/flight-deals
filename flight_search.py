import os
import requests

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
            "subType" : "CITY",
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

    def get_cheap_flights(self, city_code):
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        query_string = {
            "originLocationCode" : "MIA",
            "destinationLocationCode" : city_code,
            "departureDate" : "2025-06-17",
            "adults" : 1,
            "max":1
        }
        response = requests.get(url=url, headers=self.header, params=query_string)
        print(response.json())




from dotenv import load_dotenv
load_dotenv()
fs = FlightSearch()
fs.get_cheap_flights("PAR")
