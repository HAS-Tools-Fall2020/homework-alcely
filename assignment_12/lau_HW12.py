# %%
# Section 1: Import the modules we will use.
# Note: you may need to install some packages.
import xarray as xr
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

# Section 1.1: Functions


def R_Model(x, y, initial_xval):
    """ Regression Model
    ----------
    Parameters
    x & y : array, dataframe
            Training datasets.
    initial_xval: float
                  Initial x value to obtain a y prediction.
    ---------
    Returns
    pred : array
    Prediction dataset.
    """
    # Fitting AR model to training dataset
    model = LinearRegression().fit(x, y)

    # Printing model fitting parameters
    r_sq1 = model.score(x, y)
    print('Coefficient of Determination = ', np.round(r_sq1, 2))

    # Predicting flows with fitted AR Model
    pred = model.predict(initial_xval)

    # Output of this function will be printed as forecasted streamflow
    return pred

# %%
# Section 2: Variables to modify.
# USGS URL for the flow data:


site = '09506000'
start = '1989-01-01'
end = '2020-11-14'

# NetCDF file name:
filename = 'X190.33.76.250.318.19.15.42.nc'

# %%
# Section 3: Download the flow data directly from the USGS website.


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
# Section 4: Open a NetCDF file
# Read in the dataset as an x-array
data_path = os.path.join(r'..\data', filename)
ds = xr.open_dataset(data_path)

# Store the dataset temperature variable in a dataframe
# NOTE: XR requires to specify the lon and lat of one point,
# if not, creates a df with multindex.
lon = ds['air']['lon'].values[0]
lat = ds['air']['lat'].values[0]
tmp = ds['air'].sel(lat=lat, lon=lon)

tmpdf = tmp.to_dataframe()

# Aggregate air temperature values to weekly: from sunday to saturday
tmp_weekly = tmpdf.resample("W-SAT").mean()

# %%
# Section 5: Regression Model
# Some flow and temperature shift

tmp_name = ['air']
for i in range(1, 1):
    name = 'tm%s' % (i)
    tmp_weekly[name] = tmp_weekly['air'].shift(i)
    tmp_name.append(name)

flow_name = ['flow']
for i in range(1, 9):
    name = 'tm%s' % (i)
    flow_weekly[name] = flow_weekly['flow'].shift(i)
    flow_name.append(name)

# Selecting a training period
datei = '2020-08'
datef = '2020-10'
x1 = tmp_weekly[datei:datef][tmp_name].values
y_x2 = flow_weekly[datei:datef][flow_name].values


# %%
# NOTE: Run for 1 & 2 weeks
# -------------------------
ix1 = tmp_weekly[tmp_name].tail(1).values
ix2 = flow_weekly[flow_name[1:len(flow_name)]].tail(1).values
weeks = 2
factor = 1

# %%
# NOTE: Run for 16 weeks
# -------------------------
ix1 = tmp_weekly.loc[['2020-10-17']][tmp_name].values
ix2 = flow_weekly.loc[['2020-08-22']][flow_name[1:len(flow_name)]].values
weeks = 16
factor = 0.72

# %%
# Regression Model
x = np.concatenate((y_x2[:, 1:len(flow_name)], x1), axis=1)
y = y_x2[:, 0]

# For loop for making predictions for 2 or 16 weeks
week_pred = pd.DataFrame({})
j = 1
for i in range(weeks):
    initial_xval = np.concatenate((ix2, ix1), axis=1)
    pred = np.absolute(R_Model(x, y, initial_xval).round(2))
    week_pred.insert(i, 'Week %s' % (i+1), pred)
    ix2 = np.delete(ix2, -j, axis=1)
    ix2 = np.concatenate((ix2, pred.reshape(-1, 1)), axis=1)
    j += 1
    if j >= len(flow_name):
        j = len(flow_name)-1

print('Without correction factor', week_pred.T)

if weeks == 2:
    week2 = (week_pred * factor).round(2).T
    print('With correction factor', week2)

if weeks == 16:
    week16 = (week_pred * factor).round(2).T
    print('With correction factor', week16)

# %%
# Section 6: Line Plot
# Create Dataframe to plot
datei = '2020-08-22'
datef = '2020-12-12'
plot_df = pd.DataFrame({'tmp': tmp_weekly[datei:datef].reset_index().set_index(
                        np.arange(1, 14))['air'],
                        'flow': flow_weekly[datei:datef].reset_index(
                        ).set_index(np.arange(1, 14))['flow'],
                        'week16': week16.reset_index().set_index(
                        np.arange(1, 17))[0]}, index=np.arange(1, 17)).round(2)
observed_year = 2020

# Line Plot
plt.style.use('seaborn')

fig, ax1 = plt.subplots()
ax1.plot(plot_df['tmp'].T, color='blue', label=str(observed_year)+' weekly air temperature')
ax1.set(xlabel="Weeks", ylabel="Weekly Avg Temperature [o^K]")
ax1.tick_params(axis='y', labelcolor='blue')

# Second y axis
ax2 = ax1.twinx()
ax2.plot(plot_df['flow'].T, color='black',
         label=str(observed_year)+' weekly flows')
ax2.plot(plot_df['week16'].T, color='black', label='weekly predicted flows',
         linestyle="--")
ax2.set(title="Observed & Predicted Flow",
        ylabel="Weekly Avg Flow [cfs]")

ax1.legend()
ax2.legend()

fig.savefig('plot_line.png')

# %%
# Section 7: Scatter plot
# Create Dataframe to plot
datei = '2020-01'
datef = '2020-11'
scatter_df = pd.DataFrame({'tmp': tmp_weekly[datei:datef]['air'],
                           'flow': flow_weekly[datei:datef]['flow']}).round(2)

# Flow -vs- Temperature
plt.style.use('seaborn')

fig, ax = plt.subplots()
ax.set_aspect(1)
sns.regplot(x=scatter_df['flow'].values, y=scatter_df['tmp'].values,
            line_kws={"color": "r", "alpha": 0.7, "lw": 2})
ax.set(title="Observed Flow -vs- Air Temperature",
       ylabel="Weekly Avg Temperature [o^K]",
       xlabel="Weekly Avg Flow [cfs]",
       ylim=[200, 400], xlim=[0, 600])

fig.savefig("plot_scatter.png")

# %%
# Special plot for the NetCDF gallery
# Open GPM_DPR.py

# %%
