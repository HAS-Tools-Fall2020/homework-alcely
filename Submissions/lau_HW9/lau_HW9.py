# %%
# Import the modules we will use.
# Note: you may need to install some packages.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
import json
import urllib.request as req
import urllib
import requests

# %%
# Variables to modify:
# USGS URL for the flow data:
site = '09506000'
start = '1989-01-01'
end = '2020-10-24'
# Maximun Value Flow (mvf), uses in AR model:
mvf = 98
# How many weeks you want to predict using AR?
number_weeks = 2
# Vairables for my brainmodel:
m = 10         # Insert month (m)
fd = 11         # Insert first day (fd) of the week / or 2 last weeks
ed = 24        # Insert end day (ed) of the week / or 2 last weeks

# %%
# Define a function to grab the data by years


def grab_by_year(dataframe, year_col, value_col, year_start=None,
                 year_end=None):
    """Grab one column a of dataframe for one year or more.

    Parameters
    ----------
    dataframe : dataframe
            Input dataframe with at least two columns.
            One column must represents years and another with
            the value to grab.
    year_col : str, int
            Year column name or year column index.
    value_col : str, int, list
            Value column name or value column index.
    year_start: int (optional)
            The year (inclusive) where start grabbing the data.
            If it is not defined the function will grab the years before
            and equal to year_end.
    year_end: int (optional)
            The year (inclusive) where stop grabbing the data.
            If it is not defined the function will grab the years from
            year_start until the last year in the dataframe.

    Returns
    ------
    grab_years : dataframe
            Output dataframe with the selected values.
    """

    if year_start is None and year_end is None:
        print("year_start and year_end are not defined. Insert a value \
                    for at least one year variable.")

    if year_end is None:
        grab_years = dataframe[(dataframe[year_col] >= year_start)
                               ][value_col]
    if year_start is None:
        grab_years = dataframe[(dataframe[year_col] <= year_end)
                               ][value_col]

    if year_start is not None and year_end is not None:
        grab_years = dataframe[(dataframe[year_col] >= year_start) &
                               (dataframe[year_col] <= year_end)
                               ][value_col]

    return grab_years

# Define a function for my own model


def brainmodel(data, fmonth, fday_week, weeks, factor):
    """Do a weekly flow forecast, using historical flows.
    Parameters
    ----------
    data: dataframe
        input data with year, month, day and flow columns.
    fmonth: int
        insert first month for the desired forecast.
    fday: int
        insert first day of the first week for the desired forecast.
    weeks: int
        insert the number of weeks to forecast.
    factor: float
        correction factor for the forecast.
    Return
    ----------
    forecast: list
        flow forecast output.
    """
    forecast = []
    i = 0
    while i < weeks:
        week_data = data[(data["year"] != 2020) & (data["month"] == fmonth) &
                         (data["day"] >= fday_week) &
                         (data["day"] <= (fday_week + 6))][["flow"]]
        fday_week = fday_week + 7

        if fday_week > 31:
            fday_week = (fday_week-31) + (7-(fday_week-31))
            fmonth += 1

        week_forecast = week_data.quantile(0.6)*factor
        forecast.append(round(week_forecast[0], 1))
        i += 1
    return forecast
# %%
# Downloading the data directly from the USGS website.


url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=" + \
      site + "&referred_module=sw&period=&begin_date=" + start + \
      "&end_date=" + end
data = pd.read_table(url, skiprows=30,
                     names=['agency_cd', 'site_no',
                            'datetime', 'flow', 'code'],
                     parse_dates=['datetime'])

# Expand the dates to year, month, day, and days of the week.
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Aggregate flow values to weekly: from sunday to saturday
flow_weekly = data.resample("W-SAT", on='datetime').mean()

# %% 
# Dowloading data directly from NOAA's API.
# https://towardsdatascience.com/getting-weather-data-in-3-easy-steps-8dc10cc5c859
# NOAA NCDC's Climate Data Online (CDO) has a size data limit.
# So, let do a loop to download the data by year.
# Store lists
dates_prcp = []
prcp = []
# Insert your token here
headers = {'token': 'VSkxlHQnVGEZkuZWzGwEOuVmOXnMWNug'}

# This is the base url that will be the start our final url
base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"

# Parameters:
datasetid = "GHCND"
stationid = "GHCND:USC00025635"
datatypeid = "PRCP"
startyear = 1989
endyear = 2020

for year in range(startyear, endyear + 1):
    year = str(year)

    # writing the complete URL
    url = base_url + '?' + 'datasetid=' + datasetid + '&stationid=' + \
        stationid + '&datatypeid=' + datatypeid + '&units=metric' + \
        '&startdate=' + year + '-01-01&enddate=' + year + '-12-31&limit=1000'
    print("dowloading", year)

    # make the api call
    apicall = requests.get(url, headers=headers)

    # load the api response
    response = apicall.json()

    for i in range(len(response['results'])):
        dates_prcp_get = response['results'][i]['date']
        prcp_get = response['results'][i]['value']
        dates_prcp.append(dates_prcp_get)
        prcp.append(prcp_get)
print("download completed")

# %%
# Now we can combine this into a pandas dataframe
data_NOAA = pd.DataFrame({'Precipitation': prcp, 'datetime': dates_prcp},
                         index=pd.to_datetime(dates_prcp))

# Expand the dates to year, month, day, and days of the week.
data_NOAA['year'] = pd.DatetimeIndex(data_NOAA['datetime']).year

# %%
# Aggregate prcp values to weekly: from sunday to saturday
rain_weekly = data_NOAA.resample("W-SAT").mean()

# %%
# Section 2: Building an regressive model (R model)
# More information: https://realpython.com/linear-regression-in-python/

# Step 2.2: Apply the grab_by_year function to select
# the trainning and testing period.
# Note: drop the first week since it won't has lagged data.

# MODIFY col_names:
# Names of the columns to grab from the flow_weekly dataframe.
# In this particular case, I used flow and flow_tm1.
col_names1 = ['year', 'flow', 'flow_tm1']

train_flow = grab_by_year(flow_weekly, col_names1[0], col_names1[1:3],
                          year_start=2017, year_end=2018)
test_flow = grab_by_year(flow_weekly, col_names1[0], col_names1[1:3],
                         year_start=2019)

col_names2 = ['year', 'Precipitation']

train_rain = grab_by_year(rain_weekly, col_names2[0], col_names2[0:2],
                          year_start=2017, year_end=2018)
test_rain = grab_by_year(rain_weekly, col_names2[0], col_names2[0:2],
                         year_start=2019)


# %%
# Step 2.3: Fit a linear regression model using sklearn
# problem the datasets don't have the same sizes,
# the NOAA data has missing values.
model = LinearRegression()
x = train_rain['Precipitation'].values.reshape(-1, 1)
y = train_flow[0:len(train_rain)]['flow'].values
model.fit(x, y)

# Look at the results
# r^2 values
r_sq = model.score(x, y)
print('coefficient of determination:', np.round(r_sq, 2))

# print the intercept and the slope
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))

# %%
# Step 2.5: calculate multiple weekly forecasts
# Alcely: I don't recommend use it.

# Set the initial flow as AR model input.
initial_rain = 0.5

armodel = []
i = 0
while i < number_weeks:
    AR_prediction = model.intercept_ + model.coef_ * initial_rain
    armodel.append(np.round(AR_prediction[0], 1))

    initial_rain = (initial_rain)*2
    i += 1
print("AR model for the week 1 & 2")
print(armodel)

# %% Section 3: My brain model: This section is neccesary
# for the brainmodel to work.
# Step 3.1: check the historical data.

hist_data = data[(data["year"] != 2020) & (data["month"] == m) &
                 (data["day"] >= fd) & (data["day"] <= ed)][["flow"]]
hist_value = hist_data.quantile(0.5)

# Step 3.2: check the data for the same days in this year.
data_2020 = data[(data["year"] == 2020) & (data["month"] == m) &
                 (data["day"] >= fd) & (data["day"] <= ed)][["flow"]]
value_2020 = data_2020.quantile(0.5)

# Step 3.3: difference between 2020 and historical data.
factor = value_2020 / hist_value
print("correction factor", round(factor[0], 2))

# %%
# Finally! Lets do our predictions using the function brainmodel.
weeks2 = brainmodel(data, 10, 18, 2, factor)
print("My forecast entries for the week 1 & 2")
print(weeks2)
print()
weeks16 = brainmodel(data, 8, 22, 16, factor)
print("My forecast entries for the 16 weeks")
print(weeks16)

# %%
# Section 4: Plots (optional).
# Just need to run or adjust some dates.
# Set the variables to plot:

flow_2020 = grab_by_year(flow_weekly, col_names1[0], col_names1[1:3],
                         year_start=2020)

plt.style.use('seaborn')

# 1. Time series of flow values with the x axis range limited
# Observations
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], color='gray', linewidth=1, label='flow')
ax.plot(flow_2020['flow'], color='darkmagenta', label='2020 flows')
ax.plot(rain_weekly['Precipitation'], color='blue', linewidth=1,
        label='rain (mm)')
ax.set(title="Observed Flow and Rain in the last 3 years", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]", yscale='log',
       xlim=[datetime.date(2018, 1, 1), datetime.date(2020, 10, 30)])
ax.legend()


plt.show()

# %%
