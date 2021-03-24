"""
https://www.twilio.com/
This link is the basis for the text messaging, make sure to sign up!

After registering, press the home buton and click "Dashboard", both in the top left

You will see the following lines
"cellphone" -> Paste verified Twilio number as string
"ACCOUNT SID" -> Paste that number into account as string
"AUTH TOKEN" -> click show and paste that into token as string
"PHONE NUMBER" -> Paste that into token as string

Remember to verify your phone number
"""

from twilio.rest import Client

cellphone = "8608995785" #Input the phone number you want to send texts too (the phone number verified by twilio)

twilio_number = ""#Twilio provides a PHONE NUMBER, input it here
account = ""#Input ACCOUNT SID
token = ""#AUTH TOKEN, press show

def send_message(message):

    client = Client(account, token)
    client.messages.create(to=cellphone,
                          from_=twilio_number,
                          body=message)


#Test message if calling alerts. Run Alerts.py to test the system is working
if __name__  == "__main__":
    send_message("Test message. Did you receive it?")

