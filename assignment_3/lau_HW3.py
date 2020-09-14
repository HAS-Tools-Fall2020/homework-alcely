# Start code for assignment 3
# this code sets up the lists you will need for your homework
# and provides some examples of operations that will be helpful to you

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week3.txt'
filedirectory = 'C:/Users/alcel/Documents/GitHub/2020FA_CodingSkills/homework-alcely/data'
filepath = os.path.join(filedirectory, filename)
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

#make lists of the data
flow = data.flow.values.tolist()
date = data.datetime.values.tolist()
year = data.year.values.tolist()
month = data.month.values.tolist()
day = data.day.values.tolist()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %% 
# Here start my HW3 code.
# Step1: Grabbing out the data from the last 3 weeks.

#the index of the first sunday from the last 3 weeks:
x = len(date) - 21

last_3weeks_date = []
last_3weeks_flow = []
week1_date = [] 
week1_flow = []
week2_date = [] 
week2_flow = []
week3_date = [] 
week3_flow = []

# %%
#Making a list to store the dates and flows from last 3 weeks.
while x < len(date):
    new_date = date[x]
    new_flow = flow[x]
    last_3weeks_date.append(new_date) #creating the list of 3 weeks
    last_3weeks_flow.append(new_flow)

    if x < len(date) -14:
        week1_date = last_3weeks_date #creating the list of week 1 of the last 3 weeks
        week1_flow = last_3weeks_flow
        
        
    elif x >= len(date) -14 and x < len(date) -7:
        week2_date.append(new_date) #creating the list of week 2 of the last 3 weeks
        week2_flow.append(new_flow)  
        
    else:
        week3_date.append(new_date) #creating the list of week 3 of the last 3 weeks
        week3_flow.append(new_flow) 
          
    x += 1

print("last_3weeks_date" ,last_3weeks_date)
print("last_3weeks_flow",last_3weeks_flow)
print("week1_date",week1_date)
print("week1_flow", week1_flow)
print("week2_date", week2_date)
print("week2_flow", week2_flow)
print("week3_date", week3_date)
print("week3_flow", week3_flow)

#%%
# Calculating some basic properites from the data of the last 3 weeks
print("Last 3 weeks' summary")
print("Min =", min(last_3weeks_flow))
print("Max =", max(last_3weeks_flow))
print("Mean =", np.mean(last_3weeks_flow))
print("Standard desviation =", np.std(last_3weeks_flow))
print("")
print("Last week' summary (week 3)")
print("Min =", min(week3_flow))
print("Max =", max(week3_flow))
print("Mean =", np.mean(week3_flow))
print("Standard desviation =", np.std(week3_flow))

# %%
# Making and empty list that I will use to store
# index values I'm interested in
ilist = []
ilist1 = []
ilist2 = []
ilist3 = []

week1_forecast = [13, 14, 15, 16, 17, 18, 19] #remember to modify every week
week2_forecast = [20, 21, 22, 23, 24, 25, 26]

# Loop over the length of the flow list
# and adding the index value to the ilist
# if it meets some criteria that I specify
for i in range(len(flow)):
        if flow[i] <= max(last_3weeks_flow) and flow[i] >= min(last_3weeks_flow) and month[i] ==9 and year[i] != 2020 and day[i] in week1_forecast: #for the next code improve using a list for month and forecast days
                ilist.append(i)

        if flow[i] <= max(last_3weeks_flow) and flow[i] >= min(last_3weeks_flow) and month[i] ==9 and year[i] != 2020 and day[i] in week2_forecast:
                ilist1.append(i)

        if month[i] ==9 and day[i] in week1_forecast and year[i] == 2011:
                ilist2.append(i)
        
        if month[i] ==9 and day[i] in week1_forecast and year[i] == 2019:
                ilist2.append(i)

        if month[i] ==9 and day[i] in week2_forecast and year[i] == 2011:
                ilist3.append(i)
        
        if month[i] ==9 and day[i] in week2_forecast and year[i] == 2019:
                ilist3.append(i)

# see how many times the criteria was met by checking the length
# of the index list that was generated
print(len(ilist))
print(len(ilist1))
print(len(ilist2))
print(len(ilist3))

# %%
# Grabbing out the data that met the criteria
# This  subset of data is just the elements identified 
# in the ilist
week1_forecast_all_years_flow = [flow[j] for j in ilist]
print(week1_forecast_all_years_flow)
print("")

week2_forecast_all_years_flow = [flow[j] for j in ilist1]
print(week2_forecast_all_years_flow)
print("")

week1_forecast_some_years_flow = [flow[j] for j in ilist2]
print(week1_forecast_some_years_flow)
print("")

week2_forecast_some_years_flow = [flow[j] for j in ilist3]
print(week2_forecast_some_years_flow)
print("")

# %%
print("week 1 forecast: Using all the years and a flow range")
print("Min =", min(week1_forecast_all_years_flow))
print("Max =", max(week1_forecast_all_years_flow))
print("Mean =", np.mean(week1_forecast_all_years_flow))
print("Standard desviation =", np.std(week1_forecast_all_years_flow))
print("")
print("week 1 forecast: Using some similar years to the current year")
print("Min =", min(week1_forecast_some_years_flow))
print("Max =", max(week1_forecast_some_years_flow))
print("Mean =", np.mean(week1_forecast_some_years_flow))
print("Standard desviation =", np.std(week1_forecast_some_years_flow))
print("")
print("week 2 forecast: Using all the years and a flow range")
print("Min =", min(week2_forecast_all_years_flow))
print("Max =", max(week2_forecast_all_years_flow))
print("Mean =", np.mean(week2_forecast_all_years_flow))
print("Standard desviation =", np.std(week2_forecast_all_years_flow))
print("")
print("week 2 forecast: Using some similar years to the current year")
print("Min =", min(week2_forecast_some_years_flow))
print("Max =", max(week2_forecast_some_years_flow))
print("Mean =", np.mean(week2_forecast_some_years_flow))
print("Standard desviation =", np.std(week2_forecast_some_years_flow))

# %%
#Assignment questions

#question 1
y = [flow, year, month, day]

for i in range(len(y)):
    print(type(y[i]))
    print(type(y[i][i]))
    print(len(y[i]))

# %%
#question 2, 3 & 4
my_forecast_week1 = 67

ilist5 = []
ilist6 = []
ilist7 = []
ilist8 = []
ilist9 = []

for i in range(len(flow)):
        if  month[i] ==9 and flow[i] > my_forecast_week1: #question 2
            ilist5.append(i)

        if  month[i] ==9 and year[i] <= 2000 and flow[i] > my_forecast_week1: #question 3
            ilist6.append(i)

        if  month[i] ==9 and year[i] >= 2010 and flow[i] > my_forecast_week1:
            ilist7.append(i)

        if  month[i] ==9 and day[i] <= 15: #question 4
            ilist8.append(i)

        if month[i] ==9 and day[i] >= 16 and day[i] <= 30:
            ilist9.append(i)

print("Times that the daily flow is greater than my week 1 forecast =",len(ilist5))
print("")
per = 100 * (len(ilist5) / len(flow))
print("Times in percentage that the daily flow is greater than my week 1 forecast =", per, "%")

# %%
#continue with question 3
per1 = 100 * (len(ilist6) / len(flow))
print("in or before 2000, the number of times that the daily flow is greater than my week 1 forecast =", len(ilist6), " and in percentage =", per1, "%")
print("")

per2 = 100 * (len(ilist7) / len(flow))
print("in or after 2010, the number of times that the daily flow is greater than my week 1 forecast =", len(ilist7), " and in percentage =", per2, "%")
print("")


# %%
#continue with question 4
half1_flow = [flow[j] for j in ilist8]
half2_flow = [flow[j] for j in ilist9]

# %%
print("Summary of the first half of September")
print("Min =", min(half1_flow))
print("Max =", max(half1_flow))
print("Mean =", np.mean(half1_flow))
print("Standard desviation =", np.std(half1_flow))
print("")
print("Summary of the second half of September")
print("Min =", min(half2_flow))
print("Max =", max(half2_flow))
print("Mean =", np.mean(half2_flow))
print("Standard desviation =", np.std(half2_flow))

# %%
