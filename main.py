import requests
from datetime import datetime
import smtplib
import os



def get_weather_data(mtn_name:str):
  weather_api_key = os.environ.get('WEATHER_API')
  resorts_name = {'sugar mtn':['36.13022197817641', '-81.85925287689757']}
  sugar_lat, sugar_lon = resorts_name['sugar mtn']
  exclude = 'alerts,current,minutely,hourly'
  req = f'https://api.openweathermap.org/data/3.0/onecall?lat={sugar_lat}&lon={sugar_lon}&&units=imperial&exclude={exclude}&appid={weather_api_key}'
  response = requests.get(req)
  data = response.json()
  return mtn_name, data


def get_text_data (data):
  data_dict = {}
  for i in range(len(data['daily'])):
    date = datetime.utcfromtimestamp(data['daily'][i]['dt'])
    formatted_date = date.strftime('%m-%d-%Y')
    if ('snow' in data['daily'][i]['summary']):
      data_dict[formatted_date] = (data['daily'][i]['summary'])
  return data_dict

def send_text_message(data_dict, mtn_name:str):
  recipient_phone = '3364787808'
  carrier_gateway = 'vtext.com'

  sender_email = 'boardingboys9@gmail.com'
  sender_password = 'cbce ccek appt rrip'

  # Compose the email
  message = f'{", ".join(data_dict.keys())}'
  email_body = f'To: {recipient_phone}@{carrier_gateway}\nsnow this week in {mtn_name}!!\n{message}'


  # Connect to the SMTP server
  with smtplib.SMTP('smtp.gmail.com', 587) as server:
      server.starttls()
      server.login(sender_email, sender_password)

      # Send the email
      server.sendmail(sender_email, f'{recipient_phone}@{carrier_gateway}', email_body)

mtn_name, data = get_weather_data('sugar mtn')
data_dict = get_text_data(data)
send_text_message(data_dict, mtn_name)
