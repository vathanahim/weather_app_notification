import requests
from datetime import datetime
import smtplib
import os



def get_weather_data(mtn_name:str):
  weather_api_key = 'fa801458f0caf0a1ce9e315adb94f07a'
  resorts_name = {'sugar mtn':['36.13022197817641', '-81.85925287689757'], 'snowshoe mtn':['38.414103', '-79.997095']}
  sugar_lat, sugar_lon = resorts_name[mtn_name]
  exclude = 'alerts,current,minutely,hourly'
  req = f'https://api.openweathermap.org/data/3.0/onecall?lat={sugar_lat}&lon={sugar_lon}&&units=imperial&exclude={exclude}&appid={weather_api_key}'
  response = requests.get(req)
  data = response.json()
  return mtn_name, data

def visualize_weather_data(weather_data):
    if not weather_data:
        return "No weather data available."
    #check api data and only input to text msg if there's snow
    visualization = []
    for date, data in weather_data.items():
        if (data[0] == 'Snow'):
            summary = data[0]
            precipitation_rate = data[2]

        # Construct the visualization string
        visualization.append(
            f"Date: {date}, Summary: {summary}, Precipitation Rate: {precipitation_rate}"
        )

    return visualization

def get_text_data (data):
  data_dict = {}
  for i in range(len(data['daily'])):
      date = datetime.utcfromtimestamp(data['daily'][i]['dt'])
      formatted_date = date.strftime('%m-%d-%Y')
      if ('snow' in str(data['daily'][i]['summary'])):
          data_dict[formatted_date] = [(data['daily'][i]['weather'][0]['main'])]
          data_dict[formatted_date].append(data['daily'][i]['feels_like'])
          if ('snow' in data['daily'][i].keys()):
            data_dict[formatted_date].append(str(round((int(data['daily'][i]['snow'])/25.4), 2))+' in/h')
  return data_dict


def send_text_message(data_msg, mtn_name:str, phone_numer:dict):

    if (data_msg == "No weather data available."):
      return print('no data')

    else:

      for i in phone_number.keys():
        recipient_phone = i
        carrier_gateway = phone_number[i]

        sender_email = 'boardingboys9@gmail.com'
        sender_password = 'cbce ccek appt rrip'

          # Split the long message into segments (assuming 160 characters per segment)
        
        for j in data_msg:
            # Connect to the SMTP server
          with smtplib.SMTP('smtp.gmail.com', 587) as server:
              server.starttls()
              server.login(sender_email, sender_password)
              email_body = f'To: {recipient_phone}@{carrier_gateway}\nsnow this week in {mtn_name}!!\n{j}'
              # Send the email
              server.sendmail(sender_email, f'{recipient_phone}@{carrier_gateway}', email_body)




phone_number = {'3364787808':'vtext.com'}
mountains = ['sugar mtn', 'snowshoe mtn']
for i in mountains: 
    mtn_name, data = get_weather_data(i)
    data_dict = get_text_data(data)
    data_msg = visualize_weather_data(data_dict)
    if (data_msg != "No weather data available."):
      send_text_message(data_msg, mtn_name, phone_number)
