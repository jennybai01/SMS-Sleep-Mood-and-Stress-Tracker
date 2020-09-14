from twilio.rest import Client
from creds import *


class TwilioClient(object):
    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_message(self, msg, to):
        txt = self.client.messages.create(
            body=msg
            , from_=PHONE_NUMBER
            , to=to
        )
        return txt
