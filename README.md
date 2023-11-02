# Streamlit Workshop

## Overview:
This application will utilize the Open weather Map API. located at https://openweathermap.org/.
Connection to the API allowed us to obtain 5 days of weather forecast data for the state of Ohio.




In order to run this application, you will need to run the following code:

```
python3.11 -m venv venv
```
On Mac:
```
source venv/bin/activate
```

On PC:
```
cd venv/Scripts
activate
```

To install the requirements in your environment, you will need to run the following code in the directory where the file is located:

```
pip install -r requirements.txt
```



### User Selected City Analysis
This page will query ElephantSQL returning data processed with Pandas. Plotly Express and Seaborn visualizations are used to 
display 5 day weather forecast variables for a location of choice.

### Cumulative Ohio Analysis
This page will query ElephantSQL returning data processed with Pandas. Plotly Express and Seaborn visualizations are used to 
display 5 day weather forecast variables for a the state of Ohio.

