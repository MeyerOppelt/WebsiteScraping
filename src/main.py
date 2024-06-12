import requests
from bs4 import BeautifulSoup
import os
import pandas
from tabulate import tabulate

# move down
print("\n" * 10)

# grab the sioux falls nws weather webpage
url = 'https://forecast.weather.gov/MapClick.php?lat=43.57431&lon=-96.731297'
response_html = ''
if (not os.path.exists("src/nws.html")):
    print("Grabbing NWS Page\n")
    response = requests.get(url=url).text
    with open('src/nws.html', 'w') as f:
        f.write(response)
else:
    print("Using previously cached NWS Page\n")
    with open('src/nws.html', 'r') as f:
        response = f.read()

# replace line breaks with spaces
response = response.replace('<br>', ' ')

# get the current conditions summary
soup = BeautifulSoup(response, 'html.parser')
current_conditions = soup.find(id="current_conditions-summary")

current_forecast = current_conditions.find(class_='myforecast-current').text
temperature = current_conditions.find(class_='myforecast-current-lrg')\
    .text.replace('°F', ' °F')

long_forecast = soup.find(id="seven-day-forecast-list")
forecast_list = long_forecast.findAll(class_="tombstone-container")

# Get extended forecast

print("\nExtended Forecast")
forecast = []
for i in forecast_list:
    period_name = i.find(class_="period-name").text
    temp = i.find(class_="temp").text.replace('Low: ', 'Low:  ')
    description = i.find(class_="short-desc").text
    forecast.append({"period_name": period_name, "temp": temp, "description": description})
forecast.insert(0, {"period_name": "Current", "temp": f"Now:  {temperature}", "description": current_forecast})

df = pandas.DataFrame(forecast)
print(tabulate(df, showindex=False, headers=df.columns))
#print(f"Time: {period_name}; Temp: {temp}; Description: {description}")