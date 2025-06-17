import os
from twilio.rest import Client
from flight_data import FlightData
from datetime import datetime

class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    @staticmethod
    def send_flight_info(flight: FlightData):
        message_body = f"We found a cheap flight from {flight.origin_city} to {flight.destination_city} for {flight.price} on {flight.departure_date}"

        client = Client(os.getenv("TWILIO_ACCOUNT_SID", os.getenv("TWILIO_AUTH_TOKEN")))
        message = client.messages.create(
            body= message_body,
            from_="whatsapp:+14155238886",
            to="whatsapp:+19545795515"
        )
        print(f"Sent message for flight {flight.departure_date} at {datetime.now().strftime('%H:%M:%S')}")
