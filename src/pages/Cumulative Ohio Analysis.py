import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
import seaborn as sns
import matplotlib.pyplot as plt




st.title('Cumulative Ohio Weather Forecast Analysis')
st.write('Please review the Analysis below:')

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
    
    
    # Create a layout with two columns for charts
    col1, col2 = st.columns(2)

    

    with col1:
        st.subheader('O-H-I-O')
        fig = px.scatter(data, x='longitude', y='latitude', title='Geospatial Distribution', color='city')

        # Add neon green border to the chart
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
    
        st.plotly_chart(fig)

        st.subheader('Weather Conditions Over Time:')
        fig = px.line(data, y='current_status', x='date', title='Temperature Over Time', color='date')

        # Add neon green border to the chart
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
        
        st.plotly_chart(fig)

        st.subheader('Air Pressure Scatter Plot:')
        fig = px.scatter(data, x='date', y='air_pressure', title='Air Pressure Over Time', color='speed_of_wind_feet_per_sec')

        # Add neon green border to the chart
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
        
        st.plotly_chart(fig)

        st.subheader('Wind (feet per second):')
        fig = px.line(data, x='date', y='speed_of_wind_feet_per_sec', title='Wind Speed Over Time', color='city')

        # Add neon green border to the chart
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
        
        st.plotly_chart(fig)

        with col1:
            st.subheader('Percipitation by Date')
            fig = px.bar(data, x='date', y='pop', title='Percipitation')

            fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
            fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')

            st.plotly_chart(fig)
            

        

    with col2:
        

        st.subheader('Weather Histogram')
        hist_data = data['day_category'].value_counts(normalize=True).reset_index()
        hist_data.columns = ['day_category', 'percentage']
        fig = px.bar(hist_data, x='day_category', y='percentage', title='Upcoming Weather!', color='day_category')

        # Add neon green border to the chart
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
        
        st.plotly_chart(fig)

        st.subheader('Scatter Plot')
        fig = px.scatter(data, x='temperature', y='air_pressure', title='Temp vs. Air Pressure', color='city')

        # Add neon green border to the chart
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
        
        st.plotly_chart(fig)

        st.subheader('Box Plot of Temperature')
        fig = px.box(data, x='city', y='temperature', title='Temp by City')

        # Add neon green border to the chart
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
        
        st.plotly_chart(fig)

        st.subheader('Bar Chart of Temperature by City')
        fig = px.bar(data, x='city', y='temperature', title='Temperature by City', color='city')

        # Add neon green border to the chart
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
        
        st.plotly_chart(fig)

        st.subheader('Line Chart of Temperature Over Time')
        fig = px.line(data, x='date', y='temperature', title='Temperature Over Time (Multiple Cities)', color='city')

        # Add neon green border to the chart
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
        
        st.plotly_chart(fig)

    st.title('Aggregation Data:')

    st.subheader('Avg Weather by Date (numeric columns are averaged)')

    # Group the data by 'date' and 'day_category' and calculate the mean for columns
    columns_to_mean = ['temperature', 'air_pressure', 'speed_of_wind_feet_per_sec','pop']
    avg_weather_data = data.groupby(['date', 'day_category'])[columns_to_mean].mean().reset_index()

    # Display the resulting DataFrame
    st.write(avg_weather_data)

    st.subheader('Average Temperature Over Time by Day')
    fig = px.line(avg_weather_data, x='date', y='temperature', color='day_category', title='Average Temperature Over Time by Day Category')
    
    # Add neon green border to the chart
    fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
    
    st.plotly_chart(fig)

    st.subheader('Average Air Pressure by Day')
    fig = px.bar(avg_weather_data, x='day_category', y='air_pressure', color='temperature', title='Average Air Pressure by Day Category')
    
    # Add neon green border to the chart
    fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
    
    st.plotly_chart(fig)

    st.subheader('Scatter Plot: Wind Speed vs. Temperature by Day')
    fig = px.scatter(avg_weather_data, x='temperature', y='speed_of_wind_feet_per_sec', color='day_category', title='Wind Speed vs. Temperature by Day Category')
    
    # Add neon green border to the chart
    fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')
    
    st.plotly_chart(fig)

    st.subheader('Percipitation Pie Chart: ')

    # Group the data by 'day_category' and calculate the sum of 'pop' for each category
    pop_data = data.groupby('day_category')['pop'].sum().reset_index()

    # Create a pie chart
    fig = px.pie(pop_data, values='pop', names='day_category', title='Percent of Percipitation by Day Category')

    # Add neon green border to the chart
    fig.update_traces(marker=dict(line=dict(color='#39FF14', width=2)))

     # Add neon green border to the chart
    fig.update_xaxes(showline=True, linewidth=2, linecolor='#39FF14')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='#39FF14')

    # Display the pie chart
    st.plotly_chart(fig)



else:
    st.error('Sorry, I fell asleep. Thank you for waking me up. Please try again.')
