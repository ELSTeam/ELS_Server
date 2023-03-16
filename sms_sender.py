from twilio.rest import Client 
import os
 
class SMSSender:
    def __init__(self) -> None:
        self.account_sid = os.environ['account_sid']
        self.auto_token = os.environ['auth_token']
        self.twilio_phone = os.environ['twilio_phone']
        self.client = Client(self.account_sid,self.auto_token)
    
    def send_message(self,phone_number:str,message:str) -> None:
        message = self.client.messages.create(
         body=message,
         from_=self.twilio_phone,
         to=phone_number
     )
        print("Message sent")
        print(message.sid)