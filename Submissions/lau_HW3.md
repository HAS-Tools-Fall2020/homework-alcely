## Assignment 3: Forecast week 3
**Name: Alcely Lau**

**Date: 09/13/2020**

#### Assignment summary

This year **2020** the streamflow behavior of Verde River has broken record. It established a new weekly average streamflow minimum. I would not recommend to use only the historical streamflow data for a forecast. However, that is what we have, for now. So, I did an educated guess playing with python.

For this week I followed the next steps:

1. Download the stream gauge observations from the USGS NWIS website, [mapper](https://maps.waterdata.usgs.gov/mapper/).

2. Explore the data by coding in Python. First, taking a look at the streamflow values of the last 3 weeks. Then, into the historical data at the month of September, looking to the streamflow inside the streamflow range of the last 3 weeks. In addition, checking the statistics properties of the streamflow data, for the same forecast dates, of the years **2011** and **2019**.

#### Assignment questions

1. Describe the variables `flow`, `year`, `month`, and `day`. What type of objects are they, what are they composed of, and how long are they?
| Variable | Type |  composed of |  length |
| ------------- |-------------| -------------| -------------|
| flow      | List | float | 11578
| year     | List     |  integer |11578
| month | List     |   integer |11578
| day | List     |   integer|11578

2. How many times was the daily flow greater than your prediction in the month of September (express your answer in terms of the total number of times and as a percentage)?

  **Times that the daily flow is greater than my week 1 forecast = 870,  in percentage = 7.51%**
3. How would your answer to the previous question change if you considered only daily flows in or before 2000? Same question for the flows in or after the year 2010? (again report total number of times and percentage)
| years | number of time |  percentage |
| ------------- |-------------:| -------------:|
| <= 2000      | 356 | 3.07% |
|>= 2010    | 273     |  2.36% |
4. How does the daily flow generally change from the first half of September to the second?

  **Summary of the first half of September: Min = 36.6
, Max = 1280.0
, Mean = 178.8383647798742
, Standard desviation = 171.2679315493717**

  **Summary of the second half of September
: Min = 51.2
, Max = 5590.0
, Mean = 169.8541935483871
, Standard desviation = 371.9750870786179**
