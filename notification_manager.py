import os
import smtplib
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

    @staticmethod
    def send_email(to, subject, message):
        conn_email = os.getenv("GOOGLE_EMAIL_ACCOUNT")
        conn_password = os.getenv("GOOGLE_EMAIL_PASSWORD")
        conn_server = "smtp.gmail.com"
        with smtplib.SMTP(conn_server, 587) as conn:
            conn.starttls()
            conn.login(user=conn_email, password=conn_password)
            conn.sendmail(
                from_addr=conn_email,
                to_addrs=to,
                msg=f"Subject:{subject}\n\n{message}"
            )
            print(f"Sent email to {to}")

    def email_flight_info(self, customer, flight: FlightData):
        message = (f"Hello {customer['whatIsYourFirstName?']} {customer['whatIsYourLastName?']} "
                   f"We found a cheap {flight.stops} stop(s) flight from {flight.origin_city} to {flight.destination_city} for {flight.price} on {flight.departure_date}")
        self.send_email(customer["emailAddress"], f"Flight info found for {customer['whatIsYourFirstName?']}", message=message)
