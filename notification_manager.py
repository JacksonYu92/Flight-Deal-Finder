from twilio.rest import Client
import os

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self, text):
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body= text,
            from_=os.environ['TWILIO_PHONE_NUMBER'],
            to=os.environ['PHONE_NUMBER']
        )
        print(message.status)
