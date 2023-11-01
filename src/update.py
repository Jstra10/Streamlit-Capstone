import streamlit as st
from dotenv import load_dotenv
import pandas as pd
from os import getenv
import psycopg2
import requests, json
from datetime import datetime
from psycopg2.extras import execute_values
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import os


def weather_data(lat, lon, key):
    """Obtains weather data from the OpenWeatherMap API for the next five days and stores it in a DataFrame."""


    key = '4f44009207da925ce842972729de1b50'
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={key}'
    response = requests.get(url)
    
    if response.ok:
        data = response.json()
        
        data_frame = []

        city_name = data['city']['name']

        # Iterate through the list of weather data
        for dct in data['list']:
            timestamp = dct['dt']  # dt = unix time
            hour = datetime.fromtimestamp(timestamp)
            temp_min = dct["main"]["temp_min"]
            temp_max = dct["main"]["temp_max"]
            temperature = dct["main"]["temp"]
            humidity = dct["main"]["humidity"]
            air_pressure = dct["main"]["pressure"]
            day_category = dct["weather"][0]["main"]
            current_status = dct["weather"][0]["description"]
            speed_of_wind = dct["wind"]["speed"]
            visibility = dct.get("visibility", "0")  # Visibility may not always be available
            pop = dct.get("pop", "0")  # Pop may not always be available
            sys_info = dct["sys"]["pod"]

            # Append the data for iteration to the list
            data_frame.append([city_name, timestamp, hour, temp_min, temp_max, temperature, humidity, air_pressure, day_category, current_status, speed_of_wind, visibility, pop, sys_info])

        return data_frame
    else:
        print("Failed to retrieve weather data.")
        return None
    

def retrieve_weather_data_for_counties(counties, key):
    counties = pd.read_csv(r'C:\Users\jjs61\OneDrive\Desktop\Streamlit\src\data\us-county-boundaries.csv')
    all_weather_data = []  # Initialize an empty list to store the weather data

    for _, row in counties.iterrows():
        lat, lon = row['latitude'], row['longitude']
        weather_data_result = weather_data(lat, lon, key)
        
        if weather_data_result is not None:
            for data in weather_data_result:
                data.extend([lat, lon])  # Append latitude and longitude
            all_weather_data.extend(weather_data_result)
    
    return all_weather_data


counties = pd.read_csv(r'C:\Users\jjs61\OneDrive\Desktop\Streamlit\src\data\us-county-boundaries.csv')
key = 'bf5bec80bffcd85b43121653e17a6c4a'
# Call function to retrieve weather data for locations in the counties DataFrame
all_weather_data = retrieve_weather_data_for_counties(counties, key)



# Create a DataFrame from the combined weather data
columns = ['city', 'timestamp', 'hour', 'temp_min', 'temp_max', 'temperature', 'humidity', 'air_pressure', 'day_category', 'current_status', 'speed_of_wind', 'visibility_in_meters', 'pop', 'sys', 'latitude', 'longitude']

df_weather = pd.DataFrame(all_weather_data, columns=columns)


# Send to elephant SQL
load_dotenv()
url=getenv('SQL_URL')
df_weather.to_sql('weather_data', con = url, if_exists='replace', index=False)

