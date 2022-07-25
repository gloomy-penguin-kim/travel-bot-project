import os
from pyairtable import Table
from flask import Flask
from twilio.twiml.messaging_response import MessagingResponse
import random
 
app = Flask(__name__)
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
 
@app.route('/send-travel-rec', methods=['POST', 'GET'])
def sms_reply():
  # Access and format Airtable base
  table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "Travel")
  destinations = table.all()
 
  # Randomly choose destination and obtain values
  destination_pick = random.choice(destinations)['fields']
  name = destination_pick['Name']
  location = destination_pick['Location']
  image = destination_pick['Image']
 
  # Initialize TwiML response
  resp = MessagingResponse()
 
  # Add a text message
  msg = resp.message('Looking for a place to travel? '\
    f'Consider going to {name} in {location}!')
 
  # Add a picture to the message
  msg.media(image)
 
  return str(resp)
 
 
if __name__ == "__main__":
    app.run(debug=True)
