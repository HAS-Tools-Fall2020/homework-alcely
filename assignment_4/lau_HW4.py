# Starter code for Homework 4

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week4.txt'
filepath = os.path.join('C:/Users/alcel/Documents/GitHub/2020FA_CodingSkills/homework-alcely/data', filename)
print(os.getcwd())
print(filepath)

# %%
# DON'T change this part -- this creates the lists you 
# should use for the rest of the assignment
# no need to worry about how this is being done now we will cover
# this in later sections. 

#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# Make a numpy array of this data
flow_data = data[['year', 'month','day', 'flow']].to_numpy()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%
# Assignment 4 question2:

print("The variable `flow_data` is", type(flow_data), \
        ". It is composed of floats (in a numpy array must be the same data type).", \
                "It has", flow_data.ndim, "dimensions and its total size is:", \
                flow_data.shape, ", where (rows, columns).")

# %% Checking that the data have the same type in each column.
type(flow_data[0,0])
type(flow_data[0,1])
type(flow_data[0,2])
type(flow_data[0,3])

# %%
# Assignment 4 question3:
# Number of times my forecast is greater than the daily flow in September
weeks_text = ["week 1", "week 2", "week 3", "average"]
forecast = [65, 67, 54.05, 62.02] # Insert forecast

print("| September | Forecast value (cfs) | Number of times | Percentage |")

# Count the number of values with daily flow > forecast and month ==9
for i in range(len(forecast)):
        times_count = np.sum((flow_data[:,3] > forecast[i]) & (flow_data[:,1]==9))
        sept_days = np.sum(flow_data[:,1]==9)

        # In percetange:
        per = 100 * (times_count / sept_days)

        print("|", weeks_text[i], "|", forecast[i], "|", \
                times_count, "|", per, "% |")

# %%
# Assignment 4 question4: 
print("| Years  | September | Forecast value (cfs) | Number of times | Percentage |")

# Count the number of values with daily flow > forecast and month ==9 
# and years are <=2000
for i in range(len(forecast)):
        times_count = np.sum((flow_data[:,3] > forecast[i]) & (flow_data[:,1]==9) \
                & (flow_data[:,0] <= 2000))
        sept_days = np.sum(flow_data[:,1]==9)

        # In percetange:
        per = 100 * (times_count / sept_days)
        
        print("|<= 2000|", weeks_text[i], "|", forecast[i], "|", \
                times_count, "|", per, "% |")

# Count the number of values with daily flow > forecast and month ==9 
# and years are >=2010
for i in range(len(forecast)):
        times_count = np.sum((flow_data[:,3] > forecast[i]) & (flow_data[:,1]==9) \
                & (flow_data[:,0] >=2010))
        sept_days = np.sum(flow_data[:,1]==9)

        # In percetange:
        per = 100 * (times_count / sept_days)

        print("|>= 2010|", weeks_text[i], "|", forecast[i], "|", \
                times_count, "|", per, "% |")

# %%
# Assignment 4 question5:

half1 = np.mean(flow_data[(flow_data[:,1]==9) & (flow_data[:,2] <= 15), 3])
half2 = np.mean(flow_data[(flow_data[:,1]==9) & (flow_data[:,2] > 15), 3])

print("The average daily flows on the first half of September is:", half1, \
        "cfs , in contrast, on the second half of September is:", half2, "cfs.")

# %% 
# Here start my HW4 code.
# Step1: Grabbing out the data from the last 3 weeks.

flow_last3week = np.array(flow_data[-21:,:])
flow_last2week = np.array(flow_data[-14:,:])
flow_last1week = np.array(flow_data[-7:,:])

#%%
# Step2: Calculating some basic properites from the data of the last 3 weeks

flow_last3week_min = np.min(flow_last3week[:,3])
flow_last3week_max = np.max(flow_last3week[:,3])
flow_last3week_mean = np.mean(flow_last3week[:,3])
flow_last3week_std = np.std(flow_last3week[:,3])

flow_last2week_min = np.min(flow_last2week[:,3])
flow_last2week_max = np.max(flow_last2week[:,3])
flow_last2week_mean = np.mean(flow_last2week[:,3])
flow_last2week_std = np.std(flow_last2week[:,3])

flow_last1week_min = np.min(flow_last1week[:,3])
flow_last1week_max = np.max(flow_last1week[:,3])
flow_last1week_mean = np.mean(flow_last1week[:,3])
flow_last1week_std = np.std(flow_last1week[:,3])

# %%
# Summary of the last 3 weeks streamflows
print("The flows from the last 3 weeks")
print(flow_last3week)
print("")
print("The flows from the last 2 weeks")
print(flow_last2week)
print("")
print("The flows from the last week")
print(flow_last1week)
print("")

print("Last 3 weeks summary:")
print("min:", flow_last3week_min)
print("max:", flow_last3week_max)
print("mean:", flow_last3week_mean)
print("std:", flow_last3week_std)
print("")

print("Last 2 weeks summary:")
print("min:", flow_last2week_min)
print("max:", flow_last2week_max)
print("mean:", flow_last2week_mean)
print("std:", flow_last2week_std)
print("")

print("Last 1 week summary:")
print("min:", flow_last1week_min)
print("max:", flow_last1week_max)
print("mean:", flow_last1week_mean)
print("std:", flow_last1week_std)
print("")

# %%
#Step4: historical data analysis.
# modify the following variables:
m = 9           #Insert month
fd = 13         #Insert first day of the week
ed= 26          #Insert end day of the week
y = 2019        #Insert year

# historical mean, without the year 2020.
flow_mean1 = np.mean(flow_data[(flow_data[:,0] != 2020) & \
        (flow_data[:,1] == m) & (flow_data[:,2] >= fd) & (flow_data[:,2] <= ed),3])

# mean since the year 2009 (the last 10 years), without the year 2020.
flow_mean2 = np.mean(flow_data[(flow_data[:,0] != 2020) & (flow_data[:,0] >= 2009) &\
         (flow_data[:,1] == m) & (flow_data[:,2] >= fd) & (flow_data[:,2] <= ed),3])

# mean for a specific year.
flow_mean3 = np.mean(flow_data[(flow_data[:,0] == y) & (flow_data[:,1] == m) &\
         (flow_data[:,2] >= fd) & (flow_data[:,2] <= ed),3])

print("Using all the historical data, without the year 2020, for the month =", m, \
        ", during the week between days", fd, "and", ed, "the mean flow is =", flow_mean1)
print("")
print("Using the last 10 years data, without the year 2020, for the month =", m, \
        ", during the week between days", fd, "and", ed, "the mean flow is =", flow_mean2)
print("")
print("In the year", y, "for the month =", m, ", during the week between days", \
        fd, "and", ed, "the mean flow is =", flow_mean3)
print("")

# %%
# Quantiles
# historical quantiles, without the year 2020.
flow_quants1 = np.quantile(flow_data[(flow_data[:,0] != 2020) & \
        (flow_data[:,1] == m) & (flow_data[:,2] >= fd) & (flow_data[:,2] <= ed),3],\
                 q=[0,0.33,0.5,0.66,1.0])

# Quantiles since the year 2009 (the last 10 years), without the year 2020.
flow_quants2 = np.quantile(flow_data[(flow_data[:,0] != 2020) & (flow_data[:,0] >= 2009) &\
         (flow_data[:,1] == m) & (flow_data[:,2] >= fd) & (flow_data[:,2] <= ed),3],\
                  q=[0,0.33,0.5,0.66,1.0])

# Quantiles for a specific year.
flow_quants3 = np.quantile(flow_data[(flow_data[:,0] == y) & (flow_data[:,1] == m) &\
         (flow_data[:,2] >= fd) & (flow_data[:,2] <= ed),3], q=[0,0.33,0.5,0.66,1.0])

print("All years, month =", m, "week between days:", fd, "and", ed)
print("min, 33%, median, 66%, max")
print(flow_quants1)
print("")
print("Last 10 years, month =", m, "week between days:", fd, "and", ed)
print("min, 33%, median, 66%, max")
print(flow_quants2)
print("")
print("year =", y, "month =", m, "week between days:", fd, "and", ed)
print("min, 33%, median, 66%, max")
print(flow_quants3)
print("")

# %%
#using all years, without year 2020, and a specific month
flow_slice1 = np.array(flow_data[(flow_data[:,0] != 2020) & (flow_data[:,1] == m) ,3])

mybins1 = np.linspace(0, 200, num=10) 
#Plotting the histogram
plt.hist(flow_slice1, bins = mybins1)
plt.title('Historical Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')


# %%
#using an specific year and month
flow_slice2 = np.array(flow_data[(flow_data[:,0] == y) & (flow_data[:,1] == m) ,3])

mybins2 = np.linspace(0, np.max(flow_slice2), num=5) 
#Plotting the histogram
plt.hist(flow_slice2, bins = mybins2)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

# %%
#using all years, without year 2020, and a specific month
flow_slice3 = np.array(flow_data[(flow_data[:,0] != 2020) & (flow_data[:,1] == m) & (flow_data[:,2] >= fd) & (flow_data[:,2] <= ed),3])

mybins3 = np.linspace(0, 200, num=10) 
#Plotting the histogram
plt.hist(flow_slice3, bins = mybins3)
plt.title('Historical Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

# %%