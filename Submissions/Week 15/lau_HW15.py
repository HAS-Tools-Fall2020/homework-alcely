# Section 1: Import the modules we will use.
# Note: you may need to install some packages.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import help_function as hf
import seaborn as sns

# Section 2: Modify the following variables
current_week = 15

# USGS URL for the flow data:
site = '09506000'
start = '1989-01-01'
end = '2020-12-5'

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

# Section 4: The forecast
# Step 4.1: Calculate the historical daily mean flow.

hist_flow = hf.hist_daily_mean(data, 2020)

# Step 4.2: create a dataframe to store all the variables
# related to the forecast.
# Step 4.3: aggregate the historical daily mean flow to weekly
# starting from 2020-08-23 to the following 15 weeks.
mymodel = pd.DataFrame(
    {'hist_data': hf.weekly_mean(hist_flow, 8, 29, 16),
     'data_2020': np.zeros(16)},
    index=np.arange(1, 17))

# Step 4.4: Store in the df the 2020 weekly flow
# from 2020-08-23 to the most recent value
mymodel['data_2020'] = (mymodel['data_2020'].iloc[0:current_week] +
                        flow_weekly['2020-08-29':]['flow'].values
                        ).round(2)

# Step 4.5: calculate correction factor
mymodel['factors'] = (mymodel.data_2020.values /
                      mymodel.hist_data.values
                      ).round(3)

# Step 4.6: Brain model for 16 weeks
mymodel['forecasts16'] = (mymodel['hist_data'].values *
                          mymodel['factors'][10:current_week].mean()
                          ).round(2)

# Step 4.7: Regressive model for 16 weeks
x = mymodel.iloc[7:current_week][['hist_data']].values.reshape(-1, 1)
y = mymodel.iloc[7:current_week]['data_2020'].values

lt_pred = []
for i in range(16):
    initial_xval = mymodel['hist_data'].iloc[i]
    if i < 4:
        pred = (hf.R_Model(x, y, initial_xval) * 0.6).round(2)
    else:
        pred = hf.R_Model(x, y, initial_xval).round(2)
    lt_pred.append(pred[0])

mymodel['Rmodel'] = lt_pred

# Step 4.8: print results
print('--------------------------')
print('All you need to check:')
print(mymodel)
print('--------------------------')
print('My forecast entries #', current_week)
print('week1 =', mymodel['forecasts16'][current_week+1])
print('week2 = forecast competition end')
# print('week2 =', mymodel['forecasts16'][current_week+2])
print('--------------------------')
print('16 weeks forecast:')
print(mymodel[['Rmodel']])
print('--------------------------')
print('Completed')

# %%
(mymodel['forecasts16']*0.6).values
(mymodel['Rmodel']).values
