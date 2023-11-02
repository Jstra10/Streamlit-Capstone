import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



st.title('💑')
st.write('Please review the Relationships below:')

# Load data from SQL database
load_dotenv()
sql_url = os.getenv('SQL_URL')
sql_query = 'SELECT * FROM weather_data'
data = pd.read_sql_query(sql_query, sql_url)
data['temperature'] = (data['temperature'] - 273.15) * 9/5 + 32
data['speed_of_wind_feet_per_sec'] = data['speed_of_wind'] * 3.28084
data.drop('speed_of_wind', axis=1, inplace=True)
data['air_pressure'] = data['air_pressure'] * 0.02953



# Define the columns to exclude
exclude_columns = ['temp_min', 'temp_max', 'speed_of_wind', 'visibility_in_meters']

# Check if data is Not empty
if not data.empty:
    st.subheader('Pairplot of Numeric Values')

    # Filter numeric columns excluding the specified columns
    numeric_columns = data.select_dtypes(include=[np.number, np.bool_]).drop(columns=exclude_columns, errors='ignore')

    # Create a pairplot
    pairplot = sns.pairplot(data=numeric_columns, diag_kind='kde', markers='o')

    # Customize the plot
    st.pyplot(pairplot.fig)

    

    # Define variable explanations
variable_explanations = {
    'pop': 'Percent of Percipitation',
    'temperature': 'Temperature in Fahrenheit',
    'humidity': 'Humidity',
    'air_pressure': 'Air Pressure inHg (inches of mercury) Avg air pressure for Ohio is 30.34',
    'speed_of_wind_feet_per_sec': 'Wind Speed (feet/s)'
}

# Display variable explanations
for variable, explanation in variable_explanations.items():
    st.write(f"{variable}: {explanation}")

    st.subheader('Correlation Matrix')

    # Calculate the correlation matrix
    correlation_matrix = numeric_columns.corr()

    # Display the heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmax=1, vmin=-1, ax=ax)

    
    plt.title('Correlation Heatmap')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)

    
    st.pyplot(fig)

