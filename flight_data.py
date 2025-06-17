

class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, flight_data):
        if flight_data == "":
            self.origin_city = ""
            self.destination_city = ""
            self.price = ""
            self.departure_date = ""
            self.flight_data = ""
        else:
            self.origin_city = flight_data["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            self.destination_city = flight_data["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
            self.price = float(flight_data["price"]["total"])
            self.departure_date = flight_data["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            self.flight_data = flight_data