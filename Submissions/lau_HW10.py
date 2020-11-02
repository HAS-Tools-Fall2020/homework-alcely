# %%
# Import the modules we will use.
# Note: you may need to install some packages.

import numpy as np
import pandas as pd
import datetime


# %%
# Variables to modify:
# USGS URL for the flow data:
site = '09506000'
start = '1989-01-01'
end = '2020-10-31'

# Vairables for my brainmodel:
m = 10         # Insert month (m)
fd = 1         # Insert first day (fd) of the week / or 2 last weeks
ed = 31        # Insert end day (ed) of the week / or 2 last weeks

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
weeks2 = brainmodel(data, 1, 1, 2, factor)
print("My forecast entries for the week 1 & 2")
print(weeks2)
print()
weeks16 = brainmodel(data, 8, 22, 16, factor)
print("My forecast entries for the 16 weeks")
print(weeks16)

# %%
