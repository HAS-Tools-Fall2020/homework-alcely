# Example solution for HW 4

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week5.txt'
filepath = os.path.join('C:/Users/alcel/Documents/GitHub/2020FA_CodingSkills/homework-alcely/data', filename)
print(os.getcwd())
print(filepath)


# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# Hints - you will need the functions: describe, info, groupby, sort, head and tail.
# %%
# Assignment 5, question 1: Provide a summary of the data frames properties.
data.info()

# %%
# Assignment 5, question 2:Provide a summary of the flow column including the 
# min, mean, max, standard deviation and quartiles.
summary_data = data[["flow"]].describe()

# %%
print(summary_data.to_markdown())

# %%
# Assignment 5, question 3: Provide the same information but on a monthly basis.

flow_months = data.groupby(["month"])[["flow"]].describe().round(3)

# %%
# formatting to markdown
print(flow_months.to_markdown())

# %%
# Assignment 5, question 4: Provide a table with the 5 highest and 5 lowest flow values 
# for the period of record. Include the date, month and flow values in your summary.

max_min_flow = data.sort_values(by="flow", ascending=False)

max_flow = max_min_flow[["datetime", "month", "flow"]].head()
max_flow

# %%
min_flow = max_min_flow[["datetime", "month", "flow"]].tail()
min_flow

# %%
# formatting to markdown
print("The 5 highest historical flows")
print(max_flow.to_markdown())
print("")
print("The 5 lowest historical flows")
print(min_flow.to_markdown())

# %%
# Assignment 5, question 5:Find the highest and lowest flow values for every month of the 
# year (i.e. you will find 12 maxes and 12 mins) and report back what year these 
# occurred in.
min5 = data.groupby(["month"])[["flow"]].idxmin()
min5

# %%
max5 = data.groupby(["month"])[["flow"]].idxmax()
max5

# %%
# formatting to markdown
print("| Year|", "  Min|", " Year|", "  Max|")
print("|:---:|:----:|:----:|:----:|")
for i in range(len(min5)):
        print("| ", data.loc[min5.iloc[i,0],"year"], "| ", 
        data.loc[min5.iloc[i,0],"flow"],"| ", data.loc[max5.iloc[i,0],"year"], 
        "| ", data.loc[max5.iloc[i,0],"flow"], "|")
        
# %%
# Assignment 5, question 6:Provide a list of historical dates with flows that are within
# 10% of your week 1 forecast value.

#modify
forecast = 61.31 

quest6 = data[(data["flow"] >= forecast * 0.90) & (data["flow"] <= forecast * 1.10)][["datetime","flow"]]
quest6
# %%
quest6head = quest6.head()
quest6tail = quest6.tail()

# formatting to markdown
print("The 5 first dates with flows that are within 10'%' of my week 1 forecast value.")
print("")
print(quest6head.to_markdown())
print("")
print("The 5 last dates with flows that are within 10'%' of my week 1 forecast value.")
print("")
print(quest6tail.to_markdown())

# %%
# Here start my forecast5 code.
# Step1: Grabbing out the data from the last 3 weeks.
last3week = data[["datetime","year", "month", "day","flow"]].tail(21)
last3week
# %%
last2week = data[["datetime","year", "month", "day","flow"]].tail(14)
last2week
# %%
last1week = data[["datetime","year", "month", "day","flow"]].tail(7)
last1week

# %%
# Step2: Calculating some basic properites from the data of the last 3 weeks
stats_last3week = last3week[["flow"]].describe()
stats_last3week
# %%
stats_last2week = last2week[["flow"]].describe()
stats_last2week
# %%
stats_last1week = last1week[["flow"]].describe()
stats_last1week

# %%
#Step4: historical data analysis.
# modify the following variables:
m = 9          #Insert month
fd = 20         #Insert first day of the week / or 2 last weeks
ed= 30          #Insert end day of the week / or 2 last weeks
y = 2019        #Insert year

# %%
# using all the years, without the year 2020.
stats_all_years = data[(data["year"] != 2020) & (data["month"] == m) & \
        (data["day"] >= fd) & (data["day"] <= ed)][["flow"]].describe(percentiles=[.33, .5, .66])

print("Using all years and the conditions: month =", m, "week between days", fd, "and", ed)
stats_all_years
# %%
# using the last 10 years, without the year 2020.
stats_10_years = data[(data["year"] >= 2009) & (data["year"] != 2020) & (data["month"] == m) & \
        (data["day"] >= fd) & (data["day"] <= ed)][["flow"]].describe(percentiles=[.33, .5, .66])

print("Using the last 10 years and the conditions: month =", m, "week between days", fd, "and", ed)
stats_10_years
# %%
#using an specific year for the days of the last 2 weeks.
stats_y_year = data[(data["year"] == y) & (data["month"] == m) & \
        (data["day"] >= fd) & (data["day"] <= ed)][["flow"]].describe(percentiles=[.33, .5, .66])

print("Using an specific year =", y, "and the conditions: month =", m, "week between days", fd, "and", ed)
stats_y_year

# %%
plotx = data[(data["year"] == y) & (data["month"] == m) & \
        (data["day"] >= fd) & (data["day"] <= ed)]["day"]

ploty = data[(data["year"] == y) & (data["month"] == m) & \
        (data["day"] >= fd) & (data["day"] <= ed)]["flow"]
# %%
# Plot the data
f, ax = plt.subplots()

ax.plot(plotx,
        ploty,
        color="blue")

ax.plot(last2week["day"],
        last2week["flow"],
        color="red")

ax.set(title="Flows in river verde")
plt.show()
# %%
