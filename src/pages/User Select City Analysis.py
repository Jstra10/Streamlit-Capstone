import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

st.title('Detailed Location Analysis')
st.write('Please review the Ohio Forecast Analysis:')

# Load data from SQL database
load_dotenv()
sql_url = os.getenv('SQL_URL')
sql_query = 'SELECT * FROM weather_data'
data = pd.read_sql_query(sql_query, sql_url)

data['speed_of_wind_feet_per_sec'] = data['speed_of_wind'] * 3.28084
data.drop('speed_of_wind', axis=1, inplace=True)

data['temp_min'] = (data['temp_min'] - 273.15) * 9/5 + 32
data['temp_max'] = (data['temp_max'] - 273.15) * 9/5 + 32
data['temperature'] = (data['temperature'] - 273.15) * 9/5 + 32

data['air_pressure'] = data['air_pressure'] * 0.02953


# Check if data is not empty
if not data.empty:
    st.subheader('Visualization Analysis:')
    
    city_filter = st.selectbox('Select a Location', data['city'].unique())

    # Create a layout with two columns for charts
    col1, col2 = st.columns(2)

    # Display various charts in the two columns
    with col1:
        st.subheader('Weather Conditions Over Time:')
        fig = px.line(data[data['city'] == city_filter], y='temperature', x='date', title='Temperature Over Time', color='day_category')
        
        # Add neon green border to the chart
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
        
        st.plotly_chart(fig)

        st.subheader('Air Pressure:')
        fig = px.scatter(data[data['city'] == city_filter], x='date', y='air_pressure', title='Air Pressure Over Time', color='city')
        
        # Add neon green border to the chart
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
        
        st.plotly_chart(fig)

    with col2:
        st.subheader('Wind (feet per second):')
        fig = px.line(data[data['city'] == city_filter], x='date', y='speed_of_wind_feet_per_sec', title='Wind Speed Over Time', color='city')
        
        # Add neon green border to the chart
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
        
        st.plotly_chart(fig)

        st.subheader('Histogram with Percentage Labels')
        hist_data = data[data['city'] == city_filter]['day_category'].value_counts(normalize=True).reset_index()
        hist_data.columns = ['day_category', 'percentage']
        fig = px.bar(hist_data, x='day_category', y='percentage', title='Upcoming Weather!', color='day_category')
        
        # Add neon green border to the chart
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
        
        st.plotly_chart(fig)

    st.subheader('Scatter Plot')
    fig = px.scatter(data[data['city'] == city_filter], x='temperature', y='air_pressure', title='Temperature vs. Air Pressure', color='city')
    
    # Add neon green border to the chart
    fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
    
    st.plotly_chart(fig)


