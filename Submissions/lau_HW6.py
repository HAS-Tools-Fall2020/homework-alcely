# Starter code for week 6 illustrating how to build an AR model 
# and plot it

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
#note you may need to do pip install for sklearn

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week6.txt'
filepath = os.path.join('C:/Users/alcel/Documents/GitHub/2020FA_CodingSkills/homework-alcely/data', filename)
print(os.getcwd())
print(filepath)


# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code'],
        parse_dates=['datetime']
        )

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).dayofweek
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# %%
# Aggregate flow values to weekly: from sunday to saturday
flow_weekly = data.resample("W-SAT", on='datetime').mean()


# %%
# Here start my forecast6 code.
# Step1: Check the data from the last 3 weeks.
last3week = flow_weekly.tail(3)
last3week

# %%
# Building an autoregressive model 
# You can learn more about the approach I'm following by walking 
# Through this tutorial
# https://realpython.com/linear-regression-in-python/

# Step 1: setup the arrays you will build your model on
# This is an autoregressive model so we will be building
# it based on the lagged timeseries

flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)
flow_weekly['flow_tm2'] = flow_weekly['flow'].shift(2)

# %%
# Step 2 - pick what portion of the time series you want to use as training data
# here I'm grabbing the first 800 weeks 
# Note1 - dropping the first two weeks since they wont have lagged data
# to go with them  
#train = flow_weekly[2:800][['flow', 'flow_tm1', 'flow_tm2']]
#test = flow_weekly[800:][['flow', 'flow_tm1', 'flow_tm2']]

# modify the following variables:
yrs = 2011        #Insert start year to consider in the model
yre = 2018        #Insert end year to consider in the model
mvf = 100        #Maximun value flow to consider in the model

train = flow_weekly[(flow_weekly['year'] >= yrs) & (flow_weekly['year'] <= yre) \
        & (flow_weekly['flow'] <= mvf)][['flow', 'flow_tm1', 'flow_tm2']]
test = flow_weekly[(flow_weekly['year']  > yre) \
        & (flow_weekly['flow'] <= mvf)][['flow', 'flow_tm1', 'flow_tm2']]

# Step 3: Fit a linear regression model using sklearn 
model = LinearRegression()
x=train['flow_tm1'].values.reshape(-1,1) #See the tutorial to understand the reshape step here 
y=train['flow'].values
model.fit(x,y)

#Look at the results
# r^2 values
r_sq = model.score(x, y)
print('coefficient of determination:', np.round(r_sq,2))

#print the intercept and the slope 
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))

# %%
# Step 4 Make a prediction with your model 
# Predict the model response for a  given flow value
q_pred_train = model.predict(train['flow_tm1'].values.reshape(-1,1))
q_pred_test = model.predict(test['flow_tm1'].values.reshape(-1,1))

# %% Option 1: for a single week forecast
# Calculate the prediction bias

pred_bias = q_pred_test - flow_weekly[(flow_weekly['year'] > yre)]['flow']
print("Prediction bias:", pred_bias.tail())

# predict the q for just a single value like this (plus the prediction bias)
#last_week_flow = 500

last_week_flow = flow_weekly['flow'][-1]
prediction1 = model.intercept_ + model.coef_ * last_week_flow
print("autoregressive forecast:", prediction1)

prediction2 = model.intercept_ + model.coef_ * last_week_flow - pred_bias.tail(2).mean()
print("autoregressive forecast adjusted with the bias:", prediction2)

# %% Option 2: for multiples week forecasts
# Alcely: I don't recommend use it for more than 4 weeks.

for_flow = flow_weekly['flow'][-1]
print("initial flow:", for_flow)
number_weeks = 4
i = 0

while i < number_weeks:
        last_week_flow = for_flow
        prediction1 = model.intercept_ + model.coef_ * last_week_flow
        print("autoregressive forecast ", i,": ", prediction1)

        for_flow = prediction1

        i += 1


# %% 
# Here are some examples of things you might want to plot to get you started:
plt.style.use('seaborn')

# 1. Timeseries of observed flow values
# Note that date is the index for the dataframe so it will 
# automatically treat this as our x axis unless we tell it otherwise
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], color='gray', linewidth=1, label='full')
ax.plot(train['flow'], 'r:', label='training')
ax.plot(test['flow'], '--b', label='testing')
ax.set(title="Observed Flow", xlabel="Date", 
        ylabel="Weekly Avg Flow [cfs]",
        yscale='log')
ax.legend()

# an example of saving your figure to a file
fig.savefig("Observed_Flow_full.png")

#2. Time series of flow values with the x axis range limited
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], color='gray', linewidth=1, label='full')
ax.plot(train['flow'], 'r', label='training')
ax.plot(test['flow'], 'b', label='testing')
ax.set(title="Observed Flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        yscale='log', xlim=[datetime.date(2011, 1, 1), datetime.date(2020, 10, 4)])
ax.legend()

fig.savefig("Observed_Flow_period.png")


# 3. Line  plot comparison of predicted and observed flows
fig, ax = plt.subplots()
ax.plot(train['flow'], color='grey', linewidth=2, label='observed')
ax.plot(train.index, q_pred_train, color='red', linestyle='--', 
        label='simulated')
ax.set(title="Observed Flow & Simulated flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]")
ax.legend()

fig.savefig("Obs_Pred_Flow_train_period.png")

# 4. Line  plot comparison of predicted and observed flows
fig, ax = plt.subplots()
ax.plot(test['flow'], color='grey', linewidth=2, label='observed')
ax.plot(test.index, q_pred_test, color='blue', linestyle='--', 
        label='simulated')
ax.set(title="Observed Flow & Simulated flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]")
ax.legend()

fig.savefig("Obs_Pred_Flow_test_period.png")

# 5. Scatter plot of t vs t-1 flow with normal axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='o',
              c=train['flow'], cmap='viridis', label='observations')
ax.set(title="Flow t -vs- Flow t-1", xlabel='flow t-1', ylabel='flow t')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), color='black', label='AR model')
ax.legend()

fig.savefig("flowt_flowtm1.png")

plt.show()


# %%
#Alcely: I didn't use
# 4. Scatter plot of t vs t-1 flow with log log axes
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='p',
              color='blueviolet', label='obs')
ax.set(xlabel='flow t-1', ylabel='flow t', yscale='log', xscale='log')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model')
ax.legend()