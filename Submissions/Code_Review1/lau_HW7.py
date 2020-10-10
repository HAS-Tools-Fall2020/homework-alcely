# Alcely's homework 7.

# %%
# Import the modules we will use.
# Note: you may need to install some packages.
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime

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

# %%
# Set the file name and path to where you have stored the dowload data.
# If your computer does not recognize the relative filepath,
# replace it with the complete filepath.


# MODIFY FILENAME
filename = 'streamflow_week7.txt'
filepath = os.path.join(r'..\..\data', filename)

print('You are working here:', os.getcwd())
print()
print('The dowload data is saved here:', filepath)

# %%
# Read the data into a pandas dataframe
data = pd.read_table(filepath, sep='\t', skiprows=30,
                     names=['agency_cd', 'site_no', 'datetime', 'flow',
                            'code'], parse_dates=['datetime'])

# Expand the dates to year, month, day, and days of the week.
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Aggregate flow values to weekly: from sunday to saturday
flow_weekly = data.resample("W-SAT", on='datetime').mean()

# %%
# Section 1: Evaluate my forecast from last week with the observed flow.
# Step 1.1: Check the data from the last 5 weeks.
last5week = flow_weekly[['flow']].tail()
print("Summary of the observed flow of the last 5 weeks")
last5week

# %%
# Step 1.2: Insert the last week forecast.
# MODIFY value
last_forecast = 58.8

# Step 1.3: Calculate the difference between observed and forecast flow.
diff_obs_fore = flow_weekly[['flow']].tail(1) - last_forecast

print("Difference between the real and forecast flow:")
diff_obs_fore

# %%
# Section 2: Building an autoregressive model (AR model)
# More information: https://realpython.com/linear-regression-in-python/

# Step 2.1: setup the arrays you will build your model on
# This is an autoregressive model so we will be building it based on the
# lagged timeseries. For this case, we will just use 1 shift.

flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)

# Step 2.2: Apply the grab_by_year function to select
# the trainning and testing period.
# Note: drop the first week since it won't has lagged data.

# MODIFY col_names:
# Names of the columns to grab from the flow_weekly dataframe.
# In this particular case, I used flow and flow_tm1.
col_names = ['year', 'flow', 'flow_tm1']

train = grab_by_year(flow_weekly, col_names[0], col_names[1:3],
                     year_start=2011, year_end=2018)
test = grab_by_year(flow_weekly, col_names[0], col_names[1:3], year_start=2019)

# Looking for a better adjusment of the AR model, lets set a
# Maximun Value Flow (mvf) to consider in the model
# MODIFY mvf:
mvf = 100

train = train[(train['flow'] <= mvf)][col_names[1:3]]
test = test[(test['flow'] <= mvf)][col_names[1:3]]

# Step 2.3: Fit a linear regression model using sklearn
model = LinearRegression()
x = train['flow_tm1'].values.reshape(-1, 1)
y = train['flow'].values
model.fit(x, y)

# Look at the results
# r^2 values
r_sq = model.score(x, y)
print('coefficient of determination:', np.round(r_sq, 2))

# print the intercept and the slope
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))

# %%
# Step 2.4: Make a prediction with your model.
# Predict the model response for a the trainning and testing data.
q_pred_train = model.predict(train['flow_tm1'].values.reshape(-1, 1))
q_pred_test = model.predict(test['flow_tm1'].values.reshape(-1, 1))

# Calculate the prediction bias with the testing data.
pred_bias = test['flow'] - q_pred_test
print("Prediction mean bias:", pred_bias.mean())

# %%
# Step 2.5: calculate multiple weekly forecasts
# Alcely: I don't recommend use it for more than 2-4 weeks.

# Set the initial flow as AR model input.
initial_flow = flow_weekly['flow'].tail(2).mean()

# How many weeks you want to predict?
number_weeks = 2

i = 1
while i < (number_weeks + 1):
    print("initial flow:", np.round(initial_flow, 1))
    AR_prediction = model.intercept_ + model.coef_ * initial_flow
    print("AR forecast week", i, ": ", np.round(AR_prediction, 1))

    initial_flow = (initial_flow + AR_prediction) / 2
    i += 1

# %% Section 3: My brain model.
# Step 3.1: check the historical data.

# MODIFY the following variables:
m = 10         # Insert month (m)
fd = 1         # Insert first day (fd) of the week / or 2 last weeks
ed = 10        # Insert end day (ed) of the week / or 2 last weeks

hist_data = data[(data["year"] != 2020) & (data["month"] == m) &
                 (data["day"] >= fd) & (data["day"] <= ed)][["flow"]]
hist_data_min = hist_data.min()

hist_data_stats = hist_data.describe(percentiles=[.33, .5, .66])
print("In the historical data for the month =", m,
      ", days between", fd, "and", ed, ", the statistic summary:")
hist_data_stats

# %%
# Step 3.2: check the data for the same days in this year.
data_2020 = data[(data["year"] == 2020) & (data["month"] == m) &
                 (data["day"] >= fd) & (data["day"] <= ed)][["flow"]]
data_2020_min = data_2020.min()

data_2020_stats = data_2020.describe(percentiles=[.33, .5, .66])
print("In the 2020 data for the month =", m,
      ", days between", fd, "and", ed, ", the statistic summary:")
data_2020_stats

# %%
# Step 3.3: difference between 2020 and historical data.
diff_2020_hist = data_2020_min - hist_data_min

print("Difference between minimun flow in 2020 and\
      minimun in the historical flow:")
diff_2020_hist

# %%
# Finally! Lets do our prediction.
# MODIFY: what is the first day of our week forecast?
m = 10          # Insert month (m)
fd_week1 = 11   # Insert first day (fd) of the week1

i = 1
while i < 3:
    week_data = data[(data["year"] != 2020) & (data["month"] == m) &
                     (data["day"] >= fd_week1) &
                     (data["day"] <= (fd_week1 + 6))][["flow"]]
    fd_week1 = fd_week1 + 7
    week_forecast = week_data.min() + diff_2020_hist

    print("My brain model week", i, ": ", np.round(week_forecast, 1))
    print()
    i += 1
print("I believe these values would be more accurate for my forecast entries.")

# %%
# Section 4: Plots (optional).
# Just need to run or adjust some dates.
# Set the variables to plot:

flow_2020 = grab_by_year(flow_weekly, col_names[0], col_names[1:3],
                         year_start=2020)

plt.style.use('seaborn')

# 0. Timeseries of observed flow values
# Observations
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], color='gray', linewidth=1, label='full')
ax.plot(flow_2020['flow'], color='darkmagenta', label='2020 flows')
ax.set(title="Observed Flow", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]",
       yscale='log')
ax.legend()

# 1. Time series of flow values with the x axis range limited
# Observations
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], color='gray', linewidth=1, label='full')
ax.plot(flow_2020['flow'], color='darkmagenta', label='2020 flows')
ax.set(title="Observed Flow in the last 3 years", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]", yscale='log',
       xlim=[datetime.date(2018, 1, 1), datetime.date(2020, 10, 10)])
ax.legend()

# 2. Time series of flow values with the x axis range limited
# AR model
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], color='gray', linewidth=1, label='full')
ax.plot(train['flow'], 'r', label='training')
ax.plot(test['flow'], 'b', label='testing')
ax.set(title="Observed Flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
       yscale='log',
       xlim=[datetime.date(2011, 1, 1), datetime.date(2020, 10, 10)])
ax.legend()


# 3. Line  plot comparison of predicted and observed flows
# using the training data.
fig, ax = plt.subplots()
ax.plot(train['flow'], color='grey', linewidth=2, label='observed')
ax.plot(train.index, q_pred_train, color='red', linestyle='--',
        label='simulated')
ax.set(title="Observed Flow & Simulated flow", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]")
ax.legend()


# 4. Line  plot comparison of predicted and observed flows
# using the testing data.
fig, ax = plt.subplots()
ax.plot(test['flow'], color='grey', linewidth=2, label='observed')
ax.plot(test.index, q_pred_test, color='blue', linestyle='--',
        label='simulated')
ax.set(title="Observed Flow & Simulated flow", xlabel="Date",
       ylabel="Weekly Avg Flow [cfs]")
ax.legend()


# 5. Scatter plot of t vs t-1 flow with normal axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='o',
           c=train['flow'], cmap='viridis', label='observations')
ax.set(title="Flow t -vs- Flow t-1", xlabel='flow t-1', ylabel='flow t')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), color='black',
        label='AR model')
ax.legend()


plt.show()

# %%
