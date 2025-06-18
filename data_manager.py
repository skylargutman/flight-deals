import os
import requests

class DataManager:
    def __init__(self):
        self.sheet = os.getenv("FLIGHT_DEALS_SHEET")
        self.auth_token = os.getenv("SHEETY_BEARER_TOKEN")
        self.destinations = []
        self.header = {
            "Authorization" : f"Bearer {self.auth_token}",
        }
        self.users = []

    def get_destinations(self):
        url = f"https://api.sheety.co/{self.sheet}/flightDeals/prices"
        response = requests.get(url=url, headers=self.header)
        response.raise_for_status()
        self.destinations = response.json()["prices"]
        print("Destinations received")
        return True

    def save_city_code(self, dest_id, code):
        url = f"https://api.sheety.co/{self.sheet}/flightDeals/prices/{dest_id}"
        data = {
            "price": {
                "iataCode": code,

            }
        }

        response = requests.put(url=url, headers=self.header, json=data)
        print(self.header, data, dest_id)
        print(response.text)

    def get_customer_emails(self):
        url = f"https://api.sheety.co/{self.sheet}/flightDeals/users"
        response = requests.get(url=url, headers=self.header)
        response.raise_for_status()
        self.users = response.json()["users"]
        print(f"{len(self.users)} users received")
        return True


# from dotenv import load_dotenv
# load_dotenv()
# dm = DataManager()
# dm.get_customer_emails()
# print(dm.users)